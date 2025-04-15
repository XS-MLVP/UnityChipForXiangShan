from toffee import Env
from ..bundle import InstrUncacheIOBundle
from ..agent import InstrUncacheAgent
from toffee import *


class InstrUncacheEnv(Env):
    def __init__(self, instruncache_bundle):
        super().__init__()

        self.agent = InstrUncacheAgent(instruncache_bundle)


