import toffee_test
import toffee
from dut.WayLookup import DUTWayLookup
from toffee import start_clock
from ..env import WayLookupEnv
from ..env.waylookup_functionalcoverage import create_waylookup_coverage_groups
import asyncio


@toffee_test.fixture
async def waylookup_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTWayLookup)
    dut.InitClock("clock")
    start_clock(dut)
    waylookup_env = WayLookupEnv(dut)
    
    # Initialize reset sequence
    waylookup_env.dut.reset.value = 1
    waylookup_env.dut.Step(10)
    waylookup_env.dut.reset.value = 0
    waylookup_env.dut.Step(10)
    
    toffee.info("--- [FIXTURE SETUP] Defining WayLookup functional coverage groups... ---")
    coverage_groups = create_waylookup_coverage_groups(waylookup_env.bundle, dut)
    # toffee.info(f"all signals: {waylookup_env.dut.GetInternalSignalList(use_vpi=False)}")
    
    # Add all coverage groups to the test request
    for coverage_group in coverage_groups:
        toffee_request.add_cov_groups(coverage_group)
        toffee.info(f"Added coverage group: {coverage_group.name}")
    
    yield waylookup_env

    # Sample all coverage groups at the end
    for coverage_group in coverage_groups:
        dut.StepRis(coverage_group.sample)
        toffee.info(f"Sampled coverage group: {coverage_group.name}")

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
