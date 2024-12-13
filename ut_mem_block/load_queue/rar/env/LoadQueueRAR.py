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

from ut_mem_block.load_queue.rar.env import InnerBundle
from ut_mem_block.load_queue.rar.env.Bundle import *

g = fc.CovGroup(UT_FCOV("../../Group-A"))

def init_rar_funcov(rarqueue, g: fc.CovGroup):
    g.add_watch_point(rarqueue.req_0.ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_0")
    g.add_watch_point(rarqueue.req_1.ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_1")
    g.add_watch_point(rarqueue.req_2.ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_2")
    
    # for i in range(72): #需要跨时钟周期进行检查，需放入test中自定义检查函数 for Dequeue
    #     signal_name = f"LoadQueueRAR_allocated_{i}"  # 构造信号名称
    #     signal_name2 = f"LoadQueueRAR_allocated_{i}"
    #     g.add_watch_point(rarqueue,{
    #             "check dequeue": lambda x: x[f"{signal_name}"] ==  ,
    #         } , name=f"check_{signal_name}")
            
    # g.add_watch_point(rarqueue.io_query_0_resp_bits_rep_frm_fetch,
    #                   {
    #                       "have ld-ld violation": lambda x: x.value > 0,
    #                       "don't have ld-ld voilation": lambda x: x.value ==0,
    #                   }, name = "QUERY_0")
    # g.add_watch_point(rarqueue.io_query_0_resp_bits_rep_frm_fetch,
    #                   {
    #                       "have ld-ld violation": lambda x: x.value > 0,
    #                       "don't have ld-ld voilation": lambda x: x.value ==0,
    #                   }, name = "QUERY_1")
    # g.add_watch_point(rarqueue.io_query_0_resp_bits_rep_frm_fetch,
    #                   {
    #                       "have ld-ld violation": lambda x: x.value > 0,
    #                       "don't have ld-ld voilation": lambda x: x.value == 0,
    #                   }, name = "QUERY_2")
    # g.add_watch_point(rarqueue.io_release,
    #                   {
    #                       "released update": lambda x: x.value > 0,
    #                       "don't need update": lambda x: x.value == 0,
    #                   }, name = "CHECK_RELEASED")
    # g.add_watch_point(rarqueue.io_query_0_revoke,
    #                   {
    #                       "need revoke": lambda x: x.value > 0,
    #                   }, name = "CHECK_REVOKE")
    # g.add_watch_point(rarqueue.io_lqFull,
    #                   {
    #                       "queue is full": lambda x: x.value > 0,
    #                       "queue is not full": lambda x: x.value == 0,
    #                   }, name = "CHECK_FULL")
    def _M(name):
        # get the module name
        return module_name_with(name, "../../test_queueupdate")
    
    g.mark_function("RAR_ENQUEUE_0", _M("test_can_enqueue_smoke"), bin_name=["can receive violation query"])
    g.mark_function("RAR_ENQUEUE_1", _M("test_can_enqueue_smoke"), bin_name=["can receive violation query"])
    g.mark_function("RAR_ENQUEUE_2", _M("test_can_enqueue_smoke"), bin_name=["can receive violation query"])
    # The End
    return None

# version_check = get_version_checker("openxiangshan-kmh-*")             # 指定满足要的RTL版本
@pytest.fixture(scope="module")
def rar_queue(request):
    # version_check()                                                    # 进行版本检查
    fname = request.node.name                                          # 获取调用该fixture的测试用例
    wave_file = get_out_dir("load_queue/rar/rar_%s.fst" % fname)     # 设置波形文件路径
    coverage_file = get_out_dir("load_queue/rar/rar_%s.dat" % fname) # 设置代码覆盖率文件路径
    coverage_dir = os.path.dirname(coverage_file)
    os.makedirs(coverage_dir, exist_ok=True)                           # 目标目录不在则创建目录
    rarqueue = LoadQueueRAR(g, coverage_filename=coverage_file, waveform_filename=wave_file)  # 创建LoadQueueRAR
    # print("LLLLLLLL",rarqueue.revoke_0)
    init_rar_funcov(rarqueue, g)                              # 初始化功能检查点
    rarqueue.dut.InitClock("clock")
    yield rarqueue                                                    # 返回创建好的 RVCExpander 给 Test Case
    rarqueue.dut.Finish()                                              # Tests Case运行完成后，结束DUT
    set_line_coverage(request, coverage_file)                          # 把生成的代码覆盖率文件告诉 toffee-report
    set_func_coverage(request, g)                                      # 把生成的功能覆盖率数据告诉 toffee-report
    g.clear()                                                          # 清空功能覆盖统计
    

class LoadQueueRAR(toffee.Bundle):
    def __init__(self, cover_group, **kwargs):
        super().__init__()
        self.cover_group = cover_group
        self.diff = 0
        self.dut = DUTLoadQueueRAR(**kwargs) # 创建DUT
        self.full = FullBundle.from_dict({'lqFull':'io_lqFull'}) # 通过 Bundle 关联引脚
        self.redirect = ControlRedirectBundle.from_prefix("io_redirect_", self.dut)
        for i in range(2):
            setattr(self, f"vecFeedback_{i}", ControlvecFeedbackBundle.from_prefix(f"io_vecFeedback_{i}_", self.dut))
        for i in range(3):
            setattr(self, f"req_{i}", QueryReqBundle.from_prefix(f"io_query_{i}_req_", self.dut))
            setattr(self, f"resp_{i}", QueryRespBundle.from_prefix(f"io_query_{i}_resp_", self.dut))
        setattr(self, f"revoke_0", QueryRevokeBundle.from_dict({'revoke':'io_query_0_revoke'}))
        setattr(self, f"revoke_1", QueryRevokeBundle.from_dict({'revoke':'io_query_1_revoke'}))
        setattr(self, f"revoke_2", QueryRevokeBundle.from_dict({'revoke':'io_query_2_revoke'}))
        self.release = ReleaseBundle.from_prefix("io_release_", self.dut)
        self.ldWbPtr = WritebackBundle.from_prefix("io_ldWbPtr_", self.dut)
        self.inner = InnerBundle.Bundle.from_prefix("LoadQueueRAR_",self.dut)
        self.bind(self.dut)  # 把 Bundle 与 DUT 进行绑定
        
    def Enqueue(self, query, redirect, ldWbPtr):
        binary_query = bin(query)[2:]
        num_query = binary_query.ljust(234, '0')
        binary_redirect = bin(redirect)[2:]
        num_redirect = binary_redirect.ljust(11, '0')
        binary_ldWbPtr = bin(ldWbPtr)[2:]
        num_ldWbPtr = binary_ldWbPtr.ljust(8, '0')
        for i in range(3):
            req = getattr(self, f'req_{i}')
            revoke = getattr(self, f'revoke_{i}')
            req["valid"].value = int(num_query[1 + i*78]) # 给dut引脚赋值，没有输出了，从这里就开始有问题
            req["bits_uop_lqIdx_flag"].value = int(num_query[18+i*78])
            req["bits_uop_lqIdx_value"].value = int(num_query[19+i*78:26+i*78],2)
            # self.req[i]["ready"].value = int(num_query[0 + i*78])
            req["bits_uop_robIdx_flag"].value = int(num_query[9+i*78])
            req["bits_uop_robIdx_value"].value = int(num_query[10+i*78:18+i*78],2)
            req["bits_paddr"].value = int(num_query[26+i*78: 74+i*78],2) #有问题，会报错，需修改
            # self.resp = query.resp
            revoke["revoke"].value = int(num_query[77+i*78])
        self.redirect["valid"].value = int(str(num_redirect)[0])
        self.redirect["bits_robIdx_flag"].value = int(str(num_redirect)[1])
        self.redirect["bits_robIdx_value"].value = int(str(num_redirect)[2:10])
        self.redirect["bits_level"].value = int(str(num_redirect)[10])
        self.ldWbPtr["flag"].value = int(str(num_ldWbPtr)[0])
        self.ldWbPtr["value"].value = int(str(num_ldWbPtr)[1:8])
        self.dut.Step(1) # 推动电路
        self.cover_group.sample()  # 调用sample对功能覆盖率进行统计
        return self.req_0, self.inner
        
        
    def Dequeue(self, ldWbPtr, redirect, vecFeedback, release):
        binary_redirect = bin(redirect)[2:]
        num_redirect = binary_redirect.ljust(11, '0')
        binary_ldWbPtr = bin(ldWbPtr)[2:]
        num_ldWbPtr = binary_ldWbPtr.ljust(8, '0')
        binary_vecFeedback = bin(vecFeedback)[2:]
        num_vecFeedback = binary_vecFeedback.ljust(36, '0')
        binary_release = bin(release)[2:]
        num_release = binary_release.ljust(49, '0')
        self.ldWbPtr["flag"].value = int(str(num_ldWbPtr)[0])
        self.ldWbPtr["value"].value = int(str(num_ldWbPtr)[1:8])
        self.redirect["valid"].value = int(str(num_redirect)[0])
        self.redirect["bits_robIdx_flag"].value = int(str(num_redirect)[1])
        self.redirect["bits_robIdx_value"].value = int(str(num_redirect)[2:10])
        self.redirect["bits_level"].value = int(str(num_redirect)[10])
        for i in range(2):
            vecFeedback_temp = getattr(self, f'vecFeedback_{i}')
            vecFeedback_temp["valid"].value = int(num_vecFeedback[0 + i*18]) # 给dut引脚赋值，没有输出了，从这里就开始有问题
            vecFeedback_temp["bits_robidx_flag"].value = int(num_vecFeedback[1+i*18])
            vecFeedback_temp["bits_robidx_value"].value = int(num_vecFeedback[2+i*18:10+i*18],2)
            vecFeedback_temp["bits_uopidx"].value = int(num_vecFeedback[10+i*18:17+i*18],2)
            vecFeedback_temp["bits_feedback_0"].value = int(num_vecFeedback[17+i*18],2)
        self.release["valid"].value = int(num_release[0])
        self.release["bits_paddr"].value = int(num_release[1:48],2)
        self.dut.Step(1)
        self.cover_group.sample()
        return self.inner
        
    def detect(self, query):
        binary_query = bin(query)[2:]
        num_query = binary_query.ljust(234, '0')
        for i in range(3):
            req = getattr(self, f'req_{i}')
            revoke = getattr(self, f'revoke_{i}')
            req["valid"].value = int(num_query[1 + i*78]) # 给dut引脚赋值，没有输出了，从这里就开始有问题
            req["bits_uop_lqIdx_flag"].value = int(num_query[18+i*78])
            req["bits_uop_lqIdx_value"].value = int(num_query[19+i*78:26+i*78],2)
            # self.req[i]["ready"].value = int(num_query[0 + i*78])
            req["bits_uop_robIdx_flag"].value = int(num_query[9+i*78])
            req["bits_uop_robIdx_value"].value = int(num_query[10+i*78:18+i*78],2)
            req["bits_paddr"].value = int(num_query[26+i*78: 74+i*78],2) #有问题，会报错，需修改
            # self.resp = query.resp
            revoke["revoke"].value = int(num_query[77+i*78])
        self.dut.Step(1)
        self.cover_group.sample()
        return (self.resp, self.inner)
        
    def releasedupdate(self, release):
        binary_release = bin(release)[2:]
        num_release = binary_release.ljust(49, '0')
        self.release["valid"].value = int(num_release[0])
        self.release["bits_paddr"].value = int(num_release[1:48],2)
        return self.inner
    
    def revoke(self, query):
        binary_query = bin(query)[2:]
        num_query = binary_query.ljust(234, '0')
        for i in range(3):
            revoke = getattr(self, f'revoke_{i}')
            revoke["revoke"].value = int(num_query[77+i*78])
        return self.inner
    
    # def reset(self):

