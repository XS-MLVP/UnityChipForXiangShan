__all__ = ['get_coverage_group_of_sc_train']

from toffee.funcov import CovGroup

from comm import UT_FCOV
from ..env.tage_sc_env import TageSCEnv
from ..util.meta_parser import GetMetaParser


def is_update_calculate_total_sum(way: int):
    def update_calculate_total_sum(test_env: TageSCEnv) -> bool:
        valid = test_env.ctrl_bundle.s1_ready.value and test_env.internal_monitor.update.valid(way)
        with GetMetaParser(test_env.update_driver.bits.meta.value) as meta_parser:
            tage_valid = meta_parser.providers_valid[way].value
            return valid and tage_valid

    return update_calculate_total_sum


def is_sc_table_saturing(way: int, ti: int, up_or_down: int):
    def sc_table_saturing(test_env: TageSCEnv):
        v = 31 if up_or_down else -32
        sc_table = test_env.internal_monitor.sc.get_table(ti)
        pc = sc_table.io_update_pc.value
        mask = sc_table.update_mask(pc, way)
        old_ctr = sc_table.old_ctr(way)
        train_taken = sc_table.update_taken(way)
        valid = test_env.ctrl_bundle.s1_ready.value != 0 and mask != 0
        return valid and old_ctr == v and up_or_down == train_taken

    return sc_table_saturing


def is_update_threshold_ctr_saturing_to_neutral(way: int, up_or_down: int):
    def update_threshold_ctr_saturing_to_neutral(test_env: TageSCEnv):
        update_valid = test_env.internal_monitor.update.valid(way)
        total_sum = test_env.internal_monitor.above_threshold_total_sum(way)
        threshold = test_env.internal_monitor.sc_threshold_thres(way)
        new_ctr = test_env.internal_monitor.new_threshold_ctr(way)
        valid = test_env.ctrl_bundle.s1_ready.value and update_valid \
                and (threshold - 4 <= total_sum <= threshold - 2)
        return valid and (new_ctr == (0b11111 if up_or_down else 0))

    return update_threshold_ctr_saturing_to_neutral


def is_update_threshold_threshold_saturing_to_neutral(way: int, up_or_down: int):
    def update_threshold_threshold_saturing_to_neutral(test_env: TageSCEnv):
        v = 32 if up_or_down else 4
        threshold = test_env.internal_monitor.sc_threshold_thres(way)
        valid = test_env.ctrl_bundle.s1_ready.value
        return valid and threshold == v

    return update_threshold_threshold_saturing_to_neutral


slot_name = ["br_slot_0", "tail_slot"]


def get_coverage_group_of_sc_train(test_env: TageSCEnv) -> CovGroup:
    g = CovGroup(UT_FCOV("../UT_Tage_SC"))
    for up_or_down in range(2):
        s = "Up Saturing" if up_or_down else "Down Saturing"
        # ctr up/down saturing update
        g.add_watch_point(
            test_env,
            {slot_name[w]: is_update_threshold_ctr_saturing_to_neutral(w, up_or_down) for w in range(2)},
            name="SC Threshold Counter is " + s
        )
        # thres up/down saturing update
        g.add_watch_point(
            test_env,
            {slot_name[w]: is_update_threshold_threshold_saturing_to_neutral(w, up_or_down) for w in range(2)},
            name="SC Threshold Threshold is " + s
        )
    # Tn up/down saturing update
    for up_or_down in range(2):
        s = "Down Saturing" if up_or_down else "Up Saturing"
        g.add_watch_point(
            test_env,
            {slot_name[w]: is_sc_table_saturing(w, i, up_or_down) for i in range(4) for w in range(2)},
            name="SC Table is " + s
        )

    g.add_watch_point(
        test_env,
        {slot_name[w]: is_update_calculate_total_sum(w) for w in range(2)},
        name=f"SC Train Calculate TotalSum"
    )

    return g
