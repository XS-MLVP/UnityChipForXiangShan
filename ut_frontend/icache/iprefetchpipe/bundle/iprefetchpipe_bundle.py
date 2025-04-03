from toffee import Bundle, Signals, Signal


class _0Bundle(Bundle):
    _vSetIdx, _blkPaddr = Signals(2)


class _1Bundle(Bundle):
    _bits = _0Bundle.from_prefix("_bits")
    _valid, _ready = Signals(2)


class _2Bundle(Bundle):
    _vSetIdx, _corrupt, _blkPaddr, _waymask = Signals(4)


class _3Bundle(Bundle):
    _bits = _2Bundle.from_prefix("_bits")
    _valid = Signal()


class _4Bundle(Bundle):
    _flag, _value = Signals(2)


class _5Bundle(Bundle):
    _bits = _4Bundle.from_prefix("_bits")
    _valid = Signal()


class _6Bundle(Bundle):
    _s3 = _5Bundle.from_prefix("_s3")
    _s2 = _5Bundle.from_prefix("_s2")


class _7Bundle(Bundle):
    _bits_vaddr, _valid = Signals(2)


class _8Bundle(Bundle):
    _pf_instr, _af_instr, _gpf_instr = Signals(3)


class _9Bundle(Bundle):
    _0 = _8Bundle.from_prefix("_0")


class _10Bundle(Bundle):
    _0 = Signal()


class _11Bundle(Bundle):
    _pbmt = _10Bundle.from_prefix("_pbmt")
    _gpaddr = _10Bundle.from_prefix("_gpaddr")
    _paddr = _10Bundle.from_prefix("_paddr")
    _excp = _9Bundle.from_prefix("_excp")
    _isForVSnonLeafPTE, _miss = Signals(2)


class _12Bundle(Bundle):
    _resp_bits = _11Bundle.from_prefix("_resp_bits")
    _req = _7Bundle.from_prefix("_req")


class _13Bundle(Bundle):
    _1 = _12Bundle.from_prefix("_1")
    _0 = _12Bundle.from_prefix("_0")


class _14Bundle(Bundle):
    _0, _1, _3, _2 = Signals(4)


class _15Bundle(Bundle):
    _0 = _14Bundle.from_prefix("_0")
    _1 = _14Bundle.from_prefix("_1")


class _16Bundle(Bundle):
    _tag = Signal()


class _17Bundle(Bundle):
    _1 = _16Bundle.from_prefix("_1")
    _0 = _16Bundle.from_prefix("_0")
    _2 = _16Bundle.from_prefix("_2")
    _3 = _16Bundle.from_prefix("_3")


class _18Bundle(Bundle):
    _1 = _17Bundle.from_prefix("_1")
    _0 = _17Bundle.from_prefix("_0")


class _19Bundle(Bundle):
    _entryValid = _15Bundle.from_prefix("_entryValid")
    _codes = _15Bundle.from_prefix("_codes")
    _metas = _18Bundle.from_prefix("_metas")


class _20Bundle(Bundle):
    _0, _1 = Signals(2)


class _21Bundle(Bundle):
    _vSetIdx = _20Bundle.from_prefix("_vSetIdx")
    _isDoubleLine = Signal()


class _22Bundle(Bundle):
    _bits = _21Bundle.from_prefix("_bits")
    _valid, _ready = Signals(2)


class _23Bundle(Bundle):
    _fromIMeta = _19Bundle.from_prefix("_fromIMeta")
    _toIMeta = _22Bundle.from_prefix("_toIMeta")


class _24Bundle(Bundle):
    _mmio, _instr = Signals(2)


class _25Bundle(Bundle):
    _resp = _24Bundle.from_prefix("_resp")
    _req_bits_addr = Signal()


class _26Bundle(Bundle):
    _1 = _25Bundle.from_prefix("_1")
    _0 = _25Bundle.from_prefix("_0")


class _27Bundle(Bundle):
    _ftqIdx = _4Bundle.from_prefix("_ftqIdx")
    _backendException, _startAddr, _isSoftPrefetch, _nextlineStart = Signals(4)


class _28Bundle(Bundle):
    _bits = _27Bundle.from_prefix("_bits")
    _valid, _ready = Signals(2)


class _29Bundle(Bundle):
    _pbmt = _20Bundle.from_prefix("_pbmt")
    _exception = _20Bundle.from_prefix("_exception")


class _30Bundle(Bundle):
    _waymask = _20Bundle.from_prefix("_waymask")
    _meta_codes = _20Bundle.from_prefix("_meta_codes")
    _vSetIdx = _20Bundle.from_prefix("_vSetIdx")
    _ptag = _20Bundle.from_prefix("_ptag")
    _itlb = _29Bundle.from_prefix("_itlb")


class _31Bundle(Bundle):
    _gpaddr, _isForVSnonLeafPTE = Signals(2)


class _32Bundle(Bundle):
    _gpf = _31Bundle.from_prefix("_gpf")
    _entry = _30Bundle.from_prefix("_entry")


class _33Bundle(Bundle):
    _bits = _32Bundle.from_prefix("_bits")
    _valid, _ready = Signals(2)


class _34Bundle(Bundle):
    _MSHRReq = _1Bundle.from_prefix("_MSHRReq")
    _itlb = _13Bundle.from_prefix("_itlb")
    _flushFromBpu = _6Bundle.from_prefix("_flushFromBpu")
    _metaRead = _23Bundle.from_prefix("_metaRead")
    _wayLookupWrite = _33Bundle.from_prefix("_wayLookupWrite")
    _req = _28Bundle.from_prefix("_req")
    _pmp = _26Bundle.from_prefix("_pmp")
    _MSHRResp = _3Bundle.from_prefix("_MSHRResp")
    _csr_pf_enable, _itlbFlushPipe, _flush = Signals(3)


class IPrefetchPipeBundle(Bundle):
    io = _34Bundle.from_prefix("io")
    clock, IPrefetchPipe_s1_flush, reset = Signals(3)
