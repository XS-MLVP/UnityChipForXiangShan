import pytest
import toffee_test
from toffee import Executor

from comm.constants import TAG_LONG_TIME_RUN
from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.common_task import (
    ticks_task,
    ftrigger_common_task1,
    send_exit,
)

from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    bp_flags_generator,
    bp_update_generator,
    get_mask_one,
    int_generator,
)

from .frontend_trigger_fixture import frontend_trigger_env




@toffee_test.testcase
async def test_match_eq(frontend_trigger_env: FrontendTriggerEnv):
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
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
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


@toffee_test.testcase
async def test_match_ge(
    frontend_trigger_env: FrontendTriggerEnv,
):
    await frontend_trigger_env.agent.reset()

    # 创建生成器实例
    bp_update_gen = bp_update_generator(
        pc_width=50,
        condition=lambda x: x.matchType == 2 and x.select == 0 and x.chain == False,
    )
    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and all(x.tEnableVec)
        and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
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


@pytest.mark.toffee_tags(["BUG"])
@toffee_test.testcase
async def test_match_lt(
    frontend_trigger_env: FrontendTriggerEnv,
):
    await frontend_trigger_env.agent.reset()

    # 创建生成器实例
    bp_update_gen = bp_update_generator(
        pc_width=50,
        condition=lambda x: x.matchType == 3 and x.select == 0 and x.chain == False,
    )
    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and all(x.tEnableVec)
        and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
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
