import toffee.funcov as fc
from toffee.funcov import CovGroup


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
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "readptr_value": dut.GetInternalSignal(Waylookup_dict["readPtr_value"],use_vpi=False),
            "readptr_flag": dut.GetInternalSignal(Waylookup_dict["readptr_flag"],use_vpi=False),
            "writeptr_value": dut.GetInternalSignal(Waylookup_dict["writePtr_value"],use_vpi=False),
            "writeptr_flag": dut.GetInternalSignal(Waylookup_dict["writeptr_flag"],use_vpi=False),
            "gpf_entry_valid": dut.GetInternalSignal(Waylookup_dict["gpf_entry_valid"],use_vpi=False),
        },
        bins={
            # 23.1: 刷新读指针
            "CP23.1_flush_reset_read_ptr": lambda d: d["flush"].value == 1 and \
                                                 d["readptr_value"].value == 0 and \
                                                 d["readptr_flag"].value == 0,
            
            # 23.2: 刷新写指针
            "CP23.2_flush_reset_write_ptr": lambda d: d["flush"].value == 1 and \
                                                  d["writeptr_value"].value == 0 and \
                                                  d["writeptr_flag"].value == 0,
            
            # 23.3: 刷新 GPF 信息
            "CP23.3_flush_reset_gpf": lambda d: d["flush"].value == 1 and \
                                              d["gpf_entry_valid"].value == 0,
        },
        name="CP23_Flush_Operations"
    )
    
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
            # 24.1: 读指针更新
            "CP24.1_valid_read_fire": lambda d: d["read_valid"].value == 1 and \
                                               d["read_ready"].value == 1,
            # 24.2: 写指针更新
            "CP24.2_valid_write_fire": lambda d: d["write_valid"].value == 1 and \
                                                d["write_ready"].value == 1,
            
            # 24.1增强: 读指针环绕检测
            "CP24.1_read_ptr_wraparound": lambda d: (d["read_valid"].value == 1 and \
                                                     d["read_ready"].value == 1 and \
                                                     d["readPtr_value"].value == 31),
            
            # 24.2增强: 写指针环绕检测
            "CP24.2_write_ptr_wraparound": lambda d: (d["write_valid"].value == 1 and \
                                                      d["write_ready"].value == 1 and \
                                                      d["writePtr_value"].value == 31),
            
            # 队列空检测
            "CP24.3_queue_empty": lambda d: (d["readPtr_value"].value == d["writePtr_value"].value and \
                                             d["readPtr_flag"].value == d["writePtr_flag"].value),
            
            # 队列满检测
            "CP24.4_queue_full": lambda d: (d["readPtr_value"].value == d["writePtr_value"].value and \
                                           d["readPtr_flag"].value != d["writePtr_flag"].value)
        },
        name="CP24_Pointer_Updates_Enhanced"
    )
    
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
            # 25.1: 命中更新
            "CP25.1_hit_update_precise": lambda d: (d["update_valid"].value == 1 and \
                                                   d["vset_same"].value == 1 and \
                                                   d["ptag_same"].value == 1 and \
                                                   d["update_corrupt"].value == 0),
            
            # 25.2: 未命中更新
            "CP25.2_miss_update_precise": lambda d: (d["update_valid"].value == 1 and \
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
            
            # 26.4 & 26.5: GPF 命中读取 (消费)
            "CP26.4_5_gpf_hit_consumed": lambda d: d["read_valid"].value == 1 and d["read_ready"].value == 1 and d["gpf_hit"].value == 1,
            
            # 26.6: GPF 未命中
            "CP26.6_gpf_miss_read": lambda d: d["read_valid"].value == 1 and d["read_ready"].value == 1 and d["gpf_hit"].value == 0,
        },
        name="CP26_Read_Operations_Corrected"
    )
    
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
    
    return g


def create_waylookup_coverage_groups(bundle, dut):
    """
    创建WayLookup模块的所有功能覆盖点组合
    
    Args:
        bundle: WayLookupBundle对象
        dut: DUT对象用于访问内部信号
        
    Returns:
        list: 包含所有覆盖点组的列表
    """
    waylookup_coverage = define_waylookup_coverage(bundle, dut)
    
    return [waylookup_coverage]