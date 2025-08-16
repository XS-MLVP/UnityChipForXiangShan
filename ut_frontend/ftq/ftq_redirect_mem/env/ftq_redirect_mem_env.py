from toffee import Env
from toffee.model import *
from dut.FtqRedirectMem import DUTFtqRedirectMem
from ..agent import FtqRedirectMemAgent
from ..bundle import FtqRedirectMemBundle
# from ..bundle import rDataPort0, rDataPort1, rDataPort2, wDataPort0

# class FtqRedirectMemModel(Model):
#     def __init__(self):
#         super().__init__()
#         self.histPtrFlag = [0] * 32
#         self.histPtrValue = [0] * 32
#         self.ssp = [0] * 32
#         self.sctr = [0] * 32   
#         self.TOSWFlag = [0] * 32
#         self.TOSWValue = [0] * 32
#         self.TOSRFlag = [0] * 32
#         self.TOSRValue = [0] * 32
#         self.NOSFlag = [0] * 32
#         self.NOSValue = [0] * 32
#         self.topAddr = [0] * 32
#         self.scDisagree0 = [0] * 32
#         self.scDisagree1 = [0] * 32
    
#     @driver_hook(agent_name="agent")
#     def read_0(self, addr):
#         data = rDataPort0()
#         data.hisPtr_flag = self.histPtrFlag[addr]
#         data.hisPtr_value = self.histPtrValue[addr]
#         data.ssp = self.ssp[addr]
#         data.sctr = self.sctr[addr]
#         data.TOSW_flag = self.TOSWFlag[addr]
#         data.TOSW_value = self.TOSWValue[addr]
#         data.TOSR_flag = self.TOSRFlag[addr]
#         data.TOSR_value = self.TOSRValue[addr]
#         data.NOS_flag = self.NOSFlag[addr]
#         data.NOS_value = self.NOSValue[addr]
#         return data

#     @driver_hook(agent_name="agent")
#     def read_1(self, addr):
#         data = rDataPort1()
#         data.hisPtr_flag = self.histPtrFlag[addr]
#         data.hisPtr_value = self.histPtrValue[addr]
#         data.ssp = self.ssp[addr]
#         data.sctr = self.sctr[addr]
#         data.TOSW_flag = self.TOSWFlag[addr]
#         data.TOSW_value = self.TOSWValue[addr]
#         data.TOSR_flag = self.TOSRFlag[addr]
#         data.TOSR_value = self.TOSRValue[addr]
#         data.NOS_flag = self.NOSFlag[addr]
#         data.NOS_value = self.NOSValue[addr]
#         data.sc_disagree0 = self.scDisagree0[addr]
#         data.sc_disagree1 = self.scDisagree1[addr]
#         return data

#     @driver_hook(agent_name="agent")
#     def read_2(self, addr):
#         data = rDataPort2()
#         data.hisPtr_value = self.histPtrValue[addr]
#         return data
    
#     @driver_hook(agent_name="agent")
#     def write_0(self, addr, data: wDataPort0):
#         self.histPtrFlag[addr] = data.hisPtr_flag
#         self.histPtrValue[addr] = data.hisPtr_value
#         self.ssp[addr] = data.ssp
#         self.sctr[addr] = data.sctr
#         self.TOSWFlag[addr] = data.TOSW_flag
#         self.TOSWValue[addr] = data.TOSW_value
#         self.TOSRFlag[addr] = data.TOSR_flag
#         self.TOSRValue[addr] = data.TOSR_value
#         self.NOSFlag[addr] = data.NOS_flag
#         self.NOSValue[addr] = data.NOS_value
#         self.topAddr[addr] = data.top_addr
#         self.scDisagree0[addr] = data.sc_disagree0
#         self.scDisagree1[addr] = data.sc_disagree1
def set_write_mode_imm(dut):
    dut.io_wen_0.AsImmWrite()
    dut.io_waddr_0.AsImmWrite()
    dut.io_wdata_0_histPtr_flag.AsImmWrite()
    dut.io_wdata_0_histPtr_value.AsImmWrite()
    dut.io_wdata_0_ssp.AsImmWrite()
    dut.io_wdata_0_sctr.AsImmWrite()
    dut.io_wdata_0_TOSW_flag.AsImmWrite()
    dut.io_wdata_0_TOSW_value.AsImmWrite()
    dut.io_wdata_0_TOSR_flag.AsImmWrite()
    dut.io_wdata_0_TOSR_value.AsImmWrite()
    dut.io_wdata_0_NOS_flag.AsImmWrite()
    dut.io_wdata_0_NOS_value.AsImmWrite()
    dut.io_wdata_0_topAddr.AsImmWrite()
    dut.io_ren_0.AsImmWrite()
    dut.io_ren_1.AsImmWrite()
    dut.io_ren_2.AsImmWrite()

class FtqRedirectMemEnv(Env):

    def __init__(self, dut:DUTFtqRedirectMem):
        super().__init__()
        self.dut = dut
        set_write_mode_imm(self.dut)
        self.bundle = FtqRedirectMemBundle.from_prefix("").bind(dut)
        self.agent = FtqRedirectMemAgent(self.bundle)
        self.bundle.set_all(0)