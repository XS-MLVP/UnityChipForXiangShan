import asyncio
import toffee
import toffee_test
from toffee import start_clock, create_task
from dut.ICacheMissUnit import DUTICacheMissUnit
from ..env import ICacheMissUnitEnv
from ..env.missunit_coverage import create_all_coverage_groups

@toffee_test.fixture
async def icachemissunit_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTICacheMissUnit)
    start_clock(dut)
    icachemissunit_env = ICacheMissUnitEnv(dut)
    icachemissunit_env.dut.reset.value = 1
    icachemissunit_env.dut.Step(10)
    icachemissunit_env.dut.reset.value = 0
    icachemissunit_env.dut.Step(10)
    # all_signal_list = icachemissunit_env.dut.GetInternalSignalList(use_vpi=False)
    # for i in all_signal_list:
    #    print(f"Signal: {i}")
    # toffee.info(f"all signals: {icachemissunit_env.dut.GetInternalSignalList(use_vpi=False)}")
    dut.InitClock("clock")
    
    toffee.info("--- [FIXTURE SETUP] Defining all functional coverage groups... ---")
    coverage_info = create_all_coverage_groups(icachemissunit_env.bundle, dut)
    regular_cov_groups = coverage_info["regular"]
    timing_cov_groups = coverage_info["timing"]
    # Add regular coverage groups to the test request
    for coverage_group in regular_cov_groups:
        toffee_request.add_cov_groups(coverage_group)
        toffee.info(f"Added coverage group: {coverage_group.name}")

    timing_task = None
    if timing_cov_groups:
        last_fire_r_sig = dut.GetInternalSignal(
            "ICacheMissUnit_top.ICacheMissUnit.last_fire_r", use_vpi=False
        )

        async def timing_monitor():
            prev_last_fire = 0
            try:
                while True:
                    grant_valid = icachemissunit_env.bundle.io._mem._grant._valid.value
                    meta_valid = icachemissunit_env.bundle.io._meta_write._valid.value
                    data_valid = icachemissunit_env.bundle.io._data_write._valid.value
                    fetch_resp_valid = icachemissunit_env.bundle.io._fetch._resp._valid.value
                    flush_val = icachemissunit_env.bundle.io._flush.value
                    fencei_val = icachemissunit_env.bundle.io._fencei.value
                    curr_last_fire = last_fire_r_sig.value
                    should_sample = any(
                        [
                            grant_valid == 1,
                            meta_valid == 1,
                            data_valid == 1,
                            fetch_resp_valid == 1,
                            flush_val == 1,
                            fencei_val == 1,
                            curr_last_fire == 1,
                            prev_last_fire == 1,
                        ]
                    )
                    if should_sample:
                        for cov_group in timing_cov_groups:
                            cov_group.sample()
                    prev_last_fire = curr_last_fire
                    await icachemissunit_env.bundle.step()
            except asyncio.CancelledError:
                pass
            except Exception as exc:
                toffee.info(f"[TimingCov] monitor exception: {exc}")

        timing_task = create_task(timing_monitor())
        timing_task.set_name("missunit_timing_cov")

    yield icachemissunit_env
    
    if timing_task:
        timing_task.cancel()
        try:
            await timing_task
        except asyncio.CancelledError:
            pass

    # Include timing coverage groups in the final report
    toffee_request.cov_groups.extend(timing_cov_groups)

    # Sample all coverage groups
    for coverage_group in regular_cov_groups + timing_cov_groups:
        dut.StepRis(coverage_group.sample)
        
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
