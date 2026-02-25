import toffee_test
from ..agent import OutsideAgent
from ..instr_utils import construct_non_cfis, rebuild_cacheline_from_parts
from ..datadef import NonMMIOSingleReq, ICacheResp, FTQQuery,FTQIdx, ICacheStatusResp,ClusteredNonMMIOReqs, NonMMIOResp
from ..commons import calc_double_line, randbool
from .top_test_fixture import ifu_top_env
from ..env import IFUReceiverModel

import random

# 这部分测试的是top中stage0失败的逻辑，包含两类，一类是ICache没有ready，一类是需要冲刷当前的idx
@toffee_test.testcase
async def test_stage0_failure(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    reqs: ClusteredNonMMIOReqs = ClusteredNonMMIOReqs()
    
    icache_not_ready_req: NonMMIOSingleReq = NonMMIOSingleReq()
    icache_not_ready_req.icache_ready = False
    reqs.reqs.append(icache_not_ready_req)
    reqs.resps.append(ifu_ref.inner_deal_with_non_mmio(icache_not_ready_req))
    
    # reqs.reqs.append(icache_not_ready_req)
    choices = [(False, -1), (True, 1)] 
    
    for i in range(8):
        bpu_flush_flag_same_req: NonMMIOSingleReq = NonMMIOSingleReq()
        bpu_flush_flag_same_req.ftq_req.ftqIdx.flag = ((i%4) // 2== 0)
        bpu_flush_flag_same_req.ftq_req.ftqIdx.value = 4
        bpu_flush_flag_same_req.bpu_flush_info.clear_init()
        choice = choices[i//4]
        stg_name = f"s{i%2 + 2}"
        rev_stg_name = f"s{3-i%2}"
        bpu_flush_flag_same_req.bpu_flush_info.stgs[stg_name].stg_valid = True
        bpu_flush_flag_same_req.bpu_flush_info.stgs[rev_stg_name].stg_valid = False
        bpu_flush_flag_same_req.bpu_flush_info.stgs[stg_name].ftqIdx.value = \
            bpu_flush_flag_same_req.ftq_req.ftqIdx.value + choice[1]
        bpu_flush_flag_same_req.bpu_flush_info.stgs[stg_name].ftqIdx.flag = \
            bpu_flush_flag_same_req.ftq_req.ftqIdx.flag ^ choice[0]
        reqs.reqs.append(bpu_flush_flag_same_req)
        reqs.resps.append(ifu_ref.inner_deal_with_non_mmio(bpu_flush_flag_same_req))
    await top_agent.deal_with_non_mmio_clusters(reqs)
    ifu_top_env.top_group.mark_function("icache_ready", test_stage0_failure)
    ifu_top_env.top_group.mark_function("bpu_flush", test_stage0_failure)    

# 这个函数测试的是ICache阻塞的情况，共分为四种
@toffee_test.testcase
async def test_icache_not_valid_cases(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    
    # 设置一条请求的初始状态
    req_with_icache_invalids: NonMMIOSingleReq = NonMMIOSingleReq()
    req_with_icache_invalids.fs_is_off = randbool()
    req_with_icache_invalids.ftq_req.set_start_addr(0x1524)
    req_with_icache_invalids.ftq_req.nextStartAddr = req_with_icache_invalids.ftq_req.startAddr + 32
    
    # 情况1：icache_valid为false
    icache_resp_invalid_self: ICacheResp = ICacheResp(ftq_req=req_with_icache_invalids.ftq_req, init_as_valid=True)
    icache_resp_invalid_self.icache_valid = False
    req_with_icache_invalids.invalid_icache_resps.append(icache_resp_invalid_self)
    
    # 情况2: vaddr_0和startaddr不匹配
    icache_resp_cur_addr_err: ICacheResp = ICacheResp(ftq_req=req_with_icache_invalids.ftq_req, init_as_valid=True)
    icache_resp_cur_addr_err.vaddrs[0]=0x1444
    req_with_icache_invalids.invalid_icache_resps.append(icache_resp_cur_addr_err)
    
    # 情况3：double line错误
    icache_resp_double_line_err: ICacheResp = ICacheResp(ftq_req=req_with_icache_invalids.ftq_req, init_as_valid=True)
    icache_resp_double_line_err.double_line = False
    req_with_icache_invalids.invalid_icache_resps.append(icache_resp_double_line_err)
    
    # 情况4：vaddr_1和nextlineaddr不匹配
    icache_resp_nextline_addr_err: ICacheResp = ICacheResp(ftq_req=req_with_icache_invalids.ftq_req, init_as_valid=True)
    icache_resp_nextline_addr_err.vaddrs[1]=0x1444
    req_with_icache_invalids.invalid_icache_resps.append(icache_resp_nextline_addr_err)

    req_with_icache_invalids.final_icache_resp.randomize(req_with_icache_invalids.ftq_req)


    cluster: ClusteredNonMMIOReqs = ClusteredNonMMIOReqs()
    cluster.reqs.append(req_with_icache_invalids)
    cluster.resps.append(ifu_ref.inner_deal_with_non_mmio(req_with_icache_invalids))
    req_another: NonMMIOSingleReq = NonMMIOSingleReq()
    req_another.randomize()
    cluster.reqs.append(req_another)
    cluster.resps.append(ifu_ref.inner_deal_with_non_mmio(req_another))
    await top_agent.deal_with_non_mmio_clusters(cluster)
    ifu_top_env.top_group.mark_function("icache_all_valid", test_icache_not_valid_cases)

# 用一个真实的随即例子测试跨预测块的请求
@toffee_test.testcase
async def test_cross_prediction_block(ifu_top_env):
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    top_agent : OutsideAgent = ifu_top_env.top_agent
    req1 : NonMMIOSingleReq = NonMMIOSingleReq()
    # first req that may trigger wrong condition
    req1.fs_is_off = True
    req1.ftq_req.valid = True
    req1.ftq_req.ftqIdx.flag = True
    req1.ftq_req.ftqIdx.value = 11
    req1.ftq_req.ftqOffset.exists = False
    req1.ftq_req.ftqOffset.offsetIdx = 15
    req1.ftq_req.nextlineStart = 754912186775546
    req1.ftq_req.startAddr = 754912186775482
    # req1.ftq_req.nextStartAddr=323036143508946
    req1.ftq_req.nextStartAddr=754912186775514
    
    req1.icache_ready = True
    
    req1.final_icache_resp = ICacheResp(
        itlb_pbmts=[0, 0],
        pmp_mmios=[False, False],
        exceptions=[3, 0],
        vaddrs=[754912186775482, 754912186775546],
        paddr=404033938,
        VS_non_leaf_PTE=True,
        data=7283205146466666787615510459749180600166653367786977051173264907390803464150081059653197407328432508533526888081055979451474366030242223105181599048187283,
        backend_exception=True,
        double_line=1,
        gpaddr=29633898249398642,
        icache_valid=True
    )
    req1.bpu_flush_info.stgs["s2"].stg_valid = False
    req1.bpu_flush_info.stgs["s2"].ftqIdx.flag = False
    req1.bpu_flush_info.stgs["s2"].ftqIdx.value = 0
    
    req1.bpu_flush_info.stgs["s3"].stg_valid = False
    req1.bpu_flush_info.stgs["s3"].ftqIdx.flag = False
    req1.bpu_flush_info.stgs["s3"].ftqIdx.value = 0   
    
    # res = await top_agent.deal_with_non_mmio_outer(req1)
    
    # print(f"last res(to check last half valid): {res}")
    # print(f"last half valid: {top_agent.get_cur_last_half_valid()}")
    # await top_agent.step()
    # print(f"last half valid: {top_agent.get_cur_last_half_valid()}")
    # await top_agent.step()
    # print(f"last half valid: {top_agent.get_cur_last_half_valid()}")
    # await top_agent.step()
    # print(f"last half valid: {top_agent.get_cur_last_half_valid()}")
    req2 : NonMMIOSingleReq = NonMMIOSingleReq()
    req2.ftq_req.valid = True
    req2.ftq_req.ftqIdx.flag = False
    req2.ftq_req.ftqIdx.value = 15
    req2.ftq_req.ftqOffset.exists = True
    req2.ftq_req.ftqOffset.offsetIdx = 4
    req2.ftq_req.nextlineStart=1064050532637454
    req2.ftq_req.startAddr=1064050532637392
    req2.ftq_req.nextStartAddr=159591502088156
    req2.icache_ready = True

    # req2.icache_resp.ready = True
    req2.final_icache_resp = ICacheResp(
        itlb_pbmts=[0, 0],
        pmp_mmios=[False, False],
        exceptions=[0, 0],
        vaddrs=[1064050532637392, 1064050532637456],
        paddr=404033938,
        VS_non_leaf_PTE=True,
        data=1340603429732904944016761231998006384991999296852212916603272879707747040077396313749805960213710619513794390144730529792,
        backend_exception=False,
        double_line=0,
        gpaddr=28240919629685350,
        icache_valid=True
    )
    
    req2.bpu_flush_info.stgs["s2"].stg_valid = False
    # req2.bpu_flush_info.stgs["s2"].ftqIdx.flag = False
    # req2.bpu_flush_info.stgs["s2"].ftqIdx.value = 0
    
    req2.bpu_flush_info.stgs["s3"].stg_valid = False
    # req2.bpu_flush_info.stgs["s3"].ftqIdx.flag = False
    # req2.bpu_flush_info.stgs["s3"].ftqIdx.value = 0
    
    req2.fs_is_off=True
    # await top_agent.deal_with_non_mmio_outer(req2)   
    
    cluster: ClusteredNonMMIOReqs = ClusteredNonMMIOReqs()
    cluster.reqs.append(req1)
    res1=ifu_ref.inner_deal_with_non_mmio(req1)
    cluster.resps.append(res1)
    
    cluster.reqs.append(req1)
    res1=ifu_ref.inner_deal_with_non_mmio(req1)
    cluster.resps.append(res1)
    
    # cluster.reqs.append(req2)
    # res2=ifu_ref.inner_deal_with_non_mmio(req2)
    # cluster.resps.append(res2)
    
    
    # import copy
    # req3= copy.deepcopy(req2)
    # req3.ftq_req.ftqIdx.value += 1
    # cluster.reqs.append(req3)
    # res3=ifu_ref.inner_deal_with_non_mmio(req3)
    # cluster.resps.append(res3)
    
    # req4= copy.deepcopy(req3)
    # req4.ftq_req.ftqIdx.value += 1
    # cluster.reqs.append(req4)
    # res4=ifu_ref.inner_deal_with_non_mmio(req4)
    # cluster.resps.append(res4)
    await top_agent.deal_with_non_mmio_clusters(cluster)
    ifu_top_env.top_group.mark_function("cross_blk", test_cross_prediction_block)


# 支持多次随机的跨预测块方法
# 1. 如果发现当前last_half存在且不产生flush信号，可以直接结束生成
# 2. 如果发现当前last_half存在且无flush，若后一个非last_half，可以直接结束生成，否则继续到2的条件下判断
# 3. 如果当前last_half存在且要求flush，则
#   3.a: 重复一遍该req（保持ftq不变）
#   3.b：生成一个新的结果，然后再生成下一个结果
@toffee_test.testcase
async def test_totally_random_res(ifu_top_env):
    top_agent : OutsideAgent = ifu_top_env.top_agent
    ifu_ref: IFUReceiverModel = ifu_top_env.ifu_receiver_model
    TIMES=20000
    import time
    seed = time.time_ns()
    random.seed(seed)
    for i in range(TIMES):
        if i % 1000 == 0:
            print(f"epoch: {i}")
        STATE=0
        cluster: ClusteredNonMMIOReqs = ClusteredNonMMIOReqs()
        ifu_ref.force_flush_non_mmio_stats()
        ftq_idx: FTQIdx = FTQIdx()
        import copy
        while(True):
            if STATE == 0:
                req: NonMMIOSingleReq = NonMMIOSingleReq()
                req.randomize(randomly_choosing_finished=True, ftq_idx=copy.deepcopy(ftq_idx))
                res:NonMMIOResp = ifu_ref.inner_deal_with_non_mmio(req)
                cluster.reqs.append(req)
                cluster.resps.append(res)
                # if not res.last_half_valid:
                #     break
                if res.pin_flush:
                    # 当前未结束，且需要flush, 此时需要重新生成
                    STATE = 2
                else:
                    STATE = 1
                    if not res.last_half_valid:
                        # 只有完全合法的非跨预测块请求才能作为一次调用的结束
                        break   
            elif STATE == 1:
                # 上一个请求为last half，且合法
                # 目前几乎等同于state0
                req: NonMMIOSingleReq = NonMMIOSingleReq()
                req.randomize(randomly_choosing_finished=True, ftq_idx=copy.deepcopy(ftq_idx))
                res:NonMMIOResp = ifu_ref.inner_deal_with_non_mmio(req)
                cluster.reqs.append(req)
                cluster.resps.append(res)          
                if res.pin_flush:
                    STATE=2
                else:
                    if not res.last_half_valid:
                        # 回到状态0是因为跨预测块的请求有两种valid形态，因此这里也不能退出
                        STATE=0     
            elif STATE==2:
                choice =  random.randint(0, 99)
                if choice < 20:
                    # 上一个非法，重复请求，直接flush
                    # res: NonMMIOResp = ifu_ref.inner_deal_with_non_mmio(req)
                    # cluster.reqs.append(req)
                    # cluster.resps.append(res)
                    ifu_ref.last_half_valid = False
                    break 
                
                # 此时需要新的请求重新辅助生成
                req: NonMMIOSingleReq = NonMMIOSingleReq()
                req.randomize(ftq_idx=copy.deepcopy(ftq_idx))
                res:NonMMIOResp = ifu_ref.inner_deal_with_non_mmio(req)
                cluster.reqs.append(req)
                cluster.resps.append(res)
                STATE=0
                if res.last_half_valid:
                    # 未结束，回到状态1
                    STATE=1
                else:
                    STATE=0
            ftq_idx.inc()
        # print(cluster.reqs)
        await top_agent.deal_with_non_mmio_clusters(cluster)
        
    ifu_top_env.top_group.mark_function("gpaddr_fault", test_cross_prediction_block)
    ifu_top_env.top_group.mark_function("exception", test_cross_prediction_block)
    ifu_top_env.top_group.mark_function("cut_ptr", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("predecode_concat", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("predecode_rvc", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("predecode_jmpoff", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("predecode_brtype", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("predecode_jal_ret", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("starts", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("check_errs", test_cross_prediction_block)
    ifu_top_env.submodules_group.mark_function("rvc_expand", test_cross_prediction_block)
    
