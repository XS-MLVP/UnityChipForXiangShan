import toffee
from toffee import Value

from dut.Tage_SC import DUTTage_SC
from ut_frontend.bpu.tagesc.agent import PredictAgent
from ut_frontend.bpu.tagesc.agent.update_agent import UpdateAgent
from ut_frontend.bpu.tagesc.bundle import BranchPredictDriver, BranchPredictMonitor, ControlBundle, BranchUpdateDriver
from ut_frontend.bpu.tagesc.bundle.internal import InternalMonitor


class TageSCEnv(toffee.Env):
    def __init__(self, dut: DUTTage_SC):
        super().__init__()
        self.dut = dut
        self.predict_driver = BranchPredictDriver.from_prefix("io_in_").bind(dut)
        self.predict_monitor = BranchPredictMonitor.from_prefix("io_out_").bind(dut)
        self.update_driver = BranchUpdateDriver.from_prefix("io_update_").bind(dut)
        self.ctrl_bundle = ControlBundle.from_prefix("io_").bind(dut)
        self.internal_monitor = InternalMonitor.from_prefix("Tage_SC_").bind(dut)

        self.predict_agent = PredictAgent(self.predict_driver, self.predict_monitor, self.ctrl_bundle)
        self.update_agent = UpdateAgent(self.update_driver)

        # initial state
        self.ctrl_bundle.set_all(0)
        self.ctrl_bundle.ctrl.tage_enable.value = 1
        self.ctrl_bundle.ctrl.sc_enable.value = 1

    async def reset_dut(self):
        self.dut.reset.value = 1
        self.dut.io_reset_vector.value = 0x80000000
        await self.dut.AStep(1)
        self.dut.reset.value = 0
        await Value(self.ctrl_bundle.s1_ready, 1)
