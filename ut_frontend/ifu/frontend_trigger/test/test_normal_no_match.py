import pytest
import toffee_test
from toffee import Executor

from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_common_task import (
    ticks_task,
    ftrigger_common_task,
    send_exit,
)

from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    bp_flags_generator,
    bp_update_generator,
    get_mask_one,
    int_generator,
)
from .frontend_trigger_fixture import frontend_trigger_env, gr


@toffee_test.testcase
async def test_tselect1_no_match(
    frontend_trigger_env: FrontendTriggerEnv,
):
    """
    测试点: 测试 tselect=1 时，不应该触发任何断点
    """

    bp_update_gen = bp_update_generator(pc_width=50, condition=lambda x: x.select == 1)
    bp_flags_gen = bp_flags_generator(condition=lambda x: all(x.tEnableVec))
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    await frontend_trigger_env.agent.reset()

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_common_task(
                frontend_trigger_env.agent, bp_update_gen, bp_flags_gen, pc_gen
            )
        )

    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_enable0_no_match(
    frontend_trigger_env: FrontendTriggerEnv,
):
    """
    测试点: 测试 `enable=0` 时，不应该触发任何断点
    """
    bp_update_gen = bp_update_generator(pc_width=50)
    bp_flags_gen = bp_flags_generator(condition=lambda x: not any(x.tEnableVec))
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    await frontend_trigger_env.agent.reset()

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_common_task(
                frontend_trigger_env.agent, bp_update_gen, bp_flags_gen, pc_gen
            )
        )
        # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain_no_match(
    frontend_trigger_env: FrontendTriggerEnv,
):
    """
    测试点: 测试 `chain` 为 True 时，该断点不应该触发
    """
    
    bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.chain == True
    )

    bp_flags_gen = bp_flags_generator()

    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    await frontend_trigger_env.agent.reset()

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_common_task(
                frontend_trigger_env.agent, bp_update_gen, bp_flags_gen, pc_gen
            )
        )
        # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)
