from dut.predecode.UT_PreDecode import *
from dut.decodestage.UT_DecodeStage import *
import mlvp
import os
import pytest
import ctypes
import datetime
from comm import get_out_dir
from mlvp.reporter import set_line_coverage
from dut.rvcexpander.UT_RVCExpander import *

import mlvp.funcov as fc
from mlvp.reporter import set_func_coverage

g = fc.CovGroup("Group X")

def init_function_coverage(g):
# Add decoder module test point content: ToDO
    pass

mlvp.setup_logging(mlvp.ERROR)


class PreDecodeWrapper(mlvp.Bundle):
    def __init__(self, dut: DUTPreDecode):
        super().__init__()
        self.dut = dut
        self.input_instrution = mlvp.Bundle.from_prefix("io_in_bits_", dut)
        self.output_instrution = mlvp.Bundle.from_prefix("io_out_", dut)
        self.bind(dut)

    def predecode(self, instr, need_step=1):
        if not isinstance(instr, list):
            instr = [instr]
        predecoded_inst = []
        for i in range(0, len(instr), 16):
            sub_list = instr[i:i+16]
            for j, inst in enumerate(sub_list):
                self.input_instrution[f"data_%d"%j].value = inst
            self.dut.Step(need_step)
            predecoded_inst.extend([self.output_instrution["instr_%d"%k].value for k in range(16)])  
        return predecoded_inst


class DecodeWrapper(mlvp.Bundle):
    def __init__(self, dut: DUTDecodeStage):
        super().__init__()
        self.dut = dut
        for i in range(6):
            setattr(self, f"in_data_{i}", mlvp.Bundle.from_prefix(f"io_in_{i}_", dut))
            setattr(self, f"out_data_{i}", mlvp.Bundle.from_prefix(f"io_out_{i}_", dut))
        self.input_inst = [getattr(self, f"in_data_{i}") for i in range(6)]
        self.output_instrution = [getattr(self, f"out_data_{i}") for i in range(6)]
        self.bind(dut)

    def SetDefaultValue(self):
        ########## set default sinput ignal value ###############
        self.dut.io_redirect.value          = 0b0

        ######### set instruction releated signals
        for i in range(6):
            self.input_inst[i].valid.value              = 0
            self.input_inst[i].bits_instr.value         = 0
            self.input_inst[i].bits_foldpc.value        = 0
            self.input_inst[i].bits_isFetchMalAddr      = 0
            self.input_inst[i].bits_trigger.value       = 0
            self.input_inst[i].bits_preDecodeInfo_isRVC.value      = 0
            self.input_inst[i].bits_preDecodeInfo_brType.value     = 0
            self.input_inst[i].bits_pred_taken.value               = 0
            self.input_inst[i].bits_crossPageIPFFix.value          = 0
            self.input_inst[i].bits_ftqPtr_flag.value              = 0
            self.input_inst[i].bits_ftqPtr_value.value             = 0
            self.input_inst[i].bits_ftqOffset.value                = 0

            for j in range(24):
                setattr(self.dut, f'io_in_{i}_bits_exceptionVec_{j}', 0) 

        ########## set req ready signals from rename stage #######  
        self.dut.io_out_0_ready.value     = 0b1
        self.dut.io_out_1_ready.value     = 0b1
        self.dut.io_out_2_ready.value     = 0b1
        self.dut.io_out_3_ready.value     = 0b1
        self.dut.io_out_4_ready.value     = 0b1
        self.dut.io_out_5_ready.value     = 0b1

        ########## singlestep signal temporarily set to 0 (Because it may be hard to compare with ref model)
        self.dut.io_csrCtrl_singlestep.value  = 0b0

        ########## fromCSR #######################################
        self.dut.io_fromCSR_illegalInst_sfenceVMA.value   = 0
        self.dut.io_fromCSR_illegalInst_sfencePart.value  = 0
        self.dut.io_fromCSR_illegalInst_hfenceGVMA.value  = 0
        self.dut.io_fromCSR_illegalInst_hfenceVVMA.value  = 0
        self.dut.io_fromCSR_illegalInst_hlsv.value        = 0
        self.dut.io_fromCSR_illegalInst_fsIsOff.value     = 0
        self.dut.io_fromCSR_illegalInst_vsIsOff.value     = 0
        self.dut.io_fromCSR_illegalInst_wfi.value         = 0
        self.dut.io_fromCSR_illegalInst_frm.value         = 0
        self.dut.io_fromCSR_virtualInst_sfenceVMA.value   = 0
        self.dut.io_fromCSR_virtualInst_sfencePart.value  = 0
        self.dut.io_fromCSR_virtualInst_hfence.value      = 0
        self.dut.io_fromCSR_virtualInst_hlsv.value        = 0
        self.dut.io_fromCSR_virtualInst_wfi.value         = 0

        ######### fusion no use ##################################
        self.dut.io_fusion_0.value        = 0b0
        self.dut.io_fusion_1.value        = 0b0
        self.dut.io_fusion_2.value        = 0b0
        ########## VType signals temporarily set to 0 (Because it may be hard to compare with ref model)
        self.dut.io_fromRob_isResumeVType.value                   = 0b0
        self.dut.io_fromRob_commitVType_vtype_valid.value         = 0b0
        self.dut.io_fromRob_commitVType_vtype_bits_illegal.value  = 0b0
        self.dut.io_fromRob_commitVType_vtype_bits_vma.value      = 0b0
        self.dut.io_fromRob_commitVType_vtype_bits_vta.value      = 0b0
        self.dut.io_fromRob_commitVType_vtype_bits_vsew.value     = 0b0
        self.dut.io_fromRob_commitVType_vtype_bits_vlmul.value    = 0b0
        self.dut.io_fromRob_commitVType_hasVsetvl.value           = 0b0

        self.dut.io_fromRob_walkVType_valid.value                 = 0b0
        self.dut.io_fromRob_walkVType_bits_illegal.value          = 0b0
        self.dut.io_fromRob_walkVType_bits_vma.value              = 0b0
        self.dut.io_fromRob_walkVType_bits_vta.value              = 0b0
        self.dut.io_fromRob_walkVType_bits_vsew.value             = 0
        self.dut.io_fromRob_walkVType_bits_vlmul.value            = 0
        self.dut.io_vsetvlVType_illegal.value               = 0b0
        self.dut.io_vsetvlVType_vma.value                   = 0b0
        self.dut.io_vsetvlVType_vta.value                   = 0b0
        self.dut.io_vsetvlVType_vsew.value                  = 0
        self.dut.io_vsetvlVType_vlmul.value                 = 0
        self.dut.io_vstart.value                            = 0        

    def Reset(self):
        self.dut.reset.value  = 0
        self.dut.Step(1)
        self.dut.reset.value  = 1
        self.dut.Step(2)
        self.dut.reset.value  = 0
        self.dut.Step(1)

    def Input_instruction(self, i, valid, instr, isRVC, brType, isCall, isRet, pred_taken, instr_ex):
        self.input_inst[i].valid.value = valid
        self.input_inst[i].bits_instr.value = instr
        self.input_inst[i].bits_foldpc.value = 0
        self.input_inst[i].bits_exceptionVec_2.value = instr_ex

        for j in range(24):
            setattr(self.dut, f'io_in_{i}_bits_exceptionVec_{j}', 0)

        self.input_inst[i].bits_trigger.value                  = 0
        self.input_inst[i].bits_preDecodeInfo_isRVC.value      = isRVC
        self.input_inst[i].bits_preDecodeInfo_brType.value     = brType
        self.input_inst[i].bits_pred_taken.value               = pred_taken
        self.input_inst[i].bits_crossPageIPFFix.value          = 0
        self.input_inst[i].bits_ftqPtr_flag.value              = 0
        self.input_inst[i].bits_ftqPtr_value.value             = 0
        self.input_inst[i].bits_ftqOffset.value                = 0

    def FromCSR_illegalInst(self, sfenceVMA, sfencePart, hfenceGVMA, hfenceVVMA, hlsv, fsIsOff, vsIsOff, wfi, frm):
        self.dut.io_fromCSR_illegalInst_sfenceVMA.value   = sfenceVMA
        self.dut.io_fromCSR_illegalInst_sfencePart.value  = sfencePart
        self.dut.io_fromCSR_illegalInst_hfenceGVMA.value  = hfenceGVMA
        self.dut.io_fromCSR_illegalInst_hfenceVVMA.value  = hfenceVVMA
        self.dut.io_fromCSR_illegalInst_hlsv.value        = hlsv
        self.dut.io_fromCSR_illegalInst_fsIsOff.value     = fsIsOff
        self.dut.io_fromCSR_illegalInst_vsIsOff.value     = vsIsOff
        self.dut.io_fromCSR_illegalInst_wfi.value         = wfi
        self.dut.io_fromCSR_illegalInst_frm.value         = frm


    def FromCSR_virtualInst(self, sfenceVMA, sfencePart, hfence, hlsv, wfi):
        self.dut.io_fromCSR_virtualInst_sfenceVMA.value   = sfenceVMA
        self.dut.io_fromCSR_virtualInst_sfencePart.value  = sfencePart
        self.dut.io_fromCSR_virtualInst_hfence.value      = hfence
        self.dut.io_fromCSR_virtualInst_hlsv.value        = hlsv
        self.dut.io_fromCSR_virtualInst_wfi.value         = wfi


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
            self.Input_instruction(i, 0, 0, 0, 0, 0, 0, 0,0)
        for i, inst in enumerate(insts):
            self.Input_instruction(i, valid, inst[0], 0, 0, 0, 0, 0,inst[3])

    def Get_decode_result(self):
        insts_result = []
        num = 0
        for i in range(6):
            if self.output_instrution[i].valid.value == 1 and self.output_instrution[i].bits_lastUop.value == 1:
                insts_result.append((self.output_instrution[i].bits_instr.value, self.output_instrution[i].bits_exceptionVec_2.value or self.output_instrution[i].bits_exceptionVec_22.value, self.output_instrution[i].bits_firstUop.value))
                num = num + 1
        return num, insts_result


@pytest.fixture()
def decoder_fixture(request):
    # before test
    init_function_coverage(g)
    func_name = request.node.name
    # If the output directory does not exist, create it
    output_dir_path = get_out_dir("decoder/log")
    os.makedirs(output_dir_path, exist_ok=True)
    decoder = DecodeWrapper(DUTDecodeStage(
        waveform_filename=get_out_dir("decoder/decode_%s.fst"%func_name),
        coverage_filename=get_out_dir("decoder/decode_%s.dat"%func_name),
    ))
    decoder.dut.InitClock("clock")
    decoder.dut.StepRis(lambda x: g.sample())
    # decoder.dut.io_in_0_valid.AsImmWrite()
    # decoder.dut.io_in_0_bits_instr.AsImmWrite()
    yield decoder
    # after test
    decoder.dut.Finish()
    coverage_file = get_out_dir("decoder/decode_%s.dat"%func_name)
    if not os.path.exists(coverage_file):
        raise FileNotFoundError(f"File not found: {coverage_file}")
    set_line_coverage(request, coverage_file)
    set_func_coverage(request, g)
    g.clear()


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


# Write the comparison results to a file
# ref_value_list[i][0] = Decimal display of instructions, ref_value_list[i][1] = The reference results are used to determine whether the instruction is illegal,
# ref_value_list[i][2] = Disassembly result of the instruction, ref_value_list[i][3] = Preliminary screening for illegal instructions is conducted through the RVCExpander module
# dut_value_list[i][0] = Decimal representation of the instructions output by the Decoder module, 
# dut_value_list[i][1] = The output results from the Decoder are used to determine whether anomalies exist, 
# dut_value_list[i][2] = The output results from the Decoder are used to determine whether the instruction is a complex instruction
def comapre_result_in_text(ref_value_list, dut_value_list, num):
    if num == 0:
        return
    else:
        for i in range(num):
            # Do not change to assert for now. First, focus on implementing the functionality. Assert directly stops execution.。
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


# The main part of the test environment
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
