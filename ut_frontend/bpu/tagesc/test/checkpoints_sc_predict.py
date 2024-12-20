__all__ = ["get_coverage_group_of_sc_predict"]

from toffee.funcov import CovGroup

from comm import UT_FCOV
from ..bundle.internal import StatusBundle


def is_calculate_predict_total_sum(way: int):
    def calculate_predict_total_sum(status: StatusBundle) -> bool:
        return status.s2_valid(3)

    return calculate_predict_total_sum


def is_not_use_sc_as_tage_use_alt(way: int, tn_hit: int):
    def not_use_sc_as_tage_use_alt(status: StatusBundle) -> bool:
        internal = status.internal
        use_alt = internal.s2.alt_used(way)
        valid = status.s2_valid(3)
        provided = internal.s2.provided(way)
        tage_taken = internal.s2.tage_taken(way)
        total_sum = internal.s2.total_sum(way, tage_taken)
        threshold = internal.sc_threshold(way)
        above_threshold = abs(total_sum) > threshold
        use_sc = provided and above_threshold
        return valid and use_alt and not use_sc and (tn_hit == provided)

    return not_use_sc_as_tage_use_alt


def is_tage_taken_from_tn(way: int, use_sc_excp: int):
    def tage_taken_from_tn(status: StatusBundle) -> bool:
        internal = status.internal
        use_alt = internal.s2.alt_used(way)
        valid = status.s2_valid(3)
        provided = internal.s2.provided(way)
        tage_taken = internal.s2.tage_taken(way)
        total_sum = internal.s2.total_sum(way, tage_taken)
        threshold = internal.sc_threshold(way)
        above_threshold = abs(total_sum) > threshold
        use_sc = provided and above_threshold
        return valid and provided and not use_alt and (use_sc == use_sc_excp)

    return tage_taken_from_tn


def get_coverage_group_of_sc_predict(status: StatusBundle) -> CovGroup:
    slot_name = ["br_slot_0", "tail_slot"]

    g = CovGroup(UT_FCOV("../UT_Tage_SC"))

    # Calculate TotalSum in SC predict
    g.add_watch_point(
        status,
        {slot_name[w]: is_calculate_predict_total_sum(w) for w in range(2)},
        name="SC Predict Calculate TotalSum "
    )
    # SC doesn't use as Alt is used
    for hit in range(2):
        s = "SC is Not Used and TAGE Use T0, Tn " + ("Hit" if hit else "Miss")
        g.add_watch_point(status, {slot_name[w]: is_not_use_sc_as_tage_use_alt(w, hit) for w in range(2)}, name=s)

    # TAGE provider is used, and SC change/doesn't change prediction.
    for use_sc in range(2):
        s = " ".join(["SC", ("is used" if use_sc else "is NOT used"), ",", "TAGE use Tn"])
        g.add_watch_point(
            status,
            {slot_name[w]: is_tage_taken_from_tn(w, use_sc) for w in range(2)},
            name=s
        )

    return g
