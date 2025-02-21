from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_fpWen, _fuOpType = Signals(2)

class _1Bundle(Bundle):
	_uop = _0Bundle.from_prefix("_uop")
	_lqData, _addrOffset = Signals(2)

class _2Bundle(Bundle):
	_r = _1Bundle.from_prefix("_r")

class _3Bundle(Bundle):
	_2 = _2Bundle.from_prefix("_2")

class _4Bundle(Bundle):
	_REG = Signal()

class _5Bundle(Bundle):
	_1 = _4Bundle.from_prefix("_1")
	_2 = _4Bundle.from_prefix("_2")
	_0 = _4Bundle.from_prefix("_0")

class _6Bundle(Bundle):
	_r_robIdx_value = Signal()

class _7Bundle(Bundle):
	_1 = _6Bundle.from_prefix("_1")
	_0 = _6Bundle.from_prefix("_0")
	_2 = _6Bundle.from_prefix("_2")

class _8Bundle(Bundle):
	_mmio = _5Bundle.from_prefix("_mmio")
	_uop = _7Bundle.from_prefix("_uop")

class _9Bundle(Bundle):
	_value, _flag = Signals(2)

class _10Bundle(Bundle):
	_ftqIdx = _9Bundle.from_prefix("_ftqIdx")
	_robIdx = _9Bundle.from_prefix("_robIdx")
	_isRVC, _ftqOffset, _level = Signals(3)

class _11Bundle(Bundle):
	_bits_r = _10Bundle.from_prefix("_bits_r")
	_valid_last_REG = Signal()

class _12Bundle(Bundle):
	_rob = _8Bundle.from_prefix("_rob")
	_mmioRawData = _3Bundle.from_prefix("_mmioRawData")
	_rollback = _11Bundle.from_prefix("_rollback")

class _13Bundle(Bundle):
	_robIdx = _9Bundle.from_prefix("_robIdx")
	_level = Signal()

class _14Bundle(Bundle):
	_bits_r = _13Bundle.from_prefix("_bits_r")
	_valid_REG = Signal()

class _15Bundle(Bundle):
	_6, _7, _4, _3, _2 = Signals(5)

class _16Bundle(Bundle):
	_0 = Signal()

class _17Bundle(Bundle):
	_0, _1 = Signals(2)

class _18Bundle(Bundle):
	_2 = _17Bundle.from_prefix("_2")
	_1 = _16Bundle.from_prefix("_1")

class _19Bundle(Bundle):
	_0, _1, _2 = Signals(3)

class _20Bundle(Bundle):
	_uop_robIdx_value, _mmio = Signals(2)

class _21Bundle(Bundle):
	_0 = _20Bundle.from_prefix("_0")
	_1 = _20Bundle.from_prefix("_1")
	_2 = _20Bundle.from_prefix("_2")

class _22Bundle(Bundle):
	_0, _6, _5, _9, _7, _4, _8, _1, _3, _2, _10 = Signals(11)

class _23Bundle(Bundle):
	_5, _21, _13, _4, _3 = Signals(5)

class _24Bundle(Bundle):
	_veew, _vstart = Signals(2)

class _25Bundle(Bundle):
	_ftqPtr = _9Bundle.from_prefix("_ftqPtr")
	_sqIdx = _9Bundle.from_prefix("_sqIdx")
	_waitForRobIdx = _9Bundle.from_prefix("_waitForRobIdx")
	_lqIdx = _9Bundle.from_prefix("_lqIdx")
	_vpu = _24Bundle.from_prefix("_vpu")
	_exceptionVec = _23Bundle.from_prefix("_exceptionVec")
	_fuOpType, _storeSetHit, _loadWaitBit, _loadWaitStrict, _preDecodeInfo_isRVC, _rfWen, _uopIdx, _pdest, _trigger, _fpWen, _ftqOffset = Signals(11)

class _26Bundle(Bundle):
	_rep_info_cause = _22Bundle.from_prefix("_rep_info_cause")
	_uop = _25Bundle.from_prefix("_uop")
	_mmio, _schedIndex, _vecActive, _vaddr, _gpaddr, _mask, _isHyper, _isvec, _is128bit, _isForVSnonLeafPTE, _fullva, _nc, _paddr, _memBackTypeMM = Signals(14)

class _27Bundle(Bundle):
	_ptr = _9Bundle.from_prefix("_ptr")
	_bits = _26Bundle.from_prefix("_bits")
	_valid = Signal()

class _28Bundle(Bundle):
	_0 = _27Bundle.from_prefix("_0")
	_1 = _27Bundle.from_prefix("_1")
	_swap = Signal()

class _29Bundle(Bundle):
	_robIdx = _9Bundle.from_prefix("_robIdx")
	_ftqPtr = _9Bundle.from_prefix("_ftqPtr")
	_sqIdx = _9Bundle.from_prefix("_sqIdx")
	_waitForRobIdx = _9Bundle.from_prefix("_waitForRobIdx")
	_lqIdx = _9Bundle.from_prefix("_lqIdx")
	_vpu = _24Bundle.from_prefix("_vpu")
	_exceptionVec = _23Bundle.from_prefix("_exceptionVec")
	_fuOpType, _loadWaitBit, _loadWaitStrict, _preDecodeInfo_isRVC, _rfWen, _storeSetHit, _uopIdx, _pdest, _trigger, _fpWen, _ftqOffset = Signals(11)

class _30Bundle(Bundle):
	_rep_info_cause = _22Bundle.from_prefix("_rep_info_cause")
	_uop = _29Bundle.from_prefix("_uop")
	_mmio, _schedIndex, _vecActive, _vaddr, _gpaddr, _mask, _isHyper, _isvec, _is128bit, _isForVSnonLeafPTE, _fullva, _nc, _paddr, _memBackTypeMM = Signals(14)

class _31Bundle(Bundle):
	_bits = _30Bundle.from_prefix("_bits")
	_valid = Signal()

class _32Bundle(Bundle):
	_0 = _31Bundle.from_prefix("_0")
	_swap = Signal()

class _33Bundle(Bundle):
	_tmp1 = _32Bundle.from_prefix("_tmp1")
	_tmp0 = _28Bundle.from_prefix("_tmp0")
	_tmp2_swap = Signal()

class _34Bundle(Bundle):
	_req = _21Bundle.from_prefix("_req")
	_valid = _19Bundle.from_prefix("_valid")
	_sortedVec = _33Bundle.from_prefix("_sortedVec")

class _35Bundle(Bundle):
	_2 = _30Bundle.from_prefix("_2")
	_0 = _30Bundle.from_prefix("_0")
	_1 = _30Bundle.from_prefix("_1")

class _36Bundle(Bundle):
	_bits = _13Bundle.from_prefix("_bits")
	_valid = Signal()

class _37Bundle(Bundle):
	_1 = _36Bundle.from_prefix("_1")
	_3 = _36Bundle.from_prefix("_3")
	_5 = _36Bundle.from_prefix("_5")
	_4, _2 = Signals(2)

class _38Bundle(Bundle):
	_req = _35Bundle.from_prefix("_req")
	_enqValidVec = _19Bundle.from_prefix("_enqValidVec")
	_enqueue = _19Bundle.from_prefix("_enqueue")
	_valid_REG, _valid_REG_4, _valid_REG_2 = Signals(3)

class _39Bundle(Bundle):
	_s1 = _34Bundle.from_prefix("_s1")
	_lastCycleRedirect = _14Bundle.from_prefix("_lastCycleRedirect")
	_lastLastCycleRedirect = _14Bundle.from_prefix("_lastLastCycleRedirect")
	_io = _12Bundle.from_prefix("_io")
	_oldestOneHot_compareVec = _18Bundle.from_prefix("_oldestOneHot_compareVec")
	_reqNeedCheck = _19Bundle.from_prefix("_reqNeedCheck")
	_s2 = _38Bundle.from_prefix("_s2")
	_offset, _mmioOut_valid, _ncOutValid, _mmioReq_ready, _mmioSelect, _ncOutValid_6, _ncOutValid_7, _ncOutValid_4, _ncOutValid_3, _ncOutValid_2 = Signals(10)

class _40Bundle(Bundle):
	_11, _24, _23, _25, _17, _8, _3, _6, _12, _14, _21, _9, _28, _4, _15, _2, _26, _0, _20, _18, _22, _5, _19, _10, _16, _27, _13, _7 = Signals(28)

class _41Bundle(Bundle):
	_5, _21, _19, _13, _4, _3 = Signals(6)

class _42Bundle(Bundle):
	_exceptionVec = _41Bundle.from_prefix("_exceptionVec")
	_robIdx = _9Bundle.from_prefix("_robIdx")
	_uopIdx = Signal()

class _43Bundle(Bundle):
	_uop = _42Bundle.from_prefix("_uop")
	_gpaddr, _isHyper, _isForVSnonLeafPTE, _fullva = Signals(4)

class _44Bundle(Bundle):
	_bits = _43Bundle.from_prefix("_bits")
	_valid = Signal()

class _45Bundle(Bundle):
	_ftqPtr = _9Bundle.from_prefix("_ftqPtr")
	_waitForRobIdx = _9Bundle.from_prefix("_waitForRobIdx")
	_robIdx = _9Bundle.from_prefix("_robIdx")
	_lqIdx = _9Bundle.from_prefix("_lqIdx")
	_sqIdx = _9Bundle.from_prefix("_sqIdx")
	_vpu = _24Bundle.from_prefix("_vpu")
	_exceptionVec = _41Bundle.from_prefix("_exceptionVec")
	_fuOpType, _rfWen, _trigger, _fpWen, _storeSetHit, _preDecodeInfo_isRVC, _loadWaitStrict, _uopIdx, _replayInst, _flushPipe, _loadWaitBit, _pdest, _ftqOffset = Signals(13)

class _46Bundle(Bundle):
	_bits_uop = _45Bundle.from_prefix("_bits_uop")
	_valid = Signal()

class _47Bundle(Bundle):
	_19, _4 = Signals(2)

class _48Bundle(Bundle):
	_robIdx = _9Bundle.from_prefix("_robIdx")
	_ftqPtr = _9Bundle.from_prefix("_ftqPtr")
	_sqIdx = _9Bundle.from_prefix("_sqIdx")
	_waitForRobIdx = _9Bundle.from_prefix("_waitForRobIdx")
	_lqIdx = _9Bundle.from_prefix("_lqIdx")
	_exceptionVec = _47Bundle.from_prefix("_exceptionVec")
	_vpu = _24Bundle.from_prefix("_vpu")
	_fuOpType, _loadWaitBit, _loadWaitStrict, _preDecodeInfo_isRVC, _rfWen, _storeSetHit, _uopIdx, _pdest, _fpWen, _ftqOffset = Signals(10)

class _49Bundle(Bundle):
	_uop = _48Bundle.from_prefix("_uop")
	_schedIndex, _vaddr, _vecActive, _isvec, _data, _is128bit, _paddr = Signals(7)

class _50Bundle(Bundle):
	_bits = _49Bundle.from_prefix("_bits")
	_valid = Signal()

class _51Bundle(Bundle):
	_vaddr, _mask, _nc, _memBackTypeMM, _addr = Signals(5)

class _52Bundle(Bundle):
	_bits = _51Bundle.from_prefix("_bits")
	_valid = Signal()

class _53Bundle(Bundle):
	_ncOut = _50Bundle.from_prefix("_ncOut")
	_uncache_req = _52Bundle.from_prefix("_uncache_req")
	_exception = _44Bundle.from_prefix("_exception")
	_mmioRawData = _1Bundle.from_prefix("_mmioRawData")
	_mmioOut = _46Bundle.from_prefix("_mmioOut")
	_mmioSelect, _flush = Signals(2)

class _54Bundle(Bundle):
	_io = _53Bundle.from_prefix("_io")

class _55Bundle(Bundle):
	_3 = _54Bundle.from_prefix("_3")
	_2 = _54Bundle.from_prefix("_2")
	_1 = _54Bundle.from_prefix("_1")
	_0 = _54Bundle.from_prefix("_0")

class _56Bundle(Bundle):
	_allocateSlot = _19Bundle.from_prefix("_allocateSlot")
	_canAllocate = _19Bundle.from_prefix("_canAllocate")

class _57Bundle(Bundle):
	_9, _2 = Signals(2)

class _58Bundle(Bundle):
	_rollback_valid_flushItself_T = _57Bundle.from_prefix("_rollback_valid_flushItself_T")
	_exception_bits_T = Signal()

class _59Bundle(Bundle):
	_ready = Signal()

class _60Bundle(Bundle):
	_3 = _59Bundle.from_prefix("_3")
	_1 = _59Bundle.from_prefix("_1")
	_0 = _59Bundle.from_prefix("_0")
	_2 = _59Bundle.from_prefix("_2")

class _61Bundle(Bundle):
	_vaddr, _mask, _id, _nc, _memBackTypeMM, _addr = Signals(6)

class _62Bundle(Bundle):
	_bits = _61Bundle.from_prefix("_bits")
	_valid = Signal()

class _63Bundle(Bundle):
	_in = _60Bundle.from_prefix("_in")
	_out = _62Bundle.from_prefix("_out")

class _64Bundle(Bundle):
	_13, _6, _19 = Signals(3)

class _65Bundle(Bundle):
	_454, _439, _444 = Signals(3)

class _66Bundle(Bundle):
	_io_in_ready = Signal()

class _67Bundle(Bundle):
	_4 = _66Bundle.from_prefix("_4")
	_1 = _66Bundle.from_prefix("_1")
	_3 = _66Bundle.from_prefix("_3")
	_io_in_ready = Signal()

class _68Bundle(Bundle):
	_21, _5, _13 = Signals(3)

class _69Bundle(Bundle):
	_pipelineReg = _67Bundle.from_prefix("_pipelineReg")
	_s2_valid_flushItself_T = _68Bundle.from_prefix("_s2_valid_flushItself_T")
	_ncReqArb_io = _63Bundle.from_prefix("_ncReqArb_io")
	_entries = _55Bundle.from_prefix("_entries")
	_oldestOneHot_resultOnehot_T = _64Bundle.from_prefix("_oldestOneHot_resultOnehot_T")
	_io = _58Bundle.from_prefix("_io")
	_oldestRedirect_T = _65Bundle.from_prefix("_oldestRedirect_T")
	_freeList_io = _56Bundle.from_prefix("_freeList_io")
	_GEN, _GEN_11, _GEN_24, _GEN_23, _GEN_25, _GEN_17, _GEN_8, _GEN_3, _GEN_6, _GEN_12, _GEN_14, _GEN_21, _GEN_9, _GEN_28, _GEN_4, _GEN_15, _GEN_2, _GEN_26, _GEN_0, _GEN_20, _GEN_18, _GEN_22, _GEN_5, _GEN_19, _GEN_10, _GEN_16, _GEN_27, _GEN_13, _GEN_7 = Signals(29)

class _70Bundle(Bundle):
	_bits_uop = _45Bundle.from_prefix("_bits_uop")
	_valid, _ready = Signals(2)

class _71Bundle(Bundle):
	_2 = _70Bundle.from_prefix("_2")

class _72Bundle(Bundle):
	_2 = _1Bundle.from_prefix("_2")

class _73Bundle(Bundle):
	_bits = _49Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _74Bundle(Bundle):
	_1 = _73Bundle.from_prefix("_1")
	_2 = _73Bundle.from_prefix("_2")
	_0 = _73Bundle.from_prefix("_0")

class _75Bundle(Bundle):
	_1 = _31Bundle.from_prefix("_1")
	_0 = _31Bundle.from_prefix("_0")
	_2 = _31Bundle.from_prefix("_2")

class _76Bundle(Bundle):
	_robIdx_value = Signal()

class _77Bundle(Bundle):
	_0 = _76Bundle.from_prefix("_0")
	_2 = _76Bundle.from_prefix("_2")
	_1 = _76Bundle.from_prefix("_1")

class _78Bundle(Bundle):
	_mmio = _19Bundle.from_prefix("_mmio")
	_uop = _77Bundle.from_prefix("_uop")
	_pendingPtr = _9Bundle.from_prefix("_pendingPtr")
	_pendingMMIOld = Signal()

class _79Bundle(Bundle):
	_bits = _10Bundle.from_prefix("_bits")
	_valid = Signal()

class _80Bundle(Bundle):
	_vaddr, _mask, _data, _id, _nc, _memBackTypeMM, _addr, _cmd = Signals(8)

class _81Bundle(Bundle):
	_bits = _80Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _82Bundle(Bundle):
	_nderr, _data, _id = Signals(3)

class _83Bundle(Bundle):
	_bits = _82Bundle.from_prefix("_bits")
	_valid = Signal()

class _84Bundle(Bundle):
	_req = _81Bundle.from_prefix("_req")
	_resp = _83Bundle.from_prefix("_resp")

class _85Bundle(Bundle):
	_rollback = _79Bundle.from_prefix("_rollback")
	_uncache = _84Bundle.from_prefix("_uncache")
	_req = _75Bundle.from_prefix("_req")
	_ncOut = _74Bundle.from_prefix("_ncOut")
	_rob = _78Bundle.from_prefix("_rob")
	_mmioRawData = _72Bundle.from_prefix("_mmioRawData")
	_exception = _44Bundle.from_prefix("_exception")
	_mmioOut = _71Bundle.from_prefix("_mmioOut")
	_redirect = _36Bundle.from_prefix("_redirect")

class LoadQueueUncacheBundle(Bundle):
	io = _85Bundle.from_prefix("io")
	LoadQueueUncache = _39Bundle.from_prefix("LoadQueueUncache")
	LoadQueueUncache_ = _69Bundle.from_prefix("LoadQueueUncache_")
	clock, reset = Signals(2)

