from .waylookup_fixture import waylookup_env
from ..env import WayLookupEnv
import toffee_test


@toffee_test.testcase
async def test_smoke(waylookup_env: WayLookupEnv):
    await waylookup_env.agent.flush_write_ptr()
