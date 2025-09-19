import random

#s fetch [start, end] bits from num
def fetch(num, start, end):
    shift_left = (1 << (end - start + 1)) - 1
    return (num >> start) & shift_left

# pass in offs like [[], [], []], works similar to cat() in chisel
def concat(num, offs):
    ret = 0
    for off in offs:
        start = off[0]
        if len(off) == 1:
            end = off[0]
        elif len(off) == 2:
            end = off[1]
        move = end -start + 1
        ret <<= move
        mid = fetch(num, start, end)
        ret += mid
    return ret

def get_cfi_type(instr):
    op = fetch(instr, 0, 1)
    if op == 3: # RVI
        funct = fetch(instr, 0, 6)
        if funct == 99: # branch
            return 1

        if funct == 111: # jal
            return 2

        if funct == 103: # maybe jalr
            mids = fetch(instr, 12, 14)
            if mids == 0:
                return 3
        return 0
    else: # RVC
        funct = fetch(instr, 13, 15)
        if (funct == 6 or funct == 7) and op == 1:# c.beqz c.bnez
            return 1
        
        if funct == 5 and op == 1: # c.j
            return 2
        
        if funct == 4 and op == 2:
            rs2 = fetch(instr, 2, 6)
            rs1 = fetch(instr, 7, 11)
            if rs2 == 0 and rs1 != 0: # c.jalr
                return 3
            
            if rs2 == 0 and rs1 == 0: # c.ebreak
                return 0
        return 0
    

def if_call(instr, cfi):
    if cfi < 2 or cfi > 3:
        return False
    
    op = fetch(instr, 0, 1)
    if cfi == 2:
        if op == 3:
            rd = fetch(instr, 7, 11)
            if rd == 1 or rd == 5:
                return True
        return False
    
    # cfi == 3
    if op == 2:
        return fetch(instr, 12, 12) == 1
    elif op < 2 or op > 3:
        return False 
    
    rd = fetch(instr, 7, 11)
    return rd == 1 or rd == 5
    
def if_ret(instr, cfi):
    if cfi != 3:
        return False
    
    op = fetch(instr, 0, 1)
    if op == 3: # rvi
        rd = fetch(instr, 7, 11)
        rs = fetch(instr, 15, 19)
        return rd != 1 and rd !=5 and (rs == 1 or rs ==5)
    
    if op != 2:
        return False
    
    if fetch(instr, 12, 12) == 1:
        return False
    
    rs = fetch(instr, 7, 11)

    return rs == 1 or rs == 5


def construct_brs(rvc):
    if rvc:
        return (3 << 14 ) | (random.randint(0, 1) << 13) | (random.randint(0, (1 << 11) - 1) << 2) | 1
    else:
        return (random.randint(0, (1 << 25)-1 ) << 7) | 99

def construct_jal(rvc):
    if rvc:
        return (5 << 13) | (random.randint(0, (1 << 11) - 1 ) << 2) | 1
    
    return (random.randint(0, (1 << 25) -1 )  << 7) |  111

def construct_jalr(rvc):
    if rvc:
        rvc_jalr = (4 << 13) | (random.randint(0, 63) << 7) | 2
        return  rvc_jalr

    return (random.randint(0, (1 << 17) - 1) << 15) | (random.randint(0, 31) << 7) | 103

def construct_non_cfis(rvc=False, rvc_enabled=False):
    while True:
        if (rvc_enabled):
            if rvc:
                instr = (random.randint(0, (1 << 14) - 1) << 2) | random.randint(0, 2)
            else:
                instr = (random.randint(0, (1 << 14) - 1) << 2) | 3
        else:
            instr = random.randint(0, (1 << 32) - 1)
        if get_cfi_type(instr) == 0:
            return instr

def construct_instrs(instr_type, rvc=False, rvc_enabled=False):
    if (instr_type == 0): return construct_non_cfis(rvc, rvc_enabled)
    if (instr_type == 1): return construct_brs(rvc)
    if (instr_type == 2): return construct_jal(rvc)
    return construct_jalr(rvc)