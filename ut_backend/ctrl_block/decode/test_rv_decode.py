#coding=utf8

import ctypes
from ut_backend.ctrl_block.decode.env.decode_wrapper import *
from dut.predecode.UT_PreDecode import *
from dut.decodestage.UT_DecodeStage import *
from tools.insn_gen import *
from tools.disasm import libdisasm
from comm import TAG_LONG_TIME_RUN, debug
from dut.rvcexpander.UT_RVCExpander import *


# rvc test
def rvc_expand(full_inst):
    if full_inst:
        ref_insts  = generate_rvc_instructions()
    else:
        ref_insts  = generate_random_32bits(1)
    rvc_expand = DUTRVCExpander()
    rvc_expand.io_in.AsImmWrite()
    debug("###################### test_rvc_expand ##########################")
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
    rvc_expand(False)


@pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
def test_rvc_expand_full():
    rvc_expand(True)


# rvc test, processed by the decoder module
@pytest.mark.toffee_tags(version="openxiangshan-kmh-97e37a2237-24092702 < openxiangshan-kmh-97e37a2237-24092703")
def test_rvc_inst(decoder_fixture):
    debug("###################### test_rvc_inst ##########################")
    decoder = decoder_fixture
    need_log_file   = True
    # insn_list_temp  = generate_rvc_instructions()
    insn_list_temp  = generate_random_32bits(1)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    decode_run(decoder, ref_lists, need_log_file,"test_rvc_inst")
    g.add_cover_point(decoder, {"fast_check_RVC_ramdom": lambda _: True}, name="RVC").sample()


# randomly generate instructions for testing
def test_rvi_inst(decoder_fixture):
    debug("###################### test_rvi_inst ##########################")
    decoder = decoder_fixture
    need_log_file   = True
    insn_list_temp  = generate_random_32bits(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    decode_run(decoder, ref_lists, need_log_file,"test_rvi_inst")
    g.add_cover_point(decoder, {"fast_check_random_32bit_int": lambda _: True}, name="RVI").sample()


# testing of V extension instructions, which are not actually used
def test_rv_custom_inst(decoder_fixture):
    debug("###################### test_rv_custom_inst ##########################")
    decoder = decoder_fixture
    need_log_file   = True
    custom_v_opcode   = 0b1010111
    insn_list_temp  = generate_OP_V_insn(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm_custom_insn, libdisasm.disasm_free_mem, custom_v_opcode)
    decode_run(decoder, ref_lists, need_log_file,"test_rv_custom_inst")
    g.add_cover_point(decoder, {"fast_check_OP_V_insn": lambda _: True}, name="RVI_Costom").sample()
