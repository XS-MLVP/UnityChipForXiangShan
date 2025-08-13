from toffee import Env
from dut.FtqRedirectMem import DUTFtqRedirectMem
from ..agent import FtqRedirectMemAgent
from ..bundle import FtqRedirectMemBundle

class FtqRedirectMemEnv(Env):

    def __init__(self, dut:DUTFtqRedirectMem):
        super().__init__()
        
        bundle = FtqRedirectMemBundle.from_prefix("").bind(dut)
        self.agent = FtqRedirectMemAgent(bundle)