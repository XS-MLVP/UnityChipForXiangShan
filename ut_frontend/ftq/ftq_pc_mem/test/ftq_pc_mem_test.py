from .ftq_pc_mem_fixture import ftq_pc_mem_env
from ..env import FtqPcMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Smoke Test Passed ---")

#test read ifuPtr
#1.1 read ifuPtr at 0
@toffee_test.testcase
async def test_read_ifuPtr_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read IfuPtr At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_ifuPtr(0)
    assert data == [735087668007195, 431996364060896, 1]
    print(f"read port ifuPtr at addr 0: {data}")
    print(f"Read IfuPtr Test Passed at addr 0!!!")

#1.2 read ifuPtr at 31
@toffee_test.testcase
async def test_read_ifuPtr_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read IfuPtr At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_ifuPtr(31)
    assert data == [735087668007195, 431996364060896, 1]
    print(f"read port ifuPtr at addr 31: {data}")
    print(f"Read IfuPtr Test Passed at addr 31!!!")

#test read ifuPtrPlus1
#2.1 read ifuPtrPlus1 at 0
@toffee_test.testcase
async def test_read_ifuPtrPlus1_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read IfuPtrPlus1 At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_ifuPtrPlus1(0)
    assert data == [735087668007195, 431996364060896, 1]
    print(f"read port ifuPtrPlus1 at addr 0: {data}")
    print(f"Read IfuPtrPlus1 Test Passed at addr 0!!!")

#2.2 read ifuPtrPlus1 at 31
@toffee_test.testcase
async def test_read_ifuPtrPlus1_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read IfuPtrPlus1 At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_ifuPtrPlus1(31)
    assert data == [735087668007195, 431996364060896, 1]
    print(f"read port ifuPtrPlus1 at addr 31: {data}")
    print(f"Read IfuPtrPlus1 Test Passed at addr 31!!!")

#test read ifuPtrPlus2 
#3.1 read ifuPtrPlus2 at 0
@toffee_test.testcase
async def test_read_ifuPtrPlus2_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read IfuPtrPlus2 At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_ifuPtrPlus2(0)
    assert data == [735087668007195]
    print(f"read port ifuPtrPlus2 at addr 0: {data}")
    print(f"Read IfuPtrPlus2 Test Passed at addr 0!!!")

#3.2 read ifuPtrPlus2 at 31
@toffee_test.testcase
async def test_read_ifuPtrPlus2_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read IfuPtrPlus2 At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_ifuPtrPlus2(31)
    assert data == [735087668007195]
    print(f"read port ifuPtrPlus2 at addr 31: {data}")
    print(f"Read IfuPtrPlus2 Test Passed at addr 31!!!")

#test read pfPtr
#4.1 read pfPtr at 0
@toffee_test.testcase
async def test_read_pfPtr_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read PfPtr At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_pfPtr(0)
    assert data == [735087668007195, 431996364060896]
    print(f"read port pfPtr at addr 0: {data}")
    print(f"Read PfPtr Test Passed at addr 0!!!")

#4.2 read pfPtr at 31
@toffee_test.testcase
async def test_read_pfPtr_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read PfPtr At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_pfPtr(31)
    assert data == [735087668007195, 431996364060896]
    print(f"read port pfPtr at addr 31: {data}")
    print(f"Read PfPtr Test Passed at addr 31!!!")

#test read pfPtrPlus1
#5.1 read pfPtrPlus1 at 0
@toffee_test.testcase
async def test_read_pfPtrPlus1_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read PfPtrPlus1 At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_pfPtrPlus1(0)
    assert data == [735087668007195, 431996364060896]
    print(f"read port pfPtrPlus1 at addr 0: {data}")
    print(f"Read PfPtrPlus1 Test Passed at addr 0!!!")

#5.2 read pfPtrPlus1 at 31
@toffee_test.testcase
async def test_read_pfPtrPlus1_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read PfPtrPlus1 At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_pfPtrPlus1(31)
    assert data == [735087668007195, 431996364060896]
    print(f"read port pfPtrPlus1 at addr 31: {data}")
    print(f"Read PfPtrPlus1 Test Passed at addr 31!!!")

#test read commPtr
#6.1 read commPtr at 0
@toffee_test.testcase
async def test_read_commPtr_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read CommPtr At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_commPtr(0)
    assert data == [735087668007195]
    print(f"read port commPtr at addr 0: {data}")
    print(f"Read CommPtr Test Passed at addr 0!!!")

#6.2 read commPtr at 31
@toffee_test.testcase
async def test_read_commPtr_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read CommPtr At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_commPtr(31)
    assert data == [735087668007195]
    print(f"read port commPtr at addr 31: {data}")
    print(f"Read CommPtr Test Passed at addr 31!!!")

#test read commPtrPlus1
#7.1 read commPtrPlus1 at 0
@toffee_test.testcase
async def test_read_commPtrPlus1_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read CommPtrPlus1 At 0 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_commPtrPlus1(0)
    assert data == [735087668007195]
    print(f"read port commPtrPlus1 at addr 0: {data}")
    print(f"Read CommPtrPlus1 Test Passed at addr 0!!!")

#7.2 read commPtrPlus1 at 31
@toffee_test.testcase
async def test_read_commPtrPlus1_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Read CommPtrPlus1 At 31 Test Passed ---")
    data = await ftq_pc_mem_env.agent.read_commPtrPlus1(31)
    assert data == [735087668007195]
    print(f"read port commPtrPlus1 at addr 31: {data}")
    print(f"Read CommPtrPlus1 Test Passed at addr 31!!!")

#test write port
#8.1 write  at 0
@toffee_test.testcase
async def test_write_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Write At 0 Test Passed ---")
    data = [1, 1, 1]
    await ftq_pc_mem_env.agent.write(0, data)
    print(f"write port at addr 0: {data}")
    print(f"Write At 0 Test Passed!!!")

#8.2 write  at 31
@toffee_test.testcase
async def test_write_at_31(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Write At 31 Test Passed ---")
    data = [1, 1, 1]
    await ftq_pc_mem_env.agent.write(31, data)
    print(f"write port at addr 31: {data}")
    print(f"Write At 31 Test Passed!!!")

#test read write port
#9.1 read write port at 0
@toffee_test.testcase
async def test_writeAndread_at_0(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Write At 0 Test Passed ---")
    data = [1, 1, 1]
    await ftq_pc_mem_env.agent.write(0, data)
    rdata = await ftq_pc_mem_env.agent.read_ifuPtr(0)
    print(f"write port at addr 0: {data}")
    print(f"read port at addr 0: {rdata}")
    assert data == rdata
    print(f"Write And Read At 0 Test Passed!!!")
