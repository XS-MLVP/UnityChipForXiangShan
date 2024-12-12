from toffee import Env
from ..agent import PredCheckerAgent
from ..bundle import PredCheckerIOBundle, _13Bundle
from dut.PredChecker import DUTPredChecker


class PredCheckerEnv(Env):

    def __init__(self, dut:DUTPredChecker):
        super().__init__()
        self.predCheckerAgent = PredCheckerAgent(_13Bundle.from_prefix("").bind(dut))