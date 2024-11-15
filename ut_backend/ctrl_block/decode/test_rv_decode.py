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


def rvc_expand(rvc_expander, ref_insts):
    """compare the RVC expand result with the reference

    Args:
        rvc_expander (warpper): the fixture of the RVC expander
        ref_insts (list[int]]): the reference instruction list
    """
    find_error = 0
    for insn in ref_insts:
        insn_disasm = disasmbly(insn)
        _, instr_ex = rvc_expander.expand(insn)
        if (insn_disasm == "unknown") and  (instr_ex == 0):
            debug(f"find bad inst:{insn}, ref: 1, dut: 0")
            find_error +=1
        elif (insn_disasm != "unknown") and  (instr_ex == 1):
            debug(f"find bad inst:{insn}, ref: 0, dut: 1")
            find_error +=1
    assert 0 == find_error, "RVC expand error (%d errros)" % find_error


@pytest.mark.toffee_tags(TAG_SMOKE)
def test_rvc_expand_32bit_smoke(rvc_expander):
    """
    Test the RVC expand function with 1 fixed 32 bit instruction
    """
    rvc_expand(rvc_expander, [873825667])


@pytest.mark.toffee_tags(TAG_SMOKE)
def test_rvc_expand_16bit_smoke(rvc_expander):
    """
    Test the RVC expand function with 1 compressed instruction
    """
    rvc_expand(rvc_expander, generate_rvc_instructions(start=100, end=101))


N = 10
T = 1<<16
@pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_16bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full compressed instruction set
    
    Description:
        Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
    """
    # Add check point: RVC_EXPAND_RANGE to check expander input range.
    #   When run to here, the range[start, end] is covered
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]"%(start, end): lambda _: True
                          }, name = "RVC_EXPAND_16B_RANGE").sample()

    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_16B_RANGE", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]"%(start, end))
    g.mark_function("RVC_EXPAND_RET", test_rvc_expand_16bit_full)

    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end))


N=100000
K=10
@pytest.mark.toffee_tags([TAG_LONG_TIME_RUN, TAG_RARELY_USED])
@pytest.mark.parametrize("N", [N for _ in range(K)])
def test_rvc_expand_32bit_randomN(rvc_expander, N):
    """Test the RVC expand function with a full 32 bit instruction set
    
    Description:
        Randomly generate N 32-bit instructions for each check, and repeat the process K times.
    """
    # Add check point: RVC_EXPAND_32B_BITS to check instr bits.
    def check_bits(i):
        return lambda x: (x.stat()["instr"] & 1<<i) != 0
    g.add_watch_point(rvc_expander, {"POS_%d"%i: check_bits(i) for i in range(32)}, 
                      name = "RVC_EXPAND_32B_BITS")
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_32B_BITS", test_rvc_expand_32bit_randomN)
    g.mark_function("RVC_EXPAND_RET", test_rvc_expand_32bit_randomN)
    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_random_32bits(N))


@pytest.mark.toffee_tags(version="openxiangshan-kmh-97e37a2237-24092701 < openxiangshan-kmh-97e37a2237-24092703")
def test_rvc_inst(decoder):
    """
    Test the RVC instruction set, an example of the tag version in range.

    Args:
        decoder (fixure): the fixture of the decoder
    """
    need_log_file   = True
    # insn_list_temp  = generate_rvc_instructions()
    insn_list_temp  = generate_random_32bits(1)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    assert decode_run(decoder, ref_lists, need_log_file,"test_rvc_inst") == True, "RVC decode error"
    g.add_cover_point(decoder, {"fast_check_RVC_ramdom": lambda _: True}, name="RVC").sample()
    g.mark_function("RVC", test_rvc_inst, bin_name="fast_check_RVC_ramdom")


def test_rvi_inst(decoder):
    """
    Test the RVI instruction set. randomly generate instructions for testing

    Args:
        decoder (fixure): the fixture of the decoder
    """
    need_log_file   = True
    insn_list_temp  = generate_random_32bits(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    assert decode_run(decoder, ref_lists, need_log_file,"test_rvi_inst") == True, "RVI decode error"
    g.add_cover_point(decoder, {"fast_check_random_32bit_int": lambda _: True}, name="RVI").sample()


def test_rv_custom_inst(decoder):
    """
    Test the custom instruction set. Testing of V extension instructions, which are not actually used

    Args:
        decoder (fixure): the fixture of the decoder
    """
    need_log_file   = True
    custom_v_opcode   = 0b1010111
    insn_list_temp  = generate_OP_V_insn(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm_custom_insn, libdisasm.disasm_free_mem, custom_v_opcode)
    assert decode_run(decoder, ref_lists, need_log_file,"test_rv_custom_inst") == True, "RVI decode error"
    g.add_cover_point(decoder, {"fast_check_OP_V_insn": lambda _: True}, name="RVI_Costom").sample()
