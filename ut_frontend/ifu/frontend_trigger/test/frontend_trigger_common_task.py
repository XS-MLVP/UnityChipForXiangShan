import random
from typing import List, Literal
from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointUpdateInfo,
    FrontendTriggerAgent,
)
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    chain_bound_generator,
    gen_pcs,
    get_mask_one,
)


async def ticks_task(agent: FrontendTriggerAgent, max_ticks=None):
    """
    手动对时钟信号进行计数, 并且用于驱动 refmodel
    """
    counter = 0
    while max_ticks is None or counter < max_ticks:
        await agent.send_cycle(counter)
        counter += 1


async def send_exit(agent: FrontendTriggerAgent):
    """
    当测试结束时，通知 refmodel 停止仿真（用 reset driver）
    """
    await agent.reset()


async def ftrigger_common_task(
    agent: FrontendTriggerAgent,
    bp_update_gen,
    bp_flags_gen,
    pc_gen,
    max_task_loop=100,
    max_pcs_loop_per_task=200,
):
    """
    通用的单个断点触发测试任务，用于测试断点触发逻辑
    """
    task_count = 0
    trigger_info_list: list[BreakpointUpdateInfo] = []  # 存储断点更新信息的列表

    while task_count < max_task_loop:
        task_count += 1
        trigger_info_list.clear()
        # 生成触发PC列表
        trigger_pc_list = gen_pcs([next(pc_gen)])
        trigger_pc_sample = random.sample(trigger_pc_list, 4)
        # 配置每个断点的更新信息
        for i in range(4):
            bp_update = next(bp_update_gen)
            bp_update.tdata2 = trigger_pc_sample[i]
            trigger_info_list.append(bp_update)
            await agent.set_breakpoint_update(i, bp_update)
        # 设置断点标志
        await agent.set_breakpoint_flags(next(bp_flags_gen))

        # 随机生成PC值并验证触发逻辑
        for _ in range(max_pcs_loop_per_task):
            trigger_pcs = [x.tdata2 for x in trigger_info_list]
            sample_count = random.randint(0, 4)
            trigger_pcs_sample = [next(pc_gen)]
            if sample_count > 0:
                trigger_pcs_sample = random.sample(trigger_pcs, sample_count)

            rand_pcs = gen_pcs(trigger_pcs_sample)
            assert len(rand_pcs) == 16, "rand_pcs 的长度必须为 16"

            if rand_pcs == agent.get_old_pcs():
                continue

            await agent.set_pcs(rand_pcs)


async def ftrigger_chain_task_match(
    agent: FrontendTriggerAgent,
    chained_bp_update_gen_list,
    bp_flags_gen,
    pc_gen,
    bound_types: List[Literal[">=", "==", "<"]],
    max_task_loop=10,
):
    """
    测试链式断点触发逻辑，对于不同的链式断点配置，会遍历 0-3 的起始地址
    """
    task_count = 0
    chain_cnt = len(chained_bp_update_gen_list)
    match_type_map = {">=": 2, "==": 0, "<": 3}
    while task_count < max_task_loop:
        task_count += 1

        # 生成 pcs
        pcs_list = gen_pcs([next(pc_gen)])  # pcs_list 相邻元素之间差 2
        cur_task_bp_flags = next(bp_flags_gen)  # tEnableVec 没有用到
        pc_sample = random.choice(pcs_list)
        chained_bound_gen = chain_bound_generator(
            input_int=pc_sample,
            bound_types=bound_types,
            count=chain_cnt,
            min_value=0,
            max_value=get_mask_one(50),
        )

        # 生成 10 个 unique 的 bound, 不足 10 也没关系
        chained_bound_vec_list = [next(chained_bound_gen) for _ in range(10)]
        # Process each bound vector from the generated list
        for cur_bound_vec in chained_bound_vec_list:
            # Try chain positions at each valid starting address
            for start_addr in range(4 - chain_cnt + 1):
                # Reset and set breakpoint enables for current chain
                cur_task_bp_flags.tEnableVec = [False] * 4
                for i in range(chain_cnt):
                    cur_task_bp_flags.tEnableVec[start_addr + i] = True

                # Configure all breakpoints in the chain at once
                for i, cur_bound in enumerate(cur_bound_vec):
                    cur_bp_update = next(chained_bp_update_gen_list[i])
                    cur_bp_update.tdata2 = cur_bound[1]
                    cur_bp_update.matchType = match_type_map[cur_bound[0]]  # match_type

                    await agent.set_breakpoint_update(
                        start_addr + i, cur_bp_update, bp_flags=cur_task_bp_flags
                    )

                # Validate trigger logic with current PC list
                await agent.set_pcs(pcs_list)


async def ftrigger_chain_task_select_no_match(
    agent: FrontendTriggerAgent,
    chained_bp_update_gen_list,
    bp_flags_gen,
    pc_gen,
    bound_types: List[Literal[">=", "==", "<"]],
    max_task_loop=10,
):
    """
    测试链式断点触发逻辑，对于不同的链式断点配置，会遍历 0-3 的起始地址
    但会随机将 select 设置为 True 或 False，来模拟 select 条件不满足的情况
    """

    task_count = 0
    chain_cnt = len(chained_bp_update_gen_list)
    match_type_map = {">=": 2, "==": 0, "<": 3}
    while task_count < max_task_loop:
        task_count += 1

        # 生成 pcs
        pcs_list = gen_pcs([next(pc_gen)])  # pcs_list 相邻元素之间差 2
        cur_task_bp_flags = next(bp_flags_gen)  # tEnableVec 没有用到
        pc_sample = random.choice(pcs_list)
        chained_bound_gen = chain_bound_generator(
            input_int=pc_sample,
            bound_types=bound_types,
            count=chain_cnt,
            min_value=0,
            max_value=get_mask_one(50),
        )

        # 生成 20 个 unique 的 bound, 不足 20 也没关系
        chained_bound_vec_list = [next(chained_bound_gen) for _ in range(10)]
        # Process each bound vector from the generated list
        for cur_bound_vec in chained_bound_vec_list:
            # Try chain positions at each valid starting address
            for start_addr in range(4 - chain_cnt + 1):
                # Reset and set breakpoint enables for current chain
                cur_task_bp_flags.tEnableVec = [False] * 4
                for i in range(chain_cnt):
                    cur_task_bp_flags.tEnableVec[start_addr + i] = True

                # Configure all breakpoints in the chain at once
                for i, cur_bound in enumerate(cur_bound_vec):
                    cur_bp_update = next(chained_bp_update_gen_list[i])
                    cur_bp_update.tdata2 = cur_bound[1]
                    cur_bp_update.matchType = match_type_map[cur_bound[0]]  # match_type
                    cur_bp_update.select = random.randint(0, 1)  # 随机选择 select

                    await agent.set_breakpoint_update(
                        start_addr + i, cur_bp_update, bp_flags=cur_task_bp_flags
                    )

                # Validate trigger logic with current PC list
                await agent.set_pcs(pcs_list)


async def ftrigger_chain_task_enable_no_match(
    agent: FrontendTriggerAgent,
    chained_bp_update_gen_list,
    bp_flags_gen,
    pc_gen,
    bound_types: List[Literal[">=", "==", "<"]],
    max_task_loop=10,
):
    """
    测试链式断点触发逻辑，对于不同的链式断点配置，会遍历 0-3 的起始地址
    但会随机将 enable 设置为 True 或 False，来模拟 enable 条件不满足的情况
    """
    task_count = 0
    chain_cnt = len(chained_bp_update_gen_list)
    match_type_map = {">=": 2, "==": 0, "<": 3}
    while task_count < max_task_loop:
        task_count += 1

        # 生成 pcs
        pcs_list = gen_pcs([next(pc_gen)])  # pcs_list 相邻元素之间差 2
        cur_task_bp_flags = next(bp_flags_gen)  # tEnableVec 没有用到
        pc_sample = random.choice(pcs_list)
        chained_bound_gen = chain_bound_generator(
            input_int=pc_sample,
            bound_types=bound_types,
            count=chain_cnt,
            min_value=0,
            max_value=get_mask_one(50),
        )

        # 生成 20 个 unique 的 bound, 不足 20 也没关系
        chained_bound_vec_list = [next(chained_bound_gen) for _ in range(10)]
        # Process each bound vector from the generated list
        for cur_bound_vec in chained_bound_vec_list:
            # Try chain positions at each valid starting address
            for start_addr in range(4 - chain_cnt + 1):
                # Reset and set breakpoint enables for current chain
                cur_task_bp_flags.tEnableVec = [False] * 4
                for i in range(chain_cnt):
                    cur_task_bp_flags.tEnableVec[start_addr + i] = random.choice(
                        [True, False]
                    )

                # Configure all breakpoints in the chain at once
                for i, cur_bound in enumerate(cur_bound_vec):
                    cur_bp_update = next(chained_bp_update_gen_list[i])
                    cur_bp_update.tdata2 = cur_bound[1]
                    cur_bp_update.matchType = match_type_map[cur_bound[0]]  # match_type

                    await agent.set_breakpoint_update(
                        start_addr + i, cur_bp_update, bp_flags=cur_task_bp_flags
                    )

                # Validate trigger logic with current PC list
                await agent.set_pcs(pcs_list)
