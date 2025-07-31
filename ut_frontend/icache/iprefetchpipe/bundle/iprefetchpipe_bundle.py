from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_fire, _can_go = Signals(2)

class _1Bundle(Bundle):
	_1, _0 = Signals(2)

class _2Bundle(Bundle):
	_flag, _value = Signals(2)

class _3Bundle(Bundle):
	_ftqIdx = _2Bundle.from_prefix("_ftqIdx")
	_vaddr = _1Bundle.from_prefix("_vaddr")

class _4Bundle(Bundle):
	_backendException = _1Bundle.from_prefix("_backendException")
	_req = _3Bundle.from_prefix("_req")
	_isSoftPrefetch, _valid, _ready,_flush, _doubleline = Signals(5)

class _5Bundle(Bundle):
	_s1 = _4Bundle.from_prefix("_s1")
	_s0 = _0Bundle.from_prefix("_s0")
	_from_bpu_s0_flush_probe = Signal()
	_state = Signal()

class _6Bundle(Bundle):
	_blkPaddr, _vSetIdx = Signals(2)

class _7Bundle(Bundle):
	_bits = _6Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _8Bundle(Bundle):
	_corrupt, _waymask, _blkPaddr, _vSetIdx = Signals(4)

class _9Bundle(Bundle):
	_bits = _8Bundle.from_prefix("_bits")
	_valid = Signal()

class _10Bundle(Bundle):
	_bits = _2Bundle.from_prefix("_bits")
	_valid = Signal()

class _11Bundle(Bundle):
	_s3 = _10Bundle.from_prefix("_s3")
	_s2 = _10Bundle.from_prefix("_s2")

class _12Bundle(Bundle):
	_bits_vaddr, _valid = Signals(2)

class _13Bundle(Bundle):
	_af_instr, _pf_instr, _gpf_instr = Signals(3)

class _14Bundle(Bundle):
	_0 = _13Bundle.from_prefix("_0")

class _15Bundle(Bundle):
	_0 = Signal()

class _16Bundle(Bundle):
	_pbmt = _15Bundle.from_prefix("_pbmt")
	_gpaddr = _15Bundle.from_prefix("_gpaddr")
	_paddr = _15Bundle.from_prefix("_paddr")
	_excp = _14Bundle.from_prefix("_excp")
	_isForVSnonLeafPTE, _miss = Signals(2)

class _17Bundle(Bundle):
	_req = _12Bundle.from_prefix("_req")
	_resp_bits = _16Bundle.from_prefix("_resp_bits")

class _18Bundle(Bundle):
	_0 = _17Bundle.from_prefix("_0")
	_1 = _17Bundle.from_prefix("_1")

class _19Bundle(Bundle):
	_1, _2, _0, _3 = Signals(4)

class _20Bundle(Bundle):
	_1 = _19Bundle.from_prefix("_1")
	_0 = _19Bundle.from_prefix("_0")

class _21Bundle(Bundle):
	_tag = Signal()

class _22Bundle(Bundle):
	_1 = _21Bundle.from_prefix("_1")
	_0 = _21Bundle.from_prefix("_0")
	_3 = _21Bundle.from_prefix("_3")
	_2 = _21Bundle.from_prefix("_2")

class _23Bundle(Bundle):
	_1 = _22Bundle.from_prefix("_1")
	_0 = _22Bundle.from_prefix("_0")

class _24Bundle(Bundle):
	_metas = _23Bundle.from_prefix("_metas")
	_entryValid = _20Bundle.from_prefix("_entryValid")
	_codes = _20Bundle.from_prefix("_codes")

class _25Bundle(Bundle):
	_vSetIdx = _1Bundle.from_prefix("_vSetIdx")
	_isDoubleLine = Signal()

class _26Bundle(Bundle):
	_bits = _25Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _27Bundle(Bundle):
	_toIMeta = _26Bundle.from_prefix("_toIMeta")
	_fromIMeta = _24Bundle.from_prefix("_fromIMeta")

class _28Bundle(Bundle):
	_mmio, _instr = Signals(2)

class _29Bundle(Bundle):
	_resp = _28Bundle.from_prefix("_resp")
	_req_bits_addr = Signal()

class _30Bundle(Bundle):
	_1 = _29Bundle.from_prefix("_1")
	_0 = _29Bundle.from_prefix("_0")

class _31Bundle(Bundle):
	_ftqIdx = _2Bundle.from_prefix("_ftqIdx")
	_nextlineStart, _isSoftPrefetch, _backendException, _startAddr = Signals(4)

class _32Bundle(Bundle):
	_bits = _31Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _33Bundle(Bundle):
	_exception = _1Bundle.from_prefix("_exception")
	_pbmt = _1Bundle.from_prefix("_pbmt")

class _34Bundle(Bundle):
	_meta_codes = _1Bundle.from_prefix("_meta_codes")
	_vSetIdx = _1Bundle.from_prefix("_vSetIdx")
	_ptag = _1Bundle.from_prefix("_ptag")
	_waymask = _1Bundle.from_prefix("_waymask")
	_itlb = _33Bundle.from_prefix("_itlb")

class _35Bundle(Bundle):
	_gpaddr, _isForVSnonLeafPTE = Signals(2)

class _36Bundle(Bundle):
	_entry = _34Bundle.from_prefix("_entry")
	_gpf = _35Bundle.from_prefix("_gpf")

class _37Bundle(Bundle):
	_bits = _36Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _38Bundle(Bundle):
	_req = _32Bundle.from_prefix("_req")
	_MSHRResp = _9Bundle.from_prefix("_MSHRResp")
	_flushFromBpu = _11Bundle.from_prefix("_flushFromBpu")
	_MSHRReq = _7Bundle.from_prefix("_MSHRReq")
	_itlb = _18Bundle.from_prefix("_itlb")
	_metaRead = _27Bundle.from_prefix("_metaRead")
	_wayLookupWrite = _37Bundle.from_prefix("_wayLookupWrite")
	_pmp = _30Bundle.from_prefix("_pmp")
	_flush, _csr_pf_enable, _itlbFlushPipe = Signals(3)

class IPrefetchPipeBundle(Bundle):
	io = _38Bundle.from_prefix("io")
	IPrefetchPipe = _5Bundle.from_prefix("IPrefetchPipe")
	reset, clock = Signals(2)
