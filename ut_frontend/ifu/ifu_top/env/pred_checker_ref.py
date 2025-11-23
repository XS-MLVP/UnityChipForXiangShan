from ..datadef import F3PreDecodeData, PredCheckerRetData, ExistsIdx, PreDecodeDataDef, PredCheckerStage2RetData, PredCheckerStage1RetData
from typing import Generator
from ..commons import PREDICT_WIDTH

TYPE_JAL=2
TYPE_JALR=3
TYPE_BR = 1
TYPE_NONE = 0


NO_FAULT=0
JAL_FAULT=1
RET_FAULT=2
TGT_FAULT=3
NON_CFI_FAULT=4
INVALID_TAKEN_FAULT=5
JALR_FAULT=6


def get_first_true(bool_list: list[bool]):
    if True not in bool_list:
        return len(bool_list)
    return bool_list.index(True)


class PredCheckerRef():
    def __init__(self):
        self.generator_queue: list[Generator] = []
    
    def pred_check_stg1(self, f3_pd: F3PreDecodeData, pd: PreDecodeDataDef, instr_valids, instr_ranges, jmp_idx_all: ExistsIdx, pcs, tgt) -> PredCheckerStage1RetData:
        generator = self.pred_check_yield(f3_pd, pd, instr_valids, instr_ranges, jmp_idx_all, pcs, tgt)
        res = next(generator)
        self.generator_queue.append(generator)
        return res

    def pred_check_stg2(self, fire) -> PredCheckerStage2RetData:
        res = PredCheckerStage2RetData()
        if self.generator_queue:
            new_gen = self.generator_queue.pop()
            res = new_gen.send(fire)
        return res


    def pred_check_yield(self, f3_pd: F3PreDecodeData, pd: PreDecodeDataDef, instr_valids, instr_ranges, jmp_idx_all: ExistsIdx, pcs, tgt):
        jal_errs = [False] * 16
        jalr_errs = [False] * 16
        ret_errs = [False] * 16
        tgt_errs = [False] * 16
        non_cfi_errs = [False] * 16
        invalid_errs = [False] * 16

        decode_jmp_offs = pd.jmp_offsets
        rvcs = pd.rvcs
        whether_jmp = jmp_idx_all.exists
        jmp_idx = jmp_idx_all.offsetIdx
        # res = PredCheckerRetData()

        res1 = PredCheckerStage1RetData()
        jal_idxs = self.check_num_errs(f3_pd.brTypes, TYPE_JAL)
        jal_errs = self.jmp_type_err_check(jal_idxs, whether_jmp, jmp_idx, instr_ranges, instr_valids)

        jalr_init_idxs = self.check_num_errs(f3_pd.brTypes, TYPE_JALR)
        ret_idxs = self.check_num_errs(f3_pd.isRets, 1)
        jalr_idxs = [jalr and not ret for jalr, ret in zip(jalr_init_idxs, ret_idxs)]
        
        jalr_errs = self.jmp_type_err_check(jalr_idxs, whether_jmp, jmp_idx, instr_ranges, instr_valids)
        ret_errs = self.jmp_type_err_check(ret_idxs, whether_jmp, jmp_idx, instr_ranges, instr_valids)
        
        true_jmp_stg = min(get_first_true(jal_errs), get_first_true(jalr_errs), get_first_true(ret_errs))
        if true_jmp_stg >= jmp_idx:
            res1.ranges = instr_ranges[:]
            retake = jmp_idx
        else:
            res1.ranges = [True] * true_jmp_stg + [False] * (len(instr_ranges) - true_jmp_stg)
            retake = true_jmp_stg

        res1.fixed_length = 16 if 0 not in res1.ranges else res1.ranges.index(0)
        # above done the stage 1 work: jal/jalr/ret errs and fix range & taken idx

        res1.takens = [res1.ranges[i] and instr_valids[i] and  \
                      ( f3_pd.brTypes[i] == TYPE_JAL or f3_pd.brTypes[i] == TYPE_JALR or f3_pd.isRets[i] \
                       or (whether_jmp and f3_pd.brTypes[i] != TYPE_NONE and i == retake)) \
                      for i in range(len(instr_ranges))]

        res1.taken_occurs = (1 in res1.takens)
        

        next_fire = yield res1

        res2 = PredCheckerStage2RetData()
        
        if next_fire:
            if whether_jmp:
                jmp_off_range = res1.ranges[jmp_idx]
                instr_valid_off = instr_valids[jmp_idx]
                non_cfi_errs[jmp_idx] = jmp_off_range and instr_valid_off and f3_pd.brTypes[jmp_idx] == TYPE_NONE
                invalid_errs[jmp_idx] = jmp_off_range and not instr_valid_off
                jmp_tgt_predecode = decode_jmp_offs[jmp_idx] + pcs[jmp_idx]
                tgt_errs[jmp_idx] = jmp_off_range and instr_valid_off and (f3_pd.brTypes[jmp_idx] == TYPE_JAL or f3_pd.brTypes[jmp_idx] == TYPE_BR) and jmp_tgt_predecode != tgt
            
            # self.fault_type = []
            # self.fixed_tgt = []

            for i in range(len(jal_errs)):
                res2.faults[i] = (JAL_FAULT if jal_errs[i] else \
                                    JALR_FAULT if jalr_errs[i] else \
                                    RET_FAULT if ret_errs[i] else \
                                    TGT_FAULT if tgt_errs[i] else \
                                    NON_CFI_FAULT if non_cfi_errs[i] else \
                                    INVALID_TAKEN_FAULT if invalid_errs[i] else \
                                    NO_FAULT
                                    )
                res2.miss_pred[i] = (res2.faults[i] != NO_FAULT)
                cur_jmp_tgt = (pcs[i] + decode_jmp_offs[i]) & (1 << 64) -1
                res2.jmp_tgts[i] = cur_jmp_tgt
                if jal_errs[i] or tgt_errs[i]:
                    res2.fixed_tgts[i] = cur_jmp_tgt
                else:
                    seq_tgt = pcs[i] + (2 if rvcs[i] or not instr_valids[i] else 4)
                    res2.fixed_tgts[i] = seq_tgt
                res2.fixed_tgts[i] &= (1 << 64) -1
        
        yield res2


    def pred_check_stgs(self, f3_pd: F3PreDecodeData, pd: PreDecodeDataDef, instr_valids, instr_ranges, jmp_idx_all: ExistsIdx, pcs, tgt):
        jal_errs = [False] * 16
        jalr_errs = [False] * 16
        ret_errs = [False] * 16
        tgt_errs = [False] * 16
        non_cfi_errs = [False] * 16
        invalid_errs = [False] * 16

        decode_jmp_offs = pd.jmp_offsets
        rvcs = pd.rvcs
        whether_jmp = jmp_idx_all.exists
        jmp_idx = jmp_idx_all.offsetIdx if whether_jmp else PREDICT_WIDTH
        # res = PredCheckerRetData()

        res1 = PredCheckerStage1RetData()
        jal_idxs = self.check_num_errs(f3_pd.brTypes, TYPE_JAL)
        jal_errs = self.jmp_type_err_check(jal_idxs, whether_jmp, jmp_idx, instr_ranges, instr_valids)

        jalr_init_idxs = self.check_num_errs(f3_pd.brTypes, TYPE_JALR)
        ret_idxs = self.check_num_errs(f3_pd.isRets, 1)
        jalr_idxs = [jalr and not ret for jalr, ret in zip(jalr_init_idxs, ret_idxs)]
        
        jalr_errs = self.jmp_type_err_check(jalr_idxs, whether_jmp, jmp_idx, instr_ranges, instr_valids)
        # print(f"jalr_errs: {jalr_errs}")
        ret_errs = self.jmp_type_err_check(ret_idxs, whether_jmp, jmp_idx, instr_ranges, instr_valids)
        
        true_jmp_stg = min(get_first_true(jal_errs), get_first_true(jalr_errs), get_first_true(ret_errs))
        # print(f"valid: {whether_jmp}; jmp_idx: {jmp_idx}, true_jmp_stg: {true_jmp_stg}")
        
        if true_jmp_stg >= jmp_idx:
            res1.ranges = instr_ranges[:]
            retake = jmp_idx
        else:
            true_jmp_stg += 1
            res1.ranges = [True] * true_jmp_stg + [False] * (len(instr_ranges) - true_jmp_stg)
            retake = true_jmp_stg
        # print(f"res1_ranges: {res1.ranges}")
        res1.fixed_length = 16 if 0 not in res1.ranges else res1.ranges.index(0)
        # above done the stage 1 work: jal/jalr/ret errs and fix range & taken idx

        res1.takens = [res1.ranges[i] and instr_valids[i] and  \
                      ( f3_pd.brTypes[i] == TYPE_JAL or f3_pd.brTypes[i] == TYPE_JALR or f3_pd.isRets[i] \
                       or (whether_jmp and (f3_pd.brTypes[i] != TYPE_NONE) and (i == retake))) \
                      for i in range(len(res1.ranges))]

        res1.taken_occurs = (1 in res1.takens)
        


        res2 = PredCheckerStage2RetData()
        
        if whether_jmp:
            jmp_off_range = res1.ranges[jmp_idx]
            instr_valid_off = instr_valids[jmp_idx]
            non_cfi_errs[jmp_idx] = jmp_off_range and instr_valid_off and f3_pd.brTypes[jmp_idx] == TYPE_NONE
            invalid_errs[jmp_idx] = jmp_off_range and not instr_valid_off
            jmp_tgt_predecode = decode_jmp_offs[jmp_idx] + pcs[jmp_idx]
            tgt_errs[jmp_idx] = jmp_off_range and instr_valid_off and (f3_pd.brTypes[jmp_idx] == TYPE_JAL or f3_pd.brTypes[jmp_idx] == TYPE_BR) and jmp_tgt_predecode != tgt
        
        # self.fault_type = []
        # self.fixed_tgt = []

        for i in range(len(jal_errs)):
            res2.faults[i] = (JAL_FAULT if jal_errs[i] else \
                                JALR_FAULT if jalr_errs[i] else \
                                RET_FAULT if ret_errs[i] else \
                                TGT_FAULT if tgt_errs[i] else \
                                NON_CFI_FAULT if non_cfi_errs[i] else \
                                INVALID_TAKEN_FAULT if invalid_errs[i] else \
                                NO_FAULT
                                )
            res2.miss_pred[i] = (res2.faults[i] != NO_FAULT)
            cur_jmp_tgt = (pcs[i] + decode_jmp_offs[i]) & ((1 << 64) -1)
            res2.jmp_tgts[i] = cur_jmp_tgt
            if jal_errs[i] or tgt_errs[i]:
                res2.fixed_tgts[i] = cur_jmp_tgt
            else:
                seq_tgt = pcs[i] + (2 if (rvcs[i] or not instr_valids[i]) else 4)
                res2.fixed_tgts[i] = seq_tgt
            res2.fixed_tgts[i] &= (1 << 64) -1
        
        return res1, res2
        

    # async def agent_pred_check(self, ftqValid, ftqOffBits, instrRange, instrValid, jumpOffset, pc, pds, tgt, fire):

    # returning: whether fault exists and the true position; -1 means no
    def check_num_errs(self, num_list:list[int], tgt_val):
        return [tgt_val == x for x in num_list]
    
    def jmp_type_err_check(self, idxs, whether_jmp, jmp_instr_offset, ranges, valids):
        return [ranges[i] and valids[i] and idxs[i] and ((not whether_jmp) or ((i < jmp_instr_offset) and whether_jmp)) for i in range(len(idxs))]
    

    # def check_empty

        