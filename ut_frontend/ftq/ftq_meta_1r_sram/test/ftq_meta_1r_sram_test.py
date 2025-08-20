from .ftq_meta_1r_sram_fixture import ftq_meta_1r_sram_env
from ..env import FtqMetairSramEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(ftq_meta_1r_sram_env: FtqMetairSramEnv):
    await ftq_meta_1r_sram_env.agent.reset()
    print("\n--- Smoke Test Passed ---")