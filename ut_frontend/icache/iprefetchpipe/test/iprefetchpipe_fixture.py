import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.IPrefetchPipe import DUTIPrefetchPipe
from ..env import IPrefetchPipeEnv
from .watch_point import get_cover_group_of_receive_prefetch_quest

@toffee_test.fixture
async def iprefetchpipe_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTIPrefetchPipe)
    dut.InitClock("clock")
    start_clock(dut)
    iprefetchpipe_env = IPrefetchPipeEnv(dut)
    toffee_request.add_cov_groups([get_cover_group_of_receive_prefetch_quest(dut)])
    iprefetchpipe_env.dut.reset.value = 1
    iprefetchpipe_env.dut.Step(10)
    iprefetchpipe_env.dut.reset.value = 0
    iprefetchpipe_env.dut.Step(10)
    yield iprefetchpipe_env

    cur = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break