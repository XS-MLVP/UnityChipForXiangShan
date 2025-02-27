module Ftq_top;

  wire  clock;
  wire  reset;
  wire  io_fromBpu_resp_ready;
  wire  io_fromBpu_resp_valid;
  wire [49:0] io_fromBpu_resp_bits_s1_pc_3;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1;
  wire [49:0] io_fromBpu_resp_bits_s1_full_pred_3_targets_0;
  wire [49:0] io_fromBpu_resp_bits_s1_full_pred_3_targets_1;
  wire [3:0] io_fromBpu_resp_bits_s1_full_pred_3_offsets_0;
  wire [3:0] io_fromBpu_resp_bits_s1_full_pred_3_offsets_1;
  wire [49:0] io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddr;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErr;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharing;
  wire  io_fromBpu_resp_bits_s1_full_pred_3_hit;
  wire [49:0] io_fromBpu_resp_bits_s2_pc_3;
  wire  io_fromBpu_resp_bits_s2_valid_3;
  wire  io_fromBpu_resp_bits_s2_hasRedirect_3;
  wire  io_fromBpu_resp_bits_s2_ftq_idx_flag;
  wire [5:0] io_fromBpu_resp_bits_s2_ftq_idx_value;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1;
  wire [49:0] io_fromBpu_resp_bits_s2_full_pred_3_targets_0;
  wire [49:0] io_fromBpu_resp_bits_s2_full_pred_3_targets_1;
  wire [3:0] io_fromBpu_resp_bits_s2_full_pred_3_offsets_0;
  wire [3:0] io_fromBpu_resp_bits_s2_full_pred_3_offsets_1;
  wire [49:0] io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddr;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErr;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharing;
  wire  io_fromBpu_resp_bits_s2_full_pred_3_hit;
  wire [49:0] io_fromBpu_resp_bits_s3_pc_3;
  wire  io_fromBpu_resp_bits_s3_valid_3;
  wire  io_fromBpu_resp_bits_s3_hasRedirect_3;
  wire  io_fromBpu_resp_bits_s3_ftq_idx_flag;
  wire [5:0] io_fromBpu_resp_bits_s3_ftq_idx_value;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1;
  wire [49:0] io_fromBpu_resp_bits_s3_full_pred_3_targets_0;
  wire [49:0] io_fromBpu_resp_bits_s3_full_pred_3_targets_1;
  wire [3:0] io_fromBpu_resp_bits_s3_full_pred_3_offsets_0;
  wire [3:0] io_fromBpu_resp_bits_s3_full_pred_3_offsets_1;
  wire [49:0] io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddr;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErr;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharing;
  wire  io_fromBpu_resp_bits_s3_full_pred_3_hit;
  wire [259:0] io_fromBpu_resp_bits_last_stage_meta;
  wire  io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flag;
  wire [7:0] io_fromBpu_resp_bits_last_stage_spec_info_histPtr_value;
  wire [3:0] io_fromBpu_resp_bits_last_stage_spec_info_ssp;
  wire [2:0] io_fromBpu_resp_bits_last_stage_spec_info_sctr;
  wire  io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flag;
  wire [4:0] io_fromBpu_resp_bits_last_stage_spec_info_TOSW_value;
  wire  io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flag;
  wire [4:0] io_fromBpu_resp_bits_last_stage_spec_info_TOSR_value;
  wire  io_fromBpu_resp_bits_last_stage_spec_info_NOS_flag;
  wire [4:0] io_fromBpu_resp_bits_last_stage_spec_info_NOS_value;
  wire [49:0] io_fromBpu_resp_bits_last_stage_spec_info_topAddr;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_isCall;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_isRet;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_isJalr;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_valid;
  wire [3:0] io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offset;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharing;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_valid;
  wire [11:0] io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lower;
  wire [1:0] io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStat;
  wire [3:0] io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offset;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharing;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_valid;
  wire [19:0] io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lower;
  wire [1:0] io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStat;
  wire [3:0] io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddr;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_carry;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_call;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0;
  wire  io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1;
  wire  io_fromIfu_pdWb_valid;
  wire [49:0] io_fromIfu_pdWb_bits_pc_0;
  wire [49:0] io_fromIfu_pdWb_bits_pc_1;
  wire [49:0] io_fromIfu_pdWb_bits_pc_2;
  wire [49:0] io_fromIfu_pdWb_bits_pc_3;
  wire [49:0] io_fromIfu_pdWb_bits_pc_4;
  wire [49:0] io_fromIfu_pdWb_bits_pc_5;
  wire [49:0] io_fromIfu_pdWb_bits_pc_6;
  wire [49:0] io_fromIfu_pdWb_bits_pc_7;
  wire [49:0] io_fromIfu_pdWb_bits_pc_8;
  wire [49:0] io_fromIfu_pdWb_bits_pc_9;
  wire [49:0] io_fromIfu_pdWb_bits_pc_10;
  wire [49:0] io_fromIfu_pdWb_bits_pc_11;
  wire [49:0] io_fromIfu_pdWb_bits_pc_12;
  wire [49:0] io_fromIfu_pdWb_bits_pc_13;
  wire [49:0] io_fromIfu_pdWb_bits_pc_14;
  wire [49:0] io_fromIfu_pdWb_bits_pc_15;
  wire  io_fromIfu_pdWb_bits_pd_0_valid;
  wire  io_fromIfu_pdWb_bits_pd_0_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_0_brType;
  wire  io_fromIfu_pdWb_bits_pd_0_isCall;
  wire  io_fromIfu_pdWb_bits_pd_0_isRet;
  wire  io_fromIfu_pdWb_bits_pd_1_valid;
  wire  io_fromIfu_pdWb_bits_pd_1_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_1_brType;
  wire  io_fromIfu_pdWb_bits_pd_1_isCall;
  wire  io_fromIfu_pdWb_bits_pd_1_isRet;
  wire  io_fromIfu_pdWb_bits_pd_2_valid;
  wire  io_fromIfu_pdWb_bits_pd_2_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_2_brType;
  wire  io_fromIfu_pdWb_bits_pd_2_isCall;
  wire  io_fromIfu_pdWb_bits_pd_2_isRet;
  wire  io_fromIfu_pdWb_bits_pd_3_valid;
  wire  io_fromIfu_pdWb_bits_pd_3_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_3_brType;
  wire  io_fromIfu_pdWb_bits_pd_3_isCall;
  wire  io_fromIfu_pdWb_bits_pd_3_isRet;
  wire  io_fromIfu_pdWb_bits_pd_4_valid;
  wire  io_fromIfu_pdWb_bits_pd_4_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_4_brType;
  wire  io_fromIfu_pdWb_bits_pd_4_isCall;
  wire  io_fromIfu_pdWb_bits_pd_4_isRet;
  wire  io_fromIfu_pdWb_bits_pd_5_valid;
  wire  io_fromIfu_pdWb_bits_pd_5_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_5_brType;
  wire  io_fromIfu_pdWb_bits_pd_5_isCall;
  wire  io_fromIfu_pdWb_bits_pd_5_isRet;
  wire  io_fromIfu_pdWb_bits_pd_6_valid;
  wire  io_fromIfu_pdWb_bits_pd_6_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_6_brType;
  wire  io_fromIfu_pdWb_bits_pd_6_isCall;
  wire  io_fromIfu_pdWb_bits_pd_6_isRet;
  wire  io_fromIfu_pdWb_bits_pd_7_valid;
  wire  io_fromIfu_pdWb_bits_pd_7_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_7_brType;
  wire  io_fromIfu_pdWb_bits_pd_7_isCall;
  wire  io_fromIfu_pdWb_bits_pd_7_isRet;
  wire  io_fromIfu_pdWb_bits_pd_8_valid;
  wire  io_fromIfu_pdWb_bits_pd_8_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_8_brType;
  wire  io_fromIfu_pdWb_bits_pd_8_isCall;
  wire  io_fromIfu_pdWb_bits_pd_8_isRet;
  wire  io_fromIfu_pdWb_bits_pd_9_valid;
  wire  io_fromIfu_pdWb_bits_pd_9_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_9_brType;
  wire  io_fromIfu_pdWb_bits_pd_9_isCall;
  wire  io_fromIfu_pdWb_bits_pd_9_isRet;
  wire  io_fromIfu_pdWb_bits_pd_10_valid;
  wire  io_fromIfu_pdWb_bits_pd_10_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_10_brType;
  wire  io_fromIfu_pdWb_bits_pd_10_isCall;
  wire  io_fromIfu_pdWb_bits_pd_10_isRet;
  wire  io_fromIfu_pdWb_bits_pd_11_valid;
  wire  io_fromIfu_pdWb_bits_pd_11_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_11_brType;
  wire  io_fromIfu_pdWb_bits_pd_11_isCall;
  wire  io_fromIfu_pdWb_bits_pd_11_isRet;
  wire  io_fromIfu_pdWb_bits_pd_12_valid;
  wire  io_fromIfu_pdWb_bits_pd_12_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_12_brType;
  wire  io_fromIfu_pdWb_bits_pd_12_isCall;
  wire  io_fromIfu_pdWb_bits_pd_12_isRet;
  wire  io_fromIfu_pdWb_bits_pd_13_valid;
  wire  io_fromIfu_pdWb_bits_pd_13_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_13_brType;
  wire  io_fromIfu_pdWb_bits_pd_13_isCall;
  wire  io_fromIfu_pdWb_bits_pd_13_isRet;
  wire  io_fromIfu_pdWb_bits_pd_14_valid;
  wire  io_fromIfu_pdWb_bits_pd_14_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_14_brType;
  wire  io_fromIfu_pdWb_bits_pd_14_isCall;
  wire  io_fromIfu_pdWb_bits_pd_14_isRet;
  wire  io_fromIfu_pdWb_bits_pd_15_valid;
  wire  io_fromIfu_pdWb_bits_pd_15_isRVC;
  wire [1:0] io_fromIfu_pdWb_bits_pd_15_brType;
  wire  io_fromIfu_pdWb_bits_pd_15_isCall;
  wire  io_fromIfu_pdWb_bits_pd_15_isRet;
  wire  io_fromIfu_pdWb_bits_ftqIdx_flag;
  wire [5:0] io_fromIfu_pdWb_bits_ftqIdx_value;
  wire  io_fromIfu_pdWb_bits_misOffset_valid;
  wire [3:0] io_fromIfu_pdWb_bits_misOffset_bits;
  wire  io_fromIfu_pdWb_bits_cfiOffset_valid;
  wire [49:0] io_fromIfu_pdWb_bits_target;
  wire [49:0] io_fromIfu_pdWb_bits_jalTarget;
  wire  io_fromIfu_pdWb_bits_instrRange_0;
  wire  io_fromIfu_pdWb_bits_instrRange_1;
  wire  io_fromIfu_pdWb_bits_instrRange_2;
  wire  io_fromIfu_pdWb_bits_instrRange_3;
  wire  io_fromIfu_pdWb_bits_instrRange_4;
  wire  io_fromIfu_pdWb_bits_instrRange_5;
  wire  io_fromIfu_pdWb_bits_instrRange_6;
  wire  io_fromIfu_pdWb_bits_instrRange_7;
  wire  io_fromIfu_pdWb_bits_instrRange_8;
  wire  io_fromIfu_pdWb_bits_instrRange_9;
  wire  io_fromIfu_pdWb_bits_instrRange_10;
  wire  io_fromIfu_pdWb_bits_instrRange_11;
  wire  io_fromIfu_pdWb_bits_instrRange_12;
  wire  io_fromIfu_pdWb_bits_instrRange_13;
  wire  io_fromIfu_pdWb_bits_instrRange_14;
  wire  io_fromIfu_pdWb_bits_instrRange_15;
  wire  io_fromBackend_rob_commits_0_valid;
  wire [2:0] io_fromBackend_rob_commits_0_bits_commitType;
  wire  io_fromBackend_rob_commits_0_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_0_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_0_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_1_valid;
  wire [2:0] io_fromBackend_rob_commits_1_bits_commitType;
  wire  io_fromBackend_rob_commits_1_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_1_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_1_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_2_valid;
  wire [2:0] io_fromBackend_rob_commits_2_bits_commitType;
  wire  io_fromBackend_rob_commits_2_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_2_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_2_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_3_valid;
  wire [2:0] io_fromBackend_rob_commits_3_bits_commitType;
  wire  io_fromBackend_rob_commits_3_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_3_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_3_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_4_valid;
  wire [2:0] io_fromBackend_rob_commits_4_bits_commitType;
  wire  io_fromBackend_rob_commits_4_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_4_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_4_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_5_valid;
  wire [2:0] io_fromBackend_rob_commits_5_bits_commitType;
  wire  io_fromBackend_rob_commits_5_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_5_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_5_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_6_valid;
  wire [2:0] io_fromBackend_rob_commits_6_bits_commitType;
  wire  io_fromBackend_rob_commits_6_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_6_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_6_bits_ftqOffset;
  wire  io_fromBackend_rob_commits_7_valid;
  wire [2:0] io_fromBackend_rob_commits_7_bits_commitType;
  wire  io_fromBackend_rob_commits_7_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_rob_commits_7_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_rob_commits_7_bits_ftqOffset;
  wire  io_fromBackend_redirect_valid;
  wire  io_fromBackend_redirect_bits_ftqIdx_flag;
  wire [5:0] io_fromBackend_redirect_bits_ftqIdx_value;
  wire [3:0] io_fromBackend_redirect_bits_ftqOffset;
  wire  io_fromBackend_redirect_bits_level;
  wire [49:0] io_fromBackend_redirect_bits_cfiUpdate_pc;
  wire [49:0] io_fromBackend_redirect_bits_cfiUpdate_target;
  wire  io_fromBackend_redirect_bits_cfiUpdate_taken;
  wire  io_fromBackend_redirect_bits_cfiUpdate_isMisPred;
  wire  io_fromBackend_redirect_bits_cfiUpdate_backendIGPF;
  wire  io_fromBackend_redirect_bits_cfiUpdate_backendIPF;
  wire  io_fromBackend_redirect_bits_cfiUpdate_backendIAF;
  wire  io_fromBackend_ftqIdxAhead_0_valid;
  wire [5:0] io_fromBackend_ftqIdxAhead_0_bits_value;
  wire [2:0] io_fromBackend_ftqIdxSelOH_bits;
  wire  io_toBpu_redirect_valid;
  wire  io_toBpu_redirect_bits_level;
  wire [49:0] io_toBpu_redirect_bits_cfiUpdate_pc;
  wire  io_toBpu_redirect_bits_cfiUpdate_pd_isRVC;
  wire  io_toBpu_redirect_bits_cfiUpdate_pd_isCall;
  wire  io_toBpu_redirect_bits_cfiUpdate_pd_isRet;
  wire [3:0] io_toBpu_redirect_bits_cfiUpdate_ssp;
  wire [2:0] io_toBpu_redirect_bits_cfiUpdate_sctr;
  wire  io_toBpu_redirect_bits_cfiUpdate_TOSW_flag;
  wire [4:0] io_toBpu_redirect_bits_cfiUpdate_TOSW_value;
  wire  io_toBpu_redirect_bits_cfiUpdate_TOSR_flag;
  wire [4:0] io_toBpu_redirect_bits_cfiUpdate_TOSR_value;
  wire  io_toBpu_redirect_bits_cfiUpdate_NOS_flag;
  wire [4:0] io_toBpu_redirect_bits_cfiUpdate_NOS_value;
  wire  io_toBpu_redirect_bits_cfiUpdate_histPtr_flag;
  wire [7:0] io_toBpu_redirect_bits_cfiUpdate_histPtr_value;
  wire [49:0] io_toBpu_redirect_bits_cfiUpdate_target;
  wire  io_toBpu_redirect_bits_cfiUpdate_taken;
  wire [1:0] io_toBpu_redirect_bits_cfiUpdate_shift;
  wire  io_toBpu_redirect_bits_cfiUpdate_addIntoHist;
  wire  io_toBpu_update_valid;
  wire [49:0] io_toBpu_update_bits_pc;
  wire [7:0] io_toBpu_update_bits_spec_info_histPtr_value;
  wire  io_toBpu_update_bits_ftb_entry_isCall;
  wire  io_toBpu_update_bits_ftb_entry_isRet;
  wire  io_toBpu_update_bits_ftb_entry_isJalr;
  wire  io_toBpu_update_bits_ftb_entry_valid;
  wire [3:0] io_toBpu_update_bits_ftb_entry_brSlots_0_offset;
  wire  io_toBpu_update_bits_ftb_entry_brSlots_0_sharing;
  wire  io_toBpu_update_bits_ftb_entry_brSlots_0_valid;
  wire [11:0] io_toBpu_update_bits_ftb_entry_brSlots_0_lower;
  wire [1:0] io_toBpu_update_bits_ftb_entry_brSlots_0_tarStat;
  wire [3:0] io_toBpu_update_bits_ftb_entry_tailSlot_offset;
  wire  io_toBpu_update_bits_ftb_entry_tailSlot_sharing;
  wire  io_toBpu_update_bits_ftb_entry_tailSlot_valid;
  wire [19:0] io_toBpu_update_bits_ftb_entry_tailSlot_lower;
  wire [1:0] io_toBpu_update_bits_ftb_entry_tailSlot_tarStat;
  wire [3:0] io_toBpu_update_bits_ftb_entry_pftAddr;
  wire  io_toBpu_update_bits_ftb_entry_carry;
  wire  io_toBpu_update_bits_ftb_entry_last_may_be_rvi_call;
  wire  io_toBpu_update_bits_ftb_entry_strong_bias_0;
  wire  io_toBpu_update_bits_ftb_entry_strong_bias_1;
  wire  io_toBpu_update_bits_cfi_idx_valid;
  wire [3:0] io_toBpu_update_bits_cfi_idx_bits;
  wire  io_toBpu_update_bits_br_taken_mask_0;
  wire  io_toBpu_update_bits_br_taken_mask_1;
  wire  io_toBpu_update_bits_jmp_taken;
  wire  io_toBpu_update_bits_mispred_mask_0;
  wire  io_toBpu_update_bits_mispred_mask_1;
  wire  io_toBpu_update_bits_mispred_mask_2;
  wire  io_toBpu_update_bits_false_hit;
  wire  io_toBpu_update_bits_old_entry;
  wire [259:0] io_toBpu_update_bits_meta;
  wire [49:0] io_toBpu_update_bits_full_target;
  wire  io_toBpu_enq_ptr_flag;
  wire [5:0] io_toBpu_enq_ptr_value;
  wire  io_toBpu_redirctFromIFU;
  wire  io_toIfu_req_ready;
  wire  io_toIfu_req_valid;
  wire [49:0] io_toIfu_req_bits_startAddr;
  wire [49:0] io_toIfu_req_bits_nextlineStart;
  wire [49:0] io_toIfu_req_bits_nextStartAddr;
  wire  io_toIfu_req_bits_ftqIdx_flag;
  wire [5:0] io_toIfu_req_bits_ftqIdx_value;
  wire  io_toIfu_req_bits_ftqOffset_valid;
  wire [3:0] io_toIfu_req_bits_ftqOffset_bits;
  wire  io_toIfu_redirect_valid;
  wire  io_toIfu_redirect_bits_ftqIdx_flag;
  wire [5:0] io_toIfu_redirect_bits_ftqIdx_value;
  wire [3:0] io_toIfu_redirect_bits_ftqOffset;
  wire  io_toIfu_redirect_bits_level;
  wire  io_toIfu_flushFromBpu_s2_valid;
  wire  io_toIfu_flushFromBpu_s2_bits_flag;
  wire [5:0] io_toIfu_flushFromBpu_s2_bits_value;
  wire  io_toIfu_flushFromBpu_s3_valid;
  wire  io_toIfu_flushFromBpu_s3_bits_flag;
  wire [5:0] io_toIfu_flushFromBpu_s3_bits_value;
  wire  io_toICache_req_valid;
  wire [49:0] io_toICache_req_bits_pcMemRead_0_startAddr;
  wire [49:0] io_toICache_req_bits_pcMemRead_0_nextlineStart;
  wire [49:0] io_toICache_req_bits_pcMemRead_1_startAddr;
  wire [49:0] io_toICache_req_bits_pcMemRead_1_nextlineStart;
  wire [49:0] io_toICache_req_bits_pcMemRead_2_startAddr;
  wire [49:0] io_toICache_req_bits_pcMemRead_2_nextlineStart;
  wire [49:0] io_toICache_req_bits_pcMemRead_3_startAddr;
  wire [49:0] io_toICache_req_bits_pcMemRead_3_nextlineStart;
  wire [49:0] io_toICache_req_bits_pcMemRead_4_startAddr;
  wire [49:0] io_toICache_req_bits_pcMemRead_4_nextlineStart;
  wire  io_toICache_req_bits_readValid_0;
  wire  io_toICache_req_bits_readValid_1;
  wire  io_toICache_req_bits_readValid_2;
  wire  io_toICache_req_bits_readValid_3;
  wire  io_toICache_req_bits_readValid_4;
  wire  io_toICache_req_bits_backendException;
  wire  io_toBackend_pc_mem_wen;
  wire [5:0] io_toBackend_pc_mem_waddr;
  wire [49:0] io_toBackend_pc_mem_wdata_startAddr;
  wire  io_toBackend_newest_entry_en;
  wire [49:0] io_toBackend_newest_entry_target;
  wire [5:0] io_toBackend_newest_entry_ptr_value;
  wire  io_toPrefetch_req_ready;
  wire  io_toPrefetch_req_valid;
  wire [49:0] io_toPrefetch_req_bits_startAddr;
  wire [49:0] io_toPrefetch_req_bits_nextlineStart;
  wire  io_toPrefetch_req_bits_ftqIdx_flag;
  wire [5:0] io_toPrefetch_req_bits_ftqIdx_value;
  wire  io_toPrefetch_flushFromBpu_s2_valid;
  wire  io_toPrefetch_flushFromBpu_s2_bits_flag;
  wire [5:0] io_toPrefetch_flushFromBpu_s2_bits_value;
  wire  io_toPrefetch_flushFromBpu_s3_valid;
  wire  io_toPrefetch_flushFromBpu_s3_bits_flag;
  wire [5:0] io_toPrefetch_flushFromBpu_s3_bits_value;
  wire [1:0] io_toPrefetch_backendException;
  wire  io_icacheFlush;
  wire  io_mmioCommitRead_mmioFtqPtr_flag;
  wire [5:0] io_mmioCommitRead_mmioFtqPtr_value;
  wire  io_mmioCommitRead_mmioLastCommit;
  wire [5:0] io_perf_0_value;
  wire [5:0] io_perf_1_value;
  wire [5:0] io_perf_2_value;
  wire [5:0] io_perf_3_value;
  wire [5:0] io_perf_4_value;
  wire [5:0] io_perf_5_value;
  wire [5:0] io_perf_6_value;
  wire [5:0] io_perf_7_value;
  wire [5:0] io_perf_8_value;
  wire [5:0] io_perf_9_value;
  wire [5:0] io_perf_10_value;
  wire [5:0] io_perf_11_value;
  wire [5:0] io_perf_12_value;
  wire [5:0] io_perf_13_value;
  wire [5:0] io_perf_14_value;
  wire [5:0] io_perf_15_value;
  wire [5:0] io_perf_16_value;
  wire [5:0] io_perf_17_value;
  wire [5:0] io_perf_18_value;
  wire [5:0] io_perf_19_value;
  wire [5:0] io_perf_20_value;
  wire [5:0] io_perf_21_value;
  wire [5:0] io_perf_22_value;
  wire [5:0] io_perf_23_value;


 Ftq Ftq(
    .clock(clock),
    .reset(reset),
    .io_fromBpu_resp_ready(io_fromBpu_resp_ready),
    .io_fromBpu_resp_valid(io_fromBpu_resp_valid),
    .io_fromBpu_resp_bits_s1_pc_3(io_fromBpu_resp_bits_s1_pc_3),
    .io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0(io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0),
    .io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1(io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1),
    .io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0(io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0),
    .io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1(io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1),
    .io_fromBpu_resp_bits_s1_full_pred_3_targets_0(io_fromBpu_resp_bits_s1_full_pred_3_targets_0),
    .io_fromBpu_resp_bits_s1_full_pred_3_targets_1(io_fromBpu_resp_bits_s1_full_pred_3_targets_1),
    .io_fromBpu_resp_bits_s1_full_pred_3_offsets_0(io_fromBpu_resp_bits_s1_full_pred_3_offsets_0),
    .io_fromBpu_resp_bits_s1_full_pred_3_offsets_1(io_fromBpu_resp_bits_s1_full_pred_3_offsets_1),
    .io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddr(io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddr),
    .io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErr(io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErr),
    .io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharing(io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharing),
    .io_fromBpu_resp_bits_s1_full_pred_3_hit(io_fromBpu_resp_bits_s1_full_pred_3_hit),
    .io_fromBpu_resp_bits_s2_pc_3(io_fromBpu_resp_bits_s2_pc_3),
    .io_fromBpu_resp_bits_s2_valid_3(io_fromBpu_resp_bits_s2_valid_3),
    .io_fromBpu_resp_bits_s2_hasRedirect_3(io_fromBpu_resp_bits_s2_hasRedirect_3),
    .io_fromBpu_resp_bits_s2_ftq_idx_flag(io_fromBpu_resp_bits_s2_ftq_idx_flag),
    .io_fromBpu_resp_bits_s2_ftq_idx_value(io_fromBpu_resp_bits_s2_ftq_idx_value),
    .io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0(io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0),
    .io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1(io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1),
    .io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0(io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0),
    .io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1(io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1),
    .io_fromBpu_resp_bits_s2_full_pred_3_targets_0(io_fromBpu_resp_bits_s2_full_pred_3_targets_0),
    .io_fromBpu_resp_bits_s2_full_pred_3_targets_1(io_fromBpu_resp_bits_s2_full_pred_3_targets_1),
    .io_fromBpu_resp_bits_s2_full_pred_3_offsets_0(io_fromBpu_resp_bits_s2_full_pred_3_offsets_0),
    .io_fromBpu_resp_bits_s2_full_pred_3_offsets_1(io_fromBpu_resp_bits_s2_full_pred_3_offsets_1),
    .io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddr(io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddr),
    .io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErr(io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErr),
    .io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharing(io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharing),
    .io_fromBpu_resp_bits_s2_full_pred_3_hit(io_fromBpu_resp_bits_s2_full_pred_3_hit),
    .io_fromBpu_resp_bits_s3_pc_3(io_fromBpu_resp_bits_s3_pc_3),
    .io_fromBpu_resp_bits_s3_valid_3(io_fromBpu_resp_bits_s3_valid_3),
    .io_fromBpu_resp_bits_s3_hasRedirect_3(io_fromBpu_resp_bits_s3_hasRedirect_3),
    .io_fromBpu_resp_bits_s3_ftq_idx_flag(io_fromBpu_resp_bits_s3_ftq_idx_flag),
    .io_fromBpu_resp_bits_s3_ftq_idx_value(io_fromBpu_resp_bits_s3_ftq_idx_value),
    .io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0(io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0),
    .io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1(io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1),
    .io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0(io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0),
    .io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1(io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1),
    .io_fromBpu_resp_bits_s3_full_pred_3_targets_0(io_fromBpu_resp_bits_s3_full_pred_3_targets_0),
    .io_fromBpu_resp_bits_s3_full_pred_3_targets_1(io_fromBpu_resp_bits_s3_full_pred_3_targets_1),
    .io_fromBpu_resp_bits_s3_full_pred_3_offsets_0(io_fromBpu_resp_bits_s3_full_pred_3_offsets_0),
    .io_fromBpu_resp_bits_s3_full_pred_3_offsets_1(io_fromBpu_resp_bits_s3_full_pred_3_offsets_1),
    .io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddr(io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddr),
    .io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErr(io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErr),
    .io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharing(io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharing),
    .io_fromBpu_resp_bits_s3_full_pred_3_hit(io_fromBpu_resp_bits_s3_full_pred_3_hit),
    .io_fromBpu_resp_bits_last_stage_meta(io_fromBpu_resp_bits_last_stage_meta),
    .io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flag(io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flag),
    .io_fromBpu_resp_bits_last_stage_spec_info_histPtr_value(io_fromBpu_resp_bits_last_stage_spec_info_histPtr_value),
    .io_fromBpu_resp_bits_last_stage_spec_info_ssp(io_fromBpu_resp_bits_last_stage_spec_info_ssp),
    .io_fromBpu_resp_bits_last_stage_spec_info_sctr(io_fromBpu_resp_bits_last_stage_spec_info_sctr),
    .io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flag(io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flag),
    .io_fromBpu_resp_bits_last_stage_spec_info_TOSW_value(io_fromBpu_resp_bits_last_stage_spec_info_TOSW_value),
    .io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flag(io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flag),
    .io_fromBpu_resp_bits_last_stage_spec_info_TOSR_value(io_fromBpu_resp_bits_last_stage_spec_info_TOSR_value),
    .io_fromBpu_resp_bits_last_stage_spec_info_NOS_flag(io_fromBpu_resp_bits_last_stage_spec_info_NOS_flag),
    .io_fromBpu_resp_bits_last_stage_spec_info_NOS_value(io_fromBpu_resp_bits_last_stage_spec_info_NOS_value),
    .io_fromBpu_resp_bits_last_stage_spec_info_topAddr(io_fromBpu_resp_bits_last_stage_spec_info_topAddr),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_isCall(io_fromBpu_resp_bits_last_stage_ftb_entry_isCall),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_isRet(io_fromBpu_resp_bits_last_stage_ftb_entry_isRet),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_isJalr(io_fromBpu_resp_bits_last_stage_ftb_entry_isJalr),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_valid(io_fromBpu_resp_bits_last_stage_ftb_entry_valid),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offset(io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offset),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharing(io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharing),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_valid(io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_valid),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lower(io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lower),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStat(io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStat),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offset(io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offset),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharing(io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharing),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_valid(io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_valid),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lower(io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lower),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStat(io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStat),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddr(io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddr),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_carry(io_fromBpu_resp_bits_last_stage_ftb_entry_carry),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_call(io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_call),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0(io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0),
    .io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1(io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1),
    .io_fromIfu_pdWb_valid(io_fromIfu_pdWb_valid),
    .io_fromIfu_pdWb_bits_pc_0(io_fromIfu_pdWb_bits_pc_0),
    .io_fromIfu_pdWb_bits_pc_1(io_fromIfu_pdWb_bits_pc_1),
    .io_fromIfu_pdWb_bits_pc_2(io_fromIfu_pdWb_bits_pc_2),
    .io_fromIfu_pdWb_bits_pc_3(io_fromIfu_pdWb_bits_pc_3),
    .io_fromIfu_pdWb_bits_pc_4(io_fromIfu_pdWb_bits_pc_4),
    .io_fromIfu_pdWb_bits_pc_5(io_fromIfu_pdWb_bits_pc_5),
    .io_fromIfu_pdWb_bits_pc_6(io_fromIfu_pdWb_bits_pc_6),
    .io_fromIfu_pdWb_bits_pc_7(io_fromIfu_pdWb_bits_pc_7),
    .io_fromIfu_pdWb_bits_pc_8(io_fromIfu_pdWb_bits_pc_8),
    .io_fromIfu_pdWb_bits_pc_9(io_fromIfu_pdWb_bits_pc_9),
    .io_fromIfu_pdWb_bits_pc_10(io_fromIfu_pdWb_bits_pc_10),
    .io_fromIfu_pdWb_bits_pc_11(io_fromIfu_pdWb_bits_pc_11),
    .io_fromIfu_pdWb_bits_pc_12(io_fromIfu_pdWb_bits_pc_12),
    .io_fromIfu_pdWb_bits_pc_13(io_fromIfu_pdWb_bits_pc_13),
    .io_fromIfu_pdWb_bits_pc_14(io_fromIfu_pdWb_bits_pc_14),
    .io_fromIfu_pdWb_bits_pc_15(io_fromIfu_pdWb_bits_pc_15),
    .io_fromIfu_pdWb_bits_pd_0_valid(io_fromIfu_pdWb_bits_pd_0_valid),
    .io_fromIfu_pdWb_bits_pd_0_isRVC(io_fromIfu_pdWb_bits_pd_0_isRVC),
    .io_fromIfu_pdWb_bits_pd_0_brType(io_fromIfu_pdWb_bits_pd_0_brType),
    .io_fromIfu_pdWb_bits_pd_0_isCall(io_fromIfu_pdWb_bits_pd_0_isCall),
    .io_fromIfu_pdWb_bits_pd_0_isRet(io_fromIfu_pdWb_bits_pd_0_isRet),
    .io_fromIfu_pdWb_bits_pd_1_valid(io_fromIfu_pdWb_bits_pd_1_valid),
    .io_fromIfu_pdWb_bits_pd_1_isRVC(io_fromIfu_pdWb_bits_pd_1_isRVC),
    .io_fromIfu_pdWb_bits_pd_1_brType(io_fromIfu_pdWb_bits_pd_1_brType),
    .io_fromIfu_pdWb_bits_pd_1_isCall(io_fromIfu_pdWb_bits_pd_1_isCall),
    .io_fromIfu_pdWb_bits_pd_1_isRet(io_fromIfu_pdWb_bits_pd_1_isRet),
    .io_fromIfu_pdWb_bits_pd_2_valid(io_fromIfu_pdWb_bits_pd_2_valid),
    .io_fromIfu_pdWb_bits_pd_2_isRVC(io_fromIfu_pdWb_bits_pd_2_isRVC),
    .io_fromIfu_pdWb_bits_pd_2_brType(io_fromIfu_pdWb_bits_pd_2_brType),
    .io_fromIfu_pdWb_bits_pd_2_isCall(io_fromIfu_pdWb_bits_pd_2_isCall),
    .io_fromIfu_pdWb_bits_pd_2_isRet(io_fromIfu_pdWb_bits_pd_2_isRet),
    .io_fromIfu_pdWb_bits_pd_3_valid(io_fromIfu_pdWb_bits_pd_3_valid),
    .io_fromIfu_pdWb_bits_pd_3_isRVC(io_fromIfu_pdWb_bits_pd_3_isRVC),
    .io_fromIfu_pdWb_bits_pd_3_brType(io_fromIfu_pdWb_bits_pd_3_brType),
    .io_fromIfu_pdWb_bits_pd_3_isCall(io_fromIfu_pdWb_bits_pd_3_isCall),
    .io_fromIfu_pdWb_bits_pd_3_isRet(io_fromIfu_pdWb_bits_pd_3_isRet),
    .io_fromIfu_pdWb_bits_pd_4_valid(io_fromIfu_pdWb_bits_pd_4_valid),
    .io_fromIfu_pdWb_bits_pd_4_isRVC(io_fromIfu_pdWb_bits_pd_4_isRVC),
    .io_fromIfu_pdWb_bits_pd_4_brType(io_fromIfu_pdWb_bits_pd_4_brType),
    .io_fromIfu_pdWb_bits_pd_4_isCall(io_fromIfu_pdWb_bits_pd_4_isCall),
    .io_fromIfu_pdWb_bits_pd_4_isRet(io_fromIfu_pdWb_bits_pd_4_isRet),
    .io_fromIfu_pdWb_bits_pd_5_valid(io_fromIfu_pdWb_bits_pd_5_valid),
    .io_fromIfu_pdWb_bits_pd_5_isRVC(io_fromIfu_pdWb_bits_pd_5_isRVC),
    .io_fromIfu_pdWb_bits_pd_5_brType(io_fromIfu_pdWb_bits_pd_5_brType),
    .io_fromIfu_pdWb_bits_pd_5_isCall(io_fromIfu_pdWb_bits_pd_5_isCall),
    .io_fromIfu_pdWb_bits_pd_5_isRet(io_fromIfu_pdWb_bits_pd_5_isRet),
    .io_fromIfu_pdWb_bits_pd_6_valid(io_fromIfu_pdWb_bits_pd_6_valid),
    .io_fromIfu_pdWb_bits_pd_6_isRVC(io_fromIfu_pdWb_bits_pd_6_isRVC),
    .io_fromIfu_pdWb_bits_pd_6_brType(io_fromIfu_pdWb_bits_pd_6_brType),
    .io_fromIfu_pdWb_bits_pd_6_isCall(io_fromIfu_pdWb_bits_pd_6_isCall),
    .io_fromIfu_pdWb_bits_pd_6_isRet(io_fromIfu_pdWb_bits_pd_6_isRet),
    .io_fromIfu_pdWb_bits_pd_7_valid(io_fromIfu_pdWb_bits_pd_7_valid),
    .io_fromIfu_pdWb_bits_pd_7_isRVC(io_fromIfu_pdWb_bits_pd_7_isRVC),
    .io_fromIfu_pdWb_bits_pd_7_brType(io_fromIfu_pdWb_bits_pd_7_brType),
    .io_fromIfu_pdWb_bits_pd_7_isCall(io_fromIfu_pdWb_bits_pd_7_isCall),
    .io_fromIfu_pdWb_bits_pd_7_isRet(io_fromIfu_pdWb_bits_pd_7_isRet),
    .io_fromIfu_pdWb_bits_pd_8_valid(io_fromIfu_pdWb_bits_pd_8_valid),
    .io_fromIfu_pdWb_bits_pd_8_isRVC(io_fromIfu_pdWb_bits_pd_8_isRVC),
    .io_fromIfu_pdWb_bits_pd_8_brType(io_fromIfu_pdWb_bits_pd_8_brType),
    .io_fromIfu_pdWb_bits_pd_8_isCall(io_fromIfu_pdWb_bits_pd_8_isCall),
    .io_fromIfu_pdWb_bits_pd_8_isRet(io_fromIfu_pdWb_bits_pd_8_isRet),
    .io_fromIfu_pdWb_bits_pd_9_valid(io_fromIfu_pdWb_bits_pd_9_valid),
    .io_fromIfu_pdWb_bits_pd_9_isRVC(io_fromIfu_pdWb_bits_pd_9_isRVC),
    .io_fromIfu_pdWb_bits_pd_9_brType(io_fromIfu_pdWb_bits_pd_9_brType),
    .io_fromIfu_pdWb_bits_pd_9_isCall(io_fromIfu_pdWb_bits_pd_9_isCall),
    .io_fromIfu_pdWb_bits_pd_9_isRet(io_fromIfu_pdWb_bits_pd_9_isRet),
    .io_fromIfu_pdWb_bits_pd_10_valid(io_fromIfu_pdWb_bits_pd_10_valid),
    .io_fromIfu_pdWb_bits_pd_10_isRVC(io_fromIfu_pdWb_bits_pd_10_isRVC),
    .io_fromIfu_pdWb_bits_pd_10_brType(io_fromIfu_pdWb_bits_pd_10_brType),
    .io_fromIfu_pdWb_bits_pd_10_isCall(io_fromIfu_pdWb_bits_pd_10_isCall),
    .io_fromIfu_pdWb_bits_pd_10_isRet(io_fromIfu_pdWb_bits_pd_10_isRet),
    .io_fromIfu_pdWb_bits_pd_11_valid(io_fromIfu_pdWb_bits_pd_11_valid),
    .io_fromIfu_pdWb_bits_pd_11_isRVC(io_fromIfu_pdWb_bits_pd_11_isRVC),
    .io_fromIfu_pdWb_bits_pd_11_brType(io_fromIfu_pdWb_bits_pd_11_brType),
    .io_fromIfu_pdWb_bits_pd_11_isCall(io_fromIfu_pdWb_bits_pd_11_isCall),
    .io_fromIfu_pdWb_bits_pd_11_isRet(io_fromIfu_pdWb_bits_pd_11_isRet),
    .io_fromIfu_pdWb_bits_pd_12_valid(io_fromIfu_pdWb_bits_pd_12_valid),
    .io_fromIfu_pdWb_bits_pd_12_isRVC(io_fromIfu_pdWb_bits_pd_12_isRVC),
    .io_fromIfu_pdWb_bits_pd_12_brType(io_fromIfu_pdWb_bits_pd_12_brType),
    .io_fromIfu_pdWb_bits_pd_12_isCall(io_fromIfu_pdWb_bits_pd_12_isCall),
    .io_fromIfu_pdWb_bits_pd_12_isRet(io_fromIfu_pdWb_bits_pd_12_isRet),
    .io_fromIfu_pdWb_bits_pd_13_valid(io_fromIfu_pdWb_bits_pd_13_valid),
    .io_fromIfu_pdWb_bits_pd_13_isRVC(io_fromIfu_pdWb_bits_pd_13_isRVC),
    .io_fromIfu_pdWb_bits_pd_13_brType(io_fromIfu_pdWb_bits_pd_13_brType),
    .io_fromIfu_pdWb_bits_pd_13_isCall(io_fromIfu_pdWb_bits_pd_13_isCall),
    .io_fromIfu_pdWb_bits_pd_13_isRet(io_fromIfu_pdWb_bits_pd_13_isRet),
    .io_fromIfu_pdWb_bits_pd_14_valid(io_fromIfu_pdWb_bits_pd_14_valid),
    .io_fromIfu_pdWb_bits_pd_14_isRVC(io_fromIfu_pdWb_bits_pd_14_isRVC),
    .io_fromIfu_pdWb_bits_pd_14_brType(io_fromIfu_pdWb_bits_pd_14_brType),
    .io_fromIfu_pdWb_bits_pd_14_isCall(io_fromIfu_pdWb_bits_pd_14_isCall),
    .io_fromIfu_pdWb_bits_pd_14_isRet(io_fromIfu_pdWb_bits_pd_14_isRet),
    .io_fromIfu_pdWb_bits_pd_15_valid(io_fromIfu_pdWb_bits_pd_15_valid),
    .io_fromIfu_pdWb_bits_pd_15_isRVC(io_fromIfu_pdWb_bits_pd_15_isRVC),
    .io_fromIfu_pdWb_bits_pd_15_brType(io_fromIfu_pdWb_bits_pd_15_brType),
    .io_fromIfu_pdWb_bits_pd_15_isCall(io_fromIfu_pdWb_bits_pd_15_isCall),
    .io_fromIfu_pdWb_bits_pd_15_isRet(io_fromIfu_pdWb_bits_pd_15_isRet),
    .io_fromIfu_pdWb_bits_ftqIdx_flag(io_fromIfu_pdWb_bits_ftqIdx_flag),
    .io_fromIfu_pdWb_bits_ftqIdx_value(io_fromIfu_pdWb_bits_ftqIdx_value),
    .io_fromIfu_pdWb_bits_misOffset_valid(io_fromIfu_pdWb_bits_misOffset_valid),
    .io_fromIfu_pdWb_bits_misOffset_bits(io_fromIfu_pdWb_bits_misOffset_bits),
    .io_fromIfu_pdWb_bits_cfiOffset_valid(io_fromIfu_pdWb_bits_cfiOffset_valid),
    .io_fromIfu_pdWb_bits_target(io_fromIfu_pdWb_bits_target),
    .io_fromIfu_pdWb_bits_jalTarget(io_fromIfu_pdWb_bits_jalTarget),
    .io_fromIfu_pdWb_bits_instrRange_0(io_fromIfu_pdWb_bits_instrRange_0),
    .io_fromIfu_pdWb_bits_instrRange_1(io_fromIfu_pdWb_bits_instrRange_1),
    .io_fromIfu_pdWb_bits_instrRange_2(io_fromIfu_pdWb_bits_instrRange_2),
    .io_fromIfu_pdWb_bits_instrRange_3(io_fromIfu_pdWb_bits_instrRange_3),
    .io_fromIfu_pdWb_bits_instrRange_4(io_fromIfu_pdWb_bits_instrRange_4),
    .io_fromIfu_pdWb_bits_instrRange_5(io_fromIfu_pdWb_bits_instrRange_5),
    .io_fromIfu_pdWb_bits_instrRange_6(io_fromIfu_pdWb_bits_instrRange_6),
    .io_fromIfu_pdWb_bits_instrRange_7(io_fromIfu_pdWb_bits_instrRange_7),
    .io_fromIfu_pdWb_bits_instrRange_8(io_fromIfu_pdWb_bits_instrRange_8),
    .io_fromIfu_pdWb_bits_instrRange_9(io_fromIfu_pdWb_bits_instrRange_9),
    .io_fromIfu_pdWb_bits_instrRange_10(io_fromIfu_pdWb_bits_instrRange_10),
    .io_fromIfu_pdWb_bits_instrRange_11(io_fromIfu_pdWb_bits_instrRange_11),
    .io_fromIfu_pdWb_bits_instrRange_12(io_fromIfu_pdWb_bits_instrRange_12),
    .io_fromIfu_pdWb_bits_instrRange_13(io_fromIfu_pdWb_bits_instrRange_13),
    .io_fromIfu_pdWb_bits_instrRange_14(io_fromIfu_pdWb_bits_instrRange_14),
    .io_fromIfu_pdWb_bits_instrRange_15(io_fromIfu_pdWb_bits_instrRange_15),
    .io_fromBackend_rob_commits_0_valid(io_fromBackend_rob_commits_0_valid),
    .io_fromBackend_rob_commits_0_bits_commitType(io_fromBackend_rob_commits_0_bits_commitType),
    .io_fromBackend_rob_commits_0_bits_ftqIdx_flag(io_fromBackend_rob_commits_0_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_0_bits_ftqIdx_value(io_fromBackend_rob_commits_0_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_0_bits_ftqOffset(io_fromBackend_rob_commits_0_bits_ftqOffset),
    .io_fromBackend_rob_commits_1_valid(io_fromBackend_rob_commits_1_valid),
    .io_fromBackend_rob_commits_1_bits_commitType(io_fromBackend_rob_commits_1_bits_commitType),
    .io_fromBackend_rob_commits_1_bits_ftqIdx_flag(io_fromBackend_rob_commits_1_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_1_bits_ftqIdx_value(io_fromBackend_rob_commits_1_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_1_bits_ftqOffset(io_fromBackend_rob_commits_1_bits_ftqOffset),
    .io_fromBackend_rob_commits_2_valid(io_fromBackend_rob_commits_2_valid),
    .io_fromBackend_rob_commits_2_bits_commitType(io_fromBackend_rob_commits_2_bits_commitType),
    .io_fromBackend_rob_commits_2_bits_ftqIdx_flag(io_fromBackend_rob_commits_2_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_2_bits_ftqIdx_value(io_fromBackend_rob_commits_2_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_2_bits_ftqOffset(io_fromBackend_rob_commits_2_bits_ftqOffset),
    .io_fromBackend_rob_commits_3_valid(io_fromBackend_rob_commits_3_valid),
    .io_fromBackend_rob_commits_3_bits_commitType(io_fromBackend_rob_commits_3_bits_commitType),
    .io_fromBackend_rob_commits_3_bits_ftqIdx_flag(io_fromBackend_rob_commits_3_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_3_bits_ftqIdx_value(io_fromBackend_rob_commits_3_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_3_bits_ftqOffset(io_fromBackend_rob_commits_3_bits_ftqOffset),
    .io_fromBackend_rob_commits_4_valid(io_fromBackend_rob_commits_4_valid),
    .io_fromBackend_rob_commits_4_bits_commitType(io_fromBackend_rob_commits_4_bits_commitType),
    .io_fromBackend_rob_commits_4_bits_ftqIdx_flag(io_fromBackend_rob_commits_4_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_4_bits_ftqIdx_value(io_fromBackend_rob_commits_4_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_4_bits_ftqOffset(io_fromBackend_rob_commits_4_bits_ftqOffset),
    .io_fromBackend_rob_commits_5_valid(io_fromBackend_rob_commits_5_valid),
    .io_fromBackend_rob_commits_5_bits_commitType(io_fromBackend_rob_commits_5_bits_commitType),
    .io_fromBackend_rob_commits_5_bits_ftqIdx_flag(io_fromBackend_rob_commits_5_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_5_bits_ftqIdx_value(io_fromBackend_rob_commits_5_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_5_bits_ftqOffset(io_fromBackend_rob_commits_5_bits_ftqOffset),
    .io_fromBackend_rob_commits_6_valid(io_fromBackend_rob_commits_6_valid),
    .io_fromBackend_rob_commits_6_bits_commitType(io_fromBackend_rob_commits_6_bits_commitType),
    .io_fromBackend_rob_commits_6_bits_ftqIdx_flag(io_fromBackend_rob_commits_6_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_6_bits_ftqIdx_value(io_fromBackend_rob_commits_6_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_6_bits_ftqOffset(io_fromBackend_rob_commits_6_bits_ftqOffset),
    .io_fromBackend_rob_commits_7_valid(io_fromBackend_rob_commits_7_valid),
    .io_fromBackend_rob_commits_7_bits_commitType(io_fromBackend_rob_commits_7_bits_commitType),
    .io_fromBackend_rob_commits_7_bits_ftqIdx_flag(io_fromBackend_rob_commits_7_bits_ftqIdx_flag),
    .io_fromBackend_rob_commits_7_bits_ftqIdx_value(io_fromBackend_rob_commits_7_bits_ftqIdx_value),
    .io_fromBackend_rob_commits_7_bits_ftqOffset(io_fromBackend_rob_commits_7_bits_ftqOffset),
    .io_fromBackend_redirect_valid(io_fromBackend_redirect_valid),
    .io_fromBackend_redirect_bits_ftqIdx_flag(io_fromBackend_redirect_bits_ftqIdx_flag),
    .io_fromBackend_redirect_bits_ftqIdx_value(io_fromBackend_redirect_bits_ftqIdx_value),
    .io_fromBackend_redirect_bits_ftqOffset(io_fromBackend_redirect_bits_ftqOffset),
    .io_fromBackend_redirect_bits_level(io_fromBackend_redirect_bits_level),
    .io_fromBackend_redirect_bits_cfiUpdate_pc(io_fromBackend_redirect_bits_cfiUpdate_pc),
    .io_fromBackend_redirect_bits_cfiUpdate_target(io_fromBackend_redirect_bits_cfiUpdate_target),
    .io_fromBackend_redirect_bits_cfiUpdate_taken(io_fromBackend_redirect_bits_cfiUpdate_taken),
    .io_fromBackend_redirect_bits_cfiUpdate_isMisPred(io_fromBackend_redirect_bits_cfiUpdate_isMisPred),
    .io_fromBackend_redirect_bits_cfiUpdate_backendIGPF(io_fromBackend_redirect_bits_cfiUpdate_backendIGPF),
    .io_fromBackend_redirect_bits_cfiUpdate_backendIPF(io_fromBackend_redirect_bits_cfiUpdate_backendIPF),
    .io_fromBackend_redirect_bits_cfiUpdate_backendIAF(io_fromBackend_redirect_bits_cfiUpdate_backendIAF),
    .io_fromBackend_ftqIdxAhead_0_valid(io_fromBackend_ftqIdxAhead_0_valid),
    .io_fromBackend_ftqIdxAhead_0_bits_value(io_fromBackend_ftqIdxAhead_0_bits_value),
    .io_fromBackend_ftqIdxSelOH_bits(io_fromBackend_ftqIdxSelOH_bits),
    .io_toBpu_redirect_valid(io_toBpu_redirect_valid),
    .io_toBpu_redirect_bits_level(io_toBpu_redirect_bits_level),
    .io_toBpu_redirect_bits_cfiUpdate_pc(io_toBpu_redirect_bits_cfiUpdate_pc),
    .io_toBpu_redirect_bits_cfiUpdate_pd_isRVC(io_toBpu_redirect_bits_cfiUpdate_pd_isRVC),
    .io_toBpu_redirect_bits_cfiUpdate_pd_isCall(io_toBpu_redirect_bits_cfiUpdate_pd_isCall),
    .io_toBpu_redirect_bits_cfiUpdate_pd_isRet(io_toBpu_redirect_bits_cfiUpdate_pd_isRet),
    .io_toBpu_redirect_bits_cfiUpdate_ssp(io_toBpu_redirect_bits_cfiUpdate_ssp),
    .io_toBpu_redirect_bits_cfiUpdate_sctr(io_toBpu_redirect_bits_cfiUpdate_sctr),
    .io_toBpu_redirect_bits_cfiUpdate_TOSW_flag(io_toBpu_redirect_bits_cfiUpdate_TOSW_flag),
    .io_toBpu_redirect_bits_cfiUpdate_TOSW_value(io_toBpu_redirect_bits_cfiUpdate_TOSW_value),
    .io_toBpu_redirect_bits_cfiUpdate_TOSR_flag(io_toBpu_redirect_bits_cfiUpdate_TOSR_flag),
    .io_toBpu_redirect_bits_cfiUpdate_TOSR_value(io_toBpu_redirect_bits_cfiUpdate_TOSR_value),
    .io_toBpu_redirect_bits_cfiUpdate_NOS_flag(io_toBpu_redirect_bits_cfiUpdate_NOS_flag),
    .io_toBpu_redirect_bits_cfiUpdate_NOS_value(io_toBpu_redirect_bits_cfiUpdate_NOS_value),
    .io_toBpu_redirect_bits_cfiUpdate_histPtr_flag(io_toBpu_redirect_bits_cfiUpdate_histPtr_flag),
    .io_toBpu_redirect_bits_cfiUpdate_histPtr_value(io_toBpu_redirect_bits_cfiUpdate_histPtr_value),
    .io_toBpu_redirect_bits_cfiUpdate_target(io_toBpu_redirect_bits_cfiUpdate_target),
    .io_toBpu_redirect_bits_cfiUpdate_taken(io_toBpu_redirect_bits_cfiUpdate_taken),
    .io_toBpu_redirect_bits_cfiUpdate_shift(io_toBpu_redirect_bits_cfiUpdate_shift),
    .io_toBpu_redirect_bits_cfiUpdate_addIntoHist(io_toBpu_redirect_bits_cfiUpdate_addIntoHist),
    .io_toBpu_update_valid(io_toBpu_update_valid),
    .io_toBpu_update_bits_pc(io_toBpu_update_bits_pc),
    .io_toBpu_update_bits_spec_info_histPtr_value(io_toBpu_update_bits_spec_info_histPtr_value),
    .io_toBpu_update_bits_ftb_entry_isCall(io_toBpu_update_bits_ftb_entry_isCall),
    .io_toBpu_update_bits_ftb_entry_isRet(io_toBpu_update_bits_ftb_entry_isRet),
    .io_toBpu_update_bits_ftb_entry_isJalr(io_toBpu_update_bits_ftb_entry_isJalr),
    .io_toBpu_update_bits_ftb_entry_valid(io_toBpu_update_bits_ftb_entry_valid),
    .io_toBpu_update_bits_ftb_entry_brSlots_0_offset(io_toBpu_update_bits_ftb_entry_brSlots_0_offset),
    .io_toBpu_update_bits_ftb_entry_brSlots_0_sharing(io_toBpu_update_bits_ftb_entry_brSlots_0_sharing),
    .io_toBpu_update_bits_ftb_entry_brSlots_0_valid(io_toBpu_update_bits_ftb_entry_brSlots_0_valid),
    .io_toBpu_update_bits_ftb_entry_brSlots_0_lower(io_toBpu_update_bits_ftb_entry_brSlots_0_lower),
    .io_toBpu_update_bits_ftb_entry_brSlots_0_tarStat(io_toBpu_update_bits_ftb_entry_brSlots_0_tarStat),
    .io_toBpu_update_bits_ftb_entry_tailSlot_offset(io_toBpu_update_bits_ftb_entry_tailSlot_offset),
    .io_toBpu_update_bits_ftb_entry_tailSlot_sharing(io_toBpu_update_bits_ftb_entry_tailSlot_sharing),
    .io_toBpu_update_bits_ftb_entry_tailSlot_valid(io_toBpu_update_bits_ftb_entry_tailSlot_valid),
    .io_toBpu_update_bits_ftb_entry_tailSlot_lower(io_toBpu_update_bits_ftb_entry_tailSlot_lower),
    .io_toBpu_update_bits_ftb_entry_tailSlot_tarStat(io_toBpu_update_bits_ftb_entry_tailSlot_tarStat),
    .io_toBpu_update_bits_ftb_entry_pftAddr(io_toBpu_update_bits_ftb_entry_pftAddr),
    .io_toBpu_update_bits_ftb_entry_carry(io_toBpu_update_bits_ftb_entry_carry),
    .io_toBpu_update_bits_ftb_entry_last_may_be_rvi_call(io_toBpu_update_bits_ftb_entry_last_may_be_rvi_call),
    .io_toBpu_update_bits_ftb_entry_strong_bias_0(io_toBpu_update_bits_ftb_entry_strong_bias_0),
    .io_toBpu_update_bits_ftb_entry_strong_bias_1(io_toBpu_update_bits_ftb_entry_strong_bias_1),
    .io_toBpu_update_bits_cfi_idx_valid(io_toBpu_update_bits_cfi_idx_valid),
    .io_toBpu_update_bits_cfi_idx_bits(io_toBpu_update_bits_cfi_idx_bits),
    .io_toBpu_update_bits_br_taken_mask_0(io_toBpu_update_bits_br_taken_mask_0),
    .io_toBpu_update_bits_br_taken_mask_1(io_toBpu_update_bits_br_taken_mask_1),
    .io_toBpu_update_bits_jmp_taken(io_toBpu_update_bits_jmp_taken),
    .io_toBpu_update_bits_mispred_mask_0(io_toBpu_update_bits_mispred_mask_0),
    .io_toBpu_update_bits_mispred_mask_1(io_toBpu_update_bits_mispred_mask_1),
    .io_toBpu_update_bits_mispred_mask_2(io_toBpu_update_bits_mispred_mask_2),
    .io_toBpu_update_bits_false_hit(io_toBpu_update_bits_false_hit),
    .io_toBpu_update_bits_old_entry(io_toBpu_update_bits_old_entry),
    .io_toBpu_update_bits_meta(io_toBpu_update_bits_meta),
    .io_toBpu_update_bits_full_target(io_toBpu_update_bits_full_target),
    .io_toBpu_enq_ptr_flag(io_toBpu_enq_ptr_flag),
    .io_toBpu_enq_ptr_value(io_toBpu_enq_ptr_value),
    .io_toBpu_redirctFromIFU(io_toBpu_redirctFromIFU),
    .io_toIfu_req_ready(io_toIfu_req_ready),
    .io_toIfu_req_valid(io_toIfu_req_valid),
    .io_toIfu_req_bits_startAddr(io_toIfu_req_bits_startAddr),
    .io_toIfu_req_bits_nextlineStart(io_toIfu_req_bits_nextlineStart),
    .io_toIfu_req_bits_nextStartAddr(io_toIfu_req_bits_nextStartAddr),
    .io_toIfu_req_bits_ftqIdx_flag(io_toIfu_req_bits_ftqIdx_flag),
    .io_toIfu_req_bits_ftqIdx_value(io_toIfu_req_bits_ftqIdx_value),
    .io_toIfu_req_bits_ftqOffset_valid(io_toIfu_req_bits_ftqOffset_valid),
    .io_toIfu_req_bits_ftqOffset_bits(io_toIfu_req_bits_ftqOffset_bits),
    .io_toIfu_redirect_valid(io_toIfu_redirect_valid),
    .io_toIfu_redirect_bits_ftqIdx_flag(io_toIfu_redirect_bits_ftqIdx_flag),
    .io_toIfu_redirect_bits_ftqIdx_value(io_toIfu_redirect_bits_ftqIdx_value),
    .io_toIfu_redirect_bits_ftqOffset(io_toIfu_redirect_bits_ftqOffset),
    .io_toIfu_redirect_bits_level(io_toIfu_redirect_bits_level),
    .io_toIfu_flushFromBpu_s2_valid(io_toIfu_flushFromBpu_s2_valid),
    .io_toIfu_flushFromBpu_s2_bits_flag(io_toIfu_flushFromBpu_s2_bits_flag),
    .io_toIfu_flushFromBpu_s2_bits_value(io_toIfu_flushFromBpu_s2_bits_value),
    .io_toIfu_flushFromBpu_s3_valid(io_toIfu_flushFromBpu_s3_valid),
    .io_toIfu_flushFromBpu_s3_bits_flag(io_toIfu_flushFromBpu_s3_bits_flag),
    .io_toIfu_flushFromBpu_s3_bits_value(io_toIfu_flushFromBpu_s3_bits_value),
    .io_toICache_req_valid(io_toICache_req_valid),
    .io_toICache_req_bits_pcMemRead_0_startAddr(io_toICache_req_bits_pcMemRead_0_startAddr),
    .io_toICache_req_bits_pcMemRead_0_nextlineStart(io_toICache_req_bits_pcMemRead_0_nextlineStart),
    .io_toICache_req_bits_pcMemRead_1_startAddr(io_toICache_req_bits_pcMemRead_1_startAddr),
    .io_toICache_req_bits_pcMemRead_1_nextlineStart(io_toICache_req_bits_pcMemRead_1_nextlineStart),
    .io_toICache_req_bits_pcMemRead_2_startAddr(io_toICache_req_bits_pcMemRead_2_startAddr),
    .io_toICache_req_bits_pcMemRead_2_nextlineStart(io_toICache_req_bits_pcMemRead_2_nextlineStart),
    .io_toICache_req_bits_pcMemRead_3_startAddr(io_toICache_req_bits_pcMemRead_3_startAddr),
    .io_toICache_req_bits_pcMemRead_3_nextlineStart(io_toICache_req_bits_pcMemRead_3_nextlineStart),
    .io_toICache_req_bits_pcMemRead_4_startAddr(io_toICache_req_bits_pcMemRead_4_startAddr),
    .io_toICache_req_bits_pcMemRead_4_nextlineStart(io_toICache_req_bits_pcMemRead_4_nextlineStart),
    .io_toICache_req_bits_readValid_0(io_toICache_req_bits_readValid_0),
    .io_toICache_req_bits_readValid_1(io_toICache_req_bits_readValid_1),
    .io_toICache_req_bits_readValid_2(io_toICache_req_bits_readValid_2),
    .io_toICache_req_bits_readValid_3(io_toICache_req_bits_readValid_3),
    .io_toICache_req_bits_readValid_4(io_toICache_req_bits_readValid_4),
    .io_toICache_req_bits_backendException(io_toICache_req_bits_backendException),
    .io_toBackend_pc_mem_wen(io_toBackend_pc_mem_wen),
    .io_toBackend_pc_mem_waddr(io_toBackend_pc_mem_waddr),
    .io_toBackend_pc_mem_wdata_startAddr(io_toBackend_pc_mem_wdata_startAddr),
    .io_toBackend_newest_entry_en(io_toBackend_newest_entry_en),
    .io_toBackend_newest_entry_target(io_toBackend_newest_entry_target),
    .io_toBackend_newest_entry_ptr_value(io_toBackend_newest_entry_ptr_value),
    .io_toPrefetch_req_ready(io_toPrefetch_req_ready),
    .io_toPrefetch_req_valid(io_toPrefetch_req_valid),
    .io_toPrefetch_req_bits_startAddr(io_toPrefetch_req_bits_startAddr),
    .io_toPrefetch_req_bits_nextlineStart(io_toPrefetch_req_bits_nextlineStart),
    .io_toPrefetch_req_bits_ftqIdx_flag(io_toPrefetch_req_bits_ftqIdx_flag),
    .io_toPrefetch_req_bits_ftqIdx_value(io_toPrefetch_req_bits_ftqIdx_value),
    .io_toPrefetch_flushFromBpu_s2_valid(io_toPrefetch_flushFromBpu_s2_valid),
    .io_toPrefetch_flushFromBpu_s2_bits_flag(io_toPrefetch_flushFromBpu_s2_bits_flag),
    .io_toPrefetch_flushFromBpu_s2_bits_value(io_toPrefetch_flushFromBpu_s2_bits_value),
    .io_toPrefetch_flushFromBpu_s3_valid(io_toPrefetch_flushFromBpu_s3_valid),
    .io_toPrefetch_flushFromBpu_s3_bits_flag(io_toPrefetch_flushFromBpu_s3_bits_flag),
    .io_toPrefetch_flushFromBpu_s3_bits_value(io_toPrefetch_flushFromBpu_s3_bits_value),
    .io_toPrefetch_backendException(io_toPrefetch_backendException),
    .io_icacheFlush(io_icacheFlush),
    .io_mmioCommitRead_mmioFtqPtr_flag(io_mmioCommitRead_mmioFtqPtr_flag),
    .io_mmioCommitRead_mmioFtqPtr_value(io_mmioCommitRead_mmioFtqPtr_value),
    .io_mmioCommitRead_mmioLastCommit(io_mmioCommitRead_mmioLastCommit),
    .io_perf_0_value(io_perf_0_value),
    .io_perf_1_value(io_perf_1_value),
    .io_perf_2_value(io_perf_2_value),
    .io_perf_3_value(io_perf_3_value),
    .io_perf_4_value(io_perf_4_value),
    .io_perf_5_value(io_perf_5_value),
    .io_perf_6_value(io_perf_6_value),
    .io_perf_7_value(io_perf_7_value),
    .io_perf_8_value(io_perf_8_value),
    .io_perf_9_value(io_perf_9_value),
    .io_perf_10_value(io_perf_10_value),
    .io_perf_11_value(io_perf_11_value),
    .io_perf_12_value(io_perf_12_value),
    .io_perf_13_value(io_perf_13_value),
    .io_perf_14_value(io_perf_14_value),
    .io_perf_15_value(io_perf_15_value),
    .io_perf_16_value(io_perf_16_value),
    .io_perf_17_value(io_perf_17_value),
    .io_perf_18_value(io_perf_18_value),
    .io_perf_19_value(io_perf_19_value),
    .io_perf_20_value(io_perf_20_value),
    .io_perf_21_value(io_perf_21_value),
    .io_perf_22_value(io_perf_22_value),
    .io_perf_23_value(io_perf_23_value)
 );


endmodule
