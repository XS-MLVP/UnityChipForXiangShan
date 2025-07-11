import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.ICacheMissUnit import DUTICacheMissUnit
from ..env import ICacheMissUnitEnv
from ..env.missunit_coverage import define_missunit_coverage_groups
from ..env.missunit_coverage import define_fifo_coverage

@toffee_test.fixture
async def icachemissunit_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTICacheMissUnit)
    start_clock(dut)
    icachemissunit_env = ICacheMissUnitEnv(dut)
    icachemissunit_env.dut.reset.value = 1
    icachemissunit_env.dut.Step(10)
    icachemissunit_env.dut.reset.value = 0
    icachemissunit_env.dut.Step(10)
    # print(f"all signals: {icachemissunit_env.dut.GetInternalSignalList(use_vpi=False)}")
    dut.InitClock("clock")
    print("--- [FIXTURE SETUP] Defining FIFO functional coverage... ---")
    fifo_coverage_group = define_fifo_coverage(icachemissunit_env.bundle,dut)
    toffee_request.add_cov_groups(fifo_coverage_group)
    print("--- [FIXTURE SETUP] Defining MISSUNIT functional coverage... ---")
    missunit_coverage_group = define_missunit_coverage_groups(icachemissunit_env.bundle)
    toffee_request.add_cov_groups(missunit_coverage_group)


    yield icachemissunit_env
    dut.StepRis(fifo_coverage_group.sample)
    dut.StepRis(missunit_coverage_group.sample)
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
