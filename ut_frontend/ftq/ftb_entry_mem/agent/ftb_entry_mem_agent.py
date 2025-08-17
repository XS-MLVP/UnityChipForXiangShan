from toffee import Agent, driver_method, monitor_method
from ..bundle import FtbEntryMemBundle

class FtbEntryMemAgent(Agent):
    def __init__(self, bundle: FtbEntryMemBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
    
    # read in port 0
    @driver_method()
    async def read_0(self, raddr: int):
        self.bundle.io._ren._0.value = 1
        self.bundle.io._raddr._0.value = raddr
        await self.bundle.step()
        self.bundle.io._ren._0.value = 0
        data = list()
        data.append(self.bundle.io._rdata_0._isJalr.value)
        data.append(self.bundle.io._rdata_0._brSlots_0._offset.value)
        data.append(self.bundle.io._rdata_0._brSlots_0._valid.value)
        data.append(self.bundle.io._rdata_0._tailSlot._offset.value)
        data.append(self.bundle.io._rdata_0._tailSlot._valid.value)
        data.append(self.bundle.io._rdata_0._tailSlot._sharing.value)
        data.append(self.bundle.io._rdata_0._isCall.value)
        data.append(self.bundle.io._rdata_0._isRet.value)
        return data

    # read in port 1
    @driver_method()
    async def read_1(self, raddr: int):
        self.bundle.io._ren._1.value = 1
        self.bundle.io._raddr._1.value = raddr
        await self.bundle.step()
        self.bundle.io._ren._1.value = 0
        data = list()
        data.append(self.bundle.io._rdata_1._isJalr.value)
        data.append(self.bundle.io._rdata_1._brSlots_0._offset.value)
        data.append(self.bundle.io._rdata_1._brSlots_0._valid.value)
        data.append(self.bundle.io._rdata_1._tailSlot._offset.value)
        data.append(self.bundle.io._rdata_1._tailSlot._valid.value)
        data.append(self.bundle.io._rdata_1._tailSlot._sharing.value)
        return data

    # write in port 0
    @driver_method()
    async def write_0(self, waddr: int, wdata: list):
        self.bundle.io._wen_0.value = 1
        self.bundle.io._waddr_0.value = waddr
        self.bundle.io._wdata_0._isJalr.value = wdata[0]
        self.bundle.io._wdata_0._brSlots_0._offset.value = wdata[1]
        self.bundle.io._wdata_0._brSlots_0._valid.value = wdata[2]
        self.bundle.io._wdata_0._tailSlot._offset.value = wdata[3]
        self.bundle.io._wdata_0._tailSlot._valid.value = wdata[4]
        self.bundle.io._wdata_0._tailSlot._sharing.value = wdata[5]
        self.bundle.io._wdata_0._isCall.value = wdata[6]
        self.bundle.io._wdata_0._isRet.value = wdata[7]
        await self.bundle.step()
