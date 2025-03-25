__all__ = [name for name in locals()]

class EnqReq:
    def __init__(self, valid=False, fuType=0, fuOpType=0, uopIdx=0, lastUop=False, robIdx_flag=False, robIdx_value=0, 
                 sqIdx_flag=False, sqIdx_value=0, numLsElem=0):
        self.valid = valid
        self.fuType = fuType
        self.fuOpType = fuOpType
        self.uopIdx = uopIdx
        self.lastUop = lastUop
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value
        self.sqIdx_flag = sqIdx_flag
        self.sqIdx_value = sqIdx_value
        self.numLsElem = numLsElem

class IORedirect:
    def __init__(self, valid=False, robIdx_flag=False, robIdx_value=0, level=False):
        self.valid = valid
        self.robIdx_flag = robIdx_flag
        self.robIdx_value = robIdx_value  # 8 bits
        self.level = level
    
class VecFeedback:
    def __init__(self, valid=False, robidx_flag=False, robidx_value=0, uopidx=0, vaddr=0, vaNeedExt=False, 
                 gpaddr=0, isForVSnonLeafPTE=False, feedback_0=False, feedback_1=False, exceptionVec_3=False, 
                 exceptionVec_6=False, exceptionVec_7=False, exceptionVec_15=False, exceptionVec_23=False):
        self.valid = valid
        self.robidx_flag = robidx_flag
        self.robidx_value = robidx_value # 8 bits
        self.uopidx = uopidx # 7 bits
        self.vaddr = vaddr # 64 bits
        self.vaNeedExt = vaNeedExt
        self.gpaddr = gpaddr # 50 bits
        self.isForVSnonLeafPTE = isForVSnonLeafPTE
        self.feedback_0 = feedback_0
        self.feedback_1 = feedback_1
        self.exceptionVec_3 = exceptionVec_3
        self.exceptionVec_6 = exceptionVec_6
        self.exceptionVec_7 = exceptionVec_7
        self.exceptionVec_15 = exceptionVec_15
        self.exceptionVec_23 = exceptionVec_23
    
class StoreAddrIn:
    def __init__(self, valid=False, uop_exceptionVec_3=False, uop_exceptionVec_6=False, uop_exceptionVec_7=False, 
                 uop_exceptionVec_15=False, uop_exceptionVec_23=False, uop_fuOpType=0, uop_uopIdx=0,   
                 uop_robIdx_flag=False, uop_robIdx_value=0, uop_sqIdx_value=0, vaddr=0, fullva=0, vaNeedExt=False, 
                 isHyper=False, paddr=0, gpaddr=0, isForVSnonLeafPTE=False, mask=0, wlineflag=False, miss=False, 
                 nc=False, isFrmMisAlignBuf=False, isvec=False, isMisalign=False, misalignWith16Byte=False, updateAddrValid=False):
        self.valid = valid
        self.uop_exceptionVec_3 = uop_exceptionVec_3
        self.uop_exceptionVec_6 = uop_exceptionVec_6
        self.uop_exceptionVec_7 = uop_exceptionVec_7
        self.uop_exceptionVec_15 = uop_exceptionVec_15
        self.uop_exceptionVec_23 = uop_exceptionVec_23
        self.uop_fuOpType = uop_fuOpType # 9 bits
        self.uop_uopIdx = uop_uopIdx # 7 bits
        self.uop_robIdx_flag = uop_robIdx_flag
        self.uop_robIdx_value = uop_robIdx_value # 8 bits
        self.uop_sqIdx_value = uop_sqIdx_value # 6 bits
        self.vaddr = vaddr  # 50 bits
        self.fullva = fullva  # 64 bits
        self.vaNeedExt = vaNeedExt
        self.isHyper = isHyper
        self.paddr = paddr  # 48 bits
        self.gpaddr = gpaddr  # 64 bits
        self.isForVSnonLeafPTE = isForVSnonLeafPTE
        self.mask = mask  # 16 bits
        self.wlineflag = wlineflag
        self.miss = miss
        self.nc = nc
        self.isFrmMisAlignBuf = isFrmMisAlignBuf
        self.isvec = isvec
        self.isMisalign = isMisalign
        self.misalignWith16Byte = misalignWith16Byte
        self.updateAddrValid = updateAddrValid
    
class StoreAddrInRe:
    def __init__(self, uop_exceptionVec_3=False, uop_exceptionVec_6=False, uop_exceptionVec_15=False, 
                 uop_exceptionVec_23=False, uop_uopIdx=0, uop_robIdx_flag=False, uop_robIdx_value=0,  
                 fullva=0, vaNeedExt=False, isHyper=False, gpaddr=0, isForVSnonLeafPTE=False, af=False, 
                 mmio=False, memBackTypeMM=False, hasException=False, isvec=False, updateAddrValid=False):
        self.uop_exceptionVec_3 = uop_exceptionVec_3
        self.uop_exceptionVec_6 = uop_exceptionVec_6
        self.uop_exceptionVec_15 = uop_exceptionVec_15
        self.uop_exceptionVec_23 = uop_exceptionVec_23
        self.uop_uopIdx = uop_uopIdx   # 7 bits
        self.uop_robIdx_flag = uop_robIdx_flag
        self.uop_robIdx_value = uop_robIdx_value   # 8 bits
        self.fullva = fullva    # 64 bits
        self.vaNeedExt = vaNeedExt
        self.isHyper = isHyper
        self.gpaddr = gpaddr   # 64 bits
        self.isForVSnonLeafPTE = isForVSnonLeafPTE
        self.af = af
        self.mmio = mmio
        self.memBackTypeMM = memBackTypeMM
        self.hasException = hasException
        self.isvec = isvec
        self.updateAddrValid = updateAddrValid
    
class StoreDataIn:
    def __init__(self, valid=False, bits_uop_fuType=0, bits_uop_fuOpType=0, bits_uop_sqIdx_value=0, bits_data=0):  
        self.valid = valid
        self.bits_uop_fuType = bits_uop_fuType   # 35 bits
        self.bits_uop_fuOpType = bits_uop_fuOpType   # 9 bits
        self.bits_uop_sqIdx_value = bits_uop_sqIdx_value  # 6 bits
        self.bits_data = bits_data  # 128 bits
    
class Forward:
    def __init__(self, vaddr=0, paddr=0, mask=0, uop_waitForRobIdx_flag=False, uop_waitForRobIdx_value=0, 
                 uop_loadWaitBit=False, uop_loadWaitStrict=False, uop_sqIdx_flag=False, uop_sqIdx_value=0,      
                 valid=False, forwardMask=None, forwardData=None, sqIdx_flag=False, dataInvalid=False, 
                 matchInvalid=False, addrInvalid=False, sqIdxMask=0, dataInvalidSqIdx_flag=False, 
                 dataInvalidSqIdx_value=0, addrInvalidSqIdx_flag=False, addrInvalidSqIdx_value=0):  
        self.vaddr = vaddr    # 50 bits
        self.paddr = paddr    # 48 bits
        self.mask = mask      # 16 bits
        self.uop_waitForRobIdx_flag = uop_waitForRobIdx_flag
        self.uop_waitForRobIdx_value = uop_waitForRobIdx_value   # 8 bits
        self.uop_loadWaitBit = uop_loadWaitBit
        self.uop_loadWaitStrict = uop_loadWaitStrict
        self.uop_sqIdx_flag = uop_sqIdx_flag
        self.uop_sqIdx_value = uop_sqIdx_value   # 6 bits
        self.valid = valid
        self.forwardMask = forwardMask if forwardMask is not None else [0] * 16
        self.forwardData = forwardData if forwardData is not None else [0] * 16
        self.sqIdx_flag = sqIdx_flag
        self.dataInvalid = dataInvalid
        self.matchInvalid = matchInvalid
        self.addrInvalid = addrInvalid
        self.sqIdxMask = sqIdxMask     # 56 bits
        self.dataInvalidSqIdx_flag = dataInvalidSqIdx_flag
        self.dataInvalidSqIdx_value = dataInvalidSqIdx_value   # 6 bits
        self.addrInvalidSqIdx_flag = addrInvalidSqIdx_flag
        self.addrInvalidSqIdx_value = addrInvalidSqIdx_value   # 6 bits
    
class IORob:
    def __init__(self, rob_scommit=0, pendingst=False, pendingPtr_flag=False, pendingPtr_value=0):
        self.rob_scommit = rob_scommit       # 4 bits
        self.pendingst = pendingst
        self.pendingPtr_flag = pendingPtr_flag
        self.pendingPtr_value = pendingPtr_value  # 8 bits

class Uncache:
    def __init__(self, req_ready=False, req_valid=False, req_bits_addr=0, req_bits_vaddr=0, req_bits_data=0,
                 req_bits_mask=0, req_bits_id=0, req_bits_nc=False, req_bits_memBackTypeMM=False, 
                 resp_valid=False, resp_bits_id=0, resp_bits_nc=False, resp_bits_nderr=False):
        self.req_ready = req_ready
        self.req_valid = req_valid
        self.req_bits_addr = req_bits_addr            # 48 bits
        self.req_bits_vaddr = req_bits_vaddr          # 50 bits
        self.req_bits_data = req_bits_data          # 64 bits
        self.req_bits_mask = req_bits_mask          # 8 bits
        self.req_bits_id = req_bits_id            # 7 bits
        self.req_bits_nc = req_bits_nc
        self.req_bits_memBackTypeMM = req_bits_memBackTypeMM
        self.resp_valid = resp_valid
        self.resp_bits_id = resp_bits_id           # 7 bits
        self.resp_bits_nc = resp_bits_nc
        self.resp_bits_nderr = resp_bits_nderr
    
class MaControlInput:
    def __init__(self, crossPageWithHit=False, crossPageCanDeq=False, paddr=0, withSameUop=False):
        self.crossPageWithHit = crossPageWithHit
        self.crossPageCanDeq = crossPageCanDeq
        self.paddr = paddr                # 48 bits
        self.withSameUop = withSameUop

    
class StoreMaskIn:
    def __init__(self, valid=False, sqIdx_value=0, mask=0):
        self.valid = valid
        self.sqIdx_value = sqIdx_value
        self.mask = mask