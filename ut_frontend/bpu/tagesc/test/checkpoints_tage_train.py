__all__ = ["get_coverage_group_of_tage_train"]

from toffee.funcov import CovGroup

from comm import UT_FCOV
from ..env.tage_sc_env import TageSCEnv
from ..util.meta_parser import GetMetaParser

slot_name = ["br_slot_0", "tail_slot"]


def get_idx(pc: int, way: int):
    return ((pc >> 1) & 1) ^ (way & 1)


def is_update_t0_saturing_ctr(way: int, up_or_down: int):
    def update_t0_saturing(test_env: TageSCEnv) -> bool:
        v = 0b11 if up_or_down else 0
        pc = test_env.update_driver.bits.pc.value
        base_table = test_env.internal_monitor.base_table
        valid = test_env.ctrl_bundle.s1_ready.value and base_table.write_valid() \
                and base_table.write_mask(pc, way)
        old_ctr = base_table.old_ctr(way)
        new_ctr = base_table.new_ctr(way)
        update_taken = base_table.update_taken(pc, way)
        return valid and new_ctr == v and old_ctr == v and (update_taken == up_or_down)

    return update_t0_saturing


def is_update_tn_saturing_ctr(way: int, ti: int, up_or_down: int):
    def update_tn_saturing(test_env: TageSCEnv) -> bool:
        pc = test_env.update_driver.bits.pc.value
        tage_table = test_env.internal_monitor.tage_table
        has_silent = tage_table.has_silent(ti, way)
        mask = tage_table.get_table(ti).update_mask(pc, way)
        valid = test_env.ctrl_bundle.s1_ready.value and mask
        taken = tage_table.get_table(ti).update_taken(pc, way)
        return valid and has_silent and (taken == up_or_down)

    return update_tn_saturing


def is_allocate_new_entry(way: int, except_success_or_failure: int):
    def allocate_new_entry(test_env: TageSCEnv) -> bool:
        valid = test_env.internal_monitor.update.valid(way) and test_env.ctrl_bundle.s1_ready.value
        need_to_allocate = test_env.internal_monitor.need_to_allocate(way)
        with GetMetaParser(test_env.update_driver.bits.meta.value) as meta_parser:
            allocatable_count = sum([x.value for x in meta_parser.allocates])
            return valid and need_to_allocate \
                and ((allocatable_count > 0) if except_success_or_failure else (allocatable_count == 0))

    return allocate_new_entry


def is_allocate_as_provider_predict_incorrectly(way: int, success: int):
    def allocate_as_provider(test_env: TageSCEnv) -> bool:
        with GetMetaParser(test_env.update_driver.bits.meta.value) as meta_parser:
            expect = test_env.internal_monitor.update.provider_correct(way) == success
            valid = test_env.ctrl_bundle.s1_ready.value and test_env.update_driver.valid.value \
                    and meta_parser.providers_valid[way].value and expect
            return valid

    return allocate_as_provider


def is_update_predict_from_tagged(way: int):
    def update_predict_from_tagged(test_env: TageSCEnv) -> bool:
        with GetMetaParser(test_env.update_driver.bits.meta.value) as meta_parser:
            valid = test_env.internal_monitor.update.valid(way)
            provided = meta_parser.providers_valid[way].value
            alt_used = meta_parser.altUsed[way].value
            return valid and provided and not alt_used

    return update_predict_from_tagged


def is_update_use_alt_on_na_ctrs(way: int):
    def update_use_alt_on_na_ctrs(test_env: TageSCEnv) -> bool:
        with GetMetaParser(test_env.update_driver.bits.meta.value) as meta_parser:
            valid = test_env.internal_monitor.update.valid(way)
            provided = meta_parser.providers_valid[way].value
            weak = meta_parser.providerResps_ctr[way].value in {0b100, 0b011}
            alt_diff = (meta_parser.basecnts[way].value >= 0b10) != (meta_parser.providerResps_ctr[way].value >= 0b100)
            return valid and provided and weak and alt_diff

    return update_use_alt_on_na_ctrs


def is_reset_us(way: int):
    def reset_us(test_env: TageSCEnv) -> bool:
        valid = test_env.ctrl_bundle.s1_ready.value
        bank_tick_ctr = test_env.internal_monitor.bank_tick_ctr(way)
        reset_u = test_env.internal_monitor.update.reset_u(way)
        return valid and reset_u and bank_tick_ctr == 0x7f

    return reset_us


def is_update_strong_bias(way: int):
    def update_strong_bias(test_env: TageSCEnv) -> bool:
        strong_bias = test_env.update_driver.bits.ftb_entry.get_strong_bias(way)
        valid = test_env.ctrl_bundle.s1_ready.value and test_env.update_driver.valid.value
        return valid and strong_bias

    return update_strong_bias


def get_coverage_group_of_tage_train(test_env: TageSCEnv) -> CovGroup:
    g = CovGroup(UT_FCOV("../UT_Tage_SC"))

    # T0 up/down saturing update
    for up_or_down in range(2):
        s = "up saturing" if up_or_down else "down saturing"
        g.add_watch_point(
            test_env,
            {slot_name[w]: is_update_t0_saturing_ctr(w, up_or_down) for w in range(2)},
            name=" ".join(["T0", s.capitalize()])
        )
    # Tn up/down saturing update
    for up_or_down in range(2):
        s = "up saturing" if up_or_down else "down saturing"
        g.add_watch_point(
            test_env,
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
                = is_allocate_as_provider_predict_incorrectly(w, success_or_failure)

        g.add_watch_point(test_env, alloc, name="Tn Allocate " + cond)
        g.add_watch_point(test_env, alloc_as_provider_mis_pred, name="Tn Allocate As Provider MisPredict " + cond)

    # Reset useful counter
    g.add_watch_point(test_env, {slot_name[w]: is_reset_us(w) for w in range(2)}, name="Reset us")

    # Train Information's `always_taken` Bit is True
    g.add_watch_point(test_env, {slot_name[w]: is_update_strong_bias(w) for w in range(2)},
                      name="Strong Bias is True")
    g.add_watch_point(
        test_env,
        {
            slot_name[0]: lambda status: test_env.internal_monitor.update.valid(
                0) and test_env.ctrl_bundle.s1_fire_1.value,
            slot_name[1]: lambda status: test_env.internal_monitor.update.valid(
                1) and test_env.ctrl_bundle.s1_fire_1.value,
        },
        name="Update When Predict"
    )

    # useAltOnNaCtrs update
    g.add_watch_point(
        test_env,
        {"_".join([slot_name[w], "useAltOnNaCtrs", "update"]): is_update_use_alt_on_na_ctrs(w) for w in range(2)},
        name="Update useAltOnNaCtrs"
    )

    return g
