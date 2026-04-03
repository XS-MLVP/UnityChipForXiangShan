import random
from this import d
import toffee_test
import pytest
from collections import namedtuple

# from ut_frontend.bpu.tagesc.bundle.port import BranchPredictionBundle
from ut_frontend.ftq.ftq_top.env.ftq_bundle import BranchPredictionResp, BranchPredictionBundle, BranchPredictionBundleforS23

from ut_frontend.ftq.ftq_top.ref.ftq_meta_mem import Ftq_1R_SRAMEntry, Full_FTBEntry
from ut_frontend.ftq.ftq_top.ref.ftq_pc_mem import Ftq_RF_Components
from ut_frontend.ftq.ftq_top.ref.ftq_redirect_mem import Ftq_Redirect_SRAMEntry
from ..ref.ftq_ref import FtqAccurateRef, BpuPacket, FtqPointer, get_random_ptr_before_bpu
from .top_test_fixture import ftq_env
from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 
from .utils import *
from ut_frontend.ftq.ftq_top.ref.ftb_entry_mem import FTBEntry
from ..ref.FtqPtr import FTQSIZE, CircularQueuePtr
from ..ref.FtqRef import FTQ

@toffee_test.testcase
async def test_bpu_enqueue(ftq_env):
    # Get DUT and Ref, reset DUT
    dut = ftq_env.dut
    ref = FTQ()
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    fallThruErrors_before = []
    for i in range(64):
        fallThruErrors_before.append(dut.ftq_pc_mem[i]["fallThruError"].value)
    print("bpuPtr_dut after reset: ", dut.gen_bpu_ptr())

    for i in range(3):
        print(f"----------------------- warm up --------------------------")
        bpu_ptr = ref.bpu_ptr
        port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)
        port_dict_s1["valid"] = 1
        port_dict_s2["valid_3"] = 0
        port_dict_s3["valid_3"] = 0
        await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
        await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
        await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
        await ftq_env.ftq_agent.drive_last_stage_ftb_entry_signals(gen_last_stage_ftb_entry_dict())
        await ftq_env.ftq_agent.drive_last_stage_spec_info_signals(gen_last_stage_spec_info_dict())
        await ftq_env.ftq_agent.drive_last_stage_meta_signals()
        dut.RefreshComb()
        bpu_in_fire = check_with_ref_before_write(dut)
        selected_resp = ftq_env.ftq_agent.bundle.fromBpuNew.selected_resp()
        last_stage_spec_info = ftq_env.ftq_agent.bundle.fromBpuNew.last_stage_spec_info
        last_stage_ftb_entry = ftq_env.ftq_agent.bundle.fromBpuNew.last_stage_ftb_entry
        print("selected_resp: ", hex(selected_resp.pc_3.value), selected_resp.full_pred_3_fallThroughErr.value, selected_resp.full_pred_3_hit.value)
        selected_stage = check_bpu_in_stage(dut)
        update_ftq_ref_state(bpu_in_fire, selected_stage, selected_resp, last_stage_spec_info, last_stage_ftb_entry, ref, dut)
        dut.Step()
        if i == 0:
            dut.Step()
        # Check bpuPtr update
        print("bpuptr: ", ref.bpu_ptr)
        assert ref.bpu_ptr == dut.gen_bpu_ptr()
    
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

        dut.RefreshComb()
        bpu_in_fire = check_with_ref_before_write(dut)
        selected_resp = ftq_env.ftq_agent.bundle.fromBpuNew.selected_resp()
        last_stage_spec_info = ftq_env.ftq_agent.bundle.fromBpuNew.last_stage_spec_info
        last_stage_ftb_entry = ftq_env.ftq_agent.bundle.fromBpuNew.last_stage_ftb_entry
        selected_stage = check_bpu_in_stage(dut)
        check_every_cycle(dut, selected_stage, selected_resp)
        update_ftq_ref_state(bpu_in_fire, selected_stage, selected_resp, last_stage_spec_info, last_stage_ftb_entry, ref, dut)
        dut.Step()
        # Check bpuPtr update
        print("bpuptr_ref: ", ref.bpu_ptr)
        print("bpuptr_dut: ", dut.gen_bpu_ptr())
        assert ref.bpu_ptr == dut.gen_bpu_ptr()
        assert ref.ifu_ptr == dut.gen_ifu_ptr()
        assert ref.pf_ptr == dut.gen_pf_ptr()
    bpu_ptr = ref.bpu_ptr
    port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)
    port_dict_s1["valid"] = 0
    port_dict_s2["valid_3"] = 0
    port_dict_s3["valid_3"] = 0
    await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
    await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
    await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
    # await ftq_env.ftq_agent.drive_last_stage_ftb_entry_signals(gen_last_stage_ftb_entry_dict())
    # await ftq_env.ftq_agent.drive_last_stage_spec_info_signals(gen_last_stage_spec_info_dict())
    dut.Step(10)
    # Check FTQ PC memory
    all_kind_errors = check_with_ref_after_write(dut, ref)
    for erros in all_kind_errors: 
        for error in erros:
            print(error)

        

def check_with_ref_before_write(dut):
    dut.RefreshComb()
    check_resp_ready(dut)
    resp_fire = bpu_resp_fire_ref(dut)
    allow_bpu_in = check_allow_bpu_in(dut)
    bpu_in_fire = check_bpu_in_fire(dut)
    return bpu_in_fire

def check_every_cycle(dut, selected_stage, selected_resp):
    dut.RefreshComb()
    selected_stage = selected_stage_ref(dut)
    if selected_stage == 2:
        assert dut.io_toIfu_flushFromBpu_s3_valid.value == 1
        assert dut.io_toIfu_flushFromBpu_s3_bits_value.value == selected_resp.ftq_idx_value.value
        assert dut.io_toIfu_flushFromBpu_s3_bits_flag.value == selected_resp.ftq_idx_flag.value
        assert dut.io_toPrefetch_flushFromBpu_s3_valid.value == 1
        assert dut.io_toPrefetch_flushFromBpu_s3_bits_value.value == selected_resp.ftq_idx_value.value
        assert dut.io_toPrefetch_flushFromBpu_s3_bits_flag.value == selected_resp.ftq_idx_flag.value
    elif selected_stage == 1:
        assert dut.io_toIfu_flushFromBpu_s2_valid.value == 1
        assert dut.io_toIfu_flushFromBpu_s2_bits_value.value == selected_resp.ftq_idx_value.value
        assert dut.io_toIfu_flushFromBpu_s2_bits_flag.value == selected_resp.ftq_idx_flag.value
        assert dut.io_toPrefetch_flushFromBpu_s2_valid.value == 1
        assert dut.io_toPrefetch_flushFromBpu_s2_bits_value.value == selected_resp.ftq_idx_value.value
        assert dut.io_toPrefetch_flushFromBpu_s2_bits_flag.value == selected_resp.ftq_idx_flag.value
    

def check_ftq_pc_entry(ref_entry, dut_entry, idx):
    errors = []

    if ref_entry.startAddr != dut_entry["startAddr"].value:
        errors.append(
            f"[FTQ_PC][{idx}] startAddr mismatch: "
            f"ref={ref_entry.startAddr:#x}, dut={dut_entry['startAddr'].value:#x}"
        )

    if ref_entry.nextLineAddr != dut_entry["nextLineAddr"].value:
        errors.append(
            f"[FTQ_PC][{idx}] nextLineAddr mismatch: "
            f"ref={ref_entry.nextLineAddr:#x}, dut={dut_entry['nextLineAddr'].value:#x}"
        )

    if (ref_entry.fallThruError) != (dut_entry["fallThruError"].value):
        errors.append(
            f"[FTQ_PC][{idx}] fallThruError mismatch: "
            f"ref={ref_entry.fallThruError}, dut={dut_entry['fallThruError'].value}"
        )

    return errors

def check_ftq_pc_mem(ref_mem:FTQ, dut_ftq_pc_mem):
    all_errors = []

    for i in range(FTQSIZE):
        ref_entry = ref_mem.ftq_pc_mem.read(True, i)
        dut_entry = dut_ftq_pc_mem[i]

        errs = check_ftq_pc_entry(ref_entry, dut_entry, i)
        all_errors.extend(errs)

    return all_errors

def check_ftq_redirect_entry(ref_entry, dut_entry, idx):
    errors = []

    fields = [
        "NOS_flag", "NOS_value", "TOSR_flag", "TOSR_value",
        "TOSW_flag", "TOSW_value", "histPtr_flag", "histPtr_value",
        "sc_disagree_0", "sc_disagree_1", "sctr", "ssp", "topAddr"
    ]

    for field in fields:
        ref_value = getattr(ref_entry, field)
        dut_value = dut_entry[field].value

        if ref_value != dut_value:
            errors.append(
                f"[FTQ_REDIRECT][{idx}] {field} mismatch: "
                f"ref={ref_value}, dut={dut_value}"
            )

    return errors

def check_ftq_redirect_mem(ref_mem, dut_ftq_redirect_mem):
    all_errors = []

    for i in range(64):
        ref_entry = ref_mem.ftq_redirect_mem.read(i)
        dut_entry = dut_ftq_redirect_mem[i]

        errs = check_ftq_redirect_entry(ref_entry, dut_entry, i)
        all_errors.extend(errs)

    return all_errors

def check_ftb_entry(ref_entry, dut_entry, idx):
    errors = []

    fields = [
        "isCall", "isRet", "isJalr", 
        "brSlots_0_offset",  "brSlots_0_valid",
        "tailSlot_offset", "tailSlot_sharing", "tailSlot_valid"
    ]

    for field in fields:
        ref_value = getattr(ref_entry, field)

        if dut_entry[field] is None:
            print(f"FTB_ENTRY[{idx}] field {field} is None in DUT")        
        dut_value = dut_entry[field].value

        if ref_value != dut_value:
            errors.append(
                f"[FTB_ENTRY][{idx}] {field} mismatch: "
                f"ref={ref_value}, dut={dut_value}"
            )

    return errors

def check_ftb_entry_mem(ref_mem, dut_ftb_entry_mem):
    all_errors = []

    for i in range(64):
        ref_entry = ref_mem.ftb_entry_mem.read(i)
        dut_entry = dut_ftb_entry_mem[i] 

        errs = check_ftb_entry(ref_entry, dut_entry, i)
        all_errors.extend(errs)

    return all_errors

# def check_ftq_meta_entry(ref_entry, dut_entry, idx):
#     errors = []

# 
#     fields = [
#         "valid", "isCall", "isRet", "isJalr", "last_may_be_rvi_call",
#         "carry", "pftAddr"
#     ]

#  
#     for field in fields:
#         ref_value = getattr(ref_entry, field)
#         dut_value = getattr(dut_entry, field) 
#         if ref_value != dut_value:
#             errors.append(f"[FTQ_META][{idx}] {field} mismatch: ref={ref_value}, dut={dut_value}")

# 
#     br_slot_fields = ["offset", "sharing", "valid", "lower", "tarStat"]
#     for field in br_slot_fields:
#         ref_value = getattr(ref_entry.ftb["brslot"], field)
#         dut_value = dut_entry.ftb["brSlot"][field]
#         if ref_value != dut_value:
#             errors.append(f"[FTQ_META][{idx}] brSlot_{field} mismatch: ref={ref_value}, dut={dut_value}")

#  
#     tail_slot_fields = ["offset", "sharing", "valid"]
#     for field in tail_slot_fields:
#         ref_value = getattr(ref_entry.ftb["tailslot"], field)
#         dut_value = dut_entry.ftb["tailSlot"][field]
#         if ref_value != dut_value:
#             errors.append(f"[FTQ_META][{idx}] tailSlot_{field} mismatch: ref={ref_value}, dut={dut_value}")

#     return errors


# def check_ftq_meta_mem(ref_mem, dut_ftq_meta_mem):
#     all_errors = []

#    
#     for i in range(64):
#         ref_entry = ref_mem.ftq_meta_mem.read(i)
#         dut_entry = dut_ftq_meta_mem[i]  # DUT 中的 entry

#         errs = check_ftq_meta_entry(ref_entry, dut_entry, i)
#         all_errors.extend(errs)

#     return all_errors

def check_ftq_meta_entry(ref_entry, dut_entry, idx):
    """
    Compare a single FTQ Meta Entry
    ref_entry: Ftq_1R_SRAMEntry (Dataclass)
    dut_entry: FtqMetaEntry
    """
    errors = []

    # 1. compare meta 
    if ref_entry.meta != dut_entry.meta:
        errors.append(
            f"[FTQ_META][{idx}] meta mismatch: "
            f"ref={hex(ref_entry.meta)}, dut={hex(dut_entry.meta)}"
        )

    # 2. compare attribute in entry
    ftb_fields = [
        "valid", "isCall", "isRet", "isJalr", 
        "last_may_be_rvi_call", "carry", "pftAddr"
    ]

    for field in ftb_fields:
        ref_val = getattr(ref_entry.ftb_entry, field)
        dut_val = dut_entry.ftb[field]
        if ref_val != dut_val:
            errors.append(
                f"[FTQ_META][{idx}] ftb.{field} mismatch: "
                f"ref={ref_val}, dut={dut_val}"
            )

    # 3. compare slots
    slots_to_check = [
        ("brslot", "brSlot"),
        ("tailslot", "tailSlot")
    ]
    
    slot_fields = ["offset", "sharing", "valid", "lower", "tarStat"]

    for ref_slot_name, dut_slot_name in slots_to_check:
        ref_slot_obj = getattr(ref_entry.ftb_entry, ref_slot_name)
        dut_slot_dict = dut_entry.ftb[dut_slot_name]

        for field in slot_fields:
            if field in dut_slot_dict:
                ref_s_val = getattr(ref_slot_obj, field)
                dut_s_val = dut_slot_dict[field]
                
                if ref_s_val != dut_s_val:
                    errors.append(
                        f"[FTQ_META][{idx}] {dut_slot_name}.{field} mismatch: "
                        f"ref={ref_s_val}, dut={dut_s_val}"
                    )

    return errors

def check_ftq_meta_mem(ref_mem, dut_ftq_meta_mem_list):
    all_errors = []
    ref_mem_obj = ref_mem.ftq_meta_mem
    for i in range(64):
        ref_entry = ref_mem_obj.read(i)
        dut_entry = dut_ftq_meta_mem_list[i]

        errs = check_ftq_meta_entry(ref_entry, dut_entry, i)
        all_errors.extend(errs)

    if not all_errors:
        print("[FTQ_META] All 64 entries match perfectly.")
    else:
        print(f"[FTQ_META] Found {len(all_errors)} mismatches.")
        
    return all_errors

def check_update_targets(ref, dut_update_targets):
    errors = []
    for i in range(64):
        ref_value = ref.update_targets[i]
        dut_value = dut_update_targets[i].value
        if ref_value != dut_value:
            errors.append(
                f"[UPDATE_TARGETS][{i}] mismatch: "
                f"ref={ref_value}, dut={dut_value}"
            )
    return errors

def check_cfi_index_vec(ref, dut_cfi_index_vec):
    errors = []
    for i in range(64):
        ref_entry = ref.cfiIndex_vec[i]
        dut_entry = dut_cfi_index_vec[i]
        if ref_entry["valid"] != dut_entry["valid"].value:
            errors.append(
                f"[CFI_INDEX_VEC][{i}] valid mismatch: "
                f"ref={ref_entry['valid']}, dut={dut_entry['valid'].value}"
            )
        if ref_entry["bits"] != dut_entry["bits"].value:
            errors.append(
                f"[CFI_INDEX_VEC][{i}] bits mismatch: "
                f"ref={ref_entry['bits']}, dut={dut_entry['bits'].value}"
            )
    return errors

def check_mispredict_vec(ref, dut_mispredict_vecs):
    errors = []
    for i in range(64):
        for j in range(16):
            ref_value = ref.mispredict_vecs[i][j]
            dut_value = dut_mispredict_vecs[i][j].value
            if ref_value != dut_value:
                errors.append(
                    f"[MISPREDICT_VEC][{i}][{j}] mismatch: "
                    f"ref={ref_value}, dut={dut_value}"
                )
    return errors

def check_pred_stage_queue(ref, dut_pred_stages):
    errors = []
    for i in range(64):
        ref_value = ref.pred_stages[i]
        dut_value = dut_pred_stages[i].value
        if ref_value != dut_value:
            errors.append(
                f"[PRED_STAGE_QUEUE][{i}] mismatch: "
                f"ref={ref_value}, dut={dut_value}"
            )
    return errors

def check_entry_fetch_status(ref, dut_entry_fetch_status):
    errors = []
    for i in range(64):
        ref_value = ref.entry_fetch_status[i]
        dut_value = dut_entry_fetch_status[i].value
        if ref_value != dut_value:
            errors.append(
                f"[ENTRY_FETCH_STATUS][{i}] mismatch: "
                f"ref={ref_value}, dut={dut_value}"
            )
    return errors

def check_entry_hit_status(ref, dut_entry_hit_status):
    errors = []
    for i in range(64):
        ref_value = ref.entry_hit_status[i]
        dut_value = dut_entry_hit_status[i].value
        if ref_value != dut_value:
            errors.append(
                f"[ENTRY_HIT_STATUS][{i}] mismatch: "
                f"ref={ref_value}, dut={dut_value}"
            )
    return errors

def check_with_ref_after_write(dut, ref):
    ftq_pc_mem_errors = check_ftq_pc_mem(ref, dut.ftq_pc_mem)
    ftq_redirect_mem_errors = check_ftq_redirect_mem(ref, dut.ftq_redirect_mem)
    ftb_entry_mem_errors = check_ftb_entry_mem(ref, dut.ftb_entry_mem)
    # ftq_meta_mem_errors = check_ftq_meta_mem(ref, dut.ftq_meta_mem)
    update_target_errors = check_update_targets(ref, dut.update_targets)
    cfi_index_vec_errors = check_cfi_index_vec(ref, dut.cfiIndex_vec)
    mispredict_vec_errors = check_mispredict_vec(ref, dut.mispredict_vecs)
    pred_stage_errors = check_pred_stage_queue(ref, dut.pred_stages)
    entry_fetch_status_errors = check_entry_fetch_status(ref, dut.entry_fetch_status)
    return ftq_pc_mem_errors, ftq_redirect_mem_errors, ftb_entry_mem_errors, \
        update_target_errors, cfi_index_vec_errors, mispredict_vec_errors, pred_stage_errors, entry_fetch_status_errors

def write_into_ftq_pc_mem(bpu_in_fire, selected_stage, selected_resp, ref: FTQ):
    if selected_stage == 0:
        ftq_idx_value = ref.bpu_ptr.value
    else:
        ftq_idx_value = selected_resp.ftq_idx_value.value
    print("write into ftq pc mem at idx:", ftq_idx_value)
    ref.ftq_pc_mem.write(bpu_in_fire, ftq_idx_value, Ftq_RF_Components.from_branch_prediction(selected_resp))

def write_into_ftq_redirect_mem(last_stage_valid, last_stage_idx, last_stage_spec_info, ref: FTQ):
    # print("write into redirect mem at idx:", ftq_idx_value)
    # print("last_stage_idx:", last_stage_idx)
    # print("last_stage_valid:", last_stage_valid)
    # print("last_stage_info:", Ftq_Redirect_SRAMEntry.from_spec_info(last_stage_spec_info))
    ref.ftq_redirect_mem.write(last_stage_valid, last_stage_idx, Ftq_Redirect_SRAMEntry.from_spec_info(last_stage_spec_info))

def write_into_ftb_entry_mem(last_stage_valid, last_stage_idx, last_stage_ftb_entry, ref: FTQ):
    ref.ftb_entry_mem.write(last_stage_valid, last_stage_idx, FTBEntry.from_last_stage_ftb_entry(last_stage_ftb_entry))

def write_into_ftq_meta_mem(last_stage_valid, last_stage_idx, last_stage_meta, last_stage_meta_ftb_entry, ref: FTQ):
    ref.ftq_meta_mem.write(last_stage_valid, last_stage_idx, Ftq_1R_SRAMEntry.from_meta_and_ftb(last_stage_meta, last_stage_meta_ftb_entry))


def write_into_update_targets(bpu_in_fire, idx, selected_resp: BranchPredictionBundle, ref: FTQ):
    if not bpu_in_fire:
        return
    else:
        ref.update_targets[idx] = getTaget_ref(selected_resp)

def write_into_cfi_index_vec(bpu_in_fire, idx, selected_resp: BranchPredictionBundle, ref: FTQ):
    if not bpu_in_fire:
        return
    else:
        ref.cfiIndex_vec[idx] = getCfi_ref(selected_resp)

def write_into_mispredict_vec(bpu_in_fire, idx, ref: FTQ):
    if not bpu_in_fire:
        return
    else:
        ref.mispredict_vecs[idx] = [0] * 16
        
def write_into_pred_stage_queue(bpu_in_fire, idx, selected_stage, ref: FTQ):
    if not bpu_in_fire:
        return
    else:
        ref.pred_stages[idx] = selected_stage

def write_into_entry_fetch_status(bpu_in_fire, idx, ref: FTQ):
    if not bpu_in_fire:
        return
    else:
        ref.entry_fetch_status[idx] = 0

def write_into_entry_hit_status(idx, dut, ref: FTQ):
    if dut.io_fromBpu_resp_bits_s2_valid_3.value:
        ref.entry_hit_status[idx] = dut.io_fromBpu_resp_bits_s2_entry_hit.value

def update_ftq_ref_state(bpu_in_fire, selected_stage, selected_resp: BranchPredictionBundle, last_stage_spec_info, last_stage_ftb_entry, ref: FTQ, dut):
    if selected_stage == 0:
        ftq_idx_value = ref.bpu_ptr.value
    else:
        ftq_idx_value = selected_resp.ftq_idx_value.value
    write_into_ftq_pc_mem(bpu_in_fire, selected_stage, selected_resp, ref)
    write_into_ftq_redirect_mem(dut.io_fromBpu_resp_bits_s3_valid_3.value, dut.io_fromBpu_resp_bits_s3_ftq_idx_value.value, last_stage_spec_info, ref)
    write_into_ftb_entry_mem(dut.io_fromBpu_resp_bits_s3_valid_3.value, dut.io_fromBpu_resp_bits_s3_ftq_idx_value.value, last_stage_ftb_entry, ref)
    write_into_ftq_meta_mem(dut.io_fromBpu_resp_bits_s3_valid_3.value, dut.io_fromBpu_resp_bits_s3_ftq_idx_value.value, dut.io_fromBpu_resp_bits_last_stage_meta.value, Full_FTBEntry.from_last_stage_ftb_entry(last_stage_ftb_entry), ref)
    update_ftq_ref_bpu_ptr(bpu_in_fire, selected_stage, selected_resp, ref)
    update_ifu_ptr_when_redirect_ref(selected_stage, selected_resp, ref)
    update_prefetch_ptr_when_redirect_ref(selected_stage, selected_resp, ref)

    write_into_update_targets(bpu_in_fire, ftq_idx_value, selected_resp, ref)
    write_into_cfi_index_vec(bpu_in_fire, ftq_idx_value, selected_resp, ref)
    write_into_mispredict_vec(bpu_in_fire, ftq_idx_value, ref)
    write_into_pred_stage_queue(bpu_in_fire, ftq_idx_value, selected_stage, ref)
    write_into_entry_fetch_status(bpu_in_fire, ftq_idx_value, ref)
    
def update_ftq_ref_bpu_ptr(bpu_in_fire, selected_stage, selected_resp: BranchPredictionBundle, ref: FTQ):
    if not bpu_in_fire:
        return
    if selected_stage == 0:
        ref.bpu_ptr += 1
    else:
        print("redirect bpu ptr:", CircularQueuePtr(FTQSIZE, selected_resp.ftq_idx_flag.value, selected_resp.ftq_idx_value.value) )
        ref.bpu_ptr = CircularQueuePtr(FTQSIZE, selected_resp.ftq_idx_flag.value, selected_resp.ftq_idx_value.value) + 1

def update_ifu_ptr_when_redirect_ref(selected_stage, selected_resp: BranchPredictionBundle, ref: FTQ):
    if selected_stage == 0: 
        return
    updated_ptr = CircularQueuePtr(FTQSIZE, selected_resp.ftq_idx_flag.value, selected_resp.ftq_idx_value.value)
    if(not(ref.ifu_ptr < (updated_ptr))):
        ref.ifu_ptr = updated_ptr
        ref.pf_ptr = updated_ptr

def update_prefetch_ptr_when_redirect_ref(selected_stage, selected_resp: BranchPredictionBundle, ref: FTQ):
    if selected_stage == 0: 
        return
    updated_ptr = CircularQueuePtr(FTQSIZE, selected_resp.ftq_idx_flag.value, selected_resp.ftq_idx_value.value)
    if(not(ref.pf_ptr < (updated_ptr))):
        ref.pf_ptr = updated_ptr

def check_resp_ready(dut):
    assert dut.io_fromBpu_resp_ready.value == bpu_resp_ready_ref(dut)

def check_allow_bpu_in(dut):
    allow_bpu_in = allow_bpu_in_ref(dut)
    assert dut.allowBpuIn.value == allow_bpu_in
    return allow_bpu_in

def check_bpu_in_fire(dut):
    bpu_in_fire = bpu_in_fire_ref(dut)
    assert dut.bpu_in_fire.value == bpu_in_fire
    return bpu_in_fire

def check_bpu_in_stage(dut):
    selected_stage = selected_stage_ref(dut)
    assert dut.bpu_in_stage.value == selected_stage
    return selected_stage

    
