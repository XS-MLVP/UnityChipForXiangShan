from toffee import Env
from dut.VirtualLoadQueue import DUTVirtualLoadQueue
from ..bundle.VirtualLoadQueueBundle import VirtualLoadQueueBundle
from ..agent.VirtualLoadQueueAgent import VirtualLoadQueueAgent

class VirtualLoadQueueEnv(Env):

    def __init__(self, dut:DUTVirtualLoadQueue):
        super().__init__()

        bundle = VirtualLoadQueueBundle.from_prefix("").bind(dut)
        self.agent = VirtualLoadQueueAgent(bundle)