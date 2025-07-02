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
    print("Bundle drive tests completed.")

@toffee_test.testcase
async def test_bundle_read_fetch_req_ready(icachemissunit_env: ICacheMissUnitEnv):
    dut_bundle = icachemissunit_env.bundle
    print("\n--- Testing Bundle: Reading fetch_req_ready ---")
    ready_val = dut_bundle.io._fetch._req._ready.value
    print(f"Read dut_bundle.io._fetch._req._ready.value = {ready_val} (depends on DUT state)")
    assert ready_val in [0, 1], "fetch_req_ready should be 0 or 1"
    print("Bundle read test for fetch_req_ready (Python side) completed.")

@toffee_test.testcase
async def test_fencei_work(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that fencei works by checking if it clears all MSHRs.
    """
    print("\n--- Testing fencei functionality ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    print("Before fencei:")
    # Print initial state of MSHRs
    for i in range(10):
        print(
            f"prefetchMSHRs.{i}.io.req.ready.value:",
            getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._req_ready.value,
        )
        print(
            f"prefetchMSHRs.{i}.io.acquire.valid.value:",
            getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._acquire_valid.value,
        )
    for i in range(4):
        print(
            f"fetchMSHRs.{i}.io.req.ready.value:",
            getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value,
        )
        print(
            f"fetchMSHRs.{i}.io.acquire.valid.value:",
            getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._acquire_valid.value,
        )
    # Step 1: Set fencei to 1
    await agent.fencei_func(1)
    await bundle.step(10)  # Wait for 10 cycles to ensure fencei is processed
    print("waited 10 cycles after setting fencei")
    print("\nAfter fencei = 1, all MSHRs should be cleared")
    # Step 2: Check if all MSHRs are cleared
    for i in range(10):
        assert getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._req_ready.value == 0, \
            f"prefetchMSHRs.{i} should be cleared."
        assert getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._acquire_valid.value == 0, \
            f"prefetchMSHRs.{i} acquire should be invalid."

    for i in range(4):
        assert getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value == 0, \
            f"fetchMSHRs.{i} should be cleared."
        assert getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._acquire_valid.value == 0, \
            f"fetchMSHRs.{i} acquire should be invalid."
    
    print("All MSHRs cleared successfully after fencei.")
    # Step 3: Set fencei to 0 (optional, but good practice)
    await agent.fencei_func(0)
    await bundle.step(10)  # Wait for another 10 cycles to ensure fencei is processed
    print("after setting fencei = 0, all MSHRs_ready should be 1,and all MSHRs_acquire_valid should be 0")
    # Check if MSHRs are ready again
    for i in range(10):
        assert getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._req_ready.value == 1, \
            f"prefetchMSHRs.{i} should be ready after fencei=0."
        assert getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._acquire_valid.value == 0, \
            f"prefetchMSHRs.{i} acquire should still be invalid after fencei=0."
    for i in range(4):
        assert getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value == 1, \
            f"fetchMSHRs.{i} should be ready after fencei=0."
        assert getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._acquire_valid.value == 0, \
            f"fetchMSHRs.{i} acquire should still be invalid after fencei=0."
    print("fencei test completed successfully.")

@toffee_test.testcase
async def test_set_flush(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_set_flush` API correctly sets the io_flush signal.
    """
    print("\n--- Testing drive_set_flush API ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    # Step 1: Set flush to 1
    await agent.drive_set_flush(True)
    assert bundle.io._flush.value == 1, "Flush signal should be set to 1."
    print("Flush signal set to 1.")

    # Step 2: Step the bundle to propagate the change
    await bundle.step()
    
    # Step 3: Set flush to 0
    await agent.drive_set_flush(False)
    assert bundle.io._flush.value == 0, "Flush signal should be set to 0."
    print("Flush signal set to 0.")

@toffee_test.testcase
async def test_set_victim_way(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_set_victim_way` API correctly sets the io_victim_way signal.
    """
    print("\n--- Testing drive_set_victim_way API ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    all_victim_ways = [0, 1, 2, 3]  # Assuming 4 ways for victim cache
    # Check if the victim way is set correctly
    for way in all_victim_ways:
        print(f"Setting victim way to {way}.")
        await agent.drive_set_victim_way(way)
        assert bundle.io._victim._way.value == way, f"Victim way should be set to {way}."
        print(f"Victim way set to {way}.")
        # Step the bundle to propagate the change
        await bundle.step()
    print("Victim way test completed successfully.")

@toffee_test.testcase
async def test_send_fetch_request(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_send_fetch_request` API can successfully
    send four requests and the DUT accepts them.Also, when send the fifth 
    request, the DUT should not accept it.
    """
    print("\n--- Testing drive_send_fetch_request API ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    send_list = [
        (0x1000, 0x1A),
        (0x2000, 0x2B),
        (0x3000, 0x3C),
        (0x4000, 0x4D),
        (0x2000, 0x2B),  # This one should be accepted again
        (0x5000, 0x5E)  # This one should not be accepted
    ]
    count = 0
    for blkPaddr, vSetIdx in send_list:
        print(f"Attempting to send fetch #{count} request: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        if count < 5:
            accepted = await agent.drive_send_fetch_request(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert accepted is True and bundle.io._fetch._req._ready.value == 1, f"Fetch request {count} should be accepted."
            count += 1
            print(f"Fetch request accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        else:
            accepted = await agent.drive_send_fetch_request(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert accepted is True and bundle.io._fetch._req._ready.value == 0 , f"Fetch request {count} should accepted but after that become not ready."
            print(f"Fetch request NOT accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")

    print("four fetch requests sent successfully, with the fifth one correctly rejected.")



@toffee_test.testcase
async def test_api_fetch_request_generates_acquire(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that sending a fetch request via API correctly generates
    a memory acquire request from the DUT, captured by another API.
    This tests the link between request and acquire generation.
    """
    print("\n--- [API Test] Testing Request -> Acquire Flow ---")
    fetch_and_acquire_count = 0
    agent = icachemissunit_env.agent
    test_addr = 0x1000
    test_idx = 0x1A
    expected_mem_addr = test_addr << 6
    # We need to try to send the request and get the acquire concurrently.
    send_result = await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()
    assert send_result is True, "Fetch request should have been accepted."
    assert acquire_info is not None, "Did not capture an acquire request."
    # The first fetch request should go to fetchMSHRs[0], which has source ID 0
    assert acquire_info["source"] == 0, f"Expected source ID {fetch_and_acquire_count}, but got {acquire_info['source']}"
    assert acquire_info["address"] == expected_mem_addr, f"Expected address {hex(expected_mem_addr)}, but got {hex(acquire_info['address'])}"
    fetch_and_acquire_count+=1
    
    print("API Request -> Acquire flow test passed.")


@toffee_test.testcase
async def test_api_full_fetch_flow(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify the complete, end-to-end happy path for a fetch miss using APIs.
    """
    print("\n--- [API Test] Testing Full End-to-End Fetch Flow ---")
    agent = icachemissunit_env.agent
    
    # Test Data
    test_addr = 0x3000
    test_idx = 0x3C
    expected_mem_addr = test_addr << 6

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
async def test_send_prefetch_request(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_send_fetch_request` API can successfully
    send four requests and the DUT accepts them.Also, when send the fifth 
    request, the DUT should not accept it.
    """
    print("\n--- Testing drive_send_fetch_request API ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    send_list = []
    for i in range(11):
        blkPaddr = 0x1000 + i * 0x1000
        vSetIdx = 0x1A + i
        send_list.append((blkPaddr, vSetIdx))
    # The first 10 requests should be accepted, the 11th one should be rejected
    count = 0
    for blkPaddr, vSetIdx in send_list:
        print(f"Attempting to send fetch #{count} request: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        if count < 10:
            accepted = await agent.drive_send_prefetch_req(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert accepted is True and bundle.io._prefetch_req._ready.value == 1, f"Fetch request {count} should be accepted and ready for next request."
            count += 1
            print(f"Fetch request accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        else:
            accepted = await agent.drive_send_prefetch_req(blkPaddr= 0x1000 + 2 * 0x1000, vSetIdx=0x1A + 2)
            assert accepted is True and bundle.io._prefetch_req._ready.value == 1,"Fetch request should be accepted again, because it is in prefetch MSHR."
            accepted = await agent.drive_send_prefetch_req(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert accepted is True and bundle.io._prefetch_req._ready.value == 0, f"Fetch request {count} should be accepted but after that become not ready."
            print(f"Fetch request NOT accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")

    print("prefetch requests sent successfully.")

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
