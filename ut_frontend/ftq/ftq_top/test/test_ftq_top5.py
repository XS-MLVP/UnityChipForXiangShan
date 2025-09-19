import random
import toffee_test
from .top_test_fixture import ftq_env
from .test_configs import BACKEND_REDIRECT_LOGIC_GOALS, BACKEND_REDIRECT_PATHS


@toffee_test.testcase
async def test_example5_integration_with_agent(ftq_env):
    dut = ftq_env.dut
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    num_experiments = 300
    for i in range(num_experiments):
        logic_goal = random.choice(BACKEND_REDIRECT_LOGIC_GOALS)
        redirect_path = random.choice(BACKEND_REDIRECT_PATHS) # << 随机选择时序路径
        ftq_idx = random.randint(0, 63)
        ftq_offset = random.randint(4, 15)
        await ftq_env.ftq_agent.reset_inputs()
        await ftq_env.ftq_agent.drive_s3_signals(valid=1, redirect_idx=ftq_idx)
        ftb_configs = {
            'VERIFY_BR_HIT': {
                'brSlots_0_valid': 1,
                'brSlots_0_offset': ftq_offset
            },
            'VERIFY_JR_HIT': {
                'isJalr': 1,
                'tailSlot_valid': 1,
                'tailSlot_offset': ftq_offset
            },
            'HIT_SHIFT_1_ADDHIST_1': {
                'brSlots_0_valid': 1,
                'brSlots_0_offset': ftq_offset
            },
            'HIT_SHIFT_2_ADDHIST_1': {
                'brSlots_0_valid': 1,
                'brSlots_0_offset': ftq_offset - 1,
                'tailSlot_valid': 1,
                'tailSlot_offset': ftq_offset + 1,
                'tailSlot_sharing': 1
            }
        }
        config = ftb_configs.get(logic_goal, {})
        await ftq_env.ftq_agent.drive_s3_last_stage(
            valid=1,
            **config
        )
        await ftq_env.ftq_agent.drive_ifu_inputs(valid=1, ftqIdx_value=ftq_idx)
        await ftq_env.ftq_agent.set_ifu_pd(
            slot=ftq_offset, 
            valid=1, 
            brType=1,
        )
        hit_value = 0 if 'MISS_' in logic_goal else 1
        await ftq_env.ftq_agent.drive_s2_signals(
            valid=1, 
            redirect_idx=ftq_idx, 
            full_pred_3_hit=hit_value
        )
        await ftq_env.ftq_agent.bundle.step(2)
        await ftq_env.ftq_agent.reset_inputs()
        if redirect_path == 'AHEAD_REDIRECT':
            await ftq_env.ftq_agent.drive_backend_inputs(
                ftqIdxAhead_0_valid=1,
                ftqIdxAhead_0_bits_value=ftq_idx
            )
            await ftq_env.ftq_agent.bundle.step(1)
            await ftq_env.ftq_agent.drive_backend_inputs(
                valid=1,
                ftqIdx_value=ftq_idx,
                ftqOffset=ftq_offset,
                cfiUpdate_taken=1,
                ftqIdxSelOH_bits=1
            )
            dut.RefreshComb()  #不能删掉
        elif redirect_path == 'NORMAL_REDIRECT':
            await ftq_env.ftq_agent.drive_backend_inputs(
                valid=1,
                ftqIdx_value=ftq_idx,
                ftqOffset=ftq_offset,
                cfiUpdate_taken=1
            )
            await ftq_env.ftq_agent.bundle.step(2)
        verify_map = {
            'VERIFY_BR_HIT': lambda: 
                dut.toBpu_redirect_bits_cfiUpdate_br_hit.value == 1,
            'VERIFY_JR_HIT': lambda: 
                dut.toBpu_redirect_bits_cfiUpdate_jr_hit.value == 1,
            'HIT_SHIFT_1_ADDHIST_1': lambda: 
                dut.toBpu_redirect_bits_cfiUpdate_shift.value == 1 and dut.toBpu_redirect_bits_cfiUpdate_addIntoHist.value == 1,
            'HIT_SHIFT_2_ADDHIST_1': lambda: 
                dut.toBpu_redirect_bits_cfiUpdate_shift.value == 2 and dut.toBpu_redirect_bits_cfiUpdate_addIntoHist.value == 1,
            'MISS_SHIFT_1_ADDHIST_1': lambda: 
                dut.toBpu_redirect_bits_cfiUpdate_shift.value == 1 and dut.toBpu_redirect_bits_cfiUpdate_addIntoHist.value == 1,
        }
        verify_func = verify_map.get(logic_goal)
        if verify_func:
            assert verify_func(), f"{logic_goal} verification failed"
        else:
            raise ValueError(f"Unknown logic goal: {logic_goal}")
        await ftq_env.ftq_agent.bundle.step(3)
