# coding=utf8
# ***************************************************************************************
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
# **************************************************************************************/

import ctypes
import datetime

import toffee
import toffee.funcov as fc
import toffee_test
from dut.DecodeStage import *
from dut.PreDecode import *
from dut.RVCExpander import *

from comm import get_out_dir, debug, UT_FCOV, get_file_logger, get_version_checker, module_name_with

# Version check
version_check = get_version_checker("openxiangshan-kmh-*")

# Create a function coverage group: INT (Int instruction)
g = fc.CovGroup(UT_FCOV("../../INT"))


def init_rvc_expander_funcov(expander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""

    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR. The instruction is not illegal
    #    - bin SUCCE. The instruction is not expanded
    g.add_watch_point(expander, {
        "ERROR": lambda x: x.stat()["ilegal"] == False,
        "SUCCE": lambda x: x.stat()["ilegal"] != False,
    }, name="RVC_EXPAND_RET")

    # 2. Add point RVC_EXPAND_16B_RANGE to check expander input range
    #   - bin RANGE[start-end]. The instruction is in the range of the compressed instruction set
    # This check point is added in case 'test_rv_decode.test_rvc_expand_16bit_full' dynamically, see the test case for details

    # 3. Add point RVC_EXPAND_32B_RANGE to check expander input range
    #   - bin RANGE[start-end]. The instruction is in the range of the 32bit instruction set
    # This check point is added in case 'test_rv_decode.test_rvc_expand_32bit_full' dynamically, see the test case for details

    # 4. Add point RVC_EXPAND_32B_BITS to check expander function coverage
    #   - bin BITS[0-31]. The instruction is expanded to the corresponding 32-bit instruction
    def _check_pos(i):
        def check(expander):
            return expander.stat()["instr"] & (1 << i) != 0

        return check

    g.add_watch_point(expander, {
        "POS_%d" % i: _check_pos(i)
        for i in range(32)
    }, name="RVC_EXPAND_32B_BITS")

    # 5. Reverse mark function coverage to the check point
    def _M(name):
        # get the module name
        return module_name_with(name, "../../test_rv_decode")

    #  - mark RVC_EXPAND_RET
    g.mark_function(
        "RVC_EXPAND_RET",
        _M(["test_rvc_expand_16bit_full",
            "test_rvc_expand_32bit_full",
            "test_rvc_expand_32bit_randomN"]),
        bin_name=["ERROR", "SUCCE"])
    #  - mark RVC_EXPAND_16B_RANGE
    g.mark_function("RVC_EXPAND_32B_BITS", _M("test_rvc_expand_32bit_randomN"), bin_name=["POS_*"], raise_error=False)

    # The End
    return None


def init_rv_decoder_funcov(g: fc.CovGroup):
    # TBD
    pass


class RVCExpander(toffee.Bundle):
    def __init__(self, cover_group, dut: DUTRVCExpander):
        super().__init__()
        self.cover_group = cover_group
        self.dut = dut
        self.io = toffee.Bundle.from_prefix("io_", self.dut)
        self.bind(self.dut)

    def expand(self, instr):
        self.io["in"].value = instr
        self.io["fsIsOff"].value = False
        self.dut.RefreshComb()
        self.cover_group.sample()
        return self.io["out_bits"].value, self.io["ill"].value

    def stat(self):
        return {
            "instr": self.io["in"].value,
            "decode": self.io["out_bits"].value,
            "ilegal": self.io["ill"].value != 0,
        }


@toffee_test.fixture
async def rvc_expander(toffee_request: toffee_test.ToffeeRequest):
    version_check()
    dut = toffee_request.create_dut(DUTRVCExpander)
    expander = RVCExpander(g, dut)
    toffee_request.cov_groups.append(g)
    expander.dut.io_in.AsImmWrite()
    init_rvc_expander_funcov(expander, g)
    return expander


class Decode(toffee.Bundle):
    def __init__(self, dut: DUTDecodeStage):
        super().__init__()
        self.dut = dut
        for i in range(6):
            setattr(self, f"in_data_{i}", toffee.Bundle.from_prefix(f"io_in_{i}_", dut))
            setattr(self, f"out_data_{i}", toffee.Bundle.from_prefix(f"io_out_{i}_", dut))
        self.input_inst = [getattr(self, f"in_data_{i}") for i in range(6)]
        self.output_instrution = [getattr(self, f"out_data_{i}") for i in range(6)]
        self.io = toffee.Bundle.from_prefix(f"io_", dut)
        self.bind(dut)

    def SetDefaultValue(self):
        """Use Boundle to set DUT pin value"""
        self.io.assign({
            "out_0_ready": 0b1,
            "out_1_ready": 0b1,
            "out_2_ready": 0b1,
            "out_3_ready": 0b1,
            "out_4_ready": 0b1,
            "out_5_ready": 0b1,
            "*": 0,  # Set other pins to 0
        })

    def Reset(self):
        """Directly operate the dut pins to reset"""
        self.dut.reset.value = 0
        self.dut.Step(1)
        self.dut.reset.value = 1
        self.dut.Step(2)
        self.dut.reset.value = 0
        self.dut.Step(1)

    def Input_instruction(self, i, valid, instr, isRVC, brType, isCall, isRet, pred_taken, instr_ex):
        self.input_inst[i].valid.value = valid
        self.input_inst[i].bits_instr.value = instr
        if hasattr(self.input_inst[i], "bits_foldpc"):
            self.input_inst[i].bits_foldpc.value = 0
        self.input_inst[i].bits_exceptionVec_2.value = instr_ex
        for j in range(24):
            p = getattr(self.dut, f'io_in_{i}_bits_exceptionVec_{j}', None)
            if p:
                p.value = 0
        self.input_inst[i].bits_trigger.value = 0
        self.input_inst[i].bits_preDecodeInfo_isRVC.value = isRVC
        self.input_inst[i].bits_preDecodeInfo_brType.value = brType
        self.input_inst[i].bits_pred_taken.value = pred_taken
        self.input_inst[i].bits_crossPageIPFFix.value = 0
        self.input_inst[i].bits_ftqPtr_flag.value = 0
        self.input_inst[i].bits_ftqPtr_value.value = 0
        self.input_inst[i].bits_ftqOffset.value = 0

    def FromCSR_illegalInst(self, sfenceVMA, sfencePart, hfenceGVMA, hfenceVVMA, hlsv, fsIsOff, vsIsOff, wfi, frm):
        self.dut.io_fromCSR_illegalInst_sfenceVMA.value = sfenceVMA
        self.dut.io_fromCSR_illegalInst_sfencePart.value = sfencePart
        self.dut.io_fromCSR_illegalInst_hfenceGVMA.value = hfenceGVMA
        self.dut.io_fromCSR_illegalInst_hfenceVVMA.value = hfenceVVMA
        self.dut.io_fromCSR_illegalInst_hlsv.value = hlsv
        self.dut.io_fromCSR_illegalInst_fsIsOff.value = fsIsOff
        self.dut.io_fromCSR_illegalInst_vsIsOff.value = vsIsOff
        self.dut.io_fromCSR_illegalInst_wfi.value = wfi
        self.dut.io_fromCSR_illegalInst_frm.value = frm

    def FromCSR_virtualInst(self, sfenceVMA, sfencePart, hfence, hlsv, wfi):
        self.dut.io_fromCSR_virtualInst_sfenceVMA.value = sfenceVMA
        self.dut.io_fromCSR_virtualInst_sfencePart.value = sfencePart
        self.dut.io_fromCSR_virtualInst_hfence.value = hfence
        self.dut.io_fromCSR_virtualInst_hlsv.value = hlsv
        self.dut.io_fromCSR_virtualInst_wfi.value = wfi

    def Get_input_ready(self, i):
        return self.input_inst[i].ready.value

    def Get_allow_input_number(self):
        cnt = 0
        for i in range(6):
            if self.input_inst[i].ready.value == 1:
                cnt = i + 1
            else:
                break
        return cnt

    def Input_instruction_list(self, insts, valid):
        for i in range(6):
            self.Input_instruction(i, 0, 0, 0, 0, 0, 0, 0, 0)
        for i, inst in enumerate(insts):
            self.Input_instruction(i, valid, inst[0], 0, 0, 0, 0, 0, inst[3])

    def Get_decode_result(self):
        insts_result = []
        num = 0
        for i in range(6):
            if self.output_instrution[i].valid.value == 1 and self.output_instrution[i].bits_lastUop.value == 1:
                insts_result.append((self.output_instrution[i].bits_instr.value,
                                     self.output_instrution[i].bits_exceptionVec_2.value or self.output_instrution[
                                         i].bits_exceptionVec_22.value,
                                     self.output_instrution[i].bits_firstUop.value))
                num = num + 1
        return num, insts_result

    def Get_decode_checkpoint_illeagl_inst(self):
        illegal = 0
        for i in range(6):
            if self.output_instrution[i].valid.value == 1 and self.output_instrution[i].bits_lastUop.value == 1:
                if (self.output_instrution[i].bits_exceptionVec_2.value or self.output_instrution[
                    i].bits_exceptionVec_22.value):
                    illegal = 1
        return illegal

    def Get_decode_checkpoint_complex_inst(self):
        complex = 0
        for i in range(6):
            if self.output_instrution[i].valid.value == 1 and self.output_instrution[i].bits_lastUop.value == 1 and \
                    self.output_instrution[i].bits_firstUop.value != 1:
                complex = 1
        return complex


@toffee_test.fixture
async def decoder(toffee_request: toffee_test.ToffeeRequest):
    import os
    # before test
    init_rv_decoder_funcov(g)
    # If the output directory does not exist, create it
    output_dir_path = get_out_dir("decoder/log")
    os.makedirs(output_dir_path, exist_ok=True)
    dut = toffee_request.create_dut(DUTDecodeStage, "clock")
    toffee_request.cov_groups.append(g)
    decoder = Decode(dut)
    return decoder


def comapre_result(ref_value_list, dut_value_list, num):
    eq = True
    if num == 0:
        return None
    else:
        for i in range(num):
            if ref_value_list[i][1] != dut_value_list[i][1]:
                debug("================================")
                debug(ref_value_list[i])
                debug(dut_value_list[i])
                eq = False
    return eq


log_all_info_file = None
log_err_info_file = None


def open_log_file(name):
    global log_all_info_file
    global log_err_info_file
    # Obtain the current time and format it
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = get_out_dir("decoder/log/log")
    # Create a file name
    if name is not None:
        filename_all = output_dir + f"_all_{name}.txt"
        filename_err = output_dir + f"_err_{name}.txt"
    else:
        filename_all = output_dir + f"_all_{current_time}.txt"
        filename_err = output_dir + f"_err_{current_time}.txt"
    log_all_info_file = get_file_logger(filename_all, format=None)
    log_err_info_file = get_file_logger(filename_err, format=None)


def close_log_file():
    global log_all_info_file
    global log_err_info_file
    if log_all_info_file is not None:
        log_all_info_file = None
    if log_err_info_file is not None:
        log_err_info_file = None


def write_all_info_to_file(info):
    if log_all_info_file is not None:
        log_all_info_file.info(info)
    else:
        debug("remember open_log_file , close_log_file")


def write_err_info_to_file(info):
    if log_err_info_file is not None:
        log_err_info_file.info(info)
    else:
        debug("remember open_log_file , close_log_file")


# Write the comparison results to a file
# ref_value_list[i][0] = Decimal display of instructions, ref_value_list[i][1] = The reference results are used to determine whether the instruction is illegal,
# ref_value_list[i][2] = Disassembly result of the instruction, ref_value_list[i][3] = Preliminary screening for illegal instructions is conducted through the RVCExpander module
# dut_value_list[i][0] = Decimal representation of the instructions output by the Decoder module, 
# dut_value_list[i][1] = The output results from the Decoder are used to determine whether anomalies exist, 
# dut_value_list[i][2] = The output results from the Decoder are used to determine whether the instruction is a complex instruction
def comapre_result_in_text(ref_value_list, dut_value_list, num):
    eq = True
    if num == 0:
        return None
    else:
        for i in range(num):
            # Do not change to assert for now. First, focus on implementing the functionality. Assert directly stops execution.。
            if (ref_value_list[i][2] == 0 or (ref_value_list[i][0] == dut_value_list[i][0])) and (
                    ref_value_list[i][1] == dut_value_list[i][1]):
                # print("Meets expectations:（￣︶￣）↗")
                good_info = f"good  ----- ref: {ref_value_list[i][0]}, {ref_value_list[i][1]}, {ref_value_list[i][2]}, {ref_value_list[i][3]}"
                write_all_info_to_file(good_info)
            else:
                # print("Not meeting expectations: <(_ _)>")
                bad_info = f"bad   ----- ref: {ref_value_list[i][0]}, {ref_value_list[i][1]}, {ref_value_list[i][2]}, {ref_value_list[i][3]}, old inst: {ref_value_list[i][4]},   dut: {dut_value_list[i][0]}, {dut_value_list[i][1]}, complex: {dut_value_list[i][2] == 0}"
                write_all_info_to_file(bad_info)
                if (ref_value_list[i][2][0] != 'v'):
                    write_err_info_to_file(bad_info)
                eq = False
    return eq


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


# Disassemble the instruction and send it to the rvc_expand module for decoding of compressed instructions
def convert_reference_format(rvc_expander, ref_insts, need_expand, disasm_func, disasm_free_func, disasm_arg=0):
    inst_list = []
    for insn in ref_insts:
        c_void_ptr = disasm_func(ctypes.c_uint64(insn), disasm_arg)
        insn_disasm = ctypes.cast(c_void_ptr, ctypes.c_char_p).value.decode('utf-8')
        disasm_free_func(c_void_ptr)

        if need_expand == True:
            instr_bits, instr_ex = rvc_expander.expand(insn)
        else:
            instr_ex = 0
            instr_bits = insn

        if insn_disasm == "unknown":
            inst_list.append((instr_bits, 1, insn_disasm, instr_ex, insn))
        else:
            is_excpet = instr_filter(insn_disasm)
            inst_list.append((instr_bits, is_excpet, insn_disasm, instr_ex, insn))
    return inst_list


# The main part of the test environment
def decode_run(decoder, inst_list, need_log_file, log_file_name=None):
    if need_log_file:
        open_log_file(log_file_name)
    decoder.SetDefaultValue()
    decoder.Reset()
    pos = 0
    detect_pos = 0
    insts_length = len(inst_list)
    sub_valid = 1
    sub_list = inst_list[pos:pos + 6]
    success = True
    while True:
        decoder.Input_instruction_list(sub_list, sub_valid)
        decoder.dut.Step(1)
        allow_number = decoder.Get_allow_input_number()
        if allow_number > 0:
            pos = pos + allow_number
            sub_list = inst_list[pos:pos + allow_number]
            sub_valid = 1
        num, step_result_list = decoder.Get_decode_result()
        if num > 0:
            if need_log_file == True:
                if comapre_result_in_text(inst_list[detect_pos:detect_pos + num], step_result_list, num) == False:
                    success = False
            else:
                if comapre_result(inst_list[detect_pos:detect_pos + num], step_result_list, num) == False:
                    success = False
            detect_pos = detect_pos + num
        if pos >= insts_length:
            break
    decoder.dut.Step(10)
    close_log_file()
    return success
