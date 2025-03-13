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


class ICacheStatusResp():
    ready = True
    resp = ICacheResp()
