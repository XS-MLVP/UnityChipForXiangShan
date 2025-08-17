from .ftq_pd_mem_fixture import ftq_pd_mem_env
from ..env import FtqPdMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Smoke Test Passed!!! ---")

@toffee_test.testcase
async def test_read_0_at_0(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 0 ---")
    
    data0 = await ftq_pd_mem_env.agent.read_0(0)
    assert data0[0] == [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1]
    assert data0[1] == [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
    assert data0[2] == [1, 0, 0]
    assert data0[3] == 0
    assert data0[4] == 15
    print(f"read port 0 at addr 0: {data0}")
    print(f"Read Port 0 Test Passed at addr 0!!!")

@toffee_test.testcase
async def test_read_0_at_31(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 31 ---")
    
    data31 = await ftq_pd_mem_env.agent.read_0(31)
    assert data31[0] == [1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0]
    assert data31[1] == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]
    assert data31[2] == [0, 0, 1]   
    assert data31[3] == 1
    assert data31[4] == 14
    print(f"read port 0 at addr 31: {data31}")
    print(f"Read Port 0 Test Passed at addr 31!!!")

@toffee_test.testcase
async def test_read_1_at_0(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 0 ---")
    
    data0 = await ftq_pd_mem_env.agent.read_1(0)
    assert data0[0] == [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1]
    assert data0[1] == [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
    assert data0[2] == [1, 0, 0]
    assert data0[3] == 0
    assert data0[4] == 15
    assert data0[5] == 793242654332712
    print(f"read port 1 at addr 0: {data0}")
    print(f"Read Port 1 Test Passed at addr 0!!!")

@toffee_test.testcase
async def test_read_1_at_31(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 31 ---")
    
    data31 = await ftq_pd_mem_env.agent.read_1(31)
    assert data31[0] == [1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0]
    assert data31[1] == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]
    assert data31[2] == [0, 0, 1]
    assert data31[3] == 1
    assert data31[4] == 14
    assert data31[5] == 30502265032878
    print(f"read port 1 at addr 31: {data31}")
    print(f"Read Port 1 Test Passed at addr 31!!!")

@toffee_test.testcase
async def test_write_0_at_0(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 at addr 0 ---")
    data = [[1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0], [0, 0, 1], 1, 14, 30502265032878]
    await ftq_pd_mem_env.agent.write_0(0, data)
    print(f"Write Port 0 Test Passed at addr 0!!!")

@toffee_test.testcase
async def test_write_0_at_31(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 at addr 31 ---")
    data = [[1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0], [0, 0, 1], 1, 14, 30502265032878]
    await ftq_pd_mem_env.agent.write_0(31, data)
    print(f"Write Port 0 Test Passed at addr 31!!!")

@toffee_test.testcase
async def test_write_0_at_0_and_read_1_at_0(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 at addr 0 and Read Port 0 at addr 0 ---")
    data = [[1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0], [0, 0, 1], 1, 14, 30502265032878]
    await ftq_pd_mem_env.agent.write_0(0, data)
    read_data = await ftq_pd_mem_env.agent.read_1(0)
    assert read_data == data
    print(f"Write and Read Port 1 Test Passed at addr 0!!!")