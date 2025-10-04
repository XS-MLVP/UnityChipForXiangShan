from ..instr_utils import fetch, concat,get_cfi_type, if_call, if_ret, is_rvc
from ..datadef import PreDecodeDataDef, F3PreDecodeData



class F3PredecoderRef():

    def f3_predecode(self, instrs: list[int]) -> F3PreDecodeData: 
        ret = F3PreDecodeData()
        for i in range(16):
            instr = instrs[i]
            ret.brTypes.append(get_cfi_type(instr))
            ret.isCalls.append(1 if if_call(instr, ret.brTypes[i]) else 0)
            ret.isRets.append(1 if if_ret(instr, ret.brTypes[i]) else 0)
        return ret
        

class PredecodeRef():
    def predecode(self, instrs: list[int]) -> PreDecodeDataDef:
        ret = PreDecodeDataDef()

        for i in range(16):
            ret.new_instrs.append(instrs[i] | (instrs[i+1] << 16))
            ret.rvcs.append(is_rvc(ret.new_instrs[i]))
            ret.jmp_offsets.append(self.calc_imm(ret.new_instrs[i]))
            ret.valid_starts.append(False)
            ret.half_valid_starts.append(False)

            if i == 0:
                ret.valid_starts[i] = True
                ret.half_valid_starts[i] = False
            elif i == 1:
                ret.half_valid_starts[i] = True
                ret.valid_starts[i] = ret.rvcs[0]
            else:
                if ret.half_valid_starts[i-1] == True:
                    ret.half_valid_starts[i] = ret.rvcs[i-1]
                else:
                    ret.half_valid_starts[i] = True
                
                if ret.valid_starts[i-1] == True:
                    ret.valid_starts[i] = ret.rvcs[i-1]
                else:
                    ret.valid_starts[i] = True
        return ret
    
    def extend_to_64(self, value, bits):
        value &= (1 << bits) - 1  # 截断到 bits 位
        sign_bit = 1 << (bits - 1)
        if value & sign_bit:
            # 手动补全高位 1，但仍保持非负 Python int（模拟补码）
            value |= ((-1) << bits) & ((1 << 64) - 1)
        return value


    def calc_imm(self, instr):

        op = fetch(instr, 0, 1)
        funct = fetch(instr, 13, 15)

        if op < 3: # C.J or beq

            if op == 1 and (funct == 6 or funct == 7): # beq 
                imm = concat(instr, [[12], [5, 6], [2], [10, 11], [3, 4]]) << 1
                return self.extend_to_64(imm, 9)
                # if funct == 5: # C.J
            return self.extend_to_64(concat(instr, [[12], [8], [9, 10], [6],[7], [2], [11], [3, 5]]) << 1, 12)
            
        rvi_funct = fetch(instr, 0, 6)
        
        if rvi_funct == 99: # 1100011 b
            return self.extend_to_64(concat(instr, [[31], [7], [25, 30], [8, 11]]) << 1, 13)

        # if rvi_funct == 111: # "1101111 JAL"：
        return self.extend_to_64(concat(instr, [[31], [12, 19], [20], [21, 30]]) << 1, 21)
    
    