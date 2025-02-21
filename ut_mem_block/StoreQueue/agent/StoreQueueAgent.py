from toffee import Agent, driver_method
from typing import List

from ..bundle.StoreQueueBundle import StoreQueueBundle

class EnqReq:
    valid = False
    fuType = 0
    fuOpType = 0
    uopIdx = 0
    lastUop = False
    robIdx_flag = False
    robIdx_value = 0
    sqIdx_flag = False
    sqIdx_value = 0
    numLsElem = 0
    
class IORedirect:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    level = False
    
class VecFeedback:
    valid = False
    robidx_flag = False
    robidx_value = 0  # 8 bits
    uopidx = 0        # 7 bits
    vaddr = 0         # 64 bits
    vaNeedExt = False
    gpaddr = 0        # 50 bits
    isForVSnonLeafPTE = False
    feedback_0 = False
    feedback_1 = False
    exceptionVec_3 = False
    exceptionVec_6 = False
    exceptionVec_7 = False
    exceptionVec_15 = False
    exceptionVec_23 = False
    
class StoreAddrIn:
    valid = False
    uop_exceptionVec_3 = False
    uop_exceptionVec_6 = False
    uop_exceptionVec_7 = False
    uop_exceptionVec_15 = False
    uop_exceptionVec_23 = False
    uop_fuOpType = 0  # 9 bits
    uop_uopIdx = 0     # 7 bits
    uop_robIdx_flag = False
    uop_robIdx_value = 0  # 8 bits
    uop_sqIdx_value = 0    # 6 bits
    vaddr = 0              # 50 bits
    fullva = 0             # 64 bits
    vaNeedExt = False
    isHyper = False
    paddr = 0              # 48 bits
    gpaddr = 0             # 64 bits
    isForVSnonLeafPTE = False
    mask = 0               # 16 bits
    wlineflag = False
    miss = False
    nc = False
    isFrmMisAlignBuf = False
    isvec = False
    isMisalign = False
    misalignWith16Byte = False
    updateAddrValid = False
    
class StoreAddrInRe:
    uop_exceptionVec_3 = False
    uop_exceptionVec_6 = False
    uop_exceptionVec_15 = False
    uop_exceptionVec_23 = False
    uop_uopIdx = 0  # 7 bits
    uop_robIdx_flag = False
    uop_robIdx_value = 0  # 8 bits
    fullva = 0             # 64 bits
    vaNeedExt = False
    isHyper = False
    gpaddr = 0             # 64 bits
    isForVSnonLeafPTE = False
    af = False
    mmio = False
    memBackTypeMM = False
    hasException = False
    isvec = False
    updateAddrValid = False
    
class StoreDataIn:
    valid = False
    bits_uop_fuType = 0  # 35 bits
    bits_uop_fuOpType = 0  # 9 bits
    bits_uop_sqIdx_value = 0  # 6 bits
    bits_data = 0  # 128 bits
    
class Forward:
    vaddr = 0            # 50 bits
    paddr = 0            # 48 bits
    mask = 0             # 16 bits
    uop_waitForRobIdx_flag = False
    uop_waitForRobIdx_value = 0  # 8 bits
    uop_loadWaitBit = False
    uop_loadWaitStrict = False
    uop_sqIdx_flag = False
    uop_sqIdx_value = 0  # 6 bits
    valid = False
    forwardMask = []  # 16 outputs
    forwardData = []  # 16 outputs
    sqIdx_flag = False
    dataInvalid = False
    matchInvalid = False
    addrInvalid = False
    sqIdxMask = 0        # 56 bits
    dataInvalidSqIdx_flag = False
    dataInvalidSqIdx_value = 0  # 6 bits
    addrInvalidSqIdx_flag = False
    addrInvalidSqIdx_value = 0  # 6 bits
    
class IORob:
    rob_scommit = 0        # 4 bits
    pendingst = False
    pendingPtr_flag = False
    pendingPtr_value = 0    # 8 bits

class Uncache:
    req_ready = False
    req_valid = False
    req_bits_addr = 0          # 48 bits
    req_bits_vaddr = 0         # 50 bits
    req_bits_data = 0          # 64 bits
    req_bits_mask = 0          # 8 bits
    req_bits_id = 0            # 7 bits
    req_bits_nc = False
    req_bits_memBackTypeMM = False
    resp_valid = False
    resp_bits_id = 0           # 7 bits
    resp_bits_nc = False
    resp_bits_nderr = False
    
class MaControlInput:
    crossPageWithHit = False
    crossPageCanDeq = False
    paddr = 0  # 48 bits
    withSameUop = False
    
class StoreMaskIn:
    valid = False
    sqIdx_value = 0
    mask = 0

class StoreQueueAgent(Agent):
    def __init__(self, bundle: StoreQueueBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
        
    @driver_method
    async def update(self, enq: List[EnqReq], brqRedirect: IORedirect):
        for i in range(6):
            enq_i = getattr(self.bundle.io._enq_req, f'_{i}')
            enq_i._valid.value = enq[i].valid
            enq_i._bits._fuType.value = enq[i].fuType
            enq_i._bits._fuOpType.value = enq[i].fuOpType
            enq_i._bits._uopIdx.value = enq[i].uopIdx
            enq_i._bits._lastUop.value = enq[i].lastUop
            enq_i._bits._robIdx._flag.value = enq[i].robIdx_flag
            enq_i._bits._robIdx._value.value = enq[i].robIdx_value
            enq_i._bits._sqIdx._flag.value = enq[i].sqIdx_flag
            enq_i._bits._sqIdx._value.value = enq[i].sqIdx_value
            enq_i._bits._numLsElem.value = enq[i].numLsElem
        self.bundle.io._brqRedirect._valid.value = brqRedirect.valid
        self.bundle.io._brqRedirect._bits._robIdx._flag.value = brqRedirect.robIdx_flag
        self.bundle.io._brqRedirect._bits._robIdx._value.value = brqRedirect.robIdx_value
        self.bundle.io._brqRedirect._bits._level.value = brqRedirect.level
        await self.bundle.step()
        stAddrReadyVec = []
        stDataReadyVec = []
        for i in range(56):
            stAddrReadyVec.append(getattr(self.bundle.io._stAddrReadyVec, f"_{i}").value)
            stDataReadyVec.append(getattr(self.bundle.io._stDataReadyVec, f"_{i}").value)
        return stAddrReadyVec, self.bundle.io._stAddrReadySqPtr, \
            stDataReadyVec, self.bundle.io._stDataReadySqPtr, \
            self.bundle.io._stIssuePtr, self.bundle.StoreQueue._deqPtrExt._0, \
            self.bundle.io._sqCancelCnt, self.bundle.io._sqEmpty, \
            self.bundle.io._force_write
            
    
    @driver_method
    async def writeback(self, storeAddrIn: List[StoreAddrIn], storeAddrInRe: List[StoreAddrInRe], 
                        storeDataIn: List[StoreDataIn], storeMaskIn: List[StoreMaskIn]):
        for i in range(2):
            storeMaskIn_i = getattr(self.bundle.io._storeMaskIn, f'_{i}')
            storeMaskIn_i._valid.value = storeMaskIn[i].valid
            storeMaskIn_i._bits._sqIdx_value.value = storeMaskIn[i].sqIdx_value
            storeMaskIn_i._bits._mask.value = storeMaskIn[i].mask
            storeDataIn_i = getattr(self.bundle.io._storeDataIn, f'_{i}')
            storeDataIn_i._valid.value = storeDataIn[i].valid
            storeDataIn_i._bits._uop._fuType.value = storeDataIn[i].bits_uop_fuType
            storeDataIn_i._bits._uop._fuOpType.value = storeDataIn[i].bits_uop_fuOpType
            storeDataIn_i._bits._uop._sqIdx_value.value = storeDataIn[i].bits_uop_sqIdx_value
            storeDataIn_i._bits._data.value = storeDataIn[i].bits_data
            storeAddrInRe_i = getattr(self.bundle.io._storeAddrInRe, f'_{i}')
            storeAddrInRe_i._uop._exceptionVec._3.value = storeAddrInRe[i].uop_exceptionVec_3
            storeAddrInRe_i._uop._exceptionVec._6.value = storeAddrInRe[i].uop_exceptionVec_6
            storeAddrInRe_i._uop._exceptionVec._15.value = storeAddrInRe[i].uop_exceptionVec_15
            storeAddrInRe_i._uop._exceptionVec._23.value = storeAddrInRe[i].uop_exceptionVec_23
            storeAddrInRe_i._uop._uopIdx.value = storeAddrInRe[i].uop_uopIdx
            storeAddrInRe_i._uop._robIdx._flag.value = storeAddrInRe[i].uop_robIdx_flag
            storeAddrInRe_i._uop._robIdx._value.value = storeAddrInRe[i].uop_robIdx_value
            storeAddrInRe_i._fullva.value = storeAddrInRe[i].fullva
            storeAddrInRe_i._vaNeedExt.value = storeAddrInRe[i].vaNeedExt
            storeAddrInRe_i._isHyper.value = storeAddrInRe[i].isHyper
            storeAddrInRe_i._gpaddr.value = storeAddrInRe[i].gpaddr
            storeAddrInRe_i._isForVSnonLeafPTE.value = storeAddrInRe[i].isForVSnonLeafPTE
            storeAddrInRe_i._af.value = storeAddrInRe[i].af
            storeAddrInRe_i._mmio.value = storeAddrInRe[i].mmio
            storeAddrInRe_i._memBackTypeMM.value = storeAddrInRe[i].memBackTypeMM
            storeAddrInRe_i._hasException.value = storeAddrInRe[i].hasException
            storeAddrInRe_i._isvec.value = storeAddrInRe[i].isvec
            storeAddrInRe_i._updateAddrValid.value = storeAddrInRe[i].updateAddrValid
            storeAddrIn_i = getattr(self.bundle.io._storeAddrIn, f'_{i}')
            storeAddrIn_i._valid.value = storeAddrIn[i].valid
            storeAddrIn_i._bits._uop._exceptionVec._3.value = storeAddrIn[i].uop_exceptionVec_3
            storeAddrIn_i._bits._uop._exceptionVec._6.value = storeAddrIn[i].uop_exceptionVec_6
            storeAddrIn_i._bits._uop._exceptionVec._7.value = storeAddrIn[i].uop_exceptionVec_7
            storeAddrIn_i._bits._uop._exceptionVec._15.value = storeAddrIn[i].uop_exceptionVec_15
            storeAddrIn_i._bits._uop._exceptionVec._23.value = storeAddrIn[i].uop_exceptionVec_23
            storeAddrIn_i._bits._uop._fuOpType.value = storeAddrIn[i].uop_fuOpType
            storeAddrIn_i._bits._uop._uopIdx.value = storeAddrIn[i].uop_uopIdx
            storeAddrIn_i._bits._uop._robIdx._flag.value = storeAddrIn[i].uop_robIdx_flag
            storeAddrIn_i._bits._uop._robIdx._value.value = storeAddrIn[i].uop_robIdx_value
            storeAddrIn_i._bits._uop._sqIdx._value.value = storeAddrIn[i].uop_sqIdx_value
            storeAddrIn_i._bits._vaddr.value = storeAddrIn[i].vaddr
            storeAddrIn_i._bits._fullva.value = storeAddrIn[i].fullva
            storeAddrIn_i._bits._vaNeedExt.value = storeAddrIn[i].vaNeedExt
            storeAddrIn_i._bits._isHyper.value = storeAddrIn[i].isHyper
            storeAddrIn_i._bits._paddr.value = storeAddrIn[i].paddr
            storeAddrIn_i._bits._gpaddr.value = storeAddrIn[i].gpaddr
            storeAddrIn_i._bits._isForVSnonLeafPTE.value = storeAddrIn[i].isForVSnonLeafPTE
            storeAddrIn_i._bits._mask.value = storeAddrIn[i].mask
            storeAddrIn_i._bits._wlineflag.value = storeAddrIn[i].wlineflag
            storeAddrIn_i._bits._miss.value = storeAddrIn[i].miss
            storeAddrIn_i._bits._nc.value = storeAddrIn[i].nc
            storeAddrIn_i._bits._isFrmMisAlignBuf.value = storeAddrIn[i].isFrmMisAlignBuf
            storeAddrIn_i._bits._isvec.value = storeAddrIn[i].isvec
            storeAddrIn_i._bits._isMisalign.value = storeAddrIn[i].isMisalign
            storeAddrIn_i._bits._misalignWith16Byte.value = storeAddrIn[i].misalignWith16Byte
            storeAddrIn_i._bits._updateAddrValid.value = storeAddrIn[i].updateAddrValid
        await self.bundle.step()
        return self.bundle.StoreQueue
    
    @driver_method
    async def forwardquery(self, forward: List[Forward]):
        for i in range(2):
            forward_i = getattr(self.bundle.io._forward, f'_{i}')
            forward_i._vaddr.value = forward[i].vaddr
            forward_i._paddr.value = forward[i].paddr
            forward_i._mask.value = forward[i].mask
            forward_i._uop._waitForRobIdx._flag.value = forward[i].uop_waitForRobIdx_flag
            forward_i._uop._waitForRobIdx._value.value = forward[i].uop_waitForRobIdx_value
            forward_i._uop._loadWaitBit.value = forward[i].uop_loadWaitBit
            forward_i._uop._loadWaitStrict.value = forward[i].uop_loadWaitStrict
            forward_i._uop._sqIdx._flag.value = forward[i].uop_sqIdx_flag
            forward_i._uop._sqIdx._value.value = forward[i].uop_sqIdx_value
            forward_i._valid.value = forward[i].valid
            forward_i._sqIdx_flag.value = forward[i].sqIdx_flag
            forward_i._sqIdxMask.value = forward[i].sqIdxMask
        await self.bundle.step()
        return self.bundle.io._forward
    
    @driver_method
    async def mmio(self, uncache: Uncache, rob: IORob, cmoOpResp_valid: bool, mmioStout_ready: bool):
        self.bundle.io._uncache._req._ready.value = uncache.req_ready
        self.bundle.io._uncache._resp._valid.value = uncache.resp_valid
        self.bundle.io._uncache._resp._bits._nc.value = uncache.resp_bits_nc
        self.bundle.io._uncache._resp._bits._id.value = uncache.resp_bits_id
        self.bundle.io._uncache._resp._bits._nderr.value = uncache.resp_bits_nderr
        self.bundle.io._rob._scommit.value = rob.rob_scommit
        self.bundle.io._rob._pendingst.value = rob.pendingst
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        self.bundle.io._cmoOpResp._valid.value = cmoOpResp_valid
        self.bundle.io._mmioStout._ready.value = mmioStout_ready
        await self.bundle.step()
        return self.bundle.StoreQueue._mmioState
    
    @driver_method
    async def ncstore(self, uncacheOutstanding: bool, uncache: Uncache, cmoOpReq_ready:bool, flushSbuffer_empty: bool, mmioStout_ready: bool):
        self.bundle.io._uncache._req._ready.value = uncache.req_ready
        self.bundle.io._uncache._resp._valid.value = uncache.resp_valid
        self.bundle.io._uncache._resp._bits._nc.value = uncache.resp_bits_nc
        self.bundle.io._uncache._resp._bits._id.value = uncache.resp_bits_id
        self.bundle.io._uncache._resp._bits._nderr.value = uncache.resp_bits_nderr
        self.bundle.io._uncacheOutstanding.value = uncacheOutstanding
        self.bundle.io._cmoOpReq._ready.value = cmoOpReq_ready
        self.bundle.io._mmioStout._ready.value = mmioStout_ready
        self.bundle.io._flushSbuffer._empty.value = flushSbuffer_empty
        await self.bundle.step()
        return self.bundle.StoreQueue._ncState
    
    @driver_method
    async def commit(self, rob: IORob, maControl: MaControlInput, sbuffer_ready: List[int]):
        self.bundle.io._rob._scommit.value = rob.rob_scommit
        self.bundle.io._rob._pendingst.value = rob.pendingst
        self.bundle.io._rob._pendingPtr._flag.value = rob.pendingPtr_flag
        self.bundle.io._rob._pendingPtr._value.value = rob.pendingPtr_value
        self.bundle.io._maControl._toStoreQueue._crossPageWithHit.value = maControl.crossPageWithHit
        self.bundle.io._maControl._toStoreQueue._crossPageCanDeq.value = maControl.crossPageCanDeq
        self.bundle.io._maControl._toStoreQueue._paddr.value = maControl.paddr
        self.bundle.io._maControl._toStoreQueue._withSameUop.value = maControl.withSameUop
        for j in range(2):
                getattr(self.bundle.io._sbuffer, f'_{j}')._ready.value = sbuffer_ready[j]
        await self.bundle.step()
        return self.bundle.StoreQueue._committed
    
    @driver_method
    async def predictionfalse(self, brqRedirect: IORedirect):
        self.bundle.io._brqRedirect._valid.value = brqRedirect.valid
        self.bundle.io._brqRedirect._bits._robIdx._flag.value = brqRedirect.robIdx_flag
        self.bundle.io._brqRedirect._bits._robIdx._value.value = brqRedirect.robIdx_value
        self.bundle.io._brqRedirect._bits._level.value = brqRedirect.level
        await self.bundle.step()
        allocated = []
        for i in range(56):
            allocated.append(getattr(self.bundle.io._allocated, f"_{i}").value)
        return allocated
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    