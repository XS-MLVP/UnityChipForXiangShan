from .mainpipe_fixture import icachemainpipe_env
from ..env import ICacheMainPipeEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(icachemainpipe_env: ICacheMainPipeEnv):
    await icachemainpipe_env.agent.set_flush()