from toffee import Env
from dut.FrontendTrigger import DUTFrontendTrigger
from ..bundle import FrontendTriggerBundle
from ..agent import FrontendTriggerAgent

class FrontendTriggerEnv(Env):

    def __init__(self, dut:DUTFrontendTrigger):
        super().__init__()

        bundle = FrontendTriggerBundle.from_prefix("").bind(dut)
        self.agent = FrontendTriggerAgent(bundle)
        # self.agent.reset()