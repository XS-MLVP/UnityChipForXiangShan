from toffee import Agent, driver_method, monitor_method
from ..bundle import FtqPdMemBundle

class FtqPdMemAgent(Agent):
    def __init__(self, bundle:FtqPdMemBundle):
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
        self.bundle.io._ren._0.value = 1
        self.bundle.io._raddr._0.value = raddr
        await self.bundle.step()
        self.bundle.io._ren._0.value = 0
        data = list()
        data.append([getattr(self.bundle.io._rdata_0._brMask, f"_{i}").value for i in range(16)])
        data.append([getattr(self.bundle.io._rdata_0._rvcMask, f"_{i}").value for i in range(16)])
        data.append([getattr(self.bundle.io._rdata_0._jmp.Info._bits, f"_{i}").value for i in range(3)])
        data.append(self.bundle.io._rdata_0._jmp.Info._valid.value)
        data.append(self.bundle.io._rdata_0._jmp.Offset.value)
        return data

    #read in port 1
    @driver_method()
    async def read_1(self, raddr: int):
        self.bundle.io._ren._1.value = 1
        self.bundle.io._raddr._1.value = raddr
        await self.bundle.step()
        self.bundle.io._ren._1.value = 0
        data = list()
        data.append([getattr(self.bundle.io._rdata_1._brMask, f"_{i}").value for i in range(16)])
        data.append([getattr(self.bundle.io._rdata_1._rvcMask, f"_{i}").value for i in range(16)])
        data.append([getattr(self.bundle.io._rdata_1._jmp.Info._bits, f"_{i}").value for i in range(3)])
        data.append(self.bundle.io._rdata_1._jmp.Info._valid.value)
        data.append(self.bundle.io._rdata_1._jmp.Offset.value)
        data.append(self.bundle.io._rdata_1._jalTarget.value)
        return data
    
    #write in port 0
    @driver_method()
    async def write_0(self, waddr: int, data: list):
        self.bundle.io._wen_0.value = 1
        self.bundle.io._waddr_0.value = waddr
        for i in range(16):
            getattr(self.bundle.io._wdata_0._brMask, f"_{i}").value = data[0][i]
            getattr(self.bundle.io._wdata_0._rvcMask, f"_{i}").value = data[1][i]
        for i in range(3):
            getattr(self.bundle.io._wdata_0._jmp.Info._bits, f"_{i}").value = data[2][i]
        self.bundle.io._wdata_0._jmp.Info._valid.value = data[3]
        self.bundle.io._wdata_0._jmp.Offset.value = data[4]
        self.bundle.io._wdata_0._jalTarget.value = data[5]
        await self.bundle.step()
        self.bundle.io._wen_0.value = 0
