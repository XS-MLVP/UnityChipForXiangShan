__all__ = [name for name in locals()]

class IORedirect:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, level=False):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value
        self.level = level
    
class VecCommit:
    def __init__(self, valid=False, robidx_flag=False, robidx_value=0, uopidx=0):
        self.valid = valid
        self.robidx_flag = robidx_flag
        self.robidx_value = robidx_value
        self.uopidx = uopidx
    
class EnqReq:
    def __init__(self, valid=False, fuType=0, uopIdx=0, robIdx_flag=False, 
                 robIdx_value=0, lqIdx_flag=False, lqIdx_value=0, numLsElem=0):
        self.valid = valid
        self.fuType = fuType
        self.uopIdx = uopIdx
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value
        self.lqIdx_flag = lqIdx_flag
        self.lqIdx_value = lqIdx_value
        self.numLsElem = numLsElem
    
class LdIn:
    def __init__(self, valid=False, uop_lqIdx_value=0, isvec=False, updateAddrValid=False, rep_info_cause=None):
        self.valid = valid
        self.uop_lqIdx_value = uop_lqIdx_value
        self.isvec = isvec
        self.updateAddrValid = updateAddrValid
        self.rep_info_cause = rep_info_cause if rep_info_cause is not None else []