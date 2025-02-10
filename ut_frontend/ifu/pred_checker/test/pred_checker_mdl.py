from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
'''PredChecker reference model'''
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
        # Clear the previous result if it exists
        for i in range(PREDICT_WIDTH):
            if instrRange[i]:
                self.fixedRange[i] = 1
            else:
                self.fixedRange[i] = 0
        self.fixedTaken = [0 for i in range(PREDICT_WIDTH)]
        self.fixedMisspred = [0 for i in range(PREDICT_WIDTH)]
        self.fixedTarget = [0 for i in range(PREDICT_WIDTH)]
        self.jalTarget = [0 for i in range(PREDICT_WIDTH)]
        
        # Generage fixedTarget and jalTarget
        for idx in range(PREDICT_WIDTH):
            if pds[idx][RVC_LABEL] or (not instrValid[idx]):
                self.fixedTarget[idx] = pc[idx]  + 2
                self.jalTarget[idx] = pc[idx] + jumpOffset[idx]
            else:
                self.fixedTarget[idx] = pc[idx] + 4
                self.jalTarget[idx] = pc[idx] + jumpOffset[idx]
        
        # Check missPred accroding to pds info
        cfi_idx = []
        for idx in range(PREDICT_WIDTH):
            # First determine whether this instruction is valid
            if instrValid[idx] and (pds[idx][RET_LABEL] or (pds[idx][BRTYPE_LABEL] > 0)):
                cfi_idx.extend([idx])
        if len(cfi_idx) != 0:
            cfi_idx.sort()
            self.fixedTaken[cfi_idx[0]] = 1
            if ftqValid and (cfi_idx[0] != ftqOffbits):
                self.fixedRange = [0 for _ in range(PREDICT_WIDTH)]
                if(cfi_idx[0] < ftqOffbits):
                    self.fixedMisspred[cfi_idx[0]] = 1
                    for i in range(cfi_idx[0] + 1):
                        self.fixedRange[i] = 1
                else:
                    self.fixedMisspred[ftqOffbits] = 1
                    for i in range(ftqOffbits + 1):
                        self.fixedRange[i] = 1
                    for i in range(PREDICT_WIDTH):
                        self.fixedTaken[i] = 0
            if (not pds[cfi_idx[0]][RET_LABEL]) and (pds[cfi_idx[0]][BRTYPE_LABEL] < 3):
            # Target fix includes 2 conditions:
            # 1. ftqOffbits is less than valid CFI index number;
            # 2. ftqOffbits equal to valid CFI index, but tgt not equal to pc[x] + jumpOffset[x].
                if ((pc[cfi_idx[0]] + jumpOffset[cfi_idx[0]]) != tgt) or (cfi_idx[0] < ftqOffbits):
                    self.fixedTarget[cfi_idx[0]] = self.jalTarget[cfi_idx[0]]
                    if cfi_idx[0] <= ftqOffbits:
                        self.fixedMisspred[cfi_idx[0]] = 1
        else:
            # pds do not exist CFI but FTQ gave a jumping prediction
            if ftqValid:
                self.fixedMisspred[ftqOffbits] = 1
                   
        return self.fixedRange, self.fixedTaken, self.fixedMisspred, self.fixedTarget, self.jalTarget
    
    