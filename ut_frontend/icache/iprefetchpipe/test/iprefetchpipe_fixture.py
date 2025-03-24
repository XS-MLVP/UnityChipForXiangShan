import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.IPrefetchPipe import DUTIPrefetchPipe
from ..env import IPrefetchPipeEnv

@toffee_test.fixture
async def iprefetchpipe_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTIPrefetchPipe)
    dut.InitClock("clock")
    start_clock(dut)
    iprefetchpipe_env = IPrefetchPipeEnv(dut)
    yield iprefetchpipe_env
    
    cur = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break