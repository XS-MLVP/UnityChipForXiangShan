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
            rand_pc = random.randint(0, 2**50 - 64)
            pc = [rand_pc + i*4 for i in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            #for i in range(PREDICT_WIDTH): # make sure the jump target is not out of range
            #    while(pc[i] + jumpOffset[i] > 2**50 - 1):
            #        jumpOffset[i] = random.randint(0, 2**50-1)
            tgt = pc[PREDICT_WIDTH - 1] + 1 
            
            
        # Pds has JAL info;  insrRange&instrValid is corresponding to JAL info;
        # Check if the pred_checker will report a JAL missed prediction
        elif(case_id == 2):    
            print("Case 2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            rand_offset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[rand_offset] = {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}
            ftqValid = True
            ftqOffBits = rand_offset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            jumpOffset[rand_offset] = random.randint(0, 2**50 - pc[rand_offset])
            tgt = pc[rand_offset] + jumpOffset[rand_offset]
        
        elif(case_id == 3):
            print("Case 3: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            rand_offset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            ftqValid = True
            ftqOffBits = rand_offset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            # Cause we are testing a wrong prediction, so tgt is not cared.
            tgt = pc[rand_offset] + random.randint(0, 2**50 - pc[rand_offset]) 
        
        elif(case_id == 4):
            print("Case 4: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(0, 14)
            rand_offset = random.randint(1, 15)
            while rand_offset <= ftqOffBits:
                rand_offset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[rand_offset] = {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[rand_offset] = 200#random.randint(0, 2**50 - pc_0)
            pc = [pc_0 + i*4 for i in range(PREDICT_WIDTH)]
            tgt = pc_0 + jumpOffset[rand_offset]
            
        else:
            pass
        vec = [ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
        #print("Generated test vector: ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire\n", vec)
        return vec