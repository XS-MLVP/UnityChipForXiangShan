__all__ = [name for name in locals()]

class IORedirect:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    level = False
    
class VecCommit:
    valid = False
    robidx_flag = False
    robidx_value = 0
    uopidx = 0
    
class EnqReq:
    valid = False
    fuType = 0
    uopIdx = 0
    robIdx_flag = False
    robIdx_value = 0
    lqIdx_flag = False
    lqIdx_value = 0
    numLsElem = 0
    
class LdIn:
    valid = False
    uop_lqIdx_value = 0
    isvec = False
    updateAddrValid = False
    rep_info_cause = []