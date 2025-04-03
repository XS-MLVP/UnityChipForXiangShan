from toffee import Env
from dut.ICacheMainPipe import DUTICacheMainPipe
from..agent import ICacheMainPipeAgent
from..bundle import ICacheMainPipeBundle

class ICacheMainPipeEnv(Env):
    def __init__(self, dut: DUTICacheMainPipe):
        super().__init__()
        self.dut = dut
        self.bundle = ICacheMainPipeBundle.from_prefix("").bind(dut)
        self.agent = ICacheMainPipeAgent(self.bundle)
        self.bundle.set_all(0)