from toffee.logger import *
from toffee.triggers import *
from toffee.model import *
from dataclasses import dataclass
from typing import List, Optional

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)


@dataclass
class RefTriggerReg:
    tdata2: int
    chain: bool
    timing: bool
    matchType: int
    select: int
    action: int

    def __init__(self):
        self.tdata2 = 0
        self.chain = False
        self.timing = False
        self.matchType = 0
        self.select = 0
        self.action = 0

    def __str__(self):
        return f"tdata2: {self.tdata2}; chain: {self.chain}; timing: {self.timing}; matchType: {self.matchType}; select: {self.select}; action: {self.action}"


class BpRefImpl:
    def __init__(self):
        # bp_flags
        self.bp_flags = BreakpointFlags()

        # trigger_regs
        self.trigger_addr2idx = [0, 1, 6, 8]
        self.trigger_idx2addr = {0: 0, 1: 1, 6: 2, 8: 3}
        self.trigger_regs = [RefTriggerReg() for _ in self.trigger_addr2idx]

        # pcs
        self.pcs = [0] * 16

    @staticmethod
    def ref_match_cmp(pc: int, trigger_reg: int, match_type: int) -> bool:
        if match_type == 0:
            # equal
            return pc == trigger_reg
        elif match_type == 2:
            # greater or equal
            return pc >= trigger_reg
        elif match_type == 3:
            # less than
            return pc < trigger_reg
        else:
            raise ValueError(f"Invalid match type:{match_type}")

    def ref_update_trigger_regs(self, addr: int, bp_update: BreakpointUpdateInfo):
        assert addr < 4, "pos must be less than 4"

        self.trigger_regs[addr].tdata2 = bp_update.tdata2
        self.trigger_regs[addr].chain = bp_update.chain
        self.trigger_regs[addr].timing = False
        self.trigger_regs[addr].matchType = bp_update.matchType
        self.trigger_regs[addr].select = bp_update.select
        self.trigger_regs[addr].action = bp_update.action

    def ref_update_bp_flags(self, bp_flags: BreakpointFlags):
        self.bp_flags = bp_flags

    def ref_update_pcs(self, pcs: list[int]):
        # len(pcs) == 16
        assert len(pcs) == 16, "pcs length must be 16"
        self.pcs = pcs

    def ref_check_trigger(self) -> list[int]:
        # 16 * 4 的矩阵,记录每个pc在每个trigger上的触发情况(不检查 chain)
        pc_trigger_matrix = self.get_trigger_matrix()

        final_pc_trigger_list = []
        for pc_idx, pc_trigger_list in enumerate(pc_trigger_matrix):
            final_action = self.get_priority_action(pc_trigger_list)
            final_pc_trigger_list.append(final_action)

        assert (
            len(final_pc_trigger_list) == 16
        ), "final_pc_trigger_list length must be 16"
        return final_pc_trigger_list

    def is_trigger_enabled(self, trigger_idx: int) -> bool:
        trigger_addr = self.trigger_idx2addr[trigger_idx]
        return (
            # enable
            self.bp_flags.tEnableVec[trigger_addr]
            # select must be 0
            and self.trigger_regs[trigger_addr].select == 0
            # debugMode must be False
            and self.bp_flags.debugMode == False
        )

    def get_action_from_trigger(self, trigger_idx: int) -> int:
        """
        Args:
            trigger_idx (int): trigger 在 spec 中的索引
        """
        trigger_addr = self.trigger_idx2addr[trigger_idx]
        if (
            self.trigger_regs[trigger_addr].action == 0
            and self.bp_flags.triggerCanRaiseBpExp
        ):
            return 0
        elif self.trigger_regs[trigger_addr].action == 1:
            return 1
        else:
            return 15

    def get_trigger_matrix(self) -> list[list[int]]:
        # 初始化每个pc的触发情况矩阵（二维列表）
        #    More than one triggers can hit at the same time, but only fire one.
        # We select the first hit trigger to fire.
        num_pcs = 16
        num_triggers = 4

        # 16 * 4 的二维矩阵
        pc_trigger_matrix = [[15] * num_triggers for _ in range(num_pcs)]

        for t_reg_idx, t_reg in zip(self.trigger_addr2idx, self.trigger_regs):
            t_reg_addr = self.trigger_idx2addr[t_reg_idx]
            if not self.is_trigger_enabled(t_reg_idx):
                continue

            for pc_idx, pc in enumerate(self.pcs):
                if self.ref_match_cmp(pc, t_reg.tdata2, t_reg.matchType):
                    # 记录触发状态到矩阵
                    cur_action = self.get_action_from_trigger(t_reg_idx)
                    pc_trigger_matrix[pc_idx][t_reg_addr] = cur_action

        return pc_trigger_matrix

    # def get_priority_action(self, pc_trigger_list: list[int]) -> int:
    #     """
    #     从一个pc在每个trigger上的触发情况中获取优先级最高的触发动作, 并且处理chain trigger 的情况

    #     More than one triggers can hit at the same time, but only fire one.
    #     We select the first hit trigger to fire.
    #     Args:
    #         pc_trigger_list (list[int]): 一个pc在每个trigger上的触发情况

    #     Returns:
    #         int: 优先级最高的触发动作
    #     """
    #     tmp_chain_group = []
    #     for t_addr, t_action in enumerate(pc_trigger_list):
    #         cur_t_idx = self.trigger_addr2idx[t_addr]
    #         cur_chain = self.trigger_regs[t_addr].chain
    #         cur_timing = self.trigger_regs[t_addr].timing
    #         cur_action = t_action

    #         if len(tmp_chain_group) == 0 or tmp_chain_group[-1]["t_idx"] == (
    #             cur_t_idx - 1
    #         ):
    #             # 1. 第一个trigger没有前一个trigger
    #             # 2. 当前trigger 的 idx 是前一个trigger 的 idx - 1, 可能是chain
    #             tmp_chain_group.append(
    #                 {
    #                     "chain": cur_chain,
    #                     "timing": cur_timing,
    #                     "action": cur_action,
    #                     "t_idx": cur_t_idx,
    #                 }
    #             )
    #         else:
    #             # 3. 当前trigger 的 idx 不是前一个trigger 的 idx - 1, 不是chain
    #             # (a) 清空当前的 chain group, chain 设置为 True 必然不触发
    #             # (b) 将当前trigger加入新的 chain group
    #             tmp_chain_group.clear()
    #             tmp_chain_group.append(
    #                 {
    #                     "chain": cur_chain,
    #                     "timing": cur_timing,
    #                     "action": cur_action,
    #                     "t_idx": cur_t_idx,
    #                 }
    #             )

    #         # 如果当前trigger不是chain
    #         # 1. 如果当前chain group中的trigger数量大于1, 是 chain 的最后一个
    #         # 2. 如果当前chain group中的trigger数量等于1, 是单独的一个 trigger
    #         if tmp_chain_group[-1]["chain"] == False:
    #             # chain trigger 的 timing 必须相同
    #             all_timing_equal = all(
    #                 [
    #                     x["timing"] == tmp_chain_group[0]["timing"]
    #                     for x in tmp_chain_group
    #                 ]
    #             )
    #             # chain trigger 需要所有的 trigger 都 match
    #             all_action_match = all([x["action"] != 15 for x in tmp_chain_group])
    #             if all_timing_equal and all_action_match:
    #                 return tmp_chain_group[-1]["action"]

    #             tmp_chain_group.clear()

    #     return 15

    def get_priority_action(self, pc_trigger_list: list[int]) -> int:
        tmp_chain_group = []
        for t_addr, t_action in enumerate(pc_trigger_list):
            cur_t_idx = self.trigger_addr2idx[t_addr]
            cur_chain = self.trigger_regs[t_addr].chain
            cur_timing = self.trigger_regs[t_addr].timing
            cur_action = t_action

            # 确定当前触发器是否可加入现有链组
            if tmp_chain_group:
                last_entry = tmp_chain_group[-1]
                # 检查索引连续性和时序一致性
                if (
                    cur_t_idx != last_entry["t_idx"] + 1
                    or cur_timing != tmp_chain_group[0]["timing"]
                ):
                    tmp_chain_group.clear()

            # 将当前触发器加入链组（无论是否清空后）
            tmp_chain_group.append(
                {
                    "chain": cur_chain,
                    "action": cur_action,
                    "t_idx": cur_t_idx,
                    "timing": cur_timing,
                }
            )

            # 处理非链式触发器作为链尾的情况
            if not cur_chain:
                # 所有动作有效时触发
                if all(x["action"] != 15 for x in tmp_chain_group):
                    return cur_action
                tmp_chain_group.clear()

        # 所有触发器检查完毕仍未找到有效动作
        return 15


class BpRefModel(Model):
    def __init__(self):
        super().__init__()

        # 初始化BpRefImpl实例
        self.impl = BpRefImpl()

        # cycle驱动端口
        self.cycle_driver = DriverPort(agent_name="agent", driver_name="send_cycle")

        # reset 端口
        self.reset_driver = DriverPort(agent_name="agent", driver_name="reset")

        # 驱动端口
        self.bp_update_driver = DriverPort(
            agent_name="agent", driver_name="set_breakpoint_update"
        )
        self.bp_flags_driver = DriverPort(
            agent_name="agent", driver_name="set_breakpoint_flags"
        )
        self.pcs_driver = DriverPort(agent_name="agent", driver_name="set_pcs")

        # 监视端口
        self.bp_update_monitor = MonitorPort(
            agent_name="agent", monitor_name="monitor_breakpoint_update"
        )
        self.bp_flags_monitor = MonitorPort(
            agent_name="agent", monitor_name="monitor_breakpoint_flags"
        )
        self.pcs_monitor = MonitorPort(
            agent_name="agent", monitor_name="monitor_pcs_changed"
        )

    async def get_bp_update_driv(self):
        dict_res = await self.bp_update_driver()
        addr: int = dict_res["addr"]
        bp_update: BreakpointUpdateInfo = dict_res["bp_update"]
        bp_flags: Optional[BreakpointFlags] = dict_res["bp_flags"]
        return addr, bp_update, bp_flags

    async def get_bp_flags_driv(self) -> BreakpointFlags:
        dict_res = await self.bp_flags_driver()
        # 确保类型正确
        assert isinstance(dict_res, BreakpointFlags), "bp_flags type error"
        return dict_res

    async def get_pcs_driv(self) -> list[int]:
        dict_res = await self.pcs_driver()
        # print(f'get_pcs_driv: {dict_res}')
        return dict_res

    async def main(self):

        await self.reset_driver()
        info("reset ok")
        while True:
            cur_cycle = await self.cycle_driver()

            # 处理断点更新
            if not self.bp_update_driver.empty():
                addr, bp_update, bp_flags = await self.get_bp_update_driv()
                
                self.impl.ref_update_trigger_regs(addr, bp_update)
                if bp_flags is not None:
                    self.impl.ref_update_bp_flags(bp_flags)
                info(
                    f"cycle[{cur_cycle}][bp_update] addr: {addr}, bp_update: {bp_update}, bp_flags: {bp_flags}"
                )
                trigger_res = self.impl.ref_check_trigger()
                info(f"cycle[{cur_cycle}]trigger_res: {trigger_res}")

                await self.bp_update_monitor.put(trigger_res)

            # 处理标志更新
            if not self.bp_flags_driver.empty():
                bp_flags = await self.get_bp_flags_driv()
                self.impl.ref_update_bp_flags(bp_flags)
                info(f"cycle[{cur_cycle}][bp_flags] {bp_flags}")
                trigger_res = self.impl.ref_check_trigger()
                info(f"cycle[{cur_cycle}]trigger_res: {trigger_res}")
                await self.bp_flags_monitor.put(trigger_res)

            # 处理PCs更新
            if not self.pcs_driver.empty():
                pcs = await self.get_pcs_driv()
                old_pcs = self.impl.pcs
                old_pcs_hex = [hex(pc) for pc in old_pcs]
                pcs_hex = [hex(pc) for pc in pcs]

                info(f"cycle[{cur_cycle}]old_pcs: {old_pcs_hex}")
                info(f"cycle[{cur_cycle}]new_pcs: {pcs_hex}")

                self.impl.ref_update_pcs(pcs)

                trigger_res = self.impl.ref_check_trigger()
                info(f"cycle[{cur_cycle}]trigger_res: {trigger_res}")
                await self.pcs_monitor.put(trigger_res)

            if not self.reset_driver.empty():
                await self.reset_driver()
                info(f"cycle[{cur_cycle}]ref exit")
                break

            # 确保cycle驱动端口已清空
            assert self.cycle_driver.empty(), "cycle_driver is not empty"
