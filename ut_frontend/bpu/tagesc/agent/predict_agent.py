from toffee.agent import Agent

from ..bundle import BranchPredictReq, BranchPredictionResp
from ..env.fake_global_history import TageSCFakeGlobalHistory

__all__ = ['PredictAgent']


class PredictAgent(Agent):
    def __init__(self, in_bundle: BranchPredictReq, out_bundle: BranchPredictionResp):
        super().__init__(in_bundle.step)
        in_bundle.set_all(0)
        out_bundle.set_write_mode_as_imme()
        self.io_in = in_bundle
        self.io_out = out_bundle

    async def exec_predict(self, pc: int, global_hist: int) -> None:
        self.io_in.assign(__gen_input_dict__(pc, global_hist))
        await self.io_in.step(4)


def __gen_input_dict__(pc: int, global_hist: int):
    return {
        'bits_s0_pc_0': pc,
        'bits_s0_pc_1': pc,
        'bits_s0_pc_2': pc,
        'bits_s0_pc_3': pc,
        'fh_tage': {
            'hist_17_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 11, 32),
            'hist_16_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 11, 119),
            'hist_15_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 7, 13),
            'hist_14_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 8, 8),
            'hist_9_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 7, 32),
            'hist_8_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 8, 119),
            'hist_7_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 7, 8),
            'hist_5_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 7, 119),
            'hist_4_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 8, 13),
            'hist_3_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 8, 32),
            'hist_1_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 11, 13)
        },
        'fh_sc': {
            'hist_12_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 4, 4),
            'hist_11_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 8, 10),
            'hist_2_folded_hist': TageSCFakeGlobalHistory.calc_fh(global_hist, 8, 16)
        }
    }
