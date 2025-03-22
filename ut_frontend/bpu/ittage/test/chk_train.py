"""
    Checkpoint for train
"""

from toffee import CovGroup
from ..util.meta_parser import MetaParser

from dut.ITTage import DUTITTage


def is_table_ctr_saturing(i: int, up_or_down: int):
    sat_value = 0b11 if up_or_down else 0

    def table_ctr_saturing(dut: DUTITTage):
        alloc = getattr(dut, f"ITTage_tables_{i}_io_update_alloc").value
        correct = getattr(dut, f"ITTage_tables_{i}_io_update_correct").value
        valid = getattr(dut, f"ITTage_tables_{i}_io_update_valid").value and not alloc and up_or_down == correct
        old_ctr = getattr(dut, f"ITTage_tables_{i}_io_update_oldCtr").value
        new_ctr = getattr(dut, f"ITTage_tables_{i}_update_wdata_ctr").value
        return valid and old_ctr == sat_value and new_ctr == sat_value

    return table_ctr_saturing


def is_update_provider(update_alt: int):
    def update_provider(dut: DUTITTage):
        valid = dut.io_update_valid.value and dut.ITTage_updateValid_probe.value
        provided = dut.ITTage_s3_provided.value
        alt_provided = dut.ITTage_s3_altProvided.value
        if valid and provided:
            return update_alt == alt_provided
        return False

    return update_provider


def is_update_table_as_provider(i: int):
    def update_table_as_provider(dut: DUTITTage):
        valid = dut.io_update_valid.value and dut.ITTage_updateValid_probe.value
        provided = dut.ITTage_s3_provided.value
        provider = dut.ITTage_s3_provider.value
        return valid and provided and (provider == i)

    return update_table_as_provider


def is_update_table_as_alt(i: int):
    def update_table_as_alt(dut: DUTITTage):
        valid = dut.io_update_valid.value and dut.ITTage_updateValid_probe.value
        alt_provided = dut.ITTage_s3_altProvided.value
        alt_provider = dut.ITTage_s3_altProvider.value
        return valid and alt_provided and (alt_provider == i)

    return update_table_as_alt


def is_reset_us(dut: DUTITTage):
    valid = dut.io_update_valid.value
    tick_ctr = dut.ITTage_tickCtr.value
    reset = sum([getattr(dut, f"ITTage_tables_{i}_io_update_reset_u").value for i in range(5)])
    assert reset in {0, 5}, "Number of reset tables must be 5"
    if valid and (reset == 5):
        # assert tick_ctr == 0xff
        return True
    return False


def is_allocate_succeed_or_fail(success_or_fail: int):
    def allocate_succeed_or_fail(dut: DUTITTage):
        valid = dut.io_update_valid.value and dut.ITTage_updateValid_probe.value
        allocate_valid = MetaParser(dut.io_update_bits_meta.value).allocate_valid
        return valid and (allocate_valid == success_or_fail)

    return allocate_succeed_or_fail


def is_us_set_or_clear(set_or_clear: int, i: int):
    def us_set_or_clear(dut: DUTITTage):
        meta_wrap = MetaParser(dut.io_update_bits_meta.value)

        altDiffer = meta_wrap.altDiffers
        providerU = meta_wrap.providerU
        provider = meta_wrap.provider
        misPred = dut.io_update_bits_mispred_mask_2.value

        set_value = (not misPred) if altDiffer else providerU

        valid = dut.io_update_valid.value and meta_wrap.provided

        return valid and set_value == set_or_clear and provider == i

    return us_set_or_clear


def is_set_us_correct(dut: DUTITTage):
    meta_parser = MetaParser(dut.io_update_bits_meta.value)
    provided = meta_parser.provided
    provider = meta_parser.provider
    provider_ctr = meta_parser.providerCtr
    provider_target = meta_parser.providerTarget
    use_provider = provided and provider_ctr != 0
    real_target = dut.io_update_bits_full_target.value
    provider_correct = provider_target == real_target

    valid = dut.io_update_valid.value and dut.ITTage_updateValid_probe.value
    set_us_true = (getattr(dut, f"ITTage_tables_{provider}_io_update_uValid").value and
                   getattr(dut, f"ITTage_tables_{provider}_io_update_u").value)

    if valid and set_us_true:
        # 香山ITTAGE对于us置1的基本逻辑是，只要
        return use_provider and provider_correct
    return False


def _get_cov_grp_of_pred(dut: DUTITTage) -> CovGroup:
    grp = CovGroup("ITTAGE Train")

    # 第i个表计数器达到上/下饱和
    for i in range(5):
        for up_or_down in range(2):
            saturing_status = "up" if up_or_down else "down"
            grp.add_watch_point(
                dut,
                {"_".join([f"table{i + 1}", saturing_status, "saturing"]): is_table_ctr_saturing(i, up_or_down)},
                name=" ".join([f"Table{i + 1}", "is", saturing_status.capitalize(), "Saturing"]),
            )

    for i in range(5):
        # 第i个表被作为主预测更新
        grp.add_watch_point(
            dut,
            {"_".join([f"table{i + 1}", "update", "as", "provider"]): is_update_table_as_provider(i)},
            name=" ".join([f"Table{i + 1}", "Update", "as", "Provider"]),
        )
        # 第i个表被作为替代预测更新
        grp.add_watch_point(
            dut,
            {"_".join([f"table{i + 1}", "update", "as", "alt"]): is_update_table_as_alt(i)},
            name=" ".join([f"Table{i + 1}", "Update", "as", "Alt"]),
        )

    # 更新最长表的时候，更新/不更新替代预测
    for update_alt in range(2):
        s = ["update", "provider", "and", "alt"] if update_alt else ["only", "update", "provider"]
        grp.add_watch_point(
            dut,
            {"_".join(s): is_update_table_as_provider(update_alt)},
            name=" ".join([x.capitalize() for x in s])
        )

    # tickCtr达到最大值，触发重置useful位
    grp.add_watch_point(dut, {"reset_us": is_reset_us}, name="Reset Useful Bit")

    # 申请新表项成功/失败
    for success in range(2):
        s = "succeed" if success else "fail"
        grp.add_watch_point(
            dut,
            {"allocate_" + s: is_allocate_succeed_or_fail(success)},
            name="Allocate " + s.capitalize()
        )
    # 在正确的条件下us被置为1
    grp.add_watch_point(dut, {"us_set_1": is_set_us_correct}, name="Provider us bit Set 1")

    return grp