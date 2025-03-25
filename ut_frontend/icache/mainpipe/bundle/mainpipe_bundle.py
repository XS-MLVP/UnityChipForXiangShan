from toffee import Bundle, Signals, Signal


class _0Bundle(Bundle):
    _4 = Signal()


class _1Bundle(Bundle):
    _valid_T = _0Bundle.from_prefix("_valid_T")


class _2Bundle(Bundle):
    _0 = _1Bundle.from_prefix("_0")
    _1 = _1Bundle.from_prefix("_1")


class _3Bundle(Bundle):
    _fire, _valid = Signals(2)


class _4Bundle(Bundle):
    _6, _7, _3, _5, _4, _1, _2, _0 = Signals(8)


class _5Bundle(Bundle):
    _datas = _4Bundle.from_prefix("_datas")
    _codes = _4Bundle.from_prefix("_codes")


class _6Bundle(Bundle):
    _1, _0 = Signals(2)


class _7Bundle(Bundle):
    _1, _0, _2, _3 = Signals(4)


class _8Bundle(Bundle):
    _1 = _7Bundle.from_prefix("_1")
    _0 = _7Bundle.from_prefix("_0")


class _9Bundle(Bundle):
    _waymask = _8Bundle.from_prefix("_waymask")
    _vSetIdx = _6Bundle.from_prefix("_vSetIdx")
    _blkOffset = Signal()


class _10Bundle(Bundle):
    _bits = _9Bundle.from_prefix("_bits")
    _valid = Signal()


class _11Bundle(Bundle):
    _bits_vSetIdx = _6Bundle.from_prefix("_bits_vSetIdx")
    _valid = Signal()


class _12Bundle(Bundle):
    _bits_vSetIdx = _6Bundle.from_prefix("_bits_vSetIdx")
    _ready, _valid = Signals(2)


class _13Bundle(Bundle):
    _3 = _12Bundle.from_prefix("_3")
    _1 = _11Bundle.from_prefix("_1")
    _2 = _11Bundle.from_prefix("_2")
    _0 = _10Bundle.from_prefix("_0")


class _14Bundle(Bundle):
    _fromIData = _5Bundle.from_prefix("_fromIData")
    _toIData = _13Bundle.from_prefix("_toIData")


class _15Bundle(Bundle):
    _report_to_beu, _paddr = Signals(2)


class _16Bundle(Bundle):
    _bits = _15Bundle.from_prefix("_bits")
    _valid = Signal()


class _17Bundle(Bundle):
    _0 = _16Bundle.from_prefix("_0")
    _1 = _16Bundle.from_prefix("_1")


class _18Bundle(Bundle):
    _startAddr, _nextlineStart = Signals(2)


class _19Bundle(Bundle):
    _1 = _18Bundle.from_prefix("_1")
    _3 = _18Bundle.from_prefix("_3")
    _0 = _18Bundle.from_prefix("_0")
    _4 = _18Bundle.from_prefix("_4")
    _2 = _18Bundle.from_prefix("_2")


class _20Bundle(Bundle):
    _3, _4, _1, _2, _0 = Signals(5)


class _21Bundle(Bundle):
    _readValid = _20Bundle.from_prefix("_readValid")
    _pcMemRead = _19Bundle.from_prefix("_pcMemRead")
    _backendException = Signal()


class _22Bundle(Bundle):
    _bits = _21Bundle.from_prefix("_bits")
    _ready, _valid = Signals(2)


class _23Bundle(Bundle):
    _0 = Signal()


class _24Bundle(Bundle):
    _exception = _6Bundle.from_prefix("_exception")
    _itlb_pbmt = _6Bundle.from_prefix("_itlb_pbmt")
    _vaddr = _6Bundle.from_prefix("_vaddr")
    _pmp_mmio = _6Bundle.from_prefix("_pmp_mmio")
    _paddr = _23Bundle.from_prefix("_paddr")
    _data, _doubleline, _gpaddr, _backendException, _isForVSnonLeafPTE = Signals(5)


class _25Bundle(Bundle):
    _bits = _24Bundle.from_prefix("_bits")
    _valid = Signal()


class _26Bundle(Bundle):
    _resp = _25Bundle.from_prefix("_resp")
    _req = _22Bundle.from_prefix("_req")
    _topdownIcacheMiss, _topdownItlbMiss = Signals(2)


class _27Bundle(Bundle):
    _virIdx, _waymask = Signals(2)


class _28Bundle(Bundle):
    _bits = _27Bundle.from_prefix("_bits")
    _valid = Signal()


class _29Bundle(Bundle):
    _0 = _28Bundle.from_prefix("_0")
    _1 = _28Bundle.from_prefix("_1")


class _30Bundle(Bundle):
    _blkPaddr, _vSetIdx = Signals(2)


class _31Bundle(Bundle):
    _bits = _30Bundle.from_prefix("_bits")
    _valid, _ready = Signals(2)


class _32Bundle(Bundle):
    _corrupt, _blkPaddr, _vSetIdx, _data = Signals(4)


class _33Bundle(Bundle):
    _bits = _32Bundle.from_prefix("_bits")
    _valid = Signal()


class _34Bundle(Bundle):
    _resp = _33Bundle.from_prefix("_resp")
    _req = _31Bundle.from_prefix("_req")


class _35Bundle(Bundle):
    _1 = Signal()


class _36Bundle(Bundle):
    _miss = _35Bundle.from_prefix("_miss")
    _hit = _35Bundle.from_prefix("_hit")
    _except = _35Bundle.from_prefix("_except")


class _37Bundle(Bundle):
    _0 = _36Bundle.from_prefix("_0")


class _38Bundle(Bundle):
    _hit, _miss = Signals(2)


class _39Bundle(Bundle):
    _0 = _38Bundle.from_prefix("_0")


class _40Bundle(Bundle):
    _except = _23Bundle.from_prefix("_except")
    _miss = _37Bundle.from_prefix("_miss")
    _bank_hit = _6Bundle.from_prefix("_bank_hit")
    _only = _39Bundle.from_prefix("_only")
    _hit = Signal()


class _41Bundle(Bundle):
    _mmio, _instr = Signals(2)


class _42Bundle(Bundle):
    _resp = _41Bundle.from_prefix("_resp")
    _req_bits_addr = Signal()


class _43Bundle(Bundle):
    _0 = _42Bundle.from_prefix("_0")
    _1 = _42Bundle.from_prefix("_1")


class _44Bundle(Bundle):
    _way, _vSetIdx = Signals(2)


class _45Bundle(Bundle):
    _bits = _44Bundle.from_prefix("_bits")
    _valid = Signal()


class _46Bundle(Bundle):
    _0 = _45Bundle.from_prefix("_0")
    _1 = _45Bundle.from_prefix("_1")


class _47Bundle(Bundle):
    _pbmt = _6Bundle.from_prefix("_pbmt")
    _exception = _6Bundle.from_prefix("_exception")


class _48Bundle(Bundle):
    _waymask = _6Bundle.from_prefix("_waymask")
    _ptag = _6Bundle.from_prefix("_ptag")
    _vSetIdx = _6Bundle.from_prefix("_vSetIdx")
    _meta_codes = _6Bundle.from_prefix("_meta_codes")
    _itlb = _47Bundle.from_prefix("_itlb")


class _49Bundle(Bundle):
    _gpaddr, _isForVSnonLeafPTE = Signals(2)


class _50Bundle(Bundle):
    _entry = _48Bundle.from_prefix("_entry")
    _gpf = _49Bundle.from_prefix("_gpf")


class _51Bundle(Bundle):
    _bits = _50Bundle.from_prefix("_bits")
    _ready, _valid = Signals(2)


class _52Bundle(Bundle):
    _dataArray = _14Bundle.from_prefix("_dataArray")
    _pmp = _43Bundle.from_prefix("_pmp")
    _mshr = _34Bundle.from_prefix("_mshr")
    _wayLookupRead = _51Bundle.from_prefix("_wayLookupRead")
    _perfInfo = _40Bundle.from_prefix("_perfInfo")
    _errors = _17Bundle.from_prefix("_errors")
    _fetch = _26Bundle.from_prefix("_fetch")
    _metaArrayFlush = _29Bundle.from_prefix("_metaArrayFlush")
    _touch = _46Bundle.from_prefix("_touch")
    _flush, _respStall, _ecc_enable, _hartId = Signals(4)


class ICacheMainPipeBundle(Bundle):
    ICacheMainPipe_s2 = _3Bundle.from_prefix("ICacheMainPipe_s2")
    io = _52Bundle.from_prefix("io")
    ICacheMainPipe__toMSHRArbiter_io_in = _2Bundle.from_prefix(
        "ICacheMainPipe__toMSHRArbiter_io_in"
    )
    clock, reset = Signals(2)
