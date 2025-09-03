import random
import toffee_test
import toffee
from .top_test_fixture import ftq_env
from .test_configs import FTQ_REDIRECT_SCENARIOS, CFI_INDEX_UPDATE_STRATEGIES

@toffee_test.testcase
async def test_integration8(ftq_env):  
    dut = ftq_env.dut  
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    for cycle in range(300):
        await ftq_env.ftq_agent.reset_inputs()
        scenario = random.choice(FTQ_REDIRECT_SCENARIOS)
        ftqIdx_value = random.randint(0, 63)  
        target = random.randint(0, 2**4 - 1)  
        isMisPred = random.randint(0, 1) 
        r_idx = ftqIdx_value
        hist_bits = dut.get_cfi_index_bits(r_idx).value
        hist_valid = dut.get_cfi_index_valid(r_idx).value
        if hist_bits == 0:
            strategy = "cfiindex_valid_wen"
        else:
            strategy = random.choice(CFI_INDEX_UPDATE_STRATEGIES)
        valid = 1  
        taken = 1  
        offset = 0  
        offset_strategies = {
            "cfiindex_bits_wen": lambda: random.randint(0, hist_bits - 1),  
            "cfiindex_valid_wen": lambda: hist_bits 
        }
        offset = offset_strategies[strategy]()    
        if scenario == "backend_redirect":
            await ftq_env.ftq_agent.drive_backend_inputs(valid, ftqIdx_value, offset, target, taken, isMisPred)
        elif scenario == "ifu_redirect":
            await ftq_env.ftq_agent.drive_ifu_inputs(valid, ftqIdx_value, offset, target, 1, taken)  # misOffset_valid 固定为 1, cfiOffset_valid = taken
        await ftq_env.ftq_agent.bundle.step(3)
        assert dut.get_update_target(r_idx).value == target, f"update_target[{r_idx}] mismatch: expected {target}, got {update_target}"
        assert dut.newest_entry_target.value == target, f"newest_entry_target mismatch: expected {target}, got {newest_target}"
        assert dut.newest_entry_ptr_value.value == ftqIdx_value, f"newest_entry_ptr mismatch: expected {ftqIdx_value}, got {newest_ptr}"
        assert dut.newest_entry_target_modified.value == 1, f"newest_entry_target_modified not true: got {target_modified}"
        if scenario == "backend_redirect":
            assert dut.get_mispredict_vec(r_idx, offset).value == isMisPred, \
                f"mispredict_vec[{r_idx}][{offset}] mismatch: expected {isMisPred}, got {dut.get_mispredict_vec(r_idx, offset).value}"
        assert dut.get_cfi_index_valid(r_idx).value == 1, f"cfiIndex valid mismatch for {strategy}: expected 1, got {new_valid}"
        if strategy == "cfiindex_bits_wen":
            assert dut.get_cfi_index_bits(r_idx).value == offset, f"cfiIndex bits mismatch for {strategy}: expected {offset}, got {new_bits}"

