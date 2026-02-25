import toffee_test
from dut.NewIFU import DUTNewIFU
from toffee import start_clock
from ..env import IFUTopEnv
from .ckpt_mmio import get_coverage_group_mmio
from .ckpt_subs import get_coverage_group_sub_modules
from .ckpt_tops import get_coverage_group_tops

# 可以在这里添加覆盖组

@toffee_test.fixture
async def ifu_top_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    # version_check()
    dut: DUTNewIFU = toffee_request.create_dut(DUTNewIFU, clock_name="clock")
    start_clock(dut)
    dut.reset.value = 1
    dut.Step()
    dut.reset.value = 0 
    dut.Step()
    ifu_env_cur = IFUTopEnv(dut)
    mmio_group = get_coverage_group_mmio(ifu_env_cur)
    sub_modules_group = get_coverage_group_sub_modules(ifu_env_cur)
    top_group = get_coverage_group_tops(ifu_env_cur)
    
    ifu_env_cur.mmio_group = mmio_group
    ifu_env_cur.submodules_group = sub_modules_group
    ifu_env_cur.top_group = top_group
    
    toffee_request.add_cov_groups([mmio_group,\
        sub_modules_group,\
            top_group])
    
    yield ifu_env_cur

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break