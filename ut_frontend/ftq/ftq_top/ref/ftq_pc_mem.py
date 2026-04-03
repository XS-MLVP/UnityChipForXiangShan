from dataclasses import dataclass
from typing import List

from ut_frontend.ftq.ftq_top.env.ftq_bundle import BranchPredictionBundle
FTQSIZE = 64
@dataclass
class Ftq_RF_Components:
    startAddr: int
    nextLineAddr: int
    fallThruError: bool

    @classmethod
    def from_branch_prediction(cls, bp: BranchPredictionBundle):
        """ Generate from BranchPredictionBundle """
        return cls(
            startAddr=bp.pc_3.value,
            nextLineAddr=bp.pc_3.value + 64,  # Cache line = 64 bytes
            fallThruError=bp.full_pred_3_fallThroughErr.value and bp.full_pred_3_hit.value,
        )

class FTQPCMem:
    def __init__(self, size: int = FTQSIZE):
        self.size = size
        self.mem = [Ftq_RF_Components(0, 64, False) for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: Ftq_RF_Components):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, ren: bool, raddr: int,):
        if ren and 0 <= raddr < self.size:
            return self.mem[raddr]