import toffee_test
from .top_test_fixture import ifu_top_env
from ..datadef import FTQQuery, ICacheStatusResp, FTQFlushInfo, FromUncache, ITLBResp, PMPResp, RobCommit, FrontendTriggerReq, FTQFlushFromBPU, FTQRedirect, NonMMIOReq, MMIOReq, MMIOCycleInfo
from ..agent import OutsideAgent

import random 

""" 这只是一个测试例子，仅仅展现了5个流水级中各个接口的触发时机， 如果环境有错误欢迎指出
  TBD: 一些后续其他用例的优化例子：
  设置某些ready为False阻塞，测试模块的情况
  设置工作到一半发一个请求信号
  跨预测块的请求（至少发两次）
  构造MMIO异常
  参考模型上，目前我的思路是在agent所有方法上加参考方法，同步调用参考模型，需要统一维护一套状态和上下文环境
  另外，很多输入数据之间是存在关系的，文档里描述了一些，但可能还有隐含的关系没有写明，欢迎提issue或discussion
  以及，通过修改构建脚本依赖的内部接口文件 scripts/ifu_related/ifu_top_internals.yaml，可以暴露更多的内部
  信息，比如flush，通过这些io信号之外的内部信号，可以更好地捕捉到模块内部的行为信息"""
@toffee_test.testcase
async def test_smoke1(ifu_top_env):

    # this is just an example, maybe still some hidden relations of the inputs need to be found
    ftq_query = FTQQuery()
    ftq_query.ftqIdx.flag = False
    ftq_query.ftqIdx.value = 0

    ftq_query.ftqOffset.exists = True
    ftq_query.ftqOffset.offsetIdx = 13
    ftq_query.startAddr = 14531232
    ftq_query.nextlineStart = ftq_query.startAddr + 64

    ftq_query.nextStartAddr = ftq_query.startAddr + 32


    icache_resp = ICacheStatusResp()
    icache_resp.ready = True
    icache_resp.resp.backend_exception = False
    icache_resp.resp.double_line = (ftq_query.startAddr & 32) != 0
    icache_resp.resp.pmp_mmios[0] = False
    icache_resp.resp.pmp_mmios[1] = False
    icache_resp.resp.data = 0x1096_1227_1189_1204_1217_1221_1444
    icache_resp.resp.vaddrs[0] = ftq_query.startAddr
    icache_resp.resp.vaddrs[1] = ftq_query.nextlineStart
    icache_resp.resp.exceptions[0] = False
    icache_resp.resp.exceptions[1] = False
    icache_resp.resp.paddr = 0x18151192
    icache_resp.resp.gpaddr = 0x1798180418121
    icache_resp.resp.icache_valid = False # if valid is true, it is not true, need more ctrl infos
    icache_resp.resp.VS_non_leaf_PTE = True
    icache_resp.resp.itlb_pbmts[0] = 0
    icache_resp.resp.itlb_pbmts[1] = 0

    # ftq_flush_info = FTQFlushInfo()

    flush_from_bpu = FTQFlushFromBPU()
    flush_from_bpu.stgs["s2"].stg_valid = True
    flush_from_bpu.stgs["s2"].ftqIdx.flag = False
    flush_from_bpu.stgs["s2"].ftqIdx.value =1
    flush_from_bpu.stgs["s3"].stg_valid = True
    flush_from_bpu.stgs["s3"].ftqIdx.flag = False
    flush_from_bpu.stgs["s3"].ftqIdx.value = 1

    # this data structure has no connection with non-mmio-situation, so it won't be used later
    ftq_redirect = FTQRedirect()
    ftq_redirect.redirect_level = False
    ftq_redirect.ftqIdx.flag = True
    ftq_redirect.ftqIdx.value = 12
    ftq_redirect.valid = False
    ftq_redirect.ftqOffset = 4

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
    fs_is_off = True

    rob_commits = [RobCommit() for i in range(8)]

    triggerReq = FrontendTriggerReq()

    top_agent:OutsideAgent = ifu_top_env.top_agent
    # done at stage 0
    top_agent.query_from_ftq(ftq_query)
    top_agent.from_ftq_flush(flush_from_bpu)
    top_agent.set_icache_ready(icache_resp.ready)
    # await top_agent.ftq_valid_set(True)

    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")

    # collect res of stage 0

    # await top_agent.get_ftq_ready()
    # await top_agent.get_bpu_flush()

    # print(top_agent.top.io_ftqInter._fromFtq._req._valid.value)

    await top_agent.step()


    # collect res of stage 1
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")


    # done at stage 2?

    # entering stage1


    top_agent.fake_resp(icache_resp)
    print(top_agent.get_icache_all_resp())

    await top_agent.step()

    # await top_agent.ftq_redirect(ftq_redirect)

    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")
    print(top_agent.get_icache_all_resp())

    # collect res of stage 2

    # await top_agent.get_icache_stop()
    # await top_agent.get_cut_instrs()
    # await top_agent.get_predecode_res()
    # await top_agent.get_cut_ptrs()

    # entering stage2
    # input at stage3?

    top_agent.set_fs_is_off(fs_is_off)
    top_agent.set_mmio_commited(True)

    top_agent.set_touncache_ready(True)
    top_agent.fake_from_uncache(from_uncache)

    top_agent.set_itlb_req_ready(True)
    top_agent.fake_get_itlb_req()

    top_agent.fake_itlb_resp(itlb_resp)

    top_agent.fake_pmp_resp(pmp_resp)

    top_agent.fake_rob_commits(rob_commits)

    await top_agent.set_triggers(triggerReq)

    top_agent.set_ibuffer_ready(True)


    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")


    # entering stage3
    # collect res of stage 3

    await top_agent.get_itlb_resp_ready()
    top_agent.receive_pmp_req_addr()
    await top_agent.get_to_uncache_req()
    await top_agent.receive_mmio_ftq_ptr()
    

    # await top_agent.get_exception_vecs()

    # await top_agent.get_f3_pcs()
    # await top_agent.get_addrs()

    # await top_agent.get_ranges()
    # await top_agent.get_f3predecoder_res()
    
    # await top_agent.get_extended_instrs()

    # await top_agent.get_pred_checker_stg1_res()

    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"at wb stage res collection")    

    print(f"fires:{fires}")
    print(f"flushes:{flushes}")
        # collect res of stage wb
    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"at wb collection + 1 stage")

    print(f"fires:{fires}")
    print(f"flushes:{flushes}")

    # top_agent.set_icache_ready(True)
    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")

    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")

    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")

    await top_agent.step()
    fires = await top_agent.get_fires()
    flushes = await top_agent.get_flushes()
    print(f"fires:{fires}")
    print(f"flushes:{flushes}")


@toffee_test.testcase
async def test_smoke_non_mmio(ifu_top_env):
    non_mmio_req = NonMMIOReq()

    non_mmio_req.ftq_req.ftqIdx.flag = False
    non_mmio_req.ftq_req.ftqIdx.value = 0

    non_mmio_req.ftq_req.ftqOffset.exists = True
    non_mmio_req.ftq_req.ftqOffset.offsetIdx = 13
    non_mmio_req.ftq_req.startAddr = 14531204
    non_mmio_req.ftq_req.nextlineStart = non_mmio_req.ftq_req.startAddr + 64

    non_mmio_req.ftq_req.nextStartAddr = non_mmio_req.ftq_req.startAddr + 80


    non_mmio_req.icache_resp.ready = True
    non_mmio_req.icache_resp.resp.backend_exception = False
    non_mmio_req.icache_resp.resp.pmp_mmios[0] = False
    non_mmio_req.icache_resp.resp.pmp_mmios[1] = False
    non_mmio_req.icache_resp.resp.data = 0x1096_1227_1189_1204_1217_1221_1444
    # non_mmio_req.icache_resp.resp.data = int("F"* 128, 16)
    print(hex(non_mmio_req.icache_resp.resp.data))
    non_mmio_req.icache_resp.resp.vaddrs[0] = non_mmio_req.ftq_req.startAddr
    non_mmio_req.icache_resp.resp.vaddrs[1] = non_mmio_req.ftq_req.nextlineStart
    non_mmio_req.icache_resp.resp.double_line = (non_mmio_req.icache_resp.resp.vaddrs[0] & 32) != 0

    # icache_resp.resp.vaddrs[1] = 114
    non_mmio_req.icache_resp.resp.exceptions[0] = False
    non_mmio_req.icache_resp.resp.exceptions[1] = False
    non_mmio_req.icache_resp.resp.paddr = 0x18151192
    non_mmio_req.icache_resp.resp.gpaddr = 0x1798180418121
    non_mmio_req.icache_resp.resp.icache_valid = True # if valid is true, it is not true, need more ctrl infos
    non_mmio_req.icache_resp.resp.VS_non_leaf_PTE = True
    non_mmio_req.icache_resp.resp.itlb_pbmts[0] = 0
    non_mmio_req.icache_resp.resp.itlb_pbmts[1] = 0

    # ftq_flush_info = FTQFlushInfo()

    non_mmio_req.bpu_flush_info.stgs["s2"].stg_valid = True
    non_mmio_req.bpu_flush_info.stgs["s2"].ftqIdx.flag = False
    non_mmio_req.bpu_flush_info.stgs["s2"].ftqIdx.value =1
    non_mmio_req.bpu_flush_info.stgs["s3"].stg_valid = True
    non_mmio_req.bpu_flush_info.stgs["s3"].ftqIdx.flag = False
    non_mmio_req.bpu_flush_info.stgs["s3"].ftqIdx.value = 1

    
    non_mmio_req.fs_is_off = True

    agent: OutsideAgent = ifu_top_env.top_agent

    await agent.deal_with_non_mmio(non_mmio_req)

@toffee_test.testcase
async def test_smoke_mmio(ifu_top_env):
    top_agent:OutsideAgent = ifu_top_env.top_agent

    # this is just an example, maybe still some hidden relations of the inputs need to be found
    mmio_cycle_req = MMIOCycleInfo()
    mmio_cycle_req.csr_fs_is_off = True
    mmio_cycle_req.exceptions = [False, False]
    mmio_cycle_req.ftq_idx.flag = False
    mmio_cycle_req.ftq_idx.value = 0
    mmio_cycle_req.ftq_start_addr = 14531204
    mmio_cycle_req.icache_itlb_pbmts = [2, 0]
    mmio_cycle_req.icache_pmp_mmios = [False, False]
    mmio_cycle_req.icache_paddr = 0x18151192
    await top_agent.set_up_before_mmio_states(mmio_cycle_req)
    
    mmio_req = MMIOReq()
    mmio_req.from_uncache.data = 0x12313134
    mmio_req.from_uncache.valid = True
    
    mmio_req.to_uncache_ready = True

    mmio_req.itlb_req_ready = True

    mmio_req.itlb_resp.valid = True
    mmio_req.itlb_resp.excp.afInstr = False
    mmio_req.itlb_resp.excp.gpfInstr = False
    mmio_req.itlb_resp.excp.pfInstr = False
    mmio_req.itlb_resp.gpaddr = 0x12121212
    mmio_req.itlb_resp.paddr = 0x13461456
    mmio_req.itlb_resp.pbmt = 0

    mmio_req.pmp_resp.instr = 0
    mmio_req.pmp_resp.mmio = True

    mmio_req.rob_commits = [RobCommit() for i in range(8)]
    mmio_req.rob_commits[0].valid = True
    mmio_req.rob_commits[0].ftqIdx = mmio_cycle_req.ftq_idx

    for _ in range(5):
        await top_agent.deal_with_single_mmio_req(mmio_req)
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")

    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")

    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    await top_agent.reset_mmio_state()
    print("resetting")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    
    # ftq_redirect.ftqOffset = 

    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")

    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")
    
    # print(f"mmio state: {await top_agent.deal_with_single_mmio_req(mmio_req)}")