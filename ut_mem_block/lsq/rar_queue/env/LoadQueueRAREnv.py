from toffee import Env
from dut.LoadQueueRAR import DUTLoadQueueRAR
from ..bundle.LoadQueueRARBundle import LoadQueueRARBundle
from ..agent.LoadQueueRARAgent import LoadQueueRARAgent

class LoadQueueRAREnv(Env):

    def __init__(self, dut:DUTLoadQueueRAR):
        super().__init__()

        bundle = LoadQueueRARBundle.from_prefix("").bind(dut)
        self.agent = LoadQueueRARAgent(bundle)
        