from toffee import Env
from toffee.model import *
from dut.FtqPcMem import DUTFtqPcMem
from ..agent import FtqPcMemAgent
from ..bundle import FtqPcMemBundle

def set_write_mode_imm(dut: DUTFtqPcMem):
    dut.io_ifuPtr_w_value.AsImmWrite()
    dut.io_ifuPtrPlus1_w_value.AsImmWrite()
    dut.io_ifuPtrPlus2_w_value.AsImmWrite()
    dut.io_pfPtr_w_value.AsImmWrite()
    dut.io_pfPtrPlus1_w_value.AsImmWrite()
    dut.io_commPtr_w_value.AsImmWrite()
    dut.io_commPtrPlus1_w_value.AsImmWrite()
    dut.io_wen.AsImmWrite()
    dut.io_waddr.AsImmWrite()
    dut.io_wdata_startAddr.AsImmWrite()
    dut.io_wdata_nextLineAddr.AsImmWrite()
    dut.io_wdata_fallThruError.AsImmWrite()

class FtqPcMemEnv(Env):
    def __init__(self, dut: DUTFtqPcMem):
        super().__init__()
        self.dut = dut
        set_write_mode_imm(self.dut)
        self.bundle = FtqPcMemBundle.from_prefix("").bind(dut)
        self.agent = FtqPcMemAgent(self.bundle)
        self.bundle.set_all(0)