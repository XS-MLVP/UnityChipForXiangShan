import toffee_test
from ..agent import OutsideAgent
from ..instr_utils import construct_non_cfis, rebuild_cacheline_from_parts
from ..datadef import NonMMIOReq
from ..commons import calc_double_line, randbool
from .top_test_fixture import ifu_top_env

import random

@toffee_test.testcase
async def test_cross_prediction_block(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    
    normal_req: NonMMIOReq = NonMMIOReq()
    # instrs = []
    instrs = [construct_non_cfis(rvc=True, rvc_enabled=True) for _ in range(1)]
    for _ in range(16):
        # rvi_instr = construct_non_cfis(rvc=False, rvc_enabled=True)
        # instrs.append(rvi_instr & ((1 << 16) - 1))
        rvi_instr_lo_hi = construct_non_cfis(rvc=False, rvc_enabled=True) & ((1 << 16) - 1)
        instrs.append(rvi_instr_lo_hi)
    normal_req.fs_is_off = True
    normal_req.ftq_req.ftqIdx.randomize()
    normal_req.ftq_req.ftqOffset.exists = False
    normal_req.ftq_req.startAddr = 0x19291204
    normal_req.ftq_req.nextlineStart = normal_req.ftq_req.startAddr + 64
    normal_req.ftq_req.nextStartAddr = normal_req.ftq_req.startAddr + 32
    normal_req.ftq_req.valid = True
    
    normal_req.icache_resp.ready= True
    normal_req.icache_resp.resp.data = rebuild_cacheline_from_parts(normal_req.ftq_req.startAddr, instrs)
    normal_req.icache_resp.resp.backend_exception = True
    normal_req.icache_resp.resp.double_line = calc_double_line(normal_req.ftq_req.startAddr)
    normal_req.icache_resp.resp.gpaddr = 0x13456172
    normal_req.icache_resp.resp.icache_valid = True
    normal_req.icache_resp.resp.vaddrs = [normal_req.ftq_req.startAddr, normal_req.ftq_req.nextStartAddr]
    normal_req.icache_resp.resp.paddr = 0x1224
    
    res = await top_agent.deal_with_non_mmio(normal_req)
    print(f"last_valid_half: {top_agent.top.internal_wires._f3_lastHalf_valid.value}")
    
    # instrs = []
    instrs = [construct_non_cfis(rvc=True, rvc_enabled=True) for _ in range(2)]
    for _ in range(15):
        # rvi_instr = construct_non_cfis(rvc=False, rvc_enabled=True)
        # instrs.append(rvi_instr & ((1 << 16) - 1))
        rvi_instr_lo_hi = construct_non_cfis(rvc=False, rvc_enabled=True) & ((1 << 16) - 1)
        instrs.append(rvi_instr_lo_hi)
    normal_req.icache_resp.resp.data = rebuild_cacheline_from_parts(normal_req.ftq_req.startAddr, instrs) 
    
    res = await top_agent.deal_with_non_mmio(normal_req)

async def check_icache_valids(case, top_agent: OutsideAgent):
    normal_req: NonMMIOReq = NonMMIOReq()
    normal_req.fs_is_off = randbool()
    normal_req.ftq_req.set_start_addr(0x1524)
    normal_req.ftq_req.nextStartAddr = normal_req.ftq_req.startAddr + 32
    normal_req.icache_resp.resp.double_line = True
    normal_req.icache_resp.resp.icache_valid = True
    if case == 0:
        normal_req.icache_resp.resp.icache_valid = False
    elif case == 1:
        # cur addr err
        normal_req.icache_resp.resp.vaddrs[1] = normal_req.ftq_req.nextlineStart
    elif case == 2:
        # cur addr err
        normal_req.icache_resp.resp.double_line = False
        
        # normal_req.icache_resp.resp.vaddrs[1] = normal_req.ftq_req.nextlineStart
    elif case == 3:
        # nextline addr err
        normal_req.icache_resp.resp.vaddrs[0] = normal_req.ftq_req.startAddr
    await top_agent.deal_with_non_mmio(normal_req)


@toffee_test.testcase
async def test_cross_double_line(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    
    for i in range(4):
        await check_icache_valids(i, top_agent)
        await top_agent.reset()

@toffee_test.testcase
async def test_cross_prediction_block(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    
    normal_req: NonMMIOReq = NonMMIOReq()
    # instrs = []
    instrs = [construct_non_cfis(rvc=True, rvc_enabled=True) for _ in range(1)]
    for _ in range(16):
        # rvi_instr = construct_non_cfis(rvc=False, rvc_enabled=True)
        # instrs.append(rvi_instr & ((1 << 16) - 1))
        rvi_instr_lo_hi = construct_non_cfis(rvc=False, rvc_enabled=True) & ((1 << 16) - 1)
        instrs.append(rvi_instr_lo_hi)
    normal_req.fs_is_off = True
    normal_req.ftq_req.ftqIdx.randomize()
    normal_req.ftq_req.ftqOffset.exists = False
    normal_req.ftq_req.startAddr = 0x19291204
    normal_req.ftq_req.nextlineStart = normal_req.ftq_req.startAddr + 64
    normal_req.ftq_req.nextStartAddr = normal_req.ftq_req.startAddr + 32
    normal_req.ftq_req.valid = True
    
    normal_req.icache_resp.ready= True
    normal_req.icache_resp.resp.data = rebuild_cacheline_from_parts(normal_req.ftq_req.startAddr, instrs)
    normal_req.icache_resp.resp.backend_exception = True
    normal_req.icache_resp.resp.double_line = calc_double_line(normal_req.ftq_req.startAddr)
    normal_req.icache_resp.resp.gpaddr = 0x13456172
    normal_req.icache_resp.resp.icache_valid = True
    normal_req.icache_resp.resp.vaddrs = [normal_req.ftq_req.startAddr, normal_req.ftq_req.nextStartAddr]
    normal_req.icache_resp.resp.paddr = 0x1224
    normal_req.icache_resp.resp.exceptions = [3, 0]
    
    res = await top_agent.deal_with_non_mmio(normal_req)
    # print(f"last_valid_half: {top_agent.top.internal_wires._f3_lastHalf_valid.value}")


@toffee_test.testcase
async def test_random_non_mmios(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    random.seed(1105)
    print(f"Random seed set to: 1105 | {random.seed}")
    for _ in range(12000):
        req : NonMMIOReq = NonMMIOReq()
        req.randomize()
        await top_agent.deal_with_non_mmio(req)    
        # await top_agent.reset()