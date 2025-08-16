from toffee import Agent, driver_method, monitor_method
from ..bundle import FtqRedirectMemBundle

class BaseData:
    hisPtr_flag = 0
    hisPtr_value = 0
    ssp = 0
    sctr = 0
    TOSW_flag = 0
    TOSW_value = 0
    TOSR_flag = 0
    TOSR_value = 0
    NOS_flag = 0
    NOS_value = 0

class wDataPort0(BaseData):
    topAddr = 0
    sc_disagree_0 = 0
    sc_disagree_1 = 0


class FtqRedirectMemAgent(Agent):
    def __init__(self, bundle:FtqRedirectMemBundle):
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
        
        # get data 
        data = list()
        data.append(self.bundle.io._rdata_0._histPtr._flag.value)
        data.append(self.bundle.io._rdata_0._histPtr._value.value)
        data.append(self.bundle.io._rdata_0._ssp.value)
        data.append(self.bundle.io._rdata_0._sctr.value)
        data.append(self.bundle.io._rdata_0._TOSW._flag.value)
        data.append(self.bundle.io._rdata_0._TOSW._value.value)
        data.append(self.bundle.io._rdata_0._TOSR._flag.value)
        data.append(self.bundle.io._rdata_0._TOSR._value.value)
        data.append(self.bundle.io._rdata_0._NOS._flag.value)
        data.append(self.bundle.io._rdata_0._NOS._value.value)
        data.append(self.bundle.io._rdata_0._topAddr.value)
        await self.bundle.step()
        return data
    
    #read in port 1
    @driver_method()
    async def read_1(self, raddr: int):
        self.bundle.io._ren._1.value = 1
        self.bundle.io._raddr._1.value = raddr  
        await self.bundle.step()
        self.bundle.io._ren._1.value = 0
        #get data
        data = list()
        data.append(self.bundle.io._rdata_1._histPtr._flag.value)
        data.append(self.bundle.io._rdata_1._histPtr._value.value)
        data.append(self.bundle.io._rdata_1._ssp.value)
        data.append(self.bundle.io._rdata_1._sctr.value)
        data.append(self.bundle.io._rdata_1._TOSW._flag.value)
        data.append(self.bundle.io._rdata_1._TOSW._value.value)
        data.append(self.bundle.io._rdata_1._TOSR._flag.value)
        data.append(self.bundle.io._rdata_1._TOSR._value.value)
        data.append(self.bundle.io._rdata_1._NOS._flag.value)
        data.append(self.bundle.io._rdata_1._NOS._value.value)
        data.append(self.bundle.io._rdata_1._sc_disagree_0.value)
        data.append(self.bundle.io._rdata_1._sc_disagree_1.value)
        await self.bundle.step()
        return data

    #read in port 2
    @driver_method()
    async def read_2(self, raddr: int):
        self.bundle.io._ren._2.value = 1
        self.bundle.io._raddr._2.value = raddr
        await self.bundle.step()
        self.bundle.io._ren._2.value = 0
        data = list()
        data.append(self.bundle.io._rdata_2._histPtr_value.value)
        await self.bundle.step()
        return data
    
    #write in port 0
    @driver_method()
    async def write_0(self, wdata, waddr):        
        self.bundle.io._wen_0.value = 1
        self.bundle.io._waddr_0.value = waddr
        self.bundle.io._wdata_0._histPtr._flag.value = wdata[0]
        self.bundle.io._wdata_0._histPtr._value.value = wdata[1]
        self.bundle.io._wdata_0._ssp.value = wdata[2]
        self.bundle.io._wdata_0._sctr.value = wdata[3]
        self.bundle.io._wdata_0._TOSW._flag.value = wdata[4]
        self.bundle.io._wdata_0._TOSW._value.value = wdata[5]
        self.bundle.io._wdata_0._TOSR._flag.value = wdata[6]
        self.bundle.io._wdata_0._TOSR._value.value = wdata[7]
        self.bundle.io._wdata_0._NOS._flag.value = wdata[8]
        self.bundle.io._wdata_0._NOS._value.value = wdata[9]
        self.bundle.io._wdata_0._topAddr.value = wdata[10]
        self.bundle.io._wdata_0._sc_disagree_0.value = wdata[11]
        self.bundle.io._wdata_0._sc_disagree_1.value = wdata[12]
        await self.bundle.step()
        self.bundle.io._wen_0.value = 0
        await self.bundle.step()
        
