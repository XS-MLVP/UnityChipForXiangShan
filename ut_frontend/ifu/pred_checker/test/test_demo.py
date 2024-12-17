import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env
# from pred_checker_dut import predchecker_env

@toffee_test.testcase
async def test_fire(predchecker_env):
    valid = False
    bits = 0
    jumpOffset = [0 for i in range(PREDICT_WIDTH)]
    instrRange = [True for i in range(PREDICT_WIDTH)]
    # instrRange[15] = 0
    instrValid = [True for i in range(PREDICT_WIDTH)] # all RVCs
    pc = [0 for i in range(PREDICT_WIDTH)]
    pds = [{RVC_LABEL: True, RET_LABEL: False, BRTYPE_LABEL: 0 } for i in range(PREDICT_WIDTH)]
    tgt = 0
    async for res in predchecker_env.predCheckerAgent.agent_pred_check(valid, bits, instrRange, instrValid, jumpOffset, pc, pds, tgt, True):
        print(res)
