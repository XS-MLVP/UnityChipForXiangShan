import random

class PreDecodeInstrGen():
    def __init__(self):
        self.instrs = []
        self.new_instrs = []
        self.jmp_offsets = []
        self.rvcs = []
        self.valid_starts = []
        self.half_valid_starts = []
        
        self.isRets = []
        self.isCalls = []
        self.brTypes = []
        
    def clear(self):
        self.instrs = []
        self.new_instrs = []
        self.jmp_offsets = []
        self.rvcs = []
        self.valid_starts = []
        self.half_valid_starts = []
        
        self.isRets = []
        self.isCalls = []
        self.brTypes = []
        
    def random_instrs(self):
        #genetare random instructions
        self.instrs = [random.getrandbits(16) for _ in range(17)]
        self.new_instrs = [self.instrs[i+1] << 16 | self.instrs[i] for i in range(16)]
        return self.instrs, self.new_instrs
    def instr_gen(self, type='random', isa='rvi'):
        if type == 'random':
            instr_rvi = random.getrandbits(32) | 0b11
            instr_rvc = random.getrandbits(14) << 2 | random.choice([0b00,0b01,0b10])
            return instr_rvi if isa == 'rvi' else instr_rvc
        if type == 'j':
            opcode = 0b1101111
            instr_rvi = (random.getrandbits(25) << 7) | opcode
            instr_rvi = (0b1111100101100010010000111 << 7) | opcode
            func3 = random.choice([0b101])
            op = 0b01
            instr_rvc = (func3) << 13 | (random.getrandbits(11) << 2) | op
            
            return instr_rvi if isa == 'rvi' else instr_rvc
        
        if type == 'br':
            instr_rvi = 0 #instr_rvi is aborted
            func3 = random.choice([0b110,0b111])
            op = 0b01
            instr_rvc = func3 << 13 | random.getrandbits(11) << 2 | op
            return instr_rvi if isa == 'rvi' else instr_rvc
        
        if type == 'jalr':
            instr_rvc = (0b1101) << 12 | random.getrandbits(5) << 7 | 0b0000010
            instr_rvi = random.getrandbits(1) << 15 | (0b000) << 12 | random.getrandbits(5) << 7 | 0b1100111
            return instr_rvi
        if type == 'jal':
            instr_rvi = random.getrandbits(9) << 7 | 0b1101111
            return instr_rvi
    
    def inst_gen_new_signal(self, isa = 'random', type = 'not_cfi'):
        if type == 'br':
            #generate br type instructions
            for _ in range(16):
                #rvi
                opcode = 0b1100011
                funct3 = random.choice([0b000,0b001,0b100,0b101,0b110,0b111])
                rs1 = random.getrandbits(5)
                rs2 = random.getrandbits(5)
                instr_rvi = (random.getrandbits(7) << 25) | rs1 << 20 |\
                        rs2 << 15 | funct3 << 12 | (random.getrandbits(5) << 7) |\
                        opcode
                        
                #rvc
                op = 0b01
                func3 = random.choice([0b110,0b111])
                instr_rvc = func3 << 13 | (random.getrandbits(11) << 2) | op
                
                self.brTypes.append(1)
                if isa == 'random':
                    self.instrs.append(random.choice([instr_rvi, instr_rvc]))
                elif isa == 'rvi':
                    self.instrs.append(instr_rvi)
                elif isa == 'rvc':
                    self.instrs.append(instr_rvc)
                
        elif type == 'jal':
            #generate jal type instructions
            for _ in range(16):
                #rvi 
                opcode = 0b1101111
                instr_rvi = (random.getrandbits(25) << 7) | opcode
                
                #rvc
                func3 = 0b101
                op = 0b01
                instr_rvc = (func3 << 13) | (random.getrandbits(11) << 2) | op
                
                self.brTypes.append(2)
                if isa == 'random':
                    self.instrs.append(random.choice([instr_rvi, instr_rvc]))
                elif isa == 'rvi':
                    self.instrs.append(instr_rvi)
                elif isa == 'rvc':
                    self.instrs.append(instr_rvc)
                    
        elif type == 'jalr':
            #generate jalr type instructions
            for _ in range(16):
                #rvi
                funct3 = 0b000
                opcode = 0b1100111
                instr_rvi = (random.getrandbits(17) << 25) | funct3 << 12 |\
                            (random.getrandbits(5) << 7) | opcode
                            
                #rvc
                rs1 = random.getrandbits(5) | 0b1
                head = random.choice([0b1001,0b1000])
                tail = 0b00000_10
                instr_rvc = (head << 12) | (rs1 << 7) | tail
                
                self.brTypes.append(3)
                if isa == 'random':
                    self.instrs.append(random.choice([instr_rvi, instr_rvc]))
                elif isa == 'rvi':
                    self.instrs.append(instr_rvi)
                elif isa == 'rvc':
                    self.instrs.append(instr_rvc)
                    
        elif type == 'not_cfi':
            #generate not cfi type instructions
            for _ in range(16):
                #rvi
                opcode = random.getrandbits(7) | 0b11
                funct3 = random.getrandbits(3)
                
                while True:
                    flag1 = (opcode == 0b1100011) and (funct3 in [0b000,0b001,0b010,0b011,0b100,0b101,0b110,0b111])
                    flag2 = (opcode == 0b1101111)
                    flag3 = (opcode == 0b1100111) and (funct3 == 0b000)
                    if not flag3 and not flag2 and not flag1:
                        break
                    opcode = random.getrandbits(7) | 0b11
                    funct3 = random.getrandbits(3)
                instr_rvi = random.getrandbits(17) << 15 | funct3 << 12 | random.getrandbits(5) << 7 | opcode
                
                #rvc
                c_ebreak = 0b100_1_00000_00000_10
                instr_rvc = random.getrandbits(16)
                while True:
                    op = instr_rvc & 0b11
                    func3 = instr_rvc >> 13
                    flag1 = (op == 0b01) and (func3 in [0b110, 0b111, 0b101])
                    
                    j1 = instr_rvc & 0b1111111
                    j2 = instr_rvc >> 12
                    flag2 = (j1 == 0b0000010) and (j2 in [0b1001, 0b1000])
                    
                    flag3 = op == 0b11
                    
                    if not flag1 and not flag2 and not flag3:
                        break
                    instr_rvc = random.getrandbits(16)

                self.brTypes.append(0)
                self.instrs.append(random.choice([instr_rvc,instr_rvi,c_ebreak]))
            
        return self.instrs, self.brTypes        


    def precoding_checker(self, task = '2.1.1'):
        if task == '2.1.1':
            self.instrs = [self.instr_gen(type = 'random', isa = 'rvc') for _ in range(17)]
            self.rvcs = [1 for _ in range(16)]
            return self.instrs, self.rvcs
        if task == '2.1.2':
            self.instrs = [random.getrandbits(16) | 0b11 for _ in range(17)]
            self.rvcs = [0 for _ in range(16)]
            return self.instrs, self.rvcs

        if task == '2.2.1':
            self.instrs = [self.instr_gen(type = 'j', isa = 'rvc') for _ in range(17)]
            def offset(instr):
                mask = 0b11111111111
                offset = (instr >> 2) & mask
                o11 = (offset >> 10) & 1
                o4 = (offset >> 9) & 1
                o98 = (offset >> 7) & 0b11
                o10 = (offset >> 6) & 1
                o6 = (offset >> 5) & 1
                o7 = (offset >> 4) & 1
                o31 = (offset >> 1) & 0b111
                o5 = (offset >> 0) & 1
                offset = (o11 << 11) | (o4 << 4) | (o98 << 8) | (o10 << 10) | (o6 << 6) | (o7 << 7) | (o31 << 1) | (o5 << 5)
                offset = offset if o11 == 0 else (offset | (0b1111) << 12) & 0xFFFF
                return offset
            self.jmp_offsets = [offset(i) for i in self.instrs]
            self.jmp_offsets.pop()
            return self.instrs, self.jmp_offsets
        if task == '2.2.2':
            self.instrs = [random.getrandbits(9) << 7 | 0b1101111 for _ in range(17)]
            self.new_instrs = [self.instrs[i+1] << 16 | self.instrs[i] for i in range(16)]
            def offset(instr):
                offset = instr >> 12
                o20 = (offset >> 19) & 1
                o101 = (offset >> 9) & 0b1111111111
                o11 = (offset >> 8) & 1
                o1912 = offset & 0b11111111
                offset = (o20 << 20) | (o101 << 1) | (o11 << 11) | (o1912 << 12)
                offset = offset & 0xFFFFFFFF if o20 == 0 else (offset | (0xFFFFFF) << 21) & 0xFFFFFFFF
                return offset
            self.jmp_offsets = [offset(i) for i in self.new_instrs]
            return self.instrs, self.jmp_offsets
        
        if task == '2.2.3':
            self.instrs = [self.instr_gen(type = 'br', isa = 'rvc') for _ in range(17)]
            def offset(instr):
                o5 = (instr >> 2) & 1
                o21 = (instr >> 3) & 0b11
                o76 = (instr >> 5) & 0b11
                o43 = (instr >> 10) & 0b11
                o8 = (instr >> 12) & 1
                offset = o5 << 5 | o21 << 1 | o76 << 6 | o43 << 3 | o8 << 8
                offset = offset if o8 == 0 else (offset | 0xFF << 9) & 0xFFFF
                return offset
            self.jmp_offsets = [offset(i) for i in self.instrs]
            self.jmp_offsets.pop()
            return self.instrs, self.jmp_offsets
        if task == '2.2.4':
            def offset(instr):
                o12 = (instr >> 31) & 1
                o105 = (instr >> 25) & 0b111111
                o11 = (instr >> 7) & 1
                o41 = (instr >> 8) & 0b1111
                offset = o12 << 12 | o105 << 5 | o11 << 11 | o41 << 1
                offset = offset if o12 == 0 else (offset | 0xFFFFFFF << 13) & 0xFFFFFFFF
                return offset
            self.instrs = [random.getrandbits(5) << 7 | random.getrandbits(1) << 15 | 0b1100011 | random.choice([0b000,0b001,0b100,0b101,0b110,0b111]) << 12 for _ in range(17)]
            self.new_instrs = [self.instrs[i+1] << 16 | self.instrs[i] for i in range(16)]
            self.jmp_offsets = [offset(i) for i in self.new_instrs]
            return self.instrs, self.jmp_offsets
        
        if task == '3.1':
            self.instrs = [random.getrandbits(16) for _ in range(17)]
            self.new_instrs = [self.instrs[i+1] << 16 | self.instrs[i] for i in range(16)]
            mask = 0b11
            flag = 2
            for i in range(16):
                if i == 0:
                    self.valid_starts.append(1)
                    flag = 1 if (self.new_instrs[i] & mask) == 0b11 else 0
                else:
                    if flag == 1:
                        self.valid_starts.append(0)
                        flag = 2
                    elif flag == 0:
                        self.valid_starts.append(1)
                        flag = 1 if (self.new_instrs[i] & mask) == 0b11 else 0
                    elif flag == 2:
                        self.valid_starts.append(1)
                        flag = 1 if (self.new_instrs[i] & mask) == 0b11 else 0
            return self.instrs, self.valid_starts
        
        if task == '3.2':
            self.instrs = [random.getrandbits(16) for _ in range(17)]
            self.new_instrs = [self.instrs[i+1] << 16 | self.instrs[i] for i in range(16)]
            mask = 0b11
            flag = 2
            for i in range(16):
                if i == 0:
                    self.half_valid_starts.append(0)
                elif i == 1:
                    self.half_valid_starts.append(1)
                    flag = 1 if (self.new_instrs[i] & mask) == 0b11 else 0
                else:
                    if flag == 1:
                        self.half_valid_starts.append(0)
                        flag = 2
                    elif flag == 0:
                        self.half_valid_starts.append(1)
                        flag = 1 if (self.new_instrs[i] & mask) == 0b11 else 0
                    elif flag == 2:
                        self.half_valid_starts.append(1)
                        flag = 1 if (self.new_instrs[i] & mask) == 0b11 else 0
            return self.instrs, self.half_valid_starts
        
            
