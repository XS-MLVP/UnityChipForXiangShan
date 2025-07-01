import toffee.funcov as fc
from toffee.funcov import CovGroup
from comm import UT_FCOV
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

def get_cover_group_of_receive_prefetch_quest(dut: DUTIPrefetchPipe) -> CovGroup:
    group = CovGroup(UT_FCOV("../../receive_prefetch_quest"))
    group.add_watch_point(
        dut,
        {
            "prefetch start address": check_prefetch_start_address,
            "prefetch next line address": check_prefetch_nextline_address,
            "prefetch is soft prefetch": check_prefetch_is_soft_prefetch,
            "prefetch double line": check_prefetch_double_line,
            "prefetch ftq idx flag": check_prefetch_ftq_idx_flag,
            "prefetch ftq idx value": check_prefetch_ftq_idx_value,
            "prefetch backend exception 0": check_prefetch_backend_exception_0,
            "prefetch backend exception 1": check_prefetch_backend_exception_1,
        },
        name="receive_prefetch_quest",
    )

    return group
