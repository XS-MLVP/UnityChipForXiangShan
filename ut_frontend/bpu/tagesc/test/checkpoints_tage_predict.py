__all__ = ["get_coverage_group_of_tage_predict"]

from toffee.funcov import CovGroup

from comm import UT_FCOV
from ..env.tage_sc_env import TageSCEnv


def is_ti_provider(way: int, ti: int):
    def ti_provider(test_env: TageSCEnv) -> bool:
        s2_internal = test_env.internal_monitor.s2
        return test_env.ctrl_bundle.s2_valid_fire(1) and s2_internal.provided(way) and s2_internal.provider(way) == ti

    return ti_provider


def is_hit_no_table(way: int):
    def hit_no_table(test_env: TageSCEnv) -> bool:
        s2_internal = test_env.internal_monitor.s2
        return test_env.ctrl_bundle.s2_valid_fire(1) and (not s2_internal.provided(way))

    return hit_no_table


def is_all_slots_the_same_provider(test_env: TageSCEnv) -> bool:
    valid = all(test_env.internal_monitor.s2.provided(w) for w in range(2))
    provider = test_env.internal_monitor.s2.provider
    return test_env.ctrl_bundle.s2_valid_fire(1) and valid and provider(0) == provider(1)


def is_hit_multiple_tables(way: int):
    def hit_multiple_tables(test_env: TageSCEnv) -> bool:
        provided = test_env.internal_monitor.s2.provided(way)
        count = test_env.internal_monitor.tage_table.hit_count(way)
        return test_env.ctrl_bundle.s2_valid_fire(1) and provided and count > 1

    return hit_multiple_tables


def is_ti_unconf_provider(way: int, t_i: int, use_alt: int):
    def ti_unconf_provider(test_env: TageSCEnv) -> bool:
        provided = test_env.internal_monitor.s2.provided(way)
        provider = test_env.internal_monitor.s2.provider(way)
        unconfident = test_env.internal_monitor.s2.provider_weak(way)
        alt_used = test_env.internal_monitor.s2.alt_used(way)
        return test_env.ctrl_bundle.s2_valid_fire(
            1) and provided and provider == t_i and unconfident and alt_used == use_alt

    return ti_unconf_provider


def is_provider_unconf_and_multiple_hit(way: int, use_alt: int):
    def provider_unconf_and_multiple_hit(test_env: TageSCEnv) -> bool:
        provided = test_env.internal_monitor.s2.provided(way)
        unconfident = test_env.internal_monitor.s2.provider_weak(way)
        alt_used = test_env.internal_monitor.s2.alt_used(way)
        count = test_env.internal_monitor.tage_table.hit_count(way)
        return test_env.ctrl_bundle.s2_valid_fire(1) and provided and count > 1 and unconfident and alt_used == use_alt

    return provider_unconf_and_multiple_hit


def is_all_slots_use_same_unconf_provider_and_both(use_alt: int):
    def all_slots_use_same_unconf_provider(test_env: TageSCEnv) -> bool:
        s2 = test_env.internal_monitor.s2
        provider = s2.provider
        valid = all([s2.provided(w) and s2.alt_used(w) == use_alt for w in range(2)])
        return test_env.ctrl_bundle.s2_valid_fire(1) and valid and (provider(0) == provider(1))

    return all_slots_use_same_unconf_provider


def get_coverage_group_of_tage_predict(test_env: TageSCEnv) -> CovGroup:
    slot_name = ["br_slot_0", "tail_slot"]

    group = CovGroup(UT_FCOV("../UT_Tage_SC"))

    # Tn is provider
    group.add_watch_point(test_env, {
        "_".join([f"T{i}", "provider", slot_name[w]]): is_ti_provider(w, i) for i in range(4) for w in range(2)
    }, name="Tn is Provider")

    # Miss all tables
    group.add_watch_point(test_env, {
        "_".join([slot_name[w], "miss"]): is_hit_no_table(w) for w in range(2)
    }, name="All Tn Miss")

    # Multi tables hit
    group.add_watch_point(test_env, {
        slot_name[w]: is_hit_multiple_tables(w) for w in range(2)
    }, name="Multi Tables Hit")

    # All slots are the same provider
    group.add_watch_point(
        test_env, {"same_provider": is_all_slots_the_same_provider},
        name="All Slots use the Same Provider"
    )
    # Tn is unconfident provider and use/doesn't use alt
    alt_use_str = ["NOT use_alt", "use_alt"]
    for use_alt in range(2):
        group.add_watch_point(
            test_env,
            {f"t{i}_{slot_name[w]}": is_ti_unconf_provider(w, i, use_alt) for i in range(4) for w in range(2)},
            name=" ".join(["Tn is Unconfident Provider and ", alt_use_str[use_alt]]),
        )
    # Multi tables hit and provider is unconfident, and use/doesn't use alt.
    for use_alt in range(2):
        point_name = f"Multiple Tables Hit&Provider is Unconf and {alt_use_str[use_alt]}"
        group.add_watch_point(
            test_env,
            {slot_name[w]: is_provider_unconf_and_multiple_hit(w, use_alt) for w in range(2)},
            name=point_name
        )

    # All slots use the same unconfident provider and use/doesn't use alt
    for use_alt in range(2):
        point_name = f"All Slots Use the Same Unconfident Provider and {alt_use_str[use_alt]}"
        group.add_watch_point(
            test_env,
            {"valid": is_all_slots_use_same_unconf_provider_and_both(use_alt)},
            name=point_name
        )

    return group
