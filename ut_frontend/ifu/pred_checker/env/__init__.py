from toffee import Env
from ..agent import PredCheckerAgent
from ..bundle import PredCheckerBundle
from dut.PredChecker import DUTPredChecker


class PredCheckerEnv(Env):

    def __init__(self, dut:DUTPredChecker):
        super().__init__()
        self.predCheckerAgent = PredCheckerAgent(PredCheckerBundle.from_prefix("").bind(dut))