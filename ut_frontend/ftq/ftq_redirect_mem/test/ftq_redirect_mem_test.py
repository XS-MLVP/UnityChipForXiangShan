from .ftq_redirect_mem_fixture import ftq_redirect_mem_env
from ..env import FtqRedirectMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()

# 测试读取端口0
# hisPtr_flag, hisPtr_value, ssp, sctr, TOSW_flag, TOSW_value, TOSR_flag, TOSR_value, NOS_flag, NOS_value, topAddr

#1.1 读取端口0的地址0
@toffee_test.testcase
async def test_read_0_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 0 ---")
    
    data0 = await ftq_redirect_mem_env.agent.read_0(0)
    assert data0[0] == 0
    assert data0[1] == 46
    assert data0[2] == 11
    assert data0[3] == 2
    assert data0[4] == 0
    assert data0[5] == 13
    assert data0[6] == 1
    assert data0[7] == 12
    assert data0[8] == 0
    assert data0[9] == 26
    assert data0[10] == 351244621699960
    print(f"read port 0 at addr 0: {data0}")

# 1.2 读取端口0的地址1
@toffee_test.testcase
async def test_read_0_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 31 ---")
    data31 = await ftq_redirect_mem_env.agent.read_0(31)
    print(f"read port 0 at addr 31: {data31}")
    assert data31[0] == 0
    assert data31[1] == 46
    assert data31[2] == 11
    assert data31[3] == 2
    assert data31[4] == 0
    assert data31[5] == 13
    assert data31[6] == 1
    assert data31[7] == 12
    assert data31[8] == 0
    assert data31[9] == 26
    assert data31[10] == 351244621699960
    print(f"read port 0 at addr 31: {data31}")
    print(f"Read Port 0 Test Passed at addr 31!!!")

# @toffee_test.testcase
# async def test_bundle_drive_fetch_req_inputs(icachemissunit_env: ICacheMissUnitEnv):
#     dut_bundle = icachemissunit_env.bundle

#     print("\n--- Testing Bundle: Driving fetch_req_valid ---")
#     dut_bundle.io._fetch._req._valid.value = 1 # Corrected path
#     await dut_bundle.step()
#     assert dut_bundle.io._fetch._req._valid.value == 1
#     print(f"Python side: dut_bundle.io._fetch._req._valid.value = {dut_bundle.io._fetch._req._valid.value}")

#     dut_bundle.io._fetch._req._valid.value = 0 # Corrected path
#     await dut_bundle.step()
#     assert dut_bundle.io._fetch._req._valid.value == 0
#     print(f"Python side: dut_bundle.io._fetch._req._valid.value = {dut_bundle.io._fetch._req._valid.value}")

#     print("\n--- Testing Bundle: Driving fetch_req_bits_blkPaddr ---")
#     test_addr = 0xABCD0000
#     dut_bundle.io._fetch._req._bits._blkPaddr.value = test_addr # Corrected path
#     await dut_bundle.step()
#     assert dut_bundle.io._fetch._req._bits._blkPaddr.value == test_addr
#     print(f"Python side: dut_bundle.io._fetch._req._bits._blkPaddr.value = {hex(dut_bundle.io._fetch._req._bits._blkPaddr.value)}")

#     print("\n--- Testing Bundle: Driving fencei ---")
#     # fencei is directly under _21Bundle (io)
#     dut_bundle.io._fencei.value = 1 # This was likely correct before if _fencei exists directly under io
#     await dut_bundle.step()
#     assert dut_bundle.io._fencei.value == 1
#     print(f"Python side: dut_bundle.io._fencei.value = {dut_bundle.io._fencei.value}")
#     dut_bundle.io._fencei.value = 0
#     await dut_bundle.step()
#     assert dut_bundle.io._fencei.value == 0
#     print(f"Python side: dut_bundle.io._fencei.value = {dut_bundle.io._fencei.value}")
#     print("Bundle drive tests completed.")