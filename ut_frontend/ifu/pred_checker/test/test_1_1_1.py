import os
import sys
import random

import toffee.funcov as fc
from toffee.funcov import CovGroup
import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
from .pred_checker_mdl import pred_checker_mdl


@toffee_test.testcase
async def test_jal_error_1_1_1_single(predchecker_env):
    print("Test 1.1.1(single): Report fault jal pred error")
    mdl = pred_checker_mdl()
    fire = True
    ftqValid = True
    ftqOffBits = 0xf # ftb width 16
    instrRange = [False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    instrValid = [True for _ in range(PREDICT_WIDTH)]
    jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
    rand_pc = random.sample(range(0, 2**50-1), PREDICT_WIDTH)
    pc = sorted(rand_pc)
    tgt = pc[15] + 1
    pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
    async for res in  predchecker_env.predCheckerAgent.agent_pred_check(
        ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire
    ):
        if len(res) == 2:
            stg1_fixedRange, stg1_fixedTaken = res
            print(f"Stage 1 Fixed Range: {stg1_fixedRange}")
            print(f"Stage 1 Fixed Taken: {stg1_fixedTaken}")
        elif len(res) == 3:
            stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred = res
            print(f"Stage 2 Fixed Target: {stg2_fixedTarget}")
            print(f"Stage 2 JAL Target: {stg2_jalTarget}")
            print(f"Stage 2 Fixed Miss Prediction: {stg2_fixedMissPred}")
    # Check the result: Is JAL fix reported
    ref_res = mdl.ref_pred_check(ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire)
    assert res[2] == ref_res[2], f"Pred Checker Fixed Taken error!!!: res[2](Fixed Miss Prediction){res[2]} != {ref_res[2]}"
    print("Test Done")
    
async def test_jal_error_1_1_1(predcheker_env):
    print("Test 1.1.1: Report fault jal pred error")
    mdl = pred_checker_mdl()