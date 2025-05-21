import toffee_test
from toffee import Executor

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)
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
from .frontend_trigger_fixture import frontend_trigger_env





@toffee_test.testcase
async def test_chain4_match_smoke(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 正常情况下, chain 的触发，4 连锁情况
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
        bp_update1.matchType = 2  # 大于等于
        bp_update1.select = 0
        bp_update1.action = 0
        bp_update1.tdata2 = 0x1234_1234_5600

        bp_update2 = BreakpointUpdateInfo()
        bp_update2.chain = True
        bp_update2.matchType = 2  # 大于等于
        bp_update2.select = 0
        bp_update2.action = 0
        bp_update2.tdata2 = 0x1234_1234_5610

        bp_update3 = BreakpointUpdateInfo()
        bp_update3.chain = True
        bp_update3.matchType = 2  # 大于等于
        bp_update3.select = 0
        bp_update3.action = 0
        bp_update3.tdata2 = 0x1234_1234_5620

        bp_update4 = BreakpointUpdateInfo()
        bp_update4.chain = False  # 链式断点末尾
        bp_update4.matchType = 0  # 等于
        bp_update4.select = 0
        bp_update4.action = 0
        bp_update4.tdata2 = 0x1234_1234_5630

        start = 0x1234_1234_5620
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
        await frontend_trigger_env.agent.set_breakpoint_update(
            2, bp_update3, bp_flags=bp_flags
        )

        await frontend_trigger_env.agent.set_breakpoint_update(
            3, bp_update4, bp_flags=bp_flags
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
async def test_chain3_match_smoke(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 正常情况下, chain 的触发，3 连锁情况
    """
    await frontend_trigger_env.agent.reset()

    chain_cnt = 3

    async def __smoke__chain3_task1():
        bp_update1 = BreakpointUpdateInfo()
        bp_update1.chain = True
        bp_update1.matchType = 2  # 大于等于
        bp_update1.select = 0
        bp_update1.action = 0
        bp_update1.tdata2 = 0x1234_1234_5600

        bp_update2 = BreakpointUpdateInfo()
        bp_update2.chain = True
        bp_update2.matchType = 2  # 大于等于
        bp_update2.select = 0
        bp_update2.action = 0
        bp_update2.tdata2 = 0x1234_1234_5610

        bp_update3 = BreakpointUpdateInfo()
        bp_update3.chain = False  # 链式断点末尾
        bp_update3.matchType = 0  # 等于
        bp_update3.select = 0
        bp_update3.action = 0
        bp_update3.tdata2 = 0x1234_1234_5630

        start = 0x1234_1234_5620
        pcs = [start + i * 2 for i in range(16)]

        bp_flags = BreakpointFlags()
        bp_flags.debugMode = False
        bp_flags.triggerCanRaiseBpExp = True

        
        # 遍历所有可能的起始地址
        for start_addr in range(4 - chain_cnt + 1):
            # 只启动链式断点
            bp_flags.tEnableVec = [False] * 4
            for i in range(chain_cnt):
                bp_flags.tEnableVec[start_addr + i] = True

            await frontend_trigger_env.agent.set_breakpoint_update(
                start_addr, bp_update1, bp_flags=bp_flags
            )
            await frontend_trigger_env.agent.set_breakpoint_update(
                start_addr + 1, bp_update2, bp_flags=bp_flags
            )
            await frontend_trigger_env.agent.set_breakpoint_update(
                start_addr + 2, bp_update3, bp_flags=bp_flags
            )
            await frontend_trigger_env.agent.bundle.step(2)
            await frontend_trigger_env.agent.set_pcs(pcs)
            await frontend_trigger_env.agent.bundle.step(2)

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(__smoke__chain3_task1())

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)


@toffee_test.testcase
async def test_chain2_match_smoke(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 正常情况下, chain 的触发，2 连锁情况
    """
    await frontend_trigger_env.agent.reset()

    chain_cnt = 2

    async def __smoke__chain3_task1():
        bp_update1 = BreakpointUpdateInfo()
        bp_update1.chain = True
        bp_update1.matchType = 2  # 大于等于
        bp_update1.select = 0
        bp_update1.action = 0
        bp_update1.tdata2 = 0x1234_1234_5600



        bp_update2 = BreakpointUpdateInfo()
        bp_update2.chain = False  # 链式断点末尾
        bp_update2.matchType = 0  # 等于
        bp_update2.select = 0
        bp_update2.action = 0
        bp_update2.tdata2 = 0x1234_1234_5630

        start = 0x1234_1234_5620
        pcs = [start + i * 2 for i in range(16)]

        bp_flags = BreakpointFlags()
        bp_flags.debugMode = False
        bp_flags.triggerCanRaiseBpExp = True

        for start_addr in range(4 - chain_cnt + 1):
            # 只启动链式断点
            bp_flags.tEnableVec = [False] * 4
            for i in range(chain_cnt):
                bp_flags.tEnableVec[start_addr + i] = True

            await frontend_trigger_env.agent.set_breakpoint_update(
                start_addr, bp_update1, bp_flags=bp_flags
            )
            await frontend_trigger_env.agent.set_breakpoint_update(
                start_addr + 1, bp_update2, bp_flags=bp_flags
            )

            await frontend_trigger_env.agent.bundle.step(2)
            await frontend_trigger_env.agent.set_pcs(pcs)
            await frontend_trigger_env.agent.bundle.step(2)

    async with Executor(exit="any") as exec:
        exec(ticks_task(frontend_trigger_env.agent))
        exec(__smoke__chain3_task1())

    # notify the refmodel to stop the simulation
    await send_exit(frontend_trigger_env.agent)



@toffee_test.testcase
async def test_chain_no_match_smoke(frontend_trigger_env: FrontendTriggerEnv):
    """
    测试: 链式断点有一个不满足触发条件时, 不应该触发
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


