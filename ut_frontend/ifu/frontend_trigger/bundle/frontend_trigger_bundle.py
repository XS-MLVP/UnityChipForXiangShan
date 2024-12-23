from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_select, _matchType, _timing, _action, _tdata2, _chain = Signals(6)

class _1Bundle(Bundle):
	_2 = _0Bundle.from_prefix("_2")
	_0 = _0Bundle.from_prefix("_0")
	_3 = _0Bundle.from_prefix("_3")
	_1 = _0Bundle.from_prefix("_1")

class _2Bundle(Bundle):
	_2, _3, _1 = Signals(3)

class _3Bundle(Bundle):
	_2, _0, _1 = Signals(3)

class _4Bundle(Bundle):
	_13 = _3Bundle.from_prefix("_13")
	_7 = _3Bundle.from_prefix("_7")
	_4 = _3Bundle.from_prefix("_4")
	_11 = _3Bundle.from_prefix("_11")
	_8 = _3Bundle.from_prefix("_8")
	_6 = _3Bundle.from_prefix("_6")
	_9 = _3Bundle.from_prefix("_9")
	_14 = _3Bundle.from_prefix("_14")
	_5 = _3Bundle.from_prefix("_5")
	_10 = _3Bundle.from_prefix("_10")
	_15 = _3Bundle.from_prefix("_15")
	_3 = _3Bundle.from_prefix("_3")
	_12 = _3Bundle.from_prefix("_12")
	_1, _0, _2, _1_2, _1_0, _1_1, _2_2, _2_0, _2_1 = Signals(9)

class _5Bundle(Bundle):
	_2, _0, _3, _1 = Signals(4)

class _7Bundle(Bundle):
	_10, _5, _2, _9, _6, _15, _13, _4, _8, _7, _12, _11, _14, _3, _1, _2_10, _2_5, _2_2, _2_9, _2_6, _2_15, _2_13, _2_3, _2_4, _2_8, _2_7, _2_12, _2_11, _2_1, _2_14, _3_10, _3_5, _3_2, _3_9, _3_6, _3_15, _3_13, _3_3, _3_4, _3_8, _3_7, _3_12, _3_11, _3_1, _3_14, _1_10, _1_5, _1_2, _1_9, _1_6, _1_15, _1_13, _1_3, _1_4, _1_8, _1_7, _1_12, _1_11, _1_1, _1_14 = Signals(60)

class _9Bundle(Bundle):
	_10, _3, _5, _9, _6, _0, _13, _2, _4, _8, _7, _12, _11, _1, _14, _3_10, _3_5, _3_2, _3_9, _3_6, _3_0, _3_13, _3_3, _3_4, _3_8, _3_7, _3_12, _3_11, _3_1, _3_14, _2_10, _2_5, _2_2, _2_9, _2_6, _2_0, _2_13, _2_3, _2_4, _2_8, _2_7, _2_12, _2_11, _2_1, _2_14, _1_10, _1_5, _1_2, _1_9, _1_6, _1_0, _1_13, _1_3, _1_4, _1_8, _1_7, _1_12, _1_11, _1_1, _1_14 = Signals(60)

class _10Bundle(Bundle):
	_13 = _3Bundle.from_prefix("_13")
	_7 = _3Bundle.from_prefix("_7")
	_11 = _3Bundle.from_prefix("_11")
	_2 = _3Bundle.from_prefix("_2")
	_0 = _3Bundle.from_prefix("_0")
	_4 = _3Bundle.from_prefix("_4")
	_5 = _3Bundle.from_prefix("_5")
	_6 = _3Bundle.from_prefix("_6")
	_14 = _3Bundle.from_prefix("_14")
	_15 = _3Bundle.from_prefix("_15")
	_1 = _3Bundle.from_prefix("_1")
	_8 = _3Bundle.from_prefix("_8")
	_9 = _3Bundle.from_prefix("_9")
	_10 = _3Bundle.from_prefix("_10")
	_3 = _3Bundle.from_prefix("_3")
	_12 = _3Bundle.from_prefix("_12")
	_carryRight = _9Bundle.from_prefix("_carryRight")
	_lowPCEqual = _7Bundle.from_prefix("_lowPCEqual")
	_lowPCGreater = _7Bundle.from_prefix("_lowPCGreater")
	_carry = _7Bundle.from_prefix("_carry")
	_highPC1Equal, _highPCGreater, _highPCEqual, _highPCLess, _highPC1Equal_2, _highPC1Equal_3, _highPC1Equal_1, _highPCGreater_2, _highPCGreater_3, _highPCGreater_1, _highPCEqual_2, _highPCEqual_3, _highPCEqual_1, _highPCLess_2, _highPCLess_3, _highPCLess_1 = Signals(16)

class _11Bundle(Bundle):
	_tdataVec = _1Bundle.from_prefix("_tdataVec")
	_triggerEnableVec = _5Bundle.from_prefix("_triggerEnableVec")
	_triggerHitVec = _10Bundle.from_prefix("_triggerHitVec")
	_trigger2TimingSameVec = _2Bundle.from_prefix("_trigger2TimingSameVec")
	_triggerCanFireVec = _4Bundle.from_prefix("_triggerCanFireVec")
	_triggerFireOH_enc, _triggerFireAction, _triggerFireOH_enc_10, _triggerFireOH_enc_5, _triggerFireOH_enc_2, _triggerFireOH_enc_9, _triggerFireOH_enc_6, _triggerFireOH_enc_15, _triggerFireOH_enc_13, _triggerFireOH_enc_3, _triggerFireOH_enc_4, _triggerFireOH_enc_8, _triggerFireOH_enc_7, _triggerFireOH_enc_12, _triggerFireOH_enc_11, _triggerFireOH_enc_1, _triggerFireOH_enc_14, _triggerFireAction_10, _triggerFireAction_5, _triggerFireAction_2, _triggerFireAction_9, _triggerFireAction_6, _triggerFireAction_15, _triggerFireAction_13, _triggerFireAction_3, _triggerFireAction_4, _triggerFireAction_8, _triggerFireAction_7, _triggerFireAction_12, _triggerFireAction_11, _triggerFireAction_1, _triggerFireAction_14 = Signals(32)

class _12Bundle(Bundle):
	_select, _matchType, _action, _tdata2, _chain = Signals(5)

class _13Bundle(Bundle):
	_tdata = _12Bundle.from_prefix("_tdata")
	_addr = Signal()

class _14Bundle(Bundle):
	_bits = _13Bundle.from_prefix("_bits")
	_valid = Signal()

class _15Bundle(Bundle):
	_tUpdate = _14Bundle.from_prefix("_tUpdate")
	_tEnableVec = _5Bundle.from_prefix("_tEnableVec")
	_debugMode, _triggerCanRaiseBpExp = Signals(2)

class _16Bundle(Bundle):
	_10, _5, _2, _9, _6, _0, _13, _15, _3, _4, _7, _12, _8, _11, _1, _14 = Signals(16)

class _17Bundle(Bundle):
	_frontendTrigger = _15Bundle.from_prefix("_frontendTrigger")
	_pc = _16Bundle.from_prefix("_pc")
	_triggered = _16Bundle.from_prefix("_triggered")

class FrontendTriggerBundle(Bundle):
	FrontendTrigger = _11Bundle.from_prefix("FrontendTrigger")
	io = _17Bundle.from_prefix("io")
	clock, reset = Signals(2)

