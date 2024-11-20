from toffee.env import Env
from toffee.triggers import ClockCycles, Value


from dut.Tage_SC import DUTTage_SC
from ..agent import PredictAgent, TrainAgent, ControlAgent
from ..bundle import BranchPredictReq, BranchPredictionResp, UpdateBundle, CtrlBundle, PipelineBundle


class TageSCEnv(Env):
    def __init__(self, dut: DUTTage_SC):
        super().__init__()

        self.__dut__ = dut
        dut.reset.xdata.AsImmWrite()
        self.predict_agent = PredictAgent(
            BranchPredictReq.from_prefix("io_in_").bind(dut),
            BranchPredictionResp.from_prefix("io_out_").bind(dut)
        )
        self.train_agent = TrainAgent(UpdateBundle.from_prefix("io_update_").bind(dut))
        self.ctrl_agent = ControlAgent(
            CtrlBundle.from_prefix("io_ctrl_").bind(dut),
            PipelineBundle.from_prefix("io_").bind(dut),
        )

    async def reset_dut(self) -> None:
        self.__dut__.reset.xdata.value = 1
        self.__dut__.io_reset_vector.value = 0x80000000
        await ClockCycles(self.__dut__, 1)
        self.__dut__.reset.value = 0
        await Value(self.__dut__.io_s1_ready, 1)
