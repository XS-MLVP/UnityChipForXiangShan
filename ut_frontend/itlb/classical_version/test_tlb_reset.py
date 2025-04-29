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
# Running this test case will report a BUG:
#     The reset function fails. When a TLB request is initiated simultaneously 
# with a reset, it is observed that all signals are not properly reset. After 
# the reset ends, TLB will send a request to PTW while returning a miss to the 
# upper-level module.
# 
# NOTE: This test case is solely intended to demonstrate the scenario where 
# the bug occurs. In practice, initiating a request (req) simultaneously with 
# a reset signal constitutes an invalid input and violates the protocol 
# specification.
def reset_when_request(tlb_fixture):
    """
    Check reset
        Request & reset in the same cycle
    """
    # connect to fixture
    tlb = tlb_fixture
    # add watch point
    case_name = inspect.currentframe().f_back.f_code.co_name
    g.add_watch_point(tlb.ctrl.reset, {
                        "reset": fc.Eq(1),
                        "notreset": fc.Eq(0),
    }, name = f"{case_name}: RESET")
    # set default value
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(10000):
        # add signal and assign to dut
        _, _, _, _, _, _ = tlb.rand_req()
        tlb.ctrl.reset.value = 1

        # step to next cycle
        tlb.dut.Step(10)

        # add signal and assign to dut
        tlb.ctrl.reset.value = 0
        # step to next cycle
        tlb.dut.Step(5)

        # assert result
        assert (tlb.requestor_0.resp.miss.value == 0)
        assert (tlb.requestor_1.resp.miss.value == 0)
        assert (tlb.ctrl.io_ptw_req_0_valid.value == 0)
        assert (tlb.ctrl.io_ptw_req_1_valid.value == 0)