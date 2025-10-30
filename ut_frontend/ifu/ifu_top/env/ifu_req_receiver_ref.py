
from toffee import Model, driver_hook
from ..datadef import ExistsIdx, ICacheResp, ICacheStatusResp, FTQQuery, FTQFlushInfo, \
    FTQResp, ToIbufferAllRes,FTQRedirect, FTQFlushFromBPU, NonMMIOReq, NonMMIOResp, \
        MMIOCycleInfo, MMIOReq, ExceptionType
from .ifu_mmio_ref import IFUMMIOCtrler
from .ifu_top_ctrl_ref import IFUTopCtrl, DataManagement
from .predecode_ref import PredecodeRef, F3PredecoderRef
from .pred_checker_ref import PredCheckerRef, TYPE_JAL
from .rvc_expander_ref import rvc_expand_ref
from .ifu_icache_receiver import IFUICacheReceiverRef

from ..commons import PREDICT_WIDTH, LAST_HALF_ERR, BLOCK_OFF_BITS, is_next_line, is_last_in_line, \
    calc_double_line, calc_blk_length, calc_cut_ptr

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

        return [start_addr + i * 2 for i in range(PREDICT_WIDTH)], calc_double_line(start_addr)
    
    def get_f1_pcs(self):
        return self.f1_pcs

    def set_paddr(self, paddr):
        self.f1_paddr = paddr

    def get_f1_paddr(self):
        return self.f1_paddr
    
    def set_gpaddr(self, gpaddr):
        self.f1_gpaddr = gpaddr

    def get_f1_gpaddr(self):
        return self.f1_gpaddr
    
    def set_f2_exception(self, exception: list[int], bked_excp):
        self.f2_none_mmio_exception = exception
        self.backend_exception = bked_excp
    
    # 无跳转时的指令距离
    def calc_ftr_ranges(self, valid, cur_start_addr, next_start_addr):
        self.start_addr = cur_start_addr
        self.next_start_addr = next_start_addr
        if valid:
            length = PREDICT_WIDTH
        else:
            # block_length = (next_start_addr - cur_start_addr) // 2
            length = calc_blk_length(cur_start_addr, next_start_addr)
            # length = ((next_start_addr - cur_start_addr) & 0x1F ) // 2
        
        # self.ftr_ranges = generate_prefix_one_hots(length, PREDICT_WIDTH)
        return generate_prefix_one_hots(length, PREDICT_WIDTH)
    
    def calc_jump_ranges(self, valid, ftq_offset):
        length = ftq_offset + 1 if valid else PREDICT_WIDTH
        # self.jump_ranges = generate_prefix_one_hots(length, PREDICT_WIDTH)
        return generate_prefix_one_hots(length, PREDICT_WIDTH)

    # def get_ranges(self):
    #     return [ftr & jmp for ftr, jmp in zip(self.ftr_ranges, self.jump_ranges)]
    
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
        
AGENT_NAME="top_agent"


class IFUReceiverModel(Model):
    def __init__(self):
        super().__init__()
        self.common_data = DataManagement()
        self.step_funcs = []

        self.ifu_req_receiver = IFUReqReceiverRef()
        self.mmio_ctrl = IFUMMIOCtrler()
        self.top_ctrl = IFUTopCtrl(self.common_data)
        self.predecode_ref = PredecodeRef()
        self.f3predecoder_ref = F3PredecoderRef()
        self.pred_checker_ref = PredCheckerRef()
        self.icache_receiver_ref = IFUICacheReceiverRef()
        self.last_half_valid = False

        # self.f2_exception = [0, 0]
        # exception_each_instr = [0 for _ in range(17)]
        self.wb_tgt = 0
    
    # 根据start addr和下一个块的start addr等计算信息; this function will be called at the f0 prepare stage
    def save_ftq_offset_start_addr(self):
        # this should be removed later
        # self.next_tgt = next_start_addr
        # nothing happens at f0 prepare-f0 except set ftq valid to be true
        yield False

        # self.all_together_range = [ a & b for a, b in zip(self.ifu_req_receiver.ftr_ranges, self.ifu_req_receiver.jump_ranges)]

        # this will be calculated after the f0 prepare stage, where 
        start_addr_f1 = self.common_data.ftq_req.get(1).startAddr


        f1_pcs, double_line = self.ifu_req_receiver.cal_f1_pcs(start_addr_f1)
        self.common_data.pcs.set(f1_pcs)
        self.common_data.double_line.set(double_line)
        # TODO: add cut ptr var of stages
        cut_ptr = calc_cut_ptr(start_addr_f1)
        self.common_data.cut_ptr.set(cut_ptr)
        # print(f"calc cut_ptr: {cut_ptr}")
        yield False
        
        # works at f2 stage

        next_start_addr_f2 = self.common_data.ftq_req.get(2).nextStartAddr
        offset: ExistsIdx = self.common_data.ftq_req.get(2).ftqOffset

        ftr_ranges = self.ifu_req_receiver.calc_ftr_ranges(offset.exists, start_addr_f1, next_start_addr_f2)
        jump_ranges = self.ifu_req_receiver.calc_jump_ranges(offset.exists, offset.offsetIdx)
        instr_ranges = [ftr & jmp for ftr, jmp in zip(ftr_ranges, jump_ranges)]
        
        self.common_data.instr_range.set(instr_ranges)

        yield True
    

    def icache_resp_receive(self, icache_resp: ICacheResp):
        self.common_data.from_icache_paddr.set(icache_resp.paddr)
        self.common_data.from_icache_gpaddr.set(icache_resp.gpaddr)
        self.common_data.backend_exception.set(icache_resp.backend_exception)

        # self.ifu_req_receiver.set_paddr(icache_resp.paddr)
        # self.ifu_req_receiver.set_gpaddr(icache_resp.gpaddr)
        # self.ifu_req_receiver.set_f2_exception(icache_resp.exceptions, icache_resp.backend_exception)


        self.common_data.itlb_pbmt.set(icache_resp.itlb_pbmts[0])
        self.common_data.pmp_mmio.set(icache_resp.pmp_mmios[0])


        # mmio_exception = 
        cut_instrs = self.ifu_req_receiver.cut_from_cacheline(icache_resp.data, self.common_data.cut_ptr.get(2))
        # print(self.common_data.cut_ptr.get(2))
        # print(icache_resp.data)
        # print(cut_instrs)
        self.common_data.cut_data = cut_instrs
        
        none_mmio_exception = icache_resp.exceptions

        f2_mmio_exception = self.mmio_ctrl.calc_f2_mmio_exception(icache_resp.double_line, icache_resp.pmp_mmios, icache_resp.itlb_pbmts)

        f2_exception = []
        for i in range(2):
            f2_exception.append(none_mmio_exception[i] if none_mmio_exception[i] != 0 else f2_mmio_exception[i])

        self.common_data.exceptions.set(f2_exception)
        

        # self.top_ctrl.f2_exception = self.f2_exception
        predecode_res = self.predecode_ref.predecode(self.common_data.cut_data)
        self.common_data.predecode_res.set(predecode_res)

        cross_page_vec = []
        
        exception_each_instr = []
        # 生成每条指令的异常情况
        for i in range(PREDICT_WIDTH):
            if not is_next_line(self.common_data.pcs.get(2)[i], self.common_data.ftq_req.get(2).startAddr):
                exception_each_instr.append(f2_exception[0])
            else:
                exception_each_instr.append(f2_exception[1] if self.common_data.double_line.get(2) else 0)

            enable_next = is_last_in_line(self.common_data.pcs.get(2)[i]) and not predecode_res.rvcs[i] and self.common_data.double_line.get(2) and none_mmio_exception[0] == 0 
            cross_page_vec.append(none_mmio_exception[1] if enable_next else 0)
        self.common_data.exception_each_instr.set(exception_each_instr)
        self.common_data.crosspage_exception_vec.set(cross_page_vec)


        yield False
        
        f3predecode_res = self.f3predecoder_ref.f3_predecode(self.common_data.predecode_res.get(3).new_instrs)
        self.common_data.f3predecode_res.set(f3predecode_res)

        integrated_valids = self.common_data.predecode_res.get(3).half_valid_starts if self.top_ctrl.last_half_valid else self.common_data.predecode_res.get(3).valid_starts

        self.common_data.instr_valids.set(integrated_valids)

        pred_check_stg1_res = self.pred_checker_ref.pred_check_stg1(f3predecode_res, self.common_data.predecode_res.get(3), integrated_valids, self.common_data.instr_range.get(3), \
                                                            self.common_data.ftq_req.get(3).ftqOffset , self.common_data.pcs.get(3), self.common_data.ftq_req.get(3).nextStartAddr)

        self.common_data.pred_check_stg1_res.set(pred_check_stg1_res)
        # calculate cross page exceptions

        # self.cross_page_vec = []

        self.common_data.lastvalid_idx.set(pred_check_stg1_res.fixed_length-1)
        
        # here, will later be changed to internal values from internal wires
        ranges_and_valids = [a & b for (a,b ) in zip(pred_check_stg1_res.ranges, integrated_valids)]
        self.common_data.instr_ranges_and_valids.set(ranges_and_valids)

        # prepare to ibuffer datas
        
        self.common_data.to_ibuffer.toIbuffer.valid = True

        self.common_data.to_ibuffer.toIbuffer.instr_valids = bool_list_to_int(integrated_valids)

        self.common_data.to_ibuffer.toIbuffer.enqEnable = bool_list_to_int(ranges_and_valids)

        self.common_data.to_ibuffer.toIbuffer.instrs = self.common_data.normal_expd_instrs.get(3)

        self.common_data.to_ibuffer.toIbuffer.pds.brTypes = f3predecode_res.brTypes
        self.common_data.to_ibuffer.toIbuffer.pds.isCalls = f3predecode_res.isCalls
        self.common_data.to_ibuffer.toIbuffer.pds.isRets = f3predecode_res.isRets
        self.common_data.to_ibuffer.toIbuffer.pds.isRVCs = self.common_data.predecode_res.get(3).rvcs

        self.common_data.to_ibuffer.toIbuffer.ftqPtr = self.common_data.ftq_req.get(3).ftqIdx

        self.common_data.to_ibuffer.toIbuffer.foldpcs = [xorfold((pc>>1) & ((1 << 49) -1), 10, 49) for pc in self.common_data.pcs.get(3)]

        self.common_data.to_ibuffer.toIbuffer.exceptionTypes = []

        for i in range(PREDICT_WIDTH):
            cur_exception = self.common_data.exception_each_instr.get(3)[i] 
            self.common_data.to_ibuffer.toIbuffer.exceptionTypes.append(cur_exception if cur_exception != 0 else self.common_data.crosspage_exception_vec.get(3)[i])

        self.common_data.to_ibuffer.toIbuffer.backendException = self.common_data.backend_exception.get(3)

        print("f3 finished")
        yield False

        # wb

        pred_check_stg2_res = self.pred_checker_ref.pred_check_stg2(True)
        self.common_data.pred_check_stg2_res = pred_check_stg2_res

        fired_pred_check_stg1_res = self.common_data.pred_check_stg1_res.get(4)
        miss_pred_idx = -1 
        for i in range(len(pred_check_stg2_res.miss_pred)):
            if pred_check_stg2_res.miss_pred[i] != 0:
                miss_pred_idx = i
                break
        
        wb_lastvalid_idx = self.common_data.lastvalid_idx.get(4)
        wb_instr_valids = self.common_data.instr_valids.get(4)

        wb_stg_predecode_res = self.common_data.predecode_res.get(4)
        wb_stg_f3_predecode_res = self.common_data.f3predecode_res.get(4)

        miss_offset, mis_type = self.top_ctrl.redirect_flush(miss_pred_idx, wb_instr_valids, wb_lastvalid_idx, \
                                     wb_stg_predecode_res.rvcs, fired_pred_check_stg1_res, False)

        if miss_pred_idx <0:
            miss_pred_idx = len(pred_check_stg2_res.miss_pred) - 1

        # pc + 4
        wb_tgt = self.common_data.pcs.get(4)[wb_lastvalid_idx] + 4 if mis_type == 2 else pred_check_stg2_res.fixed_tgts[miss_pred_idx]
        # print(pred_check_stg2_res.fixed_tgts[miss_pred_idx])
        # print(mis_type)
        first_jmp_idx = len(pred_check_stg2_res.jmp_tgts) -1 

        # print(pred_check_stg2_res.jmp_tgts)

        for i in range(len(pred_check_stg2_res.jmp_tgts)):
            if wb_instr_valids[i] and wb_stg_f3_predecode_res.brTypes[i] == TYPE_JAL:
                first_jmp_idx = i
                break

        jal_tgt = pred_check_stg2_res.jmp_tgts[first_jmp_idx]


        # prepare write back datas
        self.common_data.wb_ftq.valid = True

        self.common_data.wb_ftq.ftqIdx.flag = self.common_data.ftq_req.get(4).ftqIdx.flag
        self.common_data.wb_ftq.ftqIdx.value = self.common_data.ftq_req.get(4).ftqIdx.value

        self.common_data.wb_ftq.pcs = self.common_data.pcs.get(4)
        
        self.common_data.wb_ftq.misOffset = miss_offset

        self.common_data.wb_ftq.target = wb_tgt
        self.common_data.wb_ftq.instrRanges = self.common_data.instr_ranges_and_valids.get(4)

        self.common_data.wb_ftq.pds.brTypes = wb_stg_f3_predecode_res.brTypes
        self.common_data.wb_ftq.pds.isCalls = wb_stg_f3_predecode_res.isCalls
        self.common_data.wb_ftq.pds.isRets = wb_stg_f3_predecode_res.isRets
        self.common_data.wb_ftq.pds.isRVCs = wb_stg_predecode_res.rvcs
        self.common_data.wb_ftq.pds.pdValids = self.common_data.instr_valids.get(4) # if the instr is valid in the block

        self.common_data.wb_ftq.jalTarget = jal_tgt
        self.common_data.wb_ftq.cfiOffset_valid = fired_pred_check_stg1_res.taken_occurs
        yield True

    # MMIO在这个周期里做不了，不过可以先存下来

    
    def fake_resp(self, icache_status_resp: ICacheStatusResp):
        icache_work = self.icache_resp_receive(icache_status_resp.resp)
        self.step_funcs.append(icache_work)
        # self.extd_instrs = []
        # for instr in self.predecode_res.new_instrs:
        #     ext_instr, ill = rvc_expand_ref(instr, fsIsOff=fs_is_off)
        #     self.extd_instrs.append(instr if ill else ext_instr)
        
        self.top_ctrl.check_icache_resp_all_valid(icache_status_resp.resp.icache_valid, icache_status_resp.resp.vaddrs)

    
    def set_fs_is_off(self, fs_is_off):
        expds = self.expd_instrs_yield(fs_is_off)
        self.step_funcs.append(expds)

    def expd_instrs_yield(self, fs_is_off):
        self.common_data.normal_expd_instrs.set(self.expd_instrs(fs_is_off, self.common_data.predecode_res.get(3).new_instrs))
        yield True

    def expd_instrs(self, fs_is_off, new_instrs):
        extd_instrs = []
        ills = []
        for instr in new_instrs:
            ext_instr, ill = rvc_expand_ref(instr, fsIsOff=fs_is_off)
            extd_instrs.append(instr if ill==1 else ext_instr)
            ills.append(ill)
        return extd_instrs, ills

    
    def set_icache_ready(self, icache_ready):
        self.top_ctrl.set_icache_ready(icache_ready)

    
    def query_from_ftq(self, query: FTQQuery):
        # 先把ftq query保存下来
        # 这个函数已经弃用，改为保存整个ftq
        self.common_data.ftq_req.set(query)
        self.step_funcs.append(self.save_ftq_offset_start_addr())

    def bpu_flush_redirect(self, flush_from_bpu: FTQFlushFromBPU):
        self.top_ctrl.flush_from_bpu(flush_from_bpu)
        yield True
        # later will add redirect, but not now

    
    def from_ftq_flush(self, ftqFlushInfo:FTQFlushFromBPU):
        # done 
        # self.common_data.ftq_redirect.set(ftqFlushInfo.redirect if ftqFlushInfo.redirect.valid else FTQRedirect())

        self.step_funcs.append(self.bpu_flush_redirect(ftqFlushInfo))

    
    def step(self):
        print("st...")
        # 进行所有功能性的计算
        next_step_funcs = []
        while self.step_funcs:
            step_func = self.step_funcs.pop()
            # yield 函数未结束
            res = next(step_func)
            if not res:
                next_step_funcs.append(step_func)
        self.step_funcs = next_step_funcs
        
        # 根据控制结果传递值
        self.common_data.step_pass_value(self.top_ctrl.get_fires())

    # 这个用于控制信号的检验
    
    def get_ftq_ready(self):
        return self.top_ctrl.get_ftq_ready()
    
    
    def get_bpu_flush(self):
        return self.top_ctrl.get_bpu_flush()
    
    # 以下方法协助校验接取指令的正确性
    
    def get_exception_vecs(self):
        return self.common_data.exceptions.get(3), self.common_data.exception_each_instr.get(3)
    
    
    def get_f3_pcs(self):
        return self.common_data.pcs.get(3)
    
    
    def get_cut_ptrs(self):
        return self.common_data.cut_ptr.get(2)

    
    def get_addrs(self):
        return self.common_data.from_icache_paddr.get(3), self.common_data.from_icache_gpaddr.get(3)
    
    
    def get_cut_instrs(self):
        return self.common_data.cut_data
    
    
    def get_ranges(self):
        return bool_list_to_int(self.common_data.instr_range.get(3))
    
    
    def get_predecode_res(self):
        return self.common_data.predecode_res.get(2)
    
    
    def get_f3predecoder_res(self):
        return self.common_data.f3predecode_res.get(3), self.common_data.instr_valids.get(3)
    
    
    def get_pred_checker_stg1_res(self):
        return self.common_data.pred_check_stg1_res.get(3)

    
    def get_pred_checker_stg2_res(self):
        return self.common_data.pred_check_stg2_res

    
    def get_extended_instrs(self):
        return self.common_data.normal_expd_instrs.get(3)
    

    # 
    # def get_wb_flush(self):
    #     return self.top_ctrl.miss_off
    
    
    def get_cur_last_half_valid(self):
        return self.top_ctrl.last_half_valid
    
    
    def collect_res_backto_ftq(self):
        return self.common_data.wb_ftq
    
    
    def get_toibuffer_info(self)-> ToIbufferAllRes:

        return self.common_data.to_ibuffer
    
    @driver_hook(agent_name=AGENT_NAME)
    def deal_with_non_mmio(self, req: NonMMIOReq):
        res = NonMMIOResp()

        # f0
        res.bpu_flush_res = self.top_ctrl.flush_from_bpu(req.bpu_flush_info, req.ftq_req.ftqIdx)
        res.ftq_ready = req.icache_resp.ready
        if res.bpu_flush_res or (not res.ftq_ready):
            return res
        
        # entering f1 stage

        # this will be calculated after the f0 prepare stage, where 
        start_addr_f1 = req.ftq_req.startAddr

        f1_pcs, double_line = self.ifu_req_receiver.cal_f1_pcs(start_addr_f1)

        cut_ptrs = calc_cut_ptr(start_addr_f1)

        
        # works at f2 stage

        next_start_addr_f2 = req.ftq_req.nextStartAddr
        offset: ExistsIdx = req.ftq_req.ftqOffset

        ftr_ranges = self.ifu_req_receiver.calc_ftr_ranges(offset.exists, start_addr_f1, next_start_addr_f2)
        jump_ranges = self.ifu_req_receiver.calc_jump_ranges(offset.exists, offset.offsetIdx)
        instr_ranges = [ftr & jmp for ftr, jmp in zip(ftr_ranges, jump_ranges)]
        
        # at f2 stage, icache resp comes
        res.cut_ptrs = cut_ptrs
        cacheline = req.icache_resp.resp.data | (req.icache_resp.resp.data << 512)
        res.cut_instrs = self.ifu_req_receiver.cut_from_cacheline(cacheline, res.cut_ptrs)
        res.predecode_res = self.predecode_ref.predecode(res.cut_instrs)

        res.icache_all_valid = self.top_ctrl.check_icache_resp_all_valid(req.icache_resp.resp.icache_valid, req.icache_resp.resp.vaddrs, req.icache_resp.resp.double_line, \
                                                                         double_line, req.ftq_req.startAddr, req.ftq_req.nextlineStart)
        if not res.icache_all_valid:
            return res

        # goto f3 stage:

        f2_mmio_exception = self.mmio_ctrl.calc_f2_mmio_exception(req.icache_resp.resp.double_line, req.icache_resp.resp.pmp_mmios, req.icache_resp.resp.itlb_pbmts)

        f2_exception = self.icache_receiver_ref.gen_exceptions(req.icache_resp.resp.exceptions, f2_mmio_exception)
        
        exception_each_instr, cross_page_vec = \
            self.icache_receiver_ref.gen_exceptions_each_instr(req.icache_resp.resp.exceptions, \
                f2_mmio_exception, f1_pcs, res.predecode_res.rvcs, req.ftq_req.startAddr, double_line)

        res.exception_vecs = (f2_exception, exception_each_instr)
        res.pcs = f1_pcs
        res.addrs = (req.icache_resp.resp.paddr, req.icache_resp.resp.gpaddr)

        res.ranges = bool_list_to_int(instr_ranges)
        res.f3_predecode_res = self.f3predecoder_ref.f3_predecode(res.predecode_res.new_instrs)
        
        expd_instrs, ills = self.expd_instrs(req.fs_is_off, res.predecode_res.new_instrs)
        integrated_valids = res.predecode_res.half_valid_starts if self.last_half_valid else res.predecode_res.valid_starts
        
        res.pred_checker_stg1_res, pred_checker_stg2_res = self.pred_checker_ref.pred_check_stgs(res.f3_predecode_res, res.predecode_res, integrated_valids, instr_ranges, \
                                                                                                 offset, f1_pcs, req.ftq_req.nextStartAddr)

        last_valid_idx = res.pred_checker_stg1_res.fixed_length-1
        last_half_valid = self.top_ctrl.check_last_req_half_valid(res.pred_checker_stg1_res.ranges, integrated_valids, \
                                     res.predecode_res.rvcs, res.pred_checker_stg1_res.takens)
        self.last_half_valid = last_half_valid
       
        res.to_ibuffer = self.get_toibuffer_info()
        res.to_ibuffer.toIbuffer.valid = True

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

        res.to_ibuffer.toIbuffer.backendException = req.icache_resp.resp.backend_exception
        res.to_ibuffer.toBackendGpaddrMem.wen = ExceptionType.GPF in f2_exception
        if res.to_ibuffer.toBackendGpaddrMem.wen:
            res.to_ibuffer.toBackendGpaddrMem.waddr = req.ftq_req.ftqIdx.value
            res.to_ibuffer.toBackendGpaddrMem.gpaddr = req.icache_resp.resp.gpaddr
        # entering wb stage, collect res

        res.pred_checker_stg2_res = pred_checker_stg2_res
        
        res.wb_res = self.collect_res_backto_ftq()

        res.wb_res.valid = True

        res.wb_res.ftqIdx.flag = req.ftq_req.ftqIdx.flag
        res.wb_res.ftqIdx.value = req.ftq_req.ftqIdx.value

        res.wb_res.pcs = f1_pcs

        miss_pred_idx = -1 
        for i in range(len(res.pred_checker_stg2_res.miss_pred)):
            if res.pred_checker_stg2_res.miss_pred[i] != 0:
                miss_pred_idx = i
                break

        miss_offset, mis_type = self.top_ctrl.redirect_flush(miss_pred_idx, integrated_valids, last_valid_idx, \
                                     res.predecode_res.rvcs, res.pred_checker_stg1_res, False)
        if miss_pred_idx <0:
            miss_pred_idx = len(res.pred_checker_stg2_res.miss_pred) - 1
        res.wb_res.misOffset = miss_offset
        wb_tgt = f1_pcs[last_valid_idx] + 4 if mis_type == LAST_HALF_ERR else res.pred_checker_stg2_res.fixed_tgts[miss_pred_idx]
        res.wb_res.target = wb_tgt
        res.wb_res.instrRanges = ranges_and_valids

        res.wb_res.pds.brTypes = res.f3_predecode_res.brTypes
        res.wb_res.pds.isCalls = res.f3_predecode_res.isCalls
        res.wb_res.pds.isRets = res.f3_predecode_res.isRets
        res.wb_res.pds.isRVCs = res.predecode_res.rvcs
        res.wb_res.pds.pdValids = integrated_valids # if the instr is valid in the block

        first_jmp_idx = len(res.pred_checker_stg2_res.jmp_tgts) -1 

        for i in range(len(res.pred_checker_stg2_res.jmp_tgts)):
            if integrated_valids[i] and res.f3_predecode_res.brTypes[i] == TYPE_JAL:
                first_jmp_idx = i
                break

        res.wb_res.jalTarget = res.pred_checker_stg2_res.jmp_tgts[first_jmp_idx]
        res.wb_res.cfiOffset_valid = res.pred_checker_stg1_res.taken_occurs

        res.last_half_valid = last_half_valid
        return res
    
    @driver_hook(agent_name=AGENT_NAME)
    def set_up_before_mmio_states(self, mmio_cycle_info: MMIOCycleInfo):
        f1_pcs, double_line = self.ifu_req_receiver.cal_f1_pcs(mmio_cycle_info.ftq_start_addr)
        
        mmio_exceptions = self.mmio_ctrl.calc_f2_mmio_exception(double_line, mmio_cycle_info.icache_pmp_mmios, \
            mmio_cycle_info.icache_itlb_pbmts)
        
        f2_exception = self.icache_receiver_ref.gen_exceptions(mmio_cycle_info.exceptions, mmio_exceptions)

        self.mmio_ctrl.setup_before_mmio_states(mmio_cycle_info, f2_exception)           
        self.mmio_ctrl.push_state(MMIOReq())   
          
    
    @driver_hook(agent_name=AGENT_NAME)
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