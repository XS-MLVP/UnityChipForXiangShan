__all__ = [name for name in locals()]

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