import toffee_test
from comm import get_version_checker

from dut.RVCExpander import DUTRVCExpander
from comm.functions import UT_FCOV, module_name_with
import toffee.funcov as fc
from toffee import *


version_check = get_version_checker("openxiangshan-kmh-*")

gr = fc.CovGroup(UT_FCOV("../../../TOFFEE"))
# gr = fc.CovGroup("114514")

from ..env import RVCExpanderEnv

def hit_ill_watcher(expect:bool):
    def ill_hit(dut:DUTRVCExpander):
        return getattr(dut, "io_ill") == expect
    return ill_hit

def init_rvc_expander_funcov(dut:DUTRVCExpander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""
    
    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR. The instruction is not illegal
    #    - bin SUCCE. The instruction is not expanded
    g.add_watch_point(dut, {
                                "ERROR": lambda d:  getattr(dut, "io_ill").value == False,
                                "SUCCE": lambda d:  getattr(dut, "io_ill").value == True ,
                          }, name = "RVC_EXPAND_RET")
    # 2. Add point RVC_EXPAND_16B_RANGE to check expander input range
    #   - bin RANGE[start-end]. The instruction is in the range of the compressed instruction set
    # This check point is added in case 'test_rv_decode.test_rvc_expand_16bit_full' dynamically, see the test case for details

    # 3. Add point RVC_EXPAND_32B_RANGE to check expander input range
    #   - bin RANGE[start-end]. The instruction is in the range of the 32bit instruction set
    # This check point is added in case 'test_rv_decode.test_rvc_expand_32bit_full' dynamically, see the test case for details

    # 4. Add point RVC_EXPAND_32B_BITS to check expander function coverage
    #   - bin BITS[0-31]. The instruction is expanded to the corresponding 32-bit instruction
    def _check_pos(i):
        def check(dut):
            return getattr(dut, "io_in").value & (1<<i) != 0
        return check
    g.add_watch_point(dut, {
                                  "POS_%d"%i: _check_pos(i)
                                   for i in range(32)
                                },
                      name="RVC_EXPAND_32B_BITS")

    # 5. Reverse mark function coverage to the check point
    def _M(name):
        # get the module name
        return module_name_with(name, "../test_rvc")

    #  - mark RVC_EXPAND_RET
    g.mark_function("RVC_EXPAND_RET",     _M(["test_rvc_expand_16bit_full",
                                              "test_rvc_expand_32bit_full",
                                              "test_rvc_expand_32bit_randomN"]), bin_name=["ERROR", "SUCCE"])
    #  - mark RVC_EXPAND_16B_RANGE
    g.mark_function("RVC_EXPAND_32B_BITS", _M("test_rvc_expand_32bit_randomN"), bin_name=["POS_*"], raise_error=False)




@toffee_test.fixture
async def rvc_expander(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    version_check()
    dut = toffee_request.create_dut(DUTRVCExpander)
    start_clock(dut)
    init_rvc_expander_funcov(dut, gr)
    
    toffee_request.add_cov_groups([gr])
    expander = RVCExpanderEnv(dut)
    yield expander

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break