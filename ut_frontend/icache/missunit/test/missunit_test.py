from .missunit_fixture import icachemissunit_env
from ..env import ICacheMissUnitEnv
import toffee_test


@toffee_test.testcase
async def test_smoke(icachemissunit_env: ICacheMissUnitEnv):
    await icachemissunit_env.agent.fencei_func(1)
