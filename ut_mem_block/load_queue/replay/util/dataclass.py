__all__ = [name for name in locals()]

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