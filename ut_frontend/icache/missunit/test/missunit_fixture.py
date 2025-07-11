import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.ICacheMissUnit import DUTICacheMissUnit
from ..env import ICacheMissUnitEnv
from ..env.missunit_coverage import create_all_coverage_groups

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
    
    print("--- [FIXTURE SETUP] Defining all functional coverage groups... ---")
    coverage_groups = create_all_coverage_groups(icachemissunit_env.bundle, dut)
    
    # Add all coverage groups to the test request
    for coverage_group in coverage_groups:
        toffee_request.add_cov_groups(coverage_group)
        print(f"Added coverage group: {coverage_group.name}")

    yield icachemissunit_env
    
    # Sample all coverage groups
    for coverage_group in coverage_groups:
        dut.StepRis(coverage_group.sample)
        
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
