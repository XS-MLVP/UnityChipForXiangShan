from .ftq_pc_mem_fixture import ftq_pc_mem_env
from ..env import FtqPcMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_pc_mem_env: FtqPcMemEnv):
    await ftq_pc_mem_env.agent.reset()
    print("\n--- Smoke Test Passed ---")