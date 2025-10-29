import toffee_test
import toffee
from dut.WayLookup import DUTWayLookup
from toffee import start_clock, create_task
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
    coverage_groups_dict = create_waylookup_coverage_groups(waylookup_env.bundle, dut)
    
    # Add regular coverage groups for automatic sampling
    regular_groups = coverage_groups_dict["regular"]
    timing_groups = coverage_groups_dict["timing"]
    
    toffee_request.add_cov_groups(regular_groups)
    for coverage_group in regular_groups:
        toffee.info(f"Added regular coverage group: {coverage_group.name}")
    
    # Custom timing coverage groups (not added to auto-sampling)
    flush_timing_coverage = timing_groups[0]  # WayLookup_Flush_Timing_Coverage
    pointer_and_update_timing_coverage = timing_groups[1]  # WayLookup_Timing_Effects_Coverage
    
    # Define timing monitoring tasks using state checking (safer approach)
    async def timing_monitor():
        """Monitor timing events using state checking for precise timing coverage"""
        last_flush_state = 0
        last_read_fire = False
        last_write_fire = False
        last_update_valid = False
        flush_detected = False
        
        while True:
            try:
                # ===== Flush Timing Monitor =====
                current_flush = waylookup_env.bundle.io._flush.value
                if last_flush_state == 1 and current_flush == 0:
                    # Flush just went from high to low, sample one cycle later
                    flush_detected = True
                
                if flush_detected:
                    flush_timing_coverage.sample()
                    toffee.info("Sampled flush timing coverage")
                    flush_detected = False
                
                # ===== Pointer and Update Effects Monitor =====
                read_ptr_signal = dut.GetInternalSignal("WayLookup_top.WayLookup.readPtr_value", use_vpi=False)
                write_ptr_signal = dut.GetInternalSignal("WayLookup_top.WayLookup.writePtr_value", use_vpi=False)
                
                current_read_ptr = read_ptr_signal.value
                current_write_ptr = write_ptr_signal.value
                
                # Check fire signals for timing detection
                current_read_fire = (waylookup_env.bundle.io._read._valid.value == 1 and 
                                   waylookup_env.bundle.io._read._ready.value == 1)
                current_write_fire = (waylookup_env.bundle.io._write._valid.value == 1 and 
                                    waylookup_env.bundle.io._write._ready.value == 1)
                current_update_valid = waylookup_env.bundle.io._update._valid.value == 1
                
                # Sample pointer and update effects after fire operations
                should_sample_effects = False
                
                # Sample after read/write fire (for pointer updates) 
                if last_read_fire or last_write_fire:
                    should_sample_effects = True
                    toffee.info(f"Sampling after fire: read_fire={last_read_fire}, write_fire={last_write_fire}")
                
                # Sample after update operation (for entries updates)
                if last_update_valid:
                    should_sample_effects = True
                    toffee.info("Sampling after update operation")
                
                # Sample effects coverage if needed
                if should_sample_effects:
                    pointer_and_update_timing_coverage.sample()
                    toffee.info(f"Sampled timing effects: read_ptr={current_read_ptr}, write_ptr={current_write_ptr}")
                
                # Update state for next cycle
                last_flush_state = current_flush
                last_read_fire = current_read_fire
                last_write_fire = current_write_fire
                last_update_valid = current_update_valid
                
                # Wait one cycle
                await waylookup_env.bundle.step(1)
                
            except Exception as e:
                toffee.info(f"Timing monitor exception: {e}")
                await waylookup_env.bundle.step(10)
    
    # Start timing monitoring task in background
    create_task(timing_monitor())
    toffee.info("Started background timing coverage monitoring task")
    
    yield waylookup_env

    # Add timing coverage groups to the request for final reporting
    toffee_request.cov_groups.extend(timing_groups)
    toffee.info(f"Added {len(timing_groups)} timing coverage groups for final reporting")

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
