from toffee import Agent, driver_method
from typing import List

from ..bundle.LoadQueueUncacheBundle import LoadQueueUncacheBundle

from ..util.dataclass import IORedirect, RobIO, ReqIO, Uncache

class LoadQueueUncacheAgent(Agent):
    def __init__(self, bundle: LoadQueueUncacheBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
        
    @driver_method()
    async def update(self, req:List[ReqIO], rob:RobIO, redirect: IORedirect):
        self.bundle.io._rob._pendingMMIOld.value = rob.pendingMMIOld
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        for i in range(3):
            req_i = getattr(self.bundle.io._req, f'_{i}')
            req_i._valid.value = req[i].valid
            req_i._bits._uop._exceptionVec._3.value = req[i].bits_uop_exceptionVec_3
            req_i._bits._uop._exceptionVec._4.value = req[i].bits_uop_exceptionVec_4
            req_i._bits._uop._exceptionVec._5.value = req[i].bits_uop_exceptionVec_5
            req_i._bits._uop._exceptionVec._13.value = req[i].bits_uop_exceptionVec_13
            req_i._bits._uop._exceptionVec._21.value = req[i].bits_uop_exceptionVec_21
            req_i._bits._uop._trigger.value = req[i].bits_uop_trigger
            req_i._bits._uop._preDecodeInfo_isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
            req_i._bits._uop._ftqPtr._flag.value = req[i].bits_uop_ftqPtr_flag
            req_i._bits._uop._ftqPtr._value.value = req[i].bits_uop_ftqPtr_value
            req_i._bits._uop._ftqOffset.value = req[i].bits_uop_ftqOffset
            req_i._bits._uop._fuOpType.value = req[i].bits_uop_fuOpType
            req_i._bits._uop._rfWen.value = req[i].bits_uop_rfWen
            req_i._bits._uop._fpWen.value = req[i].bits_uop_fpWen
            req_i._bits._uop._vpu._vstart.value = req[i].bits_uop_vpu_vstart
            req_i._bits._uop._vpu._veew.value = req[i].bits_uop_vpu_veew
            req_i._bits._uop._uopIdx.value = req[i].bits_uop_uopIdx
            req_i._bits._uop._pdest.value = req[i].bits_uop_pdest
            req_i._bits._uop._robIdx._flag.value = req[i].bits_uop_robIdx_flag
            req_i._bits._uop._robIdx._value.value = req[i].bits_uop_robIdx_value
            req_i._bits._uop._storeSetHit.value = req[i].bits_uop_storeSetHit
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_flag
            req_i._bits._uop._waitForRobIdx._value.value = req[i].bits_uop_waitForRobIdx_value
            req_i._bits._uop._loadWaitBit.value = req[i].bits_uop_loadWaitBit
            req_i._bits._uop._loadWaitStrict.value = req[i].bits_uop_loadWaitStrict
            req_i._bits._uop._lqIdx._flag.value = req[i].bits_uop_lqIdx_flag
            req_i._bits._uop._lqIdx._value.value = req[i].bits_uop_lqIdx_value
            req_i._bits._uop._sqIdx._flag.value = req[i].bits_uop_sqIdx_flag
            req_i._bits._uop._sqIdx._value.value = req[i].bits_uop_sqIdx_value
            req_i._bits._vaddr.value = req[i].bits_vaddr
            req_i._bits._fullva.value = req[i].bits_fullva
            req_i._bits._isHyper.value = req[i].bits_isHyper
            req_i._bits._paddr.value = req[i].bits_paddr
            req_i._bits._gpaddr.value = req[i].bits_gpaddr
            req_i._bits._isForVSnonLeafPTE.value = req[i].bits_isForVSnonLeafPTE
            req_i._bits._mask.value = req[i].bits_mask
            req_i._bits._nc.value = req[i].bits_nc
            req_i._bits._mmio.value = req[i].bits_mmio
            req_i._bits._memBackTypeMM.value = req[i].bits_memBackTypeMM
            req_i._bits._isvec.value = req[i].bits_isvec
            req_i._bits._is128bit.value = req[i].bits_is128bit
            req_i._bits._vecActive.value = req[i].bits_vecActive
            req_i._bits._schedIndex.value = req[i].bits_schedIndex
            req_i._bits._rep_info_cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep_info_cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep_info_cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep_info_cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep_info_cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep_info_cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep_info_cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep_info_cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep_info_cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep_info_cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep_info_cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step(1)
        self.bundle.io._redirect._valid.value = False
        for i in range(3):
            req_i = getattr(self.bundle.io._req, f'_{i}')
            req_i._valid.value = False
        await self.bundle.step(1)
        return  self.bundle.LoadQueueUncache
        
    @driver_method()
    async def uncache(self, uncache: Uncache):
        self.bundle.io._uncache._resp._valid.value = uncache.resp_valid
        self.bundle.io._uncache._resp._bits._data.value = uncache.resp_bits_data
        self.bundle.io._uncache._resp._bits._id.value = uncache.resp_bits_id
        self.bundle.io._uncache._resp._bits._nderr.value = uncache.resp_bits_nderr
        await self.bundle.step(1)
        self.bundle.io._uncache._resp._valid.value = False
        await self.bundle.step(2)
        return self.bundle.io._uncache._req, self.bundle.LoadQueueUncache, self.bundle.io._rollback
