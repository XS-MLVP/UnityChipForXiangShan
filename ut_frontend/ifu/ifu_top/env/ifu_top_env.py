from ..agent import OutsideAgent
from ..bundle import IFUTopBundle
from toffee import Env
from dut.NewIFU import DUTNewIFU
from .ifu_req_receiver_ref import IFUReceiverModel

class IFUTopEnv(Env):
    def __init__(self, dut: DUTNewIFU):
        super().__init__()
        top_bundle = IFUTopBundle.from_prefix("").bind(dut)
        self.top_agent = OutsideAgent(top_bundle)
        self.attach(IFUReceiverModel())
        