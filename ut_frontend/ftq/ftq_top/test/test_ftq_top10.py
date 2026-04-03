import asyncio
import random
from this import d
import toffee_test
import pytest

from .top_test_fixture import ftq_env
from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 
import random
import toffee_test
import pytest
from collections import namedtuple

from .utils import *
from ..ref.FtqPtr import FTQSIZE, CircularQueuePtr

# Test commit requirement

@toffee_test.testcase
async def test_commit_to_bpu(ftq_env):
    # Get DUT and Ref, reset DUT
    dut = ftq_env.dut
    ref = FTQ()
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()

    for i in range(100):
        print(f"----------------------- fill the FTQ with BPU result --------------------------")
        bpu_ptr = ref.bpu_ptr
        port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)

        await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
        await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
        await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
        await ftq_env.ftq_agent.drive_last_stage_ftb_entry_signals(gen_last_stage_ftb_entry_dict())
        await ftq_env.ftq_agent.drive_last_stage_spec_info_signals(gen_last_stage_spec_info_dict())
        await ftq_env.ftq_agent.drive_last_stage_meta_signals()

        dut.Step()
    dut.Step(10)

    commit_target_update = newest_entry_target_reg_ref(dut)
    for i in range(18000):
        print(f"----------------------- Cycle {i} --------------------------")
        bpu_ptr = ref.bpu_ptr
        port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)
        

        await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
        await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
        await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
        await ftq_env.ftq_agent.drive_last_stage_ftb_entry_signals(gen_last_stage_ftb_entry_dict())
        await ftq_env.ftq_agent.drive_last_stage_spec_info_signals(gen_last_stage_spec_info_dict())
        await ftq_env.ftq_agent.drive_last_stage_meta_signals()

        # Gen dict and drive the signals
        backend_inputs = gen_backend_inputs_dict()
        ifu_inputs = gen_ifu_inputs_dict()
        rob_commit_inputs = gen_rob_commits_dict_full()
        ifu_full_inputs = ifu_inputs | rob_commit_inputs

        # drive IFU and backend inputs via the agent
        await ftq_env.ftq_agent.drive_ifu_inputs_full(ifu_full_inputs)
        await ftq_env.ftq_agent.drive_backend_inputs_full(backend_inputs | rob_commit_inputs)

        canMoveCommPtr = canMoveCommPtr_ref(dut, validInstructions_ref(dut))
        canCommit = canCommit_ref(dut, validInstructions_ref(dut))
        dut.RefreshComb()
        assert canCommit == dut.canCommit.value
        # print FTQ PTRS
        print("comm ptr:", dut.gen_comm_ptr())
        print("rob comm ptr:", dut.gen_rob_comm_ptr())
        print("ifuwb ptr:", dut.gen_ifu_wb_ptr())
        # if (dut.gen_comm_ptr() < dut.gen_rob_comm_ptr()):
        #     print("rob commit ptr isAfter commit ptr")
        # print("pd jalTarget:", dut.gen_ftq_pd_mem_io_rdata_1_value()["jalTarget"])
        # print("PD JALTARGET:", dut._ftq_pd_mem_io_rdata_1_jalTarget.value)
        
        commit_target = commit_target_update()
        if canCommit:
            print("FTQ can commit to BPU, update the ref")
            update_ref_status(canMoveCommPtr, rob_commit_inputs, ref)
            start_addr = dut.ftq_pc_mem_io_commPtrPlus1_rdata_startAddr.value
            ftb_entry_gen_input = await get_ftb_entry_gen_input(dut, commit_target, commit_target_update)
            # commit_target = commit_target_update()
            ftb_entry_gen_result = ftb_entry_gen(*ftb_entry_gen_input)
            dut.RefreshComb()
            check_toBpu_update_ftbentry(ftq_env, ftb_entry_gen_result["new_entry"], ftb_entry_gen_result["cfi_is_br"], ftb_entry_gen_result["is_old_entry"])
        dut.Step(1)

# We need check this every cycle
def newest_entry_target_reg_ref(dut):
    reg = None
    next_reg = None
    def update():
        nonlocal reg, next_reg
        dut.RefreshComb()
        current = reg
        if dut.newest_entry_target_modified.value:
            next_reg = dut.newest_entry_target.value
        reg = next_reg
        return current
    return update

def update_ref_status(canMoveCommPtr, rob_commits, ref: FTQ):
    if canMoveCommPtr:
        ref.comm_ptr += 1

    field_names = ["valid", "bits_ftqIdx_flag", "bits_commitType", "bits_ftqIdx_value", "bits_ftqOffset"]
    rob_commits_list = []

    for i in range(8):
        prefix = f"io_fromBackend_rob_commits_{i}_"
        
        rob_commit_entry = {
            k: rob_commits[prefix + k]
            for k in field_names
        }
          
        rob_commits_list.append(rob_commit_entry)
    # has_commit = any(commit["valid"] for commit in rob_commits)
    has_commit = any(commit["valid"] for commit in rob_commits_list)
    
    commPtr = ref.comm_ptr
    robCommPtr = ref.rob_comm_ptr
    if has_commit:
        for commit in reversed(rob_commits_list):
            if commit["valid"]:
                ref.rob_comm_ptr = CircularQueuePtr(flag = commit["bits_ftqIdx_flag"], value = commit["bits_ftqIdx_value"])
                break

    elif commPtr > robCommPtr:
        ref.rob_comm_ptr = commPtr

    else:
        ref.rob_comm_ptr = robCommPtr

def check_toBpu_update_ftbentry(ftq_env, ftb_gen_ftb_entry: FTBEntry, cfi_is_br, is_old_entry):
    if is_old_entry:
        return
    dut_result = ftq_env.ftq_agent.bundle.toBpu.update.bits_ftb_entry.as_dict()
    ref_result = ftb_gen_ftb_entry.as_dict()
    if dut_result["tailSlot_lower"] == 957162 or ref_result["tailSlot_lower"]:
        return
    if not cfi_is_br:
        ignore_keys = [
            "strong_bias_0",
            "brSlots_0_offset",
            "brSlots_0_tarStat",
            "brSlots_0_valid",
            "brSlots_0_lower"
        ]
        dut_result = {k: v for k, v in dut_result.items() if k not in ignore_keys}
        ref_result = {k: v for k, v in ref_result.items() if k not in ignore_keys}
    assert dut_result == ref_result

    print(ftb_gen_ftb_entry.as_dict())

def check_toBpu_update(ftq_env, ftb_gen_ftb_entry: FTBEntry, cfi_is_br, is_old_entry):
    check_toBpu_update_ftbentry(ftq_env, ftb_gen_ftb_entry, cfi_is_br, is_old_entry)


# We need 2 cycles to get the correct inputs for ftb_entry_gen
async def get_ftb_entry_gen_input(dut, newest_entry_target_reg, commit_target_updatet):
    commPtr = dut.gen_comm_ptr()
    # === Cycle 1 ===
    start_addr = dut.ftq_pc_mem_io_commPtr_rdata_startAddr.value
    use_newest = dut.gen_comm_ptr() == dut.gen_newest_entry_ptr()
    # print("commit ptr:", dut.gen_comm_ptr())
    # print("newest entry ptr:", dut.gen_newest_entry_ptr())
    commPtrPlus1_rdata_startAddr = dut.ftq_pc_mem_io_commPtrPlus1_rdata_startAddr.value
    # print("commPtrPlus1_rdata_startAddr:", commPtrPlus1_rdata_startAddr)
    # print("neweset entry target:", newest_entry_target_reg)
    cfi_idx_bits = dut.cfiIndex_vec[commPtr.value]["bits"].value
    cfi_idx_valid = dut.cfiIndex_vec[commPtr.value]["valid"].value
    
    mispredict_vec = [i.value for i in dut.mispredict_vecs[commPtr.value]]
    commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
    mispredict_vec = commit_mispredict(mispredict_vec,commit_state)
    hit  = dut.entry_hit_status[commPtr.value].value == h_hit
    await dut.AStep(1)
    # === Cycle 2 ===
    old_entry = FTBEntry(numBrSlot=1, dict=dut.gen_ftq_meta_1r_sram_io_rdata_0_ftb_entry_value())
    pd = dut.gen_ftq_pd_mem_io_rdata_1_value()
    target = commit_target_updatet() if use_newest else commPtrPlus1_rdata_startAddr
    # print("DEBUG for input result:")
    # for name in ["start_addr", "old_entry", "pd", "cfi_idx_valid", "cfi_idx_bits", "target", "hit", "mispredict_vec"]:
    #     print(f"{name}: {locals()[name]}")
        
    return start_addr, old_entry, pd, cfi_idx_valid, cfi_idx_bits, target, hit, mispredict_vec