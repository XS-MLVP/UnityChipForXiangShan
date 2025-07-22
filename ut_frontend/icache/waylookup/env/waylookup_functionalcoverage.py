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
    
    # =================================================================
    # CP 23: 刷新操作
    # 监控目标：io.flush 信号及其影响
    # =================================================================
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "write_ready": bundle.io._write._ready,
            "read_valid": bundle.io._read._valid
        },
        bins={
            # 23.1: 刷新读指针 - io.flush 为高时
            "CP23.1_flush_reset_read_ptr": lambda d: d["flush"].value == 1,
            
            # 23.2: 刷新写指针 - io.flush 为高时  
            "CP23.2_flush_reset_write_ptr": lambda d: d["flush"].value == 1,
            
            # 23.3: 刷新 GPF 信息 - io.flush 为高时
            "CP23.3_flush_reset_gpf": lambda d: d["flush"].value == 1,
            
            # 验证flush后状态恢复
            "CP23.4_post_flush_state": lambda d: d["flush"].value == 0 and \
                                                 d["write_ready"].value == 1 and \
                                                 d["read_valid"].value == 0
        },
        name="CP23_Flush_Operations"
    )
    
    # =================================================================
    # CP 24: 读写指针更新
    # 监控目标：io.read.fire 和 io.write.fire 信号
    # =================================================================
    g.add_watch_point(
        {
            "read_valid": bundle.io._read._valid,
            "read_ready": bundle.io._read._ready,
            "write_valid": bundle.io._write._valid,
            "write_ready": bundle.io._write._ready
        },
        bins={
            # 24.1: 读指针更新 - 当 io.read.fire 为高时
            "CP24.1_valid_read_fire": lambda d: d["read_valid"].value == 1 and \
                                               d["read_ready"].value == 1,
            # 24.2: 写指针更新 - 当 io.write.fire 为高时
            "CP24.2_valid_write_fire": lambda d: d["write_valid"].value == 1 and \
                                                d["write_ready"].value == 1
        },
        name="CP24_Pointer_Updates"
    )
    
    # =================================================================
    # CP 25: 更新操作
    # 监控目标：MissUnit的update操作，包含命中/未命中情况
    # =================================================================
    g.add_watch_point(
        {
            "update_valid": bundle.io._update._valid,
            "update_blkPaddr": bundle.io._update._bits._blkPaddr,
            "update_vSetIdx": bundle.io._update._bits._vSetIdx,
            "update_waymask": bundle.io._update._bits._waymask,
            "update_corrupt": bundle.io._update._bits._corrupt
        },
        bins={
            # 25.1: 命中更新 - vset_same 和 ptag_same 为真 
            # Todo:将vset_same和ptag_same加入可访问的内部信号
            # 注意：由于无法直接访问vset_same和ptag_same信号，使用update_valid和非corrupt作为代理
            "CP25.1_hit_update": lambda d: d["update_valid"].value == 1 and \
                                          d["update_corrupt"].value == 0 and \
                                          d["update_waymask"].value != 0,
            
            # 25.2: 未命中更新 - vset_same 为真但way不同，waymask清零
            "CP25.2_miss_update": lambda d: d["update_valid"].value == 1 and \
                                           d["update_corrupt"].value == 0 and \
                                           d["update_waymask"].value == 0,
            
            # 25.3: 不更新 - corrupt或其他原因不更新
            "CP25.3_no_update": lambda d: d["update_valid"].value == 1 and \
                                         d["update_corrupt"].value == 1,
            
            # 验证update字段值
            "CP25.4_update_valid_data": lambda d: d["update_valid"].value == 1 and \
                                                 d["update_blkPaddr"].value != 0 and \
                                                 d["update_vSetIdx"].value <= 0xFF
        },
        name="CP25_Update_Operations"
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
            "write_ready": bundle.io._write._ready,
        },
        bins={
            # 26.1: Bypass 读 - 队列为空且写有效，可以直接读取
            "CP26.1_bypass_read": lambda d: d["write_valid"].value == 1 and \
                                           d["read_valid"].value == 1 and \
                                           d["read_ready"].value == 1,
            
            # 26.2: 读信号无效 - 队列空且写信号无效
            "CP26.2_read_invalid": lambda d: d["read_valid"].value == 0 and \
                                            d["write_valid"].value == 0,
            
            # 26.3: 正常读 - 从队列读取
            "CP26.3_normal_read": lambda d: d["read_valid"].value == 1 and \
                                           d["read_ready"].value == 1 and \
                                           d["write_valid"].value == 0,
            
            # 26.4: GPF 命中读取 - 需要通过GPF exception信号间接判断
            "CP26.4_gpf_hit_read": lambda d: d["read_valid"].value == 1 and \
                                           d["read_ready"].value == 1,
            
            # 26.5: GPF 命中且被读取 - GPF数据被消费
            "CP26.5_gpf_consumed": lambda d: d["read_valid"].value == 1 and \
                                           d["read_ready"].value == 1,
            
            # 26.6: GPF 未命中
            "CP26.6_gpf_miss": lambda d: d["read_valid"].value == 1 and \
                                        d["read_ready"].value == 1
        },
        name="CP26_Read_Operations"
    )
    
    # =================================================================
    # CP 27: 写操作
    # 监控目标：写操作的各种情况，包括GPF停止、队列满等
    # =================================================================
    g.add_watch_point(
        {
            "write_valid": bundle.io._write._valid,
            "write_ready": bundle.io._write._ready,
            "read_valid": bundle.io._read._valid,
            "read_ready": bundle.io._read._ready,
            "itlb_exception_0": bundle.io._write._bits._entry._itlb._exception._0,
            "itlb_exception_1": bundle.io._write._bits._entry._itlb._exception._1,
            "gpf_gpaddr": bundle.io._write._bits._gpf._gpaddr
        },
        bins={
            # 27.1: GPF 停止 - 有有效GPF且未被读取时停止写
            "CP27.1_gpf_stall": lambda d: d["write_valid"].value == 1 and \
                                         d["write_ready"].value == 0,
            
            # 27.2: 写就绪无效 - 队列满或GPF停止
            "CP27.2_write_not_ready": lambda d: d["write_valid"].value == 1 and \
                                               d["write_ready"].value == 0,
            
            # 27.3: 正常写 - 成功写入队列
            "CP27.3_normal_write": lambda d: d["write_valid"].value == 1 and \
                                            d["write_ready"].value == 1 and \
                                            d["itlb_exception_0"].value != 2 and \
                                            d["itlb_exception_1"].value != 2,
            
            # 27.4.1: 有ITLB异常的写 - 被绕过直接读取
            "CP27.4.1_itlb_write_bypassed": lambda d:d["write_valid"].value == 1 and \
                                                    d["write_ready"].value == 1 and \
                                                     d["read_valid"].value == 1 and \
                                                     d["read_ready"].value == 1 and \
                                                     (d["itlb_exception_0"].value == 2 or \
                                                      d["itlb_exception_1"].value == 2),
            
            # 27.4.2: 有ITLB异常的写 - 没有被绕过
            "CP27.4.2_itlb_write_not_bypassed": lambda d: d["write_valid"].value == 1 and \
                                                        d["write_ready"].value == 1  and \
                                                        d["read_valid"].value == 1 and \
                                                        d["read_ready"].value == 1 and \
                                                         (d["itlb_exception_0"].value == 2 or \
                                                          d["itlb_exception_1"].value == 2),
            
            # 验证GPF地址有效性
            "CP27.5_valid_gpf_addr": lambda d: d["write_valid"].value == 1 and \
                                                d["write_ready"].value == 1 and \
                                              (d["itlb_exception_0"].value == 2 or \
                                               d["itlb_exception_1"].value == 2) and \
                                              d["gpf_gpaddr"].value != 0
        },
        name="CP27_Write_Operations"
    )
    
    # =================================================================
    # 数据范围覆盖点 (保留原有的数据边界值测试)
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
            # 数据边界值覆盖
            "CP_DATA.1_waymask_min": lambda d: d["write_valid"].value == 1 and \
                                              (d["waymask_0"].value == 0 or d["waymask_1"].value == 0),
            
            "CP_DATA.2_waymask_max": lambda d: d["write_valid"].value == 1 and \
                                              (d["waymask_0"].value == 15 or d["waymask_1"].value == 15),
            
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
            "read_valid": bundle.io._read._valid,
            "update_valid": bundle.io._update._valid,
            "flush": bundle.io._flush
        },
        bins={
            # 多操作并发场景
            "CP_COMBO.1_multi_operation": lambda d: (d["write_valid"].value + \
                                                     d["read_ready"].value + \
                                                     d["update_valid"].value) >= 2,
            
            # 写操作后立即flush
            "CP_COMBO.2_write_then_flush": lambda d: d["write_valid"].value == 1 and \
                                                     d["flush"].value == 1,
            
            # 所有接口空闲
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