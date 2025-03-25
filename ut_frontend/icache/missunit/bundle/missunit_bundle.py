from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_acquire_valid, _req_ready = Signals(2)

class _1Bundle(Bundle):
	_io = _0Bundle.from_prefix("_io")

class _2Bundle(Bundle):
	_2 = _1Bundle.from_prefix("_2")
	_0 = _1Bundle.from_prefix("_0")
	_3 = _1Bundle.from_prefix("_3")
	_1 = _1Bundle.from_prefix("_1")

class _3Bundle(Bundle):
	_5 = _1Bundle.from_prefix("_5")
	_8 = _1Bundle.from_prefix("_8")
	_9 = _1Bundle.from_prefix("_9")
	_7 = _1Bundle.from_prefix("_7")
	_2 = _1Bundle.from_prefix("_2")
	_6 = _1Bundle.from_prefix("_6")
	_3 = _1Bundle.from_prefix("_3")
	_4 = _1Bundle.from_prefix("_4")
	_0 = _1Bundle.from_prefix("_0")
	_1 = _1Bundle.from_prefix("_1")

class _4Bundle(Bundle):
	_prefetchMSHRs = _3Bundle.from_prefix("_prefetchMSHRs")
	_fetchMSHRs = _2Bundle.from_prefix("_fetchMSHRs")

class _5Bundle(Bundle):
	_data, _virIdx, _waymask = Signals(3)

class _6Bundle(Bundle):
	_bits = _5Bundle.from_prefix("_bits")
	_valid = Signal()

class _7Bundle(Bundle):
	_vSetIdx, _blkPaddr = Signals(2)

class _8Bundle(Bundle):
	_bits = _7Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _9Bundle(Bundle):
	_waymask, _corrupt, _data, _vSetIdx, _blkPaddr = Signals(5)

class _10Bundle(Bundle):
	_bits = _9Bundle.from_prefix("_bits")
	_valid = Signal()

class _11Bundle(Bundle):
	_resp = _10Bundle.from_prefix("_resp")
	_req = _8Bundle.from_prefix("_req")

class _12Bundle(Bundle):
	_source, _address = Signals(2)

class _13Bundle(Bundle):
	_bits = _12Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _14Bundle(Bundle):
	_source, _corrupt, _data, _size, _opcode = Signals(5)

class _15Bundle(Bundle):
	_bits = _14Bundle.from_prefix("_bits")
	_valid = Signal()

class _16Bundle(Bundle):
	_acquire = _13Bundle.from_prefix("_acquire")
	_grant = _15Bundle.from_prefix("_grant")

class _17Bundle(Bundle):
	_bankIdx, _phyTag, _virIdx, _waymask = Signals(4)

class _18Bundle(Bundle):
	_bits = _17Bundle.from_prefix("_bits")
	_valid = Signal()

class _19Bundle(Bundle):
	_valid, _bits = Signals(2)

class _20Bundle(Bundle):
	_vSetIdx = _19Bundle.from_prefix("_vSetIdx")
	_way = Signal()

class _21Bundle(Bundle):
	_meta_write = _18Bundle.from_prefix("_meta_write")
	_mem = _16Bundle.from_prefix("_mem")
	_data_write = _6Bundle.from_prefix("_data_write")
	_victim = _20Bundle.from_prefix("_victim")
	_fetch = _11Bundle.from_prefix("_fetch")
	_prefetch_req = _8Bundle.from_prefix("_prefetch_req")
	_fencei, _flush, _hartId = Signals(3)

class ICacheMissUnitBundle(Bundle):
	io = _21Bundle.from_prefix("io")
	ICacheMissUnit_ = _4Bundle.from_prefix("ICacheMissUnit_")
	reset, clock = Signals(2)
