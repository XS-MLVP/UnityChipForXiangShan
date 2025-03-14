from toffee import Agent, driver_method
from typing import List

from ..bundle.VirtualLoadQueueBundle import VirtualLoadQueueBundle
from ..util.dataclass import IORedirect, VecCommit, EnqReq, LdIn

class VirtualLoadQueueAgent(Agent):
    def __init__(self, bundle: VirtualLoadQueueBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    async def reset(self):
        self.bundle.reset.value = 1
        await self.bundle.step()
        self.bundle.reset.value = 0
        await self.bundle.step()
        
    @driver_method
    async def update(self, enq: List[EnqReq], redirect: IORedirect):
        for i in range(6):
            enq_i = getattr(self.bundle.io._enq_req, f'_{i}')
            enq_i._valid.value = enq[i].valid
            enq_i._bits._fuType.value = enq[i].fuType
            enq_i._bits._uopIdx.value = enq[i].uopIdx
            enq_i._bits._robIdx._flag.value = enq[i].robIdx_flag
            enq_i._bits._robIdx._value.value = enq[i].robIdx_value
            enq_i._bits._lqIdx._flag.value = enq[i].lqIdx_flag
            enq_i._bits._lqIdx._value.value = enq[i].lqIdx_value
            enq_i._bits._numLsElem.value = enq[i].numLsElem
        self.bundle.io._redirect._valid.value = redirect.valid
        self.bundle.io._redirect._bits._robIdx._flag.value = redirect.robIdx_flag
        self.bundle.io._redirect._bits._robIdx._value.value = redirect.robIdx_value
        self.bundle.io._redirect._bits._level.value = redirect.level
        await self.bundle.step(1)
        for i in range(6):
            enq_i = getattr(self.bundle.io._enq_req, f'_{i}')
            enq_i._valid.value = False
        self.bundle.io._redirect._valid.value = False
        await self.bundle.step(1)
        return self.bundle.VirtualLoadQueue
    
    @driver_method
    async def commit(self, veccommit: List[VecCommit]):
        for i in range(2):
            veccommit_i = getattr(self.bundle.io._vecCommit, f'_{i}')
            veccommit_i._valid.value = veccommit[i].valid
            veccommit_i._bits._robidx._flag.value = veccommit[i].robidx_flag
            veccommit_i._bits._robidx._value.value = veccommit[i].robidx_value
            veccommit_i._bits._uopidx.value = veccommit[i].uopidx
        await self.bundle.step(1)
        for i in range(6):
            enq_i = getattr(self.bundle.io._enq_req, f'_{i}')
            enq_i._valid.value = False
        for i in range(2):
            veccommit_i = getattr(self.bundle.io._vecCommit, f'_{i}')
            veccommit_i._valid.value = False
        await self.bundle.step(1)
        return self.bundle.VirtualLoadQueue
    
    @driver_method
    async def writeback(self, ldin: List[LdIn]):
        for i in range(3):
            ldin_i = getattr(self.bundle.io._ldin, f'_{i}')
            ldin_i._valid.value = ldin[i].valid
            ldin_i._bits._uop._lqIdx._value.value = ldin[i].uop_lqIdx_value
            ldin_i._bits._isvec.value = ldin[i].isvec
            ldin_i._bits._updateAddrValid.value = ldin[i].updateAddrValid
            for j in range(11):
                getattr(ldin_i._bits._rep_info_cause, f'_{j}').value = ldin[i].rep_info_cause[j]
        await self.bundle.step(1)
        for i in range(3):
            ldin_i = getattr(self.bundle.io._ldin, f'_{i}')
            ldin_i._valid.value = False
        await self.bundle.step(1)
        return self.bundle.VirtualLoadQueue._committed