from itertools import islice
import random
from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
    FrontendTriggerAgent,
)
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import (
    bound_pair_generator,
    gen_pcs,
    to_even,
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
    当测试结束时，通知 refmodel 停止仿真
    """
    await agent.reset()


async def ftrigger_common_task1(
    agent: FrontendTriggerAgent,
    bp_update_gen,
    bp_flags_gen,
    pc_gen,
    max_task_loop=100,
    max_pcs_loop_per_task=200,
):

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


async def ftrigger_chain_task1(
    agent: FrontendTriggerAgent,
    first_chain_bp_update_gen,
    second_chain_bp_update_gen,
    bp_flags_gen,
    pc_gen,
    max_task_loop=100,
):
    task_count = 0

    while task_count < max_task_loop:
        task_count += 1

        # 生成 pcs
        pcs_list = gen_pcs([next(pc_gen)])
        cur_task_bp_flags = next(bp_flags_gen)

        if pcs_list == agent.get_old_pcs():
            continue

        await agent.set_pcs(pcs_list)

        # enable 0 and 1 breakpoints
        await agent.set_breakpoint_flags(cur_task_bp_flags)

        chain_trigger_pc_sample = random.choice(pcs_list)
        match_type_map = {">=": 2, "==": 0, "<": 3}

        # BUG: 因为 < 有 bug , 所以只生成 >= 和 == 的 bound
        bound_pair_gen = bound_pair_generator(chain_trigger_pc_sample, [">=", "=="])

        # 生成 20 个 unique 的 bound, 不足 20 也没关系
        bound_pair_list = list(set(islice(bound_pair_gen, 20)))

        for bound1, bound2 in bound_pair_list:

            first_chain_bp = next(first_chain_bp_update_gen)
            second_chain_bp = next(second_chain_bp_update_gen)

            first_chain_bp.tdata2 = to_even(bound1[1])
            first_chain_bp.matchType = match_type_map[bound1[0]]
            second_chain_bp.tdata2 = to_even(bound2[1])
            second_chain_bp.matchType = match_type_map[bound2[0]]

            # 配置链式断点, 并且验证触发逻辑
            await agent.set_breakpoint_update(0, first_chain_bp)
            await agent.set_breakpoint_update(1, second_chain_bp)
