import toffee.funcov as fc
from toffee.funcov import CovGroup



def define_fifo_coverage(bundle,dut):
    """
    Defines the functional coverage points for the ICacheMissUnit's FIFO.
    
    Args:
        bundle: The top-level ICacheMissUnitBundle object.
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

def define_missunit_coverage_groups(bundle):
    """
    define functional coverage groups of ICacheMissUnit.
    """
    g = CovGroup("MissUnit_Main_Coverage")

    # =================================================================
    # CP 31.1: accept new fetch 31.2:process existed fetch 
    #    31.3:low index fetch priority enqueue to MSHR
    # Monitoring target：fetch request interface and its internal state
    #                    MSHR interface and its internal state      
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
    # CP 32.1: accept new prefetch 32.2:process existed prefetch 
    #    32.3:low index prefetch priority enqueue to MSHR
    # Monitoring target：presfetch request interface and its internal state
    #                    MSHR interface and its internal state      
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

    return g