from tokenize import group
import toffee.funcov as fc
from toffee.funcov import CovGroup
from ut_frontend.ftq.ftq_top.env.ftq_bundle import FromBackendBundle
from .utils import S2_redirect_ref, S3_redirect_ref, canCommit_ref, validInstructions_ref, lastInstructionStatus_ref, firstInstructionFlushed_ref
from .utils import last_valid_rob_commit_ref

c_empty     = 0
c_toCommit  = 1
c_committed = 2
c_flushed   = 3

#==================================
#   Cov Points for testcase 10
#==================================
def redirect_from_flush(dut):
    return dut.fromIfuRedirect_valid_probe.value

def redirect_from_backend(dut):
    realAhdValid = dut.realAhdValid.value
    backendRedirectReg = dut.backendRedirectReg.value
    backendRedirect = dut.backendRedirect.value
    return backendRedirect if realAhdValid else backendRedirectReg

def to_bpu_redirect(dut)-> CovGroup:
    group = CovGroup("commit redirect info to BPU")
    group.add_watch_point(dut, {"redirect_from_flush": redirect_from_flush}, name="redirect_from_flush")
    group.add_watch_point(dut, {"redirect_from_backend": redirect_from_backend}, name="redirect_from_backend")
    return group

def update_stall(dut)-> CovGroup:
    group = CovGroup("we need stall when update BPU")
    group.add_watch_point(dut.bpu_ftb_update_stall, {
        "no stall": fc.Eq(0),
        "have stall": fc.Ne(0),
        }, name="bpu_ftb_update_stall")
    return group

def can_commit_cond1(dut):
    validInstructions = validInstructions_ref(dut)
    commPtr = dut.gen_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    robCommPtr = dut.gen_rob_comm_ptr()
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canCommit = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
            (robCommPtr > commPtr)
        )
    )
    return canCommit

def can_commit_cond2(dut):
    validInstructions = validInstructions_ref(dut)
    has_valid = any(validInstructions)
    commPtr = dut.gen_rob_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canCommit = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
                has_valid
                # and lastInstructionStatus == c_committed
        )
    )
    return canCommit

def can_commit(dut)-> CovGroup:
    group = CovGroup("can commit to bpu")
    group.add_watch_point(dut, {"can_commit_cond2": can_commit_cond2}, name="can_commit_cond2", once = True)
    group.add_watch_point(dut, {"can_commit_cond1": can_commit_cond1}, name="can_commit_cond1", once = True)
    return group

def move_commptr_when_flush(dut):
    commPtr = dut.gen_rob_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
    firstInstructionFlushed = firstInstructionFlushed_ref(commit_state)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canMoveCommPtr = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
            firstInstructionFlushed
        )
    )
    return canMoveCommPtr

def move_commptr_when_can_commit(dut):
    return dut.canCommit.value == 1

def can_move_commit_ptr(dut)-> CovGroup:
    group = CovGroup("can_move_commit_ptr")
    group.add_watch_point(dut, {"move_commptr_when_can_commit": move_commptr_when_can_commit}, name="move_commptr_when_can_commit")
    group.add_watch_point(dut, {"move_commptr_when_flush": move_commptr_when_flush}, name="move_commptr_when_flush")
    return group

def rob_commit_valid(formBackend: FromBackendBundle):
    return last_valid_rob_commit_ref(formBackend) is not None

def rob_commit_no_valid(formBackend: FromBackendBundle):
    return last_valid_rob_commit_ref(formBackend) is None

def update_rob_commit_ptr(formBackend: FromBackendBundle)->CovGroup:
    group = CovGroup("update_rob_commit_ptr")
    group.add_watch_point(formBackend, 
                          {"rob_commit_valid": rob_commit_valid,
                           "rob_commit_no_valid": rob_commit_no_valid
                           },
                          name="rob_commit_valid")
    # group.add_watch_point(formBackend, {"rob_commit_no_valid": rob_commit_no_valid}, name="rob_commit_no_valid")
    return group


def mmio_last_commit_cond1(dut):
    commPtr = dut.gen_comm_ptr()
    mmioReadValid = 1
    mmioReadPtr = dut.gen_mmio_ftq_ptr()
    mmioLastCommit = (
        mmioReadValid
        and (
            (commPtr > mmioReadPtr)
        )
    )
    return mmioLastCommit

def mmio_last_commit_cond2(dut):
    commPtr = dut.gen_comm_ptr()
    mmioReadValid = 1
    mmioReadPtr = dut.gen_mmio_ftq_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions_ref(dut))
    has_valid = any(validInstructions_ref(dut))
    mmioLastCommit = (
        mmioReadValid
        and (
            commPtr == mmioReadPtr
            and has_valid
            and lastInstructionStatus == c_committed
        )
    )
    return mmioLastCommit   

def mmio_last_commit(dut)->CovGroup:
    group = CovGroup("mmio_last_commit")
    group.add_watch_point(dut, {"mmio_last_commit_cond1": mmio_last_commit_cond1}, name="mmio_last_commit_cond1")
    group.add_watch_point(dut, {"mmio_last_commit_cond2": mmio_last_commit_cond2}, name="mmio_last_commit_cond2")
    return group

def ftb_entry_gen_modify_old(dut)->CovGroup:
    group = CovGroup("modify old ftb entry to commit")
    group.add_watch_point(dut.ftb_entry_gen_io_is_br_full, {
        "ftb_entry_gen_io_is_br_full": fc.CovEq(1),
        }, name="ftb_entry_gen_io_is_br_full")
    group.add_watch_point(dut.ftb_entry_gen_io_is_jalr_target_modified, {
        "ftb_entry_gen_io_is_jalr_target_modified": fc.CovEq(1),
        }, name="ftb_entry_gen_io_is_jalr_target_modified")
    group.add_watch_point(dut.ftb_entry_gen_io_is_new_br, {
        "ftb_entry_gen_io_is_new_br": fc.CovEq(1),
        }, name="ftb_entry_gen_io_is_new_br")
    group.add_watch_point(dut.ftb_entry_gen_io_is_strong_bias_modified, {
        "ftb_entry_gen_io_is_strong_bias_modified": fc.CovEq(1),
        }, name="ftb_entry_gen_io_is_strong_bias_modified")
    return group

def update_ftb_entry(dut)->CovGroup:
    group = CovGroup("update ftb entry and commit it to BPU")
    group.add_watch_point(dut.io_toBpu_update_bits_old_entry, {
        "io_toBpu_update_bits_old_entry": fc.Eq(1),
        }, name="io_toBpu_update_bits_old_entry")
    group.add_watch_point(dut.io_toBpu_update_bits_old_entry, {
        "io_toBpu_update_bits_init_entry": fc.Eq(0),
        }, name="io_toBpu_update_bits_init_entry")
    return group

#==================================
#   Cov Points for testcase 1
#==================================
def ftq_get_bpu_resp_ready(dut)->CovGroup:
    group = CovGroup("FTQ is ready to get the result from BPU")
    group.add_watch_point(dut.io_fromBpu_resp_ready, {
        "ftq_get_bpu_resp_ready": fc.Eq(1),
        }, name="ftq_get_bpu_resp_ready")
    group.add_watch_point(dut.io_fromBpu_resp_ready, {
        "ftq_get_bpu_resp_not_ready": fc.Eq(0),
        }, name="ftq_get_bpu_resp_not_ready")
    return group

def bpu_resp_valid(dut)->CovGroup:
    group = CovGroup("BPU's resp is valid to send to BPU")
    group.add_watch_point(dut.io_fromBpu_resp_valid, {
        "bpu_resp_valid": fc.Eq(1),
        }, name="bpu_resp_valid")
    group.add_watch_point(dut.io_fromBpu_resp_valid, {
        "bpu_resp_invalid": fc.Eq(0),
        }, name="bpu_resp_invalid")
    return group    

def bpu_in_fire(dut)->CovGroup:
    group = CovGroup("BPU result successfully into FTQ")
    group.add_watch_point(dut.bpu_in_fire, {
        "bpu_in_fire": fc.Eq(1),
        }, name="bpu_in_fire")
    return group  

def not_allow_BPU_in(dut)->CovGroup:
    group = CovGroup("not allow BPU in when redirect from backend or IFU")
    group.add_watch_point(dut.backendRedirect, {
        "backendRedirect": fc.Eq(1),
        }, name="backendRedirect")
    group.add_watch_point(dut.backendRedirectReg, {
        "backendRedirectReg": fc.Eq(1),
        }, name="backendRedirectReg")
    group.add_watch_point(dut.ifu_flush, {
        "ifuFlush": fc.Eq(1),
        }, name="ifuFlush")
    return group      

def allow_BPU_in_with_S2_redirect(dut):
    allow_bpu_in = dut.allowBpuIn.value
    S2_redirect = S2_redirect_ref(dut)
    return allow_bpu_in and S2_redirect

def allow_BPU_in_with_S3_redirect(dut):
    allow_bpu_in = dut.allowBpuIn.value
    S3_redirect = S3_redirect_ref(dut)
    return allow_bpu_in and S3_redirect

def allow_BPU_in_when_resp_redirect(dut)->CovGroup:
    group = CovGroup("allow BPU with redirect resp")
    group.add_watch_point(dut, {"allow_BPU_in_with_S2_redirect": allow_BPU_in_with_S2_redirect}, name="allow_BPU_in_with_S2_redirect")
    group.add_watch_point(dut, {"allow_BPU_in_with_S3_redirect": allow_BPU_in_with_S3_redirect}, name="allow_BPU_in_with_S3_redirect")
    return group

def transfer_flush_to_IFU(dut)->CovGroup:
    group = CovGroup("BPU will transfer flush to IFU when resp redirect")
    group.add_watch_point(dut.io_toIfu_flushFromBpu_s2_valid, {
        "io_toIfu_flushFromBpu_s2_valid": fc.Eq(1),
        }, name="io_toIfu_flushFromBpu_s2_valid")
    group.add_watch_point(dut.io_toIfu_flushFromBpu_s3_valid, {
        "io_toIfu_flushFromBpu_s3_valid": fc.Eq(1),
        }, name="io_toIfu_flushFromBpu_s3_valid")
    return group    

def transfer_flush_to_Prefetch(dut)->CovGroup:
    group = CovGroup("BPU will transfer flush to IFU when resp redirect")
    group.add_watch_point(dut.io_toPrefetch_flushFromBpu_s2_valid, {
        "io_toPrefetch_flushFromBpu_s2_valid": fc.Eq(1),
        }, name="io_toPrefetch_flushFromBpu_s2_valid")
    group.add_watch_point(dut.io_toPrefetch_flushFromBpu_s3_valid, {
        "io_toPrefetch_flushFromBpu_s3_valid": fc.Eq(1),
        }, name="io_toPrefetch_flushFromBpu_s3_valid")
    return group    