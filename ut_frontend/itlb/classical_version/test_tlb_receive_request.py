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

# test example
def test_req_from_icache_min_vaddr(tlb_fixture):
    # connect to fixture
    tlb = tlb_fixture
    # reset
    tlb.reset()
    # set default value
    tlb.set_default_value()
    # add function point
    g.add_watch_point(tlb.ptw_req_0.vpn, 
                          {"ptw_req_0_vpn_1": toffee.funcov.Eq(0)}, name = "ptw_req_0_vpn_1")
    g.add_watch_point(tlb.ptw_req_1.vpn, 
                          {"ptw_req_1_vpn_1": toffee.funcov.Eq(0)}, name = "ptw_req_1_vpn_1")

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(1000):
        # add signal
        req_0_valid = random.choice([0, 1])
        req_1_valid = 1 - req_0_valid
        req_0_vaddr = 0
        req_1_vaddr = 0

        # assign to dut
        tlb.requestor_0.req.valid.value = req_0_valid
        tlb.requestor_1.req.valid.value = req_1_valid
        tlb.requestor_0.req.bits_vaddr.value = req_0_vaddr
        tlb.requestor_1.req.bits_vaddr.value = req_1_vaddr
        # step to next cycle
        tlb.dut.Step(2)
        
        # assert result
        assert (tlb.ctrl.io_ptw_req_0_valid.value == req_0_valid)
        assert (tlb.ctrl.io_ptw_req_1_valid.value == req_1_valid)
        if (req_0_valid):
            assert (tlb.ptw_req_0.vpn.value == req_0_vaddr >> 12)
        if (req_1_valid):
            assert (tlb.ptw_req_1.vpn.value == req_1_vaddr >> 12)