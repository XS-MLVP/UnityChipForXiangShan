from toffee import Env
from dut.WayLookup import DUTWayLookup
from ..agent import WayLookupAgent
from ..bundle import WayLookupBundle


class WayLookupEnv(Env):

    def __init__(self, dut: DUTWayLookup):
        super().__init__()
        self.dut = dut
        self.bundle = WayLookupBundle.from_prefix("").bind(dut)
        self.agent = WayLookupAgent(self.bundle)
        self.bundle.set_all(0)