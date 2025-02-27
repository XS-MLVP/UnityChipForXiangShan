module Ftq_top;

  logic  clock;
  logic  reset;
  logic  io_fromBpu_resp_ready;
  logic  io_fromBpu_resp_valid;
  logic [49:0] io_fromBpu_resp_bits_s1_pc_3;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1;
  logic [49:0] io_fromBpu_resp_bits_s1_full_pred_3_targets_0;
  logic [49:0] io_fromBpu_resp_bits_s1_full_pred_3_targets_1;
  logic [3:0] io_fromBpu_resp_bits_s1_full_pred_3_offsets_0;
  logic [3:0] io_fromBpu_resp_bits_s1_full_pred_3_offsets_1;
  logic [49:0] io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddr;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErr;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharing;
  logic  io_fromBpu_resp_bits_s1_full_pred_3_hit;
  logic [49:0] io_fromBpu_resp_bits_s2_pc_3;
  logic  io_fromBpu_resp_bits_s2_valid_3;
  logic  io_fromBpu_resp_bits_s2_hasRedirect_3;
  logic  io_fromBpu_resp_bits_s2_ftq_idx_flag;
  logic [5:0] io_fromBpu_resp_bits_s2_ftq_idx_value;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1;
  logic [49:0] io_fromBpu_resp_bits_s2_full_pred_3_targets_0;
  logic [49:0] io_fromBpu_resp_bits_s2_full_pred_3_targets_1;
  logic [3:0] io_fromBpu_resp_bits_s2_full_pred_3_offsets_0;
  logic [3:0] io_fromBpu_resp_bits_s2_full_pred_3_offsets_1;
  logic [49:0] io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddr;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErr;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharing;
  logic  io_fromBpu_resp_bits_s2_full_pred_3_hit;
  logic [49:0] io_fromBpu_resp_bits_s3_pc_3;
  logic  io_fromBpu_resp_bits_s3_valid_3;
  logic  io_fromBpu_resp_bits_s3_hasRedirect_3;
  logic  io_fromBpu_resp_bits_s3_ftq_idx_flag;
  logic [5:0] io_fromBpu_resp_bits_s3_ftq_idx_value;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1;
  logic [49:0] io_fromBpu_resp_bits_s3_full_pred_3_targets_0;
  logic [49:0] io_fromBpu_resp_bits_s3_full_pred_3_targets_1;
  logic [3:0] io_fromBpu_resp_bits_s3_full_pred_3_offsets_0;
  logic [3:0] io_fromBpu_resp_bits_s3_full_pred_3_offsets_1;
  logic [49:0] io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddr;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErr;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharing;
  logic  io_fromBpu_resp_bits_s3_full_pred_3_hit;
  logic [259:0] io_fromBpu_resp_bits_last_stage_meta;
  logic  io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flag;
  logic [7:0] io_fromBpu_resp_bits_last_stage_spec_info_histPtr_value;
  logic [3:0] io_fromBpu_resp_bits_last_stage_spec_info_ssp;
  logic [2:0] io_fromBpu_resp_bits_last_stage_spec_info_sctr;
  logic  io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flag;
  logic [4:0] io_fromBpu_resp_bits_last_stage_spec_info_TOSW_value;
  logic  io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flag;
  logic [4:0] io_fromBpu_resp_bits_last_stage_spec_info_TOSR_value;
  logic  io_fromBpu_resp_bits_last_stage_spec_info_NOS_flag;
  logic [4:0] io_fromBpu_resp_bits_last_stage_spec_info_NOS_value;
  logic [49:0] io_fromBpu_resp_bits_last_stage_spec_info_topAddr;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_isCall;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_isRet;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_isJalr;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_valid;
  logic [3:0] io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offset;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharing;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_valid;
  logic [11:0] io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lower;
  logic [1:0] io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStat;
  logic [3:0] io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offset;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharing;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_valid;
  logic [19:0] io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lower;
  logic [1:0] io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStat;
  logic [3:0] io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddr;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_carry;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_call;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0;
  logic  io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1;
  logic  io_fromIfu_pdWb_valid;
  logic [49:0] io_fromIfu_pdWb_bits_pc_0;
  logic [49:0] io_fromIfu_pdWb_bits_pc_1;
  logic [49:0] io_fromIfu_pdWb_bits_pc_2;
  logic [49:0] io_fromIfu_pdWb_bits_pc_3;
  logic [49:0] io_fromIfu_pdWb_bits_pc_4;
  logic [49:0] io_fromIfu_pdWb_bits_pc_5;
  logic [49:0] io_fromIfu_pdWb_bits_pc_6;
  logic [49:0] io_fromIfu_pdWb_bits_pc_7;
  logic [49:0] io_fromIfu_pdWb_bits_pc_8;
  logic [49:0] io_fromIfu_pdWb_bits_pc_9;
  logic [49:0] io_fromIfu_pdWb_bits_pc_10;
  logic [49:0] io_fromIfu_pdWb_bits_pc_11;
  logic [49:0] io_fromIfu_pdWb_bits_pc_12;
  logic [49:0] io_fromIfu_pdWb_bits_pc_13;
  logic [49:0] io_fromIfu_pdWb_bits_pc_14;
  logic [49:0] io_fromIfu_pdWb_bits_pc_15;
  logic  io_fromIfu_pdWb_bits_pd_0_valid;
  logic  io_fromIfu_pdWb_bits_pd_0_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_0_brType;
  logic  io_fromIfu_pdWb_bits_pd_0_isCall;
  logic  io_fromIfu_pdWb_bits_pd_0_isRet;
  logic  io_fromIfu_pdWb_bits_pd_1_valid;
  logic  io_fromIfu_pdWb_bits_pd_1_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_1_brType;
  logic  io_fromIfu_pdWb_bits_pd_1_isCall;
  logic  io_fromIfu_pdWb_bits_pd_1_isRet;
  logic  io_fromIfu_pdWb_bits_pd_2_valid;
  logic  io_fromIfu_pdWb_bits_pd_2_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_2_brType;
  logic  io_fromIfu_pdWb_bits_pd_2_isCall;
  logic  io_fromIfu_pdWb_bits_pd_2_isRet;
  logic  io_fromIfu_pdWb_bits_pd_3_valid;
  logic  io_fromIfu_pdWb_bits_pd_3_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_3_brType;
  logic  io_fromIfu_pdWb_bits_pd_3_isCall;
  logic  io_fromIfu_pdWb_bits_pd_3_isRet;
  logic  io_fromIfu_pdWb_bits_pd_4_valid;
  logic  io_fromIfu_pdWb_bits_pd_4_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_4_brType;
  logic  io_fromIfu_pdWb_bits_pd_4_isCall;
  logic  io_fromIfu_pdWb_bits_pd_4_isRet;
  logic  io_fromIfu_pdWb_bits_pd_5_valid;
  logic  io_fromIfu_pdWb_bits_pd_5_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_5_brType;
  logic  io_fromIfu_pdWb_bits_pd_5_isCall;
  logic  io_fromIfu_pdWb_bits_pd_5_isRet;
  logic  io_fromIfu_pdWb_bits_pd_6_valid;
  logic  io_fromIfu_pdWb_bits_pd_6_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_6_brType;
  logic  io_fromIfu_pdWb_bits_pd_6_isCall;
  logic  io_fromIfu_pdWb_bits_pd_6_isRet;
  logic  io_fromIfu_pdWb_bits_pd_7_valid;
  logic  io_fromIfu_pdWb_bits_pd_7_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_7_brType;
  logic  io_fromIfu_pdWb_bits_pd_7_isCall;
  logic  io_fromIfu_pdWb_bits_pd_7_isRet;
  logic  io_fromIfu_pdWb_bits_pd_8_valid;
  logic  io_fromIfu_pdWb_bits_pd_8_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_8_brType;
  logic  io_fromIfu_pdWb_bits_pd_8_isCall;
  logic  io_fromIfu_pdWb_bits_pd_8_isRet;
  logic  io_fromIfu_pdWb_bits_pd_9_valid;
  logic  io_fromIfu_pdWb_bits_pd_9_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_9_brType;
  logic  io_fromIfu_pdWb_bits_pd_9_isCall;
  logic  io_fromIfu_pdWb_bits_pd_9_isRet;
  logic  io_fromIfu_pdWb_bits_pd_10_valid;
  logic  io_fromIfu_pdWb_bits_pd_10_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_10_brType;
  logic  io_fromIfu_pdWb_bits_pd_10_isCall;
  logic  io_fromIfu_pdWb_bits_pd_10_isRet;
  logic  io_fromIfu_pdWb_bits_pd_11_valid;
  logic  io_fromIfu_pdWb_bits_pd_11_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_11_brType;
  logic  io_fromIfu_pdWb_bits_pd_11_isCall;
  logic  io_fromIfu_pdWb_bits_pd_11_isRet;
  logic  io_fromIfu_pdWb_bits_pd_12_valid;
  logic  io_fromIfu_pdWb_bits_pd_12_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_12_brType;
  logic  io_fromIfu_pdWb_bits_pd_12_isCall;
  logic  io_fromIfu_pdWb_bits_pd_12_isRet;
  logic  io_fromIfu_pdWb_bits_pd_13_valid;
  logic  io_fromIfu_pdWb_bits_pd_13_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_13_brType;
  logic  io_fromIfu_pdWb_bits_pd_13_isCall;
  logic  io_fromIfu_pdWb_bits_pd_13_isRet;
  logic  io_fromIfu_pdWb_bits_pd_14_valid;
  logic  io_fromIfu_pdWb_bits_pd_14_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_14_brType;
  logic  io_fromIfu_pdWb_bits_pd_14_isCall;
  logic  io_fromIfu_pdWb_bits_pd_14_isRet;
  logic  io_fromIfu_pdWb_bits_pd_15_valid;
  logic  io_fromIfu_pdWb_bits_pd_15_isRVC;
  logic [1:0] io_fromIfu_pdWb_bits_pd_15_brType;
  logic  io_fromIfu_pdWb_bits_pd_15_isCall;
  logic  io_fromIfu_pdWb_bits_pd_15_isRet;
  logic  io_fromIfu_pdWb_bits_ftqIdx_flag;
  logic [5:0] io_fromIfu_pdWb_bits_ftqIdx_value;
  logic  io_fromIfu_pdWb_bits_misOffset_valid;
  logic [3:0] io_fromIfu_pdWb_bits_misOffset_bits;
  logic  io_fromIfu_pdWb_bits_cfiOffset_valid;
  logic [49:0] io_fromIfu_pdWb_bits_target;
  logic [49:0] io_fromIfu_pdWb_bits_jalTarget;
  logic  io_fromIfu_pdWb_bits_instrRange_0;
  logic  io_fromIfu_pdWb_bits_instrRange_1;
  logic  io_fromIfu_pdWb_bits_instrRange_2;
  logic  io_fromIfu_pdWb_bits_instrRange_3;
  logic  io_fromIfu_pdWb_bits_instrRange_4;
  logic  io_fromIfu_pdWb_bits_instrRange_5;
  logic  io_fromIfu_pdWb_bits_instrRange_6;
  logic  io_fromIfu_pdWb_bits_instrRange_7;
  logic  io_fromIfu_pdWb_bits_instrRange_8;
  logic  io_fromIfu_pdWb_bits_instrRange_9;
  logic  io_fromIfu_pdWb_bits_instrRange_10;
  logic  io_fromIfu_pdWb_bits_instrRange_11;
  logic  io_fromIfu_pdWb_bits_instrRange_12;
  logic  io_fromIfu_pdWb_bits_instrRange_13;
  logic  io_fromIfu_pdWb_bits_instrRange_14;
  logic  io_fromIfu_pdWb_bits_instrRange_15;
  logic  io_fromBackend_rob_commits_0_valid;
  logic [2:0] io_fromBackend_rob_commits_0_bits_commitType;
  logic  io_fromBackend_rob_commits_0_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_0_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_0_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_1_valid;
  logic [2:0] io_fromBackend_rob_commits_1_bits_commitType;
  logic  io_fromBackend_rob_commits_1_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_1_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_1_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_2_valid;
  logic [2:0] io_fromBackend_rob_commits_2_bits_commitType;
  logic  io_fromBackend_rob_commits_2_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_2_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_2_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_3_valid;
  logic [2:0] io_fromBackend_rob_commits_3_bits_commitType;
  logic  io_fromBackend_rob_commits_3_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_3_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_3_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_4_valid;
  logic [2:0] io_fromBackend_rob_commits_4_bits_commitType;
  logic  io_fromBackend_rob_commits_4_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_4_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_4_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_5_valid;
  logic [2:0] io_fromBackend_rob_commits_5_bits_commitType;
  logic  io_fromBackend_rob_commits_5_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_5_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_5_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_6_valid;
  logic [2:0] io_fromBackend_rob_commits_6_bits_commitType;
  logic  io_fromBackend_rob_commits_6_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_6_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_6_bits_ftqOffset;
  logic  io_fromBackend_rob_commits_7_valid;
  logic [2:0] io_fromBackend_rob_commits_7_bits_commitType;
  logic  io_fromBackend_rob_commits_7_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_rob_commits_7_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_rob_commits_7_bits_ftqOffset;
  logic  io_fromBackend_redirect_valid;
  logic  io_fromBackend_redirect_bits_ftqIdx_flag;
  logic [5:0] io_fromBackend_redirect_bits_ftqIdx_value;
  logic [3:0] io_fromBackend_redirect_bits_ftqOffset;
  logic  io_fromBackend_redirect_bits_level;
  logic [49:0] io_fromBackend_redirect_bits_cfiUpdate_pc;
  logic [49:0] io_fromBackend_redirect_bits_cfiUpdate_target;
  logic  io_fromBackend_redirect_bits_cfiUpdate_taken;
  logic  io_fromBackend_redirect_bits_cfiUpdate_isMisPred;
  logic  io_fromBackend_redirect_bits_cfiUpdate_backendIGPF;
  logic  io_fromBackend_redirect_bits_cfiUpdate_backendIPF;
  logic  io_fromBackend_redirect_bits_cfiUpdate_backendIAF;
  logic  io_fromBackend_ftqIdxAhead_0_valid;
  logic [5:0] io_fromBackend_ftqIdxAhead_0_bits_value;
  logic [2:0] io_fromBackend_ftqIdxSelOH_bits;
  logic  io_toBpu_redirect_valid;
  logic  io_toBpu_redirect_bits_level;
  logic [49:0] io_toBpu_redirect_bits_cfiUpdate_pc;
  logic  io_toBpu_redirect_bits_cfiUpdate_pd_isRVC;
  logic  io_toBpu_redirect_bits_cfiUpdate_pd_isCall;
  logic  io_toBpu_redirect_bits_cfiUpdate_pd_isRet;
  logic [3:0] io_toBpu_redirect_bits_cfiUpdate_ssp;
  logic [2:0] io_toBpu_redirect_bits_cfiUpdate_sctr;
  logic  io_toBpu_redirect_bits_cfiUpdate_TOSW_flag;
  logic [4:0] io_toBpu_redirect_bits_cfiUpdate_TOSW_value;
  logic  io_toBpu_redirect_bits_cfiUpdate_TOSR_flag;
  logic [4:0] io_toBpu_redirect_bits_cfiUpdate_TOSR_value;
  logic  io_toBpu_redirect_bits_cfiUpdate_NOS_flag;
  logic [4:0] io_toBpu_redirect_bits_cfiUpdate_NOS_value;
  logic  io_toBpu_redirect_bits_cfiUpdate_histPtr_flag;
  logic [7:0] io_toBpu_redirect_bits_cfiUpdate_histPtr_value;
  logic [49:0] io_toBpu_redirect_bits_cfiUpdate_target;
  logic  io_toBpu_redirect_bits_cfiUpdate_taken;
  logic [1:0] io_toBpu_redirect_bits_cfiUpdate_shift;
  logic  io_toBpu_redirect_bits_cfiUpdate_addIntoHist;
  logic  io_toBpu_update_valid;
  logic [49:0] io_toBpu_update_bits_pc;
  logic [7:0] io_toBpu_update_bits_spec_info_histPtr_value;
  logic  io_toBpu_update_bits_ftb_entry_isCall;
  logic  io_toBpu_update_bits_ftb_entry_isRet;
  logic  io_toBpu_update_bits_ftb_entry_isJalr;
  logic  io_toBpu_update_bits_ftb_entry_valid;
  logic [3:0] io_toBpu_update_bits_ftb_entry_brSlots_0_offset;
  logic  io_toBpu_update_bits_ftb_entry_brSlots_0_sharing;
  logic  io_toBpu_update_bits_ftb_entry_brSlots_0_valid;
  logic [11:0] io_toBpu_update_bits_ftb_entry_brSlots_0_lower;
  logic [1:0] io_toBpu_update_bits_ftb_entry_brSlots_0_tarStat;
  logic [3:0] io_toBpu_update_bits_ftb_entry_tailSlot_offset;
  logic  io_toBpu_update_bits_ftb_entry_tailSlot_sharing;
  logic  io_toBpu_update_bits_ftb_entry_tailSlot_valid;
  logic [19:0] io_toBpu_update_bits_ftb_entry_tailSlot_lower;
  logic [1:0] io_toBpu_update_bits_ftb_entry_tailSlot_tarStat;
  logic [3:0] io_toBpu_update_bits_ftb_entry_pftAddr;
  logic  io_toBpu_update_bits_ftb_entry_carry;
  logic  io_toBpu_update_bits_ftb_entry_last_may_be_rvi_call;
  logic  io_toBpu_update_bits_ftb_entry_strong_bias_0;
  logic  io_toBpu_update_bits_ftb_entry_strong_bias_1;
  logic  io_toBpu_update_bits_cfi_idx_valid;
  logic [3:0] io_toBpu_update_bits_cfi_idx_bits;
  logic  io_toBpu_update_bits_br_taken_mask_0;
  logic  io_toBpu_update_bits_br_taken_mask_1;
  logic  io_toBpu_update_bits_jmp_taken;
  logic  io_toBpu_update_bits_mispred_mask_0;
  logic  io_toBpu_update_bits_mispred_mask_1;
  logic  io_toBpu_update_bits_mispred_mask_2;
  logic  io_toBpu_update_bits_false_hit;
  logic  io_toBpu_update_bits_old_entry;
  logic [259:0] io_toBpu_update_bits_meta;
  logic [49:0] io_toBpu_update_bits_full_target;
  logic  io_toBpu_enq_ptr_flag;
  logic [5:0] io_toBpu_enq_ptr_value;
  logic  io_toBpu_redirctFromIFU;
  logic  io_toIfu_req_ready;
  logic  io_toIfu_req_valid;
  logic [49:0] io_toIfu_req_bits_startAddr;
  logic [49:0] io_toIfu_req_bits_nextlineStart;
  logic [49:0] io_toIfu_req_bits_nextStartAddr;
  logic  io_toIfu_req_bits_ftqIdx_flag;
  logic [5:0] io_toIfu_req_bits_ftqIdx_value;
  logic  io_toIfu_req_bits_ftqOffset_valid;
  logic [3:0] io_toIfu_req_bits_ftqOffset_bits;
  logic  io_toIfu_redirect_valid;
  logic  io_toIfu_redirect_bits_ftqIdx_flag;
  logic [5:0] io_toIfu_redirect_bits_ftqIdx_value;
  logic [3:0] io_toIfu_redirect_bits_ftqOffset;
  logic  io_toIfu_redirect_bits_level;
  logic  io_toIfu_flushFromBpu_s2_valid;
  logic  io_toIfu_flushFromBpu_s2_bits_flag;
  logic [5:0] io_toIfu_flushFromBpu_s2_bits_value;
  logic  io_toIfu_flushFromBpu_s3_valid;
  logic  io_toIfu_flushFromBpu_s3_bits_flag;
  logic [5:0] io_toIfu_flushFromBpu_s3_bits_value;
  logic  io_toICache_req_valid;
  logic [49:0] io_toICache_req_bits_pcMemRead_0_startAddr;
  logic [49:0] io_toICache_req_bits_pcMemRead_0_nextlineStart;
  logic [49:0] io_toICache_req_bits_pcMemRead_1_startAddr;
  logic [49:0] io_toICache_req_bits_pcMemRead_1_nextlineStart;
  logic [49:0] io_toICache_req_bits_pcMemRead_2_startAddr;
  logic [49:0] io_toICache_req_bits_pcMemRead_2_nextlineStart;
  logic [49:0] io_toICache_req_bits_pcMemRead_3_startAddr;
  logic [49:0] io_toICache_req_bits_pcMemRead_3_nextlineStart;
  logic [49:0] io_toICache_req_bits_pcMemRead_4_startAddr;
  logic [49:0] io_toICache_req_bits_pcMemRead_4_nextlineStart;
  logic  io_toICache_req_bits_readValid_0;
  logic  io_toICache_req_bits_readValid_1;
  logic  io_toICache_req_bits_readValid_2;
  logic  io_toICache_req_bits_readValid_3;
  logic  io_toICache_req_bits_readValid_4;
  logic  io_toICache_req_bits_backendException;
  logic  io_toBackend_pc_mem_wen;
  logic [5:0] io_toBackend_pc_mem_waddr;
  logic [49:0] io_toBackend_pc_mem_wdata_startAddr;
  logic  io_toBackend_newest_entry_en;
  logic [49:0] io_toBackend_newest_entry_target;
  logic [5:0] io_toBackend_newest_entry_ptr_value;
  logic  io_toPrefetch_req_ready;
  logic  io_toPrefetch_req_valid;
  logic [49:0] io_toPrefetch_req_bits_startAddr;
  logic [49:0] io_toPrefetch_req_bits_nextlineStart;
  logic  io_toPrefetch_req_bits_ftqIdx_flag;
  logic [5:0] io_toPrefetch_req_bits_ftqIdx_value;
  logic  io_toPrefetch_flushFromBpu_s2_valid;
  logic  io_toPrefetch_flushFromBpu_s2_bits_flag;
  logic [5:0] io_toPrefetch_flushFromBpu_s2_bits_value;
  logic  io_toPrefetch_flushFromBpu_s3_valid;
  logic  io_toPrefetch_flushFromBpu_s3_bits_flag;
  logic [5:0] io_toPrefetch_flushFromBpu_s3_bits_value;
  logic [1:0] io_toPrefetch_backendException;
  logic  io_icacheFlush;
  logic  io_mmioCommitRead_mmioFtqPtr_flag;
  logic [5:0] io_mmioCommitRead_mmioFtqPtr_value;
  logic  io_mmioCommitRead_mmioLastCommit;
  logic [5:0] io_perf_0_value;
  logic [5:0] io_perf_1_value;
  logic [5:0] io_perf_2_value;
  logic [5:0] io_perf_3_value;
  logic [5:0] io_perf_4_value;
  logic [5:0] io_perf_5_value;
  logic [5:0] io_perf_6_value;
  logic [5:0] io_perf_7_value;
  logic [5:0] io_perf_8_value;
  logic [5:0] io_perf_9_value;
  logic [5:0] io_perf_10_value;
  logic [5:0] io_perf_11_value;
  logic [5:0] io_perf_12_value;
  logic [5:0] io_perf_13_value;
  logic [5:0] io_perf_14_value;
  logic [5:0] io_perf_15_value;
  logic [5:0] io_perf_16_value;
  logic [5:0] io_perf_17_value;
  logic [5:0] io_perf_18_value;
  logic [5:0] io_perf_19_value;
  logic [5:0] io_perf_20_value;
  logic [5:0] io_perf_21_value;
  logic [5:0] io_perf_22_value;
  logic [5:0] io_perf_23_value;


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


  export "DPI-C" function get_clockxxcxrJQKToTQ;
  export "DPI-C" function set_clockxxcxrJQKToTQ;
  export "DPI-C" function get_resetxxcxrJQKToTQ;
  export "DPI-C" function set_resetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_readyxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_pc_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_pc_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_targets_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_targets_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_targets_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_targets_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_offsets_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_offsets_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_offsets_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_offsets_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharingxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s1_full_pred_3_hitxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s1_full_pred_3_hitxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_pc_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_pc_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_valid_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_valid_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_hasRedirect_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_hasRedirect_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_ftq_idx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_ftq_idx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_ftq_idx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_ftq_idx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_targets_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_targets_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_targets_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_targets_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_offsets_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_offsets_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_offsets_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_offsets_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharingxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s2_full_pred_3_hitxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s2_full_pred_3_hitxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_pc_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_pc_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_valid_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_valid_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_hasRedirect_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_hasRedirect_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_ftq_idx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_ftq_idx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_ftq_idx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_ftq_idx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_targets_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_targets_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_targets_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_targets_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_offsets_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_offsets_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_offsets_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_offsets_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharingxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_s3_full_pred_3_hitxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_s3_full_pred_3_hitxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_metaxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_metaxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_sspxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_sspxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_sctrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_sctrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_NOS_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_NOS_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_NOS_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_NOS_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_spec_info_topAddrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_spec_info_topAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_isJalrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_isJalrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharingxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lowerxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lowerxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStatxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStatxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharingxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lowerxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lowerxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStatxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStatxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddrxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_carryxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_carryxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_callxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_callxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_2xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_2xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_4xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_4xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_5xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_5xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_6xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_6xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_7xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_7xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_8xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_8xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_9xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_9xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_10xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_10xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_11xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_11xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_12xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_12xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_13xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_13xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_14xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_14xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pc_15xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pc_15xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_0_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_0_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_0_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_0_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_0_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_0_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_0_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_0_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_0_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_0_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_1_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_1_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_1_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_1_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_1_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_1_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_1_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_1_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_1_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_1_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_2_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_2_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_2_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_2_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_2_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_2_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_2_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_2_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_2_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_2_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_3_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_3_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_3_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_3_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_3_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_3_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_3_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_3_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_3_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_3_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_4_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_4_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_4_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_4_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_4_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_4_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_4_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_4_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_4_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_4_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_5_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_5_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_5_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_5_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_5_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_5_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_5_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_5_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_5_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_5_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_6_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_6_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_6_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_6_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_6_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_6_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_6_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_6_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_6_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_6_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_7_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_7_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_7_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_7_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_7_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_7_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_7_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_7_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_7_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_7_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_8_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_8_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_8_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_8_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_8_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_8_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_8_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_8_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_8_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_8_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_9_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_9_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_9_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_9_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_9_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_9_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_9_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_9_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_9_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_9_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_10_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_10_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_10_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_10_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_10_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_10_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_10_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_10_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_10_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_10_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_11_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_11_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_11_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_11_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_11_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_11_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_11_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_11_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_11_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_11_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_12_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_12_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_12_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_12_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_12_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_12_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_12_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_12_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_12_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_12_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_13_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_13_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_13_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_13_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_13_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_13_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_13_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_13_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_13_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_13_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_14_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_14_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_14_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_14_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_14_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_14_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_14_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_14_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_14_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_14_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_15_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_15_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_15_isRVCxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_15_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_15_brTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_15_brTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_15_isCallxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_15_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_pd_15_isRetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_pd_15_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_misOffset_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_misOffset_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_misOffset_bitsxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_misOffset_bitsxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_cfiOffset_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_cfiOffset_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_targetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_targetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_jalTargetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_jalTargetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_0xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_1xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_2xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_2xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_3xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_4xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_4xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_5xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_5xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_6xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_6xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_7xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_7xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_8xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_8xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_9xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_9xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_10xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_10xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_11xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_11xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_12xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_12xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_13xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_13xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_14xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_14xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromIfu_pdWb_bits_instrRange_15xxcxrJQKToTQ;
  export "DPI-C" function set_io_fromIfu_pdWb_bits_instrRange_15xxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_0_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_0_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_0_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_0_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_0_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_0_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_0_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_0_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_0_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_0_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_1_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_1_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_1_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_1_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_1_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_1_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_1_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_1_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_1_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_1_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_2_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_2_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_2_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_2_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_2_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_2_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_2_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_2_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_2_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_2_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_3_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_3_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_3_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_3_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_3_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_3_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_3_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_3_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_3_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_3_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_4_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_4_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_4_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_4_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_4_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_4_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_4_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_4_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_4_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_4_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_5_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_5_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_5_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_5_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_5_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_5_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_5_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_5_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_5_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_5_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_6_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_6_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_6_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_6_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_6_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_6_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_6_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_6_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_6_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_6_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_7_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_7_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_7_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_7_bits_commitTypexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_7_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_7_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_7_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_7_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_rob_commits_7_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_rob_commits_7_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_levelxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_levelxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_pcxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_pcxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_targetxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_targetxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_takenxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_takenxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_isMisPredxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_isMisPredxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_backendIGPFxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_backendIGPFxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_backendIPFxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_backendIPFxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_redirect_bits_cfiUpdate_backendIAFxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_redirect_bits_cfiUpdate_backendIAFxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_ftqIdxAhead_0_validxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_ftqIdxAhead_0_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_ftqIdxAhead_0_bits_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_ftqIdxAhead_0_bits_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_fromBackend_ftqIdxSelOH_bitsxxcxrJQKToTQ;
  export "DPI-C" function set_io_fromBackend_ftqIdxSelOH_bitsxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_levelxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_pcxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_pd_isRVCxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_pd_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_pd_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_sspxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_sctrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_TOSW_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_TOSW_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_TOSR_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_TOSR_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_NOS_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_NOS_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_histPtr_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_histPtr_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_targetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_takenxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_shiftxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirect_bits_cfiUpdate_addIntoHistxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_pcxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_spec_info_histPtr_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_isCallxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_isRetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_isJalrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_brSlots_0_offsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_brSlots_0_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_brSlots_0_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_brSlots_0_lowerxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_brSlots_0_tarStatxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_tailSlot_offsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_tailSlot_sharingxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_tailSlot_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_tailSlot_lowerxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_tailSlot_tarStatxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_pftAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_carryxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_last_may_be_rvi_callxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_strong_bias_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_ftb_entry_strong_bias_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_cfi_idx_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_cfi_idx_bitsxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_br_taken_mask_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_br_taken_mask_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_jmp_takenxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_mispred_mask_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_mispred_mask_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_mispred_mask_2xxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_false_hitxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_old_entryxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_metaxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_update_bits_full_targetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_enq_ptr_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_enq_ptr_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toBpu_redirctFromIFUxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_readyxxcxrJQKToTQ;
  export "DPI-C" function set_io_toIfu_req_readyxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_nextStartAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_ftqOffset_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_req_bits_ftqOffset_bitsxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_redirect_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_redirect_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_redirect_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_redirect_bits_ftqOffsetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_redirect_bits_levelxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_flushFromBpu_s2_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_flushFromBpu_s2_bits_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_flushFromBpu_s2_bits_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_flushFromBpu_s3_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_flushFromBpu_s3_bits_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toIfu_flushFromBpu_s3_bits_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_0_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_0_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_1_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_1_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_2_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_2_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_3_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_3_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_4_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_pcMemRead_4_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_readValid_0xxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_readValid_1xxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_readValid_2xxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_readValid_3xxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_readValid_4xxcxrJQKToTQ;
  export "DPI-C" function get_io_toICache_req_bits_backendExceptionxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBackend_pc_mem_wenxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBackend_pc_mem_waddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBackend_pc_mem_wdata_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBackend_newest_entry_enxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBackend_newest_entry_targetxxcxrJQKToTQ;
  export "DPI-C" function get_io_toBackend_newest_entry_ptr_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_req_readyxxcxrJQKToTQ;
  export "DPI-C" function set_io_toPrefetch_req_readyxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_req_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_req_bits_startAddrxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_req_bits_nextlineStartxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_req_bits_ftqIdx_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_req_bits_ftqIdx_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_flushFromBpu_s2_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_flushFromBpu_s2_bits_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_flushFromBpu_s2_bits_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_flushFromBpu_s3_validxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_flushFromBpu_s3_bits_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_flushFromBpu_s3_bits_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_toPrefetch_backendExceptionxxcxrJQKToTQ;
  export "DPI-C" function get_io_icacheFlushxxcxrJQKToTQ;
  export "DPI-C" function get_io_mmioCommitRead_mmioFtqPtr_flagxxcxrJQKToTQ;
  export "DPI-C" function set_io_mmioCommitRead_mmioFtqPtr_flagxxcxrJQKToTQ;
  export "DPI-C" function get_io_mmioCommitRead_mmioFtqPtr_valuexxcxrJQKToTQ;
  export "DPI-C" function set_io_mmioCommitRead_mmioFtqPtr_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_mmioCommitRead_mmioLastCommitxxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_0_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_1_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_2_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_3_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_4_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_5_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_6_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_7_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_8_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_9_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_10_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_11_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_12_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_13_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_14_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_15_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_16_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_17_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_18_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_19_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_20_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_21_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_22_valuexxcxrJQKToTQ;
  export "DPI-C" function get_io_perf_23_valuexxcxrJQKToTQ;


  function void get_clockxxcxrJQKToTQ;
    output logic  value;
    value=clock;
  endfunction

  function void set_clockxxcxrJQKToTQ;
    input logic  value;
    clock=value;
  endfunction

  function void get_resetxxcxrJQKToTQ;
    output logic  value;
    value=reset;
  endfunction

  function void set_resetxxcxrJQKToTQ;
    input logic  value;
    reset=value;
  endfunction

  function void get_io_fromBpu_resp_readyxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_ready;
  endfunction

  function void get_io_fromBpu_resp_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_valid;
  endfunction

  function void set_io_fromBpu_resp_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_valid=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_pc_3xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s1_pc_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_pc_3xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s1_pc_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_br_taken_mask_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_slot_valids_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_targets_0xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_targets_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_targets_0xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s1_full_pred_3_targets_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_targets_1xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_targets_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_targets_1xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s1_full_pred_3_targets_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_offsets_0xxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_offsets_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_offsets_0xxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_s1_full_pred_3_offsets_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_offsets_1xxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_offsets_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_offsets_1xxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_s1_full_pred_3_offsets_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddr;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s1_full_pred_3_fallThroughAddr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErrxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErr;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErrxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_fallThroughErr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharing;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharingxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_is_br_sharing=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s1_full_pred_3_hitxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s1_full_pred_3_hit;
  endfunction

  function void set_io_fromBpu_resp_bits_s1_full_pred_3_hitxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s1_full_pred_3_hit=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_pc_3xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s2_pc_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_pc_3xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s2_pc_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_valid_3xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_valid_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_valid_3xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_valid_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_hasRedirect_3xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_hasRedirect_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_hasRedirect_3xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_hasRedirect_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_ftq_idx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_ftq_idx_flag;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_ftq_idx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_ftq_idx_flag=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_ftq_idx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBpu_resp_bits_s2_ftq_idx_value;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_ftq_idx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBpu_resp_bits_s2_ftq_idx_value=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_br_taken_mask_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_slot_valids_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_targets_0xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_targets_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_targets_0xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s2_full_pred_3_targets_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_targets_1xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_targets_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_targets_1xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s2_full_pred_3_targets_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_offsets_0xxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_offsets_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_offsets_0xxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_s2_full_pred_3_offsets_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_offsets_1xxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_offsets_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_offsets_1xxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_s2_full_pred_3_offsets_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddr;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s2_full_pred_3_fallThroughAddr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErrxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErr;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErrxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_fallThroughErr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharing;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharingxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_is_br_sharing=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s2_full_pred_3_hitxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s2_full_pred_3_hit;
  endfunction

  function void set_io_fromBpu_resp_bits_s2_full_pred_3_hitxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s2_full_pred_3_hit=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_pc_3xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s3_pc_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_pc_3xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s3_pc_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_valid_3xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_valid_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_valid_3xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_valid_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_hasRedirect_3xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_hasRedirect_3;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_hasRedirect_3xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_hasRedirect_3=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_ftq_idx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_ftq_idx_flag;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_ftq_idx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_ftq_idx_flag=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_ftq_idx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBpu_resp_bits_s3_ftq_idx_value;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_ftq_idx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBpu_resp_bits_s3_ftq_idx_value=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_br_taken_mask_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_slot_valids_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_targets_0xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_targets_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_targets_0xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s3_full_pred_3_targets_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_targets_1xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_targets_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_targets_1xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s3_full_pred_3_targets_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_offsets_0xxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_offsets_0;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_offsets_0xxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_s3_full_pred_3_offsets_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_offsets_1xxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_offsets_1;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_offsets_1xxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_s3_full_pred_3_offsets_1=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddr;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddrxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_s3_full_pred_3_fallThroughAddr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErrxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErr;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErrxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_fallThroughErr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharing;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharingxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_is_br_sharing=value;
  endfunction

  function void get_io_fromBpu_resp_bits_s3_full_pred_3_hitxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_s3_full_pred_3_hit;
  endfunction

  function void set_io_fromBpu_resp_bits_s3_full_pred_3_hitxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_s3_full_pred_3_hit=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_metaxxcxrJQKToTQ;
    output logic [259:0] value;
    value=io_fromBpu_resp_bits_last_stage_meta;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_metaxxcxrJQKToTQ;
    input logic [259:0] value;
    io_fromBpu_resp_bits_last_stage_meta=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flag;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_spec_info_histPtr_flag=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_valuexxcxrJQKToTQ;
    output logic [7:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_histPtr_value;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_histPtr_valuexxcxrJQKToTQ;
    input logic [7:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_histPtr_value=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_sspxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_ssp;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_sspxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_ssp=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_sctrxxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_sctr;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_sctrxxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_sctr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flag;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_spec_info_TOSW_flag=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_valuexxcxrJQKToTQ;
    output logic [4:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_TOSW_value;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_TOSW_valuexxcxrJQKToTQ;
    input logic [4:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_TOSW_value=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flag;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_spec_info_TOSR_flag=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_valuexxcxrJQKToTQ;
    output logic [4:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_TOSR_value;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_TOSR_valuexxcxrJQKToTQ;
    input logic [4:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_TOSR_value=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_NOS_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_NOS_flag;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_NOS_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_spec_info_NOS_flag=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_NOS_valuexxcxrJQKToTQ;
    output logic [4:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_NOS_value;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_NOS_valuexxcxrJQKToTQ;
    input logic [4:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_NOS_value=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_spec_info_topAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBpu_resp_bits_last_stage_spec_info_topAddr;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_spec_info_topAddrxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBpu_resp_bits_last_stage_spec_info_topAddr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_isCall;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_isCall=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_isRet;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_isRet=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_isJalrxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_isJalr;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_isJalrxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_isJalr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_valid;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_valid=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offset;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_offset=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharing;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharingxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_sharing=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_valid;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_valid=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lowerxxcxrJQKToTQ;
    output logic [11:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lower;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lowerxxcxrJQKToTQ;
    input logic [11:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_lower=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStatxxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStat;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStatxxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_brSlots_0_tarStat=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offset;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_offset=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharing;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharingxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_sharing=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_valid;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_valid=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lowerxxcxrJQKToTQ;
    output logic [19:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lower;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lowerxxcxrJQKToTQ;
    input logic [19:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_lower=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStatxxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStat;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStatxxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_tailSlot_tarStat=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddrxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddr;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddrxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_pftAddr=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_carryxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_carry;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_carryxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_carry=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_callxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_call;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_callxxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_last_may_be_rvi_call=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_0=value;
  endfunction

  function void get_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1;
  endfunction

  function void set_io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1xxcxrJQKToTQ;
    input logic  value;
    io_fromBpu_resp_bits_last_stage_ftb_entry_strong_bias_1=value;
  endfunction

  function void get_io_fromIfu_pdWb_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_valid;
  endfunction

  function void set_io_fromIfu_pdWb_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_0xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_0;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_0xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_0=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_1xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_1;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_1xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_1=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_2xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_2;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_2xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_2=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_3xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_3;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_3xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_3=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_4xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_4;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_4xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_4=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_5xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_5;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_5xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_5=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_6xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_6;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_6xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_6=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_7xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_7;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_7xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_7=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_8xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_8;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_8xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_8=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_9xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_9;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_9xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_9=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_10xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_10;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_10xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_10=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_11xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_11;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_11xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_11=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_12xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_12;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_12xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_12=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_13xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_13;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_13xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_13=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_14xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_14;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_14xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_14=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pc_15xxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_pc_15;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pc_15xxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_pc_15=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_0_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_0_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_0_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_0_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_0_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_0_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_0_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_0_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_0_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_0_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_0_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_0_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_0_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_0_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_0_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_0_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_0_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_0_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_0_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_0_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_1_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_1_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_1_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_1_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_1_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_1_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_1_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_1_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_1_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_1_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_1_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_1_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_1_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_1_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_1_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_1_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_1_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_1_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_1_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_1_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_2_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_2_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_2_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_2_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_2_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_2_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_2_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_2_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_2_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_2_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_2_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_2_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_2_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_2_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_2_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_2_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_2_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_2_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_2_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_2_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_3_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_3_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_3_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_3_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_3_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_3_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_3_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_3_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_3_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_3_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_3_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_3_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_3_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_3_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_3_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_3_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_3_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_3_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_3_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_3_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_4_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_4_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_4_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_4_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_4_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_4_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_4_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_4_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_4_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_4_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_4_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_4_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_4_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_4_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_4_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_4_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_4_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_4_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_4_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_4_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_5_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_5_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_5_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_5_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_5_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_5_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_5_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_5_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_5_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_5_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_5_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_5_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_5_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_5_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_5_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_5_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_5_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_5_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_5_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_5_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_6_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_6_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_6_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_6_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_6_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_6_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_6_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_6_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_6_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_6_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_6_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_6_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_6_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_6_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_6_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_6_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_6_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_6_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_6_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_6_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_7_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_7_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_7_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_7_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_7_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_7_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_7_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_7_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_7_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_7_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_7_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_7_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_7_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_7_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_7_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_7_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_7_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_7_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_7_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_7_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_8_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_8_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_8_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_8_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_8_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_8_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_8_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_8_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_8_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_8_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_8_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_8_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_8_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_8_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_8_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_8_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_8_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_8_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_8_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_8_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_9_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_9_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_9_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_9_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_9_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_9_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_9_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_9_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_9_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_9_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_9_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_9_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_9_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_9_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_9_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_9_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_9_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_9_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_9_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_9_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_10_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_10_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_10_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_10_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_10_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_10_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_10_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_10_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_10_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_10_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_10_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_10_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_10_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_10_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_10_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_10_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_10_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_10_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_10_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_10_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_11_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_11_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_11_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_11_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_11_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_11_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_11_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_11_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_11_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_11_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_11_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_11_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_11_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_11_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_11_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_11_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_11_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_11_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_11_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_11_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_12_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_12_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_12_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_12_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_12_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_12_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_12_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_12_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_12_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_12_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_12_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_12_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_12_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_12_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_12_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_12_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_12_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_12_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_12_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_12_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_13_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_13_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_13_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_13_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_13_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_13_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_13_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_13_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_13_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_13_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_13_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_13_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_13_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_13_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_13_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_13_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_13_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_13_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_13_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_13_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_14_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_14_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_14_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_14_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_14_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_14_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_14_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_14_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_14_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_14_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_14_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_14_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_14_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_14_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_14_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_14_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_14_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_14_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_14_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_14_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_15_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_15_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_15_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_15_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_15_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_15_isRVC;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_15_isRVCxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_15_isRVC=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_15_brTypexxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_fromIfu_pdWb_bits_pd_15_brType;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_15_brTypexxcxrJQKToTQ;
    input logic [1:0] value;
    io_fromIfu_pdWb_bits_pd_15_brType=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_15_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_15_isCall;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_15_isCallxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_15_isCall=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_pd_15_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_pd_15_isRet;
  endfunction

  function void set_io_fromIfu_pdWb_bits_pd_15_isRetxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_pd_15_isRet=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromIfu_pdWb_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromIfu_pdWb_bits_ftqIdx_value;
  endfunction

  function void set_io_fromIfu_pdWb_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromIfu_pdWb_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_misOffset_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_misOffset_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_misOffset_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_misOffset_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_misOffset_bitsxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromIfu_pdWb_bits_misOffset_bits;
  endfunction

  function void set_io_fromIfu_pdWb_bits_misOffset_bitsxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromIfu_pdWb_bits_misOffset_bits=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_cfiOffset_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_cfiOffset_valid;
  endfunction

  function void set_io_fromIfu_pdWb_bits_cfiOffset_validxxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_cfiOffset_valid=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_targetxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_target;
  endfunction

  function void set_io_fromIfu_pdWb_bits_targetxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_target=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_jalTargetxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromIfu_pdWb_bits_jalTarget;
  endfunction

  function void set_io_fromIfu_pdWb_bits_jalTargetxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromIfu_pdWb_bits_jalTarget=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_0xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_0;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_0xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_0=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_1xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_1;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_1xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_1=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_2xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_2;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_2xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_2=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_3xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_3;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_3xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_3=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_4xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_4;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_4xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_4=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_5xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_5;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_5xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_5=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_6xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_6;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_6xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_6=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_7xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_7;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_7xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_7=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_8xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_8;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_8xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_8=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_9xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_9;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_9xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_9=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_10xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_10;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_10xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_10=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_11xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_11;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_11xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_11=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_12xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_12;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_12xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_12=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_13xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_13;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_13xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_13=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_14xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_14;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_14xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_14=value;
  endfunction

  function void get_io_fromIfu_pdWb_bits_instrRange_15xxcxrJQKToTQ;
    output logic  value;
    value=io_fromIfu_pdWb_bits_instrRange_15;
  endfunction

  function void set_io_fromIfu_pdWb_bits_instrRange_15xxcxrJQKToTQ;
    input logic  value;
    io_fromIfu_pdWb_bits_instrRange_15=value;
  endfunction

  function void get_io_fromBackend_rob_commits_0_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_0_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_0_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_0_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_0_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_0_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_0_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_0_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_0_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_0_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_0_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_0_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_0_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_0_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_0_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_0_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_0_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_0_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_0_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_0_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_1_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_1_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_1_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_1_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_1_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_1_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_1_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_1_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_1_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_1_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_1_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_1_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_1_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_1_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_1_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_1_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_1_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_1_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_1_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_1_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_2_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_2_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_2_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_2_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_2_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_2_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_2_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_2_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_2_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_2_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_2_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_2_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_2_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_2_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_2_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_2_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_2_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_2_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_2_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_2_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_3_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_3_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_3_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_3_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_3_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_3_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_3_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_3_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_3_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_3_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_3_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_3_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_3_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_3_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_3_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_3_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_3_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_3_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_3_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_3_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_4_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_4_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_4_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_4_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_4_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_4_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_4_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_4_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_4_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_4_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_4_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_4_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_4_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_4_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_4_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_4_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_4_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_4_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_4_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_4_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_5_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_5_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_5_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_5_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_5_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_5_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_5_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_5_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_5_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_5_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_5_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_5_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_5_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_5_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_5_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_5_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_5_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_5_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_5_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_5_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_6_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_6_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_6_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_6_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_6_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_6_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_6_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_6_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_6_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_6_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_6_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_6_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_6_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_6_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_6_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_6_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_6_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_6_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_6_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_6_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_rob_commits_7_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_7_valid;
  endfunction

  function void set_io_fromBackend_rob_commits_7_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_7_valid=value;
  endfunction

  function void get_io_fromBackend_rob_commits_7_bits_commitTypexxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_rob_commits_7_bits_commitType;
  endfunction

  function void set_io_fromBackend_rob_commits_7_bits_commitTypexxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_rob_commits_7_bits_commitType=value;
  endfunction

  function void get_io_fromBackend_rob_commits_7_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_rob_commits_7_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_rob_commits_7_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_rob_commits_7_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_rob_commits_7_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_rob_commits_7_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_rob_commits_7_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_rob_commits_7_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_rob_commits_7_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_rob_commits_7_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_rob_commits_7_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_rob_commits_7_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_redirect_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_valid;
  endfunction

  function void set_io_fromBackend_redirect_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_valid=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_ftqIdx_flag;
  endfunction

  function void set_io_fromBackend_redirect_bits_ftqIdx_flagxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_ftqIdx_flag=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_redirect_bits_ftqIdx_value;
  endfunction

  function void set_io_fromBackend_redirect_bits_ftqIdx_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_redirect_bits_ftqIdx_value=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_fromBackend_redirect_bits_ftqOffset;
  endfunction

  function void set_io_fromBackend_redirect_bits_ftqOffsetxxcxrJQKToTQ;
    input logic [3:0] value;
    io_fromBackend_redirect_bits_ftqOffset=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_levelxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_level;
  endfunction

  function void set_io_fromBackend_redirect_bits_levelxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_level=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_pcxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBackend_redirect_bits_cfiUpdate_pc;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_pcxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBackend_redirect_bits_cfiUpdate_pc=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_targetxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_fromBackend_redirect_bits_cfiUpdate_target;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_targetxxcxrJQKToTQ;
    input logic [49:0] value;
    io_fromBackend_redirect_bits_cfiUpdate_target=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_takenxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_cfiUpdate_taken;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_takenxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_cfiUpdate_taken=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_isMisPredxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_cfiUpdate_isMisPred;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_isMisPredxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_cfiUpdate_isMisPred=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_backendIGPFxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_cfiUpdate_backendIGPF;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_backendIGPFxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_cfiUpdate_backendIGPF=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_backendIPFxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_cfiUpdate_backendIPF;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_backendIPFxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_cfiUpdate_backendIPF=value;
  endfunction

  function void get_io_fromBackend_redirect_bits_cfiUpdate_backendIAFxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_redirect_bits_cfiUpdate_backendIAF;
  endfunction

  function void set_io_fromBackend_redirect_bits_cfiUpdate_backendIAFxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_redirect_bits_cfiUpdate_backendIAF=value;
  endfunction

  function void get_io_fromBackend_ftqIdxAhead_0_validxxcxrJQKToTQ;
    output logic  value;
    value=io_fromBackend_ftqIdxAhead_0_valid;
  endfunction

  function void set_io_fromBackend_ftqIdxAhead_0_validxxcxrJQKToTQ;
    input logic  value;
    io_fromBackend_ftqIdxAhead_0_valid=value;
  endfunction

  function void get_io_fromBackend_ftqIdxAhead_0_bits_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_fromBackend_ftqIdxAhead_0_bits_value;
  endfunction

  function void set_io_fromBackend_ftqIdxAhead_0_bits_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_fromBackend_ftqIdxAhead_0_bits_value=value;
  endfunction

  function void get_io_fromBackend_ftqIdxSelOH_bitsxxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_fromBackend_ftqIdxSelOH_bits;
  endfunction

  function void set_io_fromBackend_ftqIdxSelOH_bitsxxcxrJQKToTQ;
    input logic [2:0] value;
    io_fromBackend_ftqIdxSelOH_bits=value;
  endfunction

  function void get_io_toBpu_redirect_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_valid;
  endfunction

  function void get_io_toBpu_redirect_bits_levelxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_level;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_pcxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_pc;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_pd_isRVCxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_pd_isRVC;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_pd_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_pd_isCall;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_pd_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_pd_isRet;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_sspxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_ssp;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_sctrxxcxrJQKToTQ;
    output logic [2:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_sctr;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_TOSW_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_TOSW_flag;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_TOSW_valuexxcxrJQKToTQ;
    output logic [4:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_TOSW_value;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_TOSR_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_TOSR_flag;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_TOSR_valuexxcxrJQKToTQ;
    output logic [4:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_TOSR_value;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_NOS_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_NOS_flag;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_NOS_valuexxcxrJQKToTQ;
    output logic [4:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_NOS_value;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_histPtr_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_histPtr_flag;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_histPtr_valuexxcxrJQKToTQ;
    output logic [7:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_histPtr_value;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_targetxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_target;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_takenxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_taken;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_shiftxxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_toBpu_redirect_bits_cfiUpdate_shift;
  endfunction

  function void get_io_toBpu_redirect_bits_cfiUpdate_addIntoHistxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirect_bits_cfiUpdate_addIntoHist;
  endfunction

  function void get_io_toBpu_update_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_valid;
  endfunction

  function void get_io_toBpu_update_bits_pcxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toBpu_update_bits_pc;
  endfunction

  function void get_io_toBpu_update_bits_spec_info_histPtr_valuexxcxrJQKToTQ;
    output logic [7:0] value;
    value=io_toBpu_update_bits_spec_info_histPtr_value;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_isCallxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_isCall;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_isRetxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_isRet;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_isJalrxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_isJalr;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_valid;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_brSlots_0_offsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toBpu_update_bits_ftb_entry_brSlots_0_offset;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_brSlots_0_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_brSlots_0_sharing;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_brSlots_0_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_brSlots_0_valid;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_brSlots_0_lowerxxcxrJQKToTQ;
    output logic [11:0] value;
    value=io_toBpu_update_bits_ftb_entry_brSlots_0_lower;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_brSlots_0_tarStatxxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_toBpu_update_bits_ftb_entry_brSlots_0_tarStat;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_tailSlot_offsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toBpu_update_bits_ftb_entry_tailSlot_offset;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_tailSlot_sharingxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_tailSlot_sharing;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_tailSlot_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_tailSlot_valid;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_tailSlot_lowerxxcxrJQKToTQ;
    output logic [19:0] value;
    value=io_toBpu_update_bits_ftb_entry_tailSlot_lower;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_tailSlot_tarStatxxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_toBpu_update_bits_ftb_entry_tailSlot_tarStat;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_pftAddrxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toBpu_update_bits_ftb_entry_pftAddr;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_carryxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_carry;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_last_may_be_rvi_callxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_last_may_be_rvi_call;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_strong_bias_0xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_strong_bias_0;
  endfunction

  function void get_io_toBpu_update_bits_ftb_entry_strong_bias_1xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_ftb_entry_strong_bias_1;
  endfunction

  function void get_io_toBpu_update_bits_cfi_idx_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_cfi_idx_valid;
  endfunction

  function void get_io_toBpu_update_bits_cfi_idx_bitsxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toBpu_update_bits_cfi_idx_bits;
  endfunction

  function void get_io_toBpu_update_bits_br_taken_mask_0xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_br_taken_mask_0;
  endfunction

  function void get_io_toBpu_update_bits_br_taken_mask_1xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_br_taken_mask_1;
  endfunction

  function void get_io_toBpu_update_bits_jmp_takenxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_jmp_taken;
  endfunction

  function void get_io_toBpu_update_bits_mispred_mask_0xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_mispred_mask_0;
  endfunction

  function void get_io_toBpu_update_bits_mispred_mask_1xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_mispred_mask_1;
  endfunction

  function void get_io_toBpu_update_bits_mispred_mask_2xxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_mispred_mask_2;
  endfunction

  function void get_io_toBpu_update_bits_false_hitxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_false_hit;
  endfunction

  function void get_io_toBpu_update_bits_old_entryxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_update_bits_old_entry;
  endfunction

  function void get_io_toBpu_update_bits_metaxxcxrJQKToTQ;
    output logic [259:0] value;
    value=io_toBpu_update_bits_meta;
  endfunction

  function void get_io_toBpu_update_bits_full_targetxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toBpu_update_bits_full_target;
  endfunction

  function void get_io_toBpu_enq_ptr_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_enq_ptr_flag;
  endfunction

  function void get_io_toBpu_enq_ptr_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toBpu_enq_ptr_value;
  endfunction

  function void get_io_toBpu_redirctFromIFUxxcxrJQKToTQ;
    output logic  value;
    value=io_toBpu_redirctFromIFU;
  endfunction

  function void get_io_toIfu_req_readyxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_req_ready;
  endfunction

  function void set_io_toIfu_req_readyxxcxrJQKToTQ;
    input logic  value;
    io_toIfu_req_ready=value;
  endfunction

  function void get_io_toIfu_req_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_req_valid;
  endfunction

  function void get_io_toIfu_req_bits_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toIfu_req_bits_startAddr;
  endfunction

  function void get_io_toIfu_req_bits_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toIfu_req_bits_nextlineStart;
  endfunction

  function void get_io_toIfu_req_bits_nextStartAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toIfu_req_bits_nextStartAddr;
  endfunction

  function void get_io_toIfu_req_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_req_bits_ftqIdx_flag;
  endfunction

  function void get_io_toIfu_req_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toIfu_req_bits_ftqIdx_value;
  endfunction

  function void get_io_toIfu_req_bits_ftqOffset_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_req_bits_ftqOffset_valid;
  endfunction

  function void get_io_toIfu_req_bits_ftqOffset_bitsxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toIfu_req_bits_ftqOffset_bits;
  endfunction

  function void get_io_toIfu_redirect_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_redirect_valid;
  endfunction

  function void get_io_toIfu_redirect_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_redirect_bits_ftqIdx_flag;
  endfunction

  function void get_io_toIfu_redirect_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toIfu_redirect_bits_ftqIdx_value;
  endfunction

  function void get_io_toIfu_redirect_bits_ftqOffsetxxcxrJQKToTQ;
    output logic [3:0] value;
    value=io_toIfu_redirect_bits_ftqOffset;
  endfunction

  function void get_io_toIfu_redirect_bits_levelxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_redirect_bits_level;
  endfunction

  function void get_io_toIfu_flushFromBpu_s2_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_flushFromBpu_s2_valid;
  endfunction

  function void get_io_toIfu_flushFromBpu_s2_bits_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_flushFromBpu_s2_bits_flag;
  endfunction

  function void get_io_toIfu_flushFromBpu_s2_bits_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toIfu_flushFromBpu_s2_bits_value;
  endfunction

  function void get_io_toIfu_flushFromBpu_s3_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_flushFromBpu_s3_valid;
  endfunction

  function void get_io_toIfu_flushFromBpu_s3_bits_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toIfu_flushFromBpu_s3_bits_flag;
  endfunction

  function void get_io_toIfu_flushFromBpu_s3_bits_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toIfu_flushFromBpu_s3_bits_value;
  endfunction

  function void get_io_toICache_req_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_valid;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_0_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_0_startAddr;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_0_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_0_nextlineStart;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_1_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_1_startAddr;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_1_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_1_nextlineStart;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_2_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_2_startAddr;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_2_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_2_nextlineStart;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_3_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_3_startAddr;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_3_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_3_nextlineStart;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_4_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_4_startAddr;
  endfunction

  function void get_io_toICache_req_bits_pcMemRead_4_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toICache_req_bits_pcMemRead_4_nextlineStart;
  endfunction

  function void get_io_toICache_req_bits_readValid_0xxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_bits_readValid_0;
  endfunction

  function void get_io_toICache_req_bits_readValid_1xxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_bits_readValid_1;
  endfunction

  function void get_io_toICache_req_bits_readValid_2xxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_bits_readValid_2;
  endfunction

  function void get_io_toICache_req_bits_readValid_3xxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_bits_readValid_3;
  endfunction

  function void get_io_toICache_req_bits_readValid_4xxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_bits_readValid_4;
  endfunction

  function void get_io_toICache_req_bits_backendExceptionxxcxrJQKToTQ;
    output logic  value;
    value=io_toICache_req_bits_backendException;
  endfunction

  function void get_io_toBackend_pc_mem_wenxxcxrJQKToTQ;
    output logic  value;
    value=io_toBackend_pc_mem_wen;
  endfunction

  function void get_io_toBackend_pc_mem_waddrxxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toBackend_pc_mem_waddr;
  endfunction

  function void get_io_toBackend_pc_mem_wdata_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toBackend_pc_mem_wdata_startAddr;
  endfunction

  function void get_io_toBackend_newest_entry_enxxcxrJQKToTQ;
    output logic  value;
    value=io_toBackend_newest_entry_en;
  endfunction

  function void get_io_toBackend_newest_entry_targetxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toBackend_newest_entry_target;
  endfunction

  function void get_io_toBackend_newest_entry_ptr_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toBackend_newest_entry_ptr_value;
  endfunction

  function void get_io_toPrefetch_req_readyxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_req_ready;
  endfunction

  function void set_io_toPrefetch_req_readyxxcxrJQKToTQ;
    input logic  value;
    io_toPrefetch_req_ready=value;
  endfunction

  function void get_io_toPrefetch_req_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_req_valid;
  endfunction

  function void get_io_toPrefetch_req_bits_startAddrxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toPrefetch_req_bits_startAddr;
  endfunction

  function void get_io_toPrefetch_req_bits_nextlineStartxxcxrJQKToTQ;
    output logic [49:0] value;
    value=io_toPrefetch_req_bits_nextlineStart;
  endfunction

  function void get_io_toPrefetch_req_bits_ftqIdx_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_req_bits_ftqIdx_flag;
  endfunction

  function void get_io_toPrefetch_req_bits_ftqIdx_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toPrefetch_req_bits_ftqIdx_value;
  endfunction

  function void get_io_toPrefetch_flushFromBpu_s2_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_flushFromBpu_s2_valid;
  endfunction

  function void get_io_toPrefetch_flushFromBpu_s2_bits_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_flushFromBpu_s2_bits_flag;
  endfunction

  function void get_io_toPrefetch_flushFromBpu_s2_bits_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toPrefetch_flushFromBpu_s2_bits_value;
  endfunction

  function void get_io_toPrefetch_flushFromBpu_s3_validxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_flushFromBpu_s3_valid;
  endfunction

  function void get_io_toPrefetch_flushFromBpu_s3_bits_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_toPrefetch_flushFromBpu_s3_bits_flag;
  endfunction

  function void get_io_toPrefetch_flushFromBpu_s3_bits_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_toPrefetch_flushFromBpu_s3_bits_value;
  endfunction

  function void get_io_toPrefetch_backendExceptionxxcxrJQKToTQ;
    output logic [1:0] value;
    value=io_toPrefetch_backendException;
  endfunction

  function void get_io_icacheFlushxxcxrJQKToTQ;
    output logic  value;
    value=io_icacheFlush;
  endfunction

  function void get_io_mmioCommitRead_mmioFtqPtr_flagxxcxrJQKToTQ;
    output logic  value;
    value=io_mmioCommitRead_mmioFtqPtr_flag;
  endfunction

  function void set_io_mmioCommitRead_mmioFtqPtr_flagxxcxrJQKToTQ;
    input logic  value;
    io_mmioCommitRead_mmioFtqPtr_flag=value;
  endfunction

  function void get_io_mmioCommitRead_mmioFtqPtr_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_mmioCommitRead_mmioFtqPtr_value;
  endfunction

  function void set_io_mmioCommitRead_mmioFtqPtr_valuexxcxrJQKToTQ;
    input logic [5:0] value;
    io_mmioCommitRead_mmioFtqPtr_value=value;
  endfunction

  function void get_io_mmioCommitRead_mmioLastCommitxxcxrJQKToTQ;
    output logic  value;
    value=io_mmioCommitRead_mmioLastCommit;
  endfunction

  function void get_io_perf_0_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_0_value;
  endfunction

  function void get_io_perf_1_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_1_value;
  endfunction

  function void get_io_perf_2_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_2_value;
  endfunction

  function void get_io_perf_3_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_3_value;
  endfunction

  function void get_io_perf_4_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_4_value;
  endfunction

  function void get_io_perf_5_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_5_value;
  endfunction

  function void get_io_perf_6_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_6_value;
  endfunction

  function void get_io_perf_7_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_7_value;
  endfunction

  function void get_io_perf_8_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_8_value;
  endfunction

  function void get_io_perf_9_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_9_value;
  endfunction

  function void get_io_perf_10_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_10_value;
  endfunction

  function void get_io_perf_11_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_11_value;
  endfunction

  function void get_io_perf_12_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_12_value;
  endfunction

  function void get_io_perf_13_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_13_value;
  endfunction

  function void get_io_perf_14_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_14_value;
  endfunction

  function void get_io_perf_15_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_15_value;
  endfunction

  function void get_io_perf_16_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_16_value;
  endfunction

  function void get_io_perf_17_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_17_value;
  endfunction

  function void get_io_perf_18_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_18_value;
  endfunction

  function void get_io_perf_19_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_19_value;
  endfunction

  function void get_io_perf_20_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_20_value;
  endfunction

  function void get_io_perf_21_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_21_value;
  endfunction

  function void get_io_perf_22_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_22_value;
  endfunction

  function void get_io_perf_23_valuexxcxrJQKToTQ;
    output logic [5:0] value;
    value=io_perf_23_value;
  endfunction



  initial begin
    $dumpfile("FtqTop.fst");
    $dumpvars(0, Ftq_top);
  end

  export "DPI-C" function finish_cxrJQKToTQ;
  function void finish_cxrJQKToTQ;
    $finish;
  endfunction


endmodule
