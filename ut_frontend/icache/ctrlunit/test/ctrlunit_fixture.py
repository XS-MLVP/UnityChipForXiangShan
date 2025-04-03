import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.ICacheCtrlUnit import DUTICacheCtrlUnit
from ..env import CtrlUnitEnv


@toffee_test.fixture
async def ctrlunit_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTICacheCtrlUnit)
    dut.InitClock("clock")
    start_clock(dut)
    ctrlunit_env = CtrlUnitEnv(dut)
    yield ctrlunit_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
