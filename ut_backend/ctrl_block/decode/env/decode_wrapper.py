from dut.predecode.UT_PreDecode import *
from dut.decodestage.UT_DecodeStage import *
import mlvp

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
