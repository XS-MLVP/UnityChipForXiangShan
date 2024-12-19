__all__ = ['StatusBundle']

from toffee import Bundle, Signal, Signals

from ut_frontend.bpu.tagesc.bundle import PipelineBundle, UpdateBundle


class BaseTable(Bundle):
    oldCtrs_0, oldCtrs_1 = Signals(2)
    newCtrs_0, newCtrs_1 = Signals(2)
    io_update_takens_0, io_update_takens_1 = Signals(2)
    bt_io_w_req_valid = Signal()
    bt_io_w_req_bits_waymask = Signal()

    def old_ctr(self, way):
        return (self.oldCtrs_0, self.oldCtrs_1)[way].value

    def new_ctr(self, way):
        return (self.newCtrs_0, self.newCtrs_1)[way].value

    def update_taken(self, pc, way):
        w_idx = ((pc >> 1) & 1) ^ (way & 1)
        return (self.io_update_takens_0, self.io_update_takens_1)[w_idx].value

    def write_valid(self):
        return self.bt_io_w_req_valid.value

    def write_mask(self, pc, way):
        w_idx = ((pc >> 1) & 1) ^ (way & 1)
        return (self.bt_io_w_req_bits_waymask.value >> w_idx) & 1


class TageTableBundle(Bundle):
    io_resps_0_valid, io_resps_1_valid = Signals(2)
    io_update_mask_0, io_update_mask_1 = Signals(2)
    io_update_takens_0, io_update_takens_1 = Signals(2)
    per_bank_not_silent_update_0_0, per_bank_not_silent_update_0_1 = Signals(2)
    per_bank_not_silent_update_1_0, per_bank_not_silent_update_1_1 = Signals(2)
    per_bank_not_silent_update_2_0, per_bank_not_silent_update_2_1 = Signals(2)
    per_bank_not_silent_update_3_0, per_bank_not_silent_update_3_1 = Signals(2)

    def resp_valid(self, way: int):
        return (self.io_resps_0_valid, self.io_resps_1_valid)[way].value

    def update_mask(self, pc: int, way: int):
        w_idx = ((pc >> 1) & 1) ^ (way & 1)
        return (self.io_update_mask_0, self.io_update_mask_1)[w_idx].value

    def update_taken(self, pc: int, way: int):
        w_idx = ((pc >> 1) & 1) ^ (way & 1)
        return (self.io_update_takens_0, self.io_update_takens_1)[w_idx].value

    def not_silent(self, way):
        return tuple(getattr(self, f"per_bank_not_silent_update_{bank}_{way}").value for bank in range(4))


class TageTables(Bundle):
    tables_0 = TageTableBundle.from_prefix("tables_0_")
    tables_1 = TageTableBundle.from_prefix("tables_1_")
    tables_2 = TageTableBundle.from_prefix("tables_2_")
    tables_3 = TageTableBundle.from_prefix("tables_3_")

    def get_table(self, ti) -> TageTableBundle:
        return (self.tables_0, self.tables_1, self.tables_2, self.tables_3)[ti]

    def hit_count(self, way) -> int:
        return sum(tuple(self.get_table(t).resp_valid(way) for t in range(4)))

    def has_silent(self, ti, way) -> bool:
        not_silent_count = sum(self.get_table(ti).not_silent(way))
        return not_silent_count < 4


class ScTableBundle(Bundle):
    io_update_pc = Signal()
    io_update_mask_0, io_update_mask_1 = Signals(2)
    oldCtr, oldCtr_1 = Signals(2)
    taken, taken_1 = Signals(2)

    def update_mask(self, pc: int, way: int) -> int:
        w_idx = ((pc >> 1) & 1) ^ (way & 1)
        return (self.io_update_mask_0, self.io_update_mask_1)[w_idx].value

    def old_ctr(self, way: int):
        return (self.oldCtr, self.oldCtr_1)[way].S()

    def update_taken(self, way: int):
        return (self.taken, self.taken_1)[way].value


class ScTables(Bundle):
    scTables_0 = ScTableBundle.from_prefix("scTables_0_")
    scTables_1 = ScTableBundle.from_prefix("scTables_1_")
    scTables_2 = ScTableBundle.from_prefix("scTables_2_")
    scTables_3 = ScTableBundle.from_prefix("scTables_3_")

    def get_table(self, ti: int) -> ScTableBundle:
        return (self.scTables_0, self.scTables_1, self.scTables_2, self.scTables_3)[ti]


class InternalUpdate(Bundle):
    Valids_0, Valids_1 = Signals(2)
    ProviderCorrect, ProviderCorrect_1 = Signals(2)
    ResetU_0, ResetU_1 = Signals(2)

    def valid(self, way) -> int:
        return (self.Valids_0, self.Valids_1)[way].value

    def provider_correct(self, way) -> int:
        return (self.ProviderCorrect, self.ProviderCorrect_1)[way].value

    def reset_u(self, way) -> int:
        return (self.ResetU_0, self.ResetU_1)[way].value


class S2Status(Bundle):
    provideds_0, provideds_1 = Signals(2)
    providers_0, providers_1 = Signals(2)
    providerResps_0_ctr, providerResps_1_ctr = Signals(2)
    altUsed_0, altUsed_1 = Signals(2)
    tageTakens_dup_0_0, tageTakens_dup_0_1 = Signals(2)
    totalSums_0, totalSums_1, totalSums_0_1, totalSums_1_1 = Signals(4)

    def provided(self, way) -> int:
        return (self.provideds_0, self.provideds_1)[way].value

    def provider(self, way) -> int:
        return (self.providers_0, self.providers_1)[way].value

    def provider_weak(self, way) -> bool:
        return (self.providerResps_0_ctr, self.providerResps_1_ctr)[way].value in {0b011, 0b100}

    def alt_used(self, way) -> int:
        return (self.altUsed_0, self.altUsed_1)[way].value

    def tage_taken(self, way) -> int:
        return (self.tageTakens_dup_0_0, self.tageTakens_dup_0_1)[way].value

    def total_sum(self, way, taken) -> int:
        idx = way * 2 + taken
        return (self.totalSums_0, self.totalSums_1, self.totalSums_0_1, self.totalSums_1_1)[idx].S()


class InternalBundle(Bundle):
    needToAllocate, needToAllocate_1 = Signals(2)
    bankTickCtrs_0, bankTickCtrs_1 = Signals(2)
    scThresholds_0_thres, scThresholds_1_thres = Signals(2)
    sumAboveThreshold_totalSum, sumAboveThreshold_totalSum_1 = Signals(2)
    newThres_newCtr, newThres_newCtr_1 = Signals(2)

    s2 = S2Status.from_prefix("s2_")
    tage_table = TageTables.from_prefix("")
    base_table = BaseTable.from_prefix("bt_")
    update = InternalUpdate.from_prefix("update")
    sc = ScTables.from_prefix("")

    def need_to_allocate(self, way) -> int:
        return (self.needToAllocate, self.needToAllocate_1)[way].value

    def bank_tick_ctr(self, way) -> int:
        return (self.bankTickCtrs_0, self.bankTickCtrs_1)[way].value

    def sc_threshold(self, way) -> int:
        return (self.scThresholds_0_thres, self.scThresholds_1_thres)[way].value

    def above_threshold_total_sum(self, way):
        return (self.sumAboveThreshold_totalSum, self.sumAboveThreshold_totalSum_1)[way].value

    def new_threshold_ctr(self, way):
        return (self.newThres_newCtr, self.newThres_newCtr_1)[way].value


class StatusBundle(Bundle):
    pipline = PipelineBundle.from_prefix("io_")
    internal = InternalBundle.from_prefix("Tage_SC_")
    update = UpdateBundle.from_prefix("io_update_")

    def s2_valid(self, i):
        return self.pipline.s1_ready.value and getattr(self.pipline, f"s2_fire_{i}").value
