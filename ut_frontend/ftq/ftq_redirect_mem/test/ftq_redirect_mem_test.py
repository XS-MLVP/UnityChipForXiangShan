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

# 测试读取端口1
# hisPtr_flag, hisPtr_value, ssp, sctr, TOSW_flag, TOSW_value, TOSR_flag, TOSR_value, NOS_flag, NOS_value, sc_disagree_0, sc_disagree_1
# 2.1 读取端口1的地址0
@toffee_test.testcase
async def test_read_1_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 0 ---")
    
    data0 = await ftq_redirect_mem_env.agent.read_1(0)
    print(f"data0: {data0}")
    assert data0[0] == 1
    assert data0[1] == 238
    assert data0[2] == 14
    assert data0[3] == 3
    assert data0[4] == 0
    assert data0[5] == 26
    assert data0[6] == 1
    assert data0[7] == 9
    assert data0[8] == 1
    assert data0[9] == 30
    assert data0[10] == 1
    assert data0[11] == 1
    print(f"read port 1 at addr 0: {data0}")
    print(f"Read Port 1 Test Passed at addr 0!!!")

# 2.2 读取端口1的地址31
@toffee_test.testcase
async def test_read_1_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
    await ftq_redirect_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 31 ---")
    
    data31 = await ftq_redirect_mem_env.agent.read_1(31)
    print(f"data31: {data31}")
    assert data31[0] == 1
    assert data31[1] == 238
    assert data31[2] == 14
    assert data31[3] == 3
    assert data31[4] == 0
    assert data31[5] == 26
    assert data31[6] == 1
    assert data31[7] == 9
    assert data31[8] == 1
    assert data31[9] == 30
    assert data31[10] == 1
    assert data31[11] == 1
    print(f"read port 1 at addr 31: {data31}")
    print(f"Read Port 1 Test Passed at addr 31!!!")

# # 测试读取端口2
# # hisPtr_value
# async def test_read_2_at_0(ftq_redirect_mem_env:FtqRedirectMemEnv):
#     await ftq_redirect_mem_env.agent.reset()
#     print("\n--- Testing Read Port 2 at addr 0 ---")
    
#     data0 = await ftq_redirect_mem_env.agent.read_2(0)
#     assert data0[0] == 46
#     print(f"read port 2 at addr 0: {data0}")
#     print(f"Read Port 2 Test Passed at addr 0!!!")

# # 2.2 读取端口2的地址31
# @toffee_test.testcase
# async def test_read_2_at_31(ftq_redirect_mem_env:FtqRedirectMemEnv):
#     await ftq_redirect_mem_env.agent.reset()
#     print("\n--- Testing Read Port 2 at addr 31 ---")
    
#     data31 = await ftq_redirect_mem_env.agent.read_2(31)
#     assert data31[0] == 46
#     print(f"read port 2 at addr 31: {data31}")
#     print(f"Read Port 2 Test Passed at addr 31!!!")