from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL

class pred_checker_mdl:
    def __init__(self):
        self.fixed_range = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_taken = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_miss_pred = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_target = [0 for i in range(PREDICT_WIDTH)]
        self.jal_target = [0 for i in range(PREDICT_WIDTH)]
        self.jumpOffset = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_flg = False # Indicate if pds has a valid CFI and checked if FTQ has corressponding prediction
        self.missed_flg = False  # Indicate if FTQ has a prediction and checked if pds has corressponding prediction

    # Use pds info to check if the pred_checker will report any error
    def ref_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        # Clear the previous result
        self.fixed_range = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_taken = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_miss_pred = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_target = [0 for i in range(PREDICT_WIDTH)]
        self.jal_target = [0 for i in range(PREDICT_WIDTH)]
        self.jumpOffset = [0 for i in range(PREDICT_WIDTH)]
        self.fixed_flg = False
        # Copy input jumpOffset
        self.jumpOffset = jumpOffset
        if not ftqValid:
            for idx in range(PREDICT_WIDTH):
                self.fixed_target[idx] = pc[idx] + 4 #default target = pc + 4
                self.fixed_range[idx] = 1
                self.fixed_taken[idx] = 0
                self.fixed_miss_pred[idx] = 0
                self.jal_target[idx] = pc[idx]
        else:
            for idx in range(PREDICT_WIDTH): # Check each instruction
                if instrValid[idx]: # if the instruction is a valid RVC/RVI instruction
                    self.fixed_target[idx] = pc[idx] + 4
                    self.jal_target[idx] = pc[idx] + jumpOffset[idx]
                else:
                    self.fixed_target[idx] = pc[idx] + 2
                    self.jal_target[idx] = pc[idx] + jumpOffset[idx] - 2
                if instrRange[idx]: 
                    self.fixed_range[idx] = 1
                if pds[idx][BRTYPE_LABEL] == 2: # if the instruction is a JAL instruction
                    if not self.fixed_flg and idx != ftqOffBits: # if FTQ didn't give JAL, report first CFI instruction
                        self.fixed_flg = True
                        if self.missed_flg: # if FTQ has a previous prediction but pds JAL is subsequent to it 
                            self.fixed_range[idx] = 0
                            self.fixed_miss_pred[idx] = 0
                        else :
                            self.fixed_range[idx] = 1
                            self.fixed_miss_pred[idx] = 1
                    elif not self.fixed_flg and idx == ftqOffBits: # if the first CFI instruction is corresponding to the ftqOffBits
                        self.fixed_miss_pred[idx] = 0
                        self.fixed_range[idx] = 1
                    self.fixed_taken[idx] = 1
                elif idx == ftqOffBits and pds[idx][BRTYPE_LABEL] != 2: # FTQ has a wrong prediction, pds gave no JAL
                    self.missed_flg = True 
                    self.fixed_miss_pred[idx] = 1
                else: # other non-CFI instruction
                    if not self.fixed_flg and instrRange[idx]: 
                        self.fixed_range[idx] = 1
                    else:
                        self.fixed_range[idx] = 0
                    if self.fixed_flg: # if reported a fix error, mark subsequent range/tanken/miss_pred as 0
                        self.fixed_miss_pred[idx] = 0
                        self.fixed_range[idx] = 0
                        self.fixed_taken[idx] = 0
        print("ref:fixed_target", self.fixed_target)
        return self.fixed_range, self.fixed_taken, self.fixed_miss_pred, self.fixed_target, self.jal_target