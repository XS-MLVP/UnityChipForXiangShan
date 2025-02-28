from toffee import Agent
from ..bundle import ICacheInterCtrlBundle

class ICacheResp():
    itlb_pbmts = [0, 0]
    exceptions = [0, 0]
    vaddrs = [0, 0]
    pmp_mmios = [False, False]
    paddr = 0
    VS_non_leaf_PTE = False
    data = 0
    backend_exception = False
    double_line = False
    gpaddr = 0
    icache_valid = True

class ICacheAgent(Agent):
    def __init__(self, bundle: ICacheInterCtrlBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def fake_resp(self, ready, icache_resp: ICacheResp):
        self.bundle._icacheInter._icacheReady.value = ready
        self.bundle._icacheInter._resp._valid.value = icache_resp.icache_valid
        self.bundle._icacheInter._resp._bits._isForVSnonLeafPTE.value = icache_resp.VS_non_leaf_PTE
        self.bundle._icacheInter._resp._bits._doubleline.value = icache_resp.double_line
        self.bundle._icacheInter._resp._bits._backendException.value = icache_resp.backend_exception
        self.bundle._icacheInter._resp._bits._gpaddr.value = icache_resp.gpaddr
        self.bundle._icacheInter._resp._bits._data.value = icache_resp.data
        
        self.bundle._icacheInter._resp._bits._paddr._0.value = icache_resp.paddr

        for i in range(2):
            getattr(self.bundle._icacheInter._resp._bits._itlb_pbmt, f"_{i}").value = icache_resp.itlb_pbmts[i]
            getattr(self.bundle._icacheInter._resp._bits._exception, f"_{i}").value = icache_resp.exceptions[i]
            getattr(self.bundle._icacheInter._resp._bits._vaddr, f"_{i}").value = icache_resp.vaddrs[i]
            getattr(self.bundle._icacheInter._resp._bits._pmp_mmio, f"_{i}").value = icache_resp.pmp_mmios[i]

        await self.bundle.step(3)

        return self.bundle._icacheStop.value