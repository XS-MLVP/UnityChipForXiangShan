__all__ = ['UpdateBundle', 'InBundle', 'OutBundle', 'PipelineCtrl']

from toffee import Bundle, Signals, Signal

class PipelineCtrl(Bundle):
    s0_fire_0, s0_fire_1, s0_fire_2, s0_fire_3 = Signals(4)
    s1_fire_0, s1_fire_1, s1_fire_2, s1_fire_3 = Signals(4)
    s2_fire_0, s2_fire_1, s2_fire_2, s2_fire_3 = Signals(4)

class FullPred(Bundle):
    jalr_target = Signal()

class FoldedHist(Bundle):
    [hist_14_folded_hist, hist_13_folded_hist   , hist_12_folded_hist   , hist_10_folded_hist,
     hist_6_folded_hist , hist_4_folded_hist    , hist_3_folded_hist    , hist_2_folded_hist] = Signals(8)

class FTBEntry(Bundle):
    tailSlot_offset, tailSlot_sharing, tailSlot_valid, isRet, isJalr = Signals(5)

class CFI(Bundle):
    valid, bits = Signals(2)

# io_update_
class UpdateBundle(Bundle):
    valid, bits_pc, bits_jmp_taken, bits_mispred_mask_2, bits_meta, bits_full_target = Signals(6)
    bits_ghist = Signal()
    ftb_entry  = FTBEntry.from_prefix("bits_ftb_entry_")
    # folded_hist= FoldedHist.from_prefix("bits_spec_info_folded_hist_")
    cfi        = CFI.from_prefix("bits_cfi_idx_")

# io_in_
class InBundle(Bundle):
    bits_s0_pc_3 = Signal()

    folded_hist = FoldedHist.from_prefix("bits_s1_folded_hist_3_")
    pred0  = FullPred.from_prefix("bits_resp_in_0_s2_full_pred_0_")
    pred1  = FullPred.from_prefix("bits_resp_in_0_s2_full_pred_1_")
    pred2  = FullPred.from_prefix("bits_resp_in_0_s2_full_pred_2_")
    pred3  = FullPred.from_prefix("bits_resp_in_0_s2_full_pred_3_")

# io_out_
class OutBundle(Bundle):
    last_stage_meta = Signal()

    pred1  = FullPred.from_prefix("s3_full_pred_1_")
    pred0  = FullPred.from_prefix("s3_full_pred_0_")
    pred2  = FullPred.from_prefix("s3_full_pred_2_")
    pred3  = FullPred.from_prefix("s3_full_pred_3_")