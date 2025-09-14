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
        
        # S2 data should fetch signals (miss detection)
        "s2_should_fetch_0": "ICacheMainPipe_top.ICacheMainPipe.s2_should_fetch_0",
        "s2_should_fetch_1": "ICacheMainPipe_top.ICacheMainPipe.s2_should_fetch_1",
        
        # Backend exception
        "s1_backendException": "ICacheMainPipe_top.ICacheMainPipe.s1_backendException",
    }
    
    # =================================================================
    # CP 11: 访问 DataArray 的单路
    # 监控目标：根据WayLookup信息决定是否访问DataArray
    # =================================================================
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "ecc_enable": bundle.io._ecc_enable,
            "respStall": bundle.io._respStall,
            # DataArray相关信号
            "dataArray_toIData_0_valid": bundle.io._dataArray._toIData._0._valid,
            "dataArray_toIData_3_valid": bundle.io._dataArray._toIData._3._valid,
            "dataArray_toIData_3_ready": bundle.io._dataArray._toIData._3._ready,
            # Internal stage signals
            "s1_fire": dut.GetInternalSignal(MainPipe_dict["s1_fire"], use_vpi=False),
            "s1_hits_0": dut.GetInternalSignal(MainPipe_dict["s1_hits_0"], use_vpi=False),
            "s1_hits_1": dut.GetInternalSignal(MainPipe_dict["s1_hits_1"], use_vpi=False),
        },
        bins={
            # 11.1: S1阶段正常访问DataArray (S1 fire且有命中)
            "CP11.1_s1_access_dataarray": lambda d: d["s1_fire"].value == 1 and \
                                                   (d["s1_hits_0"].value == 1 or d["s1_hits_1"].value == 1) and \
                                                   d["flush"].value == 0,
            
            # 11.2: S1阶段DataArray未命中
            "CP11.2_s1_dataarray_miss": lambda d: d["s1_fire"].value == 1 and \
                                                 d["s1_hits_0"].value == 0 and \
                                                 d["s1_hits_1"].value == 0,
            
            # 11.3: DataArray写忙，无法访问
            "CP11.3_dataarray_write_busy": lambda d: d["dataArray_toIData_3_ready"].value == 0,
            
            # 11.4: Flush状态下的访问控制
            "CP11.4_access_during_flush": lambda d: d["flush"].value == 1,
        },
        name="CP11_DataArray_Access"
    )
    
    # =================================================================
    # CP 12: Meta ECC 校验
    # 监控目标：Meta ECC校验逻辑，检查数据完整性
    # =================================================================
    g.add_watch_point(
        {
            "ecc_enable": bundle.io._ecc_enable,
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
            "errors_0_report_to_beu": bundle.io._errors._0._bits._report_to_beu,
            "errors_1_report_to_beu": bundle.io._errors._1._bits._report_to_beu,
            # Internal meta corrupt hit signals
            "s1_meta_corrupt_hit_num_0": dut.GetInternalSignal(MainPipe_dict["s1_meta_corrupt_hit_num_0"], use_vpi=False),
            "s1_meta_corrupt_hit_num_1": dut.GetInternalSignal(MainPipe_dict["s1_meta_corrupt_hit_num_1"], use_vpi=False),
        },
        bins={
            # 12.1: 无ECC错误（ECC使能且无错误报告）
            "CP12.1_no_ecc_error": lambda d: d["ecc_enable"].value == 1 and \
                                            d["errors_0_valid"].value == 0 and \
                                            d["errors_1_valid"].value == 0,
            
            # 12.2: S1阶段Meta ECC corrupt检测
            "CP12.2_s1_meta_corrupt_hit_0": lambda d: d["ecc_enable"].value == 1 and \
                                                     d["s1_meta_corrupt_hit_num_0"].value != 0,
            
            # 12.3: S1阶段Meta ECC corrupt检测 - 通道1
            "CP12.3_s1_meta_corrupt_hit_1": lambda d: d["ecc_enable"].value == 1 and \
                                                     d["s1_meta_corrupt_hit_num_1"].value != 0,
            
            # 12.4: ECC功能关闭
            "CP12.4_ecc_disabled": lambda d: d["ecc_enable"].value == 0,
        },
        name="CP12_Meta_ECC_Check"
    )
    
    # =================================================================
    # CP 13: PMP 检查
    # 监控目标：物理内存保护检查
    # =================================================================
    g.add_watch_point(
        {
            "pmp_0_resp_instr": bundle.io._pmp._0._resp._instr,
            "pmp_0_resp_mmio": bundle.io._pmp._0._resp._mmio,
            "pmp_1_resp_instr": bundle.io._pmp._1._resp._instr,
            "pmp_1_resp_mmio": bundle.io._pmp._1._resp._mmio,
            "fetch_resp_pmp_mmio_0": bundle.io._fetch._resp._bits._pmp_mmio._0,
            "fetch_resp_pmp_mmio_1": bundle.io._fetch._resp._bits._pmp_mmio._1,
        },
        bins={
            # 13.1: 没有PMP异常（两个通道都有指令访问权限）
            "CP13.1_no_pmp_exception": lambda d: d["pmp_0_resp_instr"].value == 1 and \
                                                d["pmp_1_resp_instr"].value == 1,
            
            # 13.2: 通道0有PMP异常
            "CP13.2_channel0_pmp_exception": lambda d: d["pmp_0_resp_instr"].value == 0,
            
            # 13.3: 通道1有PMP异常
            "CP13.3_channel1_pmp_exception": lambda d: d["pmp_1_resp_instr"].value == 0,
            
            # 13.4: 两个通道都有PMP异常
            "CP13.4_both_channels_pmp_exception": lambda d: d["pmp_0_resp_instr"].value == 0 and \
                                                           d["pmp_1_resp_instr"].value == 0,
            
            # 13.5: 通道0映射到MMIO区域
            "CP13.5_channel0_mmio": lambda d: d["pmp_0_resp_mmio"].value == 1,
            
            # 13.6: 通道1映射到MMIO区域
            "CP13.6_channel1_mmio": lambda d: d["pmp_1_resp_mmio"].value == 1,
        },
        name="CP13_PMP_Check"
    )
    
    # =================================================================
    # CP 14: 异常合并
    # 监控目标：ITLB和PMP异常的优先级合并
    # =================================================================
    g.add_watch_point(
        {
            "wayLookupRead_entry_itlb_exception_0": bundle.io._wayLookupRead._bits._entry._itlb._exception._0,
            "wayLookupRead_entry_itlb_exception_1": bundle.io._wayLookupRead._bits._entry._itlb._exception._1,
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
        },
        bins={
            # 14.1: 没有异常
            "CP14.1_no_exception": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value == 0 and \
                                            d["wayLookupRead_entry_itlb_exception_1"].value == 0 and \
                                            d["fetch_resp_exception_0"].value == 0 and \
                                            d["fetch_resp_exception_1"].value == 0,
            
            # 14.2: 只有ITLB异常
            "CP14.2_only_itlb_exception": lambda d: (d["wayLookupRead_entry_itlb_exception_0"].value != 0 or \
                                                    d["wayLookupRead_entry_itlb_exception_1"].value != 0),
            
            # 14.3: 异常传递到fetch响应
            "CP14.3_exception_to_fetch_resp": lambda d: (d["fetch_resp_exception_0"].value != 0 or \
                                                        d["fetch_resp_exception_1"].value != 0),
            
            # 14.4: 异常优先级处理（ITLB优先于PMP）
            "CP14.4_exception_priority": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value != 0 and \
                                                  d["fetch_resp_exception_0"].value != 0,
        },
        name="CP14_Exception_Merge"
    )
    
    # =================================================================
    # CP 15: MSHR 匹配和数据选择
    # 监控目标：MSHR命中检查和数据源选择
    # =================================================================
    g.add_watch_point(
        {
            "mshr_req_valid": bundle.io._mshr._req._valid,
            "mshr_req_ready": bundle.io._mshr._req._ready,
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            "mshr_resp_corrupt": bundle.io._mshr._resp._bits._corrupt,
            # Internal S1 MSHR bank hit signals
            "s1_bankMSHRHit_0": dut.GetInternalSignal(MainPipe_dict["s1_bankMSHRHit_0"], use_vpi=False),
            "s1_bankMSHRHit_1": dut.GetInternalSignal(MainPipe_dict["s1_bankMSHRHit_1"], use_vpi=False),
            "s1_bankMSHRHit_2": dut.GetInternalSignal(MainPipe_dict["s1_bankMSHRHit_2"], use_vpi=False),
            "s1_bankMSHRHit_3": dut.GetInternalSignal(MainPipe_dict["s1_bankMSHRHit_3"], use_vpi=False),
            "s1_data_is_from_MSHR_0": dut.GetInternalSignal(MainPipe_dict["s1_data_is_from_MSHR_0"], use_vpi=False),
            "s1_data_is_from_MSHR_1": dut.GetInternalSignal(MainPipe_dict["s1_data_is_from_MSHR_1"], use_vpi=False),
        },
        bins={
            # 15.1: S1阶段MSHR bank命中
            "CP15.1_s1_mshr_bank_hit": lambda d: (d["s1_bankMSHRHit_0"].value == 1 or \
                                                  d["s1_bankMSHRHit_1"].value == 1 or \
                                                  d["s1_bankMSHRHit_2"].value == 1 or \
                                                  d["s1_bankMSHRHit_3"].value == 1),
            
            # 15.2: S1阶段数据来自MSHR
            "CP15.2_s1_data_from_mshr": lambda d: (d["s1_data_is_from_MSHR_0"].value == 1 or \
                                                   d["s1_data_is_from_MSHR_1"].value == 1),
            
            # 15.3: MSHR响应corrupt
            "CP15.3_mshr_resp_corrupt": lambda d: d["mshr_resp_valid"].value == 1 and \
                                                 d["mshr_resp_corrupt"].value == 1,
            
            # 15.4: MSHR请求发送
            "CP15.4_mshr_request": lambda d: d["mshr_req_valid"].value == 1 and \
                                           d["mshr_req_ready"].value == 1,
        },
        name="CP15_MSHR_Match_Data_Select"
    )
    
    # =================================================================
    # CP 16: Data ECC 校验
    # 监控目标：S2阶段的数据ECC校验
    # =================================================================
    g.add_watch_point(
        {
            "ecc_enable": bundle.io._ecc_enable,
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            # Internal S2 bank corrupt signals
            "s2_bank_corrupt_0": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_0"], use_vpi=False),
            "s2_bank_corrupt_1": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_1"], use_vpi=False),
            "s2_bank_corrupt_2": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_2"], use_vpi=False),
            "s2_bank_corrupt_3": dut.GetInternalSignal(MainPipe_dict["s2_bank_corrupt_3"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire
        },
        bins={
            # 16.1: S2阶段无bank corrupt
            "CP16.1_s2_no_bank_corrupt": lambda d: d["s2_fire"].value == 1 and \
                                                   d["s2_bank_corrupt_0"].value == 0 and \
                                                   d["s2_bank_corrupt_1"].value == 0 and \
                                                   d["s2_bank_corrupt_2"].value == 0 and \
                                                   d["s2_bank_corrupt_3"].value == 0,
            
            # 16.2: S2阶段单bank corrupt
            "CP16.2_s2_single_bank_corrupt": lambda d: d["s2_fire"].value == 1 and \
                                                      ((d["s2_bank_corrupt_0"].value == 1 and d["s2_bank_corrupt_1"].value == 0) or \
                                                       (d["s2_bank_corrupt_1"].value == 1 and d["s2_bank_corrupt_0"].value == 0)),
            
            # 16.3: S2阶段多bank corrupt
            "CP16.3_s2_multi_bank_corrupt": lambda d: d["s2_fire"].value == 1 and \
                                                     d["s2_bank_corrupt_0"].value == 1 and \
                                                     d["s2_bank_corrupt_1"].value == 1,
            
            # 16.4: ECC功能关闭
            "CP16.4_data_ecc_disabled": lambda d: d["ecc_enable"].value == 0,
        },
        name="CP16_Data_ECC_Check"
    )
    
    # =================================================================
    # CP 17: 冲刷 MetaArray
    # 监控目标：Meta/Data ECC错误时的MetaArray冲刷
    # =================================================================
    g.add_watch_point(
        {
            "metaArrayFlush_0_valid": bundle.io._metaArrayFlush._0._valid,
            "metaArrayFlush_1_valid": bundle.io._metaArrayFlush._1._valid,
            "metaArrayFlush_0_waymask": bundle.io._metaArrayFlush._0._bits._waymask,
            "metaArrayFlush_1_waymask": bundle.io._metaArrayFlush._1._bits._waymask,
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
        },
        bins={
            # 17.1: Meta ECC错误冲刷（所有路）
            "CP17.1_meta_ecc_flush_all_ways": lambda d: d["metaArrayFlush_0_valid"].value == 1 and \
                                                       d["metaArrayFlush_0_waymask"].value == 0xf,
            
            # 17.2: Data ECC错误冲刷（特定路）
            "CP17.2_data_ecc_flush_specific_way": lambda d: d["metaArrayFlush_0_valid"].value == 1 and \
                                                           d["metaArrayFlush_0_waymask"].value != 0xf and \
                                                           d["errors_0_valid"].value == 1,
            
            # 17.3: 两个端口都有冲刷操作
            "CP17.3_both_ports_flush": lambda d: d["metaArrayFlush_0_valid"].value == 1 and \
                                                d["metaArrayFlush_1_valid"].value == 1,
            
            # 17.4: 无冲刷操作
            "CP17.4_no_flush_operation": lambda d: d["metaArrayFlush_0_valid"].value == 0 and \
                                                  d["metaArrayFlush_1_valid"].value == 0,
        },
        name="CP17_MetaArray_Flush"
    )
    
    # =================================================================
    # CP 18: 监控 MSHR 匹配与数据更新
    # 监控目标：S2阶段MSHR匹配和数据更新逻辑
    # =================================================================
    g.add_watch_point(
        {
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            "mshr_resp_corrupt": bundle.io._mshr._resp._bits._corrupt,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
        },
        bins={
            # 18.1: MSHR命中且本阶段有效
            "CP18.1_mshr_hit_stage_valid": lambda d: d["mshr_resp_valid"].value == 1 and \
                                                    d["mshr_resp_corrupt"].value == 0,
            
            # 18.2: MSHR未命中
            "CP18.2_mshr_miss_no_update": lambda d: d["mshr_resp_valid"].value == 0 and \
                                                   d["fetch_resp_valid"].value == 1,
            
            # 18.3: MSHR响应但数据corrupt
            "CP18.3_mshr_resp_corrupt": lambda d: d["mshr_resp_valid"].value == 1 and \
                                                 d["mshr_resp_corrupt"].value == 1,
            
            # 18.4: 正常数据流转（无MSHR介入）
            "CP18.4_normal_data_flow": lambda d: d["mshr_resp_valid"].value == 0 and \
                                                d["fetch_resp_valid"].value == 0,
        },
        name="CP18_MSHR_Match_Data_Update"
    )
    
    # =================================================================
    # CP 19: Miss 请求发送逻辑和合并异常
    # 监控目标：Miss请求仲裁和异常合并
    # =================================================================
    g.add_watch_point(
        {
            "mshr_req_valid": bundle.io._mshr._req._valid,
            "mshr_req_ready": bundle.io._mshr._req._ready,
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
            "wayLookupRead_entry_itlb_exception_0": bundle.io._wayLookupRead._bits._entry._itlb._exception._0,
            # Internal should fetch signals (miss detection)
            "s2_should_fetch_0": dut.GetInternalSignal(MainPipe_dict["s2_should_fetch_0"], use_vpi=False),
            "s2_should_fetch_1": dut.GetInternalSignal(MainPipe_dict["s2_should_fetch_1"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
        },
        bins={
            # 19.1: S2阶段检测到miss需要fetch
            "CP19.1_s2_should_fetch_0": lambda d: d["s2_fire"].value == 1 and \
                                                 d["s2_should_fetch_0"].value == 1,
            
            # 19.2: S2阶段检测到miss需要fetch - 通道1
            "CP19.2_s2_should_fetch_1": lambda d: d["s2_fire"].value == 1 and \
                                                 d["s2_should_fetch_1"].value == 1,
            
            # 19.3: Miss请求被阻塞
            "CP19.3_miss_request_blocked": lambda d: d["mshr_req_valid"].value == 1 and \
                                                    d["mshr_req_ready"].value == 0,
            
            # 19.4: 仅ITLB/PMP异常
            "CP19.4_only_itlb_pmp_exception": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value != 0 and \
                                                       d["fetch_resp_exception_0"].value != 0,
            
            # 19.5: 异常情况下无Miss请求
            "CP19.5_no_miss_due_exception": lambda d: d["wayLookupRead_entry_itlb_exception_0"].value != 0 and \
                                                     d["mshr_req_valid"].value == 0,
        },
        name="CP19_Miss_Request_Exception_Merge"
    )
    
    # =================================================================
    # CP 20: 响应 IFU
    # 监控目标：S2阶段向IFU的响应逻辑
    # =================================================================
    g.add_watch_point(
        {
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "fetch_resp_doubleline": bundle.io._fetch._resp._bits._doubleline,
            "fetch_resp_exception_0": bundle.io._fetch._resp._bits._exception._0,
            "fetch_resp_exception_1": bundle.io._fetch._resp._bits._exception._1,
            "respStall": bundle.io._respStall,
        },
        bins={
            # 20.1: 正常命中并返回
            "CP20.1_normal_hit_response": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                   d["fetch_resp_exception_0"].value == 0 and \
                                                   d["fetch_resp_exception_1"].value == 0 and \
                                                   d["respStall"].value == 0,
            
            # 20.2: 异常返回
            "CP20.2_exception_response": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                  (d["fetch_resp_exception_0"].value != 0 or \
                                                   d["fetch_resp_exception_1"].value != 0),
            
            # 20.3: 跨行取指
            "CP20.3_doubleline_fetch": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                d["fetch_resp_doubleline"].value == 1,
            
            # 20.4: RespStall导致无法响应
            "CP20.4_resp_stall_block": lambda d: d["respStall"].value == 1 and \
                                                d["fetch_resp_valid"].value == 0,
        },
        name="CP20_Response_IFU"
    )
    
    # =================================================================
    # CP 21: L2 Corrupt 报告
    # 监控目标：L2 Cache corrupt错误报告
    # =================================================================
    g.add_watch_point(
        {
            "mshr_resp_valid": bundle.io._mshr._resp._valid,
            "mshr_resp_corrupt": bundle.io._mshr._resp._bits._corrupt,
            "errors_0_valid": bundle.io._errors._0._valid,
            "errors_1_valid": bundle.io._errors._1._valid,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
        },
        bins={
            # 21.1: L2 Corrupt单路报告
            "CP21.1_l2_corrupt_single_port": lambda d: d["mshr_resp_valid"].value == 1 and \
                                                      d["mshr_resp_corrupt"].value == 1 and \
                                                      d["fetch_resp_valid"].value == 1,
            
            # 21.2: 双路同时corrupt
            "CP21.2_dual_port_corrupt": lambda d: d["mshr_resp_corrupt"].value == 1 and \
                                                 d["errors_0_valid"].value == 1 and \
                                                 d["errors_1_valid"].value == 1,
            
            # 21.3: 无L2 Corrupt错误
            "CP21.3_no_l2_corrupt": lambda d: d["mshr_resp_valid"].value == 1 and \
                                             d["mshr_resp_corrupt"].value == 0,
            
            # 21.4: L2响应无效
            "CP21.4_l2_response_invalid": lambda d: d["mshr_resp_valid"].value == 0,
        },
        name="CP21_L2_Corrupt_Report"
    )
    
    # =================================================================
    # CP 22: 刷新机制
    # 监控目标：流水线刷新控制逻辑
    # =================================================================
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "fetch_req_valid": bundle.io._fetch._req._valid,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "mshr_req_valid": bundle.io._mshr._req._valid,
            # Internal stage fire signals
            "s1_fire": dut.GetInternalSignal(MainPipe_dict["s1_fire"], use_vpi=False),
            "s2_fire": bundle.ICacheMainPipe._s2._fire,
        },
        bins={
            # 22.1: 全局刷新激活且S1阶段停止
            "CP22.1_flush_stops_s1": lambda d: d["flush"].value == 1 and \
                                              d["s1_fire"].value == 0,
            
            # 22.2: 刷新激活且S2阶段停止
            "CP22.2_flush_stops_s2": lambda d: d["flush"].value == 1 and \
                                              d["s2_fire"].value == 0,
            
            # 22.3: 正常运行 - S1和S2都在fire
            "CP22.3_normal_s1_s2_fire": lambda d: d["flush"].value == 0 and \
                                                 d["s1_fire"].value == 1 and \
                                                 d["s2_fire"].value == 1,
            
            # 22.4: S2阶段刷新（MSHR请求停止）
            "CP22.4_s2_flush_stop_mshr": lambda d: d["flush"].value == 1 and \
                                                  d["mshr_req_valid"].value == 0,
            
            # 22.5: 正常运行（无刷新）
            "CP22.5_normal_operation_no_flush": lambda d: d["flush"].value == 0,
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