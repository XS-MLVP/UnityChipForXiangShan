from toffee import Env
from dut.ICache import DUTICache
from ..agent import ICacheAgent
from ..bundle import ICacheBundle


class ICacheEnv(Env):
    def __init__(self, dut: DUTICache):
        super().__init__()
        self.dut = dut
        self.bundle = ICacheBundle.from_prefix("").bind(dut)
        self.agent = ICacheAgent(self.bundle)
        self.bundle.set_all(0)
