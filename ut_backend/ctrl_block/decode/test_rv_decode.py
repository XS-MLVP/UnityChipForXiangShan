#coding=utf8

import mlvp
import os
import datetime
import pytest
import ctypes
from mlvp.reporter import set_line_coverage
from ut_backend.ctrl_block.decode.env.decode_wrapper import DecodeWrapper
from dut.predecode.UT_PreDecode import *
from dut.decodestage.UT_DecodeStage import *
from comm import get_out_dir
from tools.insn_gen import *
from dut.rvcexpander.UT_RVCExpander import *

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, '..', '..', '..', 'tools', 'disasm', 'build', 'libdisasm.so')

libdisasm = ctypes.CDLL(lib_path)

libdisasm.disasm.argtypes = [ctypes.c_uint64]
libdisasm.disasm.restype = ctypes.c_void_p

libdisasm.disasm_custom_insn.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
libdisasm.disasm_custom_insn.restype = ctypes.c_void_p

libdisasm.disasm_free_mem.argtypes = [ctypes.c_void_p]
libdisasm.disasm_free_mem.restype = None


@pytest.fixture()
def decoder_fixture(request):
    # before test
    func_name = request.node.name
    # 如果输出目录不存在则创建
    output_dir_path = get_out_dir("decoder/log")
    os.makedirs(output_dir_path, exist_ok=True)

    decoder = DecodeWrapper(DUTDecodeStage(
        waveform_filename=get_out_dir("decoder/decode_%s.fst"%func_name),
        coverage_filename=get_out_dir("decoder/decode_%s.dat"%func_name),
    ))
    decoder.dut.InitClock("clock")
    # decoder.dut.io_in_0_valid.AsImmWrite()
    # decoder.dut.io_in_0_bits_instr.AsImmWrite()
    yield decoder
    # after test
    decoder.dut.Finish()
    coverage_file = get_out_dir("decoder/decode_%s.dat"%func_name)
    if not os.path.exists(coverage_file):
        raise FileNotFoundError(f"File not found: {coverage_file}")
    set_line_coverage(request, coverage_file)

#################### Test cases Start From Here ####################


def comapre_result(ref_value_list, dut_value_list, num):
    if num == 0:
        return
    else:
        for i in range(num):
            if ref_value_list[i][1] != dut_value_list[i][1]:
                mlvp.info("================================")
                mlvp.info(ref_value_list[i])
                mlvp.info(dut_value_list[i])

log_all_info_file = None
log_err_info_file = None

def open_log_file(name):
    global log_all_info_file
    global log_err_info_file
    # 获取当前时间并格式化
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = get_out_dir("decoder/log/")
    # 创建文件名
    if name is not None:
        filename_all = output_dir + f"log_all_{name}.txt"
        filename_err = output_dir + f"log_err_{name}.txt"
    else:
        filename_all = output_dir + f"log_all_{current_time}.txt"
        filename_err = output_dir + f"log_err_{current_time}.txt"

    log_all_info_file   = open(filename_all, 'w')
    log_all_info_file.close()
    log_all_info_file   = open(filename_all, 'a')

    log_err_info_file   = open(filename_err, 'w')
    log_err_info_file.close()
    log_err_info_file   = open(filename_err, 'a')

def close_log_file():
    if log_all_info_file is not None:
        log_all_info_file.close()

    if log_err_info_file is not None:
        log_err_info_file.close()


def write_all_info_to_file(info):
    if log_all_info_file is not None:
        log_all_info_file.write(info + "\n")
    else:
        mlvp.info("remember open_log_file , close_log_file")

def write_err_info_to_file(info):
    if log_err_info_file is not None:
        log_err_info_file.write(info + "\n")
    else:
        mlvp.info("remember open_log_file , close_log_file")

# 将比较结果写入文件中。
# ref_value_list[i][0] = 指令十进制显示, ref_value_list[i][1] = 参考结果判断指令是否异常, ref_value_list[i][2] = 指令反汇编结果，ref_value_list[i][3] = 经过RVCExpander 初步初筛是否异常指令。 
# dut_value_list[i][0] = Decoder输出的指令十进制， dut_value_list[i][1] = Decoder是否判定为异常，dut_value_list[i][2] = Decoder是否判定为复杂指令
def comapre_result_in_text(ref_value_list, dut_value_list, num):
    if num == 0:
        return
    else:
        for i in range(num):
            # 暂时不改为assert，先完善功能。assert 直接停止执行了。
            if (ref_value_list[i][2] == 0 or (ref_value_list[i][0] == dut_value_list[i][0])) and (ref_value_list[i][1] == dut_value_list[i][1]):
                # print("Meets expectations:（￣︶￣）↗")
                good_info = f"good  ----- ref: {ref_value_list[i][0]}, {ref_value_list[i][1]}, {ref_value_list[i][2]}, {ref_value_list[i][3]}"
                write_all_info_to_file(good_info)
            else:
                # print("Not meeting expectations: <(_ _)>")
                bad_info =  f"bad   ----- ref: {ref_value_list[i][0]}, {ref_value_list[i][1]}, {ref_value_list[i][2]}, {ref_value_list[i][3]}, old inst: {ref_value_list[i][4]},   dut: {dut_value_list[i][0]}, {dut_value_list[i][1]}, complex: {dut_value_list[i][2] == 0}"
                write_all_info_to_file(bad_info)
                if(ref_value_list[i][2][0] != 'v'):
                    write_err_info_to_file(bad_info)

# 对部分能通过指令判断出异常的情况进行过滤，-- 补充参考模型的异常判断情况
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

# 对指令进行反汇编，送入rvc_expand进行压缩指令的译码
def convert_reference_format(ref_insts, need_expand, disasm_func, disasm_free_func, disasm_arg = 0):
    rvc_expand = DUTRVCExpander()
    rvc_expand.io_in.AsImmWrite()
    inst_list = []
    for insn in ref_insts:
        c_void_ptr = disasm_func(ctypes.c_uint64(insn), disasm_arg)
        insn_disasm = ctypes.cast(c_void_ptr, ctypes.c_char_p).value.decode('utf-8')
        disasm_free_func(c_void_ptr)

        if need_expand == True:
            rvc_expand.io_in.value = insn
            rvc_expand.RefreshComb()
            instr_ex    = rvc_expand.io_ill.value
            instr_bits  = rvc_expand.io_out_bits.value
        else:
            instr_ex    = 0
            instr_bits  = insn

        if insn_disasm == "unknown":
            inst_list.append((instr_bits, 1, insn_disasm, instr_ex, insn))
        else:
            is_excpet = instr_filter(insn_disasm)
            inst_list.append((instr_bits, is_excpet, insn_disasm, instr_ex, insn))
    return inst_list

# 主要的测试环境运行逻辑
def decode_run(decoder, inst_list, need_log_file, log_file_name = None):
    if need_log_file == True:
        open_log_file(log_file_name)

    decoder.SetDefaultValue()
    decoder.Reset()
    pos = 0
    detect_pos = 0
    insts_length = len(inst_list)
    sub_valid = 1
    sub_list  = inst_list[pos:pos+6]
    while True:
        decoder.Input_instruction_list(sub_list,sub_valid)
        decoder.dut.Step(1)
        allow_number = decoder.Get_allow_input_number()
        if allow_number > 0:
            pos = pos + allow_number
            sub_list    = inst_list[pos:pos+allow_number]
            sub_valid   = 1
        num, step_result_list = decoder.Get_decode_result()
        if num > 0:
            if need_log_file == True:
                comapre_result_in_text(inst_list[detect_pos:detect_pos+num], step_result_list, num)
            else:
                comapre_result(inst_list[detect_pos:detect_pos+num], step_result_list, num)
            
            detect_pos = detect_pos + num
        
        if pos >= insts_length:
            break           
    decoder.dut.Step(10)
    close_log_file()    

# rvc 测试
def test_rvc_expand():
    ref_insts  = generate_rvc_instructions()
    # ref_insts  = generate_random_32bits(1)
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
