from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_13, _6, _9, _2, _4, _10, _14, _3, _7, _12, _11, _15, _1, _8, _5, _0 = Signals(16)

class _1Bundle(Bundle):
	_brType = Signal()

class _2Bundle(Bundle):
	_12 = _1Bundle.from_prefix("_12")
	_1 = _1Bundle.from_prefix("_1")
	_9 = _1Bundle.from_prefix("_9")
	_15 = _1Bundle.from_prefix("_15")
	_6 = _1Bundle.from_prefix("_6")
	_5 = _1Bundle.from_prefix("_5")
	_7 = _1Bundle.from_prefix("_7")
	_3 = _1Bundle.from_prefix("_3")
	_4 = _1Bundle.from_prefix("_4")
	_2 = _1Bundle.from_prefix("_2")
	_11 = _1Bundle.from_prefix("_11")
	_8 = _1Bundle.from_prefix("_8")
	_14 = _1Bundle.from_prefix("_14")
	_13 = _1Bundle.from_prefix("_13")
	_10 = _1Bundle.from_prefix("_10")
	_0 = _1Bundle.from_prefix("_0")

class _3Bundle(Bundle):
	_13, _6, _2, _4, _10, _14, _3, _7, _12, _11, _9, _1, _8, _5, _0 = Signals(15)

class _4Bundle(Bundle):
	_fixedRange, _predTargetNext, _fixedRangeNext, _predTakenNext, _takenIdxNext = Signals(5)
	_retFaultVec = _0Bundle.from_prefix("_retFaultVec")
	_seqTargetsNext = _0Bundle.from_prefix("_seqTargetsNext")
	_notCFITakenNext = _0Bundle.from_prefix("_notCFITakenNext")
	_jalFaultVec = _0Bundle.from_prefix("_jalFaultVec")
	_jalFaultVecNext = _0Bundle.from_prefix("_jalFaultVecNext")
	_targetFault = _0Bundle.from_prefix("_targetFault")
	_jumpTargetsNext = _0Bundle.from_prefix("_jumpTargetsNext")
	_invalidTakenNext = _0Bundle.from_prefix("_invalidTakenNext")
	_retFaultVecNext = _0Bundle.from_prefix("_retFaultVecNext")
	_instrValidNext = _0Bundle.from_prefix("_instrValidNext")
	_pdsNext = _2Bundle.from_prefix("_pdsNext")
	_remaskFault = _3Bundle.from_prefix("_remaskFault")

class _5Bundle(Bundle):
	_valid, _bits = Signals(2)

class _6Bundle(Bundle):
	_isRet, _brType, _isRVC = Signals(3)

class _7Bundle(Bundle):
	_0 = _6Bundle.from_prefix("_0")
	_1 = _6Bundle.from_prefix("_1")
	_4 = _6Bundle.from_prefix("_4")
	_7 = _6Bundle.from_prefix("_7")
	_10 = _6Bundle.from_prefix("_10")
	_9 = _6Bundle.from_prefix("_9")
	_11 = _6Bundle.from_prefix("_11")
	_13 = _6Bundle.from_prefix("_13")
	_3 = _6Bundle.from_prefix("_3")
	_2 = _6Bundle.from_prefix("_2")
	_8 = _6Bundle.from_prefix("_8")
	_12 = _6Bundle.from_prefix("_12")
	_5 = _6Bundle.from_prefix("_5")
	_15 = _6Bundle.from_prefix("_15")
	_14 = _6Bundle.from_prefix("_14")
	_6 = _6Bundle.from_prefix("_6")

class _8Bundle(Bundle):
	_fire_in, _target = Signals(2)
	_instrValid = _0Bundle.from_prefix("_instrValid")
	_instrRange = _0Bundle.from_prefix("_instrRange")
	_pc = _0Bundle.from_prefix("_pc")
	_jumpOffset = _0Bundle.from_prefix("_jumpOffset")
	_ftqOffset = _5Bundle.from_prefix("_ftqOffset")
	_pds = _7Bundle.from_prefix("_pds")

class _9Bundle(Bundle):
	_fixedRange = _0Bundle.from_prefix("_fixedRange")
	_fixedTaken = _0Bundle.from_prefix("_fixedTaken")

class singleFaultTypeBundle(Bundle):
	_value = Signal()

class faultTypesBundle(Bundle):
	_12 = singleFaultTypeBundle.from_prefix("_12")
	_1 = singleFaultTypeBundle.from_prefix("_1")
	_9 = singleFaultTypeBundle.from_prefix("_9")
	_15 = singleFaultTypeBundle.from_prefix("_15")
	_6 = singleFaultTypeBundle.from_prefix("_6")
	_5 = singleFaultTypeBundle.from_prefix("_5")
	_7 = singleFaultTypeBundle.from_prefix("_7")
	_3 = singleFaultTypeBundle.from_prefix("_3")
	_4 = singleFaultTypeBundle.from_prefix("_4")
	_2 = singleFaultTypeBundle.from_prefix("_2")
	_11 = singleFaultTypeBundle.from_prefix("_11")
	_8 = singleFaultTypeBundle.from_prefix("_8")
	_14 = singleFaultTypeBundle.from_prefix("_14")
	_13 = singleFaultTypeBundle.from_prefix("_13")
	_10 = singleFaultTypeBundle.from_prefix("_10")
	_0 = singleFaultTypeBundle.from_prefix("_0")

class _10Bundle(Bundle):
	_fixedTarget = _0Bundle.from_prefix("_fixedTarget")
	_fixedMissPred = _0Bundle.from_prefix("_fixedMissPred")
	_jalTarget = _0Bundle.from_prefix("_jalTarget")
	_faultType = faultTypesBundle.from_prefix("_faultType")

class _11Bundle(Bundle):
	_stage2Out = _10Bundle.from_prefix("_stage2Out")
	_stage1Out = _9Bundle.from_prefix("_stage1Out")

class _12Bundle(Bundle):
	_in = _8Bundle.from_prefix("_in")
	_out = _11Bundle.from_prefix("_out")

class PredCheckerBundle(Bundle):
	clock = Signal()
	PredChecker = _4Bundle.from_prefix("PredChecker")
	io = _12Bundle.from_prefix("io")

