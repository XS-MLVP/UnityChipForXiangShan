from toffee import Agent, driver_method
from ..bundle import IFUTopBundle, StageFlushBundle, RobCommitBundle
from ..datadef import FTQQuery, ICacheStatusResp, FTQFlushInfo, FTQResp, FrontendTriggerReq, \
        ToIbufferAllRes, ITLBReq, ITLBResp, ToUncache, FromUncache, FTQIdx, PMPResp, RobCommit, FTQFlushFromBPU, ExistsIdx,\
        PreDecodeDataDef, F3PreDecodeData, PredCheckerRetData, PredCheckerStage1RetData, PredCheckerStage2RetData, FTQRedirect, \
            FTQFlushFromBPU, NonMMIOReq, NonMMIOResp, MMIOCycleInfo, MMIOReq, MMIOState, MMIOToIbufferFTQ
            


class OutsideAgent(Agent):
    def __init__(self, bundle: IFUTopBundle):
        super().__init__(bundle)
        self.top = bundle
        self.ftqReqBundle = bundle.io_ftqInter._fromFtq._req
        self.ftqWbBundle = bundle.io_ftqInter._toFtq_pdWb
        self.ftqRedirectBundle = bundle.io_ftqInter._fromFtq._redirect
        self.ftqFlushStgsBundle = bundle.io_ftqInter._fromFtq._flushFromBpu
        self.flushResBundle = bundle.internal_wires
        self.icacheInter = self.top._icacheInterCtrl._icacheInter
        self.frontendTriggerBundle = self.top.io_frontendTrigger
        self.toIbufferAll = self.top.to_ibuffer_all
        self.itlbInter = self.top.mmio_needed._iTLBInter
        self.uncacheInter = self.top.mmio_needed._uncacheInter
        self.cur_state = MMIOState.STATE_IDLE
        self.last_state = MMIOState.STATE_COMMITED

    # @driver_method()
    async def step(self):
        await self.top.step()

    def set_icache_ready(self, ready):
        self.icacheInter._icacheReady.value = ready

    def get_ftq_ready(self) -> bool:
        return self.ftqReqBundle._ready.value != 0

    # @driver_method()
    def query_from_ftq(self, query: FTQQuery):   
        self.ftqReqBundle._bits._ftqIdx._flag.value = query.ftqIdx.flag
        self.ftqReqBundle._bits._ftqIdx._value.value = query.ftqIdx.value

        self.ftqReqBundle._bits._ftqOffset._valid.value = query.ftqOffset.exists
        self.ftqReqBundle._bits._ftqOffset._bits.value = query.ftqOffset.offsetIdx
        self.ftqReqBundle._bits._startAddr.value = query.startAddr
        self.ftqReqBundle._bits._nextStartAddr.value = query.nextStartAddr
        
        self.ftqReqBundle._bits._nextlineStart.value = query.nextlineStart
        self.ftqReqBundle._valid.value = query.valid

    # @driver_method()
    # async def ftq_valid_set(self, valid):
    #     self.ftqReqBundle._valid.value = valid

    def get_exception(self) -> list[int]   :
        return [self.top.internal_wires.f2_exceptions[i].value for i in range(2)]
    
    def get_exception_vecs(self) -> list[int]:
        # f2_exception = [self.top.internal_wires.f2_exceptions[i].value for i in range(2)]
        exception_vec = [self.top.internal_wires.f3_exception_vec[i].value for i in range(16)]
        return exception_vec
    
    def get_f3_pcs(self)->list[int]:
        return [pc.value for pc in self.top.internal_wires.f3_pcs]
    
    def get_cut_ptrs(self) -> list[int]:
        return [cut_ptr.value for cut_ptr in self.top.internal_wires.f2_cut_ptrs]
        

    def get_addrs(self)->tuple[int, int]:
        return self.top.internal_wires._f3_paddrs_0.value, self.top.internal_wires._f3_gpaddr.value
    
    def get_cut_instrs(self) -> list[int]:
        return [instr.value for instr in self.top.internal_wires.pre_decoder.in_bits_data]
    
    def get_ranges(self) -> int:
        return self.top.internal_wires._f3_instr_range.value
    
    def get_bpu_flush(self) -> bool:
        return self.top.internal_wires._f0_flush_from_bpu_probe.value != 0    
    
    async def get_fires(self):
        return {0: self.top.internal_wires._f0_fire.value, 1: self.top.internal_wires._f1_fire.value, 2:self.top.internal_wires._f2_fire.value, 3:self.top.internal_wires._wb_enable.value}
    
    async def get_flushes(self):
        return {0: self.top.internal_wires._f0_flush_from_bpu_probe.value, 1: self.top.internal_wires._f2_flush.value, 2:self.top.internal_wires._f2_flush.value, 3:self.top.internal_wires._f3_flush.value}

    def get_icache_all_resp(self)-> bool:
        return self.top.internal_wires._icacheRespAllValid.value

    def from_ftq_flush(self, flush_bpu: FTQFlushFromBPU): 
        # redirect = ftqFlushInfo.redirect 
        # flush_bpu = ftqFlushInfo.flush_from_bpu
        stg_names = ["s2", "s3"]
        for stg_name in stg_names:
            stg_bundle: StageFlushBundle = getattr(self.ftqFlushStgsBundle, f"_{stg_name}")
            stg_redirect = flush_bpu.stgs[stg_name]
            stg_bundle._bits._flag.value = stg_redirect.ftqIdx.flag
            stg_bundle._bits._value.value = stg_redirect.ftqIdx.value
            stg_bundle._valid.value = stg_redirect.stg_valid
        
    
    def ftq_redirect(self, redirect: FTQRedirect):
        self.ftqRedirectBundle._valid.value = redirect.valid
        self.ftqRedirectBundle._bits._ftqOffset.value = redirect.ftqOffset
        self.ftqRedirectBundle._bits._level.value = redirect.redirect_level
        self.ftqRedirectBundle._bits._ftqIdx._value.value = redirect.ftqIdx.value
        self.ftqRedirectBundle._bits._ftqIdx._flag.value = redirect.ftqIdx.flag 

    def get_predecode_res(self) -> PreDecodeDataDef:
        predecode_data = PreDecodeDataDef()
        predecode_data.new_instrs=[instr.value for instr in self.top.internal_wires.pre_decoder.out_instrs]
        predecode_data.jmp_offsets=[jmp_offset.value for jmp_offset in self.top.internal_wires.pre_decoder.out_jumpOffsets]
        predecode_data.rvcs = [rvc.value for rvc in self.top.internal_wires.pre_decoder.out_pd_isRVCs]
        predecode_data.valid_starts = [1] + [valid.value for valid in self.top.internal_wires.pre_decoder.out_pd_valids]
        predecode_data.half_valid_starts = [0, 1] + [valid.value for valid in self.top.internal_wires.pre_decoder.out_hasHalfValids]
        return predecode_data

    def get_f3predecoder_res(self)->F3PreDecodeData:
        f3predecode_data = F3PreDecodeData()
        f3predecode_data.brTypes = [br_type.value for br_type in self.top.internal_wires.pre_decoder.out_pd_brTypes]
        f3predecode_data.isCalls = [is_call.value for is_call in self.top.internal_wires.pre_decoder.out_pd_isCalls]
        f3predecode_data.isRets = [is_ret.value for is_ret in self.top.internal_wires.pre_decoder.out_pd_isRets]

        return f3predecode_data

    # @driver_method()
    # async def get_pred_checker_res(self):
    #     pred_check_res = PredCheckerRetData()
    #     pred_check_res.faults = [fault.value for fault in self.top.internal_wires.pred_checker.fault_types]
    #     pred_check_res.fixed_tgts = [fixed_tgt.value for fixed_tgt in self.top.internal_wires.pred_checker.fixed_targets]
    #     pred_check_res.takens = [taken.value for taken in self.top.internal_wires.pred_checker.fixed_takens]
    #     pred_check_res.ranges = [fix_range.value for fix_range in self.top.internal_wires.pred_checker.fixed_ranges]
    #     pred_check_res.jmp_tgts = [jmp_tgt.value for jmp_tgt in self.top.internal_wires.pred_checker.jal_targets]
        
    #     return pred_check_res
    
    def get_pred_checker_stg1_res(self) -> PredCheckerStage1RetData:
        pred_check_res = PredCheckerStage1RetData()
        pred_check_res.takens = [taken.value for taken in self.top.internal_wires.pred_checker.fixed_takens]
        pred_check_res.ranges = [fix_range.value for fix_range in self.top.internal_wires.pred_checker.fixed_ranges]
        
        return pred_check_res

    def get_pred_checker_stg2_res(self) -> PredCheckerStage2RetData:
        pred_check_res = PredCheckerStage2RetData()
        pred_check_res.faults = [fault.value for fault in self.top.internal_wires.pred_checker.fault_types]
        pred_check_res.fixed_tgts = [fixed_tgt.value for fixed_tgt in self.top.internal_wires.pred_checker.fixed_targets]
        pred_check_res.jmp_tgts = [jmp_tgt.value for jmp_tgt in self.top.internal_wires.pred_checker.jal_targets]
        
        return pred_check_res

    # @driver_method()
    # async def get_wb_flush(self):
    #     idx = ExistsIdx()
    #     idx.exists = self.ftqWbBundle._bits._misOffset._valid.value
    #     idx.offsetIdx = self.ftqWbBundle._bits._misOffset._bits.value

    #     return idx

    def collect_res_backto_ftq(self)-> FTQResp:
        response = FTQResp()
        response.valid = self.ftqWbBundle._valid.value
        response.cfiOffset_valid = self.ftqWbBundle._bits._cfiOffset_valid.value
        response.ftqIdx.flag = self.ftqWbBundle._bits._ftqIdx._flag.value
        response.ftqIdx.value = self.ftqWbBundle._bits._ftqIdx._value.value
        response.jalTarget = self.ftqWbBundle._bits._jalTarget.value
        response.target = self.ftqWbBundle._bits._target.value

        # response.misOffset = await self.get_wb_flush()
        response.misOffset.exists = self.ftqWbBundle._bits._misOffset._valid.value
        response.misOffset.offsetIdx = self.ftqWbBundle._bits._misOffset._bits.value
        for i in range(16):
            response.pcs[i] = self.ftqWbBundle._bits._pc[i].value
            response.instrRanges[i] = self.ftqWbBundle._bits._instrRange[i].value
            response.pds.brTypes[i] = self.ftqWbBundle._bits._pd[i]._brType.value
            response.pds.isCalls[i] = self.ftqWbBundle._bits._pd[i]._isCall.value
            response.pds.isRets[i] = self.ftqWbBundle._bits._pd[i]._isRet.value
            response.pds.isRVCs[i] = self.ftqWbBundle._bits._pd[i]._isRVC.value
            response.pds.pdValids[i] = self.ftqWbBundle._bits._pd[i]._valid.value
        
        return response

    def fake_resp(self, icacheStatusResp: ICacheStatusResp):
        icache_resp = icacheStatusResp.resp
        self.icacheInter._resp._valid.value = icache_resp.icache_valid
        self.icacheInter._icacheReady.value = icacheStatusResp.ready
        self.icacheInter._resp._bits._isForVSnonLeafPTE.value = icache_resp.VS_non_leaf_PTE
        self.icacheInter._resp._bits._doubleline.value = icache_resp.double_line
        self.icacheInter._resp._bits._backendException.value = icache_resp.backend_exception
        self.icacheInter._resp._bits._gpaddr.value = icache_resp.gpaddr
        self.icacheInter._resp._bits._data.value = icache_resp.data
        
        self.icacheInter._resp._bits._paddr_0.value = icache_resp.paddr


        for i in range(2):
            self.icacheInter._resp._bits._itlb_pbmt[i].value = icache_resp.itlb_pbmts[i]
            self.icacheInter._resp._bits._exception[i].value = icache_resp.exceptions[i]
            self.icacheInter._resp._bits._vaddr[i].value = icache_resp.vaddrs[i]
            self.icacheInter._resp._bits._pmp_mmio[i].value = icache_resp.pmp_mmios[i]
    
    def set_fs_is_off(self, fs_is_off):
        self.top.ctrl.io_csr_fsIsOff.value = fs_is_off
        

    async def get_icache_stop(self):
        return self.top._icacheInterCtrl._icacheStop.value



    async def set_triggers(self, req: FrontendTriggerReq):
        for i in range(4):
            self.frontendTriggerBundle._tEnableVec[i].value = req.tEnableVec[i]
        
        self.frontendTriggerBundle._tUpdate._valid.value = req.bpSetter.valid

        self.frontendTriggerBundle._tUpdate._bits._addr.value = req.bpSetter.addr

        self.frontendTriggerBundle._tUpdate._bits._tdata._action.value = req.bpSetter.action 
        self.frontendTriggerBundle._tUpdate._bits._tdata._matchType.value = req.bpSetter.matchType 
        self.frontendTriggerBundle._tUpdate._bits._tdata._select.value = req.bpSetter.select 
        self.frontendTriggerBundle._tUpdate._bits._tdata._chain.value = req.bpSetter.chain 
        self.frontendTriggerBundle._tUpdate._bits._tdata._tdata2.value = req.bpSetter.tdata2 
        self.frontendTriggerBundle._debugMode.value = req.debugMode
        self.frontendTriggerBundle._triggerCanRaiseBpExp.value = req.triggerCanRaiseBPExp


    def set_ibuffer_ready(self, ready:bool):
        self.toIbufferAll._toIbuffer._ready.value = ready
    
    def get_toibuffer_info(self) -> ToIbufferAllRes:
        res = ToIbufferAllRes()
        res.toBackendGpaddrMem.gpaddr = self.toIbufferAll._toBackend_gpaddrMem._wdata._gpaddr.value
        res.toBackendGpaddrMem.isForVSnonLeafPTE = self.toIbufferAll._toBackend_gpaddrMem._wdata._isForVSnonLeafPTE.value
        res.toBackendGpaddrMem.wen = self.toIbufferAll._toBackend_gpaddrMem._wen.value
        res.toBackendGpaddrMem.waddr = self.toIbufferAll._toBackend_gpaddrMem._waddr.value  

        res.toIbuffer.valid = self.toIbufferAll._toIbuffer._valid.value
        for i in range(16):
            res.toIbuffer.pds.isRVCs[i] = self.toIbufferAll._toIbuffer._bits._pd[i]._isRVC.value
            res.toIbuffer.pds.brTypes[i] = self.toIbufferAll._toIbuffer._bits._pd[i]._brType.value
            res.toIbuffer.pds.isCalls[i] = self.toIbufferAll._toIbuffer._bits._pd[i]._isCall.value
            res.toIbuffer.pds.isRets[i] = self.toIbufferAll._toIbuffer._bits._pd[i]._isRet.value

            res.toIbuffer.triggereds[i] = self.toIbufferAll._toIbuffer._bits._triggered[i].value
            res.toIbuffer.isLastInFtqEntrys[i] = self.toIbufferAll._toIbuffer._bits._isLastInFtqEntry[i].value
            res.toIbuffer.exceptionTypes[i] = self.toIbufferAll._toIbuffer._bits._exceptionType[i].value
            res.toIbuffer.instrs[i] = self.toIbufferAll._toIbuffer._bits._instrs[i].value
            res.toIbuffer.foldpcs[i] = self.toIbufferAll._toIbuffer._bits._foldpc[i].value
            res.toIbuffer.illegalInstrs[i] = self.toIbufferAll._toIbuffer._bits._illegalInstr[i].value
            res.toIbuffer.crossPageIPFFixs[i] = self.toIbufferAll._toIbuffer._bits._crossPageIPFFix[i].value
            res.toIbuffer.ftqOffset[i] = self.toIbufferAll._toIbuffer._bits._ftqOffset[i].value
        
        res.toIbuffer.ftqPtr.flag = self.toIbufferAll._toIbuffer._bits._ftqPtr._flag.value
        res.toIbuffer.ftqPtr.value = self.toIbufferAll._toIbuffer._bits._ftqPtr._value.value

        res.toIbuffer.backendException = self.toIbufferAll._toIbuffer._bits._backendException_0.value
        res.toIbuffer.enqEnable = self.toIbufferAll._toIbuffer._bits._enqEnable.value
        res.toIbuffer.instr_valids = self.toIbufferAll._toIbuffer._bits._valid.value

        return res

    def set_itlb_req_ready(self, ready:bool):
        self.itlbInter._req._ready.value = ready
    
    def fake_get_itlb_req(self) -> ITLBReq:
        res = ITLBReq()
        res.vaddr = self.itlbInter._req._bits_vaddr.value
        res.valid = self.itlbInter._req._valid.value
        return res
    
    async def get_itlb_resp_ready(self):
        return self.itlbInter._resp._ready.value
    
    def fake_itlb_resp(self, resp: ITLBResp):
        self.itlbInter._resp._valid.value = resp.valid
        self.itlbInter._resp._bits._paddr_0.value = resp.paddr
        self.itlbInter._resp._bits._pbmt_0.value = resp.pbmt
        self.itlbInter._resp._bits._gpaddr_0.value = resp.gpaddr
        self.itlbInter._resp._bits._excp._pf_instr.value = resp.excp.pfInstr
        self.itlbInter._resp._bits._excp._af_instr.value = resp.excp.afInstr
        self.itlbInter._resp._bits._excp._gpf_instr.value = resp.excp.gpfInstr
        self.itlbInter._resp._bits._isForVSnonLeafPTE.value = resp.isForVSnonLeafPTE

    def set_touncache_ready(self, ready:bool):
        self.uncacheInter._toUncache._ready.value = ready

    async def get_to_uncache_req(self):
        to_uncache = ToUncache()
        to_uncache.addr = self.uncacheInter._toUncache._bits_addr.value
        to_uncache.valid = self.uncacheInter._toUncache._valid.value
        return to_uncache
    
    def get_to_uncache_addr(self):
        return self.uncacheInter._toUncache._bits_addr.value
    
    def fake_from_uncache(self, from_uncache: FromUncache):
        self.uncacheInter._fromUncache._bits_data.value = from_uncache.data
        self.uncacheInter._fromUncache._valid.value = from_uncache.valid

    async def receive_mmio_ftq_ptr(self):
        res = FTQIdx()
        res.flag = self.top.mmio_needed._mmioCommitRead._mmioFtqPtr._flag.value
        res.value = self.top.mmio_needed._mmioCommitRead._mmioFtqPtr._value.value
        return res

    def set_mmio_commited(self, isLastCommit: bool):
        self.top.mmio_needed._mmioCommitRead._mmioLastCommit.value = isLastCommit

    def receive_pmp_req_addr(self) -> int:
        return self.top.mmio_needed._pmp._req_bits_addr.value

    def fake_pmp_resp(self, pmp_resp: PMPResp):
        self.top.mmio_needed._pmp._resp._instr.value = pmp_resp.instr
        self.top.mmio_needed._pmp._resp._mmio.value = pmp_resp.mmio

    # list size is constant: 8
    def fake_rob_commits(self, rob_commits: list[RobCommit]):
        for i in range(8):
            robCommitBundle: RobCommitBundle = self.top.mmio_needed._rob_commits[i]
            robCommitBundle._valid.value = rob_commits[i].valid
            robCommitBundle._bits._ftqOffset.value = rob_commits[i].ftqOffset
            robCommitBundle._bits._ftqIdx._flag.value = rob_commits[i].ftqIdx.flag
            robCommitBundle._bits._ftqIdx._value.value = rob_commits[i].ftqIdx.value

    def get_extended_instrs(self) -> list[int]:
        return [instr.value for instr in self.top.to_ibuffer_all._toIbuffer._bits._instrs]

    def get_cur_last_half_valid(self) -> bool:
        return self.top.internal_wires._f3_lastHalf_valid.value != 0
    
    async def reset(self):
        self.top.ctrl.reset.value = 1
        await self.step()
        self.top.ctrl.reset.value = 0
        await self.step()
        
    @driver_method()
    async def deal_with_non_mmio(self, req: NonMMIOReq):
        ftq_query: FTQQuery = req.ftq_req
        flush_from_bpu: FTQFlushFromBPU = req.bpu_flush_info
        icache_resp : ICacheStatusResp = req.icache_resp

        resp = NonMMIOResp()
        # res = {}

        self.query_from_ftq(ftq_query)
        self.from_ftq_flush(flush_from_bpu)

        self.set_icache_ready(icache_resp.ready)
        # await top_agent.ftq_valid_set(True)

        await self.step()

        # collect res of stage 0

        resp.ftq_ready = self.get_ftq_ready()
        resp.bpu_flush_res = self.get_bpu_flush()

        if (not resp.ftq_ready) or resp.bpu_flush_res:
            await self.step()
            return resp

        # print(top_agent.top.io_ftqInter._fromFtq._req._valid.value)

        await self.step()
        # collect res of stage 1

        # done at stage 2?

        # entering stage1

        self.fake_resp(icache_resp)

        await self.step()

        # collect res of stage 2

        # await top_agent.get_icache_stop()
        resp.cut_instrs = self.get_cut_instrs()
        resp.predecode_res = self.get_predecode_res()
        resp.cut_ptrs = self.get_cut_ptrs()

        resp.icache_all_valid = self.get_icache_all_resp()
        f2_exception = self.get_exception()
        
        if not resp.icache_all_valid:
            
            return resp


        # entering stage2
        # input at stage3?


        self.set_fs_is_off(req.fs_is_off)

        self.set_ibuffer_ready(True)

        await self.step()

        # entering stage3
        # collect res of stage 3
        exception_vecs = self.get_exception_vecs()
        resp.exception_vecs = (f2_exception, exception_vecs)
        
        resp.pcs = self.get_f3_pcs()
        resp.addrs = self.get_addrs()

        resp.ranges = self.get_ranges()
        resp.f3_predecode_res = self.get_f3predecoder_res()
        
        # resp.expd_instrs = self.get_extended_instrs()

        resp.pred_checker_stg1_res = self.get_pred_checker_stg1_res()
        
        resp.to_ibuffer = self.get_toibuffer_info()

        await self.step()
            # collect res of stage wb

        resp.pred_checker_stg2_res = self.get_pred_checker_stg2_res()
        
        resp.wb_res = self.collect_res_backto_ftq()
        resp.last_half_valid = self.get_cur_last_half_valid()
        await self.step()
        # await self.step()
        
        return resp

    @driver_method()
    async def set_up_before_mmio_states(self, mmio_cycle_info: MMIOCycleInfo):
        ftq_query = FTQQuery()
        ftq_query.ftqIdx = mmio_cycle_info.ftq_idx

        ftq_query.ftqOffset.exists = True
        ftq_query.ftqOffset.offsetIdx = 0
        ftq_query.startAddr = mmio_cycle_info.ftq_start_addr
        ftq_query.nextlineStart = ftq_query.startAddr + 64

        ftq_query.nextStartAddr = mmio_cycle_info.ftq_start_addr + 28


        icache_resp = ICacheStatusResp()
        icache_resp.resp.backend_exception = False
        icache_resp.resp.double_line = (ftq_query.startAddr & 32) != 0
        icache_resp.resp.pmp_mmios = mmio_cycle_info.icache_pmp_mmios
        icache_resp.resp.data = 0x1096_1227_1189_1204_1217_1221_1444 # not important for this
        icache_resp.resp.vaddrs[0] = ftq_query.startAddr
        icache_resp.resp.vaddrs[1] = ftq_query.nextlineStart
        icache_resp.resp.exceptions = mmio_cycle_info.exceptions
        icache_resp.resp.paddr = mmio_cycle_info.icache_paddr
        icache_resp.resp.gpaddr = 0x1798180418121 # not important for now, but in the future?
        icache_resp.resp.icache_valid = True 
        icache_resp.resp.itlb_pbmts = mmio_cycle_info.icache_itlb_pbmts

        # ftq_flush_info = FTQFlushInfo()
        # use fixed value to keep it unused
        flush_from_bpu = FTQFlushFromBPU()
        safe_flag = mmio_cycle_info.ftq_idx.flag if mmio_cycle_info.ftq_idx.value < 63 else (not mmio_cycle_info.ftq_idx.flag)
        safe_value = mmio_cycle_info.ftq_idx.value + 1 if safe_flag == mmio_cycle_info.ftq_idx.flag else 0
        
        flush_from_bpu.stgs["s2"].stg_valid = False
        flush_from_bpu.stgs["s2"].ftqIdx.flag = safe_flag
        flush_from_bpu.stgs["s2"].ftqIdx.value =safe_value
        flush_from_bpu.stgs["s3"].stg_valid = False
        flush_from_bpu.stgs["s3"].ftqIdx.flag = safe_flag
        flush_from_bpu.stgs["s3"].ftqIdx.value = safe_value

        # this data structure has no connection with non-mmio-situation, so it won't be used later
        ftq_redirect = FTQRedirect()
        ftq_redirect.redirect_level = False
        ftq_redirect.ftqIdx.flag = True
        ftq_redirect.ftqIdx.value = 12
        ftq_redirect.valid = False
        ftq_redirect.ftqOffset = 4

        # done at stage 0
        self.query_from_ftq(ftq_query)
        self.from_ftq_flush(flush_from_bpu)
        self.set_icache_ready(True)
        # await top_agent.ftq_valid_set(True)

        await self.step()

        await self.step()

        # collect stage2 res

        self.fake_resp(icache_resp)

        await self.step()
        self.set_fs_is_off(mmio_cycle_info.csr_fs_is_off)

        await self.step()
        self.cur_state = self.top.internal_wires._mmio_state.value
        

    @driver_method()
    async def deal_with_single_mmio_req(self, mmio_req:MMIOReq):
        self.set_mmio_commited(mmio_req.last_commited)

        self.set_touncache_ready(mmio_req.to_uncache_ready)
        self.fake_from_uncache(mmio_req.from_uncache)

        self.set_itlb_req_ready(mmio_req.itlb_req_ready)

        self.fake_itlb_resp(mmio_req.itlb_resp)

        self.fake_pmp_resp(mmio_req.pmp_resp)

        self.fake_rob_commits(mmio_req.rob_commits)
        
        self.set_ibuffer_ready(mmio_req.to_ibuffer_ready)
        await self.step()
        self.last_state = self.cur_state
        self.cur_state = self.top.internal_wires._mmio_state.value
        if self.last_state == MMIOState.STATE_WAIT_RESP.value and self.cur_state == MMIOState.STATE_SEND_TLB.value:
            return [self.cur_state, self.fake_get_itlb_req()]
        elif (self.last_state == MMIOState.STATE_TLB_RESP.value or self.last_state == MMIOState.STATE_SEND_PMP.value) \
            and self.cur_state == MMIOState.STATE_WAIT_COMMIT.value:
            return [self.cur_state, self.top.to_ibuffer_all._toIbuffer._bits._exceptionType[0].value, \
                self.top.to_ibuffer_all._toBackend_gpaddrMem._wdata._gpaddr.value]
        elif (self.last_state == MMIOState.STATE_TLB_RESP.value and self.cur_state == MMIOState.STATE_SEND_PMP.value):
            return [self.cur_state, self.receive_pmp_req_addr()]
        elif ((self.last_state == MMIOState.STATE_IDLE.value or self.last_state == MMIOState.STATE_WAIT_LAST_CMT.value) \
            and self.cur_state == MMIOState.STATE_SEND_REQ.value) or \
                (self.last_state == MMIOState.STATE_SEND_PMP.value and self.cur_state == MMIOState.STATE_RESEND_REQ.value):
            return [self.cur_state, self.get_to_uncache_addr()]
        elif (self.last_state == MMIOState.STATE_WAIT_RESP.value or self.last_state == MMIOState.STATE_WAIT_RESEND_RESP.value) \
            and self.cur_state == MMIOState.STATE_WAIT_COMMIT.value:
                res = MMIOToIbufferFTQ()
                res.expd_instr = self.toIbufferAll._toIbuffer._bits._instrs[0].value
                res.ill = self.toIbufferAll._toIbuffer._bits._illegalInstr[0].value
                res.is_call = self.toIbufferAll._toIbuffer._bits._pd[0]._isCall.value
                res.is_ret = self.toIbufferAll._toIbuffer._bits._pd[0]._isRet.value
                res.br_type = self.toIbufferAll._toIbuffer._bits._pd[0]._brType.value
                res.is_rvc = self.toIbufferAll._toIbuffer._bits._pd[0]._isRVC.value
                return [self.cur_state, res]
        elif (self.last_state == MMIOState.STATE_WAIT_COMMIT.value and self.cur_state == MMIOState.STATE_COMMITED.value):
            return [self.cur_state, self.top.io_ftqInter._toFtq_pdWb._bits._target.value]
        return [self.cur_state]
        
    @driver_method()
    async def reset_mmio_state(self):
        ftq_redirect = FTQRedirect()
        ftq_redirect.redirect_level = True
        ftq_redirect.valid = True
        self.ftq_redirect(ftq_redirect)
        await self.step()
        ftq_redirect.valid = False
        self.ftq_redirect(ftq_redirect)
        