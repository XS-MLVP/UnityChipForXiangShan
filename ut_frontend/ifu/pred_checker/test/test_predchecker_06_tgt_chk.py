import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
from ..env.pred_checker_sqr import pred_checker_sqr

TEST_CYCLE = 10000

@toffee_test.testcase
async def test_tgt_chk_6_1_1(predchecker_env):
    print("Test case 6.1.1, pds has no jumping instruction and FTQ gave no jumping prediction, check result")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 61)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr
    
@toffee_test.testcase
async def test_tgt_chk_6_1_2(predchecker_env):
    print("Test case 6.1.2, pds gave a jumping info and FTQ prediction is corresponding with it, check result")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 62)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr
    
@toffee_test.testcase
async def test_tgt_chk_6_2(predchecker_env):
    print("Test 6.2, pds has jumping info but FTQ has error jumping target, check result")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 63)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr