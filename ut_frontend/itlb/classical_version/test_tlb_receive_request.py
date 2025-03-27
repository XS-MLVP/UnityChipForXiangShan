#coding=utf8
#***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
#**************************************************************************************/

from .env import *
import inspect

### CASE EXAMPLE
# Running the following test case will show a pass:
#     In this test case, a single port (Requestor0) sends an address translation 
# request to TLB. TLB is expected to return a miss in the next cycle and initiate 
# a request to the PTW. At this point, you can simultaneously verify whether the 
# vpn in the PTW request is correct.
def test_req_from_ifu_and_icache_rand_vaddr_rand_valid_single_port(tlb_fixture):
    """
    Func: Compare the PTW request with the reference:
        subfunc1: rand vaddr
        subfunc2: rand valid
        subfunc3: single port 0 / 1 / 2
    """
    # connect to fixture
    tlb = tlb_fixture
    # add watch point
    case_name = inspect.currentframe().f_back.f_code.co_name
    g.add_watch_point(tlb.requestor_0.resp.miss, {
                        "miss": fc.Eq(1),
                        "hit": fc.Eq(0),
    }, name = f"{case_name}: REQUESTOR_0_MISS")
    g.add_watch_point(tlb.requestor_1.resp.miss, {
                        "miss": fc.Eq(1),
                        "hit": fc.Eq(0),
    }, name = f"{case_name}: REQUESTOR_1_MISS")
    g.add_watch_point(tlb.ctrl.io_ptw_req_0_valid, {
                        "valid": fc.Eq(1),
                        "invalid": fc.Eq(0),
    }, name = f"{case_name}: PTW_REQ_0_VALID")
    g.add_watch_point(tlb.ctrl.io_ptw_req_1_valid, {
                        "valid": fc.Eq(1),
                        "invalid": fc.Eq(0),
    }, name = f"{case_name}: PTW_REQ_1_VALID")
    # set default value
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(10000):
        # add signal and assign to dut
        req_0_valid, req_0_vaddr = tlb.rand_req0()
        # step to next cycle
        tlb.dut.Step(2)
        
        # assert result
        assert (tlb.ctrl.io_ptw_req_0_valid.value == req_0_valid)
        if (req_0_valid):
            assert (tlb.ptw_req_0.vpn.value == req_0_vaddr >> 12)
    #################################### TODO EXAMPLE ####################################
    # TODO: Add Requestor1 Verification
    #     The existing test case provides verification methods for sending TLB requests 
    # from requestor0. Now, we need to verify whether sending TLB requests from requestor1 
    # also meets the expected behavior. Modify the test case such that in each cycle, a 
    # TLB request is sent from either requestor0 or requestor1, with strict attention to 
    # ensuring that both ports are not active simultaneously.
    for _ in range(10000):
        # add signal and assign to dut
        req_1_valid, req_1_vaddr = tlb.rand_req1()
        # step to next cycle
        tlb.dut.Step(2)
        
        # assert result
        assert (tlb.ctrl.io_ptw_req_1_valid.value == req_1_valid)
        if (req_1_valid):
            assert (tlb.ptw_req_1.vpn.value == req_1_vaddr >> 12)
    ######################################################################################
    ######################################################################################
    # TODO: Add Requestor2 Verification (Critical Differences)
    #     Requestor2 uses BLOCKING access protocol (vs. Non-blocking on 0/1)
    ######################################################################################

### CASE EXAMPLE
# Running the following test case will show a pass:
def test_req_from_icache_rand_vaddr_rand_valid_muti_port(tlb_fixture):
    """
    Func: compare the PTW request with the reference:
        subfunc1: rand vaddr
        subfunc2: rand valid
        subfunc3: muti port 0 & 1
    """
    # connect to fixture
    tlb = tlb_fixture
    # add watch point
    case_name = inspect.currentframe().f_back.f_code.co_name
    g.add_watch_point(tlb.requestor_0.resp.miss, {
                        "miss": fc.Eq(1),
                        "hit": fc.Eq(0),
    }, name = f"{case_name}: REQUESTOR_0_MISS")
    g.add_watch_point(tlb.requestor_1.resp.miss, {
                        "miss": fc.Eq(1),
                        "hit": fc.Eq(0),
    }, name = f"{case_name}: REQUESTOR_1_MISS")
    g.add_watch_point(tlb.ctrl.io_ptw_req_0_valid, {
                        "valid": fc.Eq(1),
                        "invalid": fc.Eq(0),
    }, name = f"{case_name}: PTW_REQ_0_VALID")
    g.add_watch_point(tlb.ctrl.io_ptw_req_1_valid, {
                        "valid": fc.Eq(1),
                        "invalid": fc.Eq(0),
    }, name = f"{case_name}: PTW_REQ_1_VALID")
    # set default value
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(10000):
        # add signal and assign to dut
        req_0_valid, req_0_vaddr = tlb.rand_req0()
        req_1_valid, req_1_vaddr = tlb.rand_req1()
        # step to next cycle
        tlb.dut.Step(2)
        
        # assert result
        assert (tlb.ctrl.io_ptw_req_0_valid.value == req_0_valid)
        assert (tlb.ctrl.io_ptw_req_1_valid.value == req_1_valid)
        if (req_0_valid):
            assert (tlb.ptw_req_0.vpn.value == req_0_vaddr >> 12)
        if (req_1_valid):
            assert (tlb.ptw_req_1.vpn.value == req_1_vaddr >> 12)