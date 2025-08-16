import toffee.funcov as fc
from toffee.funcov import CovGroup
from ..bundle import FtqRedirectMemBundle

def define_read0_coverage(bundle:FtqRedirectMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPort0")
    g.add_watch_point(
        {
            "ren": bundle.io._ren._0,
            "raddr": bundle.io._raddr._0
        },
        bins={  
            "read_when_addr_0": lambda d: d["ren"].value == 1 and d["raddr"].value == 0,
            "read_when_addr_31": lambda d: d["ren"].value == 1 and d["raddr"].value == 31
        }
    )
    return g

def define_read1_coverage(bundle:FtqRedirectMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPort1")
    g.add_watch_point(
        {
            "ren": bundle.io._ren._1,
            "raddr": bundle.io._raddr._1
        },
        bins={
            "read_when_addr_0": lambda d: d["ren"].value == 1 and d["raddr"].value == 0,
            "read_when_addr_31": lambda d: d["ren"].value == 1 and d["raddr"].value == 31
        }
    )
    return g

def define_read2_coverage(bundle:FtqRedirectMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPort2")
    g.add_watch_point(
        {
            "ren": bundle.io._ren._2,
            "raddr": bundle.io._raddr._2
        },
        bins={
            "read_when_addr_0": lambda d: d["ren"].value == 1 and d["raddr"].value == 0,
            "read_when_addr_31": lambda d: d["ren"].value == 1 and d["raddr"].value == 31
        }
    )
    return g

def define_write_coverage(bundle:FtqRedirectMemBundle, dut) -> CovGroup:
    g = CovGroup("WritePort")
    g.add_watch_point(
        {
            "wen": bundle.io._wen_0,
            "waddr": bundle.io._waddr_0
        },
        bins={
            "write_when_addr_0": lambda d: d["wen"].value == 1 and d["waddr"].value == 0,
            "write_when_addr_31": lambda d: d["wen"].value == 1 and d["waddr"].value == 31
        }
    )
    return g

def create_coverage_groups(bundle:FtqRedirectMemBundle,dut) -> list[CovGroup]:
    read0_coverage = define_read0_coverage(bundle,dut)
    read1_coverage = define_read1_coverage(bundle,dut)
    read2_coverage = define_read2_coverage(bundle,dut)
    write_coverage = define_write_coverage(bundle,dut)
    return [read0_coverage, read1_coverage, read2_coverage, write_coverage]


#  g = CovGroup("MissUnit_FIFO")
#     # create FIFO_internalsignals for FIFO functional coverage
#     FIFO_dict = {"enq_ptr_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_value",\
#                 "enq_ptr_flag":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_flag",\
#                 "enq_ptr_new_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_new_value",\
#                 "deq_ptr_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_value",\
#                 "deq_ptr_flag":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_flag",\
#                 "deq_ptr_new_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_new_value",\
#                 "full":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.full"
#                 }
#     # =================================================================
#     # CP 28.1 & 28.2 & 28.3: 正常入队 vs 入队翻转 vs 队满阻塞
#     # 监控目标：prefetch请求接口和其内部状态
#     # =================================================================
#     g.add_watch_point(
#         # 使用字典作为target，让lambda函数更易读
#         {
#             "enq_ready": bundle.priorityFIFO._io_enq._ready,
#             "enq_valid": bundle.priorityFIFO._io_enq._valid_T_probe,
#             "enq_ptr_value": dut.GetInternalSignal(FIFO_dict["enq_ptr_value"], use_vpi=False),
#             "enq_ptr_new_value": dut.GetInternalSignal(FIFO_dict["enq_ptr_new_value"], use_vpi=False),
#             "enq_ptr_flag": dut.GetInternalSignal(FIFO_dict["enq_ptr_flag"], use_vpi=False),
#             "enq_bits": bundle.prefetchDemux._io_chosen,
#             "deq_ptr_value": dut.GetInternalSignal(FIFO_dict["deq_ptr_value"], use_vpi=False),
#             "deq_ptr_flag": dut.GetInternalSignal(FIFO_dict["deq_ptr_flag"], use_vpi=False),
#             "full": dut.GetInternalSignal(FIFO_dict["full"], use_vpi=False)
#         },
#         bins={
#             # 28.1: 新请求到来，FIFO未满，成功入队 
#             "enq_when_not_full": lambda d: d["enq_ready"].value == 1 and \
#                                            d["enq_valid"].value == 1 and \
#                                            d["full"].value == 0 and \
#                                            d["enq_ptr_flag"].value == 0 and \
#                                            d["enq_ptr_value"].value == d["enq_bits"].value and \
#                                            d["enq_ptr_new_value"].value == d["enq_ptr_value"].value + 1,
            
#             # 28.2: 新请求到来，FIFO未满，入队将使FIFO满（指针到达边界）
#             "enq_when_will_full": lambda d: d["enq_ready"].value == 1 and \
#                                             d["enq_valid"].value == 1 and \
#                                             d["full"].value == 0 and \
#                                             d["enq_ptr_flag"].value == 0 and \
#                                             d["enq_ptr_new_value"].value == 0xA and d["enq_ptr_value"].value == 9, \
#             # 28.3: 新请求到来，FIFO已满，入队失败
#             "enq_blocked_when_full": lambda d: d["enq_ready"].value == 0 and\
#                                                d["full"].value == 1 and \
#                                                d["enq_ptr_value"].value == d["deq_ptr_value"].value and \
#                                                d["enq_ptr_flag"].value != d["deq_ptr_flag"].value
#         },
#         name="CP_Enqueue_Normal_vs_Full"
#     )