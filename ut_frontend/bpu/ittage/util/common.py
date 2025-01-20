__all__ = ['gen_dummy_update_req', 'UpdateReq', 'get_folded_hist']

from ..env.global_history import GlobalHistory


def gen_dummy_update_req(pc, meta):
    update_req = {}
    update_req["valid"] = 1
    update_req["bits_pc"] = pc

    update_req["ftb_entry"] = {}
    update_req["ftb_entry"]["tailSlot_offset"] = 0
    update_req["ftb_entry"]["tailSlot_sharing"] = 0
    update_req["ftb_entry"]["tailSlot_valid"] = 1
    update_req["ftb_entry"]["isRet"] = 0
    update_req["ftb_entry"]["isJalr"] = 1

    update_req["cfi"] = {}
    update_req["cfi"]["valid"] = 1
    update_req["cfi"]["bits"] = 0

    update_req["bits_jmp_taken"] = 1
    update_req["bits_mispred_mask_2"] = 1
    update_req["bits_meta"] = meta
    return update_req


def get_folded_hist(hist: int) -> dict:
    ghv = GlobalHistory(hist)
    return {
        "hist_14_folded_hist": ghv.get_fh(8, 8),
        "hist_13_folded_hist": ghv.get_fh(9, 13),
        "hist_12_folded_hist": ghv.get_fh(4, 4),
        "hist_10_folded_hist": ghv.get_fh(9, 32),
        "hist_6_folded_hist": ghv.get_fh(9, 16),
        "hist_4_folded_hist": ghv.get_fh(8, 13),
        "hist_3_folded_hist": ghv.get_fh(8, 32),
        "hist_2_folded_hist": ghv.get_fh(8, 16),
    }


class FtbEntry:
    def __init__(self):
        self.tailSlot_offset = 0
        self.tailSlot_sharing = 0
        self.tailSlot_valid = 1
        self.isRet = 0
        self.isJalr = 1


class CfiReq:
    def __init__(self):
        self.valid = 1
        self.bits = 0


class UpdateReq:
    def __init__(self, pc: int, meta: int, full_target: int, hist: int, mis_pred: int):
        self.valid = 1
        self.bits_pc = pc

        self.ftb_entry = FtbEntry()

        self.cfi = CfiReq()

        self.bits_jmp_taken = 1
        self.bits_mispred_mask_2 = mis_pred
        self.bits_meta = meta
        self.hist = hist

        self.bits_full_target = full_target

    def asdict(self) -> dict:
        update_req = {}
        update_req["valid"] = self.valid
        update_req["bits_pc"] = self.bits_pc

        update_req["ftb_entry"] = {}
        update_req["ftb_entry"]["tailSlot_offset"] = self.ftb_entry.tailSlot_offset
        update_req["ftb_entry"]["tailSlot_sharing"] = self.ftb_entry.tailSlot_sharing
        update_req["ftb_entry"]["tailSlot_valid"] = self.ftb_entry.tailSlot_valid
        update_req["ftb_entry"]["isRet"] = self.ftb_entry.isRet
        update_req["ftb_entry"]["isJalr"] = self.ftb_entry.isJalr

        update_req["cfi"] = {}
        update_req["cfi"]["valid"] = self.cfi.valid
        update_req["cfi"]["bits"] = self.cfi.bits

        update_req["bits_jmp_taken"] = self.bits_jmp_taken
        update_req["bits_mispred_mask_2"] = self.bits_mispred_mask_2
        update_req["bits_meta"] = self.bits_meta
        update_req["bits_full_target"] = self.bits_full_target

        # update_req["folded_hist"] = get_folded_hist(self.hist)
        update_req["bits_ghist"] = self.hist

        return update_req