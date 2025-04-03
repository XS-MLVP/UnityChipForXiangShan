from toffee import Env
from dut.ICacheCtrlUnit import DUTICacheCtrlUnit
from ..agent import CtrlUnitAgent
from ..bundle import CtrlUnitBundle


class CtrlUnitEnv(Env):
    def __init__(self, dut: DUTICacheCtrlUnit):
        super().__init__()
        self.dut = dut
        self.bundle = CtrlUnitBundle.from_prefix("").bind(dut)
        self.agent = CtrlUnitAgent(self.bundle)
        self.bundle.set_all(0)
