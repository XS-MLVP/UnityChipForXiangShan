from importlib.metadata import requires
from toffee import Agent, driver_method, monitor_method

from comm import info
from ..bundle import FrontendTriggerBundle
import difflib

from toffee.triggers import *
from toffee.model import *
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BreakpointUpdateInfo:
    """A class representing breakpoint update information in a trigger system.

    This class encapsulates the configuration parameters needed to update a hardware
    breakpoint trigger in RISC-V debug specification.

    Attributes:
        matchType (int): 2-bit field specifying match condition:
            - 0: Equal to
            - 2: Greater than or equal to
            - 3: Less than
        select (bool): Selection status of the breakpoint
        action (int): 4-bit field defining the action to take when triggered
        chain (bool): Whether this trigger is chained to the next trigger
        tdata2 (int): 64-bit data value to match against

    Example:
        >>> bp = BreakpointUpdateInfo(matchType=0, select=True, action=1, chain=False, tdata2=0x1000)
        >>> print(bp)
        matchType: 0; select: True; action: 1; chain: False; tdata2: 1000
    """

    matchType: int  # 2 bits， 0：等于 2: 大于等于 3: 小于
    select: bool
    action: int  # 4 bits
    chain: bool
    tdata2: int  # 64 bits

    def __init__(
        self,
        matchType: int = 0,
        select: bool = False,
        action: int = 0,
        chain: bool = False,
        tdata2: int = 0,
    ):
        self.matchType = matchType
        self.select = select
        self.action = action
        self.chain = chain
        self.tdata2 = tdata2

    def __str__(self):
        return f"matchType: {self.matchType}; select: {self.select}; action: {self.action}; chain: {self.chain}; tdata2: {self.tdata2:x}"


@dataclass
class BreakpointFlags:
    """
    A class representing breakpoint flags for debugging and trigger control.

    This class manages various debug-related flags including trigger enables,
    debug mode status, and breakpoint exception settings.

    Attributes:
        tEnableVec (List[bool]): A list of 4 boolean values controlling individual triggers
        debugMode (bool): Flag indicating if debug mode is active
        triggerCanRaiseBpExp (bool): Flag controlling if triggers can raise breakpoint exceptions

    Args:
        tEnableVec (List[bool], optional): List of 4 trigger enable flags. Defaults to [False, False, False, False]
        debugMode (bool, optional): Debug mode status. Defaults to False
        triggerCanRaiseBpExp (bool, optional): Breakpoint exception enable. Defaults to False

    Example:
        >>> flags = BreakpointFlags([True, False, True, False], True, False)
        >>> print(flags)
        tEnableVec: [True, False, True, False]; debugMode: True; triggerCanRaiseBpExp: False
    """

    tEnableVec: List[bool]  # 4 elements, each is a boolean
    debugMode: bool
    triggerCanRaiseBpExp: bool

    def __init__(
        self,
        tEnableVec: List[bool] = [False] * 4,
        debugMode: bool = False,
        triggerCanRaiseBpExp: bool = False,
    ):
        self.tEnableVec = tEnableVec
        self.debugMode = debugMode
        self.triggerCanRaiseBpExp = triggerCanRaiseBpExp

    def __str__(self):
        return f"tEnableVec: {self.tEnableVec}; debugMode: {self.debugMode}; triggerCanRaiseBpExp: {self.triggerCanRaiseBpExp}"


@dataclass
class BreakpointInfo:
    """
    A class representing breakpoint information in a processor.

    Attributes:
        timing (int): The timing information for the breakpoint.
        tdata2 (int): The tdata2 value for the breakpoint trigger.
        chain (bool): Flag indicating if this breakpoint is chained to another.
        matchType (int): The type of match for the breakpoint.
        select (int): The selection value for the breakpoint.
        action (int): The action to take when breakpoint is triggered.
    """

    timing = 0
    tdata2 = 0

    chain = False
    matchType = 0
    select = 0
    action = 0

    def __str__(self):
        return f"timing: {self.timing}; tdata2: {self.tdata2:x}; chain: {self.chain}; matchType: {self.matchType}; select: {self.select}; action: {self.action}"


class FrontendTriggerAgent(Agent):
    def __init__(self, bundle: FrontendTriggerBundle):
        super().__init__(bundle)
        self.bundle = bundle
        self.old_pcs = [0] * 16
        self.old_bp_flags = BreakpointFlags()
        self.cycle = int(0)

    @driver_method()
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()

    # 查看tdata_vec内部信号！从而查看断点是否正确设置
    @driver_method()
    async def set_breakpoint_update(
        self,
        addr: int,
        bp_update: BreakpointUpdateInfo,
        bp_flags: Optional[BreakpointFlags] = None,
    ):

        assert addr < 4, "pos must be less than 4"

        self.bundle.io._frontendTrigger._tUpdate._bits._addr.value = addr
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._tdata2.value = (
            bp_update.tdata2
        )
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._chain.value = (
            bp_update.chain
        )
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._matchType.value = (
            bp_update.matchType
        )
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._select.value = (
            bp_update.select
        )
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._action.value = (
            bp_update.action
        )

        if bp_flags is not None:
            for i in range(4):
                getattr(self.bundle.io._frontendTrigger._tEnableVec, f"_{i}").value = (
                    bp_flags.tEnableVec[i]
                )
            self.bundle.io._frontendTrigger._debugMode.value = bp_flags.debugMode
            self.bundle.io._frontendTrigger._triggerCanRaiseBpExp.value = (
                bp_flags.triggerCanRaiseBpExp
            )
        self.bundle.io._frontendTrigger._tUpdate._valid.value = True
        await self.bundle.step()
        self.bundle.io._frontendTrigger._tUpdate._valid.value = False
        await self.bundle.step()

    @driver_method()
    async def set_breakpoint_flags(
        self,
        bp_flags: BreakpointFlags,
    ):
        for i in range(4):
            getattr(self.bundle.io._frontendTrigger._tEnableVec, f"_{i}").value = (
                bp_flags.tEnableVec[i]
            )
        self.bundle.io._frontendTrigger._debugMode.value = bp_flags.debugMode
        self.bundle.io._frontendTrigger._triggerCanRaiseBpExp.value = (
            bp_flags.triggerCanRaiseBpExp
        )
        await self.bundle.step(1)

    @monitor_method()
    async def monitor_breakpoint_update(self):
        if self.bundle.io._frontendTrigger._tUpdate._valid.value:
            await self.bundle.step(1)
            return self.collect_triggered()

    @monitor_method()
    async def monitor_breakpoint_flags(self):
        cur_bp_flags = BreakpointFlags()
        cur_bp_flags.tEnableVec = [
            getattr(self.bundle.io._frontendTrigger._tEnableVec, f"_{i}").value
            for i in range(4)
        ]
        cur_bp_flags.debugMode = self.bundle.io._frontendTrigger._debugMode.value
        cur_bp_flags.triggerCanRaiseBpExp = (
            self.bundle.io._frontendTrigger._triggerCanRaiseBpExp.value
        )

        bp_flags_changed = cur_bp_flags != self.old_bp_flags

        if bp_flags_changed:
            info(f"bp_flags changed: {self.old_bp_flags} -> {cur_bp_flags}")

        self.old_bp_flags = cur_bp_flags

        if bp_flags_changed:
            return self.collect_triggered()

    @monitor_method()
    async def monitor_pcs_changed(self):
        # Fetch current PC values
        cur_pcs = [getattr(self.bundle.io._pc, f"_{i}").value for i in range(16)]

        pcs_changed = cur_pcs != self.old_pcs

        self.old_pcs = cur_pcs
        if pcs_changed:
            cur_triggered = self.collect_triggered()
            return cur_triggered

    @driver_method()
    async def set_pcs(self, pcs: list[int]):
        """
        This method sets 16 consecutive program counter values, where each PC must be exactly
        2 greater than the previous one, starting from a non-negative value.

        Args:
            pcs (list[int]): A list of 16 integers representing program counter values.
                             Must satisfy:
                             - Length must be exactly 16
                             - First value must be non-negative
                             - Each subsequent value must be exactly 2 greater than previous
        Example:
            valid_pcs = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
            await set_pcs(valid_pcs)
        """
        assert len(pcs) == 16, "pcs must contain exactly 16 elements"
        assert pcs[0] >= 0, "The first element of pcs cannot be negative"
        for i in range(1, 16):
            assert (
                pcs[i] == pcs[i - 1] + 2
            ), f"pcs[{i}] ({pcs[i]}) is not exactly 2 greater than pcs[{i - 1}] ({pcs[i - 1]})"

        num_instrs = 16
        for i in range(num_instrs):
            cur_pc = getattr(self.bundle.io._pc, f"_{i}")
            cur_pc.value = pcs[i]
        await self.bundle.step()

    @driver_method()
    async def send_cycle(self, new_cycle: int):
        self.cycle = new_cycle
        await self.bundle.step()
        # BUG: driver_method 有返回值时，不应该用于 ref model 的比对
        # return self.cycle + 1

    def get_old_pcs(self) -> list[int]:
        return self.old_pcs

    def collect_triggered(self) -> list[int]:
        """
        Collects triggered values from the bundle's IO interface.

        Returns a list of integers representing the triggered values from indexes 0 to 15.
        Each value is accessed using getattr from the bundle.io._triggered object with
        format "_i" where i ranges from 0 to 15.

        Returns:
            list[int]: A list containing 16 triggered values
        """
        ret = []
        for i in range(16):
            ret.append(getattr(self.bundle.io._triggered, f"_{i}").value)
        return ret

    def collect_breakpoint_info(self) -> list[BreakpointInfo]:
        """
        Collects and returns breakpoint information from the FrontendTrigger bundle.

        This method gathers breakpoint information for 4 trigger points, including:
        - timing
        - tdata2
        - chain
        - matchType
        - select
        - action

        Returns:
            list[BreakpointInfo]: A list containing 4 BreakpointInfo objects with the
                collected trigger information from the FrontendTrigger bundle.
        """
        res = []
        for i in range(4):
            bp_res = BreakpointInfo()
            bp_res.timing = getattr(
                self.bundle.FrontendTrigger._tdataVec, f"_{i}"
            )._timing.value
            bp_res.tdata2 = getattr(
                self.bundle.FrontendTrigger._tdataVec, f"_{i}"
            )._tdata2.value
            bp_res.chain = getattr(
                self.bundle.FrontendTrigger._tdataVec, f"_{i}"
            )._chain.value
            bp_res.matchType = getattr(
                self.bundle.FrontendTrigger._tdataVec, f"_{i}"
            )._matchType.value
            bp_res.select = getattr(
                self.bundle.FrontendTrigger._tdataVec, f"_{i}"
            )._select.value
            bp_res.action = getattr(
                self.bundle.FrontendTrigger._tdataVec, f"_{i}"
            )._action.value
            res.append(bp_res)
        return res
