import asyncio,toffee,toffee_test
from toffee import start_clock
from dut.FtqRedirectMem import DUTFtqRedirectMem
from ..env import FtqRedirectMemEnv
from ..env.ftq_redirect_mem_coverage import create_coverage_groups

@toffee_test.fixture
async def ftq_redirect_mem_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.INFO)
    dut = toffee_request.create_dut(DUTFtqRedirectMem)
    start_clock(dut)
    ftq_redirect_mem_env = FtqRedirectMemEnv(dut)
    ftq_redirect_mem_env.dut.reset.value = 1
    ftq_redirect_mem_env.dut.Step(10)
    ftq_redirect_mem_env.dut.reset.value = 0
    ftq_redirect_mem_env.dut.Step(10)
    print(f"all signals: {ftq_redirect_mem_env.dut.GetInternalSignalList(use_vpi=False)}")
    dut.InitClock("clock")
    
    print("--- [FIXTURE SETUP] Defining all functional coverage groups... ---")
    coverage_groups = create_coverage_groups(ftq_redirect_mem_env.bundle, dut)
    
    # Add all coverage groups to the test request
    for coverage_group in coverage_groups:
        toffee_request.add_cov_groups(coverage_group)
        print(f"Added coverage group: {coverage_group.name}")

    yield ftq_redirect_mem_env
    
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