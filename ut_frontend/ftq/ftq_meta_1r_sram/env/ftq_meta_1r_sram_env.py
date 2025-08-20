from toffee import Env
from toffee.model import *
from dut.FtqMetairSram import DUTFtqMetairSram
from ..agent import FtqMeta1rSramAgent
from ..bundle import FtqMeta1rSramBundle

def set_write_mode_imm(dut: DUTFtqMetairSram):
    dut.io_raddr_0.AsImmWrite()
    dut.io_ren_0.AsImmWrite()
    dut.io_wen.AsImmWrite()
    dut.io_waddr.AsImmWrite()
    dut.io_wdata_meta.AsImmWrite()
    dut.io_wdata_ftb_entry_isCall.AsImmWrite()
    dut.io_wdata_ftb_entry_isRet.AsImmWrite()
    dut.io_wdata_ftb_entry_isJalr.AsImmWrite()
    dut.io_wdata_ftb_entry_valid.AsImmWrite()
    dut.io_wdata_ftb_entry_brSlots_0_offset.AsImmWrite()
    dut.io_wdata_ftb_entry_brSlots_0_sharing.AsImmWrite()
    dut.io_wdata_ftb_entry_brSlots_0_valid.AsImmWrite()
    dut.io_wdata_ftb_entry_brSlots_0_lower.AsImmWrite()
    dut.io_wdata_ftb_entry_brSlots_0_tarStat.AsImmWrite()
    dut.io_wdata_ftb_entry_tailSlot_offset.AsImmWrite()
    dut.io_wdata_ftb_entry_tailSlot_sharing.AsImmWrite()
    dut.io_wdata_ftb_entry_tailSlot_valid.AsImmWrite()
    dut.io_wdata_ftb_entry_tailSlot_lower.AsImmWrite()
    dut.io_wdata_ftb_entry_tailSlot_tarStat.AsImmWrite()
    dut.io_wdata_ftb_entry_pftAddr.AsImmWrite()
    dut.io_wdata_ftb_entry_carry.AsImmWrite()
    dut.io_wdata_ftb_entry_last_may_be_rvi_call.AsImmWrite()
    dut.io_wdata_ftb_entry_strong_bias_0.AsImmWrite()
    dut.io_wdata_ftb_entry_strong_bias_1.AsImmWrite()


class FtqMetairSramEnv(Env):
    def __init__(self, dut: DUTFtqMetairSram):
        super().__init__()
        self.dut = dut
        set_write_mode_imm(self.dut)
        self.bundle = FtqMeta1rSramBundle.from_prefix("").bind(dut)
        self.agent = FtqMeta1rSramAgent(self.bundle)
        self.agent = FtqMeta1rSramAgent(self.bundle)