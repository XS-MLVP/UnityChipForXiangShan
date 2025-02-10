from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
import random

class pred_checker_sqr:
    def __init__(self):
        pass
    
    def gen_vec(self, PREDICT_WIDTH, vec_depth, caseId):
        vec_pkt = [self._gen_vec_single(PREDICT_WIDTH, caseId) for _ in range(vec_depth)]        
        return vec_pkt
    
    def _gen_vec_single(self, PREDICT_WIDTH, caseId):
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
        if(caseId == 1):
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: random.choice([0]) } for i in range(PREDICT_WIDTH)]
            instrRange = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            instrValid = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            pc_0 = random.randint(0, 2**50 - 64)
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[PREDICT_WIDTH - 1] + 1 
            
            
        # Pds has JAL info;  insrRange&instrValid is corresponding to JAL info;
        # Check if the pred_checker will report a JAL missed prediction
        elif(caseId == 2):    
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
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
        
        elif(caseId == 3):
            #print("Case 1.2.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            # Cause we are testing a wrong prediction, so tgt is not cared.
            tgt = pc[randOffset] + random.randint(0, 2**50 - pc[randOffset]) 
        
        elif(caseId == 4):
            #print("Case 1.2.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(1, 15)
            randOffset = random.randint(0, 14)
            while randOffset >= ftqOffBits:
                randOffset = random.randint(0, 14)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + jumpOffset[randOffset]
        elif(caseId == 21):
            #print("Case 2.1.1: generate test vector") 
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: random.choice([0]) } for i in range(PREDICT_WIDTH)]
            instrRange = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            instrValid = [random.choice([True]) for _ in range(PREDICT_WIDTH)]
            pc_0 = random.randint(0, 2**50 - 64)
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[PREDICT_WIDTH - 1] + 1 

        elif(caseId == 22):
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
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
        elif(caseId == 23):
            #print("Case 2.2.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + random.randint(0, 2**50 - pc[randOffset]) 
        
        elif(caseId == 24):
            #print("Case 2.2.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(1, 15)
            randOffset = random.randint(0, 14)
            while randOffset >= ftqOffBits:
                randOffset = random.randint(0, 14)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + jumpOffset[randOffset]
            
        elif(caseId == 32):
            #print("Case 3.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(0, 14)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}, 
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            while ftqOffBits <= randOffset:
                ftqOffBits = random.randint(1, 15)
            instrRange = [True for _ in range(ftqOffBits + 1)]
            instrRange.extend([False for _ in range(PREDICT_WIDTH - 1 - ftqOffBits)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + 200 # Cause we are testing a wrong prediction, so tgt is not cared.
            
        elif(caseId == 33):
            #print("Case 3.3: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(1, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}, 
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            while ftqOffBits >= randOffset:
                ftqOffBits = random.randint(0, 14)
            instrRange = [True for _ in range(ftqOffBits + 1)]
            instrRange.extend([False for _ in range(PREDICT_WIDTH - ftqOffBits - 1)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + jumpOffset[randOffset]
        
        elif(caseId == 41):
            #print("Case 4.1.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = False
            randOffset = random.randint(0, 15)
            ftqOffBits = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + 200 # Cause we are testing no-jumping case, so tgt is not cared.
        
        elif(caseId == 42):
            #print("Case 4.1.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: False, RET_LABEL:False, BRTYPE_LABEL:1}])
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
            
        elif(caseId == 43):
            #print("Case 4.2")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + 200 # Cause the case has to generate a fault prediction, so tgt is not cared.
            
        elif(caseId == 51):
            #print("Case 5.1.1")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = False
            ftqOffBits = 0
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + 200 # Cause the case has to generate no-jumping prediction, so tgt is not cared.
            
        elif(caseId == 52):
            #print("Case 5.1.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = False
            ftqOffBits = 0
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            instrValid[randOffset] = False
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc_0 + 200 # Cause the case has to generate no-jumping prediction, so tgt is not cared.
            
        elif(caseId == 53):
            #print("Case 5.1.3")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: random.choice([True, False]), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL:False, BRTYPE_LABEL:1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0 - 2**6)
            tgt = pc[randOffset] + jumpOffset[randOffset]
        
        elif(caseId == 54):
            #print("Case 5.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            instrValid[randOffset] = False
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0}
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[randOffset] + jumpOffset[randOffset]
        
        elif(caseId == 61):
            #print("Case 6.1.1") 
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0}
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[randOffset] + jumpOffset[randOffset]
            
        elif(caseId == 62):
            #print("Case 6.1.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: random.choice([True, False]), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL:False, BRTYPE_LABEL:1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(4, 2**50 - pc_0)
            tgt = pc[randOffset] + jumpOffset[randOffset]
            
        elif(caseId == 63):
            #print("Case 6.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: random.choice([True, False]), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL:False, BRTYPE_LABEL:1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(4, 2**50 - pc_0)
            tgt = pc[randOffset] + jumpOffset[randOffset] + 10086
        
        elif(caseId == 71):
            #print("Case 7.1")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [random.choice([True, False]) for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: random.choice([True, False]), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: random.choice([True, False]), RET_LABEL:False, BRTYPE_LABEL:1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(4, 2**50 - pc[PREDICT_WIDTH - 1])
            tgt = pc[randOffset] + jumpOffset[randOffset]
            
            
        else:
            for i in range(10):
                print("Invalid case number")
        
        vec = [ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
        #print("Generated test vector: ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire\n", vec)
        return vec
    
    def _gen_pc_list(self, pc_0, pds_info):
        pc = [0 for i in range(PREDICT_WIDTH)]
        for i in range(PREDICT_WIDTH - 1):
            pc[0] = pc_0;
            if pds_info[i][RVC_LABEL] == False:
                pc[i + 1] = pc[i] + 4
            else:
                pc[i + 1] = pc[i] + 2
        return pc