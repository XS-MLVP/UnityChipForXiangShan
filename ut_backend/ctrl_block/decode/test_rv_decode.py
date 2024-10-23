#coding=utf8

import mlvp
import ctypes
from ut_backend.ctrl_block.decode.env.decode_wrapper import *
from dut.predecode.UT_PreDecode import *
from dut.decodestage.UT_DecodeStage import *
from tools.insn_gen import *
from tools.disasm import libdisasm
from comm.functions import is_short_test
from dut.rvcexpander.UT_RVCExpander import *


# rvc 测试
def rvc_expand(full_inst):
    if full_inst:
        ref_insts  = generate_rvc_instructions()
    else:
        ref_insts  = generate_random_32bits(1)
    rvc_expand = DUTRVCExpander()
    rvc_expand.io_in.AsImmWrite()
    mlvp.info("###################### test_rvc_expand ##########################")
    for insn in ref_insts:
        c_void_ptr = libdisasm.disasm(ctypes.c_uint64(insn))
        insn_disasm = ctypes.cast(c_void_ptr, ctypes.c_char_p).value.decode('utf-8')
        libdisasm.disasm_free_mem(c_void_ptr)

        rvc_expand.io_in.value = insn
        rvc_expand.RefreshComb()
        instr_ex    = rvc_expand.io_ill.value
        instr_bits  = rvc_expand.io_out_bits.value
        if (insn_disasm == "unknown") and  (instr_ex == 0):
            mlvp.info(f"--- bad --- inst:{insn}, ref: 1, dut: 0")
        elif (insn_disasm != "unknown") and  (instr_ex == 1):
            mlvp.info(f"--- bad --- inst:{insn}, ref: 0, dut: 1")


def test_rvc_expand():
    rvc_expand(False)


@pytest.mark.skipif(is_short_test(), reason="Ignore run long execution times test in short test mode.")
def test_rvc_expand_full():
    rvc_expand(True)


# rvc 测试
def test_rvc_inst(decoder_fixture):
    mlvp.info("###################### test_rvc_inst ##########################")
    decoder = decoder_fixture
    need_log_file   = True
    # insn_list_temp  = generate_rvc_instructions()
    insn_list_temp  = generate_random_32bits(1)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    decode_run(decoder, ref_lists, need_log_file,"test_rvc_inst")


# 对指令进行随机测试
def test_rvi_inst(decoder_fixture):
    mlvp.info("###################### test_rvi_inst ##########################")
    decoder = decoder_fixture
    need_log_file   = True
    insn_list_temp  = generate_random_32bits(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
    decode_run(decoder, ref_lists, need_log_file,"test_rvi_inst")


# V扩展指令的测试，实际未使用
def test_rv_custom_inst(decoder_fixture):
    mlvp.info("###################### test_rv_custom_inst ##########################")
    decoder = decoder_fixture
    need_log_file   = True
    custom_v_opcode   = 0b1010111
    insn_list_temp  = generate_OP_V_insn(100)
    ref_lists       = convert_reference_format(insn_list_temp, True, libdisasm.disasm_custom_insn, libdisasm.disasm_free_mem, custom_v_opcode)
    decode_run(decoder, ref_lists, need_log_file,"test_rv_custom_inst")
