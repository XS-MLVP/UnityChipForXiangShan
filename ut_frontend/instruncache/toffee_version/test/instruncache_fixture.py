import toffee_test
from comm import get_version_checker

from dut.InstrUncache import DUTInstrUncache
#from comm.functions import UT_FCOV, module_name_with
#import toffee.funcov as fc
from toffee import *
from ..env import InstrUncacheEnv
from ..bundle import InstrUncacheIOBundle


version_check = get_version_checker("openxiangshan-kmh-*")


@toffee_test.fixture
async def instruncache_fixture(toffee_request: toffee_test.ToffeeRequest):
#    import asyncio
    version_check()
    dut = toffee_request.create_dut(DUTInstrUncache, "clock")
    start_clock(dut)


    instruncache_bundle = InstrUncacheIOBundle()
    instruncache_bundle.bind(dut)

    return InstrUncacheEnv(instruncache_bundle)

#    cur_loop = asyncio.get_event_loop()
#    for task in asyncio.all_tasks(cur_loop):
#        if task.get_name() == "__clock_loop":
#            task.cancel()
#            try:
#                await task
#            except asyncio.CancelledError:
#                break

