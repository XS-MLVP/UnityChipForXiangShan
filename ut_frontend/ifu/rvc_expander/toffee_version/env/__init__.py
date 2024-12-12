from toffee import Env
from dut.RVCExpander import DUTRVCExpander
from ..bundle import RVCExpanderIOBundle
from ..agent import RVCExpanderAgent
from toffee import *

class RVCExpanderEnv(Env):
    def __init__(self, dut:DUTRVCExpander):
        super().__init__()
        dut.io_in.xdata.AsImmWrite()
        dut.io_fsIsOff.xdata.AsImmWrite()
        # start_clock(dut)
        self.agent = RVCExpanderAgent(RVCExpanderIOBundle.from_prefix("io").bind(dut))
        