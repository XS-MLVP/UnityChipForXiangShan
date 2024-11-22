from toffee.funcov import CovGroup

from comm import UT_FCOV
from dut.Tage_SC import DUTTage_SC

__all__ = ["get_coverage_group_of_tage_predict"]


def is_ti_provider(way: int, ti: int):
    def ti_provider(dut: DUTTage_SC) -> bool:
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value
        provider = getattr(dut, f"Tage_SC_s2_providers_{way}").value
        return dut.io_s1_ready.value and dut.io_s2_fire_1.value and provided and provider == ti

    return ti_provider


def is_hit_no_table(way: int):
    def hit_no_table(dut: DUTTage_SC) -> bool:
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value
        return dut.io_s1_ready.value != 0 and dut.io_s2_fire_1.value != 0 and provided == 0

    return hit_no_table


def is_all_slots_the_same_provider(dut: DUTTage_SC) -> bool:
    provided_0 = dut.Tage_SC_s2_provideds_0.value
    provided_1 = dut.Tage_SC_s2_provideds_1.value
    valid = provided_0 and provided_1
    provider_0 = dut.Tage_SC_s2_providers_0.value
    provider_1 = dut.Tage_SC_s2_providers_1.value
    return dut.io_s1_ready.value and dut.io_s2_fire_1.value and valid and provider_0 == provider_1


def is_hit_multiple_tables(way: int):
    def hit_multiple_tables(dut: DUTTage_SC) -> bool:
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value
        count = sum([getattr(dut, f"Tage_SC_tables_{i}_io_resps_{way}_valid").value for i in range(4)])
        return dut.io_s1_ready.value and dut.io_s2_fire_1.value and provided and count > 1

    return hit_multiple_tables


def is_ti_unconf_provider(way: int, t_i: int, use_alt: int):
    def ti_unconf_provider(dut: DUTTage_SC) -> bool:
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value
        provider = getattr(dut, f"Tage_SC_s2_providers_{way}").value
        unconfident = getattr(dut, f"Tage_SC_s2_providerResps_{way}_ctr").value in {0b011, 0b100}
        alt_used = getattr(dut, f"Tage_SC_s2_altUsed_{way}").value
        return (dut.io_s1_ready.value and dut.io_s2_fire_1.value and provided and provider == t_i
                and unconfident and alt_used == use_alt)

    return ti_unconf_provider


def is_provider_unconf_and_multiple_hit(way: int, use_alt: int):
    def provider_unconf_and_multiple_hit(dut: DUTTage_SC) -> bool:
        provided = getattr(dut, f"Tage_SC_s2_provideds_{way}").value
        # provider = getattr(dut, f"Tage_SC_s2_providers_{way}")
        unconfident = getattr(dut, f"Tage_SC_s2_providerResps_{way}_ctr").value in {0b011, 0b100}
        alt_used = getattr(dut, f"Tage_SC_s2_altUsed_{way}").value
        count = sum([getattr(dut, f"Tage_SC_tables_{i}_io_resps_{way}_valid").value for i in range(4)])
        return (dut.io_s1_ready.value and dut.io_s2_fire_1.value and provided and count > 0
                and unconfident and alt_used == use_alt)

    return provider_unconf_and_multiple_hit


def is_all_slots_use_same_unconf_provider_and_both(use_alt: int):
    def all_slots_use_same_unconf_provider(dut: DUTTage_SC) -> bool:
        provided_0 = dut.Tage_SC_s2_provideds_0.value
        provided_1 = dut.Tage_SC_s2_provideds_1.value
        provider_0 = dut.Tage_SC_s2_providers_0.value
        provider_1 = dut.Tage_SC_s2_providers_1.value
        alt_used_0 = dut.Tage_SC_s2_altUsed_0.value
        alt_used_1 = dut.Tage_SC_s2_altUsed_1.value
        valid = provided_0 and provided_1 and alt_used_0 and alt_used_1
        return dut.io_s1_ready.value and dut.io_s2_fire_1.value and valid and (provider_0 == provider_1)

    return all_slots_use_same_unconf_provider


def get_coverage_group_of_tage_predict(dut: DUTTage_SC) -> CovGroup:
    slot_name = ["br_slot_0", "tail_slot"]

    group = CovGroup(UT_FCOV("../UT_Tage_SC"))

    # Tn is provider
    group.add_watch_point(dut, {
        "_".join([f"T{i}", "provider", slot_name[w]]): is_ti_provider(w, i) for i in range(4) for w in range(2)
    }, name="Tn is Provider")

    group.add_watch_point(dut, {
        "_".join([slot_name[w], "miss"]): is_hit_no_table(w) for w in range(2)
    }, name="All Tn Miss")

    # Multi tables hit
    group.add_watch_point(dut, {
        slot_name[w]: is_hit_multiple_tables(w) for w in range(2)
    }, name="Multi Tables Hit")

    # All slots miss all tables
    group.add_watch_point(
        dut, {"no_slot_hits": is_hit_no_table(w) for w in range(2)}, name="No Slot Hits"
    )
    # All slots are the same provider
    group.add_watch_point(
        dut, {"same_provider": is_all_slots_the_same_provider},
        name="All Slots use the Same Provider"
    )
    # Tn is unconfident provider and use/doesn't use alt
    alt_use_str = ["NOT use_alt", "use_alt"]
    for use_alt in range(2):
        group.add_watch_point(
            dut,
            {slot_name[w]: is_ti_unconf_provider(w, i, use_alt) for i in range(4) for w in range(2)},
            name=" ".join(["Tn is Unconfident Provider and ", alt_use_str[use_alt]]),
        )
    # Multi tables hit and provider is unconfident, and use/doesn't use alt.
    for use_alt in range(2):
        point_name = f"Multiple Tables Hit&Provider is Unconf and {alt_use_str[use_alt]}"
        group.add_watch_point(
            dut,
            {slot_name[w]: is_provider_unconf_and_multiple_hit(w, use_alt) for w in range(2)},
            name=point_name
        )

    # All slots use the same unconfident provider and use/doesn't use alt
    for use_alt in range(2):
        point_name = f"All Slots Use the Same Unconfident Provider and {alt_use_str[use_alt]}"
        group.add_watch_point(
            dut,
            {"valid": is_all_slots_use_same_unconf_provider_and_both(use_alt)},
            name=point_name
        )

    return group
