from toffee import Env
from ..agent import itlb_agent
from ..bundle import TlbBundle
from dut.TLB import DUTTLB
from .itlb_mdl import *

class ItlbEnv(Env):
    def __init__(self, dut:DUTTLB):
        super().__init__()
        self.itlbAgent = itlb_agent.ItlbAgent(TlbBundle.from_prefix("").bind(dut))
        
