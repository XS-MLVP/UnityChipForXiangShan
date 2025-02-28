from toffee import Agent
from ..bundle import IFUTopBundle, StageFlushBundle, RobCommitBundle
from ..datadef import FTQQuery, ICacheStatusResp, FTQFlushInfo, FTQResp, FrontendTriggerReq, \
        ToIbufferAllRes, ITLBReq, ITLBResp, ToUncache, FromUncache, FTQIdx, PMPResp, RobCommit

class OutsideAgent(Agent):
    def __init__(self, bundle: IFUTopBundle):
        super().__init__(bundle)
        self.top = bundle
        self.ftqReqBundle = bundle.io_ftqInter._fromFtq._req
        self.ftqWbBundle = bundle.io_ftqInter._toFtq_pdWb
        self.ftqRedirectBundle = bundle.io_ftqInter._fromFtq._redirect
        self.ftqFlushStgsBundle = bundle.io_ftqInter._fromFtq._flushFromBpu
        self.flushResBundle = bundle.internal_flushes
        self.icacheInter = self.top._icacheInterCtrl._icacheInter
        self.frontendTriggerBundle = self.top.io_frontendTrigger
        self.toIbufferAll = self.top.to_ibuffer_all
        self.itlbInter = self.top.mmio_needed._iTLBInter
        self.uncacheInter = self.top.mmio_needed._uncacheInter


    async def one_term(self, query: FTQQuery, ftq_flush_info: FTQFlushInfo, icacheStatusResp: ICacheStatusResp, triggerReq: FrontendTriggerReq, ibufferReady):
        from_uncache = FromUncache()
        itlb_resp = ITLBResp()
        pmp_resp = PMPResp()
        rob_commits = [RobCommit() for i in range(8)]
        # done at stage 0

        self.query_from_ftq(query)
        self.from_ftq_flush(ftq_flush_info)
        self.set_icache_ready(icacheStatusResp.ready)
        await self.top.step(2)
        # done at stage 2?
        self.get_ftq_ready()
        self.fake_resp(icacheStatusResp)
        await self.top.step()
        # done at stage3?
        self.receive_mmio_ftq_ptr()
        self.set_mmio_commited(True)

        self.set_touncache_ready(True)
        self.get_to_uncache_req()
        self.fake_from_uncache(from_uncache)

        self.set_itlb_req_ready(True)
        self.fake_get_itlb_req()

        self.get_itlb_resp_ready()
        self.fake_itlb_resp(itlb_resp)

        self.receive_pmp_req_addr()
        self.fake_pmp_resp(pmp_resp)
    
        self.fake_rob_commits(rob_commits)

        self.set_triggers(triggerReq)

        self.set_ibuffer_ready(ibufferReady)

        self.get_icache_stop()
        await self.top.step()
        
        self.collect_res_backto_ftq()

    async def set_icache_ready(self, ready):
        self.icacheInter._icacheReady.value = ready

    async def get_ftq_ready(self):
        return self.ftqReqBundle._ready.value

    async def query_from_ftq(self, query: FTQQuery):   
        self.ftqReqBundle._bits._ftqIdx._flag.value = query.ftqIdx.flag
        self.ftqReqBundle._bits._ftqIdx._value.value = query.ftqIdx.value
        self.ftqReqBundle._bits._ftqOffset._valid.value = query.ftqOffset.exists
        self.ftqReqBundle._bits._ftqOffset._bits.value = query.ftqOffset.offsetIdx
        self.ftqReqBundle._bits._nextlineStart.value = query.nextlineStart
        self.ftqReqBundle._bits._startAddr.value = query.startAddr
        self.ftqReqBundle._bits._nextStartAddr.value = query.nextStartAddr
    
    async def from_ftq_flush(self, ftqFlushInfo:FTQFlushInfo): 
        flush_bpu = ftqFlushInfo.flush_from_bpu
        redirect = ftqFlushInfo.redirect 
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
    
    async def collect_res_backto_ftq(self):
        response = FTQResp()
        response.valid = self.ftqWbBundle._valid.value
        response.cfiOffset_valid = self.ftqWbBundle._bits._cfiOffset_valid.value
        response.ftqIdx.flag = self.ftqWbBundle._bits._ftqIdx._flag.value
        response.ftqIdx.value = self.ftqWbBundle._bits._ftqIdx._value.value
        response.jalTarget = self.ftqWbBundle._bits._jalTarget.value
        response.target = self.ftqWbBundle._bits._target.value
        response.misOffset.exists = self.ftqWbBundle._bits._misOffset._valid.value
        response.misOffset.offsetIdx = self.ftqWbBundle._bits._misOffset._bits.value
        for i in range(16):
            response.pcs[i] = getattr(self.ftqWbBundle._bits._pc, f"_{i}").value
            response.instrRanges[i] = getattr(self.ftqWbBundle._bits._instrRange, f"_{i}").value
            response.pds[i].brType = getattr(self.ftqWbBundle._bits._pd, f"_{i}")._brType.value
            response.pds[i].isCall = getattr(self.ftqWbBundle._bits._pd, f"_{i}")._isCall.value
            response.pds[i].isRet = getattr(self.ftqWbBundle._bits._pd, f"_{i}")._isRet.value
            response.pds[i].isRVC = getattr(self.ftqWbBundle._bits._pd, f"_{i}")._isRVC.value
            response.pds[i].pdValid = getattr(self.ftqWbBundle._bits._pd, f"_{i}")._valid.value
        
        return response
    
    async def fake_resp(self, icacheStatusResp: ICacheStatusResp):
        icache_resp = icacheStatusResp.resp
        self.icacheInter._icacheReady.value = icacheStatusResp.ready
        self.icacheInter._resp._valid.value = icache_resp.icache_valid
        self.icacheInter._resp._bits._isForVSnonLeafPTE.value = icache_resp.VS_non_leaf_PTE
        self.icacheInter._resp._bits._doubleline.value = icache_resp.double_line
        self.icacheInter._resp._bits._backendException.value = icache_resp.backend_exception
        self.icacheInter._resp._bits._gpaddr.value = icache_resp.gpaddr
        self.icacheInter._resp._bits._data.value = icache_resp.data
        
        self.icacheInter._resp._bits._paddr._0.value = icache_resp.paddr

        for i in range(2):
            getattr(self.icacheInter._resp._bits._itlb_pbmt, f"_{i}").value = icache_resp.itlb_pbmts[i]
            getattr(self.icacheInter._resp._bits._exception, f"_{i}").value = icache_resp.exceptions[i]
            getattr(self.icacheInter._resp._bits._vaddr, f"_{i}").value = icache_resp.vaddrs[i]
            getattr(self.icacheInter._resp._bits._pmp_mmio, f"_{i}").value = icache_resp.pmp_mmios[i]

    async def get_icache_stop(self):
        return self.top._icacheInterCtrl._icacheStop.value



    async def set_triggers(self, req: FrontendTriggerReq):
        for i in range(4):
            getattr(self.frontendTriggerBundle._tEnableVec, f"_{i}").value = req.tEnableVec[i]
        
        self.frontendTriggerBundle._tUpdate._valid.value = req.bpSetter.valid

        self.frontendTriggerBundle._tUpdate._bits._addr.value = req.bpSetter.addr

        self.frontendTriggerBundle._tUpdate._bits._tdata._action.value = req.bpSetter.action 
        self.frontendTriggerBundle._tUpdate._bits._tdata._matchType.value = req.bpSetter.matchType 
        self.frontendTriggerBundle._tUpdate._bits._tdata._select.value = req.bpSetter.select 
        self.frontendTriggerBundle._tUpdate._bits._tdata._chain.value = req.bpSetter.chain 
        self.frontendTriggerBundle._tUpdate._bits._tdata._tdata2.value = req.bpSetter.tdata2 
        self.frontendTriggerBundle._debugMode.value = req.debugMode
        self.frontendTriggerBundle._triggerCanRaiseBpExp.value = req.triggerCanRaiseBPExp
        self.top.ctrl.io_csr_fsIsOff.value = req.fsIsOff


    async def set_ibuffer_ready(self, ready:bool):
        self.toIbufferAll._toIbuffer._ready.value = ready

    async def get_toibuffer_info(self):
        res = ToIbufferAllRes()
        res.toBackendGpaddrMem.gpaddr = self.toIbufferAll._toBackend_gpaddrMem._wdata._gpaddr.value
        res.toBackendGpaddrMem.isForVSnonLeafPTE = self.toIbufferAll._toBackend_gpaddrMem._wdata._isForVSnonLeafPTE.value
        res.toBackendGpaddrMem.wen = self.toIbufferAll._toBackend_gpaddrMem._wen.value
        res.toBackendGpaddrMem.waddr = self.toIbufferAll._toBackend_gpaddrMem._waddr.value  

        res.toIbuffer.valid = self.toIbufferAll._toIbuffer._valid.value
        for i in range(16):
            res.toIbuffer.pds[i].isRVC = getattr(self.toIbufferAll._toIbuffer._bits._pd, f"_{i}")._isRVC.value
            res.toIbuffer.pds[i].brType = getattr(self.toIbufferAll._toIbuffer._bits._pd, f"_{i}")._brType.value
            res.toIbuffer.triggereds[i] = getattr(self.toIbufferAll._toIbuffer._bits._triggered, f"_{i}").value
            res.toIbuffer.isLastInFtqEntrys[i] = getattr(self.toIbufferAll._toIbuffer._bits._isLastInFtqEntry, f"_{i}").value
            res.toIbuffer.exceptionTypes[i] = getattr(self.toIbufferAll._toIbuffer._bits._exceptionType, f"_{i}").value
            res.toIbuffer.instrs[i] = getattr(self.toIbufferAll._toIbuffer._bits._instrs, f"_{i}").value
            res.toIbuffer.foldpcs[i] = getattr(self.toIbufferAll._toIbuffer._bits._foldpc, f"_{i}").value
            res.toIbuffer.illegalInstrs[i] = getattr(self.toIbufferAll._toIbuffer._bits._illegalInstr, f"_{i}").value
            res.toIbuffer.crossPageIPFFixs[i] = getattr(self.toIbufferAll._toIbuffer._bits._crossPageIPFFix, f"_{i}").value
            res.toIbuffer.ftqOffset[i] = getattr(self.toIbufferAll._toIbuffer._bits._ftqOffset, f"_{i}")._valid.value
        
        res.toIbuffer.ftqPtr.flag = self.toIbufferAll._toIbuffer._bits._ftqPtr._flag.value
        res.toIbuffer.ftqPtr.flag = self.toIbufferAll._toIbuffer._bits._ftqPtr._value.value

        res.toIbuffer.backendException = self.toIbufferAll._toIbuffer._bits._backendException._0.value
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
        self.itlbInter._resp._bits._paddr.value = resp.paddr
        self.itlbInter._resp._bits._pbmt.value = resp.pbmt
        self.itlbInter._resp._bits._gpaddr.value = resp.gpaddr
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
            robCommitBundle: RobCommitBundle = getattr(self.top.mmio_needed._rob_commits, f"_{i}")
            robCommitBundle._valid.value = rob_commits[i].valid
            robCommitBundle._bits._ftqOffset.value = rob_commits[i].ftqOffset
            robCommitBundle._bits._ftqIdx._flag.value = rob_commits[i].ftqIdx.flag
            robCommitBundle._bits._ftqIdx._value.value = rob_commits[i].ftqIdx.value
