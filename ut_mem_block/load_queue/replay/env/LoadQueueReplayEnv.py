from toffee import Env
from dut.LoadQueueReplay import DUTLoadQueueReplay
from ..bundle.LoadQueueReplayBundle import LoadQueueReplayBundle
from ..agent.LoadQueueReplayAgent import LoadQueueReplayAgent

class LoadQueueReplayEnv(Env):

    def __init__(self, dut:DUTLoadQueueReplay):
        super().__init__()

        bundle = LoadQueueReplayBundle.from_prefix("").bind(dut)
        self.agent = LoadQueueReplayAgent(bundle)