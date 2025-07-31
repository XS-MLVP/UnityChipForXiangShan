from toffee import Agent, driver_method
from typing import List

from ..bundle.LoadQueueRARBundle import LoadQueueRARBundle
from ..util.dataclass import IOQuery, IOldWbPtr, IORedirect, IORelease

class LoadQueueRARAgent(Agent):
    def __init__(self, bundle: LoadQueueRARBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()

    @driver_method()
    async def Enqueue(self, query: List[IOQuery], redirect: IORedirect, ldWbPtr: IOldWbPtr):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = query[i].req_valid
            query_i._req._bits._uop._lqIdx._flag.value = query[i].uop_lqIdx_flag
            query_i._req._bits._uop._lqIdx._value.value = query[i].uop_lqIdx_value
            query_i._req._bits._uop._robIdx._flag.value = query[i].uop_robIdx_flag
            query_i._req._bits._uop._robIdx._value.value = query[i].uop_robIdx_value
            query_i._req._bits._paddr.value = query[i].bits_paddr
            query_i._req._bits._is_nc.value = query[i].is_nc
            query_i._req._bits._data_valid.value = query[i].data_valid
            # self.resp = query.resp
            query_i._revoke.value = query[i].revoke
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._ldWbPtr._flag.value = ldWbPtr.flag
        self.bundle.io._ldWbPtr._value.value = ldWbPtr.value
        await self.bundle.step(1) # 推动电路
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = False
        self.bundle.io._redirect._valid.value = False
        await self.bundle.step(1)
        return self.bundle.LoadQueueRAR
    
    
    @driver_method()
    async def Dequeue(self, ldWbPtr: IOldWbPtr, redirect: IORedirect):
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._ldWbPtr._flag.value = ldWbPtr.flag
        self.bundle.io._ldWbPtr._value.value = ldWbPtr.value
        await self.bundle.step(1)
        self.bundle.io._redirect._valid.value = False
        await self.bundle.step(1)
        return self.bundle.LoadQueueRAR