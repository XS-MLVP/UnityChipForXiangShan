import toffee_test
from dut.NewIFU import DUTNewIFU
from toffee import start_clock
from ..env import IFUTopEnv


@toffee_test.fixture
async def ifu_top_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    # version_check()
    dut = toffee_request.create_dut(DUTNewIFU)
    start_clock(dut)
    ifu_env_cur = IFUTopEnv(dut)
    yield ifu_env_cur

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break