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