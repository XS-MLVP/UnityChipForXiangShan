import random
import toffee_test
from .top_test_fixture import ftq_env
from .test_configs import (
    PREDICT_WIDTH
)


@toffee_test.testcase
async def test_example6_integration_with_agent(ftq_env):
    dut = ftq_env.dut
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    for i in range(300):
        rand_pdwb_valid        = random.choice([0, 1])
        rand_misoffset_valid   = random.choice([0, 1])
        rand_backend_redirect_valid = random.choice([0, 1])
        rand_ftq_idx           = random.randint(0, 63)
        rand_misoffset_bits    = random.randint(0, PREDICT_WIDTH - 1)
        rand_pc_val            = random.randint(0, (1 << 39) - 1)
        rand_target            = random.randint(0, (1 << 39) - 1)
        rand_cfiOffset_valid   = random.choice([0, 1])
        expected_fromIfuRedirect_valid = 1 if (rand_pdwb_valid and rand_misoffset_valid and not rand_backend_redirect_valid) else 0
        expected_pc        = rand_pc_val
        expected_pd_valid  = 1
        expected_pd_isRet  = 1
        expected_ifuFlush  = expected_fromIfuRedirect_valid
        await ftq_env.ftq_agent.drive_backend_inputs(valid=bool(rand_backend_redirect_valid))
        # IFU 头部 + 数据域（按需赋值一次性设置）
        await ftq_env.ftq_agent.drive_ifu_inputs(
            valid=bool(rand_pdwb_valid),
            ftqIdx_value=rand_ftq_idx,
            misOffset_bits=rand_misoffset_bits,
            target=rand_target,
            misOffset_valid=bool(rand_misoffset_valid),
            cfiOffset_valid=bool(rand_cfiOffset_valid),
        )
        await ftq_env.ftq_agent.set_ifu_pc(slot=rand_misoffset_bits, pc=rand_pc_val)
        await ftq_env.ftq_agent.set_ifu_pd(slot=rand_misoffset_bits, valid=True, isRet=True)
        await ftq_env.ftq_agent.bundle.step(1)
        assert dut.ifu_redirect_valid.value == expected_fromIfuRedirect_valid, \
            f"[{i}] fromIfuRedirect.valid mismatch, expect={expected_fromIfuRedirect_valid}, actual={actual_toBpu_valid}"
        if expected_fromIfuRedirect_valid:
            assert dut.ifu_redirect_pc.value        == expected_pc,        f"[{i}] pc mismatch exp={hex(expected_pc)} act={hex(actual_pc)}"
            assert dut.ifu_redirect_pd_valid.value  == expected_pd_valid,  f"[{i}] pd.valid mismatch exp={expected_pd_valid} act={actual_pd_valid}"
            assert dut.ifu_redirect_pd_isRet.value  == expected_pd_isRet,  f"[{i}] pd.isRet mismatch exp={expected_pd_isRet} act={actual_pd_isRet}"
            assert dut.ifu_redirect_target.value    == rand_target,        f"[{i}] target mismatch exp={hex(rand_target)} act={hex(actual_target)}"
            assert dut.ifu_redirect_taken.value     == rand_cfiOffset_valid, f"[{i}] taken mismatch exp={rand_cfiOffset_valid} act={actual_taken}"
            assert dut.ifu_flush.value              == expected_ifuFlush,  f"[{i}] ifuFlush mismatch exp={expected_ifuFlush} act={actual_ifuFlush}"
            assert dut.ifu_redirect_ftq_idx.value   == rand_ftq_idx,       f"[{i}] ftqIdx mismatch exp={rand_ftq_idx} act={actual_ftq_idx}"
            assert dut.ifu_redirect_ftq_offset.value== rand_misoffset_bits, f"[{i}] ftqOffset mismatch exp={rand_misoffset_bits} act={actual_ftq_offset}"
        await ftq_env.ftq_agent.reset_inputs()
        await ftq_env.ftq_agent.bundle.step(3)