from toffee import Agent, driver_method
from ..bundle import IFUTopBundle, StageFlushBundle, RobCommitBundle
from ..datadef import FTQQuery, ICacheStatusResp, FTQFlushInfo, FTQResp, FrontendTriggerReq, \
        ToIbufferAllRes, ITLBReq, ITLBResp, ToUncache, FromUncache, FTQIdx, PMPResp, RobCommit, FTQFlushFromBPU, ExistsIdx,\
        PreDecodeDataDef, F3PreDecodeData, PredCheckerRetData

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

    @driver_method()
    async def set_icache_ready(self, ready):
        self.icacheInter._icacheReady.value = ready

    @driver_method()
    async def get_ftq_ready(self):
        return self.ftqReqBundle._ready.value

    @driver_method()
    async def query_from_ftq(self, query: FTQQuery):   
        self.ftqReqBundle._bits._ftqIdx._flag.value = query.ftqIdx.flag
        self.ftqReqBundle._bits._ftqIdx._value.value = query.ftqIdx.value

        self.ftqReqBundle._bits._ftqOffset._valid.value = query.ftqOffset.exists
        self.ftqReqBundle._bits._ftqOffset._bits.value = query.ftqOffset.offsetIdx
        self.ftqReqBundle._bits._startAddr.value = query.startAddr
        self.ftqReqBundle._bits._nextStartAddr.value = query.nextStartAddr
        
        self.ftqReqBundle._bits._nextlineStart.value = query.nextlineStart
        self.ftqReqBundle._valid.value = query.valid

    @driver_method()
    async def get_exception_vecs(self):
        f2_exception = [self.top.internal_wires.f2_exceptions[i].value for i in range(2)]
        exception_vec = [self.top.internal_wires.f3_exception_vec[i].value for i in range(16)]
        return f2_exception, exception_vec
    
    @driver_method()
    async def get_f1_pcs_cut_ptrs(self):
        return [pc.value for pc in self.top.internal_wires.f3_pcs], \
               [cut_ptr.value for cut_ptr in self.top.internal_wires.f2_cut_ptrs]
    
    @driver_method()
    async def get_addrs(self):
        return self.top.internal_wires._f3_paddrs_0.value, self.top.internal_wires._f3_gpaddr.value
    
    @driver_method()
    async def get_cut_instrs(self):
        return [instr.value for instr in self.top.internal_wires.pre_decoder.in_bits_data]
    
    @driver_method()
    async def get_ranges(self):
        return self.top.internal_wires._f3_instr_range.value
    
    @driver_method()
    async def get_bpu_flush(self):
        return self.top.internal_wires._f0_flush_from_bpu_probe.value        

    @driver_method()
    async def from_ftq_flush(self, ftqFlushInfo:FTQFlushInfo): 
        redirect = ftqFlushInfo.redirect 
        flush_bpu = ftqFlushInfo.flush_from_bpu
        stg_names = ["s2", "s3"]
        for stg_name in stg_names:
            stg_bundle: StageFlushBundle = getattr(self.ftqFlushStgsBundle, f"_{stg_name}")
            stg_redirect = flush_bpu.stgs[stg_name]
            stg_bundle._bits._flag.value = stg_redirect.ftqIdx.flag
            stg_bundle._bits._value.value = stg_redirect.ftqIdx.value
            stg_bundle._valid.value = stg_redirect.stg_valid
        
        self.ftqRedirectBundle._valid.value = redirect.valid
        self.ftqRedirectBundle._bits._ftqOffset.value = redirect.ftqOffset
        self.ftqRedirectBundle._bits._level.value = redirect.redirect_level
        self.ftqRedirectBundle._bits._ftqIdx._value.value = redirect.ftqIdx.value
        self.ftqRedirectBundle._bits._ftqIdx._flag.value = redirect.ftqIdx.flag 
    
    @driver_method()
    async def get_predecode_res(self) -> PreDecodeDataDef:
        predecode_data = PreDecodeDataDef()
        predecode_data.new_instrs=[instr.value for instr in self.top.internal_wires.pre_decoder.out_instrs]
        predecode_data.jmp_offsets=[jmp_offset.value for jmp_offset in self.top.internal_wires.pre_decoder.out_jumpOffsets]
        predecode_data.rvcs = [rvc.value for rvc in self.top.internal_wires.pre_decoder.out_pd_isRVCs]
        predecode_data.valid_starts = [1] + [valid.value for valid in self.top.internal_wires.pre_decoder.out_pd_valids]
        predecode_data.half_valid_starts = [0, 1] + [valid.value for valid in self.top.internal_wires.pre_decoder.out_hasHalfValids]
        return predecode_data

    @driver_method()
    async def get_f3predecoder_res(self)->F3PreDecodeData:
        f3predecode_data = F3PreDecodeData()
        f3predecode_data.brTypes = [br_type.value for br_type in self.top.internal_wires.pre_decoder.out_pd_brTypes]
        f3predecode_data.isCalls = [is_call.value for is_call in self.top.internal_wires.pre_decoder.out_pd_isCalls]
        f3predecode_data.isRets = [is_ret.value for is_ret in self.top.internal_wires.pre_decoder.out_pd_isRets]

        return f3predecode_data, [valid.value for valid in self.top.internal_wires.pred_checker.instr_valids]

    @driver_method()
    async def get_pred_checker_res(self):
        pred_check_res = PredCheckerRetData()
        pred_check_res.faults = [fault.value for fault in self.top.internal_wires.pred_checker.fault_types]
        pred_check_res.fixed_tgts = [fixed_tgt.value for fixed_tgt in self.top.internal_wires.pred_checker.fixed_targets]
        pred_check_res.takens = [taken.value for taken in self.top.internal_wires.pred_checker.fixed_takens]
        pred_check_res.ranges = [fix_range.value for fix_range in self.top.internal_wires.pred_checker.fixed_ranges]
        pred_check_res.jmp_tgts = [jmp_tgt.value for jmp_tgt in self.top.internal_wires.pred_checker.jal_targets]
        
        return pred_check_res

    @driver_method()
    async def get_wb_flush(self):
        idx = ExistsIdx()
        idx.exists = self.ftqWbBundle._bits._misOffset._valid.value
        idx.offsetIdx = self.ftqWbBundle._bits._misOffset._bits.value

        return idx

    @driver_method()
    async def collect_res_backto_ftq(self):
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

    @driver_method()
    async def fake_resp(self, icacheStatusResp: ICacheStatusResp, fs_is_off):
        icache_resp = icacheStatusResp.resp
        self.icacheInter._resp._valid.value = icache_resp.icache_valid
        self.icacheInter._icacheReady.value = icacheStatusResp.ready
        self.icacheInter._resp._bits._isForVSnonLeafPTE.value = icache_resp.VS_non_leaf_PTE
        self.icacheInter._resp._bits._doubleline.value = icache_resp.double_line
        self.icacheInter._resp._bits._backendException.value = icache_resp.backend_exception
        self.icacheInter._resp._bits._gpaddr.value = icache_resp.gpaddr
        self.icacheInter._resp._bits._data.value = icache_resp.data
        
        self.icacheInter._resp._bits._paddr_0.value = icache_resp.paddr
        self.top.ctrl.io_csr_fsIsOff.value = fs_is_off


        for i in range(2):
            self.icacheInter._resp._bits._itlb_pbmt[i].value = icache_resp.itlb_pbmts[i]
            self.icacheInter._resp._bits._exception[i].value = icache_resp.exceptions[i]
            self.icacheInter._resp._bits._vaddr[i].value = icache_resp.vaddrs[i]
            self.icacheInter._resp._bits._pmp_mmio[i].value = icache_resp.pmp_mmios[i]

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


    async def set_ibuffer_ready(self, ready:bool):
        self.toIbufferAll._toIbuffer._ready.value = ready
    
    @driver_method()
    async def get_toibuffer_info(self):
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
        res.toIbuffer.ftqPtr.flag = self.toIbufferAll._toIbuffer._bits._ftqPtr._value.value

        res.toIbuffer.backendException = self.toIbufferAll._toIbuffer._bits._backendException_0.value
        res.toIbuffer.enqEnable = self.toIbufferAll._toIbuffer._bits._enqEnable.value
        res.toIbuffer.instr_valids = self.toIbufferAll._toIbuffer._bits._valid.value

        return res

    async def set_itlb_req_ready(self, ready:bool):
        self.itlbInter._req._ready.value = ready
    
    async def fake_get_itlb_req(self):
        res = ITLBReq()
        res.vaddr = self.itlbInter._req._bits_vaddr.value
        res.valid = self.itlbInter._req._valid.value
        return res
    
    async def get_itlb_resp_ready(self):
        return self.itlbInter._resp._ready.value
    
    async def fake_itlb_resp(self, resp: ITLBResp):
        self.itlbInter._resp._valid.value = resp.valid
        self.itlbInter._resp._bits._paddr_0.value = resp.paddr
        self.itlbInter._resp._bits._pbmt_0.value = resp.pbmt
        self.itlbInter._resp._bits._gpaddr_0.value = resp.gpaddr
        self.itlbInter._resp._bits._excp._pf_instr.value = resp.excp.pfInstr
        self.itlbInter._resp._bits._excp._af_instr.value = resp.excp.afInstr
        self.itlbInter._resp._bits._excp._gpf_instr.value = resp.excp.gpfInstr
        self.itlbInter._resp._bits._isForVSnonLeafPTE.value = resp.isForVSnonLeafPTE

    async def set_touncache_ready(self, ready:bool):
        self.uncacheInter._toUncache._ready.value = ready

    async def get_to_uncache_req(self):
        to_uncache = ToUncache()
        to_uncache.addr = self.uncacheInter._toUncache._bits_addr.value
        to_uncache.valid = self.uncacheInter._toUncache._valid.value
        return to_uncache
    
    async def fake_from_uncache(self, from_uncache: FromUncache):
        self.uncacheInter._fromUncache._bits_data.value = from_uncache.data
        self.uncacheInter._fromUncache._valid.value = from_uncache.valid

    async def receive_mmio_ftq_ptr(self):
        res = FTQIdx()
        res.flag = self.top.mmio_needed._mmioCommitRead._mmioFtqPtr._flag.value
        res.value = self.top.mmio_needed._mmioCommitRead._mmioFtqPtr._value.value
        return res

    async def set_mmio_commited(self, isLastCommit: bool):
        self.top.mmio_needed._mmioCommitRead._mmioLastCommit.value = isLastCommit

    async def receive_pmp_req_addr(self):
        return self.top.mmio_needed._pmp._req_bits_addr.value

    async def fake_pmp_resp(self, pmp_resp: PMPResp):
        self.top.mmio_needed._pmp._resp._instr.value = pmp_resp.instr
        self.top.mmio_needed._pmp._resp._mmio.value = pmp_resp.mmio

    # list size is constant: 8
    async def fake_rob_commits(self, rob_commits: list[RobCommit]):
        for i in range(8):
            robCommitBundle: RobCommitBundle = self.top.mmio_needed._rob_commits[i]
            robCommitBundle._valid.value = rob_commits[i].valid
            robCommitBundle._bits._ftqOffset.value = rob_commits[i].ftqOffset
            robCommitBundle._bits._ftqIdx._flag.value = rob_commits[i].ftqIdx.flag
            robCommitBundle._bits._ftqIdx._value.value = rob_commits[i].ftqIdx.value

    @driver_method()
    async def get_extended_instrs(self):
        return [instr.value for instr in self.top.to_ibuffer_all._toIbuffer._bits._instrs]

    @driver_method()
    async def get_cur_last_half_valid(self):
        return self.top.internal_wires._f3_lastHalf_valid.value