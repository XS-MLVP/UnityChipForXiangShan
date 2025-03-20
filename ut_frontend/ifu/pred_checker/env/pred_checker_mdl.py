from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from toffee.model import *
from ..bundle import PredCheckerBundle
'''PredChecker reference model'''

class PredCheckerModel(Model):
    def __init__(self):
        super().__init__()
        self.fixedRange = [0 for _ in range(PREDICT_WIDTH)]
        self.fixedTarget = [0 for _ in range(PREDICT_WIDTH)]
        self.fixedMisspred = [0 for _ in range(PREDICT_WIDTH)]
        self.fixedTarget = [0 for _ in range(PREDICT_WIDTH)]
        self.jalTarget = [0 for _ in range(PREDICT_WIDTH)]

    @driver_hook(agent_name="predCheckerAgent", driver_name="agent_pred_check")
    async def ref_pred_check(self, ftqValid, ftqOffbits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):
        # Store input
        self.ftqValid = ftqValid
        self.ftqOffbits = ftqOffbits
        self.instrRange = instrRange
        self.instrValid = instrValid
        self.jumpOffset = jumpOffset
        self.pc = pc
        self.pds = pds
        self.tgt = tgt
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
        
        # Generate fixedTarget and jalTarget
        for idx in range(PREDICT_WIDTH):
            if pds[idx][RVC_LABEL] or (not instrValid[idx]):
                self.fixedTarget[idx] = pc[idx]  + 2
                self.jalTarget[idx] = pc[idx] + jumpOffset[idx]
            else:
                self.fixedTarget[idx] = pc[idx] + 4
                self.jalTarget[idx] = pc[idx] + jumpOffset[idx]
        # Overflow condition
        for i in range(PREDICT_WIDTH):
            if self.jalTarget[i] >= 2**50:
                self.jalTarget[i] = self.jalTarget[i] - 2**50
                
        # Check missPred accroding to pds info
        cfi_idx = []
        for idx in range(PREDICT_WIDTH):
            # First determine whether this instruction is valid
            if instrValid[idx] and (pds[idx][RET_LABEL] or (pds[idx][BRTYPE_LABEL] > 0)):
                cfi_idx.extend([idx])
        
        # if pds gave a valid instr info
        if len(cfi_idx) != 0:
            cfi_idx.sort()
            self.fixedTaken[cfi_idx[0]] = 1
            if ftqValid and (cfi_idx[0] != ftqOffbits):
                self.fixedRange = [0 for _ in range(PREDICT_WIDTH)]
                if(cfi_idx[0] < ftqOffbits): # Renew range
                    self.fixedMisspred[cfi_idx[0]] = 1
                    for i in range(cfi_idx[0] + 1):
                        self.fixedRange[i] = 1
                else:
                    self.fixedMisspred[ftqOffbits] = 1
                    for i in range(ftqOffbits + 1):
                        self.fixedRange[i] = 1
                    for i in range(PREDICT_WIDTH):
                        self.fixedTaken[i] = 0
                    if(pds[cfi_idx[0]][BRTYPE_LABEL] == 3) and (not pds[cfi_idx[0]][RET_LABEL]):
                        for i in range(PREDICT_WIDTH):
                            if(instrRange[i]):
                                self.fixedRange[i] = 1
                        self.fixedTaken[cfi_idx[0]] = 1
            if not ftqValid:
                self.fixedRange = [1 for _ in range(cfi_idx[0] + 1)]
                self.fixedRange.extend([0 for _ in range(PREDICT_WIDTH - cfi_idx[0] - 1)])
                self.fixedMisspred[cfi_idx[0]] = 1
            # Target check for JAL and BR instr
            if (not pds[cfi_idx[0]][RET_LABEL]) and (pds[cfi_idx[0]][BRTYPE_LABEL] < 3):
            # Target fix includes 2 conditions:
            # 1. ftqOffbits is larger than valid CFI index number;
            # 2. ftqOffbits equal to valid CFI index, but tgt not equal to pc[x] + jumpOffset[x].
                pds_tgt = pc[cfi_idx[0]] + jumpOffset[cfi_idx[0]]
                if pds_tgt >= 2**50: # If target overflow
                    pds_tgt = pds_tgt - 2**50
                if (self.instrRange[cfi_idx[0]] == 1) \
                    and ((pds_tgt != tgt) or (cfi_idx[0] < ftqOffbits)) \
                    or (not ftqValid):
                    self.fixedTarget[cfi_idx[0]] = self.jalTarget[cfi_idx[0]]
                    if cfi_idx[0] <= ftqOffbits:
                        self.fixedMisspred[cfi_idx[0]] = 1
        else:
            # pds do not exist CFI but FTQ gave a jumping prediction
            if ftqValid:
                self.fixedMisspred[ftqOffbits] = 1
    
        for i in range(PREDICT_WIDTH):
            if self.fixedTarget[i] >= 2**50:
                self.fixedTarget[i] = self.fixedTarget[i] - 2**50
        stg1_fixedRange = self.fixedRange
        stg1_fixedTaken = self.fixedTaken
        stg2_fixedTarget = self.fixedTarget
        stg2_jalTarget = self.jalTarget
        stg2_fixedMissPred = self.fixedMisspred
        
        return stg1_fixedRange, stg1_fixedTaken, stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred 
    
    