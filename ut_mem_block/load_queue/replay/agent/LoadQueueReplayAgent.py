from toffee import Agent, driver_method
from typing import List

from ..bundle.LoadQueueReplayBundle import LoadQueueReplayBundle

class IORedirect:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    level = False
    
class IOEnq:
    valid: bool
    exceptionVec: List[bool]  # 包含多个 exceptionVec 信号
    isRVC: bool
    ftqPtr_flag: bool
    ftqPtr_value: int  # 6 bits
    ftqOffset: int  # 4 bits
    fuOpType: int  # 9 bits
    rfWen: bool
    fpWen: bool
    vpu_vstart: int  # 8 bits
    vpu_veew: int    # 2 bits
    uopIdx: int      # 7 bits
    pdest: int       # 8 bits
    robIdx_flag: bool
    robIdx_value: int  # 8 bits
    storeSetHit: bool
    waitForRobIdx_flag: bool
    waitForRobIdx_value: int  # 8 bits
    loadWaitBit: bool
    loadWaitStrict: bool
    lqIdx_flag: bool
    lqIdx_value: int  # 7 bits
    sqIdx_flag: bool
    sqIdx_value: int  # 6 bits
    vaddr: int        # 50 bits
    mask: int         # 16 bits
    tlbMiss: bool
    isvec: bool
    is128bit: bool
    elemIdx: int      # 8 bits
    alignedType: int  # 3 bits
    mbIndex: int      # 4 bits
    reg_offset: int    # 4 bits
    elemIdxInsideVd: int  # 8 bits
    vecActive: bool
    isLoadReplay: bool
    handledByMSHR: bool
    schedIndex: int   # 7 bits
    rep_info_mshr_id: int  # 4 bits
    rep_info_full_fwd: bool
    rep_info_data_inv_sq_idx_flag: bool
    rep_info_data_inv_sq_idx_value: int  # 6 bits
    rep_info_addr_inv_sq_idx_flag: bool
    rep_info_addr_inv_sq_idx_value: int  # 6 bits
    rep_info_last_beat: bool
    rep_info_causes: List[bool]  # 包含多个 cause 信号
    rep_info_tlb_id: int           # 4 bits
    rep_info_tlb_full: bool

class StoreAddrIn:
    valid: bool
    sqIdx_flag: bool
    sqIdx_value: int  # 6 bits
    miss: bool

class StoreDataIn:
    valid: bool
    sqIdx_flag: bool
    sqIdx_value: int  # 6 bits
    
class TLChannel:
    valid: bool
    mshrid: int
    
class ReadySqPtr:
    flag: bool
    value: int  # 6 bits

class IOldWbPtr:
    flag = False
    value = 0

class L2Hint:
    valid: bool
    sourceId: int  # 4 bits
    isKeyword: bool

class TlbHint:
    valid: bool
    id: int  # 4 bits
    replay_all: bool

class LoadQueueReplayAgent(Agent):
    def __init__(self, bundle: LoadQueueReplayBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
    
    @driver_method
    async def Enqueue(self, enq: List[IOEnq], redirect: IORedirect):
        for i in range(3):
            enq_i = getattr(self.bundle.io._enq, f'_{i}')
            enq_i._valid.value = enq[i].valid
            enq_i._bits._uop._exceptionVec._3.value = enq[i].exceptionVec[0]
            enq_i._bits._uop._exceptionVec._4.value = enq[i].exceptionVec[1]
            enq_i._bits._uop._exceptionVec._5.value = enq[i].exceptionVec[2]
            enq_i._bits._uop._exceptionVec._13.value = enq[i].exceptionVec[3]
            enq_i._bits._uop._exceptionVec._21.value = enq[i].exceptionVec[4]
            enq_i._bits._uop._preDecodeInfo._isRVC.value = enq[i].isRVC
            enq_i._bits._uop._ftqPtr._flag.value = enq[i].ftqPtr_flag
            enq_i._bits._uop._ftqPtr._value.value = enq[i].ftqPtr_value
            enq_i._bits._uop._ftqOffset.value = enq[i].ftqOffset
            enq_i._bits._uop._fuOpType.value = enq[i].fuOpType
            enq_i._bits._uop._rfWen.value = enq[i].rfWen
            enq_i._bits._uop._fpWen.value = enq[i].fpWen
            enq_i._bits._uop._vpu._vstart.value = enq[i].vpu_vstart
            enq_i._bits._uop._vpu._veew.value = enq[i].vpu_veew
            enq_i._bits._uop._uopIdx.value = enq[i].uopIdx
            enq_i._bits._uop._pdest.value = enq[i].pdest
            enq_i._bits._uop._robIdx._flag.value = enq[i].robIdx_flag
            enq_i._bits._uop._robIdx._value.value = enq[i].robIdx_value
            enq_i._bits._uop._storeSetHit.value = enq[i].schedIndex
            enq_i._bits._uop._waitForRobIdx._flag.value = enq[i].waitForRobIdx_flag
            enq_i._bits._uop._waitForRobIdx._value.value = enq[i].waitForRobIdx_value
            enq_i._bits._uop._loadWaitBit.value = enq[i].loadWaitBit
            enq_i._bits._uop._loadWaitStrict.value = enq[i].loadWaitStrict
            enq_i._bits._uop._lqIdx._flag.value = enq[i].lqIdx_flag
            enq_i._bits._uop._lqIdx._value.value = enq[i].lqIdx_value
            enq_i._bits._uop._sqIdx._flag.value = enq[i].sqIdx_flag
            enq_i._bits._uop._sqIdx._value.value = enq[i].sqIdx_value
            enq_i._bits._vaddr.value = enq[i].vaddr
            enq_i._bits._mask.value = enq[i].mask
            enq_i._bits._tlbMiss.value = enq[i].tlbMiss
            enq_i._bits._isvec.value = enq[i].isvec
            enq_i._bits._is128bit.value = enq[i].is128bit
            enq_i._bits._elemIdx.value = enq[i].elemIdx
            enq_i._bits._alignedType.value = enq[i].alignedType
            enq_i._bits._mbIndex.value = enq[i].mbIndex
            enq_i._bits._reg._offset.value = enq[i].reg_offset
            enq_i._bits._elemIdxInsideVd.value = enq[i].elemIdxInsideVd
            enq_i._bits._vecActive.value = enq[i].vecActive
            enq_i._bits._isLoadReplay.value = enq[i].isLoadReplay
            enq_i._bits._handledByMSHR.value = enq[i].handledByMSHR
            enq_i._bits._schedIndex.value = enq[i].schedIndex
            enq_i._bits._rep_info._mshr_id.value = enq[i].rep_info_mshr_id
            enq_i._bits._rep_info._full_fwd.value = enq[i].rep_info_full_fwd
            enq_i._bits._rep_info._data_inv_sq_idx._flag.value = enq[i].rep_info_data_inv_sq_idx_flag
            enq_i._bits._rep_info._data_inv_sq_idx._value.value = enq[i].rep_info_data_inv_sq_idx_value
            enq_i._bits._rep_info._addr_inv_sq_idx._flag.value = enq[i].rep_info_addr_inv_sq_idx_flag
            enq_i._bits._rep_info._addr_inv_sq_idx._value.value = enq[i].rep_info_addr_inv_sq_idx_value
            enq_i._bits._rep_info._last_beat.value = enq[i].rep_info_last_beat
            for j in range(11):
                getattr(enq_i._bits._rep_info._cause, f'_{j}').value = enq[i].rep_info_causes[j]
            enq_i._bits._rep_info._tlb._id.value = enq[i].rep_info_tlb_id
            enq_i._bits._rep_info._tlb._full.value = enq[i].rep_info_tlb_full
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        await self.bundle.step()
        return self.bundle.LoadQueueReplay._needEnqueue, self.bundle.LoadQueueReplay._allocated, \
            self.bundle.LoadQueueReplay._newEnqueue, self.bundle.LoadQueueReplay._freeMaskVec
        
    @driver_method
    async def dequeue(self, enq: List[IOEnq], redirect: IORedirect):
        for i in range(3):
            enq_i = getattr(self.bundle.io._enq, f'_{i}')
            enq_i._valid.value = enq[i].valid
            enq_i._bits._uop._exceptionVec._3.value = enq[i].exceptionVec[0]
            enq_i._bits._uop._exceptionVec._4.value = enq[i].exceptionVec[1]
            enq_i._bits._uop._exceptionVec._5.value = enq[i].exceptionVec[2]
            enq_i._bits._uop._exceptionVec._13.value = enq[i].exceptionVec[3]
            enq_i._bits._uop._exceptionVec._21.value = enq[i].exceptionVec[4]
            enq_i._bits._uop._preDecodeInfo._isRVC.value = enq[i].isRVC
            enq_i._bits._uop._ftqPtr._flag.value = enq[i].ftqPtr_flag
            enq_i._bits._uop._ftqPtr._value.value = enq[i].ftqPtr_value
            enq_i._bits._uop._ftqOffset.value = enq[i].ftqOffset
            enq_i._bits._uop._fuOpType.value = enq[i].fuOpType
            enq_i._bits._uop._rfWen.value = enq[i].rfWen
            enq_i._bits._uop._fpWen.value = enq[i].fpWen
            enq_i._bits._uop._vpu._vstart.value = enq[i].vpu_vstart
            enq_i._bits._uop._vpu._veew.value = enq[i].vpu_veew
            enq_i._bits._uop._uopIdx.value = enq[i].uopIdx
            enq_i._bits._uop._pdest.value = enq[i].pdest
            enq_i._bits._uop._robIdx._flag.value = enq[i].robIdx_flag
            enq_i._bits._uop._robIdx._value.value = enq[i].robIdx_value
            enq_i._bits._uop._storeSetHit.value = enq[i].schedIndex
            enq_i._bits._uop._waitForRobIdx._flag.value = enq[i].waitForRobIdx_flag
            enq_i._bits._uop._waitForRobIdx._value.value = enq[i].waitForRobIdx_value
            enq_i._bits._uop._loadWaitBit.value = enq[i].loadWaitBit
            enq_i._bits._uop._loadWaitStrict.value = enq[i].loadWaitStrict
            enq_i._bits._uop._lqIdx._flag.value = enq[i].lqIdx_flag
            enq_i._bits._uop._lqIdx._value.value = enq[i].lqIdx_value
            enq_i._bits._uop._sqIdx._flag.value = enq[i].sqIdx_flag
            enq_i._bits._uop._sqIdx._value.value = enq[i].sqIdx_value
            enq_i._bits._vaddr.value = enq[i].vaddr
            enq_i._bits._mask.value = enq[i].mask
            enq_i._bits._tlbMiss.value = enq[i].tlbMiss
            enq_i._bits._isvec.value = enq[i].isvec
            enq_i._bits._is128bit.value = enq[i].is128bit
            enq_i._bits._elemIdx.value = enq[i].elemIdx
            enq_i._bits._alignedType.value = enq[i].alignedType
            enq_i._bits._mbIndex.value = enq[i].mbIndex
            enq_i._bits._reg._offset.value = enq[i].reg_offset
            enq_i._bits._elemIdxInsideVd.value = enq[i].elemIdxInsideVd
            enq_i._bits._vecActive.value = enq[i].vecActive
            enq_i._bits._isLoadReplay.value = enq[i].isLoadReplay
            enq_i._bits._handledByMSHR.value = enq[i].handledByMSHR
            enq_i._bits._schedIndex.value = enq[i].schedIndex
            enq_i._bits._rep_info._mshr_id.value = enq[i].rep_info_mshr_id
            enq_i._bits._rep_info._full_fwd.value = enq[i].rep_info_full_fwd
            enq_i._bits._rep_info._data_inv_sq_idx._flag.value = enq[i].rep_info_data_inv_sq_idx_flag
            enq_i._bits._rep_info._data_inv_sq_idx._value.value = enq[i].rep_info_data_inv_sq_idx_value
            enq_i._bits._rep_info._addr_inv_sq_idx._flag.value = enq[i].rep_info_addr_inv_sq_idx_flag
            enq_i._bits._rep_info._addr_inv_sq_idx._value.value = enq[i].rep_info_addr_inv_sq_idx_value
            enq_i._bits._rep_info._last_beat.value = enq[i].rep_info_last_beat
            for j in range(11):
                getattr(enq_i._bits._rep_info._cause, f'_{j}').value = enq[i].rep_info_causes[j]
            enq_i._bits._rep_info._tlb._id.value = enq[i].rep_info_tlb_id
            enq_i._bits._rep_info._tlb._full.value = enq[i].rep_info_tlb_full
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        await self.bundle.step()
        return self.bundle.LoadQueueReplay._allocated, self.bundle.LoadQueueReplay._freeMaskVec
    
    @driver_method
    async def Update(self, stDataReadySqPtr: ReadySqPtr, stAddrReadySqPtr: ReadySqPtr, 
                      sqEmpty: bool, storeAddrIn: List[StoreAddrIn], storeDataIn: List[StoreDataIn], 
                      stAddrReadyVec: List[bool], stDataReadyVec: List[bool], tlb_hint: TlbHint, tl_channel: TLChannel, rarFull: bool, 
                     ldWbPtr: IOldWbPtr, rawFull: bool, enq: List[IOEnq]):
        self.bundle.io._stDataReadySqPtr._flag.value = stDataReadySqPtr.flag
        self.bundle.io._stDataReadySqPtr._value.value = stDataReadySqPtr.value
        self.bundle.io._sqEmpty.value = sqEmpty
        for i in range(56):
            getattr(self.bundle.io._stAddrReadyVec, f"_{i}").value= stAddrReadyVec[i]
            getattr(self.bundle.io._stDataReadyVec, f"_{i}").value= stDataReadyVec[i]
        for i in range(2):
            storeAddrIn_i = getattr(self.bundle.io._storeAddrIn, f'_{i}')
            storeAddrIn_i._valid.value = storeAddrIn[i].valid
            storeAddrIn_i._bits._uop_sqIdx._flag.value = storeAddrIn[i].sqIdx_flag
            storeAddrIn_i._bits._uop_sqIdx._value.value = storeAddrIn[i].sqIdx_value
            storeAddrIn_i._bits._miss.value = storeAddrIn[i].miss
            storeDataIn_i = getattr(self.bundle.io._storeDataIn, f'_{i}')
            storeDataIn_i._valid.value = storeDataIn[i].valid
            storeDataIn_i._bits_uop_sqIdx._flag.value = storeDataIn[i].sqIdx_flag
            storeDataIn_i._bits_uop_sqIdx._value.value = storeDataIn[i].sqIdx_value
        self.bundle.io.stAddrReadySqPtr._flag.value = stAddrReadySqPtr.flag
        self.bundle.io.stAddrReadySqPtr._value.value = stAddrReadySqPtr.value
        self.bundle.io._tlb_hint_resp._valid.value = tlb_hint.valid
        self.bundle.io._tlb_hint_resp._bits._id.value = tlb_hint.id
        self.bundle.io._tlb_hint_resp._bits._replay_all.value = tlb_hint.replay_all
        self.bundle.io._tl_d_channel._valid.value = tl_channel.valid
        self.bundle.io._tl_d_channel._mshrid.value = tl_channel.mshrid
        self.bundle.io._rarFull.value = rarFull
        self.bundle.io._rawFull.value = rawFull
        self.bundle.io._ldWbPtr._flag.value = ldWbPtr.flag
        self.bundle.io._ldWbPtr._value.value = ldWbPtr.value
        for i in range(3):
            enq_i = getattr(self.bundle.io._enq, f'_{i}')
            enq_i._valid.value = enq[i].valid
            enq_i._bits._uop._exceptionVec._3.value = enq[i].exceptionVec[0]
            enq_i._bits._uop._exceptionVec._4.value = enq[i].exceptionVec[1]
            enq_i._bits._uop._exceptionVec._5.value = enq[i].exceptionVec[2]
            enq_i._bits._uop._exceptionVec._13.value = enq[i].exceptionVec[3]
            enq_i._bits._uop._exceptionVec._21.value = enq[i].exceptionVec[4]
            enq_i._bits._uop._preDecodeInfo._isRVC.value = enq[i].isRVC
            enq_i._bits._uop._ftqPtr._flag.value = enq[i].ftqPtr_flag
            enq_i._bits._uop._ftqPtr._value.value = enq[i].ftqPtr_value
            enq_i._bits._uop._ftqOffset.value = enq[i].ftqOffset
            enq_i._bits._uop._fuOpType.value = enq[i].fuOpType
            enq_i._bits._uop._rfWen.value = enq[i].rfWen
            enq_i._bits._uop._fpWen.value = enq[i].fpWen
            enq_i._bits._uop._vpu._vstart.value = enq[i].vpu_vstart
            enq_i._bits._uop._vpu._veew.value = enq[i].vpu_veew
            enq_i._bits._uop._uopIdx.value = enq[i].uopIdx
            enq_i._bits._uop._pdest.value = enq[i].pdest
            enq_i._bits._uop._robIdx._flag.value = enq[i].robIdx_flag
            enq_i._bits._uop._robIdx._value.value = enq[i].robIdx_value
            enq_i._bits._uop._storeSetHit.value = enq[i].schedIndex
            enq_i._bits._uop._waitForRobIdx._flag.value = enq[i].waitForRobIdx_flag
            enq_i._bits._uop._waitForRobIdx._value.value = enq[i].waitForRobIdx_value
            enq_i._bits._uop._loadWaitBit.value = enq[i].loadWaitBit
            enq_i._bits._uop._loadWaitStrict.value = enq[i].loadWaitStrict
            enq_i._bits._uop._lqIdx._flag.value = enq[i].lqIdx_flag
            enq_i._bits._uop._lqIdx._value.value = enq[i].lqIdx_value
            enq_i._bits._uop._sqIdx._flag.value = enq[i].sqIdx_flag
            enq_i._bits._uop._sqIdx._value.value = enq[i].sqIdx_value
            enq_i._bits._vaddr.value = enq[i].vaddr
            enq_i._bits._mask.value = enq[i].mask
            enq_i._bits._tlbMiss.value = enq[i].tlbMiss
            enq_i._bits._isvec.value = enq[i].isvec
            enq_i._bits._is128bit.value = enq[i].is128bit
            enq_i._bits._elemIdx.value = enq[i].elemIdx
            enq_i._bits._alignedType.value = enq[i].alignedType
            enq_i._bits._mbIndex.value = enq[i].mbIndex
            enq_i._bits._reg._offset.value = enq[i].reg_offset
            enq_i._bits._elemIdxInsideVd.value = enq[i].elemIdxInsideVd
            enq_i._bits._vecActive.value = enq[i].vecActive
            enq_i._bits._isLoadReplay.value = enq[i].isLoadReplay
            enq_i._bits._handledByMSHR.value = enq[i].handledByMSHR
            enq_i._bits._schedIndex.value = enq[i].schedIndex
            enq_i._bits._rep_info._mshr_id.value = enq[i].rep_info_mshr_id
            enq_i._bits._rep_info._full_fwd.value = enq[i].rep_info_full_fwd
            enq_i._bits._rep_info._data_inv_sq_idx._flag.value = enq[i].rep_info_data_inv_sq_idx_flag
            enq_i._bits._rep_info._data_inv_sq_idx._value.value = enq[i].rep_info_data_inv_sq_idx_value
            enq_i._bits._rep_info._addr_inv_sq_idx._flag.value = enq[i].rep_info_addr_inv_sq_idx_flag
            enq_i._bits._rep_info._addr_inv_sq_idx._value.value = enq[i].rep_info_addr_inv_sq_idx_value
            enq_i._bits._rep_info._last_beat.value = enq[i].rep_info_last_beat
            for j in range(11):
                getattr(enq_i._bits._rep_info._cause, f'_{j}').value = enq[i].rep_info_causes[j]
            enq_i._bits._rep_info._tlb._id.value = enq[i].rep_info_tlb_id
            enq_i._bits._rep_info._tlb._full.value = enq[i].rep_info_tlb_full
        await self.bundle.step()
        return self.bundle.LoadQueueReplay._blocking
    
    @driver_method
    async def replay(self, enq: IOEnq, replay_ready: List[bool], l2_hint: L2Hint, redirect: IORedirect):
        self.bundle.io._l2_hint._valid.value = l2_hint.valid
        self.bundle.io._l2_hint._bits._sourceId = l2_hint.sourceId
        self.bundle.io._l2_hint._bits._isKeyword = l2_hint.isKeyword
        for i in range(3):
            enq_i = getattr(self.bundle.io._enq, f'_{i}')
            getattr(self.bundle.io._replay, f"_{i}")._ready.value = replay_ready[i]
            enq_i._valid.value = enq[i].valid
            enq_i._bits._uop._exceptionVec._3.value = enq[i].exceptionVec[0]
            enq_i._bits._uop._exceptionVec._4.value = enq[i].exceptionVec[1]
            enq_i._bits._uop._exceptionVec._5.value = enq[i].exceptionVec[2]
            enq_i._bits._uop._exceptionVec._13.value = enq[i].exceptionVec[3]
            enq_i._bits._uop._exceptionVec._21.value = enq[i].exceptionVec[4]
            enq_i._bits._uop._preDecodeInfo._isRVC.value = enq[i].isRVC
            enq_i._bits._uop._ftqPtr._flag.value = enq[i].ftqPtr_flag
            enq_i._bits._uop._ftqPtr._value.value = enq[i].ftqPtr_value
            enq_i._bits._uop._ftqOffset.value = enq[i].ftqOffset
            enq_i._bits._uop._fuOpType.value = enq[i].fuOpType
            enq_i._bits._uop._rfWen.value = enq[i].rfWen
            enq_i._bits._uop._fpWen.value = enq[i].fpWen
            enq_i._bits._uop._vpu._vstart.value = enq[i].vpu_vstart
            enq_i._bits._uop._vpu._veew.value = enq[i].vpu_veew
            enq_i._bits._uop._uopIdx.value = enq[i].uopIdx
            enq_i._bits._uop._pdest.value = enq[i].pdest
            enq_i._bits._uop._robIdx._flag.value = enq[i].robIdx_flag
            enq_i._bits._uop._robIdx._value.value = enq[i].robIdx_value
            enq_i._bits._uop._storeSetHit.value = enq[i].schedIndex
            enq_i._bits._uop._waitForRobIdx._flag.value = enq[i].waitForRobIdx_flag
            enq_i._bits._uop._waitForRobIdx._value.value = enq[i].waitForRobIdx_value
            enq_i._bits._uop._loadWaitBit.value = enq[i].loadWaitBit
            enq_i._bits._uop._loadWaitStrict.value = enq[i].loadWaitStrict
            enq_i._bits._uop._lqIdx._flag.value = enq[i].lqIdx_flag
            enq_i._bits._uop._lqIdx._value.value = enq[i].lqIdx_value
            enq_i._bits._uop._sqIdx._flag.value = enq[i].sqIdx_flag
            enq_i._bits._uop._sqIdx._value.value = enq[i].sqIdx_value
            enq_i._bits._vaddr.value = enq[i].vaddr
            enq_i._bits._mask.value = enq[i].mask
            enq_i._bits._tlbMiss.value = enq[i].tlbMiss
            enq_i._bits._isvec.value = enq[i].isvec
            enq_i._bits._is128bit.value = enq[i].is128bit
            enq_i._bits._elemIdx.value = enq[i].elemIdx
            enq_i._bits._alignedType.value = enq[i].alignedType
            enq_i._bits._mbIndex.value = enq[i].mbIndex
            enq_i._bits._reg._offset.value = enq[i].reg_offset
            enq_i._bits._elemIdxInsideVd.value = enq[i].elemIdxInsideVd
            enq_i._bits._vecActive.value = enq[i].vecActive
            enq_i._bits._isLoadReplay.value = enq[i].isLoadReplay
            enq_i._bits._handledByMSHR.value = enq[i].handledByMSHR
            enq_i._bits._schedIndex.value = enq[i].schedIndex
            enq_i._bits._rep_info._mshr_id.value = enq[i].rep_info_mshr_id
            enq_i._bits._rep_info._full_fwd.value = enq[i].rep_info_full_fwd
            enq_i._bits._rep_info._data_inv_sq_idx._flag.value = enq[i].rep_info_data_inv_sq_idx_flag
            enq_i._bits._rep_info._data_inv_sq_idx._value.value = enq[i].rep_info_data_inv_sq_idx_value
            enq_i._bits._rep_info._addr_inv_sq_idx._flag.value = enq[i].rep_info_addr_inv_sq_idx_flag
            enq_i._bits._rep_info._addr_inv_sq_idx._value.value = enq[i].rep_info_addr_inv_sq_idx_value
            enq_i._bits._rep_info._last_beat.value = enq[i].rep_info_last_beat
            for j in range(11):
                getattr(enq_i._bits._rep_info._cause, f'_{j}').value = enq[i].rep_info_causes[j]
            enq_i._bits._rep_info._tlb._id.value = enq[i].rep_info_tlb_id
            enq_i._bits._rep_info._tlb._full.value = enq[i].rep_info_tlb_full
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        await self.bundle.step()
        return self.bundle.LoadQueueReplay._scheduled
    
    