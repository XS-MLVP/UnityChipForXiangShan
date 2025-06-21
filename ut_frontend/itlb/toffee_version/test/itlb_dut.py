import toffee_test
import toffee
from operator import *
from ..env import ItlbEnv
from dut.TLB import DUTTLB
import toffee.funcov as fc
from comm.functions import UT_FCOV, module_name_with

# module path is ut_frontend.ifu.itlb.toffee_version.test.itlb_dut.py
#gr = fc.CovGroup(UT_FCOV("../../../../itlb"))



@toffee_test.fixture
async def itlb_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(DUTTLB)
    dut.InitClock("clock")
    toffee.start_clock(dut)
    env = ItlbEnv(dut)
    yield env
    
    import asyncio
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
            