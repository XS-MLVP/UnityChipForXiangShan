from .f3predecoder_fixture import f3predecoder_env
from ..env import F3PreDecoderEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(f3predecoder_env : F3PreDecoderEnv):
    instrs = [483 for i in range(16)]


    print(await f3predecoder_env.agent.f3_predecode(instrs))
    