module DecodeStage_top;

  logic  clock;
  logic  reset;
  logic  io_redirect;
  logic  io_in_0_ready;
  logic  io_in_0_valid;
  logic [31:0] io_in_0_bits_instr;
  logic  io_in_0_bits_exceptionVec_0;
  logic  io_in_0_bits_exceptionVec_1;
  logic  io_in_0_bits_exceptionVec_2;
  logic  io_in_0_bits_exceptionVec_4;
  logic  io_in_0_bits_exceptionVec_5;
  logic  io_in_0_bits_exceptionVec_6;
  logic  io_in_0_bits_exceptionVec_7;
  logic  io_in_0_bits_exceptionVec_8;
  logic  io_in_0_bits_exceptionVec_9;
  logic  io_in_0_bits_exceptionVec_10;
  logic  io_in_0_bits_exceptionVec_11;
  logic  io_in_0_bits_exceptionVec_12;
  logic  io_in_0_bits_exceptionVec_13;
  logic  io_in_0_bits_exceptionVec_14;
  logic  io_in_0_bits_exceptionVec_15;
  logic  io_in_0_bits_exceptionVec_16;
  logic  io_in_0_bits_exceptionVec_17;
  logic  io_in_0_bits_exceptionVec_18;
  logic  io_in_0_bits_exceptionVec_19;
  logic  io_in_0_bits_exceptionVec_20;
  logic  io_in_0_bits_exceptionVec_21;
  logic  io_in_0_bits_exceptionVec_23;
  logic  io_in_0_bits_isFetchMalAddr;
  logic [3:0] io_in_0_bits_trigger;
  logic  io_in_0_bits_preDecodeInfo_isRVC;
  logic [1:0] io_in_0_bits_preDecodeInfo_brType;
  logic  io_in_0_bits_pred_taken;
  logic  io_in_0_bits_crossPageIPFFix;
  logic  io_in_0_bits_ftqPtr_flag;
  logic [5:0] io_in_0_bits_ftqPtr_value;
  logic [3:0] io_in_0_bits_ftqOffset;
  logic  io_in_0_bits_isLastInFtqEntry;
  logic  io_in_1_ready;
  logic  io_in_1_valid;
  logic [31:0] io_in_1_bits_instr;
  logic  io_in_1_bits_exceptionVec_0;
  logic  io_in_1_bits_exceptionVec_1;
  logic  io_in_1_bits_exceptionVec_2;
  logic  io_in_1_bits_exceptionVec_4;
  logic  io_in_1_bits_exceptionVec_5;
  logic  io_in_1_bits_exceptionVec_6;
  logic  io_in_1_bits_exceptionVec_7;
  logic  io_in_1_bits_exceptionVec_8;
  logic  io_in_1_bits_exceptionVec_9;
  logic  io_in_1_bits_exceptionVec_10;
  logic  io_in_1_bits_exceptionVec_11;
  logic  io_in_1_bits_exceptionVec_12;
  logic  io_in_1_bits_exceptionVec_13;
  logic  io_in_1_bits_exceptionVec_14;
  logic  io_in_1_bits_exceptionVec_15;
  logic  io_in_1_bits_exceptionVec_16;
  logic  io_in_1_bits_exceptionVec_17;
  logic  io_in_1_bits_exceptionVec_18;
  logic  io_in_1_bits_exceptionVec_19;
  logic  io_in_1_bits_exceptionVec_20;
  logic  io_in_1_bits_exceptionVec_21;
  logic  io_in_1_bits_exceptionVec_23;
  logic  io_in_1_bits_isFetchMalAddr;
  logic [3:0] io_in_1_bits_trigger;
  logic  io_in_1_bits_preDecodeInfo_isRVC;
  logic [1:0] io_in_1_bits_preDecodeInfo_brType;
  logic  io_in_1_bits_pred_taken;
  logic  io_in_1_bits_crossPageIPFFix;
  logic  io_in_1_bits_ftqPtr_flag;
  logic [5:0] io_in_1_bits_ftqPtr_value;
  logic [3:0] io_in_1_bits_ftqOffset;
  logic  io_in_1_bits_isLastInFtqEntry;
  logic  io_in_2_ready;
  logic  io_in_2_valid;
  logic [31:0] io_in_2_bits_instr;
  logic  io_in_2_bits_exceptionVec_0;
  logic  io_in_2_bits_exceptionVec_1;
  logic  io_in_2_bits_exceptionVec_2;
  logic  io_in_2_bits_exceptionVec_4;
  logic  io_in_2_bits_exceptionVec_5;
  logic  io_in_2_bits_exceptionVec_6;
  logic  io_in_2_bits_exceptionVec_7;
  logic  io_in_2_bits_exceptionVec_8;
  logic  io_in_2_bits_exceptionVec_9;
  logic  io_in_2_bits_exceptionVec_10;
  logic  io_in_2_bits_exceptionVec_11;
  logic  io_in_2_bits_exceptionVec_12;
  logic  io_in_2_bits_exceptionVec_13;
  logic  io_in_2_bits_exceptionVec_14;
  logic  io_in_2_bits_exceptionVec_15;
  logic  io_in_2_bits_exceptionVec_16;
  logic  io_in_2_bits_exceptionVec_17;
  logic  io_in_2_bits_exceptionVec_18;
  logic  io_in_2_bits_exceptionVec_19;
  logic  io_in_2_bits_exceptionVec_20;
  logic  io_in_2_bits_exceptionVec_21;
  logic  io_in_2_bits_exceptionVec_23;
  logic  io_in_2_bits_isFetchMalAddr;
  logic [3:0] io_in_2_bits_trigger;
  logic  io_in_2_bits_preDecodeInfo_isRVC;
  logic [1:0] io_in_2_bits_preDecodeInfo_brType;
  logic  io_in_2_bits_pred_taken;
  logic  io_in_2_bits_crossPageIPFFix;
  logic  io_in_2_bits_ftqPtr_flag;
  logic [5:0] io_in_2_bits_ftqPtr_value;
  logic [3:0] io_in_2_bits_ftqOffset;
  logic  io_in_2_bits_isLastInFtqEntry;
  logic  io_in_3_ready;
  logic  io_in_3_valid;
  logic [31:0] io_in_3_bits_instr;
  logic  io_in_3_bits_exceptionVec_0;
  logic  io_in_3_bits_exceptionVec_1;
  logic  io_in_3_bits_exceptionVec_2;
  logic  io_in_3_bits_exceptionVec_4;
  logic  io_in_3_bits_exceptionVec_5;
  logic  io_in_3_bits_exceptionVec_6;
  logic  io_in_3_bits_exceptionVec_7;
  logic  io_in_3_bits_exceptionVec_8;
  logic  io_in_3_bits_exceptionVec_9;
  logic  io_in_3_bits_exceptionVec_10;
  logic  io_in_3_bits_exceptionVec_11;
  logic  io_in_3_bits_exceptionVec_12;
  logic  io_in_3_bits_exceptionVec_13;
  logic  io_in_3_bits_exceptionVec_14;
  logic  io_in_3_bits_exceptionVec_15;
  logic  io_in_3_bits_exceptionVec_16;
  logic  io_in_3_bits_exceptionVec_17;
  logic  io_in_3_bits_exceptionVec_18;
  logic  io_in_3_bits_exceptionVec_19;
  logic  io_in_3_bits_exceptionVec_20;
  logic  io_in_3_bits_exceptionVec_21;
  logic  io_in_3_bits_exceptionVec_23;
  logic  io_in_3_bits_isFetchMalAddr;
  logic [3:0] io_in_3_bits_trigger;
  logic  io_in_3_bits_preDecodeInfo_isRVC;
  logic [1:0] io_in_3_bits_preDecodeInfo_brType;
  logic  io_in_3_bits_pred_taken;
  logic  io_in_3_bits_crossPageIPFFix;
  logic  io_in_3_bits_ftqPtr_flag;
  logic [5:0] io_in_3_bits_ftqPtr_value;
  logic [3:0] io_in_3_bits_ftqOffset;
  logic  io_in_3_bits_isLastInFtqEntry;
  logic  io_in_4_ready;
  logic  io_in_4_valid;
  logic [31:0] io_in_4_bits_instr;
  logic  io_in_4_bits_exceptionVec_0;
  logic  io_in_4_bits_exceptionVec_1;
  logic  io_in_4_bits_exceptionVec_2;
  logic  io_in_4_bits_exceptionVec_4;
  logic  io_in_4_bits_exceptionVec_5;
  logic  io_in_4_bits_exceptionVec_6;
  logic  io_in_4_bits_exceptionVec_7;
  logic  io_in_4_bits_exceptionVec_8;
  logic  io_in_4_bits_exceptionVec_9;
  logic  io_in_4_bits_exceptionVec_10;
  logic  io_in_4_bits_exceptionVec_11;
  logic  io_in_4_bits_exceptionVec_12;
  logic  io_in_4_bits_exceptionVec_13;
  logic  io_in_4_bits_exceptionVec_14;
  logic  io_in_4_bits_exceptionVec_15;
  logic  io_in_4_bits_exceptionVec_16;
  logic  io_in_4_bits_exceptionVec_17;
  logic  io_in_4_bits_exceptionVec_18;
  logic  io_in_4_bits_exceptionVec_19;
  logic  io_in_4_bits_exceptionVec_20;
  logic  io_in_4_bits_exceptionVec_21;
  logic  io_in_4_bits_exceptionVec_23;
  logic  io_in_4_bits_isFetchMalAddr;
  logic [3:0] io_in_4_bits_trigger;
  logic  io_in_4_bits_preDecodeInfo_isRVC;
  logic [1:0] io_in_4_bits_preDecodeInfo_brType;
  logic  io_in_4_bits_pred_taken;
  logic  io_in_4_bits_crossPageIPFFix;
  logic  io_in_4_bits_ftqPtr_flag;
  logic [5:0] io_in_4_bits_ftqPtr_value;
  logic [3:0] io_in_4_bits_ftqOffset;
  logic  io_in_4_bits_isLastInFtqEntry;
  logic  io_in_5_ready;
  logic  io_in_5_valid;
  logic [31:0] io_in_5_bits_instr;
  logic  io_in_5_bits_exceptionVec_0;
  logic  io_in_5_bits_exceptionVec_1;
  logic  io_in_5_bits_exceptionVec_2;
  logic  io_in_5_bits_exceptionVec_4;
  logic  io_in_5_bits_exceptionVec_5;
  logic  io_in_5_bits_exceptionVec_6;
  logic  io_in_5_bits_exceptionVec_7;
  logic  io_in_5_bits_exceptionVec_8;
  logic  io_in_5_bits_exceptionVec_9;
  logic  io_in_5_bits_exceptionVec_10;
  logic  io_in_5_bits_exceptionVec_11;
  logic  io_in_5_bits_exceptionVec_12;
  logic  io_in_5_bits_exceptionVec_13;
  logic  io_in_5_bits_exceptionVec_14;
  logic  io_in_5_bits_exceptionVec_15;
  logic  io_in_5_bits_exceptionVec_16;
  logic  io_in_5_bits_exceptionVec_17;
  logic  io_in_5_bits_exceptionVec_18;
  logic  io_in_5_bits_exceptionVec_19;
  logic  io_in_5_bits_exceptionVec_20;
  logic  io_in_5_bits_exceptionVec_21;
  logic  io_in_5_bits_exceptionVec_23;
  logic  io_in_5_bits_isFetchMalAddr;
  logic [3:0] io_in_5_bits_trigger;
  logic  io_in_5_bits_preDecodeInfo_isRVC;
  logic [1:0] io_in_5_bits_preDecodeInfo_brType;
  logic  io_in_5_bits_pred_taken;
  logic  io_in_5_bits_crossPageIPFFix;
  logic  io_in_5_bits_ftqPtr_flag;
  logic [5:0] io_in_5_bits_ftqPtr_value;
  logic [3:0] io_in_5_bits_ftqOffset;
  logic  io_in_5_bits_isLastInFtqEntry;
  logic  io_out_0_ready;
  logic  io_out_0_valid;
  logic [31:0] io_out_0_bits_instr;
  logic  io_out_0_bits_exceptionVec_0;
  logic  io_out_0_bits_exceptionVec_1;
  logic  io_out_0_bits_exceptionVec_2;
  logic  io_out_0_bits_exceptionVec_3;
  logic  io_out_0_bits_exceptionVec_4;
  logic  io_out_0_bits_exceptionVec_5;
  logic  io_out_0_bits_exceptionVec_6;
  logic  io_out_0_bits_exceptionVec_7;
  logic  io_out_0_bits_exceptionVec_8;
  logic  io_out_0_bits_exceptionVec_9;
  logic  io_out_0_bits_exceptionVec_10;
  logic  io_out_0_bits_exceptionVec_11;
  logic  io_out_0_bits_exceptionVec_12;
  logic  io_out_0_bits_exceptionVec_13;
  logic  io_out_0_bits_exceptionVec_14;
  logic  io_out_0_bits_exceptionVec_15;
  logic  io_out_0_bits_exceptionVec_16;
  logic  io_out_0_bits_exceptionVec_17;
  logic  io_out_0_bits_exceptionVec_18;
  logic  io_out_0_bits_exceptionVec_19;
  logic  io_out_0_bits_exceptionVec_20;
  logic  io_out_0_bits_exceptionVec_21;
  logic  io_out_0_bits_exceptionVec_22;
  logic  io_out_0_bits_exceptionVec_23;
  logic  io_out_0_bits_isFetchMalAddr;
  logic [3:0] io_out_0_bits_trigger;
  logic  io_out_0_bits_preDecodeInfo_isRVC;
  logic [1:0] io_out_0_bits_preDecodeInfo_brType;
  logic  io_out_0_bits_pred_taken;
  logic  io_out_0_bits_crossPageIPFFix;
  logic  io_out_0_bits_ftqPtr_flag;
  logic [5:0] io_out_0_bits_ftqPtr_value;
  logic [3:0] io_out_0_bits_ftqOffset;
  logic [3:0] io_out_0_bits_srcType_0;
  logic [3:0] io_out_0_bits_srcType_1;
  logic [3:0] io_out_0_bits_srcType_2;
  logic [3:0] io_out_0_bits_srcType_3;
  logic [3:0] io_out_0_bits_srcType_4;
  logic [5:0] io_out_0_bits_lsrc_0;
  logic [5:0] io_out_0_bits_lsrc_1;
  logic [5:0] io_out_0_bits_lsrc_2;
  logic [5:0] io_out_0_bits_ldest;
  logic [34:0] io_out_0_bits_fuType;
  logic [8:0] io_out_0_bits_fuOpType;
  logic  io_out_0_bits_rfWen;
  logic  io_out_0_bits_fpWen;
  logic  io_out_0_bits_vecWen;
  logic  io_out_0_bits_v0Wen;
  logic  io_out_0_bits_vlWen;
  logic  io_out_0_bits_isXSTrap;
  logic  io_out_0_bits_waitForward;
  logic  io_out_0_bits_blockBackward;
  logic  io_out_0_bits_flushPipe;
  logic  io_out_0_bits_canRobCompress;
  logic [3:0] io_out_0_bits_selImm;
  logic [21:0] io_out_0_bits_imm;
  logic [1:0] io_out_0_bits_fpu_typeTagOut;
  logic  io_out_0_bits_fpu_wflags;
  logic [1:0] io_out_0_bits_fpu_typ;
  logic [1:0] io_out_0_bits_fpu_fmt;
  logic [2:0] io_out_0_bits_fpu_rm;
  logic  io_out_0_bits_vpu_vill;
  logic  io_out_0_bits_vpu_vma;
  logic  io_out_0_bits_vpu_vta;
  logic [1:0] io_out_0_bits_vpu_vsew;
  logic [2:0] io_out_0_bits_vpu_vlmul;
  logic  io_out_0_bits_vpu_specVill;
  logic  io_out_0_bits_vpu_specVma;
  logic  io_out_0_bits_vpu_specVta;
  logic [1:0] io_out_0_bits_vpu_specVsew;
  logic [2:0] io_out_0_bits_vpu_specVlmul;
  logic  io_out_0_bits_vpu_vm;
  logic [7:0] io_out_0_bits_vpu_vstart;
  logic  io_out_0_bits_vpu_fpu_isFoldTo1_2;
  logic  io_out_0_bits_vpu_fpu_isFoldTo1_4;
  logic  io_out_0_bits_vpu_fpu_isFoldTo1_8;
  logic [2:0] io_out_0_bits_vpu_nf;
  logic [1:0] io_out_0_bits_vpu_veew;
  logic  io_out_0_bits_vpu_isExt;
  logic  io_out_0_bits_vpu_isNarrow;
  logic  io_out_0_bits_vpu_isDstMask;
  logic  io_out_0_bits_vpu_isOpMask;
  logic  io_out_0_bits_vpu_isDependOldVd;
  logic  io_out_0_bits_vpu_isWritePartVd;
  logic  io_out_0_bits_vpu_isVleff;
  logic  io_out_0_bits_vlsInstr;
  logic  io_out_0_bits_wfflags;
  logic  io_out_0_bits_isMove;
  logic [6:0] io_out_0_bits_uopIdx;
  logic [5:0] io_out_0_bits_uopSplitType;
  logic  io_out_0_bits_isVset;
  logic  io_out_0_bits_firstUop;
  logic  io_out_0_bits_lastUop;
  logic [6:0] io_out_0_bits_numWB;
  logic [2:0] io_out_0_bits_commitType;
  logic  io_out_1_ready;
  logic  io_out_1_valid;
  logic [31:0] io_out_1_bits_instr;
  logic  io_out_1_bits_exceptionVec_0;
  logic  io_out_1_bits_exceptionVec_1;
  logic  io_out_1_bits_exceptionVec_2;
  logic  io_out_1_bits_exceptionVec_3;
  logic  io_out_1_bits_exceptionVec_4;
  logic  io_out_1_bits_exceptionVec_5;
  logic  io_out_1_bits_exceptionVec_6;
  logic  io_out_1_bits_exceptionVec_7;
  logic  io_out_1_bits_exceptionVec_8;
  logic  io_out_1_bits_exceptionVec_9;
  logic  io_out_1_bits_exceptionVec_10;
  logic  io_out_1_bits_exceptionVec_11;
  logic  io_out_1_bits_exceptionVec_12;
  logic  io_out_1_bits_exceptionVec_13;
  logic  io_out_1_bits_exceptionVec_14;
  logic  io_out_1_bits_exceptionVec_15;
  logic  io_out_1_bits_exceptionVec_16;
  logic  io_out_1_bits_exceptionVec_17;
  logic  io_out_1_bits_exceptionVec_18;
  logic  io_out_1_bits_exceptionVec_19;
  logic  io_out_1_bits_exceptionVec_20;
  logic  io_out_1_bits_exceptionVec_21;
  logic  io_out_1_bits_exceptionVec_22;
  logic  io_out_1_bits_exceptionVec_23;
  logic  io_out_1_bits_isFetchMalAddr;
  logic [3:0] io_out_1_bits_trigger;
  logic  io_out_1_bits_preDecodeInfo_isRVC;
  logic [1:0] io_out_1_bits_preDecodeInfo_brType;
  logic  io_out_1_bits_pred_taken;
  logic  io_out_1_bits_crossPageIPFFix;
  logic  io_out_1_bits_ftqPtr_flag;
  logic [5:0] io_out_1_bits_ftqPtr_value;
  logic [3:0] io_out_1_bits_ftqOffset;
  logic [3:0] io_out_1_bits_srcType_0;
  logic [3:0] io_out_1_bits_srcType_1;
  logic [3:0] io_out_1_bits_srcType_2;
  logic [3:0] io_out_1_bits_srcType_3;
  logic [3:0] io_out_1_bits_srcType_4;
  logic [5:0] io_out_1_bits_lsrc_0;
  logic [5:0] io_out_1_bits_lsrc_1;
  logic [5:0] io_out_1_bits_lsrc_2;
  logic [5:0] io_out_1_bits_ldest;
  logic [34:0] io_out_1_bits_fuType;
  logic [8:0] io_out_1_bits_fuOpType;
  logic  io_out_1_bits_rfWen;
  logic  io_out_1_bits_fpWen;
  logic  io_out_1_bits_vecWen;
  logic  io_out_1_bits_v0Wen;
  logic  io_out_1_bits_vlWen;
  logic  io_out_1_bits_isXSTrap;
  logic  io_out_1_bits_waitForward;
  logic  io_out_1_bits_blockBackward;
  logic  io_out_1_bits_flushPipe;
  logic  io_out_1_bits_canRobCompress;
  logic [3:0] io_out_1_bits_selImm;
  logic [21:0] io_out_1_bits_imm;
  logic [1:0] io_out_1_bits_fpu_typeTagOut;
  logic  io_out_1_bits_fpu_wflags;
  logic [1:0] io_out_1_bits_fpu_typ;
  logic [1:0] io_out_1_bits_fpu_fmt;
  logic [2:0] io_out_1_bits_fpu_rm;
  logic  io_out_1_bits_vpu_vill;
  logic  io_out_1_bits_vpu_vma;
  logic  io_out_1_bits_vpu_vta;
  logic [1:0] io_out_1_bits_vpu_vsew;
  logic [2:0] io_out_1_bits_vpu_vlmul;
  logic  io_out_1_bits_vpu_specVill;
  logic  io_out_1_bits_vpu_specVma;
  logic  io_out_1_bits_vpu_specVta;
  logic [1:0] io_out_1_bits_vpu_specVsew;
  logic [2:0] io_out_1_bits_vpu_specVlmul;
  logic  io_out_1_bits_vpu_vm;
  logic [7:0] io_out_1_bits_vpu_vstart;
  logic  io_out_1_bits_vpu_fpu_isFoldTo1_2;
  logic  io_out_1_bits_vpu_fpu_isFoldTo1_4;
  logic  io_out_1_bits_vpu_fpu_isFoldTo1_8;
  logic [2:0] io_out_1_bits_vpu_nf;
  logic [1:0] io_out_1_bits_vpu_veew;
  logic  io_out_1_bits_vpu_isExt;
  logic  io_out_1_bits_vpu_isNarrow;
  logic  io_out_1_bits_vpu_isDstMask;
  logic  io_out_1_bits_vpu_isOpMask;
  logic  io_out_1_bits_vpu_isDependOldVd;
  logic  io_out_1_bits_vpu_isWritePartVd;
  logic  io_out_1_bits_vpu_isVleff;
  logic  io_out_1_bits_vlsInstr;
  logic  io_out_1_bits_wfflags;
  logic  io_out_1_bits_isMove;
  logic [6:0] io_out_1_bits_uopIdx;
  logic [5:0] io_out_1_bits_uopSplitType;
  logic  io_out_1_bits_isVset;
  logic  io_out_1_bits_firstUop;
  logic  io_out_1_bits_lastUop;
  logic [6:0] io_out_1_bits_numWB;
  logic [2:0] io_out_1_bits_commitType;
  logic  io_out_2_ready;
  logic  io_out_2_valid;
  logic [31:0] io_out_2_bits_instr;
  logic  io_out_2_bits_exceptionVec_0;
  logic  io_out_2_bits_exceptionVec_1;
  logic  io_out_2_bits_exceptionVec_2;
  logic  io_out_2_bits_exceptionVec_3;
  logic  io_out_2_bits_exceptionVec_4;
  logic  io_out_2_bits_exceptionVec_5;
  logic  io_out_2_bits_exceptionVec_6;
  logic  io_out_2_bits_exceptionVec_7;
  logic  io_out_2_bits_exceptionVec_8;
  logic  io_out_2_bits_exceptionVec_9;
  logic  io_out_2_bits_exceptionVec_10;
  logic  io_out_2_bits_exceptionVec_11;
  logic  io_out_2_bits_exceptionVec_12;
  logic  io_out_2_bits_exceptionVec_13;
  logic  io_out_2_bits_exceptionVec_14;
  logic  io_out_2_bits_exceptionVec_15;
  logic  io_out_2_bits_exceptionVec_16;
  logic  io_out_2_bits_exceptionVec_17;
  logic  io_out_2_bits_exceptionVec_18;
  logic  io_out_2_bits_exceptionVec_19;
  logic  io_out_2_bits_exceptionVec_20;
  logic  io_out_2_bits_exceptionVec_21;
  logic  io_out_2_bits_exceptionVec_22;
  logic  io_out_2_bits_exceptionVec_23;
  logic  io_out_2_bits_isFetchMalAddr;
  logic [3:0] io_out_2_bits_trigger;
  logic  io_out_2_bits_preDecodeInfo_isRVC;
  logic [1:0] io_out_2_bits_preDecodeInfo_brType;
  logic  io_out_2_bits_pred_taken;
  logic  io_out_2_bits_crossPageIPFFix;
  logic  io_out_2_bits_ftqPtr_flag;
  logic [5:0] io_out_2_bits_ftqPtr_value;
  logic [3:0] io_out_2_bits_ftqOffset;
  logic [3:0] io_out_2_bits_srcType_0;
  logic [3:0] io_out_2_bits_srcType_1;
  logic [3:0] io_out_2_bits_srcType_2;
  logic [3:0] io_out_2_bits_srcType_3;
  logic [3:0] io_out_2_bits_srcType_4;
  logic [5:0] io_out_2_bits_lsrc_0;
  logic [5:0] io_out_2_bits_lsrc_1;
  logic [5:0] io_out_2_bits_lsrc_2;
  logic [5:0] io_out_2_bits_ldest;
  logic [34:0] io_out_2_bits_fuType;
  logic [8:0] io_out_2_bits_fuOpType;
  logic  io_out_2_bits_rfWen;
  logic  io_out_2_bits_fpWen;
  logic  io_out_2_bits_vecWen;
  logic  io_out_2_bits_v0Wen;
  logic  io_out_2_bits_vlWen;
  logic  io_out_2_bits_isXSTrap;
  logic  io_out_2_bits_waitForward;
  logic  io_out_2_bits_blockBackward;
  logic  io_out_2_bits_flushPipe;
  logic  io_out_2_bits_canRobCompress;
  logic [3:0] io_out_2_bits_selImm;
  logic [21:0] io_out_2_bits_imm;
  logic [1:0] io_out_2_bits_fpu_typeTagOut;
  logic  io_out_2_bits_fpu_wflags;
  logic [1:0] io_out_2_bits_fpu_typ;
  logic [1:0] io_out_2_bits_fpu_fmt;
  logic [2:0] io_out_2_bits_fpu_rm;
  logic  io_out_2_bits_vpu_vill;
  logic  io_out_2_bits_vpu_vma;
  logic  io_out_2_bits_vpu_vta;
  logic [1:0] io_out_2_bits_vpu_vsew;
  logic [2:0] io_out_2_bits_vpu_vlmul;
  logic  io_out_2_bits_vpu_specVill;
  logic  io_out_2_bits_vpu_specVma;
  logic  io_out_2_bits_vpu_specVta;
  logic [1:0] io_out_2_bits_vpu_specVsew;
  logic [2:0] io_out_2_bits_vpu_specVlmul;
  logic  io_out_2_bits_vpu_vm;
  logic [7:0] io_out_2_bits_vpu_vstart;
  logic  io_out_2_bits_vpu_fpu_isFoldTo1_2;
  logic  io_out_2_bits_vpu_fpu_isFoldTo1_4;
  logic  io_out_2_bits_vpu_fpu_isFoldTo1_8;
  logic [2:0] io_out_2_bits_vpu_nf;
  logic [1:0] io_out_2_bits_vpu_veew;
  logic  io_out_2_bits_vpu_isExt;
  logic  io_out_2_bits_vpu_isNarrow;
  logic  io_out_2_bits_vpu_isDstMask;
  logic  io_out_2_bits_vpu_isOpMask;
  logic  io_out_2_bits_vpu_isDependOldVd;
  logic  io_out_2_bits_vpu_isWritePartVd;
  logic  io_out_2_bits_vpu_isVleff;
  logic  io_out_2_bits_vlsInstr;
  logic  io_out_2_bits_wfflags;
  logic  io_out_2_bits_isMove;
  logic [6:0] io_out_2_bits_uopIdx;
  logic [5:0] io_out_2_bits_uopSplitType;
  logic  io_out_2_bits_isVset;
  logic  io_out_2_bits_firstUop;
  logic  io_out_2_bits_lastUop;
  logic [6:0] io_out_2_bits_numWB;
  logic [2:0] io_out_2_bits_commitType;
  logic  io_out_3_ready;
  logic  io_out_3_valid;
  logic [31:0] io_out_3_bits_instr;
  logic  io_out_3_bits_exceptionVec_0;
  logic  io_out_3_bits_exceptionVec_1;
  logic  io_out_3_bits_exceptionVec_2;
  logic  io_out_3_bits_exceptionVec_3;
  logic  io_out_3_bits_exceptionVec_4;
  logic  io_out_3_bits_exceptionVec_5;
  logic  io_out_3_bits_exceptionVec_6;
  logic  io_out_3_bits_exceptionVec_7;
  logic  io_out_3_bits_exceptionVec_8;
  logic  io_out_3_bits_exceptionVec_9;
  logic  io_out_3_bits_exceptionVec_10;
  logic  io_out_3_bits_exceptionVec_11;
  logic  io_out_3_bits_exceptionVec_12;
  logic  io_out_3_bits_exceptionVec_13;
  logic  io_out_3_bits_exceptionVec_14;
  logic  io_out_3_bits_exceptionVec_15;
  logic  io_out_3_bits_exceptionVec_16;
  logic  io_out_3_bits_exceptionVec_17;
  logic  io_out_3_bits_exceptionVec_18;
  logic  io_out_3_bits_exceptionVec_19;
  logic  io_out_3_bits_exceptionVec_20;
  logic  io_out_3_bits_exceptionVec_21;
  logic  io_out_3_bits_exceptionVec_22;
  logic  io_out_3_bits_exceptionVec_23;
  logic  io_out_3_bits_isFetchMalAddr;
  logic [3:0] io_out_3_bits_trigger;
  logic  io_out_3_bits_preDecodeInfo_isRVC;
  logic [1:0] io_out_3_bits_preDecodeInfo_brType;
  logic  io_out_3_bits_pred_taken;
  logic  io_out_3_bits_crossPageIPFFix;
  logic  io_out_3_bits_ftqPtr_flag;
  logic [5:0] io_out_3_bits_ftqPtr_value;
  logic [3:0] io_out_3_bits_ftqOffset;
  logic [3:0] io_out_3_bits_srcType_0;
  logic [3:0] io_out_3_bits_srcType_1;
  logic [3:0] io_out_3_bits_srcType_2;
  logic [3:0] io_out_3_bits_srcType_3;
  logic [3:0] io_out_3_bits_srcType_4;
  logic [5:0] io_out_3_bits_lsrc_0;
  logic [5:0] io_out_3_bits_lsrc_1;
  logic [5:0] io_out_3_bits_lsrc_2;
  logic [5:0] io_out_3_bits_ldest;
  logic [34:0] io_out_3_bits_fuType;
  logic [8:0] io_out_3_bits_fuOpType;
  logic  io_out_3_bits_rfWen;
  logic  io_out_3_bits_fpWen;
  logic  io_out_3_bits_vecWen;
  logic  io_out_3_bits_v0Wen;
  logic  io_out_3_bits_vlWen;
  logic  io_out_3_bits_isXSTrap;
  logic  io_out_3_bits_waitForward;
  logic  io_out_3_bits_blockBackward;
  logic  io_out_3_bits_flushPipe;
  logic  io_out_3_bits_canRobCompress;
  logic [3:0] io_out_3_bits_selImm;
  logic [21:0] io_out_3_bits_imm;
  logic [1:0] io_out_3_bits_fpu_typeTagOut;
  logic  io_out_3_bits_fpu_wflags;
  logic [1:0] io_out_3_bits_fpu_typ;
  logic [1:0] io_out_3_bits_fpu_fmt;
  logic [2:0] io_out_3_bits_fpu_rm;
  logic  io_out_3_bits_vpu_vill;
  logic  io_out_3_bits_vpu_vma;
  logic  io_out_3_bits_vpu_vta;
  logic [1:0] io_out_3_bits_vpu_vsew;
  logic [2:0] io_out_3_bits_vpu_vlmul;
  logic  io_out_3_bits_vpu_specVill;
  logic  io_out_3_bits_vpu_specVma;
  logic  io_out_3_bits_vpu_specVta;
  logic [1:0] io_out_3_bits_vpu_specVsew;
  logic [2:0] io_out_3_bits_vpu_specVlmul;
  logic  io_out_3_bits_vpu_vm;
  logic [7:0] io_out_3_bits_vpu_vstart;
  logic  io_out_3_bits_vpu_fpu_isFoldTo1_2;
  logic  io_out_3_bits_vpu_fpu_isFoldTo1_4;
  logic  io_out_3_bits_vpu_fpu_isFoldTo1_8;
  logic [2:0] io_out_3_bits_vpu_nf;
  logic [1:0] io_out_3_bits_vpu_veew;
  logic  io_out_3_bits_vpu_isExt;
  logic  io_out_3_bits_vpu_isNarrow;
  logic  io_out_3_bits_vpu_isDstMask;
  logic  io_out_3_bits_vpu_isOpMask;
  logic  io_out_3_bits_vpu_isDependOldVd;
  logic  io_out_3_bits_vpu_isWritePartVd;
  logic  io_out_3_bits_vpu_isVleff;
  logic  io_out_3_bits_vlsInstr;
  logic  io_out_3_bits_wfflags;
  logic  io_out_3_bits_isMove;
  logic [6:0] io_out_3_bits_uopIdx;
  logic [5:0] io_out_3_bits_uopSplitType;
  logic  io_out_3_bits_isVset;
  logic  io_out_3_bits_firstUop;
  logic  io_out_3_bits_lastUop;
  logic [6:0] io_out_3_bits_numWB;
  logic [2:0] io_out_3_bits_commitType;
  logic  io_out_4_ready;
  logic  io_out_4_valid;
  logic [31:0] io_out_4_bits_instr;
  logic  io_out_4_bits_exceptionVec_0;
  logic  io_out_4_bits_exceptionVec_1;
  logic  io_out_4_bits_exceptionVec_2;
  logic  io_out_4_bits_exceptionVec_3;
  logic  io_out_4_bits_exceptionVec_4;
  logic  io_out_4_bits_exceptionVec_5;
  logic  io_out_4_bits_exceptionVec_6;
  logic  io_out_4_bits_exceptionVec_7;
  logic  io_out_4_bits_exceptionVec_8;
  logic  io_out_4_bits_exceptionVec_9;
  logic  io_out_4_bits_exceptionVec_10;
  logic  io_out_4_bits_exceptionVec_11;
  logic  io_out_4_bits_exceptionVec_12;
  logic  io_out_4_bits_exceptionVec_13;
  logic  io_out_4_bits_exceptionVec_14;
  logic  io_out_4_bits_exceptionVec_15;
  logic  io_out_4_bits_exceptionVec_16;
  logic  io_out_4_bits_exceptionVec_17;
  logic  io_out_4_bits_exceptionVec_18;
  logic  io_out_4_bits_exceptionVec_19;
  logic  io_out_4_bits_exceptionVec_20;
  logic  io_out_4_bits_exceptionVec_21;
  logic  io_out_4_bits_exceptionVec_22;
  logic  io_out_4_bits_exceptionVec_23;
  logic  io_out_4_bits_isFetchMalAddr;
  logic [3:0] io_out_4_bits_trigger;
  logic  io_out_4_bits_preDecodeInfo_isRVC;
  logic [1:0] io_out_4_bits_preDecodeInfo_brType;
  logic  io_out_4_bits_pred_taken;
  logic  io_out_4_bits_crossPageIPFFix;
  logic  io_out_4_bits_ftqPtr_flag;
  logic [5:0] io_out_4_bits_ftqPtr_value;
  logic [3:0] io_out_4_bits_ftqOffset;
  logic [3:0] io_out_4_bits_srcType_0;
  logic [3:0] io_out_4_bits_srcType_1;
  logic [3:0] io_out_4_bits_srcType_2;
  logic [3:0] io_out_4_bits_srcType_3;
  logic [3:0] io_out_4_bits_srcType_4;
  logic [5:0] io_out_4_bits_lsrc_0;
  logic [5:0] io_out_4_bits_lsrc_1;
  logic [5:0] io_out_4_bits_lsrc_2;
  logic [5:0] io_out_4_bits_ldest;
  logic [34:0] io_out_4_bits_fuType;
  logic [8:0] io_out_4_bits_fuOpType;
  logic  io_out_4_bits_rfWen;
  logic  io_out_4_bits_fpWen;
  logic  io_out_4_bits_vecWen;
  logic  io_out_4_bits_v0Wen;
  logic  io_out_4_bits_vlWen;
  logic  io_out_4_bits_isXSTrap;
  logic  io_out_4_bits_waitForward;
  logic  io_out_4_bits_blockBackward;
  logic  io_out_4_bits_flushPipe;
  logic  io_out_4_bits_canRobCompress;
  logic [3:0] io_out_4_bits_selImm;
  logic [21:0] io_out_4_bits_imm;
  logic [1:0] io_out_4_bits_fpu_typeTagOut;
  logic  io_out_4_bits_fpu_wflags;
  logic [1:0] io_out_4_bits_fpu_typ;
  logic [1:0] io_out_4_bits_fpu_fmt;
  logic [2:0] io_out_4_bits_fpu_rm;
  logic  io_out_4_bits_vpu_vill;
  logic  io_out_4_bits_vpu_vma;
  logic  io_out_4_bits_vpu_vta;
  logic [1:0] io_out_4_bits_vpu_vsew;
  logic [2:0] io_out_4_bits_vpu_vlmul;
  logic  io_out_4_bits_vpu_specVill;
  logic  io_out_4_bits_vpu_specVma;
  logic  io_out_4_bits_vpu_specVta;
  logic [1:0] io_out_4_bits_vpu_specVsew;
  logic [2:0] io_out_4_bits_vpu_specVlmul;
  logic  io_out_4_bits_vpu_vm;
  logic [7:0] io_out_4_bits_vpu_vstart;
  logic  io_out_4_bits_vpu_fpu_isFoldTo1_2;
  logic  io_out_4_bits_vpu_fpu_isFoldTo1_4;
  logic  io_out_4_bits_vpu_fpu_isFoldTo1_8;
  logic [2:0] io_out_4_bits_vpu_nf;
  logic [1:0] io_out_4_bits_vpu_veew;
  logic  io_out_4_bits_vpu_isExt;
  logic  io_out_4_bits_vpu_isNarrow;
  logic  io_out_4_bits_vpu_isDstMask;
  logic  io_out_4_bits_vpu_isOpMask;
  logic  io_out_4_bits_vpu_isDependOldVd;
  logic  io_out_4_bits_vpu_isWritePartVd;
  logic  io_out_4_bits_vpu_isVleff;
  logic  io_out_4_bits_vlsInstr;
  logic  io_out_4_bits_wfflags;
  logic  io_out_4_bits_isMove;
  logic [6:0] io_out_4_bits_uopIdx;
  logic [5:0] io_out_4_bits_uopSplitType;
  logic  io_out_4_bits_isVset;
  logic  io_out_4_bits_firstUop;
  logic  io_out_4_bits_lastUop;
  logic [6:0] io_out_4_bits_numWB;
  logic [2:0] io_out_4_bits_commitType;
  logic  io_out_5_ready;
  logic  io_out_5_valid;
  logic [31:0] io_out_5_bits_instr;
  logic  io_out_5_bits_exceptionVec_0;
  logic  io_out_5_bits_exceptionVec_1;
  logic  io_out_5_bits_exceptionVec_2;
  logic  io_out_5_bits_exceptionVec_3;
  logic  io_out_5_bits_exceptionVec_4;
  logic  io_out_5_bits_exceptionVec_5;
  logic  io_out_5_bits_exceptionVec_6;
  logic  io_out_5_bits_exceptionVec_7;
  logic  io_out_5_bits_exceptionVec_8;
  logic  io_out_5_bits_exceptionVec_9;
  logic  io_out_5_bits_exceptionVec_10;
  logic  io_out_5_bits_exceptionVec_11;
  logic  io_out_5_bits_exceptionVec_12;
  logic  io_out_5_bits_exceptionVec_13;
  logic  io_out_5_bits_exceptionVec_14;
  logic  io_out_5_bits_exceptionVec_15;
  logic  io_out_5_bits_exceptionVec_16;
  logic  io_out_5_bits_exceptionVec_17;
  logic  io_out_5_bits_exceptionVec_18;
  logic  io_out_5_bits_exceptionVec_19;
  logic  io_out_5_bits_exceptionVec_20;
  logic  io_out_5_bits_exceptionVec_21;
  logic  io_out_5_bits_exceptionVec_22;
  logic  io_out_5_bits_exceptionVec_23;
  logic  io_out_5_bits_isFetchMalAddr;
  logic [3:0] io_out_5_bits_trigger;
  logic  io_out_5_bits_preDecodeInfo_isRVC;
  logic [1:0] io_out_5_bits_preDecodeInfo_brType;
  logic  io_out_5_bits_pred_taken;
  logic  io_out_5_bits_crossPageIPFFix;
  logic  io_out_5_bits_ftqPtr_flag;
  logic [5:0] io_out_5_bits_ftqPtr_value;
  logic [3:0] io_out_5_bits_ftqOffset;
  logic [3:0] io_out_5_bits_srcType_0;
  logic [3:0] io_out_5_bits_srcType_1;
  logic [3:0] io_out_5_bits_srcType_2;
  logic [3:0] io_out_5_bits_srcType_3;
  logic [3:0] io_out_5_bits_srcType_4;
  logic [5:0] io_out_5_bits_lsrc_0;
  logic [5:0] io_out_5_bits_lsrc_1;
  logic [5:0] io_out_5_bits_lsrc_2;
  logic [5:0] io_out_5_bits_ldest;
  logic [34:0] io_out_5_bits_fuType;
  logic [8:0] io_out_5_bits_fuOpType;
  logic  io_out_5_bits_rfWen;
  logic  io_out_5_bits_fpWen;
  logic  io_out_5_bits_vecWen;
  logic  io_out_5_bits_v0Wen;
  logic  io_out_5_bits_vlWen;
  logic  io_out_5_bits_isXSTrap;
  logic  io_out_5_bits_waitForward;
  logic  io_out_5_bits_blockBackward;
  logic  io_out_5_bits_flushPipe;
  logic  io_out_5_bits_canRobCompress;
  logic [3:0] io_out_5_bits_selImm;
  logic [21:0] io_out_5_bits_imm;
  logic [1:0] io_out_5_bits_fpu_typeTagOut;
  logic  io_out_5_bits_fpu_wflags;
  logic [1:0] io_out_5_bits_fpu_typ;
  logic [1:0] io_out_5_bits_fpu_fmt;
  logic [2:0] io_out_5_bits_fpu_rm;
  logic  io_out_5_bits_vpu_vill;
  logic  io_out_5_bits_vpu_vma;
  logic  io_out_5_bits_vpu_vta;
  logic [1:0] io_out_5_bits_vpu_vsew;
  logic [2:0] io_out_5_bits_vpu_vlmul;
  logic  io_out_5_bits_vpu_specVill;
  logic  io_out_5_bits_vpu_specVma;
  logic  io_out_5_bits_vpu_specVta;
  logic [1:0] io_out_5_bits_vpu_specVsew;
  logic [2:0] io_out_5_bits_vpu_specVlmul;
  logic  io_out_5_bits_vpu_vm;
  logic [7:0] io_out_5_bits_vpu_vstart;
  logic  io_out_5_bits_vpu_fpu_isFoldTo1_2;
  logic  io_out_5_bits_vpu_fpu_isFoldTo1_4;
  logic  io_out_5_bits_vpu_fpu_isFoldTo1_8;
  logic [2:0] io_out_5_bits_vpu_nf;
  logic [1:0] io_out_5_bits_vpu_veew;
  logic  io_out_5_bits_vpu_isExt;
  logic  io_out_5_bits_vpu_isNarrow;
  logic  io_out_5_bits_vpu_isDstMask;
  logic  io_out_5_bits_vpu_isOpMask;
  logic  io_out_5_bits_vpu_isDependOldVd;
  logic  io_out_5_bits_vpu_isWritePartVd;
  logic  io_out_5_bits_vpu_isVleff;
  logic  io_out_5_bits_vlsInstr;
  logic  io_out_5_bits_wfflags;
  logic  io_out_5_bits_isMove;
  logic [6:0] io_out_5_bits_uopIdx;
  logic [5:0] io_out_5_bits_uopSplitType;
  logic  io_out_5_bits_isVset;
  logic  io_out_5_bits_firstUop;
  logic  io_out_5_bits_lastUop;
  logic [6:0] io_out_5_bits_numWB;
  logic [2:0] io_out_5_bits_commitType;
  logic  io_intRat_0_0_hold;
  logic [31:0] io_intRat_0_0_addr;
  logic  io_intRat_0_1_hold;
  logic [31:0] io_intRat_0_1_addr;
  logic  io_intRat_1_0_hold;
  logic [31:0] io_intRat_1_0_addr;
  logic  io_intRat_1_1_hold;
  logic [31:0] io_intRat_1_1_addr;
  logic  io_intRat_2_0_hold;
  logic [31:0] io_intRat_2_0_addr;
  logic  io_intRat_2_1_hold;
  logic [31:0] io_intRat_2_1_addr;
  logic  io_intRat_3_0_hold;
  logic [31:0] io_intRat_3_0_addr;
  logic  io_intRat_3_1_hold;
  logic [31:0] io_intRat_3_1_addr;
  logic  io_intRat_4_0_hold;
  logic [31:0] io_intRat_4_0_addr;
  logic  io_intRat_4_1_hold;
  logic [31:0] io_intRat_4_1_addr;
  logic  io_intRat_5_0_hold;
  logic [31:0] io_intRat_5_0_addr;
  logic  io_intRat_5_1_hold;
  logic [31:0] io_intRat_5_1_addr;
  logic  io_fpRat_0_0_hold;
  logic [33:0] io_fpRat_0_0_addr;
  logic  io_fpRat_0_1_hold;
  logic [33:0] io_fpRat_0_1_addr;
  logic  io_fpRat_0_2_hold;
  logic [33:0] io_fpRat_0_2_addr;
  logic  io_fpRat_1_0_hold;
  logic [33:0] io_fpRat_1_0_addr;
  logic  io_fpRat_1_1_hold;
  logic [33:0] io_fpRat_1_1_addr;
  logic  io_fpRat_1_2_hold;
  logic [33:0] io_fpRat_1_2_addr;
  logic  io_fpRat_2_0_hold;
  logic [33:0] io_fpRat_2_0_addr;
  logic  io_fpRat_2_1_hold;
  logic [33:0] io_fpRat_2_1_addr;
  logic  io_fpRat_2_2_hold;
  logic [33:0] io_fpRat_2_2_addr;
  logic  io_fpRat_3_0_hold;
  logic [33:0] io_fpRat_3_0_addr;
  logic  io_fpRat_3_1_hold;
  logic [33:0] io_fpRat_3_1_addr;
  logic  io_fpRat_3_2_hold;
  logic [33:0] io_fpRat_3_2_addr;
  logic  io_fpRat_4_0_hold;
  logic [33:0] io_fpRat_4_0_addr;
  logic  io_fpRat_4_1_hold;
  logic [33:0] io_fpRat_4_1_addr;
  logic  io_fpRat_4_2_hold;
  logic [33:0] io_fpRat_4_2_addr;
  logic  io_fpRat_5_0_hold;
  logic [33:0] io_fpRat_5_0_addr;
  logic  io_fpRat_5_1_hold;
  logic [33:0] io_fpRat_5_1_addr;
  logic  io_fpRat_5_2_hold;
  logic [33:0] io_fpRat_5_2_addr;
  logic  io_vecRat_0_0_hold;
  logic [46:0] io_vecRat_0_0_addr;
  logic  io_vecRat_0_1_hold;
  logic [46:0] io_vecRat_0_1_addr;
  logic  io_vecRat_0_2_hold;
  logic [46:0] io_vecRat_0_2_addr;
  logic  io_vecRat_1_0_hold;
  logic [46:0] io_vecRat_1_0_addr;
  logic  io_vecRat_1_1_hold;
  logic [46:0] io_vecRat_1_1_addr;
  logic  io_vecRat_1_2_hold;
  logic [46:0] io_vecRat_1_2_addr;
  logic  io_vecRat_2_0_hold;
  logic [46:0] io_vecRat_2_0_addr;
  logic  io_vecRat_2_1_hold;
  logic [46:0] io_vecRat_2_1_addr;
  logic  io_vecRat_2_2_hold;
  logic [46:0] io_vecRat_2_2_addr;
  logic  io_vecRat_3_0_hold;
  logic [46:0] io_vecRat_3_0_addr;
  logic  io_vecRat_3_1_hold;
  logic [46:0] io_vecRat_3_1_addr;
  logic  io_vecRat_3_2_hold;
  logic [46:0] io_vecRat_3_2_addr;
  logic  io_vecRat_4_0_hold;
  logic [46:0] io_vecRat_4_0_addr;
  logic  io_vecRat_4_1_hold;
  logic [46:0] io_vecRat_4_1_addr;
  logic  io_vecRat_4_2_hold;
  logic [46:0] io_vecRat_4_2_addr;
  logic  io_vecRat_5_0_hold;
  logic [46:0] io_vecRat_5_0_addr;
  logic  io_vecRat_5_1_hold;
  logic [46:0] io_vecRat_5_1_addr;
  logic  io_vecRat_5_2_hold;
  logic [46:0] io_vecRat_5_2_addr;
  logic  io_csrCtrl_singlestep;
  logic  io_fromCSR_illegalInst_sfenceVMA;
  logic  io_fromCSR_illegalInst_sfencePart;
  logic  io_fromCSR_illegalInst_hfenceGVMA;
  logic  io_fromCSR_illegalInst_hfenceVVMA;
  logic  io_fromCSR_illegalInst_hlsv;
  logic  io_fromCSR_illegalInst_fsIsOff;
  logic  io_fromCSR_illegalInst_vsIsOff;
  logic  io_fromCSR_illegalInst_wfi;
  logic  io_fromCSR_illegalInst_frm;
  logic  io_fromCSR_illegalInst_cboZ;
  logic  io_fromCSR_illegalInst_cboCF;
  logic  io_fromCSR_illegalInst_cboI;
  logic  io_fromCSR_virtualInst_sfenceVMA;
  logic  io_fromCSR_virtualInst_sfencePart;
  logic  io_fromCSR_virtualInst_hfence;
  logic  io_fromCSR_virtualInst_hlsv;
  logic  io_fromCSR_virtualInst_wfi;
  logic  io_fromCSR_virtualInst_cboZ;
  logic  io_fromCSR_virtualInst_cboCF;
  logic  io_fromCSR_virtualInst_cboI;
  logic  io_fromCSR_special_cboI2F;
  logic  io_fusion_0;
  logic  io_fusion_1;
  logic  io_fusion_2;
  logic  io_fusion_3;
  logic  io_fusion_4;
  logic  io_fromRob_isResumeVType;
  logic  io_fromRob_walkToArchVType;
  logic  io_fromRob_commitVType_vtype_valid;
  logic  io_fromRob_commitVType_vtype_bits_illegal;
  logic  io_fromRob_commitVType_vtype_bits_vma;
  logic  io_fromRob_commitVType_vtype_bits_vta;
  logic [1:0] io_fromRob_commitVType_vtype_bits_vsew;
  logic [2:0] io_fromRob_commitVType_vtype_bits_vlmul;
  logic  io_fromRob_commitVType_hasVsetvl;
  logic  io_fromRob_walkVType_valid;
  logic  io_fromRob_walkVType_bits_illegal;
  logic  io_fromRob_walkVType_bits_vma;
  logic  io_fromRob_walkVType_bits_vta;
  logic [1:0] io_fromRob_walkVType_bits_vsew;
  logic [2:0] io_fromRob_walkVType_bits_vlmul;
  logic  io_vsetvlVType_illegal;
  logic  io_vsetvlVType_vma;
  logic  io_vsetvlVType_vta;
  logic [1:0] io_vsetvlVType_vsew;
  logic [2:0] io_vsetvlVType_vlmul;
  logic [7:0] io_vstart;
  logic  io_toCSR_trapInstInfo_valid;
  logic [31:0] io_toCSR_trapInstInfo_bits_instr;
  logic  io_toCSR_trapInstInfo_bits_ftqPtr_flag;
  logic [5:0] io_toCSR_trapInstInfo_bits_ftqPtr_value;
  logic [3:0] io_toCSR_trapInstInfo_bits_ftqOffset;
  logic [5:0] io_perf_0_value;
  logic [5:0] io_perf_1_value;
  logic [5:0] io_perf_2_value;
  logic [5:0] io_perf_3_value;


 DecodeStage DecodeStage(
    .clock(clock),
    .reset(reset),
    .io_redirect(io_redirect),
    .io_in_0_ready(io_in_0_ready),
    .io_in_0_valid(io_in_0_valid),
    .io_in_0_bits_instr(io_in_0_bits_instr),
    .io_in_0_bits_exceptionVec_0(io_in_0_bits_exceptionVec_0),
    .io_in_0_bits_exceptionVec_1(io_in_0_bits_exceptionVec_1),
    .io_in_0_bits_exceptionVec_2(io_in_0_bits_exceptionVec_2),
    .io_in_0_bits_exceptionVec_4(io_in_0_bits_exceptionVec_4),
    .io_in_0_bits_exceptionVec_5(io_in_0_bits_exceptionVec_5),
    .io_in_0_bits_exceptionVec_6(io_in_0_bits_exceptionVec_6),
    .io_in_0_bits_exceptionVec_7(io_in_0_bits_exceptionVec_7),
    .io_in_0_bits_exceptionVec_8(io_in_0_bits_exceptionVec_8),
    .io_in_0_bits_exceptionVec_9(io_in_0_bits_exceptionVec_9),
    .io_in_0_bits_exceptionVec_10(io_in_0_bits_exceptionVec_10),
    .io_in_0_bits_exceptionVec_11(io_in_0_bits_exceptionVec_11),
    .io_in_0_bits_exceptionVec_12(io_in_0_bits_exceptionVec_12),
    .io_in_0_bits_exceptionVec_13(io_in_0_bits_exceptionVec_13),
    .io_in_0_bits_exceptionVec_14(io_in_0_bits_exceptionVec_14),
    .io_in_0_bits_exceptionVec_15(io_in_0_bits_exceptionVec_15),
    .io_in_0_bits_exceptionVec_16(io_in_0_bits_exceptionVec_16),
    .io_in_0_bits_exceptionVec_17(io_in_0_bits_exceptionVec_17),
    .io_in_0_bits_exceptionVec_18(io_in_0_bits_exceptionVec_18),
    .io_in_0_bits_exceptionVec_19(io_in_0_bits_exceptionVec_19),
    .io_in_0_bits_exceptionVec_20(io_in_0_bits_exceptionVec_20),
    .io_in_0_bits_exceptionVec_21(io_in_0_bits_exceptionVec_21),
    .io_in_0_bits_exceptionVec_23(io_in_0_bits_exceptionVec_23),
    .io_in_0_bits_isFetchMalAddr(io_in_0_bits_isFetchMalAddr),
    .io_in_0_bits_trigger(io_in_0_bits_trigger),
    .io_in_0_bits_preDecodeInfo_isRVC(io_in_0_bits_preDecodeInfo_isRVC),
    .io_in_0_bits_preDecodeInfo_brType(io_in_0_bits_preDecodeInfo_brType),
    .io_in_0_bits_pred_taken(io_in_0_bits_pred_taken),
    .io_in_0_bits_crossPageIPFFix(io_in_0_bits_crossPageIPFFix),
    .io_in_0_bits_ftqPtr_flag(io_in_0_bits_ftqPtr_flag),
    .io_in_0_bits_ftqPtr_value(io_in_0_bits_ftqPtr_value),
    .io_in_0_bits_ftqOffset(io_in_0_bits_ftqOffset),
    .io_in_0_bits_isLastInFtqEntry(io_in_0_bits_isLastInFtqEntry),
    .io_in_1_ready(io_in_1_ready),
    .io_in_1_valid(io_in_1_valid),
    .io_in_1_bits_instr(io_in_1_bits_instr),
    .io_in_1_bits_exceptionVec_0(io_in_1_bits_exceptionVec_0),
    .io_in_1_bits_exceptionVec_1(io_in_1_bits_exceptionVec_1),
    .io_in_1_bits_exceptionVec_2(io_in_1_bits_exceptionVec_2),
    .io_in_1_bits_exceptionVec_4(io_in_1_bits_exceptionVec_4),
    .io_in_1_bits_exceptionVec_5(io_in_1_bits_exceptionVec_5),
    .io_in_1_bits_exceptionVec_6(io_in_1_bits_exceptionVec_6),
    .io_in_1_bits_exceptionVec_7(io_in_1_bits_exceptionVec_7),
    .io_in_1_bits_exceptionVec_8(io_in_1_bits_exceptionVec_8),
    .io_in_1_bits_exceptionVec_9(io_in_1_bits_exceptionVec_9),
    .io_in_1_bits_exceptionVec_10(io_in_1_bits_exceptionVec_10),
    .io_in_1_bits_exceptionVec_11(io_in_1_bits_exceptionVec_11),
    .io_in_1_bits_exceptionVec_12(io_in_1_bits_exceptionVec_12),
    .io_in_1_bits_exceptionVec_13(io_in_1_bits_exceptionVec_13),
    .io_in_1_bits_exceptionVec_14(io_in_1_bits_exceptionVec_14),
    .io_in_1_bits_exceptionVec_15(io_in_1_bits_exceptionVec_15),
    .io_in_1_bits_exceptionVec_16(io_in_1_bits_exceptionVec_16),
    .io_in_1_bits_exceptionVec_17(io_in_1_bits_exceptionVec_17),
    .io_in_1_bits_exceptionVec_18(io_in_1_bits_exceptionVec_18),
    .io_in_1_bits_exceptionVec_19(io_in_1_bits_exceptionVec_19),
    .io_in_1_bits_exceptionVec_20(io_in_1_bits_exceptionVec_20),
    .io_in_1_bits_exceptionVec_21(io_in_1_bits_exceptionVec_21),
    .io_in_1_bits_exceptionVec_23(io_in_1_bits_exceptionVec_23),
    .io_in_1_bits_isFetchMalAddr(io_in_1_bits_isFetchMalAddr),
    .io_in_1_bits_trigger(io_in_1_bits_trigger),
    .io_in_1_bits_preDecodeInfo_isRVC(io_in_1_bits_preDecodeInfo_isRVC),
    .io_in_1_bits_preDecodeInfo_brType(io_in_1_bits_preDecodeInfo_brType),
    .io_in_1_bits_pred_taken(io_in_1_bits_pred_taken),
    .io_in_1_bits_crossPageIPFFix(io_in_1_bits_crossPageIPFFix),
    .io_in_1_bits_ftqPtr_flag(io_in_1_bits_ftqPtr_flag),
    .io_in_1_bits_ftqPtr_value(io_in_1_bits_ftqPtr_value),
    .io_in_1_bits_ftqOffset(io_in_1_bits_ftqOffset),
    .io_in_1_bits_isLastInFtqEntry(io_in_1_bits_isLastInFtqEntry),
    .io_in_2_ready(io_in_2_ready),
    .io_in_2_valid(io_in_2_valid),
    .io_in_2_bits_instr(io_in_2_bits_instr),
    .io_in_2_bits_exceptionVec_0(io_in_2_bits_exceptionVec_0),
    .io_in_2_bits_exceptionVec_1(io_in_2_bits_exceptionVec_1),
    .io_in_2_bits_exceptionVec_2(io_in_2_bits_exceptionVec_2),
    .io_in_2_bits_exceptionVec_4(io_in_2_bits_exceptionVec_4),
    .io_in_2_bits_exceptionVec_5(io_in_2_bits_exceptionVec_5),
    .io_in_2_bits_exceptionVec_6(io_in_2_bits_exceptionVec_6),
    .io_in_2_bits_exceptionVec_7(io_in_2_bits_exceptionVec_7),
    .io_in_2_bits_exceptionVec_8(io_in_2_bits_exceptionVec_8),
    .io_in_2_bits_exceptionVec_9(io_in_2_bits_exceptionVec_9),
    .io_in_2_bits_exceptionVec_10(io_in_2_bits_exceptionVec_10),
    .io_in_2_bits_exceptionVec_11(io_in_2_bits_exceptionVec_11),
    .io_in_2_bits_exceptionVec_12(io_in_2_bits_exceptionVec_12),
    .io_in_2_bits_exceptionVec_13(io_in_2_bits_exceptionVec_13),
    .io_in_2_bits_exceptionVec_14(io_in_2_bits_exceptionVec_14),
    .io_in_2_bits_exceptionVec_15(io_in_2_bits_exceptionVec_15),
    .io_in_2_bits_exceptionVec_16(io_in_2_bits_exceptionVec_16),
    .io_in_2_bits_exceptionVec_17(io_in_2_bits_exceptionVec_17),
    .io_in_2_bits_exceptionVec_18(io_in_2_bits_exceptionVec_18),
    .io_in_2_bits_exceptionVec_19(io_in_2_bits_exceptionVec_19),
    .io_in_2_bits_exceptionVec_20(io_in_2_bits_exceptionVec_20),
    .io_in_2_bits_exceptionVec_21(io_in_2_bits_exceptionVec_21),
    .io_in_2_bits_exceptionVec_23(io_in_2_bits_exceptionVec_23),
    .io_in_2_bits_isFetchMalAddr(io_in_2_bits_isFetchMalAddr),
    .io_in_2_bits_trigger(io_in_2_bits_trigger),
    .io_in_2_bits_preDecodeInfo_isRVC(io_in_2_bits_preDecodeInfo_isRVC),
    .io_in_2_bits_preDecodeInfo_brType(io_in_2_bits_preDecodeInfo_brType),
    .io_in_2_bits_pred_taken(io_in_2_bits_pred_taken),
    .io_in_2_bits_crossPageIPFFix(io_in_2_bits_crossPageIPFFix),
    .io_in_2_bits_ftqPtr_flag(io_in_2_bits_ftqPtr_flag),
    .io_in_2_bits_ftqPtr_value(io_in_2_bits_ftqPtr_value),
    .io_in_2_bits_ftqOffset(io_in_2_bits_ftqOffset),
    .io_in_2_bits_isLastInFtqEntry(io_in_2_bits_isLastInFtqEntry),
    .io_in_3_ready(io_in_3_ready),
    .io_in_3_valid(io_in_3_valid),
    .io_in_3_bits_instr(io_in_3_bits_instr),
    .io_in_3_bits_exceptionVec_0(io_in_3_bits_exceptionVec_0),
    .io_in_3_bits_exceptionVec_1(io_in_3_bits_exceptionVec_1),
    .io_in_3_bits_exceptionVec_2(io_in_3_bits_exceptionVec_2),
    .io_in_3_bits_exceptionVec_4(io_in_3_bits_exceptionVec_4),
    .io_in_3_bits_exceptionVec_5(io_in_3_bits_exceptionVec_5),
    .io_in_3_bits_exceptionVec_6(io_in_3_bits_exceptionVec_6),
    .io_in_3_bits_exceptionVec_7(io_in_3_bits_exceptionVec_7),
    .io_in_3_bits_exceptionVec_8(io_in_3_bits_exceptionVec_8),
    .io_in_3_bits_exceptionVec_9(io_in_3_bits_exceptionVec_9),
    .io_in_3_bits_exceptionVec_10(io_in_3_bits_exceptionVec_10),
    .io_in_3_bits_exceptionVec_11(io_in_3_bits_exceptionVec_11),
    .io_in_3_bits_exceptionVec_12(io_in_3_bits_exceptionVec_12),
    .io_in_3_bits_exceptionVec_13(io_in_3_bits_exceptionVec_13),
    .io_in_3_bits_exceptionVec_14(io_in_3_bits_exceptionVec_14),
    .io_in_3_bits_exceptionVec_15(io_in_3_bits_exceptionVec_15),
    .io_in_3_bits_exceptionVec_16(io_in_3_bits_exceptionVec_16),
    .io_in_3_bits_exceptionVec_17(io_in_3_bits_exceptionVec_17),
    .io_in_3_bits_exceptionVec_18(io_in_3_bits_exceptionVec_18),
    .io_in_3_bits_exceptionVec_19(io_in_3_bits_exceptionVec_19),
    .io_in_3_bits_exceptionVec_20(io_in_3_bits_exceptionVec_20),
    .io_in_3_bits_exceptionVec_21(io_in_3_bits_exceptionVec_21),
    .io_in_3_bits_exceptionVec_23(io_in_3_bits_exceptionVec_23),
    .io_in_3_bits_isFetchMalAddr(io_in_3_bits_isFetchMalAddr),
    .io_in_3_bits_trigger(io_in_3_bits_trigger),
    .io_in_3_bits_preDecodeInfo_isRVC(io_in_3_bits_preDecodeInfo_isRVC),
    .io_in_3_bits_preDecodeInfo_brType(io_in_3_bits_preDecodeInfo_brType),
    .io_in_3_bits_pred_taken(io_in_3_bits_pred_taken),
    .io_in_3_bits_crossPageIPFFix(io_in_3_bits_crossPageIPFFix),
    .io_in_3_bits_ftqPtr_flag(io_in_3_bits_ftqPtr_flag),
    .io_in_3_bits_ftqPtr_value(io_in_3_bits_ftqPtr_value),
    .io_in_3_bits_ftqOffset(io_in_3_bits_ftqOffset),
    .io_in_3_bits_isLastInFtqEntry(io_in_3_bits_isLastInFtqEntry),
    .io_in_4_ready(io_in_4_ready),
    .io_in_4_valid(io_in_4_valid),
    .io_in_4_bits_instr(io_in_4_bits_instr),
    .io_in_4_bits_exceptionVec_0(io_in_4_bits_exceptionVec_0),
    .io_in_4_bits_exceptionVec_1(io_in_4_bits_exceptionVec_1),
    .io_in_4_bits_exceptionVec_2(io_in_4_bits_exceptionVec_2),
    .io_in_4_bits_exceptionVec_4(io_in_4_bits_exceptionVec_4),
    .io_in_4_bits_exceptionVec_5(io_in_4_bits_exceptionVec_5),
    .io_in_4_bits_exceptionVec_6(io_in_4_bits_exceptionVec_6),
    .io_in_4_bits_exceptionVec_7(io_in_4_bits_exceptionVec_7),
    .io_in_4_bits_exceptionVec_8(io_in_4_bits_exceptionVec_8),
    .io_in_4_bits_exceptionVec_9(io_in_4_bits_exceptionVec_9),
    .io_in_4_bits_exceptionVec_10(io_in_4_bits_exceptionVec_10),
    .io_in_4_bits_exceptionVec_11(io_in_4_bits_exceptionVec_11),
    .io_in_4_bits_exceptionVec_12(io_in_4_bits_exceptionVec_12),
    .io_in_4_bits_exceptionVec_13(io_in_4_bits_exceptionVec_13),
    .io_in_4_bits_exceptionVec_14(io_in_4_bits_exceptionVec_14),
    .io_in_4_bits_exceptionVec_15(io_in_4_bits_exceptionVec_15),
    .io_in_4_bits_exceptionVec_16(io_in_4_bits_exceptionVec_16),
    .io_in_4_bits_exceptionVec_17(io_in_4_bits_exceptionVec_17),
    .io_in_4_bits_exceptionVec_18(io_in_4_bits_exceptionVec_18),
    .io_in_4_bits_exceptionVec_19(io_in_4_bits_exceptionVec_19),
    .io_in_4_bits_exceptionVec_20(io_in_4_bits_exceptionVec_20),
    .io_in_4_bits_exceptionVec_21(io_in_4_bits_exceptionVec_21),
    .io_in_4_bits_exceptionVec_23(io_in_4_bits_exceptionVec_23),
    .io_in_4_bits_isFetchMalAddr(io_in_4_bits_isFetchMalAddr),
    .io_in_4_bits_trigger(io_in_4_bits_trigger),
    .io_in_4_bits_preDecodeInfo_isRVC(io_in_4_bits_preDecodeInfo_isRVC),
    .io_in_4_bits_preDecodeInfo_brType(io_in_4_bits_preDecodeInfo_brType),
    .io_in_4_bits_pred_taken(io_in_4_bits_pred_taken),
    .io_in_4_bits_crossPageIPFFix(io_in_4_bits_crossPageIPFFix),
    .io_in_4_bits_ftqPtr_flag(io_in_4_bits_ftqPtr_flag),
    .io_in_4_bits_ftqPtr_value(io_in_4_bits_ftqPtr_value),
    .io_in_4_bits_ftqOffset(io_in_4_bits_ftqOffset),
    .io_in_4_bits_isLastInFtqEntry(io_in_4_bits_isLastInFtqEntry),
    .io_in_5_ready(io_in_5_ready),
    .io_in_5_valid(io_in_5_valid),
    .io_in_5_bits_instr(io_in_5_bits_instr),
    .io_in_5_bits_exceptionVec_0(io_in_5_bits_exceptionVec_0),
    .io_in_5_bits_exceptionVec_1(io_in_5_bits_exceptionVec_1),
    .io_in_5_bits_exceptionVec_2(io_in_5_bits_exceptionVec_2),
    .io_in_5_bits_exceptionVec_4(io_in_5_bits_exceptionVec_4),
    .io_in_5_bits_exceptionVec_5(io_in_5_bits_exceptionVec_5),
    .io_in_5_bits_exceptionVec_6(io_in_5_bits_exceptionVec_6),
    .io_in_5_bits_exceptionVec_7(io_in_5_bits_exceptionVec_7),
    .io_in_5_bits_exceptionVec_8(io_in_5_bits_exceptionVec_8),
    .io_in_5_bits_exceptionVec_9(io_in_5_bits_exceptionVec_9),
    .io_in_5_bits_exceptionVec_10(io_in_5_bits_exceptionVec_10),
    .io_in_5_bits_exceptionVec_11(io_in_5_bits_exceptionVec_11),
    .io_in_5_bits_exceptionVec_12(io_in_5_bits_exceptionVec_12),
    .io_in_5_bits_exceptionVec_13(io_in_5_bits_exceptionVec_13),
    .io_in_5_bits_exceptionVec_14(io_in_5_bits_exceptionVec_14),
    .io_in_5_bits_exceptionVec_15(io_in_5_bits_exceptionVec_15),
    .io_in_5_bits_exceptionVec_16(io_in_5_bits_exceptionVec_16),
    .io_in_5_bits_exceptionVec_17(io_in_5_bits_exceptionVec_17),
    .io_in_5_bits_exceptionVec_18(io_in_5_bits_exceptionVec_18),
    .io_in_5_bits_exceptionVec_19(io_in_5_bits_exceptionVec_19),
    .io_in_5_bits_exceptionVec_20(io_in_5_bits_exceptionVec_20),
    .io_in_5_bits_exceptionVec_21(io_in_5_bits_exceptionVec_21),
    .io_in_5_bits_exceptionVec_23(io_in_5_bits_exceptionVec_23),
    .io_in_5_bits_isFetchMalAddr(io_in_5_bits_isFetchMalAddr),
    .io_in_5_bits_trigger(io_in_5_bits_trigger),
    .io_in_5_bits_preDecodeInfo_isRVC(io_in_5_bits_preDecodeInfo_isRVC),
    .io_in_5_bits_preDecodeInfo_brType(io_in_5_bits_preDecodeInfo_brType),
    .io_in_5_bits_pred_taken(io_in_5_bits_pred_taken),
    .io_in_5_bits_crossPageIPFFix(io_in_5_bits_crossPageIPFFix),
    .io_in_5_bits_ftqPtr_flag(io_in_5_bits_ftqPtr_flag),
    .io_in_5_bits_ftqPtr_value(io_in_5_bits_ftqPtr_value),
    .io_in_5_bits_ftqOffset(io_in_5_bits_ftqOffset),
    .io_in_5_bits_isLastInFtqEntry(io_in_5_bits_isLastInFtqEntry),
    .io_out_0_ready(io_out_0_ready),
    .io_out_0_valid(io_out_0_valid),
    .io_out_0_bits_instr(io_out_0_bits_instr),
    .io_out_0_bits_exceptionVec_0(io_out_0_bits_exceptionVec_0),
    .io_out_0_bits_exceptionVec_1(io_out_0_bits_exceptionVec_1),
    .io_out_0_bits_exceptionVec_2(io_out_0_bits_exceptionVec_2),
    .io_out_0_bits_exceptionVec_3(io_out_0_bits_exceptionVec_3),
    .io_out_0_bits_exceptionVec_4(io_out_0_bits_exceptionVec_4),
    .io_out_0_bits_exceptionVec_5(io_out_0_bits_exceptionVec_5),
    .io_out_0_bits_exceptionVec_6(io_out_0_bits_exceptionVec_6),
    .io_out_0_bits_exceptionVec_7(io_out_0_bits_exceptionVec_7),
    .io_out_0_bits_exceptionVec_8(io_out_0_bits_exceptionVec_8),
    .io_out_0_bits_exceptionVec_9(io_out_0_bits_exceptionVec_9),
    .io_out_0_bits_exceptionVec_10(io_out_0_bits_exceptionVec_10),
    .io_out_0_bits_exceptionVec_11(io_out_0_bits_exceptionVec_11),
    .io_out_0_bits_exceptionVec_12(io_out_0_bits_exceptionVec_12),
    .io_out_0_bits_exceptionVec_13(io_out_0_bits_exceptionVec_13),
    .io_out_0_bits_exceptionVec_14(io_out_0_bits_exceptionVec_14),
    .io_out_0_bits_exceptionVec_15(io_out_0_bits_exceptionVec_15),
    .io_out_0_bits_exceptionVec_16(io_out_0_bits_exceptionVec_16),
    .io_out_0_bits_exceptionVec_17(io_out_0_bits_exceptionVec_17),
    .io_out_0_bits_exceptionVec_18(io_out_0_bits_exceptionVec_18),
    .io_out_0_bits_exceptionVec_19(io_out_0_bits_exceptionVec_19),
    .io_out_0_bits_exceptionVec_20(io_out_0_bits_exceptionVec_20),
    .io_out_0_bits_exceptionVec_21(io_out_0_bits_exceptionVec_21),
    .io_out_0_bits_exceptionVec_22(io_out_0_bits_exceptionVec_22),
    .io_out_0_bits_exceptionVec_23(io_out_0_bits_exceptionVec_23),
    .io_out_0_bits_isFetchMalAddr(io_out_0_bits_isFetchMalAddr),
    .io_out_0_bits_trigger(io_out_0_bits_trigger),
    .io_out_0_bits_preDecodeInfo_isRVC(io_out_0_bits_preDecodeInfo_isRVC),
    .io_out_0_bits_preDecodeInfo_brType(io_out_0_bits_preDecodeInfo_brType),
    .io_out_0_bits_pred_taken(io_out_0_bits_pred_taken),
    .io_out_0_bits_crossPageIPFFix(io_out_0_bits_crossPageIPFFix),
    .io_out_0_bits_ftqPtr_flag(io_out_0_bits_ftqPtr_flag),
    .io_out_0_bits_ftqPtr_value(io_out_0_bits_ftqPtr_value),
    .io_out_0_bits_ftqOffset(io_out_0_bits_ftqOffset),
    .io_out_0_bits_srcType_0(io_out_0_bits_srcType_0),
    .io_out_0_bits_srcType_1(io_out_0_bits_srcType_1),
    .io_out_0_bits_srcType_2(io_out_0_bits_srcType_2),
    .io_out_0_bits_srcType_3(io_out_0_bits_srcType_3),
    .io_out_0_bits_srcType_4(io_out_0_bits_srcType_4),
    .io_out_0_bits_lsrc_0(io_out_0_bits_lsrc_0),
    .io_out_0_bits_lsrc_1(io_out_0_bits_lsrc_1),
    .io_out_0_bits_lsrc_2(io_out_0_bits_lsrc_2),
    .io_out_0_bits_ldest(io_out_0_bits_ldest),
    .io_out_0_bits_fuType(io_out_0_bits_fuType),
    .io_out_0_bits_fuOpType(io_out_0_bits_fuOpType),
    .io_out_0_bits_rfWen(io_out_0_bits_rfWen),
    .io_out_0_bits_fpWen(io_out_0_bits_fpWen),
    .io_out_0_bits_vecWen(io_out_0_bits_vecWen),
    .io_out_0_bits_v0Wen(io_out_0_bits_v0Wen),
    .io_out_0_bits_vlWen(io_out_0_bits_vlWen),
    .io_out_0_bits_isXSTrap(io_out_0_bits_isXSTrap),
    .io_out_0_bits_waitForward(io_out_0_bits_waitForward),
    .io_out_0_bits_blockBackward(io_out_0_bits_blockBackward),
    .io_out_0_bits_flushPipe(io_out_0_bits_flushPipe),
    .io_out_0_bits_canRobCompress(io_out_0_bits_canRobCompress),
    .io_out_0_bits_selImm(io_out_0_bits_selImm),
    .io_out_0_bits_imm(io_out_0_bits_imm),
    .io_out_0_bits_fpu_typeTagOut(io_out_0_bits_fpu_typeTagOut),
    .io_out_0_bits_fpu_wflags(io_out_0_bits_fpu_wflags),
    .io_out_0_bits_fpu_typ(io_out_0_bits_fpu_typ),
    .io_out_0_bits_fpu_fmt(io_out_0_bits_fpu_fmt),
    .io_out_0_bits_fpu_rm(io_out_0_bits_fpu_rm),
    .io_out_0_bits_vpu_vill(io_out_0_bits_vpu_vill),
    .io_out_0_bits_vpu_vma(io_out_0_bits_vpu_vma),
    .io_out_0_bits_vpu_vta(io_out_0_bits_vpu_vta),
    .io_out_0_bits_vpu_vsew(io_out_0_bits_vpu_vsew),
    .io_out_0_bits_vpu_vlmul(io_out_0_bits_vpu_vlmul),
    .io_out_0_bits_vpu_specVill(io_out_0_bits_vpu_specVill),
    .io_out_0_bits_vpu_specVma(io_out_0_bits_vpu_specVma),
    .io_out_0_bits_vpu_specVta(io_out_0_bits_vpu_specVta),
    .io_out_0_bits_vpu_specVsew(io_out_0_bits_vpu_specVsew),
    .io_out_0_bits_vpu_specVlmul(io_out_0_bits_vpu_specVlmul),
    .io_out_0_bits_vpu_vm(io_out_0_bits_vpu_vm),
    .io_out_0_bits_vpu_vstart(io_out_0_bits_vpu_vstart),
    .io_out_0_bits_vpu_fpu_isFoldTo1_2(io_out_0_bits_vpu_fpu_isFoldTo1_2),
    .io_out_0_bits_vpu_fpu_isFoldTo1_4(io_out_0_bits_vpu_fpu_isFoldTo1_4),
    .io_out_0_bits_vpu_fpu_isFoldTo1_8(io_out_0_bits_vpu_fpu_isFoldTo1_8),
    .io_out_0_bits_vpu_nf(io_out_0_bits_vpu_nf),
    .io_out_0_bits_vpu_veew(io_out_0_bits_vpu_veew),
    .io_out_0_bits_vpu_isExt(io_out_0_bits_vpu_isExt),
    .io_out_0_bits_vpu_isNarrow(io_out_0_bits_vpu_isNarrow),
    .io_out_0_bits_vpu_isDstMask(io_out_0_bits_vpu_isDstMask),
    .io_out_0_bits_vpu_isOpMask(io_out_0_bits_vpu_isOpMask),
    .io_out_0_bits_vpu_isDependOldVd(io_out_0_bits_vpu_isDependOldVd),
    .io_out_0_bits_vpu_isWritePartVd(io_out_0_bits_vpu_isWritePartVd),
    .io_out_0_bits_vpu_isVleff(io_out_0_bits_vpu_isVleff),
    .io_out_0_bits_vlsInstr(io_out_0_bits_vlsInstr),
    .io_out_0_bits_wfflags(io_out_0_bits_wfflags),
    .io_out_0_bits_isMove(io_out_0_bits_isMove),
    .io_out_0_bits_uopIdx(io_out_0_bits_uopIdx),
    .io_out_0_bits_uopSplitType(io_out_0_bits_uopSplitType),
    .io_out_0_bits_isVset(io_out_0_bits_isVset),
    .io_out_0_bits_firstUop(io_out_0_bits_firstUop),
    .io_out_0_bits_lastUop(io_out_0_bits_lastUop),
    .io_out_0_bits_numWB(io_out_0_bits_numWB),
    .io_out_0_bits_commitType(io_out_0_bits_commitType),
    .io_out_1_ready(io_out_1_ready),
    .io_out_1_valid(io_out_1_valid),
    .io_out_1_bits_instr(io_out_1_bits_instr),
    .io_out_1_bits_exceptionVec_0(io_out_1_bits_exceptionVec_0),
    .io_out_1_bits_exceptionVec_1(io_out_1_bits_exceptionVec_1),
    .io_out_1_bits_exceptionVec_2(io_out_1_bits_exceptionVec_2),
    .io_out_1_bits_exceptionVec_3(io_out_1_bits_exceptionVec_3),
    .io_out_1_bits_exceptionVec_4(io_out_1_bits_exceptionVec_4),
    .io_out_1_bits_exceptionVec_5(io_out_1_bits_exceptionVec_5),
    .io_out_1_bits_exceptionVec_6(io_out_1_bits_exceptionVec_6),
    .io_out_1_bits_exceptionVec_7(io_out_1_bits_exceptionVec_7),
    .io_out_1_bits_exceptionVec_8(io_out_1_bits_exceptionVec_8),
    .io_out_1_bits_exceptionVec_9(io_out_1_bits_exceptionVec_9),
    .io_out_1_bits_exceptionVec_10(io_out_1_bits_exceptionVec_10),
    .io_out_1_bits_exceptionVec_11(io_out_1_bits_exceptionVec_11),
    .io_out_1_bits_exceptionVec_12(io_out_1_bits_exceptionVec_12),
    .io_out_1_bits_exceptionVec_13(io_out_1_bits_exceptionVec_13),
    .io_out_1_bits_exceptionVec_14(io_out_1_bits_exceptionVec_14),
    .io_out_1_bits_exceptionVec_15(io_out_1_bits_exceptionVec_15),
    .io_out_1_bits_exceptionVec_16(io_out_1_bits_exceptionVec_16),
    .io_out_1_bits_exceptionVec_17(io_out_1_bits_exceptionVec_17),
    .io_out_1_bits_exceptionVec_18(io_out_1_bits_exceptionVec_18),
    .io_out_1_bits_exceptionVec_19(io_out_1_bits_exceptionVec_19),
    .io_out_1_bits_exceptionVec_20(io_out_1_bits_exceptionVec_20),
    .io_out_1_bits_exceptionVec_21(io_out_1_bits_exceptionVec_21),
    .io_out_1_bits_exceptionVec_22(io_out_1_bits_exceptionVec_22),
    .io_out_1_bits_exceptionVec_23(io_out_1_bits_exceptionVec_23),
    .io_out_1_bits_isFetchMalAddr(io_out_1_bits_isFetchMalAddr),
    .io_out_1_bits_trigger(io_out_1_bits_trigger),
    .io_out_1_bits_preDecodeInfo_isRVC(io_out_1_bits_preDecodeInfo_isRVC),
    .io_out_1_bits_preDecodeInfo_brType(io_out_1_bits_preDecodeInfo_brType),
    .io_out_1_bits_pred_taken(io_out_1_bits_pred_taken),
    .io_out_1_bits_crossPageIPFFix(io_out_1_bits_crossPageIPFFix),
    .io_out_1_bits_ftqPtr_flag(io_out_1_bits_ftqPtr_flag),
    .io_out_1_bits_ftqPtr_value(io_out_1_bits_ftqPtr_value),
    .io_out_1_bits_ftqOffset(io_out_1_bits_ftqOffset),
    .io_out_1_bits_srcType_0(io_out_1_bits_srcType_0),
    .io_out_1_bits_srcType_1(io_out_1_bits_srcType_1),
    .io_out_1_bits_srcType_2(io_out_1_bits_srcType_2),
    .io_out_1_bits_srcType_3(io_out_1_bits_srcType_3),
    .io_out_1_bits_srcType_4(io_out_1_bits_srcType_4),
    .io_out_1_bits_lsrc_0(io_out_1_bits_lsrc_0),
    .io_out_1_bits_lsrc_1(io_out_1_bits_lsrc_1),
    .io_out_1_bits_lsrc_2(io_out_1_bits_lsrc_2),
    .io_out_1_bits_ldest(io_out_1_bits_ldest),
    .io_out_1_bits_fuType(io_out_1_bits_fuType),
    .io_out_1_bits_fuOpType(io_out_1_bits_fuOpType),
    .io_out_1_bits_rfWen(io_out_1_bits_rfWen),
    .io_out_1_bits_fpWen(io_out_1_bits_fpWen),
    .io_out_1_bits_vecWen(io_out_1_bits_vecWen),
    .io_out_1_bits_v0Wen(io_out_1_bits_v0Wen),
    .io_out_1_bits_vlWen(io_out_1_bits_vlWen),
    .io_out_1_bits_isXSTrap(io_out_1_bits_isXSTrap),
    .io_out_1_bits_waitForward(io_out_1_bits_waitForward),
    .io_out_1_bits_blockBackward(io_out_1_bits_blockBackward),
    .io_out_1_bits_flushPipe(io_out_1_bits_flushPipe),
    .io_out_1_bits_canRobCompress(io_out_1_bits_canRobCompress),
    .io_out_1_bits_selImm(io_out_1_bits_selImm),
    .io_out_1_bits_imm(io_out_1_bits_imm),
    .io_out_1_bits_fpu_typeTagOut(io_out_1_bits_fpu_typeTagOut),
    .io_out_1_bits_fpu_wflags(io_out_1_bits_fpu_wflags),
    .io_out_1_bits_fpu_typ(io_out_1_bits_fpu_typ),
    .io_out_1_bits_fpu_fmt(io_out_1_bits_fpu_fmt),
    .io_out_1_bits_fpu_rm(io_out_1_bits_fpu_rm),
    .io_out_1_bits_vpu_vill(io_out_1_bits_vpu_vill),
    .io_out_1_bits_vpu_vma(io_out_1_bits_vpu_vma),
    .io_out_1_bits_vpu_vta(io_out_1_bits_vpu_vta),
    .io_out_1_bits_vpu_vsew(io_out_1_bits_vpu_vsew),
    .io_out_1_bits_vpu_vlmul(io_out_1_bits_vpu_vlmul),
    .io_out_1_bits_vpu_specVill(io_out_1_bits_vpu_specVill),
    .io_out_1_bits_vpu_specVma(io_out_1_bits_vpu_specVma),
    .io_out_1_bits_vpu_specVta(io_out_1_bits_vpu_specVta),
    .io_out_1_bits_vpu_specVsew(io_out_1_bits_vpu_specVsew),
    .io_out_1_bits_vpu_specVlmul(io_out_1_bits_vpu_specVlmul),
    .io_out_1_bits_vpu_vm(io_out_1_bits_vpu_vm),
    .io_out_1_bits_vpu_vstart(io_out_1_bits_vpu_vstart),
    .io_out_1_bits_vpu_fpu_isFoldTo1_2(io_out_1_bits_vpu_fpu_isFoldTo1_2),
    .io_out_1_bits_vpu_fpu_isFoldTo1_4(io_out_1_bits_vpu_fpu_isFoldTo1_4),
    .io_out_1_bits_vpu_fpu_isFoldTo1_8(io_out_1_bits_vpu_fpu_isFoldTo1_8),
    .io_out_1_bits_vpu_nf(io_out_1_bits_vpu_nf),
    .io_out_1_bits_vpu_veew(io_out_1_bits_vpu_veew),
    .io_out_1_bits_vpu_isExt(io_out_1_bits_vpu_isExt),
    .io_out_1_bits_vpu_isNarrow(io_out_1_bits_vpu_isNarrow),
    .io_out_1_bits_vpu_isDstMask(io_out_1_bits_vpu_isDstMask),
    .io_out_1_bits_vpu_isOpMask(io_out_1_bits_vpu_isOpMask),
    .io_out_1_bits_vpu_isDependOldVd(io_out_1_bits_vpu_isDependOldVd),
    .io_out_1_bits_vpu_isWritePartVd(io_out_1_bits_vpu_isWritePartVd),
    .io_out_1_bits_vpu_isVleff(io_out_1_bits_vpu_isVleff),
    .io_out_1_bits_vlsInstr(io_out_1_bits_vlsInstr),
    .io_out_1_bits_wfflags(io_out_1_bits_wfflags),
    .io_out_1_bits_isMove(io_out_1_bits_isMove),
    .io_out_1_bits_uopIdx(io_out_1_bits_uopIdx),
    .io_out_1_bits_uopSplitType(io_out_1_bits_uopSplitType),
    .io_out_1_bits_isVset(io_out_1_bits_isVset),
    .io_out_1_bits_firstUop(io_out_1_bits_firstUop),
    .io_out_1_bits_lastUop(io_out_1_bits_lastUop),
    .io_out_1_bits_numWB(io_out_1_bits_numWB),
    .io_out_1_bits_commitType(io_out_1_bits_commitType),
    .io_out_2_ready(io_out_2_ready),
    .io_out_2_valid(io_out_2_valid),
    .io_out_2_bits_instr(io_out_2_bits_instr),
    .io_out_2_bits_exceptionVec_0(io_out_2_bits_exceptionVec_0),
    .io_out_2_bits_exceptionVec_1(io_out_2_bits_exceptionVec_1),
    .io_out_2_bits_exceptionVec_2(io_out_2_bits_exceptionVec_2),
    .io_out_2_bits_exceptionVec_3(io_out_2_bits_exceptionVec_3),
    .io_out_2_bits_exceptionVec_4(io_out_2_bits_exceptionVec_4),
    .io_out_2_bits_exceptionVec_5(io_out_2_bits_exceptionVec_5),
    .io_out_2_bits_exceptionVec_6(io_out_2_bits_exceptionVec_6),
    .io_out_2_bits_exceptionVec_7(io_out_2_bits_exceptionVec_7),
    .io_out_2_bits_exceptionVec_8(io_out_2_bits_exceptionVec_8),
    .io_out_2_bits_exceptionVec_9(io_out_2_bits_exceptionVec_9),
    .io_out_2_bits_exceptionVec_10(io_out_2_bits_exceptionVec_10),
    .io_out_2_bits_exceptionVec_11(io_out_2_bits_exceptionVec_11),
    .io_out_2_bits_exceptionVec_12(io_out_2_bits_exceptionVec_12),
    .io_out_2_bits_exceptionVec_13(io_out_2_bits_exceptionVec_13),
    .io_out_2_bits_exceptionVec_14(io_out_2_bits_exceptionVec_14),
    .io_out_2_bits_exceptionVec_15(io_out_2_bits_exceptionVec_15),
    .io_out_2_bits_exceptionVec_16(io_out_2_bits_exceptionVec_16),
    .io_out_2_bits_exceptionVec_17(io_out_2_bits_exceptionVec_17),
    .io_out_2_bits_exceptionVec_18(io_out_2_bits_exceptionVec_18),
    .io_out_2_bits_exceptionVec_19(io_out_2_bits_exceptionVec_19),
    .io_out_2_bits_exceptionVec_20(io_out_2_bits_exceptionVec_20),
    .io_out_2_bits_exceptionVec_21(io_out_2_bits_exceptionVec_21),
    .io_out_2_bits_exceptionVec_22(io_out_2_bits_exceptionVec_22),
    .io_out_2_bits_exceptionVec_23(io_out_2_bits_exceptionVec_23),
    .io_out_2_bits_isFetchMalAddr(io_out_2_bits_isFetchMalAddr),
    .io_out_2_bits_trigger(io_out_2_bits_trigger),
    .io_out_2_bits_preDecodeInfo_isRVC(io_out_2_bits_preDecodeInfo_isRVC),
    .io_out_2_bits_preDecodeInfo_brType(io_out_2_bits_preDecodeInfo_brType),
    .io_out_2_bits_pred_taken(io_out_2_bits_pred_taken),
    .io_out_2_bits_crossPageIPFFix(io_out_2_bits_crossPageIPFFix),
    .io_out_2_bits_ftqPtr_flag(io_out_2_bits_ftqPtr_flag),
    .io_out_2_bits_ftqPtr_value(io_out_2_bits_ftqPtr_value),
    .io_out_2_bits_ftqOffset(io_out_2_bits_ftqOffset),
    .io_out_2_bits_srcType_0(io_out_2_bits_srcType_0),
    .io_out_2_bits_srcType_1(io_out_2_bits_srcType_1),
    .io_out_2_bits_srcType_2(io_out_2_bits_srcType_2),
    .io_out_2_bits_srcType_3(io_out_2_bits_srcType_3),
    .io_out_2_bits_srcType_4(io_out_2_bits_srcType_4),
    .io_out_2_bits_lsrc_0(io_out_2_bits_lsrc_0),
    .io_out_2_bits_lsrc_1(io_out_2_bits_lsrc_1),
    .io_out_2_bits_lsrc_2(io_out_2_bits_lsrc_2),
    .io_out_2_bits_ldest(io_out_2_bits_ldest),
    .io_out_2_bits_fuType(io_out_2_bits_fuType),
    .io_out_2_bits_fuOpType(io_out_2_bits_fuOpType),
    .io_out_2_bits_rfWen(io_out_2_bits_rfWen),
    .io_out_2_bits_fpWen(io_out_2_bits_fpWen),
    .io_out_2_bits_vecWen(io_out_2_bits_vecWen),
    .io_out_2_bits_v0Wen(io_out_2_bits_v0Wen),
    .io_out_2_bits_vlWen(io_out_2_bits_vlWen),
    .io_out_2_bits_isXSTrap(io_out_2_bits_isXSTrap),
    .io_out_2_bits_waitForward(io_out_2_bits_waitForward),
    .io_out_2_bits_blockBackward(io_out_2_bits_blockBackward),
    .io_out_2_bits_flushPipe(io_out_2_bits_flushPipe),
    .io_out_2_bits_canRobCompress(io_out_2_bits_canRobCompress),
    .io_out_2_bits_selImm(io_out_2_bits_selImm),
    .io_out_2_bits_imm(io_out_2_bits_imm),
    .io_out_2_bits_fpu_typeTagOut(io_out_2_bits_fpu_typeTagOut),
    .io_out_2_bits_fpu_wflags(io_out_2_bits_fpu_wflags),
    .io_out_2_bits_fpu_typ(io_out_2_bits_fpu_typ),
    .io_out_2_bits_fpu_fmt(io_out_2_bits_fpu_fmt),
    .io_out_2_bits_fpu_rm(io_out_2_bits_fpu_rm),
    .io_out_2_bits_vpu_vill(io_out_2_bits_vpu_vill),
    .io_out_2_bits_vpu_vma(io_out_2_bits_vpu_vma),
    .io_out_2_bits_vpu_vta(io_out_2_bits_vpu_vta),
    .io_out_2_bits_vpu_vsew(io_out_2_bits_vpu_vsew),
    .io_out_2_bits_vpu_vlmul(io_out_2_bits_vpu_vlmul),
    .io_out_2_bits_vpu_specVill(io_out_2_bits_vpu_specVill),
    .io_out_2_bits_vpu_specVma(io_out_2_bits_vpu_specVma),
    .io_out_2_bits_vpu_specVta(io_out_2_bits_vpu_specVta),
    .io_out_2_bits_vpu_specVsew(io_out_2_bits_vpu_specVsew),
    .io_out_2_bits_vpu_specVlmul(io_out_2_bits_vpu_specVlmul),
    .io_out_2_bits_vpu_vm(io_out_2_bits_vpu_vm),
    .io_out_2_bits_vpu_vstart(io_out_2_bits_vpu_vstart),
    .io_out_2_bits_vpu_fpu_isFoldTo1_2(io_out_2_bits_vpu_fpu_isFoldTo1_2),
    .io_out_2_bits_vpu_fpu_isFoldTo1_4(io_out_2_bits_vpu_fpu_isFoldTo1_4),
    .io_out_2_bits_vpu_fpu_isFoldTo1_8(io_out_2_bits_vpu_fpu_isFoldTo1_8),
    .io_out_2_bits_vpu_nf(io_out_2_bits_vpu_nf),
    .io_out_2_bits_vpu_veew(io_out_2_bits_vpu_veew),
    .io_out_2_bits_vpu_isExt(io_out_2_bits_vpu_isExt),
    .io_out_2_bits_vpu_isNarrow(io_out_2_bits_vpu_isNarrow),
    .io_out_2_bits_vpu_isDstMask(io_out_2_bits_vpu_isDstMask),
    .io_out_2_bits_vpu_isOpMask(io_out_2_bits_vpu_isOpMask),
    .io_out_2_bits_vpu_isDependOldVd(io_out_2_bits_vpu_isDependOldVd),
    .io_out_2_bits_vpu_isWritePartVd(io_out_2_bits_vpu_isWritePartVd),
    .io_out_2_bits_vpu_isVleff(io_out_2_bits_vpu_isVleff),
    .io_out_2_bits_vlsInstr(io_out_2_bits_vlsInstr),
    .io_out_2_bits_wfflags(io_out_2_bits_wfflags),
    .io_out_2_bits_isMove(io_out_2_bits_isMove),
    .io_out_2_bits_uopIdx(io_out_2_bits_uopIdx),
    .io_out_2_bits_uopSplitType(io_out_2_bits_uopSplitType),
    .io_out_2_bits_isVset(io_out_2_bits_isVset),
    .io_out_2_bits_firstUop(io_out_2_bits_firstUop),
    .io_out_2_bits_lastUop(io_out_2_bits_lastUop),
    .io_out_2_bits_numWB(io_out_2_bits_numWB),
    .io_out_2_bits_commitType(io_out_2_bits_commitType),
    .io_out_3_ready(io_out_3_ready),
    .io_out_3_valid(io_out_3_valid),
    .io_out_3_bits_instr(io_out_3_bits_instr),
    .io_out_3_bits_exceptionVec_0(io_out_3_bits_exceptionVec_0),
    .io_out_3_bits_exceptionVec_1(io_out_3_bits_exceptionVec_1),
    .io_out_3_bits_exceptionVec_2(io_out_3_bits_exceptionVec_2),
    .io_out_3_bits_exceptionVec_3(io_out_3_bits_exceptionVec_3),
    .io_out_3_bits_exceptionVec_4(io_out_3_bits_exceptionVec_4),
    .io_out_3_bits_exceptionVec_5(io_out_3_bits_exceptionVec_5),
    .io_out_3_bits_exceptionVec_6(io_out_3_bits_exceptionVec_6),
    .io_out_3_bits_exceptionVec_7(io_out_3_bits_exceptionVec_7),
    .io_out_3_bits_exceptionVec_8(io_out_3_bits_exceptionVec_8),
    .io_out_3_bits_exceptionVec_9(io_out_3_bits_exceptionVec_9),
    .io_out_3_bits_exceptionVec_10(io_out_3_bits_exceptionVec_10),
    .io_out_3_bits_exceptionVec_11(io_out_3_bits_exceptionVec_11),
    .io_out_3_bits_exceptionVec_12(io_out_3_bits_exceptionVec_12),
    .io_out_3_bits_exceptionVec_13(io_out_3_bits_exceptionVec_13),
    .io_out_3_bits_exceptionVec_14(io_out_3_bits_exceptionVec_14),
    .io_out_3_bits_exceptionVec_15(io_out_3_bits_exceptionVec_15),
    .io_out_3_bits_exceptionVec_16(io_out_3_bits_exceptionVec_16),
    .io_out_3_bits_exceptionVec_17(io_out_3_bits_exceptionVec_17),
    .io_out_3_bits_exceptionVec_18(io_out_3_bits_exceptionVec_18),
    .io_out_3_bits_exceptionVec_19(io_out_3_bits_exceptionVec_19),
    .io_out_3_bits_exceptionVec_20(io_out_3_bits_exceptionVec_20),
    .io_out_3_bits_exceptionVec_21(io_out_3_bits_exceptionVec_21),
    .io_out_3_bits_exceptionVec_22(io_out_3_bits_exceptionVec_22),
    .io_out_3_bits_exceptionVec_23(io_out_3_bits_exceptionVec_23),
    .io_out_3_bits_isFetchMalAddr(io_out_3_bits_isFetchMalAddr),
    .io_out_3_bits_trigger(io_out_3_bits_trigger),
    .io_out_3_bits_preDecodeInfo_isRVC(io_out_3_bits_preDecodeInfo_isRVC),
    .io_out_3_bits_preDecodeInfo_brType(io_out_3_bits_preDecodeInfo_brType),
    .io_out_3_bits_pred_taken(io_out_3_bits_pred_taken),
    .io_out_3_bits_crossPageIPFFix(io_out_3_bits_crossPageIPFFix),
    .io_out_3_bits_ftqPtr_flag(io_out_3_bits_ftqPtr_flag),
    .io_out_3_bits_ftqPtr_value(io_out_3_bits_ftqPtr_value),
    .io_out_3_bits_ftqOffset(io_out_3_bits_ftqOffset),
    .io_out_3_bits_srcType_0(io_out_3_bits_srcType_0),
    .io_out_3_bits_srcType_1(io_out_3_bits_srcType_1),
    .io_out_3_bits_srcType_2(io_out_3_bits_srcType_2),
    .io_out_3_bits_srcType_3(io_out_3_bits_srcType_3),
    .io_out_3_bits_srcType_4(io_out_3_bits_srcType_4),
    .io_out_3_bits_lsrc_0(io_out_3_bits_lsrc_0),
    .io_out_3_bits_lsrc_1(io_out_3_bits_lsrc_1),
    .io_out_3_bits_lsrc_2(io_out_3_bits_lsrc_2),
    .io_out_3_bits_ldest(io_out_3_bits_ldest),
    .io_out_3_bits_fuType(io_out_3_bits_fuType),
    .io_out_3_bits_fuOpType(io_out_3_bits_fuOpType),
    .io_out_3_bits_rfWen(io_out_3_bits_rfWen),
    .io_out_3_bits_fpWen(io_out_3_bits_fpWen),
    .io_out_3_bits_vecWen(io_out_3_bits_vecWen),
    .io_out_3_bits_v0Wen(io_out_3_bits_v0Wen),
    .io_out_3_bits_vlWen(io_out_3_bits_vlWen),
    .io_out_3_bits_isXSTrap(io_out_3_bits_isXSTrap),
    .io_out_3_bits_waitForward(io_out_3_bits_waitForward),
    .io_out_3_bits_blockBackward(io_out_3_bits_blockBackward),
    .io_out_3_bits_flushPipe(io_out_3_bits_flushPipe),
    .io_out_3_bits_canRobCompress(io_out_3_bits_canRobCompress),
    .io_out_3_bits_selImm(io_out_3_bits_selImm),
    .io_out_3_bits_imm(io_out_3_bits_imm),
    .io_out_3_bits_fpu_typeTagOut(io_out_3_bits_fpu_typeTagOut),
    .io_out_3_bits_fpu_wflags(io_out_3_bits_fpu_wflags),
    .io_out_3_bits_fpu_typ(io_out_3_bits_fpu_typ),
    .io_out_3_bits_fpu_fmt(io_out_3_bits_fpu_fmt),
    .io_out_3_bits_fpu_rm(io_out_3_bits_fpu_rm),
    .io_out_3_bits_vpu_vill(io_out_3_bits_vpu_vill),
    .io_out_3_bits_vpu_vma(io_out_3_bits_vpu_vma),
    .io_out_3_bits_vpu_vta(io_out_3_bits_vpu_vta),
    .io_out_3_bits_vpu_vsew(io_out_3_bits_vpu_vsew),
    .io_out_3_bits_vpu_vlmul(io_out_3_bits_vpu_vlmul),
    .io_out_3_bits_vpu_specVill(io_out_3_bits_vpu_specVill),
    .io_out_3_bits_vpu_specVma(io_out_3_bits_vpu_specVma),
    .io_out_3_bits_vpu_specVta(io_out_3_bits_vpu_specVta),
    .io_out_3_bits_vpu_specVsew(io_out_3_bits_vpu_specVsew),
    .io_out_3_bits_vpu_specVlmul(io_out_3_bits_vpu_specVlmul),
    .io_out_3_bits_vpu_vm(io_out_3_bits_vpu_vm),
    .io_out_3_bits_vpu_vstart(io_out_3_bits_vpu_vstart),
    .io_out_3_bits_vpu_fpu_isFoldTo1_2(io_out_3_bits_vpu_fpu_isFoldTo1_2),
    .io_out_3_bits_vpu_fpu_isFoldTo1_4(io_out_3_bits_vpu_fpu_isFoldTo1_4),
    .io_out_3_bits_vpu_fpu_isFoldTo1_8(io_out_3_bits_vpu_fpu_isFoldTo1_8),
    .io_out_3_bits_vpu_nf(io_out_3_bits_vpu_nf),
    .io_out_3_bits_vpu_veew(io_out_3_bits_vpu_veew),
    .io_out_3_bits_vpu_isExt(io_out_3_bits_vpu_isExt),
    .io_out_3_bits_vpu_isNarrow(io_out_3_bits_vpu_isNarrow),
    .io_out_3_bits_vpu_isDstMask(io_out_3_bits_vpu_isDstMask),
    .io_out_3_bits_vpu_isOpMask(io_out_3_bits_vpu_isOpMask),
    .io_out_3_bits_vpu_isDependOldVd(io_out_3_bits_vpu_isDependOldVd),
    .io_out_3_bits_vpu_isWritePartVd(io_out_3_bits_vpu_isWritePartVd),
    .io_out_3_bits_vpu_isVleff(io_out_3_bits_vpu_isVleff),
    .io_out_3_bits_vlsInstr(io_out_3_bits_vlsInstr),
    .io_out_3_bits_wfflags(io_out_3_bits_wfflags),
    .io_out_3_bits_isMove(io_out_3_bits_isMove),
    .io_out_3_bits_uopIdx(io_out_3_bits_uopIdx),
    .io_out_3_bits_uopSplitType(io_out_3_bits_uopSplitType),
    .io_out_3_bits_isVset(io_out_3_bits_isVset),
    .io_out_3_bits_firstUop(io_out_3_bits_firstUop),
    .io_out_3_bits_lastUop(io_out_3_bits_lastUop),
    .io_out_3_bits_numWB(io_out_3_bits_numWB),
    .io_out_3_bits_commitType(io_out_3_bits_commitType),
    .io_out_4_ready(io_out_4_ready),
    .io_out_4_valid(io_out_4_valid),
    .io_out_4_bits_instr(io_out_4_bits_instr),
    .io_out_4_bits_exceptionVec_0(io_out_4_bits_exceptionVec_0),
    .io_out_4_bits_exceptionVec_1(io_out_4_bits_exceptionVec_1),
    .io_out_4_bits_exceptionVec_2(io_out_4_bits_exceptionVec_2),
    .io_out_4_bits_exceptionVec_3(io_out_4_bits_exceptionVec_3),
    .io_out_4_bits_exceptionVec_4(io_out_4_bits_exceptionVec_4),
    .io_out_4_bits_exceptionVec_5(io_out_4_bits_exceptionVec_5),
    .io_out_4_bits_exceptionVec_6(io_out_4_bits_exceptionVec_6),
    .io_out_4_bits_exceptionVec_7(io_out_4_bits_exceptionVec_7),
    .io_out_4_bits_exceptionVec_8(io_out_4_bits_exceptionVec_8),
    .io_out_4_bits_exceptionVec_9(io_out_4_bits_exceptionVec_9),
    .io_out_4_bits_exceptionVec_10(io_out_4_bits_exceptionVec_10),
    .io_out_4_bits_exceptionVec_11(io_out_4_bits_exceptionVec_11),
    .io_out_4_bits_exceptionVec_12(io_out_4_bits_exceptionVec_12),
    .io_out_4_bits_exceptionVec_13(io_out_4_bits_exceptionVec_13),
    .io_out_4_bits_exceptionVec_14(io_out_4_bits_exceptionVec_14),
    .io_out_4_bits_exceptionVec_15(io_out_4_bits_exceptionVec_15),
    .io_out_4_bits_exceptionVec_16(io_out_4_bits_exceptionVec_16),
    .io_out_4_bits_exceptionVec_17(io_out_4_bits_exceptionVec_17),
    .io_out_4_bits_exceptionVec_18(io_out_4_bits_exceptionVec_18),
    .io_out_4_bits_exceptionVec_19(io_out_4_bits_exceptionVec_19),
    .io_out_4_bits_exceptionVec_20(io_out_4_bits_exceptionVec_20),
    .io_out_4_bits_exceptionVec_21(io_out_4_bits_exceptionVec_21),
    .io_out_4_bits_exceptionVec_22(io_out_4_bits_exceptionVec_22),
    .io_out_4_bits_exceptionVec_23(io_out_4_bits_exceptionVec_23),
    .io_out_4_bits_isFetchMalAddr(io_out_4_bits_isFetchMalAddr),
    .io_out_4_bits_trigger(io_out_4_bits_trigger),
    .io_out_4_bits_preDecodeInfo_isRVC(io_out_4_bits_preDecodeInfo_isRVC),
    .io_out_4_bits_preDecodeInfo_brType(io_out_4_bits_preDecodeInfo_brType),
    .io_out_4_bits_pred_taken(io_out_4_bits_pred_taken),
    .io_out_4_bits_crossPageIPFFix(io_out_4_bits_crossPageIPFFix),
    .io_out_4_bits_ftqPtr_flag(io_out_4_bits_ftqPtr_flag),
    .io_out_4_bits_ftqPtr_value(io_out_4_bits_ftqPtr_value),
    .io_out_4_bits_ftqOffset(io_out_4_bits_ftqOffset),
    .io_out_4_bits_srcType_0(io_out_4_bits_srcType_0),
    .io_out_4_bits_srcType_1(io_out_4_bits_srcType_1),
    .io_out_4_bits_srcType_2(io_out_4_bits_srcType_2),
    .io_out_4_bits_srcType_3(io_out_4_bits_srcType_3),
    .io_out_4_bits_srcType_4(io_out_4_bits_srcType_4),
    .io_out_4_bits_lsrc_0(io_out_4_bits_lsrc_0),
    .io_out_4_bits_lsrc_1(io_out_4_bits_lsrc_1),
    .io_out_4_bits_lsrc_2(io_out_4_bits_lsrc_2),
    .io_out_4_bits_ldest(io_out_4_bits_ldest),
    .io_out_4_bits_fuType(io_out_4_bits_fuType),
    .io_out_4_bits_fuOpType(io_out_4_bits_fuOpType),
    .io_out_4_bits_rfWen(io_out_4_bits_rfWen),
    .io_out_4_bits_fpWen(io_out_4_bits_fpWen),
    .io_out_4_bits_vecWen(io_out_4_bits_vecWen),
    .io_out_4_bits_v0Wen(io_out_4_bits_v0Wen),
    .io_out_4_bits_vlWen(io_out_4_bits_vlWen),
    .io_out_4_bits_isXSTrap(io_out_4_bits_isXSTrap),
    .io_out_4_bits_waitForward(io_out_4_bits_waitForward),
    .io_out_4_bits_blockBackward(io_out_4_bits_blockBackward),
    .io_out_4_bits_flushPipe(io_out_4_bits_flushPipe),
    .io_out_4_bits_canRobCompress(io_out_4_bits_canRobCompress),
    .io_out_4_bits_selImm(io_out_4_bits_selImm),
    .io_out_4_bits_imm(io_out_4_bits_imm),
    .io_out_4_bits_fpu_typeTagOut(io_out_4_bits_fpu_typeTagOut),
    .io_out_4_bits_fpu_wflags(io_out_4_bits_fpu_wflags),
    .io_out_4_bits_fpu_typ(io_out_4_bits_fpu_typ),
    .io_out_4_bits_fpu_fmt(io_out_4_bits_fpu_fmt),
    .io_out_4_bits_fpu_rm(io_out_4_bits_fpu_rm),
    .io_out_4_bits_vpu_vill(io_out_4_bits_vpu_vill),
    .io_out_4_bits_vpu_vma(io_out_4_bits_vpu_vma),
    .io_out_4_bits_vpu_vta(io_out_4_bits_vpu_vta),
    .io_out_4_bits_vpu_vsew(io_out_4_bits_vpu_vsew),
    .io_out_4_bits_vpu_vlmul(io_out_4_bits_vpu_vlmul),
    .io_out_4_bits_vpu_specVill(io_out_4_bits_vpu_specVill),
    .io_out_4_bits_vpu_specVma(io_out_4_bits_vpu_specVma),
    .io_out_4_bits_vpu_specVta(io_out_4_bits_vpu_specVta),
    .io_out_4_bits_vpu_specVsew(io_out_4_bits_vpu_specVsew),
    .io_out_4_bits_vpu_specVlmul(io_out_4_bits_vpu_specVlmul),
    .io_out_4_bits_vpu_vm(io_out_4_bits_vpu_vm),
    .io_out_4_bits_vpu_vstart(io_out_4_bits_vpu_vstart),
    .io_out_4_bits_vpu_fpu_isFoldTo1_2(io_out_4_bits_vpu_fpu_isFoldTo1_2),
    .io_out_4_bits_vpu_fpu_isFoldTo1_4(io_out_4_bits_vpu_fpu_isFoldTo1_4),
    .io_out_4_bits_vpu_fpu_isFoldTo1_8(io_out_4_bits_vpu_fpu_isFoldTo1_8),
    .io_out_4_bits_vpu_nf(io_out_4_bits_vpu_nf),
    .io_out_4_bits_vpu_veew(io_out_4_bits_vpu_veew),
    .io_out_4_bits_vpu_isExt(io_out_4_bits_vpu_isExt),
    .io_out_4_bits_vpu_isNarrow(io_out_4_bits_vpu_isNarrow),
    .io_out_4_bits_vpu_isDstMask(io_out_4_bits_vpu_isDstMask),
    .io_out_4_bits_vpu_isOpMask(io_out_4_bits_vpu_isOpMask),
    .io_out_4_bits_vpu_isDependOldVd(io_out_4_bits_vpu_isDependOldVd),
    .io_out_4_bits_vpu_isWritePartVd(io_out_4_bits_vpu_isWritePartVd),
    .io_out_4_bits_vpu_isVleff(io_out_4_bits_vpu_isVleff),
    .io_out_4_bits_vlsInstr(io_out_4_bits_vlsInstr),
    .io_out_4_bits_wfflags(io_out_4_bits_wfflags),
    .io_out_4_bits_isMove(io_out_4_bits_isMove),
    .io_out_4_bits_uopIdx(io_out_4_bits_uopIdx),
    .io_out_4_bits_uopSplitType(io_out_4_bits_uopSplitType),
    .io_out_4_bits_isVset(io_out_4_bits_isVset),
    .io_out_4_bits_firstUop(io_out_4_bits_firstUop),
    .io_out_4_bits_lastUop(io_out_4_bits_lastUop),
    .io_out_4_bits_numWB(io_out_4_bits_numWB),
    .io_out_4_bits_commitType(io_out_4_bits_commitType),
    .io_out_5_ready(io_out_5_ready),
    .io_out_5_valid(io_out_5_valid),
    .io_out_5_bits_instr(io_out_5_bits_instr),
    .io_out_5_bits_exceptionVec_0(io_out_5_bits_exceptionVec_0),
    .io_out_5_bits_exceptionVec_1(io_out_5_bits_exceptionVec_1),
    .io_out_5_bits_exceptionVec_2(io_out_5_bits_exceptionVec_2),
    .io_out_5_bits_exceptionVec_3(io_out_5_bits_exceptionVec_3),
    .io_out_5_bits_exceptionVec_4(io_out_5_bits_exceptionVec_4),
    .io_out_5_bits_exceptionVec_5(io_out_5_bits_exceptionVec_5),
    .io_out_5_bits_exceptionVec_6(io_out_5_bits_exceptionVec_6),
    .io_out_5_bits_exceptionVec_7(io_out_5_bits_exceptionVec_7),
    .io_out_5_bits_exceptionVec_8(io_out_5_bits_exceptionVec_8),
    .io_out_5_bits_exceptionVec_9(io_out_5_bits_exceptionVec_9),
    .io_out_5_bits_exceptionVec_10(io_out_5_bits_exceptionVec_10),
    .io_out_5_bits_exceptionVec_11(io_out_5_bits_exceptionVec_11),
    .io_out_5_bits_exceptionVec_12(io_out_5_bits_exceptionVec_12),
    .io_out_5_bits_exceptionVec_13(io_out_5_bits_exceptionVec_13),
    .io_out_5_bits_exceptionVec_14(io_out_5_bits_exceptionVec_14),
    .io_out_5_bits_exceptionVec_15(io_out_5_bits_exceptionVec_15),
    .io_out_5_bits_exceptionVec_16(io_out_5_bits_exceptionVec_16),
    .io_out_5_bits_exceptionVec_17(io_out_5_bits_exceptionVec_17),
    .io_out_5_bits_exceptionVec_18(io_out_5_bits_exceptionVec_18),
    .io_out_5_bits_exceptionVec_19(io_out_5_bits_exceptionVec_19),
    .io_out_5_bits_exceptionVec_20(io_out_5_bits_exceptionVec_20),
    .io_out_5_bits_exceptionVec_21(io_out_5_bits_exceptionVec_21),
    .io_out_5_bits_exceptionVec_22(io_out_5_bits_exceptionVec_22),
    .io_out_5_bits_exceptionVec_23(io_out_5_bits_exceptionVec_23),
    .io_out_5_bits_isFetchMalAddr(io_out_5_bits_isFetchMalAddr),
    .io_out_5_bits_trigger(io_out_5_bits_trigger),
    .io_out_5_bits_preDecodeInfo_isRVC(io_out_5_bits_preDecodeInfo_isRVC),
    .io_out_5_bits_preDecodeInfo_brType(io_out_5_bits_preDecodeInfo_brType),
    .io_out_5_bits_pred_taken(io_out_5_bits_pred_taken),
    .io_out_5_bits_crossPageIPFFix(io_out_5_bits_crossPageIPFFix),
    .io_out_5_bits_ftqPtr_flag(io_out_5_bits_ftqPtr_flag),
    .io_out_5_bits_ftqPtr_value(io_out_5_bits_ftqPtr_value),
    .io_out_5_bits_ftqOffset(io_out_5_bits_ftqOffset),
    .io_out_5_bits_srcType_0(io_out_5_bits_srcType_0),
    .io_out_5_bits_srcType_1(io_out_5_bits_srcType_1),
    .io_out_5_bits_srcType_2(io_out_5_bits_srcType_2),
    .io_out_5_bits_srcType_3(io_out_5_bits_srcType_3),
    .io_out_5_bits_srcType_4(io_out_5_bits_srcType_4),
    .io_out_5_bits_lsrc_0(io_out_5_bits_lsrc_0),
    .io_out_5_bits_lsrc_1(io_out_5_bits_lsrc_1),
    .io_out_5_bits_lsrc_2(io_out_5_bits_lsrc_2),
    .io_out_5_bits_ldest(io_out_5_bits_ldest),
    .io_out_5_bits_fuType(io_out_5_bits_fuType),
    .io_out_5_bits_fuOpType(io_out_5_bits_fuOpType),
    .io_out_5_bits_rfWen(io_out_5_bits_rfWen),
    .io_out_5_bits_fpWen(io_out_5_bits_fpWen),
    .io_out_5_bits_vecWen(io_out_5_bits_vecWen),
    .io_out_5_bits_v0Wen(io_out_5_bits_v0Wen),
    .io_out_5_bits_vlWen(io_out_5_bits_vlWen),
    .io_out_5_bits_isXSTrap(io_out_5_bits_isXSTrap),
    .io_out_5_bits_waitForward(io_out_5_bits_waitForward),
    .io_out_5_bits_blockBackward(io_out_5_bits_blockBackward),
    .io_out_5_bits_flushPipe(io_out_5_bits_flushPipe),
    .io_out_5_bits_canRobCompress(io_out_5_bits_canRobCompress),
    .io_out_5_bits_selImm(io_out_5_bits_selImm),
    .io_out_5_bits_imm(io_out_5_bits_imm),
    .io_out_5_bits_fpu_typeTagOut(io_out_5_bits_fpu_typeTagOut),
    .io_out_5_bits_fpu_wflags(io_out_5_bits_fpu_wflags),
    .io_out_5_bits_fpu_typ(io_out_5_bits_fpu_typ),
    .io_out_5_bits_fpu_fmt(io_out_5_bits_fpu_fmt),
    .io_out_5_bits_fpu_rm(io_out_5_bits_fpu_rm),
    .io_out_5_bits_vpu_vill(io_out_5_bits_vpu_vill),
    .io_out_5_bits_vpu_vma(io_out_5_bits_vpu_vma),
    .io_out_5_bits_vpu_vta(io_out_5_bits_vpu_vta),
    .io_out_5_bits_vpu_vsew(io_out_5_bits_vpu_vsew),
    .io_out_5_bits_vpu_vlmul(io_out_5_bits_vpu_vlmul),
    .io_out_5_bits_vpu_specVill(io_out_5_bits_vpu_specVill),
    .io_out_5_bits_vpu_specVma(io_out_5_bits_vpu_specVma),
    .io_out_5_bits_vpu_specVta(io_out_5_bits_vpu_specVta),
    .io_out_5_bits_vpu_specVsew(io_out_5_bits_vpu_specVsew),
    .io_out_5_bits_vpu_specVlmul(io_out_5_bits_vpu_specVlmul),
    .io_out_5_bits_vpu_vm(io_out_5_bits_vpu_vm),
    .io_out_5_bits_vpu_vstart(io_out_5_bits_vpu_vstart),
    .io_out_5_bits_vpu_fpu_isFoldTo1_2(io_out_5_bits_vpu_fpu_isFoldTo1_2),
    .io_out_5_bits_vpu_fpu_isFoldTo1_4(io_out_5_bits_vpu_fpu_isFoldTo1_4),
    .io_out_5_bits_vpu_fpu_isFoldTo1_8(io_out_5_bits_vpu_fpu_isFoldTo1_8),
    .io_out_5_bits_vpu_nf(io_out_5_bits_vpu_nf),
    .io_out_5_bits_vpu_veew(io_out_5_bits_vpu_veew),
    .io_out_5_bits_vpu_isExt(io_out_5_bits_vpu_isExt),
    .io_out_5_bits_vpu_isNarrow(io_out_5_bits_vpu_isNarrow),
    .io_out_5_bits_vpu_isDstMask(io_out_5_bits_vpu_isDstMask),
    .io_out_5_bits_vpu_isOpMask(io_out_5_bits_vpu_isOpMask),
    .io_out_5_bits_vpu_isDependOldVd(io_out_5_bits_vpu_isDependOldVd),
    .io_out_5_bits_vpu_isWritePartVd(io_out_5_bits_vpu_isWritePartVd),
    .io_out_5_bits_vpu_isVleff(io_out_5_bits_vpu_isVleff),
    .io_out_5_bits_vlsInstr(io_out_5_bits_vlsInstr),
    .io_out_5_bits_wfflags(io_out_5_bits_wfflags),
    .io_out_5_bits_isMove(io_out_5_bits_isMove),
    .io_out_5_bits_uopIdx(io_out_5_bits_uopIdx),
    .io_out_5_bits_uopSplitType(io_out_5_bits_uopSplitType),
    .io_out_5_bits_isVset(io_out_5_bits_isVset),
    .io_out_5_bits_firstUop(io_out_5_bits_firstUop),
    .io_out_5_bits_lastUop(io_out_5_bits_lastUop),
    .io_out_5_bits_numWB(io_out_5_bits_numWB),
    .io_out_5_bits_commitType(io_out_5_bits_commitType),
    .io_intRat_0_0_hold(io_intRat_0_0_hold),
    .io_intRat_0_0_addr(io_intRat_0_0_addr),
    .io_intRat_0_1_hold(io_intRat_0_1_hold),
    .io_intRat_0_1_addr(io_intRat_0_1_addr),
    .io_intRat_1_0_hold(io_intRat_1_0_hold),
    .io_intRat_1_0_addr(io_intRat_1_0_addr),
    .io_intRat_1_1_hold(io_intRat_1_1_hold),
    .io_intRat_1_1_addr(io_intRat_1_1_addr),
    .io_intRat_2_0_hold(io_intRat_2_0_hold),
    .io_intRat_2_0_addr(io_intRat_2_0_addr),
    .io_intRat_2_1_hold(io_intRat_2_1_hold),
    .io_intRat_2_1_addr(io_intRat_2_1_addr),
    .io_intRat_3_0_hold(io_intRat_3_0_hold),
    .io_intRat_3_0_addr(io_intRat_3_0_addr),
    .io_intRat_3_1_hold(io_intRat_3_1_hold),
    .io_intRat_3_1_addr(io_intRat_3_1_addr),
    .io_intRat_4_0_hold(io_intRat_4_0_hold),
    .io_intRat_4_0_addr(io_intRat_4_0_addr),
    .io_intRat_4_1_hold(io_intRat_4_1_hold),
    .io_intRat_4_1_addr(io_intRat_4_1_addr),
    .io_intRat_5_0_hold(io_intRat_5_0_hold),
    .io_intRat_5_0_addr(io_intRat_5_0_addr),
    .io_intRat_5_1_hold(io_intRat_5_1_hold),
    .io_intRat_5_1_addr(io_intRat_5_1_addr),
    .io_fpRat_0_0_hold(io_fpRat_0_0_hold),
    .io_fpRat_0_0_addr(io_fpRat_0_0_addr),
    .io_fpRat_0_1_hold(io_fpRat_0_1_hold),
    .io_fpRat_0_1_addr(io_fpRat_0_1_addr),
    .io_fpRat_0_2_hold(io_fpRat_0_2_hold),
    .io_fpRat_0_2_addr(io_fpRat_0_2_addr),
    .io_fpRat_1_0_hold(io_fpRat_1_0_hold),
    .io_fpRat_1_0_addr(io_fpRat_1_0_addr),
    .io_fpRat_1_1_hold(io_fpRat_1_1_hold),
    .io_fpRat_1_1_addr(io_fpRat_1_1_addr),
    .io_fpRat_1_2_hold(io_fpRat_1_2_hold),
    .io_fpRat_1_2_addr(io_fpRat_1_2_addr),
    .io_fpRat_2_0_hold(io_fpRat_2_0_hold),
    .io_fpRat_2_0_addr(io_fpRat_2_0_addr),
    .io_fpRat_2_1_hold(io_fpRat_2_1_hold),
    .io_fpRat_2_1_addr(io_fpRat_2_1_addr),
    .io_fpRat_2_2_hold(io_fpRat_2_2_hold),
    .io_fpRat_2_2_addr(io_fpRat_2_2_addr),
    .io_fpRat_3_0_hold(io_fpRat_3_0_hold),
    .io_fpRat_3_0_addr(io_fpRat_3_0_addr),
    .io_fpRat_3_1_hold(io_fpRat_3_1_hold),
    .io_fpRat_3_1_addr(io_fpRat_3_1_addr),
    .io_fpRat_3_2_hold(io_fpRat_3_2_hold),
    .io_fpRat_3_2_addr(io_fpRat_3_2_addr),
    .io_fpRat_4_0_hold(io_fpRat_4_0_hold),
    .io_fpRat_4_0_addr(io_fpRat_4_0_addr),
    .io_fpRat_4_1_hold(io_fpRat_4_1_hold),
    .io_fpRat_4_1_addr(io_fpRat_4_1_addr),
    .io_fpRat_4_2_hold(io_fpRat_4_2_hold),
    .io_fpRat_4_2_addr(io_fpRat_4_2_addr),
    .io_fpRat_5_0_hold(io_fpRat_5_0_hold),
    .io_fpRat_5_0_addr(io_fpRat_5_0_addr),
    .io_fpRat_5_1_hold(io_fpRat_5_1_hold),
    .io_fpRat_5_1_addr(io_fpRat_5_1_addr),
    .io_fpRat_5_2_hold(io_fpRat_5_2_hold),
    .io_fpRat_5_2_addr(io_fpRat_5_2_addr),
    .io_vecRat_0_0_hold(io_vecRat_0_0_hold),
    .io_vecRat_0_0_addr(io_vecRat_0_0_addr),
    .io_vecRat_0_1_hold(io_vecRat_0_1_hold),
    .io_vecRat_0_1_addr(io_vecRat_0_1_addr),
    .io_vecRat_0_2_hold(io_vecRat_0_2_hold),
    .io_vecRat_0_2_addr(io_vecRat_0_2_addr),
    .io_vecRat_1_0_hold(io_vecRat_1_0_hold),
    .io_vecRat_1_0_addr(io_vecRat_1_0_addr),
    .io_vecRat_1_1_hold(io_vecRat_1_1_hold),
    .io_vecRat_1_1_addr(io_vecRat_1_1_addr),
    .io_vecRat_1_2_hold(io_vecRat_1_2_hold),
    .io_vecRat_1_2_addr(io_vecRat_1_2_addr),
    .io_vecRat_2_0_hold(io_vecRat_2_0_hold),
    .io_vecRat_2_0_addr(io_vecRat_2_0_addr),
    .io_vecRat_2_1_hold(io_vecRat_2_1_hold),
    .io_vecRat_2_1_addr(io_vecRat_2_1_addr),
    .io_vecRat_2_2_hold(io_vecRat_2_2_hold),
    .io_vecRat_2_2_addr(io_vecRat_2_2_addr),
    .io_vecRat_3_0_hold(io_vecRat_3_0_hold),
    .io_vecRat_3_0_addr(io_vecRat_3_0_addr),
    .io_vecRat_3_1_hold(io_vecRat_3_1_hold),
    .io_vecRat_3_1_addr(io_vecRat_3_1_addr),
    .io_vecRat_3_2_hold(io_vecRat_3_2_hold),
    .io_vecRat_3_2_addr(io_vecRat_3_2_addr),
    .io_vecRat_4_0_hold(io_vecRat_4_0_hold),
    .io_vecRat_4_0_addr(io_vecRat_4_0_addr),
    .io_vecRat_4_1_hold(io_vecRat_4_1_hold),
    .io_vecRat_4_1_addr(io_vecRat_4_1_addr),
    .io_vecRat_4_2_hold(io_vecRat_4_2_hold),
    .io_vecRat_4_2_addr(io_vecRat_4_2_addr),
    .io_vecRat_5_0_hold(io_vecRat_5_0_hold),
    .io_vecRat_5_0_addr(io_vecRat_5_0_addr),
    .io_vecRat_5_1_hold(io_vecRat_5_1_hold),
    .io_vecRat_5_1_addr(io_vecRat_5_1_addr),
    .io_vecRat_5_2_hold(io_vecRat_5_2_hold),
    .io_vecRat_5_2_addr(io_vecRat_5_2_addr),
    .io_csrCtrl_singlestep(io_csrCtrl_singlestep),
    .io_fromCSR_illegalInst_sfenceVMA(io_fromCSR_illegalInst_sfenceVMA),
    .io_fromCSR_illegalInst_sfencePart(io_fromCSR_illegalInst_sfencePart),
    .io_fromCSR_illegalInst_hfenceGVMA(io_fromCSR_illegalInst_hfenceGVMA),
    .io_fromCSR_illegalInst_hfenceVVMA(io_fromCSR_illegalInst_hfenceVVMA),
    .io_fromCSR_illegalInst_hlsv(io_fromCSR_illegalInst_hlsv),
    .io_fromCSR_illegalInst_fsIsOff(io_fromCSR_illegalInst_fsIsOff),
    .io_fromCSR_illegalInst_vsIsOff(io_fromCSR_illegalInst_vsIsOff),
    .io_fromCSR_illegalInst_wfi(io_fromCSR_illegalInst_wfi),
    .io_fromCSR_illegalInst_frm(io_fromCSR_illegalInst_frm),
    .io_fromCSR_illegalInst_cboZ(io_fromCSR_illegalInst_cboZ),
    .io_fromCSR_illegalInst_cboCF(io_fromCSR_illegalInst_cboCF),
    .io_fromCSR_illegalInst_cboI(io_fromCSR_illegalInst_cboI),
    .io_fromCSR_virtualInst_sfenceVMA(io_fromCSR_virtualInst_sfenceVMA),
    .io_fromCSR_virtualInst_sfencePart(io_fromCSR_virtualInst_sfencePart),
    .io_fromCSR_virtualInst_hfence(io_fromCSR_virtualInst_hfence),
    .io_fromCSR_virtualInst_hlsv(io_fromCSR_virtualInst_hlsv),
    .io_fromCSR_virtualInst_wfi(io_fromCSR_virtualInst_wfi),
    .io_fromCSR_virtualInst_cboZ(io_fromCSR_virtualInst_cboZ),
    .io_fromCSR_virtualInst_cboCF(io_fromCSR_virtualInst_cboCF),
    .io_fromCSR_virtualInst_cboI(io_fromCSR_virtualInst_cboI),
    .io_fromCSR_special_cboI2F(io_fromCSR_special_cboI2F),
    .io_fusion_0(io_fusion_0),
    .io_fusion_1(io_fusion_1),
    .io_fusion_2(io_fusion_2),
    .io_fusion_3(io_fusion_3),
    .io_fusion_4(io_fusion_4),
    .io_fromRob_isResumeVType(io_fromRob_isResumeVType),
    .io_fromRob_walkToArchVType(io_fromRob_walkToArchVType),
    .io_fromRob_commitVType_vtype_valid(io_fromRob_commitVType_vtype_valid),
    .io_fromRob_commitVType_vtype_bits_illegal(io_fromRob_commitVType_vtype_bits_illegal),
    .io_fromRob_commitVType_vtype_bits_vma(io_fromRob_commitVType_vtype_bits_vma),
    .io_fromRob_commitVType_vtype_bits_vta(io_fromRob_commitVType_vtype_bits_vta),
    .io_fromRob_commitVType_vtype_bits_vsew(io_fromRob_commitVType_vtype_bits_vsew),
    .io_fromRob_commitVType_vtype_bits_vlmul(io_fromRob_commitVType_vtype_bits_vlmul),
    .io_fromRob_commitVType_hasVsetvl(io_fromRob_commitVType_hasVsetvl),
    .io_fromRob_walkVType_valid(io_fromRob_walkVType_valid),
    .io_fromRob_walkVType_bits_illegal(io_fromRob_walkVType_bits_illegal),
    .io_fromRob_walkVType_bits_vma(io_fromRob_walkVType_bits_vma),
    .io_fromRob_walkVType_bits_vta(io_fromRob_walkVType_bits_vta),
    .io_fromRob_walkVType_bits_vsew(io_fromRob_walkVType_bits_vsew),
    .io_fromRob_walkVType_bits_vlmul(io_fromRob_walkVType_bits_vlmul),
    .io_vsetvlVType_illegal(io_vsetvlVType_illegal),
    .io_vsetvlVType_vma(io_vsetvlVType_vma),
    .io_vsetvlVType_vta(io_vsetvlVType_vta),
    .io_vsetvlVType_vsew(io_vsetvlVType_vsew),
    .io_vsetvlVType_vlmul(io_vsetvlVType_vlmul),
    .io_vstart(io_vstart),
    .io_toCSR_trapInstInfo_valid(io_toCSR_trapInstInfo_valid),
    .io_toCSR_trapInstInfo_bits_instr(io_toCSR_trapInstInfo_bits_instr),
    .io_toCSR_trapInstInfo_bits_ftqPtr_flag(io_toCSR_trapInstInfo_bits_ftqPtr_flag),
    .io_toCSR_trapInstInfo_bits_ftqPtr_value(io_toCSR_trapInstInfo_bits_ftqPtr_value),
    .io_toCSR_trapInstInfo_bits_ftqOffset(io_toCSR_trapInstInfo_bits_ftqOffset),
    .io_perf_0_value(io_perf_0_value),
    .io_perf_1_value(io_perf_1_value),
    .io_perf_2_value(io_perf_2_value),
    .io_perf_3_value(io_perf_3_value)
 );


  export "DPI-C" function get_clockxxPfBDHOAJXyl;
  export "DPI-C" function set_clockxxPfBDHOAJXyl;
  export "DPI-C" function get_resetxxPfBDHOAJXyl;
  export "DPI-C" function set_resetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_redirectxxPfBDHOAJXyl;
  export "DPI-C" function set_io_redirectxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_0_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_0_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_1_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_1_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_2_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_2_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_3_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_3_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_4_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_4_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_in_5_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function set_io_in_5_bits_isLastInFtqEntryxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_readyxxPfBDHOAJXyl;
  export "DPI-C" function set_io_out_0_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_22xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_srcType_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_srcType_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_srcType_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_srcType_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_srcType_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_lsrc_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_lsrc_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_lsrc_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_ldestxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fuTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fuOpTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_rfWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fpWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vecWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_v0WenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vlWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_isXSTrapxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_waitForwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_blockBackwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_flushPipexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_canRobCompressxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_selImmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_immxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fpu_typeTagOutxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fpu_wflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fpu_typxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fpu_fmtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_fpu_rmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_villxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_specVillxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_specVmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_specVtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_specVsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_specVlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_vmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_nfxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_veewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isExtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isNarrowxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isDstMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isOpMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vpu_isVleffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_vlsInstrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_wfflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_isMovexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_uopIdxxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_uopSplitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_isVsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_firstUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_lastUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_numWBxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_0_bits_commitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_readyxxPfBDHOAJXyl;
  export "DPI-C" function set_io_out_1_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_22xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_srcType_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_srcType_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_srcType_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_srcType_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_srcType_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_lsrc_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_lsrc_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_lsrc_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_ldestxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fuTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fuOpTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_rfWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fpWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vecWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_v0WenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vlWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_isXSTrapxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_waitForwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_blockBackwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_flushPipexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_canRobCompressxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_selImmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_immxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fpu_typeTagOutxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fpu_wflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fpu_typxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fpu_fmtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_fpu_rmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_villxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_specVillxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_specVmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_specVtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_specVsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_specVlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_vmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_nfxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_veewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isExtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isNarrowxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isDstMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isOpMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vpu_isVleffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_vlsInstrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_wfflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_isMovexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_uopIdxxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_uopSplitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_isVsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_firstUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_lastUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_numWBxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_1_bits_commitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_readyxxPfBDHOAJXyl;
  export "DPI-C" function set_io_out_2_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_22xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_srcType_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_srcType_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_srcType_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_srcType_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_srcType_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_lsrc_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_lsrc_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_lsrc_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_ldestxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fuTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fuOpTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_rfWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fpWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vecWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_v0WenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vlWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_isXSTrapxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_waitForwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_blockBackwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_flushPipexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_canRobCompressxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_selImmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_immxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fpu_typeTagOutxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fpu_wflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fpu_typxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fpu_fmtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_fpu_rmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_villxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_specVillxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_specVmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_specVtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_specVsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_specVlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_vmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_nfxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_veewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isExtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isNarrowxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isDstMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isOpMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vpu_isVleffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_vlsInstrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_wfflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_isMovexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_uopIdxxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_uopSplitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_isVsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_firstUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_lastUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_numWBxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_2_bits_commitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_readyxxPfBDHOAJXyl;
  export "DPI-C" function set_io_out_3_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_22xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_srcType_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_srcType_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_srcType_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_srcType_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_srcType_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_lsrc_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_lsrc_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_lsrc_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_ldestxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fuTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fuOpTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_rfWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fpWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vecWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_v0WenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vlWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_isXSTrapxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_waitForwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_blockBackwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_flushPipexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_canRobCompressxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_selImmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_immxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fpu_typeTagOutxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fpu_wflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fpu_typxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fpu_fmtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_fpu_rmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_villxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_specVillxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_specVmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_specVtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_specVsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_specVlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_vmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_nfxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_veewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isExtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isNarrowxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isDstMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isOpMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vpu_isVleffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_vlsInstrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_wfflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_isMovexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_uopIdxxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_uopSplitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_isVsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_firstUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_lastUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_numWBxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_3_bits_commitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_readyxxPfBDHOAJXyl;
  export "DPI-C" function set_io_out_4_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_22xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_srcType_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_srcType_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_srcType_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_srcType_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_srcType_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_lsrc_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_lsrc_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_lsrc_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_ldestxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fuTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fuOpTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_rfWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fpWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vecWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_v0WenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vlWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_isXSTrapxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_waitForwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_blockBackwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_flushPipexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_canRobCompressxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_selImmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_immxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fpu_typeTagOutxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fpu_wflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fpu_typxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fpu_fmtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_fpu_rmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_villxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_specVillxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_specVmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_specVtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_specVsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_specVlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_vmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_nfxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_veewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isExtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isNarrowxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isDstMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isOpMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vpu_isVleffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_vlsInstrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_wfflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_isMovexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_uopIdxxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_uopSplitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_isVsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_firstUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_lastUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_numWBxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_4_bits_commitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_readyxxPfBDHOAJXyl;
  export "DPI-C" function set_io_out_5_readyxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_5xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_6xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_7xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_9xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_10xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_11xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_12xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_13xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_14xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_15xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_16xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_17xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_18xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_19xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_20xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_21xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_22xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_exceptionVec_23xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_isFetchMalAddrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_triggerxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_pred_takenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_crossPageIPFFixxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_srcType_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_srcType_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_srcType_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_srcType_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_srcType_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_lsrc_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_lsrc_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_lsrc_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_ldestxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fuTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fuOpTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_rfWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fpWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vecWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_v0WenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vlWenxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_isXSTrapxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_waitForwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_blockBackwardxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_flushPipexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_canRobCompressxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_selImmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_immxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fpu_typeTagOutxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fpu_wflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fpu_typxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fpu_fmtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_fpu_rmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_villxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_specVillxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_specVmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_specVtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_specVsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_specVlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_vmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_nfxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_veewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isExtxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isNarrowxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isDstMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isOpMaskxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vpu_isVleffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_vlsInstrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_wfflagsxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_isMovexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_uopIdxxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_uopSplitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_isVsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_firstUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_lastUopxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_numWBxxPfBDHOAJXyl;
  export "DPI-C" function get_io_out_5_bits_commitTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_0_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_0_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_0_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_0_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_1_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_1_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_1_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_1_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_2_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_2_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_2_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_2_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_3_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_3_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_3_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_3_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_4_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_4_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_4_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_4_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_5_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_5_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_5_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_intRat_5_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_0_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_0_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_0_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_0_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_0_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_0_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_1_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_1_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_1_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_1_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_1_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_1_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_2_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_2_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_2_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_2_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_2_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_2_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_3_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_3_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_3_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_3_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_3_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_3_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_4_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_4_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_4_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_4_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_4_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_4_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_5_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_5_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_5_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_5_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_5_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fpRat_5_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_0_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_0_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_0_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_0_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_0_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_0_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_1_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_1_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_1_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_1_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_1_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_1_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_2_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_2_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_2_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_2_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_2_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_2_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_3_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_3_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_3_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_3_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_3_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_3_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_4_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_4_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_4_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_4_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_4_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_4_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_5_0_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_5_0_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_5_1_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_5_1_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_5_2_holdxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vecRat_5_2_addrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_csrCtrl_singlestepxxPfBDHOAJXyl;
  export "DPI-C" function set_io_csrCtrl_singlestepxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_sfenceVMAxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_sfenceVMAxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_sfencePartxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_sfencePartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_hfenceGVMAxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_hfenceGVMAxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_hfenceVVMAxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_hfenceVVMAxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_hlsvxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_hlsvxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_fsIsOffxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_fsIsOffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_vsIsOffxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_vsIsOffxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_wfixxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_wfixxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_frmxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_frmxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_cboZxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_cboZxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_cboCFxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_cboCFxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_illegalInst_cboIxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_illegalInst_cboIxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_sfenceVMAxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_sfenceVMAxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_sfencePartxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_sfencePartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_hfencexxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_hfencexxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_hlsvxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_hlsvxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_wfixxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_wfixxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_cboZxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_cboZxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_cboCFxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_cboCFxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_virtualInst_cboIxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_virtualInst_cboIxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromCSR_special_cboI2FxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromCSR_special_cboI2FxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fusion_0xxPfBDHOAJXyl;
  export "DPI-C" function set_io_fusion_0xxPfBDHOAJXyl;
  export "DPI-C" function get_io_fusion_1xxPfBDHOAJXyl;
  export "DPI-C" function set_io_fusion_1xxPfBDHOAJXyl;
  export "DPI-C" function get_io_fusion_2xxPfBDHOAJXyl;
  export "DPI-C" function set_io_fusion_2xxPfBDHOAJXyl;
  export "DPI-C" function get_io_fusion_3xxPfBDHOAJXyl;
  export "DPI-C" function set_io_fusion_3xxPfBDHOAJXyl;
  export "DPI-C" function get_io_fusion_4xxPfBDHOAJXyl;
  export "DPI-C" function set_io_fusion_4xxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_isResumeVTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_isResumeVTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkToArchVTypexxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkToArchVTypexxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_vtype_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_vtype_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_vtype_bits_illegalxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_vtype_bits_illegalxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_vtype_bits_vmaxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_vtype_bits_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_vtype_bits_vtaxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_vtype_bits_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_vtype_bits_vsewxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_vtype_bits_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_vtype_bits_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_vtype_bits_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_commitVType_hasVsetvlxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_commitVType_hasVsetvlxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkVType_validxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkVType_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkVType_bits_illegalxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkVType_bits_illegalxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkVType_bits_vmaxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkVType_bits_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkVType_bits_vtaxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkVType_bits_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkVType_bits_vsewxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkVType_bits_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_fromRob_walkVType_bits_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function set_io_fromRob_walkVType_bits_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vsetvlVType_illegalxxPfBDHOAJXyl;
  export "DPI-C" function set_io_vsetvlVType_illegalxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vsetvlVType_vmaxxPfBDHOAJXyl;
  export "DPI-C" function set_io_vsetvlVType_vmaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vsetvlVType_vtaxxPfBDHOAJXyl;
  export "DPI-C" function set_io_vsetvlVType_vtaxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vsetvlVType_vsewxxPfBDHOAJXyl;
  export "DPI-C" function set_io_vsetvlVType_vsewxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vsetvlVType_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function set_io_vsetvlVType_vlmulxxPfBDHOAJXyl;
  export "DPI-C" function get_io_vstartxxPfBDHOAJXyl;
  export "DPI-C" function set_io_vstartxxPfBDHOAJXyl;
  export "DPI-C" function get_io_toCSR_trapInstInfo_validxxPfBDHOAJXyl;
  export "DPI-C" function get_io_toCSR_trapInstInfo_bits_instrxxPfBDHOAJXyl;
  export "DPI-C" function get_io_toCSR_trapInstInfo_bits_ftqPtr_flagxxPfBDHOAJXyl;
  export "DPI-C" function get_io_toCSR_trapInstInfo_bits_ftqPtr_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_toCSR_trapInstInfo_bits_ftqOffsetxxPfBDHOAJXyl;
  export "DPI-C" function get_io_perf_0_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_perf_1_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_perf_2_valuexxPfBDHOAJXyl;
  export "DPI-C" function get_io_perf_3_valuexxPfBDHOAJXyl;


  function void get_clockxxPfBDHOAJXyl;
    output logic  value;
    value=clock;
  endfunction

  function void set_clockxxPfBDHOAJXyl;
    input logic  value;
    clock=value;
  endfunction

  function void get_resetxxPfBDHOAJXyl;
    output logic  value;
    value=reset;
  endfunction

  function void set_resetxxPfBDHOAJXyl;
    input logic  value;
    reset=value;
  endfunction

  function void get_io_redirectxxPfBDHOAJXyl;
    output logic  value;
    value=io_redirect;
  endfunction

  function void set_io_redirectxxPfBDHOAJXyl;
    input logic  value;
    io_redirect=value;
  endfunction

  function void get_io_in_0_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_ready;
  endfunction

  function void get_io_in_0_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_valid;
  endfunction

  function void set_io_in_0_validxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_valid=value;
  endfunction

  function void get_io_in_0_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_in_0_bits_instr;
  endfunction

  function void set_io_in_0_bits_instrxxPfBDHOAJXyl;
    input logic [31:0] value;
    io_in_0_bits_instr=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_0;
  endfunction

  function void set_io_in_0_bits_exceptionVec_0xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_0=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_1;
  endfunction

  function void set_io_in_0_bits_exceptionVec_1xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_1=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_2;
  endfunction

  function void set_io_in_0_bits_exceptionVec_2xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_2=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_4;
  endfunction

  function void set_io_in_0_bits_exceptionVec_4xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_4=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_5;
  endfunction

  function void set_io_in_0_bits_exceptionVec_5xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_5=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_6;
  endfunction

  function void set_io_in_0_bits_exceptionVec_6xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_6=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_7;
  endfunction

  function void set_io_in_0_bits_exceptionVec_7xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_7=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_8;
  endfunction

  function void set_io_in_0_bits_exceptionVec_8xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_8=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_9;
  endfunction

  function void set_io_in_0_bits_exceptionVec_9xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_9=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_10;
  endfunction

  function void set_io_in_0_bits_exceptionVec_10xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_10=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_11;
  endfunction

  function void set_io_in_0_bits_exceptionVec_11xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_11=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_12;
  endfunction

  function void set_io_in_0_bits_exceptionVec_12xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_12=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_13;
  endfunction

  function void set_io_in_0_bits_exceptionVec_13xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_13=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_14;
  endfunction

  function void set_io_in_0_bits_exceptionVec_14xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_14=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_15;
  endfunction

  function void set_io_in_0_bits_exceptionVec_15xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_15=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_16;
  endfunction

  function void set_io_in_0_bits_exceptionVec_16xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_16=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_17;
  endfunction

  function void set_io_in_0_bits_exceptionVec_17xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_17=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_18;
  endfunction

  function void set_io_in_0_bits_exceptionVec_18xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_18=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_19;
  endfunction

  function void set_io_in_0_bits_exceptionVec_19xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_19=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_20;
  endfunction

  function void set_io_in_0_bits_exceptionVec_20xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_20=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_21;
  endfunction

  function void set_io_in_0_bits_exceptionVec_21xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_21=value;
  endfunction

  function void get_io_in_0_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_exceptionVec_23;
  endfunction

  function void set_io_in_0_bits_exceptionVec_23xxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_exceptionVec_23=value;
  endfunction

  function void get_io_in_0_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_isFetchMalAddr;
  endfunction

  function void set_io_in_0_bits_isFetchMalAddrxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_isFetchMalAddr=value;
  endfunction

  function void get_io_in_0_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_0_bits_trigger;
  endfunction

  function void set_io_in_0_bits_triggerxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_0_bits_trigger=value;
  endfunction

  function void get_io_in_0_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_preDecodeInfo_isRVC;
  endfunction

  function void set_io_in_0_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_preDecodeInfo_isRVC=value;
  endfunction

  function void get_io_in_0_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_in_0_bits_preDecodeInfo_brType;
  endfunction

  function void set_io_in_0_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    input logic [1:0] value;
    io_in_0_bits_preDecodeInfo_brType=value;
  endfunction

  function void get_io_in_0_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_pred_taken;
  endfunction

  function void set_io_in_0_bits_pred_takenxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_pred_taken=value;
  endfunction

  function void get_io_in_0_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_crossPageIPFFix;
  endfunction

  function void set_io_in_0_bits_crossPageIPFFixxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_crossPageIPFFix=value;
  endfunction

  function void get_io_in_0_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_ftqPtr_flag;
  endfunction

  function void set_io_in_0_bits_ftqPtr_flagxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_ftqPtr_flag=value;
  endfunction

  function void get_io_in_0_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_in_0_bits_ftqPtr_value;
  endfunction

  function void set_io_in_0_bits_ftqPtr_valuexxPfBDHOAJXyl;
    input logic [5:0] value;
    io_in_0_bits_ftqPtr_value=value;
  endfunction

  function void get_io_in_0_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_0_bits_ftqOffset;
  endfunction

  function void set_io_in_0_bits_ftqOffsetxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_0_bits_ftqOffset=value;
  endfunction

  function void get_io_in_0_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_0_bits_isLastInFtqEntry;
  endfunction

  function void set_io_in_0_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    input logic  value;
    io_in_0_bits_isLastInFtqEntry=value;
  endfunction

  function void get_io_in_1_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_ready;
  endfunction

  function void get_io_in_1_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_valid;
  endfunction

  function void set_io_in_1_validxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_valid=value;
  endfunction

  function void get_io_in_1_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_in_1_bits_instr;
  endfunction

  function void set_io_in_1_bits_instrxxPfBDHOAJXyl;
    input logic [31:0] value;
    io_in_1_bits_instr=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_0;
  endfunction

  function void set_io_in_1_bits_exceptionVec_0xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_0=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_1;
  endfunction

  function void set_io_in_1_bits_exceptionVec_1xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_1=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_2;
  endfunction

  function void set_io_in_1_bits_exceptionVec_2xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_2=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_4;
  endfunction

  function void set_io_in_1_bits_exceptionVec_4xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_4=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_5;
  endfunction

  function void set_io_in_1_bits_exceptionVec_5xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_5=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_6;
  endfunction

  function void set_io_in_1_bits_exceptionVec_6xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_6=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_7;
  endfunction

  function void set_io_in_1_bits_exceptionVec_7xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_7=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_8;
  endfunction

  function void set_io_in_1_bits_exceptionVec_8xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_8=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_9;
  endfunction

  function void set_io_in_1_bits_exceptionVec_9xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_9=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_10;
  endfunction

  function void set_io_in_1_bits_exceptionVec_10xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_10=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_11;
  endfunction

  function void set_io_in_1_bits_exceptionVec_11xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_11=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_12;
  endfunction

  function void set_io_in_1_bits_exceptionVec_12xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_12=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_13;
  endfunction

  function void set_io_in_1_bits_exceptionVec_13xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_13=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_14;
  endfunction

  function void set_io_in_1_bits_exceptionVec_14xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_14=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_15;
  endfunction

  function void set_io_in_1_bits_exceptionVec_15xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_15=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_16;
  endfunction

  function void set_io_in_1_bits_exceptionVec_16xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_16=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_17;
  endfunction

  function void set_io_in_1_bits_exceptionVec_17xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_17=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_18;
  endfunction

  function void set_io_in_1_bits_exceptionVec_18xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_18=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_19;
  endfunction

  function void set_io_in_1_bits_exceptionVec_19xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_19=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_20;
  endfunction

  function void set_io_in_1_bits_exceptionVec_20xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_20=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_21;
  endfunction

  function void set_io_in_1_bits_exceptionVec_21xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_21=value;
  endfunction

  function void get_io_in_1_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_exceptionVec_23;
  endfunction

  function void set_io_in_1_bits_exceptionVec_23xxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_exceptionVec_23=value;
  endfunction

  function void get_io_in_1_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_isFetchMalAddr;
  endfunction

  function void set_io_in_1_bits_isFetchMalAddrxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_isFetchMalAddr=value;
  endfunction

  function void get_io_in_1_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_1_bits_trigger;
  endfunction

  function void set_io_in_1_bits_triggerxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_1_bits_trigger=value;
  endfunction

  function void get_io_in_1_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_preDecodeInfo_isRVC;
  endfunction

  function void set_io_in_1_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_preDecodeInfo_isRVC=value;
  endfunction

  function void get_io_in_1_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_in_1_bits_preDecodeInfo_brType;
  endfunction

  function void set_io_in_1_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    input logic [1:0] value;
    io_in_1_bits_preDecodeInfo_brType=value;
  endfunction

  function void get_io_in_1_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_pred_taken;
  endfunction

  function void set_io_in_1_bits_pred_takenxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_pred_taken=value;
  endfunction

  function void get_io_in_1_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_crossPageIPFFix;
  endfunction

  function void set_io_in_1_bits_crossPageIPFFixxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_crossPageIPFFix=value;
  endfunction

  function void get_io_in_1_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_ftqPtr_flag;
  endfunction

  function void set_io_in_1_bits_ftqPtr_flagxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_ftqPtr_flag=value;
  endfunction

  function void get_io_in_1_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_in_1_bits_ftqPtr_value;
  endfunction

  function void set_io_in_1_bits_ftqPtr_valuexxPfBDHOAJXyl;
    input logic [5:0] value;
    io_in_1_bits_ftqPtr_value=value;
  endfunction

  function void get_io_in_1_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_1_bits_ftqOffset;
  endfunction

  function void set_io_in_1_bits_ftqOffsetxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_1_bits_ftqOffset=value;
  endfunction

  function void get_io_in_1_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_1_bits_isLastInFtqEntry;
  endfunction

  function void set_io_in_1_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    input logic  value;
    io_in_1_bits_isLastInFtqEntry=value;
  endfunction

  function void get_io_in_2_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_ready;
  endfunction

  function void get_io_in_2_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_valid;
  endfunction

  function void set_io_in_2_validxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_valid=value;
  endfunction

  function void get_io_in_2_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_in_2_bits_instr;
  endfunction

  function void set_io_in_2_bits_instrxxPfBDHOAJXyl;
    input logic [31:0] value;
    io_in_2_bits_instr=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_0;
  endfunction

  function void set_io_in_2_bits_exceptionVec_0xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_0=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_1;
  endfunction

  function void set_io_in_2_bits_exceptionVec_1xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_1=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_2;
  endfunction

  function void set_io_in_2_bits_exceptionVec_2xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_2=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_4;
  endfunction

  function void set_io_in_2_bits_exceptionVec_4xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_4=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_5;
  endfunction

  function void set_io_in_2_bits_exceptionVec_5xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_5=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_6;
  endfunction

  function void set_io_in_2_bits_exceptionVec_6xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_6=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_7;
  endfunction

  function void set_io_in_2_bits_exceptionVec_7xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_7=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_8;
  endfunction

  function void set_io_in_2_bits_exceptionVec_8xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_8=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_9;
  endfunction

  function void set_io_in_2_bits_exceptionVec_9xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_9=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_10;
  endfunction

  function void set_io_in_2_bits_exceptionVec_10xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_10=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_11;
  endfunction

  function void set_io_in_2_bits_exceptionVec_11xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_11=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_12;
  endfunction

  function void set_io_in_2_bits_exceptionVec_12xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_12=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_13;
  endfunction

  function void set_io_in_2_bits_exceptionVec_13xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_13=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_14;
  endfunction

  function void set_io_in_2_bits_exceptionVec_14xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_14=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_15;
  endfunction

  function void set_io_in_2_bits_exceptionVec_15xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_15=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_16;
  endfunction

  function void set_io_in_2_bits_exceptionVec_16xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_16=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_17;
  endfunction

  function void set_io_in_2_bits_exceptionVec_17xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_17=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_18;
  endfunction

  function void set_io_in_2_bits_exceptionVec_18xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_18=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_19;
  endfunction

  function void set_io_in_2_bits_exceptionVec_19xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_19=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_20;
  endfunction

  function void set_io_in_2_bits_exceptionVec_20xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_20=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_21;
  endfunction

  function void set_io_in_2_bits_exceptionVec_21xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_21=value;
  endfunction

  function void get_io_in_2_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_exceptionVec_23;
  endfunction

  function void set_io_in_2_bits_exceptionVec_23xxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_exceptionVec_23=value;
  endfunction

  function void get_io_in_2_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_isFetchMalAddr;
  endfunction

  function void set_io_in_2_bits_isFetchMalAddrxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_isFetchMalAddr=value;
  endfunction

  function void get_io_in_2_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_2_bits_trigger;
  endfunction

  function void set_io_in_2_bits_triggerxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_2_bits_trigger=value;
  endfunction

  function void get_io_in_2_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_preDecodeInfo_isRVC;
  endfunction

  function void set_io_in_2_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_preDecodeInfo_isRVC=value;
  endfunction

  function void get_io_in_2_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_in_2_bits_preDecodeInfo_brType;
  endfunction

  function void set_io_in_2_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    input logic [1:0] value;
    io_in_2_bits_preDecodeInfo_brType=value;
  endfunction

  function void get_io_in_2_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_pred_taken;
  endfunction

  function void set_io_in_2_bits_pred_takenxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_pred_taken=value;
  endfunction

  function void get_io_in_2_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_crossPageIPFFix;
  endfunction

  function void set_io_in_2_bits_crossPageIPFFixxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_crossPageIPFFix=value;
  endfunction

  function void get_io_in_2_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_ftqPtr_flag;
  endfunction

  function void set_io_in_2_bits_ftqPtr_flagxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_ftqPtr_flag=value;
  endfunction

  function void get_io_in_2_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_in_2_bits_ftqPtr_value;
  endfunction

  function void set_io_in_2_bits_ftqPtr_valuexxPfBDHOAJXyl;
    input logic [5:0] value;
    io_in_2_bits_ftqPtr_value=value;
  endfunction

  function void get_io_in_2_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_2_bits_ftqOffset;
  endfunction

  function void set_io_in_2_bits_ftqOffsetxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_2_bits_ftqOffset=value;
  endfunction

  function void get_io_in_2_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_2_bits_isLastInFtqEntry;
  endfunction

  function void set_io_in_2_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    input logic  value;
    io_in_2_bits_isLastInFtqEntry=value;
  endfunction

  function void get_io_in_3_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_ready;
  endfunction

  function void get_io_in_3_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_valid;
  endfunction

  function void set_io_in_3_validxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_valid=value;
  endfunction

  function void get_io_in_3_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_in_3_bits_instr;
  endfunction

  function void set_io_in_3_bits_instrxxPfBDHOAJXyl;
    input logic [31:0] value;
    io_in_3_bits_instr=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_0;
  endfunction

  function void set_io_in_3_bits_exceptionVec_0xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_0=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_1;
  endfunction

  function void set_io_in_3_bits_exceptionVec_1xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_1=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_2;
  endfunction

  function void set_io_in_3_bits_exceptionVec_2xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_2=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_4;
  endfunction

  function void set_io_in_3_bits_exceptionVec_4xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_4=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_5;
  endfunction

  function void set_io_in_3_bits_exceptionVec_5xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_5=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_6;
  endfunction

  function void set_io_in_3_bits_exceptionVec_6xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_6=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_7;
  endfunction

  function void set_io_in_3_bits_exceptionVec_7xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_7=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_8;
  endfunction

  function void set_io_in_3_bits_exceptionVec_8xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_8=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_9;
  endfunction

  function void set_io_in_3_bits_exceptionVec_9xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_9=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_10;
  endfunction

  function void set_io_in_3_bits_exceptionVec_10xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_10=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_11;
  endfunction

  function void set_io_in_3_bits_exceptionVec_11xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_11=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_12;
  endfunction

  function void set_io_in_3_bits_exceptionVec_12xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_12=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_13;
  endfunction

  function void set_io_in_3_bits_exceptionVec_13xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_13=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_14;
  endfunction

  function void set_io_in_3_bits_exceptionVec_14xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_14=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_15;
  endfunction

  function void set_io_in_3_bits_exceptionVec_15xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_15=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_16;
  endfunction

  function void set_io_in_3_bits_exceptionVec_16xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_16=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_17;
  endfunction

  function void set_io_in_3_bits_exceptionVec_17xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_17=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_18;
  endfunction

  function void set_io_in_3_bits_exceptionVec_18xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_18=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_19;
  endfunction

  function void set_io_in_3_bits_exceptionVec_19xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_19=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_20;
  endfunction

  function void set_io_in_3_bits_exceptionVec_20xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_20=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_21;
  endfunction

  function void set_io_in_3_bits_exceptionVec_21xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_21=value;
  endfunction

  function void get_io_in_3_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_exceptionVec_23;
  endfunction

  function void set_io_in_3_bits_exceptionVec_23xxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_exceptionVec_23=value;
  endfunction

  function void get_io_in_3_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_isFetchMalAddr;
  endfunction

  function void set_io_in_3_bits_isFetchMalAddrxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_isFetchMalAddr=value;
  endfunction

  function void get_io_in_3_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_3_bits_trigger;
  endfunction

  function void set_io_in_3_bits_triggerxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_3_bits_trigger=value;
  endfunction

  function void get_io_in_3_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_preDecodeInfo_isRVC;
  endfunction

  function void set_io_in_3_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_preDecodeInfo_isRVC=value;
  endfunction

  function void get_io_in_3_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_in_3_bits_preDecodeInfo_brType;
  endfunction

  function void set_io_in_3_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    input logic [1:0] value;
    io_in_3_bits_preDecodeInfo_brType=value;
  endfunction

  function void get_io_in_3_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_pred_taken;
  endfunction

  function void set_io_in_3_bits_pred_takenxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_pred_taken=value;
  endfunction

  function void get_io_in_3_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_crossPageIPFFix;
  endfunction

  function void set_io_in_3_bits_crossPageIPFFixxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_crossPageIPFFix=value;
  endfunction

  function void get_io_in_3_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_ftqPtr_flag;
  endfunction

  function void set_io_in_3_bits_ftqPtr_flagxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_ftqPtr_flag=value;
  endfunction

  function void get_io_in_3_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_in_3_bits_ftqPtr_value;
  endfunction

  function void set_io_in_3_bits_ftqPtr_valuexxPfBDHOAJXyl;
    input logic [5:0] value;
    io_in_3_bits_ftqPtr_value=value;
  endfunction

  function void get_io_in_3_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_3_bits_ftqOffset;
  endfunction

  function void set_io_in_3_bits_ftqOffsetxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_3_bits_ftqOffset=value;
  endfunction

  function void get_io_in_3_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_3_bits_isLastInFtqEntry;
  endfunction

  function void set_io_in_3_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    input logic  value;
    io_in_3_bits_isLastInFtqEntry=value;
  endfunction

  function void get_io_in_4_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_ready;
  endfunction

  function void get_io_in_4_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_valid;
  endfunction

  function void set_io_in_4_validxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_valid=value;
  endfunction

  function void get_io_in_4_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_in_4_bits_instr;
  endfunction

  function void set_io_in_4_bits_instrxxPfBDHOAJXyl;
    input logic [31:0] value;
    io_in_4_bits_instr=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_0;
  endfunction

  function void set_io_in_4_bits_exceptionVec_0xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_0=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_1;
  endfunction

  function void set_io_in_4_bits_exceptionVec_1xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_1=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_2;
  endfunction

  function void set_io_in_4_bits_exceptionVec_2xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_2=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_4;
  endfunction

  function void set_io_in_4_bits_exceptionVec_4xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_4=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_5;
  endfunction

  function void set_io_in_4_bits_exceptionVec_5xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_5=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_6;
  endfunction

  function void set_io_in_4_bits_exceptionVec_6xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_6=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_7;
  endfunction

  function void set_io_in_4_bits_exceptionVec_7xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_7=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_8;
  endfunction

  function void set_io_in_4_bits_exceptionVec_8xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_8=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_9;
  endfunction

  function void set_io_in_4_bits_exceptionVec_9xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_9=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_10;
  endfunction

  function void set_io_in_4_bits_exceptionVec_10xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_10=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_11;
  endfunction

  function void set_io_in_4_bits_exceptionVec_11xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_11=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_12;
  endfunction

  function void set_io_in_4_bits_exceptionVec_12xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_12=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_13;
  endfunction

  function void set_io_in_4_bits_exceptionVec_13xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_13=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_14;
  endfunction

  function void set_io_in_4_bits_exceptionVec_14xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_14=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_15;
  endfunction

  function void set_io_in_4_bits_exceptionVec_15xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_15=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_16;
  endfunction

  function void set_io_in_4_bits_exceptionVec_16xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_16=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_17;
  endfunction

  function void set_io_in_4_bits_exceptionVec_17xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_17=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_18;
  endfunction

  function void set_io_in_4_bits_exceptionVec_18xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_18=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_19;
  endfunction

  function void set_io_in_4_bits_exceptionVec_19xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_19=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_20;
  endfunction

  function void set_io_in_4_bits_exceptionVec_20xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_20=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_21;
  endfunction

  function void set_io_in_4_bits_exceptionVec_21xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_21=value;
  endfunction

  function void get_io_in_4_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_exceptionVec_23;
  endfunction

  function void set_io_in_4_bits_exceptionVec_23xxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_exceptionVec_23=value;
  endfunction

  function void get_io_in_4_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_isFetchMalAddr;
  endfunction

  function void set_io_in_4_bits_isFetchMalAddrxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_isFetchMalAddr=value;
  endfunction

  function void get_io_in_4_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_4_bits_trigger;
  endfunction

  function void set_io_in_4_bits_triggerxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_4_bits_trigger=value;
  endfunction

  function void get_io_in_4_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_preDecodeInfo_isRVC;
  endfunction

  function void set_io_in_4_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_preDecodeInfo_isRVC=value;
  endfunction

  function void get_io_in_4_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_in_4_bits_preDecodeInfo_brType;
  endfunction

  function void set_io_in_4_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    input logic [1:0] value;
    io_in_4_bits_preDecodeInfo_brType=value;
  endfunction

  function void get_io_in_4_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_pred_taken;
  endfunction

  function void set_io_in_4_bits_pred_takenxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_pred_taken=value;
  endfunction

  function void get_io_in_4_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_crossPageIPFFix;
  endfunction

  function void set_io_in_4_bits_crossPageIPFFixxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_crossPageIPFFix=value;
  endfunction

  function void get_io_in_4_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_ftqPtr_flag;
  endfunction

  function void set_io_in_4_bits_ftqPtr_flagxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_ftqPtr_flag=value;
  endfunction

  function void get_io_in_4_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_in_4_bits_ftqPtr_value;
  endfunction

  function void set_io_in_4_bits_ftqPtr_valuexxPfBDHOAJXyl;
    input logic [5:0] value;
    io_in_4_bits_ftqPtr_value=value;
  endfunction

  function void get_io_in_4_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_4_bits_ftqOffset;
  endfunction

  function void set_io_in_4_bits_ftqOffsetxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_4_bits_ftqOffset=value;
  endfunction

  function void get_io_in_4_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_4_bits_isLastInFtqEntry;
  endfunction

  function void set_io_in_4_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    input logic  value;
    io_in_4_bits_isLastInFtqEntry=value;
  endfunction

  function void get_io_in_5_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_ready;
  endfunction

  function void get_io_in_5_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_valid;
  endfunction

  function void set_io_in_5_validxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_valid=value;
  endfunction

  function void get_io_in_5_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_in_5_bits_instr;
  endfunction

  function void set_io_in_5_bits_instrxxPfBDHOAJXyl;
    input logic [31:0] value;
    io_in_5_bits_instr=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_0;
  endfunction

  function void set_io_in_5_bits_exceptionVec_0xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_0=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_1;
  endfunction

  function void set_io_in_5_bits_exceptionVec_1xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_1=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_2;
  endfunction

  function void set_io_in_5_bits_exceptionVec_2xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_2=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_4;
  endfunction

  function void set_io_in_5_bits_exceptionVec_4xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_4=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_5;
  endfunction

  function void set_io_in_5_bits_exceptionVec_5xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_5=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_6;
  endfunction

  function void set_io_in_5_bits_exceptionVec_6xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_6=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_7;
  endfunction

  function void set_io_in_5_bits_exceptionVec_7xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_7=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_8;
  endfunction

  function void set_io_in_5_bits_exceptionVec_8xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_8=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_9;
  endfunction

  function void set_io_in_5_bits_exceptionVec_9xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_9=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_10;
  endfunction

  function void set_io_in_5_bits_exceptionVec_10xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_10=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_11;
  endfunction

  function void set_io_in_5_bits_exceptionVec_11xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_11=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_12;
  endfunction

  function void set_io_in_5_bits_exceptionVec_12xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_12=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_13;
  endfunction

  function void set_io_in_5_bits_exceptionVec_13xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_13=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_14;
  endfunction

  function void set_io_in_5_bits_exceptionVec_14xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_14=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_15;
  endfunction

  function void set_io_in_5_bits_exceptionVec_15xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_15=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_16;
  endfunction

  function void set_io_in_5_bits_exceptionVec_16xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_16=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_17;
  endfunction

  function void set_io_in_5_bits_exceptionVec_17xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_17=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_18;
  endfunction

  function void set_io_in_5_bits_exceptionVec_18xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_18=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_19;
  endfunction

  function void set_io_in_5_bits_exceptionVec_19xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_19=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_20;
  endfunction

  function void set_io_in_5_bits_exceptionVec_20xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_20=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_21;
  endfunction

  function void set_io_in_5_bits_exceptionVec_21xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_21=value;
  endfunction

  function void get_io_in_5_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_exceptionVec_23;
  endfunction

  function void set_io_in_5_bits_exceptionVec_23xxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_exceptionVec_23=value;
  endfunction

  function void get_io_in_5_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_isFetchMalAddr;
  endfunction

  function void set_io_in_5_bits_isFetchMalAddrxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_isFetchMalAddr=value;
  endfunction

  function void get_io_in_5_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_5_bits_trigger;
  endfunction

  function void set_io_in_5_bits_triggerxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_5_bits_trigger=value;
  endfunction

  function void get_io_in_5_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_preDecodeInfo_isRVC;
  endfunction

  function void set_io_in_5_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_preDecodeInfo_isRVC=value;
  endfunction

  function void get_io_in_5_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_in_5_bits_preDecodeInfo_brType;
  endfunction

  function void set_io_in_5_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    input logic [1:0] value;
    io_in_5_bits_preDecodeInfo_brType=value;
  endfunction

  function void get_io_in_5_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_pred_taken;
  endfunction

  function void set_io_in_5_bits_pred_takenxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_pred_taken=value;
  endfunction

  function void get_io_in_5_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_crossPageIPFFix;
  endfunction

  function void set_io_in_5_bits_crossPageIPFFixxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_crossPageIPFFix=value;
  endfunction

  function void get_io_in_5_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_ftqPtr_flag;
  endfunction

  function void set_io_in_5_bits_ftqPtr_flagxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_ftqPtr_flag=value;
  endfunction

  function void get_io_in_5_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_in_5_bits_ftqPtr_value;
  endfunction

  function void set_io_in_5_bits_ftqPtr_valuexxPfBDHOAJXyl;
    input logic [5:0] value;
    io_in_5_bits_ftqPtr_value=value;
  endfunction

  function void get_io_in_5_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_in_5_bits_ftqOffset;
  endfunction

  function void set_io_in_5_bits_ftqOffsetxxPfBDHOAJXyl;
    input logic [3:0] value;
    io_in_5_bits_ftqOffset=value;
  endfunction

  function void get_io_in_5_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    output logic  value;
    value=io_in_5_bits_isLastInFtqEntry;
  endfunction

  function void set_io_in_5_bits_isLastInFtqEntryxxPfBDHOAJXyl;
    input logic  value;
    io_in_5_bits_isLastInFtqEntry=value;
  endfunction

  function void get_io_out_0_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_ready;
  endfunction

  function void set_io_out_0_readyxxPfBDHOAJXyl;
    input logic  value;
    io_out_0_ready=value;
  endfunction

  function void get_io_out_0_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_valid;
  endfunction

  function void get_io_out_0_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_out_0_bits_instr;
  endfunction

  function void get_io_out_0_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_0;
  endfunction

  function void get_io_out_0_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_1;
  endfunction

  function void get_io_out_0_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_2;
  endfunction

  function void get_io_out_0_bits_exceptionVec_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_3;
  endfunction

  function void get_io_out_0_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_4;
  endfunction

  function void get_io_out_0_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_5;
  endfunction

  function void get_io_out_0_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_6;
  endfunction

  function void get_io_out_0_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_7;
  endfunction

  function void get_io_out_0_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_8;
  endfunction

  function void get_io_out_0_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_9;
  endfunction

  function void get_io_out_0_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_10;
  endfunction

  function void get_io_out_0_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_11;
  endfunction

  function void get_io_out_0_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_12;
  endfunction

  function void get_io_out_0_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_13;
  endfunction

  function void get_io_out_0_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_14;
  endfunction

  function void get_io_out_0_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_15;
  endfunction

  function void get_io_out_0_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_16;
  endfunction

  function void get_io_out_0_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_17;
  endfunction

  function void get_io_out_0_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_18;
  endfunction

  function void get_io_out_0_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_19;
  endfunction

  function void get_io_out_0_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_20;
  endfunction

  function void get_io_out_0_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_21;
  endfunction

  function void get_io_out_0_bits_exceptionVec_22xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_22;
  endfunction

  function void get_io_out_0_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_exceptionVec_23;
  endfunction

  function void get_io_out_0_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_isFetchMalAddr;
  endfunction

  function void get_io_out_0_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_trigger;
  endfunction

  function void get_io_out_0_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_preDecodeInfo_isRVC;
  endfunction

  function void get_io_out_0_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_preDecodeInfo_brType;
  endfunction

  function void get_io_out_0_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_pred_taken;
  endfunction

  function void get_io_out_0_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_crossPageIPFFix;
  endfunction

  function void get_io_out_0_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_ftqPtr_flag;
  endfunction

  function void get_io_out_0_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_0_bits_ftqPtr_value;
  endfunction

  function void get_io_out_0_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_ftqOffset;
  endfunction

  function void get_io_out_0_bits_srcType_0xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_srcType_0;
  endfunction

  function void get_io_out_0_bits_srcType_1xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_srcType_1;
  endfunction

  function void get_io_out_0_bits_srcType_2xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_srcType_2;
  endfunction

  function void get_io_out_0_bits_srcType_3xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_srcType_3;
  endfunction

  function void get_io_out_0_bits_srcType_4xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_srcType_4;
  endfunction

  function void get_io_out_0_bits_lsrc_0xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_0_bits_lsrc_0;
  endfunction

  function void get_io_out_0_bits_lsrc_1xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_0_bits_lsrc_1;
  endfunction

  function void get_io_out_0_bits_lsrc_2xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_0_bits_lsrc_2;
  endfunction

  function void get_io_out_0_bits_ldestxxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_0_bits_ldest;
  endfunction

  function void get_io_out_0_bits_fuTypexxPfBDHOAJXyl;
    output logic [34:0] value;
    value=io_out_0_bits_fuType;
  endfunction

  function void get_io_out_0_bits_fuOpTypexxPfBDHOAJXyl;
    output logic [8:0] value;
    value=io_out_0_bits_fuOpType;
  endfunction

  function void get_io_out_0_bits_rfWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_rfWen;
  endfunction

  function void get_io_out_0_bits_fpWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_fpWen;
  endfunction

  function void get_io_out_0_bits_vecWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vecWen;
  endfunction

  function void get_io_out_0_bits_v0WenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_v0Wen;
  endfunction

  function void get_io_out_0_bits_vlWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vlWen;
  endfunction

  function void get_io_out_0_bits_isXSTrapxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_isXSTrap;
  endfunction

  function void get_io_out_0_bits_waitForwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_waitForward;
  endfunction

  function void get_io_out_0_bits_blockBackwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_blockBackward;
  endfunction

  function void get_io_out_0_bits_flushPipexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_flushPipe;
  endfunction

  function void get_io_out_0_bits_canRobCompressxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_canRobCompress;
  endfunction

  function void get_io_out_0_bits_selImmxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_0_bits_selImm;
  endfunction

  function void get_io_out_0_bits_immxxPfBDHOAJXyl;
    output logic [21:0] value;
    value=io_out_0_bits_imm;
  endfunction

  function void get_io_out_0_bits_fpu_typeTagOutxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_fpu_typeTagOut;
  endfunction

  function void get_io_out_0_bits_fpu_wflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_fpu_wflags;
  endfunction

  function void get_io_out_0_bits_fpu_typxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_fpu_typ;
  endfunction

  function void get_io_out_0_bits_fpu_fmtxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_fpu_fmt;
  endfunction

  function void get_io_out_0_bits_fpu_rmxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_0_bits_fpu_rm;
  endfunction

  function void get_io_out_0_bits_vpu_villxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_vill;
  endfunction

  function void get_io_out_0_bits_vpu_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_vma;
  endfunction

  function void get_io_out_0_bits_vpu_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_vta;
  endfunction

  function void get_io_out_0_bits_vpu_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_vpu_vsew;
  endfunction

  function void get_io_out_0_bits_vpu_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_0_bits_vpu_vlmul;
  endfunction

  function void get_io_out_0_bits_vpu_specVillxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_specVill;
  endfunction

  function void get_io_out_0_bits_vpu_specVmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_specVma;
  endfunction

  function void get_io_out_0_bits_vpu_specVtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_specVta;
  endfunction

  function void get_io_out_0_bits_vpu_specVsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_vpu_specVsew;
  endfunction

  function void get_io_out_0_bits_vpu_specVlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_0_bits_vpu_specVlmul;
  endfunction

  function void get_io_out_0_bits_vpu_vmxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_vm;
  endfunction

  function void get_io_out_0_bits_vpu_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_out_0_bits_vpu_vstart;
  endfunction

  function void get_io_out_0_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_fpu_isFoldTo1_2;
  endfunction

  function void get_io_out_0_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_fpu_isFoldTo1_4;
  endfunction

  function void get_io_out_0_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_fpu_isFoldTo1_8;
  endfunction

  function void get_io_out_0_bits_vpu_nfxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_0_bits_vpu_nf;
  endfunction

  function void get_io_out_0_bits_vpu_veewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_0_bits_vpu_veew;
  endfunction

  function void get_io_out_0_bits_vpu_isExtxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isExt;
  endfunction

  function void get_io_out_0_bits_vpu_isNarrowxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isNarrow;
  endfunction

  function void get_io_out_0_bits_vpu_isDstMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isDstMask;
  endfunction

  function void get_io_out_0_bits_vpu_isOpMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isOpMask;
  endfunction

  function void get_io_out_0_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isDependOldVd;
  endfunction

  function void get_io_out_0_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isWritePartVd;
  endfunction

  function void get_io_out_0_bits_vpu_isVleffxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vpu_isVleff;
  endfunction

  function void get_io_out_0_bits_vlsInstrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_vlsInstr;
  endfunction

  function void get_io_out_0_bits_wfflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_wfflags;
  endfunction

  function void get_io_out_0_bits_isMovexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_isMove;
  endfunction

  function void get_io_out_0_bits_uopIdxxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_0_bits_uopIdx;
  endfunction

  function void get_io_out_0_bits_uopSplitTypexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_0_bits_uopSplitType;
  endfunction

  function void get_io_out_0_bits_isVsetxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_isVset;
  endfunction

  function void get_io_out_0_bits_firstUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_firstUop;
  endfunction

  function void get_io_out_0_bits_lastUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_0_bits_lastUop;
  endfunction

  function void get_io_out_0_bits_numWBxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_0_bits_numWB;
  endfunction

  function void get_io_out_0_bits_commitTypexxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_0_bits_commitType;
  endfunction

  function void get_io_out_1_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_ready;
  endfunction

  function void set_io_out_1_readyxxPfBDHOAJXyl;
    input logic  value;
    io_out_1_ready=value;
  endfunction

  function void get_io_out_1_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_valid;
  endfunction

  function void get_io_out_1_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_out_1_bits_instr;
  endfunction

  function void get_io_out_1_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_0;
  endfunction

  function void get_io_out_1_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_1;
  endfunction

  function void get_io_out_1_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_2;
  endfunction

  function void get_io_out_1_bits_exceptionVec_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_3;
  endfunction

  function void get_io_out_1_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_4;
  endfunction

  function void get_io_out_1_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_5;
  endfunction

  function void get_io_out_1_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_6;
  endfunction

  function void get_io_out_1_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_7;
  endfunction

  function void get_io_out_1_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_8;
  endfunction

  function void get_io_out_1_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_9;
  endfunction

  function void get_io_out_1_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_10;
  endfunction

  function void get_io_out_1_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_11;
  endfunction

  function void get_io_out_1_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_12;
  endfunction

  function void get_io_out_1_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_13;
  endfunction

  function void get_io_out_1_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_14;
  endfunction

  function void get_io_out_1_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_15;
  endfunction

  function void get_io_out_1_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_16;
  endfunction

  function void get_io_out_1_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_17;
  endfunction

  function void get_io_out_1_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_18;
  endfunction

  function void get_io_out_1_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_19;
  endfunction

  function void get_io_out_1_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_20;
  endfunction

  function void get_io_out_1_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_21;
  endfunction

  function void get_io_out_1_bits_exceptionVec_22xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_22;
  endfunction

  function void get_io_out_1_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_exceptionVec_23;
  endfunction

  function void get_io_out_1_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_isFetchMalAddr;
  endfunction

  function void get_io_out_1_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_trigger;
  endfunction

  function void get_io_out_1_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_preDecodeInfo_isRVC;
  endfunction

  function void get_io_out_1_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_preDecodeInfo_brType;
  endfunction

  function void get_io_out_1_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_pred_taken;
  endfunction

  function void get_io_out_1_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_crossPageIPFFix;
  endfunction

  function void get_io_out_1_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_ftqPtr_flag;
  endfunction

  function void get_io_out_1_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_1_bits_ftqPtr_value;
  endfunction

  function void get_io_out_1_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_ftqOffset;
  endfunction

  function void get_io_out_1_bits_srcType_0xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_srcType_0;
  endfunction

  function void get_io_out_1_bits_srcType_1xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_srcType_1;
  endfunction

  function void get_io_out_1_bits_srcType_2xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_srcType_2;
  endfunction

  function void get_io_out_1_bits_srcType_3xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_srcType_3;
  endfunction

  function void get_io_out_1_bits_srcType_4xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_srcType_4;
  endfunction

  function void get_io_out_1_bits_lsrc_0xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_1_bits_lsrc_0;
  endfunction

  function void get_io_out_1_bits_lsrc_1xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_1_bits_lsrc_1;
  endfunction

  function void get_io_out_1_bits_lsrc_2xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_1_bits_lsrc_2;
  endfunction

  function void get_io_out_1_bits_ldestxxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_1_bits_ldest;
  endfunction

  function void get_io_out_1_bits_fuTypexxPfBDHOAJXyl;
    output logic [34:0] value;
    value=io_out_1_bits_fuType;
  endfunction

  function void get_io_out_1_bits_fuOpTypexxPfBDHOAJXyl;
    output logic [8:0] value;
    value=io_out_1_bits_fuOpType;
  endfunction

  function void get_io_out_1_bits_rfWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_rfWen;
  endfunction

  function void get_io_out_1_bits_fpWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_fpWen;
  endfunction

  function void get_io_out_1_bits_vecWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vecWen;
  endfunction

  function void get_io_out_1_bits_v0WenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_v0Wen;
  endfunction

  function void get_io_out_1_bits_vlWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vlWen;
  endfunction

  function void get_io_out_1_bits_isXSTrapxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_isXSTrap;
  endfunction

  function void get_io_out_1_bits_waitForwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_waitForward;
  endfunction

  function void get_io_out_1_bits_blockBackwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_blockBackward;
  endfunction

  function void get_io_out_1_bits_flushPipexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_flushPipe;
  endfunction

  function void get_io_out_1_bits_canRobCompressxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_canRobCompress;
  endfunction

  function void get_io_out_1_bits_selImmxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_1_bits_selImm;
  endfunction

  function void get_io_out_1_bits_immxxPfBDHOAJXyl;
    output logic [21:0] value;
    value=io_out_1_bits_imm;
  endfunction

  function void get_io_out_1_bits_fpu_typeTagOutxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_fpu_typeTagOut;
  endfunction

  function void get_io_out_1_bits_fpu_wflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_fpu_wflags;
  endfunction

  function void get_io_out_1_bits_fpu_typxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_fpu_typ;
  endfunction

  function void get_io_out_1_bits_fpu_fmtxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_fpu_fmt;
  endfunction

  function void get_io_out_1_bits_fpu_rmxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_1_bits_fpu_rm;
  endfunction

  function void get_io_out_1_bits_vpu_villxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_vill;
  endfunction

  function void get_io_out_1_bits_vpu_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_vma;
  endfunction

  function void get_io_out_1_bits_vpu_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_vta;
  endfunction

  function void get_io_out_1_bits_vpu_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_vpu_vsew;
  endfunction

  function void get_io_out_1_bits_vpu_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_1_bits_vpu_vlmul;
  endfunction

  function void get_io_out_1_bits_vpu_specVillxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_specVill;
  endfunction

  function void get_io_out_1_bits_vpu_specVmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_specVma;
  endfunction

  function void get_io_out_1_bits_vpu_specVtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_specVta;
  endfunction

  function void get_io_out_1_bits_vpu_specVsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_vpu_specVsew;
  endfunction

  function void get_io_out_1_bits_vpu_specVlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_1_bits_vpu_specVlmul;
  endfunction

  function void get_io_out_1_bits_vpu_vmxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_vm;
  endfunction

  function void get_io_out_1_bits_vpu_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_out_1_bits_vpu_vstart;
  endfunction

  function void get_io_out_1_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_fpu_isFoldTo1_2;
  endfunction

  function void get_io_out_1_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_fpu_isFoldTo1_4;
  endfunction

  function void get_io_out_1_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_fpu_isFoldTo1_8;
  endfunction

  function void get_io_out_1_bits_vpu_nfxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_1_bits_vpu_nf;
  endfunction

  function void get_io_out_1_bits_vpu_veewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_1_bits_vpu_veew;
  endfunction

  function void get_io_out_1_bits_vpu_isExtxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isExt;
  endfunction

  function void get_io_out_1_bits_vpu_isNarrowxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isNarrow;
  endfunction

  function void get_io_out_1_bits_vpu_isDstMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isDstMask;
  endfunction

  function void get_io_out_1_bits_vpu_isOpMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isOpMask;
  endfunction

  function void get_io_out_1_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isDependOldVd;
  endfunction

  function void get_io_out_1_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isWritePartVd;
  endfunction

  function void get_io_out_1_bits_vpu_isVleffxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vpu_isVleff;
  endfunction

  function void get_io_out_1_bits_vlsInstrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_vlsInstr;
  endfunction

  function void get_io_out_1_bits_wfflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_wfflags;
  endfunction

  function void get_io_out_1_bits_isMovexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_isMove;
  endfunction

  function void get_io_out_1_bits_uopIdxxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_1_bits_uopIdx;
  endfunction

  function void get_io_out_1_bits_uopSplitTypexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_1_bits_uopSplitType;
  endfunction

  function void get_io_out_1_bits_isVsetxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_isVset;
  endfunction

  function void get_io_out_1_bits_firstUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_firstUop;
  endfunction

  function void get_io_out_1_bits_lastUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_1_bits_lastUop;
  endfunction

  function void get_io_out_1_bits_numWBxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_1_bits_numWB;
  endfunction

  function void get_io_out_1_bits_commitTypexxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_1_bits_commitType;
  endfunction

  function void get_io_out_2_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_ready;
  endfunction

  function void set_io_out_2_readyxxPfBDHOAJXyl;
    input logic  value;
    io_out_2_ready=value;
  endfunction

  function void get_io_out_2_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_valid;
  endfunction

  function void get_io_out_2_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_out_2_bits_instr;
  endfunction

  function void get_io_out_2_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_0;
  endfunction

  function void get_io_out_2_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_1;
  endfunction

  function void get_io_out_2_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_2;
  endfunction

  function void get_io_out_2_bits_exceptionVec_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_3;
  endfunction

  function void get_io_out_2_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_4;
  endfunction

  function void get_io_out_2_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_5;
  endfunction

  function void get_io_out_2_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_6;
  endfunction

  function void get_io_out_2_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_7;
  endfunction

  function void get_io_out_2_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_8;
  endfunction

  function void get_io_out_2_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_9;
  endfunction

  function void get_io_out_2_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_10;
  endfunction

  function void get_io_out_2_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_11;
  endfunction

  function void get_io_out_2_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_12;
  endfunction

  function void get_io_out_2_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_13;
  endfunction

  function void get_io_out_2_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_14;
  endfunction

  function void get_io_out_2_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_15;
  endfunction

  function void get_io_out_2_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_16;
  endfunction

  function void get_io_out_2_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_17;
  endfunction

  function void get_io_out_2_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_18;
  endfunction

  function void get_io_out_2_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_19;
  endfunction

  function void get_io_out_2_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_20;
  endfunction

  function void get_io_out_2_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_21;
  endfunction

  function void get_io_out_2_bits_exceptionVec_22xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_22;
  endfunction

  function void get_io_out_2_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_exceptionVec_23;
  endfunction

  function void get_io_out_2_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_isFetchMalAddr;
  endfunction

  function void get_io_out_2_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_trigger;
  endfunction

  function void get_io_out_2_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_preDecodeInfo_isRVC;
  endfunction

  function void get_io_out_2_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_preDecodeInfo_brType;
  endfunction

  function void get_io_out_2_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_pred_taken;
  endfunction

  function void get_io_out_2_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_crossPageIPFFix;
  endfunction

  function void get_io_out_2_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_ftqPtr_flag;
  endfunction

  function void get_io_out_2_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_2_bits_ftqPtr_value;
  endfunction

  function void get_io_out_2_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_ftqOffset;
  endfunction

  function void get_io_out_2_bits_srcType_0xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_srcType_0;
  endfunction

  function void get_io_out_2_bits_srcType_1xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_srcType_1;
  endfunction

  function void get_io_out_2_bits_srcType_2xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_srcType_2;
  endfunction

  function void get_io_out_2_bits_srcType_3xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_srcType_3;
  endfunction

  function void get_io_out_2_bits_srcType_4xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_srcType_4;
  endfunction

  function void get_io_out_2_bits_lsrc_0xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_2_bits_lsrc_0;
  endfunction

  function void get_io_out_2_bits_lsrc_1xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_2_bits_lsrc_1;
  endfunction

  function void get_io_out_2_bits_lsrc_2xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_2_bits_lsrc_2;
  endfunction

  function void get_io_out_2_bits_ldestxxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_2_bits_ldest;
  endfunction

  function void get_io_out_2_bits_fuTypexxPfBDHOAJXyl;
    output logic [34:0] value;
    value=io_out_2_bits_fuType;
  endfunction

  function void get_io_out_2_bits_fuOpTypexxPfBDHOAJXyl;
    output logic [8:0] value;
    value=io_out_2_bits_fuOpType;
  endfunction

  function void get_io_out_2_bits_rfWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_rfWen;
  endfunction

  function void get_io_out_2_bits_fpWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_fpWen;
  endfunction

  function void get_io_out_2_bits_vecWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vecWen;
  endfunction

  function void get_io_out_2_bits_v0WenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_v0Wen;
  endfunction

  function void get_io_out_2_bits_vlWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vlWen;
  endfunction

  function void get_io_out_2_bits_isXSTrapxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_isXSTrap;
  endfunction

  function void get_io_out_2_bits_waitForwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_waitForward;
  endfunction

  function void get_io_out_2_bits_blockBackwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_blockBackward;
  endfunction

  function void get_io_out_2_bits_flushPipexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_flushPipe;
  endfunction

  function void get_io_out_2_bits_canRobCompressxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_canRobCompress;
  endfunction

  function void get_io_out_2_bits_selImmxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_2_bits_selImm;
  endfunction

  function void get_io_out_2_bits_immxxPfBDHOAJXyl;
    output logic [21:0] value;
    value=io_out_2_bits_imm;
  endfunction

  function void get_io_out_2_bits_fpu_typeTagOutxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_fpu_typeTagOut;
  endfunction

  function void get_io_out_2_bits_fpu_wflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_fpu_wflags;
  endfunction

  function void get_io_out_2_bits_fpu_typxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_fpu_typ;
  endfunction

  function void get_io_out_2_bits_fpu_fmtxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_fpu_fmt;
  endfunction

  function void get_io_out_2_bits_fpu_rmxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_2_bits_fpu_rm;
  endfunction

  function void get_io_out_2_bits_vpu_villxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_vill;
  endfunction

  function void get_io_out_2_bits_vpu_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_vma;
  endfunction

  function void get_io_out_2_bits_vpu_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_vta;
  endfunction

  function void get_io_out_2_bits_vpu_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_vpu_vsew;
  endfunction

  function void get_io_out_2_bits_vpu_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_2_bits_vpu_vlmul;
  endfunction

  function void get_io_out_2_bits_vpu_specVillxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_specVill;
  endfunction

  function void get_io_out_2_bits_vpu_specVmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_specVma;
  endfunction

  function void get_io_out_2_bits_vpu_specVtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_specVta;
  endfunction

  function void get_io_out_2_bits_vpu_specVsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_vpu_specVsew;
  endfunction

  function void get_io_out_2_bits_vpu_specVlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_2_bits_vpu_specVlmul;
  endfunction

  function void get_io_out_2_bits_vpu_vmxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_vm;
  endfunction

  function void get_io_out_2_bits_vpu_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_out_2_bits_vpu_vstart;
  endfunction

  function void get_io_out_2_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_fpu_isFoldTo1_2;
  endfunction

  function void get_io_out_2_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_fpu_isFoldTo1_4;
  endfunction

  function void get_io_out_2_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_fpu_isFoldTo1_8;
  endfunction

  function void get_io_out_2_bits_vpu_nfxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_2_bits_vpu_nf;
  endfunction

  function void get_io_out_2_bits_vpu_veewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_2_bits_vpu_veew;
  endfunction

  function void get_io_out_2_bits_vpu_isExtxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isExt;
  endfunction

  function void get_io_out_2_bits_vpu_isNarrowxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isNarrow;
  endfunction

  function void get_io_out_2_bits_vpu_isDstMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isDstMask;
  endfunction

  function void get_io_out_2_bits_vpu_isOpMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isOpMask;
  endfunction

  function void get_io_out_2_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isDependOldVd;
  endfunction

  function void get_io_out_2_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isWritePartVd;
  endfunction

  function void get_io_out_2_bits_vpu_isVleffxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vpu_isVleff;
  endfunction

  function void get_io_out_2_bits_vlsInstrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_vlsInstr;
  endfunction

  function void get_io_out_2_bits_wfflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_wfflags;
  endfunction

  function void get_io_out_2_bits_isMovexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_isMove;
  endfunction

  function void get_io_out_2_bits_uopIdxxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_2_bits_uopIdx;
  endfunction

  function void get_io_out_2_bits_uopSplitTypexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_2_bits_uopSplitType;
  endfunction

  function void get_io_out_2_bits_isVsetxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_isVset;
  endfunction

  function void get_io_out_2_bits_firstUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_firstUop;
  endfunction

  function void get_io_out_2_bits_lastUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_2_bits_lastUop;
  endfunction

  function void get_io_out_2_bits_numWBxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_2_bits_numWB;
  endfunction

  function void get_io_out_2_bits_commitTypexxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_2_bits_commitType;
  endfunction

  function void get_io_out_3_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_ready;
  endfunction

  function void set_io_out_3_readyxxPfBDHOAJXyl;
    input logic  value;
    io_out_3_ready=value;
  endfunction

  function void get_io_out_3_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_valid;
  endfunction

  function void get_io_out_3_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_out_3_bits_instr;
  endfunction

  function void get_io_out_3_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_0;
  endfunction

  function void get_io_out_3_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_1;
  endfunction

  function void get_io_out_3_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_2;
  endfunction

  function void get_io_out_3_bits_exceptionVec_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_3;
  endfunction

  function void get_io_out_3_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_4;
  endfunction

  function void get_io_out_3_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_5;
  endfunction

  function void get_io_out_3_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_6;
  endfunction

  function void get_io_out_3_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_7;
  endfunction

  function void get_io_out_3_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_8;
  endfunction

  function void get_io_out_3_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_9;
  endfunction

  function void get_io_out_3_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_10;
  endfunction

  function void get_io_out_3_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_11;
  endfunction

  function void get_io_out_3_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_12;
  endfunction

  function void get_io_out_3_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_13;
  endfunction

  function void get_io_out_3_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_14;
  endfunction

  function void get_io_out_3_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_15;
  endfunction

  function void get_io_out_3_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_16;
  endfunction

  function void get_io_out_3_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_17;
  endfunction

  function void get_io_out_3_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_18;
  endfunction

  function void get_io_out_3_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_19;
  endfunction

  function void get_io_out_3_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_20;
  endfunction

  function void get_io_out_3_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_21;
  endfunction

  function void get_io_out_3_bits_exceptionVec_22xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_22;
  endfunction

  function void get_io_out_3_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_exceptionVec_23;
  endfunction

  function void get_io_out_3_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_isFetchMalAddr;
  endfunction

  function void get_io_out_3_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_trigger;
  endfunction

  function void get_io_out_3_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_preDecodeInfo_isRVC;
  endfunction

  function void get_io_out_3_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_preDecodeInfo_brType;
  endfunction

  function void get_io_out_3_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_pred_taken;
  endfunction

  function void get_io_out_3_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_crossPageIPFFix;
  endfunction

  function void get_io_out_3_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_ftqPtr_flag;
  endfunction

  function void get_io_out_3_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_3_bits_ftqPtr_value;
  endfunction

  function void get_io_out_3_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_ftqOffset;
  endfunction

  function void get_io_out_3_bits_srcType_0xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_srcType_0;
  endfunction

  function void get_io_out_3_bits_srcType_1xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_srcType_1;
  endfunction

  function void get_io_out_3_bits_srcType_2xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_srcType_2;
  endfunction

  function void get_io_out_3_bits_srcType_3xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_srcType_3;
  endfunction

  function void get_io_out_3_bits_srcType_4xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_srcType_4;
  endfunction

  function void get_io_out_3_bits_lsrc_0xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_3_bits_lsrc_0;
  endfunction

  function void get_io_out_3_bits_lsrc_1xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_3_bits_lsrc_1;
  endfunction

  function void get_io_out_3_bits_lsrc_2xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_3_bits_lsrc_2;
  endfunction

  function void get_io_out_3_bits_ldestxxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_3_bits_ldest;
  endfunction

  function void get_io_out_3_bits_fuTypexxPfBDHOAJXyl;
    output logic [34:0] value;
    value=io_out_3_bits_fuType;
  endfunction

  function void get_io_out_3_bits_fuOpTypexxPfBDHOAJXyl;
    output logic [8:0] value;
    value=io_out_3_bits_fuOpType;
  endfunction

  function void get_io_out_3_bits_rfWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_rfWen;
  endfunction

  function void get_io_out_3_bits_fpWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_fpWen;
  endfunction

  function void get_io_out_3_bits_vecWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vecWen;
  endfunction

  function void get_io_out_3_bits_v0WenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_v0Wen;
  endfunction

  function void get_io_out_3_bits_vlWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vlWen;
  endfunction

  function void get_io_out_3_bits_isXSTrapxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_isXSTrap;
  endfunction

  function void get_io_out_3_bits_waitForwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_waitForward;
  endfunction

  function void get_io_out_3_bits_blockBackwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_blockBackward;
  endfunction

  function void get_io_out_3_bits_flushPipexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_flushPipe;
  endfunction

  function void get_io_out_3_bits_canRobCompressxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_canRobCompress;
  endfunction

  function void get_io_out_3_bits_selImmxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_3_bits_selImm;
  endfunction

  function void get_io_out_3_bits_immxxPfBDHOAJXyl;
    output logic [21:0] value;
    value=io_out_3_bits_imm;
  endfunction

  function void get_io_out_3_bits_fpu_typeTagOutxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_fpu_typeTagOut;
  endfunction

  function void get_io_out_3_bits_fpu_wflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_fpu_wflags;
  endfunction

  function void get_io_out_3_bits_fpu_typxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_fpu_typ;
  endfunction

  function void get_io_out_3_bits_fpu_fmtxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_fpu_fmt;
  endfunction

  function void get_io_out_3_bits_fpu_rmxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_3_bits_fpu_rm;
  endfunction

  function void get_io_out_3_bits_vpu_villxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_vill;
  endfunction

  function void get_io_out_3_bits_vpu_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_vma;
  endfunction

  function void get_io_out_3_bits_vpu_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_vta;
  endfunction

  function void get_io_out_3_bits_vpu_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_vpu_vsew;
  endfunction

  function void get_io_out_3_bits_vpu_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_3_bits_vpu_vlmul;
  endfunction

  function void get_io_out_3_bits_vpu_specVillxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_specVill;
  endfunction

  function void get_io_out_3_bits_vpu_specVmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_specVma;
  endfunction

  function void get_io_out_3_bits_vpu_specVtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_specVta;
  endfunction

  function void get_io_out_3_bits_vpu_specVsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_vpu_specVsew;
  endfunction

  function void get_io_out_3_bits_vpu_specVlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_3_bits_vpu_specVlmul;
  endfunction

  function void get_io_out_3_bits_vpu_vmxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_vm;
  endfunction

  function void get_io_out_3_bits_vpu_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_out_3_bits_vpu_vstart;
  endfunction

  function void get_io_out_3_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_fpu_isFoldTo1_2;
  endfunction

  function void get_io_out_3_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_fpu_isFoldTo1_4;
  endfunction

  function void get_io_out_3_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_fpu_isFoldTo1_8;
  endfunction

  function void get_io_out_3_bits_vpu_nfxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_3_bits_vpu_nf;
  endfunction

  function void get_io_out_3_bits_vpu_veewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_3_bits_vpu_veew;
  endfunction

  function void get_io_out_3_bits_vpu_isExtxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isExt;
  endfunction

  function void get_io_out_3_bits_vpu_isNarrowxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isNarrow;
  endfunction

  function void get_io_out_3_bits_vpu_isDstMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isDstMask;
  endfunction

  function void get_io_out_3_bits_vpu_isOpMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isOpMask;
  endfunction

  function void get_io_out_3_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isDependOldVd;
  endfunction

  function void get_io_out_3_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isWritePartVd;
  endfunction

  function void get_io_out_3_bits_vpu_isVleffxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vpu_isVleff;
  endfunction

  function void get_io_out_3_bits_vlsInstrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_vlsInstr;
  endfunction

  function void get_io_out_3_bits_wfflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_wfflags;
  endfunction

  function void get_io_out_3_bits_isMovexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_isMove;
  endfunction

  function void get_io_out_3_bits_uopIdxxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_3_bits_uopIdx;
  endfunction

  function void get_io_out_3_bits_uopSplitTypexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_3_bits_uopSplitType;
  endfunction

  function void get_io_out_3_bits_isVsetxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_isVset;
  endfunction

  function void get_io_out_3_bits_firstUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_firstUop;
  endfunction

  function void get_io_out_3_bits_lastUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_3_bits_lastUop;
  endfunction

  function void get_io_out_3_bits_numWBxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_3_bits_numWB;
  endfunction

  function void get_io_out_3_bits_commitTypexxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_3_bits_commitType;
  endfunction

  function void get_io_out_4_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_ready;
  endfunction

  function void set_io_out_4_readyxxPfBDHOAJXyl;
    input logic  value;
    io_out_4_ready=value;
  endfunction

  function void get_io_out_4_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_valid;
  endfunction

  function void get_io_out_4_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_out_4_bits_instr;
  endfunction

  function void get_io_out_4_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_0;
  endfunction

  function void get_io_out_4_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_1;
  endfunction

  function void get_io_out_4_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_2;
  endfunction

  function void get_io_out_4_bits_exceptionVec_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_3;
  endfunction

  function void get_io_out_4_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_4;
  endfunction

  function void get_io_out_4_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_5;
  endfunction

  function void get_io_out_4_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_6;
  endfunction

  function void get_io_out_4_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_7;
  endfunction

  function void get_io_out_4_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_8;
  endfunction

  function void get_io_out_4_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_9;
  endfunction

  function void get_io_out_4_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_10;
  endfunction

  function void get_io_out_4_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_11;
  endfunction

  function void get_io_out_4_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_12;
  endfunction

  function void get_io_out_4_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_13;
  endfunction

  function void get_io_out_4_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_14;
  endfunction

  function void get_io_out_4_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_15;
  endfunction

  function void get_io_out_4_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_16;
  endfunction

  function void get_io_out_4_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_17;
  endfunction

  function void get_io_out_4_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_18;
  endfunction

  function void get_io_out_4_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_19;
  endfunction

  function void get_io_out_4_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_20;
  endfunction

  function void get_io_out_4_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_21;
  endfunction

  function void get_io_out_4_bits_exceptionVec_22xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_22;
  endfunction

  function void get_io_out_4_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_exceptionVec_23;
  endfunction

  function void get_io_out_4_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_isFetchMalAddr;
  endfunction

  function void get_io_out_4_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_trigger;
  endfunction

  function void get_io_out_4_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_preDecodeInfo_isRVC;
  endfunction

  function void get_io_out_4_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_preDecodeInfo_brType;
  endfunction

  function void get_io_out_4_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_pred_taken;
  endfunction

  function void get_io_out_4_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_crossPageIPFFix;
  endfunction

  function void get_io_out_4_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_ftqPtr_flag;
  endfunction

  function void get_io_out_4_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_4_bits_ftqPtr_value;
  endfunction

  function void get_io_out_4_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_ftqOffset;
  endfunction

  function void get_io_out_4_bits_srcType_0xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_srcType_0;
  endfunction

  function void get_io_out_4_bits_srcType_1xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_srcType_1;
  endfunction

  function void get_io_out_4_bits_srcType_2xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_srcType_2;
  endfunction

  function void get_io_out_4_bits_srcType_3xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_srcType_3;
  endfunction

  function void get_io_out_4_bits_srcType_4xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_srcType_4;
  endfunction

  function void get_io_out_4_bits_lsrc_0xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_4_bits_lsrc_0;
  endfunction

  function void get_io_out_4_bits_lsrc_1xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_4_bits_lsrc_1;
  endfunction

  function void get_io_out_4_bits_lsrc_2xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_4_bits_lsrc_2;
  endfunction

  function void get_io_out_4_bits_ldestxxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_4_bits_ldest;
  endfunction

  function void get_io_out_4_bits_fuTypexxPfBDHOAJXyl;
    output logic [34:0] value;
    value=io_out_4_bits_fuType;
  endfunction

  function void get_io_out_4_bits_fuOpTypexxPfBDHOAJXyl;
    output logic [8:0] value;
    value=io_out_4_bits_fuOpType;
  endfunction

  function void get_io_out_4_bits_rfWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_rfWen;
  endfunction

  function void get_io_out_4_bits_fpWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_fpWen;
  endfunction

  function void get_io_out_4_bits_vecWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vecWen;
  endfunction

  function void get_io_out_4_bits_v0WenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_v0Wen;
  endfunction

  function void get_io_out_4_bits_vlWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vlWen;
  endfunction

  function void get_io_out_4_bits_isXSTrapxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_isXSTrap;
  endfunction

  function void get_io_out_4_bits_waitForwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_waitForward;
  endfunction

  function void get_io_out_4_bits_blockBackwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_blockBackward;
  endfunction

  function void get_io_out_4_bits_flushPipexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_flushPipe;
  endfunction

  function void get_io_out_4_bits_canRobCompressxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_canRobCompress;
  endfunction

  function void get_io_out_4_bits_selImmxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_4_bits_selImm;
  endfunction

  function void get_io_out_4_bits_immxxPfBDHOAJXyl;
    output logic [21:0] value;
    value=io_out_4_bits_imm;
  endfunction

  function void get_io_out_4_bits_fpu_typeTagOutxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_fpu_typeTagOut;
  endfunction

  function void get_io_out_4_bits_fpu_wflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_fpu_wflags;
  endfunction

  function void get_io_out_4_bits_fpu_typxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_fpu_typ;
  endfunction

  function void get_io_out_4_bits_fpu_fmtxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_fpu_fmt;
  endfunction

  function void get_io_out_4_bits_fpu_rmxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_4_bits_fpu_rm;
  endfunction

  function void get_io_out_4_bits_vpu_villxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_vill;
  endfunction

  function void get_io_out_4_bits_vpu_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_vma;
  endfunction

  function void get_io_out_4_bits_vpu_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_vta;
  endfunction

  function void get_io_out_4_bits_vpu_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_vpu_vsew;
  endfunction

  function void get_io_out_4_bits_vpu_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_4_bits_vpu_vlmul;
  endfunction

  function void get_io_out_4_bits_vpu_specVillxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_specVill;
  endfunction

  function void get_io_out_4_bits_vpu_specVmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_specVma;
  endfunction

  function void get_io_out_4_bits_vpu_specVtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_specVta;
  endfunction

  function void get_io_out_4_bits_vpu_specVsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_vpu_specVsew;
  endfunction

  function void get_io_out_4_bits_vpu_specVlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_4_bits_vpu_specVlmul;
  endfunction

  function void get_io_out_4_bits_vpu_vmxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_vm;
  endfunction

  function void get_io_out_4_bits_vpu_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_out_4_bits_vpu_vstart;
  endfunction

  function void get_io_out_4_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_fpu_isFoldTo1_2;
  endfunction

  function void get_io_out_4_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_fpu_isFoldTo1_4;
  endfunction

  function void get_io_out_4_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_fpu_isFoldTo1_8;
  endfunction

  function void get_io_out_4_bits_vpu_nfxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_4_bits_vpu_nf;
  endfunction

  function void get_io_out_4_bits_vpu_veewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_4_bits_vpu_veew;
  endfunction

  function void get_io_out_4_bits_vpu_isExtxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isExt;
  endfunction

  function void get_io_out_4_bits_vpu_isNarrowxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isNarrow;
  endfunction

  function void get_io_out_4_bits_vpu_isDstMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isDstMask;
  endfunction

  function void get_io_out_4_bits_vpu_isOpMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isOpMask;
  endfunction

  function void get_io_out_4_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isDependOldVd;
  endfunction

  function void get_io_out_4_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isWritePartVd;
  endfunction

  function void get_io_out_4_bits_vpu_isVleffxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vpu_isVleff;
  endfunction

  function void get_io_out_4_bits_vlsInstrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_vlsInstr;
  endfunction

  function void get_io_out_4_bits_wfflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_wfflags;
  endfunction

  function void get_io_out_4_bits_isMovexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_isMove;
  endfunction

  function void get_io_out_4_bits_uopIdxxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_4_bits_uopIdx;
  endfunction

  function void get_io_out_4_bits_uopSplitTypexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_4_bits_uopSplitType;
  endfunction

  function void get_io_out_4_bits_isVsetxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_isVset;
  endfunction

  function void get_io_out_4_bits_firstUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_firstUop;
  endfunction

  function void get_io_out_4_bits_lastUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_4_bits_lastUop;
  endfunction

  function void get_io_out_4_bits_numWBxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_4_bits_numWB;
  endfunction

  function void get_io_out_4_bits_commitTypexxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_4_bits_commitType;
  endfunction

  function void get_io_out_5_readyxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_ready;
  endfunction

  function void set_io_out_5_readyxxPfBDHOAJXyl;
    input logic  value;
    io_out_5_ready=value;
  endfunction

  function void get_io_out_5_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_valid;
  endfunction

  function void get_io_out_5_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_out_5_bits_instr;
  endfunction

  function void get_io_out_5_bits_exceptionVec_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_0;
  endfunction

  function void get_io_out_5_bits_exceptionVec_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_1;
  endfunction

  function void get_io_out_5_bits_exceptionVec_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_2;
  endfunction

  function void get_io_out_5_bits_exceptionVec_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_3;
  endfunction

  function void get_io_out_5_bits_exceptionVec_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_4;
  endfunction

  function void get_io_out_5_bits_exceptionVec_5xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_5;
  endfunction

  function void get_io_out_5_bits_exceptionVec_6xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_6;
  endfunction

  function void get_io_out_5_bits_exceptionVec_7xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_7;
  endfunction

  function void get_io_out_5_bits_exceptionVec_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_8;
  endfunction

  function void get_io_out_5_bits_exceptionVec_9xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_9;
  endfunction

  function void get_io_out_5_bits_exceptionVec_10xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_10;
  endfunction

  function void get_io_out_5_bits_exceptionVec_11xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_11;
  endfunction

  function void get_io_out_5_bits_exceptionVec_12xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_12;
  endfunction

  function void get_io_out_5_bits_exceptionVec_13xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_13;
  endfunction

  function void get_io_out_5_bits_exceptionVec_14xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_14;
  endfunction

  function void get_io_out_5_bits_exceptionVec_15xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_15;
  endfunction

  function void get_io_out_5_bits_exceptionVec_16xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_16;
  endfunction

  function void get_io_out_5_bits_exceptionVec_17xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_17;
  endfunction

  function void get_io_out_5_bits_exceptionVec_18xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_18;
  endfunction

  function void get_io_out_5_bits_exceptionVec_19xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_19;
  endfunction

  function void get_io_out_5_bits_exceptionVec_20xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_20;
  endfunction

  function void get_io_out_5_bits_exceptionVec_21xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_21;
  endfunction

  function void get_io_out_5_bits_exceptionVec_22xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_22;
  endfunction

  function void get_io_out_5_bits_exceptionVec_23xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_exceptionVec_23;
  endfunction

  function void get_io_out_5_bits_isFetchMalAddrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_isFetchMalAddr;
  endfunction

  function void get_io_out_5_bits_triggerxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_trigger;
  endfunction

  function void get_io_out_5_bits_preDecodeInfo_isRVCxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_preDecodeInfo_isRVC;
  endfunction

  function void get_io_out_5_bits_preDecodeInfo_brTypexxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_preDecodeInfo_brType;
  endfunction

  function void get_io_out_5_bits_pred_takenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_pred_taken;
  endfunction

  function void get_io_out_5_bits_crossPageIPFFixxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_crossPageIPFFix;
  endfunction

  function void get_io_out_5_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_ftqPtr_flag;
  endfunction

  function void get_io_out_5_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_5_bits_ftqPtr_value;
  endfunction

  function void get_io_out_5_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_ftqOffset;
  endfunction

  function void get_io_out_5_bits_srcType_0xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_srcType_0;
  endfunction

  function void get_io_out_5_bits_srcType_1xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_srcType_1;
  endfunction

  function void get_io_out_5_bits_srcType_2xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_srcType_2;
  endfunction

  function void get_io_out_5_bits_srcType_3xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_srcType_3;
  endfunction

  function void get_io_out_5_bits_srcType_4xxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_srcType_4;
  endfunction

  function void get_io_out_5_bits_lsrc_0xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_5_bits_lsrc_0;
  endfunction

  function void get_io_out_5_bits_lsrc_1xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_5_bits_lsrc_1;
  endfunction

  function void get_io_out_5_bits_lsrc_2xxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_5_bits_lsrc_2;
  endfunction

  function void get_io_out_5_bits_ldestxxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_5_bits_ldest;
  endfunction

  function void get_io_out_5_bits_fuTypexxPfBDHOAJXyl;
    output logic [34:0] value;
    value=io_out_5_bits_fuType;
  endfunction

  function void get_io_out_5_bits_fuOpTypexxPfBDHOAJXyl;
    output logic [8:0] value;
    value=io_out_5_bits_fuOpType;
  endfunction

  function void get_io_out_5_bits_rfWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_rfWen;
  endfunction

  function void get_io_out_5_bits_fpWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_fpWen;
  endfunction

  function void get_io_out_5_bits_vecWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vecWen;
  endfunction

  function void get_io_out_5_bits_v0WenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_v0Wen;
  endfunction

  function void get_io_out_5_bits_vlWenxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vlWen;
  endfunction

  function void get_io_out_5_bits_isXSTrapxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_isXSTrap;
  endfunction

  function void get_io_out_5_bits_waitForwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_waitForward;
  endfunction

  function void get_io_out_5_bits_blockBackwardxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_blockBackward;
  endfunction

  function void get_io_out_5_bits_flushPipexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_flushPipe;
  endfunction

  function void get_io_out_5_bits_canRobCompressxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_canRobCompress;
  endfunction

  function void get_io_out_5_bits_selImmxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_out_5_bits_selImm;
  endfunction

  function void get_io_out_5_bits_immxxPfBDHOAJXyl;
    output logic [21:0] value;
    value=io_out_5_bits_imm;
  endfunction

  function void get_io_out_5_bits_fpu_typeTagOutxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_fpu_typeTagOut;
  endfunction

  function void get_io_out_5_bits_fpu_wflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_fpu_wflags;
  endfunction

  function void get_io_out_5_bits_fpu_typxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_fpu_typ;
  endfunction

  function void get_io_out_5_bits_fpu_fmtxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_fpu_fmt;
  endfunction

  function void get_io_out_5_bits_fpu_rmxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_5_bits_fpu_rm;
  endfunction

  function void get_io_out_5_bits_vpu_villxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_vill;
  endfunction

  function void get_io_out_5_bits_vpu_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_vma;
  endfunction

  function void get_io_out_5_bits_vpu_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_vta;
  endfunction

  function void get_io_out_5_bits_vpu_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_vpu_vsew;
  endfunction

  function void get_io_out_5_bits_vpu_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_5_bits_vpu_vlmul;
  endfunction

  function void get_io_out_5_bits_vpu_specVillxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_specVill;
  endfunction

  function void get_io_out_5_bits_vpu_specVmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_specVma;
  endfunction

  function void get_io_out_5_bits_vpu_specVtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_specVta;
  endfunction

  function void get_io_out_5_bits_vpu_specVsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_vpu_specVsew;
  endfunction

  function void get_io_out_5_bits_vpu_specVlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_5_bits_vpu_specVlmul;
  endfunction

  function void get_io_out_5_bits_vpu_vmxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_vm;
  endfunction

  function void get_io_out_5_bits_vpu_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_out_5_bits_vpu_vstart;
  endfunction

  function void get_io_out_5_bits_vpu_fpu_isFoldTo1_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_fpu_isFoldTo1_2;
  endfunction

  function void get_io_out_5_bits_vpu_fpu_isFoldTo1_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_fpu_isFoldTo1_4;
  endfunction

  function void get_io_out_5_bits_vpu_fpu_isFoldTo1_8xxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_fpu_isFoldTo1_8;
  endfunction

  function void get_io_out_5_bits_vpu_nfxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_5_bits_vpu_nf;
  endfunction

  function void get_io_out_5_bits_vpu_veewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_out_5_bits_vpu_veew;
  endfunction

  function void get_io_out_5_bits_vpu_isExtxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isExt;
  endfunction

  function void get_io_out_5_bits_vpu_isNarrowxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isNarrow;
  endfunction

  function void get_io_out_5_bits_vpu_isDstMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isDstMask;
  endfunction

  function void get_io_out_5_bits_vpu_isOpMaskxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isOpMask;
  endfunction

  function void get_io_out_5_bits_vpu_isDependOldVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isDependOldVd;
  endfunction

  function void get_io_out_5_bits_vpu_isWritePartVdxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isWritePartVd;
  endfunction

  function void get_io_out_5_bits_vpu_isVleffxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vpu_isVleff;
  endfunction

  function void get_io_out_5_bits_vlsInstrxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_vlsInstr;
  endfunction

  function void get_io_out_5_bits_wfflagsxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_wfflags;
  endfunction

  function void get_io_out_5_bits_isMovexxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_isMove;
  endfunction

  function void get_io_out_5_bits_uopIdxxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_5_bits_uopIdx;
  endfunction

  function void get_io_out_5_bits_uopSplitTypexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_out_5_bits_uopSplitType;
  endfunction

  function void get_io_out_5_bits_isVsetxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_isVset;
  endfunction

  function void get_io_out_5_bits_firstUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_firstUop;
  endfunction

  function void get_io_out_5_bits_lastUopxxPfBDHOAJXyl;
    output logic  value;
    value=io_out_5_bits_lastUop;
  endfunction

  function void get_io_out_5_bits_numWBxxPfBDHOAJXyl;
    output logic [6:0] value;
    value=io_out_5_bits_numWB;
  endfunction

  function void get_io_out_5_bits_commitTypexxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_out_5_bits_commitType;
  endfunction

  function void get_io_intRat_0_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_0_0_hold;
  endfunction

  function void get_io_intRat_0_0_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_0_0_addr;
  endfunction

  function void get_io_intRat_0_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_0_1_hold;
  endfunction

  function void get_io_intRat_0_1_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_0_1_addr;
  endfunction

  function void get_io_intRat_1_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_1_0_hold;
  endfunction

  function void get_io_intRat_1_0_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_1_0_addr;
  endfunction

  function void get_io_intRat_1_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_1_1_hold;
  endfunction

  function void get_io_intRat_1_1_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_1_1_addr;
  endfunction

  function void get_io_intRat_2_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_2_0_hold;
  endfunction

  function void get_io_intRat_2_0_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_2_0_addr;
  endfunction

  function void get_io_intRat_2_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_2_1_hold;
  endfunction

  function void get_io_intRat_2_1_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_2_1_addr;
  endfunction

  function void get_io_intRat_3_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_3_0_hold;
  endfunction

  function void get_io_intRat_3_0_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_3_0_addr;
  endfunction

  function void get_io_intRat_3_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_3_1_hold;
  endfunction

  function void get_io_intRat_3_1_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_3_1_addr;
  endfunction

  function void get_io_intRat_4_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_4_0_hold;
  endfunction

  function void get_io_intRat_4_0_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_4_0_addr;
  endfunction

  function void get_io_intRat_4_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_4_1_hold;
  endfunction

  function void get_io_intRat_4_1_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_4_1_addr;
  endfunction

  function void get_io_intRat_5_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_5_0_hold;
  endfunction

  function void get_io_intRat_5_0_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_5_0_addr;
  endfunction

  function void get_io_intRat_5_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_intRat_5_1_hold;
  endfunction

  function void get_io_intRat_5_1_addrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_intRat_5_1_addr;
  endfunction

  function void get_io_fpRat_0_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_0_0_hold;
  endfunction

  function void get_io_fpRat_0_0_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_0_0_addr;
  endfunction

  function void get_io_fpRat_0_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_0_1_hold;
  endfunction

  function void get_io_fpRat_0_1_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_0_1_addr;
  endfunction

  function void get_io_fpRat_0_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_0_2_hold;
  endfunction

  function void get_io_fpRat_0_2_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_0_2_addr;
  endfunction

  function void get_io_fpRat_1_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_1_0_hold;
  endfunction

  function void get_io_fpRat_1_0_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_1_0_addr;
  endfunction

  function void get_io_fpRat_1_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_1_1_hold;
  endfunction

  function void get_io_fpRat_1_1_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_1_1_addr;
  endfunction

  function void get_io_fpRat_1_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_1_2_hold;
  endfunction

  function void get_io_fpRat_1_2_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_1_2_addr;
  endfunction

  function void get_io_fpRat_2_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_2_0_hold;
  endfunction

  function void get_io_fpRat_2_0_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_2_0_addr;
  endfunction

  function void get_io_fpRat_2_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_2_1_hold;
  endfunction

  function void get_io_fpRat_2_1_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_2_1_addr;
  endfunction

  function void get_io_fpRat_2_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_2_2_hold;
  endfunction

  function void get_io_fpRat_2_2_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_2_2_addr;
  endfunction

  function void get_io_fpRat_3_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_3_0_hold;
  endfunction

  function void get_io_fpRat_3_0_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_3_0_addr;
  endfunction

  function void get_io_fpRat_3_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_3_1_hold;
  endfunction

  function void get_io_fpRat_3_1_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_3_1_addr;
  endfunction

  function void get_io_fpRat_3_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_3_2_hold;
  endfunction

  function void get_io_fpRat_3_2_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_3_2_addr;
  endfunction

  function void get_io_fpRat_4_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_4_0_hold;
  endfunction

  function void get_io_fpRat_4_0_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_4_0_addr;
  endfunction

  function void get_io_fpRat_4_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_4_1_hold;
  endfunction

  function void get_io_fpRat_4_1_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_4_1_addr;
  endfunction

  function void get_io_fpRat_4_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_4_2_hold;
  endfunction

  function void get_io_fpRat_4_2_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_4_2_addr;
  endfunction

  function void get_io_fpRat_5_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_5_0_hold;
  endfunction

  function void get_io_fpRat_5_0_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_5_0_addr;
  endfunction

  function void get_io_fpRat_5_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_5_1_hold;
  endfunction

  function void get_io_fpRat_5_1_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_5_1_addr;
  endfunction

  function void get_io_fpRat_5_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_fpRat_5_2_hold;
  endfunction

  function void get_io_fpRat_5_2_addrxxPfBDHOAJXyl;
    output logic [33:0] value;
    value=io_fpRat_5_2_addr;
  endfunction

  function void get_io_vecRat_0_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_0_0_hold;
  endfunction

  function void get_io_vecRat_0_0_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_0_0_addr;
  endfunction

  function void get_io_vecRat_0_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_0_1_hold;
  endfunction

  function void get_io_vecRat_0_1_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_0_1_addr;
  endfunction

  function void get_io_vecRat_0_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_0_2_hold;
  endfunction

  function void get_io_vecRat_0_2_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_0_2_addr;
  endfunction

  function void get_io_vecRat_1_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_1_0_hold;
  endfunction

  function void get_io_vecRat_1_0_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_1_0_addr;
  endfunction

  function void get_io_vecRat_1_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_1_1_hold;
  endfunction

  function void get_io_vecRat_1_1_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_1_1_addr;
  endfunction

  function void get_io_vecRat_1_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_1_2_hold;
  endfunction

  function void get_io_vecRat_1_2_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_1_2_addr;
  endfunction

  function void get_io_vecRat_2_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_2_0_hold;
  endfunction

  function void get_io_vecRat_2_0_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_2_0_addr;
  endfunction

  function void get_io_vecRat_2_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_2_1_hold;
  endfunction

  function void get_io_vecRat_2_1_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_2_1_addr;
  endfunction

  function void get_io_vecRat_2_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_2_2_hold;
  endfunction

  function void get_io_vecRat_2_2_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_2_2_addr;
  endfunction

  function void get_io_vecRat_3_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_3_0_hold;
  endfunction

  function void get_io_vecRat_3_0_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_3_0_addr;
  endfunction

  function void get_io_vecRat_3_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_3_1_hold;
  endfunction

  function void get_io_vecRat_3_1_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_3_1_addr;
  endfunction

  function void get_io_vecRat_3_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_3_2_hold;
  endfunction

  function void get_io_vecRat_3_2_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_3_2_addr;
  endfunction

  function void get_io_vecRat_4_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_4_0_hold;
  endfunction

  function void get_io_vecRat_4_0_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_4_0_addr;
  endfunction

  function void get_io_vecRat_4_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_4_1_hold;
  endfunction

  function void get_io_vecRat_4_1_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_4_1_addr;
  endfunction

  function void get_io_vecRat_4_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_4_2_hold;
  endfunction

  function void get_io_vecRat_4_2_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_4_2_addr;
  endfunction

  function void get_io_vecRat_5_0_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_5_0_hold;
  endfunction

  function void get_io_vecRat_5_0_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_5_0_addr;
  endfunction

  function void get_io_vecRat_5_1_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_5_1_hold;
  endfunction

  function void get_io_vecRat_5_1_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_5_1_addr;
  endfunction

  function void get_io_vecRat_5_2_holdxxPfBDHOAJXyl;
    output logic  value;
    value=io_vecRat_5_2_hold;
  endfunction

  function void get_io_vecRat_5_2_addrxxPfBDHOAJXyl;
    output logic [46:0] value;
    value=io_vecRat_5_2_addr;
  endfunction

  function void get_io_csrCtrl_singlestepxxPfBDHOAJXyl;
    output logic  value;
    value=io_csrCtrl_singlestep;
  endfunction

  function void set_io_csrCtrl_singlestepxxPfBDHOAJXyl;
    input logic  value;
    io_csrCtrl_singlestep=value;
  endfunction

  function void get_io_fromCSR_illegalInst_sfenceVMAxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_sfenceVMA;
  endfunction

  function void set_io_fromCSR_illegalInst_sfenceVMAxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_sfenceVMA=value;
  endfunction

  function void get_io_fromCSR_illegalInst_sfencePartxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_sfencePart;
  endfunction

  function void set_io_fromCSR_illegalInst_sfencePartxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_sfencePart=value;
  endfunction

  function void get_io_fromCSR_illegalInst_hfenceGVMAxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_hfenceGVMA;
  endfunction

  function void set_io_fromCSR_illegalInst_hfenceGVMAxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_hfenceGVMA=value;
  endfunction

  function void get_io_fromCSR_illegalInst_hfenceVVMAxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_hfenceVVMA;
  endfunction

  function void set_io_fromCSR_illegalInst_hfenceVVMAxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_hfenceVVMA=value;
  endfunction

  function void get_io_fromCSR_illegalInst_hlsvxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_hlsv;
  endfunction

  function void set_io_fromCSR_illegalInst_hlsvxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_hlsv=value;
  endfunction

  function void get_io_fromCSR_illegalInst_fsIsOffxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_fsIsOff;
  endfunction

  function void set_io_fromCSR_illegalInst_fsIsOffxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_fsIsOff=value;
  endfunction

  function void get_io_fromCSR_illegalInst_vsIsOffxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_vsIsOff;
  endfunction

  function void set_io_fromCSR_illegalInst_vsIsOffxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_vsIsOff=value;
  endfunction

  function void get_io_fromCSR_illegalInst_wfixxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_wfi;
  endfunction

  function void set_io_fromCSR_illegalInst_wfixxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_wfi=value;
  endfunction

  function void get_io_fromCSR_illegalInst_frmxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_frm;
  endfunction

  function void set_io_fromCSR_illegalInst_frmxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_frm=value;
  endfunction

  function void get_io_fromCSR_illegalInst_cboZxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_cboZ;
  endfunction

  function void set_io_fromCSR_illegalInst_cboZxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_cboZ=value;
  endfunction

  function void get_io_fromCSR_illegalInst_cboCFxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_cboCF;
  endfunction

  function void set_io_fromCSR_illegalInst_cboCFxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_cboCF=value;
  endfunction

  function void get_io_fromCSR_illegalInst_cboIxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_illegalInst_cboI;
  endfunction

  function void set_io_fromCSR_illegalInst_cboIxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_illegalInst_cboI=value;
  endfunction

  function void get_io_fromCSR_virtualInst_sfenceVMAxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_sfenceVMA;
  endfunction

  function void set_io_fromCSR_virtualInst_sfenceVMAxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_sfenceVMA=value;
  endfunction

  function void get_io_fromCSR_virtualInst_sfencePartxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_sfencePart;
  endfunction

  function void set_io_fromCSR_virtualInst_sfencePartxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_sfencePart=value;
  endfunction

  function void get_io_fromCSR_virtualInst_hfencexxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_hfence;
  endfunction

  function void set_io_fromCSR_virtualInst_hfencexxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_hfence=value;
  endfunction

  function void get_io_fromCSR_virtualInst_hlsvxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_hlsv;
  endfunction

  function void set_io_fromCSR_virtualInst_hlsvxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_hlsv=value;
  endfunction

  function void get_io_fromCSR_virtualInst_wfixxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_wfi;
  endfunction

  function void set_io_fromCSR_virtualInst_wfixxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_wfi=value;
  endfunction

  function void get_io_fromCSR_virtualInst_cboZxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_cboZ;
  endfunction

  function void set_io_fromCSR_virtualInst_cboZxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_cboZ=value;
  endfunction

  function void get_io_fromCSR_virtualInst_cboCFxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_cboCF;
  endfunction

  function void set_io_fromCSR_virtualInst_cboCFxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_cboCF=value;
  endfunction

  function void get_io_fromCSR_virtualInst_cboIxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_virtualInst_cboI;
  endfunction

  function void set_io_fromCSR_virtualInst_cboIxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_virtualInst_cboI=value;
  endfunction

  function void get_io_fromCSR_special_cboI2FxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromCSR_special_cboI2F;
  endfunction

  function void set_io_fromCSR_special_cboI2FxxPfBDHOAJXyl;
    input logic  value;
    io_fromCSR_special_cboI2F=value;
  endfunction

  function void get_io_fusion_0xxPfBDHOAJXyl;
    output logic  value;
    value=io_fusion_0;
  endfunction

  function void set_io_fusion_0xxPfBDHOAJXyl;
    input logic  value;
    io_fusion_0=value;
  endfunction

  function void get_io_fusion_1xxPfBDHOAJXyl;
    output logic  value;
    value=io_fusion_1;
  endfunction

  function void set_io_fusion_1xxPfBDHOAJXyl;
    input logic  value;
    io_fusion_1=value;
  endfunction

  function void get_io_fusion_2xxPfBDHOAJXyl;
    output logic  value;
    value=io_fusion_2;
  endfunction

  function void set_io_fusion_2xxPfBDHOAJXyl;
    input logic  value;
    io_fusion_2=value;
  endfunction

  function void get_io_fusion_3xxPfBDHOAJXyl;
    output logic  value;
    value=io_fusion_3;
  endfunction

  function void set_io_fusion_3xxPfBDHOAJXyl;
    input logic  value;
    io_fusion_3=value;
  endfunction

  function void get_io_fusion_4xxPfBDHOAJXyl;
    output logic  value;
    value=io_fusion_4;
  endfunction

  function void set_io_fusion_4xxPfBDHOAJXyl;
    input logic  value;
    io_fusion_4=value;
  endfunction

  function void get_io_fromRob_isResumeVTypexxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_isResumeVType;
  endfunction

  function void set_io_fromRob_isResumeVTypexxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_isResumeVType=value;
  endfunction

  function void get_io_fromRob_walkToArchVTypexxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_walkToArchVType;
  endfunction

  function void set_io_fromRob_walkToArchVTypexxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_walkToArchVType=value;
  endfunction

  function void get_io_fromRob_commitVType_vtype_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_commitVType_vtype_valid;
  endfunction

  function void set_io_fromRob_commitVType_vtype_validxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_commitVType_vtype_valid=value;
  endfunction

  function void get_io_fromRob_commitVType_vtype_bits_illegalxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_commitVType_vtype_bits_illegal;
  endfunction

  function void set_io_fromRob_commitVType_vtype_bits_illegalxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_commitVType_vtype_bits_illegal=value;
  endfunction

  function void get_io_fromRob_commitVType_vtype_bits_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_commitVType_vtype_bits_vma;
  endfunction

  function void set_io_fromRob_commitVType_vtype_bits_vmaxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_commitVType_vtype_bits_vma=value;
  endfunction

  function void get_io_fromRob_commitVType_vtype_bits_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_commitVType_vtype_bits_vta;
  endfunction

  function void set_io_fromRob_commitVType_vtype_bits_vtaxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_commitVType_vtype_bits_vta=value;
  endfunction

  function void get_io_fromRob_commitVType_vtype_bits_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_fromRob_commitVType_vtype_bits_vsew;
  endfunction

  function void set_io_fromRob_commitVType_vtype_bits_vsewxxPfBDHOAJXyl;
    input logic [1:0] value;
    io_fromRob_commitVType_vtype_bits_vsew=value;
  endfunction

  function void get_io_fromRob_commitVType_vtype_bits_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_fromRob_commitVType_vtype_bits_vlmul;
  endfunction

  function void set_io_fromRob_commitVType_vtype_bits_vlmulxxPfBDHOAJXyl;
    input logic [2:0] value;
    io_fromRob_commitVType_vtype_bits_vlmul=value;
  endfunction

  function void get_io_fromRob_commitVType_hasVsetvlxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_commitVType_hasVsetvl;
  endfunction

  function void set_io_fromRob_commitVType_hasVsetvlxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_commitVType_hasVsetvl=value;
  endfunction

  function void get_io_fromRob_walkVType_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_walkVType_valid;
  endfunction

  function void set_io_fromRob_walkVType_validxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_walkVType_valid=value;
  endfunction

  function void get_io_fromRob_walkVType_bits_illegalxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_walkVType_bits_illegal;
  endfunction

  function void set_io_fromRob_walkVType_bits_illegalxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_walkVType_bits_illegal=value;
  endfunction

  function void get_io_fromRob_walkVType_bits_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_walkVType_bits_vma;
  endfunction

  function void set_io_fromRob_walkVType_bits_vmaxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_walkVType_bits_vma=value;
  endfunction

  function void get_io_fromRob_walkVType_bits_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_fromRob_walkVType_bits_vta;
  endfunction

  function void set_io_fromRob_walkVType_bits_vtaxxPfBDHOAJXyl;
    input logic  value;
    io_fromRob_walkVType_bits_vta=value;
  endfunction

  function void get_io_fromRob_walkVType_bits_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_fromRob_walkVType_bits_vsew;
  endfunction

  function void set_io_fromRob_walkVType_bits_vsewxxPfBDHOAJXyl;
    input logic [1:0] value;
    io_fromRob_walkVType_bits_vsew=value;
  endfunction

  function void get_io_fromRob_walkVType_bits_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_fromRob_walkVType_bits_vlmul;
  endfunction

  function void set_io_fromRob_walkVType_bits_vlmulxxPfBDHOAJXyl;
    input logic [2:0] value;
    io_fromRob_walkVType_bits_vlmul=value;
  endfunction

  function void get_io_vsetvlVType_illegalxxPfBDHOAJXyl;
    output logic  value;
    value=io_vsetvlVType_illegal;
  endfunction

  function void set_io_vsetvlVType_illegalxxPfBDHOAJXyl;
    input logic  value;
    io_vsetvlVType_illegal=value;
  endfunction

  function void get_io_vsetvlVType_vmaxxPfBDHOAJXyl;
    output logic  value;
    value=io_vsetvlVType_vma;
  endfunction

  function void set_io_vsetvlVType_vmaxxPfBDHOAJXyl;
    input logic  value;
    io_vsetvlVType_vma=value;
  endfunction

  function void get_io_vsetvlVType_vtaxxPfBDHOAJXyl;
    output logic  value;
    value=io_vsetvlVType_vta;
  endfunction

  function void set_io_vsetvlVType_vtaxxPfBDHOAJXyl;
    input logic  value;
    io_vsetvlVType_vta=value;
  endfunction

  function void get_io_vsetvlVType_vsewxxPfBDHOAJXyl;
    output logic [1:0] value;
    value=io_vsetvlVType_vsew;
  endfunction

  function void set_io_vsetvlVType_vsewxxPfBDHOAJXyl;
    input logic [1:0] value;
    io_vsetvlVType_vsew=value;
  endfunction

  function void get_io_vsetvlVType_vlmulxxPfBDHOAJXyl;
    output logic [2:0] value;
    value=io_vsetvlVType_vlmul;
  endfunction

  function void set_io_vsetvlVType_vlmulxxPfBDHOAJXyl;
    input logic [2:0] value;
    io_vsetvlVType_vlmul=value;
  endfunction

  function void get_io_vstartxxPfBDHOAJXyl;
    output logic [7:0] value;
    value=io_vstart;
  endfunction

  function void set_io_vstartxxPfBDHOAJXyl;
    input logic [7:0] value;
    io_vstart=value;
  endfunction

  function void get_io_toCSR_trapInstInfo_validxxPfBDHOAJXyl;
    output logic  value;
    value=io_toCSR_trapInstInfo_valid;
  endfunction

  function void get_io_toCSR_trapInstInfo_bits_instrxxPfBDHOAJXyl;
    output logic [31:0] value;
    value=io_toCSR_trapInstInfo_bits_instr;
  endfunction

  function void get_io_toCSR_trapInstInfo_bits_ftqPtr_flagxxPfBDHOAJXyl;
    output logic  value;
    value=io_toCSR_trapInstInfo_bits_ftqPtr_flag;
  endfunction

  function void get_io_toCSR_trapInstInfo_bits_ftqPtr_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_toCSR_trapInstInfo_bits_ftqPtr_value;
  endfunction

  function void get_io_toCSR_trapInstInfo_bits_ftqOffsetxxPfBDHOAJXyl;
    output logic [3:0] value;
    value=io_toCSR_trapInstInfo_bits_ftqOffset;
  endfunction

  function void get_io_perf_0_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_perf_0_value;
  endfunction

  function void get_io_perf_1_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_perf_1_value;
  endfunction

  function void get_io_perf_2_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_perf_2_value;
  endfunction

  function void get_io_perf_3_valuexxPfBDHOAJXyl;
    output logic [5:0] value;
    value=io_perf_3_value;
  endfunction



  initial begin
    $dumpfile("decode.fst");
    $dumpvars(0, DecodeStage_top);
  end

  export "DPI-C" function finish_PfBDHOAJXyl;
  function void finish_PfBDHOAJXyl;
    $finish;
  endfunction


endmodule
