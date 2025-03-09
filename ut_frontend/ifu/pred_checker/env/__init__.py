from toffee import Env
from ..agent import PredCheckerAgent
from ..bundle import PredCheckerBundle
from dut.PredChecker import DUTPredChecker
from .pred_checker_mdl import *


class PredCheckerEnv(Env):

    def __init__(self, dut:DUTPredChecker):
        super().__init__()
        self.predCheckerAgent = PredCheckerAgent(PredCheckerBundle.from_prefix("").bind(dut))
        self.mdl = PredCheckerModel()
        self.attach(self.mdl)
        