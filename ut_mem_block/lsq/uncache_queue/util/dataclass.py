__all__ = [name for name in locals()]

class IORedirect:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, level=False):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value  # 8-bit
        self.level = level
    
class RobIO:
        def __init__(self,  pendingMMIOld=False,  pendingPtr_flag=False,  pendingPtr_value=0):  
            self.pendingMMIOld = pendingMMIOld
            self.pendingPtr_flag = pendingPtr_flag
            self.pendingPtr_value = pendingPtr_value  # 8-bit

class ReqIO:
    def __init__(self, valid=False, bits_uop_exceptionVec_3=False, bits_uop_exceptionVec_4=False, bits_uop_exceptionVec_5=False,
                 bits_uop_exceptionVec_13=False, bits_uop_exceptionVec_21=False, bits_uop_trigger=0, bits_uop_preDecodeInfo_isRVC=False,
                 bits_uop_ftqPtr_flag=False, bits_uop_ftqPtr_value=0, bits_uop_ftqOffset=0, bits_uop_fuOpType=0, bits_uop_rfWen=False,
                 bits_uop_fpWen=False, bits_uop_vpu_vstart=0, bits_uop_vpu_veew=0, bits_uop_uopIdx=0, bits_uop_pdest=0,
                 bits_uop_robIdx_flag=False, bits_uop_robIdx_value=0, bits_uop_storeSetHit=False, bits_uop_waitForRobIdx_flag=False,
                 bits_uop_waitForRobIdx_value=0, bits_uop_loadWaitBit=False, bits_uop_loadWaitStrict=False, bits_uop_lqIdx_flag=False,
                 bits_uop_lqIdx_value=0, bits_uop_sqIdx_flag=False, bits_uop_sqIdx_value=0, bits_vaddr=0, bits_fullva=0,
                 bits_isHyper=False, bits_paddr=0, bits_gpaddr=0, bits_isForVSnonLeafPTE=False, bits_mask=0, bits_nc=False,
                 bits_mmio=False, bits_memBackTypeMM=False, bits_isvec=False, bits_is128bit=False, bits_vecActive=False,
                 bits_schedIndex=0, bits_rep_info_cause_0=False, bits_rep_info_cause_1=False, bits_rep_info_cause_2=False,
                 bits_rep_info_cause_3=False, bits_rep_info_cause_4=False, bits_rep_info_cause_5=False, bits_rep_info_cause_6=False,
                 bits_rep_info_cause_7=False, bits_rep_info_cause_8=False, bits_rep_info_cause_9=False, bits_rep_info_cause_10=False):
        self.valid = valid
        self.bits_uop_exceptionVec_3 = bits_uop_exceptionVec_3
        self.bits_uop_exceptionVec_4 = bits_uop_exceptionVec_4
        self.bits_uop_exceptionVec_5 = bits_uop_exceptionVec_5
        self.bits_uop_exceptionVec_13 = bits_uop_exceptionVec_13
        self.bits_uop_exceptionVec_21 = bits_uop_exceptionVec_21
        self.bits_uop_trigger = bits_uop_trigger
        self.bits_uop_preDecodeInfo_isRVC = bits_uop_preDecodeInfo_isRVC
        self.bits_uop_ftqPtr_flag = bits_uop_ftqPtr_flag
        self.bits_uop_ftqPtr_value = bits_uop_ftqPtr_value
        self.bits_uop_ftqOffset = bits_uop_ftqOffset
        self.bits_uop_fuOpType = bits_uop_fuOpType
        self.bits_uop_rfWen = bits_uop_rfWen
        self.bits_uop_fpWen = bits_uop_fpWen
        self.bits_uop_vpu_vstart = bits_uop_vpu_vstart
        self.bits_uop_vpu_veew = bits_uop_vpu_veew
        self.bits_uop_uopIdx = bits_uop_uopIdx
        self.bits_uop_pdest = bits_uop_pdest
        self.bits_uop_robIdx_flag = bits_uop_robIdx_flag
        self.bits_uop_robIdx_value = bits_uop_robIdx_value
        self.bits_uop_storeSetHit = bits_uop_storeSetHit
        self.bits_uop_waitForRobIdx_flag = bits_uop_waitForRobIdx_flag
        self.bits_uop_waitForRobIdx_value = bits_uop_waitForRobIdx_value
        self.bits_uop_loadWaitBit = bits_uop_loadWaitBit
        self.bits_uop_loadWaitStrict = bits_uop_loadWaitStrict
        self.bits_uop_lqIdx_flag = bits_uop_lqIdx_flag
        self.bits_uop_lqIdx_value = bits_uop_lqIdx_value
        self.bits_uop_sqIdx_flag = bits_uop_sqIdx_flag
        self.bits_uop_sqIdx_value = bits_uop_sqIdx_value
        self.bits_vaddr = bits_vaddr
        self.bits_fullva = bits_fullva
        self.bits_isHyper = bits_isHyper
        self.bits_paddr = bits_paddr
        self.bits_gpaddr = bits_gpaddr
        self.bits_isForVSnonLeafPTE = bits_isForVSnonLeafPTE
        self.bits_mask = bits_mask
        self.bits_nc = bits_nc
        self.bits_mmio = bits_mmio
        self.bits_memBackTypeMM = bits_memBackTypeMM
        self.bits_isvec = bits_isvec
        self.bits_is128bit = bits_is128bit
        self.bits_vecActive = bits_vecActive
        self.bits_schedIndex = bits_schedIndex
        self.bits_rep_info_cause_0 = bits_rep_info_cause_0
        self.bits_rep_info_cause_1 = bits_rep_info_cause_1
        self.bits_rep_info_cause_2 = bits_rep_info_cause_2
        self.bits_rep_info_cause_3 = bits_rep_info_cause_3
        self.bits_rep_info_cause_4 = bits_rep_info_cause_4
        self.bits_rep_info_cause_5 = bits_rep_info_cause_5
        self.bits_rep_info_cause_6 = bits_rep_info_cause_6
        self.bits_rep_info_cause_7 = bits_rep_info_cause_7
        self.bits_rep_info_cause_8 = bits_rep_info_cause_8
        self.bits_rep_info_cause_9 = bits_rep_info_cause_9
        self.bits_rep_info_cause_10 = bits_rep_info_cause_10

class Uncache:
    def __init__(self, resp_valid=False, resp_bits_data=0, resp_bits_id=0, resp_bits_nderr=False):
        self.resp_valid = resp_valid
        self.resp_bits_data = resp_bits_data
        self.resp_bits_id = resp_bits_id
        self.resp_bits_nderr = resp_bits_nderr