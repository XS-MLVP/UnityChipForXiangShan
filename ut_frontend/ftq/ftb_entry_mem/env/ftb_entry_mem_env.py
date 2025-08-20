from toffee import Env
from toffee.model import *
from dut.FtbEntryMem import DUTFtbEntryMem
from ..agent import FtbEntryMemAgent
from ..bundle import FtbEntryMemBundle

def set_write_mode_imm(dut: DUTFtbEntryMem):
    dut.io_ren_0.AsImmWrite()
    dut.io_ren_1.AsImmWrite()
    dut.io_raddr_0.AsImmWrite()
    dut.io_raddr_1.AsImmWrite()
    dut.io_wen_0.AsImmWrite()
    dut.io_waddr_0.AsImmWrite()
    dut.io_wdata_0_isCall.AsImmWrite()
    dut.io_wdata_0_isRet.AsImmWrite()
    dut.io_wdata_0_isJalr.AsImmWrite()
    dut.io_wdata_0_brSlots_0_offset.AsImmWrite()
    dut.io_wdata_0_brSlots_0_valid.AsImmWrite()
    dut.io_wdata_0_tailSlot_offset.AsImmWrite()
    dut.io_wdata_0_tailSlot_sharing.AsImmWrite()
    dut.io_wdata_0_tailSlot_valid.AsImmWrite()

class FtbEntryMemEnv(Env):
    def __init__(self, dut: DUTFtbEntryMem):
        super().__init__()
        self.dut = dut
        set_write_mode_imm(self.dut)
        self.bundle = FtbEntryMemBundle.from_prefix("").bind(dut)
        self.agent = FtbEntryMemAgent(self.bundle)
        self.bundle.set_all(0)  