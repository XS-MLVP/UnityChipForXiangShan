import random

class F3PredecodeInstrGen():
    def __init__(self):
        self.brTypes = [] 
        self.isCalls = [] 
        self.isRets = []
        self.instrs = []
    
    def clear(self):
        self.brTypes = []
        self.isCalls = []
        self.isRets = []
        self.instrs = []
        
    def inst_gen(self, isa = 'random', type = 'not_cfi'):
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
    
    def ret_call_checker(self,task = '2.1.1'):
        if task =='2.1.1':
            self.inst_gen(type = 'not_cfi')
            self.isCalls = [0 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        if task == '2.1.2':
            self.inst_gen(type = 'br')
            self.isCalls = [0 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        if task == '2.2.1.1':
            def rd():
                return random.choice([1, 5]) << 7
            mask = 0b1111_1111_1111_1111_1111_0000_0111_1111
            self.inst_gen(type = 'jal', isa = 'rvi')
            self.instrs = [i & mask | rd() for i in self.instrs]
            self.isCalls = [1 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        if task == '2.2.1.2':
            def rd():
                valid_numbers = [x for x in range(33) if x not in {1, 5}]
                num = random.choice(valid_numbers)
                return num << 7
            mask = 0b1111_1111_1111_1111_1111_0000_0111_1111
            self.inst_gen(type = 'jal', isa = 'rvi')
            self.instrs = [i & mask | rd() for i in self.instrs]
            self.isCalls = [0 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        if task == '2.2.2':
            self.isCalls = [0 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            self.inst_gen(type = 'jal', isa = 'rvc')
            return self.instrs, self.isCalls, self.isRets
        if task == '2.3.1.1':
            def rd():
                return random.choice([1, 5]) << 7
            mask = 0b1111_1111_1111_1111_1111_0000_0111_1111
            self.inst_gen(type = 'jalr', isa = 'rvi')
            self.instrs = [i & mask | rd() for i in self.instrs]
            self.isCalls = [1 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        
        if task == '2.3.1.2':
            def rs():
                return random.choice([1,5]) << 15
            def rd():
                valid_numbers = [x for x in range(32) if x not in {1, 5}]
                num = random.choice(valid_numbers)
                return num << 7
            mask = 0b1111_1111_1111_0000_0111_0000_0111_1111
            self.inst_gen('jalr', 'rvi')
            self.inst_gen(type = 'jalr', isa = 'rvi')
            self.instrs = [i & mask | rd() | rs() for i in self.instrs]
            self.isCalls = [0 for _ in range(16)]
            self.isRets = [1 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        
        if task == '2.3.1.3':
            def rd():
                valid_numbers = [x for x in range(32) if x not in {1, 5}]
                num = random.choice(valid_numbers)
                return num << 7
            def rs():
                valid_numbers = [x for x in range(32) if x not in {1, 5}]
                num = random.choice(valid_numbers)
                return num << 15
            mask = 0b1111_1111_1111_0000_0111_0000_0111_1111
            self.inst_gen('jalr', 'rvi')
            self.inst_gen(type = 'jalr', isa = 'rvi')
            self.instrs = [i & mask | rd() | rs() for i in self.instrs]
            self.isCalls = [0 for _ in range(16)]
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets    
        
        if task == '2.3.2.1':
            self.inst_gen(type = 'jalr', isa = 'rvc')
            self.instrs = [i | 1 << 12 for i in self.instrs]   
            self.isCalls = [1 for _ in range(16)]  
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets 
        
        if task == '2.3.2.2.1':
            def rs():
                return random.choice([1,5]) << 7
            mask = 0b1110000001111111
            self.inst_gen(type = 'jalr', isa = 'rvc')
            self.instrs = [i & mask | rs() for i in self.instrs]   
            self.isCalls = [0 for _ in range(16)]  
            self.isRets = [1 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
        
        if task == '2.3.2.2.2':
            def rs():
                valid_numbers = [x for x in range(32) if x not in {1, 5}]
                num = random.choice(valid_numbers)
                return num << 7
            mask = 0b1110000001111111
            self.inst_gen(type = 'jalr', isa = 'rvc')
            self.instrs = [i & mask | rs() for i in self.instrs]   
            self.isCalls = [0 for _ in range(16)]  
            self.isRets = [0 for _ in range(16)]
            return self.instrs, self.isCalls, self.isRets
            
