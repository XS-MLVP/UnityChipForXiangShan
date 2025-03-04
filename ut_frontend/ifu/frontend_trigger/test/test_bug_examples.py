import pytest
import toffee_test
from toffee import Executor

from comm.constants import TAG_LONG_TIME_RUN
from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)
from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.common_task import (
    ftrigger_common_task1,
    ticks_task,
    send_exit,
)
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    bp_flags_generator,
    bp_update_generator,
    int_generator,
)


from .frontend_trigger_fixture import frontend_trigger_env


@pytest.mark.toffee_tags(["BUG"])
@toffee_test.testcase
async def test_bug_match_lt(frontend_trigger_env: FrontendTriggerEnv):
    """
    BUG:当 matchType 为 3 时(小于), 断点比较逻辑出错
    BUG:在 refmodel 中, 即使对比失败，最后还是会输出 passed（测试环境无法捕获 assert）
    """
    await frontend_trigger_env.agent.reset()

    async def __smoke_task1():
        bp_update = BreakpointUpdateInfo()
        bp_update.chain = False
        bp_update.matchType = 3
        bp_update.select = 0
        bp_update.action = 0
        bp_update.tdata2 = 0xDEAD_DEAD_BEE6

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
    # BUG:必须要手动通知 refmodel 停止, refmodel 不会自动停止
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


N = 1000
T = 1 << 50


@pytest.mark.toffee_tags(["BUG", TAG_LONG_TIME_RUN])
@pytest.mark.parametrize(
    "pc_min,pc_max",
    [(r * (T // N), (r + 1) * (T // N) if r < N else T) for r in range(N)],
)
@toffee_test.testcase
async def test_match_eq_new(
    frontend_trigger_env: FrontendTriggerEnv, pc_min: int, pc_max: int
):
    """
    BUG: 启用功能覆盖率，如果测试数量过多，bash 中的 ARGMAX 过长导致程序崩溃
    """
    await frontend_trigger_env.agent.reset()

    # 创建生成器实例
    bp_update_gen = bp_update_generator(
        pc_width=50,
        condition=lambda x: x.matchType == 0 and x.select == 0 and x.chain == False,
    )
    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and all(x.tEnableVec)
        and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=pc_min, max_value=pc_max - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_common_task1(
                frontend_trigger_env.agent, bp_update_gen, bp_flags_gen, pc_gen
            )
        )

    # 通知参考模型停止模拟
    await send_exit(frontend_trigger_env.agent)
