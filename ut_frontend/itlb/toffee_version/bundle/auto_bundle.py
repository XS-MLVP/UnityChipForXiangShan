from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_vmid, _changed, _mode = Signals(3)

class _1Bundle(Bundle):
	_imode, _virt = Signals(2)

class _2Bundle(Bundle):
	_changed, _mode, _asid = Signals(3)

class _3Bundle(Bundle):
	_priv = _1Bundle.from_prefix("_priv")
	_vsatp = _2Bundle.from_prefix("_vsatp")
	_satp = _2Bundle.from_prefix("_satp")
	_hgatp = _0Bundle.from_prefix("_hgatp")

class _4Bundle(Bundle):
	_1, _2, _0 = Signals(3)

class _5Bundle(Bundle):
	_getGpa, _vpn, _s2xlate = Signals(3)

class _6Bundle(Bundle):
	_bits = _5Bundle.from_prefix("_bits")
	_valid = Signal()

class _7Bundle(Bundle):
	_bits = _5Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _8Bundle(Bundle):
	_2 = _7Bundle.from_prefix("_2")
	_1 = _6Bundle.from_prefix("_1")
	_0 = _6Bundle.from_prefix("_0")

class _9Bundle(Bundle):
	_g, _r, _w, _a, _u, _d, _x = Signals(7)

class _10Bundle(Bundle):
	_perm = _9Bundle.from_prefix("_perm")
	_level, _tag, _pbmt, _v, _vmid, _asid, _ppn, _n = Signals(8)

class _11Bundle(Bundle):
	_6, _4, _3, _0, _1, _7, _2, _5 = Signals(8)

class _12Bundle(Bundle):
	_valididx = _11Bundle.from_prefix("_valididx")
	_ppn_low = _11Bundle.from_prefix("_ppn_low")
	_pteidx = _11Bundle.from_prefix("_pteidx")
	_entry = _10Bundle.from_prefix("_entry")
	_af, _addr_low, _pf = Signals(3)

class _13Bundle(Bundle):
	_perm = _9Bundle.from_prefix("_perm")
	_level, _tag, _pbmt, _vmid, _ppn, _n = Signals(6)

class _14Bundle(Bundle):
	_entry = _13Bundle.from_prefix("_entry")
	_gpf, _gaf = Signals(2)

class _15Bundle(Bundle):
	_s1 = _12Bundle.from_prefix("_s1")
	_s2 = _14Bundle.from_prefix("_s2")
	_getGpa, _s2xlate = Signals(2)

class _16Bundle(Bundle):
	_bits = _15Bundle.from_prefix("_bits")
	_valid = Signal()

class _17Bundle(Bundle):
	_req = _8Bundle.from_prefix("_req")
	_resp = _16Bundle.from_prefix("_resp")

class _18Bundle(Bundle):
	_valid, _bits_vaddr = Signals(2)

class _19Bundle(Bundle):
	_af_instr, _pf_instr, _gpf_instr = Signals(3)

class _20Bundle(Bundle):
	_0 = _19Bundle.from_prefix("_0")

class _21Bundle(Bundle):
	_0 = Signal()

class _22Bundle(Bundle):
	_gpaddr = _21Bundle.from_prefix("_gpaddr")
	_pbmt = _21Bundle.from_prefix("_pbmt")
	_paddr = _21Bundle.from_prefix("_paddr")
	_excp = _20Bundle.from_prefix("_excp")
	_miss, _isForVSnonLeafPTE = Signals(2)

class _23Bundle(Bundle):
	_resp_bits = _22Bundle.from_prefix("_resp_bits")
	_req = _18Bundle.from_prefix("_req")

class _24Bundle(Bundle):
	_valid, _bits_vaddr, _ready = Signals(3)

class _25Bundle(Bundle):
	_gpaddr = _21Bundle.from_prefix("_gpaddr")
	_pbmt = _21Bundle.from_prefix("_pbmt")
	_paddr = _21Bundle.from_prefix("_paddr")
	_excp = _20Bundle.from_prefix("_excp")
	_isForVSnonLeafPTE = Signal()

class _26Bundle(Bundle):
	_bits = _25Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _27Bundle(Bundle):
	_resp = _26Bundle.from_prefix("_resp")
	_req = _24Bundle.from_prefix("_req")

class _28Bundle(Bundle):
	_0 = _23Bundle.from_prefix("_0")
	_1 = _23Bundle.from_prefix("_1")
	_2 = _27Bundle.from_prefix("_2")

class _29Bundle(Bundle):
	_rs2, _rs1, _hg, _flushPipe, _hv, _addr, _id = Signals(7)

class _30Bundle(Bundle):
	_bits = _29Bundle.from_prefix("_bits")
	_valid = Signal()

class _31Bundle(Bundle):
	_flushPipe = _4Bundle.from_prefix("_flushPipe")
	_sfence = _30Bundle.from_prefix("_sfence")
	_csr = _3Bundle.from_prefix("_csr")
	_ptw = _17Bundle.from_prefix("_ptw")
	_requestor = _28Bundle.from_prefix("_requestor")

class TlbBundle(Bundle):
	clock, reset = Signals(2)
	io = _31Bundle.from_prefix("io")