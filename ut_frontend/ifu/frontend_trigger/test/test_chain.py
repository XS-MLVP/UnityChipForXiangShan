import toffee_test
from toffee import Executor

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)
from ut_frontend.ifu.frontend_trigger.env.frontend_trigger_env import FrontendTriggerEnv
from ut_frontend.ifu.frontend_trigger.test.common_task import (
    ftrigger_chain_task1,
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
async def test_chain1_no_match(
    frontend_trigger_env: FrontendTriggerEnv,
):
    """
    测试: chain 设为 True 时, 不应该有 trigger 触发
    """
    await frontend_trigger_env.agent.reset()

    # 创建生成器实例
    bp_update_gen = bp_update_generator(
        pc_width=50,
        condition=lambda x: x.select == 0 and x.chain == True,
        # and x.action == 0,
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
async def test_chain_match_smoke(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 正常情况下, chain 的触发
    """
    await frontend_trigger_env.agent.reset()

    # 创建生成器实例
    bp_update_chain_gen = bp_update_generator(
        pc_width=50,
        condition=lambda x: x.select == 0 and x.chain == True and x.matchType != 3,
        # and x.action == 0,
    )

    bp_update_no_chain_gen = bp_update_generator(
        pc_width=50,
        condition=lambda x: x.select == 0 and x.chain == False and x.matchType != 3,
    )

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
        bp_update2.tdata2 = 0x1234_1234_5630

        start = 0x1234_1234_5630
        pcs = [start + i * 2 for i in range(16)]

        bp_flags = BreakpointFlags()
        bp_flags.debugMode = False
        bp_flags.triggerCanRaiseBpExp = True
        bp_flags.tEnableVec = [True, True, True, True]

        await frontend_trigger_env.agent.set_breakpoint_update(
            0, bp_update1, bp_flags=bp_flags
        )
        await frontend_trigger_env.agent.set_breakpoint_update(
            1, bp_update2, bp_flags=bp_flags
        )

        await frontend_trigger_env.agent.bundle.step(2)
        await frontend_trigger_env.agent.set_pcs(pcs)
        await frontend_trigger_env.agent.bundle.step(2)

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(__smoke_task1())

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain_no_match_smoke(frontend_trigger_env: FrontendTriggerEnv):
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
        bp_flags.debugMode = False  # TODO: 搞清楚这个参数的含义
        bp_flags.triggerCanRaiseBpExp = True
        bp_flags.tEnableVec = [True, True, True, True]

        await frontend_trigger_env.agent.set_breakpoint_update(
            0, bp_update1, bp_flags=bp_flags
        )
        await frontend_trigger_env.agent.set_breakpoint_update(
            1, bp_update2, bp_flags=bp_flags
        )

        await frontend_trigger_env.agent.bundle.step(2)
        await frontend_trigger_env.agent.set_pcs(pcs)
        await frontend_trigger_env.agent.bundle.step(2)

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(__smoke_task1())

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain_match(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 正常情况下, chain 的触发
    """
    await frontend_trigger_env.agent.reset()

    first_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 0 and x.chain == True
    )
    second_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 0 and x.chain == False
    )

    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and x.tEnableVec == [True, True, False, False]
        and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task1(
                agent=frontend_trigger_env.agent,
                first_chain_bp_update_gen=first_chain_bp_update_gen,
                second_chain_bp_update_gen=second_chain_bp_update_gen,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain_no_match1(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 任何一个链式断点不满足触发 select 条件时, 不应该触发
    """
    await frontend_trigger_env.agent.reset()

    first_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 1 and x.chain == True
    )
    second_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 0 and x.chain == False
    )

    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and x.tEnableVec == [True, True, False, False]
        and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task1(
                agent=frontend_trigger_env.agent,
                first_chain_bp_update_gen=first_chain_bp_update_gen,
                second_chain_bp_update_gen=second_chain_bp_update_gen,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain_no_match2(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 任何一个链式断点不满足触发 select 条件时, 不应该触发
    """
    await frontend_trigger_env.agent.reset()

    first_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 0 and x.chain == True
    )
    second_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 1 and x.chain == False
    )

    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and x.tEnableVec == [True, True, False, False]
        and x.triggerCanRaiseBpExp
    )
    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task1(
                agent=frontend_trigger_env.agent,
                first_chain_bp_update_gen=first_chain_bp_update_gen,
                second_chain_bp_update_gen=second_chain_bp_update_gen,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain_no_match3(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 任何一个链上的断点没有 enable 时, 链式断点不会触发
    """
    await frontend_trigger_env.agent.reset()

    first_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 0 and x.chain == True
    )
    second_chain_bp_update_gen = bp_update_generator(
        pc_width=50, condition=lambda x: x.select == 0 and x.chain == False
    )

    available_enable_vecs = [
        [True, False, False, False],
        [False, True, False, False],
        [False, False, False, False],
    ]
    bp_flags_gen = bp_flags_generator(
        condition=lambda x: x.debugMode == False
        and x.tEnableVec in available_enable_vecs
        and x.triggerCanRaiseBpExp
    )

    pc_gen = int_generator(
        min_value=0, max_value=get_mask_one(50) - 30, condition=lambda x: x & 1 == 0
    )

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(
            ftrigger_chain_task1(
                agent=frontend_trigger_env.agent,
                first_chain_bp_update_gen=first_chain_bp_update_gen,
                second_chain_bp_update_gen=second_chain_bp_update_gen,
                bp_flags_gen=bp_flags_gen,
                pc_gen=pc_gen,
            )
        )

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)
