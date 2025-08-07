import toffee_test
from toffee import Executor


from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_common_task import (
    ftrigger_chain_task_select_no_match,
    ftrigger_chain_task_match,
    ticks_task,
    ftrigger_common_task,
    send_exit,
)

from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    bp_flags_generator,
    bp_update_generator,
    chained_bp_update_generator,
    get_bound_type,
    get_mask_one,
    int_generator,
)
from .frontend_trigger_fixture import frontend_trigger_env


max_test_loop = 100


@toffee_test.testcase
async def test_chain2_select_no_match(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试点：链式断点个数为 2 时，且随机一个 select 条件不满足，不应该触链式断点
    """
    await frontend_trigger_env.agent.reset()

    chained_bp_update_gen_list = chained_bp_update_generator(pc_width=50, chain_count=2)

    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False and x.triggerCanRaiseBpExp
    )

    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task_select_no_match(
                agent=frontend_trigger_env.agent,
                chained_bp_update_gen_list=chained_bp_update_gen_list,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
                bound_types=get_bound_type(),
                max_task_loop=max_test_loop,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain3_select_no_match(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试点：链式断点个数为 3 时，且随机一个 select 条件不满足，不应该触链式断点
    """
    await frontend_trigger_env.agent.reset()

    chained_bp_update_gen_list = chained_bp_update_generator(pc_width=50, chain_count=3)

    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task_select_no_match(
                agent=frontend_trigger_env.agent,
                chained_bp_update_gen_list=chained_bp_update_gen_list,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
                bound_types=get_bound_type(),
                max_task_loop=max_test_loop,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain4_select_no_match(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试点：链式断点个数为 4 时，且随机一个 select 条件不满足，不应该触链式断点
    """
    await frontend_trigger_env.agent.reset()
    chained_bp_update_gen_list = chained_bp_update_generator(pc_width=50, chain_count=4)

    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task_select_no_match(
                agent=frontend_trigger_env.agent,
                chained_bp_update_gen_list=chained_bp_update_gen_list,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
                bound_types=get_bound_type(),
                max_task_loop=max_test_loop,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)
