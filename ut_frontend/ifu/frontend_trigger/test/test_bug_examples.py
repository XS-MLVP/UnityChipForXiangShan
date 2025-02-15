import pytest
import toffee_test
from toffee import Executor

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)
from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.common_task import (
    ticks_task,
    send_exit,
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
        bp_update.tdata2 = 0xDEAD_DEAD_BEE5

        start = 0xDEAD_DEAD_BEE4
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


@pytest.mark.toffee_tags(["BUG"])
@toffee_test.testcase
async def test_chain_no_match_bug(frontend_trigger_env: FrontendTriggerEnv):
    """
    BUG: trigger idx 设置错误, 应该为 [0,1,6,8], 而不是 [0,1,2,3]
    """
    await frontend_trigger_env.agent.reset()

    async def __smoke_task1():
        bp_update1 = BreakpointUpdateInfo()
        bp_update1.chain = True
        bp_update1.matchType = 2
        bp_update1.select = 0
        bp_update1.action = 0
        bp_update1.tdata2 = 0x1234_1234_5600

        bp_update2 = BreakpointUpdateInfo()
        bp_update2.chain = False
        bp_update2.matchType = 0
        bp_update2.select = 0
        bp_update2.action = 0
        bp_update2.tdata2 = 0x1234_1234_5530

        start = 0x1234_1234_5530
        pcs = [start + i * 2 for i in range(16)]

        bp_flags = BreakpointFlags()
        bp_flags.debugMode = False
        bp_flags.triggerCanRaiseBpExp = True
        bp_flags.tEnableVec = [True, True, True, True]

        await frontend_trigger_env.agent.set_breakpoint_update(
            2, bp_update1, bp_flags=bp_flags
        )
        await frontend_trigger_env.agent.set_breakpoint_update(
            3, bp_update2, bp_flags=bp_flags
        )

        await frontend_trigger_env.agent.bundle.step(2)
        await frontend_trigger_env.agent.set_pcs(pcs)
        await frontend_trigger_env.agent.bundle.step(2)

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(__smoke_task1())

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)
