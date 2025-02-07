
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

TEST_CYCLES = 20

@toffee_test.testcase
async def test_renew_range_3_1(predchecker_env):
    print("Test 3.1: If prediction is correct, check instrRange")
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 2)
    vec_pkt.extend(sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 6))
    for i in range(TEST_CYCLES):
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
        ref_res = mdl.ref_pred_check(*vec_pkt[i])
        assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!! at vec_pkt[{i}]: stg1_fixedRange {stg1_fixedRange} != {ref_res[0]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!! at vec_pkt[{i}]: stg1_fixedTaken {stg1_fixedTaken} != {ref_res[1]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!! at vec_pkt[{i}]: stg2_fixedMissPred {stg2_fixedMissPred} != {ref_res[2]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!! at vec_pkt[{i}]: stg2_fixedTarget {stg2_fixedTarget} != {ref_res[3]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!! at vec_pkt[{i}]: stg2_jalTarget {stg2_jalTarget} != {ref_res[4]} \n\nvec_pkt[i]: {vec_pkt[i]}"
    del mdl, sqr

@toffee_test.testcase  
async def test_renew_range_3_2(predchecker_env):
    print("Test 3.2: RET/JAL prediction fault, pds gave a narrower range")
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 32)
    for i in range(TEST_CYCLES):
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
        ref_res = mdl.ref_pred_check(*vec_pkt[i])
        assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!! at vec_pkt[{i}]: stg1_fixedRange {stg1_fixedRange} != {ref_res[0]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!! at vec_pkt[{i}]: stg1_fixedTaken {stg1_fixedTaken} != {ref_res[1]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!! at vec_pkt[{i}]: stg2_fixedMissPred {stg2_fixedMissPred} != {ref_res[2]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!! at vec_pkt[{i}]: stg2_fixedTarget {stg2_fixedTarget} != {ref_res[3]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!! at vec_pkt[{i}]: stg2_jalTarget {stg2_jalTarget} != {ref_res[4]} \n\nvec_pkt[i]: {vec_pkt[i]}"
    del mdl, sqr
    
@toffee_test.testcase
async def test_renew_range_3_3(predchecker_env):
    print("Test 3.3: No-CFI/Invalid prediction, fixing range to the first CFI instruction")
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 33)
    for i in range(TEST_CYCLES):
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
        ref_res = mdl.ref_pred_check(*vec_pkt[i])
        print("\nftqOffbits: ", vec_pkt[i][1])
        print("\nref:fixed_range", ref_res[0])
        print("\nres:fixed_range", stg1_fixedRange)
        assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!! at vec_pkt[{i}]: stg1_fixedRange {stg1_fixedRange} != {ref_res[0]} \n\nvec_pkt[i]: {vec_pkt[i]} "
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!! at vec_pkt[{i}]: stg1_fixedTaken {stg1_fixedTaken} != {ref_res[1]} \n\nvec_pkt[i]: {vec_pkt[i]} "
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!! at vec_pkt[{i}]: stg2_fixedMissPred {stg2_fixedMissPred} != {ref_res[2]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!! at vec_pkt[{i}]: stg2_fixedTarget {stg2_fixedTarget} != {ref_res[3]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!! at vec_pkt[{i}]: stg2_jalTarget {stg2_jalTarget} != {ref_res[4]} \n\nvec_pkt[i]: {vec_pkt[i]}"
    del mdl, sqr