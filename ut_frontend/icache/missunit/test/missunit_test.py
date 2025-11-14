from .missunit_fixture import icachemissunit_env
from ..env import ICacheMissUnitEnv
import toffee_test
import toffee

def get_internal_signal(dut, signal_name:str):
    signal_dict = {
        "enq_ptr_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_value",\
        "enq_ptr_flag":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_flag",\
        "enq_ptr_new_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.enq_ptr_new_value",\
        "enq_ready":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.__Vtogcov__io_enq_ready",\
        "enq_valid":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.__Vtogcov__io_enq_valid",\
        "deq_ptr_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_value",\
        "deq_ptr_flag":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_flag",\
        "deq_ptr_new_value":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.deq_ptr_new_value",\
        "deq_ready":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.__Vtogcov__io_deq_ready",\
        "deq_valid":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.__Vtogcov__io_deq_valid",\
        "fifo_deq_bits":"ICacheMissUnit_top.ICacheMissUnit._priorityFIFO_io_deq_bits",\
        "full":"ICacheMissUnit_top.ICacheMissUnit.priorityFIFO.full",\

        "enq_bits":"ICacheMissUnit_top.ICacheMissUnit._prefetchDemux_io_chosen",\
        
        "fetch_demux_valid":"ICacheMissUnit_top.ICacheMissUnit.fetchDemux.__Vtogcov__io_in_valid",\
        "fetch_hit":"ICacheMissUnit_top.ICacheMissUnit.fetchHit",\
        "prefetch_demux_valid":"ICacheMissUnit_top.ICacheMissUnit.prefetchDemux.__Vtogcov__io_in_valid",\
        "prefetch_hit":"ICacheMissUnit_top.ICacheMissUnit.prefetchHit",\
        "last_fire":"ICacheMissUnit_top.ICacheMissUnit.last_fire",\
        "last_fire_r":"ICacheMissUnit_top.ICacheMissUnit.last_fire_r",\
        "io_mem_acquire_bits_source":"ICacheMissUnit_top.io_mem_acquire_bits_source",\
        "readBeatCnt":"ICacheMissUnit_top.ICacheMissUnit.readBeatCnt",\
        "respDataReg_0":"ICacheMissUnit_top.ICacheMissUnit.respDataReg_0",\
        "respDataReg_1":"ICacheMissUnit_top.ICacheMissUnit.respDataReg_1",\
        "id_r":"ICacheMissUnit_top.ICacheMissUnit.id_r",\
        "corrupt_r":"ICacheMissUnit_top.ICacheMissUnit.corrupt_r",\
        "victim_valid":"ICacheMissUnit_top.io_victim_vSetIdx_valid",\
        "mshr_resp_way":"ICacheMissUnit_top.ICacheMissUnit.mshr_resp_way",\
        "mshr_resp_blkPaddr":"ICacheMissUnit_top.ICacheMissUnit.mshr_resp_blkPaddr",\
        "mshr_resp_vSetIdx":"ICacheMissUnit_top.ICacheMissUnit.mshr_resp_vSetIdx",\
        "refill_done_r_counter":"ICacheMissUnit_top.ICacheMissUnit.refill_done_r_counter",\
    }
    return dut.GetInternalSignal(signal_dict[signal_name], use_vpi=False).value



@toffee_test.testcase
async def test_smoke(icachemissunit_env: ICacheMissUnitEnv):
    await icachemissunit_env.agent.fencei_func(1)

@toffee_test.testcase
async def test_bundle_drive_fetch_req_inputs(icachemissunit_env: ICacheMissUnitEnv):
    dut_bundle = icachemissunit_env.bundle

    toffee.info("\n--- Testing Bundle: Driving fetch_req_valid ---")
    dut_bundle.io._fetch._req._valid.value = 1 # Corrected path
    await dut_bundle.step()
    assert dut_bundle.io._fetch._req._valid.value == 1
    toffee.info(f"Python side: dut_bundle.io._fetch._req._valid.value = {dut_bundle.io._fetch._req._valid.value}")

    dut_bundle.io._fetch._req._valid.value = 0 # Corrected path
    await dut_bundle.step()
    assert dut_bundle.io._fetch._req._valid.value == 0
    toffee.info(f"Python side: dut_bundle.io._fetch._req._valid.value = {dut_bundle.io._fetch._req._valid.value}")

    toffee.info("\n--- Testing Bundle: Driving fetch_req_bits_blkPaddr ---")
    test_addr = 0xABCD0000
    dut_bundle.io._fetch._req._bits._blkPaddr.value = test_addr # Corrected path
    await dut_bundle.step()
    assert dut_bundle.io._fetch._req._bits._blkPaddr.value == test_addr
    toffee.info(f"Python side: dut_bundle.io._fetch._req._bits._blkPaddr.value = {hex(dut_bundle.io._fetch._req._bits._blkPaddr.value)}")

    toffee.info("\n--- Testing Bundle: Driving fencei ---")
    # fencei is directly under _21Bundle (io)
    dut_bundle.io._fencei.value = 1 # This was likely correct before if _fencei exists directly under io
    await dut_bundle.step()
    assert dut_bundle.io._fencei.value == 1
    toffee.info(f"Python side: dut_bundle.io._fencei.value = {dut_bundle.io._fencei.value}")
    dut_bundle.io._fencei.value = 0
    await dut_bundle.step()
    assert dut_bundle.io._fencei.value == 0
    toffee.info(f"Python side: dut_bundle.io._fencei.value = {dut_bundle.io._fencei.value}")
    toffee.info("Bundle drive tests completed.")

@toffee_test.testcase
async def test_fencei_work(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that fencei works by checking if it clears all MSHRs.
    """
    toffee.info("\n--- Testing fencei functionality ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    toffee.info("Before fencei:")
    # toffee.info initial state of MSHRs
    for i in range(10):
        toffee.info(
            f"prefetchMSHRs.{i}.io.req.ready.value:",
            getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._req_ready.value,
        )
        toffee.info(
            f"prefetchMSHRs.{i}.io.acquire.valid.value:",
            getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._acquire_valid.value,
        )
    for i in range(4):
        toffee.info(
            f"fetchMSHRs.{i}.io.req.ready.value:",
            getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value,
        )
        toffee.info(
            f"fetchMSHRs.{i}.io.acquire.valid.value:",
            getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._acquire_valid.value,
        )
    # Step 1: Set fencei to 1
    await agent.fencei_func(1)
    await bundle.step(10)  # Wait for 10 cycles to ensure fencei is processed
    toffee.info("waited 10 cycles after setting fencei")
    toffee.info("\nAfter fencei = 1, all MSHRs should be cleared")
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
    
    toffee.info("All MSHRs cleared successfully after fencei.")
    # Step 3: Set fencei to 0 (optional, but good practice)
    await agent.fencei_func(0)
    await bundle.step(10)  # Wait for another 10 cycles to ensure fencei is processed
    toffee.info("after setting fencei = 0, all MSHRs_ready should be 1,and all MSHRs_acquire_valid should be 0")
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
    toffee.info("fencei test completed successfully.")

@toffee_test.testcase
async def test_set_flush(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_set_flush` API correctly sets the io_flush signal.
    """
    toffee.info("\n--- Testing drive_set_flush API ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    # Step 1: Set flush to 1
    await agent.drive_set_flush(True)
    assert bundle.io._flush.value == 1, "Flush signal should be set to 1."
    toffee.info("Flush signal set to 1.")

    # Step 2: Step the bundle to propagate the change
    await bundle.step()
    
    # Step 3: Set flush to 0
    await agent.drive_set_flush(False)
    assert bundle.io._flush.value == 0, "Flush signal should be set to 0."
    toffee.info("Flush signal set to 0.")

@toffee_test.testcase
async def test_set_victim_way(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_set_victim_way` API correctly sets the io_victim_way signal.
    """
    toffee.info("\n--- Testing drive_set_victim_way API ---")
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    all_victim_ways = [0, 1, 2, 3]  # Assuming 4 ways for victim cache
    # Check if the victim way is set correctly
    for way in all_victim_ways:
        toffee.info(f"Setting victim way to {way}.")
        await agent.drive_set_victim_way(way)
        assert bundle.io._victim._way.value == way, f"Victim way should be set to {way}."
        toffee.info(f"Victim way set to {way}.")
        # Step the bundle to propagate the change
        await bundle.step()
    toffee.info("Victim way test completed successfully.")

@toffee_test.testcase
async def test_send_fetch_request(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_send_fetch_request` API can successfully
    send four requests and the DUT accepts them.Also, when send the fifth 
    request, the DUT should not accept it.
    """
    toffee.info("\n--- Testing drive_send_fetch_request API ---")
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
        toffee.info(f"Attempting to send fetch #{count} request: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        if count < 5:
            request_info = await agent.drive_send_fetch_request(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert request_info["send_success"] is True and bundle.io._fetch._req._ready.value == 1, f"Fetch request {count} should be accepted."
            assert request_info["blkPaddr"] == blkPaddr and request_info["vSetIdx"] == vSetIdx
            count += 1
            toffee.info(f"Fetch request accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        else:
            request_info = await agent.drive_send_fetch_request(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert request_info["send_success"] is False and bundle.io._fetch._req._ready.value == 0 , f"Fetch request {count} should not accepted."
            toffee.info(f"Fetch request NOT accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")

    toffee.info("four fetch requests sent successfully, with the fifth one correctly rejected.")



@toffee_test.testcase
async def test_api_fetch_request_generates_acquire(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that sending a fetch request via API correctly generates
    a memory acquire request from the DUT, captured by another API.
    This tests the link between request and acquire generation.
    """
    toffee.info("\n--- [API Test] Testing Request -> Acquire Flow ---")
    fetch_and_acquire_count = 0
    agent = icachemissunit_env.agent
    test_addr = 0x1000
    test_idx = 0x1A
    expected_mem_addr = test_addr << 6
    # We need to try to send the request and get the acquire concurrently.
    send_result = await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()
    assert send_result["send_success"] is True, "Fetch request should have been accepted."
    assert acquire_info is not None, "Did not capture an acquire request."
    # The first fetch request should go to fetchMSHRs[0], which has source ID 0
    assert acquire_info["source"] == 0, f"Expected source ID {fetch_and_acquire_count}, but got {acquire_info['source']}"
    assert acquire_info["address"] == expected_mem_addr, f"Expected address {hex(expected_mem_addr)}, but got {hex(acquire_info['address'])}"
    fetch_and_acquire_count+=1
    
    toffee.info("API Request -> Acquire flow test passed.")


@toffee_test.testcase
async def test_api_full_fetch_flow(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify the complete, end-to-end happy path for a fetch miss using APIs.
    """
    toffee.info("\n--- [API Test] Testing Full End-to-End Fetch Flow ---")
    agent = icachemissunit_env.agent
    
    # Test Data
    test_addr = 0x3000
    test_idx = 0x3C
    expected_mem_addr = test_addr << 6

    # 1. Send Fetch Request
    toffee.info("Step 1: Sending fetch request.")
    send_result = await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    assert send_result["send_success"] is True, "Fetch request was not accepted when DUT should be idle."

    # 2. Capture acquire AND drive victim_way concurrently
    # We want to ensure that the acquire request is captured
    toffee.info("Step 2: Waiting for acquire and driving victim way.")
    
    acquire_info = await agent.drive_get_acquire_request(timeout_cycles=10)
    # assuming victim_way is 2 for this test
    await agent.drive_set_victim_way(way=2)

    
    assert acquire_info is not None, "Did not capture an acquire request after sending fetch_req."
    assert acquire_info["address"] == expected_mem_addr
    assert acquire_info["source"] == 0
    toffee.info(f"Step 2 Passed. Got correct acquire for source ID 0 and drove victim_way=2.")
    
    # 3. Acknowledge acquire
    toffee.info("Step 3: Acknowledging acquire request.")
    await agent.drive_acknowledge_acquire(cycles=1)
    
    # 4. Respond with Grant and wait for Fetch Response
    toffee.info("Step 4: Responding with Grant and waiting for Fetch Response.")
    grant_data = [0x1122334455667788_99AABBCCDDEEFF00, 0x00FF_EEDDCCBBAA99_8877665544332211]
    
    await agent.drive_respond_with_grant(source_id=acquire_info['source'], data_beats=grant_data)
    response_info = await agent.drive_get_fetch_response()
    
    assert response_info is not None, "Did not receive a fetch response."
    
    # 5. Verify the response, now including the waymask
    toffee.info("Step 5: Verifying fetch response contents.")
    assert response_info["blkPaddr"] == test_addr
    # check waymask 
    assert response_info["waymask"] == (1 << 2), f"Expected waymask for way 2, but got {response_info['waymask']}"
    
    toffee.info("API Full End-to-End Fetch Flow test passed.")



@toffee_test.testcase
async def test_api_grant_with_corruption(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that if a grant is sent with the corrupt flag, the final
    fetch_resp is still generated, but correctly propagates the corrupt flag.
     """
    toffee.info("\n--- [API Test] Testing Grant with Corruption ---")
    agent = icachemissunit_env.agent
    
    # --- Setup: Start a fetch miss ---
    test_addr, test_idx = 0x4000, 0x4D
    
    await agent.drive_send_fetch_request(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()
    
    assert acquire_info is not None, "Setup failed: Did not get acquire."
    source_id = acquire_info["source"]
    await agent.drive_acknowledge_acquire()
    
    # --- Act: send a Grant with corrupt ，and waiting for fetch_resp ---
    toffee.info("Act: Responding with corrupt Grant and waiting for Fetch Response.")
    grant_data = [0xAAAAAAAA, 0xBBBBBBBB]

    # send Grant and capture Response
    await agent.drive_respond_with_grant(
            source_id=source_id, 
            data_beats=grant_data, 
            is_corrupt_list=[False, True] # the second beat is corrupt
        )
    response_info = await agent.drive_get_fetch_response()

    # --- Assert: verifing the response，and the sign of corrupt is True ---
    toffee.info("Assert: Verifying the received response.")
    
    assert response_info is not None, "Did not receive a fetch response, which is unexpected."
    
    # verify the core content
    assert response_info["blkPaddr"] == test_addr, "Response blkPaddr mismatch."
    assert response_info["corrupt"] is True, "Corruption flag was NOT propagated to the fetch response."
    
    toffee.info("Verification passed: fetch_resp was generated and correctly marked as corrupt.")

@toffee_test.testcase
async def test_send_prefetch_request(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify that the `drive_send_fetch_request` API can successfully
    send four requests and the DUT accepts them.Also, when send the fifth 
    request, the DUT should not accept it.
    """
    toffee.info("\n--- Testing drive_send_fetch_request API ---")
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
        toffee.info(f"Attempting to send fetch #{count} request: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        if count < 10:
            send_result = await agent.drive_send_prefetch_req(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert send_result["send_success"] is True and bundle.io._prefetch_req._ready.value == 1, f"Fetch request {count} should be accepted and ready for next request."
            assert send_result["blkPaddr"] == blkPaddr and send_result["vSetIdx"] == vSetIdx, "send result should match with what send"
            count += 1
            toffee.info(f"Fetch request accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        else:
            send_result = await agent.drive_send_prefetch_req(blkPaddr= 0x1000 + 2 * 0x1000, vSetIdx=0x1A + 2)
            assert send_result["send_success"] is True and bundle.io._prefetch_req._ready.value == 1,"Fetch request should be accepted again, because it is in prefetch MSHR."
            send_result = await agent.drive_send_prefetch_req(blkPaddr=blkPaddr, vSetIdx=vSetIdx)
            assert send_result["send_success"] is False and bundle.io._prefetch_req._ready.value == 0, f"Fetch request {count} should not be accepted."
            toffee.info(f"Fetch request NOT accepted: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
    toffee.info("prefetch requests sent successfully.")

@toffee_test.testcase
async def test_api_full_prefetch_flow(icachemissunit_env: ICacheMissUnitEnv):
    """
    Goal: Verify the complete end-to-end happy path for a PREFETCH miss.
    This is similar to the fetch flow, but uses prefetch APIs and expects a different source ID.
    """
    toffee.info("\n--- [API Test] Testing Full End-to-End PREFETCH Flow ---")
    agent = icachemissunit_env.agent
    
    # Test Data
    test_addr = 0x5000
    test_idx = 0x5E

    # 1. Send PREFETCH Request and wait for Acquire
    send_result = await agent.drive_send_prefetch_req(blkPaddr=test_addr, vSetIdx=test_idx)
    acquire_info = await agent.drive_get_acquire_request()
    toffee.info(acquire_info)

    assert send_result["send_success"] is True and acquire_info is not None, "Failed to send prefetch or get acquire."
    
    source_id = acquire_info["source"]
    assert acquire_info["source"] == 4, f"Expected source ID 4 for prefetch, but got {acquire_info['source']}"
    toffee.info(f"Prefetch request correctly assigned to a prefetch MSHR with source ID: {source_id}")
    
    # --- use captured source_id ---
    await agent.drive_acknowledge_acquire(cycles=1)
    await agent.drive_respond_with_grant(source_id=source_id, data_beats=[0x1, 0x2])
    
    toffee.info("Verifying that a prefetch request ALSO generates a valid fetch_resp.")
    response_info = await agent.drive_get_fetch_response(timeout_cycles=10)
    
    assert response_info is not None, "A prefetch request SHOULD generate a fetch_resp, but it was not captured."
    
    # check the responsed content whether matched with prefetch
    assert response_info["blkPaddr"] == test_addr, "Response blkPaddr does not match the prefetch request."
    assert response_info["vSetIdx"] == test_idx, "Response vSetIdx does not match the prefetch request."
    toffee.info(f"Received fetch_resp for prefetch request: {response_info}")
    toffee.info("API Full End-to-End PREFETCH Flow test passed.")

@toffee_test.testcase
async def test_FIFO_moudle_CP28_CP29_enq_and_deq_operation(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers FIFO CP28.x (enqueue behaviors) and CP29.x (dequeue behaviors) by
    directly driving prefetch requests and observing FIFO internals.
    """
    dut = icachemissunit_env.dut
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    toffee.info("\n--- [FIFO Test] CP28/CP29 enqueue & dequeue operations ---")

    def fifo_state():
        names = [
            "enq_ptr_value", "enq_ptr_flag",
            "deq_ptr_value", "deq_ptr_flag",
            "full", "enq_ready", "deq_ready", "deq_valid"
        ]
        return {name: int(get_internal_signal(dut, name)) for name in names}

    async def step_and_sample(cycles: int = 1):
        await bundle.step(cycles)
        return fifo_state()

    async def send_prefetch(slot_idx: int):
        blk = 0x8000 + slot_idx * 0x1000
        vset = (0x10 + slot_idx) & 0xFF
        info = await agent.drive_send_prefetch_req(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], f"Prefetch {slot_idx} should enter FIFO"
        return info

    # Ensure control signals are deasserted and FIFO starts empty
    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    bundle.io._mem._acquire._ready.value = 0
    await bundle.step()

    state = fifo_state()
    assert state["enq_ptr_value"] == 0 and state["deq_ptr_value"] == 0
    assert state["enq_ptr_flag"] == 0 and state["deq_ptr_flag"] == 0
    assert state["full"] == 0 and state["enq_ready"] == 1

    # ---------------------------
    # CP28.1/CP28.2/CP28.3 checks
    # ---------------------------
    toffee.info("CP28.1: Enqueuing 9 entries without flag flip.")
    for i in range(9):
        await send_prefetch(i)
        state = await step_and_sample()
    assert state["enq_ptr_value"] == i + 1, f"Enqueue pointer should advance to {i+1}"
    assert state["enq_ptr_flag"] == 0, "Flag must not flip before wrap"
    assert state["full"] == 0, "FIFO must not report full before wrap"
    assert state["enq_ready"] == 1, "Internal enqueue ready remains high while not full"

    toffee.info("CP28.2: Enqueue hitting tail causes wrap & flag flip.")
    await send_prefetch(9)
    state = await step_and_sample()
    assert state["enq_ptr_value"] == 0, "Pointer should wrap to 0 after slot 9"
    assert state["enq_ptr_flag"] == 1, "Flag should flip when pointer wraps"
    assert state["full"] == 1, "FIFO should report full after 10th enqueue"
    assert state["enq_ptr_value"] == state["deq_ptr_value"], "Full condition requires equal pointers"
    assert state["enq_ptr_flag"] ^ state["deq_ptr_flag"] == 1, "Full condition requires flag mismatch"
    assert state["enq_ready"] == 0, "Internal enqueue ready must drop when FIFO full"

    toffee.info("CP28.3: Further enqueue blocked while FIFO is full.")
    reject_info = await agent.drive_send_prefetch_req(
        blkPaddr=0xDEAD_BEEF, vSetIdx=0x55, timeout_cycles=5
    )
    assert reject_info["send_success"] is False, "Request must be rejected when FIFO is full"
    state = fifo_state()
    assert state["full"] == 1 and state["enq_ready"] == 0

    # ---------------------------
    # CP29.1/CP29.2/CP29.3 checks
    # ---------------------------
    toffee.info("CP29.x: Start draining FIFO via memory acquires.")

    async def acknowledge_next_acquire():
        acquire = await agent.drive_get_and_acknowledge_acquire(timeout_cycles=80, ack_cycles=1)
        assert acquire is not None, "Expected acquire request while FIFO is non-empty"
        return await step_and_sample()

    # Allow pending MSHR scheduling to run before draining
    await bundle.step(5)

    toffee.info("CP29.1: Normal dequeue without flag flip for first nine entries.")
    for expected_value in range(1, 10):
        state = await acknowledge_next_acquire()
        assert state["deq_ptr_value"] == expected_value, f"Dequeue pointer should advance to {expected_value}"
        assert state["deq_ptr_flag"] == 0, "Flag must remain 0 before wrap"
        assert state["deq_valid"] == 1, "FIFO should still report valid data"

    toffee.info("CP29.2: Dequeue at tail wraps pointer and flips flag.")
    wrap_state = await acknowledge_next_acquire()
    assert wrap_state["deq_ptr_value"] == 0, "Pointer should wrap to 0 on final dequeue"
    assert wrap_state["deq_ptr_flag"] == 1, "Flag should flip after wrap on dequeue"

    toffee.info("CP29.3: FIFO empty -> io.deq.valid must be low, enqueues allowed again.")
    await bundle.step()
    empty_state = fifo_state()
    assert empty_state["deq_valid"] == 0, "Dequeue valid should drop when FIFO empty"
    assert empty_state["enq_ptr_value"] == empty_state["deq_ptr_value"]
    assert empty_state["enq_ptr_flag"] == empty_state["deq_ptr_flag"]
    assert empty_state["enq_ready"] == 1, "Internal ready must reassert once FIFO empties"

    toffee.info("FIFO CP28/CP29 behavioral checks completed successfully.")


@toffee_test.testcase
async def test_FIFO_moudle_CP30_flush_operation(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers FIFO CP30: flush clears pointers/flags and reopens enqueue interface.
    """
    dut = icachemissunit_env.dut
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    def fifo_state():
        names = [
            "enq_ptr_value", "enq_ptr_flag",
            "deq_ptr_value", "deq_ptr_flag",
            "full", "enq_ready", "deq_valid"
        ]
        return {name: int(get_internal_signal(dut, name)) for name in names}

    async def send_prefetch(slot_idx: int):
        blk = 0xA000 + slot_idx * 0x1000
        vset = (0x20 + slot_idx) & 0xFF
        info = await agent.drive_send_prefetch_req(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], f"Prefetch {slot_idx} should enqueue before flush"

    toffee.info("\n--- [FIFO Test] CP30 flush operation ---")

    # Ensure flush/fencei are low and FIFO empty
    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()
    state = fifo_state()
    assert state["enq_ptr_value"] == state["deq_ptr_value"] == 0
    assert state["enq_ptr_flag"] == state["deq_ptr_flag"] == 0
    assert state["full"] == 0 and state["enq_ready"] == 1 and state["deq_valid"] == 0

    # Fill a few entries to put FIFO into non-empty state
    for i in range(5):
        await send_prefetch(i)
        await bundle.step()
    filled_state = fifo_state()
    assert filled_state["enq_ptr_value"] == 5
    assert filled_state["deq_valid"] == 1

    # Drive flush high and check pointers/flags reset immediately
    await agent.drive_set_flush(True)
    await bundle.step()
    flushed_state = fifo_state()
    assert flushed_state["enq_ptr_value"] == 0
    assert flushed_state["deq_ptr_value"] == 0
    assert flushed_state["enq_ptr_flag"] == 0
    assert flushed_state["deq_ptr_flag"] == 0
    assert flushed_state["full"] == 0
    assert flushed_state["enq_ready"] == 1
    assert flushed_state["deq_valid"] == 0

    # Clear flush and ensure FIFO remains empty/ready
    await agent.drive_set_flush(False)
    await bundle.step()
    post_state = fifo_state()
    assert post_state == flushed_state
    toffee.info("FIFO CP30 flush behavior verified successfully.")


@toffee_test.testcase
async def test_MISSUNIT_CP31_fetch_miss_process(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP31.x: fetch miss acceptance, duplicate filtering, and low-index MSHR allocation.
    """
    dut = icachemissunit_env.dut
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    def fetch_mshr_ready_vec():
        return [
            int(getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value)
            for i in range(4)
        ]

    async def send_fetch_once(blk, vset):
        info = await agent.drive_send_fetch_request(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], f"Fetch ({hex(blk)}, {hex(vset)}) should be accepted"
        await bundle.step()

    toffee.info("\n--- [MISSUNIT] CP31 fetch miss process ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    assert fetch_mshr_ready_vec() == [1, 1, 1, 1], "Fetch MSHRs must start idle"

    fetch_reqs = [
        (0x1000, 0x10),
        (0x2000, 0x20),
        (0x3000, 0x30),
        (0x4000, 0x40),
    ]

    toffee.info("CP31.1 & CP31.3: new misses take lowest-index available fetch MSHRs.")
    for idx, (blk, vset) in enumerate(fetch_reqs):
        await send_fetch_once(blk, vset)
        ready_vec = fetch_mshr_ready_vec()
        expected = [0 if j <= idx else 1 for j in range(4)]
        assert ready_vec == expected, (
            f"Low-index allocation violated after request #{idx}: expected {expected}, got {ready_vec}"
        )

    toffee.info("CP31.2: duplicate miss hits existing entry and is filtered.")
    dup_blk, dup_vset = fetch_reqs[0]
    await send_fetch_once(dup_blk, dup_vset)
    fetch_hit = int(get_internal_signal(dut, "fetch_hit"))
    demux_valid = int(get_internal_signal(dut, "fetch_demux_valid"))
    assert fetch_hit == 1, "Duplicate miss should assert fetch_hit"
    assert demux_valid == 0, "Duplicate miss should not re-enter fetch demux"
    assert fetch_mshr_ready_vec() == [0, 0, 0, 0], "Duplicate miss must not consume additional MSHR"

    toffee.info("MISSUNIT CP31 checks completed successfully.")


@toffee_test.testcase
async def test_MISSUNIT_CP32_prefetch_miss_process(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP32.x: prefetch miss acceptance, duplicate filtering, and FIFO ordering.
    """
    dut = icachemissunit_env.dut
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    def prefetch_mshr_ready_vec():
        return [
            int(getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._req_ready.value)
            for i in range(10)
        ]

    async def send_prefetch_once(blk, vset):
        info = await agent.drive_send_prefetch_req(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], f"Prefetch ({hex(blk)}, {hex(vset)}) should be accepted"
        await bundle.step()

    toffee.info("\n--- [MISSUNIT] CP32 prefetch miss process ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    assert prefetch_mshr_ready_vec() == [1] * 10, "Prefetch MSHRs must start idle"

    prefetch_reqs = [
        (0x6000, 0x11),
        (0x7000, 0x12),
        (0x8000, 0x13),
    ]

    toffee.info("CP32.1: enqueue new prefetch misses and observe FIFO pointer advance.")
    for idx, (blk, vset) in enumerate(prefetch_reqs):
        await send_prefetch_once(blk, vset)
        enq_ptr = int(get_internal_signal(dut, "enq_ptr_value"))
        assert enq_ptr == (idx + 1) % 10

    toffee.info("CP32.3 & CP32.4: drain FIFO in-order and verify priorityFIFO head indices.")
    for expected_idx, (blk, vset) in enumerate(prefetch_reqs):
        fifo_head = int(get_internal_signal(dut, "fifo_deq_bits"))
        assert fifo_head == expected_idx, (
            f"priorityFIFO head mismatch before dequeue #{expected_idx}: expected {expected_idx}, got {fifo_head}"
        )
        acquire = await agent.drive_get_and_acknowledge_acquire(timeout_cycles=80, ack_cycles=1)
        assert acquire is not None, "Expected acquire for enqueued prefetch"
        assert acquire["source"] == 4 + expected_idx, (
            f"Prefetch acquire source mismatch: expected {4 + expected_idx}, got {acquire['source']}"
        )
        await bundle.step()

    toffee.info("CP32.2: duplicate prefetch hit should be filtered.")
    dup_blk, dup_vset = prefetch_reqs[1]
    await send_prefetch_once(dup_blk, dup_vset)
    prefetch_hit = int(get_internal_signal(dut, "prefetch_hit"))
    demux_valid = int(get_internal_signal(dut, "prefetch_demux_valid"))
    assert prefetch_hit == 1, "Duplicate prefetch should assert prefetch_hit"
    assert demux_valid == 0, "Prefetch demux must stall when hit occurs"

    toffee.info("MISSUNIT CP32 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_CP33_MSHR_manage(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP33.1/CP33.2: MSHR lookup hits within same pipe and across fetch/prefetch groups.
    """
    dut = icachemissunit_env.dut
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    def prefetch_mshr_ready_vec():
        return [
            int(getattr(bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}")._io._req_ready.value)
            for i in range(10)
        ]

    async def send_fetch(blk, vset):
        info = await agent.drive_send_fetch_request(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], f"Fetch ({hex(blk)}, {hex(vset)}) should handshake"
        await bundle.step()

    async def send_prefetch(blk, vset):
        info = await agent.drive_send_prefetch_req(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], f"Prefetch ({hex(blk)}, {hex(vset)}) should handshake"
        await bundle.step()

    toffee.info("\n--- [MISSUNIT] CP33 MSHR manage ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    fetch_addr = 0x9000
    fetch_idx = 0x21

    toffee.info("CP33.1a: Create a fetch MSHR entry.")
    await send_fetch(fetch_addr, fetch_idx)

    toffee.info("CP33.1b: Duplicate fetch should assert fetchHit (same-pipe lookup).")
    await send_fetch(fetch_addr, fetch_idx)
    fetch_hit = int(get_internal_signal(dut, "fetch_hit"))
    fetch_demux_valid = int(get_internal_signal(dut, "fetch_demux_valid"))
    assert fetch_hit == 1, "Duplicate fetch should hit existing entry"
    assert fetch_demux_valid == 0, "Fetch demux must not forward duplicate request"

    toffee.info("CP33.2a: Prefetch of same line should see fetch MSHRs via lookups.")
    # Drive fetch/prefetch concurrently to cover CP33.3 (same-cycle same-line lookup).
    bundle.io._fetch._req._bits._blkPaddr.value = fetch_addr
    bundle.io._fetch._req._bits._vSetIdx.value = fetch_idx
    bundle.io._fetch._req._valid.value = 1
    bundle.io._prefetch_req._bits._blkPaddr.value = fetch_addr
    bundle.io._prefetch_req._bits._vSetIdx.value = fetch_idx
    bundle.io._prefetch_req._valid.value = 1
    await bundle.step()
    bundle.io._fetch._req._valid.value = 0
    bundle.io._prefetch_req._valid.value = 0
    prefetch_hit = int(get_internal_signal(dut, "prefetch_hit"))
    prefetch_demux_valid = int(get_internal_signal(dut, "prefetch_demux_valid"))
    assert prefetch_hit == 1, "Prefetch should detect existing fetch MSHR entry"
    assert prefetch_demux_valid == 0, "Prefetch demux must stay idle when hit occurs"

    toffee.info("CP33.1c: Allocate a standalone prefetch entry (miss expected).")
    prefetch_addr = 0xB000
    prefetch_idx = 0x35
    ready_before_prefetch = prefetch_mshr_ready_vec()
    await send_prefetch(prefetch_addr, prefetch_idx)
    ready_after_prefetch = prefetch_mshr_ready_vec()
    assert ready_before_prefetch[0] == 1 and ready_after_prefetch[0] == 0, \
        "Unique prefetch should consume the lowest-index prefetch MSHR"
    assert ready_before_prefetch[1:] == ready_after_prefetch[1:], \
        "Only one prefetch MSHR should be consumed for a single miss"

    toffee.info("CP33.1d: Duplicate prefetch should assert prefetchHit (same-pipe lookup).")
    await send_prefetch(prefetch_addr, prefetch_idx)
    dup_prefetch_hit = int(get_internal_signal(dut, "prefetch_hit"))
    dup_prefetch_demux_valid = int(get_internal_signal(dut, "prefetch_demux_valid"))
    assert dup_prefetch_hit == 1, "Duplicate prefetch should hit existing prefetch MSHR entry"
    assert dup_prefetch_demux_valid == 0, "Prefetch demux remains idle on duplicate hit"
    assert prefetch_mshr_ready_vec() == ready_after_prefetch, \
        "Duplicate prefetch must not allocate additional MSHRs"

    toffee.info("CP33.2b: Fetch same line should detect prefetch MSHR entry.")
    await send_fetch(prefetch_addr, prefetch_idx)
    fetch_hit_cross = int(get_internal_signal(dut, "fetch_hit"))
    fetch_demux_valid_cross = int(get_internal_signal(dut, "fetch_demux_valid"))
    assert fetch_hit_cross == 1, "Fetch should detect prefetch MSHR entry"
    assert fetch_demux_valid_cross == 0, "Fetch demux remains idle on hit"

    toffee.info("MISSUNIT CP33 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_CP34_acquireArb_arbitration(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP34.1: acquireArb prioritizes fetch MSHRs over prefetch MSHRs.
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle

    async def send_fetch(blk, vset):
        info = await agent.drive_send_fetch_request(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], "Fetch request should handshake"
        await bundle.step()

    async def send_prefetch(blk, vset):
        info = await agent.drive_send_prefetch_req(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], "Prefetch request should handshake"
        await bundle.step()

    toffee.info("\n--- [MISSUNIT] CP34 acquire arbiter ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    async def next_acquire_source():
        acquire = await agent.drive_get_and_acknowledge_acquire(timeout_cycles=40, ack_cycles=1)
        assert acquire is not None, "Expected acquire from arbiter"
        return acquire["source"]

    toffee.info("CP34.1a: Three independent fetches should consume sources 0/1/2 in order.")
    fetch_seq = [
        (0xC000, 0x40),
        (0xC010, 0x41),
        (0xC020, 0x42),
    ]
    for expected_src, (blk, vset) in enumerate(fetch_seq):
        await send_fetch(blk=blk, vset=vset)
        src = await next_acquire_source()
        assert src == expected_src, f"Fetch #{expected_src} should use source {expected_src}, got {src}"

    toffee.info("CP34.1b: Prefetch should use prefetch source (>=4) once fetch slots are occupied.")
    await send_prefetch(blk=0xD000, vset=0x50)
    prefetch_src = await next_acquire_source()
    assert prefetch_src == 4, f"Prefetch acquire should use source 4, got {prefetch_src}"

    toffee.info("MISSUNIT CP34 checks completed successfully.")


@toffee_test.testcase
async def test_MISSUNIT_CP35_grant_accept_and_refill(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP35.x: grant beat handling, readBeatCnt sequencing, last_fire/id tracking, and corrupt flag behavior.
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    dut = icachemissunit_env.dut

    def fetch_mshr_ready_vec():
        return [
            int(getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value)
            for i in range(4)
        ]

    async def send_fetch_for_acquire(blk, vset):
        info = await agent.drive_send_fetch_request(blkPaddr=blk, vSetIdx=vset)
        assert info["send_success"], "Fetch request should handshake"
        await bundle.step()
        acquire = await agent.drive_get_and_acknowledge_acquire(timeout_cycles=40, ack_cycles=1)
        assert acquire is not None, "Expected acquire after fetch miss"
        return acquire["source"]

    def sample_grant_state():
        return {
        "readBeatCnt": int(get_internal_signal(dut, "readBeatCnt")),
        "last_fire": int(get_internal_signal(dut, "last_fire")),
        "last_fire_r": int(get_internal_signal(dut, "last_fire_r")),
        "id_r": int(get_internal_signal(dut, "id_r")),
        "corrupt_r": int(get_internal_signal(dut, "corrupt_r")),
        }

    toffee.info("\n--- [MISSUNIT] CP35 grant accept & refill ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    # CP35.0 / CP35.3-start: MSHR occupancy before grants
    toffee.info("CP35.0/35.3-start: verify fetch MSHR idle → occupied after request.")
    initial_ready = fetch_mshr_ready_vec()
    assert initial_ready == [1, 1, 1, 1], "Fetch MSHRs should start idle"
    source = await send_fetch_for_acquire(blk=0xE000, vset=0x60)
    busy_ready = fetch_mshr_ready_vec()
    busy_index = next((i for i, r in enumerate(busy_ready) if r == 0), None)
    assert busy_index is not None, "One fetch MSHR should be occupied after sending request"
    toffee.info(f"CP35.3-start: fetch MSHR {busy_index} busy (vector {busy_ready})")

    # CP35.1: first grant beat
    toffee.info("CP35.1: apply first grant beat and check readBeatCnt toggles.")
    data_beat0 = 0x11223344556677889900AABBCCDDEEFF
    await agent.drive_respond_with_grant(
        source_id=source,
        data_beats=[data_beat0],
        is_corrupt_list=[False],
    )
    state_after_first = sample_grant_state()
    assert int(get_internal_signal(dut, "respDataReg_0")) == data_beat0, "respDataReg_0 should capture first beat data"
    assert state_after_first["readBeatCnt"] == 1, "readBeatCnt should increment after first beat"

    # CP35.2 + CP35.4: second beat, last_fire, corrupt latch
    toffee.info("CP35.2/CP35.4: send second grant beat.")
    data_beat1 = 0xFFEEDDCCBBAA00998877665544332211
    await agent.drive_respond_with_grant(
        source_id=source,
        data_beats=[data_beat1],
        is_corrupt_list=[True],
    )
    state_after_second = sample_grant_state()
    resp1 = int(get_internal_signal(dut, "respDataReg_1"))
    assert resp1 == data_beat1, "respDataReg_1 should capture second beat data"
    assert state_after_second["readBeatCnt"] == 0, "readBeatCnt should reset after second beat"
    assert state_after_second["corrupt_r"] == 1, "corrupt_r should latch high during corrupt beat"

    # CP35.3-end: check last_fire_r/id_r/corrupt_r latch and release MSHR
    toffee.info("CP35.3-end: verify last_fire_r/id_r latch.")
    state_after_last_fire = sample_grant_state()
    assert state_after_last_fire["last_fire_r"] == 1, "last_fire_r should latch high in the next cycle"
    assert state_after_last_fire["id_r"] == source, "id_r should capture grant source"
    assert state_after_last_fire["corrupt_r"] == 1, "corrupt_r remains high until response window completes"

    await bundle.step()
    state_after_clear = sample_grant_state()
    assert state_after_clear["corrupt_r"] == 0, "corrupt_r should clear after response window"
    assert state_after_clear["last_fire_r"] == 0, "last_fire_r should drop after one cycle"

    final_ready = fetch_mshr_ready_vec()
    assert final_ready == initial_ready, "Fetch MSHR should be released after grant completes"
    toffee.info(f"CP35.3-end: fetch MSHR released (vector {final_ready})")

    toffee.info("MISSUNIT CP35 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_CP36_Replacer(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP36.x: Replacer update (victim set idx + waymask).
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    dut = icachemissunit_env.dut

    toffee.info("\n--- [MISSUNIT] CP36 replacer update ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    toffee.info("CP36.1: send fetch miss and check victim vSetIdx update.")
    victim_way = 2
    await agent.drive_set_victim_way(victim_way)
    test_addr = 0xF000
    test_vset = 0x70
    send_result = await agent.drive_send_fetch_request(test_addr, test_vset)
    assert send_result["send_success"], "Fetch miss should be accepted for replacer test"

    acquire = await agent.drive_get_acquire_request(timeout_cycles=40)
    assert acquire is not None, "Expected acquire for replacer test"

    # CP36.1: victim should update on acquire fire
    bundle.io._mem._acquire._ready.value = 1
    await bundle.step()
    victim_valid = int(get_internal_signal(dut, "victim_valid"))
    victim_bits = bundle.io._victim._vSetIdx._bits.value
    assert victim_valid == 1, "Victim update valid should be asserted on acquire fire"
    assert victim_bits == test_vset, f"Victim vSetIdx should match request ({test_vset}), got {victim_bits}"
    bundle.io._mem._acquire._ready.value = 0
    await bundle.step()

    toffee.info("CP36.2: verify replacer waymask matches victim way.")
    grant_data = [
        0x0123456789ABCDEF_0123456789ABCDEF,
        0xFEDCBA9876543210_FEDCBA9876543210,
    ]
    await agent.drive_respond_with_grant(
        source_id=acquire["source"],
        data_beats=grant_data,
        is_corrupt_list=[False, False],
    )
    response = await agent.drive_get_fetch_response()
    assert response is not None, "Fetch response should be produced after grant"
    expected_waymask = 1 << victim_way
    observed_way = int(get_internal_signal(dut, "mshr_resp_way"))
    assert observed_way == victim_way, \
        f"mshr_resp_way should match victim way {victim_way}, got {observed_way}"
    assert response["waymask"] == expected_waymask, \
        f"Waymask should match victim way {victim_way}, expected {expected_waymask:#x}, got {response['waymask']:#x}"

    toffee.info("MISSUNIT CP36 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_CP37_SRAM_writeback(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP37.x: SRAM writeback controls/data.
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    dut = icachemissunit_env.dut

    def expected_waymask(way):
        return 1 << way

    toffee.info("\n--- [MISSUNIT] CP37 SRAM writeback ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    test_addr = 0x12345000
    test_vset = 0x5A
    victim_way = 1

    await agent.drive_set_victim_way(victim_way)
    send_result = await agent.drive_send_fetch_request(test_addr, test_vset)
    assert send_result["send_success"], "Fetch miss should be accepted for SRam writeback test"

    acquire = await agent.drive_get_acquire_request(timeout_cycles=40)
    assert acquire is not None, "Expected acquire for SRAM writeback test"
    await agent.drive_acknowledge_acquire(cycles=1)

    grant_data = [
        0x11112222333344445555666677778888,
        0x9999AAAABBBBCCCCDDDDEEEEFFFF0000,
    ]
    await agent.drive_respond_with_grant(
        source_id=acquire["source"],
        data_beats=grant_data,
        is_corrupt_list=[False, False],
    )

    response = await agent.drive_get_fetch_response()
    assert response is not None, "Fetch response should be produced after grant"

    # CP37.1: meta/data write valids asserted when difftest_valid true
    assert bundle.io._meta_write._valid.value == 1, "meta_write.valid should be high when difftest_valid"
    assert bundle.io._data_write._valid.value == 1, "data_write.valid should be high when difftest_valid"

    # CP37.2: meta/data contents reflect miss info
    meta_bits = bundle.io._meta_write._bits
    data_bits = bundle.io._data_write._bits
    expected_phy = test_addr >> 6
    assert meta_bits._virIdx.value == test_vset, "meta virIdx mismatch"
    assert meta_bits._phyTag.value == expected_phy, "meta phyTag mismatch"
    assert meta_bits._waymask.value == expected_waymask(victim_way), "meta waymask mismatch"
    assert meta_bits._bankIdx.value == (test_vset & 0x1), "meta bankIdx mismatch"

    assert data_bits._virIdx.value == test_vset, "data virIdx mismatch"
    assert data_bits._waymask.value == expected_waymask(victim_way), "data waymask mismatch"
    assert data_bits._data.value == int(response["data"]), "data payload mismatch"

    toffee.info("MISSUNIT CP37 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_CP38_mainpipe_iprefetchpipe_response(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP38.x: fetch response generation for fetch/prefetch paths.
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    dut = icachemissunit_env.dut

    async def run_miss_and_capture(fetch=True, corrupt=False):
        addr = 0x2000 if fetch else 0x3000
        vset = 0x22 if fetch else 0x33
        if fetch:
            result = await agent.drive_send_fetch_request(addr, vset)
        else:
            result = await agent.drive_send_prefetch_req(addr, vset)
        assert result["send_success"], "Miss request should be accepted"
        acquire = await agent.drive_get_acquire_request(timeout_cycles=40)
        assert acquire is not None, "Expected acquire after miss"
        await agent.drive_acknowledge_acquire(cycles=1)
        grant_words = [
            0xAAAABBBBCCCCDDDDEEEEFFFF11112222,
            0x3333444455556666777788889999AAAA,
        ]
        await agent.drive_respond_with_grant(
            source_id=acquire["source"],
            data_beats=grant_words,
            is_corrupt_list=[corrupt, corrupt],
        )
        resp = await agent.drive_get_fetch_response()
        assert resp is not None, "Fetch response should be produced"
        return resp, addr, vset, corrupt

    toffee.info("\n--- [MISSUNIT] CP38 main/prefetch response ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    resp_fetch, fetch_addr, fetch_vset, _ = await run_miss_and_capture(fetch=True, corrupt=False)
    assert resp_fetch["blkPaddr"] == fetch_addr, "fetch blkPaddr mismatch"
    assert resp_fetch["vSetIdx"] == fetch_vset, "fetch vSetIdx mismatch"
    assert resp_fetch["data"] == bundle.io._data_write._bits._data.value, "fetch data payload mismatch"
    assert resp_fetch["corrupt"] is False, "fetch corrupt flag should be false"

    resp_prefetch, prefetch_addr, prefetch_vset, _ = await run_miss_and_capture(fetch=False, corrupt=True)
    assert resp_prefetch["blkPaddr"] == prefetch_addr, "prefetch blkPaddr mismatch"
    assert resp_prefetch["vSetIdx"] == prefetch_vset, "prefetch vSetIdx mismatch"
    assert resp_prefetch["corrupt"] is True, "prefetch corrupt flag should propagate"

    toffee.info("MISSUNIT CP38 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_CP39_flush_fencei_operation(icachemissunit_env: ICacheMissUnitEnv):
    """
    Covers MISSUNIT CP39.x: flush/fencei behavior before and after MSHR fire.
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    dut = icachemissunit_env.dut

    async def send_fetch(addr, vset):
        info = await agent.drive_send_fetch_request(addr, vset)
        assert info["send_success"], "Fetch miss should be accepted"

    async def wait_for_acquire():
        acquire = await agent.drive_get_acquire_request(timeout_cycles=40)
        assert acquire is not None, "Expected acquire"
        return acquire

    def fetch_mshr_ready_vec():
        return [
            int(getattr(bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}")._io._req_ready.value)
            for i in range(4)
        ]

    toffee.info("\n--- [MISSUNIT] CP39 flush/fencei ---")

    await agent.fencei_func(0)
    await agent.drive_set_flush(False)
    await bundle.step()

    # CP39.1: fencei before fire should block all MSHRs
    toffee.info("CP39.1: assert fencei before any acquire fires.")
    await agent.fencei_func(1)
    await bundle.step()
    ready_vec = fetch_mshr_ready_vec()
    assert ready_vec == [0, 0, 0, 0], "Fencei should force all fetch MSHRs ready low"
    acquire = await agent.drive_get_acquire_request(timeout_cycles=5)
    assert acquire is None, "Fencei asserted -> no acquire should be observed"
    await agent.fencei_func(0)

    # CP39.2: flush prevents prefetch MSHR from firing
    toffee.info("CP39.2: assert flush, only fetch requests may fire.")
    await agent.drive_set_flush(True)
    await send_fetch(0x5000, 0x50)
    prefetch = await agent.drive_send_prefetch_req(0x7000, 0x70)
    assert not prefetch["send_success"], "Prefetch request should be blocked under flush"
    acquire_fetch = await wait_for_acquire()
    assert acquire_fetch["source"] == 0, "Only fetch MSHR should fire under flush"
    await agent.drive_acknowledge_acquire(cycles=2)
    for _ in range(6):
        if bundle.io._mem._acquire._valid.value == 0:
            break
        await bundle.step()
    else:
        raise AssertionError("Acquire valid should drop after handshake")
    prefetch_acquire = await agent.drive_get_acquire_request(timeout_cycles=5)
    assert prefetch_acquire is None, "Prefetch should be blocked under flush"
    await agent.drive_set_flush(False)

    # CP39.3: flush after fire suppresses SRAM writes but still responds
    toffee.info("CP39.3: assert flush after acquire fired, ensure SRAM write suppressed.")
    await send_fetch(0x8000, 0x80)
    acquire = await wait_for_acquire()
    await agent.drive_acknowledge_acquire(cycles=1)
    await agent.drive_set_flush(True)
    grant_data = [
        0xAAAA5555AAAA5555AAAA5555AAAA5555,
        0xBBBB6666BBBB6666BBBB6666BBBB6666,
    ]
    await agent.drive_respond_with_grant(
        source_id=acquire["source"],
        data_beats=grant_data,
        is_corrupt_list=[False, False],
    )
    resp = await agent.drive_get_fetch_response()
    assert resp is not None, "Fetch response should still be produced under flush"
    assert bundle.io._meta_write._valid.value == 0, "meta write should be suppressed when flush asserted after fire"
    assert bundle.io._data_write._valid.value == 0, "data write should be suppressed when flush asserted after fire"
    await agent.drive_set_flush(False)

    toffee.info("MISSUNIT CP39 checks completed successfully.")

@toffee_test.testcase
async def test_MISSUNIT_addational_all_mshr_lookup_coverage(icachemissunit_env: ICacheMissUnitEnv):
    """
    Drives enough fetch/prefetch misses to exercise every MSHR instance
    (4 fetch + 10 prefetch) and then re-issues matching requests to trigger
    both io_lookUps_0_hit and io_lookUps_1_hit in every entry. This ensures
    the per-instance RTL files (ICacheMSHR*.sv) are covered.
    """
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    dut = icachemissunit_env.dut

    toffee.info("\n--- [MISSUNIT] CP40 full MSHR lookup coverage ---")
    await agent.fencei_func(0)
    await agent.drive_set_flush(False)

    fetch_slots = 4
    prefetch_slots = 10

    fetch_miss_list = [(0x1000 + i * 0x1000, 0x10 + i) for i in range(fetch_slots)]
    prefetch_miss_list = [(0xA000 + i * 0x1000, 0x60 + i) for i in range(prefetch_slots)]

    async def allocate_and_collect(miss_list, sender):
        acquire_sources = []
        for idx, (addr, vset) in enumerate(miss_list):
            await agent.drive_set_victim_way(idx & 0x3)
            info = await sender(addr, vset)
            assert info["send_success"], f"MSHR allocation {idx} should succeed"
            acquire = await agent.drive_get_acquire_request(timeout_cycles=40)
            assert acquire is not None, "Expected acquire for miss"
            acquire_sources.append(acquire["source"])
            await agent.drive_acknowledge_acquire(cycles=1)
        return acquire_sources

    fetch_sources = await allocate_and_collect(fetch_miss_list, agent.drive_send_fetch_request)

    async def send_prefetch(addr, vset):
        result = await agent.drive_send_prefetch_req(addr, vset, timeout_cycles=20)
        return result

    prefetch_sources = []
    for idx, (addr, vset) in enumerate(prefetch_miss_list):
        result = await send_prefetch(addr, vset)
        assert result["send_success"], f"Prefetch miss {idx} should be accepted"
        acquire = await agent.drive_get_acquire_request(timeout_cycles=40)
        assert acquire is not None, "Prefetch miss should generate acquire"
        prefetch_sources.append(acquire["source"])
        await agent.drive_acknowledge_acquire(cycles=1)

    toffee.info("Prefetch requests probing existing fetch entries (cross-hit).")
    for addr, vset in fetch_miss_list:
        info = await agent.drive_send_prefetch_req(addr, vset, timeout_cycles=5)
        assert info["send_success"], "Prefetch request should still handshake"
        dup = await agent.drive_get_acquire_request(timeout_cycles=5)
        assert dup is None, "Prefetch hit must not create a new acquire"

    toffee.info("Fetch requests probing existing prefetch entries (cross-hit).")
    for addr, vset in prefetch_miss_list:
        info = await agent.drive_send_fetch_request(addr, vset)
        assert info["send_success"], "Fetch request should still handshake"
        dup = await agent.drive_get_acquire_request(timeout_cycles=5)
        assert dup is None, "Fetch hit must not create a new acquire"

    async def service_grants(source_id):
        grant_data = [
            0x11112222333344445555666677778888,
            0x9999AAAABBBBCCCCDDDDEEEEFFFF0000,
        ]
        await agent.drive_respond_with_grant(
            source_id=source_id,
            data_beats=grant_data,
            is_corrupt_list=[False, False],
        )
        await bundle.step()

    for source in fetch_sources + prefetch_sources:
        await service_grants(source)

    toffee.info("Re-issuing after refill completes to confirm entries free again.")
    fetch_sources_second = await allocate_and_collect(fetch_miss_list, agent.drive_send_fetch_request)
    prefetch_sources_second = await allocate_and_collect(prefetch_miss_list, agent.drive_send_prefetch_req)

    for source in fetch_sources_second + prefetch_sources_second:
        await service_grants(source)

    toffee.info("CP40: All MSHR entries exercised; hits observed without extra acquires and entries verified free after refill.")
