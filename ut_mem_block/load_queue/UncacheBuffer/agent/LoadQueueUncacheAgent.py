from toffee import Agent, driver_method
from typing import List

from ..bundle.LoadQueueUncacheBundle import LoadQueueUncacheBundle

class IORedirect:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    level = False
    
class RobIO:
    pendingMMIOld = False
    pendingPtr_flag = False
    pendingPtr_value = 0  # 8-bit
    mmio_0 = False   
    mmio_1 = False   
    mmio_2 = False
    uop_0_robIdx_value = 0  # 8-bit
    uop_1_robIdx_value = 0  # 8-bit
    uop_2_robIdx_value = 0  # 8-bit
    
class ReqIO:
    valid = False
    bits_uop_exceptionVec_3 = False
    bits_uop_exceptionVec_4 = False
    bits_uop_exceptionVec_5 = False
    bits_uop_exceptionVec_13 = False
    bits_uop_exceptionVec_21 = False
    bits_uop_trigger = 0  # 4-bit value
    bits_uop_preDecodeInfo_isRVC = False
    bits_uop_ftqPtr_flag = False
    bits_uop_ftqPtr_value = 0  # 6-bit value
    bits_uop_ftqOffset = 0  # 4-bit value
    bits_uop_fuOpType = 0  # 9-bit value
    bits_uop_rfWen = False
    bits_uop_fpWen = False
    bits_uop_vpu_vstart = 0  # 8-bit value
    bits_uop_vpu_veew = 0  # 2-bit value
    bits_uop_uopIdx = 0  # 7-bit value
    bits_uop_pdest = 0  # 8-bit value
    bits_uop_robIdx_flag = False
    bits_uop_robIdx_value = 0  # 8-bit value
    bits_uop_storeSetHit = False
    bits_uop_waitForRobIdx_flag = False
    bits_uop_waitForRobIdx_value = 0  # 8-bit value
    bits_uop_loadWaitBit = False
    bits_uop_loadWaitStrict = False
    bits_uop_lqIdx_flag = False
    bits_uop_lqIdx_value = 0  # 7-bit value
    bits_uop_sqIdx_flag = False
    bits_uop_sqIdx_value = 0  # 6-bit value
    bits_vaddr = 0  # 50-bit value
    bits_fullva = 0  # 64-bit value
    bits_isHyper = False
    bits_paddr = 0  # 48-bit value
    bits_gpaddr = 0  # 64-bit value
    bits_isForVSnonLeafPTE = False
    bits_mask = 0  # 16-bit value
    bits_nc = False
    bits_mmio = False
    bits_memBackTypeMM = False
    bits_isvec = False
    bits_is128bit = False
    bits_vecActive = False
    bits_schedIndex = 0  # 7-bit value
    bits_rep_info_cause_0 = False
    bits_rep_info_cause_1 = False
    bits_rep_info_cause_2 = False
    bits_rep_info_cause_3 = False
    bits_rep_info_cause_4 = False
    bits_rep_info_cause_5 = False
    bits_rep_info_cause_6 = False
    bits_rep_info_cause_7 = False
    bits_rep_info_cause_8 = False
    bits_rep_info_cause_9 = False
    bits_rep_info_cause_10 = False
    
class MmioOut:
    ready = False
    valid = False
    bits_uop_exceptionVec_3 = False
    bits_uop_exceptionVec_4 = False
    bits_uop_exceptionVec_5 = False
    bits_uop_exceptionVec_13 = False
    bits_uop_exceptionVec_19 = False
    bits_uop_exceptionVec_21 = False
    bits_uop_trigger = 0  # 4-bit value
    bits_uop_preDecodeInfo_isRVC = False
    bits_uop_ftqPtr_flag = False
    bits_uop_ftqPtr_value = 0  # 6-bit value
    bits_uop_ftqOffset = 0  # 4-bit value
    bits_uop_fuOpType = 0  # 9-bit value
    bits_uop_rfWen = False
    bits_uop_fpWen = False
    bits_uop_flushPipe = False
    bits_uop_vpu_vstart = 0  # 8-bit value
    bits_uop_vpu_veew = 0  # 2-bit value
    bits_uop_uopIdx = 0  # 7-bit value
    bits_uop_pdest = 0  # 8-bit value
    bits_uop_robIdx_flag = False
    bits_uop_robIdx_value = 0  # 8-bit value
    bits_uop_storeSetHit = False
    bits_uop_waitForRobIdx_flag = False
    bits_uop_waitForRobIdx_value = 0  # 8-bit value
    bits_uop_loadWaitBit = False
    bits_uop_loadWaitStrict = False
    bits_uop_lqIdx_flag = False
    bits_uop_lqIdx_value = 0  # 7-bit value
    bits_uop_sqIdx_flag = False
    bits_uop_sqIdx_value = 0  # 6-bit value
    bits_uop_replayInst = False

class NcOut:
    ready = False
    valid = False
    bits_uop_exceptionVec_4 = False
    bits_uop_exceptionVec_19 = False
    bits_uop_preDecodeInfo_isRVC = False
    bits_uop_ftqPtr_flag = False
    bits_uop_ftqPtr_value = 0  # 6-bit value
    bits_uop_ftqOffset = 0  # 4-bit value
    bits_uop_fuOpType = 0  # 9-bit value
    bits_uop_rfWen = False
    bits_uop_fpWen = False
    bits_uop_vpu_vstart = 0  # 8-bit value
    bits_uop_vpu_veew = 0  # 2-bit value
    bits_uop_uopIdx = 0  # 7-bit value
    bits_uop_pdest = 0  # 8-bit value
    bits_uop_robIdx_flag = False
    bits_uop_robIdx_value = 0  # 8-bit value
    bits_uop_storeSetHit = False
    bits_uop_waitForRobIdx_flag = False
    bits_uop_waitForRobIdx_value = 0  # 8-bit value
    bits_uop_loadWaitBit = False
    bits_uop_loadWaitStrict = False
    bits_uop_lqIdx_flag = False
    bits_uop_lqIdx_value = 0  # 7-bit value
    bits_uop_sqIdx_flag = False
    bits_uop_sqIdx_value = 0  # 6-bit value
    bits_vaddr = 0  # 50-bit value
    bits_paddr = 0  # 48-bit value
    bits_data = 0  # 128-bit value
    bits_isvec = False
    bits_is128bit = False
    bits_vecActive = False
    bits_schedIndex = 0  # 7-bit value
    
class Uncache:
    req_ready = False
    req_valid = False
    req_bits_cmd = 0  # 5-bit value
    req_bits_addr = 0  # 48-bit value
    req_bits_vaddr = 0  # 50-bit value
    req_bits_data = 0  # 64-bit value
    req_bits_mask = 0  # 8-bit value
    req_bits_id = 0  # 7-bit value
    req_bits_nc = False
    req_bits_memBackTypeMM = False
    resp_valid = False
    resp_bits_data = 0  # 64-bit value
    resp_bits_id = 0  # 7-bit value
    resp_bits_nderr = False
    
class Rollback:
    valid = False
    bits_isRVC = False
    bits_robIdx_flag = False
    bits_robIdx_value = 0  # 8-bit value
    bits_ftqIdx_flag = False
    bits_ftqIdx_value = 0  # 6-bit value
    bits_ftqOffset = 0  # 4-bit value
    bits_level = False

class LoadQueueUncacheAgent(Agent):
    def __init__(self, bundle: LoadQueueUncacheBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
        
    @driver_method
    async def Enqueue1(self, req:List[ReqIO], rob:RobIO):
        self.bundle.io._rob._pendingMMIOld.value = rob.pendingMMIOld
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        for i in range(3):
            req_i = getattr(self.bundle.io._req, f'_{i}')
            req_i._valid.value = req[i].valid
            req_i._bits._uop._exceptionVec._3.value = req[i].bits_uop_exceptionVec_3
            req_i._bits._uop._exceptionVec._4.value = req[i].bits_uop_exceptionVec_4
            req_i._bits._uop._exceptionVec._5.value = req[i].bits_uop_exceptionVec_5
            req_i._bits._uop._exceptionVec._13.value = req[i].bits_uop_exceptionVec_13
            req_i._bits._uop._exceptionVec._21.value = req[i].bits_uop_exceptionVec_21
            req_i._bits._uop._trigger.value = req[i].bits_uop_trigger
            req_i._bits._uop._preDecodeInfo._isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
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
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_value
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
            req_i._bits._rep._info._cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep._info._cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep._info._cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep._info._cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep._info._cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep._info._cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep._info._cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep._info._cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep._info._cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep._info._cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep._info._cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step()
        return  self.bundle.LoadQueueUncache, self.bundle.LoadQueueUncache_
        
    @driver_method
    async def Enqueue2(self, req: List[ReqIO], redirect: IORedirect, rob: RobIO):
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
            req_i._bits._uop._preDecodeInfo._isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
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
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_value
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
            req_i._bits._rep._info._cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep._info._cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep._info._cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep._info._cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep._info._cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep._info._cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep._info._cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep._info._cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep._info._cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep._info._cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep._info._cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step()
        return self.bundle.LoadQueueUncache, self.bundle.LoadQueueUncache_
    
    @driver_method
    async def uncachereq(self, req: List[ReqIO], uncache: Uncache, mmioOut: MmioOut, ncOut: List[NcOut], rob: RobIO):
        self.bundle.io._rob._pendingMMIOld.value = rob.pendingMMIOld
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        self.bundle.io._uncache._req._ready.value = uncache.req_ready
        self.bundle.io._uncache._resp._valid.value = uncache.resp_valid
        self.bundle.io._uncache._resp._bits._data.value = uncache.resp_bits_data
        self.bundle.io._uncache._resp._bits._id.value = uncache.resp_bits_id
        self.bundle.io._uncache._resp._bits._nderr.value = uncache.resp_bits_nderr
        self.bundle.io._mmioOut._2._ready.value = mmioOut.ready
        for i in range(3):
            req_i = getattr(self.bundle.io._req, f'_{i}')
            ncOut_i = getattr(self.bundle.io._ncOut, f'_{i}')
            ncOut_i._ready.value = ncOut[i].ready
            req_i._valid.value = req[i].valid
            req_i._bits._uop._exceptionVec._3.value = req[i].bits_uop_exceptionVec_3
            req_i._bits._uop._exceptionVec._4.value = req[i].bits_uop_exceptionVec_4
            req_i._bits._uop._exceptionVec._5.value = req[i].bits_uop_exceptionVec_5
            req_i._bits._uop._exceptionVec._13.value = req[i].bits_uop_exceptionVec_13
            req_i._bits._uop._exceptionVec._21.value = req[i].bits_uop_exceptionVec_21
            req_i._bits._uop._trigger.value = req[i].bits_uop_trigger
            req_i._bits._uop._preDecodeInfo._isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
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
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_value
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
            req_i._bits._rep._info._cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep._info._cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep._info._cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep._info._cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep._info._cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep._info._cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep._info._cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep._info._cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep._info._cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep._info._cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep._info._cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step()
        return self.bundle.io._uncache._req, self.bundle.LoadQueueUncache, self.bundle.LoadQueueUncache_
    
    @driver_method
    async def uncacheresp(self, uncache: Uncache, req: List[ReqIO], rob: RobIO):
        self.bundle.io._rob._pendingMMIOld.value = rob.pendingMMIOld
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        self.bundle.io._uncache._req._ready.value = uncache.req_ready
        self.bundle.io._uncache._resp._valid.value = uncache.resp_valid
        self.bundle.io._uncache._resp._bits._data.value = uncache.resp_bits_data
        self.bundle.io._uncache._resp._bits._id.value = uncache.resp_bits_id
        self.bundle.io._uncache._resp._bits._nderr.value = uncache.resp_bits_nderr
        for i in range(3):
            req_i = getattr(self.bundle.io._req, f'_{i}')
            req_i._valid.value = req[i].valid
            req_i._bits._uop._exceptionVec._3.value = req[i].bits_uop_exceptionVec_3
            req_i._bits._uop._exceptionVec._4.value = req[i].bits_uop_exceptionVec_4
            req_i._bits._uop._exceptionVec._5.value = req[i].bits_uop_exceptionVec_5
            req_i._bits._uop._exceptionVec._13.value = req[i].bits_uop_exceptionVec_13
            req_i._bits._uop._exceptionVec._21.value = req[i].bits_uop_exceptionVec_21
            req_i._bits._uop._trigger.value = req[i].bits_uop_trigger
            req_i._bits._uop._preDecodeInfo._isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
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
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_value
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
            req_i._bits._rep._info._cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep._info._cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep._info._cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep._info._cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep._info._cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep._info._cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep._info._cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep._info._cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep._info._cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep._info._cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep._info._cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step()
        return self.bundle.LoadQueueUncache, self.bundle.LoadQueueUncache_
    
    @driver_method
    async def Dequeue(self, rob: RobIO, req: List[ReqIO]):
        self.bundle.io._rob._pendingMMIOld.value = rob.pendingMMIOld
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        for i in range(3):
            req_i = getattr(self.bundle.io._req, f'_{i}')
            req_i._valid.value = req[i].valid
            req_i._bits._uop._exceptionVec._3.value = req[i].bits_uop_exceptionVec_3
            req_i._bits._uop._exceptionVec._4.value = req[i].bits_uop_exceptionVec_4
            req_i._bits._uop._exceptionVec._5.value = req[i].bits_uop_exceptionVec_5
            req_i._bits._uop._exceptionVec._13.value = req[i].bits_uop_exceptionVec_13
            req_i._bits._uop._exceptionVec._21.value = req[i].bits_uop_exceptionVec_21
            req_i._bits._uop._trigger.value = req[i].bits_uop_trigger
            req_i._bits._uop._preDecodeInfo._isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
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
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_value
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
            req_i._bits._rep._info._cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep._info._cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep._info._cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep._info._cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep._info._cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep._info._cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep._info._cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep._info._cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep._info._cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep._info._cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep._info._cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step()
        return self.bundle.LoadQueueUncache, self.bundle.LoadQueueUncache_
    
    @driver_method
    async def rollback(self, redirect: IORedirect, rob: RobIO, req: ReqIO):
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
            req_i._bits._uop._preDecodeInfo._isRVC.value = req[i].bits_uop_preDecodeInfo_isRVC
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
            req_i._bits._uop._waitForRobIdx._flag.value = req[i].bits_uop_waitForRobIdx_value
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
            req_i._bits._rep._info._cause._0.value = req[i].bits_rep_info_cause_0
            req_i._bits._rep._info._cause._1.value = req[i].bits_rep_info_cause_1
            req_i._bits._rep._info._cause._2.value = req[i].bits_rep_info_cause_2
            req_i._bits._rep._info._cause._3.value = req[i].bits_rep_info_cause_3
            req_i._bits._rep._info._cause._4.value = req[i].bits_rep_info_cause_4
            req_i._bits._rep._info._cause._5.value = req[i].bits_rep_info_cause_5
            req_i._bits._rep._info._cause._6.value = req[i].bits_rep_info_cause_6
            req_i._bits._rep._info._cause._7.value = req[i].bits_rep_info_cause_7
            req_i._bits._rep._info._cause._8.value = req[i].bits_rep_info_cause_8
            req_i._bits._rep._info._cause._9.value = req[i].bits_rep_info_cause_9
            req_i._bits._rep._info._cause._10.value = req[i].bits_rep_info_cause_10
        await self.bundle.step()
        return self.bundle.io._rollback
    