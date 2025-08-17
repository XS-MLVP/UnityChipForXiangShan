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
    
    #read in port ifuPtr
    @driver_method()
    async def read_ifuPtr(self, raddr: int):
        self.bundle.io._ifuPtr._w_value = raddr
        await self.bundle.step()
        data = list()
        data.append(self.bundle.io._ifuPtr._rdata._startAddr.value)
        data.append(self.bundle.io._ifuPtr._rdata._nextLineAddr.value)
        data.append(self.bundle.io._ifuPtr._rdata._fallThruError.value)    
        return data

    #read in port ifuPtrPlus1
    @driver_method()
    async def read_ifuPtrPlus1(self, raddr: int):
        self.bundle.io._ifuPtrPlus1._w_value = raddr
        await self.bundle.step()
        data = list()
        data.append(self.bundle.io._ifuPtr.Plus1_rdata._startAddr.value)
        data.append(self.bundle.io._ifuPtr.Plus1_rdata._nextLineAddr.value)
        data.append(self.bundle.io._ifuPtr.Plus1_rdata._fallThruError.value)    
        return data
    
    #read in port ifuPtrPlus2
    @driver_method()
    async def read_ifuPtrPlus2(self, raddr: int):
        self.bundle.io._ifuPtrPlus2._w_value = raddr
        await self.bundle.step()
        data = [self.bundle.io._ifuPtr.Plus2_rdata._startAddr.value]
        return data

    #read in port pfPtr
    @driver_method()
    async def read_pfPtr(self, raddr: int):
        self.bundle.io._pfPtr._w_value = raddr
        await self.bundle.step()
        data = list()
        data.append(self.bundle.io._pfPtr._rdata._startAddr.value)
        data.append(self.bundle.io._pfPtr._rdata._nextLineAddr.value)
        return data

    #read in port pfPtrPlus1
    @driver_method()
    async def read_pfPtrPlus1(self, raddr: int):
        self.bundle.io._pfPtrPlus1._w_value = raddr
        await self.bundle.step()
        data = list()
        data.append(self.bundle.io._pfPtr.Plus1_rdata._startAddr.value)
        data.append(self.bundle.io._pfPtr.Plus1_rdata._nextLineAddr.value)
        return data

    #read in port commPtr
    async def read_commPtr(self, raddr: int):
        self.bundle.io._commPtr._w_value = raddr
        await self.bundle.step()
        data = [self.bundle.io._commPtr._rdata._startAddr.value]
        return data

    #read in port commPtrPlus1
    async def read_commPtrPlus1(self, raddr: int):
        self.bundle.io._commPtrPlus1._w_value = raddr
        await self.bundle.step()
        data = [self.bundle.io._commPtr.Plus1_rdata._startAddr.value]
        return data

    #write in port 0
    async def write(self, waddr: int, wdata: list):
        self.bundle.io._wen.value = 1
        self.bundle.io._waddr.value = waddr
        self.bundle.io._wdata._startAddr.value = wdata[0]
        self.bundle.io._wdata._nextLineAddr.value = wdata[1]
        self.bundle.io._wdata._fallThruError.value = wdata[2]
        await self.bundle.step()
        self.bundle.io._wen.value = 0