from ..bundle import RVCExpanderIOBundle
from toffee import Agent, driver_method

class RVCExpanderAgent(Agent):
    def __init__(self, bundle:RVCExpanderIOBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    # @driver_method()
    async def expand(self, instr, fsIsOff): 
        self.bundle._in.value = instr
        self.bundle._fsIsOff.value = fsIsOff
        
        await self.bundle.step()
        return self.bundle._out_bits.value, self.bundle._ill.value