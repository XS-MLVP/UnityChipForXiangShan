import toffee_test
from .top_test_fixture import ifu_top_env
from ..datadef import FTQQuery, ICacheStatusResp, FTQFlushInfo, FromUncache, ITLBResp, PMPResp, RobCommit, FrontendTriggerReq

import random 

@toffee_test.testcase
async def test_smoke(ifu_top_env):

    # this is just an example, maybe still some hidden relations of the inputs need to be found
    ftq_query = FTQQuery()
    ftq_query.ftqIdx.flag = False
    ftq_query.ftqIdx.value = 2

    ftq_query.ftqOffset.exists = False
    ftq_query.ftqOffset.offsetIdx = 0 
    ftq_query.startAddr = 14531204
    ftq_query.nextlineStart = ftq_query.startAddr + 64

    # TBD: 随机生成指令序列之后再造一个
    # prepare_next = random.randint(0, (1 << 50) - 128)
    # ftq_query.nextStartAddr = (random.randint(0, (1 << 50) - 128) + ftq_query.startAddr) % (ftq_query.startAddr - 64)
    ftq_query.nextStartAddr = 19191898


    icache_resp = ICacheStatusResp()
    icache_resp.ready = True
    icache_resp.resp.backend_exception = False
    icache_resp.resp.double_line = (ftq_query.startAddr & 256)
    icache_resp.resp.pmp_mmios[0] = False
    icache_resp.resp.pmp_mmios[1] = False
    icache_resp.resp.data = 0x1096_1144_1189_1204_1217_1221_1444
    icache_resp.resp.vaddrs[0] = ftq_query.startAddr
    icache_resp.resp.vaddrs[1] = ftq_query.nextlineStart
    icache_resp.resp.exceptions[0] = False
    icache_resp.resp.exceptions[1] = False
    icache_resp.resp.paddr = 0x18151192
    icache_resp.resp.gpaddr = 0x1798180418121814
    icache_resp.resp.icache_valid = True
    icache_resp.resp.VS_non_leaf_PTE = True
    icache_resp.resp.itlb_pbmts[0] = 0
    icache_resp.resp.itlb_pbmts[1] = 0

    ftq_flush_info = FTQFlushInfo()
    ftq_flush_info.flush_from_bpu.stgs["s2"].stg_valid = True
    ftq_flush_info.flush_from_bpu.stgs["s2"].ftqIdx.flag = False
    ftq_flush_info.flush_from_bpu.stgs["s2"].ftqIdx.value = 4
    ftq_flush_info.flush_from_bpu.stgs["s3"].stg_valid = False
    ftq_flush_info.flush_from_bpu.stgs["s3"].ftqIdx.flag = False
    ftq_flush_info.flush_from_bpu.stgs["s3"].ftqIdx.value = 6

    ftq_flush_info.redirect.redirect_level = False
    ftq_flush_info.redirect.ftqIdx.flag = True
    ftq_flush_info.redirect.ftqIdx.value = 12
    ftq_flush_info.redirect.valid = False
    ftq_flush_info.redirect.ftqOffset = 4

    from_uncache = FromUncache()
    from_uncache.data = 0x12313134
    from_uncache.valid = True

    itlb_resp = ITLBResp()

    itlb_resp.valid = True
    itlb_resp.excp.afInstr = False
    itlb_resp.excp.gpfInstr = False
    itlb_resp.excp.pfInstr = False
    itlb_resp.gpaddr = 0x12121212
    itlb_resp.isForVSnonLeafPTE = False
    itlb_resp.paddr = 0x13461456
    itlb_resp.pbmt = 0

    pmp_resp = PMPResp()
    pmp_resp.instr = 0
    pmp_resp.mmio = True

    rob_commits = [RobCommit() for i in range(8)]

    triggerReq = FrontendTriggerReq()
    triggerReq.fsIsOff = True
    # done at stage 0

    await ifu_top_env.top_agent.query_from_ftq(ftq_query)
    await ifu_top_env.top_agent.from_ftq_flush(ftq_flush_info)
    await ifu_top_env.top_agent.set_icache_ready(icache_resp.ready)
    await ifu_top_env.top_agent.top.step(2)
    # done at stage 2?
    await ifu_top_env.top_agent.get_ftq_ready()
    await ifu_top_env.top_agent.fake_resp(icache_resp)
    await ifu_top_env.top_agent.top.step()
    # done at stage3?
    await ifu_top_env.top_agent.receive_mmio_ftq_ptr()
    await ifu_top_env.top_agent.set_mmio_commited(True)

    await ifu_top_env.top_agent.set_touncache_ready(True)
    await ifu_top_env.top_agent.get_to_uncache_req()
    await ifu_top_env.top_agent.fake_from_uncache(from_uncache)

    await ifu_top_env.top_agent.set_itlb_req_ready(True)
    await ifu_top_env.top_agent.fake_get_itlb_req()

    await ifu_top_env.top_agent.get_itlb_resp_ready()
    await ifu_top_env.top_agent.fake_itlb_resp(itlb_resp)

    await ifu_top_env.top_agent.receive_pmp_req_addr()
    await ifu_top_env.top_agent.fake_pmp_resp(pmp_resp)

    await ifu_top_env.top_agent.fake_rob_commits(rob_commits)

    await ifu_top_env.top_agent.set_triggers(triggerReq)

    await ifu_top_env.top_agent.set_ibuffer_ready(True)
    await ifu_top_env.top_agent.get_toibuffer_info()

    await ifu_top_env.top_agent.get_icache_stop()
    await ifu_top_env.top_agent.top.step()
    
    await ifu_top_env.top_agent.collect_res_backto_ftq()



