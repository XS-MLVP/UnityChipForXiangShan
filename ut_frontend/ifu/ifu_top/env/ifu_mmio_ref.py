from .ifu_top_ctrl_ref import IFUTopCtrl
from ..datadef import MMIOReq, ExceptionType, FTQIdx, ITLBReq, MMIOToIbufferFTQ, MMIOCycleInfo, MMIOState, PbmtAssist
from ..instr_utils import is_rvc, if_call, if_ret, get_cfi_type
from .rvc_expander_ref import rvc_expand_ref

class IFUMMIOCtrler():
    def __init__(self):
        super().__init__()
        self.pbmt_assist = PbmtAssist()
        self.cur_state = MMIOState.STATE_IDLE
        self.next_mmio_state = MMIOState.STATE_IDLE
        self.first_instr = True
        self.low_instr = 0
        self.high_instr = 0
        self.mmio_rvc = False
        self.need_resend = False
        self.mmio_exception = 0
        self.resend_paddr = 0
        self.resend_gpaddr = 0
        self.exceptions = [False, False]
        self.commit_res = MMIOToIbufferFTQ()
        
    
    def calc_f2_mmio_exception(self, double_line, pmps, pbmts):
        f2_mmio_exception = [0, 0]
        if not double_line:
            return f2_mmio_exception
        
        if pmps[0] != pmps[1] or pbmts[0] != pbmts[1]:
            f2_mmio_exception[1] = 3
        return f2_mmio_exception

    def setup_before_mmio_states(self, cycle_req: MMIOCycleInfo, final_exceptions):
        self.cycle_req = cycle_req
        self.exceptions = final_exceptions
    
    def reset_all_state(self):
        self.reset_state()
        self.cur_state = MMIOState.STATE_IDLE
    
    def reset_state(self):
        self.next_mmio_state = MMIOState.STATE_IDLE
        self.need_resend = False
        self.mmio_rvc = False
        self.resend_paddr = 0
        self.resend_gpaddr = 0
        self.mmio_exception = ExceptionType.NONE
        
    def push_state(self, req: MMIOReq):
        last_state = self.cur_state
        self.cur_state = self.next_mmio_state
        if self.next_mmio_state == MMIOState.STATE_IDLE:
            is_mmio_space = (self.cycle_req.icache_pmp_mmios[0] or self.pbmt_assist.is_uncache(self.cycle_req.icache_itlb_pbmts[0])) and (self.exceptions[0] + self.exceptions[1] == 0)
            if is_mmio_space:
                if self.cycle_req.icache_itlb_pbmts[0] == PbmtAssist.NC:
                    self.next_mmio_state = MMIOState.STATE_SEND_REQ
                    # return self.next_mmio_state, self.cycle_req.icache_paddr
                else:
                    self.next_mmio_state = MMIOState.STATE_WAIT_LAST_CMT
                # self.from_icache_itlb_pbmt = req.itlb_pbmt
                # self.from_icache_pmp_mmio = req.pmp_mmio
        elif self.next_mmio_state == MMIOState.STATE_WAIT_LAST_CMT:            
            if self.first_instr or req.last_commited:
                self.next_mmio_state = MMIOState.STATE_SEND_REQ
                # return self.next_mmio_state, self.cycle_req.icache_paddr
            # else:
            #     if req.last_commit:
            #         self.mmio_state = MMIOState.STATE_SEND_REQ
            
        elif self.next_mmio_state == MMIOState.STATE_SEND_REQ:
            if req.to_uncache_ready:
                self.next_mmio_state = MMIOState.STATE_WAIT_RESP
        elif self.next_mmio_state == MMIOState.STATE_WAIT_RESP:
            self.high_instr = (req.from_uncache.data >> 16) & ((1 << 16) -1)
            self.low_instr = req.from_uncache.data & ((1 << 16) -1)
            self.commit_res = self.calc_instr_and_infos()
            if req.from_uncache.valid:
                self.mmio_rvc = (req.from_uncache.data & 3) != 3
                self.need_resend = (not self.mmio_rvc) and ((self.cycle_req.icache_paddr >> 1) & 3) == 3

                if self.need_resend:
                    self.next_mmio_state = MMIOState.STATE_SEND_TLB
                    itlb_req = ITLBReq()
                    itlb_req.vaddr = self.cycle_req.ftq_start_addr + 2
                    # return self.next_mmio_state, itlb_req
                else:
                    self.next_mmio_state = MMIOState.STATE_WAIT_COMMIT
                    # return self.next_mmio_state, self.get_instr_and_infos()

        elif self.next_mmio_state == MMIOState.STATE_SEND_TLB:
            if req.itlb_req_ready:
                self.next_mmio_state = MMIOState.STATE_TLB_RESP
                
        elif self.next_mmio_state == MMIOState.STATE_TLB_RESP:
            if req.itlb_resp.valid:
                itlb_resp_excp_code = req.itlb_resp.get_excp_code()
                self.resend_paddr = req.itlb_resp.paddr
                self.resend_gpaddr = req.itlb_resp.gpaddr
                if itlb_resp_excp_code != ExceptionType.NONE:
                    self.mmio_exception = itlb_resp_excp_code
                else:
                    self.mmio_exception = ExceptionType.AF if req.itlb_resp.pbmt != self.cycle_req.icache_itlb_pbmts[0] else ExceptionType.NONE
                
                if self.mmio_exception != ExceptionType.NONE:
                    self.next_mmio_state = MMIOState.STATE_WAIT_COMMIT
                    # return self.next_mmio_state, self.mmio_exception
                else:
                    self.next_mmio_state = MMIOState.STATE_SEND_PMP
                    # return self.next_mmio_state, self.resend_paddr


        elif self.next_mmio_state == MMIOState.STATE_SEND_PMP:
            self.mmio_exception = ExceptionType.AF if (req.pmp_resp.instr) or self.cycle_req.icache_pmp_mmios[0] != req.pmp_resp.mmio else ExceptionType.NONE 
            if self.mmio_exception != ExceptionType.NONE:
                self.next_mmio_state = MMIOState.STATE_WAIT_COMMIT
                # return self.next_mmio_state, self.mmio_exception
            else:
                self.next_mmio_state = MMIOState.STATE_RESEND_REQ
                # return self.next_mmio_state, self.resend_paddr

        elif self.next_mmio_state == MMIOState.STATE_RESEND_REQ:
            if req.to_uncache_ready:
                self.next_mmio_state = MMIOState.STATE_WAIT_RESEND_RESP
        elif self.next_mmio_state == MMIOState.STATE_WAIT_RESEND_RESP:
            if req.from_uncache.valid:
                self.next_mmio_state = MMIOState.STATE_WAIT_COMMIT
                self.high_instr = req.from_uncache.data & ((1 << 16) -1)
                self.commit_res = self.calc_instr_and_infos()
                # return self.next_mmio_state, self.get_instr_and_infos()
        elif self.next_mmio_state == MMIOState.STATE_WAIT_COMMIT:
            mmio_commit = any(commit.valid and commit.ftqIdx == self.cycle_req.ftq_idx and commit.ftqOffset == 0 for commit in req.rob_commits)
            if mmio_commit or self.cycle_req.icache_itlb_pbmts[0] == PbmtAssist.NC:
                self.next_mmio_state = MMIOState.STATE_COMMITED
                # return self.next_mmio_state, self.cycle_req.ftq_start_addr + 2 if self.is_rvc else self.cycle_req.ftq_start_addr + 4
        elif self.next_mmio_state == MMIOState.STATE_COMMITED:
            self.first_instr = self.first_instr and (not req.to_ibuffer_ready)
            self.reset_state()
            
        if last_state == MMIOState.STATE_WAIT_RESP and self.cur_state == MMIOState.STATE_SEND_TLB:
            itlb_req = ITLBReq()
            itlb_req.vaddr = self.cycle_req.ftq_start_addr + 2
            return [self.cur_state, itlb_req]
        elif (last_state == MMIOState.STATE_TLB_RESP or last_state == MMIOState.STATE_SEND_PMP) \
            and self.cur_state == MMIOState.STATE_WAIT_COMMIT.value:
            return [self.cur_state, self.mmio_exception, self.resend_gpaddr]
        elif (last_state == MMIOState.STATE_TLB_RESP.value and self.cur_state == MMIOState.STATE_SEND_PMP) \
            or (last_state == MMIOState.STATE_SEND_PMP.value and self.cur_state == MMIOState.STATE_RESEND_REQ):
            return [self.cur_state, self.resend_paddr]
        elif ((last_state == MMIOState.STATE_IDLE or last_state == MMIOState.STATE_WAIT_LAST_CMT) \
            and self.cur_state == MMIOState.STATE_SEND_REQ):
            return [self.cur_state, self.cycle_req.icache_paddr]
        elif (last_state == MMIOState.STATE_WAIT_RESP.value or last_state == MMIOState.STATE_WAIT_RESEND_RESP.value) \
            and self.cur_state == MMIOState.STATE_WAIT_COMMIT.value:
                return [self.cur_state, self.commit_res]
        elif (last_state == MMIOState.STATE_WAIT_COMMIT and self.cur_state == MMIOState.STATE_COMMITED):
            return [MMIOState.STATE_COMMITED, self.cycle_req.ftq_start_addr + 2 if self.commit_res.is_rvc else self.cycle_req.ftq_start_addr + 4]
            
        return [self.cur_state]
    
    def calc_instr_and_infos(self):
        res = MMIOToIbufferFTQ()
        new_instr = (self.high_instr << 16) | self.low_instr
        res.br_type = get_cfi_type(new_instr)
        
        res.is_rvc = is_rvc(new_instr)
        res.is_call = if_call(new_instr, res.br_type)
        res.is_ret = if_ret(new_instr, res.br_type)
        res.expd_instr, res.ill = rvc_expand_ref(new_instr, self.cycle_req.csr_fs_is_off)
        if res.ill:
            res.expd_instr = new_instr
        return res
