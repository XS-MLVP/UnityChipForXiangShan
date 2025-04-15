#from toffee import Env
#from dut.RVCExpander import DUTRVCExpander
#from ..bundle import RVCExpanderIOBundle
#from ..agent import RVCExpanderAgent
#from toffee import *
#
#class RVCExpanderEnv(Env):
#    def __init__(self, dut:DUTRVCExpander):
#        super().__init__()
#        dut.io_in.xdata.AsImmWrite()
#        dut.io_fsIsOff.xdata.AsImmWrite()
#        self.agent = RVCExpanderAgent(RVCExpanderIOBundle.from_prefix("io").bind(dut))


from toffee import Env
from dut.InstrUncache import DUTInstrUncache
from ..bundle import InstrUncacheIOBundle
from ..agent import InstrUncacheAgent
from toffee import *


class InstrUncacheEnv(Env):
    def __init__(self, instruncache_bundle):
        super().__init__()

        #dut.io_req_valid.xdata.AsImmWrite();
        #dut.io_req_bits_addr.xdata.AsImmWrite();

        #instruncache_bundle = InstrUncacheIOBundle()
        #instruncache_bundle.bind(dut)
    

        #self.agent = InstrUncacheAgent(instruncache_bundle)

        #self.bundle = InstrUncacheIOBundle()
        #self.bundle.bind(dut)
        #self.agent = InstrUncacheAgent(self.bundle)
        self.agent = InstrUncacheAgent(instruncache_bundle)


