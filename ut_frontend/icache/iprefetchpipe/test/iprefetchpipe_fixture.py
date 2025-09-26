import asyncio
import toffee
import toffee_test
from toffee import start_clock
from dut.IPrefetchPipe import DUTIPrefetchPipe
from ..env import IPrefetchPipeEnv
from ..env.watch_point import create_iprefetchpipe_coverage_groups

@toffee_test.fixture
async def iprefetchpipe_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTIPrefetchPipe)
    dut.InitClock("clock")
    start_clock(dut)
    iprefetchpipe_env = IPrefetchPipeEnv(dut)
    iprefetchpipe_env.dut.reset.value = 1
    iprefetchpipe_env.dut.Step(10)
    iprefetchpipe_env.dut.reset.value = 0
    iprefetchpipe_env.dut.Step(10)
    #all_signals = dut.GetInternalSignalList(use_vpi=True)
    #for signal in all_signals:
    #    print(f"Internal Signal: {signal}")
    coverage_groups = create_iprefetchpipe_coverage_groups(iprefetchpipe_env.bundle, dut)
    for coverage_group in coverage_groups:
        toffee_request.add_cov_groups(coverage_group)
        print(f"Added coverage group: {coverage_group.name}")
    yield iprefetchpipe_env
    # Sample all coverage groups at the end
    for coverage_group in coverage_groups:
        dut.StepRis(coverage_group.sample)
        print(f"Sampled coverage group: {coverage_group.name}")

    cur = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break