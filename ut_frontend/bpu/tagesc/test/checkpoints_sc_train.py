from toffee.funcov import CovGroup

from dut.tage_sc.UT_Tage_SC import DUTTage_SC
from ..util.meta_parser import MetaParser

__all__ = ['get_coverage_group_of_sc_train']


def get_idx(pc: int, way: int):
    return ((pc >> 1) & 1) ^ (way & 1)


def is_update_calculate_total_sum(way: int):
    def update_calculate_total_sum(dut: DUTTage_SC) -> bool:
        valid = dut.io_s1_ready.value != 0 and getattr(dut, f"Tage_SC_updateValids_{way}").value
        with MetaParser(dut.io_update_bits_meta.value) as meta_parser:
            tage_valid = meta_parser.providers_valid[way]
            return valid and tage_valid

    return update_calculate_total_sum


def is_sc_table_saturing(way: int, ti: int, up_or_down: int):
    def sc_table_saturing(dut: DUTTage_SC):
        v = 31 if up_or_down else -32
        w_idx = get_idx(getattr(dut, f"Tage_SC_scTables_{ti}_io_update_pc").value, way)
        mask = getattr(dut, f"Tage_SC_scTables_{ti}_io_update_mask_{w_idx}").value
        old_ctr = getattr(dut, f"Tage_SC_scTables_{ti}_oldCtr" + ("_1" if way else "")).S()
        train_taken = getattr(dut, f"Tage_SC_scTables_{ti}_taken" + ("_1" if way else "")).value
        valid = dut.io_s1_ready.value != 0 and mask != 0
        return valid and old_ctr == v and up_or_down == train_taken

    return sc_table_saturing


def is_update_threshold_ctr_saturing_to_neutral(way: int, up_or_down: int):
    def update_threshold_ctr_saturing_to_neutral(dut: DUTTage_SC):
        update_valid = getattr(dut, f"Tage_SC_updateValids_{way}").value
        total_sum = getattr(dut, "Tage_SC_sumAboveThreshold_totalSum" + ("_1" if way else "")).S()
        threshold = getattr(dut, f"Tage_SC_scThresholds_{way}_thres").value
        new_ctr = getattr(dut, "Tage_SC_newThres_newCtr" + ("_1" if way else "")).value
        valid = (dut.io_s1_ready.value != 0 and dut.io_update_valid.value != 0 and update_valid
                 and (threshold - 4 <= total_sum <= threshold - 2))

        return valid and (new_ctr == (0b11111 if up_or_down else 0))

    return update_threshold_ctr_saturing_to_neutral


def is_update_threshold_threshold_saturing_to_neutral(way: int, up_or_down: int):
    def update_threshold_threshold_saturing_to_neutral(dut: DUTTage_SC):
        v = 32 if up_or_down else 4
        threshold = getattr(dut, f"Tage_SC_scThresholds_{way}_thres").value
        valid = dut.io_s1_ready.value != 0
        return valid and threshold == v

    return update_threshold_threshold_saturing_to_neutral


slot_name = ["br_slot_0", "tail_slot"]


def get_coverage_group_of_sc_train(dut: DUTTage_SC) -> CovGroup:
    g = CovGroup("SC Train")
    for up_or_down in range(2):
        s = "Up Saturing" if up_or_down else "Down Saturing"
        # ctr up/down saturing update
        g.add_watch_point(
            dut,
            {slot_name[w]: is_update_threshold_ctr_saturing_to_neutral(w, up_or_down) for w in range(2)},
            name="SC Threshold Counter is " + s
        )
        # thres up/down saturing update
        g.add_watch_point(
            dut,
            {slot_name[w]: is_update_threshold_threshold_saturing_to_neutral(w, up_or_down) for w in range(2)},
            name="SC Threshold Threshold is " + s
        )
    # Tn up/down saturing update
    for up_or_down in range(2):
        s = "Down Saturing" if up_or_down else "Up Saturing"
        g.add_watch_point(
            dut,
            {slot_name[w]: is_sc_table_saturing(w, i, up_or_down) for i in range(4) for w in range(2)},
            name="SC Table is " + s
        )

    g.add_watch_point(
        dut,
        {slot_name[w]: is_update_calculate_total_sum(w) for w in range(2)},
        name=f"SC Train Calculate TotalSum"
    )

    return g
