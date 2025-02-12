import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
from ..env.pred_checker_sqr import pred_checker_sqr

TEST_CYCLE = 10000

@toffee_test.testcase 
async def test_jal_chk_1_1_1(predchecker_env):
    print("Testing case 1.1.1")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 1)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr
    
    
@toffee_test.testcase
async def test_jal_chk_1_1_2(predchecker_env):
    print("Testing case 1.1.2")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 2)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr
    

@toffee_test.testcase
async def test_jal_chk_1_2_1(predchecker_env):
    print("Testing case 1.2.1")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 3)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr



@toffee_test.testcase
async def test_jal_chk_1_2_2(predchecker_env):
    print("Testing case 1_2_2")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 4)
    for i in range(TEST_CYCLE):
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
    del sqr