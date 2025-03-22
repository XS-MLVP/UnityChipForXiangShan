__all__ = ["BranchPredictDriver", "BranchPredictMonitor", "BranchUpdateDriver", "ControlBundle", "BranchUpdateDriver"]

from toffee import Bundle, Signal, Signals


class CtrlBundle(Bundle):
    tage_enable, sc_enable = Signals(2)


class ControlBundle(Bundle):
    s1_ready = Signal()
    # 0->BPU, 1->Tage, 3->SC
    s0_fire_0, s1_fire_0, s2_fire_0 = Signals(3)
    s0_fire_1, s1_fire_1, s2_fire_1 = Signals(3)
    s0_fire_2, s1_fire_2, s2_fire_2 = Signals(3)
    s0_fire_3, s1_fire_3, s2_fire_3 = Signals(3)

    ctrl = CtrlBundle().from_prefix("ctrl_")

    def s0_fire_xdata(self, i):
        return (self.s0_fire_0, self.s0_fire_1, self.s0_fire_2, self.s0_fire_3)[i]

    def s1_fire_xdata(self, i):
        return (self.s1_fire_0, self.s1_fire_1, self.s1_fire_2, self.s1_fire_3)[i]

    def s2_fire_xdata(self, i):
        return (self.s2_fire_0, self.s2_fire_1, self.s2_fire_2, self.s2_fire_3)[i]

    def s2_valid_fire(self, i):
        return self.s2_fire_xdata(i).value and self.s1_ready.value


class TageFoldedHistoryBundle(Bundle):
    [hist_1_folded_hist, hist_3_folded_hist,
     hist_4_folded_hist, hist_5_folded_hist,
     hist_7_folded_hist,
     hist_8_folded_hist, hist_9_folded_hist,
     hist_14_folded_hist, hist_15_folded_hist,
     hist_16_folded_hist, hist_17_folded_hist] = Signals(11)


class SCFoldedHistoryBundle(Bundle):
    hist_2_folded_hist, hist_11_folded_hist, hist_12_folded_hist = Signals(3)


class FTBBranchSlotBundle(Bundle):
    valid = Signal()


class FTBTailSlotBundle(Bundle):
    valid, sharing = Signals(2)


class FTBEntryBundle(Bundle):
    strong_bias_0, strong_bias_1 = Signals(2)
    br_slot = FTBBranchSlotBundle.from_prefix("brSlots_0_")
    tail_slot = FTBTailSlotBundle.from_prefix("tailSlot_")

    def get_strong_bias(self, way: int):
        return (self.strong_bias_0, self.strong_bias_1)[way].value


class BranchPredictionBundle(Bundle):
    br_taken_mask_0, br_taken_mask_1 = Signals(2)


class BranchPredictDriver(Bundle):
    bits_s0_pc_0, bits_s0_pc_1, bits_s0_pc_2, bits_s0_pc_3 = Signals(4)
    bits_ghist = Signal()
    fh_tage = TageFoldedHistoryBundle.from_prefix("bits_folded_hist_1_")
    fh_sc = SCFoldedHistoryBundle.from_prefix("bits_folded_hist_3_")


class BranchPredictMonitor(Bundle):
    last_stage_meta = Signal()
    s2 = BranchPredictionBundle.from_prefix("s2_full_pred_3_")
    s3 = BranchPredictionBundle.from_prefix("s3_full_pred_3_")


class BranchPredictionUpdate(Bundle):
    pc, meta, br_taken_mask_0, br_taken_mask_1, mispred_mask_0, mispred_mask_1 = Signals(6)
    ghist = Signal()
    ftb_entry = FTBEntryBundle.from_prefix("ftb_entry_")


class BranchUpdateDriver(Bundle):
    valid = Signal()
    bits = BranchPredictionUpdate.from_prefix("bits_")
