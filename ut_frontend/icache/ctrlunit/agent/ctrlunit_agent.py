from toffee import Agent
from..bundle import CtrlUnitBundle

class CtrlUnitAgent(Agent):
    def __init__(self, bundle: CtrlUnitBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle
        
    async def set_opcode(self, set_value):  
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
        self.bundle.auto_in._a._valid.value = 1
        print("\nBefore setting, auto_in_a_bits_opcode is: ",self.bundle.auto_in._a._bits._opcode.value)
        self.bundle.auto_in._a._bits._opcode.value = set_value
        print("After setting, auto_in_a_bits_opcode is :",self.bundle.auto_in._a._bits._opcode.value)
        await self.bundle.step(10)
        print("Output auto_in_d_bits_opcode is :",self.bundle.auto_in._d._bits._opcode.value)