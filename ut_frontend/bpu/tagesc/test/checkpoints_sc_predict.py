from toffee.funcov import CovGroup

__all__ = ["get_coverage_group_of_sc_predict"]

from comm import UT_FCOV
from dut.tage_sc.UT_Tage_SC import DUTTage_SC


def is_calculate_predict_total_sum(way: int):
    def calculate_predict_total_sum(dut: DUTTage_SC) -> bool:
        valid = dut.io_s1_ready.value != 0 and dut.io_s2_fire_3.value != 0
        return valid

    return calculate_predict_total_sum


def is_not_use_sc_as_tage_use_alt(way: int, tn_hit: int):
    def not_use_sc_as_tage_use_alt(dut: DUTTage_SC) -> bool:
        use_alt = getattr(dut, f"Tage_SC_s2_altUsed_{way}").value
        valid = dut.io_s1_ready.value != 0 and dut.io_s2_fire_3.value != 0
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value  # sc_used is same as provided
        tage_taken = getattr(dut, f"Tage_SC_s2_tageTakens_dup_0_{way}").value
        total_sum = getattr(dut, f"Tage_SC_s2_totalSums_{tage_taken}" + ("_1" if way else "")).S()
        threshold = getattr(dut, f"Tage_SC_scThresholds_{way}_thres").value
        above_threshold = abs(total_sum) > threshold
        use_sc = provided and above_threshold

        return valid and use_alt and not use_sc and (tn_hit == provided)

    return not_use_sc_as_tage_use_alt


def is_tage_taken_from_tn(way: int, use_sc_excp: int):
    def tage_taken_from_tn(dut: DUTTage_SC) -> bool:
        use_alt = getattr(dut, f"Tage_SC_s2_altUsed_{way}").value
        valid = dut.io_s1_ready.value != 0 and dut.io_s2_fire_3.value != 0
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value  # sc_used is same as provided
        tage_taken = getattr(dut, f"Tage_SC_s2_tageTakens_dup_0_{way}").value
        total_sum = getattr(dut, f"Tage_SC_s2_totalSums_{tage_taken}" + ("_1" if way else "")).S()
        threshold = getattr(dut, f"Tage_SC_scThresholds_{way}_thres").value
        above_threshold = abs(total_sum) > threshold
        use_sc = provided and above_threshold

        return valid and provided and not use_alt and (use_sc == use_sc_excp)

    return tage_taken_from_tn


def get_coverage_group_of_sc_predict(dut: DUTTage_SC) -> CovGroup:
    slot_name = ["br_slot_0", "tail_slot"]

    g = CovGroup(UT_FCOV("UT_Tage_SC", "UnityChipForXiangShan.ut_", parent=-1))

    # Calculate TotalSum in SC predict
    g.add_watch_point(
        dut,
        {slot_name[w]: is_calculate_predict_total_sum(w) for w in range(2)},
        name="SC Predict Calculate TotalSum "
    )
    # SC doesn't use as Alt is used
    for hit in range(2):
        s = "SC is Not Used and TAGE Use T0, Tn " + ("Hit" if hit else "Miss")
        g.add_watch_point(dut, {slot_name[w]: is_not_use_sc_as_tage_use_alt(w, hit) for w in range(2)}, name=s)

    # TAGE provider is used, and SC change/doesn't change prediction.
    for use_sc in range(2):
        s = " ".join(["SC", ("is used" if use_sc else "is NOT used"), ",", "TAGE use Tn"])
        g.add_watch_point(
            dut,
            {slot_name[w]: is_tage_taken_from_tn(w, use_sc) for w in range(2)},
            name=s
        )

    return g
