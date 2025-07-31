from toffee import Env
from dut.StoreQueue import DUTStoreQueue
from ..bundle.StoreQueueBundle import StoreQueueBundle
from ..agent.StoreQueueAgent import StoreQueueAgent

class StoreQueueEnv(Env):

    def __init__(self, dut:DUTStoreQueue):
        super().__init__()

        bundle = StoreQueueBundle.from_prefix("").bind(dut)
        self.agent = StoreQueueAgent(bundle)