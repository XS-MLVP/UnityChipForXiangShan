from .commons import PREDICT_WIDTH, randbool, calc_cut_ptr
from random import randint

#s fetch [start, end] bits from num
def fetch(num, start, end):
    shift_left = (1 << (end - start + 1)) - 1
    return (num >> start) & shift_left

# pass in offs like [[], [], []], works similar to cat() in chisel
# 靠前的off在高位
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


def construct_brs(rvc, imm = -1):
    if rvc:
        if imm == -1:
            return (3 << 14 ) | (randint(0, 1) << 13) | (randint(0, (1 << 11) - 1) << 2) | 1
        replay1 = concat(imm, [[8], [3, 4]])
        replay2 = concat(imm, [[6, 7], [1,2], [5]])
        return (randint(6, 7) << 13) | (replay1 << 10) | (randint(0, 7) << 7)|(replay2 << 2 )| 1
    else:
        opcode = 0b1100011
        if imm == -1:
            return (randint(0, (1 << 25)-1 ) << 7) | opcode
        imm_hi = concat(imm, [[12], [5, 10]])   # 1 + 6 = 7 bits
        # 低位域 [11:7]  <- imm[4:1|11]
        imm_lo = concat(imm, [[1, 4], [11]])    # 4 + 1 = 5 bits

        funct3 = 0b000
        opcode = 0b1100011

        return (imm_hi << 25) \
            | (randint(0, 31) << 20) \
            | (randint(0, 31) << 15) \
            | (funct3 << 12) \
            | (imm_lo << 7) \
            | opcode

def construct_jal(rvc, imm=-1):
    if rvc:
        if imm == -1:
            return (5 << 13) | (randint(0, (1 << 11) - 1 ) << 2) | 1
        replay = concat(imm, [[11], [4], [8, 9], [10], [6], [7], [1, 3], [5]])
        return (5 << 13) | (replay << 2 ) | 1
    opcode = 0b1101111
    if imm == -1:
        return (randint(0, (1 << 25) -1 )  << 7) |  opcode
    replay = concat(imm, [[20], [1, 10], [11], [12, 19]])
    instr = (imm << 12) | (randint(0, 31) << 7) | opcode
    return instr

def construct_jalr(rvc):
    if rvc:
        rvc_jalr = (4 << 13) | (randint(0, 63) << 7) | 2
        return  rvc_jalr

    return (randint(0, (1 << 17) - 1) << 15) | (randint(0, 31) << 7) | 103

def construct_ret(rvc):
    rs = 1 if randbool() else 5
    if rvc:
        return (8 << 12) | rs << 7 | 2
    rd = 3
    return (randint(0, (1 << 12) - 1) << 20) | ( rs<< 15)| (rd << 7) | 103
    

def construct_non_cfis(rvc=False, rvc_enabled=False):
    while True:
        if (rvc_enabled):
            if rvc:
                instr = (randint(0, (1 << 14) - 1) << 2) | randint(0, 2)
            else:
                instr = (randint(0, (1 << 14) - 1) << 2) | 3
        else:
            instr = randint(0, (1 << 32) - 1)
        if get_cfi_type(instr) == 0:
            return instr

def construct_instrs(instr_type, rvc=False, rvc_enabled=False, target_imm = -1):
    if (instr_type == 0): return construct_non_cfis(rvc, rvc_enabled)
    if (instr_type == 1): return construct_brs(rvc, imm=target_imm)
    if (instr_type == 2): return construct_jal(rvc, imm=target_imm)
    return construct_jalr(rvc)

def is_rvc(concate_instr):
    return (concate_instr & 3) != 3

def construct_instrs_with_jump_idx(jmp_idx, cfi_res=-1, imm=-1):
    instrs = [ 0 for _ in range(17)]
    seq_end_idx = min(jmp_idx, PREDICT_WIDTH)
    for i in range(max(0, seq_end_idx)):
        if i < seq_end_idx - 2:
            is_rvc = randbool()
        elif i == seq_end_idx - 2:
            is_rvc = False
        else:
            is_rvc = True
        res = construct_non_cfis(rvc=is_rvc, rvc_enabled=True)
        instrs[i] = res & ((1 << 16) - 1)
        if not is_rvc:
            i += 1
            instrs[i] =(res >> 16) & ((1 << 16)-1)

    for i in range(jmp_idx, PREDICT_WIDTH+1):
        # default not cross block
        if i == jmp_idx:
            cfi_type = randint(1, 3) if cfi_res == -1 else cfi_res
            cur_imm = imm
        else:
            cfi_type = randint(0, 3)
            cur_imm = -1
        
        # if i == PREDICT_WIDTH:
        #     is_rvc = True
        # elif i == PREDICT_WIDTH-1:
        #     is_rvc = False
        # else:
        is_rvc = randbool()
        res = construct_instrs(cfi_type, rvc=is_rvc, rvc_enabled=True, target_imm=cur_imm) if 0 <= cfi_type < 4 else construct_ret(rvc=is_rvc)
        instrs[i] = res & ((1 << 16) - 1)
        if not is_rvc:
            i += 1
            if i < PREDICT_WIDTH:
                instrs[i] =(res >> 16) & ((1 << 16)-1)
    return instrs

# def rebuild_cacheline_from_parts(next_start, instrs):
#     """
#     用给定的 idx 列表和对应的 16bit 指令值，重建一个 1024bit 缓存行；
#     未提供的槽位用 0 填充。
#     """
#     cut_ptrs = calc_cut_ptr(next_start)
#     assert len(cut_ptrs) == len(instrs)
#     cacheline = 0
#     for idx, instr in zip(cut_ptrs, instrs):
#         assert 0 <= idx < 64
#         assert 0 <= instr <= 0xFFFF
#         pos = idx * 16
#         cacheline |= (instr & 0xFFFF) << pos
#     print(len(cut_ptrs))
#     print(f"res: {hex(cacheline)}")
#     low = cacheline & ((1 << 512) - 1)
#     high = (cacheline >> 512) & ((1 << 512) - 1)
#     res = low | high
#     print(f"cacheline: {hex(res)}")
#     return res 

SLOT_BITS=16
PERIOD_SLOTS=32

def rebuild_cacheline_from_parts(start_addr, instrs: list[int]) -> int:
    cut_ptrs: list[int] = calc_cut_ptr(start_addr)
    """
    逆向 Cat(512b, 512b)+cut：把 (idx, 16-bit) 写回到一个 512b cacheline（32槽）中。
    规则：slot = idx % 32；重复命中时后写覆盖（可换策略）。
    返回：单条 512-bit cacheline 的整数表示。
    """
    assert len(cut_ptrs) == len(instrs)
    line = 0
    # 先清空被写入过的位置（可选，但安全）
    written_mask = 0
    for idx, ins in zip(cut_ptrs, instrs):
        assert 0 <= ins <= 0xFFFF
        j = idx % PERIOD_SLOTS
        pos = j * SLOT_BITS
        # 清空该槽位
        line &= ~((0xFFFF) << pos)
        # 写入该槽位
        line |= (ins & 0xFFFF) << pos
        written_mask |= 1 << j
    # print(f"cacheline_place_instrs: {hex(line)}")
    return line

