from toffee import Agent, driver_method
from typing import List

from ..bundle.LoadQueueRARBundle import LoadQueueRARBundle

class IORedirect:
    valid = False
    robIdx_flag = False
    # 8 bits
    robIdx_value = 0
    level = False

class IOQuery:
    req_ready = False  # output io_query_0_req_ready
    req_valid = False  # input io_query_0_req_valid
    uop_robIdx_flag = False  # input io_query_0_req_bits_uop_robIdx_flag
    uop_robIdx_value = 0  # input [7:0] io_query_0_req_bits_uop_robIdx_value
    uop_lqIdx_flag = False  # input io_query_0_req_bits_uop_lqIdx_flag
    uop_lqIdx_value = 0  # input [6:0] io_query_0_req_bits_uop_lqIdx_value
    bits_paddr = 0  # input [47:0] io_query_0_req_bits_paddr
    data_valid = False  # input io_query_0_req_bits_data_valid
    is_nc = False  # input io_query_0_req_bits_is_nc
    resp_valid = False  # output io_query_0_resp_valid
    rep_frm_fetch = False  # output io_query_0_resp_bits_rep_frm_fetch
    revoke = False  # input io_query_0_revoke
    
class IOldWbPtr:
    flag = False
    value = 0
    
class IORelease:
    valid = False  # input io_release_valid
    paddr = 0   # input [47:0] io_release_bits_paddr

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
            # self.resp = query.resp
            query_i._revoke.value = query[i].revoke
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._ldWbPtr._flag.value = ldWbPtr.flag
        self.bundle.io._ldWbPtr.value.value = ldWbPtr.value
        await self.bundle.Step() # 推动电路
        res = []
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            res.append(query_i._req)
        return res, self.bundle.LoadQueueRAR, self.bundle.LoadQueueRAR_
    
    
    @driver_method()
    async def Dequeue(self, query: List[IOQuery], ldWbPtr: IOldWbPtr, redirect: IORedirect, release: IORelease):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = query[i].req_valid
            query_i._req._bits._uop._lqIdx._flag.value = query[i].uop_lqIdx_flag
            query_i._req._bits._uop._lqIdx._value.value = query[i].uop_lqIdx_value
            query_i._req._bits._uop._robIdx._flag.value = query[i].uop_robIdx_flag
            query_i._req._bits._uop._robIdx._value.value = query[i].uop_robIdx_value
            query_i._req._bits._paddr.value = query[i].bits_paddr
            # self.resp = query.resp
            query_i._revoke.value = query[i].revoke
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        self.bundle.io._ldWbPtr._flag.value = ldWbPtr.flag
        self.bundle.io._ldWbPtr.value.value = ldWbPtr.value
        self.bundle.io._release._valid.value = release.valid
        self.bundle.io._release._bits._paddr.value = release.paddr
        await self.bundle.Step()
        return self.bundle.io._redirect, self.bundle.io._ldWbPtr, self.bundle.LoadQueueRAR, self.bundle.LoadQueueRAR_
        
    @driver_method()
    async def detect(self, query: List[IOQuery]):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._req._valid.value = query[i].req_valid
            query_i._req._bits._uop._lqIdx._flag.value = query[i].uop_lqIdx_flag
            query_i._req._bits._uop._lqIdx._value.value = query[i].uop_lqIdx_value
            query_i._req._bits._uop._robIdx._flag.value = query[i].uop_robIdx_flag
            query_i._req._bits._uop._robIdx._value.value = query[i].uop_robIdx_value
            query_i._req._bits._paddr.value = query[i].bits_paddr
            # self.resp = query.resp
            query_i._revoke.value = query[i].revoke
        await self.bundle.Step()
        return self.bundle.io._query._resp, self.bundle.LoadQueueRAR, self.bundle.LoadQueueRAR_
        
    @driver_method()
    async def releasedupdate(self, release: IORelease):
        self.bundle.io._release._valid.value = release.valid
        self.bundle.io._release._bits._paddr.value = release.paddr
        await self.bundle.Step()
        return self.bundle.LoadQueueRAR, self.bundle.LoadQueueRAR_
    
    @driver_method()
    async def revoke(self, query: List[IOQuery]):
        for i in range(3):
            query_i = getattr(self.bundle.io._query, f'_{i}')
            query_i._revoke.value = query[i].revoke
        await self.bundle.Step()
        return self.bundle.LoadQueueRAR, self.bundle.LoadQueueRAR_