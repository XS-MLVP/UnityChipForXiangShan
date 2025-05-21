#coding=utf8
#***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
#**************************************************************************************/


from .env import *
from tools.insn_gen import *
from tools.disasm import disasmbly, libdisasm
from comm import TAG_LONG_TIME_RUN, TAG_SMOKE, TAG_RARELY_USED, debug


def rvc_expand(rvc_expander, ref_insts, is_32bit=False, fsIsOff=False):
    """compare the RVC expand result with the reference

    Args:
        rvc_expander (warpper): the fixture of the RVC expander
        ref_insts (list[int]]): the reference instruction list
    """
    find_error = 0
    for insn in ref_insts:
        insn_disasm = disasmbly(insn)
        value, instr_ex = rvc_expander.expand(insn, fsIsOff)
#        assert instr_ex == 0
#        debug(f"find bad inst:{value},ref: 1, dut: 0")
        if is_32bit:
            assert value == insn, "RVC expand error, 32bit instruction need to be the same"
            assert instr_ex == 0
        else :
            insn_ref, ill = rvc_expand_ref(insn,fsIsOff)
            if ill == 0: 
                if  (value != insn_ref) or (ill != instr_ex) :
                    debug(f"find bad inst:{insn},rcv_expand:{value},ref:{insn_ref},fsIsOff:{fsIsOff},ref_ill:{ill}, dut:{instr_ex}")
                assert value == insn_ref
                assert ill   == instr_ex
            else:
                #if(insn_ref == 0x7f)|(ill==2):
                #    debug(f"find reverse inst:{insn},rcv_expand:{value}, ref_ill:{ill}, dut:{instr_ex}")
                #    assert ill == instr_ex

                if((ill != instr_ex)&(ill!=2)&(insn_ref != 0x7f)):
                    debug(f"find bad inst:{insn},rcv_expand:{value},ref:{insn_ref},fsIsOff:{fsIsOff},ref_ill:{ill}, dut:{instr_ex}")
                    assert ill == instr_ex
                
        if (insn_disasm == "unknown") and  (instr_ex == 0):
            debug(f"find bad inst:{insn}, ref: 1, dut: 0")
            find_error +=1
        elif (insn_disasm != "unknown") and  (instr_ex == 1) and(fsIsOff ==False):
            if (instr_filter(insn_disasm) != 1): 
                debug(f"find bad inst:{insn},disasm:{insn_disasm}, ref: 0, dut: 1")
                find_error +=1
    assert 0 == find_error, "RVC expand error (%d errros)" % find_error



@pytest.mark.toffee_tags(TAG_SMOKE)
def test_rvc_expand_32bit_smoke(rvc_expander):
    """
    Test the RVC expand function with 1 fixed 32 bit instruction
    """
    rvc_expand(rvc_expander, [873825667],is_32bit=True)


#@pytest.mark.toffee_tags(TAG_SMOKE)
#def test_rvc_expand_16bit_smoke(rvc_expander):
#    """
#    Test the RVC expand function with 1 compressed instruction
#    """
#    rvc_expand(rvc_expander, generate_rvc_instructions(start=100, end=101),is_32bit=True)


N = 10
T = 1<<16
pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_16bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full compressed instruction set
    
    Description:
        Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
    """
    # Add check point: RVC_EXPAND_RANGE to check expander input range.
    #   When run to here, the range[start, end] is covered
    covered = -1
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]"%(start, end): lambda _: covered == end
                          }, name = "RVC_EXPAND_ALL_16B", dynamic_bin=True)
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]"%(start, end))
    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end))
    # When go to here, the range[start, end] is covered
    covered = end
    g.sample()

pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_16bit_full_fsIsOff_True(rvc_expander, start, end):
    """Test the RVC expand function with a full compressed instruction set
    
    Description:
        Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
    """
    # Add check point: RVC_EXPAND_RANGE to check expander input range.
    #   When run to here, the range[start, end] is covered
    covered = -1
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]"%(start, end): lambda _: covered == end
                          }, name = "RVC_EXPAND_ALL_16B", dynamic_bin=True)
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]"%(start, end))
    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end),False,True)
    # When go to here, the range[start, end] is covered
    covered = end
    g.sample()


#N=10
#T=1<<32
# @pytest.mark.toffee_tags([TAG_LONG_TIME_RUN, TAG_RARELY_USED])
# @pytest.mark.parametrize("start,end",
#                          [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
# def test_rvc_expand_32bit_full(rvc_expander, start, end):
#     """Test the RVC expand function with a full 32 bit instruction set

#     Description:
#         Randomly generate N 32-bit instructions for each check, and repeat the process K times.
#     """
#     # Add check point: RVC_EXPAND_ALL_32B to check instr bits.
#     covered = -1
#     g.add_watch_point(rvc_expander, {"RANGE[%d-%d]"%(start, end): lambda _: covered == end},
#                       name = "RVC_EXPAND_ALL_32B", dynamic_bin=True)
#     # Reverse mark function to the check point
#     g.mark_function("RVC_EXPAND_ALL_32B", test_rvc_expand_32bit_full)
#     # Drive the expander and check the result
#     rvc_expand(rvc_expander, list([_ for _ in range(start, end)]))
#     # When go to here, the range[start, end] is covered
#     covered = end
#     g.sample()


# @pytest.mark.skip("This test is allways failed, need to be fixed")
# def test_rvc_expand_32bit_randomN(rvc_expander):
#     """Test the RVC expand function with a random 32 bit instruction set

#     Description:
#         Randomly generate 32-bit instructions for testing
#     """
#     rvc_expand(rvc_expander, generate_random_32bits(10000))
def generate_random_register():
    """生成随机的寄存器编号（0-31）"""
    return random.randint(0, 31)

def generate_random_immediate(bits):
    """生成随机的立即数，bits 表示立即数的位数"""
    return random.randint(0, (1 << bits) - 1)

def test_rvc_expand_32bit_csr_all(rvc_expander):
     #CSR
    num_instructions=100
    instructions = [
    {"name": "CSRRW",  "opcode": 0b1110011, "funct3": 0b001, "type": "CSR"},
    {"name": "CSRRS",  "opcode": 0b1110011, "funct3": 0b010, "type": "CSR"},
    {"name": "CSRRC",  "opcode": 0b1110011, "funct3": 0b011, "type": "CSR"},
    {"name": "CSRRWI", "opcode": 0b1110011, "funct3": 0b101, "type": "CSR"},
    {"name": "CSRRSI", "opcode": 0b1110011, "funct3": 0b110, "type": "CSR"},
    {"name": "CSRRCI", "opcode": 0b1110011, "funct3": 0b111, "type": "CSR"},
    ]
    instruction_encodings = []
    for _ in range(num_instructions):
        instr = random.choice(instructions)
        opcode = instr["opcode"]
        funct3 = instr.get("funct3", 0)
        rd = random.randint(0, 31)
        rs1 = random.randint(0, 31)
        fs_isoff = 1
        imm = generate_random_immediate(12)
        encoding = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        instruction_encodings.append(encoding)
        #fs_isoff = random.randint(0, 1)

    if (fs_isoff==1):
        rvc_expand(rvc_expander, instruction_encodings,is_32bit=True,fsIsOff=True)
    else:
        rvc_expand(rvc_expander, instruction_encodings,is_32bit=True,fsIsOff=False)

def test_rvc_expand_32bit_rvi_all(rvc_expander):

    all_instructions,fs_isoff = generate_rv32i_rv64i_instructions(10000)
    fs_isoff = random.randint(0, 1)
    if (fs_isoff==1):
        rvc_expand(rvc_expander, all_instructions,is_32bit=True,fsIsOff=True)
    else:
        rvc_expand(rvc_expander, all_instructions,is_32bit=True,fsIsOff=False)



def generate_rv32i_rv64i_instructions(num_instructions=10):
    """生成 RV32I 和 RV64I 指令集的随机编码"""
    instructions = [
         #CSR
        {"name": "CSRRW",  "opcode": 0b1110011, "funct3": 0b001, "type": "CSR"},
        {"name": "CSRRS",  "opcode": 0b1110011, "funct3": 0b010, "type": "CSR"},
        {"name": "CSRRC",  "opcode": 0b1110011, "funct3": 0b011, "type": "CSR"},
        {"name": "CSRRWI", "opcode": 0b1110011, "funct3": 0b101, "type": "CSR"},
        {"name": "CSRRSI", "opcode": 0b1110011, "funct3": 0b110, "type": "CSR"},
        {"name": "CSRRCI", "opcode": 0b1110011, "funct3": 0b111, "type": "CSR"},
        # R-type instructions
        {"name": "ADD",  "opcode": 0b0110011, "funct3": 0b000, "funct7": 0b0000000, "type": "R"},
        {"name": "SUB",  "opcode": 0b0110011, "funct3": 0b000, "funct7": 0b0100000, "type": "R"},
        {"name": "SLL",  "opcode": 0b0110011, "funct3": 0b001, "funct7": 0b0000000, "type": "R"},
        {"name": "SLT",  "opcode": 0b0110011, "funct3": 0b010, "funct7": 0b0000000, "type": "R"},
        {"name": "SLTU", "opcode": 0b0110011, "funct3": 0b011, "funct7": 0b0000000, "type": "R"},
        {"name": "XOR",  "opcode": 0b0110011, "funct3": 0b100, "funct7": 0b0000000, "type": "R"},
        {"name": "SRL",  "opcode": 0b0110011, "funct3": 0b101, "funct7": 0b0000000, "type": "R"},
        {"name": "SRA",  "opcode": 0b0110011, "funct3": 0b101, "funct7": 0b0100000, "type": "R"},
        {"name": "OR",   "opcode": 0b0110011, "funct3": 0b110, "funct7": 0b0000000, "type": "R"},
        {"name": "AND",  "opcode": 0b0110011, "funct3": 0b111, "funct7": 0b0000000, "type": "R"},

        # I-type instructions
        {"name": "ADDI",  "opcode": 0b0010011, "funct3": 0b000, "type": "I"},
        {"name": "SLTI",  "opcode": 0b0010011, "funct3": 0b010, "type": "I"},
        {"name": "SLTIU", "opcode": 0b0010011, "funct3": 0b011, "type": "I"},
        {"name": "XORI",  "opcode": 0b0010011, "funct3": 0b100, "type": "I"},
        {"name": "ORI",   "opcode": 0b0010011, "funct3": 0b110, "type": "I"},
        {"name": "ANDI",  "opcode": 0b0010011, "funct3": 0b111, "type": "I"},
        {"name": "SLLI",  "opcode": 0b0010011, "funct3": 0b001, "funct7": 0b0000000, "type": "R"},
        {"name": "SRLI",  "opcode": 0b0010011, "funct3": 0b101, "funct7": 0b0000000, "type": "R"},
        {"name": "SRAI",  "opcode": 0b0010011, "funct3": 0b101, "funct7": 0b0100000, "type": "R"},

        # Load/Store instructions (I-type and S-type)
        {"name": "LB",   "opcode": 0b0000011, "funct3": 0b000, "type": "I"},
        {"name": "LH",   "opcode": 0b0000011, "funct3": 0b001, "type": "I"},
        {"name": "LW",   "opcode": 0b0000011, "funct3": 0b010, "type": "I"},
        {"name": "LBU",  "opcode": 0b0000011, "funct3": 0b100, "type": "I"},
        {"name": "LHU",  "opcode": 0b0000011, "funct3": 0b101, "type": "I"},
        {"name": "SB",   "opcode": 0b0100011, "funct3": 0b000, "type": "S"},
        {"name": "SH",   "opcode": 0b0100011, "funct3": 0b001, "type": "S"},
        {"name": "SW",   "opcode": 0b0100011, "funct3": 0b010, "type": "S"},

        # Branch instructions (B-type)
        {"name": "BEQ",  "opcode": 0b1100011, "funct3": 0b000, "type": "B"},
        {"name": "BNE",  "opcode": 0b1100011, "funct3": 0b001, "type": "B"},
        {"name": "BLT",  "opcode": 0b1100011, "funct3": 0b100, "type": "B"},
        {"name": "BGE",  "opcode": 0b1100011, "funct3": 0b101, "type": "B"},
        {"name": "BLTU", "opcode": 0b1100011, "funct3": 0b110, "type": "B"},
        {"name": "BGEU", "opcode": 0b1100011, "funct3": 0b111, "type": "B"},

        # J-type instructions
        {"name": "JAL",  "opcode": 0b1101111, "type": "J"},
        {"name": "JALR", "opcode": 0b1100111, "funct3": 0b000, "type": "I"},

        # U-type instructions
        {"name": "LUI",  "opcode": 0b0110111, "type": "U"},
        {"name": "AUIPC","opcode": 0b0010111, "type": "U"},

        # RV64I additional instructions
        {"name": "LWU",  "opcode": 0b0000011, "funct3": 0b110, "type": "I"},
        {"name": "LD",   "opcode": 0b0000011, "funct3": 0b011, "type": "I"},
        {"name": "SD",   "opcode": 0b0100011, "funct3": 0b011, "type": "S"},
        {"name": "ADDIW","opcode": 0b0011011, "funct3": 0b000, "type": "I"},
        {"name": "SLLIW","opcode": 0b0011011, "funct3": 0b001, "funct7": 0b0000000, "type": "R"},
        {"name": "SRLIW","opcode": 0b0011011, "funct3": 0b101, "funct7": 0b0000000, "type": "R"},
        {"name": "SRAIW","opcode": 0b0011011, "funct3": 0b101, "funct7": 0b0100000, "type": "R"},
        {"name": "ADDW", "opcode": 0b0111011, "funct3": 0b000, "funct7": 0b0000000, "type": "R"},
        {"name": "SUBW", "opcode": 0b0111011, "funct3": 0b000, "funct7": 0b0100000, "type": "R"},
        {"name": "SLLW", "opcode": 0b0111011, "funct3": 0b001, "funct7": 0b0000000, "type": "R"},
        {"name": "SRLW", "opcode": 0b0111011, "funct3": 0b101, "funct7": 0b0000000, "type": "R"},
        {"name": "SRAW", "opcode": 0b0111011, "funct3": 0b101, "funct7": 0b0100000, "type": "R"},

       



    ]

    # 生成随机指令编码
    instruction_encodings = []
    for _ in range(num_instructions):
        instr = random.choice(instructions)
        opcode = instr["opcode"]
        funct3 = instr.get("funct3", 0)
        funct7 = instr.get("funct7", 0)
        rd = generate_random_register()
        rs1 = generate_random_register()
        rs2 = generate_random_register()
        fs_isoff = 0
        if instr["type"] == "R":
            # R-type: funct7 | rs2 | rs1 | funct3 | rd | opcode
            encoding = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        elif instr["type"] == "I":
            # I-type: imm[11:0] | rs1 | funct3 | rd | opcode
            imm = generate_random_immediate(12)
            encoding = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        elif instr["type"] == "S":
            # S-type: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
            imm = generate_random_immediate(12)
            encoding = ((imm & 0xFE0) << 20) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | ((imm & 0x1F) << 7) | opcode
        elif instr["type"] == "B":
            # B-type: imm[12] | imm[10:5] | rs2 | rs1 | funct3 | imm[4:1] | imm[11] | opcode
            imm = generate_random_immediate(13)
            encoding = ((imm & 0x1000) << 19) | ((imm & 0x7E0) << 20) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | ((imm & 0x1E) << 7) | ((imm & 0x800) >> 4) | opcode
        elif instr["type"] == "U":
            # U-type: imm[31:12] | rd | opcode
            imm = generate_random_immediate(20)
            encoding = (imm << 12) | (rd << 7) | opcode
        elif instr["type"] == "J":
            # J-type: imm[20] | imm[10:1] | imm[11] | imm[19:12] | rd | opcode
            imm = generate_random_immediate(21)
            encoding = ((imm & 0x100000) << 11) | ((imm & 0x7FE) << 20) | ((imm & 0x800) << 9) | ((imm & 0xFF000) << 0) | (rd << 7) | opcode
        elif instr["type"] == "CSR":
            # R-type: funct7 | rs2 | rs1 | funct3 | rd | opcode
            imm = generate_random_immediate(12)
            encoding = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
            fs_isoff == 1
        instruction_encodings.append(encoding)

    return instruction_encodings,fs_isoff


import random

def test_rvc_expand_16bit_rvc_all(rvc_expander):

    all_instructions = generate_rv32c_rv64c_instructions(10000)
    fsIsOff = random.randint(0, 1)
    if(fsIsOff):
        rvc_expand(rvc_expander, all_instructions,False,True)
    else:
        rvc_expand(rvc_expander, all_instructions)

def generate_rv32c_rv64c_instructions(num_instructions=10):
    """生成 RVC 指令集的随机编码"""
    # RVC 指令集的操作码和功能码
    rvc_instructions = [
        # C.ADDI4SPN (Add Immediate to Stack Pointer, Nondestructive) pass
        {"name": "C.ADDI4SPN", "opcode": 0b00, "funct3": 0b000, "type": "CIW"},
        # C.FLD pass
        {"name": "C.FLD", "opcode": 0b00, "funct3": 0b001, "type": "CL"},
        # C.LW (Load Word) pass
        {"name": "C.LW",  "opcode": 0b00, "funct3": 0b010, "type": "CL"},
        # C.LD (Load Word) pass
        {"name": "C.LD",  "opcode": 0b00, "funct3": 0b011, "type": "CL"},
        # 扩展（100）
        # C.lbu,lhu,lh,sb,sh pass
        {"name": "C.LBU",  "opcode": 0b00, "funct3": 0b100000, "type": "CA"}, #c.lbu pass
        {"name": "C.LHU/LH",  "opcode": 0b00, "funct3": 0b100001, "type": "CA"}, #c.lhu/c.lh pass
  
        {"name": "C.SB",  "opcode": 0b00, "funct3": 0b100010, "type": "CA"},
        {"name": "C.SH",  "opcode": 0b00, "funct3": 0b100011, "type": "CA"},
        #
        # C.FSD pass
        {"name": "C.FSD", "opcode": 0b00, "funct3": 0b101, "type": "CS"},
        # C.SW (Store Word) pass
        {"name": "C.SW", "opcode": 0b00, "funct3": 0b110, "type": "CS"},
        # C.SD pass
        {"name": "C.SD", "opcode": 0b00, "funct3": 0b111, "type": "CS"},

        # 00 end 01 begin #############################################################

        # C.ADDI (Add Immediate) pass
        {"name": "C.ADDI", "opcode": 0b01, "funct3": 0b000, "type": "CI"},
        # C.ADDIW (Add Immediate) pass
        {"name": "C.ADDIW", "opcode": 0b01, "funct3": 0b001, "type": "CI"},
        # C.LI (Load Immediate) pass
        {"name": "C.LI", "opcode": 0b01, "funct3": 0b010, "type": "CI"},
        # C.LUI/addi16sp/zcm (Load Upper ) pass
        {"name": "C.LUI", "opcode": 0b01, "funct3": 0b011, "type": "CI"},
        #扩展（100）
        # C.SRLI64 (Shift Right Logical Immediate) pass
        {"name": "C.SRLI64", "opcode": 0b01, "funct3": 0b100000, "type": "CLL"},
        {"name": "C.SRLI64", "opcode": 0b01, "funct3": 0b100100, "type": "CLL"},
        # C.SRAI64 (Shift Right Logical Immediate) pass
        {"name": "C.SRAI64", "opcode": 0b01, "funct3": 0b100001, "type": "CLL"},
        {"name": "C.SRAI64", "opcode": 0b01, "funct3": 0b100101, "type": "CLL"},
        # C.ANDI (And Immediate) pass
        {"name": "C.ANDI", "opcode": 0b01, "funct3": 0b100110, "type": "CLL"},
        {"name": "C.ANDI", "opcode": 0b01, "funct3": 0b100010, "type": "CLL"},
        # C.sub/xor/or/and 
        {"name": "C.SUB", "opcode": 0b01, "funct3": 0b100011, "type": "CA"},
        # C.subw/addw/mul/not/zext.b/sext.b/zext.h/sext.h/zext.w/
        {"name": "C.SUB", "opcode": 0b01, "funct3": 0b100111, "type": "CAA"},
        # end 100
#        #C.J pass
        {"name": "C.J", "opcode": 0b01, "funct3": 0b101, "type": "CJ"},
        #C.BEQZ pass
        {"name": "C.BEQZ", "opcode": 0b01, "funct3": 0b110, "type": "CB"},
        #C.BNEZ pass
        {"name": "C.SUB", "opcode": 0b01, "funct3": 0b111, "type": "CB"},
        # 01 end 10 begin #############################################################
          #C.SLLI64 pass
        {"name": "C.SLLI64", "opcode": 0b10, "funct3": 0b000, "type": "CI"},
          #C.fldsp  pass
        {"name": "C.fldsp", "opcode": 0b10, "funct3": 0b001, "type": "CI"},
          #C.lwsp   pass
        {"name": "C.lwsp", "opcode": 0b10, "funct3": 0b010, "type": "CI"},
          #C.ldsp    pass
        {"name": "C.ldsp", "opcode": 0b10, "funct3": 0b011, "type": "CI"},
          #jr/mv/ebreark/jalr/add pass
        {"name": "C.ldsp", "opcode": 0b10, "funct3": 0b100, "type": "CI"},
          #C.fsdsp    pass
        {"name": "C.fsdsp", "opcode": 0b10, "funct3": 0b101, "type": "CSS"},
          #C.swsp    pass
        {"name": "C.swsp", "opcode": 0b10, "funct3": 0b110, "type": "CSS"},
          #C.sdsp    pass
        {"name": "C.sdsp", "opcode": 0b10, "funct3": 0b111, "type": "CSS"},
    ]

    # 生成随机指令编码
    instruction_encodings = []
    for _ in range(num_instructions):
        instr = random.choice(rvc_instructions)
        opcode = instr["opcode"]
        funct3 = instr["funct3"]
      #  funct6 = instr["funct6"]
        instr_type = instr["type"]

        if instr_type == "CIW":
            # CIW 类型：imm[9:2] | rd' | opcode
            imm = random.randint(1,255)  # 10-bit immediate
            rd = random.randint(0, 7)      # 3-bit compressed register
            encoding = (65535 << 16) | (funct3 << 13) | (imm << 5) | (rd << 2) | opcode
        elif instr_type == "CL":
            # CL 类型：imm[5:3] | rs1' | imm[2:0] | rd' | opcode
            imm = random.randint(0, 31)    # 6-bit immediate
            rs1 = random.randint(0, 7)     # 3-bit compressed register
            rd  = random.randint(0, 7)      # 3-bit compressed register
            encoding =  (funct3 << 13) |  ((imm & 0x1C) << 8) | (rs1 << 7) | ((imm & 0x03) << 5) | (rd << 2) | opcode
        elif instr_type == "CS":
            # CS 类型：imm[5:3] | rs1' | imm[2:0] | rs2' | opcode
            imm = random.randint(0, 31)    # 6-bit immediate
            rs1 = random.randint(0, 7)     # 3-bit compressed register
            rs2 = random.randint(0, 7)     # 3-bit compressed register
            encoding =  (funct3 << 13) |  ((imm & 0x1C) << 8) | (rs1 << 7) | ((imm & 0x03) << 5) | (rs2 << 2) | opcode
        elif instr_type == "CI":
            # CI 类型：imm[5:0] | rd | opcode
            imm = random.randint(0, 63)    # 6-bit immediate
            rd = random.randint(0, 31)     # 5-bit register
            encoding = (funct3  << 13) |  ((imm & 0x20) << 7) | (rd << 7) | ((imm & 0x1F) << 2) | opcode
        elif instr_type == "CJ":
            # CJ 类型：imm[11:1] | opcode
            imm = random.randint(0, 2047)  # 11-bit immediate
            encoding = (funct3  << 13) | ((imm & 0x7FF) << 2) | opcode
        elif instr_type == "CB":
            # CB 类型：imm[8:4] | rs1' | imm[3:0] | opcode
            imm = random.randint(0, 255)   # 9-bit immediate
            rs1 = random.randint(0, 7)     # 3-bit compressed register
            encoding = (funct3  << 13) | ((imm & 0xE0) << 5) | (rs1 << 7) | ((imm & 0x1F) << 2) | opcode
        elif instr_type == "CA":
            # CA 类型：funct6 | rs2' | rs1' | opcode
        #    funct6 = random.randint(0, 63)  # 6-bit function code
            rs2 = random.randint(0, 7)     # 3-bit compressed register
            rs1 = random.randint(0, 7)     # 3-bit compressed register
            if(funct3 != 0b100011)&(opcode==0b00):
                imm = random.randint(0, 3)
            else:
                imm = random.randint(0, 1)
            encoding = (funct3 << 10) | (rs2 << 7) | imm<<5 | (rs1 << 2) | opcode
        elif instr_type == "CSS":
            # CSS 类型：funct6 | imm[8:3] | rs2' | opcode
            rs2 = random.randint(0, 31)     # 3-bit compressed register
            imm = random.randint(0, 63)    # 6-bit immediate
            encoding = (funct3 << 13) | (imm << 7) | (rs2 << 2) | opcode
        elif instr_type == "CLL":
            # CLL 类型：funct6 | imm[8:3] | rs2' | opcode
            rs1 = random.randint(0, 7)     # 3-bit compressed register
            imm = random.randint(0, 63)    # 6-bit immediate
            encoding = (funct3 << 10)| (rs1 << 7) | (imm << 2)   |opcode    
        elif instr_type == "CAA":
            # CAA 类型：funct6 | imm[8:3] | rs2' | opcode
            imm = random.randint(0, 3) 
            rs1 = random.randint(0, 7)     # 3-bit compressed register
            if(imm!=0b11):
                rs2 = random.randint(0, 7)     # 3-bit compressed register
            else:
                rs2 = random.randint(0, 5)
            encoding = (funct3 << 10) | (rs1 << 7) | imm<<5 | (rs2 << 2) | opcode
        instruction_encodings.append(encoding)

    return instruction_encodings

def rvc_expand_ref(rvc_instr,fsIsOff):
     ill = 0
     expanded = 0
     rvc_instr_16bit = rvc_instr & 0xFFFF
     opcode = rvc_instr_16bit & 0b11
     if opcode == 0b00:
        # C.ADDI4SPN指令
        if (rvc_instr_16bit & 0xE003) == 0x0000:
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3C) << 4) | (((rvc_instr_16bit >> 5) & 0x1) << 3) | (((rvc_instr_16bit >> 5) & 0x2) << 1) |  (((rvc_instr_16bit >> 5) & 0xC0) >> 2)
            rd = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            expanded = 0x00000013 | (nzuimm << 20) | (rd << 7) |(2<<15) # ADDI
            if nzuimm == 0:
                ill = 1
            else :
                ill = 0
            return expanded,ill  #"C.ADDI4SPN -> ADDI"
        # C.FLD
        elif (rvc_instr_16bit & 0xE003) == 0x2000:
            rd  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2) 
            expanded = 0x00000007 | (nzuimm << 20) | (rd << 7) |(0b011 <<12) |(rs1 << 15) # ADDI
            if(fsIsOff==True):
                ill=1
            else:
                ill=0
            return expanded,ill
        #C.lw  lw的格式形如： | imm[11:0] | rs1 | 010 | rd | 0000011 |
        elif (rvc_instr_16bit & 0xE003) == 0x4000:
            rd  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x1) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)| (((rvc_instr_16bit >> 5) & 0x2) << 1) 
            expanded = 0x00000003 | (nzuimm << 20) | (rd << 7) |(0b010 <<12) |(rs1 << 15) # ADDI
            return expanded,ill
        #C.ld 
        elif (rvc_instr_16bit & 0xE003) == 0x6000:
            rd2  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)
            expanded = 0x00000003 | (nzuimm << 20) | (rd2 << 7) |(0b011 <<12) |(rs1 << 15) # ADDI
            return expanded,ill
        #c.lbu/lhu/lh/sb/sh
        elif (rvc_instr_16bit & 0xE003) == 0x8000:
            rs2  = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            fun6 = (rvc_instr_16bit>>10)&0x3F
            if(fun6==0b100000):#lbu
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2) | ((rvc_instr_16bit >> 6) & 0x1)
                expanded = 0x00000003 | (rs2 << 7) | (0b100 <<12) | (rs1 << 15) |(nzuimm << 20)  #
                return expanded,ill
            elif(fun6==0b100001)&(((rvc_instr_16bit >> 6) & 0x1)==0):#lhu
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2)
                expanded = 0x00000003 | (rs2 << 7) | (0b101 <<12) | (rs1 << 15) |(nzuimm << 20)  # 
                return expanded,ill
            elif(fun6==0b100001)&(((rvc_instr_16bit >> 6) & 0x1)==1):#lh
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2)
                expanded = 0x00000003 | (rs2 << 7) | (0b001 <<12) | (rs1 << 15) |(nzuimm << 20)  # 
                return expanded,ill
            elif(fun6==0b100010):#sb
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2) | ((rvc_instr_16bit >> 6) & 0x1)
                expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b000 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
                return expanded,ill
            elif((fun6==0b100011)&(((rvc_instr_16bit >> 6) & 0x1)==0)):#sh
                nzuimm = ((rvc_instr_16bit >> 4) & 0x2)
                expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b001 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
                return expanded,ill
            else:
                ill=2
                return expanded,ill
        #C.fsd 
        elif (rvc_instr_16bit & 0xE003) == 0xa000:
            rs2 = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2) 
            expanded = 0x00000027 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b011 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
            if(fsIsOff==True):
                ill=1
            else:
                ill=0
            return expanded,ill
           
        #C.sw  RVI的SW格式形如：| imm[11:5]| rs2 | rs1 | 010 | imm[4:0] | 0100011 |
        elif (rvc_instr_16bit & 0xE003) == 0xC000:
            rs2 = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x1) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)| (((rvc_instr_16bit >> 5) & 0x2) << 1) 
            expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b010 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
            return expanded,ill
        #C.sd
        elif (rvc_instr_16bit & 0xE003) == 0xE000:
            rs2 = 8 + ((rvc_instr_16bit >> 2) & 0x7)
            rs1 = 8 + ((rvc_instr_16bit >> 7) & 0x7)
            nzuimm = (((rvc_instr_16bit >> 5) & 0x3) << 6) | (((rvc_instr_16bit >> 5) & 0xE0) >>2)
            expanded = 0x00000023 | ((nzuimm & 0x1F) << 7) | (rs2 << 20) |(0b011 <<12) |(rs1 << 15) |((nzuimm & 0xFE0) << 20)# 
            return expanded,ill
        else:
            return expanded,ill
        
     elif opcode == 0b01:
        #C.addi
        if (rvc_instr_16bit & 0xE003) == 0x0001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            rs1 = ((rvc_instr_16bit >> 7) & 0x1F)
            if ((rvc_instr_16bit >> 12) & 0x1):
                nzuimm = 0xFE0 | ((rvc_instr_16bit >> 2) & 0x1F) 
            else:
                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) 
            expanded = 0x00000013 | (rd << 7) | (0b000 << 12) |(rs1 << 15) | (nzuimm  << 20) # 
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0x2001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            rs1 = ((rvc_instr_16bit >> 7) & 0x1F)
            if ((rvc_instr_16bit >> 12) & 0x1):
                nzuimm = 0xFE0 | ((rvc_instr_16bit >> 2) & 0x1F) 
            else:
                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) 
            expanded = 0x0000001B | (rd << 7) | (0b000 << 12) |(rs1 << 15) | (nzuimm  << 20) # 
            if (rd == 0):
                ill = 1
            
            return expanded,ill

        elif (rvc_instr_16bit & 0xE003) == 0x4001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            if ((rvc_instr_16bit >> 12) & 0x1):
                nzuimm = 0xFE0 | ((rvc_instr_16bit >> 2) & 0x1F) 
            else:
                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) 
            expanded = 0x00000013 | (rd << 7) | (0b000 << 12) |(0b00000 << 15) | (nzuimm  << 20) # 
          
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0x6001:
            rd  = ((rvc_instr_16bit >> 7) & 0x1F)
            if(rd == 2) or (rd == 0):
                if ((rvc_instr_16bit >> 12) & 0x1):
                    nzuimm=0xE00|(((rvc_instr_16bit>>2)&0x1)<<5)|(((rvc_instr_16bit>>3)&0x3)<<7)|(((rvc_instr_16bit>>5)&0x1)<<6)|(((rvc_instr_16bit>>6)&0x1)<<4)  
                else:
                    nzuimm=0x000|(((rvc_instr_16bit>>2)&0x1)<<5)|(((rvc_instr_16bit>>3)&0x3)<<7)|(((rvc_instr_16bit>>5)&0x1)<<6)|(((rvc_instr_16bit>>6)&0x1)<<4) 
                if(nzuimm == 0):
                    ill = 1
                expanded = 0x00000013 | (rd << 7) | (0b000 << 12) |(rd << 15) | (nzuimm  << 20) #     
            else:#lui  lui指令的格式形如： | imm[31:12] | rd | 0110111 |        
                if ((rvc_instr_16bit >> 12) & 0x1):
                    nzuimm = 0xFFFE0000 | (((rvc_instr_16bit >> 2) & 0x1F) << 12)
                else:
                    nzuimm = 0x00000000 | (((rvc_instr_16bit >> 2) & 0x1F) << 12)
                expanded = 0x00000037 | (rd << 7) | (nzuimm)
                if(nzuimm == 0):
                    ill = 1
                    expanded = 0x0000007F

            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0x8001:
            fun6  = (rvc_instr_16bit>>10) & 0x3F
            fun2  = (rvc_instr_16bit>>5 ) & 0x3
            fun3  = ((rvc_instr_16bit >> 2) & 0x7)
            rd  =  8+((rvc_instr_16bit >> 7) & 0x7)
            rs2  = 8+((rvc_instr_16bit >> 2) & 0x7)
            nzuimm = (rvc_instr_16bit>>2)&0x1F
            if(fun6 == 0x20):#SRLI
                expanded = 0x00000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)
                return expanded,ill
            elif(fun6 == 0x24):#SRLI
                expanded = 0x02000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)
                return expanded,ill
            elif(fun6 == 0x21):#SRAI
                expanded = 0x00000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)|(0b0100000<<25)
                return expanded,ill
            elif(fun6 == 0x25):#SRAI
                expanded = 0x00000013 | (rd << 7) |0b101<<12| (rd << 15)| (nzuimm<<20)|(0b0100001<<25)
                return expanded,ill
            elif(fun6 == 0x22):#andi
                expanded = 0x00000013 | (rd << 7) |0b111<<12| (rd << 15)| (nzuimm<<20)
                return expanded,ill
            elif(fun6 == 0x26):#andi
                expanded = 0x00000013 | (rd << 7) |0b111<<12| (rd << 15)| (nzuimm<<20)|(0b1111111<<25)
                return expanded,ill
            elif(fun6 == 0x23):#sub/xor/or/and
                if(fun2 == 0b00):#sub
                    expanded = 0x00000033 | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0100000<<25)
                    return expanded,ill
                elif(fun2 == 0b01):#xor
                    expanded = 0x00000033 | (rd << 7) |0b100<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
                elif(fun2 == 0b10):#or
                    expanded = 0x00000033 | (rd << 7) |0b110<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
                elif(fun2 == 0b11):
                    expanded = 0x00000033 | (rd << 7) |0b111<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
            elif(fun6 == 0x27):# C.subw/addw/mul/not/zext.b/sext.b/zext.h/sext.h/zext.w/
                if(fun2 == 0b00):#subw
                    expanded = 0x0000003B | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0100000<<25)
                    return expanded,ill
                elif(fun2 == 0b01):#addw
                    expanded = 0x0000003B | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0000000<<25)
                    return expanded,ill
                elif(fun2 == 0b10):#mul
                    expanded = 0x00000033 | (rd << 7) |0b000<<12| (rd << 15)| (rs2<<20)|(0b0000001<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b000):#zext.b
                    expanded = 0x0ff00013 | (rd << 7) |0b111<<12| (rd << 15)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b001):#sext.b
                    expanded = 0x00000013 | (rd << 7) |0b001<<12| (rd << 15)|(0b00100<<20)|(0b0110000<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b010):#zext.h
                    expanded = 0x0000003B | (rd << 7) |0b100<<12| (rd << 15)|(0b00000<<20)|(0b0000100<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b011):#sext.h
                    expanded = 0x00000013 | (rd << 7) |0b001<<12| (rd << 15)|(0b00101<<20)|(0b0110000<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b100):#zext.w
                    expanded = 0x0000003B | (rd << 7) |0b000<<12| (rd << 15)|(0b00000<<20)|(0b0000100<<25)
                    return expanded,ill
                elif(fun2 == 0b11)&(fun3==0b101):#not
                    expanded = 0xfff00013 | (rd << 7) |0b100<<12| (rd << 15)|(0b00000<<20)
                    return expanded,ill
                else:
                    ill =2
                    return expanded,ill
            else:
                return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0xa001:
            nzuimm = 0xFFFE0000|(((rvc_instr_16bit>>2)&0x1)<<5)|(((rvc_instr_16bit>>2)&0xe))|(((rvc_instr_16bit>>2)&0x10)<<3)|(((rvc_instr_16bit>>2)&0x20)<<1)|(((rvc_instr_16bit>>2)&0x40)<<4)|(((rvc_instr_16bit>>2)&0x180)<<1)|(((rvc_instr_16bit>>2)&0x200)>>5)|(((rvc_instr_16bit>>2)&0x400)<<1)                                                                                                                                          
            if(((rvc_instr_16bit>>2)&0x400)>>10):
                expanded = 0x800FF06F|(0b00000 << 7)|((nzuimm &0x7fe) <<20)|((nzuimm &0x800) <<9)# 
            else: 
                expanded = 0x0000006F|(0b00000 << 7)|((nzuimm &0x7fe) <<20)|((nzuimm &0x800) <<9)# 
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0xc001:
            rs1 = ((rvc_instr_16bit >> 7) & 0x7)+8
            nzuimm = 0xFF & ((((rvc_instr_16bit>>2)&0x1)<<4)|((((rvc_instr_16bit>>2)&0x6)>>1))|(((rvc_instr_16bit>>2)&0x18)<<2)|(((rvc_instr_16bit>>2)&0x300)>>6)|(((rvc_instr_16bit>>2)&0x400)>>3))
            if((((rvc_instr_16bit>>2)&0x400)>>10)):
                expanded = 0xF00000E3|((nzuimm&0x0F)<<8)|rs1<<15|((nzuimm&0xF0)<<21)
            else:
                expanded = 0x00000063|((nzuimm&0x0F)<<8)|rs1<<15|((nzuimm&0xF0)<<21)
            return expanded,ill
        elif (rvc_instr_16bit & 0xE003) == 0xe001:
            rs1 = ((rvc_instr_16bit >> 7) & 0x7)+8
            nzuimm = 0xFF & ((((rvc_instr_16bit>>2)&0x1)<<4)|((((rvc_instr_16bit>>2)&0x6)>>1))|(((rvc_instr_16bit>>2)&0x18)<<2)|(((rvc_instr_16bit>>2)&0x300)>>6)|(((rvc_instr_16bit>>2)&0x400)>>3))
            if((((rvc_instr_16bit>>2)&0x400)>>10)):
                expanded = 0xF00000E3|((nzuimm&0x0F)<<8)|0x001<<12|rs1<<15|((nzuimm&0xF0)<<21)
            else:
                expanded = 0x00000063|((nzuimm&0x0F)<<8)|0x001<<12|rs1<<15|((nzuimm&0xF0)<<21)
            return expanded,ill
     elif opcode == 0b10:
            if (rvc_instr_16bit & 0xE003) == 0x0002:
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = 0x000 | ((rvc_instr_16bit >> 2) & 0x1F) | ((rvc_instr_16bit >> 7) & 0x20)
                expanded = 0x00000013 | (rd << 7) | (0b001 << 12) |(rs1 << 15) | (nzuimm  << 20) # 
               
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x2002:#fldsp
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = (((rvc_instr_16bit >> 2) & 0x7) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x18)
                expanded = 0x00000007 | (rd << 7) | (0b011 << 12) |(0b00010 << 15) | (nzuimm  << 20) # 
                if(fsIsOff==True):
                    ill=1
                else:
                    ill=0
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x4002:#lwsp
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = (((rvc_instr_16bit >> 2) & 0x3) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x1c)
                expanded = 0x00000003 | (rd << 7) | (0b010 << 12) |(0b00010 << 15) | (nzuimm  << 20) # 
                if (rd == 0):
                    ill = 1
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x6002:#ldsp
                rd  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs1 = ((rvc_instr_16bit >> 7) & 0x1F)

                nzuimm = (((rvc_instr_16bit >> 2) & 0x7) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x18)
                expanded = 0x00000003 | (rd << 7) | (0b011 << 12) |(0b00010 << 15) | (nzuimm  << 20) # 
                if (rd == 0):
                    ill = 1
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0x8002:#JR/MV/EBREAK/JALR/ADD
                rs1  = ((rvc_instr_16bit >> 7) & 0x1F)
                rs2 =  ((rvc_instr_16bit >> 2) & 0x1F)
                funct4 = (rvc_instr_16bit>>12)&0x1
                nzuimm = (((rvc_instr_16bit >> 2) & 0x7) <<6) | ((rvc_instr_16bit >> 7) & 0x20) | ((rvc_instr_16bit >> 2) & 0x18)
                if((funct4==0)&(rs2==0)&(rs1!=0)): #JR
                    expanded = 0x00000067 | (0b00000 << 7) | (0b000 << 12) |(rs1 << 15) # 
                elif(funct4==0)&(rs2!=0):#&(rs1!=0)):#MV  0000000 rs2 rs1 000 rd 0110011 ADD
                    expanded = 0x00000013 | (rs1 << 7) | (0b000 << 12) |(rs2 << 15)  # 
                elif((funct4==1)&(rs2==0)&(rs1==0)): #ebreak
                    expanded = 0b00000000000100000000000001110011
                elif((funct4==1)&(rs2==0)&(rs1!=0)): #jalr
                    expanded = 0x00000067 | (0b00001 << 7) | (0b000 << 12) |(rs1 << 15) #
                elif(funct4==1)&(rs2!=0):#&(rs1!=0)): #add
                    expanded = 0x00000033 | (rs1 << 7) | (0b000 << 12) |(rs1 << 15) |(rs2 << 20) #              
                else: 
                    ill = 1
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0xa002:#fsdsp
                rs2 = ((rvc_instr_16bit >> 2) & 0x1F)
                nzuimm = ((rvc_instr_16bit >> 1) & 0x1C0) | ((rvc_instr_16bit >> 7) & 0x38) 
                expanded = 0x00000027 |((nzuimm & 0x1F)<<7)| (0b011 << 12 ) |  (0b00010 << 15)| (rs2 << 20)| ((nzuimm&0xFE0)<< 20) # 
                if(fsIsOff==True):
                    ill=1
                else:
                    ill=0
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0xc002:#swsp
                rs2 = ((rvc_instr_16bit >> 2) & 0x1F)
                nzuimm = ((rvc_instr_16bit >> 1) & 0xC0) | ((rvc_instr_16bit >> 7) & 0x3C) 
                expanded = 0x00000023 |((nzuimm & 0x1F)<<7)| (0b010 << 12 ) |  (0b00010 << 15)| (rs2 << 20)| ((nzuimm&0xFE0)<< 20) # 
              
                return expanded,ill
            elif (rvc_instr_16bit & 0xE003) == 0xE002:#sdsp
                rs2 = ((rvc_instr_16bit >> 2) & 0x1F)
                nzuimm = ((rvc_instr_16bit >> 1) & 0x1C0) | ((rvc_instr_16bit >> 7) & 0x38) 
                expanded = 0x00000023 |((nzuimm & 0x1F)<<7)| (0b011 << 12 ) |  (0b00010 << 15)| (rs2 << 20)| ((nzuimm&0xFE0)<< 20) # 
              
                return expanded,ill
            else:
                return expanded,ill
        
#        elif (rvc_instr_16bit & 0xE003) == 0x4000:  
        # 其他00格式指令...



