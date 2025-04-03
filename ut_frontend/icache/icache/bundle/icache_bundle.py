from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_address, _source = Signals(2)

class _1Bundle(Bundle):
	_bits = _0Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _2Bundle(Bundle):
	_size, _data, _source, _opcode, _corrupt = Signals(5)

class _3Bundle(Bundle):
	_bits = _2Bundle.from_prefix("_bits")
	_valid = Signal()

class _4Bundle(Bundle):
	_a = _1Bundle.from_prefix("_a")
	_d = _3Bundle.from_prefix("_d")

class _5Bundle(Bundle):
	_size, _mask, _data, _source, _opcode, _address = Signals(6)

class _6Bundle(Bundle):
	_bits = _5Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _7Bundle(Bundle):
	_opcode, _source, _size, _data = Signals(4)

class _8Bundle(Bundle):
	_bits = _7Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _9Bundle(Bundle):
	_d = _8Bundle.from_prefix("_d")
	_a = _6Bundle.from_prefix("_a")

class _10Bundle(Bundle):
	_ctrlUnitOpt_in = _9Bundle.from_prefix("_ctrlUnitOpt_in")
	_client_out = _4Bundle.from_prefix("_client_out")

class _11Bundle(Bundle):
	_addr_rd, _indata, _writeen, _ack, _readen, _be, _all, _outdata, _array, _req = Signals(10)

class _12Bundle(Bundle):
	_1 = _11Bundle.from_prefix("_1")
	_3 = _11Bundle.from_prefix("_3")
	_2 = _11Bundle.from_prefix("_2")
	_4 = _11Bundle.from_prefix("_4")
	_addr_rd, _indata, _writeen, _ack, _readen, _be, _all, _outdata, _array, _req = Signals(10)

class _13Bundle(Bundle):
	_report_to_beu, _paddr = Signals(2)

class _14Bundle(Bundle):
	_bits = _13Bundle.from_prefix("_bits")
	_valid = Signal()

class _15Bundle(Bundle):
	_startAddr, _nextlineStart = Signals(2)

class _16Bundle(Bundle):
	_3 = _15Bundle.from_prefix("_3")
	_2 = _15Bundle.from_prefix("_2")
	_1 = _15Bundle.from_prefix("_1")
	_4 = _15Bundle.from_prefix("_4")
	_0 = _15Bundle.from_prefix("_0")

class _17Bundle(Bundle):
	_0, _3, _1, _4, _2 = Signals(5)

class _18Bundle(Bundle):
	_pcMemRead = _16Bundle.from_prefix("_pcMemRead")
	_readValid = _17Bundle.from_prefix("_readValid")
	_backendException = Signal()

class _19Bundle(Bundle):
	_bits = _18Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _20Bundle(Bundle):
	_0, _1 = Signals(2)

class _21Bundle(Bundle):
	_0 = Signal()

class _22Bundle(Bundle):
	_exception = _20Bundle.from_prefix("_exception")
	_itlb_pbmt = _20Bundle.from_prefix("_itlb_pbmt")
	_pmp_mmio = _20Bundle.from_prefix("_pmp_mmio")
	_vaddr = _20Bundle.from_prefix("_vaddr")
	_paddr = _21Bundle.from_prefix("_paddr")
	_data, _gpaddr, _backendException, _isForVSnonLeafPTE, _doubleline = Signals(5)

class _23Bundle(Bundle):
	_bits = _22Bundle.from_prefix("_bits")
	_valid = Signal()

class _24Bundle(Bundle):
	_req = _19Bundle.from_prefix("_req")
	_resp = _23Bundle.from_prefix("_resp")
	_topdownItlbMiss, _topdownIcacheMiss = Signals(2)

class _25Bundle(Bundle):
	_value, _flag = Signals(2)

class _26Bundle(Bundle):
	_bits = _25Bundle.from_prefix("_bits")
	_valid = Signal()

class _27Bundle(Bundle):
	_s3 = _26Bundle.from_prefix("_s3")
	_s2 = _26Bundle.from_prefix("_s2")

class _28Bundle(Bundle):
	_ftqIdx = _25Bundle.from_prefix("_ftqIdx")
	_startAddr, _nextlineStart = Signals(2)

class _29Bundle(Bundle):
	_bits = _28Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _30Bundle(Bundle):
	_req = _29Bundle.from_prefix("_req")
	_flushFromBpu = _27Bundle.from_prefix("_flushFromBpu")
	_backendException = Signal()

class _31Bundle(Bundle):
	_valid, _bits_vaddr = Signals(2)

class _32Bundle(Bundle):
	_gpf_instr, _pf_instr, _af_instr = Signals(3)

class _33Bundle(Bundle):
	_0 = _32Bundle.from_prefix("_0")

class _34Bundle(Bundle):
	_pbmt = _21Bundle.from_prefix("_pbmt")
	_paddr = _21Bundle.from_prefix("_paddr")
	_gpaddr = _21Bundle.from_prefix("_gpaddr")
	_excp = _33Bundle.from_prefix("_excp")
	_miss, _isForVSnonLeafPTE = Signals(2)

class _35Bundle(Bundle):
	_req = _31Bundle.from_prefix("_req")
	_resp_bits = _34Bundle.from_prefix("_resp_bits")

class _36Bundle(Bundle):
	_1 = _35Bundle.from_prefix("_1")
	_0 = _35Bundle.from_prefix("_0")

class _37Bundle(Bundle):
	_1 = Signal()

class _38Bundle(Bundle):
	_miss = _37Bundle.from_prefix("_miss")
	_except = _37Bundle.from_prefix("_except")
	_hit = _37Bundle.from_prefix("_hit")

class _39Bundle(Bundle):
	_0 = _38Bundle.from_prefix("_0")

class _40Bundle(Bundle):
	_hit, _miss = Signals(2)

class _41Bundle(Bundle):
	_0 = _40Bundle.from_prefix("_0")

class _42Bundle(Bundle):
	_bank_hit = _20Bundle.from_prefix("_bank_hit")
	_only = _41Bundle.from_prefix("_only")
	_miss = _39Bundle.from_prefix("_miss")
	_except = _21Bundle.from_prefix("_except")
	_hit = Signal()

class _43Bundle(Bundle):
	_instr, _mmio = Signals(2)

class _44Bundle(Bundle):
	_resp = _43Bundle.from_prefix("_resp")
	_req_bits_addr = Signal()

class _45Bundle(Bundle):
	_1 = _44Bundle.from_prefix("_1")
	_3 = _44Bundle.from_prefix("_3")
	_2 = _44Bundle.from_prefix("_2")
	_0 = _44Bundle.from_prefix("_0")

class _46Bundle(Bundle):
	_1 = _31Bundle.from_prefix("_1")
	_2 = _31Bundle.from_prefix("_2")
	_0 = _31Bundle.from_prefix("_0")

class _47Bundle(Bundle):
	_error = _14Bundle.from_prefix("_error")
	_pmp = _45Bundle.from_prefix("_pmp")
	_itlb = _36Bundle.from_prefix("_itlb")
	_perfInfo = _42Bundle.from_prefix("_perfInfo")
	_fetch = _24Bundle.from_prefix("_fetch")
	_softPrefetch = _46Bundle.from_prefix("_softPrefetch")
	_ftqPrefetch = _30Bundle.from_prefix("_ftqPrefetch")
	_fencei, _flush, _toIFU, _hartId, _stop, _csr_pf_enable, _itlbFlushPipe = Signals(7)

class ICacheBundle(Bundle):
	io = _47Bundle.from_prefix("io")
	boreChildrenBd_bore = _12Bundle.from_prefix("boreChildrenBd_bore")
	auto = _10Bundle.from_prefix("auto")
	reset, ICache__metaArray_io_read_ready, clock = Signals(3)
