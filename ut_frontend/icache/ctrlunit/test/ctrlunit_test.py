from .ctrlunit_fixture import ctrlunit_env
from ..env import CtrlUnitEnv
import toffee_test


@toffee_test.testcase
async def test_smoke(ctrlunit_env: CtrlUnitEnv):


    await ctrlunit_env.agent.set_opcode(4)
