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

TEST_CYCLES = 10000

@toffee_test.testcase 
async def test_ret_chk_2_1_1(predchecker_env):
    res = []
    ref_res = []
    mdl = pred_checker_mdl()
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 5)
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
        assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!!: stg1_fixedRange{stg1_fixedRange} != {ref_res[0]}"
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!!: stg1_fixedTaken{stg1_fixedTaken} != {ref_res[1]}"
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!!: stg2_fixedMissPred{stg2_fixedMissPred} != {ref_res[2]}"
        #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!!: stg2_fixedTarget{stg2_fixedTarget} != {ref_res[3]}"
        #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!!: stg2_jalTarget{stg2_jalTarget} != {ref_res[4]}"
    del mdl, sqr
    
@toffee_test.testcase
async def test_ret_chk_2_1_2(predchecker_env):
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 6)
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
    
@toffee_test.testcase
async def test_ret_chk_2_2_1(predchecker_env):
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 7)
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


@toffee_test.testcase
async def test_ret_chk_2_2_2(predchecker_env):
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLES, 8)
    #print(f"vec_pkt: \n{vec_pkt}\n")
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
        #assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!! at vec_pkt[{i}]: stg1_fixedRange {stg1_fixedRange} != {ref_res[0]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!! at vec_pkt[{i}]: stg1_fixedTaken {stg1_fixedTaken} != {ref_res[1]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!! at vec_pkt[{i}]: stg2_fixedMissPred {stg2_fixedMissPred} != {ref_res[2]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!! at vec_pkt[{i}]: stg2_fixedTarget {stg2_fixedTarget} != {ref_res[3]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        #assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!! at vec_pkt[{i}]: stg2_jalTarget {stg2_jalTarget} != {ref_res[4]} \n\nvec_pkt[i]: {vec_pkt[i]}"
    del mdl, sqr