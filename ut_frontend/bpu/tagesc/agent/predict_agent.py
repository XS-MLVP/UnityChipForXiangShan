from toffee import driver_method, monitor_method
from toffee.agent import Agent

from ..bundle import BranchPredictDriver, BranchPredictMonitor, ControlBundle
from ..env.fake_global_history import FakeGlobalHistory

__all__ = ['PredictAgent']


class PredictAgent(Agent):
    def __init__(self, driver: BranchPredictDriver, monitor: BranchPredictMonitor, control: ControlBundle):
        super().__init__(driver)

        driver.set_all(0)
        self.driver = driver
        self.monitor = monitor
        self.control = control

    @driver_method()
    async def exec_predict(self, pc: int, global_hist: int):
        # stage 0
        self.driver.assign(__create_input_dict__(pc, global_hist))
        for i in range(4):
            self.control.s0_fire_xdata(i).value = 1
        await self.driver.step()

        # stage 1
        for i in range(4):
            self.control.s0_fire_xdata(i).value = 0
        for i in range(4):
            self.control.s1_fire_xdata(i).value = 1
        await self.driver.step()
        # stage 2
        for i in range(4):
            self.control.s1_fire_xdata(i).value = 0
        for i in range(4):
            self.control.s2_fire_xdata(i).value = 1
        await self.driver.step()
        # stage 3
        for i in range(4):
            self.control.s2_fire_xdata(i).value = 0
        await self.driver.step()

    @monitor_method()
    async def get_tage_prediction(self):
        if self.control.s1_ready.value and self.control.s2_fire_1.value:
            return self.monitor.s2.br_taken_mask_0.value, self.monitor.s2.br_taken_mask_1.value

    @monitor_method()
    async def get_sc_prediction(self):
        if self.control.s1_ready.value and self.control.s2_fire_3.value:
            await self.monitor.step()
            return self.monitor.s3.br_taken_mask_0.value, self.monitor.s3.br_taken_mask_1.value

    @monitor_method()
    async def get_meta_value(self):
        if self.control.s1_ready.value and (self.control.s2_fire_1.value or self.control.s2_fire_3.value):
            await self.monitor.step()
            return self.monitor.last_stage_meta.value


def __create_input_dict__(pc: int, global_hist: int):
    d = {
        'bits_s0_pc_0': pc,
        'bits_s0_pc_1': pc,
        'bits_s0_pc_2': pc,
        'bits_s0_pc_3': pc,
        'bits_ghist': global_hist,
        'fh_tage': {
            'hist_17_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 11, 32),
            'hist_16_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 11, 119),
            'hist_15_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 7, 13),
            'hist_14_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 8, 8),
            'hist_9_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 7, 32),
            'hist_8_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 8, 119),
            'hist_7_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 7, 8),
            'hist_5_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 7, 119),
            'hist_4_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 8, 13),
            'hist_3_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 8, 32),
            'hist_1_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 11, 13)
        },
        'fh_sc': {
            'hist_12_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 4, 4),
            'hist_11_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 8, 10),
            'hist_2_folded_hist': FakeGlobalHistory.calc_fh(global_hist, 8, 16)
        }
    }
    return d
