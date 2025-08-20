from .ftq_meta_1r_sram_fixture import ftq_meta_1r_sram_env
from ..env import FtqMetairSramEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Smoke Test Passed ---")

@toffee_test.testcase
async def test_read0_at_0(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Read Test at Address 0  ---")
    data = await ftq_meta_1r_sram_env.agent.read_0(0)
    test_data = [42228871559087839688890920994387459653046576960819779137767868438182708524363385898872395232866436747684060057095278048975039949216259833233620415175993771, 1, 0, 1, 1, 11, 1, 0, 3437, 0, 12, 1, 1, 70386, 1, None, 0, 0, 1, 1]
    assert data == test_data, f"Expected {test_data}, but got {data}"
    print(f"Read Data at Address 0: {data}")
    print(f"Read Test Passed at Address 0!!!")

@toffee_test.testcase
async def test_read0_at_31(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Read Test at Address 31  ---")
    data = await ftq_meta_1r_sram_env.agent.read_0(31)
    test_data = [42228871559087839688890920994387459653046576960819779137767868438182708524363385898872395232866436747684060057095278048975039949216259833233620415175993771, 1, 0, 1, 1, 11, 1, 0, 3437, 0, 12, 1, 1, 70386, 1, None, 0, 0, 1, 1]
    assert data == test_data, f"Expected {test_data}, but got {data}"
    print(f"Read Data at Address 31: {data}")
    print(f"Read Test Passed at Address 31!!!")

@toffee_test.testcase
async def test_write_at_0(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Write Test at Address 0  ---")
    await ftq_meta_1r_sram_env.agent.write(0, 57696081977, [1, 0, 1, 1, 11, 1, 0, 3437, 0, 12, 1, 1, 70386, 1, None, 0, 0, 1, 1])
    print(f"Write Test Passed at Address 0!!!")

@toffee_test.testcase
async def test_write_at_31(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Write Test at Address 31  ---")
    await ftq_meta_1r_sram_env.agent.write(31, 57696081977, [1, 0, 1, 1, 11, 1, 0, 3437, 0, 12, 1, 1, 70386, 1, None, 0, 0, 1, 1])
    print(f"Write Test Passed at Address 31!!!")

@toffee_test.testcase
async def test_read_after_write(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Read After Write Test at Address 0  ---")
    await ftq_meta_1r_sram_env.agent.write(0, 57696081977, [1, 0, 1, 1, 11, 1, 0, 3437, 0, 12, 1, 1, 70386, 1, None, 0, 0, 1, 1])
    data = await ftq_meta_1r_sram_env.agent.read_0(0)
    test_data = [57696081977, 1, 0, 1, 1, 11, 1, 0, 3437, 0, 12, 1, 1, 70386, 1, None, 0, 0, 1, 1]
    assert data == test_data
    print(f"Read Data after Write at Address 0: {data}")
    print(f"Read After Write Test Passed at Address 0!!!")