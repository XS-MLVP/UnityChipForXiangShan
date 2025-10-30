from toffee import Bundle, Signals, Signal, SignalList, BundleList

class ValidBundle(Bundle):
	_valid = Signal()

class RVBundle(ValidBundle):
	_ready = Signal()

class _1Bundle(Bundle):
	_matchType, _action, _tdata2, _select, _chain = Signals(5)

class _2Bundle(Bundle):
	_tdata = _1Bundle.from_prefix("_tdata")
	_addr = Signal()

class _3Bundle(ValidBundle):
	_bits = _2Bundle.from_prefix("_bits")

class FrontendTriggerBundle(Bundle):
	_tEnableVec = SignalList("_tEnableVec_#", 4)
	_tUpdate = _3Bundle.from_prefix("_tUpdate")
	_debugMode, _triggerCanRaiseBpExp = Signals(2)

class _5Bundle(Bundle):
	_flag, _value = Signals(2)

class StageFlushBundle(ValidBundle):
	_bits = _5Bundle.from_prefix("_bits")

class _7Bundle(Bundle):
	_s3 = StageFlushBundle.from_prefix("_s3")
	_s2 = StageFlushBundle.from_prefix("_s2")

class _8Bundle(Bundle):
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_level, _ftqOffset = Signals(2)

class _9Bundle(ValidBundle):
	_bits = _8Bundle.from_prefix("_bits")

class _10Bundle(ValidBundle):
	_bits = Signal()

class _11Bundle(Bundle):
	_ftqOffset = _10Bundle.from_prefix("_ftqOffset")
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_nextlineStart, _startAddr, _nextStartAddr = Signals(3)

class _12Bundle(RVBundle):
	_bits = _11Bundle.from_prefix("_bits")

class _13Bundle(Bundle):
	_redirect = _9Bundle.from_prefix("_redirect")
	_flushFromBpu = _7Bundle.from_prefix("_flushFromBpu")
	_req = _12Bundle.from_prefix("_req")

class _15Bundle(ValidBundle):
	_isCall, _brType, _isRet, _isRVC = Signals(4)

class _17Bundle(Bundle):
	_pd = BundleList(_15Bundle, "_pd_#", 16)
	_misOffset = _10Bundle.from_prefix("_misOffset")
	_pc = SignalList("_pc_#", 16)
	_instrRange = SignalList("_instrRange_#", 16)
	_ftqIdx = _5Bundle.from_prefix("_ftqIdx")
	_jalTarget, _cfiOffset_valid, _target = Signals(3)

class _18Bundle(ValidBundle):
	_bits = _17Bundle.from_prefix("_bits")

class FTQInterBundle(Bundle):
	_fromFtq = _13Bundle.from_prefix("_fromFtq")
	_toFtq_pdWb = _18Bundle.from_prefix("_toFtq_pdWb")

class _20Bundle(RVBundle):
	_bits_vaddr = Signal()

class _21Bundle(Bundle):
	_gpf_instr, _af_instr, _pf_instr = Signals(3)

# class _22Bundle(Bundle):
# 	_0 = _21Bundle.from_prefix("_0")

class _24Bundle(Bundle):
	_paddr_0 = Signal()
	_pbmt_0 = Signal()
	_gpaddr_0 = Signal()
	_excp = _21Bundle.from_prefix("_excp_0")
	_isForVSnonLeafPTE = Signal()

class _25Bundle(RVBundle):
	_bits = _24Bundle.from_prefix("_bits")

class ITLBInferBundle(Bundle):
	_req = 	_20Bundle.from_prefix("_req")
	_resp = _25Bundle.from_prefix("_resp")

class _27Bundle(Bundle):
	_1, _0 = Signals(2)

class _28Bundle(Bundle):
	_itlb_pbmt = SignalList("_itlb_pbmt_#", 2)
	_exception = SignalList("_exception_#", 2)
	_vaddr = SignalList("_vaddr_#", 2)
	_pmp_mmio = SignalList("_pmp_mmio_#", 2)
	_paddr_0 = Signal()
	_isForVSnonLeafPTE, _data, _backendException, _doubleline, _gpaddr = Signals(5)

class _29Bundle(ValidBundle):
	_bits = _28Bundle.from_prefix("_bits")

class ICacheInterBundle(Bundle):
	_resp = _29Bundle.from_prefix("_resp")
	_icacheReady = Signal()

class _32Bundle(Bundle):
	_miss_1 = Signal()
	_hit_1 = Signal()

class _33Bundle(Bundle):
	_0 = _32Bundle.from_prefix("_0")

class _34Bundle(Bundle):
	_hit, _miss = Signals(2)

class _35Bundle(Bundle):
	_0 = _34Bundle.from_prefix("_0")

class _36Bundle(Bundle):
	_miss = _33Bundle.from_prefix("_miss")
	_only = _35Bundle.from_prefix("_only")
	_bank_hit_1 = Signal()
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

class RobCommitBundle(ValidBundle):
	_bits = _42Bundle.from_prefix("_bits")

# class _44Bundle(Bundle):
# 	_7 = RobCommitBundle.from_prefix("_7")
# 	_0 = RobCommitBundle.from_prefix("_0")
# 	_4 = RobCommitBundle.from_prefix("_4")
# 	_1 = RobCommitBundle.from_prefix("_1")
# 	_6 = RobCommitBundle.from_prefix("_6")
# 	_2 = RobCommitBundle.from_prefix("_2")
# 	_5 = RobCommitBundle.from_prefix("_5")
# 	_3 = RobCommitBundle.from_prefix("_3")

class _45Bundle(Bundle):
	_gpaddr, _isForVSnonLeafPTE = Signals(2)

class _46Bundle(Bundle):
	_wdata = _45Bundle.from_prefix("_wdata")
	_waddr, _wen = Signals(2)

# class _47Bundle(Bundle):
# 	_valid = Signal()

# class _48Bundle(Bundle):
# 	_13 = _47Bundle.from_prefix("_13")
# 	_3 = _47Bundle.from_prefix("_3")
# 	_7 = _47Bundle.from_prefix("_7")
# 	_4 = _47Bundle.from_prefix("_4")
# 	_10 = _47Bundle.from_prefix("_10")
# 	_15 = _47Bundle.from_prefix("_15")
# 	_5 = _47Bundle.from_prefix("_5")
# 	_8 = _47Bundle.from_prefix("_8")
# 	_9 = _47Bundle.from_prefix("_9")
# 	_12 = _47Bundle.from_prefix("_12")
# 	_1 = _47Bundle.from_prefix("_1")
# 	_6 = _47Bundle.from_prefix("_6")
# 	_2 = _47Bundle.from_prefix("_2")
# 	_11 = _47Bundle.from_prefix("_11")
# 	_14 = _47Bundle.from_prefix("_14")
# 	_0 = _47Bundle.from_prefix("_0")

class _49Bundle(Bundle):
	_isRVC, _brType, _isCall, _isRet = Signals(4)

class _51Bundle(ValidBundle):
	_pd = BundleList(_49Bundle, "_pd_#", 16)
	_valids = SignalList("_pd_#_valid", 15, lambda x: str(x+1))
	_ftqPtr = _5Bundle.from_prefix("_ftqPtr")
	_triggered = SignalList("_triggered_#", 16)
	_isLastInFtqEntry = SignalList("_isLastInFtqEntry_#", 16)
	_exceptionType = SignalList("_exceptionType_#", 16)
	_instrs = SignalList("_instrs_#", 16)
	_foldpc = SignalList("_foldpc_#", 16)
	_illegalInstr = SignalList("_illegalInstr_#", 16)
	_crossPageIPFFix = SignalList("_crossPageIPFFix_#", 16)
	# _ftqOffset = _48Bundle.from_prefix("_ftqOffset")
	_ftqOffset = SignalList("_ftqOffset_#_valid", 16)
	_backendException_0 = Signal()
	_enqEnable = Signal()

class _52Bundle(RVBundle):
	_bits = _51Bundle.from_prefix("_bits")

class _53Bundle(ValidBundle):
	_bits_data = Signal()

class _54Bundle(RVBundle):
	_bits_addr = Signal()

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
	_perf = BundleList(_38Bundle, "_perf_#", 13)

class MMIONeededBundle(Bundle):
	_iTLBInter = ITLBInferBundle.from_prefix("_iTLBInter") # done
	_uncacheInter = UncacheInterBundle.from_prefix("_uncacheInter") # done
	# _rob_commits = _44Bundle.from_prefix("_rob_commits")	
	_rob_commits = BundleList(RobCommitBundle, "_rob_commits_#", 8)
	_mmioCommitRead = _37Bundle.from_prefix("_mmioCommitRead") # done
	_pmp = PMPBundle.from_prefix("_pmp") # done

class ToIbufferBundle(Bundle):
	_toIbuffer = _52Bundle.from_prefix("_toIbuffer")
	_toBackend_gpaddrMem = _46Bundle.from_prefix("_toBackend_gpaddrMem")

class CtrlBundle(Bundle):
	reset, clock = Signals(2)
	io_csr_fsIsOff = Signal()

class PredecodeBundle(Bundle):
	in_bits_data = SignalList("_io_in_bits_data_#", 17)
	out_pd_valids = SignalList("_io_out_pd_#_valid", 15, lambda x: str(x+1))
	out_pd_isRVCs = SignalList("_io_out_pd_#_isRVC", 16)
	out_pd_brTypes = SignalList("_io_out_pd_#_brType", 16)
	out_pd_isCalls = SignalList("_io_out_pd_#_isCall", 16)
	out_pd_isRets = SignalList("_io_out_pd_#_isRet", 16)
	out_hasHalfValids = SignalList("_io_out_hasHalfValid_#", 14, lambda x: str(x+2))
	out_jumpOffsets = SignalList("_io_out_jumpOffset_#", 16)
	out_instrs = SignalList("_io_out_instr_#", 16)

class PredCheckerBundle(Bundle):
	instr_valids = SignalList("_io_in_instrValid_#", 16)
	fixed_ranges = SignalList("_io_out_stage1Out_fixedRange_#", 16)
	fixed_takens = SignalList("_io_out_stage1Out_fixedTaken_#", 16)
	fixed_targets = SignalList("_io_out_stage2Out_fixedTarget_#", 16)
	jal_targets = SignalList("_io_out_stage2Out_jalTarget_#", 16)
	fault_types = SignalList("_io_out_stage2Out_faultType_#_value", 16)

class InternalBundle(Bundle):
	_f2_flush, _f3_flush = Signals(2)
	_f1_fire, _f1_valid = Signals(2)
	_f0_flush_from_bpu_probe = Signal()
	_f2_ready = Signal()
	_f2_fire = Signal()
	_f0_fire, _wb_enable = Signals(2)
	_f2_valid = Signal()
	_f3_ready = Signal()
	_icacheRespAllValid = Signal()
	f3_exception_vec = SignalList("_f3_exception_vec_#", 16)
	f2_exceptions = SignalList("_f2_exception_#", 2)
	f3_pcs = SignalList("_f3_pc_#", 16)
	f2_cut_ptrs = SignalList("_f2_cut_ptr_#", 17)
	_f3_paddrs_0, _f3_gpaddr = Signals(2)
	_f3_lastHalf_valid = Signal()
	
	_f3_instr_range = Signal()
	pre_decoder = PredecodeBundle.from_prefix("_preDecoder")
	pred_checker = PredCheckerBundle.from_prefix("_predChecker")

	_mmio_state = Signal()
	_is_first_instr = Signal()
	
	# mmio_wb_pd_0 = mmioFlushPdBundle.from_prefix("_mmioFlushWb_bits_pd_0")
 
	# preDecoder_io_in_bits_data = SignalList("_preDecoder_io_in_bits_data_#", 17)

	

class IFUTopBundle(Bundle):
	# io = _56Bundle.from_prefix("io")
	ctrl = CtrlBundle.from_prefix("")
	io_ftqInter = FTQInterBundle.from_prefix("io_ftqInter") #done
	_icacheInterCtrl = ICacheInterCtrlBundle.from_prefix("io") #done
	to_ibuffer_all = ToIbufferBundle.from_prefix("io") # done
	mmio_needed = MMIONeededBundle.from_prefix("io") 
	io_frontendTrigger = FrontendTriggerBundle.from_prefix("io_frontendTrigger") # done
	internal_wires = InternalBundle.from_prefix("NewIFU") # done