from .ftq_redirect_mem_fixture import ftq_redirect_mem_env
from ..env import FtqRedirectMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Smoke Test Passed!!! ---")

# 测试读取端口0
# hisPtr_flag, hisPtr_value, ssp, sctr, TOSW_flag, TOSW_value, TOSR_flag, TOSR_value, NOS_flag, NOS_value, topAddr

#1.1 读取端口0的地址0
@toffee_test.testcase
async def test_read_0_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 0 ---")
    
    data0 = await ftq_redirect_mem_env.agent.read_0(0)
    assert data0[0] == 0
    assert data0[1] == 199
    assert data0[2] == 8
    assert data0[3] == 6
    assert data0[4] == 1
    assert data0[5] == 5
    assert data0[6] == 1
    assert data0[7] == 15
    assert data0[8] == 0
    assert data0[9] ==  1
    assert data0[10] == 84348167230997
    print(f"read port 0 at addr 0: {data0}")

# 1.2 读取端口0的地址1
@toffee_test.testcase
async def test_read_0_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 31 ---")
    data31 = await ftq_redirect_mem_env.agent.read_0(31)
    assert data31[0] == 0
    assert data31[1] == 199
    assert data31[2] == 8
    assert data31[3] == 6
    assert data31[4] == 1
    assert data31[5] == 5
    assert data31[6] == 1
    assert data31[7] == 15
    assert data31[8] == 0
    assert data31[9] == 1
    assert data31[10] == 84348167230997
    print(f"read port 0 at addr 31: {data31}")
    print(f"Read Port 0 Test Passed at addr 31!!!")

# 测试读取端口1
# hisPtr_flag, hisPtr_value, ssp, sctr, TOSW_flag, TOSW_value, TOSR_flag, TOSR_value, NOS_flag, NOS_value, sc_disagree_0, sc_disagree_1
# 2.1 读取端口1的地址0
@toffee_test.testcase
async def test_read_1_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 0 ---")
    
    data0 = await ftq_redirect_mem_env.agent.read_1(0)
    print(f"data0: {data0}")
    assert data0[0] == 0
    assert data0[1] == 199
    assert data0[2] == 8
    assert data0[3] == 6
    assert data0[4] == 1
    assert data0[5] == 5
    assert data0[6] == 1
    assert data0[7] == 15
    assert data0[8] == 0
    assert data0[9] == 1
    assert data0[10] == 0
    assert data0[11] == 0
    print(f"read port 1 at addr 0: {data0}")
    print(f"Read Port 1 Test Passed at addr 0!!!")

# 2.2 读取端口1的地址31
@toffee_test.testcase
async def test_read_1_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 31 ---")
    
    data31 = await ftq_redirect_mem_env.agent.read_1(31)
    assert data31[0] == 0
    assert data31[1] == 199
    assert data31[2] == 8
    assert data31[3] == 6
    assert data31[4] == 1
    assert data31[5] == 5
    assert data31[6] == 1
    assert data31[7] == 15
    assert data31[8] ==  0
    assert data31[9] == 1
    assert data31[10] == 0
    assert data31[11] == 0
    print(f"read port 1 at addr 31: {data31}")
    print(f"Read Port 1 Test Passed at addr 31!!!")

# 测试读取端口2
# hisPtr_value
# 3.1 读取端口2的地址0
@toffee_test.testcase
async def test_read_2_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 2 at addr 0 ---")
    
    data0 = await ftq_redirect_mem_env.agent.read_2(0)
    assert data0[0] == 199
    print(f"read port 2 at addr 0: {data0}")
    print(f"Read Port 2 Test Passed at addr 0!!!")

# 3.2 读取端口2的地址31
@toffee_test.testcase
async def test_read_2_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 2 at addr 31 ---")
    
    data31 = await ftq_redirect_mem_env.agent.read_2(31)
    assert data31[0] == 199
    print(f"read port 2 at addr 31: {data31}")
    print(f"Read Port 2 Test Passed at addr 31!!!")

# 测试写入端口0
# hisPtr_flag, hisPtr_value, ssp, sctr, TOSW_flag, TOSW_value, TOSR_flag, TOSR_value, NOS_flag, NOS_value, topAddr, sc_disagree_0, sc_disagree_1
# 4.1 写入端口0的地址0
@toffee_test.testcase
async def test_write_0_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 at addr 0 ---")
    data = [1, 100, 13, 3, 0, 26, 1, 8, 1, 30, 1234567890123456, 0, 0]
    await ftq_redirect_mem_env.agent.write_0(data, 0)
    print(f"write port 0 at addr 0: {data}")
    print(f"Write Port 0 Test Passed at addr 0!!!")

# 4.2 写入端口0的地址31
@toffee_test.testcase
async def test_write_0_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 at addr 31 ---")
    data = [1, 100, 13, 3, 0, 26, 1, 8, 1, 30, 1234567890123456, 0, 0]
    await ftq_redirect_mem_env.agent.write_0(data, 31)
    print(f"write port 0 at addr 31: {data}")
    print(f"Write Port 0 Test Passed at addr 31!!!")

# 测试写入端口0 and 读取端口0
# 5.1 写入端口0的地址0后读取端口0的地址0
@toffee_test.testcase
async def test_write_0_and_read_0_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    # await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 and Read Port 0 at addr 0 ---")
    data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    await ftq_redirect_mem_env.agent.write_0(data, 0)
    print(f"write port 0 at addr 0: {data}")
    print(f"Write Port 0 Test Passed at addr 0!!!")
    read_data = await ftq_redirect_mem_env.agent.read_0(0)
    res_data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert read_data == res_data
    print(f"read port 0 at addr 0: {read_data}")
    print(f"Read Port 0 Test Passed at addr 0!!!")