from .iprefetchpipe_fixture import iprefetchpipe_env
from ..env import IPrefetchPipeEnv
import toffee_test


@toffee_test.testcase
async def test_smoke(iprefetchpipe_env: IPrefetchPipeEnv):
    await iprefetchpipe_env.agent.set_s1_flush()
