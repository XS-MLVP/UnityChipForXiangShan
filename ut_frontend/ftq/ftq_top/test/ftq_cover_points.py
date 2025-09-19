import toffee.funcov as fc
from toffee.funcov import CovGroup
from .test_configs import C_EMPTY, C_FLUSHED, C_COMMITTED



def toifu_cov_points(g, dut, bundle):
    g.add_cover_point(bundle.toICache.req_valid, {"toicache_req_valid is 0": fc.Eq(0)}, name="ToICache req_valid is 0", once=True)
    g.add_cover_point(bundle.toICache.req_valid, {"toicache_req_valid is 1": fc.Eq(1)}, name="ToICache req_valid is 1", once=True)
    for i in range(5):
        signal = getattr(bundle.toICache, f"req_bits_readValid_{i}")
        g.add_cover_point(signal, {"toicache_readValid[{i}] is 0": fc.Eq(0)}, name=f"ToICache readValid[{i}] is 0", once=True)
        g.add_cover_point(signal, {"toicache_readValid[{i}] is 1": fc.Eq(1)}, name=f"ToICache readValid[{i}] is 1", once=True)
    for i in range(5):
        signal = getattr(bundle.toICache, f"req_bits_pcMemRead_{i}_startAddr")
        g.add_cover_point(signal, {"toicache_startAddr[{i}] non-zero": fc.Ne(0)}, name=f"ToICache startAddr[{i}] non-zero", once=True)
    for i in range(5):
        signal = getattr(bundle.toICache, f"req_bits_pcMemRead_{i}_nextlineStart")
        g.add_cover_point(signal, {"toicache_nextlineStart[{i}] non-zero": fc.Ne(0)}, name=f"ToICache nextlineStart[{i}] non-zero", once=True)
    s3_signals = [
        (bundle.toPrefetch.flushFromBpu_s3_valid, "toprefetch_s3_valid", [fc.Eq(0), fc.Eq(1)]),
        (bundle.toPrefetch.flushFromBpu_s3_bits_flag, "toprefetch_s3_flag", [fc.Eq(0), fc.Eq(1)]),
        (bundle.toPrefetch.flushFromBpu_s3_bits_value, "toprefetch_s3_value", [fc.Eq(0), fc.Ne(0)])
    ]
    for signal, prefix, bins_list in s3_signals:
        for bin_cond in bins_list:
            bin_suffix = "non-zero" if isinstance(bin_cond, fc.CovNe) else f"is {bin_cond.value}"
            g.add_cover_point(signal, {f"{prefix} {bin_suffix}": bin_cond}, name=f"{prefix.capitalize()} {bin_suffix}", once=True)

def wb_from_ifu_cov_points(g, dut, bundle):
    g.add_cover_point(dut.has_false_hit.value, {"has_false_hit is 1": fc.Eq(1)}, name="Has false hit is 1", once=True)

def redirect_from_backend_cov_points(g, dut, bundle):
    prefix = "toBpu_redirect_bits_cfiUpdate_"
    zero_bin = {"{signal} is 0": fc.Eq(0)}
    one_bin = {"{signal} is 1": fc.Eq(1)}
    signals = ["br_hit", "jr_hit", "shift", "addIntoHist"]
    for signal_name in signals:
        signal = getattr(dut, f"{prefix}{signal_name}")
        g.add_cover_point(signal, zero_bin, name=f"ToBPU redirect {signal_name} is 0", once=True)
        g.add_cover_point(signal, one_bin, name=f"ToBPU redirect {signal_name} is 1", once=True)

def redirect_from_ifu_cov_points(g, dut, bundle):
    prefix = "ifu_redirect_"
    non_zero_bin = {"{name} non-zero": fc.Ne(0)}
    eq_one_bin = {"{name} is 1": fc.Eq(1)}
    range_bin = {"{name} low": fc.IsInRange(0, 63)}
    prefixed_signals = [
        ("pc", non_zero_bin, "pc non-zero"),
        ("pd_valid", eq_one_bin, "pd valid is 1"),
        ("target", non_zero_bin, "target non-zero"),
        ("taken", eq_one_bin, "taken is 1"),
        ("ftq_idx", range_bin, "ftq idx low (0-31)"),
        ("ftq_offset", non_zero_bin, "ftq offset non-zero")
    ]

    for attr, bin_template, name_suffix in prefixed_signals:
        signal = getattr(dut, f"{prefix}{attr}")
        full_name = f"IFU redirect {name_suffix}"
        g.add_cover_point(signal.value, bin_template, name=full_name, once=True)
    g.add_cover_point(dut.ifu_flush.value, {"ifu_flush is 1": fc.Eq(1)}, name="IFU flush is 1", once=True)

def tobackend_cov_points(g, dut, bundle):
    prefix = "tobackend_"
    eq_one_bin = {"{name} is 1": fc.Eq(1)}
    range_bin = {"{name} high": fc.IsInRange(0, 63)}
    non_zero_bin = {"{name} non-zero": fc.Ne(0)}
    signals = [
        ("pc_mem_wen", eq_one_bin, "pc mem wen is 1"),
        ("pc_mem_waddr", range_bin, "pc mem waddr high (32-63)"),
        ("pc_mem_wdata_start", non_zero_bin, "pc mem wdata start non-zero"),
        ("newest_entry_ptr", non_zero_bin, "newest entry ptr non-zero"),
        ("newest_target", non_zero_bin, "newest target non-zero")
    ]
    for attr, bin_template, name_suffix in signals:
        signal = getattr(dut, f"{prefix}{attr}")
        full_name = f"ToBackend {name_suffix}"
        g.add_cover_point(signal.value, bin_template, name=full_name, once=True)

def flush_and_queue_cov_points(g, dut, bundle):
    range_bin = {"{name}": fc.IsInRange(0, 63)}
    ptr_signals = [
        (dut.bpu_ptr, "BPU ptr"),
        (dut.ifu_ptr_write, "IFU ptr write"),
        (dut.ifu_wb_ptr_write, "IFU wb ptr write"),
        (dut.ifu_ptr_plus1_write, "IFU ptr plus1 write"),
        (dut.ifu_ptr_plus2_write, "IFU ptr plus2 write"),
        (dut.pf_ptr_write, "PF ptr write"),
        (dut.pf_ptr_plus1_write, "PF ptr plus1 write high (32-63)")
    ]
    for signal, name_prefix in ptr_signals:
        g.add_cover_point(signal.value, range_bin, name=name_prefix, once=True)
    is_one_signals = [
        (dut.topdown_redirect_debugIsCtrl, "Topdown debugIsCtrl is 1"),
        (dut.topdown_redirect_debugIsMemVio, "Topdown debugIsMemVio is 1"),
        (dut.toifu_redirect_level, "ToIFU redirect level is 1")
    ]
    for signal, name in is_one_signals:
        g.add_cover_point(signal.value, {"{name} is 1": fc.Eq(1)}, name=name, once=True)
    g.add_cover_point(dut.toifu_redirect_ftqIdx_value.value, {"toifu_redirect_ftqIdx_value": fc.IsInRange(0, 63)}, name="ToIFU redirect ftqIdx value high (32-63)", once=True)
    g.add_cover_point(dut.toifu_redirect_ftqOffset.value, {"toifu_redirect_ftqOffset non-zero": fc.Ne(0)}, name="ToIFU redirect ftqOffset non-zero", once=True)

def wb_from_exu_cov_points(g, dut, bundle):
    non_zero_bin = {"{name} non-zero": fc.Ne(0)}
    eq_zero_bin = {"{name} is 0": fc.Eq(0)}
    eq_one_bin = {"{name} is 1": fc.Eq(1)}
    range_bin = {"{name} high": fc.IsInRange(0, 63)}
    range_bin_small = {"{name} high": fc.IsInRange(0, 7)}
    signals = [
        (dut.get_update_target(0), non_zero_bin, "update_target[0] non-zero"),
        (dut.newest_entry_target, eq_zero_bin, "Newest entry target is 0"),
        (dut.newest_entry_target, non_zero_bin, "Newest entry target non-zero"),
        (dut.newest_entry_ptr_value, range_bin, "Newest entry ptr high (32-63)"),
        (dut.newest_entry_target_modified, eq_zero_bin, "Newest entry target modified is 0"),
        (dut.newest_entry_target_modified, eq_one_bin, "Newest entry target modified is 1"),
        (dut.get_mispredict_vec(0, 0), eq_zero_bin, "Mispredict vec[0][0] is 0"),
        (dut.get_mispredict_vec(0, 0), eq_one_bin, "Mispredict vec[0][0] is 1"),
        (dut.get_cfi_index_valid(0), eq_one_bin, "Cfi index valid[0] is 1"),
        (dut.get_cfi_index_bits(0), range_bin_small, "Cfi index bits[0] high (4-7)")
    ]
    for signal, bin_template, name_suffix in signals:
        full_name = name_suffix
        g.add_cover_point(signal, bin_template, name=full_name, once=True)

def ftq_cover_points(dut, bundle):
    g = CovGroup("FTQ redirect and management function")
    toifu_cov_points(g, dut, bundle)
    wb_from_ifu_cov_points(g, dut, bundle)
    redirect_from_backend_cov_points(g, dut, bundle)
    redirect_from_ifu_cov_points(g, dut, bundle)
    tobackend_cov_points(g, dut, bundle)
    wb_from_exu_cov_points(g, dut, bundle)
    flush_and_queue_cov_points(g, dut, bundle)
    return g
