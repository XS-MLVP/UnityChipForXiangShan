import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.ICache import DUTICache
from ..env import ICacheEnv


@toffee_test.fixture
async def icache_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTICache)
    dut.InitClock("clock")
    start_clock(dut)
    icache_env = ICacheEnv(dut)
    yield icache_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
