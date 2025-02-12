import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
from ..env.pred_checker_sqr import pred_checker_sqr

TEST_CYCLE = 10000

@toffee_test.testcase
async def test_renew_range_3_1(predchecker_env):
    print("Test 3.1: If prediction is correct, check instrRange")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 31)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr

@toffee_test.testcase  
async def test_renew_range_3_2(predchecker_env):
    print("Test 3.2: RET/JAL prediction fault, pds gave a narrower range")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 32)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr
    
@toffee_test.testcase
async def test_renew_range_3_3(predchecker_env):
    print("Test 3.3: No-CFI/Invalid prediction, fixing range to the first CFI instruction")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 33)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr