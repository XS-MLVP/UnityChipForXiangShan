from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
import random


class pred_checker_sqr:
    latest_vec_pkt = None

    def __init__(self):
        pass

    def gen_vec(self, PREDICT_WIDTH, vec_depth, caseId):
        vec_pkt = [self._gen_vec_single(PREDICT_WIDTH, caseId)
                   for _ in range(vec_depth)]
        self.latest_vec_pkt = vec_pkt
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
        pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
               for i in range(PREDICT_WIDTH)]

        if caseId in (1, 21, 31, 51, 61):
            # print("Case 1.1.1/2.1.1/3.1.1/5.1.1/6.1.1: generate test vector")
            ftqValid = False
            ftqOffBits = 0
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pc_0 = random.randint(0, 2**50 - 64)
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            # tgt = pc[PREDICT_WIDTH - 1] + 1
            # Cause the case has to generate a fault prediction, so tgt is not cared.
            tgt = pc_0 + 114514

        elif caseId in (2, 22, 32):
            # print("Case 1.1.2/2.1.2/3.1.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            if (caseId == 2):
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: False, BRTYPE_LABEL: 2}
            elif (caseId == 22):
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: True, BRTYPE_LABEL: 3}
            else:
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: False, BRTYPE_LABEL: 3}
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif caseId in (3, 23, 33):
            # print("Case 1.2.1/2.2.1/3.2.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            ftqValid = False
            ftqOffBits = 0
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            if (caseId == 3):
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: False, BRTYPE_LABEL: 2}
            elif (caseId == 23):
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: True, BRTYPE_LABEL: 3}
            else:
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: False, BRTYPE_LABEL: 3}
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            pc = self._gen_pc_list(pc_0, pds)
            # Cause we are testing a wrong prediction, so tgt is not cared.
            tgt = pc[randOffset] + random.randint(0, 2**50 - pc[randOffset])

        elif caseId in (4, 24, 34):
            # print("Case 1.2.2/2.2.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(1, 15)
            randOffset = random.randint(0, 14)
            while randOffset >= ftqOffBits:
                randOffset = random.randint(0, 14)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            if (caseId == 4):
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: False, BRTYPE_LABEL: 2}
            elif (caseId == 24):
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: True, BRTYPE_LABEL: 3}
            else:
                pds[randOffset] = {RVC_LABEL: False,
                                   RET_LABEL: False, BRTYPE_LABEL: 3}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 33):
            # print("Case 3.2.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            ftqValid = False
            ftqOffBits = 0
            pds[randOffset] = {RVC_LABEL: False,
                               RET_LABEL: False, BRTYPE_LABEL: 3}
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + random.randint(0, 2**50 - pc[randOffset])

        elif (caseId == 41):
            # print("Case 4.1: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(0, 14)
            ftqOffBits = randOffset
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2},
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            instrRange = [True for _ in range(ftqOffBits + 1)]
            instrRange.extend(
                [False for _ in range(PREDICT_WIDTH - 1 - ftqOffBits)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + jumpOffset[randOffset]

        elif (caseId == 42):
            # print("Case 4.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(0, 14)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2},
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            while ftqOffBits <= randOffset:
                ftqOffBits = random.randint(1, 15)
            instrRange = [True for _ in range(ftqOffBits + 1)]
            instrRange.extend(
                [False for _ in range(PREDICT_WIDTH - 1 - ftqOffBits)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            # Cause we are testing a wrong prediction, so tgt is not cared.
            tgt = pc_0 + 114514

        elif (caseId == 43):
            # print("Case 4.3: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            randOffset = random.randint(1, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2},
                                            {RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3}])
            while ftqOffBits >= randOffset:
                ftqOffBits = random.randint(0, 14)
            instrRange = [True for _ in range(ftqOffBits + 1)]
            instrRange.extend(
                [False for _ in range(PREDICT_WIDTH - ftqOffBits - 1)])
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 52):
            # print("Case 5.1.2: generate test vector")
            pc_0 = random.randint(0, 2**50 - 2**6)
            randOffset = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: False, RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: False, RET_LABEL: False,
                                                 BRTYPE_LABEL: 2},
                                             {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 1}])
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc[randOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 53):
            # print("Case 5.2")
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = random.randint(0, 15)
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for i in range(PREDICT_WIDTH)]
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc_0 + 114514

        elif (caseId == 62):
            # print("Case 6.1.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = False
            ftqOffBits = 0
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            instrValid[randOffset] = False
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            # randOffset_1: true jump instr location
            if randOffset != 15:
                randOffset_1 = random.randint(randOffset + 1, 15)
                pds[randOffset_1] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                                   {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 2}])
                # {RVC_LABEL: not random.getrandbits(1), RET_LABEL:False, BRTYPE_LABEL:1}])
                jumpOffset[randOffset_1] = random.randint(
                    0, 2**50 - pc_0 - 2**6)
                tgt = pc[randOffset_1] + jumpOffset[randOffset_1]
            else:
                tgt = pc[randOffset]

        elif (caseId == 63):
            # print("Case 6.1.3")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2**6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(PREDICT_WIDTH)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice(
                                                 [True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(0, 2**50 - pc_0 - 2**6)
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 64):
            # print("Case 6.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            # randOffset: fault prediction location
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            instrValid[randOffset] = False
            pds = [{RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0}
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            # randOffset_1: true jump instr location
            if randOffset != 15:
                randOffset_1 = random.randint(randOffset + 1, 15)
                pds[randOffset_1] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                                   {RVC_LABEL: random.choice(
                                                       [True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                                   {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 1}])
                jumpOffset[randOffset_1] = random.randint(
                    0, 2**50 - pc_0 - 2**6)
            pc = self._gen_pc_list(pc_0, pds)
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 71):
            # print("Case 7.1.1")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0}
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 72):
            # print("Case 7.1.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice(
                                                 [True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(4, 2**50 - pc_0)
            tgt = pc[randOffset] + jumpOffset[randOffset]

        elif (caseId == 73):
            # print("Case 7.2")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: random.choice(
                [True, False]), RET_LABEL: False, BRTYPE_LABEL: 0} for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice(
                                                 [True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(4, 2**50 - pc_0)
            tgt = pc[randOffset] + jumpOffset[randOffset] + 114514

        elif (caseId == 81):
            # print("Case 8")
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(0, 2**50 - 2 ** 6)
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [not random.getrandbits(1)
                          for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice(
                                                 [True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            negJumpOffset = - 2**50
            while (negJumpOffset + pc_0 < 0):
                negJumpOffset = random.randint(-(2**50), -4)
            posJumpOffset = random.randint(4, 2**50 - pc[PREDICT_WIDTH - 1])
            jumpOffset[randOffset] = random.choice(
                [negJumpOffset, posJumpOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
            if tgt >= 2**50:
                tgt = tgt - 2**50

        elif (caseId == 82):
            # Case 8 with additional target boundary test
            randOffset = random.randint(0, 15)
            pc_0 = random.randint(
                2**50 - 2 ** 8, 2**50 - 2**6 - 1)  # boundary pc
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [not random.getrandbits(1)
                          for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = random.choice([{RVC_LABEL: not random.getrandbits(1), RET_LABEL: True, BRTYPE_LABEL: 3},
                                             {RVC_LABEL: random.choice(
                                                 [True, False]), RET_LABEL: False, BRTYPE_LABEL: 2},
                                             {RVC_LABEL: not random.getrandbits(1), RET_LABEL: False, BRTYPE_LABEL: 1}])
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            negJumpOffset = - 2**50
            while (negJumpOffset + pc_0 < 0):
                negJumpOffset = random.randint(-(2**50), -4)
            posJumpOffset = random.randint(4, 2**50 - pc[PREDICT_WIDTH - 1])
            jumpOffset[randOffset] = random.choice(
                [negJumpOffset, posJumpOffset])
            tgt = pc[randOffset] + jumpOffset[randOffset]
            if tgt >= 2**50:
                tgt = tgt - 2**50

        elif (caseId == 83):
            # Case 8 with additional target boundary test: overflow
            randOffset = random.randint(0, 15)
            pc_0 = 2**50 - random.randint(1, 65)  # boundary pc
            ftqValid = True
            ftqOffBits = randOffset
            instrRange = [True for _ in range(
                randOffset + 1)] + [False for _ in range(PREDICT_WIDTH - randOffset - 1)]
            instrValid = [True for _ in range(PREDICT_WIDTH)]
            pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0}
                   for _ in range(PREDICT_WIDTH)]
            pds[randOffset] = {RVC_LABEL: False,
                               RET_LABEL: False, BRTYPE_LABEL: 2}
            pc = self._gen_pc_list(pc_0, pds)
            jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
            jumpOffset[randOffset] = random.randint(66, 128)
            tgt = pc[randOffset] + jumpOffset[randOffset]
            if tgt >= 2**50:
                tgt = tgt - 2**50

        else:
            print(f"Invalid case number, caseId == {caseId}")
            assert caseId == -1, "caseId error"

        vec = [ftqValid, ftqOffBits, instrRange,
               instrValid, jumpOffset, pc, pds, tgt, fire]
        # print("Generated test vector: ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire\n", vec)
        return vec

    def _gen_pc_list(self, pc_0, pds_info):
        pc = [0 for i in range(PREDICT_WIDTH)]
        for i in range(PREDICT_WIDTH - 1):
            pc[0] = pc_0
            if pds_info[i][RVC_LABEL] == False:
                pc[i + 1] = pc[i] + 4
            else:
                pc[i + 1] = pc[i] + 2
        return pc
