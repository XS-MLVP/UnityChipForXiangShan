from toffee import Agent
from ..bundle import F3PreDecoderBundle

class F3PreDecodeData():
    brTypes = [] 
    isCalls = [] 
    isRets = []

    def __str__(self):
        return f"brTypes: {self.brTypes}\nisCalls: {self.isCalls}\nisRets: {self.isRets}"

class F3PreDecoderAgent(Agent):
    
    def __init__(self, bundle:F3PreDecoderBundle):
        super().__init__(bundle)
        self.bundle = bundle
    

    async def f3_predecode(self, instrs: list[int]) -> F3PreDecodeData:
        for i in range(16):
            getattr(self.bundle.io._in_instr, f"_{i}").value= instrs[i]

        await self.bundle.step()

        ret = F3PreDecodeData()
        for i in range(16):
            ret.brTypes.append(getattr(self.bundle.io._out_pd, f"_{i}")._brType.value)
            ret.isCalls.append(getattr(self.bundle.io._out_pd, f"_{i}")._isCall.value)
            ret.isRets.append(getattr(self.bundle.io._out_pd, f"_{i}")._isRet.value)
        return ret