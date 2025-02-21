from toffee import Env
from dut.LoadQueueUncache import DUTLoadQueueUncache
from ..bundle.LoadQueueUncacheBundle import LoadQueueUncacheBundle
from ..agent.LoadQueueUncacheAgent import LoadQueueUncacheAgent

class LoadQueueUncacheEnv(Env):

    def __init__(self, dut:DUTLoadQueueUncache):
        super().__init__()

        bundle = LoadQueueUncacheBundle.from_prefix("").bind(dut)
        self.agent = LoadQueueUncacheAgent(bundle)