import toffee
import os
import pytest
import ctypes
import datetime
import toffee.funcov as fc

from dut.LoadQueueRAR import *

from comm import get_out_dir, get_root_dir, debug, UT_FCOV, get_file_logger, get_version_checker, module_name_with

from toffee_test.reporter import set_func_coverage
from toffee_test.reporter import set_line_coverage

g = fc.CovGroup(UT_FCOV("../../Group-A"))

def init_rar_funcov(rarqueue, g: fc.CovGroup):
    g.add_watch_point(rarqueue.io_query_0_req_ready_0, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        "can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_0")
    g.add_watch_point(rarqueue.io_query_1_req_ready_0, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        "can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_1")
    g.add_watch_point(rarqueue.io_query_2_req_ready_0, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        "can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_2")
    
    # for i in range(72): #需要跨时钟周期进行检查，需放入test中自定义检查函数 for Dequeue
    #     signal_name = f"LoadQueueRAR_allocated_{i}"  # 构造信号名称
    #     signal_name2 = f"LoadQueueRAR_allocated_{i}"
    #     g.add_watch_point(rarqueue,{
    #             "check dequeue": lambda x: x[f"{signal_name}"] ==  ,
    #         } , name=f"check_{signal_name}")
            
    g.add_watch_point(rarqueue.io_query_0_resp_bits_rep_frm_fetch,
                      {
                          "have ld-ld violation": lambda x: x.value > 0,
                          "don't have ld-ld voilation": lambda x: x.value ==0,
                      }, name = "QUERY_0")
    g.add_watch_point(rarqueue.io_query_0_resp_bits_rep_frm_fetch,
                      {
                          "have ld-ld violation": lambda x: x.value > 0,
                          "don't have ld-ld voilation": lambda x: x.value ==0,
                      }, name = "QUERY_1")
    g.add_watch_point(rarqueue.io_query_0_resp_bits_rep_frm_fetch,
                      {
                          "have ld-ld violation": lambda x: x.value > 0,
                          "don't have ld-ld voilation": lambda x: x.value == 0,
                      }, name = "QUERY_2")
    g.add_watch_point(rarqueue.io_release,
                      {
                          "released update": lambda x: x.value > 0,
                          "don't need update": lambda x:x.value == 0,
                      }, name = "CHECK_RELEASED")
    g.add_watch_point(rarqueue.io_query_0_revoke,
                      {
                          "need revoke": lambda x: x.value > 0,
                      }, name = "CHECK_REVOKE")
    g.add_watch_point(rarqueue.io_lqFull,
                      {
                          "queue is full": lambda x: x.value > 0,
                          "queue is not full": lambda x: x.value == 0,
                      }, name = "CHECK_FULL")
    # The End
    return None

class LoadQueueRAR(toffee.Bundle):
    def __init__(self, cover_group, **kwargs):
        super().__init__()
        self.cover_group = cover_group
        self.dut = DUTLoadQueueRAR(**kwargs) # 创建DUT
        self.full = toffee.Bundle.from_prefix("io_", self.dut) # 通过 Bundle 关联引脚
        self.redirect = toffee.Bundle.from_prefix("io_redirect_", self.dut)
        self.vecFeedback = toffee.Bundle.from_prefix("io_vecFeedback_", self.dut)
        self.req = [toffee.Bundle.from_prefix(f"io_query_{i}_req_", self.dut) for i in range(3)]
        self.resp = [toffee.Bundle.from_prefix(f"io_query_{i}_resp_", self.dut) for i in range(3)]
        self.revoke = [toffee.Bundle.from_prefix(f"io_query_{i}_", self.dut) for i in range(3)]
        self.release = toffee.Bundle.from_prefix("io_release_", self.dut)
        self.ldWbPtr = toffee.Bundle.from_prefix("io_ldWbPtr_", self.dut)
        self.inner = toffee.Bundle.from_prefix("LoadQueueRAR_",self.dut)
        self.bind(self.dut)  # 把 Bunldle 与 DUT 进行绑定
        
    def Enqueue(self, query, redirect, ldWbPtr):
        self.req["valid"].value = query.req.valid # 给dut引脚赋值
        self.req["bits_uop_lqIdx_flag"].value = query.req.bits.uop.lqIdx.flag
        self.req["bits_uop_lqIdx_value"].value = query.req.bits.uop.lqIdx.value
        self.req["ready"].value = query.req.ready
        self.req["bits_uop_robIdx_flag"].value = query.req.bits.uop.robIdx.flag
        self.req["bits_uop_robIdx_value"].value = query.req.bits.uop.robIdx.value
        self.req["bits_paddr"].value = query.req.bits.paddr
        # self.resp = query.resp
        self.revoke["revoke"].value = query.revoke
        self.redirect["valid"].value = redirect.valid
        self.redirect["bits_robIdx_flag"].value = redirect.bits.robIdx.flag
        self.redirect["bits_robIdx_value"].value = redirect.bits.robIdx.value
        self.redirect["bits_level"].value = redirect.bits.level
        self.ldWbPtr["flag"].value = ldWbPtr.flag
        self.ldWbPtr["value"].value = ldWbPtr.value
        self.dut.Step(1) # 推动电路
        self.cover_group.sample()  # 调用sample对功能覆盖率进行统计
        return self.inner
        
        
    def Dequeue(self, ldWbPtr, redirect, vecFeedback, release):
        self.ldWbPtr["flag"].value = ldWbPtr.flag
        self.ldWbPtr["value"].value = ldWbPtr.value
        self.redirect["valid"].value = redirect.valid
        self.redirect["bits_robIdx_flag"].value = redirect.bits.robIdx.flag
        self.redirect["bits_robIdx_value"].value = redirect.bits.robIdx.value
        self.redirect["bits_level"].value = redirect.bits.level
        self.vecFeedback["valid"].value = vecFeedback.valid
        self.vecFeedback["bits_robidx_flag"].value = vecFeedback.bits.robidx.flag
        self.vecFeedback["bits_robidx_value"].value = vecFeedback.bits.robidx.value
        self.vecFeedback["bits_uopidx"].value = vecFeedback.bits.uopidx
        self.vecFeedback["bits_feedback_0"].value = vecFeedback.bits.feedback_0
        self.release["valid"].value = release.valid
        self.release["bits_paddr"].value = release.bits.paddr
        self.dut.Step(1)
        self.cover_group.sample()
        return self.inner
        
    def detect(self, query):
        self.req["valid"].value = query.req.valid
        self.req["bits_uop_lqIdx_flag"].value = query.req.bits.uop.lqIdx.flag
        self.req["bits_uop_lqIdx_value"].value = query.req.bits.uop.lqIdx.value
        self.req["ready"].value = query.req.ready
        self.req["bits_uop_robIdx_flag"].value = query.req.bits.uop.robIdx.flag
        self.req["bits_uop_robIdx_value"].value = query.req.bits.uop.robIdx.value
        self.req["bits_paddr"].value = query.req.bits.paddr
        self.revoke["revoke"].value = query.revoke
        self.dut.Step(1)
        self.cover_group.sample()
        return (self.resp, self.inner)
        
    def releasedupdate(self, release):
        self.release["valid"].value = release.valid
        self.release["bits_paddr"].value = release.bits.paddr
        return self.inner
    
    def revoke(self, query):
        self.revoke["revoke"].value = query.revoke
        return self.inner