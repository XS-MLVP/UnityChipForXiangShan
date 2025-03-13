from ..agent import OutsideAgent
from ..bundle import IFUTopBundle
from toffee import Env
from dut.NewIFU import DUTNewIFU

class IFUTopEnv(Env):
    def __init__(self, dut: DUTNewIFU):
        super().__init__()
        top_bundle = IFUTopBundle.from_prefix("").bind(dut)
        self.top_agent = OutsideAgent(top_bundle)