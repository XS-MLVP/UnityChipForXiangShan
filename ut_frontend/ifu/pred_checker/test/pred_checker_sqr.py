from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
import random

class pred_checker_sqr:
    def __init__(self):
        pass
    
    def gen_vec(self, PREDICT_WIDTH, vec_depth, case_id):
        vec_pkt = [self._gen_vec_single(PREDICT_WIDTH, case_id) for _ in range(vec_depth)]        
        return vec_pkt
    
    def _gen_vec_single(self, PREDICT_WIDTH, case_id):
        fire = True
        ftqValid = False
        ftqOffBits = random.randint(0, 15)
        instrRange = [False for _ in range(PREDICT_WIDTH)]
        instrValid = [False for _ in range(PREDICT_WIDTH)]
        jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
        pc = [0 for _ in range(PREDICT_WIDTH)]
        tgt = 0
        pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
        
        # Pds has no JAL info; instrRange is False; instrValid is False;
        # Check if the pred_checker will report a JAL missed prediction
        if(case_id == 1):
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: random.choice([0]) } for i in range(PREDICT_WIDTH)]
            instrRange = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            instrValid = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            randPc = random.randint(0, 2**50 - 64)
            pc = [randPc + i*4 for i in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[PREDICT_WIDTH - 1] + 1 
            
            
        # Pds has JAL info;  insrRange&instrValid is corresponding to JAL info;
        # Check if the pred_checker will report a JAL missed prediction
        elif(case_id == 2):    
            #print("Case 1.1.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
        
        elif(case_id == 3):
            #print("Case 1.2.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            # Cause we are testing a wrong prediction, so tgt is not cared.
            tgt = pc[randOffset] + random.randint(0, 2**50 - pc[randOffset]) 
        
        elif(case_id == 4):
            #print("Case 1.2.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(0, 14)
            randOffset = random.randint(1, 15)
            while randOffset <= ftqOffBits:
                randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            tgt = pc_0 + jumpOffset[randOffset]
        elif(case_id == 5):
            #print("Case 2.1.1: generate test vector") 
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: random.choice([0]) } for i in range(PREDICT_WIDTH)]
            instrRange = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            instrValid = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            randPc = random.randint(0, 2**50 - 64)
            pc = [randPc + i*4 for i in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[PREDICT_WIDTH - 1] + 1 

        elif(case_id == 6):
            #print("Case 2.1.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
        elif(case_id == 7):
            #print("Case 2.2.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            # Cause we are testing a wrong prediction, so tgt is not cared.
            tgt = pc[randOffset] + random.randint(0, 2**50 - pc[randOffset]) 
        
        elif(case_id == 8):
            #print("Case 2.2.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(0, 14)
            randOffset = random.randint(1, 15)
            while randOffset <= ftqOffBits:
                randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            tgt = pc_0 + jumpOffset[randOffset]
            
        elif(case_id == 32):
            #print("Case 3.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(0, 14)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}, 
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            while ftqOffBits <= randOffset:
                ftqOffBits = random.randint(1, 15)
            instrRange = [True for _ in range(ftqOffBits)]
            instrRange.extend([False for _ in range(PREDICT_WIDTH - ftqOffBits)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            tgt = pc_0 + 200 # Cause we are testing a wrong prediction, so tgt is not cared.
            
        elif(case_id == 33):
            #print("Case 3.3: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(1, 15)
            print("randOffset: ", randOffset)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}, 
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            while ftqOffBits >= randOffset:
                ftqOffBits = random.randint(0, 14)
            instrRange = [True for _ in range(ftqOffBits)]
            instrRange.extend([False for _ in range(PREDICT_WIDTH - ftqOffBits)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            tgt = pc_0 + 200
        else:
            pass
        
        vec = [ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
        #print("Generated test vector: ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire\n", vec)
        return vec