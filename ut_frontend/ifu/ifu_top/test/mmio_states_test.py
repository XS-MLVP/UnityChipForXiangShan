from .top_test_fixture import ifu_top_env
import toffee_test
from ..agent import OutsideAgent
from ..datadef import MMIOCycleInfo, MMIOReq, PbmtAssist, MMIOState

async def state_changing_at_very_beginning(cycle_info: MMIOCycleInfo, top_agent:OutsideAgent):
    await top_agent.set_up_before_mmio_states(cycle_info)
    await top_agent.deal_with_single_mmio_req(MMIOReq())

# use this case to check if the state machine will go to next stage with mmio not enabled
@toffee_test.testcase
async def test_mmio_not_into_mmio(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    mmio_cycle = MMIOCycleInfo()
    await state_changing_at_very_beginning(mmio_cycle, top_agent)

@toffee_test.testcase
async def test_mmio_itlb_pmp_and_first_instr(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_pmp_mmios[0] = True
    await state_changing_at_very_beginning(mmio_cycle, top_agent)
    mmio_req: MMIOReq = MMIOReq()
    await top_agent.deal_with_single_mmio_req(mmio_req)

@toffee_test.testcase
async def test_mmio_itlb_nc_skip_first(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.NC
    await top_agent.set_up_before_mmio_states(mmio_cycle)
    mmio_req: MMIOReq = MMIOReq()
    mmio_req = MMIOReq()
    mmio_req.from_uncache.data = 0x7b7e6081
    mmio_req.from_uncache.valid = True
    
    mmio_req.to_uncache_ready = True

    mmio_req.rob_commits[0].valid = True
    mmio_req.rob_commits[0].ftqIdx = mmio_cycle.ftq_idx
    for i in range(4):
        await top_agent.deal_with_single_mmio_req(mmio_req)        
    
    # print(f"state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    await top_agent.reset_mmio_state()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    await top_agent.set_up_before_mmio_states(mmio_cycle)
    mmio_req.last_commited = True
    for _ in range(2):
        await top_agent.deal_with_single_mmio_req(mmio_req)     
    
@toffee_test.testcase
async def test_mmio_itlb_io(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    await state_changing_at_very_beginning(mmio_cycle, top_agent)

async def double_line_diffs(case, top_agent: OutsideAgent):
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    if case == 0:
        # for this case, check pmp not equal and causing exception
        mmio_cycle.icache_pmp_mmios[0] = True
    else:
        # for this case check pbmt not equal
        mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.ftq_start_addr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent)
    mmio_req : MMIOReq = MMIOReq()
    await top_agent.deal_with_single_mmio_req(mmio_req)
    await top_agent.reset_mmio_state()
    
@toffee_test.testcase
async def test_double_line_diffs(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    await double_line_diffs(0, top_agent)
    await double_line_diffs(1, top_agent)

# @toffee_test.testcase
# async def test_double_line_diff_pmp(ifu_top_env):
#     top_agent: OutsideAgent = ifu_top_env.top_agent
#     mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
#     mmio_cycle.icache_pmp_mmios[0] = True
#     mmio_cycle.ftq_start_addr = 0x576
#     await state_changing_at_very_beginning(mmio_cycle, top_agent)
#     mmio_req : MMIOReq = MMIOReq()
#     await top_agent.deal_with_single_mmio_req(mmio_req)

def get_resend_default_cfg(ftq_idx) -> MMIOReq:
    mmio_req: MMIOReq = MMIOReq()
    mmio_req.from_uncache.valid = True
    mmio_req.from_uncache.data = 0x443
    mmio_req.to_uncache_ready = True
    mmio_req.rob_commits[1].ftqIdx = ftq_idx
    mmio_req.rob_commits[1].valid = True
    return mmio_req

async def resend_send_tlb_excps(case, top_agent: OutsideAgent):
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.icache_paddr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent)
    mmio_req: MMIOReq = get_resend_default_cfg(mmio_cycle.ftq_idx)
    mmio_req.itlb_req_ready = True
    mmio_req.itlb_resp.valid = True
    if case == 0:
        # for this case, check exception due to pbmt not equal
        mmio_req.itlb_resp.pbmt = 0
    else:
        # check for exception report by itlb
        mmio_req.itlb_resp.pbmt = mmio_cycle.icache_itlb_pbmts[0]
        mmio_req.itlb_resp.excp.set_excp_one_hot(case)
    for _ in range(6):
        await top_agent.deal_with_single_mmio_req(mmio_req)
    await top_agent.reset_mmio_state()

@toffee_test.testcase
async def test_resend_send_tlb_exception(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    for i in range(4):
        await resend_send_tlb_excps(i, top_agent)

async def resend_send_pmp_excp(case, top_agent: OutsideAgent):
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.icache_paddr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent)
    mmio_req : MMIOReq = get_resend_default_cfg(mmio_cycle.ftq_idx)
    mmio_req.itlb_req_ready = True
    mmio_req.itlb_resp.valid = True
    mmio_req.itlb_resp.pbmt = mmio_cycle.icache_itlb_pbmts[0]
    if case == 0: 
        # for this case, pmp.mmio is not equal to that of icache
        mmio_req.pmp_resp.mmio = not mmio_cycle.icache_pmp_mmios[0]
    else:
        # for this case, pmp itself respond the exception
        mmio_req.pmp_resp.mmio = mmio_cycle.icache_pmp_mmios[0]
        mmio_req.pmp_resp.instr = True
    for _ in range(7):
        await top_agent.deal_with_single_mmio_req(mmio_req)
    await top_agent.reset_mmio_state()
    
@toffee_test.testcase
async def test_resend_send_pmp_mismatch(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    await resend_send_pmp_excp(0, top_agent)
    await resend_send_pmp_excp(1, top_agent)

import random

async def rand_run_times(mmio_req: MMIOReq, top_agent: OutsideAgent):
    for _ in range(random.randint(0, 4)):
        print(f"next: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
        
@toffee_test.testcase
async def test_resend_normal(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.icache_paddr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent)
    mmio_req : MMIOReq = get_resend_default_cfg(mmio_cycle.ftq_idx)
    mmio_req.itlb_req_ready = True
    mmio_req.itlb_resp.valid = True
    mmio_req.itlb_resp.pbmt = mmio_cycle.icache_itlb_pbmts[0]
    mmio_req.pmp_resp.mmio = mmio_cycle.icache_pmp_mmios[0]
    mmio_req.to_uncache_ready = False
    mmio_req.from_uncache.valid = False
    mmio_req.itlb_req_ready = False
    mmio_req.itlb_resp.valid = False
    await rand_run_times(mmio_req, top_agent)
    mmio_req.to_uncache_ready = True
    await rand_run_times(mmio_req, top_agent)
    mmio_req.from_uncache.valid = True
    await rand_run_times(mmio_req, top_agent)
    mmio_req.itlb_req_ready = True
    mmio_req.to_uncache_ready = False
    mmio_req.from_uncache.valid = False
    await rand_run_times(mmio_req, top_agent)
    mmio_req.itlb_resp.valid = True
    mmio_req.rob_commits[1].valid = False
    
    await rand_run_times(mmio_req, top_agent)
    mmio_req.to_uncache_ready = True
    await rand_run_times(mmio_req, top_agent)
    mmio_req.from_uncache.valid = True
    await rand_run_times(mmio_req, top_agent)
    mmio_req.rob_commits[1].valid = True
    for _ in range(2):
        print(f"next: {await top_agent.deal_with_single_mmio_req(mmio_req)}")

async def random_once_req(top_agent: OutsideAgent):
    cycle_info: MMIOCycleInfo = MMIOCycleInfo()
    cycle_info.workable_randomize()
    await top_agent.set_up_before_mmio_states(cycle_info)
    while True:
        mmio_req: MMIOReq = MMIOReq()
        mmio_req.randomize_with_cycles(cycle_info)
        res = await top_agent.deal_with_single_mmio_req(mmio_req)
        if res[0] == MMIOState.STATE_COMMITED:
            break
    await top_agent.reset_mmio_state()
        
@toffee_test.testcase
async def test_random_resends(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    for _ in range(5000):
        await random_once_req(top_agent)

