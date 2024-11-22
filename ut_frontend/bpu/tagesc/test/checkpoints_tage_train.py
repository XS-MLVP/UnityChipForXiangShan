from toffee.funcov import CovGroup

from comm import UT_FCOV
from dut.Tage_SC import DUTTage_SC
from ..util.meta_parser import MetaParser

__all__ = ["get_coverage_group_of_tage_train"]

slot_name = ["br_slot_0", "tail_slot"]


def get_idx(pc: int, way: int):
    return ((pc >> 1) & 1) ^ (way & 1)


def is_update_t0_saturing_ctr(way: int, up_or_down: int):
    def update_t0_saturing(dut: DUTTage_SC) -> bool:
        v = 0b11 if up_or_down else 0
        w_idx = get_idx(dut.io_update_bits_pc.value, way)
        valid = dut.io_s1_ready.value and dut.Tage_SC_bt_bt_io_w_req_valid.value \
                and ((dut.Tage_SC_bt_bt_io_w_req_bits_waymask.value >> w_idx) & 1)
        old_ctr = getattr(dut, f"Tage_SC_bt_oldCtrs_{way}").value
        new_ctr = getattr(dut, f"Tage_SC_bt_newCtrs_{way}").value
        taken = getattr(dut, f"Tage_SC_bt_io_update_takens_{w_idx}").value
        return valid and new_ctr == v and old_ctr == v and (taken == up_or_down)

    return update_t0_saturing


def is_update_tn_saturing_ctr(way: int, t_i: int, up_or_down: int):
    def update_tn_saturing(dut: DUTTage_SC) -> bool:
        for b in range(4):
            silent = getattr(dut, f"Tage_SC_tables_{t_i}_per_bank_not_silent_update_{b}_{way}").value == 0

            w_idx = get_idx(dut.io_update_bits_pc.value, way)
            update_mask = getattr(dut, f"Tage_SC_tables_{t_i}_io_update_mask_{w_idx}").value != 0
            valid = dut.io_s1_ready.value and update_mask
            taken = getattr(dut, f"Tage_SC_tables_{t_i}_io_update_takens_{w_idx}").value
            if valid and silent and (taken == up_or_down):
                return True
        return False

    return update_tn_saturing


def is_allocate_new_entry(way: int, except_success_or_failure: int):
    """
    #WARNING: 目前的判断逻辑还是按照Chisel代码进行的, 所以可用表项信息失效的bug依旧存在.
    """
    need_to_allocates = ["Tage_SC_needToAllocate", "Tage_SC_needToAllocate_1"]

    def allocate_new_entry(dut: DUTTage_SC) -> bool:
        valid = getattr(dut, f"Tage_SC_updateValids_{way}").value and dut.io_update_valid.value
        need_to_allocate = getattr(dut, need_to_allocates[way]).value
        with MetaParser(dut.io_update_bits_meta.value) as meta_parser:
            allocatable_count = sum([x.value for x in meta_parser.allocates])
            return dut.io_s1_ready.value and valid and need_to_allocate \
                and ((allocatable_count > 0) if except_success_or_failure else (allocatable_count == 0))

    return allocate_new_entry


def is_allocate_as_provider_predict_incorrectly(way: int):
    def allocate_as_provider(dut: DUTTage_SC) -> bool:
        with MetaParser(dut.io_update_bits_meta.value) as meta_parser:
            incorrect = getattr(dut, "Tage_SC_updateProviderCorrect" + ("_1" if way else "")).value == 0
            valid = dut.io_s1_ready.value and dut.io_update_valid.value and meta_parser.providers_valid[
                way].value and incorrect
            return valid

    return allocate_as_provider


def is_update_predict_from_tagged(way: int):
    def update_predict_from_tagged(dut: DUTTage_SC) -> bool:
        with MetaParser(dut.io_update_bits_meta.value) as meta_parser:
            valid = getattr(dut, f"Tage_SC_updateValids_{way}").value and dut.io_update_valid.value
            provided = meta_parser.providers_valid[way].value
            alt_used = meta_parser.altUsed[way].value
            return valid and provided and not alt_used

    return update_predict_from_tagged


def is_update_use_alt_on_na_ctrs(way: int):
    def update_use_alt_on_na_ctrs(dut: DUTTage_SC) -> bool:
        with MetaParser(dut.io_update_bits_meta.value) as meta_parser:
            valid = getattr(dut, f"Tage_SC_updateValids_{way}").value and dut.io_s1_ready.value
            provided = meta_parser.providers_valid[way].value
            weak = meta_parser.providerResps_ctr[way].value in {0b100, 0b011}
            alt_diff = (meta_parser.basecnts[way].value >= 0b10) != (meta_parser.providerResps_ctr[way].value >= 0b100)
            return valid and provided and weak and alt_diff

    return update_use_alt_on_na_ctrs


def is_reset_us(way: int):
    def reset_us(dut: DUTTage_SC) -> bool:
        valid = dut.io_s1_ready.value != 0
        bank_tick_ctr = getattr(dut, f"Tage_SC_bankTickCtrs_{way}").value
        reset_u = getattr(dut, f"Tage_SC_updateResetU_{way}").value != 0
        return valid and reset_u and bank_tick_ctr == 0x7f

    return reset_us


def is_update_always_taken(way: int):
    def update_always_taken(dut: DUTTage_SC) -> bool:
        always_taken = getattr(dut, f"io_update_bits_ftb_entry_always_taken_{way}").value != 0
        return dut.io_s1_ready.value != 0 and dut.io_update_valid.value != 0 and always_taken

    return update_always_taken


def get_coverage_group_of_tage_train(dut: DUTTage_SC) -> CovGroup:
    g = CovGroup(UT_FCOV("../UT_Tage_SC"))

    # T0 up/down saturing update
    for up_or_down in range(2):
        s = "up saturing" if up_or_down else "down saturing"
        g.add_watch_point(
            dut,
            {slot_name[w]: is_update_t0_saturing_ctr(w, up_or_down) for w in range(2)},
            name=" ".join(["T0", s.capitalize()])
        )
    # Tn up/down saturing update
    for up_or_down in range(2):
        s = "up saturing" if up_or_down else "down saturing"
        g.add_watch_point(
            dut,
            {"_".join([f"T{i}", slot_name[w]]): is_update_tn_saturing_ctr(w, i, up_or_down) for i in range(4) for w in
             range(2)},
            name=" ".join(["Tn", s.capitalize()])
        )

    for success_or_failure in range(2):
        # Tn allocate new entry successfully/unsuccessfully
        alloc = {}
        alloc_as_provider_mis_pred = {}
        # Tn allocate new entry successfully/unsuccessfully as incorrect provider
        cond = "Success" if success_or_failure else "Failure"
        for w in range(2):
            bin_name = ["allocate", slot_name[w], ("success" if success_or_failure else "failure")]
            alloc[slot_name[w]] = is_allocate_new_entry(w, success_or_failure)

            alloc_as_provider_mis_pred[f"{slot_name[w]} provider incorrect"] \
                = is_allocate_as_provider_predict_incorrectly(w)

        g.add_watch_point(dut, alloc, name="Tn Allocate " + cond)
        g.add_watch_point(dut, alloc_as_provider_mis_pred, name="Tn Allocate As Provider MisPredict " + cond)

    # Reset useful counter
    g.add_watch_point(dut, {slot_name[w]: is_reset_us(w) for w in range(2)}, name="Reset us")

    # Train Information's `always_taken` Bit is True
    g.add_watch_point(dut, {slot_name[w]: is_update_always_taken(w) for w in range(2)}, name="Always Taken is True")

    g.add_watch_point(
        dut,
        {
            slot_name[0]: lambda d: d.Tage_SC_updateValids_0.value and d.io_s0_fire_1.value,
            slot_name[1]: lambda d: d.Tage_SC_updateValids_1.value and d.io_s0_fire_1.value,
        },
        name="Update When Predict"
    )

    # useAltOnNaCtrs update
    g.add_watch_point(
        dut,
        {"_".join([slot_name[w], "useAltOnNaCtrs", "update"]): is_update_use_alt_on_na_ctrs(w) for w in range(2)},
        name="Update useAltOnNaCtrs"
    )

    return g
