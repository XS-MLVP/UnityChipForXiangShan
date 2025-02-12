import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
from ..env.pred_checker_sqr import pred_checker_sqr

TEST_CYCLE = 10000

@toffee_test.testcase
async def test_rand(predchecker_env):
    print("Test 7, random pds info, check result")
    sqr = pred_checker_sqr()
    vec_pkt = sqr.gen_vec(PREDICT_WIDTH, TEST_CYCLE, 71)
    for i in range(TEST_CYCLE):
        print(f"Test cycle {i}")
        #print(*vec_pkt[i])
        res = await predchecker_env.predCheckerAgent.agent_pred_check(*vec_pkt[i])
        #print(f"res:fixedRange::{res[0]}")
        #print(f"res:fixedTaken::{res[1]}")
        #print(f"res:fixedMissPred::{res[2]}")
        #print(f"res:fixedTarget::{res[3]}")
        #print(f"res:jalTarget::{res[4]}")
    del sqr