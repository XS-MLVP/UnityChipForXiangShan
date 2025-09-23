from .ftb_entry_mem_fixture  import ftb_entry_mem_env
from ..env import FtbEntryMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Smoke Test Passed ---")

# 测试读取端口0
#isCall, isRet, isJalr, brSlots_offset, brSlots_valid, tailSlot_offset, tailSlot_valid, brSlots_mask, tailSlot_sharing
# 1.1 读取端口0的地址0
@toffee_test.testcase
async def test_read_0_at_0(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 0 ---")
    
    data0 = await ftb_entry_mem_env.agent.read_0(0)
    assert data0[0] == 0
    assert data0[1] == 14
    assert data0[2] == 0
    assert data0[3] == 11
    assert data0[4] == 1
    assert data0[5] == 0
    assert data0[6] == 0
    assert data0[7] == 0
    print(f"read port 0 at addr 0: {data0}")
    print(f"Read Port 0 Test Passed at addr 0!!!")

# 1.2 读取端口0的地址31
@toffee_test.testcase
async def test_read_0_at_31(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Read Port 0 at addr 31 ---")

    data31 = await ftb_entry_mem_env.agent.read_0(31)
    assert data31[0] == 0
    assert data31[1] == 1
    assert data31[2] == 0
    assert data31[3] == 11
    assert data31[4] == 0
    assert data31[5] == 1
    assert data31[6] == 0
    assert data31[7] == 0
    print(f"read port 0 at addr 31: {data31}")
    print(f"Read Port 0 Test Passed at addr 31!!!")

# 测试读取端口1
# isJalr, brSlots_offset, brSlots_valid, tailSlot_offset, tailSlot_valid, tailSlot_sharing
# 2.1 读取端口1的地址0
@toffee_test.testcase
async def test_read_1_at_0(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 0 ---")

    data0 = await ftb_entry_mem_env.agent.read_1(0)
    assert data0[0] == 0
    assert data0[1] == 14
    assert data0[2] == 0
    assert data0[3] == 11
    assert data0[4] == 1
    assert data0[5] == 0
    print(f"read port 1 at addr 0: {data0}")
    print(f"Read Port 1 Test Passed at addr 0!!!")

# 2.2 读取端口1的地址31
@toffee_test.testcase
async def test_read_1_at_31(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Read Port 1 at addr 31 ---")

    data31 = await ftb_entry_mem_env.agent.read_1(31)
    assert data31[0] == 0
    assert data31[1] == 1
    assert data31[2] == 0
    assert data31[3] == 11
    assert data31[4] == 0
    assert data31[5] == 1
    print(f"read port 1 at addr 31: {data31}")
    print(f"Read Port 1 Test Passed at addr 31!!!")

# 测试写入端口0
# isCall, isRet, isJalr, brSlots_offset, brSlots_valid, tailSlot_offset, tailSlot_valid, tailSlot_sharing
# 3.1 写入端口0的地址0
@toffee_test.testcase
async def test_write_0(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 ---")

    await ftb_entry_mem_env.agent.write_0(0, [0, 14, 0, 11, 1, 0, 0, 0])
    print(f"Write Port 0 Test Passed!!!")

# 3.2 写入端口0的地址31
@toffee_test.testcase
async def test_write_0_at_31(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Write Port 0 at addr 31 ---")

    await ftb_entry_mem_env.agent.write_0(31, [0, 1, 0, 11, 0, 1, 0, 0])
    print(f"Write Port 0 Test Passed!!!")

# 测试读入和写出端口
@toffee_test.testcase
async def test_read_write(ftb_entry_mem_env: FtbEntryMemEnv):
    await ftb_entry_mem_env.agent.reset()
    print("\n--- Testing Read and Write Port ---")

    # 写入端口0
    await ftb_entry_mem_env.agent.write_0(0, [1, 1, 1, 11, 1, 1, 1, 1])
    print("Write to Port 0 at addr 0 completed.")

    # 读取端口0
    data0 = await ftb_entry_mem_env.agent.read_0(0)
    assert data0 == [1, 1, 1, 11, 1, 1, 1, 1]
    print(f"Read from Port 0 at addr 0: {data0}")

    print(f"Read and Write Port Test Passed!!!")