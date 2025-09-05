from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_5, _4, _9, _6, _7 = Signals(5)

class _1Bundle(Bundle):
	_1, _2 = Signals(2)

class _2Bundle(Bundle):
	_3, _1, _2 = Signals(3)

class _3Bundle(Bundle):
	_new_value = _2Bundle.from_prefix("_new_value")
	_reverse_flag, _reverse_flag_3, _reverse_flag_1, _reverse_flag_2 = Signals(4)

class _4Bundle(Bundle):
	_flag, _value = Signals(2)

class _5Bundle(Bundle):
	_50, _21, _31, _8, _24, _46, _1, _48, _9, _33, _14, _3, _52, _6, _26, _35, _12, _10, _15, _25, _37, _19, _42, _5, _53, _44, _23, _4, _34, _43, _45, _7, _16, _32, _11, _38, _40, _47, _17, _27, _49, _51, _18, _39, _2, _28, _0, _41, _55, _29, _13, _54, _20, _36, _30, _22 = Signals(56)

class _6Bundle(Bundle):
	_50, _21, _31, _8, _24, _46, _48, _9, _33, _14, _3, _52, _6, _26, _35, _12, _10, _15, _25, _37, _19, _42, _5, _53, _44, _23, _4, _34, _43, _45, _7, _16, _32, _11, _38, _40, _47, _17, _27, _49, _51, _18, _39, _28, _0, _41, _55, _2, _1, _29, _13, _54, _20, _36, _30, _22, _2_50, _2_21, _2_31, _2_8, _2_24, _2_46, _2_1, _2_48, _2_9, _2_33, _2_14, _2_3, _2_52, _2_6, _2_26, _2_35, _2_12, _2_10, _2_15, _2_25, _2_37, _2_19, _2_42, _2_5, _2_53, _2_44, _2_23, _2_4, _2_34, _2_43, _2_45, _2_7, _2_16, _2_32, _2_11, _2_38, _2_40, _2_47, _2_17, _2_27, _2_49, _2_51, _2_18, _2_39, _2_2, _2_28, _2_0, _2_41, _2_55, _2_29, _2_13, _2_54, _2_20, _2_36, _2_30, _2_22, _1_50, _1_21, _1_31, _1_8, _1_24, _1_46, _1_1, _1_48, _1_9, _1_33, _1_14, _1_3, _1_52, _1_6, _1_26, _1_35, _1_12, _1_10, _1_15, _1_25, _1_37, _1_19, _1_42, _1_5, _1_53, _1_44, _1_23, _1_4, _1_34, _1_43, _1_45, _1_7, _1_16, _1_32, _1_11, _1_38, _1_40, _1_47, _1_17, _1_27, _1_49, _1_51, _1_18, _1_39, _1_2, _1_28, _1_0, _1_41, _1_55, _1_29, _1_13, _1_54, _1_20, _1_36, _1_30, _1_22 = Signals(168)

class _7Bundle(Bundle):
	_value = Signal()

class _8Bundle(Bundle):
	_5 = _7Bundle.from_prefix("_5")
	_1 = _7Bundle.from_prefix("_1")
	_2 = _7Bundle.from_prefix("_2")
	_4 = _7Bundle.from_prefix("_4")
	_6 = _7Bundle.from_prefix("_6")
	_3 = _7Bundle.from_prefix("_3")
	_7 = _7Bundle.from_prefix("_7")
	_0 = _4Bundle.from_prefix("_0")

class _9Bundle(Bundle):
	_0, _5, _1, _4, _2, _6, _3 = Signals(7)

class _10Bundle(Bundle):
	_0 = _4Bundle.from_prefix("_0")

class _11Bundle(Bundle):
	_5, _1, _4, _2, _3 = Signals(5)

class _12Bundle(Bundle):
	_0, _5, _compare, _differentFlag, _1, _4, _2, _3, _compare_5, _compare_1, _compare_4, _compare_2, _compare_3, _differentFlag_5, _differentFlag_1, _differentFlag_4, _differentFlag_2, _differentFlag_3 = Signals(18)

class _13Bundle(Bundle):
	_reverse_flag, _new_value, _reverse_flag_5, _reverse_flag_1, _reverse_flag_4, _reverse_flag_2, _reverse_flag_3, _new_value_5, _new_value_1, _new_value_4, _new_value_2, _new_value_3 = Signals(12)

class _14Bundle(Bundle):
	_50, _21, _31, _8, _24, _46, _1, _48, _9, _33, _14, _3, _52, _6, _26, _35, _12, _10, _15, _25, _37, _19, _42, _5, _53, _44, _23, _4, _34, _43, _45, _7, _16, _32, _11, _38, _40, _47, _17, _27, _49, _51, _18, _39, _2, _28, _41, _55, _29, _13, _54, _20, _36, _30, _22 = Signals(55)

class _15Bundle(Bundle):
	_1, _4, _0, _3, _2, _1_50, _1_21, _1_31, _1_8, _1_24, _1_46, _1_1, _1_48, _1_9, _1_33, _1_14, _1_3, _1_52, _1_6, _1_26, _1_35, _1_12, _1_10, _1_15, _1_25, _1_37, _1_19, _1_42, _1_5, _1_53, _1_44, _1_23, _1_4, _1_34, _1_43, _1_45, _1_7, _1_16, _1_32, _1_11, _1_38, _1_40, _1_47, _1_17, _1_27, _1_49, _1_51, _1_18, _1_39, _1_2, _1_28, _1_41, _1_55, _1_29, _1_13, _1_54, _1_20, _1_36, _1_30, _1_22, _4_50, _4_21, _4_31, _4_8, _4_24, _4_46, _4_1, _4_48, _4_9, _4_33, _4_14, _4_3, _4_52, _4_6, _4_26, _4_35, _4_12, _4_10, _4_15, _4_25, _4_37, _4_19, _4_42, _4_5, _4_53, _4_44, _4_23, _4_4, _4_34, _4_43, _4_45, _4_7, _4_16, _4_32, _4_11, _4_38, _4_40, _4_47, _4_17, _4_27, _4_49, _4_51, _4_18, _4_39, _4_2, _4_28, _4_41, _4_55, _4_29, _4_13, _4_54, _4_20, _4_36, _4_30, _4_22, _0_50, _0_21, _0_31, _0_8, _0_24, _0_46, _0_1, _0_48, _0_9, _0_33, _0_14, _0_3, _0_52, _0_6, _0_26, _0_35, _0_12, _0_10, _0_15, _0_25, _0_37, _0_19, _0_42, _0_5, _0_53, _0_44, _0_23, _0_4, _0_34, _0_43, _0_45, _0_7, _0_16, _0_32, _0_11, _0_38, _0_40, _0_47, _0_17, _0_27, _0_49, _0_51, _0_18, _0_39, _0_2, _0_28, _0_41, _0_55, _0_29, _0_13, _0_54, _0_20, _0_36, _0_30, _0_22, _3_50, _3_21, _3_31, _3_8, _3_24, _3_46, _3_1, _3_48, _3_9, _3_33, _3_14, _3_3, _3_52, _3_6, _3_26, _3_35, _3_12, _3_10, _3_15, _3_25, _3_37, _3_19, _3_42, _3_5, _3_53, _3_44, _3_23, _3_4, _3_34, _3_43, _3_45, _3_7, _3_16, _3_32, _3_11, _3_38, _3_40, _3_47, _3_17, _3_27, _3_49, _3_51, _3_18, _3_39, _3_2, _3_28, _3_41, _3_55, _3_29, _3_13, _3_54, _3_20, _3_36, _3_30, _3_22, _2_50, _2_21, _2_31, _2_8, _2_24, _2_46, _2_1, _2_48, _2_9, _2_33, _2_14, _2_3, _2_52, _2_6, _2_26, _2_35, _2_12, _2_10, _2_15, _2_25, _2_37, _2_19, _2_42, _2_5, _2_53, _2_44, _2_23, _2_4, _2_34, _2_43, _2_45, _2_7, _2_16, _2_32, _2_11, _2_38, _2_40, _2_47, _2_17, _2_27, _2_49, _2_51, _2_18, _2_39, _2_2, _2_28, _2_41, _2_55, _2_29, _2_13, _2_54, _2_20, _2_36, _2_30, _2_22 = Signals(280)

class _16Bundle(Bundle):
	_reverse_flag, _new_value = Signals(2)

class _17Bundle(Bundle):
	_0 = Signal()

class _18Bundle(Bundle):
	_REG, _r = Signals(2)

class _19Bundle(Bundle):
	_1 = _4Bundle.from_prefix("_1")
	_flag, _value = Signals(2)

class _20Bundle(Bundle):
	_flipped_new_ptr = _16Bundle.from_prefix("_flipped_new_ptr")
	_r = _19Bundle.from_prefix("_r")

class _21Bundle(Bundle):
	_addrInvalid = _18Bundle.from_prefix("_addrInvalid")
	_addrInvalidSqIdx = _20Bundle.from_prefix("_addrInvalidSqIdx")
	_dataInvalidSqIdx_r = _4Bundle.from_prefix("_dataInvalidSqIdx_r")
	_dataInvalid_REG = Signal()

class _22Bundle(Bundle):
	_0 = _21Bundle.from_prefix("_0")
	_1 = _21Bundle.from_prefix("_1")
	_2 = _21Bundle.from_prefix("_2")

class _23Bundle(Bundle):
	_flag = _17Bundle.from_prefix("_flag")
	_value = _17Bundle.from_prefix("_value")

class _24Bundle(Bundle):
	_1 = Signal()

class _27Bundle(Bundle):
	_forward = _22Bundle.from_prefix("_forward")
	_uncache_req_valid = _17Bundle.from_prefix("_uncache_req_valid")
	_cmoOpResp_ready = _17Bundle.from_prefix("_cmoOpResp_ready")
	_cmoOpReq_valid = _17Bundle.from_prefix("_cmoOpReq_valid")
	_mmioStout_valid = _17Bundle.from_prefix("_mmioStout_valid")
	_maControl_toStoreMisalignBuffer_uop_robIdx = _23Bundle.from_prefix("_maControl_toStoreMisalignBuffer_uop_robIdx")
	_force_write_REG, _sqDeq_REG, _sqEmpty_REG, _sqDeq_REG_1 = Signals(4)

class _28Bundle(Bundle):
	_bits_memBackTypeMM_next_r = _4Bundle.from_prefix("_bits_memBackTypeMM_next_r")
	_valid = Signal()

class _29Bundle(Bundle):
	_memBackTypeMM_next_r = _4Bundle.from_prefix("_memBackTypeMM_next_r")
	_id = Signal()

class _30Bundle(Bundle):
	_flag = Signal()

class _31Bundle(Bundle):
	_1 = _30Bundle.from_prefix("_1")
	_5 = _30Bundle.from_prefix("_5")

class _32Bundle(Bundle):
	_12, _10, _15, _16, _8, _5, _11, _13, _1, _4, _9, _2, _14, _3 = Signals(14)

class _33Bundle(Bundle):
	_ptr = _31Bundle.from_prefix("_ptr")
	_value, _value_12, _value_10, _value_15, _value_16, _value_8, _value_5, _value_11, _value_13, _value_1, _value_4, _value_9, _value_2, _value_14, _value_3 = Signals(15)

class _34Bundle(Bundle):
	_4 = _4Bundle.from_prefix("_4")
	_2 = _4Bundle.from_prefix("_2")
	_7 = _4Bundle.from_prefix("_7")
	_1 = _4Bundle.from_prefix("_1")
	_5 = _4Bundle.from_prefix("_5")
	_6 = _4Bundle.from_prefix("_6")
	_3 = _4Bundle.from_prefix("_3")
	_flag, _value = Signals(2)

class _37Bundle(Bundle):
	_50, _21, _31, _8, _24, _46, _48, _33, _6, _3, _52, _26, _35, _12, _10, _25, _37, _42, _19, _53, _44, _23, _4, _34, _43, _45, _7, _16, _32, _11, _38, _40, _47, _17, _27, _49, _5, _18, _39, _51, _2, _13, _28, _0, _41, _55, _15, _1, _14, _29, _54, _20, _36, _30, _9, _22, _5_0, _13_0, _15_0, _14_0, _9_0, _1_50, _1_21, _1_31, _1_8, _1_24, _1_46, _1_1, _1_48, _1_9, _1_33, _1_14, _1_3, _1_52, _1_6, _1_26, _1_35, _1_12, _1_10, _1_15, _1_25, _1_37, _1_19, _1_42, _1_5, _1_53, _1_44, _1_23, _1_4, _1_34, _1_43, _1_45, _1_7, _1_16, _1_32, _1_11, _1_38, _1_40, _1_47, _1_17, _1_27, _1_49, _1_51, _1_18, _1_39, _1_2, _1_28, _1_0, _1_41, _1_55, _1_29, _1_13, _1_54, _1_20, _1_36, _1_30, _1_22 = Signals(117)

class _38Bundle(Bundle):
	_1 = _7Bundle.from_prefix("_1")
	_0 = _4Bundle.from_prefix("_0")

class _39Bundle(Bundle):
	_16, _8, _5, _1, _4 = Signals(5)

class _40Bundle(Bundle):
	_2 = _4Bundle.from_prefix("_2")
	_1 = _4Bundle.from_prefix("_1")
	_flag, _value = Signals(2)

class _41Bundle(Bundle):
	_1 = _30Bundle.from_prefix("_1")
	_2 = _30Bundle.from_prefix("_2")
	_flag = Signal()

class _42Bundle(Bundle):
	_enqPtrExt = _41Bundle.from_prefix("_enqPtrExt")
	_deqPtrExt = _40Bundle.from_prefix("_deqPtrExt")
	_differentFlag, _differentFlag_1, _differentFlag_2 = Signals(3)

class _43Bundle(Bundle):
	_fuType = Signal()

class _44Bundle(Bundle):
	_14 = _43Bundle.from_prefix("_14")
	_41 = _43Bundle.from_prefix("_41")
	_39 = _43Bundle.from_prefix("_39")
	_1 = _43Bundle.from_prefix("_1")
	_7 = _43Bundle.from_prefix("_7")
	_24 = _43Bundle.from_prefix("_24")
	_36 = _43Bundle.from_prefix("_36")
	_28 = _43Bundle.from_prefix("_28")
	_52 = _43Bundle.from_prefix("_52")
	_32 = _43Bundle.from_prefix("_32")
	_10 = _43Bundle.from_prefix("_10")
	_11 = _43Bundle.from_prefix("_11")
	_2 = _43Bundle.from_prefix("_2")
	_40 = _43Bundle.from_prefix("_40")
	_43 = _43Bundle.from_prefix("_43")
	_6 = _43Bundle.from_prefix("_6")
	_46 = _43Bundle.from_prefix("_46")
	_12 = _43Bundle.from_prefix("_12")
	_27 = _43Bundle.from_prefix("_27")
	_45 = _43Bundle.from_prefix("_45")
	_38 = _43Bundle.from_prefix("_38")
	_34 = _43Bundle.from_prefix("_34")
	_13 = _43Bundle.from_prefix("_13")
	_8 = _43Bundle.from_prefix("_8")
	_3 = _43Bundle.from_prefix("_3")
	_25 = _43Bundle.from_prefix("_25")
	_26 = _43Bundle.from_prefix("_26")
	_44 = _43Bundle.from_prefix("_44")
	_19 = _43Bundle.from_prefix("_19")
	_16 = _43Bundle.from_prefix("_16")
	_33 = _43Bundle.from_prefix("_33")
	_15 = _43Bundle.from_prefix("_15")
	_18 = _43Bundle.from_prefix("_18")
	_29 = _43Bundle.from_prefix("_29")
	_50 = _43Bundle.from_prefix("_50")
	_22 = _43Bundle.from_prefix("_22")
	_21 = _43Bundle.from_prefix("_21")
	_51 = _43Bundle.from_prefix("_51")
	_47 = _43Bundle.from_prefix("_47")
	_49 = _43Bundle.from_prefix("_49")
	_17 = _43Bundle.from_prefix("_17")
	_54 = _43Bundle.from_prefix("_54")
	_31 = _43Bundle.from_prefix("_31")
	_55 = _43Bundle.from_prefix("_55")
	_9 = _43Bundle.from_prefix("_9")
	_48 = _43Bundle.from_prefix("_48")
	_37 = _43Bundle.from_prefix("_37")
	_53 = _43Bundle.from_prefix("_53")
	_5 = _43Bundle.from_prefix("_5")
	_42 = _43Bundle.from_prefix("_42")
	_23 = _43Bundle.from_prefix("_23")
	_20 = _43Bundle.from_prefix("_20")
	_30 = _43Bundle.from_prefix("_30")
	_4 = _43Bundle.from_prefix("_4")
	_35 = _43Bundle.from_prefix("_35")
	_fuType = Signal()

class _45Bundle(Bundle):
	_1, _REG, _REG_1 = Signals(3)

class _46Bundle(Bundle):
	_7 = Signal()

class _47Bundle(Bundle):
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_exceptionVec = _46Bundle.from_prefix("_exceptionVec")
	_uopIdx, _fuOpType = Signals(2)

class _48Bundle(Bundle):
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_uopIdx, _fuOpType = Signals(2)

class _49Bundle(Bundle):
	_27 = _48Bundle.from_prefix("_27")
	_46 = _48Bundle.from_prefix("_46")
	_12 = _48Bundle.from_prefix("_12")
	_41 = _48Bundle.from_prefix("_41")
	_16 = _48Bundle.from_prefix("_16")
	_44 = _48Bundle.from_prefix("_44")
	_32 = _48Bundle.from_prefix("_32")
	_21 = _48Bundle.from_prefix("_21")
	_33 = _48Bundle.from_prefix("_33")
	_28 = _48Bundle.from_prefix("_28")
	_55 = _48Bundle.from_prefix("_55")
	_23 = _48Bundle.from_prefix("_23")
	_14 = _48Bundle.from_prefix("_14")
	_20 = _48Bundle.from_prefix("_20")
	_38 = _48Bundle.from_prefix("_38")
	_24 = _48Bundle.from_prefix("_24")
	_35 = _48Bundle.from_prefix("_35")
	_5 = _48Bundle.from_prefix("_5")
	_34 = _48Bundle.from_prefix("_34")
	_9 = _48Bundle.from_prefix("_9")
	_25 = _48Bundle.from_prefix("_25")
	_15 = _48Bundle.from_prefix("_15")
	_45 = _48Bundle.from_prefix("_45")
	_47 = _48Bundle.from_prefix("_47")
	_19 = _48Bundle.from_prefix("_19")
	_51 = _48Bundle.from_prefix("_51")
	_26 = _48Bundle.from_prefix("_26")
	_49 = _48Bundle.from_prefix("_49")
	_29 = _48Bundle.from_prefix("_29")
	_54 = _48Bundle.from_prefix("_54")
	_6 = _48Bundle.from_prefix("_6")
	_7 = _48Bundle.from_prefix("_7")
	_13 = _48Bundle.from_prefix("_13")
	_8 = _48Bundle.from_prefix("_8")
	_22 = _48Bundle.from_prefix("_22")
	_37 = _48Bundle.from_prefix("_37")
	_1 = _48Bundle.from_prefix("_1")
	_2 = _48Bundle.from_prefix("_2")
	_40 = _48Bundle.from_prefix("_40")
	_48 = _48Bundle.from_prefix("_48")
	_0 = _48Bundle.from_prefix("_0")
	_18 = _48Bundle.from_prefix("_18")
	_42 = _48Bundle.from_prefix("_42")
	_43 = _48Bundle.from_prefix("_43")
	_36 = _48Bundle.from_prefix("_36")
	_10 = _48Bundle.from_prefix("_10")
	_52 = _48Bundle.from_prefix("_52")
	_39 = _48Bundle.from_prefix("_39")
	_11 = _48Bundle.from_prefix("_11")
	_3 = _48Bundle.from_prefix("_3")
	_31 = _48Bundle.from_prefix("_31")
	_4 = _48Bundle.from_prefix("_4")
	_53 = _48Bundle.from_prefix("_53")
	_50 = _48Bundle.from_prefix("_50")
	_30 = _48Bundle.from_prefix("_30")
	_17 = _48Bundle.from_prefix("_17")

class _50Bundle(Bundle):
	_0, _5, _1, _4, _2, _3 = Signals(6)

class _51Bundle(Bundle):
	_1 = _24Bundle.from_prefix("_1")

class _52Bundle(Bundle):
	_bits_robIdx = _4Bundle.from_prefix("_bits_robIdx")
	_valid = Signal()

class _53Bundle(Bundle):
	_next_r, _r, _REG, _next_r_1, _next_r_2, _REG_1, _REG_2, _r_5, _r_1, _r_4, _r_2, _r_3 = Signals(12)

class _54Bundle(Bundle):
	_entryCanEnqSeq = _15Bundle.from_prefix("_entryCanEnqSeq")
	_mmio = _5Bundle.from_prefix("_mmio")
	_addrvalid = _5Bundle.from_prefix("_addrvalid")
	_allocated = _5Bundle.from_prefix("_allocated")
	_memBackTypeMM = _5Bundle.from_prefix("_memBackTypeMM")
	_stDataReadyVecReg = _5Bundle.from_prefix("_stDataReadyVecReg")
	_vecCommit = _5Bundle.from_prefix("_vecCommit")
	_pending = _5Bundle.from_prefix("_pending")
	_addrValidVec = _5Bundle.from_prefix("_addrValidVec")
	_stAddrReadyVecReg = _5Bundle.from_prefix("_stAddrReadyVecReg")
	_lastCycleCancelCount_r = _5Bundle.from_prefix("_lastCycleCancelCount_r")
	_needCancel = _5Bundle.from_prefix("_needCancel")
	_waitStoreS2 = _5Bundle.from_prefix("_waitStoreS2")
	_nc = _5Bundle.from_prefix("_nc")
	_committed = _5Bundle.from_prefix("_committed")
	_vecMbCommit = _5Bundle.from_prefix("_vecMbCommit")
	_datavalid = _5Bundle.from_prefix("_datavalid")
	_unaligned = _5Bundle.from_prefix("_unaligned")
	_hasException = _5Bundle.from_prefix("_hasException")
	_vecLastFlow = _5Bundle.from_prefix("_vecLastFlow")
	_cross16Byte = _5Bundle.from_prefix("_cross16Byte")
	_isVec = _5Bundle.from_prefix("_isVec")
	_allvalid = _5Bundle.from_prefix("_allvalid")
	_dataReadyPtrExt = _4Bundle.from_prefix("_dataReadyPtrExt")
	_addrReadyPtrExt = _4Bundle.from_prefix("_addrReadyPtrExt")
	_enqUpBound = _13Bundle.from_prefix("_enqUpBound")
	_vpmaskNotEqual = _53Bundle.from_prefix("_vpmaskNotEqual")
	_selectBits = _44Bundle.from_prefix("_selectBits")
	_uop = _49Bundle.from_prefix("_uop")
	_commitVec = _9Bundle.from_prefix("_commitVec")
	_next_r = _34Bundle.from_prefix("_next_r")
	_allValidVec = _6Bundle.from_prefix("_allValidVec")
	_storeSetHitVec = _6Bundle.from_prefix("_storeSetHitVec")
	_io = _27Bundle.from_prefix("_io")
	_rdataPtrExt = _38Bundle.from_prefix("_rdataPtrExt")
	_mmioReq = _28Bundle.from_prefix("_mmioReq")
	_nextDataReadyPtr = _16Bundle.from_prefix("_nextDataReadyPtr")
	_nextAddrReadyPtr = _16Bundle.from_prefix("_nextAddrReadyPtr")
	_flipped_new_ptr = _16Bundle.from_prefix("_flipped_new_ptr")
	_deqPtrExt = _10Bundle.from_prefix("_deqPtrExt")
	_enqPtrExt = _10Bundle.from_prefix("_enqPtrExt")
	_vStoreFlow = _50Bundle.from_prefix("_vStoreFlow")
	_enqCancel = _12Bundle.from_prefix("_enqCancel")
	_s2 = _42Bundle.from_prefix("_s2")
	_new = _33Bundle.from_prefix("_new")
	_r = _37Bundle.from_prefix("_r")
	_ncReq_bits = _29Bundle.from_prefix("_ncReq_bits")
	_addrReadyLookupVec = _3Bundle.from_prefix("_addrReadyLookupVec")
	_dataReadyLookupVec = _3Bundle.from_prefix("_dataReadyLookupVec")
	_vecExceptionFlag = _52Bundle.from_prefix("_vecExceptionFlag")
	_cmtPtrExt = _8Bundle.from_prefix("_cmtPtrExt")
	_vecCommitHasException = _51Bundle.from_prefix("_vecCommitHasException")
	_uncacheUop = _47Bundle.from_prefix("_uncacheUop")
	_cboFlushedSb, _forwardMask1, _ncStall, _dataInvalidMask1, _forwardMask2, _ncDeqTrigger_REG, _ncState, _addrInvalidMask2Reg_REG, _ncDoReq, _needForward, _lastStWbIndex, _validVStoreFlow_REG, _lastlastCycleRedirect, _redirectCancelCount, _addrInvalidSqIdx, _scommit_next_r, _mmioState, _mmioDoReq, _deqCanDoCbo_next_r, _lastCycleRedirect, _dataInvalidMask2Reg_REG, _valid_cnt, _REG, _stWbIndexReg, _ncPtr_REG, _dataInvalidMaskReg, _reverse_flag, _lastEnqCancel, _addrInvalidMask1Reg_REG, _entryCanEnq, _canDeqMisaligned, _ncDoResp, _cboMmioPAddr, _storeAddrInFireReg, _toSbufferVecValid, _dataInvalidMask2, _vaddrMatchFailed_REG, _dataInvalidSqIdx, _dataInvalidMask1Reg_REG, _addrInvalidMaskReg, _forwardMask1_1, _forwardMask1_2, _dataInvalidMask1_1, _dataInvalidMask1_2, _forwardMask2_1, _forwardMask2_2, _addrInvalidMask2Reg_REG_1, _addrInvalidMask2Reg_REG_2, _needForward_1, _needForward_2, _addrInvalidSqIdx_1, _addrInvalidSqIdx_2, _dataInvalidMask2Reg_REG_1, _dataInvalidMask2Reg_REG_2, _dataInvalidMaskReg_1, _dataInvalidMaskReg_2, _addrInvalidMask1Reg_REG_1, _addrInvalidMask1Reg_REG_2, _dataInvalidMask2_1, _dataInvalidMask2_2, _vaddrMatchFailed_REG_1, _vaddrMatchFailed_REG_2, _dataInvalidSqIdx_1, _dataInvalidSqIdx_2, _dataInvalidMask1Reg_REG_1, _dataInvalidMask1Reg_REG_2, _addrInvalidMaskReg_1, _addrInvalidMaskReg_2, _ncDeqTrigger_REG_1, _lastStWbIndex_1, _stWbIndexReg_1, _ncPtr_REG_1, _validVStoreFlow_REG_5, _validVStoreFlow_REG_1, _validVStoreFlow_REG_4, _validVStoreFlow_REG_2, _validVStoreFlow_REG_3, _REG_5, _REG_4, _REG_9, _REG_6, _REG_7, _reverse_flag_16, _reverse_flag_8, _reverse_flag_5, _reverse_flag_1, _reverse_flag_4, _entryCanEnq_50, _entryCanEnq_21, _entryCanEnq_31, _entryCanEnq_8, _entryCanEnq_24, _entryCanEnq_46, _entryCanEnq_1, _entryCanEnq_48, _entryCanEnq_9, _entryCanEnq_33, _entryCanEnq_14, _entryCanEnq_3, _entryCanEnq_52, _entryCanEnq_6, _entryCanEnq_26, _entryCanEnq_35, _entryCanEnq_12, _entryCanEnq_10, _entryCanEnq_15, _entryCanEnq_25, _entryCanEnq_37, _entryCanEnq_19, _entryCanEnq_42, _entryCanEnq_5, _entryCanEnq_53, _entryCanEnq_44, _entryCanEnq_23, _entryCanEnq_4, _entryCanEnq_34, _entryCanEnq_43, _entryCanEnq_45, _entryCanEnq_7, _entryCanEnq_16, _entryCanEnq_32, _entryCanEnq_11, _entryCanEnq_38, _entryCanEnq_40, _entryCanEnq_47, _entryCanEnq_17, _entryCanEnq_27, _entryCanEnq_49, _entryCanEnq_51, _entryCanEnq_18, _entryCanEnq_39, _entryCanEnq_2, _entryCanEnq_28, _entryCanEnq_41, _entryCanEnq_55, _entryCanEnq_29, _entryCanEnq_13, _entryCanEnq_54, _entryCanEnq_20, _entryCanEnq_36, _entryCanEnq_30, _entryCanEnq_22, _storeAddrInFireReg_1, _storeAddrInFireReg_REG, _storeAddrInFireReg_REG_1 = Signals(145)

class _55Bundle(Bundle):
	_3, _1 = Signals(2)

class _56Bundle(Bundle):
	_154, _195, _739, _875, _257, _427, _646, _137, _133, _432, _585, _321, _599, _588, _611, _207, _633, _80, _615, _473, _754, _1071, _603, _146, _470, _285, _985, _357, _1073, _233, _813, _223, _929, _968, _67, _678, _170, _641, _592, _17, _57, _270, _807, _400, _940, _941, _76, _650, _167, _561, _898, _969, _1050, _1017, _29, _657, _725, _13, _418, _569, _618, _644, _288, _696, _85, _238, _604, _86, _375, _610, _294, _744, _70, _341, _467, _879, _958, _990, _381, _446, _808, _934, _811, _826, _1086, _331, _265, _492, _15, _412, _42, _1056, _305, _1020, _706, _855, _108, _466, _372, _68, _1036, _123, _117, _34, _581, _1066, _438, _45, _369, _455, _692, _1101, _392, _749, _964, _49, _1032, _27, _966, _971, _1028, _249, _1048, _859, _149, _365, _190, _632, _965, _231, _266, _312, _1038, _992, _648, _429, _302, _691, _768, _370, _394, _1112, _600, _723, _1092, _289, _188, _938, _508, _258, _793, _279, _1005, _326, _499, _630, _334, _818, _591, _208, _629, _1004, _671, _298, _743, _590, _212, _399, _1016, _1063, _526, _735, _1060, _140, _622, _895, _909, _153, _371, _684, _746, _325, _60, _1075, _827, _978, _346, _319, _535, _805, _841, _789, _870, _842, _221, _1052, _554, _780, _558, _1029, _872, _750, _382, _491, _662, _751, _1053, _511, _316, _464, _888, _406, _874, _344, _1111, _383, _218, _24, _514, _583, _840, _361, _663, _769, _324, _972, _539, _1107, _203, _503, _1070, _626, _37, _430, _795, _936, _245, _956, _838, _469, _220, _472, _931, _163, _557, _260, _379, _688, _71, _75, _261, _161, _187, _368, _51, _652, _515, _273, _417, _1096, _338, _800, _342, _982, _880, _449, _836, _471, _124, _851, _988, _893, _348, _329, _914, _1088, _214, _1104, _31, _686, _199, _46, _843, _1011, _275, _766, _839, _230, _6, _950, _709, _951, _98, _890, _529, _740, _575, _967, _247, _959, _23, _290, _229, _1100, _164, _576, _764, _219, _453, _579, _720, _385, _1054, _482, _1077, _820, _601, _787, _970, _624, _821, _197, _92, _1094, _332, _584, _752, _200, _790, _339, _741, _763, _465, _426, _179, _587, _106, _699, _983, _1061, _864, _627, _340, _291, _634, _797, _668, _871, _1099, _524, _850, _90, _785, _477, _669, _1031, _264, _378, _409, _468, _66, _792, _165, _431, _269, _586, _336, _284, _907, _93, _83, _824, _240, _711, _906, _543, _104, _1076, _38, _566, _333, _887, _675, _428, _234, _287, _804, _693, _765, _548, _99, _135, _393, _217, _122, _113, _198, _1089, _172, _58, _61, _726, _386, _1027, _295, _1018, _925, _559, _313, _1072, _309, _987, _955, _377, _14, _1033, _504, _623, _806, _25, _452, _447, _460, _120, _462, _53, _608, _911, _134, _79, _1065, _574, _645, _1045, _157, _183, _395, _1105, _241, _411, _494, _597, _771, _89, _948, _991, _729, _182, _456, _102, _944, _817, _156, _28, _565, _939, _55, _595, _310, _307, _308, _59, _1021, _450, _986, _388, _672, _215, _367, _181, _22, _815, _109, _21, _410, _478, _402, _387, _373, _239, _742, _661, _48, _801, _363, _416, _903, _835, _95, _943, _918, _130, _772, _114, _995, _445, _401, _343, _213, _423, _250, _708, _374, _828, _837, _802, _848, _127, _537, _441, _1001, _205, _211, _40, _366, _759, _922, _900, _39, _927, _832, _863, _609, _337, _892, _242, _619, _788, _884, _413, _226, _534, _745, _69, _883, _128, _727, _176, _50, _126, _935, _620, _1042, _442, _347, _687, _822, _701, _318, _132, _621, _674, _896, _352, _571, _144, _677, _682, _894, _3, _497, _404, _52, _525, _532, _527, _283, _777, _510, _762, _643, _251, _424, _88, _523, _314, _490, _767, _1068, _300, _91, _278, _194, _628, _849, _869, _885, _358, _847, _328, _73, _1087, _232, _538, _760, _82, _952, _62, _796, _829, _1059, _169, _41, _94, _1110, _158, _823, _1098, _810, _567, _1084, _322, _1043, _564, _201, _573, _721, _932, _937, _915, _186, _8, _782, _236, _362, _715, _1, _397, _177, _33, _116, _159, _244, _209, _26, _35, _282, _403, _718, _724, _676, _776, _716, _819, _1046, _1000, _738, _1047, _192, _4, _862, _474, _1085, _224, _920, _1019, _1024, _710, _728, _414, _546, _296, _602, _786, _216, _812, _926, _100, _166, _297, _461, _204, _562, _606, _139, _235, _908, _667, _142, _1074, _20, _419, _679, _901, _649, _509, _904, _631, _286, _263, _1044, _844, _97, _1023, _281, _996, _651, _877, _454, _513, _798, _178, _129, _593, _1041, _580, _845, _617, _301, _439, _448, _861, _945, _873, _398, _946, _536, _930, _1051, _637, _253, _1069, _43, _981, _522, _237, _496, _1081, _143, _255, _121, _111, _809, _1057, _1079, _0, _280, _306, _330, _495, _605, _660, _518, _443, _722, _899, _390, _360, _707, _549, _612, _997, _171, _254, _757, _761, _980, _304, _476, _665, _876, _702, _993, _994, _268, _1090, _833, _897, _151, _781, _1014, _345, _1106, _9, _973, _1009, _516, _656, _517, _689, _866, _1097, _458, _457, _636, _243, _355, _778, _484, _415, _1002, _481, _274, _506, _555, _1008, _1026, _64, _860, _905, _953, _72, _570, _642, _173, _389, _485, _779, _191, _791, _1093, _141, _407, _881, _480, _594, _47, _596, _323, _773, _327, _854, _857, _852, _87, _921, _614, _961, _54, _189, _533, _405, _698, _487, _168, _867, _1103, _196, _891, _933, _185, _502, _528, _733, _1108, _784, _974, _1025, _420, _115, _479, _999, _56, _380, _498, _1083, _659, _19, _222, _673, _912, _227, _814, _639, _664, _913, _737, _160, _435, _666, _145, _267, _713, _976, _32, _436, _483, _910, _589, _18, _507, _544, _206, _292, _519, _65, _1078, _878, _1049, _531, _560, _505, _868, _384, _36, _356, _103, _1013, _638, _556, _175, _680, _758, _1012, _110, _152, _635, _1015, _1034, _364, _731, _77, _1039, _1003, _616, _658, _700, _703, _248, _315, _613, _774, _422, _928, _949, _107, _998, _1067, _1006, _101, _831, _125, _989, _259, _541, _1035, _717, _512, _493, _1040, _889, _228, _155, _919, _277, _11, _770, _799, _112, _834, _714, _184, _463, _150, _246, _1030, _2, _916, _647, _320, _311, _147, _783, _755, _902, _640, _138, _1064, _444, _433, _475, _501, _530, _578, _753, _747, _30, _105, _350, _598, _317, _865, _825, _136, _210, _174, _293, _500, _459, _719, _853, _882, _924, _1037, _162, _225, _697, _451, _96, _272, _193, _625, _10, _582, _5, _44, _335, _1080, _1058, _654, _521, _540, _734, _545, _816, _830, _434, _856, _16, _653, _262, _1102, _408, _547, _607, _670, _271, _681, _685, _942, _962, _550, _858, _1007, _486, _1010, _704, _440, _1055, _563, _421, _276, _542, _84, _846, _252, _794, _756, _119, _712, _568, _572, _520, _1095, _118, _180, _655, _954, _977, _303, _957, _730, _12, _947, _148, _396, _923, _63, _975, _705, _960, _551, _683, _690, _7, _354, _78, _81, _437, _256, _736, _74, _775, _1062, _553, _425, _886, _1109, _552, _131, _299, _359, _488, _391, _489, _695, _803, _732, _376, _979, _202, _577, _917, _984, _1091, _1022, _748, _963, _694, _1082 = Signals(1110)

class _57Bundle(Bundle):
	_980, _1111, _218, _365, _964, _607, _361, _736, _738, _363, _1109, _591, _734, _1107, _234 = Signals(15)

class _58Bundle(Bundle):
	_16, _10, _4, _22 = Signals(4)

class _59Bundle(Bundle):
	_3, _5, _1, _7 = Signals(4)

class _60Bundle(Bundle):
	_new_ptr_value_T = _59Bundle.from_prefix("_new_ptr_value_T")
	_diff_T = _58Bundle.from_prefix("_diff_T")

class _61Bundle(Bundle):
	_5, _1, _4, _2, _6, _3 = Signals(6)

class _62Bundle(Bundle):
	_vecValid, _wline, _sqPtr_value, _sqNeedDeq = Signals(4)

class _63Bundle(Bundle):
	_bits = _62Bundle.from_prefix("_bits")
	_valid = Signal()

class _64Bundle(Bundle):
	_1 = _63Bundle.from_prefix("_1")
	_0 = _63Bundle.from_prefix("_0")

class _65Bundle(Bundle):
	_24 = Signal()

class _66Bundle(Bundle):
	_bits_data_T = _24Bundle.from_prefix("_bits_data_T")
	_valid_T = _65Bundle.from_prefix("_valid_T")
	_ready = Signal()

class _67Bundle(Bundle):
	_13, _38 = Signals(2)

class _68Bundle(Bundle):
	_bits_data_T = _24Bundle.from_prefix("_bits_data_T")
	_valid_T = _67Bundle.from_prefix("_valid_T")
	_ready = Signal()

class _69Bundle(Bundle):
	_0 = _66Bundle.from_prefix("_0")
	_1 = _68Bundle.from_prefix("_1")

class _70Bundle(Bundle):
	_deq = _64Bundle.from_prefix("_deq")
	_enq = _69Bundle.from_prefix("_enq")

class _71Bundle(Bundle):
	_19, _9, _29 = Signals(3)

class _72Bundle(Bundle):
	_mask, _data = Signals(2)

class _73Bundle(Bundle):
	_1 = _72Bundle.from_prefix("_1")
	_0 = _72Bundle.from_prefix("_0")

class _74Bundle(Bundle):
	_22 = Signal()

class _75Bundle(Bundle):
	_6 = Signal()

class _76Bundle(Bundle):
	_16, _10, _64, _70, _58, _94, _76, _88, _4, _82, _22, _100, _52, _34, _28 = Signals(15)

class _77Bundle(Bundle):
	_21, _5, _13, _17, _1, _9, _22 = Signals(7)

class _78Bundle(Bundle):
	_16, _10, _22, _4, _34, _28 = Signals(6)

class _79Bundle(Bundle):
	_5, _11, _1, _9, _3, _7 = Signals(6)

class _80Bundle(Bundle):
	_diff_T = _78Bundle.from_prefix("_diff_T")
	_new_ptr_value_T = _79Bundle.from_prefix("_new_ptr_value_T")

class _81Bundle(Bundle):
	_154, _195, _1822, _1582, _1972, _1564, _646, _1569, _1756, _1192, _1623, _1635, _585, _321, _207, _633, _1449, _615, _1744, _754, _1071, _603, _285, _357, _813, _1413, _592, _57, _1935, _1455, _400, _807, _940, _76, _898, _561, _969, _1017, _657, _1426, _418, _238, _604, _1605, _1845, _375, _1263, _610, _1606, _1941, _879, _958, _1629, _1618, _381, _808, _1210, _934, _826, _1360, _1617, _1719, _1456, _1551, _15, _1870, _412, _706, _1611, _1503, _1912, _855, _1186, _1486, _466, _711, _1036, _123, _117, _1516, _1299, _1066, _45, _369, _1575, _1101, _964, _27, _1251, _249, _1048, _1288, _190, _231, _1185, _429, _1942, _370, _394, _723, _1774, _508, _1275, _279, _1005, _334, _591, _1162, _208, _1863, _298, _1833, _1408, _1317, _399, _1600, _1203, _1341, _526, _735, _1918, _1654, _1665, _1438, _1060, _1834, _622, _909, _1558, _153, _346, _1330, _1414, _1576, _789, _1977, _1852, _1029, _382, _1053, _1636, _316, _1708, _406, _874, _1389, _514, _1666, _663, _1737, _1936, _1107, _1828, _430, _795, _1900, _838, _220, _472, _1240, _1324, _688, _1161, _75, _261, _652, _51, _273, _417, _1096, _1720, _982, _880, _1197, _1281, _471, _1113, _988, _1588, _1785, _1347, _1587, _1959, _1677, _1672, _1659, _214, _1888, _1461, _843, _1011, _1348, _766, _1533, _1875, _951, _1401, _219, _453, _579, _1054, _1509, _1077, _1761, _820, _970, _1204, _1366, _1402, _1755, _790, _339, _741, _1522, _465, _1528, _699, _106, _1971, _627, _340, _1954, _291, _634, _1851, _1473, _850, _477, _1552, _1953, _669, _2007, _1474, _1534, _165, _586, _1540, _1312, _93, _543, _1714, _333, _675, _1947, _693, _1797, _1726, _765, _99, _135, _1216, _1731, _393, _1335, _1089, _1738, _1222, _1180, _1545, _172, _1966, _1209, _1018, _1257, _1072, _309, _1815, _987, _1342, _2013, _447, _460, _1420, _2001, _1725, _1065, _1294, _645, _1515, _183, _411, _597, _1156, _771, _1527, _1114, _729, _1179, _939, _1810, _1821, _310, _1786, _388, _1887, _1353, _1581, _21, _1905, _478, _387, _1929, _742, _1599, _801, _363, _903, _772, _1707, _1323, _213, _423, _250, _837, _802, _537, _441, _759, _1869, _1660, _922, _39, _927, _832, _1300, _609, _1978, _892, _1803, _1983, _1419, _226, _1630, _69, _1641, _1042, _442, _687, _621, _352, _1378, _682, _3, _525, _532, _1696, _777, _1857, _424, _88, _490, _1504, _628, _1485, _849, _1557, _885, _1246, _1287, _358, _328, _1624, _1521, _232, _1167, _1653, _538, _760, _82, _952, _796, _1804, _1059, _94, _1233, _1084, _322, _567, _1846, _201, _573, _915, _1683, _1425, _1911, _1498, _177, _33, _159, _244, _718, _724, _819, _676, _1000, _1995, _1047, _862, _1395, _1510, _1024, _1563, _1792, _1173, _1984, _1450, _1384, _100, _166, _297, _1702, _1444, _1791, _1750, _1779, _1930, _904, _844, _1269, _1882, _1023, _651, _454, _513, _178, _129, _1041, _580, _1546, _448, _861, _945, _873, _946, _1906, _1989, _981, _1329, _237, _496, _255, _1168, _111, _1390, _1695, _495, _1336, _1198, _549, _1479, _171, _304, _993, _994, _1467, _1960, _1090, _1881, _1359, _897, _1191, _1876, _345, _9, _1311, _778, _243, _484, _1437, _555, _1306, _1767, _1713, _141, _1443, _1678, _1491, _327, _1258, _1282, _1239, _1365, _921, _87, _189, _2014, _405, _867, _1396, _196, _1965, _1924, _891, _933, _502, _1432, _1108, _1798, _784, _1293, _1462, _999, _1684, _1492, _1594, _1083, _1647, _1497, _1780, _1642, _814, _639, _664, _1372, _1354, _160, _435, _1221, _267, _976, _483, _436, _1155, _1612, _910, _507, _292, _519, _1858, _1318, _1174, _1078, _531, _1894, _868, _1480, _1840, _1228, _1012, _1732, _1383, _364, _1264, _616, _1648, _658, _1749, _700, _315, _928, _1893, _1743, _1923, _1006, _1234, _831, _1305, _1035, _717, _1773, _1377, _184, _1030, _916, _351, _147, _1227, _783, _1468, _640, _753, _501, _747, _1371, _1671, _1215, _105, _1768, _598, _825, _1431, _459, _225, _1701, _856, _1864, _1270, _1102, _1276, _670, _1539, _681, _1407, _1690, _1689, _1996, _1917, _1809, _1990, _1827, _2008, _712, _520, _1095, _303, _957, _730, _148, _63, _975, _705, _1899, _1252, _81, _1816, _2002, _736, _1245, _1762, _886, _1948, _489, _376, _1839, _202, _748, _1593, _963, _1570, _694 = Signals(630)

class _82Bundle(Bundle):
	_4 = Signal()

class _83Bundle(Bundle):
	_addrInvalidSqIdx_flipped_new_ptr_diff_T = _82Bundle.from_prefix("_addrInvalidSqIdx_flipped_new_ptr_diff_T")

class _84Bundle(Bundle):
	_2 = _83Bundle.from_prefix("_2")
	_1 = _83Bundle.from_prefix("_1")
	_0 = _83Bundle.from_prefix("_0")

class _85Bundle(Bundle):
	_forward = _84Bundle.from_prefix("_forward")
	_sqDeq_T, _maControl_toStoreMisalignBuffer_doDeq_T, _sqDeq_T_2 = Signals(3)

class _86Bundle(Bundle):
	_T = _46Bundle.from_prefix("_T")

class _87Bundle(Bundle):
	_15 = _86Bundle.from_prefix("_15")
	_12 = _86Bundle.from_prefix("_12")
	_28 = _86Bundle.from_prefix("_28")
	_13 = _86Bundle.from_prefix("_13")
	_4 = _86Bundle.from_prefix("_4")
	_25 = _86Bundle.from_prefix("_25")
	_29 = _86Bundle.from_prefix("_29")
	_49 = _86Bundle.from_prefix("_49")
	_18 = _86Bundle.from_prefix("_18")
	_1 = _86Bundle.from_prefix("_1")
	_36 = _86Bundle.from_prefix("_36")
	_9 = _86Bundle.from_prefix("_9")
	_34 = _86Bundle.from_prefix("_34")
	_20 = _86Bundle.from_prefix("_20")
	_3 = _86Bundle.from_prefix("_3")
	_23 = _86Bundle.from_prefix("_23")
	_6 = _86Bundle.from_prefix("_6")
	_38 = _86Bundle.from_prefix("_38")
	_52 = _86Bundle.from_prefix("_52")
	_11 = _86Bundle.from_prefix("_11")
	_5 = _86Bundle.from_prefix("_5")
	_40 = _86Bundle.from_prefix("_40")
	_8 = _86Bundle.from_prefix("_8")
	_26 = _86Bundle.from_prefix("_26")
	_24 = _86Bundle.from_prefix("_24")
	_43 = _86Bundle.from_prefix("_43")
	_31 = _86Bundle.from_prefix("_31")
	_22 = _86Bundle.from_prefix("_22")
	_55 = _86Bundle.from_prefix("_55")
	_21 = _86Bundle.from_prefix("_21")
	_47 = _86Bundle.from_prefix("_47")
	_39 = _86Bundle.from_prefix("_39")
	_44 = _86Bundle.from_prefix("_44")
	_30 = _86Bundle.from_prefix("_30")
	_53 = _86Bundle.from_prefix("_53")
	_14 = _86Bundle.from_prefix("_14")
	_16 = _86Bundle.from_prefix("_16")
	_2 = _86Bundle.from_prefix("_2")
	_46 = _86Bundle.from_prefix("_46")
	_51 = _86Bundle.from_prefix("_51")
	_41 = _86Bundle.from_prefix("_41")
	_50 = _86Bundle.from_prefix("_50")
	_35 = _86Bundle.from_prefix("_35")
	_37 = _86Bundle.from_prefix("_37")
	_10 = _86Bundle.from_prefix("_10")
	_32 = _86Bundle.from_prefix("_32")
	_0 = _86Bundle.from_prefix("_0")
	_54 = _86Bundle.from_prefix("_54")
	_27 = _86Bundle.from_prefix("_27")
	_45 = _86Bundle.from_prefix("_45")
	_17 = _86Bundle.from_prefix("_17")
	_33 = _86Bundle.from_prefix("_33")
	_48 = _86Bundle.from_prefix("_48")
	_42 = _86Bundle.from_prefix("_42")
	_7 = _86Bundle.from_prefix("_7")
	_19 = _86Bundle.from_prefix("_19")

class _88Bundle(Bundle):
	_5, _8, _2 = Signals(3)

class _89Bundle(Bundle):
	_11, _3, _7 = Signals(3)

class _90Bundle(Bundle):
	_21 = Signal()

class _91Bundle(Bundle):
	_0 = _5Bundle.from_prefix("_0")
	_2 = _5Bundle.from_prefix("_2")
	_1 = _5Bundle.from_prefix("_1")

class _92Bundle(Bundle):
	_0, _1 = Signals(2)

class _93Bundle(Bundle):
	_rlineflag = _92Bundle.from_prefix("_rlineflag")
	_rdata = _92Bundle.from_prefix("_rdata")
	_forwardMmask = _91Bundle.from_prefix("_forwardMmask")

class _94Bundle(Bundle):
	_128, _344, _119, _218, _281, _110, _326, _236, _479, _353, _362, _56, _380, _137, _497, _272, _209, _416, _452, _245, _398, _227, _335, _317, _290, _101, _146, _164, _470, _434, _173, _389, _83, _155, _191, _407, _371, _11, _38, _47, _65, _74, _182, _2, _92, _425, _461, _299, _488, _200, _29, _443, _20, _308, _263, _254 = Signals(56)

class _95Bundle(Bundle):
	_252, _126, _459, _279, _387, _90, _162, _225, _324, _180, _9, _144, _477, _315, _432, _396, _207, _378, _243, _468, _63, _108, _117, _423, _45, _72, _369, _441, _81, _261, _153, _414, _27, _333, _270, _18, _216, _342, _297, _351, _486, _234, _306, _495, _99, _135, _54, _189, _288, _36, _405, _450, _198, _360, _171 = Signals(55)

class _96Bundle(Bundle):
	_T = _24Bundle.from_prefix("_T")

class _97Bundle(Bundle):
	_2 = _96Bundle.from_prefix("_2")
	_37 = _96Bundle.from_prefix("_37")
	_16 = _96Bundle.from_prefix("_16")
	_27 = _96Bundle.from_prefix("_27")
	_19 = _96Bundle.from_prefix("_19")
	_14 = _96Bundle.from_prefix("_14")
	_4 = _96Bundle.from_prefix("_4")
	_6 = _96Bundle.from_prefix("_6")
	_31 = _96Bundle.from_prefix("_31")
	_12 = _96Bundle.from_prefix("_12")
	_35 = _96Bundle.from_prefix("_35")
	_43 = _96Bundle.from_prefix("_43")
	_29 = _96Bundle.from_prefix("_29")
	_0 = _96Bundle.from_prefix("_0")
	_45 = _96Bundle.from_prefix("_45")
	_49 = _96Bundle.from_prefix("_49")
	_8 = _96Bundle.from_prefix("_8")
	_42 = _96Bundle.from_prefix("_42")
	_33 = _96Bundle.from_prefix("_33")
	_50 = _96Bundle.from_prefix("_50")
	_25 = _96Bundle.from_prefix("_25")
	_24 = _96Bundle.from_prefix("_24")
	_5 = _96Bundle.from_prefix("_5")
	_9 = _96Bundle.from_prefix("_9")
	_51 = _96Bundle.from_prefix("_51")
	_48 = _96Bundle.from_prefix("_48")
	_32 = _96Bundle.from_prefix("_32")
	_54 = _96Bundle.from_prefix("_54")
	_1 = _96Bundle.from_prefix("_1")
	_20 = _96Bundle.from_prefix("_20")
	_15 = _96Bundle.from_prefix("_15")
	_3 = _96Bundle.from_prefix("_3")
	_17 = _96Bundle.from_prefix("_17")
	_22 = _96Bundle.from_prefix("_22")
	_30 = _96Bundle.from_prefix("_30")
	_7 = _96Bundle.from_prefix("_7")
	_10 = _96Bundle.from_prefix("_10")
	_53 = _96Bundle.from_prefix("_53")
	_36 = _96Bundle.from_prefix("_36")
	_34 = _96Bundle.from_prefix("_34")
	_11 = _96Bundle.from_prefix("_11")
	_41 = _96Bundle.from_prefix("_41")
	_55 = _96Bundle.from_prefix("_55")
	_26 = _96Bundle.from_prefix("_26")
	_46 = _96Bundle.from_prefix("_46")
	_52 = _96Bundle.from_prefix("_52")
	_28 = _96Bundle.from_prefix("_28")
	_13 = _96Bundle.from_prefix("_13")
	_44 = _96Bundle.from_prefix("_44")
	_47 = _96Bundle.from_prefix("_47")
	_23 = _96Bundle.from_prefix("_23")
	_40 = _96Bundle.from_prefix("_40")
	_38 = _96Bundle.from_prefix("_38")
	_18 = _96Bundle.from_prefix("_18")
	_21 = _96Bundle.from_prefix("_21")
	_39 = _96Bundle.from_prefix("_39")

class _98Bundle(Bundle):
	_557, _221, _893 = Signals(3)

class _99Bundle(Bundle):
	_rdata = _92Bundle.from_prefix("_rdata")
	_forwardMmask = _91Bundle.from_prefix("_forwardMmask")

class _100Bundle(Bundle):
	_3 = Signal()

class _101Bundle(Bundle):
	_T, _T_3 = Signals(2)

class _102Bundle(Bundle):
	_0 = _101Bundle.from_prefix("_0")
	_1 = _101Bundle.from_prefix("_1")

class _103Bundle(Bundle):
	_55 = _102Bundle.from_prefix("_55")

class _104Bundle(Bundle):
	_5, _6, _4, _9 = Signals(4)

class _105Bundle(Bundle):
	_16, _10, _4 = Signals(3)

class _106Bundle(Bundle):
	_nextAddrReadyPtr_diff_T = _82Bundle.from_prefix("_nextAddrReadyPtr_diff_T")
	_nextDataReadyPtr_diff_T = _82Bundle.from_prefix("_nextDataReadyPtr_diff_T")
	_flipped_new_ptr_diff_T = _82Bundle.from_prefix("_flipped_new_ptr_diff_T")
	_paddrModule_io = _93Bundle.from_prefix("_paddrModule_io")
	_deqCanDoCbo_T = _75Bundle.from_prefix("_deqCanDoCbo_T")
	_addrInvalidSqIdx2_T = _57Bundle.from_prefix("_addrInvalidSqIdx2_T")
	_dataInvalidSqIdx1_T = _57Bundle.from_prefix("_dataInvalidSqIdx1_T")
	_dataInvalidSqIdx2_T = _57Bundle.from_prefix("_dataInvalidSqIdx2_T")
	_addrInvalidSqIdx1_T = _57Bundle.from_prefix("_addrInvalidSqIdx1_T")
	_dataInvalidMask1_T = _71Bundle.from_prefix("_dataInvalidMask1_T")
	_dataInvalidMask2_T = _71Bundle.from_prefix("_dataInvalidMask2_T")
	_dataModule_io_rdata = _73Bundle.from_prefix("_dataModule_io_rdata")
	_next_T = _90Bundle.from_prefix("_next_T")
	_vaddrModule_io = _99Bundle.from_prefix("_vaddrModule_io")
	_addrReadyLookupVec = _60Bundle.from_prefix("_addrReadyLookupVec")
	_dataReadyLookupVec = _60Bundle.from_prefix("_dataReadyLookupVec")
	_storeSetHitVec_T = _98Bundle.from_prefix("_storeSetHitVec_T")
	_stDataReadyVecReg = _97Bundle.from_prefix("_stDataReadyVecReg")
	_dataBuffer_io = _70Bundle.from_prefix("_dataBuffer_io")
	_io = _85Bundle.from_prefix("_io")
	_vpmaskNotEqual_T = _105Bundle.from_prefix("_vpmaskNotEqual_T")
	_enqCancelValid_flushItself_T = _77Bundle.from_prefix("_enqCancelValid_flushItself_T")
	_new_ptr_value_T = _89Bundle.from_prefix("_new_ptr_value_T")
	_dataReadyLookup_T = _74Bundle.from_prefix("_dataReadyLookup_T")
	_enqUpBound = _80Bundle.from_prefix("_enqUpBound")
	_entryCanEnqSeq_entryHitBound_T = _81Bundle.from_prefix("_entryCanEnqSeq_entryHitBound_T")
	_selectBits_T = _94Bundle.from_prefix("_selectBits_T")
	_needForward_T = _88Bundle.from_prefix("_needForward_T")
	_vecCommittmp = _103Bundle.from_prefix("_vecCommittmp")
	_diff_T = _76Bundle.from_prefix("_diff_T")
	_Cross16ByteData_T = _55Bundle.from_prefix("_Cross16ByteData_T")
	_cross16Byte_T = _55Bundle.from_prefix("_cross16Byte_T")
	_needCancel = _87Bundle.from_prefix("_needCancel")
	_vecExceptionFlagCancel_vecLastFlowCommit_T, _selectUpBound_T, _addrReadyPtrExt_T, _ncDoReq_T, _Cross16ByteMask_T, _deqMask_T, _committed_T, _ncReq_bits_memBackTypeMM_next_T, _dataReadyPtrExt_T, _vecExceptionFlagCancel_vecLastFlowCommit_T_5, _vecExceptionFlagCancel_vecLastFlowCommit_T_6, _vecExceptionFlagCancel_vecLastFlowCommit_T_4, _vecExceptionFlagCancel_vecLastFlowCommit_T_9, _selectUpBound_T_252, _selectUpBound_T_126, _selectUpBound_T_459, _selectUpBound_T_279, _selectUpBound_T_387, _selectUpBound_T_90, _selectUpBound_T_162, _selectUpBound_T_225, _selectUpBound_T_324, _selectUpBound_T_180, _selectUpBound_T_9, _selectUpBound_T_144, _selectUpBound_T_477, _selectUpBound_T_315, _selectUpBound_T_432, _selectUpBound_T_396, _selectUpBound_T_207, _selectUpBound_T_378, _selectUpBound_T_243, _selectUpBound_T_468, _selectUpBound_T_63, _selectUpBound_T_108, _selectUpBound_T_117, _selectUpBound_T_423, _selectUpBound_T_45, _selectUpBound_T_72, _selectUpBound_T_369, _selectUpBound_T_441, _selectUpBound_T_81, _selectUpBound_T_261, _selectUpBound_T_153, _selectUpBound_T_414, _selectUpBound_T_27, _selectUpBound_T_333, _selectUpBound_T_270, _selectUpBound_T_18, _selectUpBound_T_216, _selectUpBound_T_342, _selectUpBound_T_297, _selectUpBound_T_351, _selectUpBound_T_486, _selectUpBound_T_234, _selectUpBound_T_306, _selectUpBound_T_495, _selectUpBound_T_99, _selectUpBound_T_135, _selectUpBound_T_54, _selectUpBound_T_189, _selectUpBound_T_288, _selectUpBound_T_36, _selectUpBound_T_405, _selectUpBound_T_450, _selectUpBound_T_198, _selectUpBound_T_360, _selectUpBound_T_171, _Cross16ByteMask_T_1, _deqMask_T_2, _committed_T_5, _committed_T_1, _committed_T_4, _committed_T_2, _committed_T_6, _committed_T_3 = Signals(76)

class _107Bundle(Bundle):
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_level = Signal()

class _108Bundle(Bundle):
	_bits = _107Bundle.from_prefix("_bits")
	_valid = Signal()

class _109Bundle(Bundle):
	_address, _opcode = Signals(2)

class _110Bundle(Bundle):
	_bits = _109Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _111Bundle(Bundle):
	_ready, _valid = Signals(2)

class _112Bundle(Bundle):
	_sqIdx = _4Bundle.from_prefix("_sqIdx")
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_fuType, _numLsElem, _lastUop, _uopIdx, _fuOpType = Signals(5)

class _113Bundle(Bundle):
	_bits = _112Bundle.from_prefix("_bits")
	_valid = Signal()

class _114Bundle(Bundle):
	_3 = _113Bundle.from_prefix("_3")
	_0 = _113Bundle.from_prefix("_0")
	_1 = _113Bundle.from_prefix("_1")
	_5 = _113Bundle.from_prefix("_5")
	_4 = _113Bundle.from_prefix("_4")
	_2 = _113Bundle.from_prefix("_2")

class _115Bundle(Bundle):
	_isHyper, _isForVSnonLeafPTE, _vaddr, _gpaddr, _vaNeedExt = Signals(5)

class _116Bundle(Bundle):
	_valid, _empty = Signals(2)

class _117Bundle(Bundle):
	_12, _10, _0, _15, _8, _5, _11, _13, _1, _4, _6, _9, _2, _14, _3, _7 = Signals(16)

class _118Bundle(Bundle):
	_sqIdx = _4Bundle.from_prefix("_sqIdx")
	_waitForRobIdx = _4Bundle.from_prefix("_waitForRobIdx")
	_loadWaitStrict, _loadWaitBit = Signals(2)

class _119Bundle(Bundle):
	_addrInvalidSqIdx = _4Bundle.from_prefix("_addrInvalidSqIdx")
	_dataInvalidSqIdx = _4Bundle.from_prefix("_dataInvalidSqIdx")
	_forwardMask = _117Bundle.from_prefix("_forwardMask")
	_forwardData = _117Bundle.from_prefix("_forwardData")
	_uop = _118Bundle.from_prefix("_uop")
	_addrInvalid, _valid, _sqIdxMask, _paddr, _vaddr, _dataInvalid, _matchInvalid, _sqIdx_flag, _mask = Signals(9)

class _120Bundle(Bundle):
	_1 = _119Bundle.from_prefix("_1")
	_0 = _119Bundle.from_prefix("_0")
	_2 = _119Bundle.from_prefix("_2")

class _121Bundle(Bundle):
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_uopIdx = Signal()

class _122Bundle(Bundle):
	_uop = _121Bundle.from_prefix("_uop")
	_sqPtr = _4Bundle.from_prefix("_sqPtr")
	_doDeq = Signal()

class _123Bundle(Bundle):
	_crossPageWithHit, _paddr, _withSameUop, _crossPageCanDeq = Signals(4)

class _124Bundle(Bundle):
	_toStoreQueue = _123Bundle.from_prefix("_toStoreQueue")
	_toStoreMisalignBuffer = _122Bundle.from_prefix("_toStoreMisalignBuffer")

class _125Bundle(Bundle):
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_exceptionVec = _46Bundle.from_prefix("_exceptionVec")
	_flushPipe = Signal()

class _126Bundle(Bundle):
	_bits_uop = _125Bundle.from_prefix("_bits_uop")
	_ready, _valid = Signals(2)


class _128Bundle(Bundle):
	_pendingPtr = _4Bundle.from_prefix("_pendingPtr")
	_scommit, _pendingst = Signals(2)

class _129Bundle(Bundle):
	_data, _addr, _wline, _vaddr, _vecValid, _mask = Signals(6)

class _130Bundle(Bundle):
	_bits = _129Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _131Bundle(Bundle):
	_0 = _130Bundle.from_prefix("_0")
	_1 = _130Bundle.from_prefix("_1")

class _132Bundle(Bundle):
	_15, _23, _6, _3, _7 = Signals(5)

class _133Bundle(Bundle):
	_exceptionVec = _132Bundle.from_prefix("_exceptionVec")
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_sqIdx_value, _uopIdx, _fuOpType = Signals(3)

class _134Bundle(Bundle):
	_uop = _133Bundle.from_prefix("_uop")
	_wlineflag, _updateAddrValid, _vaNeedExt, _isHyper, _paddr, _vaddr, _nc, _isvec, _miss, _isForVSnonLeafPTE, _fullva, _gpaddr, _misalignWith16Byte, _mask, _isFrmMisAlignBuf, _isMisalign = Signals(16)

class _135Bundle(Bundle):
	_bits = _134Bundle.from_prefix("_bits")
	_valid = Signal()

class _136Bundle(Bundle):
	_0 = _135Bundle.from_prefix("_0")
	_1 = _135Bundle.from_prefix("_1")

class _137Bundle(Bundle):
	_15, _6, _3, _23 = Signals(4)

class _138Bundle(Bundle):
	_robIdx = _4Bundle.from_prefix("_robIdx")
	_exceptionVec = _137Bundle.from_prefix("_exceptionVec")
	_uopIdx = Signal()

class _139Bundle(Bundle):
	_uop = _138Bundle.from_prefix("_uop")
	_mmio, _vaNeedExt, _hasException, _isHyper, _memBackTypeMM, _isvec, _fullva, _af, _gpaddr, _updateAddrValid, _isForVSnonLeafPTE = Signals(11)

class _140Bundle(Bundle):
	_1 = _139Bundle.from_prefix("_1")
	_0 = _139Bundle.from_prefix("_0")

class _141Bundle(Bundle):
	_fuType, _sqIdx_value, _fuOpType = Signals(3)

class _142Bundle(Bundle):
	_uop = _141Bundle.from_prefix("_uop")
	_data = Signal()

class _143Bundle(Bundle):
	_bits = _142Bundle.from_prefix("_bits")
	_valid = Signal()

class _144Bundle(Bundle):
	_0 = _143Bundle.from_prefix("_0")
	_1 = _143Bundle.from_prefix("_1")

class _145Bundle(Bundle):
	_sqIdx_value, _mask = Signals(2)

class _146Bundle(Bundle):
	_bits = _145Bundle.from_prefix("_bits")
	_valid = Signal()

class _147Bundle(Bundle):
	_1 = _146Bundle.from_prefix("_1")
	_0 = _146Bundle.from_prefix("_0")

class _148Bundle(Bundle):
	_data, _memBackTypeMM, _addr, _id, _nc, _vaddr, _mask = Signals(7)

class _149Bundle(Bundle):
	_bits = _148Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _150Bundle(Bundle):
	_nc, _nderr, _id = Signals(3)

class _151Bundle(Bundle):
	_bits = _150Bundle.from_prefix("_bits")
	_valid = Signal()

class _152Bundle(Bundle):
	_req = _149Bundle.from_prefix("_req")
	_resp = _151Bundle.from_prefix("_resp")

class _153Bundle(Bundle):
	_robidx = _4Bundle.from_prefix("_robidx")
	_exceptionVec = _132Bundle.from_prefix("_exceptionVec")
	_feedback = _92Bundle.from_prefix("_feedback")
	_vaddr, _uopidx, _gpaddr, _vaNeedExt, _isForVSnonLeafPTE = Signals(5)

class _154Bundle(Bundle):
	_bits = _153Bundle.from_prefix("_bits")
	_valid = Signal()

class _155Bundle(Bundle):
	_0 = _154Bundle.from_prefix("_0")
	_1 = _154Bundle.from_prefix("_1")

class _156Bundle(Bundle):
	_rob = _128Bundle.from_prefix("_rob")
	_maControl = _124Bundle.from_prefix("_maControl")
	_forward = _120Bundle.from_prefix("_forward")
	_enq_req = _114Bundle.from_prefix("_enq_req")
	_brqRedirect = _108Bundle.from_prefix("_brqRedirect")
	_flushSbuffer = _116Bundle.from_prefix("_flushSbuffer")
	_storeAddrIn = _136Bundle.from_prefix("_storeAddrIn")
	_sbuffer = _131Bundle.from_prefix("_sbuffer")
	_storeMaskIn = _147Bundle.from_prefix("_storeMaskIn")
	_stIssuePtr = _4Bundle.from_prefix("_stIssuePtr")
	_stDataReadySqPtr = _4Bundle.from_prefix("_stDataReadySqPtr")
	_stAddrReadySqPtr = _4Bundle.from_prefix("_stAddrReadySqPtr")
	_storeDataIn = _144Bundle.from_prefix("_storeDataIn")
	_stAddrReadyVec = _5Bundle.from_prefix("_stAddrReadyVec")
	_stDataReadyVec = _5Bundle.from_prefix("_stDataReadyVec")
	_mmioStout = _126Bundle.from_prefix("_mmioStout")
	_cmoOpResp = _111Bundle.from_prefix("_cmoOpResp")
	_cmoOpReq = _110Bundle.from_prefix("_cmoOpReq")
	_storeAddrInRe = _140Bundle.from_prefix("_storeAddrInRe")
	_vecFeedback = _155Bundle.from_prefix("_vecFeedback")
	_exceptionAddr = _115Bundle.from_prefix("_exceptionAddr")
	_uncache = _152Bundle.from_prefix("_uncache")
	_sqDeq, _sqEmpty, _uncacheOutstanding, _force_write, _sqCancelCnt = Signals(5)

class StoreQueueBundle(Bundle):
	io = _156Bundle.from_prefix("io")
	StoreQueue = _54Bundle.from_prefix("StoreQueue")
	StoreQueue_ = _106Bundle.from_prefix("StoreQueue_")
	reset, clock = Signals(2)

