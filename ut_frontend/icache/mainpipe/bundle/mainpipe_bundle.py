from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_fire, _valid = Signals(2)

class _1Bundle(Bundle):
	_s2 = _0Bundle.from_prefix("_s2")
	_s0_fire = Signal()

class _2Bundle(Bundle):
	_4 = Signal()

class _3Bundle(Bundle):
	_valid_T = _2Bundle.from_prefix("_valid_T")

class _4Bundle(Bundle):
	_1 = _3Bundle.from_prefix("_1")
	_0 = _3Bundle.from_prefix("_0")

class _5Bundle(Bundle):
	_1, _7, _3, _4, _6, _2, _5, _0 = Signals(8)

class _6Bundle(Bundle):
	_datas = _5Bundle.from_prefix("_datas")
	_codes = _5Bundle.from_prefix("_codes")

class _7Bundle(Bundle):
	_1, _0 = Signals(2)

class _8Bundle(Bundle):
	_1, _2, _3, _0 = Signals(4)

class _9Bundle(Bundle):
	_0 = _8Bundle.from_prefix("_0")
	_1 = _8Bundle.from_prefix("_1")

class _10Bundle(Bundle):
	_waymask = _9Bundle.from_prefix("_waymask")
	_vSetIdx = _7Bundle.from_prefix("_vSetIdx")
	_blkOffset = Signal()

class _11Bundle(Bundle):
	_bits = _10Bundle.from_prefix("_bits")
	_valid = Signal()

class _12Bundle(Bundle):
	_bits_vSetIdx = _7Bundle.from_prefix("_bits_vSetIdx")
	_valid = Signal()

class _13Bundle(Bundle):
	_bits_vSetIdx = _7Bundle.from_prefix("_bits_vSetIdx")
	_valid, _ready = Signals(2)

class _14Bundle(Bundle):
	_3 = _13Bundle.from_prefix("_3")
	_1 = _12Bundle.from_prefix("_1")
	_2 = _12Bundle.from_prefix("_2")
	_0 = _11Bundle.from_prefix("_0")

class _15Bundle(Bundle):
	_toIData = _14Bundle.from_prefix("_toIData")
	_fromIData = _6Bundle.from_prefix("_fromIData")

class _16Bundle(Bundle):
	_paddr, _report_to_beu = Signals(2)

class _17Bundle(Bundle):
	_bits = _16Bundle.from_prefix("_bits")
	_valid = Signal()

class _18Bundle(Bundle):
	_0 = _17Bundle.from_prefix("_0")
	_1 = _17Bundle.from_prefix("_1")

class _19Bundle(Bundle):
	_nextlineStart, _startAddr = Signals(2)

class _20Bundle(Bundle):
	_0 = _19Bundle.from_prefix("_0")
	_1 = _19Bundle.from_prefix("_1")
	_4 = _19Bundle.from_prefix("_4")
	_2 = _19Bundle.from_prefix("_2")
	_3 = _19Bundle.from_prefix("_3")

class _21Bundle(Bundle):
	_1, _3, _4, _2, _0 = Signals(5)

class _22Bundle(Bundle):
	_pcMemRead = _20Bundle.from_prefix("_pcMemRead")
	_readValid = _21Bundle.from_prefix("_readValid")
	_backendException = Signal()

class _23Bundle(Bundle):
	_bits = _22Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _24Bundle(Bundle):
	_0 = Signal()

class _25Bundle(Bundle):
	_vaddr = _7Bundle.from_prefix("_vaddr")
	_itlb_pbmt = _7Bundle.from_prefix("_itlb_pbmt")
	_exception = _7Bundle.from_prefix("_exception")
	_pmp_mmio = _7Bundle.from_prefix("_pmp_mmio")
	_paddr = _24Bundle.from_prefix("_paddr")
	_data, _doubleline, _isForVSnonLeafPTE, _gpaddr, _backendException = Signals(5)

class _26Bundle(Bundle):
	_bits = _25Bundle.from_prefix("_bits")
	_valid = Signal()

class _27Bundle(Bundle):
	_resp = _26Bundle.from_prefix("_resp")
	_req = _23Bundle.from_prefix("_req")
	_topdownIcacheMiss, _topdownItlbMiss = Signals(2)

class _28Bundle(Bundle):
	_waymask, _virIdx = Signals(2)

class _29Bundle(Bundle):
	_bits = _28Bundle.from_prefix("_bits")
	_valid = Signal()

class _30Bundle(Bundle):
	_1 = _29Bundle.from_prefix("_1")
	_0 = _29Bundle.from_prefix("_0")

class _31Bundle(Bundle):
	_blkPaddr, _vSetIdx = Signals(2)

class _32Bundle(Bundle):
	_bits = _31Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _33Bundle(Bundle):
	_data, _blkPaddr, _vSetIdx, _corrupt = Signals(4)

class _34Bundle(Bundle):
	_bits = _33Bundle.from_prefix("_bits")
	_valid = Signal()

class _35Bundle(Bundle):
	_resp = _34Bundle.from_prefix("_resp")
	_req = _32Bundle.from_prefix("_req")

class _36Bundle(Bundle):
	_1 = Signal()

class _37Bundle(Bundle):
	_hit = _36Bundle.from_prefix("_hit")
	_except = _36Bundle.from_prefix("_except")
	_miss = _36Bundle.from_prefix("_miss")

class _38Bundle(Bundle):
	_0 = _37Bundle.from_prefix("_0")

class _39Bundle(Bundle):
	_miss, _hit = Signals(2)

class _40Bundle(Bundle):
	_0 = _39Bundle.from_prefix("_0")

class _41Bundle(Bundle):
	_bank_hit = _7Bundle.from_prefix("_bank_hit")
	_miss = _38Bundle.from_prefix("_miss")
	_except = _24Bundle.from_prefix("_except")
	_only = _40Bundle.from_prefix("_only")
	_hit = Signal()

class _42Bundle(Bundle):
	_instr, _mmio = Signals(2)

class _43Bundle(Bundle):
	_resp = _42Bundle.from_prefix("_resp")
	_req_bits_addr = Signal()

class _44Bundle(Bundle):
	_1 = _43Bundle.from_prefix("_1")
	_0 = _43Bundle.from_prefix("_0")

class _45Bundle(Bundle):
	_way, _vSetIdx = Signals(2)

class _46Bundle(Bundle):
	_bits = _45Bundle.from_prefix("_bits")
	_valid = Signal()

class _47Bundle(Bundle):
	_0 = _46Bundle.from_prefix("_0")
	_1 = _46Bundle.from_prefix("_1")

class _48Bundle(Bundle):
	_pbmt = _7Bundle.from_prefix("_pbmt")
	_exception = _7Bundle.from_prefix("_exception")

class _49Bundle(Bundle):
	_ptag = _7Bundle.from_prefix("_ptag")
	_meta_codes = _7Bundle.from_prefix("_meta_codes")
	_waymask = _7Bundle.from_prefix("_waymask")
	_vSetIdx = _7Bundle.from_prefix("_vSetIdx")
	_itlb = _48Bundle.from_prefix("_itlb")

class _50Bundle(Bundle):
	_isForVSnonLeafPTE, _gpaddr = Signals(2)

class _51Bundle(Bundle):
	_entry = _49Bundle.from_prefix("_entry")
	_gpf = _50Bundle.from_prefix("_gpf")

class _52Bundle(Bundle):
	_bits = _51Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _53Bundle(Bundle):
	_perfInfo = _41Bundle.from_prefix("_perfInfo")
	_pmp = _44Bundle.from_prefix("_pmp")
	_errors = _18Bundle.from_prefix("_errors")
	_metaArrayFlush = _30Bundle.from_prefix("_metaArrayFlush")
	_wayLookupRead = _52Bundle.from_prefix("_wayLookupRead")
	_dataArray = _15Bundle.from_prefix("_dataArray")
	_mshr = _35Bundle.from_prefix("_mshr")
	_fetch = _27Bundle.from_prefix("_fetch")
	_touch = _47Bundle.from_prefix("_touch")
	_hartId, _flush, _ecc_enable, _respStall = Signals(4)

class ICacheMainPipeBundle(Bundle):
	ICacheMainPipe = _1Bundle.from_prefix("ICacheMainPipe")
	ICacheMainPipe__toMSHRArbiter_io_in = _4Bundle.from_prefix("ICacheMainPipe__toMSHRArbiter_io_in")
	io = _53Bundle.from_prefix("io")
	reset, clock = Signals(2)

