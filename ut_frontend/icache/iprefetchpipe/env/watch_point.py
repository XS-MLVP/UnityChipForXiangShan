import toffee.funcov as fc
from toffee.funcov import CovGroup
from dut.IPrefetchPipe import DUTIPrefetchPipe

def check_prefetch_start_address(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_req_vaddr_0.value == dut.io_req_bits_startAddr.value

def check_prefetch_nextline_address(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_req_vaddr_1.value == dut.io_req_bits_nextlineStart.value

def check_prefetch_is_soft_prefetch(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_isSoftPrefetch.value == dut.io_req_bits_isSoftPrefetch.value

def check_prefetch_double_line(dut: DUTIPrefetchPipe) -> bool:
    if dut.io_req_bits_startAddr.value:
        return dut.IPrefetchPipe_s1_doubleline.value == int((bin(dut.io_req_bits_startAddr.value)[2:])[-6])
    else:
        return False

def check_prefetch_ftq_idx_flag(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_req_ftqIdx_flag.value == dut.io_req_bits_ftqIdx_flag.value

def check_prefetch_ftq_idx_value(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_req_ftqIdx_value.value == dut.io_req_bits_ftqIdx_value.value

def check_prefetch_backend_exception_0(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_backendException_0.value == dut.io_req_bits_backendException.value

def check_prefetch_backend_exception_1(dut: DUTIPrefetchPipe) -> bool:
    return dut.IPrefetchPipe_s1_backendException_1.value == dut.io_req_bits_backendException.value


def define_iprefetchpipe_coverage(bundle, dut):
    """
    定义IPrefetchPipe模块的功能覆盖点。
    覆盖点设计符合IPrefetchPipe.md功能规范文档。
    
    Args:
        bundle: IPrefetchPipeBundle顶层对象
        dut: DUT对象，用于访问内部信号
    """
    g = CovGroup("IPrefetchPipe_Coverage")
    
    # 创建IPrefetchPipe内部信号字典，便于访问（根据实际可访问的信号更新）
    IPrefetchPipe_dict = {
        "s0_fire": "IPrefetchPipe_top.IPrefetchPipe.s0_fire",
        "s1_doubleline": "IPrefetchPipe_top.IPrefetchPipe.s1_doubleline",
        "s1_valid": "IPrefetchPipe_top.IPrefetchPipe.s1_valid", 
        "s1_real_fire": "IPrefetchPipe_top.IPrefetchPipe.s1_real_fire",
        "s1_isSoftPrefetch": "IPrefetchPipe_top.IPrefetchPipe.s1_isSoftPrefetch",
        "s2_valid": "IPrefetchPipe_top.IPrefetchPipe.s2_valid",
        "s2_ready": "IPrefetchPipe_top.IPrefetchPipe.s2_ready",
        "state": "IPrefetchPipe_top.IPrefetchPipe.state",
        "next_state": "IPrefetchPipe_top.IPrefetchPipe.next_state",
        "itlb_finish": "IPrefetchPipe_top.IPrefetchPipe.itlb_finish",
        # 异常处理相关内部信号
        "s1_backend_exception_0": "IPrefetchPipe_top.IPrefetchPipe.s1_backendException_0",
        "s1_backend_exception_1": "IPrefetchPipe_top.IPrefetchPipe.s1_backendException_1",
        "s2_exception_0": "IPrefetchPipe_top.IPrefetchPipe.s2_exception_0",
        "s2_exception_1": "IPrefetchPipe_top.IPrefetchPipe.s2_exception_1",
        # CP2相关的ITLB处理信号
        "s1_wait_itlb_0": "IPrefetchPipe_top.IPrefetchPipe.s1_wait_itlb_0",
        "s1_wait_itlb_1": "IPrefetchPipe_top.IPrefetchPipe.s1_wait_itlb_1",
        "s1_need_itlb_0": "IPrefetchPipe_top.IPrefetchPipe.s1_need_itlb_0",
        "s1_need_itlb_1": "IPrefetchPipe_top.IPrefetchPipe.s1_need_itlb_1",
        "tlb_valid_pulse_0": "IPrefetchPipe_top.IPrefetchPipe.tlb_valid_pulse_0",
        "tlb_valid_pulse_1": "IPrefetchPipe_top.IPrefetchPipe.tlb_valid_pulse_1",
        "s1_req_paddr_0": "IPrefetchPipe_top.IPrefetchPipe.s1_req_paddr_0",
        "s1_req_paddr_1": "IPrefetchPipe_top.IPrefetchPipe.s1_req_paddr_1",
        "s1_itlb_exception_0": "IPrefetchPipe_top.IPrefetchPipe.s1_itlb_exception_0",
        "s1_itlb_exception_1": "IPrefetchPipe_top.IPrefetchPipe.s1_itlb_exception_1",
        "s1_itlb_pbmt_0": "IPrefetchPipe_top.IPrefetchPipe.s1_itlb_pbmt_0",
        "s1_itlb_pbmt_1": "IPrefetchPipe_top.IPrefetchPipe.s1_itlb_pbmt_1",
        # CP8和CP9相关的MSHR和SRAM信号
        "s2_waymasks_0": "IPrefetchPipe_top.IPrefetchPipe.s2_waymasks_0",
        "s2_waymasks_1": "IPrefetchPipe_top.IPrefetchPipe.s2_waymasks_1",
        "s2_MSHR_hits_valid": "IPrefetchPipe_top.IPrefetchPipe.s2_MSHR_hits_valid",
        "s2_MSHR_hits_valid_1": "IPrefetchPipe_top.IPrefetchPipe.s2_MSHR_hits_valid_1",
        "s2_MSHR_match_0": "IPrefetchPipe_top.IPrefetchPipe.s2_MSHR_match_0",
        "s2_MSHR_match_1": "IPrefetchPipe_top.IPrefetchPipe.s2_MSHR_match_1",
        "s2_doubleline": "IPrefetchPipe_top.IPrefetchPipe.s2_doubleline",
        "s2_req_vaddr_0": "IPrefetchPipe_top.IPrefetchPipe.s2_req_vaddr_0",
        "s2_req_vaddr_1": "IPrefetchPipe_top.IPrefetchPipe.s2_req_vaddr_1",
        "s2_req_paddr_0": "IPrefetchPipe_top.IPrefetchPipe.s2_req_paddr_0",
        "s2_req_paddr_1": "IPrefetchPipe_top.IPrefetchPipe.s2_req_paddr_1",
        # CP9专用信号 - 发送请求到missUnit
        "s2_miss_0": "IPrefetchPipe_top.IPrefetchPipe.s2_miss_0",
        "s2_miss_1": "IPrefetchPipe_top.IPrefetchPipe.s2_miss_1",
        "has_send_0": "IPrefetchPipe_top.IPrefetchPipe.has_send_0",
        "has_send_1": "IPrefetchPipe_top.IPrefetchPipe.has_send_1",
        "s2_mmio_0": "IPrefetchPipe_top.IPrefetchPipe.s2_mmio_0",
        "s2_mmio_1": "IPrefetchPipe_top.IPrefetchPipe.s2_mmio_1",
        # 仲裁器相关信号
        "toMSHRArbiter_io_in_0_valid": "IPrefetchPipe._toMSHRArbiter_io_in_0_valid_T_2",
        "toMSHRArbiter_io_in_1_valid": "IPrefetchPipe._toMSHRArbiter_io_in_1_valid_T_2",
        "toMSHRArbiter_io_in_0_ready": "IPrefetchPipe._toMSHRArbiter_io_in_0_ready",
        "toMSHRArbiter_io_in_1_ready": "IPrefetchPipe._toMSHRArbiter_io_in_1_ready",
        # CP10刷新机制相关内部信号
        "from_bpu_s0_flush_probe": "IPrefetchPipe_top.IPrefetchPipe.from_bpu_s0_flush_probe",
        "from_bpu_s1_flush_probe": "IPrefetchPipe_top.IPrefetchPipe.from_bpu_s1_flush_probe",
    }
    
    # =================================================================
    # CP 1: 接收预取请求覆盖点
    # 监控目标：硬件/软件预取请求的接收和处理，单/双cacheline
    # =================================================================
    g.add_watch_point(
        {
            "s0_fire": dut.GetInternalSignal(IPrefetchPipe_dict["s0_fire"], use_vpi=False),
            "s0_doubleline": dut.GetInternalSignal(IPrefetchPipe_dict["s1_doubleline"], use_vpi=False),
            "req_valid": bundle.io._req._valid,
            "req_ready": bundle.io._req._ready,
            "req_is_soft_prefetch": bundle.io._req._bits._isSoftPrefetch,
        },
        bins={
            # CP 1.1.1: 硬件预取请求可以继续
            "CP1_1_1_hw_prefetch_can_continue": lambda d: (d["req_valid"].value == 1 and 
                                                           d["req_ready"].value == 1 and 
                                                           d["req_is_soft_prefetch"].value == 0 and 
                                                           d["s0_fire"].value == 1),
            
            # CP 1.1.2: 硬件预取请求被拒绝–预取请求无效
            "CP1_1_2_hw_prefetch_rejected_invalid": lambda d: (d["req_valid"].value == 0 and 
                                                               d["req_is_soft_prefetch"].value == 0 and 
                                                               d["s0_fire"].value == 0),
            
            # CP 1.1.3: 硬件预取请求被拒绝–IPrefetchPipe非空闲
            "CP1_1_3_hw_prefetch_rejected_not_ready": lambda d: (d["req_valid"].value == 1 and 
                                                                 d["req_ready"].value == 0 and 
                                                                 d["req_is_soft_prefetch"].value == 0 and 
                                                                 d["s0_fire"].value == 0),
            
            # CP 1.1.5: 硬件预取请求有效且为单cacheline
            "CP1_1_5_hw_prefetch_single_cacheline": lambda d: (d["req_valid"].value == 1 and 
                                                               d["req_ready"].value == 1 and 
                                                               d["req_is_soft_prefetch"].value == 0 and 
                                                               d["s0_fire"].value == 1 and 
                                                               d["s0_doubleline"].value == 0),
            
            # CP 1.1.6: 硬件预取请求有效且为双cacheline
            "CP1_1_6_hw_prefetch_double_cacheline": lambda d: (d["req_valid"].value == 1 and 
                                                               d["req_ready"].value == 1 and 
                                                               d["req_is_soft_prefetch"].value == 0 and 
                                                               d["s0_fire"].value == 1 and 
                                                               d["s0_doubleline"].value == 1),
            
            # CP 1.2.1: 软件预取请求可以继续
            "CP1_2_1_sw_prefetch_can_continue": lambda d: (d["req_valid"].value == 1 and 
                                                           d["req_ready"].value == 1 and 
                                                           d["req_is_soft_prefetch"].value == 1 and 
                                                           d["s0_fire"].value == 1),
            
            # CP 1.2.2: 软件预取请求被拒绝–预取请求无效
            "CP1_2_2_sw_prefetch_rejected_invalid": lambda d: (d["req_valid"].value == 0 and 
                                                               d["req_is_soft_prefetch"].value == 1 and 
                                                               d["s0_fire"].value == 0),
            
            # CP 1.2.5: 软件预取请求有效且为单cacheline
            "CP1_2_5_sw_prefetch_single_cacheline": lambda d: (d["req_valid"].value == 1 and 
                                                               d["req_ready"].value == 1 and 
                                                               d["req_is_soft_prefetch"].value == 1 and 
                                                               d["s0_fire"].value == 1 and 
                                                               d["s0_doubleline"].value == 0),
            
            # CP 1.2.6: 软件预取请求有效且为双cacheline
            "CP1_2_6_sw_prefetch_double_cacheline": lambda d: (d["req_valid"].value == 1 and 
                                                               d["req_ready"].value == 1 and 
                                                               d["req_is_soft_prefetch"].value == 1 and 
                                                               d["s0_fire"].value == 1 and 
                                                               d["s0_doubleline"].value == 1),
        },
        name="CP1_Prefetch_Request_Reception"
    )
    
    # =================================================================
    # CP 2: 接收来自ITLB的响应并处理结果覆盖点
    # 监控目标：ITLB响应的接收、地址转换完成、异常处理、虚拟机物理地址处理、pbmt信息
    # =================================================================
    g.add_watch_point(
        {
            # 基本控制信号
            "s1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s1_valid"], use_vpi=False),
            "itlb_finish": dut.GetInternalSignal(IPrefetchPipe_dict["itlb_finish"], use_vpi=False),
            "s1_doubleline": dut.GetInternalSignal(IPrefetchPipe_dict["s1_doubleline"], use_vpi=False),
            
            # ITLB响应信号
            "itlb_miss_0": bundle.io._itlb._0._resp_bits._miss,
            "itlb_miss_1": bundle.io._itlb._1._resp_bits._miss,
            "itlb_paddr_0": bundle.io._itlb._0._resp_bits._paddr._0,
            "itlb_paddr_1": bundle.io._itlb._1._resp_bits._paddr._0,
            "itlb_gpaddr_0": bundle.io._itlb._0._resp_bits._gpaddr._0,
            "itlb_gpaddr_1": bundle.io._itlb._1._resp_bits._gpaddr._0,
            "itlb_pbmt_0": bundle.io._itlb._0._resp_bits._pbmt._0,
            "itlb_pbmt_1": bundle.io._itlb._1._resp_bits._pbmt._0,
            "itlb_isForVSnonLeafPTE_0": bundle.io._itlb._0._resp_bits._isForVSnonLeafPTE,
            "itlb_isForVSnonLeafPTE_1": bundle.io._itlb._1._resp_bits._isForVSnonLeafPTE,
            
            # ITLB异常信号
            "itlb_0_pf_instr": bundle.io._itlb._0._resp_bits._excp._0._pf_instr,
            "itlb_0_gpf_instr": bundle.io._itlb._0._resp_bits._excp._0._gpf_instr,
            "itlb_0_af_instr": bundle.io._itlb._0._resp_bits._excp._0._af_instr,
            "itlb_1_pf_instr": bundle.io._itlb._1._resp_bits._excp._0._pf_instr,
            "itlb_1_gpf_instr": bundle.io._itlb._1._resp_bits._excp._0._gpf_instr,
            "itlb_1_af_instr": bundle.io._itlb._1._resp_bits._excp._0._af_instr,
        },
        bins={
            # =========== CP 2.1: 地址转换完成 ===========
            
            # CP 2.1.1: ITLB正常返回物理地址（单端口）
            "CP2_1_1_itlb_normal_paddr_return_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                                 d["itlb_finish"].value == 1 and 
                                                                 d["itlb_miss_0"].value == 0 and 
                                                                 d["itlb_paddr_0"].value != 0 and
                                                                 d["s1_doubleline"].value == 0),
            
            # CP 2.1.1: ITLB正常返回物理地址（双端口）
            "CP2_1_1_itlb_normal_paddr_return_dual_port": lambda d: (d["s1_valid"].value == 1 and 
                                                                     d["itlb_finish"].value == 1 and 
                                                                     d["itlb_miss_0"].value == 0 and 
                                                                     d["itlb_miss_1"].value == 0 and
                                                                     d["itlb_paddr_0"].value != 0 and
                                                                     d["itlb_paddr_1"].value != 0 and
                                                                     d["s1_doubleline"].value == 1),
            
            # CP 2.1.2: ITLB发生TLB缺失，需要重试-端口0
            "CP2_1_2_itlb_miss_retry_port0": lambda d: (d["itlb_finish"].value == 0 and 
                                                        d["itlb_miss_0"].value == 1),
            
            # CP 2.1.2: ITLB发生TLB缺失，需要重试-端口1  
            "CP2_1_2_itlb_miss_retry_port1": lambda d: (d["itlb_finish"].value == 0 and 
                                                        d["itlb_miss_1"].value == 1 and
                                                        d["s1_doubleline"].value == 1),
            
            # CP 2.1.2: ITLB重试完成后继续处理
            "CP2_1_2_itlb_retry_completed": lambda d: (d["itlb_finish"].value == 1 and 
                                                       d["itlb_miss_0"].value == 0 and 
                                                       (d["itlb_miss_1"].value == 0 or d["s1_doubleline"].value == 0)),
            
            # =========== CP 2.2: 处理ITLB异常 ===========
            
            # CP 2.2.1: ITLB发生页错误异常-端口0
            "CP2_2_1_itlb_page_fault_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                        d["itlb_miss_0"].value == 0 and 
                                                        d["itlb_0_pf_instr"].value == 1 and
                                                        d["itlb_0_gpf_instr"].value == 0 and
                                                        d["itlb_0_af_instr"].value == 0),
            
            # CP 2.2.2: ITLB发生虚拟机页错误异常-端口0
            "CP2_2_2_itlb_guest_page_fault_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                              d["itlb_miss_0"].value == 0 and 
                                                              d["itlb_0_gpf_instr"].value == 1 and
                                                              d["itlb_0_pf_instr"].value == 0 and
                                                              d["itlb_0_af_instr"].value == 0),
            
            # CP 2.2.3: ITLB发生访问错误异常-端口0
            "CP2_2_3_itlb_access_fault_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                          d["itlb_miss_0"].value == 0 and 
                                                          d["itlb_0_af_instr"].value == 1 and
                                                          d["itlb_0_pf_instr"].value == 0 and
                                                          d["itlb_0_gpf_instr"].value == 0),
            
            # CP 2.2.1: ITLB发生页错误异常-端口1
            "CP2_2_1_itlb_page_fault_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                        d["s1_doubleline"].value == 1 and
                                                        d["itlb_miss_1"].value == 0 and 
                                                        d["itlb_1_pf_instr"].value == 1 and
                                                        d["itlb_1_gpf_instr"].value == 0 and
                                                        d["itlb_1_af_instr"].value == 0),
            
            # CP 2.2.2: ITLB发生虚拟机页错误异常-端口1
            "CP2_2_2_itlb_guest_page_fault_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                              d["s1_doubleline"].value == 1 and
                                                              d["itlb_miss_1"].value == 0 and 
                                                              d["itlb_1_gpf_instr"].value == 1 and
                                                              d["itlb_1_pf_instr"].value == 0 and
                                                              d["itlb_1_af_instr"].value == 0),
            
            # CP 2.2.3: ITLB发生访问错误异常-端口1
            "CP2_2_3_itlb_access_fault_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                          d["s1_doubleline"].value == 1 and
                                                          d["itlb_miss_1"].value == 0 and 
                                                          d["itlb_1_af_instr"].value == 1 and
                                                          d["itlb_1_pf_instr"].value == 0 and
                                                          d["itlb_1_gpf_instr"].value == 0),
            
            # =========== CP 2.3: 处理虚拟机物理地址 ===========
            
            # CP 2.3.1: 发生虚拟机页错误异常返回虚拟机物理地址-端口0
            "CP2_3_1_gpf_return_gpaddr_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                          d["itlb_0_gpf_instr"].value == 1 and
                                                          d["itlb_gpaddr_0"].value != 0),
            
            # CP 2.3.1: 发生虚拟机页错误异常返回虚拟机物理地址-端口1
            "CP2_3_1_gpf_return_gpaddr_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                          d["s1_doubleline"].value == 1 and
                                                          d["itlb_1_gpf_instr"].value == 1 and
                                                          d["itlb_gpaddr_1"].value != 0),
            
            # CP 2.3.2: ITLB发生虚拟机页错误异常且访问二级虚拟机非叶子页表项
            "CP2_3_2_gpf_vs_nonleaf_pte": lambda d: (d["s1_valid"].value == 1 and 
                                                     (d["itlb_0_gpf_instr"].value == 1 and d["itlb_isForVSnonLeafPTE_0"].value == 1) or
                                                     (d["itlb_1_gpf_instr"].value == 1 and d["itlb_isForVSnonLeafPTE_1"].value == 1 and d["s1_doubleline"].value == 1)),
            
            # =========== CP 2.4: 返回pbmt信息 ===========
            
            # CP 2.4: TLB有效时返回pbmt信息-端口0
            "CP2_4_return_pbmt_info_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                       d["itlb_miss_0"].value == 0 and
                                                       d["itlb_pbmt_0"].value != 0),
            
            # CP 2.4: TLB有效时返回pbmt信息-端口1  
            "CP2_4_return_pbmt_info_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                       d["s1_doubleline"].value == 1 and
                                                       d["itlb_miss_1"].value == 0 and
                                                       d["itlb_pbmt_1"].value != 0),
        },
        name="CP2_ITLB_Response_Processing"
    )
    
    # =================================================================
    # CP 3: 接收来自IMeta（缓存元数据）的响应并检查缓存命中覆盖点
    # 监控目标：从Meta SRAM读取缓存标签和有效位，进行标签比较和缓存命中检查
    # =================================================================
    g.add_watch_point(
        {
            "s1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s1_valid"], use_vpi=False),
            
            # 端口0的4路有效位
            "meta_valid_0_way0": bundle.io._metaRead._fromIMeta._entryValid._0._0,
            "meta_valid_0_way1": bundle.io._metaRead._fromIMeta._entryValid._0._1,
            "meta_valid_0_way2": bundle.io._metaRead._fromIMeta._entryValid._0._2,
            "meta_valid_0_way3": bundle.io._metaRead._fromIMeta._entryValid._0._3,
            # 端口1的4路有效位
            "meta_valid_1_way0": bundle.io._metaRead._fromIMeta._entryValid._1._0,
            "meta_valid_1_way1": bundle.io._metaRead._fromIMeta._entryValid._1._1,
            "meta_valid_1_way2": bundle.io._metaRead._fromIMeta._entryValid._1._2,
            "meta_valid_1_way3": bundle.io._metaRead._fromIMeta._entryValid._1._3,
            
            # 端口0的4路标签（通过GetInternalSignal获取）
            "meta_tag_0_way0": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_0_0_tag", use_vpi=False),
            "meta_tag_0_way1": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_0_1_tag", use_vpi=False),
            "meta_tag_0_way2": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_0_2_tag", use_vpi=False),
            "meta_tag_0_way3": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_0_3_tag", use_vpi=False),
            # 端口1的4路标签
            "meta_tag_1_way0": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_1_0_tag", use_vpi=False),
            "meta_tag_1_way1": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_1_1_tag", use_vpi=False),
            "meta_tag_1_way2": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_1_2_tag", use_vpi=False),
            "meta_tag_1_way3": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.io_metaRead_fromIMeta_metas_1_3_tag", use_vpi=False),
            
            # 物理地址（用于提取标签进行比较）
            "s1_req_paddr_0": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s1_req_paddr_0", use_vpi=False),
            "s1_req_paddr_1": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s1_req_paddr_1", use_vpi=False),
            
            # 最终waymask结果（缓存命中指示）
            "s1_SRAM_waymasks_0": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s1_SRAM_waymasks_0", use_vpi=False),
            "s1_SRAM_waymasks_1": dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s1_SRAM_waymasks_1", use_vpi=False),
            
            "meta_req_valid": bundle.io._metaRead._toIMeta._valid,
            "meta_req_ready": bundle.io._metaRead._toIMeta._ready,
        },
        bins={
            # CP 3.1: 缓存标签比较和有效位检查 - 验证比较过程
            # 端口0各路的标签比较和有效位检查
            "CP3_1_tag_compare_and_valid_check_port0_way0": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_0"].value != 0 and
                # 检查标签比较：物理地址[47:12] 与 meta标签比较
                ((d["meta_tag_0_way0"].value == (d["s1_req_paddr_0"].value >> 12) and d["meta_valid_0_way0"].value == 1) or
                 (d["meta_tag_0_way0"].value != (d["s1_req_paddr_0"].value >> 12) or d["meta_valid_0_way0"].value == 0))
            ),
            
            "CP3_1_tag_compare_and_valid_check_port0_way1": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_0"].value != 0 and
                ((d["meta_tag_0_way1"].value == (d["s1_req_paddr_0"].value >> 12) and d["meta_valid_0_way1"].value == 1) or
                 (d["meta_tag_0_way1"].value != (d["s1_req_paddr_0"].value >> 12) or d["meta_valid_0_way1"].value == 0))
            ),
            
            "CP3_1_tag_compare_and_valid_check_port0_way2": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_0"].value != 0 and
                ((d["meta_tag_0_way2"].value == (d["s1_req_paddr_0"].value >> 12) and d["meta_valid_0_way2"].value == 1) or
                 (d["meta_tag_0_way2"].value != (d["s1_req_paddr_0"].value >> 12) or d["meta_valid_0_way2"].value == 0))
            ),
            
            "CP3_1_tag_compare_and_valid_check_port0_way3": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_0"].value != 0 and
                ((d["meta_tag_0_way3"].value == (d["s1_req_paddr_0"].value >> 12) and d["meta_valid_0_way3"].value == 1) or
                 (d["meta_tag_0_way3"].value != (d["s1_req_paddr_0"].value >> 12) or d["meta_valid_0_way3"].value == 0))
            ),
            
            # 端口1各路的标签比较和有效位检查
            "CP3_1_tag_compare_and_valid_check_port1_way0": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_1"].value != 0 and
                ((d["meta_tag_1_way0"].value == (d["s1_req_paddr_1"].value >> 12) and d["meta_valid_1_way0"].value == 1) or
                 (d["meta_tag_1_way0"].value != (d["s1_req_paddr_1"].value >> 12) or d["meta_valid_1_way0"].value == 0))
            ),
            
            "CP3_1_tag_compare_and_valid_check_port1_way1": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_1"].value != 0 and
                ((d["meta_tag_1_way1"].value == (d["s1_req_paddr_1"].value >> 12) and d["meta_valid_1_way1"].value == 1) or
                 (d["meta_tag_1_way1"].value != (d["s1_req_paddr_1"].value >> 12) or d["meta_valid_1_way1"].value == 0))
            ),
            
            "CP3_1_tag_compare_and_valid_check_port1_way2": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_1"].value != 0 and
                ((d["meta_tag_1_way2"].value == (d["s1_req_paddr_1"].value >> 12) and d["meta_valid_1_way2"].value == 1) or
                 (d["meta_tag_1_way2"].value != (d["s1_req_paddr_1"].value >> 12) or d["meta_valid_1_way2"].value == 0))
            ),
            
            "CP3_1_tag_compare_and_valid_check_port1_way3": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_req_paddr_1"].value != 0 and
                ((d["meta_tag_1_way3"].value == (d["s1_req_paddr_1"].value >> 12) and d["meta_valid_1_way3"].value == 1) or
                 (d["meta_tag_1_way3"].value != (d["s1_req_paddr_1"].value >> 12) or d["meta_valid_1_way3"].value == 0))
            ),
            
            # CP 3.1: 缓存未命中（标签不匹配或有效位为假）- 验证最终结果
            "CP3_1_cache_miss_port0": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_SRAM_waymasks_0"].value == 0  # waymasks为全0表示缓存未命中
            ),
            
            "CP3_1_cache_miss_port1": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_SRAM_waymasks_1"].value == 0  # waymasks为全0表示缓存未命中
            ),
            
            # CP 3.2: 单路缓存命中（标签匹配且有效位为真）- 验证最终结果
            "CP3_2_cache_hit_port0": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_SRAM_waymasks_0"].value != 0  # waymasks非0表示缓存命中
            ),
            
            "CP3_2_cache_hit_port1": lambda d: (
                d["s1_valid"].value == 1 and 
                d["s1_SRAM_waymasks_1"].value != 0  # waymasks非0表示缓存命中
            ),
        },
        name="CP3_IMeta_Response_And_Cache_Hit_Check"
    )
    
    # =================================================================
    # CP 4: PMP（物理内存保护）权限检查覆盖点
    # 监控目标：对物理地址进行PMP权限检查，确保预取操作的合法性，处理PMP返回的异常和MMIO信息
    # =================================================================
    g.add_watch_point(
        {
            "s1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s1_valid"], use_vpi=False),
            "pmp_0_instr": bundle.io._pmp._0._resp._instr,
            "pmp_0_mmio": bundle.io._pmp._0._resp._mmio,
            "pmp_1_instr": bundle.io._pmp._1._resp._instr,
            "pmp_1_mmio": bundle.io._pmp._1._resp._mmio,
            "pmp_req_addr_0": bundle.io._pmp._0._req_bits_addr,
            "pmp_req_addr_1": bundle.io._pmp._1._req_bits_addr,
        },
        bins={
            # CP 4.1: 访问被允许的内存区域 - 端口0权限检查通过
            "CP4_1_access_allowed_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                     d["pmp_req_addr_0"].value != 0 and 
                                                     d["pmp_0_instr"].value == 0 and 
                                                     d["pmp_0_mmio"].value == 0),
            
            # CP 4.1: 访问被允许的内存区域 - 端口1权限检查通过
            "CP4_1_access_allowed_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                     d["pmp_req_addr_1"].value != 0 and 
                                                     d["pmp_1_instr"].value == 0 and 
                                                     d["pmp_1_mmio"].value == 0),
            
            # CP 4.2: 访问被禁止的内存区域 - 端口0权限检查失败
            "CP4_2_access_forbidden_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                       d["pmp_req_addr_0"].value != 0 and 
                                                       d["pmp_0_instr"].value == 1),
            
            # CP 4.2: 访问被禁止的内存区域 - 端口1权限检查失败  
            "CP4_2_access_forbidden_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                       d["pmp_req_addr_1"].value != 0 and 
                                                       d["pmp_1_instr"].value == 1),
            
            # CP 4.3: 访问MMIO区域 - 端口0检测到MMIO
            "CP4_3_mmio_access_port0": lambda d: (d["s1_valid"].value == 1 and 
                                                  d["pmp_req_addr_0"].value != 0 and 
                                                  d["pmp_0_mmio"].value == 1),
            
            # CP 4.3: 访问MMIO区域 - 端口1检测到MMIO
            "CP4_3_mmio_access_port1": lambda d: (d["s1_valid"].value == 1 and 
                                                  d["pmp_req_addr_1"].value != 0 and 
                                                  d["pmp_1_mmio"].value == 1),
        },
        name="CP4_PMP_Permission_Check"
    )
    
    # =================================================================
    # CP 5: 异常处理和合并覆盖点
    # 监控目标：合并来自后端、ITLB、PMP的异常信息，按照优先级确定最终的异常类型
    # 使用内部信号直接监控异常处理状态
    # =================================================================
    g.add_watch_point(
        {
            "s1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s1_valid"], use_vpi=False),
            "s1_backend_exception_0": dut.GetInternalSignal(IPrefetchPipe_dict["s1_backend_exception_0"], use_vpi=False),
            "s1_backend_exception_1": dut.GetInternalSignal(IPrefetchPipe_dict["s1_backend_exception_1"], use_vpi=False),
            "s1_itlb_exception_0": dut.GetInternalSignal(IPrefetchPipe_dict["s1_itlb_exception_0"], use_vpi=False),
            "s1_itlb_exception_1": dut.GetInternalSignal(IPrefetchPipe_dict["s1_itlb_exception_1"], use_vpi=False),
            "s2_exception_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_exception_0"], use_vpi=False),
            "s2_exception_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_exception_1"], use_vpi=False),
            # PMP权限检查结果：instr=1表示异常（访问被禁止），instr=0表示正常
            "pmp_0_instr": bundle.io._pmp._0._resp._instr,
            "pmp_1_instr": bundle.io._pmp._1._resp._instr,
            # ITLB的原始异常信号（作为参考）
            "itlb_0_af_instr": bundle.io._itlb._0._resp_bits._excp._0._af_instr,
            "itlb_0_pf_instr": bundle.io._itlb._0._resp_bits._excp._0._pf_instr,
            "itlb_0_gpf_instr": bundle.io._itlb._0._resp_bits._excp._0._gpf_instr,
            "itlb_1_af_instr": bundle.io._itlb._1._resp_bits._excp._0._af_instr,
            "itlb_1_pf_instr": bundle.io._itlb._1._resp_bits._excp._0._pf_instr,
            "itlb_1_gpf_instr": bundle.io._itlb._1._resp_bits._excp._0._gpf_instr,
            # miss信号用于区分正常状态
            "itlb_miss_0": bundle.io._itlb._0._resp_bits._miss,
            "itlb_miss_1": bundle.io._itlb._1._resp_bits._miss,
        },
        bins={
            # CP 5.1: 仅ITLB产生异常
            "CP5_1_itlb_exception_only": lambda d: (d["s1_valid"].value == 1 and 
                                                    d["s1_backend_exception_0"].value == 0 and 
                                                    d["s1_backend_exception_1"].value == 0 and 
                                                    # 无PMP异常（PMP正常=0，异常=1）
                                                    d["pmp_0_instr"].value == 0 and 
                                                    d["pmp_1_instr"].value == 0 and 
                                                    # 有ITLB异常（使用内部信号）
                                                    (d["s1_itlb_exception_0"].value != 0 or
                                                     d["s1_itlb_exception_1"].value != 0)),
            
            # CP 5.2: 仅PMP产生异常
            "CP5_2_pmp_exception_only": lambda d: (d["s1_valid"].value == 1 and 
                                                   d["s1_backend_exception_0"].value == 0 and 
                                                   d["s1_backend_exception_1"].value == 0 and 
                                                   # 有PMP异常（PMP异常=1，正常=0）
                                                   (d["pmp_0_instr"].value == 1 or 
                                                    d["pmp_1_instr"].value == 1) and 
                                                   # 无ITLB异常（使用内部信号）
                                                   d["s1_itlb_exception_0"].value == 0 and
                                                   d["s1_itlb_exception_1"].value == 0),
            
            # CP 5.3: 仅后端产生异常
            "CP5_3_backend_exception_only": lambda d: (d["s1_valid"].value == 1 and 
                                                       (d["s1_backend_exception_0"].value != 0 or 
                                                        d["s1_backend_exception_1"].value != 0) and 
                                                       # 无PMP异常（PMP正常=0）
                                                       d["pmp_0_instr"].value == 0 and 
                                                       d["pmp_1_instr"].value == 0 and 
                                                       # 无ITLB异常（使用内部信号）
                                                       d["s1_itlb_exception_0"].value == 0 and
                                                       d["s1_itlb_exception_1"].value == 0),
            
            # CP 5.4: ITLB和PMP都产生异常（ITLB异常优先级更高）
            "CP5_4_itlb_and_pmp_exception": lambda d: (d["s1_valid"].value == 1 and 
                                                       d["s1_backend_exception_0"].value == 0 and 
                                                       d["s1_backend_exception_1"].value == 0 and 
                                                       # 有ITLB异常（使用内部信号）
                                                       (d["s1_itlb_exception_0"].value != 0 or
                                                        d["s1_itlb_exception_1"].value != 0) and 
                                                       # 有PMP异常（PMP异常=1）
                                                       (d["pmp_0_instr"].value == 1 or 
                                                        d["pmp_1_instr"].value == 1)),
            
            # CP 5.5: ITLB和后端都产生异常（后端异常优先级更高）
            "CP5_5_itlb_and_backend_exception": lambda d: (d["s1_valid"].value == 1 and 
                                                           (d["s1_backend_exception_0"].value != 0 or 
                                                            d["s1_backend_exception_1"].value != 0) and 
                                                           # 有ITLB异常（使用内部信号）
                                                           (d["s1_itlb_exception_0"].value != 0 or
                                                            d["s1_itlb_exception_1"].value != 0)),
            
            # CP 5.6: PMP和后端都产生异常（后端异常优先级更高）  
            "CP5_6_pmp_and_backend_exception": lambda d: (d["s1_valid"].value == 1 and 
                                                          (d["s1_backend_exception_0"].value != 0 or 
                                                           d["s1_backend_exception_1"].value != 0) and 
                                                          # 有PMP异常（PMP异常=1）
                                                          (d["pmp_0_instr"].value == 1 or 
                                                           d["pmp_1_instr"].value == 1)),
            
            # CP 5.7: ITLB、PMP和后端都产生异常（后端异常优先级最高）
            "CP5_7_all_exceptions": lambda d: (d["s1_valid"].value == 1 and 
                                               (d["s1_backend_exception_0"].value != 0 or 
                                                d["s1_backend_exception_1"].value != 0) and 
                                               # 有ITLB异常（使用内部信号）
                                               (d["s1_itlb_exception_0"].value != 0 or
                                                d["s1_itlb_exception_1"].value != 0) and 
                                               # 有PMP异常（PMP异常=1）
                                               (d["pmp_0_instr"].value == 1 or 
                                                d["pmp_1_instr"].value == 1)),
            
            # CP 5.8: 无任何异常
            "CP5_8_no_exception": lambda d: (d["s1_valid"].value == 1 and 
                                             d["s1_backend_exception_0"].value == 0 and 
                                             d["s1_backend_exception_1"].value == 0 and 
                                             # 无PMP异常（PMP正常=0）
                                             d["pmp_0_instr"].value == 0 and 
                                             d["pmp_1_instr"].value == 0 and 
                                             # 无ITLB异常（使用内部信号）
                                             d["s1_itlb_exception_0"].value == 0 and
                                             d["s1_itlb_exception_1"].value == 0),
        },
        name="CP5_Exception_Handling_And_Merging"
    )
    
    # =================================================================
    # CP 6: 发送请求到WayLookup模块覆盖点
    # 监控目标：当条件满足时，将请求发送到WayLookup模块，以进行后续的缓存访问
    # =================================================================
    g.add_watch_point(
        {
            "s1_valid": bundle.IPrefetchPipe._s1._valid,
            "way_lookup_valid": bundle.io._wayLookupWrite._valid,
            "way_lookup_ready": bundle.io._wayLookupWrite._ready,
            "s1_isSoftPrefetch": bundle.IPrefetchPipe._s1._isSoftPrefetch,
        },
        bins={
            # CP 6.1: 正常发送请求到WayLookup
            "CP6_1_normal_send_to_waylookup": lambda d: (d["way_lookup_valid"].value == 1 and 
                                                        d["way_lookup_ready"].value == 1 and 
                                                        d["s1_isSoftPrefetch"].value == 0 and 
                                                        d["s1_valid"].value == 1),
            
            # CP 6.2: WayLookup无法接收请求
            "CP6_2_waylookup_not_ready": lambda d: (d["way_lookup_valid"].value == 1 and 
                                                   d["way_lookup_ready"].value == 0 and 
                                                   d["s1_valid"].value == 1),
            
            # CP 6.3: 软件预取请求不发送到WayLookup
            "CP6_3_soft_prefetch_no_waylookup": lambda d: (d["s1_isSoftPrefetch"].value == 1 and 
                                                          d["way_lookup_valid"].value == 0 and 
                                                          d["s1_valid"].value == 1),
            
            # 额外的覆盖点：WayLookup请求成功发送
            "CP6_1_waylookup_request_fired": lambda d: (d["way_lookup_valid"].value == 1 and 
                                                       d["way_lookup_ready"].value == 1),
            
            # 额外的覆盖点：非软件预取且S1有效
            "CP6_1_hw_prefetch_with_s1_valid": lambda d: (d["s1_valid"].value == 1 and 
                                                         d["s1_isSoftPrefetch"].value == 0),
        },
        name="CP6_WayLookup_Request_Sending"
    )
    
    # =================================================================
    # CP 7: 状态机控制和请求处理流程覆盖点
    # 监控目标：使用状态机管理s1阶段的请求处理流程，包括ITLB重发、Meta重发、进入WayLookup、等待s2准备等状态
    # =================================================================
    g.add_watch_point(
        {
            "state": dut.GetInternalSignal(IPrefetchPipe_dict["state"], use_vpi=False),
            "next_state": dut.GetInternalSignal(IPrefetchPipe_dict["next_state"], use_vpi=False),
            "s1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s1_valid"], use_vpi=False),
            "s2_ready": dut.GetInternalSignal(IPrefetchPipe_dict["s2_ready"], use_vpi=False),
            "itlb_finish": dut.GetInternalSignal(IPrefetchPipe_dict["itlb_finish"], use_vpi=False),
            "way_lookup_valid": bundle.io._wayLookupWrite._valid,
            "way_lookup_ready": bundle.io._wayLookupWrite._ready,
            "meta_req_ready": bundle.io._metaRead._toIMeta._ready,
            "s1_isSoftPrefetch": bundle.IPrefetchPipe._s1._isSoftPrefetch,
            "s1_flush": bundle.IPrefetchPipe._s1._flush,
        },
        bins={
            # CP 7.1.1: 正常流程推进，保持m_idle状态（从 idle 直接完成所有步骤）
            "CP7_1_1_idle_normal_flow": lambda d: (d["state"].value == 0 and 
                                                   d["s1_valid"].value == 1 and 
                                                   d["itlb_finish"].value == 1 and 
                                                   d["way_lookup_valid"].value == 1 and 
                                                   d["way_lookup_ready"].value == 1 and 
                                                   d["s2_ready"].value == 1),
            
            # CP 7.1.2: 从 idle 转到 itlb_resend（s1_valid=1, itlb_finish=0）
            "CP7_1_2_idle_to_itlb_resend": lambda d: (d["state"].value == 0 and 
                                                      d["next_state"].value == 1 and
                                                      d["s1_valid"].value == 1 and 
                                                      d["itlb_finish"].value == 0),
            
            # CP 7.1.3: 从 idle 转到 enq_way（itlb_finish=1, way_lookup_ready=0）
            "CP7_1_3_idle_to_enq_way": lambda d: (d["state"].value == 0 and 
                                                  d["next_state"].value == 3 and
                                                  d["s1_valid"].value == 1 and 
                                                  d["itlb_finish"].value == 1 and 
                                                  d["way_lookup_ready"].value == 0),
            
            # CP 7.2.1: 从 itlb_resend 转到 enq_way（itlb_finish=1, meta_ready=1）
            "CP7_2_1_itlb_resend_to_enq_way": lambda d: (d["state"].value == 1 and 
                                                         d["next_state"].value == 3 and
                                                         d["itlb_finish"].value == 1 and 
                                                         d["meta_req_ready"].value == 1),
            
            # CP 7.2.2: 从 itlb_resend 转到 meta_resend（itlb_finish=1, meta_ready=0）
            "CP7_2_2_itlb_resend_to_meta_resend": lambda d: (d["state"].value == 1 and 
                                                             d["next_state"].value == 2 and
                                                             d["itlb_finish"].value == 1 and 
                                                             d["meta_req_ready"].value == 0),
            
            # CP 7.3: 从 meta_resend 转到 enq_way（meta_ready=1）
            "CP7_3_meta_resend_to_enq_way": lambda d: (d["state"].value == 2 and 
                                                       d["next_state"].value == 3 and
                                                       d["meta_req_ready"].value == 1),
            
            # CP 7.4.1: 从 enq_way 转到 idle（way_lookup_ready=1, s2_ready=1）
            # 根据Verilog: {~s2_ready, 2'h0} 当s2_ready=1时，~s2_ready=0，所以next_state=0(idle)
            "CP7_4_1_enq_way_to_idle": lambda d: (d["state"].value == 3 and 
                                                  d["next_state"].value == 0 and
                                                  ((d["way_lookup_valid"].value == 1 and d["way_lookup_ready"].value == 1) or 
                                                   d["s1_isSoftPrefetch"].value == 1) and 
                                                  d["s2_ready"].value == 1),
            
            # CP 7.4.2: 从 enq_way 转到 enter_s2（way_lookup_ready=1, s2_ready=0）  
            "CP7_4_2_enq_way_to_enter_s2": lambda d: (d["state"].value == 3 and 
                                                       d["next_state"].value == 4 and
                                                       ((d["way_lookup_valid"].value == 1 and d["way_lookup_ready"].value == 1) or 
                                                        d["s1_isSoftPrefetch"].value == 1) and 
                                                       d["s2_ready"].value == 0),
            # CP 7.5: 从 enter_s2 转到 idle（s2_ready=1）
            "CP7_5_enter_s2_to_idle": lambda d: (d["state"].value == 4 and 
                                                 d["next_state"].value == 0 and
                                                 d["s2_ready"].value == 1),
        },
        name="CP7_State_Machine_Control_And_Request_Processing"
    )
    
    # =================================================================
    # CP 8: 监控missUnit的请求覆盖点
    # 监控目标：检查missUnit的响应，更新缓存的命中状态和MSHR的匹配状态
    # =================================================================
    g.add_watch_point(
        {
            # 基本控制信号
            "s2_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s2_valid"], use_vpi=False),
            "s2_doubleline": dut.GetInternalSignal(IPrefetchPipe_dict["s2_doubleline"], use_vpi=False),
            
            # SRAM waymasks信号（用于检查SRAM命中）
            "s2_waymasks_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_waymasks_0"], use_vpi=False),
            "s2_waymasks_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_waymasks_1"], use_vpi=False),
            
            # MSHR命中状态保持信号
            "s2_MSHR_hits_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_hits_valid"], use_vpi=False),
            "s2_MSHR_hits_valid_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_hits_valid_1"], use_vpi=False),
            
            # MSHR实时匹配信号（用于检查MSHR匹配）
            "s2_MSHR_match_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_match_0"], use_vpi=False),
            "s2_MSHR_match_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_match_1"], use_vpi=False),
            
            # MSHR响应相关信号（Bundle已绑定）- 用于验证匹配逻辑
            "mshr_resp_valid": bundle.io._MSHRResp._valid,
            "mshr_resp_corrupt": bundle.io._MSHRResp._bits._corrupt,
        },
        bins={
            # =========== CP 8.1: 请求与MSHR匹配且有效 ===========
            # 文档要求：s2_req_vSetIdx和s2_req_ptags与fromMSHR中的数据匹配，且fromMSHR.valid为高，fromMSHR.bits.corrupt为假
            # s2_MSHR_match(PortNumber)为真, s2_MSHR_hits(PortNumber)应保持为真
            
            "CP8_1_mshr_match_and_valid_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                # s2_MSHR_match_0已经包含所有匹配条件(verilog L438-441)
                d["s2_MSHR_match_0"].value == 1 and
                d["s2_MSHR_hits_valid"].value == 1
            ),
            
            "CP8_1_mshr_match_and_valid_port1": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_doubleline"].value == 1 and
                # s2_MSHR_match_1已经包含所有匹配条件(verilog L442-445)
                d["s2_MSHR_match_1"].value == 1 and
                d["s2_MSHR_hits_valid_1"].value == 1
            ),
            
            # =========== CP 8.2: 请求在SRAM中命中 ===========
            # 文档要求：s2_waymasks(PortNumber)中有一位为高，表示在缓存中命中
            # s2_SRAM_hits(PortNumber)为真,s2_hits(PortNumber)应为真
            
            "CP8_2_sram_hit_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                # s2_waymasks_0中有一位为高表示SRAM命中(verilog |s2_waymasks_0)
                d["s2_waymasks_0"].value != 0
            ),
            
            "CP8_2_sram_hit_port1": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_doubleline"].value == 1 and
                # s2_waymasks_1中有一位为高表示SRAM命中(verilog |s2_waymasks_1)
                d["s2_waymasks_1"].value != 0
            ),
            
            # =========== CP 8.3: 请求未命中MSHR和SRAM ===========
            # 文档要求：请求未匹配MSHR，且s2_waymasks(PortNumber)为空
            # s2_MSHR_hits(PortNumber)、s2_SRAM_hits(PortNumber)均为假, s2_hits(PortNumber)为假
            # 根据verilog L448-453: s2_miss = ~(s2_MSHR_hits_valid | s2_MSHR_match | |s2_waymasks)
            
            "CP8_3_miss_mshr_and_sram_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                # 未命中MSHR：既没有历史命中记录，也没有当前匹配
                d["s2_MSHR_hits_valid"].value == 0 and
                d["s2_MSHR_match_0"].value == 0 and
                # 未命中SRAM：waymask为空
                d["s2_waymasks_0"].value == 0
            ),
            
            "CP8_3_miss_mshr_and_sram_port1": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_doubleline"].value == 1 and
                # 未命中MSHR：既没有历史命中记录，也没有当前匹配  
                d["s2_MSHR_hits_valid_1"].value == 0 and
                d["s2_MSHR_match_1"].value == 0 and
                # 未命中SRAM：waymask为空
                d["s2_waymasks_1"].value == 0
            ),
        },
        name="CP8_MissUnit_Monitoring"
    )
    
    # =================================================================
    # CP 9: 发送请求到missUnit覆盖点
    # 监控目标：对于未命中的预取请求，向missUnit发送请求，包括确定需要发送的请求和避免重复发送
    # =================================================================
    g.add_watch_point(
        {
            # 基本控制信号
            "s2_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s2_valid"], use_vpi=False),
            "s1_real_fire": dut.GetInternalSignal(IPrefetchPipe_dict["s1_real_fire"], use_vpi=False),
            "s2_doubleline": dut.GetInternalSignal(IPrefetchPipe_dict["s2_doubleline"], use_vpi=False),
            
            # miss判断相关信号 - 使用字典中的信号路径
            "s2_miss_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_miss_0"], use_vpi=False),
            "s2_miss_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_miss_1"], use_vpi=False),
            
            # has_send寄存器 - 避免重复发送
            "has_send_0": dut.GetInternalSignal(IPrefetchPipe_dict["has_send_0"], use_vpi=False),
            "has_send_1": dut.GetInternalSignal(IPrefetchPipe_dict["has_send_1"], use_vpi=False),
            
            # 异常和MMIO检查信号
            "s2_exception_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_exception_0"], use_vpi=False),
            "s2_exception_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_exception_1"], use_vpi=False),
            "s2_mmio_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_mmio_0"], use_vpi=False),
            "s2_mmio_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_mmio_1"], use_vpi=False),
            
            # 命中状态检查信号
            "s2_waymasks_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_waymasks_0"], use_vpi=False),
            "s2_waymasks_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_waymasks_1"], use_vpi=False),
            "s2_MSHR_hits_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_hits_valid"], use_vpi=False),
            "s2_MSHR_hits_valid_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_hits_valid_1"], use_vpi=False),
            "s2_MSHR_match_0": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_match_0"], use_vpi=False),
            "s2_MSHR_match_1": dut.GetInternalSignal(IPrefetchPipe_dict["s2_MSHR_match_1"], use_vpi=False),
            
            # 仲裁器相关信号
            "toMSHRArbiter_io_in_0_valid": dut.GetInternalSignal(IPrefetchPipe_dict["toMSHRArbiter_io_in_0_valid"], use_vpi=True),
            "toMSHRArbiter_io_in_1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["toMSHRArbiter_io_in_1_valid"], use_vpi=True),
            "toMSHRArbiter_io_in_0_ready": dut.GetInternalSignal(IPrefetchPipe_dict["toMSHRArbiter_io_in_0_ready"], use_vpi=True),
            "toMSHRArbiter_io_in_1_ready": dut.GetInternalSignal(IPrefetchPipe_dict["toMSHRArbiter_io_in_1_ready"], use_vpi=True),
            
            # bundle中的MSHR相关信号
            "mshr_req_valid": bundle.io._MSHRReq._valid,
            "mshr_req_ready": bundle.io._MSHRReq._ready,
        },
        bins={
            # =========== CP 9.1: 确定需要发送给missUnit的请求 ===========
            
            # CP 9.1.1: 请求未命中且无异常，需要发送到missUnit - 端口0
            "CP9_1_1_miss_no_exception_send_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_miss_0"].value == 1 and  # 未命中缓存
                d["s2_exception_0"].value == 0 and  # 无异常
                d["s2_mmio_0"].value == 0 and  # 不是MMIO
                d["toMSHRArbiter_io_in_0_valid"].value == 1  # 仲裁器输入有效
            ),
            
            # CP 9.1.1: 请求未命中且无异常，需要发送到missUnit - 端口1（双行预取）
            "CP9_1_1_miss_no_exception_send_port1": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_doubleline"].value == 1 and  # 双行预取
                d["s2_miss_1"].value == 1 and  # 未命中缓存
                d["s2_exception_0"].value == 0 and  # 第一个请求无异常
                d["s2_exception_1"].value == 0 and  # 第二个请求无异常
                d["s2_mmio_0"].value == 0 and  # 不是MMIO
                d["s2_mmio_1"].value == 0 and
                d["toMSHRArbiter_io_in_1_valid"].value == 1  # 仲裁器输入有效
            ),
            
            # CP 9.1.2: 请求命中或有异常，不需要发送到missUnit - 端口0（SRAM命中）
            "CP9_1_2_sram_hit_no_send_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_waymasks_0"].value != 0 and  # SRAM命中
                d["s2_miss_0"].value == 0  # 不需要发送
            ),
            
            # CP 9.1.2: 请求命中或有异常，不需要发送到missUnit - 端口0（MSHR命中）
            "CP9_1_2_mshr_hit_no_send_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                (d["s2_MSHR_hits_valid"].value == 1 or d["s2_MSHR_match_0"].value == 1) and  # MSHR命中
                d["s2_miss_0"].value == 0  # 不需要发送
            ),
            
            # CP 9.1.2: 请求有异常，不需要发送到missUnit - 端口0
            "CP9_1_2_exception_no_send_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_exception_0"].value != 0 and  # 有异常
                d["s2_miss_0"].value == 0  # 不需要发送
            ),
            
            # CP 9.1.2: 请求访问MMIO，不需要发送到missUnit - 端口0
            "CP9_1_2_mmio_no_send_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_mmio_0"].value == 1 and  # 访问MMIO
                d["s2_miss_0"].value == 0  # 不需要发送
            ),
            
            # CP 9.1.3: 双行预取时，处理第二个请求的条件
            "CP9_1_3_doubleline_second_request": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_doubleline"].value == 1 and  # 双行预取
                # 如果第一个请求有异常或MMIO，第二个请求应该被取消
                ((d["s2_exception_0"].value != 0 or d["s2_mmio_0"].value == 1) and d["s2_miss_1"].value == 0) or
                # 如果第一个请求正常，第二个请求根据自身条件处理
                ((d["s2_exception_0"].value == 0 and d["s2_mmio_0"].value == 0) and 
                 (d["s2_miss_1"].value == 1 if (d["s2_exception_1"].value == 0 and d["s2_mmio_1"].value == 0) else d["s2_miss_1"].value == 0))
            ),
            
            # =========== CP 9.2: 避免发送重复请求，发送请求到missUnit ===========
            
            # CP 9.2.1: 在s1_real_fire时，复位has_send
            "CP9_2_1_s1_real_fire_reset_has_send": lambda d: (
                d["s1_real_fire"].value == 1  # 当新请求进入S2时，has_send应该被复位
            ),
            
            # CP 9.2.2: 当请求成功发送时，更新has_send - 端口0
            "CP9_2_2_request_sent_update_has_send_port0": lambda d: (
                d["toMSHRArbiter_io_in_0_ready"].value == 1 and 
                d["toMSHRArbiter_io_in_0_valid"].value == 1  # 端口0请求成功发送
            ),
            
            # CP 9.2.2: 当请求成功发送时，更新has_send - 端口1
            "CP9_2_2_request_sent_update_has_send_port1": lambda d: (
                d["toMSHRArbiter_io_in_1_ready"].value == 1 and 
                d["toMSHRArbiter_io_in_1_valid"].value == 1  # 端口1请求成功发送
            ),
            
            # CP 9.2.3: 避免重复发送请求 - 端口0
            "CP9_2_3_avoid_duplicate_send_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_miss_0"].value == 1 and  # 需要发送
                d["has_send_0"].value == 1 and  # 已经发送过
                d["toMSHRArbiter_io_in_0_valid"].value == 0  # 因此不再发送
            ),
            
            # CP 9.2.3: 避免重复发送请求 - 端口1
            "CP9_2_3_avoid_duplicate_send_port1": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_miss_1"].value == 1 and  # 需要发送
                d["has_send_1"].value == 1 and  # 已经发送过
                d["toMSHRArbiter_io_in_1_valid"].value == 0  # 因此不再发送
            ),
            
            # CP 9.2.4: 正确发送需要的请求到missUnit - 端口0
            "CP9_2_4_correct_send_to_missunit_port0": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_miss_0"].value == 1 and  # 需要发送
                d["has_send_0"].value == 0 and  # 尚未发送
                d["toMSHRArbiter_io_in_0_valid"].value == 1  # 请求有效
            ),
            
            # CP 9.2.4: 正确发送需要的请求到missUnit - 端口1  
            "CP9_2_4_correct_send_to_missunit_port1": lambda d: (
                d["s2_valid"].value == 1 and 
                d["s2_miss_1"].value == 1 and  # 需要发送
                d["has_send_1"].value == 0 and  # 尚未发送
                d["toMSHRArbiter_io_in_1_valid"].value == 1  # 请求有效
            ),
            
            # CP 9.2.5: 仲裁器正确仲裁多个请求 - 只有一个端口被选中发送
            "CP9_2_5_arbiter_correct_arbitration": lambda d: (
                d["s2_valid"].value == 1 and 
                d["mshr_req_valid"].value == 1 and  # 输出到MSHR的请求有效
                # 检查不会同时发送两个请求（仲裁器应该选择一个）
                not (d["toMSHRArbiter_io_in_0_ready"].value == 1 and 
                     d["toMSHRArbiter_io_in_0_valid"].value == 1 and
                     d["toMSHRArbiter_io_in_1_ready"].value == 1 and 
                     d["toMSHRArbiter_io_in_1_valid"].value == 1)
            ),
        },
        name="CP9_Send_Request_To_MissUnit"
    )
    
    # =================================================================
    # CP 10: 刷新机制覆盖点
    # 监控目标：全局刷新信号、来自BPU的刷新信号、状态机复位、ITLB管道同步刷新
    # =================================================================
    g.add_watch_point(
        {
            # 刷新信号输入
            "global_flush": bundle.io._flush,
            "bpu_s2_valid": bundle.io._flushFromBpu._s2._valid,
            "bpu_s2_bits_flag": bundle.io._flushFromBpu._s2._bits._flag,
            "bpu_s2_bits_value": bundle.io._flushFromBpu._s2._bits._value,
            "bpu_s3_valid": bundle.io._flushFromBpu._s3._valid,
            "bpu_s3_bits_flag": bundle.io._flushFromBpu._s3._bits._flag,
            "bpu_s3_bits_value": bundle.io._flushFromBpu._s3._bits._value,
            "req_ftq_flag": bundle.io._req._bits._ftqIdx._flag,
            "req_ftq_value": bundle.io._req._bits._ftqIdx._value,
            
            # 内部刷新信号（使用bundle中的信号）
            "s1_flush": bundle.IPrefetchPipe._s1._flush,
            "req_is_soft_prefetch": bundle.io._req._bits._isSoftPrefetch,
            "s1_is_soft_prefetch": bundle.IPrefetchPipe._s1._isSoftPrefetch,
            
            # BPU刷新探测信号（内部信号）
            "from_bpu_s0_flush_probe": dut.GetInternalSignal(IPrefetchPipe_dict["from_bpu_s0_flush_probe"], use_vpi=False),
            "from_bpu_s1_flush_probe": dut.GetInternalSignal(IPrefetchPipe_dict["from_bpu_s1_flush_probe"], use_vpi=False),
            
            # 流水线控制信号
            "s0_fire": dut.GetInternalSignal(IPrefetchPipe_dict["s0_fire"], use_vpi=False),
            "s1_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s1_valid"], use_vpi=False),
            "s2_valid": dut.GetInternalSignal(IPrefetchPipe_dict["s2_valid"], use_vpi=False),
            "state": dut.GetInternalSignal(IPrefetchPipe_dict["state"], use_vpi=False),
            "itlb_flush_pipe": bundle.io._itlbFlushPipe,
        },
        bins={
            # CP 10.1: 发生全局刷新 - io.flush为高，s0_flush、s1_flush、s2_flush分别为高，所有阶段的请求被正确清除
            "CP10_1_global_flush": lambda d: (
                d["global_flush"].value == 1 and
                d["s1_flush"].value == 1 and
                d["s0_fire"].value == 0 and  # s0阶段被抑制
                d["s1_valid"].value == 0 and  # s1阶段被清除
                d["s2_valid"].value == 0  # s2阶段被清除
            ),
            
            # CP 10.2: 来自BPU的刷新 - io.flushFromBpu.shouldFlushByStageX为真且请求不是软件预取，对应阶段的刷新信号为高
            "CP10_2_bpu_s0_flush": lambda d: (
                d["req_is_soft_prefetch"].value == 0 and 
                d["from_bpu_s0_flush_probe"].value == 1 and
                (d["bpu_s2_valid"].value == 1 or d["bpu_s3_valid"].value == 1)
            ),
            
            "CP10_2_bpu_s1_flush": lambda d: (
                d["s1_is_soft_prefetch"].value == 0 and 
                d["from_bpu_s1_flush_probe"].value == 1 and
                d["bpu_s3_valid"].value == 1
            ),
            
            # CP 10.3: 刷新时状态机复位 - s1_flush为高，状态机state被重置为m_idle状态
            "CP10_3_flush_state_reset": lambda d: (
                d["s1_flush"].value == 1 and 
                d["state"].value == 0  # m_idle = 0
            ),
            
            # CP 10.4: ITLB管道同步刷新 - s1_flush为高，io.itlbFlushPipe为高，ITLB被同步刷新
            "CP10_4_itlb_pipe_flush": lambda d: (
                d["s1_flush"].value == 1 and 
                d["itlb_flush_pipe"].value == 1
            ),
        },
        name="CP10_Flush_Mechanism"
    )
    
    return g


def create_iprefetchpipe_coverage_groups(bundle, dut):
    """
    创建IPrefetchPipe模块的所有功能覆盖点组合
    
    Args:
        bundle: IPrefetchPipeBundle对象
        dut: DUT对象用于访问内部信号
        
    Returns:
        list: 包含所有覆盖点组的列表
    """
    iprefetchpipe_coverage = define_iprefetchpipe_coverage(bundle, dut)
    
    return [iprefetchpipe_coverage]