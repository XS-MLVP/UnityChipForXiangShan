from toffee.funcov import CovGroup


def define_mainpipe_coverage(bundle, dut):
    """
    Defines comprehensive functional coverage for MainPipe module based on MainPipe.md.
    Covers verification points CP11-CP22 as documented.
    
    Args:
        bundle: The top-level MainPipeBundle object.
        dut: The DUT object for accessing internal signals.
    """
    g = CovGroup("MainPipe_Coverage")
    
    # Create MainPipe internal signals dictionary for coverage
    MainPipe_dict = {
        # Pipeline stage control signals
        "s1_fire": "ICacheMainPipe_top.ICacheMainPipe.s1_fire",
        "s1_valid": "ICacheMainPipe_top.ICacheMainPipe.s1_valid",
        
        # S1 stage signals
        "s1_hits_0": "ICacheMainPipe_top.ICacheMainPipe.s1_hits_REG",
        "s1_hits_1": "ICacheMainPipe_top.ICacheMainPipe.s1_hits_REG_1",
        "s1_hits_valid_0": "ICacheMainPipe_top.ICacheMainPipe.s1_hits_valid",
        "s1_hits_valid_1": "ICacheMainPipe_top.ICacheMainPipe.s1_hits_valid_1",
        "s1_SRAMhits_0": "ICacheMainPipe_top.ICacheMainPipe.s1_SRAMhits_0",
        "s1_SRAMhits_1": "ICacheMainPipe_top.ICacheMainPipe.s1_SRAMhits_1",
        "s1_MSHR_hits_1": "ICacheMainPipe_top.ICacheMainPipe.s1_MSHR_hits_1",
        "s1_meta_corrupt_hit_num_0": "ICacheMainPipe_top.ICacheMainPipe.s1_meta_corrupt_hit_num",
        "s1_meta_corrupt_hit_num_1": "ICacheMainPipe_top.ICacheMainPipe.s1_meta_corrupt_hit_num_1",
        
        # S1 MSHR bank hit signals
        "s1_bankMSHRHit_0": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_0",
        "s1_bankMSHRHit_1": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_1",
        "s1_bankMSHRHit_2": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_2",
        "s1_bankMSHRHit_3": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_3",
        "s1_bankMSHRHit_4": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_4",
        "s1_bankMSHRHit_5": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_5",
        "s1_bankMSHRHit_6": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_6",
        "s1_bankMSHRHit_7": "ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_7",
        
        # S2 meta corrupt signals
        "s2_meta_corrupt_0": "ICacheMainPipe_top.ICacheMainPipe.s2_meta_corrupt_0",
        "s2_meta_corrupt_1": "ICacheMainPipe_top.ICacheMainPipe.s2_meta_corrupt_1",
        
        # S2 exception signals (actual exception merge results)
        "s2_exception_0": "ICacheMainPipe_top.ICacheMainPipe.s2_exception_0",
        "s2_exception_1": "ICacheMainPipe_top.ICacheMainPipe.s2_exception_1",
        
        # S1 data from MSHR signals
        "s1_data_is_from_MSHR_0": "ICacheMainPipe_top.ICacheMainPipe.s1_data_is_from_MSHR_REG",
        "s1_data_is_from_MSHR_1": "ICacheMainPipe_top.ICacheMainPipe.s1_data_is_from_MSHR_REG_1",
        "s1_data_is_from_MSHR_2": "ICacheMainPipe_top.ICacheMainPipe.s1_data_is_from_MSHR_REG_2",
        "s1_data_is_from_MSHR_3": "ICacheMainPipe_top.ICacheMainPipe.s1_data_is_from_MSHR_REG_3",
        
        # S2 stage corrupt signals
        "s2_bank_corrupt_0": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_0",
        "s2_bank_corrupt_1": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_1",
        "s2_bank_corrupt_2": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_2",
        "s2_bank_corrupt_3": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_3",
        "s2_bank_corrupt_4": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_4",
        "s2_bank_corrupt_5": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_5",
        "s2_bank_corrupt_6": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_6",
        "s2_bank_corrupt_7": "ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_7",
        
        # S2 data corrupt signals
        "s2_data_corrupt_0": "ICacheMainPipe_top.ICacheMainPipe.s2_data_corrupt_0",
        "s2_data_corrupt_1": "ICacheMainPipe_top.ICacheMainPipe.s2_data_corrupt_1",
        
        # S2 data should fetch signals (miss detection)
        "s2_should_fetch_0": "ICacheMainPipe_top.ICacheMainPipe.s2_should_fetch_0",
        "s2_should_fetch_1": "ICacheMainPipe_top.ICacheMainPipe.s2_should_fetch_1",
        
        # S2 has send signals (duplicate request prevention)
        "s2_has_send_0": "ICacheMainPipe_top.ICacheMainPipe.s2_has_send_0",
        "s2_has_send_1": "ICacheMainPipe_top.ICacheMainPipe.s2_has_send_1",
        
        # S2 L2 corrupt signals
        "s2_l2_corrupt_0": "ICacheMainPipe_top.ICacheMainPipe.s2_l2_corrupt_0",
        "s2_l2_corrupt_1": "ICacheMainPipe_top.ICacheMainPipe.s2_l2_corrupt_1",
        
        # S2 MSHR match signals (关键bug验证需要)
        "s2_bankMSHRHit_0": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_0",
        "s2_bankMSHRHit_1": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_1",
        "s2_bankMSHRHit_2": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_2",
        "s2_bankMSHRHit_3": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_3",
        "s2_bankMSHRHit_4": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_4",
        "s2_bankMSHRHit_5": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_5",
        "s2_bankMSHRHit_6": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_6",
        "s2_bankMSHRHit_7": "ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_7",
        "s2_MSHR_hits_1": "ICacheMainPipe_top.ICacheMainPipe.s2_MSHR_hits_1",
        
        # S2 data from MSHR signals
        "s2_data_is_from_MSHR_0": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_0",
        "s2_data_is_from_MSHR_1": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_1",
        "s2_data_is_from_MSHR_2": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_2",
        "s2_data_is_from_MSHR_3": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_3",
        "s2_data_is_from_MSHR_4": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_4",
        "s2_data_is_from_MSHR_5": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_5",
        "s2_data_is_from_MSHR_6": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_6",
        "s2_data_is_from_MSHR_7": "ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_7",
        
        # S2 stage control signals 
        "s2_valid": "ICacheMainPipe_top.ICacheMainPipe.s2_valid",
        "s2_hits_0": "ICacheMainPipe_top.ICacheMainPipe.s2_hits_0",
        "s2_hits_1": "ICacheMainPipe_top.ICacheMainPipe.s2_hits_1",
        "s2_SRAMhits_0": "ICacheMainPipe_top.ICacheMainPipe.s2_SRAMhits_0",
        "s2_SRAMhits_1": "ICacheMainPipe_top.ICacheMainPipe.s2_SRAMhits_1",
        
        # S2 corrupt refetch signals
        "s2_corrupt_refetch_0": "ICacheMainPipe_top.ICacheMainPipe.s2_corrupt_refetch_0",
        "s2_corrupt_refetch_1": "ICacheMainPipe_top.ICacheMainPipe.s2_corrupt_refetch_1",
        
        # S2 MMIO signals
        "s2_mmio_0": "ICacheMainPipe_top.ICacheMainPipe.s2_mmio_0",
        
        # S2 doubleline signal
        "s2_doubleline": "ICacheMainPipe_top.ICacheMainPipe.s2_doubleline",
        # S2 reg signal
        "s2_req_vaddr_0": "ICacheMainPipe_top.ICacheMainPipe.s2_req_vaddr_0",
        "s2_req_vaddr_1": "ICacheMainPipe_top.ICacheMainPipe.s2_req_vaddr_1",
        "s2_req_ptags_0": "ICacheMainPipe_top.ICacheMainPipe.s2_req_ptags_0",
        "s2_req_ptags_1": "ICacheMainPipe_top.ICacheMainPipe.s2_req_ptags_1",
        "s2_doubleline": "ICacheMainPipe_top.ICacheMainPipe.s2_doubleline",
        # Backend exception
        "s1_backendException": "ICacheMainPipe_top.ICacheMainPipe.s1_backendException",
    }
    
    # =================================================================
    # CP 11: 访问 DataArray 的单路
    # =================================================================
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "fetch_req_valid": bundle.io._fetch._req._valid,
            "wayLookupRead_valid": bundle.io._wayLookupRead._valid,
            "wayLookupRead_ready": bundle.io._wayLookupRead._ready,
            # S0阶段命中检查信号
            "wayLookupRead_waymask_0": bundle.io._wayLookupRead._bits._entry._waymask._0,
            "wayLookupRead_waymask_1": bundle.io._wayLookupRead._bits._entry._waymask._1,
            "wayLookupRead_itlb_exception_0": bundle.io._wayLookupRead._bits._entry._itlb._exception._0,
            "wayLookupRead_itlb_exception_1": bundle.io._wayLookupRead._bits._entry._itlb._exception._1,
            # DataArray访问信号
            "dataArray_toIData_0_valid": bundle.io._dataArray._toIData._0._valid,
            "dataArray_toIData_1_valid": bundle.io._dataArray._toIData._1._valid,
            "dataArray_toIData_2_valid": bundle.io._dataArray._toIData._2._valid,
            "dataArray_toIData_3_valid": bundle.io._dataArray._toIData._3._valid,
            "dataArray_toIData_3_ready": bundle.io._dataArray._toIData._3._ready,
            # S0阶段fire控制
            "s1_fire": dut.GetInternalSignal(MainPipe_dict["s1_fire"], use_vpi=False),
        },
        bins={
            # 11.1: S0阶段正常访问DataArray（有命中且无ITLB异常且DataArray可用）
            "CP11.1_s0_access_dataarray": lambda d: d["fetch_req_valid"].value == 1 and \
                                                   d["wayLookupRead_valid"].value == 1 and \
                                                   d["dataArray_toIData_3_ready"].value == 1 and \
                                                   (d["wayLookupRead_waymask_0"].value != 0 or d["wayLookupRead_waymask_1"].value != 0) and \
                                                   d["wayLookupRead_itlb_exception_0"].value == 0 and \
                                                   d["wayLookupRead_itlb_exception_1"].value == 0 and \
                                                   d["flush"].value == 0,
            
            # 11.2: Way未命中但仍会访问DataArray（返回无效数据）
            "CP11.2_way_miss_still_access": lambda d: d["fetch_req_valid"].value == 1 and \
                                                     d["wayLookupRead_valid"].value == 1 and \
                                                     d["dataArray_toIData_3_ready"].value == 1 and \
                                                     d["wayLookupRead_waymask_0"].value == 0 and \
                                                     d["wayLookupRead_waymask_1"].value == 0 and \
                                                     d["flush"].value == 0,
            
            # 11.3: ITLB查询失败但仍会访问DataArray（返回无效数据）
            "CP11.3_itlb_fail_still_access": lambda d: d["fetch_req_valid"].value == 1 and \
                                                       d["wayLookupRead_valid"].value == 1 and \
                                                       d["dataArray_toIData_3_ready"].value == 1 and \
                                                       (d["wayLookupRead_itlb_exception_0"].value != 0 or \
                                                        d["wayLookupRead_itlb_exception_1"].value != 0) and \
                                                       d["flush"].value == 0,
            
            # 11.4: DataArray写忙，无法访问
            "CP11.4_dataarray_write_busy": lambda d: d["fetch_req_valid"].value == 1 and \
                                                    d["wayLookupRead_valid"].value == 1 and \
                                                    d["dataArray_toIData_3_ready"].value == 0 and \
                                                    d["flush"].value == 0,
            
            # 11.5: Flush状态下停止访问
            "CP11.5_flush_blocks_access": lambda d: d["flush"].value == 1,
        },
        name="CP11_DataArray_Access"
    )
    
    # =================================================================
    # CP 12: Meta ECC 校验
    # =================================================================
    g.add_watch_point(
        {
            "ecc_enable": bundle.io._ecc_enable,
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
            "errors_0_report_to_beu": bundle.io._errors._0._bits._report_to_beu,
            "errors_1_report_to_beu": bundle.io._errors._1._bits._report_to_beu,
            # S2 meta corrupt signals
            "s2_meta_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_meta_corrupt_0"], use_vpi=False),
            "s2_meta_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_meta_corrupt_1"], use_vpi=False),
            # S1 meta corrupt hit num for analyzing hit counts
            "s1_meta_corrupt_hit_num_0": dut.GetInternalSignal(MainPipe_dict["s1_meta_corrupt_hit_num_0"], use_vpi=False),
            "s1_meta_corrupt_hit_num_1": dut.GetInternalSignal(MainPipe_dict["s1_meta_corrupt_hit_num_1"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
        },
        bins={
            # 12.1: 无ECC错误（ECC使能且无meta corrupt）
            "CP12.1_no_ecc_error": lambda d: d["ecc_enable"].value == 1 and \
                                            d["s2_meta_corrupt_0"].value == 0 and \
                                            d["s2_meta_corrupt_1"].value == 0 and \
                                            d["s2_fire"].value == 1,
            
            # 12.2: 单路命中的ECC错误（通道0，命中数==1且meta corrupt）
            "CP12.2_single_way_ecc_error_0": lambda d: d["ecc_enable"].value == 1 and \
                                                      d["s2_meta_corrupt_0"].value == 1 and \
                                                      d["s1_meta_corrupt_hit_num_0"].value == 1 and \
                                                      d["errors_0_valid"].value == 1 and \
                                                      d["errors_0_report_to_beu"].value == 1,
            
            # 12.3: 多路命中（通道0，命中数>=2且meta corrupt）
            "CP12.3_multi_way_hit_0": lambda d: d["ecc_enable"].value == 1 and \
                                               d["s2_meta_corrupt_0"].value == 1 and \
                                               d["s1_meta_corrupt_hit_num_0"].value >= 2 and \
                                               d["errors_0_valid"].value == 1 and \
                                               d["errors_0_report_to_beu"].value == 1,
            
            # 12.4: 单路命中的ECC错误（通道1，命中数==1且meta corrupt）
            "CP12.4_single_way_ecc_error_1": lambda d: d["ecc_enable"].value == 1 and \
                                                      d["s2_meta_corrupt_1"].value == 1 and \
                                                      d["s1_meta_corrupt_hit_num_1"].value == 1 and \
                                                      d["errors_1_valid"].value == 1 and \
                                                      d["errors_1_report_to_beu"].value == 1,

            # 12.5: ECC功能关闭（meta corrupt始终为0）
            "CP12.6_ecc_disabled": lambda d: d["ecc_enable"].value == 0 and \
                                            d["s2_meta_corrupt_0"].value == 0 and \
                                            d["s2_meta_corrupt_1"].value == 0,
        },
        name="CP12_Meta_ECC_Check"
    )
    
    # =================================================================
    # CP 13: PMP 检查
    # 监控目标：物理内存保护检查和MMIO区域检测
    # =================================================================
    g.add_watch_point(
        {
            "pmp_0_resp_instr": bundle.io._pmp._0._resp._instr,
            "pmp_0_resp_mmio": bundle.io._pmp._0._resp._mmio,
            "pmp_1_resp_instr": bundle.io._pmp._1._resp._instr,
            "pmp_1_resp_mmio": bundle.io._pmp._1._resp._mmio,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
            "fetch_resp_pmp_mmio_0": bundle.io._fetch._resp._bits._pmp_mmio._0,
            "fetch_resp_pmp_mmio_1": bundle.io._fetch._resp._bits._pmp_mmio._1,
        },
        bins={
            # 13.1: 没有PMP异常（两个通道都有指令访问权限且最终无异常输出）
            "CP13.1_no_pmp_exception": lambda d: d["pmp_0_resp_instr"].value == 0 and \
                                                d["pmp_1_resp_instr"].value == 0 and \
                                                d["fetch_resp_exception_0"].value == 0 and \
                                                d["fetch_resp_exception_1"].value == 0 and \
                                                d["fetch_resp_valid"].value == 1,
            
            # 13.2: 通道0有PMP异常（PMP响应异常且最终有异常输出）
            "CP13.2_channel0_pmp_exception": lambda d: d["pmp_0_resp_instr"].value == 1 and \
                                                      d["fetch_resp_exception_0"].value != 0 and \
                                                      d["fetch_resp_valid"].value == 1,
            
            # 13.3: 通道1有PMP异常（PMP响应异常且最终有异常输出）
            "CP13.3_channel1_pmp_exception": lambda d: d["pmp_1_resp_instr"].value == 1 and \
                                                      d["fetch_resp_exception_1"].value != 0 and \
                                                      d["fetch_resp_valid"].value == 1,
            
            # 13.4: 两个通道都有PMP异常
            "CP13.4_both_channels_pmp_exception": lambda d: d["pmp_0_resp_instr"].value == 1 and \
                                                           d["pmp_1_resp_instr"].value == 1 and \
                                                           d["fetch_resp_exception_0"].value != 0 and \
                                                           d["fetch_resp_exception_1"].value != 0 and \
                                                           d["fetch_resp_valid"].value == 1,
            
            # 13.5: 没有映射到MMIO区域
            "CP13.5_no_mmio_mapping": lambda d: d["pmp_0_resp_mmio"].value == 0 and \
                                               d["pmp_1_resp_mmio"].value == 0 and \
                                               d["fetch_resp_valid"].value == 1,
            
            # 13.6: 通道0映射到MMIO区域
            "CP13.6_channel0_mmio": lambda d: d["pmp_0_resp_mmio"].value == 1 and \
                                             d["fetch_resp_pmp_mmio_0"].value == 1,
            
            # 13.7: 通道1映射到MMIO区域
            "CP13.7_channel1_mmio": lambda d: d["pmp_1_resp_mmio"].value == 1 and \
                                             d["fetch_resp_pmp_mmio_1"].value == 1,
            
            # 13.8: 两个通道都映射到MMIO区域
            "CP13.8_both_channels_mmio": lambda d: d["pmp_0_resp_mmio"].value == 1 and \
                                                  d["pmp_1_resp_mmio"].value == 1 and \
                                                  d["fetch_resp_pmp_mmio_0"].value == 1 and \
                                                  d["fetch_resp_pmp_mmio_1"].value == 1,
        },
        name="CP13_PMP_Check"
    )
    
    # =================================================================
    # CP 14: 异常合并
    # 监控目标：ITLB和PMP异常合并
    # =================================================================
    g.add_watch_point(
        {
            "wayLookupRead_entry_itlb_exception_0": bundle.io._wayLookupRead._bits._entry._itlb._exception._0,
            "wayLookupRead_entry_itlb_exception_1": bundle.io._wayLookupRead._bits._entry._itlb._exception._1,
            "pmp_0_resp_instr": bundle.io._pmp._0._resp._instr,
            "pmp_1_resp_instr": bundle.io._pmp._1._resp._instr,
            # S2阶段实际的异常合并结果
            "s2_exception_0": dut.GetInternalSignal(MainPipe_dict["s2_exception_0"], use_vpi=False),
            "s2_exception_1": dut.GetInternalSignal(MainPipe_dict["s2_exception_1"], use_vpi=False),
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
        },
        bins={
            # 14.1: 没有异常（s1_exception_out为全零）
            # 实际：无ITLB异常，有PMP权限，S2异常合并结果为全零
            "CP14.1_no_exception": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value == 0 and \
                                            d["wayLookupRead_entry_itlb_exception_1"].value == 0 and \
                                            d["pmp_0_resp_instr"].value == 0 and \
                                            d["pmp_1_resp_instr"].value == 0 and \
                                            d["s2_exception_0"].value == 0 and \
                                            d["s2_exception_1"].value == 0 and \
                                            d["fetch_resp_valid"].value == 1,
            
            # 14.2: 只有ITLB异常（s1_exception_out和s1_itlb_exception一致）
            # 实际：有ITLB异常，S2异常合并结果等于ITLB异常
            "CP14.2_only_itlb_exception": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value != 0 and \
                                                   d["pmp_0_resp_instr"].value == 1 and \
                                                   d["s2_exception_0"].value == d["wayLookupRead_entry_itlb_exception_0"].value and \
                                                   d["fetch_resp_valid"].value == 1,
            
            # 14.3: 只有PMP异常（s1_exception_out和s1_pmp_exception一致）
            # 实际：无ITLB异常，有PMP异常，S2异常合并结果反映PMP状态
            "CP14.3_only_pmp_exception": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value == 0 and \
                                                  d["pmp_0_resp_instr"].value == 0 and \
                                                  d["s2_exception_0"].value != 0 and \
                                                  d["fetch_resp_valid"].value == 1,
            
            # 14.4: ITLB与PMP异常同时出现（ITLB优先）
            # 实际：有ITLB异常和PMP异常，S2异常合并结果等于ITLB异常（优先级体现）
            "CP14.4_itlb_pmp_both_itlb_priority": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value != 0 and \
                                                           d["pmp_0_resp_instr"].value == 0 and \
                                                           d["s2_exception_0"].value == d["wayLookupRead_entry_itlb_exception_0"].value and \
                                                           d["fetch_resp_valid"].value == 1,
        },
        name="CP14_Exception_Merge"
    )
    
    # =================================================================
    # CP 15: MSHR 匹配和数据选择
    # =================================================================
    g.add_watch_point(
        {
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            "mshr_resp_corrupt": bundle.io._mshr._resp._bits._corrupt,
            # S1阶段MSHR匹配信号
            "s1_bankMSHRHit_7": dut.GetInternalSignal(MainPipe_dict["s1_bankMSHRHit_7"], use_vpi=False),
            "s1_MSHR_hits_1": dut.GetInternalSignal(MainPipe_dict["s1_MSHR_hits_1"], use_vpi=False),
            "s1_data_is_from_MSHR_0": dut.GetInternalSignal(MainPipe_dict["s1_data_is_from_MSHR_0"], use_vpi=False),
            "s1_data_is_from_MSHR_1": dut.GetInternalSignal(MainPipe_dict["s1_data_is_from_MSHR_1"], use_vpi=False),
            "s1_bankMSHRHit_0": dut.GetInternalSignal(MainPipe_dict["s1_bankMSHRHit_0"], use_vpi=False),
            # 阶段控制信号
            "s1_fire": dut.GetInternalSignal(MainPipe_dict["s1_fire"], use_vpi=False),
        },
        bins={
            # 15.1: 命中MSHR - MSHR中已有正确数据时，S1阶段能直接拿到
            "CP15.1_mshr_hit": lambda d: d["s1_fire"].value == 1 and \
                                        d["mshr_resp_valid"].value == 1 and \
                                        d["mshr_resp_corrupt"].value == 0 and \
                                        (d["s1_bankMSHRHit_7"].value == 1 or d["s1_MSHR_hits_1"].value == 1) and \
                                        (d["s1_data_is_from_MSHR_0"].value == 1 or d["s1_data_is_from_MSHR_1"].value == 1),
            
            # 15.2: 未命中MSHR - MSHR中存放的地址与当前请求不同，读取SRAM数据
            "CP15.2_mshr_miss": lambda d: d["s1_fire"].value == 1 and \
                                         d["s1_bankMSHRHit_7"].value == 0 and \
                                         d["s1_MSHR_hits_1"].value == 0 and \
                                         d["s1_data_is_from_MSHR_0"].value == 0 and \
                                         d["s1_data_is_from_MSHR_1"].value == 0,
            
            # 15.3: MSHR数据corrupt - corrupt=true时MSHR不匹配，读取SRAM数据
            "CP15.3_mshr_corrupt": lambda d: d["s1_fire"].value == 1 and \
                                            d["mshr_resp_valid"].value == 1 and \
                                            d["mshr_resp_corrupt"].value == 1 and \
                                            d["s1_bankMSHRHit_7"].value == 0 and \
                                            d["s1_MSHR_hits_1"].value == 0 and \
                                            d["s1_data_is_from_MSHR_0"].value == 0,
        },
        name="CP15_MSHR_Match_Data_Select"
    )
    
    # =================================================================
    # CP 16: Data ECC 校验
    # =================================================================
    g.add_watch_point(
        {
            "ecc_enable": bundle.io._ecc_enable,
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
            "errors_0_report_to_beu": bundle.io._errors._0._bits._report_to_beu,
            "errors_1_report_to_beu": bundle.io._errors._1._bits._report_to_beu,
            # Internal S2 bank corrupt signals (all 8 banks)
            "s2_bank_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_0"], use_vpi=False),
            "s2_bank_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_1"], use_vpi=False),
            "s2_bank_corrupt_2": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_2"], use_vpi=False),
            "s2_bank_corrupt_3": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_3"], use_vpi=False),
            "s2_bank_corrupt_4": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_4"], use_vpi=False),
            "s2_bank_corrupt_5": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_5"], use_vpi=False),
            "s2_bank_corrupt_6": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_6"], use_vpi=False),
            "s2_bank_corrupt_7": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_7"], use_vpi=False),
            # Internal S2 data corrupt signals
            "s2_data_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_data_corrupt_0"], use_vpi=False),
            "s2_data_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_data_corrupt_1"], use_vpi=False),
            # Data from MSHR flags
            "s2_data_is_from_MSHR_0": dut.GetInternalSignal(MainPipe_dict["s2_data_is_from_MSHR_0"], use_vpi=False),
            "s2_data_is_from_MSHR_1": dut.GetInternalSignal(MainPipe_dict["s2_data_is_from_MSHR_1"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire
        },
        bins={
            # 16.1: 无ECC错误 - s2_data_corrupt(i)为false，没有ECC错误
            "CP16.1_no_ecc_error": lambda d: d["s2_fire"].value == 1 and \
                                             d["ecc_enable"].value == 1 and \
                                             d["s2_data_corrupt_0"].value == 0 and \
                                             d["s2_data_corrupt_1"].value == 0,
            
            # 16.2: 单Bank ECC错误 - 修复：删除不存在的source.data检查，基于实际Verilog实现
            # 当s2_data_corrupt为true且数据不来自MSHR时，通过s2_corrupt_refetch触发错误报告
            "CP16.2_single_bank_ecc_error_port0": lambda d: d["s2_fire"].value == 1 and \
                                                            d["ecc_enable"].value == 1 and \
                                                            d["s2_data_corrupt_0"].value == 1 and \
                                                            d["s2_data_is_from_MSHR_0"].value == 0 and \
                                                            d["errors_0_valid"].value == 1 and \
                                                            d["errors_0_report_to_beu"].value == 1,
            
            "CP16.2_single_bank_ecc_error_port1": lambda d: d["s2_fire"].value == 1 and \
                                                            d["ecc_enable"].value == 1 and \
                                                            d["s2_data_corrupt_1"].value == 1 and \
                                                            d["s2_data_is_from_MSHR_1"].value == 0 and \
                                                            d["errors_1_valid"].value == 1 and \
                                                            d["errors_1_report_to_beu"].value == 1,
            
            # 16.3: 多Bank ECC错误
            # 检查多个bank corrupt且对应端口有data corrupt和错误报告
            "CP16.3_multi_bank_ecc_error_port0": lambda d: d["s2_fire"].value == 1 and \
                                                          d["ecc_enable"].value == 1 and \
                                                          sum([d[f"s2_bank_corrupt_{i}"].value for i in range(8)]) >= 2 and \
                                                          d["s2_data_corrupt_0"].value == 1 and \
                                                          d["s2_data_is_from_MSHR_0"].value == 0 and \
                                                          d["errors_0_valid"].value == 1 and \
                                                          d["errors_0_report_to_beu"].value == 1,
            
            "CP16.3_multi_bank_ecc_error_port1": lambda d: d["s2_fire"].value == 1 and \
                                                          d["ecc_enable"].value == 1 and \
                                                          sum([d[f"s2_bank_corrupt_{i}"].value for i in range(8)]) >= 2 and \
                                                          d["s2_data_corrupt_1"].value == 1 and \
                                                          d["s2_data_is_from_MSHR_1"].value == 0 and \
                                                          d["errors_1_valid"].value == 1 and \
                                                          d["errors_1_report_to_beu"].value == 1,
            
            # 16.4: ECC功能关闭 - 当ecc_enable为低时，强制清除s2_data_corrupt信号
            "CP16.4_data_ecc_disabled": lambda d: d["ecc_enable"].value == 0 and \
                                                  d["s2_data_corrupt_0"].value == 0 and \
                                                  d["s2_data_corrupt_1"].value == 0,
        },
        name="CP16_Data_ECC_Check"
    )
    
    # =================================================================
    # CP 17: 冲刷 MetaArray
    # =================================================================
    g.add_watch_point(
        {
            "ecc_enable": bundle.io._ecc_enable,
            "metaArrayFlush_0_valid": bundle.io._metaArrayFlush._0._valid,
            "metaArrayFlush_1_valid": bundle.io._metaArrayFlush._1._valid,
            "metaArrayFlush_0_waymask": bundle.io._metaArrayFlush._0._bits._waymask,
            "metaArrayFlush_1_waymask": bundle.io._metaArrayFlush._1._bits._waymask,
            # 内部corrupt信号 - 用于精确区分Meta和Data错误
            "s2_meta_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_meta_corrupt_0"], use_vpi=False),
            "s2_meta_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_meta_corrupt_1"], use_vpi=False),
            "s2_data_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_data_corrupt_0"], use_vpi=False),
            "s2_data_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_data_corrupt_1"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
        },
        bins={
            # 17.1: 只有Meta ECC校验错误 - 当s2_meta_corrupt为真时，MetaArray的所有路都会被冲刷
            # toMetaFlush(i).valid为真，toMetaFlush(i).bits.waymask对应端口的所有路置位
            "CP17.1_meta_ecc_error_port0": lambda d: d["ecc_enable"].value == 1 and \
                                                    d["s2_meta_corrupt_0"].value == 1 and \
                                                    d["s2_data_corrupt_0"].value == 0 and \
                                                    d["metaArrayFlush_0_valid"].value == 1 and \
                                                    d["metaArrayFlush_0_waymask"].value == 0xF,
            
            "CP17.1_meta_ecc_error_port1": lambda d: d["ecc_enable"].value == 1 and \
                                                    d["s2_meta_corrupt_1"].value == 1 and \
                                                    d["s2_data_corrupt_1"].value == 0 and \
                                                    d["metaArrayFlush_1_valid"].value == 1 and \
                                                    d["metaArrayFlush_1_waymask"].value == 0xF,
            
            # 17.2: 只有Data ECC校验错误 - 当s2_data_corrupt为真时，只有对应路会被冲刷
            # toMetaFlush(i).valid为真，toMetaFlush(i).bits.waymask对应端口的对应路置位
            "CP17.2_data_ecc_error_port0": lambda d: d["ecc_enable"].value == 1 and \
                                                    d["s2_meta_corrupt_0"].value == 0 and \
                                                    d["s2_data_corrupt_0"].value == 1 and \
                                                    d["metaArrayFlush_0_valid"].value == 1 and \
                                                    d["metaArrayFlush_0_waymask"].value != 0xF and \
                                                    d["metaArrayFlush_0_waymask"].value != 0x0,
            
            "CP17.2_data_ecc_error_port1": lambda d: d["ecc_enable"].value == 1 and \
                                                    d["s2_meta_corrupt_1"].value == 0 and \
                                                    d["s2_data_corrupt_1"].value == 1 and \
                                                    d["metaArrayFlush_1_valid"].value == 1 and \
                                                    d["metaArrayFlush_1_waymask"].value != 0xF and \
                                                    d["metaArrayFlush_1_waymask"].value != 0x0,
            
            # 17.3: 同时有Meta ECC校验错误和Data ECC校验错误 - 处理Meta ECC的优先级更高，将MetaArray的所有路冲刷
            # toMetaFlush(i).valid为真，toMetaFlush(i).bits.waymask对应端口的所有路置位
            "CP17.3_both_errors_meta_priority_port0": lambda d: d["ecc_enable"].value == 1 and \
                                                              d["s2_meta_corrupt_0"].value == 1 and \
                                                              d["s2_data_corrupt_0"].value == 1 and \
                                                              d["metaArrayFlush_0_valid"].value == 1 and \
                                                              d["metaArrayFlush_0_waymask"].value == 0xF,
            
            "CP17.3_both_errors_meta_priority_port1": lambda d: d["ecc_enable"].value == 1 and \
                                                              d["s2_meta_corrupt_1"].value == 1 and \
                                                              d["s2_data_corrupt_1"].value == 1 and \
                                                              d["metaArrayFlush_1_valid"].value == 1 and \
                                                              d["metaArrayFlush_1_waymask"].value == 0xF,
        },
        name="CP17_MetaArray_Flush"
    )
    
    # =================================================================
    # CP 18: 监控 MSHR 匹配与数据更新
    # =================================================================
    g.add_watch_point(
        {
            # MSHR响应信号
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            "mshr_resp_corrupt": bundle.io._mshr._resp._bits._corrupt,
            "mshr_resp_vSetIdx": bundle.io._mshr._resp._bits._vSetIdx,
            "mshr_resp_blkPaddr": bundle.io._mshr._resp._bits._blkPaddr,
            
            # S2阶段状态和请求信息
            "s2_valid": bundle.ICacheMainPipe._s2._valid,
            "s2_req_vaddr_0": dut.GetInternalSignal(MainPipe_dict["s2_req_vaddr_0"], use_vpi=False),
            "s2_req_vaddr_1": dut.GetInternalSignal(MainPipe_dict["s2_req_vaddr_1"], use_vpi=False),
            "s2_req_ptags_0": dut.GetInternalSignal(MainPipe_dict["s2_req_ptags_0"], use_vpi=False),
            "s2_req_ptags_1": dut.GetInternalSignal(MainPipe_dict["s2_req_ptags_1"], use_vpi=False),
            "s2_doubleline": dut.GetInternalSignal(MainPipe_dict["s2_doubleline"], use_vpi=False),
        },
        bins={
            # 18.1: MSHR命中（匹配且本阶段有效）- 单行
            "CP18.1_mshr_hit_single_line": lambda d: (
                d["s2_valid"].value == 1 and
                d["mshr_resp_valid"].value == 1 and
                d["mshr_resp_corrupt"].value == 0 and
                d["s2_doubleline"].value == 0 and
                (d["s2_req_vaddr_0"].value >> 6) & 0xFF == d["mshr_resp_vSetIdx"].value and
                d["s2_req_ptags_0"].value == (d["mshr_resp_blkPaddr"].value >> 6) & 0xFFFFFFFFF
            ),
            
            # 18.1: MSHR命中（匹配且本阶段有效）- 跨行
            "CP18.1_mshr_hit_double_line": lambda d: (
                d["s2_valid"].value == 1 and
                d["mshr_resp_valid"].value == 1 and
                d["mshr_resp_corrupt"].value == 0 and
                d["s2_doubleline"].value == 1 and
                (
                    # 端口0匹配
                    ((d["s2_req_vaddr_0"].value >> 6) & 0xFF == d["mshr_resp_vSetIdx"].value and
                     d["s2_req_ptags_0"].value == (d["mshr_resp_blkPaddr"].value >> 6) & 0xFFFFFFFFF)
                    or
                    # 端口1匹配
                    ((d["s2_req_vaddr_1"].value >> 6) & 0xFF == d["mshr_resp_vSetIdx"].value and
                     d["s2_req_ptags_1"].value == (d["mshr_resp_blkPaddr"].value >> 6) & 0xFFFFFFFFF)
                )
            ),
            
            # 18.2: MSHR未命中 - 单行
            "CP18.2_mshr_miss_single_line": lambda d: (
                d["s2_doubleline"].value == 0 and
                not (
                    d["s2_valid"].value == 1 and
                    d["mshr_resp_valid"].value == 1 and
                    d["mshr_resp_corrupt"].value == 0 and
                    (d["s2_req_vaddr_0"].value >> 6) & 0xFF == d["mshr_resp_vSetIdx"].value and
                    d["s2_req_ptags_0"].value == (d["mshr_resp_blkPaddr"].value >> 6) & 0xFFFFFFFFF
                )
            ),
            
            # 18.2: MSHR未命中 - 跨行
            "CP18.2_mshr_miss_double_line": lambda d: (
                d["s2_doubleline"].value == 1 and
                not (
                    d["s2_valid"].value == 1 and
                    d["mshr_resp_valid"].value == 1 and
                    d["mshr_resp_corrupt"].value == 0 and
                    (
                        # 端口0匹配
                        ((d["s2_req_vaddr_0"].value >> 6) & 0xFF == d["mshr_resp_vSetIdx"].value and
                         d["s2_req_ptags_0"].value == (d["mshr_resp_blkPaddr"].value >> 6) & 0xFFFFFFFFF)
                        or
                        # 端口1匹配
                        ((d["s2_req_vaddr_1"].value >> 6) & 0xFF == d["mshr_resp_vSetIdx"].value and
                         d["s2_req_ptags_1"].value == (d["mshr_resp_blkPaddr"].value >> 6) & 0xFFFFFFFFF)
                    )
                )
            ),
        },
        name="CP18_MSHR_Match_Data_Update"
    )
    
    # =================================================================
    # CP 19: Miss 请求发送逻辑和合并异常
    # =================================================================
    g.add_watch_point(
        {
            # MSHR请求发送接口
            "mshr_req_valid": bundle.io._mshr._req._valid,
            "mshr_req_ready": bundle.io._mshr._req._ready,
            "flush": bundle.io._flush,
            
            # S2阶段控制和状态信号
            "s2_valid": dut.GetInternalSignal(MainPipe_dict["s2_valid"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
            "s2_hits_0": dut.GetInternalSignal(MainPipe_dict["s2_hits_0"], use_vpi=False),
            "s2_hits_1": dut.GetInternalSignal(MainPipe_dict["s2_hits_1"], use_vpi=False),
            "s2_doubleline": dut.GetInternalSignal(MainPipe_dict["s2_doubleline"], use_vpi=False),
            
            # Miss检测信号
            "s2_should_fetch_0": dut.GetInternalSignal(MainPipe_dict["s2_should_fetch_0"], use_vpi=False),
            "s2_should_fetch_1": dut.GetInternalSignal(MainPipe_dict["s2_should_fetch_1"], use_vpi=False),
            "s2_has_send_0": dut.GetInternalSignal(MainPipe_dict["s2_has_send_0"], use_vpi=False),
            "s2_has_send_1": dut.GetInternalSignal(MainPipe_dict["s2_has_send_1"], use_vpi=False),
            
            # ECC错误检测信号
            "s2_meta_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_meta_corrupt_0"], use_vpi=False),
            "s2_meta_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_meta_corrupt_1"], use_vpi=False),
            "s2_data_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_data_corrupt_0"], use_vpi=False),
            "s2_data_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_data_corrupt_1"], use_vpi=False),
            "s2_corrupt_refetch_0": dut.GetInternalSignal(MainPipe_dict["s2_corrupt_refetch_0"], use_vpi=False),
            "s2_corrupt_refetch_1": dut.GetInternalSignal(MainPipe_dict["s2_corrupt_refetch_1"], use_vpi=False),
            
            # 异常信号
            "s2_exception_0": dut.GetInternalSignal(MainPipe_dict["s2_exception_0"], use_vpi=False),
            "s2_exception_1": dut.GetInternalSignal(MainPipe_dict["s2_exception_1"], use_vpi=False),
            "s2_l2_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_l2_corrupt_0"], use_vpi=False),
            "s2_l2_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_l2_corrupt_1"], use_vpi=False),
            
            # MMIO检测信号
            "s2_mmio_0": dut.GetInternalSignal(MainPipe_dict["s2_mmio_0"], use_vpi=False),
            
            # 异常输出信号（用于验证合并结果）
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            
            # RespStall信号用于判断取指完成
            "respStall": bundle.io._respStall,
        },
        bins={
            # 19.1: 未发生Miss - 当s2_hits为高，meta和data都没有错误，无异常，非MMIO区域时，s2_should_fetch为低
            "CP19.1_no_miss_needed": lambda d: d["s2_valid"].value == 1 and \
                                              d["s2_hits_0"].value == 1 and \
                                              d["s2_meta_corrupt_0"].value == 0 and \
                                              d["s2_data_corrupt_0"].value == 0 and \
                                              d["s2_exception_0"].value == 0 and \
                                              d["s2_mmio_0"].value == 0 and \
                                              d["s2_should_fetch_0"].value == 0,
            
            # 19.2: 单口Miss - 当出现未命中或ECC错误，端口不存在异常且未处于MMIO区域时，向MSHR发送Miss请求
            "CP19.2_single_port_miss_port0": lambda d: d["s2_valid"].value == 1 and \
                                                      (d["s2_hits_0"].value == 0 or d["s2_corrupt_refetch_0"].value == 1) and \
                                                      d["s2_exception_0"].value == 0 and \
                                                      d["s2_mmio_0"].value == 0 and \
                                                      d["s2_should_fetch_0"].value == 1 and \
                                                      d["s2_has_send_0"].value == 0 and \
                                                      d["flush"].value == 0 and \
                                                      d["mshr_req_valid"].value == 1,
            
            "CP19.2_single_port_miss_port1": lambda d: d["s2_valid"].value == 1 and \
                                                      d["s2_doubleline"].value == 1 and \
                                                      (d["s2_hits_1"].value == 0 or d["s2_corrupt_refetch_1"].value == 1) and \
                                                      d["s2_exception_0"].value == 0 and d["s2_exception_1"].value == 0 and \
                                                      d["s2_should_fetch_1"].value == 1 and \
                                                      d["s2_has_send_1"].value == 0 and \
                                                      d["flush"].value == 0,
            
            # 19.3: 双口都需要Miss - 两个端口都满足s2_should_fetch为高的条件
            "CP19.3_dual_port_miss": lambda d: d["s2_valid"].value == 1 and \
                                              d["s2_doubleline"].value == 1 and \
                                              d["s2_should_fetch_0"].value == 1 and \
                                              d["s2_should_fetch_1"].value == 1 and \
                                              d["s2_has_send_0"].value == 0 and \
                                              d["s2_has_send_1"].value == 0 and \
                                              d["flush"].value == 0,
            
            # 19.4: 重复请求屏蔽 - 当已经发送了请求，s2_has_send为true，阻止重复发送
            "CP19.4_duplicate_request_blocked": lambda d: d["s2_valid"].value == 1 and \
                                                         d["s2_should_fetch_0"].value == 1 and \
                                                         d["s2_has_send_0"].value == 1 and \
                                                         d["mshr_req_valid"].value == 0,
            
            # 19.5: 仅ITLB/PMP异常 - S1阶段已记录了ITLB或PMP异常，L2 corrupt=false
            "CP19.5_only_itlb_pmp_exception": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                       d["s2_exception_0"].value != 0 and \
                                                       d["s2_l2_corrupt_0"].value == 0 and \
                                                       d["fetch_resp_exception_0"].value == d["s2_exception_0"].value,
            
            # 19.6: 仅L2异常 - S2阶段s2_l2_corrupt为true，且无ITLB/PMP异常
            "CP19.6_only_l2_exception": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                 d["s2_exception_0"].value == 0 and \
                                                 d["s2_l2_corrupt_0"].value == 1 and \
                                                 d["fetch_resp_exception_0"].value != 0,
            
            # 19.7: ITLB + L2同时出现 - 同时触发ITLB异常和L2 corrupt，s2_exception_out优先保留ITLB异常类型
            "CP19.7_itlb_l2_both_itlb_priority": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                          d["s2_exception_0"].value != 0 and \
                                                          d["s2_l2_corrupt_0"].value == 1 and \
                                                          d["fetch_resp_exception_0"].value == d["s2_exception_0"].value,
            
            # 19.8: s2阶段取指完成 - s2_should_fetch的所有端口都为低，表示不需要取指，那么取指完成
            # 在verilog实现中通过~io_fetch_topdownIcacheMiss_0和s2_fire来表示
            "CP19.8_s2_fetch_finish": lambda d: d["s2_valid"].value == 1 and \
                                               d["s2_should_fetch_0"].value == 0 and \
                                               d["s2_should_fetch_1"].value == 0 and \
                                               d["respStall"].value == 0 and \
                                               d["s2_fire"].value == 1,
        },
        name="CP19_Miss_Request_Exception_Merge"
    )
    
    # =================================================================
    # CP 20: 响应 IFU
    # =================================================================
    g.add_watch_point(
        {
            # 核心控制信号 (对应toIFU.valid = s2_fire)
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
            
            # S2阶段内部状态信号
            "s2_valid": bundle.ICacheMainPipe._s2._valid,
            
            "s2_hits_0": dut.GetInternalSignal(MainPipe_dict["s2_hits_0"], use_vpi=False),
            "s2_hits_1": dut.GetInternalSignal(MainPipe_dict["s2_hits_1"], use_vpi=False),
            "s2_doubleline": dut.GetInternalSignal(MainPipe_dict["s2_doubleline"], use_vpi=False),
            "s2_should_fetch_0": dut.GetInternalSignal(MainPipe_dict["s2_should_fetch_0"], use_vpi=False),
            "s2_should_fetch_1": dut.GetInternalSignal(MainPipe_dict["s2_should_fetch_1"], use_vpi=False),
            
            # 输出响应信号
            "fetch_resp_doubleline": bundle.io._fetch._resp._bits._doubleline,
            "fetch_resp_data": bundle.io._fetch._resp._bits._data,
            "fetch_resp_paddr_0": bundle.io._fetch._resp._bits._paddr._0,
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
            "fetch_resp_pmp_mmio_0": bundle.io._fetch._resp._bits._pmp_mmio._0,
            "fetch_resp_pmp_mmio_1": bundle.io._fetch._resp._bits._pmp_mmio._1,
            "fetch_resp_itlb_pbmt_0": bundle.io._fetch._resp._bits._itlb_pbmt._0,
            "fetch_resp_itlb_pbmt_1": bundle.io._fetch._resp._bits._itlb_pbmt._1,
            
            # 控制信号
            "respStall": bundle.io._respStall,
            "flush": bundle.io._flush,
        },
        bins={
            # 20.1: 正常命中并返回
            # 文档条件：不存在任何异常或Miss，s2命中，s2阶段取指完成，外部respStall停止信号也为低
            # 期望：toIFU.valid=true，toIFU.bits.data为正确Cacheline数据，exception/pmp_mmio/itlb_pbmt=none
            "CP20.1_normal_hit_response": lambda d: (
                # 核心条件：s2_fire = true (对应s2成功发射)
                d["s2_fire"].value == 1 and
                d["fetch_resp_valid"].value == 1 and
                # s2命中条件
                d["s2_valid"].value == 1 and
                d["s2_hits_0"].value == 1 and
                # s2阶段取指完成 (s2_fetch_finish等效：不需要fetch)
                d["s2_should_fetch_0"].value == 0 and
                d["s2_should_fetch_1"].value == 0 and
                # 无异常条件
                d["fetch_resp_exception_0"].value == 0 and
                d["fetch_resp_exception_1"].value == 0 and
                # 外部控制信号
                d["respStall"].value == 0 and
                d["flush"].value == 0 and
                # pmp_mmio和itlb_pbmt为none(0)
                d["fetch_resp_pmp_mmio_0"].value == 0 and
                d["fetch_resp_itlb_pbmt_0"].value == 0
            ),
            
            # 20.2: 异常返回
            # 条件：设置ITLB、PMP、或L2 corrupt异常
            # 期望：toIFU.bits.exception(i)=对应异常类型，pmp_mmio、itlb_pbmt根据异常设置
            "CP20.2_exception_response": lambda d: (
                d["s2_fire"].value == 1 and
                d["fetch_resp_valid"].value == 1 and
                # 有异常的情况
                (d["fetch_resp_exception_0"].value != 0 or 
                 d["fetch_resp_exception_1"].value != 0 or
                 d["fetch_resp_pmp_mmio_0"].value == 1 or
                 d["fetch_resp_pmp_mmio_1"].value == 1 or
                 d["fetch_resp_itlb_pbmt_0"].value != 0 or
                 d["fetch_resp_itlb_pbmt_1"].value != 0)
            ),
            
            # 20.3: 跨行取指
            # 条件：s2_doubleline=true，同时检查第一路、第二路返回情况
            # 期望：toIFU.bits.doubleline=true，第二路异常处理
            "CP20.3_doubleline_fetch": lambda d: (
                d["s2_fire"].value == 1 and
                d["fetch_resp_valid"].value == 1 and
                d["s2_doubleline"].value == 1 and
                d["fetch_resp_doubleline"].value == 1 and
                # 至少一路有效响应
                (d["s2_hits_0"].value == 1 or d["s2_hits_1"].value == 1)
            ),
            
            # 20.4: RespStall阻塞响应
            # 条件：外部io.respStall=true，导致S2阶段无法发射到IFU
            # 期望：s2_fire=false，toIFU.valid也不拉高，S2保持原状态等待
            "CP20.4_resp_stall_block": lambda d: (
                d["respStall"].value == 1 and
                d["s2_fire"].value == 0 and
                d["fetch_resp_valid"].value == 0 and
                # S2阶段保持有效但无法发射
                d["s2_valid"].value == 1
            ),
        },
        name="CP20_Response_IFU"
    )
    
    # =================================================================
    # CP 21: L2 Corrupt 报告
    # =================================================================
    g.add_watch_point(
        {
            # Bundle接口信号（错误报告接口）
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
            
            # MSHR响应信号（用于理解L2 corrupt来源，但不是直接验证条件）
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            "mshr_resp_corrupt": bundle.io._mshr._resp._bits._corrupt,
            
            # 时序控制信号
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
            "s1_fire": dut.GetInternalSignal(MainPipe_dict["s1_fire"], use_vpi=False),
            
            "s2_l2_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_l2_corrupt_0"], use_vpi=False),
            "s2_l2_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_l2_corrupt_1"], use_vpi=False),
            "s2_bankMSHRHit_7": dut.GetInternalSignal(MainPipe_dict["s2_bankMSHRHit_7"], use_vpi=False),
            "s2_bankMSHRHit_0": dut.GetInternalSignal(MainPipe_dict["s2_bankMSHRHit_0"], use_vpi=False),
            "s2_MSHR_hits_1": dut.GetInternalSignal(MainPipe_dict["s2_MSHR_hits_1"], use_vpi=False),
            "s2_valid": dut.GetInternalSignal(MainPipe_dict["s2_valid"], use_vpi=False),
            "s2_doubleline": dut.GetInternalSignal(MainPipe_dict["s2_doubleline"], use_vpi=False),
        },
        bins={
            # 21.1: L2 Corrupt单路
            # 要求：s2阶段准备完成可以发射（s2_fire为高），s2_MSHR_hits(0)和fromMSHR.bits.corrupt为高
            # s2_l2_corrupt(0) = true，io.errors(0).valid = true，io.errors(0).bits.source.l2 = true
            "CP21.1_l2_corrupt_single": lambda d: (
                d["s2_fire"].value == 1 and
                d["s2_l2_corrupt_0"].value == 1 and
                (d["s2_bankMSHRHit_7"].value == 1 or d["s2_bankMSHRHit_0"].value == 1) and
                d["mshr_resp_valid"].value == 1 and
                d["mshr_resp_corrupt"].value == 1
            ),
            
            # 21.2: 双路同时corrupt
            # 要求：端口0和端口1都从L2 corrupt数据中获取
            # s2_l2_corrupt均为true，发射后分别报告到io.errors(0)和io.errors(1)
            "CP21.2_dual_port_corrupt": lambda d: (
                d["s2_fire"].value == 1 and
                d["s2_doubleline"].value == 1 and
                (d["s2_bankMSHRHit_7"].value == 1 or d["s2_bankMSHRHit_0"].value == 1) and
                d["s2_l2_corrupt_0"].value == 1 and
                d["s2_l2_corrupt_1"].value == 1 and
                d["mshr_resp_valid"].value == 1 and
                d["mshr_resp_corrupt"].value == 1
            ),
        },
        name="CP21_L2_Corrupt_Report"
    )
    
    # =================================================================
    # CP 22: 刷新机制
    # =================================================================
    g.add_watch_point(
        {
            # 全局刷新控制信号
            "flush": bundle.io._flush,
            
            # 各阶段fire控制信号（使用bundle中已绑定的信号优先）
            "s0_fire": bundle.ICacheMainPipe._s0_fire,
            "s1_fire": dut.GetInternalSignal(MainPipe_dict["s1_fire"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
            
            # 各阶段valid控制信号
            "s1_valid": dut.GetInternalSignal(MainPipe_dict["s1_valid"], use_vpi=False),
            "s2_valid": bundle.ICacheMainPipe._s2._valid,
            
            # MSHR请求控制信号（验证S2阶段刷新对MSHR的影响）
            "mshr_req_valid": bundle.io._mshr._req._valid,
            
            # 其他相关信号用于辅助验证
            "fetch_req_valid": bundle.io._fetch._req._valid,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
        },
        bins={
            # 22.1: 全局刷新 - io.flush = true 时，各阶段都正确响应刷新
            # 要求：s0_flush, s1_flush, s2_flush = true（功能等价：各fire信号 = false）
            "CP22.1_global_flush": lambda d: d["flush"].value == 1 and \
                                            d["s0_fire"].value == 0 and \
                                            d["s1_fire"].value == 0 and \
                                            d["s2_fire"].value == 0,
            
            # 22.2: S0阶段刷新效果 - s0_flush = true 时 s0_fire = false
            # 要求：s0_flush = true, s0_fire = false（功能等价：flush时s0_fire被阻止）
            "CP22.2_s0_flush_effect": lambda d: d["flush"].value == 1 and \
                                               d["s0_fire"].value == 0,
            
            # 22.3: S1阶段刷新效果 - s1_flush = true 时 s1_valid, s1_fire = false
            # 要求：s1_flush = true, s1_valid, s1_fire = false（功能等价：flush时s1被清除）
            "CP22.3_s1_flush_effect": lambda d: d["flush"].value == 1 and \
                                               d["s1_fire"].value == 0,
                                               # 注意：s1_valid的清除在时序逻辑中体现，flush时s1_valid会被异步清除
            
            # 22.4: S2阶段刷新效果 - s2_flush = true 时多个信号被清除
            # 要求：s2_flush = true, s2_valid, toMSHRArbiter.io.in(i).valid, s2_fire = false
            "CP22.4_s2_flush_effect": lambda d: d["flush"].value == 1 and \
                                               d["s2_fire"].value == 0 and \
                                               d["mshr_req_valid"].value == 0,
        },
        name="CP22_Flush_Mechanism"
    )
    
    return g


def create_mainpipe_coverage_groups(bundle, dut):
    """
    创建MainPipe模块的功能覆盖点组合，完整实现CP11-CP22验证点
    
    Args:
        bundle: MainPipeBundle对象
        dut: DUT对象用于访问内部信号
        
    Returns:
        list: 包含所有覆盖点组的列表
    """
    mainpipe_coverage = define_mainpipe_coverage(bundle, dut)
    
    return [mainpipe_coverage]