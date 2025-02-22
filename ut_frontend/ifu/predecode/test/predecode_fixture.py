import toffee_test
from dut.PreDecode import DUTPreDecode
from ..env import PreDecodeEnv
from toffee import start_clock
import toffee.funcov as fc
from comm import UT_FCOV, module_name_with, get_version_checker

grp = fc.CovGroup(UT_FCOV("../../CLASSIC"))

@toffee_test.fixture
async def predecode_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTPreDecode)
    start_clock(dut)
    predecode_env = PreDecodeEnv(dut)
    yield predecode_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break