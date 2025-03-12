import os
import random
import toffee_test
import toffee
from dut.LoadQueueRAW import DUTLoadQueueRAW
from .checkpoints_rar_static import init_rar_funcov
from ..util.dataclass import IOQuery, IORedirect, Ptr, StoreIn
from ..env.LoadQueueRAWEnv import LoadQueueRAWEnv



@toffee_test.fixture
async def loadqueue_raw_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTLoadQueueRAW, "clock")
    toffee.start_clock(dut)
    env = LoadQueueRAWEnv(dut)
    toffee_request.add_cov_groups(init_rar_funcov(env))
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
