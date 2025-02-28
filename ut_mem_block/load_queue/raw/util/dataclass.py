__all__ = [name for name in locals()]

class IORedirect:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    level = False

class IOQuery:
    ready = False
    valid = False
    uop_preDecodeInfo_isRVC = False
    uop_ftqPtr_flag = False
    # 6 bits
    uop_ftqPtr_value = 0
    # 4 bits
    uop_ftqOffset = 0
    uop_robIdx_flag = False
    # 8 bits
    uop_robIdx_value = 0
    uop_sqIdx_flag = False
    # 6 bits
    uop_sqIdx_value = 0
    # 15 bits
    mask = 0
    # 48 bits
    bits_paddr = 0
    datavalid = False
    revoke = False
    
class StoreIn:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    # 48 bits
    paddr = 0
    # 16 bits
    mask = 0
    miss = False
    
class Ptr:
    flag = False
    # 6 bits
    value = 0
    