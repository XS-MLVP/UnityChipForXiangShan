__all__ = [name for name in locals()]

class IORedirect:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, level=False):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value  # 8 bits
        self.level = level

class IOQuery:
    def __init__(self, valid=False, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=False, 
                 uop_ftqPtr_value=0, uop_ftqOffset=0, uop_robIdx_flag=False, uop_robIdx_value=0, 
                 uop_sqIdx_flag=False, uop_sqIdx_value=0, mask=0, bits_paddr=0, datavalid=False, revoke=False):
        self.valid = valid
        self.uop_preDecodeInfo_isRVC = uop_preDecodeInfo_isRVC
        self.uop_ftqPtr_flag = uop_ftqPtr_flag
        self.uop_ftqPtr_value = uop_ftqPtr_value  # 6 bits
        self.uop_ftqOffset = uop_ftqOffset        # 4 bits
        self.uop_robIdx_flag = uop_robIdx_flag
        self.uop_robIdx_value = uop_robIdx_value  # 8 bits
        self.uop_sqIdx_flag = uop_sqIdx_flag
        self.uop_sqIdx_value = uop_sqIdx_value    # 6 bits
        self.mask = mask                          # 15 bits
        self.bits_paddr = bits_paddr              # 48 bits
        self.datavalid = datavalid
        self.revoke = revoke

class StoreIn:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, paddr=0, mask=0, miss=False):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value  # 8 bits
        self.paddr = paddr                 # 48 bits
        self.mask = mask                   # 16 bits
        self.miss = miss
    
class Ptr:
    def __init__(self, flag=False, value=0):
        self.flag = flag
        self.value = value  # 6 bits