from toffee import Model, driver_hook, monitor_hook
from ..datadef import FTQFlushFromBPU, FTQFlushFromBPUStg, FTQIdx, ExistsIdx, FTQRedirect, FTQQuery, PreDecodeDataDef, \
    F3PreDecodeData, ToIbufferAllRes, PredCheckerStage1RetData, PredCheckerStage2RetData, FTQResp, ICacheResp
from enum import Enum

from .tools import FakeReg, StagesWire, StagesWireManager
from ..commons import PREDICT_WIDTH, PRED_ERR, LAST_HALF_ERR
AGENT_NAME="top_agent"
FULL_LAST_IDX = PREDICT_WIDTH - 1


class MMIOState(Enum):
    STATE_IDLE = 0
    STATE_WAIT_LAST_CMT = 1
    STATE_SEND_REQ = 2
    STATE_WAIT_RESP = 3
    STATE_SEND_TLB = 4
    STATE_TLB_RESP = 5
    STATE_SEND_PMP = 6
    STATE_RESEND_REQ = 7
    STATE_WAIT_RESEND_RESP = 8
    STATE_WAIT_COMMIT = 9
    STATE_COMMITED = 10

class PbmtAssist():
    NC = 1
    IO = 2

    def is_uncache(self, num):
        return num == self.NC or num == self.IO

class DataManagement():
    def __init__(self):
        self.stage_wire_manager = StagesWireManager()
        self.ftq_req: StagesWire[FTQQuery] = self.stage_wire_manager.create(init_val=FTQQuery())
        self.pcs: StagesWire[list[int]] = self.stage_wire_manager.create(init_val=[0] * PREDICT_WIDTH, start=1)
        self.double_line: StagesWire[int] = self.stage_wire_manager.create(start=1, end=3, init_val=False)
        self.cut_ptr: StagesWire[list[int]] = self.stage_wire_manager.create(start=1, end=2, init_val=[0] * (PREDICT_WIDTH+1))
        self.instr_range: StagesWire[list[int]] = self.stage_wire_manager.create(start=2, end=3, init_val=[0] * PREDICT_WIDTH)
        self.from_icache_paddr: StagesWire[int] = self.stage_wire_manager.create(start=2, end=3, init_val=0)
        self.from_icache_gpaddr: StagesWire[int] = self.stage_wire_manager.create(start=2, end=3, init_val=0)
        self.exceptions: StagesWire[list[int]] = self.stage_wire_manager.create(start=2, end=3, init_val=[0, 0])
        self.backend_exception: StagesWire[bool] = self.stage_wire_manager.create(start=2, end=3, init_val=False)
        self.pmp_mmio: StagesWire[bool] = self.stage_wire_manager.create(start=2, end=3, init_val=False)
        self.itlb_pbmt: StagesWire[bool] = self.stage_wire_manager.create(start=2, end=3, init_val=False)
        self.exception_each_instr: StagesWire[list[int]] = self.stage_wire_manager.create(start=2, end=3, init_val=[0] * 16)
        self.predecode_res: StagesWire[PreDecodeDataDef] = self.stage_wire_manager.create(start=2, end=4, init_val=PreDecodeDataDef())
        self.f3predecode_res: StagesWire[F3PreDecodeData] = self.stage_wire_manager.create(start=3, end=4, init_val=F3PreDecodeData())
        self.crosspage_exception_vec: StagesWire[list[int]] = self.stage_wire_manager.create(start=2, end=3, init_val=[0] * 16)
        self.lastvalid_idx: StagesWire[int] = self.stage_wire_manager.create(start=3, end=4, init_val=16)
        self.instr_valids: StagesWire[list[bool]] = self.stage_wire_manager.create(start=3, end=4, init_val=[False] * 16)
        self.pred_check_stg1_res: StagesWire[PredCheckerStage1RetData] = self.stage_wire_manager.create(start=3, end=4, init_val=PredCheckerStage1RetData())
        self.normal_expd_instrs: StagesWire[list[int]] = self.stage_wire_manager.create(start=3, end=4, init_val=[0] * 16)
        self.instr_ranges_and_valids : StagesWire[list[int]] = self.stage_wire_manager.create(start=3, end=4, init_val=[0] * 16)

        self.ftq_redirect: FakeReg[FTQRedirect] = FakeReg(FTQRedirect())
        self.cut_data: list[int] = [0] * (PREDICT_WIDTH + 1)

        # self.ftq_bpu_flush_info = FTQFlushFromBPU()

        self.to_ibuffer = ToIbufferAllRes()
        self.wb_ftq = FTQResp()

        self.pred_check_stg2_res: PredCheckerStage2RetData = PredCheckerStage2RetData()

        # self.from_icache: ICacheResp = ICacheResp()


    def step_pass_value(self, fires):
        self.stage_wire_manager.fresh_all(fires)
        
        

class IFUTopCtrl():
    
    def __init__(self, reuseable_data: DataManagement):
        self.common_data = reuseable_data

        self.f2_exception = [0, 0]

        self.f1_ready = True
        self.f2_ready = True
        self.icache_ready = True
        self.icache_resp_valid = True
        self.f0_fire = True
        self.f1_fire = True
        self.f2_fire = True
        self.wb_enable = True
        self.to_ibuffer_ready = True
        self.from_uncache_valid = True

        self.f0_flush = False
        self.bpu_f0_flush = False
        # self.cur_ftq_idx = None
        self.last_half_valid = False
        self.f3_mmio_use_seq_pc = False

        # self.miss_off = ExistsIdx()
        # self.mis_type = 0

        self.mmio_state = MMIOState.STATE_IDLE

        self.ftq_redirect : FTQRedirect = FTQRedirect()
        
    
    # @driver_hook(agent_name=AGENT_NAME)
    def get_ftq_ready(self):
        # self.f1_ready = self.f1_fire
        return self.icache_ready and self.f1_ready
    
    def get_fires(self):
        return {1: self.f0_fire, 2:self.f1_fire, 3: self.f2_fire, 4: self.wb_enable}
    
    # @driver_hook(agent_name=AGENT_NAME)
    def set_icache_ready(self, icache_ready):
        self.icache_ready = icache_ready

    def set_f2_mmio_exception(self, double_line, pmps, pbmts):
        self.f2_mmio_exception = [0, 0]
        if not double_line:
            return
        
        if pmps[0] != pmps[1] or pbmts[0] != pbmts[1]:
            self.f2_mmio_exception[1] = 3

        self.pmp_mmio = pmps[0]
        self.itlb_pbmt = pbmts[0]

    def set_ftq_valid(self, ftq_valid):
        self.ftq_valid = ftq_valid

    def step(self):
        # 更新f0_flush, f2_flush, f3_flush, mmio_redirect, wb_redirect
        last_f2_flush = self.f2_flush
        last_f2_fire = self.f2_fire
        last_f3_valid = self.f3_valid
        last_wb_valid = self.wb_valid
        # last_wb_redirect = self.wb_redirect
        # last_mmio_redirect = self.mmio_redirect
        last_f3_wb_not_flush = self.f3_wb_not_flush
        last_f1_valid = self.f1_valid
        last_f2_valid = self.f2_valid
        mmio_f3_flush = self.f3_flush
        last_f3_mmio_use_seq_pc = self.f3_mmio_use_seq_pc

        last_f2_icache_all_resp_reg = self.f2_icache_all_resp_reg


        self.ftq_valid = self.common_data.ftq_req.get(0).valid


        last_wb_enable =  self.wb_enable

        self.wb_valid = last_wb_enable

        self.wb_redirect = self.common_data.wb_ftq.misOffset.exists and last_wb_valid


        exception_exists = False
        for exc in self.f3_exception:
            if exc != 0:
                exception_exists = True
                break
        
        # done
        # the res related to func will not change 
        self.f3_req_is_mmio = last_f3_valid and (self.pmp_mmio or self.itlb_pbmt == PbmtAssist.NC ) and not exception_exists

        # temporarily done
        self.f3_wb_not_flush = self.common_data.ftq_req.get(4).ftqIdx == self.common_data.ftq_req.get(3).ftqIdx and last_f3_valid and last_wb_valid


#   val redirect_mmio_req =
#     fromFtqRedirectReg.valid && redirect_ftqIdx === f3_ftq_req.ftqIdx && redirect_ftqOffset === 0.U
        self.redirect_mmio_req = self.ftq_redirect.valid and self.ftq_redirect.ftqIdx == self.common_data.ftq_req.get(3).ftqIdx

        if ((last_f2_fire and not last_f2_flush) and self.f3_req_is_mmio):
            self.f3_mmio_use_seq_pc = True
        elif self.redirect_mmio_req: 
            # this condition value will be handled while receiving redirect req?
            self.f3_mmio_use_seq_pc = False
            
        # here is the 'last' mmio state
        self.mmio_redirect = self.f3_req_is_mmio and self.mmio_state == MMIOState.STATE_WAIT_COMMIT and self.last_from_uncache_valid and last_f3_mmio_use_seq_pc

        backend_redirect = self.ftq_redirect.valid
        self.f3_flush = backend_redirect or (self.wb_redirect and not last_f3_wb_not_flush)


        # these are all wires, so they all use value of this term
        self.f2_flush = backend_redirect or self.mmio_redirect or self.wb_redirect

        self.f0_flush = self.f2_flush or self.bpu_f0_flush


        # fires & readys to control

        
        # f3_ready := (io.toIbuffer.ready && (f3_mmio_req_commit || !f3_req_is_mmio)) || !f3_valid

        # ibuffer ready 是外部信号；也就是当前不是mmio状态或者mmio提交已经完成时可以为真

        self.f3_ready = self.to_ibuffer_ready and (self.f3_mmio_req_commit or not self.f3_req_is_mmio) or not last_f3_valid

                # icache_resp_all_valid

    #       val f2_icache_all_resp_wire =
    # fromICache.valid &&
    #   fromICache.bits.vaddr(0) === f2_ftq_req.startAddr &&
    #   (fromICache.bits.doubleline && fromICache.bits.vaddr(1) === f2_ftq_req.nextlineStart || !f2_doubleLine)

        

        #   when(f2_flush)(f2_icache_all_resp_reg := false.B)
    # .elsewhen(f2_valid && f2_icache_all_resp_wire && !f3_ready)(f2_icache_all_resp_reg := true.B)
    # .elsewhen(f2_fire && f2_icache_all_resp_reg)(f2_icache_all_resp_reg := false.B)


        self.f2_fire = last_f2_valid and self.f3_ready and self.icache_resp_all_valid

        self.f2_ready = self.f2_fire or not last_f2_valid

        self.f1_fire = last_f1_valid and self.f2_ready


        self.f3_fire = self.to_ibuffer_valid and self.to_ibuffer_ready
        

        self.f1_ready = self.f1_fire or not last_f1_valid

        self.f0_fire = self.ftq_valid and self.icache_ready and self.f1_ready



        # valids to control
        # f0 valid is ftq valid
        if self.f2_flush:
            self.f1_valid = False
        elif self.f0_fire and not self.f0_flush:
            self.f1_valid = True
        elif self.f1_fire:
            self.f1_valid = False

    #       when(f2_flush)(f2_valid := false.B)
    # .elsewhen(f1_fire && !f1_flush)(f2_valid := true.B)
    # .elsewhen(f2_fire)(f2_valid := false.B)

        if self.f2_flush:
            self.f2_valid = False
        elif self.f1_fire and not self.f2_flush:
            self.f2_valid = True
        elif self.f2_fire:
            self.f2_valid = False


        if self.f3_flush and not self.f3_req_is_mmio:
            self.f3_valid = False
        elif mmio_f3_flush and self.f3_req_is_mmio and not self.f3_need_not_flush:
            self.f3_valid = False
        elif self.f2_fire and not self.f2_flush:
            self.f3_valid = True
        elif self.f3_fire and not self.f3_req_is_mmio:
            self.f3_valid = False
        elif self.f3_req_is_mmio and self.f3_mmio_req_commit:
            self.f3_valid = False

        # done
        self.wb_enable = (last_f2_fire and not last_f2_flush) and (self.f3_req_is_mmio) and (not self.f3_flush) 

        self.f3_exception = self.f2_exception

        self.last_from_uncache_valid = self.from_uncache_valid

    # @driver_hook(agent_name=AGENT_NAME)
    def check_icache_resp_all_valid(self, icache_resp_valid, vaddrs, icache_doubleline, req_doubleline, start, next_start):
        if not req_doubleline:
            return True
        return icache_resp_valid and vaddrs[0] == start and (icache_doubleline and vaddrs[1] == next_start)

        # self.icache_resp_valid = icache_resp_valid
        # if not icache_resp_valid:
        #     self.f2_ready = False
        #     self.f1_fire = self.f2_ready
        # else:
        #     # here will be further changed and tested
        #     self.f2_ready = True
        #     self.f1_fire = self.f2_ready

            #       val f2_icache_all_resp_wire =
    # fromICache.valid &&
    #   fromICache.bits.vaddr(0) === f2_ftq_req.startAddr &&
    #   (fromICache.bits.doubleline && fromICache.bits.vaddr(1) === f2_ftq_req.nextlineStart || !f2_doubleLine)

    # @driver_hook(agent_name=AGENT_NAME)
    def flush_from_bpu(self, flush_bpu: FTQFlushFromBPU, cur_ftq_idx: FTQIdx):
        for key in flush_bpu.stgs.keys():
            flush_info: FTQFlushFromBPUStg = flush_bpu.stgs[key]
            if not flush_info.stg_valid:
                continue
            if not (flush_info.ftqIdx > cur_ftq_idx):
                return True
        return False

    def ftq_redirect(self, redirect: FTQRedirect):
        self.ftq_redirect.valid = redirect.valid
        self.ftq_redirect.ftqIdx.flag = redirect.ftqIdx.flag
        self.ftq_redirect.ftqIdx.value = redirect.ftqIdx.value
        self.ftq_redirect.ftqOffset = redirect.ftqOffset
        self.ftq_redirect.redirect_level = redirect.redirect_level

        self.backend_redirect = self.ftq_redirect.valid
        
    
    # @driver_hook(agent_name=AGENT_NAME)
    def get_bpu_flush(self):
        return self.bpu_f0_flush
    
    
    
    # may TODO: add pred checker err check and add mmio
    def redirect_flush(self, miss_pred_idx, valids, last_idx, rvcs, pred_check_stg1_res: PredCheckerStage1RetData, mmio=False):
        # TODO
        miss_off = ExistsIdx()
        mis_type = 0
        ranges = pred_check_stg1_res.ranges
        takens = pred_check_stg1_res.takens

        
        exists_last_half_err = check_last_valid(ranges, valids, last_idx, rvcs, takens, mmio=mmio) and last_idx != FULL_LAST_IDX
        # print(exists_last_half_err)
        self.last_half_valid = check_last_valid(ranges, valids, PREDICT_WIDTH - 1, rvcs, takens, mmio)
        if exists_last_half_err:
            miss_off.exists = True
            miss_off.offsetIdx = last_idx
            mis_type = LAST_HALF_ERR
            return miss_off, mis_type

        # here may to be fixed

        if 0 <= miss_pred_idx < 16:
            miss_off.exists = True
            miss_off.offsetIdx = miss_pred_idx
            mis_type = PRED_ERR

        return miss_off, mis_type
    
    def check_last_req_half_valid(self, ranges, valids, rvcs, takens):
        return check_last_valid(ranges, valids, PREDICT_WIDTH-1, rvcs, takens)

        
def check_last_valid(ranges, valids, last_idx, rvcs, takens, mmio=False):
    return ranges[last_idx] and valids[last_idx] and (not rvcs[last_idx]) and (not takens[last_idx]) \
        and (not mmio)
    
        
            
            
    
