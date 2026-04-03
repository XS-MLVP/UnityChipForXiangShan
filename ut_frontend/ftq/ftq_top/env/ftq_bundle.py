from toffee import *
from ut_frontend.bpu.tagesc import bundle  

class IfuPdSlotBundle(Bundle):
    brType = Signal()
    isCall = Signal()
    isRet  = Signal()
    valid  = Signal()

class RobCommitBundle(Bundle):
    valid             = Signal()
    bits_commitType   = Signal()
    bits_ftqIdx_flag  = Signal()
    bits_ftqIdx_value = Signal()
    bits_ftqOffset    = Signal()     

class LastStageFtbEntryBundle(Bundle):
    valid = Signal()
    isJalr = Signal()
    isCall = Signal()
    isRet = Signal()
    brSlots_0_valid = Signal()
    brSlots_0_offset = Signal()
    tailSlot_valid = Signal()
    tailSlot_offset = Signal()
    tailSlot_sharing = Signal()


class ToIfuBundle(Bundle):  
    req_ready = Signal()  
    req_valid = Signal()  
      


class ToICacheBundle(Bundle):  
    req_valid = Signal()
    req_bits_readValid_0 = Signal()
    req_bits_readValid_1 = Signal()
    req_bits_readValid_2 = Signal()
    req_bits_readValid_3 = Signal()
    req_bits_readValid_4 = Signal()
    req_bits_pcMemRead_0_startAddr = Signal()
    req_bits_pcMemRead_1_startAddr = Signal()
    req_bits_pcMemRead_2_startAddr = Signal()
    req_bits_pcMemRead_3_startAddr = Signal()
    req_bits_pcMemRead_4_startAddr = Signal()
    req_bits_pcMemRead_0_nextlineStart = Signal()
    req_bits_pcMemRead_1_nextlineStart = Signal()
    req_bits_pcMemRead_2_nextlineStart = Signal()
    req_bits_pcMemRead_3_nextlineStart = Signal()
    req_bits_pcMemRead_4_nextlineStart = Signal()

class ToPrefetchBundle(Bundle):  
    req_ready = Signal()
    req_valid = Signal()

    flushFromBpu_s2_valid = Signal()
    flushFromBpu_s2_bits_flag = Signal()
    flushFromBpu_s2_bits_value = Signal()
    flushFromBpu_s3_valid = Signal()
    flushFromBpu_s3_bits_flag = Signal()
    flushFromBpu_s3_bits_value = Signal()    

 

class FromBpuBundle(Bundle):  
    
    resp_valid = Signal()  
    resp_ready = Signal()
    resp_bits_s1_pc_3 = Signal()  
    resp_bits_s1_full_pred_3_fallThroughErr = Signal()  
    
    resp_bits_s2_valid_3 = Signal()  
    resp_bits_s2_hasRedirect_3 = Signal()  
    resp_bits_s2_pc_3 = Signal()  
    resp_bits_s2_ftq_idx_value = Signal()  
    resp_bits_s2_ftq_idx_flag = Signal()  
    resp_bits_s2_full_pred_3_fallThroughErr = Signal()  
    resp_bits_s2_full_pred_3_hit = Signal()
    
    resp_bits_s3_valid_3 = Signal()  
    resp_bits_s3_hasRedirect_3 = Signal()  
    resp_bits_s3_pc_3 = Signal()  
    resp_bits_s3_ftq_idx_value = Signal()  
    resp_bits_s3_ftq_idx_flag = Signal()  
    resp_bits_s3_full_pred_3_fallThroughErr = Signal()  


    last_stage_ftb_entry = LastStageFtbEntryBundle.from_prefix("resp_bits_last_stage_ftb_entry_")

class FromBackendBundle(Bundle):  
    redirect_valid = Signal()  
    redirect_bits_ftqIdx_value = Signal()  
    redirect_bits_ftqIdx_flag = Signal()
    redirect_bits_ftqOffset = Signal()  
    redirect_bits_cfiUpdate_target = Signal()  
    redirect_bits_cfiUpdate_taken = Signal()  
    redirect_bits_cfiUpdate_isMisPred = Signal()  

    redirect_bits_level                    = Signal()
    redirect_bits_debugIsCtrl              = Signal()
    redirect_bits_debugIsMemVio            = Signal()

    ftqIdxSelOH_bits = Signal()
    ftqIdxAhead_0_valid = Signal()
    ftqIdxAhead_0_bits_value = Signal()

    rob_commits_0 = RobCommitBundle.from_prefix("rob_commits_0_")
    rob_commits_1 = RobCommitBundle.from_prefix("rob_commits_1_")
    rob_commits_2 = RobCommitBundle.from_prefix("rob_commits_2_")
    rob_commits_3 = RobCommitBundle.from_prefix("rob_commits_3_")
    rob_commits_4 = RobCommitBundle.from_prefix("rob_commits_4_")
    rob_commits_5 = RobCommitBundle.from_prefix("rob_commits_5_")
    rob_commits_6 = RobCommitBundle.from_prefix("rob_commits_6_")
    rob_commits_7 = RobCommitBundle.from_prefix("rob_commits_7_")

class FromIfuBundle(Bundle):  
    pdWb_bits_target = Signal()  
    pdWb_bits_cfiOffset_valid = Signal()  
    pdWb_bits_misOffset_valid = Signal()  
    pdWb_bits_ftqIdx_value = Signal()  
    pdWb_bits_ftqIdx_flag = Signal()
    pdWb_bits_misOffset_bits = Signal()  
    pdWb_valid = Signal()  

    
    

    

        
    pdWb_bits_pd_0 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_0_")
    pdWb_bits_pd_1 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_1_")
    pdWb_bits_pd_2 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_2_")
    pdWb_bits_pd_3 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_3_")
    pdWb_bits_pd_4 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_4_")
    pdWb_bits_pd_5 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_5_")
    pdWb_bits_pd_6 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_6_")
    pdWb_bits_pd_7 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_7_")
    pdWb_bits_pd_8  = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_8_")
    pdWb_bits_pd_9  = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_9_")
    pdWb_bits_pd_10 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_10_")
    pdWb_bits_pd_11 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_11_")
    pdWb_bits_pd_12 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_12_")
    pdWb_bits_pd_13 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_13_")
    pdWb_bits_pd_14 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_14_")
    pdWb_bits_pd_15 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_15_")

    pdWb_bits_pc_0  = Signal()
    pdWb_bits_pc_1  = Signal()
    pdWb_bits_pc_2  = Signal()
    pdWb_bits_pc_3  = Signal()
    pdWb_bits_pc_4  = Signal()
    pdWb_bits_pc_5  = Signal()
    pdWb_bits_pc_6  = Signal()
    pdWb_bits_pc_7  = Signal()
    pdWb_bits_pc_8  = Signal()
    pdWb_bits_pc_9  = Signal()
    pdWb_bits_pc_10 = Signal()
    pdWb_bits_pc_11 = Signal()
    pdWb_bits_pc_12 = Signal()
    pdWb_bits_pc_13 = Signal()
    pdWb_bits_pc_14 = Signal()
    pdWb_bits_pc_15 = Signal()

# class FtqBundle(Bundle):

    
#     fromBackend = FromBackendBundle.from_prefix("fromBackend_")  
#     fromIfu = FromIfuBundle.from_prefix("fromIfu_")  
#     fromBpu = FromBpuBundle.from_prefix("fromBpu_")
#     toIfu = ToIfuBundle.from_prefix("toIfu_")
#     toICache = ToICacheBundle.from_prefix("toICache_")  
#     toPrefetch = ToPrefetchBundle.from_prefix("toPrefetch_")  

#     fromBpuNew = BranchPredictionResp.from_prefix("fromBpu_resp_bits_")


class BranchPredictionBundle(Bundle):
    # Pins every stage share
    pc_3 = Signal()
    full_pred_3_br_taken_mask_0 = Signal()
    full_pred_3_br_taken_mask_1 = Signal()
    full_pred_3_slot_valids_0 = Signal()
    full_pred_3_slot_valids_1 = Signal()
    full_pred_3_targets_0 = Signal()
    full_pred_3_targets_1 = Signal()
    full_pred_3_offsets_0 = Signal()
    full_pred_3_offsets_1 = Signal()
    full_pred_3_fallThroughAddr = Signal()
    full_pred_3_fallThroughErr = Signal()
    full_pred_3_is_br_sharing = Signal()
    full_pred_3_hit = Signal()

    # Only for s2 and s3
    # valid_3 = Signal()
    # hasRedirect_3 = Signal()
    # ftq_idx_flag = Signal()  
    # ftq_idx_value = Signal()  

class BranchPredictionBundleforS23(BranchPredictionBundle):

    # Only for s2 and s3
    valid_3 = Signal()
    hasRedirect_3 = Signal()
    ftq_idx_flag = Signal()  
    ftq_idx_value = Signal()  


class LastStageFtbEntryBundle(Bundle):
    isCall = Signal()
    isRet = Signal()
    isJalr = Signal()
    valid = Signal()
    brSlots_0_offset = Signal()
    brSlots_0_sharing = Signal()
    brSlots_0_valid = Signal()
    brSlots_0_lower = Signal()
    brSlots_0_tarStat = Signal()
    tailSlot_offset = Signal()         
    tailSlot_sharing = Signal()
    tailSlot_valid = Signal()
    tailSlot_lower = Signal()
    tailSlot_tarStat = Signal()
    pftAddr = Signal()
    carry = Signal()
    last_may_be_rvi_call = Signal()
    strong_bias_0 = Signal()
    strong_bias_1 = Signal()

class LastStageSpecInfoBundle(Bundle):
    histPtr_flag = Signal()
    histPtr_value = Signal()
    ssp = Signal()
    sctr = Signal()
    TOSW_flag = Signal()
    TOSW_value = Signal()
    TOSR_flag = Signal()
    TOSR_value = Signal()
    NOS_flag = Signal()
    NOS_value = Signal()
    topAddr = Signal()
    sc_disagree_0 = Signal()
    sc_disagree_1 = Signal()

class LastStageMetaBundle(Bundle):
    last_stage_meta = Signal()

class BranchPredictionResp(Bundle):
    valid = Signal()  
    ready = Signal()
    s1 = BranchPredictionBundle.from_prefix("bits_s1_")
    s2 = BranchPredictionBundleforS23.from_prefix("bits_s2_")  
    s3 = BranchPredictionBundleforS23.from_prefix("bits_s3_")

    last_stage_spec_info = LastStageSpecInfoBundle.from_prefix("bits_last_stage_spec_info_")
    last_stage_meta = LastStageMetaBundle.from_prefix("bits_")
    last_stage_ftb_entry = LastStageFtbEntryBundle.from_prefix("bits_last_stage_ftb_entry_")

    def selected_resp(self) -> BranchPredictionBundle:
        if self.s3.valid_3.value and self.s3.hasRedirect_3.value:
            print("s3 selected")
            return self.s3
        elif self.s2.valid_3.value and self.s2.hasRedirect_3.value:
            print("s2 selected")
            return self.s2
        elif self.valid.value:
            print("s1 selected")
            return self.s1 
        else:
            print("No stage selected, fallback to s1")
            return self.s1  # fallback

class toBpu_redirect(Bundle):
    valid = Signal()
    bits_level = Signal()
    bits_cfiUpdate_pc = Signal()
    bits_cfiUpdate_pd_valid = Signal()
    bits_cfiUpdate_pd_isRVC = Signal()
    bits_cfiUpdate_pd_isCall = Signal()
    bits_cfiUpdate_pd_isRet = Signal()
    bits_cfiUpdate_ssp = Signal()
    bits_cfiUpdate_sctr = Signal()
    bits_cfiUpdate_TOSW_flag = Signal()
    bits_cfiUpdate_TOSW_value = Signal()
    bits_cfiUpdate_TOSR_flag = Signal()
    bits_cfiUpdate_TOSR_value = Signal()
    bits_cfiUpdate_NOS_flag = Signal()
    bits_cfiUpdate_NOS_value = Signal()
    bits_cfiUpdate_histPtr_flag = Signal()
    bits_cfiUpdate_histPtr_value = Signal()
    bits_cfiUpdate_br_hit = Signal()
    bits_cfiUpdate_jr_hit = Signal()
    bits_cfiUpdate_sc_hit = Signal()
    bits_cfiUpdate_target = Signal()
    bits_cfiUpdate_taken = Signal()
    bits_cfiUpdate_shift = Signal()
    bits_cfiUpdate_addIntoHist = Signal()
    bits_debugIsCtrl = Signal()
    bits_debugIsMemVio = Signal()
    bits_BTBMissBubble = Signal()


class toBpu_update(Bundle):
    valid = Signal()
    bits_pc = Signal()

    # spec info (provides bits_spec_info_histPtr_value etc.)
    bits_spec_info_histPtr_value = Signal()

    # ftb entry (provides bits_ftb_entry_* fields)
    bits_ftb_entry = LastStageFtbEntryBundle.from_prefix("bits_ftb_entry_")

    bits_cfi_idx_valid = Signal()
    bits_cfi_idx_bits = Signal()

    bits_br_taken_mask_0 = Signal()
    bits_br_taken_mask_1 = Signal()
    bits_jmp_taken = Signal()

    bits_mispred_mask_0 = Signal()
    bits_mispred_mask_1 = Signal()
    bits_mispred_mask_2 = Signal()

    bits_false_hit = Signal()
    bits_old_entry = Signal()

    bits_meta = Signal()
    bits_full_target = Signal()


class toBpuBundle(Bundle):
    redirect = toBpu_redirect.from_prefix("redirect_")
    update = toBpu_update.from_prefix("update_")


class FtqBundle(Bundle):

    
    fromBackend = FromBackendBundle.from_prefix("fromBackend_")  
    fromIfu = FromIfuBundle.from_prefix("fromIfu_")  
    fromBpu = FromBpuBundle.from_prefix("fromBpu_")
    toIfu = ToIfuBundle.from_prefix("toIfu_")
    toICache = ToICacheBundle.from_prefix("toICache_")  
    toPrefetch = ToPrefetchBundle.from_prefix("toPrefetch_")  
    # fromBpuNew = BranchPredictionResp.from_prefix("fromBpu_resp_")
    toBpu = toBpuBundle.from_prefix("toBpu_")


