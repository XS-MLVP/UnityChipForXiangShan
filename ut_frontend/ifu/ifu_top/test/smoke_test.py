import toffee_test
from .top_test_fixture import ifu_top_env
from ..datadef import FTQQuery, ICacheStatusResp, FTQFlushInfo, FromUncache, ITLBResp, PMPResp, RobCommit, FrontendTriggerReq
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

    ftq_query.ftqOffset.exists = False
    ftq_query.ftqOffset.offsetIdx = 0
    ftq_query.startAddr = 14531204
    ftq_query.nextlineStart = ftq_query.startAddr + 64

    ftq_query.nextStartAddr = 14531230


    icache_resp = ICacheStatusResp()
    icache_resp.ready = True
    icache_resp.resp.backend_exception = False
    icache_resp.resp.double_line = (ftq_query.startAddr & 256)
    icache_resp.resp.pmp_mmios[0] = False
    icache_resp.resp.pmp_mmios[1] = False
    icache_resp.resp.data = 0x1096_1227_1189_1204_1217_1221_1444
    icache_resp.resp.vaddrs[0] = ftq_query.startAddr
    icache_resp.resp.vaddrs[1] = ftq_query.nextlineStart
    icache_resp.resp.exceptions[0] = False
    icache_resp.resp.exceptions[1] = False
    icache_resp.resp.paddr = 0x18151192
    icache_resp.resp.gpaddr = 0x1798180418121
    icache_resp.resp.icache_valid = True # if valid is true, it is not true, need more ctrl infos
    icache_resp.resp.VS_non_leaf_PTE = True
    icache_resp.resp.itlb_pbmts[0] = 0
    icache_resp.resp.itlb_pbmts[1] = 0

    ftq_flush_info = FTQFlushInfo()
    ftq_flush_info.flush_from_bpu.stgs["s2"].stg_valid = True
    ftq_flush_info.flush_from_bpu.stgs["s2"].ftqIdx.flag = False
    ftq_flush_info.flush_from_bpu.stgs["s2"].ftqIdx.value = 2
    ftq_flush_info.flush_from_bpu.stgs["s3"].stg_valid = True
    ftq_flush_info.flush_from_bpu.stgs["s3"].ftqIdx.flag = False
    ftq_flush_info.flush_from_bpu.stgs["s3"].ftqIdx.value = 1

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
    fs_is_off = True

    rob_commits = [RobCommit() for i in range(8)]

    triggerReq = FrontendTriggerReq()

    top_agent:OutsideAgent = ifu_top_env.top_agent
    # done at stage 0
    await top_agent.query_from_ftq(ftq_query)
    await top_agent.from_ftq_flush(ftq_flush_info)
    await top_agent.set_icache_ready(icache_resp.ready)

    await top_agent.top.step()

    # entering stage 0

    await top_agent.get_bpu_flush()

    # print(top_agent.top.io_ftqInter._fromFtq._req._valid.value)

    await top_agent.top.step()
    await top_agent.get_ftq_ready()

    # done at stage 2?

    # entering stage1

    await top_agent.fake_resp(icache_resp, fs_is_off=fs_is_off)

    await top_agent.top.step()

    # entering stage2
    # done at stage3?
    await top_agent.receive_mmio_ftq_ptr()
    await top_agent.set_mmio_commited(True)

    await top_agent.set_touncache_ready(True)
    await top_agent.get_to_uncache_req()
    await top_agent.fake_from_uncache(from_uncache)

    await top_agent.set_itlb_req_ready(True)
    await top_agent.fake_get_itlb_req()

    await top_agent.get_itlb_resp_ready()
    await top_agent.fake_itlb_resp(itlb_resp)

    await top_agent.receive_pmp_req_addr()
    await top_agent.fake_pmp_resp(pmp_resp)

    await top_agent.fake_rob_commits(rob_commits)

    await top_agent.set_triggers(triggerReq)

    await top_agent.set_ibuffer_ready(True)
    await top_agent.get_icache_stop()
    await top_agent.get_cut_instrs()
    await top_agent.get_predecode_res()

    await top_agent.top.step()
    
    # entering stage3
    # collect res of stage 2
    await top_agent.get_exception_vecs()

    await top_agent.get_f1_pcs_cut_ptrs()
    await top_agent.get_addrs()

    print()
    print(f"f1_valid: {top_agent.top.internal_wires._f1_valid.value}")
    print(f"f2_flush: {top_agent.top.internal_wires._f2_flush.value}")
    print(f"f0_flush_from_bpu_probe: {top_agent.top.internal_wires._f0_flush_from_bpu_probe.value}")
    # print(top_agent.top.internal_flushes._f2_ready.value)
    print(f"f1_fire: {top_agent.top.internal_wires._f1_fire.value}")
    print(f"f2_fire: {top_agent.top.internal_wires._f2_fire.value}")
    print(f"f3_fire: {top_agent.top.internal_wires._f3_ready.value}")

    await top_agent.get_ranges()
    await top_agent.get_f3predecoder_res()
    
    await top_agent.get_extended_instrs()

    await top_agent.top.step()

        # collect res of stage 3

    res1 = await top_agent.get_pred_checker_res()
    await top_agent.collect_res_backto_ftq()

    await top_agent.get_cur_last_half_valid()

    await top_agent.get_toibuffer_info()


    

