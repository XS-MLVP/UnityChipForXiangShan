from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
	_1, _3, _2, _0 = Signals(4)

class _1Bundle(Bundle):
	_matchType, _action, _tdata2, _select, _chain = Signals(5)

class _2Bundle(Bundle):
	_tdata = _1Bundle.from_prefix("_tdata")
	_addr = Signal()

class _3Bundle(Bundle):
	_bits = _2Bundle.from_prefix("_bits")
	_valid = Signal()

class FrontendTriggerBundle(Bundle):
	_tEnableVec = _0Bundle.from_prefix("_tEnableVec")
	_tUpdate = _3Bundle.from_prefix("_tUpdate")
	_debugMode, _triggerCanRaiseBpExp = Signals(2)

class _5Bundle(Bundle):
	_flag, _value = Signals(2)

class StageFlushBundle(Bundle):
	_bits = _5Bundle.from_prefix("_bits")
	_valid = Signal()

class _7Bundle(Bundle):
	_s3 = StageFlushBundle.from_prefix("_s3")
	_s2 = StageFlushBundle.from_prefix("_s2")

class _8Bundle(Bundle):
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_level, _ftqOffset = Signals(2)

class _9Bundle(Bundle):
	_bits = _8Bundle.from_prefix("_bits")
	_valid = Signal()

class _10Bundle(Bundle):
	_bits, _valid = Signals(2)

class _11Bundle(Bundle):
	_ftqOffset = _10Bundle.from_prefix("_ftqOffset")
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_nextlineStart, _startAddr, _nextStartAddr = Signals(3)

class _12Bundle(Bundle):
	_bits = _11Bundle.from_prefix("_bits")
	_ready, _valid = Signals(2)

class _13Bundle(Bundle):
	_redirect = _9Bundle.from_prefix("_redirect")
	_flushFromBpu = _7Bundle.from_prefix("_flushFromBpu")
	_req = _12Bundle.from_prefix("_req")

class _14Bundle(Bundle):
	_13, _11, _8, _14, _1, _3, _5, _7, _10, _2, _15, _12, _4, _0, _9, _6 = Signals(16)

class _15Bundle(Bundle):
	_isCall, _brType, _isRet, _isRVC, _valid = Signals(5)

class _16Bundle(Bundle):
	_12 = _15Bundle.from_prefix("_12")
	_7 = _15Bundle.from_prefix("_7")
	_8 = _15Bundle.from_prefix("_8")
	_14 = _15Bundle.from_prefix("_14")
	_3 = _15Bundle.from_prefix("_3")
	_1 = _15Bundle.from_prefix("_1")
	_4 = _15Bundle.from_prefix("_4")
	_5 = _15Bundle.from_prefix("_5")
	_10 = _15Bundle.from_prefix("_10")
	_6 = _15Bundle.from_prefix("_6")
	_15 = _15Bundle.from_prefix("_15")
	_13 = _15Bundle.from_prefix("_13")
	_2 = _15Bundle.from_prefix("_2")
	_0 = _15Bundle.from_prefix("_0")
	_9 = _15Bundle.from_prefix("_9")
	_11 = _15Bundle.from_prefix("_11")

class _17Bundle(Bundle):
	_pd = _16Bundle.from_prefix("_pd")
	_misOffset = _10Bundle.from_prefix("_misOffset")
	_pc = _14Bundle.from_prefix("_pc")
	_instrRange = _14Bundle.from_prefix("_instrRange")
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_jalTarget, _cfiOffset_valid, _target = Signals(3)

class _18Bundle(Bundle):
	_bits = _17Bundle.from_prefix("_bits")
	_valid = Signal()

class FTQInterBundle(Bundle):
	_fromFtq = _13Bundle.from_prefix("_fromFtq")
	_toFtq_pdWb = _18Bundle.from_prefix("_toFtq_pdWb")

class _20Bundle(Bundle):
	_bits_vaddr, _valid, _ready = Signals(3)

class _21Bundle(Bundle):
	_gpf_instr, _af_instr, _pf_instr = Signals(3)

# class _22Bundle(Bundle):
# 	_0 = _21Bundle.from_prefix("_0")

class _23Bundle(Bundle):
	_0 = Signal()

class _24Bundle(Bundle):
	_paddr = _23Bundle.from_prefix("_paddr")
	_pbmt = _23Bundle.from_prefix("_pbmt")
	_gpaddr = _23Bundle.from_prefix("_gpaddr")
	_excp = _21Bundle.from_prefix("_excp_0")
	_isForVSnonLeafPTE = Signal()

class _25Bundle(Bundle):
	_bits = _24Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class ITLBInferBundle(Bundle):
	_req = 	_20Bundle.from_prefix("_req")
	_resp = _25Bundle.from_prefix("_resp")

class _27Bundle(Bundle):
	_1, _0 = Signals(2)

class _28Bundle(Bundle):
	_itlb_pbmt = _27Bundle.from_prefix("_itlb_pbmt")
	_exception = _27Bundle.from_prefix("_exception")
	_vaddr = _27Bundle.from_prefix("_vaddr")
	_pmp_mmio = _27Bundle.from_prefix("_pmp_mmio")
	_paddr = _23Bundle.from_prefix("_paddr")
	_isForVSnonLeafPTE, _data, _backendException, _doubleline, _gpaddr = Signals(5)

class _29Bundle(Bundle):
	_bits = _28Bundle.from_prefix("_bits")
	_valid = Signal()

class ICacheInterBundle(Bundle):
	_resp = _29Bundle.from_prefix("_resp")
	_icacheReady = Signal()

class _31Bundle(Bundle):
	_1 = Signal()

class _32Bundle(Bundle):
	_miss = _31Bundle.from_prefix("_miss")
	_hit = _31Bundle.from_prefix("_hit")

class _33Bundle(Bundle):
	_0 = _32Bundle.from_prefix("_0")

class _34Bundle(Bundle):
	_hit, _miss = Signals(2)

class _35Bundle(Bundle):
	_0 = _34Bundle.from_prefix("_0")

class _36Bundle(Bundle):
	_miss = _33Bundle.from_prefix("_miss")
	_only = _35Bundle.from_prefix("_only")
	_bank_hit = _31Bundle.from_prefix("_bank_hit")
	_hit = Signal()

class _37Bundle(Bundle):
	_mmioFtqPtr = _5Bundle.from_prefix("_mmioFtqPtr")
	_mmioLastCommit = Signal()

class _38Bundle(Bundle):
	_value = Signal()

class _39Bundle(Bundle):
	_5 = _38Bundle.from_prefix("_5")
	_12 = _38Bundle.from_prefix("_12")
	_4 = _38Bundle.from_prefix("_4")
	_10 = _38Bundle.from_prefix("_10")
	_0 = _38Bundle.from_prefix("_0")
	_2 = _38Bundle.from_prefix("_2")
	_8 = _38Bundle.from_prefix("_8")
	_9 = _38Bundle.from_prefix("_9")
	_7 = _38Bundle.from_prefix("_7")
	_1 = _38Bundle.from_prefix("_1")
	_3 = _38Bundle.from_prefix("_3")
	_6 = _38Bundle.from_prefix("_6")
	_11 = _38Bundle.from_prefix("_11")

class _40Bundle(Bundle):
	_instr, _mmio = Signals(2)

class PMPBundle(Bundle):
	_resp = _40Bundle.from_prefix("_resp")
	_req_bits_addr = Signal()

class _42Bundle(Bundle):
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_ftqOffset = Signal()

class RobCommitBundle(Bundle):
	_bits = _42Bundle.from_prefix("_bits")
	_valid = Signal()

class _44Bundle(Bundle):
	_7 = RobCommitBundle.from_prefix("_7")
	_0 = RobCommitBundle.from_prefix("_0")
	_4 = RobCommitBundle.from_prefix("_4")
	_1 = RobCommitBundle.from_prefix("_1")
	_6 = RobCommitBundle.from_prefix("_6")
	_2 = RobCommitBundle.from_prefix("_2")
	_5 = RobCommitBundle.from_prefix("_5")
	_3 = RobCommitBundle.from_prefix("_3")

class _45Bundle(Bundle):
	_gpaddr, _isForVSnonLeafPTE = Signals(2)

class _46Bundle(Bundle):
	_wdata = _45Bundle.from_prefix("_wdata")
	_waddr, _wen = Signals(2)

class _47Bundle(Bundle):
	_valid = Signal()

class _48Bundle(Bundle):
	_13 = _47Bundle.from_prefix("_13")
	_3 = _47Bundle.from_prefix("_3")
	_7 = _47Bundle.from_prefix("_7")
	_4 = _47Bundle.from_prefix("_4")
	_10 = _47Bundle.from_prefix("_10")
	_15 = _47Bundle.from_prefix("_15")
	_5 = _47Bundle.from_prefix("_5")
	_8 = _47Bundle.from_prefix("_8")
	_9 = _47Bundle.from_prefix("_9")
	_12 = _47Bundle.from_prefix("_12")
	_1 = _47Bundle.from_prefix("_1")
	_6 = _47Bundle.from_prefix("_6")
	_2 = _47Bundle.from_prefix("_2")
	_11 = _47Bundle.from_prefix("_11")
	_14 = _47Bundle.from_prefix("_14")
	_0 = _47Bundle.from_prefix("_0")

class _49Bundle(Bundle):
	_isRVC, _brType = Signals(2)

class _50Bundle(Bundle):
	_15 = _49Bundle.from_prefix("_15")
	_9 = _49Bundle.from_prefix("_9")
	_11 = _49Bundle.from_prefix("_11")
	_0 = _49Bundle.from_prefix("_0")
	_13 = _49Bundle.from_prefix("_13")
	_12 = _49Bundle.from_prefix("_12")
	_2 = _49Bundle.from_prefix("_2")
	_10 = _49Bundle.from_prefix("_10")
	_14 = _49Bundle.from_prefix("_14")
	_4 = _49Bundle.from_prefix("_4")
	_8 = _49Bundle.from_prefix("_8")
	_6 = _49Bundle.from_prefix("_6")
	_3 = _49Bundle.from_prefix("_3")
	_1 = _49Bundle.from_prefix("_1")
	_7 = _49Bundle.from_prefix("_7")
	_5 = _49Bundle.from_prefix("_5")

class _51Bundle(Bundle):
	_pd = _50Bundle.from_prefix("_pd")
	_ftqPtr = _5Bundle.from_prefix("_ftqPtr")
	_triggered = _14Bundle.from_prefix("_triggered")
	_isLastInFtqEntry = _14Bundle.from_prefix("_isLastInFtqEntry")
	_exceptionType = _14Bundle.from_prefix("_exceptionType")
	_instrs = _14Bundle.from_prefix("_instrs")
	_foldpc = _14Bundle.from_prefix("_foldpc")
	_illegalInstr = _14Bundle.from_prefix("_illegalInstr")
	_crossPageIPFFix = _14Bundle.from_prefix("_crossPageIPFFix")
	_ftqOffset = _48Bundle.from_prefix("_ftqOffset")
	_backendException = _23Bundle.from_prefix("_backendException")
	_enqEnable, _valid = Signals(2)

class _52Bundle(Bundle):
	_bits = _51Bundle.from_prefix("_bits")
	_valid, _ready = Signals(2)

class _53Bundle(Bundle):
	_bits_data, _valid = Signals(2)

class _54Bundle(Bundle):
	_bits_addr, _valid, _ready = Signals(3)

class UncacheInterBundle(Bundle):
	_toUncache = _54Bundle.from_prefix("_toUncache")
	_fromUncache = _53Bundle.from_prefix("_fromUncache")

# class _56Bundle(Bundle):
# 	_icacheInter = ICacheInterBundle.from_prefix("_icacheInter")
# 	_toIbuffer = _52Bundle.from_prefix("_toIbuffer")
# 	_perf = _39Bundle.from_prefix("_perf")
# 	_ftqInter = FTQInterBundle.from_prefix("_ftqInter")
# 	_rob_commits = _44Bundle.from_prefix("_rob_commits")
# 	_toBackend_gpaddrMem = _46Bundle.from_prefix("_toBackend_gpaddrMem")
# 	_frontendTrigger = FrontendTriggerBundle.from_prefix("_frontendTrigger")
# 	_mmioCommitRead = _37Bundle.from_prefix("_mmioCommitRead")
# 	_uncacheInter = UncacheInterBundle.from_prefix("_uncacheInter")
# 	_pmp = PMPBundle.from_prefix("_pmp")
# 	_iTLBInter = ITLBInferBundle.from_prefix("_iTLBInter")
# 	_icachePerfInfo = _36Bundle.from_prefix("_icachePerfInfo")
# 	_icacheStop, _csr_fsIsOff = Signals(2)

class ICacheInterCtrlBundle(Bundle):
	_icacheStop = Signal()
	_icacheInter = ICacheInterBundle.from_prefix("_icacheInter")

class PerformanceBundle(Bundle):
	_icachePerfInfo = _36Bundle.from_prefix("_icachePerfInfo")
	_perf = _39Bundle.from_prefix("_perf")

class MMIONeededBundle(Bundle):
	_iTLBInter = ITLBInferBundle.from_prefix("_iTLBInter") # done
	_uncacheInter = UncacheInterBundle.from_prefix("_uncacheInter") # done
	_rob_commits = _44Bundle.from_prefix("_rob_commits")	
	_mmioCommitRead = _37Bundle.from_prefix("_mmioCommitRead") # done
	_pmp = PMPBundle.from_prefix("_pmp") # done

class ToIbufferBundle(Bundle):
	_toIbuffer = _52Bundle.from_prefix("_toIbuffer")
	_toBackend_gpaddrMem = _46Bundle.from_prefix("_toBackend_gpaddrMem")

class CtrlBundle(Bundle):
	reset, clock = Signals(2)
	io_csr_fsIsOff = Signal()

class InternalFlushesBundle(Bundle):
	_f2_flush, _f3_flush = Signals(2)

class IFUTopBundle(Bundle):
	# io = _56Bundle.from_prefix("io")
	ctrl = CtrlBundle.from_prefix("")
	io_ftqInter = FTQInterBundle.from_prefix("io_ftqInter") #done
	_icacheInterCtrl = ICacheInterCtrlBundle.from_prefix("io") #done
	to_ibuffer_all = ToIbufferBundle.from_prefix("io") # done
	mmio_needed = MMIONeededBundle.from_prefix("io") 
	performance = PerformanceBundle.from_prefix("io") # not need
	io_frontendTrigger = FrontendTriggerBundle.from_prefix("io_frontendTrigger") # done
	internal_flushes = InternalFlushesBundle.from_prefix("NewIFU") # done