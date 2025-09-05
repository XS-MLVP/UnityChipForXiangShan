from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_1, _0, _2 = Signals(3)

class _1Bundle(Bundle):
	_valid = Signal()

class _2Bundle(Bundle):
	_0 = _1Bundle.from_prefix("_0")
	_1 = _1Bundle.from_prefix("_1")

class _3Bundle(Bundle):
	_1, _26, _29, _10, _30, _11, _8, _12, _21, _13, _0, _16, _4, _28, _23, _27, _18, _19, _20, _6, _3, _14, _2, _24, _15, _7, _31, _22, _9, _5, _17, _25 = Signals(32)

class _4Bundle(Bundle):
	_26, _29, _10, _30, _11, _8, _12, _21, _13, _0, _16, _4, _28, _23, _27, _1, _18, _19, _20, _6, _3, _14, _2, _24, _15, _7, _31, _22, _9, _5, _17, _25, _1_1, _1_26, _1_29, _1_10, _1_30, _1_11, _1_8, _1_12, _1_21, _1_13, _1_0, _1_16, _1_4, _1_28, _1_23, _1_27, _1_18, _1_19, _1_20, _1_6, _1_3, _1_14, _1_2, _1_24, _1_15, _1_7, _1_31, _1_22, _1_9, _1_5, _1_17, _1_25 = Signals(64)

class _5Bundle(Bundle):
	_flag, _value = Signals(2)

class _6Bundle(Bundle):
	_robIdx = _5Bundle.from_prefix("_robIdx")
	_ftqPtr = _5Bundle.from_prefix("_ftqPtr")
	_ftqOffset, _preDecodeInfo_isRVC = Signals(2)

class _7Bundle(Bundle):
	_uop = _6Bundle.from_prefix("_uop")

class _8Bundle(Bundle):
	_uop = _6Bundle.from_prefix("_uop")
	_1 = _7Bundle.from_prefix("_1")

class _9Bundle(Bundle):
	_0 = _8Bundle.from_prefix("_0")

class _10Bundle(Bundle):
	_robIdx = _5Bundle.from_prefix("_robIdx")
	_level = Signal()

class _11Bundle(Bundle):
	_bits = _10Bundle.from_prefix("_bits")
	_valid = Signal()

class _12Bundle(Bundle):
	_bits = _10Bundle.from_prefix("_bits")
	_1 = _11Bundle.from_prefix("_1")
	_valid = Signal()

class _13Bundle(Bundle):
	_1 = _1Bundle.from_prefix("_1")
	_valid = Signal()

class _14Bundle(Bundle):
	_bits_uop = _6Bundle.from_prefix("_bits_uop")
	_valid = Signal()

class _15Bundle(Bundle):
	_1 = _14Bundle.from_prefix("_1")
	_bits_uop = _6Bundle.from_prefix("_bits_uop")
	_valid = Signal()

class _16Bundle(Bundle):
	_1 = _15Bundle.from_prefix("_1")
	_0 = _15Bundle.from_prefix("_0")

class _17Bundle(Bundle):
	_1 = Signal()

class _18Bundle(Bundle):
	_2 = _8Bundle.from_prefix("_2")
	_1, _1_1 = Signals(2)

class _19Bundle(Bundle):
	_bits = _10Bundle.from_prefix("_bits")
	_5 = _11Bundle.from_prefix("_5")
	_4 = _11Bundle.from_prefix("_4")
	_6 = _11Bundle.from_prefix("_6")
	_2 = _11Bundle.from_prefix("_2")
	_7 = _11Bundle.from_prefix("_7")
	_1 = _11Bundle.from_prefix("_1")
	_3 = _11Bundle.from_prefix("_3")
	_valid = Signal()

class _20Bundle(Bundle):
	_robIdx = _5Bundle.from_prefix("_robIdx")
	_ftqPtr = _5Bundle.from_prefix("_ftqPtr")
	_ftqOffset = Signal()

class _21Bundle(Bundle):
	_bits_uop = _20Bundle.from_prefix("_bits_uop")
	_valid = Signal()

class _22Bundle(Bundle):
	_3 = _21Bundle.from_prefix("_3")
	_7 = _21Bundle.from_prefix("_7")
	_4 = _21Bundle.from_prefix("_4")
	_6 = _21Bundle.from_prefix("_6")
	_5 = _21Bundle.from_prefix("_5")
	_1 = _21Bundle.from_prefix("_1")
	_2 = _21Bundle.from_prefix("_2")
	_bits_uop = _20Bundle.from_prefix("_bits_uop")
	_valid = Signal()

class _23Bundle(Bundle):
	_0 = _22Bundle.from_prefix("_0")
	_1 = _22Bundle.from_prefix("_1")

class _24Bundle(Bundle):
	_1 = _1Bundle.from_prefix("_1")
	_4 = _1Bundle.from_prefix("_4")
	_2 = _1Bundle.from_prefix("_2")
	_5 = _1Bundle.from_prefix("_5")
	_6 = _1Bundle.from_prefix("_6")
	_7 = _1Bundle.from_prefix("_7")
	_3 = _1Bundle.from_prefix("_3")
	_valid = Signal()

class _25Bundle(Bundle):
	_6 = _14Bundle.from_prefix("_6")
	_1 = _14Bundle.from_prefix("_1")
	_4 = _14Bundle.from_prefix("_4")
	_2 = _14Bundle.from_prefix("_2")
	_7 = _14Bundle.from_prefix("_7")
	_3 = _14Bundle.from_prefix("_3")
	_5 = _14Bundle.from_prefix("_5")
	_bits_uop = _6Bundle.from_prefix("_bits_uop")
	_valid = Signal()

class _26Bundle(Bundle):
	_0 = _25Bundle.from_prefix("_0")
	_1 = _25Bundle.from_prefix("_1")

class _27Bundle(Bundle):
	_1, _5, _4, _6, _3, _2, _7 = Signals(7)

class _28Bundle(Bundle):
	_right_res = _23Bundle.from_prefix("_right_res")
	_left_res = _23Bundle.from_prefix("_left_res")
	_0 = _18Bundle.from_prefix("_0")
	_3 = _18Bundle.from_prefix("_3")
	_1 = _18Bundle.from_prefix("_1")
	_2 = _18Bundle.from_prefix("_2")
	_res = _26Bundle.from_prefix("_res")
	_oldest = _24Bundle.from_prefix("_oldest")
	_REG = _19Bundle.from_prefix("_REG")
	_selValidNext, _selValidNext_1, _selValidNext_5, _selValidNext_4, _selValidNext_6, _selValidNext_3, _selValidNext_2, _selValidNext_7 = Signals(8)

class _29Bundle(Bundle):
	_select = _28Bundle.from_prefix("_select")
	_oldest = _13Bundle.from_prefix("_oldest")
	_res = _16Bundle.from_prefix("_res")
	_REG = _12Bundle.from_prefix("_REG")
	_2 = _9Bundle.from_prefix("_2")
	_selValidNext_last_REG, _selValidNext_last_REG_1 = Signals(2)

class _30Bundle(Bundle):
	_r = Signal()

class _31Bundle(Bundle):
	_1 = _30Bundle.from_prefix("_1")
	_0 = _30Bundle.from_prefix("_0")

class _32Bundle(Bundle):
	_lqViolationSelVec = _4Bundle.from_prefix("_lqViolationSelVec")
	_entryNeedCheck_r = _4Bundle.from_prefix("_entryNeedCheck_r")
	_paddrModule_io_violationMdata = _31Bundle.from_prefix("_paddrModule_io_violationMdata")
	_maskModule_io_violationMdata = _31Bundle.from_prefix("_maskModule_io_violationMdata")
	_lqSelect = _29Bundle.from_prefix("_lqSelect")

class _35Bundle(Bundle):
	_0 = Signal()

class _36Bundle(Bundle):
	_req_ready = _35Bundle.from_prefix("_req_ready")

class _37Bundle(Bundle):
	_1 = _36Bundle.from_prefix("_1")
	_2 = _36Bundle.from_prefix("_2")
	_0 = _36Bundle.from_prefix("_0")

class _38Bundle(Bundle):
	_query = _37Bundle.from_prefix("_query")

class _39Bundle(Bundle):
	_1 = _30Bundle.from_prefix("_1")
	_2 = _30Bundle.from_prefix("_2")
	_0 = _30Bundle.from_prefix("_0")

class _40Bundle(Bundle):
	_1, _26, _29, _10, _30, _11, _8, _12, _21, _13, _16, _4, _28, _23, _27, _18, _19, _20, _6, _3, _14, _2, _24, _15, _7, _31, _22, _9, _5, _17, _25 = Signals(31)

class _41Bundle(Bundle):
	_differentFlag, _compare, _differentFlag_1, _differentFlag_26, _differentFlag_29, _differentFlag_10, _differentFlag_30, _differentFlag_11, _differentFlag_8, _differentFlag_12, _differentFlag_21, _differentFlag_13, _differentFlag_16, _differentFlag_4, _differentFlag_28, _differentFlag_23, _differentFlag_27, _differentFlag_18, _differentFlag_19, _differentFlag_20, _differentFlag_6, _differentFlag_3, _differentFlag_14, _differentFlag_2, _differentFlag_24, _differentFlag_15, _differentFlag_7, _differentFlag_31, _differentFlag_22, _differentFlag_9, _differentFlag_5, _differentFlag_17, _differentFlag_25, _compare_1, _compare_26, _compare_29, _compare_10, _compare_30, _compare_11, _compare_8, _compare_12, _compare_21, _compare_13, _compare_16, _compare_4, _compare_28, _compare_23, _compare_27, _compare_18, _compare_19, _compare_20, _compare_6, _compare_3, _compare_14, _compare_2, _compare_24, _compare_15, _compare_7, _compare_31, _compare_22, _compare_9, _compare_5, _compare_17, _compare_25 = Signals(64)

class _42Bundle(Bundle):
	_ftqPtr = _5Bundle.from_prefix("_ftqPtr")
	_robIdx = _5Bundle.from_prefix("_robIdx")
	_sqIdx = _5Bundle.from_prefix("_sqIdx")
	_preDecodeInfo_isRVC, _ftqOffset = Signals(2)

class _43Bundle(Bundle):
	_20 = _42Bundle.from_prefix("_20")
	_23 = _42Bundle.from_prefix("_23")
	_2 = _42Bundle.from_prefix("_2")
	_12 = _42Bundle.from_prefix("_12")
	_0 = _42Bundle.from_prefix("_0")
	_11 = _42Bundle.from_prefix("_11")
	_4 = _42Bundle.from_prefix("_4")
	_29 = _42Bundle.from_prefix("_29")
	_14 = _42Bundle.from_prefix("_14")
	_6 = _42Bundle.from_prefix("_6")
	_26 = _42Bundle.from_prefix("_26")
	_1 = _42Bundle.from_prefix("_1")
	_10 = _42Bundle.from_prefix("_10")
	_27 = _42Bundle.from_prefix("_27")
	_24 = _42Bundle.from_prefix("_24")
	_18 = _42Bundle.from_prefix("_18")
	_13 = _42Bundle.from_prefix("_13")
	_5 = _42Bundle.from_prefix("_5")
	_21 = _42Bundle.from_prefix("_21")
	_22 = _42Bundle.from_prefix("_22")
	_31 = _42Bundle.from_prefix("_31")
	_30 = _42Bundle.from_prefix("_30")
	_16 = _42Bundle.from_prefix("_16")
	_19 = _42Bundle.from_prefix("_19")
	_7 = _42Bundle.from_prefix("_7")
	_25 = _42Bundle.from_prefix("_25")
	_9 = _42Bundle.from_prefix("_9")
	_17 = _42Bundle.from_prefix("_17")
	_28 = _42Bundle.from_prefix("_28")
	_15 = _42Bundle.from_prefix("_15")
	_8 = _42Bundle.from_prefix("_8")
	_3 = _42Bundle.from_prefix("_3")

class _44Bundle(Bundle):
	_needEnqueue = _0Bundle.from_prefix("_needEnqueue")
	_acceptedVec = _0Bundle.from_prefix("_acceptedVec")
	_lastCanAccept_r = _0Bundle.from_prefix("_lastCanAccept_r")
	_datavalid = _3Bundle.from_prefix("_datavalid")
	_allocated = _3Bundle.from_prefix("_allocated")
	_detectedRollback = _32Bundle.from_prefix("_detectedRollback")
	_io = _38Bundle.from_prefix("_io")
	_lastAllocIndex_next_nextVec = _39Bundle.from_prefix("_lastAllocIndex_next_nextVec")
	_needCancel = _41Bundle.from_prefix("_needCancel")
	_uop = _43Bundle.from_prefix("_uop")
	_allRedirect = _2Bundle.from_prefix("_allRedirect")
	_offset = Signal()

class _45Bundle(Bundle):
	_26, _222, _212, _36, _102, _8, _379, _314, _260, _263, _235, _364, _18, _158, _51, _243, _88, _191, _209, _221, _280, _195, _373, _289, _339, _113, _32, _334, _43, _345, _12, _104, _171, _370, _254, _249, _95, _72, _118, _229, _112, _287, _227, _205, _272, _217, _355, _270, _45, _151, _156, _0, _16, _177, _315, _164, _342, _336, _201, _369, _78, _306, _381, _380, _76, _2, _267, _128, _160, _360, _99, _141, _372, _57, _48, _134, _349, _290, _107, _11, _82, _316, _346, _305, _90, _168, _307, _220, _377, _62, _81, _226, _60, _29, _375, _66, _326, _228, _366, _178, _231, _251, _214, _358, _213, _59, _74, _119, _376, _146, _252, _343, _303, _266, _352, _101, _68, _298, _170, _138, _150, _385, _125, _264, _149, _144, _234, _286, _194, _37, _341, _137, _189, _75, _232, _50, _335, _197, _28, _44, _302, _117, _348, _276, _173, _106, _176, _121, _103, _15, _159, _224, _9, _325, _258, _223, _46, _367, _70, _237, _354, _192, _293, _53, _257, _268, _324, _250, _87, _363, _123, _371, _153, _110, _129, _310, _317, _198, _130, _241, _148, _63, _291, _186, _347, _283, _321, _20, _256, _206, _265, _332, _157, _71, _24, _179, _244, _93, _174, _162, _142, _242, _361, _204, _318, _132, _152, _218, _187, _337, _135, _40, _80, _340, _94, _105, _183, _274, _131, _6, _41, _275, _67, _190, _143, _65, _42, _52, _175, _238, _215, _108, _277, _216, _47, _167, _180, _126, _98, _333, _188, _77, _312, _236, _85, _297, _56, _172, _288, _382, _253, _247, _323, _248, _207, _109, _139, _3, _365, _7, _133, _208, _282, _22, _359, _79, _25, _300, _169, _357, _278, _181, _140, _261, _301, _384, _35, _329, _116, _13, _353, _97, _19, _245, _240, _114, _259, _202, _230, _378, _38, _374, _184, _166, _122, _309, _331, _273, _185, _351, _73, _49, _54, _145, _69, _199, _14, _327, _356, _211, _193, _239, _262, _322, _83, _165, _362, _285, _64, _10, _147, _155, _61, _368, _196, _246, _91, _203, _182, _299, _163, _219, _269, _31, _281, _5, _161, _92, _200, _294, _124, _319, _1, _225, _308, _279, _30, _350, _338, _233, _21, _58, _304, _23, _27, _271, _255, _89, _34, _296, _84, _111, _383, _115, _154, _136, _311, _328, _313, _330, _100, _320, _55, _127, _4, _210, _292, _96, _39, _86, _120, _344, _295, _284, _17 = Signals(385)

class _46Bundle(Bundle):
	_93 = Signal()

class _47Bundle(Bundle):
	_308, _362, _26, _278, _398, _470, _134, _317, _107, _326, _452, _551, _8, _233, _152, _35, _251, _116, _407, _53, _353, _515, _260, _197, _215, _335, _443, _533, _434, _44, _461, _524, _569, _80, _206, _416, _299, _62, _380, _488, _71, _560, _389, _425, _371, _89, _287, _269, _479, _344, _98, _170, _179, _224, _188, _161, _125, _542, _506, _17, _143, _497, _578, _242 = Signals(64)

class _48Bundle(Bundle):
	_169, _225, _181, _237, _189, _137, _233, _241, _185, _249, _213, _197, _253, _177, _149, _201, _145, _245, _157, _173, _229, _133, _209, _221, _161, _193, _153, _205, _141, _129, _217, _165 = Signals(32)

class _49Bundle(Bundle):
	_T = _47Bundle.from_prefix("_T")
	_flushItself_T = _48Bundle.from_prefix("_flushItself_T")

class _50Bundle(Bundle):
	_1, _10, _6, _4, _7 = Signals(5)

class _51Bundle(Bundle):
	_37, _53, _45, _13, _29, _5, _61, _21, _58 = Signals(9)

class _52Bundle(Bundle):
	_1, _37, _43, _10, _30, _36, _42, _12, _13, _40, _16, _4, _28, _18, _19, _6, _24, _7, _34, _31, _22, _46, _25 = Signals(23)

class _53Bundle(Bundle):
	_right_oldest_T, _oldest_T, _left_oldest_T, _right_oldest_T_1, _right_oldest_T_37, _right_oldest_T_43, _right_oldest_T_10, _right_oldest_T_30, _right_oldest_T_36, _right_oldest_T_42, _right_oldest_T_12, _right_oldest_T_13, _right_oldest_T_40, _right_oldest_T_16, _right_oldest_T_4, _right_oldest_T_28, _right_oldest_T_18, _right_oldest_T_19, _right_oldest_T_6, _right_oldest_T_24, _right_oldest_T_7, _right_oldest_T_34, _right_oldest_T_31, _right_oldest_T_22, _right_oldest_T_46, _right_oldest_T_25, _oldest_T_1, _oldest_T_37, _oldest_T_43, _oldest_T_10, _oldest_T_30, _oldest_T_36, _oldest_T_42, _oldest_T_12, _oldest_T_13, _oldest_T_40, _oldest_T_16, _oldest_T_4, _oldest_T_28, _oldest_T_18, _oldest_T_19, _oldest_T_6, _oldest_T_24, _oldest_T_7, _oldest_T_34, _oldest_T_31, _oldest_T_22, _oldest_T_46, _oldest_T_25, _left_oldest_T_1, _left_oldest_T_37, _left_oldest_T_43, _left_oldest_T_10, _left_oldest_T_30, _left_oldest_T_36, _left_oldest_T_42, _left_oldest_T_12, _left_oldest_T_13, _left_oldest_T_40, _left_oldest_T_16, _left_oldest_T_4, _left_oldest_T_28, _left_oldest_T_18, _left_oldest_T_19, _left_oldest_T_6, _left_oldest_T_24, _left_oldest_T_7, _left_oldest_T_34, _left_oldest_T_31, _left_oldest_T_22, _left_oldest_T_46, _left_oldest_T_25 = Signals(72)

class _54Bundle(Bundle):
	_left = _53Bundle.from_prefix("_left")
	_right = _53Bundle.from_prefix("_right")
	_flushItself_T = _51Bundle.from_prefix("_flushItself_T")
	_oldest_T, _oldest_T_1, _oldest_T_37, _oldest_T_43, _oldest_T_10, _oldest_T_30, _oldest_T_36, _oldest_T_42, _oldest_T_12, _oldest_T_13, _oldest_T_40, _oldest_T_16, _oldest_T_4, _oldest_T_28, _oldest_T_18, _oldest_T_19, _oldest_T_6, _oldest_T_24, _oldest_T_7, _oldest_T_34, _oldest_T_31, _oldest_T_22, _oldest_T_46, _oldest_T_25 = Signals(24)

class _55Bundle(Bundle):
	_select = _54Bundle.from_prefix("_select")
	_oldest_T, _right_oldest_T, _left_oldest_T, _oldest_T_1, _oldest_T_10, _oldest_T_6, _oldest_T_4, _oldest_T_7, _right_oldest_T_1, _right_oldest_T_10, _right_oldest_T_6, _right_oldest_T_4, _right_oldest_T_7, _left_oldest_T_1, _left_oldest_T_10, _left_oldest_T_6, _left_oldest_T_4, _left_oldest_T_7 = Signals(18)

class _56Bundle(Bundle):
	_entryNeedCheck = _49Bundle.from_prefix("_entryNeedCheck")
	_lqSelect = _55Bundle.from_prefix("_lqSelect")

class _57Bundle(Bundle):
	_canAllocate = _0Bundle.from_prefix("_canAllocate")
	_allocateSlot = _0Bundle.from_prefix("_allocateSlot")

class _58Bundle(Bundle):
	_1 = _3Bundle.from_prefix("_1")
	_0 = _3Bundle.from_prefix("_0")

class _59Bundle(Bundle):
	_valid_delay_io_out = Signal()

class _60Bundle(Bundle):
	_1 = _59Bundle.from_prefix("_1")
	_0 = _59Bundle.from_prefix("_0")

class _61Bundle(Bundle):
	_freeList_io = _57Bundle.from_prefix("_freeList_io")
	_deqNotBlock_T = _46Bundle.from_prefix("_deqNotBlock_T")
	_maskModule_io_violationMmask = _58Bundle.from_prefix("_maskModule_io_violationMmask")
	_paddrModule_io_violationMmask = _58Bundle.from_prefix("_paddrModule_io_violationMmask")
	_rollbackLqWb = _60Bundle.from_prefix("_rollbackLqWb")
	_detectedRollback = _56Bundle.from_prefix("_detectedRollback")

class _64Bundle(Bundle):
	_uop = _42Bundle.from_prefix("_uop")
	_mask, _data_valid, _paddr = Signals(3)

class _65Bundle(Bundle):
	_bits = _64Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _66Bundle(Bundle):
	_req = _65Bundle.from_prefix("_req")
	_revoke = Signal()

class _67Bundle(Bundle):
	_2 = _66Bundle.from_prefix("_2")
	_0 = _66Bundle.from_prefix("_0")
	_1 = _66Bundle.from_prefix("_1")

class _68Bundle(Bundle):
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_robIdx = _5Bundle.from_prefix("_robIdx")
	_isRVC, _ftqOffset = Signals(2)

class _69Bundle(Bundle):
	_bits = _68Bundle.from_prefix("_bits")
	_valid = Signal()

class _70Bundle(Bundle):
	_1 = _69Bundle.from_prefix("_1")
	_0 = _69Bundle.from_prefix("_0")

class _71Bundle(Bundle):
	_uop_robIdx = _5Bundle.from_prefix("_uop_robIdx")
	_mask, _paddr, _miss = Signals(3)

class _72Bundle(Bundle):
	_bits = _71Bundle.from_prefix("_bits")
	_valid = Signal()

class _73Bundle(Bundle):
	_0 = _72Bundle.from_prefix("_0")
	_1 = _72Bundle.from_prefix("_1")

class _74Bundle(Bundle):
	_rollback = _70Bundle.from_prefix("_rollback")
	_stIssuePtr = _5Bundle.from_prefix("_stIssuePtr")
	_stAddrReadySqPtr = _5Bundle.from_prefix("_stAddrReadySqPtr")
	_storeIn = _73Bundle.from_prefix("_storeIn")
	_query = _67Bundle.from_prefix("_query")
	_redirect = _11Bundle.from_prefix("_redirect")
	_lqFull = Signal()

class LoadQueueRAWBundle(Bundle):
	LoadQueueRAW_ = _61Bundle.from_prefix("LoadQueueRAW_")
	io = _74Bundle.from_prefix("io")
	LoadQueueRAW = _44Bundle.from_prefix("LoadQueueRAW")
	reset, clock = Signals(2)