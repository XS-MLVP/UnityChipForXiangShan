from toffee import Agent, driver_method, monitor_method
from ..bundle import FtqPcMemBundle

class FtqPcMemAgent(Agent):
    def __init__(self, bundle:FtqPcMemBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
    
    #read in port 0
    @driver_method()
    async def read_0(self, raddr: int):
        self.bundle.io_ren_0.value = 1
        