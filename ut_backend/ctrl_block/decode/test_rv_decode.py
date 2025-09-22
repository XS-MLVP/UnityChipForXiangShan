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


@toffee_test.testcase
async def test_rvc_inst(decoder, rvc_expander):
    """
    Test the RVC instruction set, an example of the tag version in range.

    Args:
        decoder (fixure): the fixture of the decoder
    """
    need_log_file   = True
    # insn_list_temp  = generate_rvc_instructions()
    insn_list_temp  = generate_random_32bits(1)
    ref_lists       = convert_reference_format(rvc_expander, insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    assert decode_run(decoder, ref_lists, need_log_file,"test_rvc_inst") == True, "RVC decode error"
    g.add_cover_point(decoder, {"fast_check_RVC_ramdom": lambda _: True}, name="RVC").sample()
    g.mark_function("RVC", test_rvc_inst, bin_name="fast_check_RVC_ramdom")


@toffee_test.testcase
async def test_rvi_inst(decoder, rvc_expander):
    """
    Test the RVI instruction set. randomly generate instructions for testing

    Args:
        decoder (fixure): the fixture of the decoder
    """
    need_log_file   = True
    insn_list_temp  = generate_random_32bits(100)
    ref_lists       = convert_reference_format(rvc_expander, insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    assert decode_run(decoder, ref_lists, need_log_file,"test_rvi_inst") == True, "RVI decode error"
    g.add_cover_point(decoder, {"illegal_inst_triggers_an_exception": lambda _: decoder.Get_decode_checkpoint_illeagl_inst() != 0}, name="RVI_illegal_inst").sample()
    g.add_cover_point(decoder, {"fast_check_random_32bit_int": lambda _: True}, name="RVI").sample()


@toffee_test.testcase
async def test_rv_custom_inst(decoder, rvc_expander):
    """
    Test the custom instruction set. Testing of V extension instructions, which are not actually used

    Args:
        decoder (fixure): the fixture of the decoder
    """
    need_log_file   = True
    custom_v_opcode   = 0b1010111
    insn_list_temp  = generate_OP_V_insn(100)
    ref_lists       = convert_reference_format(rvc_expander, insn_list_temp, True, libdisasm.disasm_custom_insn, libdisasm.disasm_free_mem, custom_v_opcode)
    assert decode_run(decoder, ref_lists, need_log_file,"test_rv_custom_inst") == True, "RVI decode error"
    g.add_cover_point(decoder, {"input_data_contains_complex_insts": lambda _: decoder.Get_decode_checkpoint_complex_inst() != 0}, name="RVI_complex_inst").sample()
    g.add_cover_point(decoder, {"fast_check_OP_V_insn": lambda _: True}, name="RVI_Costom").sample()
