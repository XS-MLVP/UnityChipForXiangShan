from toffee import Agent, driver_method
from typing import List

from ..bundle.LoadQueueRAWBundle import LoadQueueRAWBundle
from ..util.dataclass import IOQuery, IORedirect, Ptr, StoreIn

class LoadQueueRAWAgent(Agent):
    def __init__(self, bundle: LoadQueueRAWBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
    
    @driver_method()
    async def Enqueue(self, query: List[IOQuery], redirect: IORedirect, stIssuePtr: Ptr, stAddrReadySqPtr: Ptr):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = query[i].valid
            query_i._req._bits._uop._preDecodeInfo._isRVC.value = query[i].uop_preDecodeInfo_isRVC
            query_i._req._bits._uop._ftqPtr._flag.value = query[i].uop_ftqPtr_flag
            query_i._req._bits._uop._ftqPtr._value.value = query[i].uop_ftqPtr_value
            query_i._req._bits._uop._ftqOffset.value = query[i].uop_ftqOffset
            query_i._req._bits._uop._robIdx._flag.value = query[i].uop_robIdx_flag
            query_i._req._bits._uop._robIdx._value.value = query[i].uop_robIdx_value
            query_i._req._bits._uop._sqIdx._flag.value = query[i].uop_sqIdx_flag
            query_i._req._bits._uop._sqIdx._value.value = query[i].uop_sqIdx_value
            query_i._req._bits._mask.value = query[i].mask
            query_i._req._bits._paddr.value = query[i].bits_paddr
            query_i._req._bits._data._valid.value = query[i].datavalid
            query_i._revoke.value = query[i].revoke
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._stIssuePtr._flag.value = stIssuePtr.flag
        self.bundle.io._stIssuePtr._value.value = stIssuePtr.value
        self.bundle.io._stAddrReadySqPtr._flag.value = stAddrReadySqPtr.flag
        self.bundle.io._stAddrReadySqPtr._value.value = stAddrReadySqPtr.value
        await self.bundle.Step()
        res = []
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            res.append(query_i._req)
        return res, self.bundle.LoadQueueRAW, self.bundle.LoadQueueRAW_
    
    @driver_method()
    async def Dequeue(self, stAddrReadySqPtr: Ptr, stIssuePtr: Ptr, redirect: IORedirect, query: List[IOQuery]):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = query[i].valid
            query_i._req._bits._uop._preDecodeInfo._isRVC.value = query[i].uop_preDecodeInfo_isRVC
            query_i._req._bits._uop._ftqPtr._flag.value = query[i].uop_ftqPtr_flag
            query_i._req._bits._uop._ftqPtr._value.value = query[i].uop_ftqPtr_value
            query_i._req._bits._uop._ftqOffset.value = query[i].uop_ftqOffset
            query_i._req._bits._uop._robIdx._flag.value = query[i].uop_robIdx_flag
            query_i._req._bits._uop._robIdx._value.value = query[i].uop_robIdx_value
            query_i._req._bits._uop._sqIdx._flag.value = query[i].uop_sqIdx_flag
            query_i._req._bits._uop._sqIdx._value.value = query[i].uop_sqIdx_value
            query_i._req._bits._mask.value = query[i].mask
            query_i._req._bits._paddr.value = query[i].bits_paddr
            query_i._req._bits._data._valid.value = query[i].datavalid
            query_i._revoke.value = query[i].revoke
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._stIssuePtr._flag.value = stIssuePtr.flag
        self.bundle.io._stIssuePtr._value.value = stIssuePtr.value
        self.bundle.io._stAddrReadySqPtr._flag.value = stAddrReadySqPtr.flag
        self.bundle.io._stAddrReadySqPtr._value.value = stAddrReadySqPtr.value
        await self.bundle.Step()
        return self.bundle.LoadQueueRAW, self.bundle.LoadQueueRAW_
    
    @driver_method()
    async def detect(self, stAddrReadySqPtr: Ptr, stIssuePtr: Ptr, redirect: IORedirect, query: List[IOQuery], storeIn: List[StoreIn]):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = query[i].valid
            query_i._req._bits._uop._preDecodeInfo._isRVC.value = query[i].uop_preDecodeInfo_isRVC
            query_i._req._bits._uop._ftqPtr._flag.value = query[i].uop_ftqPtr_flag
            query_i._req._bits._uop._ftqPtr._value.value = query[i].uop_ftqPtr_value
            query_i._req._bits._uop._ftqOffset.value = query[i].uop_ftqOffset
            query_i._req._bits._uop._robIdx._flag.value = query[i].uop_robIdx_flag
            query_i._req._bits._uop._robIdx._value.value = query[i].uop_robIdx_value
            query_i._req._bits._uop._sqIdx._flag.value = query[i].uop_sqIdx_flag
            query_i._req._bits._uop._sqIdx._value.value = query[i].uop_sqIdx_value
            query_i._req._bits._mask.value = query[i].mask
            query_i._req._bits._paddr.value = query[i].bits_paddr
            query_i._req._bits._data._valid.value = query[i].datavalid
            query_i._revoke.value = query[i].revoke
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._stIssuePtr._flag.value = stIssuePtr.flag
        self.bundle.io._stIssuePtr._value.value = stIssuePtr.value
        self.bundle.io._stAddrReadySqPtr._flag.value = stAddrReadySqPtr.flag
        self.bundle.io._stAddrReadySqPtr._value.value = stAddrReadySqPtr.value
        for i in range(2):
            storeIn_i = getattr(self.bundle.io._storeIn, f'_{i}')
            storeIn_i.valid = storeIn[i].valid
            storeIn_i._bits._uop._robIdx._flag.value = storeIn[i].robIdx_flag
            storeIn_i._bits._uop._robIdx._value.value = storeIn[i].robIdx_value
            storeIn_i._bits._paddr.value = storeIn[i].paddr
            storeIn_i._bits._mask.value = storeIn[i].mask
            storeIn_i._bits._miss.value = storeIn[i].miss
        await self.bundle.Step()
        rollback = []
        for i in range(2):
            rollback.append(getattr(self.bundle.io._rollback, f'_{i}'))
        ready = []
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            ready.append(query_i._req._ready)
        return ready, rollback, self.bundle.LoadQueueRAW, self.bundle.LoadQueueRAW_
    
    @driver_method()
    async def revoke(self, query: List[IOQuery]):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._revoke.value = query[i].revoke
        await self.bundle.Step()
        return self.bundle.LoadQueueRAW, self.bundle.LoadQueueRAW_