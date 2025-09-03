import random
import toffee_test
from .top_test_fixture import ftq_env
from .test_configs import FTQ_FLUSH_REDIRECT_TYPES
from .test_configs import (
    FTQ_FLUSH_REDIRECT_TYPES,
    PREDICT_WIDTH, FTQ_SIZE, C_EMPTY, C_FLUSHED, C_COMMITTED, COMMIT_WIDTH
)

@toffee_test.testcase
async def test_example9_integration_with_agent(ftq_env):
    dut = ftq_env.dut
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    for cycle in range(300):
        await ftq_env.ftq_agent.drive_backend_inputs(
            valid=False, ftqIdx_value=0, ftqOffset=0,
            level=0, debugIsCtrl=False, debugIsMemVio=False
        )
        await ftq_env.ftq_agent.drive_ifu_inputs(
            valid=False, misOffset_valid=False,
            ftqIdx_value=0, misOffset_bits=0
        )
        for i in range(COMMIT_WIDTH):
            await ftq_env.ftq_agent.set_rob_commit(
                i, valid=False, commitType=0, ftqIdx_flag=False, ftqIdx_value=0, ftqOffset=0
            )
        redirect_type = random.choice(FTQ_FLUSH_REDIRECT_TYPES)
        idx = random.randint(0, FTQ_SIZE - 1)
        offset = random.randint(0, PREDICT_WIDTH - 1)
        flush_itself = random.randint(0, 1)
        commit_valid = 1
        commit_type = random.randint(0, 7)  
        commit_ftq_idx = random.randint(0, 63)  
        commit_offset = random.randint(0, 15)   
        commit_idx = random.randint(0, COMMIT_WIDTH - 1)
        random_i = random.randint(0, PREDICT_WIDTH - 1)
        expected_next = (idx + 1) % 64
        expected_idx_plus2 = (idx + 2) % 64
        expected_idx_plus3 = (idx + 3) % 64
        expected_debugIsCtrl = random.randint(0, 1)
        expected_debugIsMemVio = random.randint(0, 1)
        backend_poked = False
        ifu_poked = False
        if redirect_type in ("backend_only", "both"):
            backend_poked = True
            await ftq_env.ftq_agent.drive_backend_inputs(
                valid=True,
                ftqIdx_value=idx,
                ftqOffset=offset,
                level=flush_itself,
                debugIsCtrl=bool(expected_debugIsCtrl),
                debugIsMemVio=bool(expected_debugIsMemVio),
            )
        if redirect_type in ("ifu_only", "both"):
            ifu_poked = True
            await ftq_env.ftq_agent.drive_ifu_inputs(
                valid=True,
                misOffset_valid=True,
                ftqIdx_value=idx,
                misOffset_bits=offset
            )
        await ftq_env.ftq_agent.bundle.step(5)
        assert dut.icache_flush.value == (1 if (backend_poked or ifu_poked) else 0)
        assert dut.bpu_ptr.value == expected_next
        assert dut.ifu_ptr_write.value == expected_next
        assert dut.ifu_wb_ptr_write.value == expected_next
        assert dut.ifu_ptr_plus1_write.value == expected_idx_plus2
        assert dut.ifu_ptr_plus2_write.value == expected_idx_plus3
        assert dut.pf_ptr_write.value == expected_next
        assert dut.pf_ptr_plus1_write.value == expected_idx_plus2
        if redirect_type in ("backend_only", "both"):
            assert dut.topdown_redirect_valid.value == 1
            assert dut.topdown_redirect_debugIsCtrl.value == expected_debugIsCtrl
            assert dut.topdown_redirect_debugIsMemVio.value == expected_debugIsMemVio
            after_state = dut.get_commit_state_queue_reg(idx, random_i).value
            if random_i > offset:
                assert after_state == C_EMPTY
            elif random_i == offset and flush_itself:
                assert after_state == C_FLUSHED
            assert dut.toifu_redirect_valid.value == 1
            assert dut.toifu_redirect_ftqIdx_value.value == idx
            assert dut.toifu_redirect_ftqOffset.value == offset
            assert dut.toifu_redirect_level.value == flush_itself
        await ftq_env.ftq_agent.set_rob_commit(
            commit_idx, 
            valid=commit_valid, 
            commitType=commit_type, 
            ftqIdx_flag=False,  
            ftqIdx_value=commit_ftq_idx, 
            ftqOffset=commit_offset
        )
        await ftq_env.ftq_agent.bundle.step(5)
        def get_target_coords(c_type, current_ftq_idx, current_offset):
            if c_type <= 3: 
                return current_ftq_idx, current_offset
            elif c_type == 4: 
                return current_ftq_idx, (current_offset + 1) % PREDICT_WIDTH
            elif c_type == 5: 
                return current_ftq_idx, (current_offset + 2) % PREDICT_WIDTH
            elif c_type == 6: 
                return (current_ftq_idx + 1) % FTQ_SIZE, 0
            elif c_type == 7: 
                return (current_ftq_idx + 1) % FTQ_SIZE, 1
            else:
                raise ValueError(f"Unknown commit_type: {c_type}")
        #expected_state = 2
        target_ftq_idx, target_offset = get_target_coords(commit_type, commit_ftq_idx, commit_offset)
        reg_state_signal = dut.get_commit_state_queue_reg(target_ftq_idx, target_offset).value
        assert reg_state_signal == C_COMMITTED, \
            f"commitStateQueueReg[{target_ftq_idx}][{target_offset}] mismatch: " \
            f"expected {C_COMMITTED}, got {reg_state_signal} (commit_type={commit_type})"
 

