#coding=utf8

import ctypes
from ut_backend.ctrl_block.decode.env.decode_wrapper import *
from dut.predecode.UT_PreDecode import *
from dut.decodestage.UT_DecodeStage import *
from tools.insn_gen import *
from tools.disasm import libdisasm
from comm import TAG_LONG_TIME_RUN, debug
from dut.rvcexpander.UT_RVCExpander import *


def rvc_expand(full_inst):
    """
    Test the RVC expansion function

    @param full_inst: whether to use a full instruction set
    """
    if full_inst:
        ref_insts  = generate_rvc_instructions()
    else:
        ref_insts  = generate_random_32bits(1)
    rvc_expand = DUTRVCExpander()
    rvc_expand.io_in.AsImmWrite()
    for insn in ref_insts:
        c_void_ptr = libdisasm.disasm(ctypes.c_uint64(insn))
        insn_disasm = ctypes.cast(c_void_ptr, ctypes.c_char_p).value.decode('utf-8')
        libdisasm.disasm_free_mem(c_void_ptr)

        rvc_expand.io_in.value = insn
        rvc_expand.RefreshComb()
        instr_ex    = rvc_expand.io_ill.value
        instr_bits  = rvc_expand.io_out_bits.value
        if (insn_disasm == "unknown") and  (instr_ex == 0):
            debug(f"--- bad --- inst:{insn}, ref: 1, dut: 0")
        elif (insn_disasm != "unknown") and  (instr_ex == 1):
            debug(f"--- bad --- inst:{insn}, ref: 0, dut: 1")


def test_rvc_expand():
    """
    Test the RVC expansion function with a partial instruction set
    """
    rvc_expand(False)


@pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
def test_rvc_expand_full():
    """
    Test the RVC expansion function with a full instruction set
    """
    rvc_expand(True)


@pytest.mark.toffee_tags(version="openxiangshan-kmh-97e37a2237-24092701 < openxiangshan-kmh-97e37a2237-24092703")
def test_rvc_inst(decoder_fixture):
    """
    Test the RVC instruction set, an example of the tag version in range.

    @param decoder_fixture: the fixture of the decoder
    """
    decoder = decoder_fixture
    need_log_file   = True
    # insn_list_temp  = generate_rvc_instructions()
    insn_list_temp  = generate_random_32bits(1)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    decode_run(decoder, ref_lists, need_log_file,"test_rvc_inst")
    g.add_cover_point(decoder, {"fast_check_RVC_ramdom": lambda _: True}, name="RVC").sample()


def test_rvi_inst(decoder_fixture):
    """
    Test the RVI instruction set. randomly generate instructions for testing

    @param decoder_fixture: the fixture of the decoder
    """
    decoder = decoder_fixture
    need_log_file   = True
    insn_list_temp  = generate_random_32bits(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    decode_run(decoder, ref_lists, need_log_file,"test_rvi_inst")
    g.add_cover_point(decoder, {"fast_check_random_32bit_int": lambda _: True}, name="RVI").sample()


def test_rv_custom_inst(decoder_fixture):
    """
    Test the custom instruction set. Testing of V extension instructions, which are not actually used

    @param decoder_fixture: the fixture of the decoder
    """
    decoder = decoder_fixture
    need_log_file   = True
    custom_v_opcode   = 0b1010111
    insn_list_temp  = generate_OP_V_insn(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm_custom_insn, libdisasm.disasm_free_mem, custom_v_opcode)
    decode_run(decoder, ref_lists, need_log_file,"test_rv_custom_inst")
    g.add_cover_point(decoder, {"fast_check_OP_V_insn": lambda _: True}, name="RVI_Costom").sample()
