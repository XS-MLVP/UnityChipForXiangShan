import random
import toffee_test
from .top_test_fixture import ftq_env
from .test_configs import test_scenarios

@toffee_test.testcase
async def test_example4_integration_with_agent(ftq_env):
    dut = ftq_env.dut
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    for i in range(300):
        scenario = random.choice(test_scenarios)
        test_idx = random.randint(0, 63)
        pred_offset = random.randint(0, 7)
        await ftq_env.ftq_agent.drive_s1_signals(valid=True)
        await ftq_env.ftq_agent.drive_s2_signals(
            valid=True,
            full_pred_3_hit=True,
            redirect_idx=test_idx
        )
        await ftq_env.ftq_agent.bundle.step(3)
        await ftq_env.ftq_agent.drive_s2_signals(
            valid=False,
            full_pred_3_hit=False,
            redirect_idx=0
        )
        await ftq_env.ftq_agent.drive_s1_signals(valid=True)
        await ftq_env.ftq_agent.drive_s3_signals(valid=True, redirect_idx=test_idx)
        drive_configs = {
            "br_true_hit": {"isJalr": False, "isCall": False, "isRet": False, "brSlots_0_valid": True, "brSlots_0_offset": pred_offset, "tailSlot_valid": False, "tailSlot_offset": 0, "tailSlot_sharing": False},
            "br_false_hit": {"isJalr": False, "isCall": False, "isRet": False, "brSlots_0_valid": True, "brSlots_0_offset": pred_offset, "tailSlot_valid": False, "tailSlot_offset": 0, "tailSlot_sharing": False},
            "shared_br_true_hit": {"isJalr": False, "isCall": False, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": True},
            "shared_br_false_hit": {"isJalr": False, "isCall": False, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": True},
            "jalr_true_hit": {"isJalr": True, "isCall": False, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "jalr_false_hit": {"isJalr": True, "isCall": False, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "call_true_hit": {"isJalr": False, "isCall": True, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "call_false_hit": {"isJalr": False, "isCall": True, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "ret_true_hit": {"isJalr": False, "isCall": False, "isRet": True, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "ret_false_hit": {"isJalr": False, "isCall": False, "isRet": True, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "jal_true_hit": {"isJalr": False, "isCall": False, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False},
            "jal_false_hit": {"isJalr": False, "isCall": False, "isRet": False, "brSlots_0_valid": False, "brSlots_0_offset": 0, "tailSlot_valid": True, "tailSlot_offset": pred_offset, "tailSlot_sharing": False}
            }
        config = drive_configs.get(scenario)
        config and await ftq_env.ftq_agent.drive_s3_last_stage(**config)
        await ftq_env.ftq_agent.bundle.step(1)
        await ftq_env.ftq_agent.drive_s1_signals(valid=False)
        await ftq_env.ftq_agent.drive_s3_signals(valid=False, redirect_idx=0)
        await ftq_env.ftq_agent.drive_s3_last_stage(
            isJalr=False, isCall=False, isRet=False,
            brSlots_0_valid=False, brSlots_0_offset=0,
            tailSlot_valid=False, tailSlot_offset=0, tailSlot_sharing=False
        )
        await ftq_env.ftq_agent.drive_ifu_inputs(
            valid=True,
            ftqIdx_value=test_idx,
            misOffset_valid=(scenario == "pd_mispred_hit")
        )
        await ftq_env.ftq_agent.set_ifu_pd(
            slot=pred_offset,
            brType=0,
            isCall=False,
            isRet=False,
            valid=True
        )
        scenario_configs = {
            "br_true_hit": {"brType": 1, "isCall": False, "isRet": False, "valid": True},
            "shared_br_true_hit": {"brType": 1, "isCall": False, "isRet": False, "valid": True},
            "shared_br_false_hit": {"brType": 1, "isCall": False, "isRet": False, "valid": False},  # 添加这个
            "jal_true_hit": {"brType": 2, "isCall": False, "isRet": False, "valid": True},
            "jalr_true_hit": {"brType": 3, "isCall": False, "isRet": False, "valid": True},
            "call_true_hit": {"brType": 2, "isCall": True, "isRet": False, "valid": True},
            "ret_true_hit": {"brType": 2, "isCall": False, "isRet": True, "valid": True}
            }
        config = scenario_configs.get(scenario)
        config and await ftq_env.ftq_agent.set_ifu_pd(pred_offset, **config)
        await ftq_env.ftq_agent.bundle.step(1)
        await ftq_env.ftq_agent.drive_ifu_inputs(valid=False, ftqIdx_value=0, misOffset_valid=False)
        for s in range(8):
            await ftq_env.ftq_agent.set_ifu_pd(s, valid=False)
        expected_br_false_hit  = 1 if scenario in ["br_false_hit", "shared_br_false_hit"] else 0
        expected_jal_false_hit = 1 if ("false_hit" in scenario and scenario.startswith(("jal", "jalr", "call", "ret"))) else 0
        expected_pd_mispred    = 1 if scenario == "pd_mispred_hit" else 0
        expected_has_false_hit = 1 if (expected_br_false_hit or expected_jal_false_hit or expected_pd_mispred) else 0
        assert dut.has_false_hit.value == expected_has_false_hit, \
            f"[{i}] scenario={scenario} has_false_hit mismatch: expect={expected_has_false_hit}, actual={actual_has_false_hit}"