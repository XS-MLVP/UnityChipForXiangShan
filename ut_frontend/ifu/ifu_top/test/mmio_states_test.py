from .top_test_fixture import ifu_top_env
import toffee_test
from ..agent import OutsideAgent
from ..datadef import MMIOCycleInfo, MMIOReq, PbmtAssist, MMIOState, mmio_data_logger_instance
from ..env import IFUReceiverModel

async def state_changing_at_very_beginning(cycle_info: MMIOCycleInfo, top_agent:OutsideAgent, ifu_ref:IFUReceiverModel):
    await top_agent.set_up_before_mmio_states(cycle_info)
    ifu_ref.set_up_before_mmio_states(cycle_info)
    req = MMIOReq()
    await top_agent.cmp_single_mmio_req(req, ifu_ref.deal_with_single_mmio_req(req))

# use this case to check if the state machine will go to next stage with mmio not enabled
@toffee_test.testcase
async def test_mmio_not_into_mmio(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    mmio_cycle = MMIOCycleInfo()
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
    ifu_top_env.mmio_group.mark_function("state_transfer", test_mmio_not_into_mmio)
    
# 这个案例用来测试一般情况下first_instr会不会跳过
@toffee_test.testcase
async def test_mmio_itlb_pmp_and_first_instr(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_pmp_mmios[0] = True
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
    mmio_req: MMIOReq = MMIOReq()
    await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))
    ifu_top_env.mmio_group.mark_function("first_instrs", test_mmio_itlb_pmp_and_first_instr)

# 这个用例用来测试NC状态下会跳过first_instr
@toffee_test.testcase
async def test_mmio_itlb_nc_skip_first(ifu_top_env):
    # 测试设置为NC，是否跳过了first instr
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.NC
    await top_agent.set_up_before_mmio_states(mmio_cycle)
    ifu_ref.set_up_before_mmio_states(mmio_cycle)
    mmio_req: MMIOReq = MMIOReq()
    mmio_req = MMIOReq()
    mmio_req.from_uncache.data = 0x7b7e6081
    mmio_req.from_uncache.valid = True
    
    mmio_req.to_uncache_ready = True

    mmio_req.rob_commits[0].valid = True
    mmio_req.rob_commits[0].ftqIdx = mmio_cycle.ftq_idx
    for i in range(4):
        await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))        
    
    # print(f"state: {await top_agent.deal_with_single_mmio_req(mmio_req, mmio_data_logger_instance)}")
    # 添加一条新的MMIO单请求，判定NC对first instr的跳过是否不影响后续指令的判定
    await top_agent.reset_mmio_state()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    await top_agent.set_up_before_mmio_states(mmio_cycle)
    ifu_ref.set_up_before_mmio_states(mmio_cycle)
    mmio_req.last_commited = True
    for _ in range(2):
        await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))
    ifu_top_env.mmio_group.mark_function("state_transfer", test_mmio_itlb_nc_skip_first)
           

# 这个检查点检查在IO状态下的请求发送情况（类似NC）
@toffee_test.testcase
async def test_mmio_itlb_io_send_uncache_safe(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
    ifu_top_env.mmio_group.mark_function("state_transfer", test_mmio_itlb_io_send_uncache_safe)
    


async def double_line_diffs(case, top_agent: OutsideAgent, ifu_ref: IFUReceiverModel):
    """这个函数包含两个会引发doubleline异常的case

    Args:
        case (_type_): 引发异常的case序号，case 0 表示pmp端口状态不等，case 1 表示itlb pbmt两个端口状态不等
        top_agent (OutsideAgent): 用于驱动的agent
        ifu_ref (IFUReceiverModel): 功能ref
    """
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    if case == 0:
        # for this case, check pmp not equal and causing exception
        mmio_cycle.icache_pmp_mmios[0] = True
    else:
        # for this case check itlb pbmt not equal
        mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.ftq_start_addr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
    mmio_req : MMIOReq = MMIOReq()
    await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))  
    await top_agent.reset_mmio_state()
    

# 这个用例测试double line情况下的预测错误
@toffee_test.testcase
async def test_double_line_diffs(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    await double_line_diffs(0, top_agent, ifu_ref)
    await double_line_diffs(1, top_agent, ifu_ref)
    ifu_top_env.mmio_group.mark_function("state_transfer", test_double_line_diffs)
    
def get_resend_default_cfg(ftq_idx) -> MMIOReq:
    """这个函数根据ftq_idx生成一个默认的可以重发的配置

    Args:
        ftq_idx (_type_): ftqquery的ftqidx

    Returns:
        MMIOReq: 一个请求，作为重发的基础
    """
    mmio_req: MMIOReq = MMIOReq()
    mmio_req.from_uncache.valid = True
    mmio_req.from_uncache.data = 0x443
    mmio_req.to_uncache_ready = True
    mmio_req.rob_commits[1].ftqIdx = ftq_idx
    mmio_req.rob_commits[1].valid = True
    return mmio_req

# 测试向TLB发送异常下的处理情况
async def resend_send_tlb_excps(case, top_agent: OutsideAgent, ifu_ref:IFUReceiverModel):
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.icache_paddr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
    mmio_req: MMIOReq = get_resend_default_cfg(mmio_cycle.ftq_idx)
    mmio_req.itlb_req_ready = True
    mmio_req.itlb_resp.valid = True
    if case == 0:
        # for this case, check exception due to pbmt not equal
        mmio_req.itlb_resp.pbmt = 0
    else:
        # check for exception report by itlb
        mmio_req.itlb_resp.pbmt = mmio_cycle.icache_itlb_pbmts[0]
        # 设置三种异常独热码
        mmio_req.itlb_resp.excp.set_excp_one_hot(case)
    for _ in range(6):
        await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req)) 
    await top_agent.reset_mmio_state()

# 测试TLB发送遇异常的情况，包含状态不一致，和ITLB报告异常的情况
@toffee_test.testcase
async def test_resend_send_tlb_exception(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    for i in range(4):
        await resend_send_tlb_excps(i, top_agent, ifu_ref)
    ifu_top_env.mmio_group.mark_function("state_transfer", test_resend_send_tlb_exception)
    
# 测试重发过程中，pmp遇到异常的情况
async def resend_send_pmp_excp(case, top_agent: OutsideAgent, ifu_ref: IFUReceiverModel):
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.icache_paddr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
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
        await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))
    
    await top_agent.reset_mmio_state()

# pmp重发错误问题
@toffee_test.testcase
async def test_resend_send_pmp_mismatch(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    await resend_send_pmp_excp(0, top_agent, ifu_ref)
    await resend_send_pmp_excp(1, top_agent, ifu_ref)
    ifu_top_env.mmio_group.mark_function("state_transfer", test_resend_send_pmp_mismatch)
    

import random

async def rand_run_times(mmio_req: MMIOReq, top_agent: OutsideAgent, ifu_ref: IFUReceiverModel):
    for _ in range(random.randint(0, 4)):
        await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))

# 这个测试用例对应一次成功的重发，中间存在若干次停顿
@toffee_test.testcase
async def test_resend_normal(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    mmio_cycle: MMIOCycleInfo = MMIOCycleInfo()
    mmio_cycle.icache_itlb_pbmts[0] = PbmtAssist.IO
    mmio_cycle.icache_paddr = 0x576
    await state_changing_at_very_beginning(mmio_cycle, top_agent, ifu_ref)
    mmio_req : MMIOReq = get_resend_default_cfg(mmio_cycle.ftq_idx)
    mmio_req.itlb_req_ready = True
    mmio_req.itlb_resp.valid = True
    mmio_req.itlb_resp.pbmt = mmio_cycle.icache_itlb_pbmts[0]
    mmio_req.pmp_resp.mmio = mmio_cycle.icache_pmp_mmios[0]
    mmio_req.to_uncache_ready = False
    mmio_req.from_uncache.valid = False
    mmio_req.itlb_req_ready = False
    mmio_req.itlb_resp.valid = False
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.to_uncache_ready = True
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.from_uncache.valid = True
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.itlb_req_ready = True
    mmio_req.to_uncache_ready = False
    mmio_req.from_uncache.valid = False
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.itlb_resp.valid = True
    mmio_req.rob_commits[1].valid = False
    
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.to_uncache_ready = True
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.from_uncache.valid = True
    await rand_run_times(mmio_req, top_agent, ifu_ref)
    mmio_req.rob_commits[1].valid = True
    for _ in range(2):
        await top_agent.cmp_single_mmio_req(mmio_req, ifu_ref.deal_with_single_mmio_req(mmio_req))
        # print(f"first_instr: {top_agent.top.internal_wires._is_first_instr.value}")
    ifu_top_env.mmio_group.mark_function("state_transfer", test_resend_normal)

# 一次状态闭环的重新发送
async def random_once_req(top_agent: OutsideAgent, ifu_ref: IFUReceiverModel):
    cycle_info: MMIOCycleInfo = MMIOCycleInfo()
    cycle_info.workable_randomize()
    await top_agent.set_up_before_mmio_states(cycle_info)
    ifu_ref.set_up_before_mmio_states(cycle_info)
    while True:
        mmio_req: MMIOReq = MMIOReq()
        mmio_req.randomize_with_cycles(cycle_info)
        ref_state = ifu_ref.deal_with_single_mmio_req(mmio_req)
        res = await top_agent.cmp_single_mmio_req(mmio_req, ref_state)
        if res[0] == MMIOState.STATE_COMMITED:
            break
    await top_agent.reset_mmio_state()
        
import time
import random

@toffee_test.testcase
async def test_random_resends(ifu_top_env):
    top_agent: OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    seed = time.time_ns()
    random.seed(seed)
    # 1771817322909433303
    # 1771206108183421321
    # 1758367223082587666
    # 1758370058889010927
    print("seed =", seed)
    for i in range(20000):
        if i % 1000 == 0:
            print(f"epoch: {i}")
        await random_once_req(top_agent, ifu_ref)
    ifu_top_env.mmio_group.mark_function("state_transfer", test_random_resends)
    ifu_top_env.mmio_group.mark_function("seq_target", test_random_resends)
