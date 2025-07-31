import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.ICacheMainPipe import DUTICacheMainPipe
from ..env.mainpipe_functionalcoverage import create_mainpipe_coverage_groups
from ..env import ICacheMainPipeEnv


@toffee_test.fixture
async def icachemainpipe_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.ERROR)
    dut = toffee_request.create_dut(DUTICacheMainPipe)
    dut.InitClock("clock")
    start_clock(dut)
    icachemainpipe_env = ICacheMainPipeEnv(dut)
    icachemainpipe_env.dut.reset.value = 1
    icachemainpipe_env.dut.Step(10)
    icachemainpipe_env.dut.reset.value = 0
    icachemainpipe_env.dut.Step(10)
    # internallist = icachemainpipe_env.dut.GetInternalSignalList(use_vpi=False)
    # print(f"Found {len(internallist)} internal signals:")
    # for i in internallist:
    #    print(f"  - {i}")
    print("------ [FIXTURE SETUP] Defining ICacheMainPipe functional coverage groups... ------")
    coverage_groups = create_mainpipe_coverage_groups(icachemainpipe_env.bundle, dut)
    for coverage_group in coverage_groups:
        toffee_request.add_cov_groups(coverage_group)
        print(f"Added coverage group: {coverage_group.name}")
    
    yield icachemainpipe_env

    # Sample all coverage groups at the end
    for coverage_group in coverage_groups:
        dut.StepRis(coverage_group.sample)
        print(f"Sampled coverage group: {coverage_group.name}")

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
