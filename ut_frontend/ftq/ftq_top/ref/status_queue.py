from dataclasses import dataclass
from typing import List

FtqSize = 64
PredictWidth = 16

C_EMPTY = 0
C_TO_COMMIT = 1
C_COMMITTED = 2
C_FLUSHED = 3

F_SENT = 0
F_TO_SEND = 1

NOT_HIT = False
HIT = True

class UpdateTargetQueue:
    def __init__(self, size: int = FtqSize):
        self.size = size
        self.mem = [0] * size

    def write(self, wen: bool, waddr: int, target: int):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = target

    def read(self, raddr: int) -> int:
        return self.mem[raddr] if 0 <= raddr < self.size else 0

class CfiIndexVec:
    def __init__(self, size: int = FtqSize):
        self.size = size
        self.mem = [0] * size

    def write(self, wen: bool, waddr: int, cfi_offset: int):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = cfi_offset

    def read(self, raddr: int) -> int:
        return self.mem[raddr] if 0 <= raddr < self.size else 0

class MispredictVec:
    def __init__(self, size: int = FtqSize):
        self.size = size
        self.mem = [False] * size

    def write(self, wen: bool, waddr: int, is_mispredict: bool = False):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = is_mispredict

    def read(self, raddr: int) -> bool:
        return self.mem[raddr] if 0 <= raddr < self.size else False

BP_S1, BP_S2, BP_S3 = 0, 1, 2

class PredStageQueue:
    def __init__(self, size: int = FtqSize):
        self.size = size
        self.mem = [0] * size

    def write(self, wen: bool, waddr: int, stage: int):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = stage

    def read(self, raddr: int) -> int:
        return self.mem[raddr] if 0 <= raddr < self.size else 0

class CommitStateQueue:
    def __init__(self, size: int = FtqSize, width: int = PredictWidth):
        self.size = size
        self.width = width
        self.mem = [[C_EMPTY for _ in range(width)] for _ in range(size)]

    def write(self, wen: bool, waddr: int):
        """Set as C_EMPTY"""
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = [C_EMPTY] * self.width

    def read(self, raddr: int) -> List[int]:
        if 0 <= raddr < self.size:
            return self.mem[raddr][:]
        else:
            return [C_EMPTY] * self.width

    def update_single(self, addr: int, inst_idx: int, state: int):
        if 0 <= addr < self.size and 0 <= inst_idx < self.width:
            self.mem[addr][inst_idx] = state

class EntryHitStatusQueue:
    def __init__(self, size: int = FtqSize):
        self.size = size
        self.mem = [NOT_HIT] * size

    def write(self, wen: bool, waddr: int, hit: bool):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = hit

    def read(self, raddr: int) -> bool:
        return self.mem[raddr] if 0 <= raddr < self.size else NOT_HIT

class EntryFetchStatusQueue:
    def __init__(self, size: int = FtqSize):
        self.size = size
        self.mem = [F_SENT] * size

    def write(self, wen: bool, waddr: int, status: int = F_TO_SEND):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = status

    def read(self, raddr: int) -> int:
        return self.mem[raddr] if 0 <= raddr < self.size else F_SENT