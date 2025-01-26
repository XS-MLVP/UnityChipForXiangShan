import os
import sys
import random

import toffee.funcov as fc
from toffee.funcov import CovGroup
import toffee_test
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL
from dut.PredChecker import DUTPredChecker
from .pred_checker_dut import predchecker_env



# 功能点1.1.1: JAL预测错误检查 无JAL指令输入，是否会误报JAL预测错误
# instrRange: 1
# instrValid: 1
# jumpOffset: 4
# pc: random
# pds: BRTYPE_LABEL: 0 # 无JAL指令
# tgt: 0
# fire: 1
@toffee_test.testcase
async def test_jal_error_1_1_1(predchecker_env):
    print("Test 1.1.1: JAL error")
    for _ in range (0, 2):
        ftqValid = True
        ftqOffBits = 0
        instrRange = [True for _ in range(PREDICT_WIDTH)]
        instrValid = [True for _ in range(PREDICT_WIDTH)]
        jumpOffset = [24 for _ in range(PREDICT_WIDTH)]
        #pc = [random.randint(0, 2**50-16) for _ in range(PREDICT_WIDTH)]
        pc = [12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72]
        pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2 } for i in range(PREDICT_WIDTH)]
        tgt = 80
        fire = True
        #vec=[ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
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
        # Check the result: Is JAL fix reported
        #assert res[2] == [0 for _ in range(PREDICT_WIDTH)], f"Pred Checker report JAL prediction error!!!: res[2](Fixed Miss Prediction){res[2]} != {[0 for _ in range(PREDICT_WIDTH)]}"
    print("Test Done")


"""
# 功能的1.1.2: JAL预测错误检查，有JAL指令输入，是否会误报JAL预测错误
async def test_jal_error_1_1_2(predchecker_env):
    ftqValid = True
    ftqOffBits = 0 #random.randint(0, 15)  # 假定的偏移量
    instrRange = [True for _ in range(PREDICT_WIDTH)]  # 随机有效范围  # 假定都在范围内
    instrValid = [True for _ in range(PREDICT_WIDTH)]  # 随机指令有效性 # 假定都有效
    jumpOffset = [4 for _ in range(PREDICT_WIDTH)]  # 随机跳转偏移量
    pc = [random.randint(0, 2**50-16) for _ in range(PREDICT_WIDTH)]  # 随机程序计数器
    pds = [{RVC_LABEL: False, RET_LABEL: False, BRTYPE_LABEL: 2 } for i in range(PREDICT_WIDTH)]  # 假定的分支信息
    tgt = 0
    fire = True #random.choice([True, False])  # 随机触发信号
    vec=[ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire]
    print(f"jumpOffset: {jumpOffset}")
    print(f"pc: {pc}")

    # Test: Is res[1] equal to pc + jumpOffset
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
    
    # Check the result: JAL target fix
    for i in range(len(pc)):
        try:
            computed_tgt = pc[i] + jumpOffset[i]
            assert res[1][i] == computed_tgt, f"JAL target error: {res[1][i]} != {computed_tgt}"
        except AssertionError as e:
            print(f"Error: {e}")
    print("DUT output res[1] checked")
    # Check the result: JAL Fixed Miss Prediction
    try:
        computed_fixed_miss_pred = [0 for _ in range(PREDICT_WIDTH)]
        for i in range(PREDICT_WIDTH):
            if pc[i] + jumpOffset[i] != tgt:
                computed_fixed_miss_pred[i] = 0
            else:
                computed_fixed_miss_pred[i] = 1
        assert res[2] == computed_fixed_miss_pred, f"Fixed Miss Prediction error: {res[2]} != {computed_fixed_miss_pred}"
    except AssertionError as e:
        print(f"Error: {e}")
    print("Test Done")
"""