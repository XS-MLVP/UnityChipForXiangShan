from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_0 = Signal()

class _1Bundle(Bundle):
	_io_injecting = _0Bundle.from_prefix("_io_injecting")
	_eccctrl_istatus = Signal()

class _2Bundle(Bundle):
	_address, _opcode, _mask, _data, _size, _source = Signals(6)

class _3Bundle(Bundle):
	_bits = _2Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _4Bundle(Bundle):
	_opcode, _size, _data, _source = Signals(4)

class _5Bundle(Bundle):
	_bits = _4Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _6Bundle(Bundle):
	_a = _3Bundle.from_prefix("_a")
	_d = _5Bundle.from_prefix("_d")

class _7Bundle(Bundle):
	_waymask, _virIdx = Signals(2)

class _8Bundle(Bundle):
	_bits = _7Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _9Bundle(Bundle):
	_1, _0 = Signals(2)

class _10Bundle(Bundle):
	_bits_vSetIdx = _9Bundle.from_prefix("_bits_vSetIdx")
	_ready, _valid = Signals(2)

class _11Bundle(Bundle):
	_1, _2, _0, _3 = Signals(4)

class _12Bundle(Bundle):
	_0 = _11Bundle.from_prefix("_0")

class _13Bundle(Bundle):
	_tag = Signal()

class _14Bundle(Bundle):
	_1 = _13Bundle.from_prefix("_1")
	_2 = _13Bundle.from_prefix("_2")
	_3 = _13Bundle.from_prefix("_3")
	_0 = _13Bundle.from_prefix("_0")

class _15Bundle(Bundle):
	_0 = _14Bundle.from_prefix("_0")

class _16Bundle(Bundle):
	_entryValid = _12Bundle.from_prefix("_entryValid")
	_metas = _15Bundle.from_prefix("_metas")

class _17Bundle(Bundle):
	_phyTag, _waymask, _virIdx, _bankIdx = Signals(4)

class _18Bundle(Bundle):
	_bits = _17Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _19Bundle(Bundle):
	_dataWrite = _8Bundle.from_prefix("_dataWrite")
	_metaRead = _10Bundle.from_prefix("_metaRead")
	_metaReadResp = _16Bundle.from_prefix("_metaReadResp")
	_metaWrite = _18Bundle.from_prefix("_metaWrite")
	_ecc_enable, _injecting = Signals(2)

class CtrlUnitBundle(Bundle):
	io = _19Bundle.from_prefix("io")
	ICacheCtrlUnit = _1Bundle.from_prefix("ICacheCtrlUnit")
	auto_in = _6Bundle.from_prefix("auto_in")
	clock, reset = Signals(2)
