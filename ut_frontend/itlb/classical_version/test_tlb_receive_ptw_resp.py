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
            assert(tlb.requestor_0.resp.paddr_0.value == ((ppn << 12) | offset))
            assert(tlb.requestor_0.resp.miss.value == 0)
        # reset
        tlb.reset()


def test_receive_ptw_resp_nonstage_single_hit(tlb_fixture):
    """
    no stage，单次miss
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    ################################################################################
    # requestor_0
    ################################################################################
    # generate signals
    signals = _gen_signal_rand()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # check whether PTW resp is stored
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_0.resp.miss.value == 0)

    ################################################################################
    # requestor_1
    ################################################################################
    # generate signals
    signals = _gen_signal_rand()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # check whether PTW resp is stored
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_1.resp.miss.value == 0)


def test_receive_ptw_resp_nonstage_single_miss(tlb_fixture):
    """
    no stage，单次miss
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    ################################################################################
    # requestor_0
    ################################################################################
    # generate signals
    signals = _gen_signal_rand()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # check whether PTW resp is stored
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.miss.value == 1)

    ################################################################################
    # requestor_1
    ################################################################################
    # generate signals
    signals = _gen_signal_rand()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # check whether PTW resp is stored
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.miss.value == 1)


def _gen_signal_rand() -> dict:
    vaddr = random.randint(0, 2 ** 50 - 1)
    asid = random.randint(0, 2 ** 16 - 1)
    vpn = vaddr >> 12
    offset = vaddr & 0xfff
    ppn = random.randint(0, 2 ** 36 - 1)
    ppn_low = [random.randint(0, 2 ** 3 - 1) for _ in range(8)]
    valid_idx = [random.choice([0, 1]) for _ in range(8)]
    return {
        "asid": asid,
        "vpn": vpn,
        "offset": offset,
        "ppn": ppn,
        "ppn_low": ppn_low,
        "valid_idx": valid_idx,
    }