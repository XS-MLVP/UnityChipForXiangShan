from toffee import Env
from toffee.model import *
from dut.FtqTop import DUTFtqTop
from ..agent import FtqTopAgent
from ..bundle import FtqTopBundle

class FtqTopEnv(Env):
    def __init__(self, ftq_bundle, dut=None): 
        super().__init__()
        self.agent = FtqTopAgent(ftq_bundle)  # 设置 agent
        self.dut = dut  # 存储 dut 作为实例属性
        self.bundle = FtqTopBundle.from_prefix("").bind(dut)
        self.bundle.set_all(0)