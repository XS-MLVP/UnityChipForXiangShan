from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL

class pred_checker_sqr:
    def __init__(self):
        pass
    
    def gen_vec(self, FTB_DEPTH, ):
        fire = True
        ftqValid = True
        ftqOffBits = FTB_DEPTH
        instrRange = [False for _ in range(FTB_DEPTH)]
        instrValid = [False for _ in range(FTB_DEPTH)]
        jumpOffset = [0 for _ in range(FTB_DEPTH)]
        pc = [0 for _ in range(FTB_DEPTH)]
        tgt = 0
        pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(FTB_DEPTH)]
        
        vec = [ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
        
        return vec