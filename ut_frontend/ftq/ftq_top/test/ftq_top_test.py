from .ftq_top_fixture import ftq_top_env
from ..env import FtqTopEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_top_env: FtqTopEnv):
    await ftq_top_env.agent.reset()
    print("\n--- Smoke Test Passed!!! ---")