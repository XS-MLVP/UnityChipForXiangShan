from .missunit_fixture import icachemissunit_env
from ..env import ICacheMissUnitEnv
import toffee_test


@toffee_test.testcase
async def test_smoke(icachemissunit_env: ICacheMissUnitEnv):
    await icachemissunit_env.agent.fencei_func(1)

@toffee_test.testcase
async def test_bundle_drive_fetch_req_inputs(icachemissunit_env: ICacheMissUnitEnv):
    dut_bundle = icachemissunit_env.bundle

    print("\n--- Testing Bundle: Driving fetch_req_valid ---")
    dut_bundle.io._fetch._req._valid.value = 1 # Corrected path
    await dut_bundle.step()
    assert dut_bundle.io._fetch._req._valid.value == 1
    print(f"Python side: dut_bundle.io._fetch._req._valid.value = {dut_bundle.io._fetch._req._valid.value}")

    dut_bundle.io._fetch._req._valid.value = 0 # Corrected path
    await dut_bundle.step()
    assert dut_bundle.io._fetch._req._valid.value == 0
    print(f"Python side: dut_bundle.io._fetch._req._valid.value = {dut_bundle.io._fetch._req._valid.value}")

    print("\n--- Testing Bundle: Driving fetch_req_bits_blkPaddr ---")
    test_addr = 0xABCD0000
    dut_bundle.io._fetch._req._bits._blkPaddr.value = test_addr # Corrected path
    await dut_bundle.step()
    assert dut_bundle.io._fetch._req._bits._blkPaddr.value == test_addr
    print(f"Python side: dut_bundle.io._fetch._req._bits._blkPaddr.value = {hex(dut_bundle.io._fetch._req._bits._blkPaddr.value)}")

    print("\n--- Testing Bundle: Driving fencei ---")
    # fencei is directly under _21Bundle (io)
    dut_bundle.io._fencei.value = 1 # This was likely correct before if _fencei exists directly under io
    await dut_bundle.step()
    assert dut_bundle.io._fencei.value == 1
    print(f"Python side: dut_bundle.io._fencei.value = {dut_bundle.io._fencei.value}")
    dut_bundle.io._fencei.value = 0
    await dut_bundle.step()
    assert dut_bundle.io._fencei.value == 0
    print(f"Python side: dut_bundle.io._fencei.value = {dut_bundle.io._fencei.value}")

    print("Bundle drive tests (Python side) completed.")

@toffee_test.testcase
async def test_bundle_read_fetch_req_ready(icachemissunit_env: ICacheMissUnitEnv):
    dut_bundle = icachemissunit_env.bundle
    print("\n--- Testing Bundle: Reading fetch_req_ready ---")
    ready_val = dut_bundle.io._fetch._req._ready.value
    print(f"Read dut_bundle.io._fetch._req._ready.value = {ready_val} (depends on DUT state)")
    assert ready_val in [0, 1], "fetch_req_ready should be 0 or 1"
    print("Bundle read test for fetch_req_ready (Python side) completed.")

@toffee_test.testcase
async def test_api_send_fetch_request_accepted(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_send_fetch_request` API can successfully
    send a request and the DUT accepts it (ready is high).
    """
    print("\n--- [API Test] Testing drive_send_fetch_request ---")
    
    # In an idle DUT, the fetch_req should be accepted immediately.
    accepted = await icachemissunit_env.agent.drive_send_fetch_request(
        blkPaddr=0x1000, 
        vSetIdx=0x1A
    )
    
    assert accepted is True, "drive_send_fetch_request should return True on success."
    print("API drive_send_fetch_request test passed.")


@toffee_test.testcase
async def test_api_fetch_request_generates_acquire(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that sending a fetch request via API correctly generates
    a memory acquire request from the DUT, captured by another API.
    This tests the link between request and acquire generation.
    """
    print("\n--- [API Test] Testing Request -> Acquire Flow ---")
    agent = icachemissunit_env.agent
    test_addr = 0x2000
    test_idx = 0x2B
    expected_mem_addr = test_addr << 6  # Assuming a 64-byte cache line (<< 6)

    # We need to try to send the request and get the acquire concurrently.
    send_result = await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()

    assert send_result is True, "Fetch request should have been accepted."
    assert acquire_info is not None, "Did not capture an acquire request."
    
    # The first fetch request should go to fetchMSHRs[0], which has source ID 0
    assert acquire_info["source"] == 0, f"Expected source ID 0, but got {acquire_info['source']}"
    assert acquire_info["address"] == expected_mem_addr, f"Expected address {hex(expected_mem_addr)}, but got {hex(acquire_info['address'])}"
    
    print("API Request -> Acquire flow test passed.")


@toffee_test.testcase
async def test_api_full_fetch_flow(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify the complete, end-to-end happy path for a fetch miss using APIs.
    (Updated with debugging steps)
    """
    print("\n--- [API Test] Testing Full End-to-End Fetch Flow ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle # For direct signal inspection
    
    # Test Data
    test_addr = 0x3000
    test_idx = 0x3C
    expected_mem_addr = test_addr << 6
    
    print("--- Debug: Running a few cycles post-reset to settle DUT ---")
    # check acquire valid
    if bundle.io._mem._acquire._valid.value == 1:
        print("Debug: Found an unexpected acquire valid on the first cycle after reset.")
        await agent.drive_acknowledge_acquire(cycles=1)
        print("Debug: Acknowledged the unexpected acquire. Waiting for it to deassert.")
        for _ in range(5):
            if bundle.io._mem._acquire._valid.value == 0:
                break
            await bundle.step()
        assert bundle.io._mem._acquire._valid.value == 0, "Unexpected acquire signal did not deassert."
    
    print("--- DUT is now presumed idle. Starting actual test. ---")
    # -----------------------

    # 1. Send Fetch Request (now we are sure the DUT is idle)
    print("Step 1: Sending fetch request.")
    accepted = await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    assert accepted, "Fetch request was not accepted when DUT should be idle."

    # 2. Capture acquire AND drive victim_way concurrently
    # We want to ensure that the acquire request is captured
    print("Step 2: Waiting for acquire and driving victim way.")
    
    acquire_info = await agent.drive_get_acquire_request(timeout_cycles=10)
    # assuming victim_way is 2 for this test
    await agent.drive_set_victim_way(way=2)

    
    assert acquire_info is not None, "Did not capture an acquire request after sending fetch_req."
    assert acquire_info["address"] == expected_mem_addr
    assert acquire_info["source"] == 0
    print(f"Step 2 Passed. Got correct acquire for source ID 0 and drove victim_way=2.")
    
    # 3. Acknowledge acquire
    print("Step 3: Acknowledging acquire request.")
    await agent.drive_acknowledge_acquire(cycles=1)
    
    # 4. Respond with Grant and wait for Fetch Response
    print("Step 4: Responding with Grant and waiting for Fetch Response.")
    grant_data = [0x1122334455667788_99AABBCCDDEEFF00, 0x00FF_EEDDCCBBAA99_8877665544332211]
    
    await agent.drive_respond_with_grant(source_id=acquire_info['source'], data_beats=grant_data)
    response_info = await agent.drive_get_fetch_response()
    
    assert response_info is not None, "Did not receive a fetch response."
    
    # 5. Verify the response, now including the waymask
    print("Step 5: Verifying fetch response contents.")
    assert response_info["blkPaddr"] == test_addr
    # check waymask 
    assert response_info["waymask"] == (1 << 2), f"Expected waymask for way 2, but got {response_info['waymask']}"
    
    print("API Full End-to-End Fetch Flow test passed.")



@toffee_test.testcase
async def test_api_grant_with_corruption(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that if a grant is sent with the corrupt flag, the final
    fetch_resp is still generated, but correctly propagates the corrupt flag.
     """
    print("\n--- [API Test] Testing Grant with Corruption ---")
    agent = icachemissunit_env.agent
    
    # --- Setup: Start a fetch miss ---
    test_addr, test_idx = 0x4000, 0x4D
    
    await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()
    
    assert acquire_info is not None, "Setup failed: Did not get acquire."
    source_id = acquire_info["source"]
    await agent.drive_acknowledge_acquire()
    
    # --- Act: send a Grant with corrupt ，and waiting for fetch_resp ---
    print("Act: Responding with corrupt Grant and waiting for Fetch Response.")
    grant_data = [0xAAAAAAAA, 0xBBBBBBBB]

    # send Grant and capture Response
    await agent.drive_respond_with_grant(
            source_id=source_id, 
            data_beats=grant_data, 
            is_corrupt_list=[False, True] # the second beat is corrupt
        )
    response_info = await agent.drive_get_fetch_response()

    # --- Assert: verifing the response，and the sign of corrupt is True ---
    print("Assert: Verifying the received response.")
    
    assert response_info is not None, "Did not receive a fetch response, which is unexpected."
    
    # verify the core content
    assert response_info["blkPaddr"] == test_addr, "Response blkPaddr mismatch."
    assert response_info["corrupt"] is True, "Corruption flag was NOT propagated to the fetch response."
    
    print("Verification passed: fetch_resp was generated and correctly marked as corrupt.")

@toffee_test.testcase
async def test_api_drive_prefetch_signal_directly(icachemissunit_env: ICacheMissUnitEnv):
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    # step 1: drive signal in this cycle
    agent.drive_prefetch_req(blkPaddr=0x9000, vSetIdx=0x99, valid=True)

    # step 2: push one cycle
    await bundle.step()

    # step 3: before next cycle need to check
    assert bundle.io._prefetch_req._valid.value == 1
    assert bundle.io._prefetch_req._bits._blkPaddr.value == 0x9000
    
    # step 4: cancel the prefetch request
    agent.drive_prefetch_req(0, 0, valid=False)
    await bundle.step()
    assert bundle.io._prefetch_req._valid.value == 0

@toffee_test.testcase
async def test_api_prefetch_data_assignment(icachemissunit_env: ICacheMissUnitEnv):
    """
    [CORRECTED VERSION]
    Goal: Verify that the low-level drive_prefetch_req API correctly assigns
    values to the DUT's input pins within a single clock cycle.
    """
    print("\n--- [API Verification] Testing prefetch addr/idx assignment ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    test_addr = 0xABCDE
    test_idx = 0x42

    # --- step 1: before this cycle，drive prefetch req ---
    print("Driving signals with low-level API 'drive_prefetch_req'.")
    agent.drive_prefetch_req(blkPaddr=test_addr, vSetIdx=test_idx, valid=True)

    # --- step 2: in this cycle，check the value in the Bundle  ---
    print("Verifying bundle values immediately after driving...")
    
    actual_addr = bundle.io._prefetch_req._bits._blkPaddr.value
    actual_idx = bundle.io._prefetch_req._bits._vSetIdx.value
    actual_valid = bundle.io._prefetch_req._valid.value
    
    print(f"  Expected Addr: {hex(test_addr)}, Actual Addr: {hex(actual_addr)}")
    print(f"  Expected Idx:  {hex(test_idx)},  Actual Idx:  {hex(actual_idx)}")
    print(f"  Expected Valid: 1,           Actual Valid: {actual_valid}")

    assert actual_addr == test_addr, "blkPaddr was not assigned correctly!"
    assert actual_idx == test_idx, "vSetIdx was not assigned correctly!"
    assert actual_valid == 1, "valid was not asserted!"
    
    # --- step 3: push to next cycle ---
    print("Advancing one clock cycle...")
    await bundle.step()
    
    # in this cycle，DUT will response ready=1
    assert bundle.io._prefetch_req._ready.value == 1, "DUT did not become ready."
    print("DUT correctly responded with ready=1.")
    
    # --- step 4: cancel drive and clean ---
    agent.drive_prefetch_req(0, 0, valid=False)
    await bundle.step()
    assert bundle.io._prefetch_req._valid.value == 0
    
    print("\n--- [API Verification] Data assignment test passed. ---")


@toffee_test.testcase
async def test_api_full_prefetch_flow(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify the complete end-to-end happy path for a PREFETCH miss.
    This is similar to the fetch flow, but uses prefetch APIs and expects a different source ID.
    """
    print("\n--- [API Test] Testing Full End-to-End PREFETCH Flow ---")
    agent = icachemissunit_env.agent
    
    # Test Data
    test_addr = 0x5000
    test_idx = 0x5E

    # 1. Send PREFETCH Request and wait for Acquire
    send_result = await agent.drive_send_prefetch_req(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()
    print(acquire_info)

    assert send_result and acquire_info is not None, "Failed to send prefetch or get acquire."
    
    source_id = acquire_info["source"]
    assert acquire_info["source"] == 4, f"Expected source ID 4 for prefetch, but got {acquire_info['source']}"
    print(f"Prefetch request correctly assigned to a prefetch MSHR with source ID: {source_id}")
    
    # --- use captured source_id ---
    await agent.drive_acknowledge_acquire(cycles=1)
    await agent.drive_respond_with_grant(source_id=source_id, data_beats=[0x1, 0x2])
    
    print("Verifying that a prefetch request ALSO generates a valid fetch_resp.")
    response_info = await agent.drive_get_fetch_response(timeout_cycles=10)
    
    assert response_info is not None, "A prefetch request SHOULD generate a fetch_resp, but it was not captured."
    
    # check the responsed content whether matched with prefetch
    assert response_info["blkPaddr"] == test_addr, "Response blkPaddr does not match the prefetch request."
    assert response_info["vSetIdx"] == test_idx, "Response vSetIdx does not match the prefetch request."
    print(f"Received fetch_resp for prefetch request: {response_info}")
    print("API Full End-to-End PREFETCH Flow test passed.")

@toffee_test.testcase
async def test_api_fetch_request_timeout(icachemissunit_env: ICacheMissUnitEnv):
    """
    [FINAL VERSION]
    Goal: Verify timeout logic by serially filling all 4 fetch MSHRs,
    adding a small delay between requests to handle internal DUT settling time.
    """
    print("\n--- [API Test] Testing fetch request API timeout ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    All_filled_fetch_count = 5
    NUM_FETCH_MSHRS = 4
    print(f"ASSUMPTION: DUT has {NUM_FETCH_MSHRS} fetch MSHRs.")

    # 1. 串行地填满所有 4 个 MSHR
    print(f"Step 1: Serially filling up all {NUM_FETCH_MSHRS} fetch MSHRs.")
    
    for i in range(All_filled_fetch_count):
        addr, idx = 0xA000 + i, 0xA0 + i
        print(f"\n The top io_fetch_req.ready.value is {bundle.io._fetch._req._ready.value}")
        if i < NUM_FETCH_MSHRS:
            print(f"\n--- Filling MSHR slot #{i} ---")
            for h in range(4):
                print(
                    f"fetchMSHRs.{h}.io.req.ready.value:",
                    getattr(
                        bundle.ICacheMissUnit_._fetchMSHRs, f"_{h}"
                    )._io._req_ready.value,
                )
                print(
                    f"fetchMSHRs.{h}.io.acquire.valid.value:",
                    getattr(
                        bundle.ICacheMissUnit_._fetchMSHRs, f"_{h}"
                    )._io._acquire_valid.value,
                )
            accepted = await agent.drive_send_fetch_request(addr, idx)
            assert accepted, f"Request to fill MSHR slot #{i} was not accepted."        
            acquire_info = await agent.drive_get_acquire_request()
            assert acquire_info is not None, f"Did not get acquire for request #{i}."    
            await agent.drive_acknowledge_acquire(cycles=1)
            print(f"Waiting 2 extra cycles for DUT to settle before next request...")
            await bundle.step(2)
        else:
            print(f"\nAll {NUM_FETCH_MSHRS} fetch MSHRs are now occupied.")
            print("we hope this filling will timeout.")
            print(f"\n--- Filling MSHR slot #{i} ---")
            for h in range(4):
                print(
                    f"fetchMSHRs.{h}.io.req.ready.value:",
                    getattr(
                        bundle.ICacheMissUnit_._fetchMSHRs, f"_{h}"
                    )._io._req_ready.value,
                )
                print(
                    f"fetchMSHRs.{h}.io.acquire.valid.value:",
                    getattr(
                        bundle.ICacheMissUnit_._fetchMSHRs, f"_{h}"
                    )._io._acquire_valid.value,
                )

            # If we try to fill more than NUM_FETCH_MSHRS, we expect a timeout
            print(f"\n The top io_fetch_req.ready.value is {bundle.io._fetch._req._ready.value}")
            print(f"\n--- Attempting to fill MSHR slot #{i} ---")
            timeout_result = await agent.drive_send_fetch_request(addr, idx)
            print(f"\n The top io_fetch_req.ready.value is {bundle.io._fetch._req._ready.value}")
            assert timeout_result is False, f"Request to fill MSHR slot #{i} " \
                "should have timed out as all slots are already filled."    
            print(f"Skipping MSHR slot #{i} as all {NUM_FETCH_MSHRS} slots are already filled.")
        # ---------------------------------------------
    print("\nAPI timeout logic test passed.")