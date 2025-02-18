import random
import toffee_test
from toffee import Executor

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
    FrontendTriggerAgent,
)
from ut_frontend.ifu.frontend_trigger.test.common_task import (
    ftrigger_common_task1,
    send_exit,
    ticks_task,
)
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    bp_flags_generator,
    bp_update_generator,
    gen_pcs,
    get_mask_one,
    int_generator,
)
from .frontend_trigger_fixture import frontend_trigger_env
from ..env import FrontendTriggerEnv


@toffee_test.testcase
async def test_smoke(frontend_trigger_env: FrontendTriggerEnv):
    await frontend_trigger_env.agent.reset()

    async def __smoke_task1():
        bp_update = BreakpointUpdateInfo()
        bp_update.chain = False
        bp_update.matchType = 0
        bp_update.select = 0
        bp_update.action = 0
        bp_update.tdata2 = 0x1234_1234_5678

        start = 0x1234_1234_5670
        pcs = [start + i * 2 for i in range(16)]

        bp_flags = BreakpointFlags()
        bp_flags.debugMode = False  # TODO: 搞清楚这个参数的含义
        bp_flags.triggerCanRaiseBpExp = True
        bp_flags.tEnableVec = [True, False, False, False]

        await frontend_trigger_env.agent.set_breakpoint_update(
            0, bp_update, bp_flags=bp_flags
        )

        await frontend_trigger_env.agent.bundle.step(2)
        await frontend_trigger_env.agent.set_pcs(pcs)
        await frontend_trigger_env.agent.bundle.step(2)

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(__smoke_task1())

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)
