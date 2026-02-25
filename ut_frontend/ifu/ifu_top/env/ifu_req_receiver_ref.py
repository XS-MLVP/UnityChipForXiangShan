
from toffee import Model, driver_hook
from ..datadef import ExistsIdx, ICacheResp, ICacheStatusResp, FTQIdx, FTQFlushFromBPUStg, \
    FTQResp, ToIbufferAllRes,FTQRedirect, FTQFlushFromBPU, NonMMIOSingleReq, NonMMIOResp, \
        MMIOCycleInfo, MMIOReq, ExceptionType, PredCheckerStage1RetData, NonMMIOReqLogger, ClusteredNonMMIOReqs
from .ifu_mmio_ref import IFUMMIOCtrler
# from .ifu_top_ctrl_ref import IFUTopCtrl
from .predecode_ref import PredecodeRef, F3PredecoderRef
from .pred_checker_ref import PredCheckerRef, TYPE_JAL
from .rvc_expander_ref import rvc_expand_ref
from .ifu_icache_receiver import IFUICacheReceiverRef

from ..commons import PREDICT_WIDTH, LAST_HALF_ERR, PRED_ERR, is_next_line, is_last_in_line, \
    calc_double_line, calc_blk_length, calc_cut_ptr, check_icache_resp_all_valid
FULL_LAST_IDX = PREDICT_WIDTH - 1

def generate_prefix_one_hots(prefix_length, length):
    prefix_length = min(max(prefix_length, 0), length)
    bits = [1] * prefix_length + [0] * (length - prefix_length)
    return bits

def bool_list_to_int(bits):
    result = 0
    for bit in reversed(bits):
        result = (result << 1) | bit
    return result


class IFUReqReceiverRef():
    def __init__(self):
        # self.ftq_double_line = False
        pass

    def cal_f1_pcs(self, start_addr):
        # self.f1_pcs = [start_addr + i * 2 for i in range(PREDICT_WIDTH)]

        return [start_addr + i * 2 for i in range(PREDICT_WIDTH)]
    
    # 无跳转时的指令距离
    def calc_ftr_ranges(self, valid, cur_start_addr, next_start_addr):
        self.start_addr = cur_start_addr
        self.next_start_addr = next_start_addr
        if valid:
            length = PREDICT_WIDTH
        else:
            length = calc_blk_length(cur_start_addr, next_start_addr)
        
        return generate_prefix_one_hots(length, PREDICT_WIDTH)
    
    def calc_jump_ranges(self, valid, ftq_offset):
        length = ftq_offset + 1 if valid else PREDICT_WIDTH
        return generate_prefix_one_hots(length, PREDICT_WIDTH)

    
    def calc_cut_ptr(self, startAddr):
        idx_pos = (startAddr >> 1) & 0x1F
        # self.cut_ptr = [idx_pos + i for i in range(PREDICT_WIDTH + 1)]
        return [idx_pos + i for i in range(PREDICT_WIDTH + 1)]
    
    def cut_from_cacheline(self, cacheline, cut_ptr):
        instrs = []
        for idx in cut_ptr:
            assert 0 <= idx < 64
            pos = idx * 16
            instrs.append((cacheline >> pos) & 0xFFFF)
        return instrs

def flush_from_bpu(flush_bpu: FTQFlushFromBPU, cur_ftq_idx: FTQIdx):
    for key in flush_bpu.stgs.keys():
        flush_info: FTQFlushFromBPUStg = flush_bpu.stgs[key]
        if not flush_info.stg_valid:
            continue
        if not (flush_info.ftqIdx > cur_ftq_idx):
            return True
    return False    

def check_last_req_half_valid(ranges, valids, rvcs, takens):
    return check_last_valid(ranges, valids, PREDICT_WIDTH-1, rvcs, takens)

        
def check_last_valid(ranges, valids, last_idx, rvcs, takens, mmio=False):
    return ranges[last_idx] and valids[last_idx] and (not rvcs[last_idx]) and (not takens[last_idx]) \
        and (not mmio)

def redirect_flush(miss_pred_idx, valids, last_idx, rvcs, pred_check_stg1_res: PredCheckerStage1RetData, mmio=False):
    miss_off = ExistsIdx()
    mis_type = 0
    ranges = pred_check_stg1_res.ranges
    takens = pred_check_stg1_res.takens

    
    exists_last_half_err = check_last_valid(ranges, valids, last_idx, rvcs, takens, mmio=mmio) and last_idx != FULL_LAST_IDX
    # print(exists_last_half_err)
    last_half_valid = check_last_valid(ranges, valids, PREDICT_WIDTH - 1, rvcs, takens, mmio)
    if exists_last_half_err:
        miss_off.exists = True
        miss_off.offsetIdx = last_idx
        mis_type = LAST_HALF_ERR
        return miss_off, mis_type

    if 0 <= miss_pred_idx < 16:
        miss_off.exists = True
        miss_off.offsetIdx = miss_pred_idx
        mis_type = PRED_ERR

    return miss_off, mis_type

AGENT_NAME="top_agent"


class IFUReceiverModel(Model):
    def __init__(self):
        super().__init__()
        self.step_funcs = []

        self.ifu_req_receiver = IFUReqReceiverRef()
        self.mmio_ctrl = IFUMMIOCtrler()
        # self.top_ctrl = IFUTopCtrl()
        self.predecode_ref = PredecodeRef()
        self.f3predecoder_ref = F3PredecoderRef()
        self.pred_checker_ref = PredCheckerRef()
        self.icache_receiver_ref = IFUICacheReceiverRef()
        self.last_half_valid = False

        # self.f2_exception = [0, 0]
        # exception_each_instr = [0 for _ in range(17)]
        self.wb_tgt = 0
        self.last_pin_flush = False
        self.ftq_idx = None    

    # MMIO在这个周期里做不了，不过可以先存下来

    def set_fs_is_off(self, fs_is_off):
        expds = self.expd_instrs_yield(fs_is_off)
        self.step_funcs.append(expds)

    def expd_instrs(self, fs_is_off, new_instrs):
        extd_instrs = []
        ills = []
        for instr in new_instrs:
            ext_instr, ill = rvc_expand_ref(instr, fsIsOff=fs_is_off)
            extd_instrs.append(instr if ill==1 else ext_instr)
            ills.append(ill)
        return extd_instrs, ills  
    
    def deal_with_non_mmio(self, req: NonMMIOSingleReq, logger: NonMMIOReqLogger):
        self.inner_deal_with_non_mmio(req)
    
    def deal_with_non_mmio_clusters(self, reqs: ClusteredNonMMIOReqs):
        res_list = []
        for req in reqs.reqs:
            res_list.append(self.inner_deal_with_non_mmio(req))
        return res_list
    
    def force_flush_non_mmio_stats(self):
        self.last_pin_flush = False
    
    def inner_deal_with_non_mmio(self, req: NonMMIOSingleReq):
        res = NonMMIOResp()

        # f0
        res.bpu_flush_res = flush_from_bpu(req.bpu_flush_info, req.ftq_req.ftqIdx)
        res.ftq_ready = req.icache_ready
        if res.bpu_flush_res or (not res.ftq_ready):
            self.last_pin_flush = False
            res.last_half_valid = self.last_half_valid
            return res
        
        # entering f1 stage

        # this will be calculated after the f0 prepare stage, where 
        start_addr_f1 = req.ftq_req.startAddr
        # print(f"start addr: {start_addr_f1}")
        f1_pcs = self.ifu_req_receiver.cal_f1_pcs(start_addr_f1)
        double_line = calc_double_line(start_addr_f1)
        cut_ptrs = calc_cut_ptr(start_addr_f1)

        
        # works at f2 stage

        next_start_addr_f2 = req.ftq_req.nextStartAddr
        offset: ExistsIdx = req.ftq_req.ftqOffset

        ftr_ranges = self.ifu_req_receiver.calc_ftr_ranges(offset.exists, start_addr_f1, next_start_addr_f2)
        jump_ranges = self.ifu_req_receiver.calc_jump_ranges(offset.exists, offset.offsetIdx)
        instr_ranges = [ftr & jmp for ftr, jmp in zip(ftr_ranges, jump_ranges)]
        
        # at f2 stage, icache resp comes
        res.cut_ptrs = cut_ptrs
        cacheline = req.final_icache_resp.data | (req.final_icache_resp.data << 512)
        res.cut_instrs = self.ifu_req_receiver.cut_from_cacheline(cacheline, res.cut_ptrs)
        res.predecode_res = self.predecode_ref.predecode(res.cut_instrs)

        res.icache_all_valid = check_icache_resp_all_valid(req.final_icache_resp.icache_valid, req.final_icache_resp.vaddrs, req.final_icache_resp.double_line, \
                                                                         double_line, req.ftq_req.startAddr, req.ftq_req.nextlineStart)
        # if not res.icache_all_valid:
        #     return res
        assert res.icache_all_valid

        # goto f3 stage:

        f2_mmio_exception = self.mmio_ctrl.calc_f2_mmio_exception(req.final_icache_resp.double_line, req.final_icache_resp.pmp_mmios, req.final_icache_resp.itlb_pbmts)

        f2_exception = self.icache_receiver_ref.gen_exceptions(req.final_icache_resp.exceptions, f2_mmio_exception)
        
        exception_each_instr, cross_page_vec = \
            self.icache_receiver_ref.gen_exceptions_each_instr(req.final_icache_resp.exceptions, \
                f2_mmio_exception, f1_pcs, res.predecode_res.rvcs, req.ftq_req.startAddr, double_line)

        res.exceptions = f2_exception
        res.exception_vecs =exception_each_instr
        res.pcs = f1_pcs
        res.addrs = (req.final_icache_resp.paddr, req.final_icache_resp.gpaddr)

        res.ranges = bool_list_to_int(instr_ranges)
        res.f3_predecode_res = self.f3predecoder_ref.f3_predecode(res.predecode_res.new_instrs)
        
        expd_instrs, ills = self.expd_instrs(req.fs_is_off, res.predecode_res.new_instrs)
        integrated_valids = res.predecode_res.half_valid_starts if self.last_half_valid else res.predecode_res.valid_starts
        
        res.pred_checker_stg1_res, pred_checker_stg2_res = self.pred_checker_ref.pred_check_stgs(res.f3_predecode_res, res.predecode_res, integrated_valids, instr_ranges, \
                                                                                                 offset, f1_pcs, req.ftq_req.nextStartAddr)

        last_half_valid = check_last_req_half_valid(res.pred_checker_stg1_res.ranges, integrated_valids, \
                                     res.predecode_res.rvcs, res.pred_checker_stg1_res.takens)
        flush_f3 = self.last_pin_flush and self.ftq_idx != req.ftq_req.ftqIdx
        self.ftq_idx = req.ftq_req.ftqIdx
        if self.last_pin_flush:
            if self.ftq_idx == req.ftq_req.ftqIdx:
                self.last_half_valid = False
            else:
                self.last_half_valid = last_half_valid and not self.last_half_valid
        else:
            self.last_half_valid = last_half_valid
        # self.last_half_valid = (last_half_valid and not self.last_half_valid) if not flush_f3 else False
        # print(f"res: last half valid: {last_half_valid}")
       
        res.to_ibuffer.toIbuffer.valid = not flush_f3
        last_valid_idx = res.pred_checker_stg1_res.fixed_length-1

        res.to_ibuffer.toIbuffer.instr_valids = bool_list_to_int(integrated_valids)

        ranges_and_valids = [a & b for (a,b ) in zip(res.pred_checker_stg1_res.ranges, integrated_valids)]

        res.to_ibuffer.toIbuffer.enqEnable = bool_list_to_int(ranges_and_valids)

        res.to_ibuffer.toIbuffer.instrs = expd_instrs
        res.to_ibuffer.toIbuffer.illegalInstrs = ills

        res.to_ibuffer.toIbuffer.pds.brTypes = res.f3_predecode_res.brTypes
        res.to_ibuffer.toIbuffer.pds.isCalls = res.f3_predecode_res.isCalls
        res.to_ibuffer.toIbuffer.pds.isRets = res.f3_predecode_res.isRets
        res.to_ibuffer.toIbuffer.pds.isRVCs = res.predecode_res.rvcs

        res.to_ibuffer.toIbuffer.ftqPtr = req.ftq_req.ftqIdx

        res.to_ibuffer.toIbuffer.foldpcs = [xorfold((pc>>1) & ((1 << 49) -1), 10, 49) for pc in f1_pcs]

        res.to_ibuffer.toIbuffer.exceptionTypes = []

        for i in range(PREDICT_WIDTH):
            cur_exception = exception_each_instr[i] 
            res.to_ibuffer.toIbuffer.exceptionTypes.append(cur_exception if cur_exception != 0 else cross_page_vec[i])

        res.to_ibuffer.toIbuffer.backendException = req.final_icache_resp.backend_exception
        res.to_ibuffer.toBackendGpaddrMem.wen = ExceptionType.GPF in f2_exception
        if res.to_ibuffer.toBackendGpaddrMem.wen:
            res.to_ibuffer.toBackendGpaddrMem.waddr = req.ftq_req.ftqIdx.value
            res.to_ibuffer.toBackendGpaddrMem.gpaddr = req.final_icache_resp.gpaddr
            
        # entering wb stage, collect res

        res.pred_checker_stg2_res = pred_checker_stg2_res
        
        res.wb_res.valid = not flush_f3

        res.wb_res.ftqIdx.flag = req.ftq_req.ftqIdx.flag
        res.wb_res.ftqIdx.value = req.ftq_req.ftqIdx.value

        res.wb_res.pcs = f1_pcs

        miss_pred_idx = -1 
        for i in range(len(res.pred_checker_stg2_res.miss_pred)):
            if res.pred_checker_stg2_res.miss_pred[i] != 0:
                miss_pred_idx = i
                break

        miss_offset, mis_type = redirect_flush(miss_pred_idx, integrated_valids, last_valid_idx, \
                                     res.predecode_res.rvcs, res.pred_checker_stg1_res, False)
        if miss_pred_idx <0:
            miss_pred_idx = len(res.pred_checker_stg2_res.miss_pred) - 1
        res.wb_res.misOffset = miss_offset if res.wb_res.valid else ExistsIdx()
        wb_tgt = f1_pcs[last_valid_idx] + 4 if mis_type == LAST_HALF_ERR else res.pred_checker_stg2_res.fixed_tgts[miss_pred_idx]
        res.wb_res.target = wb_tgt if res.wb_res.valid else f1_pcs[0] + 4
        if res.wb_res.valid:
            res.wb_res.pds.pdValids = integrated_valids
            res.wb_res.instrRanges = ranges_and_valids
        else:
            res.wb_res.instrRanges = [0 for _ in range(16)]
            res.wb_res.instrRanges[0] = 1
            res.wb_res.pds.pdValids = res.wb_res.instrRanges
        res.wb_res.pds.brTypes = res.f3_predecode_res.brTypes
        res.wb_res.pds.isCalls = res.f3_predecode_res.isCalls
        res.wb_res.pds.isRets = res.f3_predecode_res.isRets
        res.wb_res.pds.isRVCs = res.predecode_res.rvcs
        # res.wb_res.pds.pdValids = integrated_valids # if the instr is valid in the block

        first_jmp_idx = len(res.pred_checker_stg2_res.jmp_tgts) -1 

        for i in range(len(res.pred_checker_stg2_res.jmp_tgts)):
            if integrated_valids[i] and res.f3_predecode_res.brTypes[i] == TYPE_JAL:
                first_jmp_idx = i
                break

        res.wb_res.jalTarget = res.pred_checker_stg2_res.jmp_tgts[first_jmp_idx] if res.wb_res.valid else 0
        res.wb_res.cfiOffset_valid = res.pred_checker_stg1_res.taken_occurs if res.wb_res.valid else 0

        res.last_half_valid = self.last_half_valid
        # req
        
        # 如果这个stage已经是flush阶段，就不触发flush
        self.last_pin_flush = res.wb_res.misOffset.exists and not flush_f3
        res.pin_flush = self.last_pin_flush
        res.f3_flush = flush_f3
        return res
    
    # @driver_hook(agent_name=AGENT_NAME)
    def set_up_before_mmio_states(self, mmio_cycle_info: MMIOCycleInfo):
        double_line = calc_double_line(mmio_cycle_info.ftq_start_addr)
        mmio_exceptions = self.mmio_ctrl.calc_f2_mmio_exception(double_line, mmio_cycle_info.icache_pmp_mmios, \
            mmio_cycle_info.icache_itlb_pbmts)
        
        f2_exception = self.icache_receiver_ref.gen_exceptions(mmio_cycle_info.exceptions, mmio_exceptions)

        self.mmio_ctrl.setup_before_mmio_states(mmio_cycle_info, f2_exception)           
        self.mmio_ctrl.push_state(MMIOReq())   
          
    
    # @driver_hook(agent_name=AGENT_NAME)
    def deal_with_single_mmio_req(self, mmio_req:MMIOReq):
        return self.mmio_ctrl.push_state(mmio_req)
    
    @driver_hook
    def reset_mmio_state(self):
        self.mmio_ctrl.reset_all_state()
        

def xorfold(x: int, res_width: int, width: int | None = None) -> int:
    """
    把整数 x 按 res_width 分块并按位 XOR 折叠，返回 res_width 位结果。
    - x: 非负整数（对应 UInt）
    - res_width: 每块位宽，>0
    - width: x 的逻辑位宽（可选）。如果不写，就用 x.bit_length()；如需和硬件一致（保留前导0），请显式传入。
    """
    assert res_width > 0
    if width is None:
        width = max(1, x.bit_length())  # Python 对 0 的 bit_length 是 0，这里至少给 1

    k = (width + res_width - 1) // res_width  # 上取整块数
    acc = 0
    mask_block = (1 << res_width) - 1

    # 逐块提取并 XOR：第 i 块是 [i*res_width, (i+1)*res_width)
    for i in range(k):
        chunk = (x >> (i * res_width)) & mask_block
        acc ^= chunk

    # 结果自然落在 res_width 位
    return acc