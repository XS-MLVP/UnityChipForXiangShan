from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL

class pred_checker_mdl:
    fixed_range = [0 for i in range(PREDICT_WIDTH)]
    fixed_taken = [0 for i in range(PREDICT_WIDTH)]
    fixed_miss_pred = [0 for i in range(PREDICT_WIDTH)]
    fixed_target = [0 for i in range(PREDICT_WIDTH)]
    jal_target = [0 for i in range(PREDICT_WIDTH)]
    
    def __init__(self):
        pass
    
    def ref_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        for rang_idx in range(PREDICT_WIDTH):
            self.fixed_target[rang_idx] = pc[rang_idx] + jumpOffset[rang_idx] #default 
            if(instrRange[rang_idx] & instrValid[rang_idx]): #if instr is marked as valid
                if(pds[rang_idx][BRTYPE_LABEL] == 0):
                    self.fixed_taken[rang_idx] = 0
                    self.fixed_miss_pred[rang_idx] = 0
        
        return self.fixed_range, self.fixed_taken, self.fixed_miss_pred, self.fixed_target, self.jal_target