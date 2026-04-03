import random
from toffee import *
FTQSIZE = 64

class FtqAgent(Agent):
    def __init__(self, ftq_bundle):
        super().__init__(ftq_bundle) 

    


    @driver_method()
    async def drive_backend_inputs(
        self,
        valid=None,
        ftqIdx_value=None,
        ftqOffset=None,
        cfiUpdate_target=None,
        cfiUpdate_taken=None,
        cfiUpdate_isMisPred=None,
        ftqIdx_flag=None, 
        level=None,
        debugIsCtrl=None,
        debugIsMemVio=None,
        ftqIdxAhead_0_valid=None,
        ftqIdxAhead_0_bits_value=None,
        ftqIdxSelOH_bits=None,
    ):
        if valid is not None:
            self.bundle.fromBackend.redirect_valid.value = 1 if valid else 0
        if ftqIdx_value is not None:
            self.bundle.fromBackend.redirect_bits_ftqIdx_value.value = ftqIdx_value
        if ftqOffset is not None:
            self.bundle.fromBackend.redirect_bits_ftqOffset.value = ftqOffset
        if cfiUpdate_target is not None:
            self.bundle.fromBackend.redirect_bits_cfiUpdate_target.value = cfiUpdate_target
        if cfiUpdate_taken is not None:
            self.bundle.fromBackend.redirect_bits_cfiUpdate_taken.value = 1 if cfiUpdate_taken else 0
        if cfiUpdate_isMisPred is not None:
            self.bundle.fromBackend.redirect_bits_cfiUpdate_isMisPred.value = 1 if cfiUpdate_isMisPred else 0
        if ftqIdx_flag is not None: 
            self.bundle.fromBackend.redirect_bits_ftqIdx_flag.value = 1 if ftqIdx_flag else 0
        if level is not None:
            self.bundle.fromBackend.redirect_bits_level.value = level
        if debugIsCtrl is not None:
            self.bundle.fromBackend.redirect_bits_debugIsCtrl.value = 1 if debugIsCtrl else 0
        if debugIsMemVio is not None:
            self.bundle.fromBackend.redirect_bits_debugIsMemVio.value = 1 if debugIsMemVio else 0
        if ftqIdxAhead_0_valid is not None:
            self.bundle.fromBackend.ftqIdxAhead_0_valid.value = 1 if ftqIdxAhead_0_valid else 0
        if ftqIdxAhead_0_bits_value is not None:
            self.bundle.fromBackend.ftqIdxAhead_0_bits_value.value = ftqIdxAhead_0_bits_value
        if ftqIdxSelOH_bits is not None:
            self.bundle.fromBackend.ftqIdxSelOH_bits.value = ftqIdxSelOH_bits    
        return self.bundle.as_dict()

    @driver_method()
    async def set_rob_commit(self, idx: int, valid=None, commitType=None, ftqIdx_flag=None, ftqIdx_value=None, ftqOffset=None):
        assert 0 <= idx <= 7, "rob commit idx 必须在 [0..7]"
        rb = getattr(self.bundle.fromBackend, f'rob_commits_{idx}')
        if valid is not None:        rb.valid.value = 1 if valid else 0
        if commitType is not None:   rb.bits_commitType.value = commitType
        if ftqIdx_flag is not None:  rb.bits_ftqIdx_flag.value = 1 if ftqIdx_flag else 0
        if ftqIdx_value is not None: rb.bits_ftqIdx_value.value = ftqIdx_value
        if ftqOffset is not None:    rb.bits_ftqOffset.value = ftqOffset
        return self.bundle.as_dict()
    

    @driver_method()
    async def drive_ifu_inputs(
        self,
        valid=None,
        ftqIdx_value=None,
        misOffset_bits=None,
        target=None,
        misOffset_valid=None,
        cfiOffset_valid=None,
        ftqIdx_flag=None, 
    ):
        if valid is not None:
            self.bundle.fromIfu.pdWb_valid.value = 1 if valid else 0
        if ftqIdx_value is not None:
            self.bundle.fromIfu.pdWb_bits_ftqIdx_value.value = ftqIdx_value
        if misOffset_bits is not None:
            self.bundle.fromIfu.pdWb_bits_misOffset_bits.value = misOffset_bits
        if target is not None:
            self.bundle.fromIfu.pdWb_bits_target.value = target
        if misOffset_valid is not None:
            self.bundle.fromIfu.pdWb_bits_misOffset_valid.value = 1 if misOffset_valid else 0
        if cfiOffset_valid is not None:
            self.bundle.fromIfu.pdWb_bits_cfiOffset_valid.value = 1 if cfiOffset_valid else 0
        if ftqIdx_flag is not None: 
            self.bundle.fromIfu.pdWb_bits_ftqIdx_flag.value = 1 if ftqIdx_flag else 0
        return self.bundle.as_dict()



    @driver_method()
    async def drive_toifu_ready(self, ready):        
        self.bundle.toIfu.req_ready.value = 1 if ready else 0
    
        return self.bundle.as_dict()



    @driver_method()
    async def drive_s1_signals(self, valid=None, pc=None, fallThruError=None):
        if valid is not None:
            self.bundle.fromBpu.resp_valid.value = 1 if valid else 0
        if pc is not None:
            self.bundle.fromBpu.resp_bits_s1_pc_3.value = pc
        if fallThruError is not None:
            self.bundle.fromBpu.resp_bits_s1_full_pred_3_fallThroughErr.value = 1 if fallThruError else 0
        return self.bundle.as_dict()

    @driver_method()
    async def drive_s2_signals(
        self,
        valid=None, hasRedirect=None, pc=None,
        redirect_idx=None, redirect_flag=None, fallThruError=None,
        full_pred_3_hit=None, 
    ):
        if valid is not None:
            self.bundle.fromBpu.resp_bits_s2_valid_3.value = 1 if valid else 0
        if hasRedirect is not None:
            self.bundle.fromBpu.resp_bits_s2_hasRedirect_3.value = 1 if hasRedirect else 0
        if pc is not None:
            self.bundle.fromBpu.resp_bits_s2_pc_3.value = pc
        if redirect_idx is not None:
            self.bundle.fromBpu.resp_bits_s2_ftq_idx_value.value = redirect_idx
        if redirect_flag is not None:
            self.bundle.fromBpu.resp_bits_s2_ftq_idx_flag.value = redirect_flag
        if fallThruError is not None:
            self.bundle.fromBpu.resp_bits_s2_full_pred_3_fallThroughErr.value = 1 if fallThruError else 0
        if full_pred_3_hit is not None:  
            self.bundle.fromBpu.resp_bits_s2_full_pred_3_hit.value = 1 if full_pred_3_hit else 0
        return self.bundle.as_dict()



    @driver_method()
    async def drive_s3_signals(
        self,
        valid=None, hasRedirect=None, pc=None,
        redirect_idx=None, redirect_flag=None, fallThruError=None,
    ):
        if valid is not None:
            self.bundle.fromBpu.resp_bits_s3_valid_3.value = 1 if valid else 0
        if hasRedirect is not None:
            self.bundle.fromBpu.resp_bits_s3_hasRedirect_3.value = 1 if hasRedirect else 0
        if pc is not None:
            self.bundle.fromBpu.resp_bits_s3_pc_3.value = pc
        if redirect_idx is not None:
            self.bundle.fromBpu.resp_bits_s3_ftq_idx_value.value = redirect_idx
        if redirect_flag is not None:
            self.bundle.fromBpu.resp_bits_s3_ftq_idx_flag.value = redirect_flag
        if fallThruError is not None:
            self.bundle.fromBpu.resp_bits_s3_full_pred_3_fallThroughErr.value = 1 if fallThruError else 0
        return self.bundle.as_dict()


    @driver_method()
    async def drive_s3_last_stage(
        self,
        isJalr=None, isCall=None, isRet=None,
        brSlots_0_valid=None, brSlots_0_offset=None,
        tailSlot_valid=None, tailSlot_offset=None, tailSlot_sharing=None,
        valid=None,
    ):
        ls = self.bundle.fromBpu.last_stage_ftb_entry
        if valid is not None:             ls.valid.value = 1 if valid else 0
        if isJalr is not None:            ls.isJalr.value = 1 if isJalr else 0
        if isCall is not None:            ls.isCall.value = 1 if isCall else 0
        if isRet is not None:             ls.isRet.value = 1 if isRet else 0
        if brSlots_0_valid is not None:   ls.brSlots_0_valid.value = 1 if brSlots_0_valid else 0
        if brSlots_0_offset is not None:  ls.brSlots_0_offset.value = brSlots_0_offset
        if tailSlot_valid is not None:    ls.tailSlot_valid.value = 1 if tailSlot_valid else 0
        if tailSlot_offset is not None:   ls.tailSlot_offset.value = tailSlot_offset
        if tailSlot_sharing is not None:  ls.tailSlot_sharing.value = 1 if tailSlot_sharing else 0
        return self.bundle.as_dict()

    @driver_method()
    async def set_ifu_pd(self, slot: int, brType=None, isCall=None, isRet=None, valid=None):
        assert 0 <= slot <= 15, "slot 必须在 [0..15]"
        if slot == 0:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_0.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_0.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_0.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_0.valid.value  = 1 if valid else 0
        elif slot == 1:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_1.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_1.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_1.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_1.valid.value  = 1 if valid else 0
        elif slot == 2:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_2.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_2.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_2.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_2.valid.value  = 1 if valid else 0
        elif slot == 3:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_3.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_3.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_3.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_3.valid.value  = 1 if valid else 0
        elif slot == 4:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_4.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_4.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_4.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_4.valid.value  = 1 if valid else 0
        elif slot == 5:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_5.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_5.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_5.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_5.valid.value  = 1 if valid else 0
        elif slot == 6:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_6.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_6.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_6.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_6.valid.value  = 1 if valid else 0
        elif slot == 7:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_7.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_7.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_7.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_7.valid.value  = 1 if valid else 0
        elif slot == 8:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_8.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_8.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_8.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_8.valid.value  = 1 if valid else 0
        elif slot == 9:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_9.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_9.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_9.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_9.valid.value  = 1 if valid else 0
        elif slot == 10:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_10.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_10.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_10.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_10.valid.value  = 1 if valid else 0
        elif slot == 11:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_11.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_11.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_11.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_11.valid.value  = 1 if valid else 0
        elif slot == 12:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_12.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_12.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_12.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_12.valid.value  = 1 if valid else 0
        elif slot == 13:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_13.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_13.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_13.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_13.valid.value  = 1 if valid else 0
        elif slot == 14:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_14.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_14.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_14.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_14.valid.value  = 1 if valid else 0
        elif slot == 15:
            if brType is not None: self.bundle.fromIfu.pdWb_bits_pd_15.brType.value = int(brType)
            if isCall is not None: self.bundle.fromIfu.pdWb_bits_pd_15.isCall.value = 1 if isCall else 0
            if isRet  is not None: self.bundle.fromIfu.pdWb_bits_pd_15.isRet.value  = 1 if isRet  else 0
            if valid is not None: self.bundle.fromIfu.pdWb_bits_pd_15.valid.value  = 1 if valid else 0
        return self.bundle.as_dict()
 

    @driver_method()
    async def set_ifu_pc(self, slot: int, pc):
        assert 0 <= slot <= 15, "必须在0-15"
        if slot == 0:   self.bundle.fromIfu.pdWb_bits_pc_0.value  = pc
        elif slot == 1: self.bundle.fromIfu.pdWb_bits_pc_1.value  = pc
        elif slot == 2: self.bundle.fromIfu.pdWb_bits_pc_2.value  = pc
        elif slot == 3: self.bundle.fromIfu.pdWb_bits_pc_3.value  = pc
        elif slot == 4: self.bundle.fromIfu.pdWb_bits_pc_4.value  = pc
        elif slot == 5: self.bundle.fromIfu.pdWb_bits_pc_5.value  = pc
        elif slot == 6: self.bundle.fromIfu.pdWb_bits_pc_6.value  = pc
        elif slot == 7: self.bundle.fromIfu.pdWb_bits_pc_7.value  = pc
        elif slot == 8: self.bundle.fromIfu.pdWb_bits_pc_8.value  = pc
        elif slot == 9: self.bundle.fromIfu.pdWb_bits_pc_9.value  = pc
        elif slot == 10: self.bundle.fromIfu.pdWb_bits_pc_10.value = pc
        elif slot == 11: self.bundle.fromIfu.pdWb_bits_pc_11.value = pc
        elif slot == 12: self.bundle.fromIfu.pdWb_bits_pc_12.value = pc
        elif slot == 13: self.bundle.fromIfu.pdWb_bits_pc_13.value = pc
        elif slot == 14: self.bundle.fromIfu.pdWb_bits_pc_14.value = pc
        else:            self.bundle.fromIfu.pdWb_bits_pc_15.value = pc
        return self.bundle.as_dict()    

    @driver_method()
    async def set_rob_commit(self, idx: int, valid=None, commitType=None, ftqIdx_flag=None, ftqIdx_value=None, ftqOffset=None):
    
        assert 0 <= idx <= 7, "必须在0-7"
        rb = getattr(self.bundle.fromBackend, f'rob_commits_{idx}')
        if valid is not None:        rb.valid.value = 1 if valid else 0
        if commitType is not None:   rb.bits_commitType.value = commitType
        if ftqIdx_flag is not None:  rb.bits_ftqIdx_flag.value = 1 if ftqIdx_flag else 0
        if ftqIdx_value is not None: rb.bits_ftqIdx_value.value = ftqIdx_value
        if ftqOffset is not None:    rb.bits_ftqOffset.value = ftqOffset
        return self.bundle.as_dict()    

    @driver_method()
    async def reset_inputs(self):

        self.bundle.fromBackend.redirect_valid.value = 0
        self.bundle.fromBackend.redirect_bits_ftqIdx_value.value = 0
        self.bundle.fromBackend.redirect_bits_ftqIdx_flag.value = 0
        self.bundle.fromBackend.redirect_bits_ftqOffset.value = 0
        self.bundle.fromBackend.redirect_bits_cfiUpdate_target.value = 0
        self.bundle.fromBackend.redirect_bits_cfiUpdate_taken.value = 0
        self.bundle.fromBackend.redirect_bits_cfiUpdate_isMisPred.value = 0
        self.bundle.fromBackend.redirect_bits_level.value = 0
        self.bundle.fromBackend.redirect_bits_debugIsCtrl.value = 0
        self.bundle.fromBackend.redirect_bits_debugIsMemVio.value = 0
        self.bundle.fromBackend.ftqIdxSelOH_bits.value = 0
        self.bundle.fromBackend.ftqIdxAhead_0_valid.value = 0
        self.bundle.fromBackend.ftqIdxAhead_0_bits_value.value = 0


        for i in range(8):
            rb = getattr(self.bundle.fromBackend, f'rob_commits_{i}')
            rb.valid.value = 0
            rb.bits_commitType.value = 0
            rb.bits_ftqIdx_flag.value = 0
            rb.bits_ftqIdx_value.value = 0
            rb.bits_ftqOffset.value = 0
        

        self.bundle.fromIfu.pdWb_bits_target.value = 0
        self.bundle.fromIfu.pdWb_bits_cfiOffset_valid.value = 0
        self.bundle.fromIfu.pdWb_bits_misOffset_valid.value = 0
        self.bundle.fromIfu.pdWb_bits_ftqIdx_value.value = 0
        self.bundle.fromIfu.pdWb_bits_ftqIdx_flag.value = 0
        self.bundle.fromIfu.pdWb_bits_misOffset_bits.value = 0
        self.bundle.fromIfu.pdWb_valid.value = 0
        

        self.bundle.toIfu.req_ready.value = 0


        self.bundle.fromBpu.resp_valid.value = 0
        self.bundle.fromBpu.resp_bits_s1_pc_3.value = 0
        self.bundle.fromBpu.resp_bits_s1_full_pred_3_fallThroughErr.value = 0
        self.bundle.fromBpu.resp_bits_s2_valid_3.value = 0
        self.bundle.fromBpu.resp_bits_s2_hasRedirect_3.value = 0
        self.bundle.fromBpu.resp_bits_s2_pc_3.value = 0
        self.bundle.fromBpu.resp_bits_s2_ftq_idx_value.value = 0
        self.bundle.fromBpu.resp_bits_s2_ftq_idx_flag.value = 0
        self.bundle.fromBpu.resp_bits_s2_full_pred_3_fallThroughErr.value = 0
        self.bundle.fromBpu.resp_bits_s2_full_pred_3_hit.value = 0
        self.bundle.fromBpu.resp_bits_s3_valid_3.value = 0
        self.bundle.fromBpu.resp_bits_s3_hasRedirect_3.value = 0
        self.bundle.fromBpu.resp_bits_s3_pc_3.value = 0
        self.bundle.fromBpu.resp_bits_s3_ftq_idx_value.value = 0
        self.bundle.fromBpu.resp_bits_s3_ftq_idx_flag.value = 0
        self.bundle.fromBpu.resp_bits_s3_full_pred_3_fallThroughErr.value = 0

        self.bundle.fromBpu.last_stage_ftb_entry.valid.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.isJalr.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.isCall.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.isRet.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.brSlots_0_valid.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.brSlots_0_offset.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.tailSlot_valid.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.tailSlot_offset.value = 0
        self.bundle.fromBpu.last_stage_ftb_entry.tailSlot_sharing.value = 0


        self.bundle.fromIfu.pdWb_bits_pd_0.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_0.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_0.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_0.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_1.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_1.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_1.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_1.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_2.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_2.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_2.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_2.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_3.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_3.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_3.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_3.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_4.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_4.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_4.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_4.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_5.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_5.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_5.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_5.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_6.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_6.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_6.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_6.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_7.brType.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_7.isCall.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_7.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_7.valid.value  = 0
 
        self.bundle.fromIfu.pdWb_bits_pd_8.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_8.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_9.isRet.value  = 0
        self.bundle.fromIfu.pdWb_bits_pd_9.valid.value  = 0

        self.bundle.fromIfu.pdWb_bits_pd_10.isRet.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_10.valid.value = 0

        self.bundle.fromIfu.pdWb_bits_pd_11.isRet.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_11.valid.value = 0

        self.bundle.fromIfu.pdWb_bits_pd_12.isRet.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_12.valid.value = 0

        self.bundle.fromIfu.pdWb_bits_pd_13.isRet.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_13.valid.value = 0

        self.bundle.fromIfu.pdWb_bits_pd_14.isRet.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_14.valid.value = 0

        self.bundle.fromIfu.pdWb_bits_pd_15.isRet.value = 0
        self.bundle.fromIfu.pdWb_bits_pd_15.valid.value = 0

        self.bundle.fromIfu.pdWb_bits_pc_0.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_1.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_2.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_3.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_4.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_5.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_6.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_7.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_8.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_9.value  = 0
        self.bundle.fromIfu.pdWb_bits_pc_10.value = 0
        self.bundle.fromIfu.pdWb_bits_pc_11.value = 0
        self.bundle.fromIfu.pdWb_bits_pc_12.value = 0
        self.bundle.fromIfu.pdWb_bits_pc_13.value = 0
        self.bundle.fromIfu.pdWb_bits_pc_14.value = 0
        self.bundle.fromIfu.pdWb_bits_pc_15.value = 0

        for i in range(8):
            rb = getattr(self.bundle.fromBackend, f'rob_commits_{i}')
            rb.valid.value = 0
            rb.bits_commitType.value = 0
            rb.bits_ftqIdx_flag.value = 0
            rb.bits_ftqIdx_value.value = 0
            rb.bits_ftqOffset.value = 0

        return self.bundle.as_dict() 

    @driver_method()
    async def set_write_mode_as_imme(self):

        self.bundle.set_write_mode_as_imme()
        print("already set immediate mode")

        return self.bundle.as_dict()  

    @driver_method()
    async def set_write_mode_as_rise(self):
 
        self.bundle.set_write_mode_as_rise()
        print("already set immediate mode")

        return self.bundle.as_dict()  

    @driver_method()
    async def set_write_mode_as_fall(self):

        self.bundle.set_write_mode_as_fall()
        print("already set immediate mode")

        return self.bundle.as_dict()  

    @driver_method()
    async def reset5(self, dut):
      
        dut.reset.value = 1
        await self.bundle.step(5)
        dut.reset.value = 0
        return self.bundle.as_dict()  

    @driver_method()
    async def get_toicache_outputs(self):
     
        outputs = {
            'req_valid': self.bundle.toICache.req_valid.value,
            'readValid': {
                '0': self.bundle.toICache.req_bits_readValid_0.value,
                '1': self.bundle.toICache.req_bits_readValid_1.value,
                '2': self.bundle.toICache.req_bits_readValid_2.value,
                '3': self.bundle.toICache.req_bits_readValid_3.value,
                '4': self.bundle.toICache.req_bits_readValid_4.value,
            },
            'startAddr': {
                '0': self.bundle.toICache.req_bits_pcMemRead_0_startAddr.value,
                '1': self.bundle.toICache.req_bits_pcMemRead_1_startAddr.value,
                '2': self.bundle.toICache.req_bits_pcMemRead_2_startAddr.value,
                '3': self.bundle.toICache.req_bits_pcMemRead_3_startAddr.value,
                '4': self.bundle.toICache.req_bits_pcMemRead_4_startAddr.value,
            },
            'nextlineStart': {
                '0': self.bundle.toICache.req_bits_pcMemRead_0_nextlineStart.value,
                '1': self.bundle.toICache.req_bits_pcMemRead_1_nextlineStart.value,
                '2': self.bundle.toICache.req_bits_pcMemRead_2_nextlineStart.value,
                '3': self.bundle.toICache.req_bits_pcMemRead_3_nextlineStart.value,
                '4': self.bundle.toICache.req_bits_pcMemRead_4_nextlineStart.value,
            }
        }
        return outputs    

    @driver_method()
    async def get_toprefetch_outputs(self):
        
        outputs = {
            'req_ready': self.bundle.toPrefetch.req_ready.value,
            'req_valid': self.bundle.toPrefetch.req_valid.value,
            'flushFromBpu': {
                's2': {
                    'valid': self.bundle.toPrefetch.flushFromBpu_s2_valid.value,
                    'flag': self.bundle.toPrefetch.flushFromBpu_s2_bits_flag.value,
                    'value': self.bundle.toPrefetch.flushFromBpu_s2_bits_value.value,
                },
                's3': {
                    'valid': self.bundle.toPrefetch.flushFromBpu_s3_valid.value,
                    'flag': self.bundle.toPrefetch.flushFromBpu_s3_bits_flag.value,
                    'value': self.bundle.toPrefetch.flushFromBpu_s3_bits_value.value,
                }
            }
        }
        return outputs  
          
    @driver_method()
    async def get_fromBpu_resp_ready(self):
        
        return self.bundle.fromBpu.resp_ready.value    

    @driver_method()
    async def drive_s1_full_signals(self, dict):
        self.bundle.fromBpuNew.valid.value = dict['valid']
        self.bundle.fromBpuNew.s1.pc_3.value = dict['pc_3']
        self.bundle.fromBpuNew.s1.full_pred_3_fallThroughErr.value = dict['full_pred_3_fallThroughErr']
        self.bundle.fromBpuNew.s1.full_pred_3_br_taken_mask_0.value = dict['full_pred_3_br_taken_mask_0']
        self.bundle.fromBpuNew.s1.full_pred_3_br_taken_mask_1.value = dict['full_pred_3_br_taken_mask_1']
        self.bundle.fromBpuNew.s1.full_pred_3_slot_valids_0.value = dict['full_pred_3_slot_valids_0']
        self.bundle.fromBpuNew.s1.full_pred_3_slot_valids_1.value = dict['full_pred_3_slot_valids_1']
        self.bundle.fromBpuNew.s1.full_pred_3_targets_0.value = dict['full_pred_3_targets_0']
        self.bundle.fromBpuNew.s1.full_pred_3_targets_1.value = dict['full_pred_3_targets_1']
        self.bundle.fromBpuNew.s1.full_pred_3_offsets_0.value = dict['full_pred_3_offsets_0']
        self.bundle.fromBpuNew.s1.full_pred_3_offsets_1.value = dict['full_pred_3_offsets_1']
        self.bundle.fromBpuNew.s1.full_pred_3_fallThroughAddr.value = dict['full_pred_3_fallThroughAddr']
        self.bundle.fromBpuNew.s1.full_pred_3_is_br_sharing.value = dict['full_pred_3_is_br_sharing']
        self.bundle.fromBpuNew.s1.full_pred_3_hit.value = dict['full_pred_3_hit']
        return self.bundle.as_dict()

    @driver_method()
    async def drive_s2_full_signals(self, dict):
        self.bundle.fromBpuNew.s2.pc_3.value = dict['pc_3']
        self.bundle.fromBpuNew.s2.full_pred_3_fallThroughErr.value = dict['full_pred_3_fallThroughErr']
        self.bundle.fromBpuNew.s2.full_pred_3_br_taken_mask_0.value = dict['full_pred_3_br_taken_mask_0']
        self.bundle.fromBpuNew.s2.full_pred_3_br_taken_mask_1.value = dict['full_pred_3_br_taken_mask_1']
        self.bundle.fromBpuNew.s2.full_pred_3_slot_valids_0.value = dict['full_pred_3_slot_valids_0']
        self.bundle.fromBpuNew.s2.full_pred_3_slot_valids_1.value = dict['full_pred_3_slot_valids_1']
        self.bundle.fromBpuNew.s2.full_pred_3_targets_0.value = dict['full_pred_3_targets_0']
        self.bundle.fromBpuNew.s2.full_pred_3_targets_1.value = dict['full_pred_3_targets_1']
        self.bundle.fromBpuNew.s2.full_pred_3_offsets_0.value = dict['full_pred_3_offsets_0']
        self.bundle.fromBpuNew.s2.full_pred_3_offsets_1.value = dict['full_pred_3_offsets_1']
        self.bundle.fromBpuNew.s2.full_pred_3_fallThroughAddr.value = dict['full_pred_3_fallThroughAddr']
        self.bundle.fromBpuNew.s2.full_pred_3_is_br_sharing.value = dict['full_pred_3_is_br_sharing']
        self.bundle.fromBpuNew.s2.full_pred_3_hit.value = dict['full_pred_3_hit']
        self.bundle.fromBpuNew.s2.valid_3.value = dict['valid_3']
        self.bundle.fromBpuNew.s2.hasRedirect_3.value = dict['hasRedirect_3']
        self.bundle.fromBpuNew.s2.ftq_idx_flag.value = dict['ftq_idx_flag']
        self.bundle.fromBpuNew.s2.ftq_idx_value.value = dict['ftq_idx_value']
        return self.bundle.as_dict()

    @driver_method()
    async def drive_s3_full_signals(self, dict):
        self.bundle.fromBpuNew.s3.pc_3.value = dict['pc_3']
        self.bundle.fromBpuNew.s3.full_pred_3_fallThroughErr.value = dict['full_pred_3_fallThroughErr']
        self.bundle.fromBpuNew.s3.full_pred_3_br_taken_mask_0.value = dict['full_pred_3_br_taken_mask_0']
        self.bundle.fromBpuNew.s3.full_pred_3_br_taken_mask_1.value = dict['full_pred_3_br_taken_mask_1']
        self.bundle.fromBpuNew.s3.full_pred_3_slot_valids_0.value = dict['full_pred_3_slot_valids_0']
        self.bundle.fromBpuNew.s3.full_pred_3_slot_valids_1.value = dict['full_pred_3_slot_valids_1']
        self.bundle.fromBpuNew.s3.full_pred_3_targets_0.value = dict['full_pred_3_targets_0']
        self.bundle.fromBpuNew.s3.full_pred_3_targets_1.value = dict['full_pred_3_targets_1']
        self.bundle.fromBpuNew.s3.full_pred_3_offsets_0.value = dict['full_pred_3_offsets_0']
        self.bundle.fromBpuNew.s3.full_pred_3_offsets_1.value = dict['full_pred_3_offsets_1']
        self.bundle.fromBpuNew.s3.full_pred_3_fallThroughAddr.value = dict['full_pred_3_fallThroughAddr']
        self.bundle.fromBpuNew.s3.full_pred_3_is_br_sharing.value = dict['full_pred_3_is_br_sharing']
        self.bundle.fromBpuNew.s3.full_pred_3_hit.value = dict['full_pred_3_hit']
        self.bundle.fromBpuNew.s3.valid_3.value = dict['valid_3']
        self.bundle.fromBpuNew.s3.hasRedirect_3.value = dict['hasRedirect_3']
        self.bundle.fromBpuNew.s3.ftq_idx_flag.value = dict['ftq_idx_flag']
        self.bundle.fromBpuNew.s3.ftq_idx_value.value = dict['ftq_idx_value']
        return self.bundle.as_dict()
    
    @driver_method()
    async def drive_last_stage_ftb_entry_signals(self, dict):
        self.bundle.fromBpuNew.last_stage_ftb_entry.valid.value = dict['valid']
        self.bundle.fromBpuNew.last_stage_ftb_entry.isJalr.value = dict['isJalr']
        self.bundle.fromBpuNew.last_stage_ftb_entry.isCall.value = dict['isCall']
        self.bundle.fromBpuNew.last_stage_ftb_entry.isRet.value = dict['isRet']
        self.bundle.fromBpuNew.last_stage_ftb_entry.last_may_be_rvi_call.value = dict['last_may_be_rvi_call']
        self.bundle.fromBpuNew.last_stage_ftb_entry.carry.value = dict['carry']
        self.bundle.fromBpuNew.last_stage_ftb_entry.pftAddr.value = dict['pftAddr']
        self.bundle.fromBpuNew.last_stage_ftb_entry.brSlots_0_valid.value = dict['brSlots_0_valid']
        self.bundle.fromBpuNew.last_stage_ftb_entry.brSlots_0_sharing.value = dict['brSlots_0_sharing']
        self.bundle.fromBpuNew.last_stage_ftb_entry.brSlots_0_offset.value = dict['brSlots_0_offset']
        self.bundle.fromBpuNew.last_stage_ftb_entry.tailSlot_valid.value = dict['tailSlot_valid']
        self.bundle.fromBpuNew.last_stage_ftb_entry.tailSlot_offset.value = dict['tailSlot_offset']
        self.bundle.fromBpuNew.last_stage_ftb_entry.tailSlot_sharing.value = dict['tailSlot_sharing']
        
        return self.bundle.as_dict()
    
    @driver_method()
    async def drive_last_stage_spec_info_signals(self, dict):
        self.bundle.fromBpuNew.last_stage_spec_info.histPtr_flag.value = dict['histPtr_flag']
        self.bundle.fromBpuNew.last_stage_spec_info.histPtr_value.value = dict['histPtr_value']
        self.bundle.fromBpuNew.last_stage_spec_info.ssp.value = dict['ssp']
        self.bundle.fromBpuNew.last_stage_spec_info.sctr.value = dict['sctr']
        self.bundle.fromBpuNew.last_stage_spec_info.TOSW_flag.value = dict['TOSW_flag']
        self.bundle.fromBpuNew.last_stage_spec_info.TOSW_value.value = dict['TOSW_value']
        self.bundle.fromBpuNew.last_stage_spec_info.TOSR_flag.value = dict['TOSR_flag']
        self.bundle.fromBpuNew.last_stage_spec_info.TOSR_value.value = dict['TOSR_value']
        self.bundle.fromBpuNew.last_stage_spec_info.NOS_flag.value = dict['NOS_flag']
        self.bundle.fromBpuNew.last_stage_spec_info.NOS_value.value = dict['NOS_value']
        self.bundle.fromBpuNew.last_stage_spec_info.topAddr.value = dict['topAddr']
        self.bundle.fromBpuNew.last_stage_spec_info.sc_disagree_0.value = dict['sc_disagree_0']
        self.bundle.fromBpuNew.last_stage_spec_info.sc_disagree_1.value = dict['sc_disagree_1']
        return self.bundle.as_dict()
    
    @driver_method()
    async def drive_last_stage_meta_signals(self):
        self.bundle.fromBpuNew.last_stage_meta.last_stage_meta.value = random.randint(0, (1 << 516) - 1)

    @driver_method()
    async def drive_backend_inputs_full(self, dict):
        b = self.bundle.fromBackend
        # simple direct mappings where fields are known to exist in FtqBundle.fromBackend
        if 'io_fromBackend_redirect_valid' in dict:
            b.redirect_valid.value = dict['io_fromBackend_redirect_valid']
        if 'io_fromBackend_redirect_bits_ftqIdx_flag' in dict:
            b.redirect_bits_ftqIdx_flag.value = dict['io_fromBackend_redirect_bits_ftqIdx_flag']
        if 'io_fromBackend_redirect_bits_ftqIdx_value' in dict:
            b.redirect_bits_ftqIdx_value.value = dict['io_fromBackend_redirect_bits_ftqIdx_value']
        if 'io_fromBackend_redirect_bits_ftqOffset' in dict:
            b.redirect_bits_ftqOffset.value = dict['io_fromBackend_redirect_bits_ftqOffset']
        if 'io_fromBackend_redirect_bits_level' in dict:
            b.redirect_bits_level.value = dict['io_fromBackend_redirect_bits_level']
        # cfi update fields (map to known names if present)
        if 'io_fromBackend_redirect_bits_cfiUpdate_target' in dict:
            b.redirect_bits_cfiUpdate_target.value = dict['io_fromBackend_redirect_bits_cfiUpdate_target']
        if 'io_fromBackend_redirect_bits_cfiUpdate_taken' in dict:
            b.redirect_bits_cfiUpdate_taken.value = dict['io_fromBackend_redirect_bits_cfiUpdate_taken']
        if 'io_fromBackend_redirect_bits_cfiUpdate_isMisPred' in dict:
            b.redirect_bits_cfiUpdate_isMisPred.value = dict['io_fromBackend_redirect_bits_cfiUpdate_isMisPred']
        # debug fields
        if 'io_fromBackend_redirect_bits_debugIsCtrl' in dict:
            b.redirect_bits_debugIsCtrl.value = dict['io_fromBackend_redirect_bits_debugIsCtrl']
        if 'io_fromBackend_redirect_bits_debugIsMemVio' in dict:
            b.redirect_bits_debugIsMemVio.value = dict['io_fromBackend_redirect_bits_debugIsMemVio']
        # ftq ahead / selector
        if 'io_fromBackend_ftqIdxAhead_0_valid' in dict:
            b.ftqIdxAhead_0_valid.value = dict['io_fromBackend_ftqIdxAhead_0_valid']
        if 'io_fromBackend_ftqIdxAhead_0_bits_value' in dict:
            b.ftqIdxAhead_0_bits_value.value = dict['io_fromBackend_ftqIdxAhead_0_bits_value']
        if 'io_fromBackend_ftqIdxSelOH_bits' in dict:
            b.ftqIdxSelOH_bits.value = dict['io_fromBackend_ftqIdxSelOH_bits']

        # For any extra cfi fields that may exist on the bundle, set them if present
        # e.g., cfiUpdate_pc, backendIGPF/IPF/IAF — only set if those attributes exist.
        try:
            if 'io_fromBackend_redirect_bits_cfiUpdate_pc' in dict and hasattr(b, 'redirect_bits_cfiUpdate_pc'):
                b.redirect_bits_cfiUpdate_pc.value = dict['io_fromBackend_redirect_bits_cfiUpdate_pc']
        except Exception:
            pass
        for extra in ('io_fromBackend_redirect_bits_cfiUpdate_backendIGPF',
                      'io_fromBackend_redirect_bits_cfiUpdate_backendIPF',
                      'io_fromBackend_redirect_bits_cfiUpdate_backendIAF'):
            if extra in dict:
                # try common attribute name pattern on bundle; ignore if not present
                attr = extra.replace('io_fromBackend_redirect_bits_', 'redirect_bits_')
                if hasattr(b, attr):
                    getattr(b, attr).value = dict[extra]

        # rob_commits: handle 0..7 RobCommitBundle entries if present in bundle and dict
        for i in range(8):
            rb_name = f'rob_commits_{i}'
            key_base = f'io_fromBackend_rob_commits_{i}_'
            if not hasattr(b, rb_name):
                continue
            rb = getattr(b, rb_name)
            if key_base + 'valid' in dict and hasattr(rb, 'valid'):
                rb.valid.value = dict[key_base + 'valid']
            if key_base + 'bits_commitType' in dict and hasattr(rb, 'bits_commitType'):
                rb.bits_commitType.value = dict[key_base + 'bits_commitType']
            if key_base + 'bits_ftqIdx_flag' in dict and hasattr(rb, 'bits_ftqIdx_flag'):
                rb.bits_ftqIdx_flag.value = dict[key_base + 'bits_ftqIdx_flag']
            if key_base + 'bits_ftqIdx_value' in dict and hasattr(rb, 'bits_ftqIdx_value'):
                rb.bits_ftqIdx_value.value = dict[key_base + 'bits_ftqIdx_value']
            if key_base + 'bits_ftqOffset' in dict and hasattr(rb, 'bits_ftqOffset'):
                rb.bits_ftqOffset.value = dict[key_base + 'bits_ftqOffset']

        return self.bundle.as_dict()

    @driver_method()
    async def drive_ifu_inputs_full(self, dict):
        f = self.bundle.fromIfu
        # top-level valid / ftqIdx fields
        if 'io_fromIfu_pdWb_valid' in dict:
            f.pdWb_valid.value = dict['io_fromIfu_pdWb_valid']
        if 'io_fromIfu_pdWb_bits_ftqIdx_flag' in dict:
            f.pdWb_bits_ftqIdx_flag.value = dict['io_fromIfu_pdWb_bits_ftqIdx_flag']
        if 'io_fromIfu_pdWb_bits_ftqIdx_value' in dict:
            f.pdWb_bits_ftqIdx_value.value = dict['io_fromIfu_pdWb_bits_ftqIdx_value']

        # pc entries
        for i in range(16):
            key = f"io_fromIfu_pdWb_bits_pc_{i}"
            attr = f"pdWb_bits_pc_{i}"
            if key in dict and hasattr(f, attr):
                getattr(f, attr).value = dict[key]

        # per-slot pd fields (brType, isCall, isRet, valid, isRVC) if present
        for i in range(16):
            base = f"pdWb_bits_pd_{i}"
            if hasattr(f, base):
                pd_obj = getattr(f, base)
                if f"io_fromIfu_pdWb_bits_pd_{i}_valid" in dict and hasattr(pd_obj, "valid"):
                    pd_obj.valid.value = dict[f"io_fromIfu_pdWb_bits_pd_{i}_valid"]
                if f"io_fromIfu_pdWb_bits_pd_{i}_isRVC" in dict and hasattr(pd_obj, "isRVC"):
                    pd_obj.isRVC.value = dict[f"io_fromIfu_pdWb_bits_pd_{i}_isRVC"]
                if f"io_fromIfu_pdWb_bits_pd_{i}_brType" in dict and hasattr(pd_obj, "brType"):
                    pd_obj.brType.value = dict[f"io_fromIfu_pdWb_bits_pd_{i}_brType"]
                if f"io_fromIfu_pdWb_bits_pd_{i}_isCall" in dict and hasattr(pd_obj, "isCall"):
                    pd_obj.isCall.value = dict[f"io_fromIfu_pdWb_bits_pd_{i}_isCall"]
                if f"io_fromIfu_pdWb_bits_pd_{i}_isRet" in dict and hasattr(pd_obj, "isRet"):
                    pd_obj.isRet.value = dict[f"io_fromIfu_pdWb_bits_pd_{i}_isRet"]

        # misOffset / cfiOffset / target / jalTarget / instrRange
        if 'io_fromIfu_pdWb_bits_misOffset_valid' in dict:
            f.pdWb_bits_misOffset_valid.value = dict['io_fromIfu_pdWb_bits_misOffset_valid']
        if 'io_fromIfu_pdWb_bits_misOffset_bits' in dict:
            f.pdWb_bits_misOffset_bits.value = dict['io_fromIfu_pdWb_bits_misOffset_bits']
        if 'io_fromIfu_pdWb_bits_cfiOffset_valid' in dict:
            f.pdWb_bits_cfiOffset_valid.value = dict['io_fromIfu_pdWb_bits_cfiOffset_valid']
        if 'io_fromIfu_pdWb_bits_target' in dict and hasattr(f, 'pdWb_bits_target'):
            f.pdWb_bits_target.value = dict['io_fromIfu_pdWb_bits_target']
        if 'io_fromIfu_pdWb_bits_jalTarget' in dict and hasattr(f, 'pdWb_bits_jalTarget'):
            f.pdWb_bits_jalTarget.value = dict['io_fromIfu_pdWb_bits_jalTarget']

        # instrRange entries if they exist on bundle
        for i in range(16):
            key = f"io_fromIfu_pdWb_bits_instrRange_{i}"
            attr = f"pdWb_bits_instrRange_{i}"
            if key in dict and hasattr(f, attr):
                getattr(f, attr).value = dict[key]

        return self.bundle.as_dict()