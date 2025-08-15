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
            flag = (self.new_instrs[0] & mask) == 0b11
            self.valid_starts.append(1)

            for i in range(1, 16):
                if flag:
                    self.valid_starts.append(0)
                    flag = False
                else:
                    self.valid_starts.append(1)
                    flag = (self.new_instrs[i] & mask) == 0b11
            return self.instrs, self.valid_starts
        
        if task == '3.2':
            self.instrs = [random.getrandbits(16) for _ in range(17)]
            self.new_instrs = [self.instrs[i+1] << 16 | self.instrs[i] for i in range(16)]
            mask = 0b11
            self.half_valid_starts.append(0)  # i == 0
            self.half_valid_starts.append(1)  # i == 1
            flag = (self.new_instrs[1] & mask) == 0b11

            for i in range(2, 16):
                if flag:
                    self.half_valid_starts.append(0)
                    flag = False
                else:
                    self.half_valid_starts.append(1)
                    flag = (self.new_instrs[i] & mask) == 0b11
            return self.instrs, self.half_valid_starts
        
            
