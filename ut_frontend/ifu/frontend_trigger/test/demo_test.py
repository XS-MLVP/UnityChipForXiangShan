import toffee_test
from .frontend_trigger_fixture import frontend_trigger_env
from ..env import FrontendTriggerEnv
from ..agent import BreakpointReq

@toffee_test.testcase
async def test_smoke(frontend_trigger_env: FrontendTriggerEnv):
    await frontend_trigger_env.agent.reset()

    bp_req = BreakpointReq()
    bp_req.chain = False
    bp_req.data = 121213242
    bp_req.matchType = 0
    bp_req.select = 0

    bp_infos = await frontend_trigger_env.agent.set_breakpoint(0, bp_req)   
    # bp_infos = await frontend_trigger_env.agent.set_breakpoint(2, bp_req)   
    for i in range(4):
        print(bp_infos[i])

    start=121213230
    pcs = [start+i*2 for i in range(16)]

    print(await frontend_trigger_env.agent.check(pcs))