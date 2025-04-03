import toffee_test
import toffee
from dut.WayLookup import DUTWayLookup
from toffee import start_clock
from ..env import WayLookupEnv
import asyncio


@toffee_test.fixture
async def waylookup_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTWayLookup)
    dut.InitClock("clock")
    start_clock(dut)
    waylookup_env = WayLookupEnv(dut)
    yield waylookup_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
