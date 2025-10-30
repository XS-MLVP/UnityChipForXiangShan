from ..env import IFUTopEnv
from toffee.funcov import CovGroup
from ..datadef import MMIOState

from comm import UT_FCOV


mmio_transfer = [
    ("not_in_mmio", MMIOState.STATE_IDLE, MMIOState.STATE_IDLE),
    ("not_nc_so_wait", MMIOState.STATE_IDLE, MMIOState.STATE_WAIT_LAST_CMT),
    ("nc_so_send", MMIOState.STATE_IDLE, MMIOState.STATE_SEND_REQ),
    ("wait_last_finished", MMIOState.STATE_WAIT_LAST_CMT, MMIOState.STATE_SEND_REQ),
    ("waiting_for_last", MMIOState.STATE_WAIT_LAST_CMT, MMIOState.STATE_WAIT_LAST_CMT),
    ("waiting_sending", MMIOState.STATE_SEND_REQ, MMIOState.STATE_SEND_REQ),
    ("send_to_uncache", MMIOState.STATE_SEND_REQ, MMIOState.STATE_WAIT_RESP),
    ("waiting_uncache_resp", MMIOState.STATE_WAIT_RESP, MMIOState.STATE_WAIT_RESP),
    ("uncache_once_finished", MMIOState.STATE_WAIT_RESP, MMIOState.STATE_WAIT_COMMIT),
    ("need_resend", MMIOState.STATE_WAIT_RESP, MMIOState.STATE_SEND_TLB),
    ("waiting_sending_tlb", MMIOState.STATE_SEND_TLB, MMIOState.STATE_SEND_TLB),
    ("send_to_tlb", MMIOState.STATE_SEND_TLB, MMIOState.STATE_TLB_RESP),
    ("waiting_tlb_resp", MMIOState.STATE_TLB_RESP, MMIOState.STATE_TLB_RESP),
    ("tlb_resp_exception", MMIOState.STATE_TLB_RESP, MMIOState.STATE_WAIT_COMMIT),
    ("able_to_send_pmp", MMIOState.STATE_TLB_RESP, MMIOState.STATE_SEND_PMP),
    ("pmp_resp_exception", MMIOState.STATE_SEND_PMP, MMIOState.STATE_WAIT_COMMIT),
    ("going_to_resend", MMIOState.STATE_SEND_PMP, MMIOState.STATE_RESEND_REQ),
    ("waiting_resend", MMIOState.STATE_RESEND_REQ, MMIOState.STATE_RESEND_REQ),
    ("resend_to_uncache", MMIOState.STATE_RESEND_REQ, MMIOState.STATE_WAIT_RESEND_RESP),
    ("waiting_uncache_resp", MMIOState.STATE_WAIT_RESEND_RESP, MMIOState.STATE_WAIT_RESEND_RESP),
    ("resend_commit", MMIOState.STATE_WAIT_RESEND_RESP, MMIOState.STATE_WAIT_COMMIT),
    ("committing", MMIOState.STATE_WAIT_COMMIT, MMIOState.STATE_WAIT_COMMIT),
    ("commited", MMIOState.STATE_WAIT_COMMIT, MMIOState.STATE_COMMITED)
]

def is_provider_start_end_state(start_state, end_state):
    def provider_start_end_state(env: IFUTopEnv) -> bool:
        return env.top_agent.last_state == start_state and env.top_agent.cur_state == end_state
    return provider_start_end_state

def is_provider_mmio_rvc(rvc):
    def provider_mmio_rvc(env: IFUTopEnv) -> bool:
        return env.top_agent.cur_state == MMIOState.STATE_WAIT_COMMIT and env.top_agent.toIbufferAll._toIbuffer._bits._pd[0]._isRVC.value == rvc
    return provider_mmio_rvc
    
def is_provider_first_instr(is_first):
    def provider_first_instr(env: IFUTopEnv) -> bool:
        return env.top_agent.top.internal_wires._is_first_instr.value == is_first
    return provider_first_instr

def get_coverage_group_mmio(env: IFUTopEnv):
    group = CovGroup(UT_FCOV("../UT_IFU_TOP"))
    
    group.add_watch_point(env, {
        "_first_instr_unused": is_provider_first_instr(True),
        "_first_instr_used": is_provider_first_instr(False)
    }, name="first_instrs")
    
    group.add_watch_point(env, 
        {f"_{desc}": is_provider_start_end_state(start, end) for (desc, start, end) in mmio_transfer}
    , name="state_transfer")   
    
    group.add_watch_point(env,
        {f"_rvc_is_{i}": is_provider_mmio_rvc(i) for i in range(2)}
    , name="seq_target")
    return group
    
    
    
    
    
    
    
    