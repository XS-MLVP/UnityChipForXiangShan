from toffee import Env
from toffee.model import *
from dut.FtqPdMem import DUTFtqPdMem
from ..agent import FtqPdMemAgent
from ..bundle import FtqPdMemBundle

def set_write_mode_imm(dut: DUTFtqPdMem):
    dut.io_ren_0.AsImmWrite()
    dut.io_ren_1.AsImmWrite()
    dut.io_raddr_0.AsImmWrite()
    dut.io_raddr_1.AsImmWrite()
    dut.io_wen_0.AsImmWrite()
    dut.io_waddr_0.AsImmWrite()
    for i in range(16):
        getattr(dut, f"io_wdata_0_brMask_{i}").AsImmWrite()
        getattr(dut, f"io_wdata_0_rvcMask_{i}").AsImmWrite()
    for i in range(3):
        getattr(dut, f"io_wdata_0_jmpInfo_bits_{i}").AsImmWrite()
    dut.io_wdata_0_jmpInfo_valid.AsImmWrite()
    dut.io_wdata_0_jmpOffset.AsImmWrite()
    dut.io_wdata_0_jalTarget.AsImmWrite()

class FtqPdMemEnv(Env):
    def __init__(self, dut: DUTFtqPdMem):
        super().__init__()
        self.dut = dut
        set_write_mode_imm(self.dut)
        self.bundle = FtqPdMemBundle.from_prefix("").bind(dut)
        self.agent = FtqPdMemAgent(self.bundle)
        self.bundle.set_all(0)