import pytest
import toffee_test
from toffee import Executor

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)
from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_common_task import (
    send_exit,
    ticks_task,
)


from .frontend_trigger_fixture import frontend_trigger_env


@pytest.mark.toffee_tags(["BUG"])
@toffee_test.testcase
async def test_bug_match_lt(frontend_trigger_env: FrontendTriggerEnv):
    """
    当 matchType 为 3 时(小于), 断点比较逻辑出错
    """
    await frontend_trigger_env.agent.reset()

    async def __smoke_task1():
        bp_update = BreakpointUpdateInfo()
        bp_update.chain = False
        bp_update.matchType = 3
        bp_update.select = 0
        bp_update.action = 0
        bp_update.tdata2 = 0xDEAD_BEE8

        start = 0xDEAD_BEE4
        pcs = [start + i * 2 for i in range(16)]

        bp_flags = BreakpointFlags()
        bp_flags.debugMode = False
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
