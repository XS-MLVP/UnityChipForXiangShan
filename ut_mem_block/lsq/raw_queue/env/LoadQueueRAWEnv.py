from toffee import Env
from dut.LoadQueueRAW import DUTLoadQueueRAW
from ..bundle.LoadQueueRAWBundle import LoadQueueRAWBundle
from ..agent.LoadQueueRAWAgent import LoadQueueRAWAgent

class LoadQueueRAWEnv(Env):

    def __init__(self, dut:DUTLoadQueueRAW):
        super().__init__()

        bundle = LoadQueueRAWBundle.from_prefix("").bind(dut)
        self.agent = LoadQueueRAWAgent(bundle)