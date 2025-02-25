import toffee_test
import toffee
from dut.LoadQueueRAR import DUTLoadQueueRAR
from ..env import LoadQueueRAREnv

@toffee_test.fixture
async def frontend_trigger_env(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(DUTLoadQueueRAR)
    # toffee_request.add_cov_groups(pred_checker_cover_point(dut))
    dut.InitClock("clock")
    toffee.start_clock(dut)
    env = LoadQueueRAREnv(dut)
    # await env.agent.reset()
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
