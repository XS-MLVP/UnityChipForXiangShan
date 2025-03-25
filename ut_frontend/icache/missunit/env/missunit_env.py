from toffee import Env
from dut.ICacheMissUnit import DUTICacheMissUnit
from ..agent import ICacheMissUnitAgent
from ..bundle import ICacheMissUnitBundle


class ICacheMissUnitEnv(Env):
    def __init__(self, dut: DUTICacheMissUnit):
        super().__init__()
        self.dut = dut
        self.bundle = ICacheMissUnitBundle.from_prefix("").bind(dut)
        self.agent = ICacheMissUnitAgent(self.bundle)
        self.bundle.set_all(0)
