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
from .pred_checker_sqr import pred_checker_sqr

@toffee_test.testcase
async def test_jal_error_1_1_2_single(predchecker_env):
    print("Test 1.1.2(single): Report fault jal pred error")
    mdl = pred_checker_mdl()
    fire = True
    ftqValid = True
    ftqOffBits = 0xe
    instrRange = [True for _ in range(PREDICT_WIDTH)]
    instrValid = [True for _ in range(PREDICT_WIDTH)]
    jumpOffset = [0 for _ in range(PREDICT_WIDTH)]
    jumpOffset[14] = 0x8
    rand_pc = 0#random.randint(0, 2**50 - 64)
    pc = [rand_pc + i*4 for i in range(PREDICT_WIDTH)]
    tgt = pc[14] + jumpOffset[14]
    pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
    pds[14] = {RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2}
    instrRange[15] = False
    print("pds: \n", pds)
    print("pc: \n", pc)
    print("instrRange: \n", instrRange)
    print("instrValid: \n", instrValid)
    print("jumpOffset: \n", jumpOffset)
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
    print("\nref:fixed_range", ref_res[0])
    print("\nref:fixed_taken", ref_res[1])
    print("\nref:fixed_miss_pred", ref_res[2])    
    print("\nref:fixed_target", ref_res[3])
    print("\nref:jal_target", ref_res[4])
    assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!!: stg1_fixedRange{stg1_fixedRange} != {ref_res[0]}"
    assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!!: stg1_fixedTaken{stg1_fixedTaken} != {ref_res[1]}"
    assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!!: stg2_fixedMissPred{stg2_fixedMissPred} != {ref_res[2]}"
    #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!!: stg2_fixedTarget{stg2_fixedTarget} != {ref_res[3]}"
    #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!!: stg2_jalTarget{stg2_jalTarget} != {ref_res[4]}"
    del mdl
    
@toffee_test.testcase
async def test_1_1_2(predchecker_env):
    print("Test 1.1.2")
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, 1000, 2)
    for i in range(len(vec_pkt)):
        print(f"Test cycle {i}")
        async for res in predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i]):
            if len(res) == 2:
                stg1_fixedRange, stg1_fixedTaken = res
                #print(f"Stage 1 Fixed Range: {stg1_fixedRange}")
                #print(f"Stage 1 Fixed Taken: {stg1_fixedTaken}")
            elif len(res) == 3:
                stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred = res
                #print(f"Stage 2 Fixed Target: {stg2_fixedTarget}")
                #print(f"Stage 2 JAL Target: {stg2_jalTarget}")
                #print(f"Stage 2 Fixed Miss Prediction: {stg2_fixedMissPred}")
        # Check the result: Is JAL fix reported
        ref_res = mdl.ref_pred_check(*vec_pkt[i])
        assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!! at vec_pkt[{i}]: stg1_fixedRange {stg1_fixedRange} != {ref_res[0]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!! at vec_pkt[{i}]: stg1_fixedTaken {stg1_fixedTaken} != {ref_res[1]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!! at vec_pkt[{i}]: stg2_fixedMissPred {stg2_fixedMissPred} != {ref_res[2]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!! at vec_pkt[{i}]: stg2_fixedTarget {stg2_fixedTarget} != {ref_res[3]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!! at vec_pkt[{i}]: stg2_jalTarget {stg2_jalTarget} != {ref_res[4]} \n\nvec_pkt[i]: {vec_pkt[i]}"
    del mdl, sqr