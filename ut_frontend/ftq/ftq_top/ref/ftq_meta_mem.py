from dataclasses import dataclass, field

from ut_frontend.ftq.ftq_top.env.ftq_bundle import LastStageFtbEntryBundle

# from ut_frontend.ftq.ftq_top.ref.ftb_entry_mem import FTBEntry, FTBEntryMem
@dataclass
class FtbSlot:
    offset: int    # UInt(log2Ceil(PredictWidth)) → 0~15
    sharing: int
    valid: int
    lower: int = 0
    tarStat: int = 0

@dataclass
class Full_FTBEntry:
    valid: int=0
    isCall: int=0
    isRet: int=0
    isJalr: int=0
    last_may_be_rvi_call: int=0
    carry: int=0
    pftAddr: int=0
    # brSlots_0_offset : int = 0,
    # brSlots_0_sharing : int = 0,
    # brSlots_0_valid : int = 0,
    # tailSlot_offset : int = 0,
    # tailSlot_sharing : int = 0,
    # tailSlot_valid : int = 0
    brslot: FtbSlot = field(default_factory=lambda: FtbSlot(offset=0, sharing=0, valid=0, lower=0, tarStat=0))
    tailslot: FtbSlot = field(default_factory=lambda: FtbSlot(offset=0, sharing=0, valid=0))

    @classmethod
    def from_last_stage_ftb_entry(cls, ftb: 'LastStageFtbEntryBundle'):
        """从 LastStageFtbEntryBundle 构造 FTBEntry"""
        return cls(
            isCall = ftb.isCall.value,
            isRet = ftb.isRet.value,
            isJalr = ftb.isJalr.value,
            valid = ftb.valid.value,
            last_may_be_rvi_call = ftb.last_may_be_rvi_call.value,
            carry = ftb.carry.value,
            pftAddr = ftb.pftAddr.value,
            brslot = FtbSlot(
                offset=ftb.brSlots_0_offset.value,
                sharing=ftb.brSlots_0_sharing.value,
                valid=ftb.brSlots_0_valid.value,
                lower=ftb.brSlots_0_lower.value,
                tarStat=ftb.brSlots_0_tarStat.value,
            ),
            tailslot = FtbSlot(
                offset=ftb.tailSlot_offset.value,
                sharing=ftb.tailSlot_sharing.value,
                valid=ftb.tailSlot_valid.value,
            ),
            # brSlots_0_offset = ftb.brSlots_0_offset.value,
            # brSlots_0_sharing = ftb.brSlots_0_sharing.value,
            # brSlots_0_valid = ftb.brSlots_0_valid.value,
            # tailSlot_offset = ftb.tailSlot_offset.value,
            # tailSlot_sharing = ftb.tailSlot_sharing.value,
            # tailSlot_valid = ftb.tailSlot_valid.value,
        )

@dataclass
class Ftq_1R_SRAMEntry:
    meta: int
    ftb_entry: Full_FTBEntry

    @classmethod
    def default(cls):
        return cls(meta=0, ftb_entry=Full_FTBEntry())

    @classmethod
    def from_meta_and_ftb(cls, meta: int, ftb_entry: Full_FTBEntry):
        return cls(meta=meta, ftb_entry=ftb_entry)

class FTQMeta1RSram:
    def __init__(self, size: int = 64):
        self.size = size
        self.mem = [Ftq_1R_SRAMEntry.default() for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: Ftq_1R_SRAMEntry):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, raddr: int) -> Ftq_1R_SRAMEntry:
        if 0 <= raddr < self.size:
            return self.mem[raddr]
        else:
            return Ftq_1R_SRAMEntry.default()