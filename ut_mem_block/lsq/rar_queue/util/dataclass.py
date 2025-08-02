__all__ = [name for name in locals()]

class IORedirect:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, level=0):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value
        self.level = level

class IOQuery:
    def __init__(self, req_valid=False, uop_robIdx_flag=False, uop_robIdx_value=0,
                 uop_lqIdx_flag=False, uop_lqIdx_value=0, bits_paddr=0,
                 data_valid=False, is_nc=False, revoke=False):
        self.req_valid = req_valid  # input io_query_0_req_valid
        self.uop_robIdx_flag = uop_robIdx_flag  # input io_query_0_req_bits_uop_robIdx_flag
        self.uop_robIdx_value = uop_robIdx_value  # input [7:0] io_query_0_req_bits_uop_robIdx_value
        self.uop_lqIdx_flag = uop_lqIdx_flag  # input io_query_0_req_bits_uop_lqIdx_flag
        self.uop_lqIdx_value = uop_lqIdx_value  # input [6:0] io_query_0_req_bits_uop_lqIdx_value
        self.bits_paddr = bits_paddr  # input [47:0] io_query_0_req_bits_paddr
        self.data_valid = data_valid  # input io_query_0_req_bits_data_valid
        self.is_nc = is_nc  # input io_query_0_req_bits_is_nc
        self.revoke = revoke  # input io_query_0_revoke
    
class IOldWbPtr:
    def __init__(self, flag=False, value=0):
        self.flag = flag
        self.value = value
    
class IORelease:
    def __init__(self, valid=False, paddr=0):
        self.valid = valid  # input io_release_valid
        self.paddr = paddr  # input [47:0] io_release_bits_paddr