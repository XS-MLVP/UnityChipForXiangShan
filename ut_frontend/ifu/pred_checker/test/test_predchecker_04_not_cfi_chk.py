import os
import sys
import random

import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
from ..env.pred_checker_sqr import pred_checker_sqr

TEST_CYCLE = 10000

@toffee_test.testcase
async def test_not_cfi_chk_4_1_1(predchecker_env):
    print("Test case 4.1.1: Input no-exist CFI and FTQ hasn't given a jump prediction, check pred_checker report")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 41)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr
    
@toffee_test.testcase
async def test_not_cfi_chk_4_1_2(predchecker_env):
    print("Test case 4.1.2: Input a valid CFI and FTQ gave a correct jump prediction, check pred_checker report")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 42)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr

@toffee_test.testcase
async def test_not_cfi_chk_4_2(predchecker_env):
    print("Test case 4.2: Input no-exist CFI but FTQ gave a jump prediction, check pred_checker report")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 43)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr