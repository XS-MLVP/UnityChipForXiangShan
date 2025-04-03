from .icache_fixture import icache_env
from ..env import ICacheEnv
import toffee_test


@toffee_test.testcase
async def test_smoke(icache_env: ICacheEnv):
    await icache_env.agent.fencei_meta_array_func(1)
