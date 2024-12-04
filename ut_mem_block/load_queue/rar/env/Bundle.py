from mlvp import Bundle

class ControlRedirectBundle(Bundle):
    # 通过前缀进行绑定io_redirect_
    signals = ["valid", "bits_robIdx_flag", "bits_robIdx_value", "bits_level"]

class ControlvecFeedbackBundle(Bundle): 
    # 通过前缀进行绑定io_vecFeedback_
    signals = ["valid", "bits_robidx_flag", "bits_robidx_value", "bits_uopidx", "bits_feedback_0"]

class QueryReqBundle(Bundle):
    # 通过前缀进行绑定io_query_0/1/2_req_
    signals = ["ready", "valid", "bits_uop_uopIdx", "bits_uop_robIdx_flag", "bits_uop_robIdx_value", 
               "bits_uop_lqIdx_flag", "bits_uop_lqIdx_value", "bits_paddr", "bits_data_valid"]

class QueryRespBundle(Bundle):
    # 通过前缀进行绑定io_query_0/1/2_resp_
    signals = ["valid", "bits_rep_frm_fetch"]
    
class QueryRevokeBundle(Bundle):
    # 通过前缀进行绑定io_query_0/1/2_
    signals = ["revoke"]
    
class ReleaseBundle(Bundle):
    # 通过前缀进行绑定io_release_
    signals = ["valid", "bits_paddr"]

class WritebackBundle(Bundle):
    # 通过前缀进行绑定io_ldWbPtr_
    signals = ["flag", "value"]
  
class FullBundle(Bundle):
    # 通过前缀进行绑定io_  (full)
    signals = ["lqFull"]