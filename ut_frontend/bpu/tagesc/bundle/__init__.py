from toffee import Bundle, Signal, Signals

__all__ = ["BranchPredictReq", "BranchPredictionResp", "UpdateBundle", "CtrlBundle", "PipelineBundle"]


class CtrlBundle(Bundle):
    tage_enable, sc_enable = Signals(2)


class PipelineBundle(Bundle):
    # 0->BPU, 1->Tage, 3->SC
    s0_fire_0, s1_fire_0, s2_fire_0 = Signals(3)
    s0_fire_1, s1_fire_1, s2_fire_1 = Signals(3)
    s0_fire_2, s1_fire_2, s2_fire_2 = Signals(3)
    s0_fire_3, s1_fire_3, s2_fire_3 = Signals(3)


class FoldedHistoryBundle(Bundle):
    [hist_0_folded_hist, hist_1_folded_hist, hist_2_folded_hist, hist_3_folded_hist,
     hist_4_folded_hist, hist_5_folded_hist, hist_6_folded_hist, hist_7_folded_hist,
     hist_8_folded_hist, hist_9_folded_hist, hist_10_folded_hist, hist_11_folded_hist,
     hist_12_folded_hist, hist_13_folded_hist, hist_14_folded_hist, hist_15_folded_hist,
     hist_16_folded_hist, hist_17_folded_hist] = Signals(18)


class FTBSlotBundle(Bundle):
    valid, sharing = Signals(2)


class FTBEntryBundle(Bundle):
    always_taken_0, always_taken_1 = Signals(2)
    br_slot = FTBSlotBundle.from_prefix("brSlots_0_")
    tail_slot = FTBSlotBundle.from_prefix("tailSlot_")


class BranchPredictionBundle(Bundle):
    br_taken_mask_0, br_taken_mask_1 = Signals(2)


class BranchPredictReq(Bundle):
    bits_s0_pc_0, bits_s0_pc_1, bits_s0_pc_2, bits_s0_pc_3 = Signals(4)
    fh_tage = FoldedHistoryBundle.from_prefix("bits_folded_hist_1_")
    fh_sc = FoldedHistoryBundle.from_prefix("bits_folded_hist_3_")


class BranchPredictionResp(Bundle):
    last_stage_meta = Signal()
    s2 = BranchPredictionBundle.from_prefix(r"s2_full_pred_3_")
    s3 = BranchPredictionBundle.from_prefix(r"s3_full_pred_3_")


class BranchPredictionUpdate(Bundle):
    pc, meta, br_taken_mask_0, br_taken_mask_1, mispred_mask_0, mispred_mask_1 = Signals(6)
    ghist = Signal()
    ftb_entry = FTBEntryBundle.from_prefix("ftb_entry_")


class UpdateBundle(Bundle):
    valid = Signal()
    bits = BranchPredictionUpdate.from_prefix("bits_")
