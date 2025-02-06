"""
    Define all the coverage group calculation here
    Author: yzcc
"""
from comm import UT_FCOV
from .chk_pred import *
from .chk_train import *
from ..env.ittage_wrapper import ITTageWrapper


def get_cov_grp_of_alt_pred(dut: DUTITTage) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))

    bins = {}
    for i in range(4):
        bins[f"alt_use_table_{i}"] = is_alt_from_table_i(i)

    grp.add_watch_point(dut, bins, name="ITTAGE Alt Pred altProvider from Tn")
    return grp


def get_cov_grp_of_longest_and_alt_train(dut: ITTageWrapper) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))

    bins_as_provider = {}
    bins_as_alt = {}
    for i in range(5):
        # 第i个表被作为主预测更新
        bins_as_provider["_".join([f"table{i + 1}", "update", "as", "provider"])] = is_update_table_as_provider(i)

        # 第i个表被作为替代预测更新
        if i != 4:
            bins_as_alt["_".join([f"table{i + 1}", "update", "as", "alt"])] = is_update_table_as_alt(i)

    grp.add_watch_point(dut, bins_as_provider, name="ITTAGE Longest and Alt Train Update as Provider")
    grp.add_watch_point(dut, bins_as_alt, name="ITTAGE Longest and Alt Train Update as Alt Provider")
    return grp


def get_cov_grp_of_main_pred(dut: DUTITTage) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))

    bins = {}
    for i in range(5):
        bins[f"T{i}_hit"] = is_hit_table_i(i)

    grp.add_watch_point(dut, bins, name="ITTAGE Main Pred Hit Tn")
    return grp


def get_cov_grp_of_other_pred(dut: DUTITTage) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))
    # 是否命中多个表
    grp.add_watch_point(dut, {"hit_multi": is_hit_multi_table()}, name="ITTAGE Other Pred Hit Multi Table")

    # 是否一个表都没命中
    grp.add_watch_point(dut, {"hit_no": is_hit_no_table()}, name="ITTAGE Other Pred Hit No Table")

    # Res src
    # 替代预测来自ftb
    bins_src = {}
    bins_src["src_from_main"] = is_src_from_main()
    bins_src["src_from_alt"] = is_src_from_alt()
    bins_src["src_from_ftb"] = is_src_from_ftb()
    grp.add_watch_point(dut, bins_src, name="ITTAGE Other Pred Result Source")

    return grp


def get_cov_grp_of_other_train(dut: DUTITTage) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))

    # tickCtr -> reset
    grp.add_watch_point(dut, {"reset_us": is_reset_us}, name="ITTAGE Other Train Reset Useful Bit")

    # 更新最长表的时候，更新/不更新替代预测
    bins_update = {}
    for update_alt in range(2):
        s = ["update", "provider", "and", "alt"] if update_alt else ["only", "update", "provider"]
        bins_update["_".join(s)] = is_update_table_as_provider(update_alt)
    grp.add_watch_point(dut, bins_update, name="ITTAGE Other Train Update Entry")

    # 申请新表项成功/失败
    bins_alloc = {}
    for success in range(2):
        s = "succeed" if success else "fail"
        bins_alloc["allocate_" + s] = is_allocate_succeed_or_fail(success)
    grp.add_watch_point(dut, bins_alloc, name="ITTAGE Other Train Allocate Entry")

    return grp


def get_cov_grp_of_train_saturation(dut: DUTITTage) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))

    for up_or_down in range(2):
        saturating_status = "up" if up_or_down else "down"
        bins = {}
        for i in range(5):
            bins[f"T{i}_{saturating_status}_saturate"] = is_table_ctr_saturing(i, up_or_down)
        grp.add_watch_point(dut, bins, name=f"ITTAGE Saturation Train {saturating_status} saturing")

    return grp


def get_cov_grp_of_us_train(dut: DUTITTage) -> CovGroup:
    grp = CovGroup(UT_FCOV("../UT_ITTage"))

    bins_set = {}
    bins_clr = {}
    for i in range(5):
        bins_set[f"T{i} us set"] = is_us_set_or_clear(1, i)
        bins_clr[f"T{i} us clear"] = is_us_set_or_clear(0, i)
    grp.add_watch_point(dut, bins_set, name="ITTAGE Us Train Tn us set")
    grp.add_watch_point(dut, bins_clr, name="ITTAGE Us Train Tn us clear")
    return grp