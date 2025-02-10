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

TEST_CYCLE = 10000

@toffee_test.testcase
async def test_rand(predchecker_env):
    print("Test 7, random pds info, check result")
    sqr = pred_checker_sqr()
    mdl = pred_checker_mdl()
    res = []
    ref_res = []
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 71)
    for i in range(TEST_CYCLE):
        print(f"Test cycle {i}")
        #print(*vec_pkt[i])
        async for res in predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i]):
            if len(res) == 2:
                stg1_fixedRange, stg1_fixedTaken = res
            elif len(res) == 3:
                stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred = res
        ref_res = mdl.ref_pred_check(*vec_pkt[i])
        #print(f"res:fixedRange::{stg1_fixedRange}")
        #print(f"ref:fixedRange::{ref_res[0]}")
        #print(f"res:fixedTaken::{stg1_fixedTaken}")
        #print(f"ref:fixedTaken::{ref_res[1]}")
        #print(f"res:fixedMissPred::{stg2_fixedMissPred}")
        #print(f"ref:fixedMissPred::{ref_res[2]}")
        #print(f"res:fixedTarget::{stg2_fixedTarget}")
        #print(f"ref:fixedTarget::{ref_res[3]}")
        #print(f"res:jalTarget::{stg2_jalTarget}")
        #print(f"ref:jalTarget::{ref_res[4]}")
        assert stg1_fixedRange == ref_res[0], f"Pred Checker Fixed Range error!!! at vec_pkt[{i}]: stg1_fixedRange {stg1_fixedRange} != {ref_res[0]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg1_fixedTaken == ref_res[1], f"Pred Checker Fixed Taken error!!! at vec_pkt[{i}]: stg1_fixedTaken {stg1_fixedTaken} != {ref_res[1]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_fixedMissPred == ref_res[2], f"Pred Checker Fixed Miss Prediction error!!! at vec_pkt[{i}]: stg2_fixedMissPred {stg2_fixedMissPred} != {ref_res[2]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_fixedTarget == ref_res[3], f"Pred Checker Fixed Target error!!! at vec_pkt[{i}]: stg2_fixedTarget {stg2_fixedTarget} != {ref_res[3]} \n\nvec_pkt[i]: {vec_pkt[i]}"
        assert stg2_jalTarget == ref_res[4], f"Pred Checker JAL Target error!!! at vec_pkt[{i}]: stg2_jalTarget {stg2_jalTarget} != {ref_res[4]} \n\nvec_pkt[i]: {vec_pkt[i]}"
    del mdl, sqr