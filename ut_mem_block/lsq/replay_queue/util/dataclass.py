__all__ = [name for name in locals()]

class IORedirect:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, level=False):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value
        self.level = level

class IOEnq:
    def __init__(self, valid=False, exceptionVec=None, isRVC=False, ftqPtr_flag=False, ftqPtr_value=0, ftqOffset=0,
                 fuOpType=0, rfWen=False, fpWen=False, vpu_vstart=0, vpu_veew=0, uopIdx=0, pdest=0, robIdx_flag=False,
                 robIdx_value=0, storeSetHit=False, waitForRobIdx_flag=False, waitForRobIdx_value=0, loadWaitBit=False,
                 loadWaitStrict=False, lqIdx_flag=False, lqIdx_value=0, sqIdx_flag=False, sqIdx_value=0, vaddr=0, mask=0, 
                 tlbMiss=False, isvec=False, is128bit=False, elemIdx=0, alignedType=0, mbIndex=0, reg_offset=0, elemIdxInsideVd=0,
                 vecActive=False, isLoadReplay=False, handledByMSHR=False, schedIndex=0, rep_info_mshr_id=0, rep_info_full_fwd=False,
                 rep_info_data_inv_sq_idx_flag=False, rep_info_data_inv_sq_idx_value=0, rep_info_addr_inv_sq_idx_flag=False,
                 rep_info_addr_inv_sq_idx_value=0, rep_info_last_beat=False, rep_info_causes=None, rep_info_tlb_id=0, rep_info_tlb_full=False):
        self.valid = valid
        self.exceptionVec = exceptionVec if exceptionVec is not None else [False] * 8  # 默认 8 个信号
        self.isRVC = isRVC
        self.ftqPtr_flag = ftqPtr_flag
        self.ftqPtr_value = ftqPtr_value
        self.ftqOffset = ftqOffset
        self.fuOpType = fuOpType
        self.rfWen = rfWen
        self.fpWen = fpWen
        self.vpu_vstart = vpu_vstart
        self.vpu_veew = vpu_veew
        self.uopIdx = uopIdx
        self.pdest = pdest
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value
        self.storeSetHit = storeSetHit
        self.waitForRobIdx_flag = waitForRobIdx_flag
        self.waitForRobIdx_value = waitForRobIdx_value
        self.loadWaitBit = loadWaitBit
        self.loadWaitStrict = loadWaitStrict
        self.lqIdx_flag = lqIdx_flag
        self.lqIdx_value = lqIdx_value
        self.sqIdx_flag = sqIdx_flag
        self.sqIdx_value = sqIdx_value
        self.vaddr = vaddr
        self.mask = mask
        self.tlbMiss = tlbMiss
        self.isvec = isvec
        self.is128bit = is128bit
        self.elemIdx = elemIdx
        self.alignedType = alignedType
        self.mbIndex = mbIndex
        self.reg_offset = reg_offset
        self.elemIdxInsideVd = elemIdxInsideVd
        self.vecActive = vecActive
        self.isLoadReplay = isLoadReplay
        self.handledByMSHR = handledByMSHR
        self.schedIndex = schedIndex
        self.rep_info_mshr_id = rep_info_mshr_id
        self.rep_info_full_fwd = rep_info_full_fwd
        self.rep_info_data_inv_sq_idx_flag = rep_info_data_inv_sq_idx_flag
        self.rep_info_data_inv_sq_idx_value = rep_info_data_inv_sq_idx_value
        self.rep_info_addr_inv_sq_idx_flag = rep_info_addr_inv_sq_idx_flag
        self.rep_info_addr_inv_sq_idx_value = rep_info_addr_inv_sq_idx_value
        self.rep_info_last_beat = rep_info_last_beat
        self.rep_info_causes = rep_info_causes if rep_info_causes is not None else [False] * 11
        self.rep_info_tlb_id = rep_info_tlb_id
        self.rep_info_tlb_full = rep_info_tlb_full

class StoreAddrIn:
    def __init__(self, 
                 valid=False, 
                 sqIdx_flag=False, 
                 sqIdx_value=0,  # 6 bits
                 miss=False):
        self.valid = valid
        self.sqIdx_flag = sqIdx_flag
        self.sqIdx_value = sqIdx_value
        self.miss = miss

class StoreDataIn:
    def __init__(self, valid=False, sqIdx_flag=False, sqIdx_value=0):
        self.valid = valid
        self.sqIdx_flag = sqIdx_flag
        self.sqIdx_value = sqIdx_value
    
class TLChannel:
    def __init__(self, valid=False, mshrid=0):
        self.valid = valid
        self.mshrid = mshrid
    
class ReadySqPtr:
    def __init__(self, flag=False, value=0):
        self.flag = flag
        self.value = value

class IOldWbPtr:
    def __init__(self, flag=False, value=0):
        self.flag = flag
        self.value = value

class L2Hint:
    def __init__(self, valid=False, sourceId=0, isKeyword=False):
        self.valid = valid
        self.sourceId = sourceId
        self.isKeyword = isKeyword

class TlbHint:
    def __init__(self, valid=False, id=0, replay_all=False):
        self.valid = valid
        self.id = id
        self.replay_all = replay_all