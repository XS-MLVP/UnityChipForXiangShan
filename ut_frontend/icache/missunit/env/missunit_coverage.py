import toffee.funcov as fc
from toffee.funcov import CovGroup


def define_fifo_coverage(bundle,dut):
    """
    Defines the functional coverage points for the ICacheMissUnit's FIFO.
    
    Args:
        bundle: The top-level ICacheMissUnitBundle object.
        dut: The DUT object for accessing internal signals.
    """
    g = CovGroup("MissUnit_FIFO")
    # create FIFO_internalsignals for FIFO functional coverage
    FIFO_dict = {"enq_ptr_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_value",\
                "enq_ptr_flag":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_flag",\
                "enq_ptr_new_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_new_value",\
                "deq_ptr_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_value",\
                "deq_ptr_flag":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_flag",\
                "deq_ptr_new_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_new_value",\
                "full":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.full"
                }
    # =================================================================
    # CP 28.1 & 28.2 & 28.3: 正常入队 vs 入队翻转 vs 队满阻塞
    # 监控目标：prefetch请求接口和其内部状态
    # =================================================================
    g.add_watch_point(
        # 使用字典作为target，让lambda函数更易读
        {
            "enq_ready": bundle.priorityFIFO._io_enq._ready,
            "enq_valid": bundle.priorityFIFO._io_enq._valid_T_probe,
            "enq_ptr_value": dut.GetInternalSignal(FIFO_dict["enq_ptr_value"], use_vpi=False),
            "enq_ptr_new_value": dut.GetInternalSignal(FIFO_dict["enq_ptr_new_value"], use_vpi=False),
            "enq_ptr_flag": dut.GetInternalSignal(FIFO_dict["enq_ptr_flag"], use_vpi=False),
            "enq_bits": bundle.prefetchDemux._io_chosen,
            "deq_ptr_value": dut.GetInternalSignal(FIFO_dict["deq_ptr_value"], use_vpi=False),
            "deq_ptr_flag": dut.GetInternalSignal(FIFO_dict["deq_ptr_flag"], use_vpi=False),
            "full": dut.GetInternalSignal(FIFO_dict["full"], use_vpi=False)
        },
        bins={
            # 28.1: 新请求到来，FIFO未满，成功入队 
            "enq_when_not_full": lambda d: d["enq_ready"].value == 1 and \
                                           d["enq_valid"].value == 1 and \
                                           d["full"].value == 0 and \
                                           d["enq_ptr_flag"].value == 0 and \
                                           d["enq_ptr_value"].value == d["enq_bits"].value and \
                                           d["enq_ptr_new_value"].value == d["enq_ptr_value"].value + 1,
            
            # 28.2: 新请求到来，FIFO未满，入队将使FIFO满（指针到达边界）
            "enq_when_will_full": lambda d: d["enq_ready"].value == 1 and \
                                            d["enq_valid"].value == 1 and \
                                            d["full"].value == 0 and \
                                            d["enq_ptr_flag"].value == 0 and \
                                            d["enq_ptr_new_value"].value == 0xA and d["enq_ptr_value"].value == 9, \
            # 28.3: 新请求到来，FIFO已满，入队失败
            "enq_blocked_when_full": lambda d: d["enq_ready"].value == 0 and\
                                               d["full"].value == 1 and \
                                               d["enq_ptr_value"].value == d["deq_ptr_value"].value and \
                                               d["enq_ptr_flag"].value != d["deq_ptr_flag"].value
        },
        name="CP_Enqueue_Normal_vs_Full"
    )
    # =================================================================
    # CP 29.1 & 29.2 & 29.3: 正常出队 vs 出队翻转 vs 队空阻塞
    # 监控目标：prefetch请求接口和其内部状态
    # =================================================================
    g.add_watch_point(
        # 使用字典作为target，让lambda函数更易读
        {
            "deq_ready": bundle.priorityFIFO._io_deq._ready_T,
            "deq_valid": bundle.priorityFIFO._io_deq._valid,
            "enq_ptr_value": dut.GetInternalSignal(FIFO_dict["enq_ptr_value"], use_vpi=False),
            "enq_ptr_flag": dut.GetInternalSignal(FIFO_dict["enq_ptr_flag"], use_vpi=False),
            "deq_bits": bundle.priorityFIFO._io_deq_bits,
            "deq_ptr_value": dut.GetInternalSignal(FIFO_dict["deq_ptr_value"], use_vpi=False),
            "deq_ptr_new_value":dut.GetInternalSignal(FIFO_dict["deq_ptr_new_value"], use_vpi=False),
            "deq_ptr_flag": dut.GetInternalSignal(FIFO_dict["deq_ptr_flag"], use_vpi=False),
        },
        bins={
            # 29.1: 新请求到来，FIFO非空，成功出队 
            "deq_when_not_null": lambda d: d["deq_ready"].value == 1 and \
                                           d["deq_valid"].value == 1 and \
                                           d["deq_ptr_flag"].value == 0 and \
                                           d["deq_ptr_new_value"].value == d["deq_ptr_value"].value + 1 and \
                                           d["deq_ptr_value"].value == d["deq_bits"].value, \
            
            # 29.2: 出队时，FIFO非空，出队指针将回环到起始位置
            "deq_when_will_wrap": lambda d: d["deq_ready"].value == 1 and \
                                            d["deq_valid"].value == 1 and \
                                            d["deq_ptr_flag"].value == 0 and \
                                            d["deq_ptr_value"].value == 9 and \
                                            d["deq_ptr_new_value"].value == 0xA, \
            
            # 29.3: 新请求到来，FIFO已空，出队失败
            "deq_blocked_when_null": lambda d: d["deq_valid"].value == 0 and \
                                               d["deq_ptr_flag"].value == 0 and \
                                               d["enq_ptr_value"].value == d["deq_ptr_value"].value
        },
        name="CP_Dequeue_Normal_vs_null"
    )

    # =================================================================
    # CP 30: flush
    # 监控目标：prefetch请求接口和其内部状态
    # =================================================================
    g.add_watch_point(
        # 使用字典作为target，让lambda函数更易读
        {
            "flush":bundle.io._flush,
            "full":dut.GetInternalSignal(FIFO_dict["full"], use_vpi=False),
            "enq_ptr_value": dut.GetInternalSignal(FIFO_dict["enq_ptr_value"], use_vpi=False),
            "enq_ptr_flag": dut.GetInternalSignal(FIFO_dict["enq_ptr_flag"], use_vpi=False),
            "deq_ptr_value": dut.GetInternalSignal(FIFO_dict["deq_ptr_value"], use_vpi=False),
            "deq_ptr_flag": dut.GetInternalSignal(FIFO_dict["deq_ptr_flag"], use_vpi=False),
        },
        bins={
            # 30: flush 
            "after_flush": lambda d: d["flush"].value == 1 and \
                                     d["full"].value == 0 and \
                                     d["enq_ptr_value"].value == 0 and d["enq_ptr_flag"].value == 0 and\
                                     d["deq_ptr_value"].value == 0 and d["deq_ptr_flag"].value == 0\
            
        },
        name="CP_flush"
    )

    return g

def define_missunit_coverage_groups(bundle, dut):
    """
    define functional coverage groups of ICacheMissUnit.
    """
    g = CovGroup("MissUnit_Main_Coverage")

    # =================================================================
    # CP 31.1: 接受新的fetch 31.2:处理已经存在的 fetch 
    #    31.3: 低索引优先
    # 监控目标：fetch request接口和其内部状态，MSHR接口和其内部状态      
    # =================================================================
    def low_index_priority(dic) -> bool:
        if dic["MSHR_1_acquire_valid"].value == 1:
            if dic["MSHR_0_acquire_valid"].value == 1:
                return True
        elif dic["MSHR_2_acquire_valid"].value == 1:
            if dic["MSHR_0_acquire_valid"].value == 1 and dic["MSHR_1_acquire_valid"].value == 1:
                return True
        elif dic["MSHR_3_acquire_valid"].value == 1:
            if dic["MSHR_0_acquire_valid"].value == 1 and dic["MSHR_1_acquire_valid"].value == 1 and dic["MSHR_2_acquire_valid"].value == 1:
                return True
        else:
            return False
    g.add_watch_point(
        {
            "fetch_req_ready": bundle.io._fetch._req._ready,
            "fetch_req_valid": bundle.io._fetch._req._valid,
            "fetch_demux_valid": bundle.fetchDemux._io_in_valid_T_1,
            "fetch_hit":bundle.ICacheMissUnit_.fetchHit,
            "MSHR_0_acquire_valid":bundle.ICacheMissUnit_._fetchMSHRs._0._io._acquire_valid,
            "MSHR_1_acquire_valid":bundle.ICacheMissUnit_._fetchMSHRs._1._io._acquire_valid,
            "MSHR_2_acquire_valid":bundle.ICacheMissUnit_._fetchMSHRs._2._io._acquire_valid,
            "MSHR_3_acquire_valid":bundle.ICacheMissUnit_._fetchMSHRs._3._io._acquire_valid,
        },
        bins={
            # 功能点 31.1: 接受新的取指请求
            # 条件: req_valid=1, req_hit=0 => 期望: demux_fired=1
            "CP31.1": lambda d: d["fetch_req_ready"].value==1 and d["fetch_req_valid"].value==1 and d["fetch_hit"].value==0,
            
            # 功能点 31.2: 处理已有的取指请求
            # 条件: req_valid=1, req_hit=1 => 期望: demux_fired=0
            "CP31.2": lambda d: d["fetch_req_ready"].value==1 and d["fetch_req_valid"].value==1 and d["fetch_hit"].value==1 \
                                and d["fetch_demux_valid"].value==0,
            # 功能点31.3 低索引优先
            "CP31.3":lambda d:low_index_priority(d),

        },
        name="fetch_req_new_vs_hit"
    )

    # =================================================================
    # CP 32.1: 接受新的prefetch 32.2:处理已经存在的 prefetch
    #    32.3: 新请求命中已有MSHR
    # 监控目标：prefetch request接口和其内部状态，MSHR接口和其内部状态
    # =================================================================

    g.add_watch_point(
        {
            "prefetch_req_ready": bundle.io._prefetch_req._ready,
            "prefetch_req_valid": bundle.io._prefetch_req._valid,
            "prefetch_demux_valid": bundle.prefetchDemux._io_in_valid_T_1,
            "prefetch_hit":bundle.ICacheMissUnit_.prefetchHit,
        },
        bins={
            # 功能点 32.1: 接受新的预取请求
            # 条件: req_hit=0 => 期望: demux_fired=1
            "CP32.1": lambda d: d["prefetch_req_ready"].value==1 and d["prefetch_req_valid"].value==1 and d["prefetch_hit"].value==0,
            
            # 功能点 32.2: 处理已有的预取请求
            # 条件: req_hit=1 => 期望: demux_fired=0
            "CP32.2": lambda d: d["prefetch_req_ready"].value==1 and d["prefetch_req_valid"].value==1 and d["prefetch_hit"].value==1 \
                                and d["prefetch_demux_valid"].value==0,
        },
        # 功能点32.3 需要在missunit test中使用assert来验证，
        # 这里不需要覆盖点
        name="prefetch_req_new_vs_hit"
    )

    # =================================================================
    # CP 33: MSHR查找命中逻辑
    # 监控目标：MSHR查找接口和命中状态
    # =================================================================
    g.add_watch_point(
        {
            "fetch_req_valid": bundle.io._fetch._req._valid,
            "fetch_req_blkPaddr": bundle.io._fetch._req._bits._blkPaddr,
            "fetch_req_vSetIdx": bundle.io._fetch._req._bits._vSetIdx,
            "prefetch_req_valid": bundle.io._prefetch_req._valid,
            "prefetch_req_blkPaddr": bundle.io._prefetch_req._bits._blkPaddr,
            "prefetch_req_vSetIdx": bundle.io._prefetch_req._bits._vSetIdx,
            "fetch_hit": bundle.ICacheMissUnit_.fetchHit,
            "prefetch_hit": bundle.ICacheMissUnit_.prefetchHit,
        },
        bins={
            # 33.1: Fetch请求命中现有MSHR
            "CP33.1_fetch_hit_existing": lambda d: d["fetch_req_valid"].value == 1 and d["fetch_hit"].value == 1,
            
            # 33.2: Prefetch请求命中现有MSHR
            "CP33.2_prefetch_hit_existing": lambda d: d["prefetch_req_valid"].value == 1 and d["prefetch_hit"].value == 1,
            
            # 33.3: Prefetch请求与fetch请求地址相同时命中
            "CP33.3_prefetch_hit_fetch_same": lambda d: d["prefetch_req_valid"].value == 1 and \
                                                        d["fetch_req_valid"].value == 1 and \
                                                        d["prefetch_req_blkPaddr"].value == d["fetch_req_blkPaddr"].value and \
                                                        d["prefetch_req_vSetIdx"].value == d["fetch_req_vSetIdx"].value and \
                                                        d["prefetch_hit"].value == 1,
            
            # 33.4: 新请求未命中任何MSHR
            "CP33.4_no_hit": lambda d: (d["fetch_req_valid"].value == 1 and d["fetch_hit"].value == 0) or \
                                       (d["prefetch_req_valid"].value == 1 and d["prefetch_hit"].value == 0),
        },
        name="MSHR_lookup_hit_logic"
    )

    # =================================================================
    # CP 34: acquireArb仲裁逻辑
    # 监控目标：仲裁器的选择逻辑和优先级
    # =================================================================
    g.add_watch_point(
        {
            "acquire_valid": bundle.io._mem._acquire._valid,
            "acquire_source": bundle.io._mem._acquire._bits._source,
            "fetch_0_acquire_valid": bundle.ICacheMissUnit_._fetchMSHRs._0._io._acquire_valid,
            "fetch_1_acquire_valid": bundle.ICacheMissUnit_._fetchMSHRs._1._io._acquire_valid,
            "fetch_2_acquire_valid": bundle.ICacheMissUnit_._fetchMSHRs._2._io._acquire_valid,
            "fetch_3_acquire_valid": bundle.ICacheMissUnit_._fetchMSHRs._3._io._acquire_valid,
            "prefetch_arb_valid": bundle.ICacheMissUnit_._prefetchMSHRs._0._io._acquire_valid, 
        },
        bins={
            # 34.1: Fetch请求优先于prefetch请求
            "CP34.1_fetch_priority": lambda d: d["acquire_valid"].value == 1 and \
                                               d["acquire_source"].value < 4 and \
                                               (d["fetch_0_acquire_valid"].value == 1 or \
                                                d["fetch_1_acquire_valid"].value == 1 or \
                                                d["fetch_2_acquire_valid"].value == 1 or \
                                                d["fetch_3_acquire_valid"].value == 1),
            
            # 34.2: 只有prefetch请求时被选中
            "CP34.2_prefetch_selected": lambda d: d["acquire_valid"].value == 1 and \
                                                  d["acquire_source"].value >= 4 and \
                                                  d["fetch_0_acquire_valid"].value == 0 and \
                                                  d["fetch_1_acquire_valid"].value == 0 and \
                                                  d["fetch_2_acquire_valid"].value == 0 and \
                                                  d["fetch_3_acquire_valid"].value == 0,
        },
        name="acquire_arbitration_logic"
    )

    # =================================================================
    # CP 35: Grant数据接收与处理
    # 监控目标：Grant数据收集和状态更新
    # =================================================================
    g.add_watch_point(
        {
            "grant_valid": bundle.io._mem._grant._valid,
            "grant_opcode": bundle.io._mem._grant._bits._opcode,
            "grant_source": bundle.io._mem._grant._bits._source,
            "grant_corrupt": bundle.io._mem._grant._bits._corrupt,
            "last_fire": bundle.ICacheMissUnit_.last_fire,
            "last_fire_r": bundle.ICacheMissUnit_.last_fire_r,
        },
        bins={
            # 35.1: 第一个beat数据接收
            "CP35.1_first_beat": lambda d: d["grant_valid"].value == 1 and \
                                           d["grant_opcode"].value & 0x1 == 1 and \
                                           d["last_fire"].value == 0,
            
            # 35.2: 最后一个beat数据接收
            "CP35.2_last_beat": lambda d: d["grant_valid"].value == 1 and \
                                          d["grant_opcode"].value & 0x1 == 1 and \
                                          d["last_fire"].value == 1,
            
            # 35.3: Grant数据带有corrupt标志
            "CP35.3_grant_corrupt": lambda d: d["grant_valid"].value == 1 and \
                                              d["grant_opcode"].value & 0x1 == 1 and \
                                              d["grant_corrupt"].value == 1,
            
            # 35.4: Grant完成后一拍的状态
            "CP35.4_grant_completion": lambda d: d["last_fire_r"].value == 1,
        },
        name="grant_data_collection"
    )

    # =================================================================
    # CP 36: 替换策略更新
    # 监控目标：victim更新信号
    # =================================================================
    g.add_watch_point(
        {
            "victim_valid": bundle.io._victim._vSetIdx._valid,
            "victim_bits": bundle.io._victim._vSetIdx._bits,
            "acquire_valid": bundle.io._mem._acquire._valid,
            "acquire_ready": bundle.io._mem._acquire._ready,
        },
        bins={
            # 36.1: Acquire成功时更新victim
            "CP36.1_victim_update": lambda d: d["victim_valid"].value == 1 and \
                                              d["acquire_valid"].value == 1 and \
                                              d["acquire_ready"].value == 1,
        },
        name="victim_replacement_update"
    )

    # =================================================================
    # CP 37: SRAM写回操作
    # 监控目标：Meta/Data写操作信号
    # =================================================================
    g.add_watch_point(
        {
            "meta_write_valid": bundle.io._meta_write._valid,
            "data_write_valid": bundle.io._data_write._valid,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "fetch_resp_corrupt": bundle.io._fetch._resp._bits._corrupt,
            "flush": bundle.io._flush,
            "fencei": bundle.io._fencei,
            "last_fire_r": bundle.ICacheMissUnit_.last_fire_r,
        },
        bins={
            # 37.1: 正常写SRAM（无flush/fencei/corrupt）
            "CP37.1_normal_sram_write": lambda d: d["meta_write_valid"].value == 1 and \
                                                  d["data_write_valid"].value == 1 and \
                                                  d["flush"].value == 0 and \
                                                  d["fencei"].value == 0 and \
                                                  d["last_fire_r"].value == 1,
            
            # 37.2: 有flush/fencei时不写SRAM但仍发送响应
            "CP37.2_no_write_with_flush": lambda d: d["meta_write_valid"].value == 0 and \
                                                    d["data_write_valid"].value == 0 and \
                                                    d["fetch_resp_valid"].value == 1 and \
                                                    (d["flush"].value == 1 or d["fencei"].value == 1) and \
                                                    d["last_fire_r"].value == 1,
            
            # 37.3: fetch响应总是生成（无论是否写SRAM）
            "CP37.3_fetch_resp_always": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                  d["last_fire_r"].value == 1,
            
            # 37.4: corrupt数据的响应
            "CP37.4_corrupt_response": lambda d: d["fetch_resp_valid"].value == 1 and \
                                                 d["fetch_resp_corrupt"].value == 1 and \
                                                 d["last_fire_r"].value == 1,
        },
        name="sram_write_operations"
    )

    # =================================================================
    # CP 38: Miss 完成响应
    # 监控目标：向 mainPipe/prefetchPipe 发出 Miss 完成响应
    # =================================================================
    g.add_watch_point(
        {
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "last_fire_r": bundle.ICacheMissUnit_.last_fire_r,
            "mshr_resp_blkPaddr": dut.GetInternalSignal("ICacheMissUnit_top.ICacheMissUnit.mshr_resp_blkPaddr", use_vpi=False),
            "mshr_resp_vSetIdx": dut.GetInternalSignal("ICacheMissUnit_top.ICacheMissUnit.mshr_resp_vSetIdx", use_vpi=False),
            "fetch_resp_blkPaddr": bundle.io._fetch._resp._bits._blkPaddr,
            "fetch_resp_vSetIdx": bundle.io._fetch._resp._bits._vSetIdx,
            "fetch_resp_waymask": bundle.io._fetch._resp._bits._waymask,
            "fetch_resp_corrupt": bundle.io._fetch._resp._bits._corrupt,
            "flush": bundle.io._flush,
            "fencei": bundle.io._fencei,
        },
        bins={
            # 38.1: 正常 Miss 完成响应
            # 当 last_fire_r 为高时，且内部mshr_resp有效数据时，无论是否有刷新信号，
            # io.fetch_resp.valid 都为高，且 fetch_resp.bits 数据正确更新
            "CP38.1_normal_miss_completion": lambda d: d["last_fire_r"].value == 1 and \
                                                       d["fetch_resp_valid"].value == 1 and \
                                                       (d["mshr_resp_blkPaddr"].value != 0 or d["mshr_resp_vSetIdx"].value != 0),
        },
        name="miss_completion_response"
    )

    # =================================================================
    # CP 39: 处理 flush/fencei
    # 监控目标：flush/fencei对MSHR状态和写回操作的影响
    # =================================================================
    g.add_watch_point(
        {
            "fencei": bundle.io._fencei,
            "flush": bundle.io._flush,
            "fetch_req_ready": bundle.io._fetch._req._ready,
            "prefetch_req_ready": bundle.io._prefetch_req._ready,
            "fetch_0_req_ready": bundle.ICacheMissUnit_._fetchMSHRs._0._io._req_ready,
            "fetch_0_acquire_valid": bundle.ICacheMissUnit_._fetchMSHRs._0._io._acquire_valid,
            "prefetch_0_req_ready": bundle.ICacheMissUnit_._prefetchMSHRs._0._io._req_ready,
            "prefetch_0_acquire_valid": bundle.ICacheMissUnit_._prefetchMSHRs._0._io._acquire_valid,
        },
        bins={
            # 39.1: MSHR 未发射前 fencei
            # 当 io.fencei 为高时，fetchMSHRs 和 prefetchMSHRs 的 io.req.ready 和 io.acquire.valid 均为低
            "CP39.1_fencei_before_fire": lambda d: d["fencei"].value == 1 and \
                                                   d["fetch_0_req_ready"].value == 0 and \
                                                   d["fetch_0_acquire_valid"].value == 0 and \
                                                   d["prefetch_0_req_ready"].value == 0 and \
                                                   d["prefetch_0_acquire_valid"].value == 0,
            
            # 39.2: MSHR 未发射前 flush  
            # 当 io.flush 为高时，只能发射 fetchMSHRs 的请求，prefetchMSHRs 被阻止
            "CP39.2_flush_before_fire": lambda d: d["flush"].value == 1 and \
                                                  d["fencei"].value == 0 and \
                                                  d["prefetch_0_req_ready"].value == 0,
        },
        name="flush_fencei_mshr_handling"
    )

    # =================================================================
    # CP 39.3: MSHR 已发射后 flush/fencei 的处理
    # 监控目标：发射后的写回抑制
    # =================================================================
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "fencei": bundle.io._fencei,
            "last_fire_r": bundle.ICacheMissUnit_.last_fire_r,
            "meta_write_valid": bundle.io._meta_write._valid,
            "data_write_valid": bundle.io._data_write._valid,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
        },
        bins={
            # 39.3: MSHR 已发射后 flush/fencei
            # 已经发射了请求，之后再有刷新信号，等数据回来但不写 SRAM
            # 写 SRAM 的信号均为低，但 fetch_resp 无影响
            "CP39.3_flush_fencei_after_fire": lambda d: (d["flush"].value == 1 or d["fencei"].value == 1) and \
                                                        d["last_fire_r"].value == 1 and \
                                                        d["meta_write_valid"].value == 0 and \
                                                        d["data_write_valid"].value == 0 and \
                                                        d["fetch_resp_valid"].value == 1,
        },
        name="flush_fencei_after_fire"
    )

    return g

def create_all_coverage_groups(bundle, dut):
    """
    创建所有覆盖点组合,包括FIFO和主要功能覆盖点
    """
    fifo_coverage = define_fifo_coverage(bundle, dut)
    main_coverage = define_missunit_coverage_groups(bundle, dut)
    
    return [fifo_coverage, main_coverage]