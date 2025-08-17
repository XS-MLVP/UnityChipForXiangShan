from .ftq_pd_mem_fixture import ftq_pd_mem_env
from ..env import FtqPdMemEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_pd_mem_env:FtqPdMemEnv):
    await ftq_pd_mem_env.agent.reset()
    print("\n--- Smoke Test Passed!!! ---")
