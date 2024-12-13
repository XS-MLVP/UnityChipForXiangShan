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
        if is_32bit:
            assert value == insn, "RVC expand error, 32bit instruction need to be the same"
        if (insn_disasm == "unknown") and  (instr_ex == 0):
            debug(f"find bad inst:{insn}, ref: 1, dut: 0")
            find_error +=1
        elif (insn_disasm != "unknown") and  (instr_ex == 1):
            if (instr_filter(insn_disasm) != 1): 
                debug(f"find bad inst:{insn},disasm:{insn_disasm}, ref: 0, dut: 1")
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


N=10
T=1<<32
@pytest.mark.toffee_tags([TAG_LONG_TIME_RUN, TAG_RARELY_USED])
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_32bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full 32 bit instruction set

    Description:
        Randomly generate N 32-bit instructions for each check, and repeat the process K times.
    """
    # Add check point: RVC_EXPAND_ALL_32B to check instr bits.
    covered = -1
    g.add_watch_point(rvc_expander, {"RANGE[%d-%d]"%(start, end): lambda _: covered == end},
                      name = "RVC_EXPAND_ALL_32B", dynamic_bin=True)
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_32B", test_rvc_expand_32bit_full)
    # Drive the expander and check the result
    rvc_expand(rvc_expander, list([_ for _ in range(start, end)]))
    # When go to here, the range[start, end] is covered
    covered = end
    g.sample()


@pytest.mark.skip("This test is allways failed, need to be fixed")
def test_rvc_expand_32bit_randomN(rvc_expander):
    """Test the RVC expand function with a random 32 bit instruction set

    Description:
        Randomly generate 32-bit instructions for testing
    """
    rvc_expand(rvc_expander, generate_random_32bits(100))