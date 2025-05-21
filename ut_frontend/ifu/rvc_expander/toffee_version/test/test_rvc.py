from tools.insn_gen import *
from tools.disasm import disasmbly, libdisasm
from comm import TAG_LONG_TIME_RUN, TAG_SMOKE, TAG_RARELY_USED, debug
import pytest
from .rvc_expander_fixture import gr, rvc_expander
import toffee_test
from ..env import RVCExpanderEnv

async def rvc_expand(rvc_expander, ref_insts, is_32bit=False):
    """compare the RVC expand result with the reference

    Args:
        rvc_expander (warpper): the fixture of the RVC expander
        ref_insts (list[int]]): the reference instruction list
    """
    find_error = 0
    for insn in ref_insts:
        insn_disasm = disasmbly(insn)
        value, instr_ex = await rvc_expander.expand(insn, False)
        if is_32bit:
            assert value == insn, "RVC expand error, 32bit instruction need to be the same"
            assert instr_ex == False, "RVC expand error, 32bit instruction is always not illegal"
        else:
            if (insn_disasm == "unknown") and  (instr_ex == 0):
                debug(f"find bad inst:{insn}, ref: 1, dut: 0")
                find_error +=1
            elif (insn_disasm != "unknown") and  (instr_ex == 1):
                if (instr_filter(insn_disasm) != 1): 
                    debug(f"find bad inst:{insn},disasm:{insn_disasm},dut_ex:{value} ref: 0, dut: 1")
                    find_error += 1
    assert 0 == find_error, "RVC expand error (%d errros)" % find_error


# Filter out certain cases where exception can be identified through instruction itself, 
# Supplement with the exception detection situation of the reference model.
def instr_filter(insn_disasm_text):
    instr_opcode = insn_disasm_text.split(' ')[0]
    is_except = 0
    if (instr_opcode == "c.lwsp" or instr_opcode == "c.ldsp" or instr_opcode == "c.addiw"):
        dst = insn_disasm_text.split()[1].split(',')[0]
        if dst == "zero":
            is_except = 1
    elif (instr_opcode == "c.addi4spn"):
        imm = insn_disasm_text.split()[3]
        if imm == "0":
            is_except = 1
    elif (instr_opcode == "c.addi16sp"):
        imm = insn_disasm_text.split()[2]
        if imm == "0":
            is_except = 1
    elif (instr_opcode == "c.lui"):
        imm = insn_disasm_text.split()[2]
        if imm == "0x0":
            is_except = 1
    elif (instr_opcode == "c.jr"):
        rs1 = insn_disasm_text.split()[1]
        if rs1 == "zero":
            is_except = 1
    elif (instr_opcode == "c.unimp"):
        is_except = 1
    return is_except

# @pytest.mark.toffee_tags(TAG_SMOKE)
# @toffee_test.testcase
# async def test_rvc_expand_32bit_smoke(rvc_expander: RVCExpanderEnv):
#     """
#     Test the RVC expand function with 1 fixed 32 bit instruction
#     """
#     await rvc_expand(rvc_expander.agent, [873825667])


# # @pytest.mark.toffee_tags(TAG_SMOKE)
# @toffee_test.testcase
# async def test_rvc_expand_16bit_smoke(rvc_expander: RVCExpanderEnv):
#     """
#     Test the RVC expand function with 1 compressed instruction
#     """
#     await rvc_expand(rvc_expander.agent, generate_rvc_instructions(start=90, end=101))


# N = 10
# T = 1<<16
# @pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
# @pytest.mark.parametrize("start,end",
#                          [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
# @toffee_test.testcase
# async def test_rvc_expand_16bit_full(rvc_expander: RVCExpanderEnv, start, end):
#     """Test the RVC expand function with a full compressed instruction set
    
#     Description:
#         Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
#     """
#     # Add check point: RVC_EXPAND_RANGE to check expander input range.
#     #   When run to here, the range[start, end] is covered
#     covered = -1
#     gr.add_watch_point(rvc_expander, {
#                                 "RANGE[%d-%d]"%(start, end): lambda _: covered == end
#                           }, name = "RVC_EXPAND_ALL_16B", dynamic_bin=True)
#     # Reverse mark function to the check point
#     gr.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]"%(start, end))
#     # Drive the expander and check the result
#     await rvc_expand(rvc_expander.agent, generate_rvc_instructions(start, end))
#     # When go to here, the range[start, end] is covered
#     # covered = end
#     # gr.sample()


# N=10
# T=1<<32
# @pytest.mark.toffee_tags([TAG_LONG_TIME_RUN, TAG_RARELY_USED])
# @pytest.mark.parametrize("start,end",
#                          [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
# @toffee_test.testcase
# async def test_rvc_expand_32bit_full(rvc_expander: RVCExpanderEnv, start, end):
#     """Test the RVC expand function with a full 32 bit instruction set

#     Description:
#         Randomly generate N 32-bit instructions for each check, and repeat the process K times.
#     """
#     # Add check point: RVC_EXPAND_ALL_32B to check instr bits.
#     covered = -1
#     gr.add_watch_point(rvc_expander, {"RANGE[%d-%d]"%(start, end): lambda _: covered == end},
#                       name = "RVC_EXPAND_ALL_32B", dynamic_bin=True)
#     # Reverse mark function to the check point
#     gr.mark_function("RVC_EXPAND_ALL_32B", test_rvc_expand_32bit_full)
#     # Drive the expander and check the result
#     await rvc_expand(rvc_expander.agent, list([_ for _ in range(start, end)]))
#     # When go to here, the range[start, end] is covered
#     covered = end
#     # gr.sample()


# @pytest.mark.skip("This test is allways failed, need to be fixed")
# @toffee_test.testcase
# def test_rvc_expand_32bit_randomN(rvc_expander: RVCExpanderEnv):
#     """Test the RVC expand function with a random 32 bit instruction set

#     Description:
#         Randomly generate 32-bit instructions for testing
#     """
#     rvc_expand(rvc_expander.agent, generate_random_32bits(100))
