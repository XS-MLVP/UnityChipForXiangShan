from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL

class pred_checker_mdl:
    def __init__(self):
        self.fixedRange = [0 for i in range(PREDICT_WIDTH)]
        self.fixedTaken = [0 for i in range(PREDICT_WIDTH)]
        self.fixedMisspred = [0 for i in range(PREDICT_WIDTH)]
        self.fixedTarget = [0 for i in range(PREDICT_WIDTH)]
        self.jalTarget = [0 for i in range(PREDICT_WIDTH)]
        self.fixedFlg = False # Indicate if pds has a valid CFI and checked if FTQ has corressponding prediction
        self.missedFlg = False  # Indicate if FTQ has a prediction and checked if pds has corressponding prediction

    def ref_pred_check(self, ftqValid, ftqOffbits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        # Clear the previous result
        self.fixedRange = instrRange
        self.fixedTaken = [0 for i in range(PREDICT_WIDTH)]
        self.fixedMisspred = [0 for i in range(PREDICT_WIDTH)]
        self.fixedTarget = [0 for i in range(PREDICT_WIDTH)]
        self.jalTarget = [0 for i in range(PREDICT_WIDTH)]
        
        # Generage fixedTarget and jalTarget
        for idx in range(PREDICT_WIDTH):
            if jumpOffset[idx] == 0:
                stepFlg = 1
            else:
                stepFlg = 0
            if pds[idx][RVC_LABEL]:
                self.fixedTarget[idx] = pc[idx] + jumpOffset[idx] + 2 * stepFlg
                self.jalTarget[idx] = pc[idx] + jumpOffset[idx]
            else:
                self.fixedTarget[idx] = pc[idx] + jumpOffset[idx] + 4 * stepFlg
                self.jalTarget[idx] = pc[idx] + jumpOffset[idx]
        
        # Check missPred accroding to pds info
        cfi_pos = []
        for idx in range(PREDICT_WIDTH):
            # First determine whether this instruction is valid
            if instrValid[idx] and (pds[idx][RET_LABEL] or (pds[idx][BRTYPE_LABEL] > 0)):
                cfi_pos.extend([idx])
        if len(cfi_pos) != 0:
            cfi_pos.sort()
            #print(f"first cfi postition::{cfi_pos[0]}")
            self.fixedTaken[cfi_pos[0]] = 1
            if ftqValid and (cfi_pos[0] != ftqOffbits):
                self.fixedRange = [0 for _ in range(PREDICT_WIDTH)]
                if(cfi_pos[0] < ftqOffbits):
                    self.fixedMisspred[cfi_pos[0]] = 1
                else:
                    self.fixedMisspred[ftqOffbits] = 1
                for i in range(cfi_pos[0] + 1):
                    self.fixedRange[i] = 1
            else:
                # Pds and FTQ have same taken prediction(cfi_pos == ftqOffbits), check jump target
                if self.jalTarget[cfi_pos[0]] != tgt:
                    self.fixedMisspred[cfi_pos[0]] = 1
        else:
            # pds do not exist CFI but FTQ gave a jumping prediction
            if ftqValid:
                self.fixedMisspred[ftqOffbits] = 1
                   
        return self.fixedRange, self.fixedTaken, self.fixedMisspred, self.fixedTarget, self.jalTarget
    
    
    
    ## Use pds info to check if the pred_checker will report any error
    #def _ref_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
    #    # Clear the previous result
    #    self.fixedRange = [0 for i in range(PREDICT_WIDTH)]
    #    self.fixedTaken = [0 for i in range(PREDICT_WIDTH)]
    #    self.fixedMisspred = [0 for i in range(PREDICT_WIDTH)]
    #    self.fixedTarget = [0 for i in range(PREDICT_WIDTH)]
    #    self.jalTarget = [0 for i in range(PREDICT_WIDTH)]
    #    self.jumpOffset = [0 for i in range(PREDICT_WIDTH)]
    #    self.fixedFlg = False
    #    # Copy input jumpOffset
    #    self.jumpOffset = jumpOffset
    #    if not ftqValid:
    #        for idx in range(PREDICT_WIDTH):
    #            self.fixedTarget[idx] = pc[idx] + 4 #default target = pc + 4
    #            self.fixedRange[idx] = 1
    #            self.fixedTaken[idx] = 0
    #            self.fixedMisspred[idx] = 0
    #            self.jalTarget[idx] = pc[idx]
    #    else:
    #        for idx in range(PREDICT_WIDTH): # Check each instruction
    #            if instrRange[idx]: 
    #                self.fixedRange[idx] = 1
    #            if (pds[idx][BRTYPE_LABEL] >= 1) or (pds[idx][RET_LABEL] == True): # if the instruction is a BR/JAL/RET instruction
    #                if not self.fixedFlg and idx != ftqOffBits: # if FTQ didn't give JAL, report first CFI instruction
    #                    self.fixedFlg = True
    #                    if self.missedFlg: # if FTQ has a previous prediction but pds JAL is subsequent to it 
    #                        self.fixedMisspred[idx] = 0
    #                        self.missedFlg = False
    #                    else :
    #                        self.fixedMisspred[idx] = 1
    #                elif not self.fixedFlg and idx == ftqOffBits: # if the first CFI instruction is corresponding to the ftqOffBits
    #                    self.fixedMisspred[idx] = 0
    #                self.fixedTaken[idx] = 1
    #            # FTQ has a wrong prediction, pds gave no BR/JAL/RET
    #            elif idx == ftqOffBits and (pds[idx][BRTYPE_LABEL] < 1):                      
    #                if not self.fixedFlg:
    #                    # ftqOffset < pds CFI index
    #                    self.fixedMisspred[idx] = 1
    #                    self.missedFlg = True
    #                else:
    #                    self.fixedMisspred[idx] = 0
    #            else: # other non-CFI instruction
    #                if not self.fixedFlg and instrRange[idx]: # Copy instrRange to fixedRange if pred is correct
    #                    self.fixedRange[idx] = 1
    #                else:
    #                    self.fixedRange[idx] = 0
    #                if self.fixedFlg: # if reported a fix error, mark subsequent tanken/miss_pred as 0
    #                    self.fixedMisspred[idx] = 0
    #                    self.fixedTaken[idx] = 0
    #            if instrValid[idx]: # if the instruction is a valid RVC/RVI instruction
    #                pcStep = 4
    #            else:
    #                pcStep = 2
    #            if self.fixedFlg:
    #                self.fixedTarget[idx] = pc[idx] + jumpOffset[idx] + pcStep
    #                if pds[idx][BRTYPE_LABEL] == 2:
    #                    self.jalTarget[idx] = pc[idx] + jumpOffset[idx] + pcStep
    #            else:
    #                self.fixedTarget[idx] = pc[idx] + pcStep
    #                self.jalTarget[idx] = pc[idx]
    #        if self.fixedFlg:
    #            index = 0
    #            while index < PREDICT_WIDTH:
    #                if self.fixedTaken[index] == 1:
    #                    break
    #                index += 1
    #            index += 1
    #            self.fixedRange = [1] * (index) + [0] * (PREDICT_WIDTH - index)
    #                
    #    #print("ref:fixedTarget", self.fixedTarget)
    #    return self.fixedRange, self.fixedTaken, self.fixedMisspred, self.fixedTarget, self.jalTarget