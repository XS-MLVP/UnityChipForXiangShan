from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_2, _1, _10, _15, _4, _7, _8, _0, _11, _6, _5, _12, _14, _9, _3, _13 = Signals(16)

class _1Bundle(Bundle):
	_23, _31, _26, _33, _30, _24, _25, _32, _27 = Signals(9)

class _2Bundle(Bundle):
	_2, _4, _7, _6, _5, _3 = Signals(6)

class _3Bundle(Bundle):
	_lastIsValidEnd = _1Bundle.from_prefix("_lastIsValidEnd")
	_validEnd = _2Bundle.from_prefix("_validEnd")

class _4Bundle(Bundle):
	_2, _1, _4, _7, _6, _5, _3 = Signals(7)

class _5Bundle(Bundle):
	_h = _3Bundle.from_prefix("_h")
	_lastIsValidEnd = _1Bundle.from_prefix("_lastIsValidEnd")
	_validEnd = _4Bundle.from_prefix("_validEnd")
	_currentIsRVC = _0Bundle.from_prefix("_currentIsRVC")

class _6Bundle(Bundle):
	_2, _1, _10, _15, _16, _4, _7, _8, _0, _11, _6, _5, _12, _14, _9, _3, _13 = Signals(17)

class _7Bundle(Bundle):
	_2, _10, _15, _4, _7, _8, _11, _6, _5, _12, _14, _9, _3, _13 = Signals(14)

class _8Bundle(Bundle):
	_isRVC = Signal()

class _9Bundle(Bundle):
	_isRVC, _valid = Signals(2)

class _10Bundle(Bundle):
	_2 = _9Bundle.from_prefix("_2")
	_3 = _9Bundle.from_prefix("_3")
	_14 = _9Bundle.from_prefix("_14")
	_8 = _9Bundle.from_prefix("_8")
	_1 = _9Bundle.from_prefix("_1")
	_9 = _9Bundle.from_prefix("_9")
	_4 = _9Bundle.from_prefix("_4")
	_6 = _9Bundle.from_prefix("_6")
	_10 = _9Bundle.from_prefix("_10")
	_15 = _9Bundle.from_prefix("_15")
	_11 = _9Bundle.from_prefix("_11")
	_13 = _9Bundle.from_prefix("_13")
	_5 = _9Bundle.from_prefix("_5")
	_12 = _9Bundle.from_prefix("_12")
	_7 = _9Bundle.from_prefix("_7")
	_0 = _8Bundle.from_prefix("_0")

class _11Bundle(Bundle):
	_instr = _0Bundle.from_prefix("_instr")
	_jumpOffset = _0Bundle.from_prefix("_jumpOffset")
	_hasHalfValid = _7Bundle.from_prefix("_hasHalfValid")
	_pd = _10Bundle.from_prefix("_pd")

class _12Bundle(Bundle):
	_in_bits_data = _6Bundle.from_prefix("_in_bits_data")
	_out = _11Bundle.from_prefix("_out")

class PreDecodeBundle(Bundle):
	io = _12Bundle.from_prefix("io")
	PreDecode = _5Bundle.from_prefix("PreDecode")

