import asyncio,toffee,toffee_test
from toffee import start_clock
from dut.FtbEntryMem import DUTFtbEntryMem
from ..env import FtbEntryMemEnv, create_coverage_groups

@toffee_test.fixture
async def ftb_entry_mem_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.INFO)
    dut = toffee_request.create_dut(DUTFtbEntryMem)
    start_clock(dut)
    ftb_entry_mem_env = FtbEntryMemEnv(dut)
    ftb_entry_mem_env.dut.reset.value = 1
    ftb_entry_mem_env.dut.Step(10)
    ftb_entry_mem_env.dut.reset.value = 0
    ftb_entry_mem_env.dut.Step(10)
    # print(f"all signals: {ftb_entry_mem_env.dut.GetInternalSignalList(use_vpi=False)}")
    dut.InitClock("clock")
    
    print("--- [FIXTURE SETUP] Defining all functional coverage groups... ---")
    coverage_groups = create_coverage_groups(ftb_entry_mem_env.bundle, dut)
    
    # Add all coverage groups to the test request
    for g in coverage_groups:
        toffee_request.add_cov_groups(g)
        dut.StepRis(lambda x: g.sample())
        print(f"Added coverage group: {g.name}")
        
    yield ftb_entry_mem_env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break