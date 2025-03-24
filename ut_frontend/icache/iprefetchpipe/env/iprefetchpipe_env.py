from toffee import Env
from dut.IPrefetchPipe import DUTIPrefetchPipe
from ..agent import IPrefetchPipeAgent
from ..bundle import IPrefetchPipeBundle


class IPrefetchPipeEnv(Env):
    def __init__(self, dut: DUTIPrefetchPipe):
        super().__init__()
        self.dut = dut
        self.bundle = IPrefetchPipeBundle.from_prefix("").bind(dut)
        self.agent = IPrefetchPipeAgent(self.bundle)
        self.bundle.set_all(0)
