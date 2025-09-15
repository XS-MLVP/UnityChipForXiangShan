# coding=utf8
# ***************************************************************************************
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
# **************************************************************************************/

from .env import *


### CASE EXAMPLE
# Running the following test case will show a pass:
@pytest.mark.skip
def test_receive_ptw_resp_nonstage(tlb_fixture):
    """
    Func: receive PTW response under nonstage condition and stored it into TLB entry
        subfunc1: TODO
    """
    # connect to fixture
    tlb = tlb_fixture
    # add watch point
    # case_name = inspect.currentframe().f_back.f_code.co_name
    # g.add_watch_point(tlb.TODO, {
    #                     "TODO": fc.Eq(TODO),
    #                     "TODO": lambda TODO: TODO.value == TODO,
    # }, name = f"{case_name}: TODO")
    # set default value
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(1000):
        for _ in range(30):
            # add signal and assign to dut
            vaddr = random.randint(0, 2 ** 50 - 1)
            asid = random.randint(0, 2 ** 16 - 1)
            vpn = vaddr >> 12
            offset = vaddr & 0xfff
            s2xlate = 0b00
            ppn = tlb.rand_ptw_resp(vpn, asid, s2xlate)

            tlb.csr.satp.asid.value = asid

            # step to next cycle
            tlb.dut.Step()

            # check whether PTW resp is stored
            tlb.requestor_0.req.valid.value = 1
            tlb.requestor_0.req.bits_vaddr.value = (vpn << 12) | offset

            # step to next cycle
            tlb.dut.Step(2)

            # assert result
            assert (tlb.requestor_0.resp.paddr_0.value == ((ppn << 12) | offset))
            assert (tlb.requestor_0.resp.miss.value == 0)
        # reset
        tlb.reset()
