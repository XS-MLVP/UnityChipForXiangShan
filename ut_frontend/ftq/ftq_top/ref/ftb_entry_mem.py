from dataclasses import dataclass
from typing import List

from ut_frontend.ftq.ftq_top.env.ftq_bundle import LastStageFtbEntryBundle

PredictWidth = 16
numBrSlot = 1

@dataclass
class FTBEntry:
    isCall : int = 0
    isRet : int = 0
    isJalr : int = 0
    valid : int = 0
    brSlots_0_offset : int = 0
    brSlots_0_sharing : int = 0
    brSlots_0_valid : int = 0
    tailSlot_offset : int = 0
    tailSlot_sharing : int = 0
    tailSlot_valid : int = 0

    @classmethod
    def from_last_stage_ftb_entry(cls, ftb: 'LastStageFtbEntryBundle'):
        """ Generate FTBEntry from LastStageFtbEntryBundle """
        return cls(
            isCall = ftb.isCall.value,
            isRet = ftb.isRet.value,
            isJalr = ftb.isJalr.value,
            valid = ftb.valid.value,
            brSlots_0_offset = ftb.brSlots_0_offset.value,
            brSlots_0_sharing = ftb.brSlots_0_sharing.value,
            brSlots_0_valid = ftb.brSlots_0_valid.value,
            tailSlot_offset = ftb.tailSlot_offset.value,
            tailSlot_sharing = ftb.tailSlot_sharing.value,
            tailSlot_valid = ftb.tailSlot_valid.value,
        )

class FTBEntryMem:
    def __init__(self, size: int = 64):
        self.size = size
        self.mem = [FTBEntry() for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: FTBEntry):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, raddr: int) -> FTBEntry:
        if 0 <= raddr < self.size:
            return self.mem[raddr]
        else:
            raise IndexError("FTBEntryMem read address out of range")
