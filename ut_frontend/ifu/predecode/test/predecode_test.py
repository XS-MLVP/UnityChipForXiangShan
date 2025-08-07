import toffee_test
from .predecode_fixture import predecode_env
from ..env import PreDecodeEnv

@toffee_test.testcase
async def test_smoke(predecode_env : PreDecodeEnv):
    fake_instrs = [54541 for i in range(17)]

    res = await predecode_env.agent.predecode(fake_instrs)
    print(res)
