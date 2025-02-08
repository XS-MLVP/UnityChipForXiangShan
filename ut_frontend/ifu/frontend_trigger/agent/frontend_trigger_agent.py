from toffee import Agent, driver_method
from ..bundle import FrontendTriggerBundle
import difflib

# 设置断点的控制数据类
class BreakpointReq():
    data = 0
    chain = False
    matchType = 0
    select = 0

# 断点信息，一部分来自内部信号
class BreakpointInfo():
    timing = 0
    tdata2 = 0 
    chain = False
    matchType = 0
    select = 0
    action = 0

    def __str__(self):
        return f"timing: {self.timing}; tdata2: {self.tdata2}; chain: {self.chain}; matchType: {self.matchType}; select: {self.select}; action: {self.action}"

class FrontendTriggerAgent(Agent):
    def __init__(self, bundle:FrontendTriggerBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()

    # 查看tdata_vec内部信号！从而查看断点是否正确设置
    @driver_method()
    async def set_breakpoint(self, pos: int, req: BreakpointReq, _raise:bool = True, enable:bool=True) -> list[BreakpointInfo]:
        self.bundle.io._frontendTrigger._tUpdate._bits._addr.value = pos
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._tdata2.value = req.data
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._chain.value = req.chain
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._matchType.value = req.matchType
        self.bundle.io._frontendTrigger._tUpdate._bits._tdata._select.value = req.select
        getattr(self.bundle.io._frontendTrigger._tEnableVec, f"_{pos}").value = enable
        self.bundle.io._frontendTrigger._triggerCanRaiseBpExp.value = _raise
        self.bundle.io._frontendTrigger._tUpdate._valid.value = True
        await self.bundle.step(2)

        res = []

        for i in range(4):
            bp_res = BreakpointInfo()
            bp_res.timing = getattr(self.bundle.FrontendTrigger._tdataVec, f"_{i}")._timing.value
            bp_res.tdata2 = getattr(self.bundle.FrontendTrigger._tdataVec, f"_{i}")._tdata2.value
            bp_res.chain = getattr(self.bundle.FrontendTrigger._tdataVec, f"_{i}")._chain.value
            bp_res.matchType = getattr(self.bundle.FrontendTrigger._tdataVec, f"_{i}")._matchType.value
            bp_res.select = getattr(self.bundle.FrontendTrigger._tdataVec, f"_{i}")._select.value
            bp_res.action = getattr(self.bundle.FrontendTrigger._tdataVec, f"_{i}")._action.value
            res.append(bp_res)
        return res
    
    # param: pcs: 16 x pc
    # return: triggered?s: 16 x triggered
    @driver_method()
    async def check(self, pcs: list[int]) -> list[int]:
        num_instrs = 16
        for i in range(num_instrs):
            getattr(self.bundle.io._pc, f"_{i}").value = pcs[i]
        await self.bundle.step()

        ret = []

        for i in range(num_instrs):
            ret.append(getattr(self.bundle.io._triggered, f"_{i}").value)

        return ret