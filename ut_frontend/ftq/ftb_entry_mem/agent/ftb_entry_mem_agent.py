from toffee import Agent, driver_method, monitor_method
from ..bundle import FtbEntryMemBundle

class BaseData:
    isJalr = 0
    brSlotsOffset = 0
    brSlotsValid = 0
    tailSlotOffset = 0
    tailSlotValid = 0
    tailSlotSharing = 0

class R0Data(BaseData):
    isCall = 0
    isRet = 0

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
        data = R0Data()
        data.isJalr = self.bundle.io._rdata_0._isJalr.value
        data.brSlotsOffset = self.bundle.io._rdata_0._brSlots_0._offset.value
        data.brSlotsValid = self.bundle.io._rdata_0._brSlots_0._valid.value
        data.tailSlotOffset = self.bundle.io._rdata_0._tailSlot._offset.value
        data.tailSlotValid = self.bundle.io._rdata_0._tailSlot._valid.value
        data.tailSlotSharing = self.bundle.io._rdata_0._tailSlot._sharing.value
        data.isCall = self.bundle.io._rdata_0._isCall.value
        data.isRet = self.bundle.io._rdata_0._isRet.value
        # await self.bundle.step()
        return data

    # read in port 1
    @driver_method()
    async def read_1(self, raddr: int):
        self.bundle.io._ren._1.value = 1
        self.bundle.io._raddr._1.value = raddr
        await self.bundle.step()
        self.bundle.io._ren._1.value = 0
        data = BaseData()
        data.isJalr = self.bundle.io._rdata_1._isJalr.value
        data.brSlotsOffset = self.bundle.io._rdata_1._brSlots_0._offset.value
        data.brSlotsValid = self.bundle.io._rdata_1._brSlots_0._valid.value
        data.tailSlotOffset = self.bundle.io._rdata_1._tailSlot._offset.value
        data.tailSlotValid = self.bundle.io._rdata_1._tailSlot._valid.value
        data.tailSlotSharing = self.bundle.io._rdata_1._tailSlot._sharing.value
        # await self.bundle.step()
        return data

    # write in port 0
    @driver_method()
    async def write_0(self, waddr: int, wdata: R0Data):
        self.bundle.io._wen_0.value = 1
        self.bundle.io._waddr_0.value = waddr
        self.bundle.io._wdata_0._isJalr.value = wdata.isJalr
        self.bundle.io._wdata_0._brSlots_0._offset.value = wdata.brSlotsOffset
        self.bundle.io._wdata_0._brSlots_0._valid.value = wdata.brSlotsValid
        self.bundle.io._wdata_0._tailSlot._offset.value = wdata.tailSlotOffset
        self.bundle.io._wdata_0._tailSlot._valid.value = wdata.tailSlotValid
        self.bundle.io._wdata_0._tailSlot._sharing.value = wdata.tailSlotSharing
        self.bundle.io._wdata_0._isCall.value = wdata.isCall
        self.bundle.io._wdata_0._isRet.value = wdata.isRet
        await self.bundle.step()
