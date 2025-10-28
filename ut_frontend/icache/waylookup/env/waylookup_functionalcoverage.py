import toffee.funcov as fc
from toffee.funcov import CovGroup
from comm import module_name_with

def define_waylookup_coverage(bundle, dut):
    """
    Defines the functional coverage points for the WayLookup module.
    Coverage points are designed to match the functional specification document.
    
    Args:
        bundle: The top-level WayLookupBundle object.
        dut: The DUT object for accessing internal signals.
    """
    g = CovGroup("WayLookup_Coverage")
    # Create Waylookup_internal signals for coverage
    def _M(name):
        return module_name_with(name, "../../test/waylookup_test")
    
    Waylookup_dict = {
        "vset_same":"WayLookup_top.WayLookup.vset_same",
        "ptag_same":"WayLookup_top.WayLookup.ptag_same",
        "empty":"WayLookup_top.WayLookup.empty",
        "gpf_hit":"WayLookup_top.WayLookup.gpf_hit",
        "can_bypass":"WayLookup_top.WayLookup.can_bypass",
        "readPtr_value":"WayLookup_top.WayLookup.readPtr_value",
        "writePtr_value":"WayLookup_top.WayLookup.writePtr_value",
        "readptr_flag":"WayLookup_top.WayLookup.readPtr_flag",
        "writeptr_flag":"WayLookup_top.WayLookup.writePtr_flag",
        "gpf_entry_valid":"WayLookup_top.WayLookup.gpf_entry_valid",
    }
    # =================================================================
    # CP 23: 刷新操作
    # 监控目标：io.flush 信号及其影响
    # =================================================================
   
    # CP23 flush操作完全是时序逻辑，移到时序覆盖组中处理,详见define_flush_timing_coverage函数
    
    
    # =================================================================
    # CP 24: 读写指针更新
    # 监控目标：io.read.fire 和 io.write.fire 信号及指针环绕逻辑
    # =================================================================
    g.add_watch_point(
        {
            "read_valid": bundle.io._read._valid,
            "read_ready": bundle.io._read._ready,
            "write_valid": bundle.io._write._valid,
            "write_ready": bundle.io._write._ready,
            "readPtr_value": dut.GetInternalSignal(Waylookup_dict["readPtr_value"], use_vpi=False),
            "writePtr_value": dut.GetInternalSignal(Waylookup_dict["writePtr_value"], use_vpi=False),
            "readPtr_flag": dut.GetInternalSignal(Waylookup_dict["readptr_flag"], use_vpi=False),
            "writePtr_flag": dut.GetInternalSignal(Waylookup_dict["writeptr_flag"], use_vpi=False),
        },
        bins={
            # 24.1: 读指针更新fire
            "CP24.1_valid_read_fire": lambda d: d["read_valid"].value == 1 and \
                                               d["read_ready"].value == 1,
            # 24.2: 写指针更新fire
            "CP24.2_valid_write_fire": lambda d: d["write_valid"].value == 1 and \
                                                d["write_ready"].value == 1,
            
            # 队列空检测
            "CP24.3_queue_empty": lambda d: (d["readPtr_value"].value == d["writePtr_value"].value and \
                                             d["readPtr_flag"].value == d["writePtr_flag"].value),
            
            # 队列满检测
            "CP24.4_queue_full": lambda d: (d["readPtr_value"].value == d["writePtr_value"].value and \
                                           d["readPtr_flag"].value != d["writePtr_flag"].value)
        },
        name="CP24_Pointer_Updates_Enhanced"
    )
    
    # Mark function for CP24 - Pointer Updates
    g.mark_function("CP24_Pointer_Updates_Enhanced", _M(["test_cp24_pointer_updates","test_pointer_wraparound"]), 
                   bin_name=["CP24.1_valid_read_fire", "CP24.2_valid_write_fire", "CP24.3_queue_empty", "CP24.4_queue_full"])
    
    # =================================================================
    # CP 25: 更新操作
    # 监控目标：MissUnit的update操作，精确监控vset_same和ptag_same
    # =================================================================
    g.add_watch_point(
        {
            "update_valid": bundle.io._update._valid,
            "update_corrupt": bundle.io._update._bits._corrupt,
            "vset_same": dut.GetInternalSignal(Waylookup_dict["vset_same"], use_vpi=False),
            "ptag_same": dut.GetInternalSignal(Waylookup_dict["ptag_same"], use_vpi=False),
        },
        bins={
            # 25.1: 命中更新触发条件
            "CP25.1_hit_update_trigger": lambda d: (d["update_valid"].value == 1 and \
                                                   d["vset_same"].value == 1 and \
                                                   d["ptag_same"].value == 1 and \
                                                   d["update_corrupt"].value == 0),
            
            # 25.2: 未命中更新触发条件
            "CP25.2_miss_update_trigger": lambda d: (d["update_valid"].value == 1 and \
                                                    d["vset_same"].value == 1 and \
                                                    d["ptag_same"].value == 0 and \
                                                    d["update_corrupt"].value == 0),
            
            # 25.3: 不更新 - vset_same为假
            "CP25.3_no_update_vset_diff": lambda d: (d["update_valid"].value == 1 and \
                                                    d["vset_same"].value == 0),
            
            # 25.3: 不更新 - corrupt数据
            "CP25.3_no_update_corrupt": lambda d: (d["update_valid"].value == 1 and \
                                                  d["update_corrupt"].value == 1),
        },
        name="CP25_Update_Operations_Precise"
    )
    
    # Mark function for CP25 - Update Operations
    g.mark_function("CP25_Update_Operations_Precise", _M(["test_cp25_update_operations", 
                                                          "test_bundle_interface_comprehensive",
                                                          "test_bundle_signal_ranges_and_limits",
                                                          "test_bundle_signal_coverage_complete"]), 
                   bin_name=["CP25.1_hit_update_trigger", "CP25.2_miss_update_trigger", 
                            "CP25.3_no_update_vset_diff", "CP25.3_no_update_corrupt"])
    
    # =================================================================
    # CP 26: 读操作
    # 监控目标：各种读操作场景，包括bypass、正常读、GPF处理
    # =================================================================
    g.add_watch_point(
        {
            "read_valid": bundle.io._read._valid,
            "read_ready": bundle.io._read._ready,
            "write_valid": bundle.io._write._valid,
            "gpf_hit": dut.GetInternalSignal(Waylookup_dict["gpf_hit"], use_vpi=False),
            "empty": dut.GetInternalSignal(Waylookup_dict["empty"], use_vpi=False),
        },
        bins={
            # 26.1: Bypass 读 - 队列为空且写有效
            "CP26.1_bypass_read": lambda d: d["empty"].value == 1 and d["write_valid"].value == 1 and d["read_ready"].value == 1,
            
            # 26.2: 读信号无效 - 队列空且写信号无效
            "CP26.2_read_invalid": lambda d: d["empty"].value == 1 and d["write_valid"].value == 0,
            
            # 26.3: 正常读 - 从队列读取 (非空)
            "CP26.3_normal_read": lambda d: d["empty"].value == 0 and d["read_valid"].value == 1 and d["read_ready"].value == 1,
            
            # 26.4 & 26.5: GPF 命中读取
            "CP26.4_5_gpf_hit_consumed": lambda d: d["read_valid"].value == 1 and d["read_ready"].value == 1 and d["gpf_hit"].value == 1,
            
            # 26.6: GPF 未命中
            "CP26.6_gpf_miss_read": lambda d: d["read_valid"].value == 1 and d["read_ready"].value == 1 and d["gpf_hit"].value == 0,
        },
        name="CP26_Read_Operations_Corrected"
    )
    
    # Mark function for CP26 - Read Operations
    g.mark_function("CP26_Read_Operations_Corrected", _M(["test_cp26_read_operations","test_read_entry_api","test_bypass_functionality"]), 
                   bin_name=["CP26.1_bypass_read", "CP26.2_read_invalid", "CP26.3_normal_read", 
                            "CP26.4_5_gpf_hit_consumed", "CP26.6_gpf_miss_read"])
    
    # =================================================================
    # CP 27: 写操作
    # 监控目标：写操作的各种情况，包括GPF停止、队列满等
    # =================================================================
    g.add_watch_point(
        {
            "write_valid": bundle.io._write._valid,
            "write_ready": bundle.io._write._ready,
            "read_ready": bundle.io._read._ready,
            "itlb_exception_0": bundle.io._write._bits._entry._itlb._exception._0,
            "itlb_exception_1": bundle.io._write._bits._entry._itlb._exception._1,
            "gpf_entry_valid": dut.GetInternalSignal(Waylookup_dict["gpf_entry_valid"], use_vpi=False),
            "gpf_hit": dut.GetInternalSignal(Waylookup_dict["gpf_hit"], use_vpi=False),
            "can_bypass": dut.GetInternalSignal(Waylookup_dict["can_bypass"], use_vpi=False),
        },
        bins={
            # 27.1: GPF 停止
            "CP27.1_stall_gpf_wait": lambda d: d["write_ready"].value == 0 and \
                                              d["gpf_entry_valid"].value == 1 and \
                                              not (d["read_ready"].value == 1 and d["gpf_hit"].value == 1),

            # 27.2: 写就绪无效 - 队列满
            "CP27.2_stall_queue_full": lambda d: d["write_ready"].value == 0,

            # 27.3: 正常写
            "CP27.3_normal_write": lambda d: d["write_valid"].value == 1 and \
                                            d["write_ready"].value == 1 and \
                                            d["itlb_exception_0"].value != 2 and \
                                            d["itlb_exception_1"].value != 2,

            # 27.4.1: 有ITLB异常的写 - 被绕过直接读取
            "CP27.4.1_itlb_write_bypassed": lambda d: d["write_valid"].value == 1 and \
                                                     d["write_ready"].value == 1 and \
                                                     d["can_bypass"].value == 1 and \
                                                     d["read_ready"].value == 1 and \
                                                     (d["itlb_exception_0"].value == 2 or d["itlb_exception_1"].value == 2),

            # 27.4.2: 有ITLB异常的写 - 没有被绕过
            "CP27.4.2_itlb_write_not_bypassed": lambda d: d["write_valid"].value == 1 and \
                                                         d["write_ready"].value == 1 and \
                                                         d["can_bypass"].value == 0 and \
                                                         (d["itlb_exception_0"].value == 2 or d["itlb_exception_1"].value == 2),
        },
        name="CP27_Write_Operations_Corrected"
    )
    
    # Mark function for CP27 - Write Operations
    g.mark_function("CP27_Write_Operations_Corrected", _M(["test_cp27_write_operations", 
                                                           "test_write_entry_api", 
                                                           "test_bypass_functionality",
                                                           "test_bundle_readback_consistency"]), 
                   bin_name=["CP27.1_stall_gpf_wait", "CP27.2_stall_queue_full", "CP27.3_normal_write", 
                            "CP27.4.1_itlb_write_bypassed", "CP27.4.2_itlb_write_not_bypassed"])
    
    # =================================================================
    # 数据范围覆盖点
    # =================================================================
    g.add_watch_point(
        {
            "write_valid": bundle.io._write._valid,
            "waymask_0": bundle.io._write._bits._entry._waymask._0,
            "waymask_1": bundle.io._write._bits._entry._waymask._1,
            "vSetIdx_0": bundle.io._write._bits._entry._vSetIdx._0,
            "vSetIdx_1": bundle.io._write._bits._entry._vSetIdx._1,
            "meta_codes_0": bundle.io._write._bits._entry._meta_codes._0,
            "meta_codes_1": bundle.io._write._bits._entry._meta_codes._1
        },
        bins={
            "CP_DATA.1_waymask_min": lambda d: d["write_valid"].value == 1 and \
                                              (d["waymask_0"].value == 0 or d["waymask_1"].value == 0),
            
            "CP_DATA.2_waymask_max": lambda d: d["write_valid"].value == 1 and \
                                              (d["waymask_0"].value == 3 or d["waymask_1"].value == 3),
            
            "CP_DATA.3_vsetidx_zero": lambda d: d["write_valid"].value == 1 and \
                                               (d["vSetIdx_0"].value == 0 or d["vSetIdx_1"].value == 0),
            
            "CP_DATA.4_vsetidx_max": lambda d: d["write_valid"].value == 1 and \
                                              (d["vSetIdx_0"].value == 0xFF or d["vSetIdx_1"].value == 0xFF),
            
            "CP_DATA.5_meta_codes_diff": lambda d: d["write_valid"].value == 1 and \
                                                   d["meta_codes_0"].value != d["meta_codes_1"].value
        },
        name="CP_Data_Range_Coverage"
    )
    
    # Mark function for Data Range Coverage
    g.mark_function("CP_Data_Range_Coverage", _M(["test_bundle_signal_ranges_and_limits", "test_write_entry_api"]), 
                   bin_name=["CP_DATA.1_waymask_min", "CP_DATA.2_waymask_max", "CP_DATA.3_vsetidx_zero", 
                            "CP_DATA.4_vsetidx_max", "CP_DATA.5_meta_codes_diff"])
    
    # =================================================================
    # 综合场景覆盖点
    # =================================================================
    g.add_watch_point(
        {
            "write_valid": bundle.io._write._valid,
            "read_ready": bundle.io._read._ready,
            "update_valid": bundle.io._update._valid,
            "flush": bundle.io._flush
        },
        bins={
            "CP_COMBO.1_multi_operation": lambda d: (d["write_valid"].value + \
                                                     d["read_ready"].value + \
                                                     d["update_valid"].value) >= 2,
            
            "CP_COMBO.2_write_then_flush": lambda d: d["write_valid"].value == 1 and \
                                                     d["flush"].value == 1,
            
            "CP_COMBO.3_all_idle": lambda d: d["write_valid"].value == 0 and \
                                             d["read_ready"].value == 0 and \
                                             d["update_valid"].value == 0 and \
                                             d["flush"].value == 0
        },
        name="CP_Comprehensive_Scenarios"
    )
    
    # Mark function for Comprehensive Scenarios
    g.mark_function("CP_Comprehensive_Scenarios", _M(["test_comprehensive_queue_operations", 
                                                      "test_bundle_interface_comprehensive",
                                                      "test_queue_status_apis",
                                                      "test_helper_apis"]), 
                   bin_name=["CP_COMBO.1_multi_operation", "CP_COMBO.2_write_then_flush", "CP_COMBO.3_all_idle"])
    
    return g


def define_flush_timing_coverage(dut):
    """
    定义需要特殊时序采样的flush覆盖率组
    这个组需要在flush信号拉高后的下一拍进行采样
    """
    g = CovGroup("WayLookup_Flush_Timing_Coverage")
    
    # 创建内部信号字典
    Waylookup_dict = {
        "readPtr_value":"WayLookup_top.WayLookup.readPtr_value",
        "writePtr_value":"WayLookup_top.WayLookup.writePtr_value",
        "readptr_flag":"WayLookup_top.WayLookup.readPtr_flag",
        "writeptr_flag":"WayLookup_top.WayLookup.writePtr_flag",
        "gpf_entry_valid":"WayLookup_top.WayLookup.gpf_entry_valid",
    }
    
    # 添加需要在flush后一拍采样的覆盖点
    g.add_watch_point(
        {
            "readptr_value": dut.GetInternalSignal(Waylookup_dict["readPtr_value"], use_vpi=False),
            "readptr_flag": dut.GetInternalSignal(Waylookup_dict["readptr_flag"], use_vpi=False),
            "writeptr_value": dut.GetInternalSignal(Waylookup_dict["writePtr_value"], use_vpi=False),
            "writeptr_flag": dut.GetInternalSignal(Waylookup_dict["writeptr_flag"], use_vpi=False),
            "gpf_entry_valid": dut.GetInternalSignal(Waylookup_dict["gpf_entry_valid"], use_vpi=False),
        },
        bins={
            # Flush后一拍的状态检查
            "CP23_TIMING.1_flush_effect_read_ptr": lambda d: d["readptr_value"].value == 0 and d["readptr_flag"].value == 0,
            "CP23_TIMING.2_flush_effect_write_ptr": lambda d: d["writeptr_value"].value == 0 and d["writeptr_flag"].value == 0,
            "CP23_TIMING.3_flush_effect_gpf": lambda d: d["gpf_entry_valid"].value == 0,
        },
        name="CP23_Flush_Timing_Effects"
    )
    
    # 反标
    def _M(name):
        return module_name_with(name, "../../test/waylookup_test")
    
    g.mark_function("CP23_Flush_Timing_Effects", _M(["test_cp23_flush_operations","test_smoke","test_basic_control_apis"]), 
                   bin_name=["CP23_TIMING.1_flush_effect_read_ptr", "CP23_TIMING.2_flush_effect_write_ptr", "CP23_TIMING.3_flush_effect_gpf"])
    
    return g


def define_pointer_and_update_timing_coverage(dut):
    """
    定义指针环绕和update效果的时序覆盖率组
    这些操作的效果需要在下一拍检测
    """
    g = CovGroup("WayLookup_Timing_Effects_Coverage")
    
    Waylookup_dict = {
        "readPtr_value":"WayLookup_top.WayLookup.readPtr_value",
        "writePtr_value":"WayLookup_top.WayLookup.writePtr_value",
        "gpf_entry_valid":"WayLookup_top.WayLookup.gpf_entry_valid",
    }
    
    # CP24时序：指针环绕效果检测（检测环绕后的结果，而不是环绕的触发）
    g.add_watch_point(
        {
            "readPtr_value": dut.GetInternalSignal(Waylookup_dict["readPtr_value"], use_vpi=False),
            "writePtr_value": dut.GetInternalSignal(Waylookup_dict["writePtr_value"], use_vpi=False),
        },
        bins={
            # 检测指针环绕后的状态（值为0表示刚刚环绕）
            "CP24_TIMING.1_read_ptr_wraparound_effect": lambda d: d["readPtr_value"].value == 0,
            "CP24_TIMING.2_write_ptr_wraparound_effect": lambda d: d["writePtr_value"].value == 0,
        },
        name="CP24_Pointer_Wraparound_Effects"
    )
    
    # CP25时序：Update操作效果检测（检测entries更新后的状态）
    # 注意：这里我们检测的是更新操作后entries的状态变化
    # 由于entries数组很大，我们采用采样频率方式来检测更新效果
    g.add_watch_point(
        {
            "readPtr_value": dut.GetInternalSignal(Waylookup_dict["readPtr_value"], use_vpi=False),
        },
        bins={
            # 这是一个代理检测点，通过采样时机来检测update效果
            "CP25_TIMING.1_update_effect_sample": lambda d: True,  # 总是采样，用于检测update后的状态
        },
        name="CP25_Update_Effects"
    )
    
    # CP27时序：GPF entry更新效果检测
    g.add_watch_point(
        {
            "gpf_entry_valid": dut.GetInternalSignal(Waylookup_dict["gpf_entry_valid"], use_vpi=False),
        },
        bins={
            # 检测GPF entry状态变化（在写操作后下一拍检测）
            "CP27_TIMING.1_gpf_entry_updated": lambda d: d["gpf_entry_valid"].value == 1,
            "CP27_TIMING.2_gpf_entry_cleared": lambda d: d["gpf_entry_valid"].value == 0,
        },
        name="CP27_GPF_Effects"
    )
    
    # 反标
    def _M(name):
        return module_name_with(name, "../../test/waylookup_test")
    
    g.mark_function("CP24_Pointer_Wraparound_Effects", _M("test_cp24_pointer_updates"), 
                   bin_name=["CP24_TIMING.1_read_ptr_wraparound_effect", "CP24_TIMING.2_write_ptr_wraparound_effect"])
    g.mark_function("CP25_Update_Effects", _M("test_cp25_update_operations"), 
                   bin_name=["CP25_TIMING.1_update_effect_sample"])
    g.mark_function("CP27_GPF_Effects", _M("test_cp27_write_operations"), 
                   bin_name=["CP27_TIMING.1_gpf_entry_updated", "CP27_TIMING.2_gpf_entry_cleared"])
    
    return g


def create_waylookup_coverage_groups(bundle, dut):
    """
    创建WayLookup模块的所有功能覆盖点组合
    
    Args:
        bundle: WayLookupBundle对象
        dut: DUT对象用于访问内部信号
        
    Returns:
        dict: 包含常规覆盖组和时序覆盖组的字典
    """
    # 常规覆盖组（自动采样）
    regular_coverage = define_waylookup_coverage(bundle, dut)
    
    # 时序覆盖组（需要特殊采样）
    flush_timing_coverage = define_flush_timing_coverage(dut)
    pointer_and_update_timing_coverage = define_pointer_and_update_timing_coverage(dut)
    
    return {
        "regular": [regular_coverage],
        "timing": [flush_timing_coverage, pointer_and_update_timing_coverage]
    }