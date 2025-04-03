import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.ICacheMissUnit import DUTICacheMissUnit
from ..env import ICacheMissUnitEnv


@toffee_test.fixture
async def icachemissunit_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTICacheMissUnit)
    dut.InitClock("clock")
    start_clock(dut)
    icachemissunit_env = ICacheMissUnitEnv(dut)
    yield icachemissunit_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
