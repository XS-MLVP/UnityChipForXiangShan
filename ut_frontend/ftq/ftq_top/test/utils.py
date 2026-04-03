import random

from ut_frontend.ftq.ftq_top.env.ftq_bundle import BranchPredictionBundle, FromBackendBundle
from ut_frontend.ftq.ftq_top.ref.FtqRef import FTQ

from ..ref.FtqPtr import CircularQueuePtr, distance_between
FTQSIZE = 64

#=====================================
#   Generate input to assign the port
#=====================================
def gen_bpu_branch_resp_dict() -> dict:
    return {
        # 3 stages
        "valid": random.randint(0, 1),
        "pc_3": random.randint(0, (1 << 50) - 1),  # 50
        "full_pred_3_br_taken_mask_0": random.randint(0, 1),
        "full_pred_3_br_taken_mask_1": random.randint(0, 1),
        "full_pred_3_slot_valids_0": random.randint(0, 1),
        "full_pred_3_slot_valids_1": random.randint(0, 1),
        "full_pred_3_targets_0": random.randint(0, (1 << 50) - 1),  # 50
        "full_pred_3_targets_1": random.randint(0, (1 << 50) - 1),
        "full_pred_3_offsets_0": random.randint(0, (1 << 4) - 1),
        "full_pred_3_offsets_1": random.randint(0, (1 << 4) - 1),
        "full_pred_3_fallThroughAddr": random.randint(0, (1 << 50) - 1),
        "full_pred_3_fallThroughErr": random.randint(0, 1),
        "full_pred_3_is_br_sharing": random.randint(0, 1),
        "full_pred_3_hit": random.randint(0, 1),
        # s2/s3 
        "valid_3": random.randint(0, 1),
        "hasRedirect_3": random.randint(0, 1),
        "ftq_idx_flag": random.randint(0, 1),
        "ftq_idx_value": random.randint(0, (1 << 6) - 1),  # 6
    }

def gen_last_stage_ftb_entry_dict() -> dict:
    return {
        "isCall": random.randint(0, 1),
        "isRet": random.randint(0, 1),
        "isJalr": random.randint(0, 1),
        "valid": random.randint(0, 1),
        "last_may_be_rvi_call": random.randint(0, 1),
        "carry": random.randint(0, 1),
        "pftAddr": random.randint(0, 15),          # 4 bits
        "brSlots_0_offset": random.randint(0, 15),         # 4 bits
        "brSlots_0_sharing": random.randint(0, 1),
        "brSlots_0_valid": random.randint(0, 1),
        "tailSlot_offset": random.randint(0, 15),         # 4 bits
        "tailSlot_sharing": random.randint(0, 1),
        "tailSlot_valid": random.randint(0, 1),
    }

def gen_last_stage_spec_info_dict() -> dict:
    return {
            "histPtr_flag": random.randint(0, 1),
            "histPtr_value": random.randint(0, (1 << 8) - 1),   # 8 bits
            "ssp": random.randint(0, (1 << 4) - 1),             # 4 bits
            "sctr": random.randint(0, (1 << 3) - 1),            # 3 bits
            "TOSW_flag": random.randint(0, 1),
            "TOSW_value": random.randint(0, (1 << 5) - 1),      # 5 bits
            "TOSR_flag": random.randint(0, 1),
            "TOSR_value": random.randint(0, (1 << 5) - 1),      # 5 bits
            "NOS_flag": random.randint(0, 1),
            "NOS_value": random.randint(0, (1 << 5) - 1),       # 5 bits
            "topAddr": random.randint(0, (1 << 50) - 1),        # 50 bits
            "sc_disagree_0": random.randint(0, 1),
            "sc_disagree_1": random.randint(0, 1)
    }


def gen_bpu_resp(bpu_ptr: CircularQueuePtr = None):
    port_dict_s1 = gen_bpu_branch_resp_dict()
    if(bpu_ptr is not None):
        bpuPtr = bpu_ptr
        port_dict_s1["ftq_idx_flag"] = bpuPtr.flag
        port_dict_s1["ftq_idx_value"] = bpuPtr.value
    else:
        bpuPtr = CircularQueuePtr(FTQSIZE, flag=port_dict_s1["ftq_idx_flag"], value=port_dict_s1["ftq_idx_value"])
    bpuPtr_sub1 = bpuPtr - 1
    bpuPtr_sub2 = bpuPtr_sub1 - 1
    port_dict_s2 = gen_bpu_branch_resp_dict()
    port_dict_s3 = gen_bpu_branch_resp_dict()

    # Set constraint signals
    port_dict_s2["ftq_idx_flag"] = bpuPtr_sub1.flag
    port_dict_s2["ftq_idx_value"] = bpuPtr_sub1.value
    port_dict_s3["ftq_idx_flag"] = bpuPtr_sub2.flag
    port_dict_s3["ftq_idx_value"] = bpuPtr_sub2.value

    # Set redirect info not totally random
    if random.random() < 0.5:
        port_dict_s2["valid_3"] = 1
        port_dict_s2["hasRedirect_3"] = 1
    else:
        port_dict_s2["valid_3"] = 0
        port_dict_s2["hasRedirect_3"] = 0
    
    if random.random() < 0.5:
        port_dict_s3["valid_3"] = 1
        port_dict_s3["hasRedirect_3"] = 1
    else:
        port_dict_s3["valid_3"] = 0
        port_dict_s3["hasRedirect_3"] = 0

    return port_dict_s1, port_dict_s2, port_dict_s3

def gen_backend_inputs_dict():
    """ backend -> ftq """
    return {
        "io_fromBackend_redirect_valid": random.randint(0, 1),
        "io_fromBackend_redirect_bits_ftqIdx_flag": random.randint(0, 1),
        "io_fromBackend_redirect_bits_ftqIdx_value": random.randint(0, (1 << 6) - 1),
        "io_fromBackend_redirect_bits_ftqOffset": random.randint(0, (1 << 4) - 1),
        "io_fromBackend_redirect_bits_level": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_pc": random.randint(0, (1 << 50) - 1),
        "io_fromBackend_redirect_bits_cfiUpdate_target": random.randint(0, (1 << 50) - 1),
        "io_fromBackend_redirect_bits_cfiUpdate_taken": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_isMisPred": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_backendIGPF": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_backendIPF": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_backendIAF": random.randint(0, 1),
        "io_fromBackend_redirect_bits_debugIsCtrl": random.randint(0, 1),
        "io_fromBackend_redirect_bits_debugIsMemVio": random.randint(0, 1),
        "io_fromBackend_ftqIdxAhead_0_valid": random.randint(0, 1),
        "io_fromBackend_ftqIdxAhead_0_bits_value": random.randint(0, (1 << 6) - 1),
        "io_fromBackend_ftqIdxSelOH_bits": random.randint(0, (1 << 3) - 1),
    }

def gen_rob_commits_dict():
    """rob_commit"""
    return {
        "valid": random.randint(0, 1),
        "commitType": random.randint(0, (1 << 3) - 1),
        "ftqIdx_flag": random.randint(0, 1),
        "ftqIdx_value": random.randint(0, (1 << 6) - 1),
        "ftqOffset": random.randint(0, (1 << 4) - 1),
    }

def gen_ifu_inputs_dict():
    """ ifu -> ftq """
    d = {}
    d["io_fromIfu_pdWb_valid"] = random.randint(0, 1)
    # PCs
    for i in range(16):
        d[f"io_fromIfu_pdWb_bits_pc_{i}"] = random.randint(0, (1 << 50) - 1)
    # pd fields for 16 lanes
    for i in range(16):
        d[f"io_fromIfu_pdWb_bits_pd_{i}_valid"] = random.randint(0, 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_isRVC"] = random.randint(0, 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_brType"] = random.randint(0, (1 << 2) - 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_isCall"] = random.randint(0, 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_isRet"] = random.randint(0, 1)
    # ftq idx / misc
    d["io_fromIfu_pdWb_bits_ftqIdx_flag"] = random.randint(0, 1)
    d["io_fromIfu_pdWb_bits_ftqIdx_value"] = random.randint(0, (1 << 6) - 1)
    d["io_fromIfu_pdWb_bits_misOffset_valid"] = random.randint(0, 1)
    d["io_fromIfu_pdWb_bits_misOffset_bits"] = random.randint(0, (1 << 4) - 1)
    d["io_fromIfu_pdWb_bits_cfiOffset_valid"] = random.randint(0, 1)
    d["io_fromIfu_pdWb_bits_target"] = random.randint(0, (1 << 50) - 1)
    d["io_fromIfu_pdWb_bits_jalTarget"] = random.randint(0, (1 << 50) - 1)
    # instrRange bits
    for i in range(16):
        d[f"io_fromIfu_pdWb_bits_instrRange_{i}"] = random.randint(0, 1)
    return d

def gen_ifu_inputs_dict_full() -> dict:
    """ ifu -> ftq """
    d = gen_ifu_inputs_dict()
    return d | gen_rob_commits_dict_full()

def gen_rob_commits_dict_full() -> dict:
    """ full rob_commit info """
    d = {}
    for i in range(8):
        rc = gen_rob_commits_dict()
        prefix = f"io_fromBackend_rob_commits_{i}_"
        for k, v in rc.items():
            if k != "valid":
                d[prefix + "bits_" + k] = v
            else:
                d[prefix + k] = v
    return d








#=====================================
#   Simulate the behavior of FTQ
#=====================================
def bpu_resp_ready_ref(dut):
    if dut.canCommit.value == 1 or dut.valid_entries() < FTQSIZE:
        assert dut.io_fromBpu_resp_ready.value == 1
        return 1
    else:
        assert dut.io_fromBpu_resp_ready.value == 0
        return 0

# resp_ready & resp_valid will make resp_fire, but it need call dut.RefreshComb() to refresh the circuit 
# and then resp_fire will actually be true
def bpu_resp_fire_ref(dut):
    resp_ready = bpu_resp_ready_ref(dut)
    resp_valid = dut.io_fromBpu_resp_valid.value
    resp_fire = resp_ready & resp_valid
    return resp_fire


# from BPU S1 result
def enq_fire_ref(dut):
    resp_fire = bpu_resp_fire_ref(dut)
    allow_bpu_in = allow_bpu_in_ref(dut)
    enq_fire = resp_fire & allow_bpu_in
    return enq_fire

# S2 redirect
def S2_redirect_ref(dut):
    S2_redirect_valid = dut.io_fromBpu_resp_bits_s2_valid_3.value
    S2_redirect_hasRedirect = dut.io_fromBpu_resp_bits_s2_hasRedirect_3.value
    return S2_redirect_valid and S2_redirect_hasRedirect

# S3 redirect
def S3_redirect_ref(dut):
    S3_redirect_valid = dut.io_fromBpu_resp_bits_s3_valid_3.value
    S3_redirect_hasRedirect = dut.io_fromBpu_resp_bits_s3_hasRedirect_3.value
    return S3_redirect_valid and S3_redirect_hasRedirect

# from BPU result
def bpu_in_fire_ref(dut):
    resp_fire = bpu_resp_fire_ref(dut)
    allow_bpu_in = allow_bpu_in_ref(dut)
    S2_redirect = S2_redirect_ref(dut)
    S3_redirect = S3_redirect_ref(dut)
    return allow_bpu_in and (S2_redirect or S3_redirect or resp_fire)

def allow_bpu_in_ref(dut):
    ifuFlush = dut.ifu_flush.value
    backendRedirect = dut.backendRedirect.value
    backendRedirectReg = dut.backendRedirectReg.value
    return not ifuFlush and not backendRedirect and not backendRedirectReg

def selected_stage_ref(dut):
    S2_redirect = S2_redirect_ref(dut)
    S3_redirect = S3_redirect_ref(dut)
    if S3_redirect:
        return 2
    elif S2_redirect:
        return 1
    else:
        return 0 

def get_idx_of_selected_stage_ref(selectedResp: BranchPredictionBundle, selected_stage: int, ref: FTQ):
    if selected_stage == 0:
        ftq_idx_value = ref.bpu_ptr.value
    else:
        ftq_idx_value = selectedResp.ftq_idx_value.value
    return ftq_idx_value

# jiexi selectedResp
def getTaget_ref(selectedResp: BranchPredictionBundle):
    hit = selectedResp.full_pred_3_hit.value
    fallThroughErr = selectedResp.full_pred_3_fallThroughErr.value
    if hit and not fallThroughErr:
        # taken
        # get first taken target
        if selectedResp.full_pred_3_br_taken_mask_0.value == 1 and selectedResp.full_pred_3_slot_valids_0.value == 1:
            return selectedResp.full_pred_3_targets_0.value
        elif selectedResp.full_pred_3_is_br_sharing.value:
            if selectedResp.full_pred_3_br_taken_mask_1.value == 1 and selectedResp.full_pred_3_slot_valids_1.value == 1:
                return selectedResp.full_pred_3_targets_1.value
            return selectedResp.full_pred_3_fallThroughAddr.value
        elif selectedResp.full_pred_3_slot_valids_1.value == 1:
            return selectedResp.full_pred_3_targets_1.value
        return selectedResp.full_pred_3_fallThroughAddr.value
    else:
        # not taken
        return selectedResp.pc_3.value + 32

def getCfi_ref(selectedResp: BranchPredictionBundle):
    hit = selectedResp.full_pred_3_hit.value
    if hit:
        if selectedResp.full_pred_3_slot_valids_0.value == 1 and selectedResp.full_pred_3_br_taken_mask_0.value == 1:
            valid = 1
            offset = selectedResp.full_pred_3_offsets_0.value
        elif selectedResp.full_pred_3_is_br_sharing.value:
            if selectedResp.full_pred_3_slot_valids_1.value == 1 and selectedResp.full_pred_3_br_taken_mask_1.value == 1:
                valid = 1
                offset = selectedResp.full_pred_3_offsets_1.value
            else:
                valid = 0
                offset = 15 # when no takens, set cfiIndex to PredictWidth-1
        elif selectedResp.full_pred_3_slot_valids_1.value == 1:
            valid = 1
            offset = selectedResp.full_pred_3_offsets_1.value
        else:
            valid = 0
            offset = 15
    else:
        valid = 0
        offset = 15
    return {"valid":valid, "bits": offset}

h_not_hit, h_false_hit,  h_hit = range(3)

c_empty     = 0
c_toCommit  = 1
c_committed = 2
c_flushed   = 3

def validInstructions_ref(dut):

    # canCommit = dut.gen_rob_comm_ptr() != dut.gen_ifu_wb_ptr() and not dut.bpu_ftb_update_stall.value == 0
    commPtr = dut.gen_comm_ptr()
    row = [i.value for i in dut.commitStateQueue[commPtr.value]]
    validInstructions = [
        (s == c_toCommit or s == c_committed)
        for s in row
    ]
    return validInstructions

def lastInstructionStatus_ref(dut, validInstructions):
    commPtr = dut.gen_comm_ptr()
    row = [i.value for i in dut.commitStateQueue[commPtr.value]]
    indices = [i for i, v in enumerate(validInstructions) if v]
    idx = indices[-1] if indices else -1
    if idx >= 0:
        return row[idx]
    else:
        return None

def firstInstructionFlushed_ref(row):
    firstInstructionFlushed = (
    row[0] == c_flushed or (row[0] == c_empty and row[1] == c_flushed))
    return firstInstructionFlushed

def canCommit_ref(dut, validInstructions):
    has_valid = any(validInstructions)
    commPtr = dut.gen_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    robCommPtr = dut.gen_rob_comm_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions)
    # print("lastInstructionStatus: ", lastInstructionStatus)
    # print("commPtr: ", commPtr.value)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canCommit = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
            (robCommPtr > commPtr)
            or (
                has_valid
                and lastInstructionStatus == c_committed
            )
        )
    )
    return canCommit

def canMoveCommPtr_ref(dut, validInstructions):
    has_valid = any(validInstructions)
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions)
    commPtr = dut.gen_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    robCommPtr = dut.gen_rob_comm_ptr()
    commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
    firstInstructionFlushed = firstInstructionFlushed_ref(commit_state)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canMoveCommPtr = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
                (robCommPtr > commPtr)
                or (
                    has_valid
                    and lastInstructionStatus == c_committed
                )
                or firstInstructionFlushed
        )
    )
    return canMoveCommPtr

def last_valid_rob_commit_ref(fromBackend: FromBackendBundle):
    rob_commits = []
    for i in range(8):
        rob_commit = getattr(fromBackend, f"rob_commits_{i}")
        rob_commits.append(rob_commit)

    valid_commits = [commit for commit in rob_commits if commit.valid.value == 1]

    return valid_commits[-1] if valid_commits else None


def mmioLastCommit_ref(dut):
    commPtr = dut.gen_comm_ptr()
    # mmioReadValid = dut.mmioReadValid.value
    mmioReadValid = 1
    mmioReadPtr = dut.gen_mmio_ftq_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions_ref(dut))
    has_valid = any(validInstructions_ref(dut))
    mmioLastCommit = (
        mmioReadValid
        and (
            (commPtr > mmioReadPtr)
            or (
                commPtr == mmioReadPtr
                and has_valid
                and lastInstructionStatus == c_committed
            )
        )
    )
    return mmioLastCommit

TAR_OVF = 1
TAR_UDF = 2
TAR_FIT = 0
BR_OFFSET_LEN  = 12
JMP_OFFSET_LEN = 20

class FtbSlot:
    def __init__(self, offsetLen, subOffsetLen=None):
        if subOffsetLen is not None:
            assert subOffsetLen <= offsetLen

        self.offsetLen = offsetLen
        self.subOffsetLen = subOffsetLen

        self.valid = False
        self.offset = 0

        self.lower = 0
        self.tarStat = TAR_FIT
        self.sharing = False


    def set_lower_stat_by_target(self, pc, target, is_share):
        offLen = self.subOffsetLen if is_share else self.offsetLen
        VAddrBits = 50
        shift_amt = offLen + 1
        higher_mask = (1 << (VAddrBits - shift_amt)) - 1
        
        pc_higher = (pc >> shift_amt) & higher_mask
        target_higher = (target >> shift_amt) & higher_mask

        if target_higher > pc_higher:
            stat = TAR_OVF
        elif target_higher < pc_higher:
            stat = TAR_UDF
        else:
            stat = TAR_FIT

        lower_mask = (1 << offLen) - 1
        raw_lower = (target >> 1) & lower_mask

        self.lower = raw_lower & ((1 << self.offsetLen) - 1)
        
        self.tarStat = stat
        self.sharing = int(is_share)


    
    # --------------------------------------
    # getTarget 
    # --------------------------------------
    def get_target(self, pc):
        offLen = self.subOffsetLen if self.sharing else self.offsetLen
        assert offLen is not None and offLen > 0

        pc_higher = pc >> (offLen + 1)

        if self.tarStat == TAR_OVF:
            higher = pc_higher + 1
        elif self.tarStat == TAR_UDF:
            higher = pc_higher - 1
        else:
            higher = pc_higher

        target = (
            (higher << (offLen + 1))
            | (self.lower << 1)
        )

        return target

    # --------------------------------------
    # fromAnotherSlot
    # --------------------------------------
    def from_another_slot(self, that):
        if self.offsetLen > that.offsetLen:
            assert self.subOffsetLen == that.offsetLen
            self.sharing = True
        else:
            assert self.offsetLen == that.offsetLen
            self.sharing = False

        self.offset = that.offset
        self.tarStat = that.tarStat
        self.valid = that.valid

        # ZeroExt 
        self.lower = that.lower

from copy import deepcopy



class TailSlot(FtbSlot):
    def set_by_jmp_target(self, pc, target):
        self.set_lower_stat_by_target(pc, target, False)

class FTBEntry:
    def __init__(self, numBrSlot, dict=None):
        self.numBrSlot = numBrSlot
        self.numBr = numBrSlot + 1
        self.valid = False
        numBr = self.numBr

        self.brSlots = [
            FtbSlot(offsetLen=BR_OFFSET_LEN)
            for _ in range(numBrSlot)
        ]

        self.strong_bias = [False] * numBr

        self.tailSlot = TailSlot(offsetLen=JMP_OFFSET_LEN, subOffsetLen=BR_OFFSET_LEN)
        self.allSlots = [*self.brSlots, self.tailSlot]

        self.pftAddr = 0
        self.carry = False

        self.isJalr = False  
        self.isCall = False
        self.isRet = False
        self.last_may_be_rvi_call = False
        if dict is not None:
            self.valid = dict.get("valid", False)
            self.pftAddr = dict.get("pftAddr", 0)
            self.carry = dict.get("carry", False)
            self.isJalr = dict.get("isJalr", False)
            self.isCall = dict.get("isCall", False)
            self.isRet = dict.get("isRet", False)
            self.last_may_be_rvi_call = dict.get("last_may_be_rvi_call", False)

            for i in range(numBrSlot):
                slot_dict = {
                    "valid": dict.get(f"brSlots_{i}_valid", False),
                    "offset": dict.get(f"brSlots_{i}_offset", 0),
                    "lower": dict.get(f"brSlots_{i}_lower", 0),
                    "tarStat": dict.get(f"brSlots_{i}_tarStat", TAR_FIT),
                    "sharing": dict.get(f"brSlots_{i}_sharing", False),
                }
                self.brSlots[i].valid = slot_dict["valid"]
                self.brSlots[i].offset = slot_dict["offset"]
                self.brSlots[i].lower = slot_dict["lower"]
                self.brSlots[i].tarStat = slot_dict["tarStat"]
                self.brSlots[i].sharing = slot_dict["sharing"]
            
            for i in range(numBr):
                self.strong_bias[i] = dict.get(f"strong_bias_{i}", False)

            tail_dict = {
                "valid": dict.get("tailSlot_valid", False),
                "offset": dict.get("tailSlot_offset", 0),
                "lower": dict.get("tailSlot_lower", 0),
                "tarStat": dict.get("tailSlot_tarStat", TAR_FIT),
                "sharing": dict.get("tailSlot_sharing", False),
            }
            self.tailSlot.valid = tail_dict["valid"]
            self.tailSlot.offset = tail_dict["offset"]
            self.tailSlot.lower = tail_dict["lower"]
            self.tailSlot.tarStat = tail_dict["tarStat"]
            self.tailSlot.sharing = tail_dict["sharing"]

    # ---------------------------
    # helper functions
    # ---------------------------

    def get_br_recorded_vec(self, offset):
        return [
            slot.valid and slot.offset == offset
            for slot in self.brSlots
        ] + [
            self.tailSlot.valid and self.tailSlot.offset == offset and self.tailSlot.sharing
        ]

    @property
    def brValids(self):
        return [s.valid for s in self.brSlots] + [
            self.tailSlot.valid and self.tailSlot.sharing
        ]

    @property
    def brOffset(self):
        return [s.offset for s in self.brSlots] + [
            self.tailSlot.offset
        ]

    @property
    def jmpValid(self):
        return self.tailSlot.valid and not self.tailSlot.sharing

    @property
    def noEmptySlotForNewBr(self):
        return all(s.valid for s in self.allSlots)

    def as_dict(self):
        d = {
            "valid": self.valid,
            "pftAddr": self.pftAddr,
            "carry": self.carry,
            "isJalr": self.isJalr,
            "isCall": self.isCall,
            "isRet": self.isRet,
            "last_may_be_rvi_call": self.last_may_be_rvi_call,
        }
        for i in range(self.numBrSlot):
            d.update({
                f"brSlots_{i}_valid": self.brSlots[i].valid,
                f"brSlots_{i}_offset": self.brSlots[i].offset,
                f"brSlots_{i}_lower": self.brSlots[i].lower,
                f"brSlots_{i}_tarStat": self.brSlots[i].tarStat,
                f"brSlots_{i}_sharing": self.brSlots[i].sharing,
            })
        for i in range(self.numBr):
            d.update({
                f"strong_bias_{i}": self.strong_bias[i],
            })
        d.update({
            "tailSlot_valid": self.tailSlot.valid,
            "tailSlot_offset": self.tailSlot.offset,
            "tailSlot_lower": self.tailSlot.lower,
            "tailSlot_tarStat": self.tailSlot.tarStat,
            "tailSlot_sharing": self.tailSlot.sharing,
        })
        return d

    # ---------------------------
    # debug helper
    # ---------------------------
    def dump(self):
        print("FTBEntry:")
        print(" valid:", self.valid)
        for i, s in enumerate(self.brSlots):
            print(
                f"  BR[{i}] valid={s.valid} "
                f"offset={s.offset} lower={s.lower} "
                f"tarStat={s.tarStat} sharing={s.sharing} "
                f"bias={self.strong_bias[i]}"
            )
        print("  Tail:",
              "valid=", self.tailSlot.valid,
              "offset=", self.tailSlot.offset,
              "lower=", self.tailSlot.lower,
              "tarStat=", self.tailSlot.tarStat,
              "sharing=", self.tailSlot.sharing)
        print(" pftAddr:", self.pftAddr,
              "carry:", self.carry)

def ftb_entry_gen(
    start_addr,
    old_entry: FTBEntry,
    pd,
    cfiIndex_valid,
    cfiIndex_bits,
    target,
    hit, 
    mispredict_vec,
    numBrSlot=1,
    PredictWidth=16,
):
    numBr = numBrSlot + 1
    instOffsetBits = 1

    carryPos = (PredictWidth - 1).bit_length() + instOffsetBits  # log2Ceil 

    def get_lower(pc):
        # move instOffsetBits bit right ，then take  (carryPos - instOffsetBits) bits
        return (pc >> instOffsetBits) & ((1 << (carryPos - instOffsetBits)) - 1)

    # ------------------------------------------------
    # 1 init entry
    # ------------------------------------------------

    init_entry = FTBEntry(numBrSlot=1)
    init_entry.valid = True

    cfi_is_br = pd["brMask"][cfiIndex_bits] and cfiIndex_valid

    entry_has_jmp = pd["jmpInfo_valid"]

    new_jmp_is_jal = entry_has_jmp and not pd["jmpInfo_bits"][0] and cfiIndex_valid
    new_jmp_is_jalr = entry_has_jmp and pd["jmpInfo_bits"][0] and cfiIndex_valid
    new_jmp_is_call = entry_has_jmp and pd["jmpInfo_bits"][1] and cfiIndex_valid
    new_jmp_is_ret = entry_has_jmp and pd["jmpInfo_bits"][2] and cfiIndex_valid

    cfi_is_jal = cfiIndex_bits == pd["jmpOffset"] and new_jmp_is_jal
    cfi_is_jalr = cfiIndex_bits == pd["jmpOffset"] and new_jmp_is_jalr
    
    # ---- case br ----
    if cfi_is_br:
        print("cfi is br")
        slot = init_entry.brSlots[0]
        slot.valid = True
        slot.offset = cfiIndex_bits
        # slot.set_lower_stat_by_target(start_addr, target, numBr == 1)
        slot.set_lower_stat_by_target(start_addr, target, numBr == 1)

        init_entry.strong_bias[0] = True

    # print("cfiindex valid:", cfiIndex_valid)

    # ---- case jmp ----
    if entry_has_jmp:
        print("entry_has_jmp")
        init_entry.tailSlot.offset = pd["jmpOffset"]
        init_entry.tailSlot.valid = new_jmp_is_jal or new_jmp_is_jalr
        # print("DEBUG: start_addr = ", start_addr)
        # print("DEBUG: target = ", target)
        # print("DEBUG: jalTarget = ", pd["jalTarget"])
        init_entry.tailSlot.set_lower_stat_by_target(
            start_addr,
            target if cfi_is_jalr else pd["jalTarget"],
            False,
        )
        # print("DEBUG: tailSlot_lower = ", init_entry.tailSlot.lower)
        init_entry.strong_bias[-1] = new_jmp_is_jalr

    # last_jmp_rvi
    last_jmp_rvi = entry_has_jmp and pd["jmpOffset"] == (PredictWidth - 1) and not pd["rvcMask"][-1]

    # jmpPft
    jmp_inst_len = 1 if pd["rvcMask"][pd["jmpOffset"]] else 2
    jmp_pft = get_lower(start_addr) + pd["jmpOffset"] + jmp_inst_len
    # print("jmp_pft: ", jmp_pft)
    # print("lower start addr: ", get_lower(start_addr))
    # print("entry has jmp: ", entry_has_jmp)
    # print("last jmp rvi:", last_jmp_rvi)
    # print("jmpOffset: ", pd["jmpOffset"])
    # print("last rvc mask:",pd["rvcMask"][-1])

    if entry_has_jmp and not last_jmp_rvi:
        init_entry.pftAddr = jmp_pft & 0b1111
        init_entry.carry = (jmp_pft >> (carryPos - instOffsetBits)) & 1
    else:
        init_entry.pftAddr = get_lower(start_addr)
        init_entry.carry = True

    # last_may_be_rvi_call
    init_entry.last_may_be_rvi_call = (
        pd["jmpOffset"] == PredictWidth - 1 and not pd["rvcMask"][pd["jmpOffset"]]
    )

    init_entry.isJalr = new_jmp_is_jalr
    init_entry.isCall = new_jmp_is_call
    init_entry.isRet = new_jmp_is_ret

    # ------------------------------------------------
    # 2 hit check：check if it is new br
    # ------------------------------------------------

    oe = old_entry
    br_recorded_vec = oe.get_br_recorded_vec(cfiIndex_bits)
    br_recorded = any(br_recorded_vec)

    is_new_br = cfi_is_br and not br_recorded
    new_br_offset = cfiIndex_bits

    # insert position
    new_br_insert_onehot = []
    for i in range(numBr):
        if i == 0:
            cond = (not oe.brSlots[0].valid) or new_br_offset < oe.brSlots[0].offset
        else:
            cond = (
                oe.allSlots[i - 1].valid
                and new_br_offset > oe.allSlots[i - 1].offset
                and (
                    not oe.allSlots[i].valid
                    or new_br_offset < oe.allSlots[i].offset
                )
            )
        new_br_insert_onehot.append(cond)

    old_entry_modified = deepcopy(oe)

    # insert logic
    for i in range(numBr):
        slot = old_entry_modified.allSlots[i]

        if new_br_insert_onehot[i]:
            slot.valid = True
            slot.offset = new_br_offset
            slot.set_lower_stat_by_target(start_addr, target, i == numBr - 1)
            # slot.set_lower_stat_by_target(start_addr, target, False)
            old_entry_modified.strong_bias[i] = True

        elif new_br_offset > oe.allSlots[i].offset:
            old_entry_modified.strong_bias[i] = False

        else:
            if i != 0:
                noNeedToMoveFromFormerSlot = (i == numBr - 1) and not oe.brSlots[numBrSlot-1].valid
                if not noNeedToMoveFromFormerSlot:
                    slot.from_another_slot(oe.allSlots[i - 1])
                    old_entry_modified.strong_bias[i] = oe.strong_bias[i]
    
    may_have_to_replace = oe.noEmptySlotForNewBr  # 所有br槽都满了
    pft_need_to_change = is_new_br and may_have_to_replace


    if pft_need_to_change:

        if not any(new_br_insert_onehot):
            new_pft_offset = new_br_offset
        else:
            new_pft_offset = oe.allSlots[-1].offset


        lower_width = carryPos - instOffsetBits
        mask = (1 << lower_width) - 1

        base_lower = get_lower(start_addr) & mask
        
        pft_off = new_pft_offset & mask

        full_sum = base_lower + pft_off

        new_pft_addr = full_sum & mask
        
        carry_bit = (full_sum >> lower_width) & 1

        old_entry_modified.pftAddr = new_pft_addr
        old_entry_modified.carry = bool(carry_bit)

        old_entry_modified.last_may_be_rvi_call = False
        old_entry_modified.isCall = False
        old_entry_modified.isRet = False
        old_entry_modified.isJalr = False

        # print(f"[DEBUG] New PFT Addr: {hex(new_pft_addr)}, Carry: {old_entry_modified.carry}")
    # ------------------------------------------------
    # 3 jalr target modify
    # ------------------------------------------------

    old_target = oe.tailSlot.get_target(start_addr)
    old_tail_is_jmp = not oe.tailSlot.sharing

    jalr_target_modified = (
        new_jmp_is_jalr
        and old_target != target
        and old_tail_is_jmp
    )

    old_entry_jmp_target_modified = deepcopy(oe)

    if jalr_target_modified:
        old_entry_jmp_target_modified.tailSlot.set_lower_stat_by_target(
            start_addr, target, False
        )
        old_entry_jmp_target_modified.strong_bias = [False] * numBr

    # ------------------------------------------------
    # 4 strong bias modify
    # ------------------------------------------------

    old_entry_strong_bias = deepcopy(oe)
    strong_bias_modified = False

    if br_recorded_vec[0]:
        old_entry_strong_bias.strong_bias[0] = (
            oe.strong_bias[0] and cfiIndex_valid and oe.brSlots[0].valid 
            and cfiIndex_bits == oe.brSlots[0].offset
        )
    elif br_recorded_vec[numBr - 1]:
        old_entry_strong_bias.strong_bias[0] = False
        old_entry_strong_bias.strong_bias[numBr - 1] = (
            oe.strong_bias[numBr - 1] and cfiIndex_valid and oe.brValids[numBr - 1]
            and cfiIndex_bits == oe.brOffset[numBr - 1]
        )
    # strong_bias_modified
    for i in range(numBr):
        if oe.strong_bias[i] and oe.brValids[i] and not old_entry_strong_bias.strong_bias[i]:
            strong_bias_modified = True
            break
    # ------------------------------------------------
    # 5 choose final entry
    # ------------------------------------------------

    if not hit:
        new_entry = init_entry
    else:
        if is_new_br:
            new_entry = old_entry_modified
            print("use old_entry_modified result")
        elif jalr_target_modified:
            new_entry = old_entry_jmp_target_modified
            print("use old_entry_jmp_target_modified result")
        else:
            new_entry = old_entry_strong_bias
            print("use old_entry_strong_bias result")

    # ------------------------------------------------
    # 6 out put signal
    # ------------------------------------------------

    taken_mask = [
        cfiIndex_valid and new_entry.brValids[i] and
        new_entry.brOffset[i] == cfiIndex_bits
        for i in range(numBr)
    ]

    jmp_taken = (
        new_entry.jmpValid
        and new_entry.tailSlot.offset == cfiIndex_bits
    )

    mispred_mask = [
        new_entry.brValids[i]
        and mispredict_vec[new_entry.brOffset[i]]
        for i in range(numBr)
    ]

    mispred_mask.append(
        new_entry.jmpValid
        and mispredict_vec[pd["jmpOffset"]]
    )

    if hit and not is_new_br and not jalr_target_modified and not strong_bias_modified:
        print("ftb_entry_gen result is old entry")
    else:
        print("ftb_entry_gen result is new entry")
    print("FTB entry hit" if hit else "FTB entry miss")
    return {
        "new_entry": new_entry,
        "new_br_insert_pos": new_br_insert_onehot,
        "taken_mask": taken_mask,
        "jmp_taken": jmp_taken,
        "mispred_mask": mispred_mask,
        "is_init_entry": not hit,
        "is_old_entry": hit and not is_new_br and not jalr_target_modified and not strong_bias_modified,
        "is_new_br": hit and is_new_br,
        "is_jalr_target_modified": hit and jalr_target_modified,
        "is_strong_bias_modified": hit and strong_bias_modified,
        "is_br_full": hit and is_new_br and oe.noEmptySlotForNewBr,
        "cfi_is_br": cfi_is_br
    }

def commit_mispredict(
    mis,
    commit_state,
):

    return [
        m and (state == c_committed)
        for m, state in zip(mis, commit_state)
    ]
