from toffee import Agent, driver_method, monitor_method
from ..bundle import FtqMeta1rSramBundle

class FtqMeta1rSramAgent(Agent):
    def __init__(self, bundle: FtqMeta1rSramBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
    
    @driver_method()
    async def read_0(self, raddr: int):
        self.bundle.io._raddr_0.value = raddr
        self.bundle.io.ren_0.value = 1
        await self.bundle.step()
        self.bundle.io.ren_0.value = 0
        data = list()
        data.append(self.bundle.io._rdata_0_meta.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._isCall.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._isRet.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._isJalr.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._valid.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._brSlots_0._offset.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._brSlots_0._sharing.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._brSlots_0._valid.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._brSlots_0._lower.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._brSlots_0._tarStat.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._tailSlot._offset.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._tailSlot._sharing.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._tailSlot._valid.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._tailSlot._lower.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._tailSlot._tarStat.value)
        data.append(self.bundle.io._rdata_0_ftb_entry.pftAddr.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._carry.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._last_may_be_rvi_call.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._strong_bias._0.value)
        data.append(self.bundle.io._rdata_0_ftb_entry._strong_bias._1.value)
        return data

    @driver_method()
    async def write(self, waddr: int, wdata_meta: int, wdata: list):
        self.bundle.io._wen.value = 1
        self.bundle.io._waddr.value = waddr
        self.bundle.io._wdata_meta.value = wdata_meta
        self.bundle.io._wdata_ftb_entry._isCall.value = wdata[0]
        self.bundle.io._wdata_ftb_entry._isRet.value = wdata[1]
        self.bundle.io._wdata_ftb_entry._isJalr.value = wdata[2]
        self.bundle.io._wdata_ftb_entry._valid.value = wdata[3]
        self.bundle.io._wdata_ftb_entry._brSlots_0._offset.value = wdata[4]
        self.bundle.io._wdata_ftb_entry._brSlots_0._sharing.value = wdata[5]
        self.bundle.io._wdata_ftb_entry._brSlots_0._valid.value = wdata[6]
        self.bundle.io._wdata_ftb_entry._brSlots_0._lower.value = wdata[7]
        self.bundle.io._wdata_ftb_entry._brSlots_0._tarStat.value = wdata[8]
        self.bundle.io._wdata_ftb_entry._tailSlot._offset.value = wdata[9]
        self.bundle.io._wdata_ftb_entry._tailSlot._sharing.value = wdata[10]
        self.bundle.io._wdata_ftb_entry._tailSlot._valid.value = wdata[11]
        self.bundle.io._wdata_ftb_entry._tailSlot._lower.value = wdata[12]
        self.bundle.io._wdata_ftb_entry._tailSlot._tarStat.value = wdata[13]
        self.bundle.io._wdata_ftb_entry.pftAddr.value = wdata[14]
        self.bundle.io._wdata_ftb_entry._carry.value = wdata[15]
        self.bundle.io._wdata_ftb_entry._last_may_be_rvi_call.value = wdata[16]
        self.bundle.io._wdata_ftb_entry._strong_bias._0.value = wdata[17]
        self.bundle.io._wdata_ftb_entry._strong_bias._1.value = wdata[18]
        await self.bundle.step()
        self.bundle.io._wen.value = 0