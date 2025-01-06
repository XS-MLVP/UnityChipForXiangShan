import os
import sys
import random

import toffee.funcov as fc
from toffee.funcov import CovGroup
import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env


def pred_checker_cover_point(vec, chk_res):
    g = CovGroup("predChecker addition function")
    i_jumpOffset = vec[4]
    i_pc = vec[5]
    g.add_cover_point(target=chk_res, bins=[j + p for j, p in zip(i_jumpOffset, i_pc)], name="JAL target fix")
    return g


@toffee_test.testcase
async def test_jal_instruction(predchecker_env):
    ftqValid = True
    ftqOffBits = 0 #random.randint(0, 15)  # 假定的偏移量
    instrRange = [True for _ in range(PREDICT_WIDTH)]  # 随机有效范围  # 假定都在范围内
    instrValid = [True for _ in range(PREDICT_WIDTH)]  # 随机指令有效性 # 假定都有效
    jumpOffset = [random.randint(0, 1024) for _ in range(PREDICT_WIDTH)]  # 随机跳转偏移量
    pc = [random.randint(0, 1024) for _ in range(PREDICT_WIDTH)]  # 随机程序计数器
    pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2 } for i in range(PREDICT_WIDTH)]  # 假定的分支信息
    tgt = random.randint(0, 1024)  # 假定的跳转目标地址
    fire = True #random.choice([True, False])  # 随机触发信号
    vec=[ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
    print(f"jumpOffset: {jumpOffset}")
    print(f"pc: {pc}")

    # 调用 agent_pred_check 函数进行测试
    async for res in  predchecker_env.predCheckerAgent.agent_pred_check(
        ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire
    ):
        if len(res) == 2:
            stg1_fixedRange, stg1_fixedTaken = res
            print(f"Stage 1 Fixed Range: {stg1_fixedRange}")
            print(f"Stage 1 Fixed Taken: {stg1_fixedTaken}")
        elif len(res) == 3:
            stg2_fixedTarget, stg2_jalTarget, stg2_fixedMissPred = res
            print(f"Stage 2 Fixed Target(Maybe this is original target): {stg2_fixedTarget}")
            print(f"Stage 2 JAL Target: {stg2_jalTarget}")
            print(f"Stage 2 Fixed Miss Prediction: {stg2_fixedMissPred}")
    print("Test Done")
    print(res) # {original target, (fixed)jal target, miss prediction}
    
    # Check the result: JAL target fix
    for i in range(len(pc)):
        try:
            computed_tgt = pc[i] + jumpOffset[i]
            assert res[1][i] == computed_tgt, f"JAL target error: {res[1][i]} != {computed_tgt}"
        except AssertionError as e:
            print(f"Error: {e}")
    # Check the result: JAL Fixed Miss Prediction
    for i in range(len(pc)):
        try:
            for i in range(len(pc)):
                if pc[i] + jumpOffset[i] != tgt:
                    computed_fixed_miss_pred = True
                else:
                    computed_fixed_miss_pred = False
                assert res[2][i] == computed_fixed_miss_pred, f"Fixed Miss Prediction error: {res[2][i]} != {computed_fixed_miss_pred}"
        except AssertionError as e:
            print(f"Error: {e}")