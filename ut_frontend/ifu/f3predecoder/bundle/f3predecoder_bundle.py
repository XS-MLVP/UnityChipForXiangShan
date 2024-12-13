from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_11, _0, _2, _12, _10, _5, _3, _14, _8, _13, _7, _6, _9, _1, _4, _15 = Signals(16)

class _1Bundle(Bundle):
	_brType, _isCall, _isRet = Signals(3)

class _2Bundle(Bundle):
	_11 = _1Bundle.from_prefix("_11")
	_14 = _1Bundle.from_prefix("_14")
	_9 = _1Bundle.from_prefix("_9")
	_5 = _1Bundle.from_prefix("_5")
	_2 = _1Bundle.from_prefix("_2")
	_6 = _1Bundle.from_prefix("_6")
	_15 = _1Bundle.from_prefix("_15")
	_13 = _1Bundle.from_prefix("_13")
	_7 = _1Bundle.from_prefix("_7")
	_1 = _1Bundle.from_prefix("_1")
	_10 = _1Bundle.from_prefix("_10")
	_4 = _1Bundle.from_prefix("_4")
	_0 = _1Bundle.from_prefix("_0")
	_12 = _1Bundle.from_prefix("_12")
	_3 = _1Bundle.from_prefix("_3")
	_8 = _1Bundle.from_prefix("_8")

class _3Bundle(Bundle):
	_in_instr = _0Bundle.from_prefix("_in_instr")
	_out_pd = _2Bundle.from_prefix("_out_pd")

class F3PreDecoderBundle(Bundle):
	io = _3Bundle.from_prefix("io")

