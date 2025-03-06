from toffee import Agent
from ..bundle import PreDecodeBundle
from toffee import *

class PreDecodeDataDef():
    new_instrs = []
    jmp_offsets = []
    rvcs = []
    valid_starts = []
    half_valid_starts = []
    isRets = []
    isCalls = []
    brTypes = []

    def __str__(self):
        res = f"new instrs: {self.new_instrs}\njump offsets: {self.jmp_offsets}\nrvcs: {self.rvcs}\nvalid_starts: {self.valid_starts}\nhalf_valid_starts: {self.half_valid_starts}\n"
        res += f"isRets:{self.isRets}\nisCalls:{self.isCalls}\nbyTypes:{self.brTypes}"
        return res
        

class PreDecodeAgent(Agent):
    def __init__(self, bundle:PreDecodeBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    # input: 17 x 2B raw instrs
    # return: (16 x 4B instrs, 16 x jumpoffsets, 16 x RVC, 16 x (valid), 16 x half_valid )
    @driver_method()
    async def predecode(self, instrs: list[int]) -> PreDecodeDataDef:
        for i in range(17):
            getattr(self.bundle.io._in_bits_data, f"_{i}").value = instrs[i]
        print("going to step")
        await self.bundle.step()
        print("step over")
        ret = PreDecodeDataDef()

        for i in range(16):
            ret.new_instrs.append(getattr(self.bundle.io._out._instr, f"_{i}").value)
            ret.jmp_offsets.append(getattr(self.bundle.io._out._jumpOffset, f"_{i}").value)
            ret.rvcs.append(getattr(self.bundle.io._out._pd, f"_{i}")._isRVC.value)
            
            ret.brTypes.append(getattr(self.bundle.io._out._pd, f"_{i}")._brType.value)
            ret.isCalls.append(getattr(self.bundle.io._out._pd, f"_{i}")._isCall.value)
            ret.isRets.append(getattr(self.bundle.io._out._pd, f"_{i}")._isRet.value)

            if i == 0: 
                ret.half_valid_starts.append(0)
                ret.valid_starts.append(1)

            elif i == 1:
                ret.half_valid_starts.append(1)
                ret.valid_starts.append(getattr(self.bundle.io._out._pd, f"_{i}")._valid.value)

            else:
                ret.half_valid_starts.append(getattr(self.bundle.io._out._hasHalfValid, f"_{i}").value)
                ret.valid_starts.append(getattr(self.bundle.io._out._pd, f"_{i}")._valid.value)

        return ret