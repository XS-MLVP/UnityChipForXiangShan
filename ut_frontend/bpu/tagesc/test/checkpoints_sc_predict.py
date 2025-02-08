__all__ = ["get_coverage_group_of_sc_predict"]

from toffee.funcov import CovGroup

from comm import UT_FCOV
from ..env.tage_sc_env import TageSCEnv


def is_calculate_predict_total_sum():
    def calculate_predict_total_sum(test_env: TageSCEnv) -> bool:
        return test_env.ctrl_bundle.s2_valid_fire(3)

    return calculate_predict_total_sum


def is_not_use_sc_as_tage_use_alt(way: int, tn_hit: int):
    def not_use_sc_as_tage_use_alt(test_env: TageSCEnv) -> bool:
        internal = test_env.internal_monitor
        use_alt = internal.s2.alt_used(way)
        valid = test_env.ctrl_bundle.s2_valid_fire(3)
        provided = internal.s2.provided(way)
        tage_taken = internal.s2.tage_taken(way)
        total_sum = internal.s2.total_sum(way)[tage_taken]
        threshold = internal.sc_threshold_thres(way)
        above_threshold = abs(total_sum) > threshold
        use_sc = provided and above_threshold
        return valid and use_alt and not use_sc and (tn_hit == provided)

    return not_use_sc_as_tage_use_alt


def is_tage_taken_from_tn(way: int, use_sc_excp: int):
    def tage_taken_from_tn(test_env: TageSCEnv) -> bool:
        internal = test_env.internal_monitor
        use_alt = internal.s2.alt_used(way)
        valid = test_env.ctrl_bundle.s2_valid_fire(3)
        provided = internal.s2.provided(way)
        tage_taken = internal.s2.tage_taken(way)
        total_sum = internal.s2.total_sum(way)[tage_taken]
        threshold = internal.sc_threshold_thres(way)
        above_threshold = abs(total_sum) > threshold
        use_sc = provided and above_threshold
        return valid and provided and not use_alt and (use_sc == use_sc_excp)

    return tage_taken_from_tn


def get_coverage_group_of_sc_predict(test_env: TageSCEnv) -> CovGroup:
    slot_name = ["br_slot_0", "tail_slot"]

    g = CovGroup(UT_FCOV("../UT_Tage_SC"))

    # Calculate TotalSum in SC predict
    g.add_watch_point(test_env, {"trigger_times": is_calculate_predict_total_sum()},
                      name="SC Predict Calculate TotalSum")
    # SC doesn't use as Alt is used
    for hit in range(2):
        s = "SC is Not Used and TAGE Use T0, Tn " + ("Hit" if hit else "Miss")
        g.add_watch_point(test_env, {slot_name[w]: is_not_use_sc_as_tage_use_alt(w, hit) for w in range(2)}, name=s)

    # TAGE provider is used, and SC change/doesn't change prediction.
    for use_sc in range(2):
        s = " ".join(["SC", ("is used" if use_sc else "is NOT used"), ",", "TAGE use Tn"])
        g.add_watch_point(
            test_env,
            {slot_name[w]: is_tage_taken_from_tn(w, use_sc) for w in range(2)},
            name=s
        )

    return g
