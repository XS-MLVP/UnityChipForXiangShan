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

ROUND_NUM = 1000
ROUND_SIZE = 30

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


def test_receive_ptw_resp_nonstage_single_hit_icache(tlb_fixture):
    """
    no stage，单次hit
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_hit_requestor_0(tlb)
        tlb.cleanup_requestor(0)

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_hit_requestor_1(tlb)
        tlb.cleanup_requestor(1)


def test_receive_ptw_resp_nonstage_single_hit_ifu(tlb_fixture):
    """
    no stage，单次hit
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_hit_requestor_2(tlb)
        tlb.cleanup_requestor(2)


def _do_test_receive_ptw_resp_nonstage_hit_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_0.resp.miss.value == 0)


def _do_test_receive_ptw_resp_nonstage_hit_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_1.resp.miss.value == 0)


def _do_test_receive_ptw_resp_nonstage_hit_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_2.resp.miss.value == 0)


def test_receive_ptw_resp_nonstage_single_miss_icache(tlb_fixture):
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

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_miss_requestor_0(tlb)
        tlb.cleanup_requestor(0)

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_miss_requestor_1(tlb)
        tlb.cleanup_requestor(1)


def test_receive_ptw_resp_nonstage_single_miss_ifu(tlb_fixture):
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

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_miss_requestor_2(tlb)
            tlb.cleanup_requestor(2)  # cleanup requestor 2 after each missing


def _do_test_receive_ptw_resp_nonstage_miss_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.miss.value == 1)


def _do_test_receive_ptw_resp_nonstage_miss_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.miss.value == 1)


def _do_test_receive_ptw_resp_nonstage_miss_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.miss.value == 1)


def test_receive_ptw_resp_nonstage_valid_icache(tlb_fixture):
    """
    no stage，valid有效性
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_valid_requestor_0(tlb)
            tlb.cleanup_requestor(0)
            _do_test_receive_ptw_resp_nonstage_invalid_requestor_0(tlb)
            tlb.cleanup_requestor(0)

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_valid_requestor_1(tlb)
            tlb.cleanup_requestor(1)
            _do_test_receive_ptw_resp_nonstage_invalid_requestor_1(tlb)
            tlb.cleanup_requestor(1)


def test_receive_ptw_resp_nonstage_valid_ifu(tlb_fixture):
    """
    no stage，valid-ready有效性
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            _do_test_receive_ptw_resp_nonstage_valid_ready_requestor_2(tlb)
            tlb.cleanup_requestor(2)
            _do_test_receive_ptw_resp_nonstage_invalid_ready_requestor_2(tlb)
            tlb.cleanup_requestor(2)
            _do_test_receive_ptw_resp_nonstage_valid_busy_requestor_2(tlb)
            tlb.cleanup_requestor(2)
            _do_test_receive_ptw_resp_nonstage_invalid_busy_requestor_2(tlb)
            tlb.cleanup_requestor(2)


def _do_test_receive_ptw_resp_nonstage_valid_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_0.resp.miss.value == 0)


def _do_test_receive_ptw_resp_nonstage_invalid_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result, no hit anyway
    assert not (tlb.requestor_0.resp.miss.value == 0 and
                tlb.requestor_0.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))


def _do_test_receive_ptw_resp_nonstage_valid_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_1.resp.miss.value == 0)


def _do_test_receive_ptw_resp_nonstage_invalid_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result, no hit anyway
    assert not (tlb.requestor_1.resp.miss.value == 0 and
                tlb.requestor_1.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))


def _do_test_receive_ptw_resp_nonstage_valid_ready_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_2.resp.miss.value == 0)


def _do_test_receive_ptw_resp_nonstage_invalid_ready_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result, no hit anyway
    assert not (tlb.requestor_2.resp.miss.value == 0 and
                tlb.requestor_2.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))


def _do_test_receive_ptw_resp_nonstage_valid_busy_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 0
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result, no hit anyway
    assert not (tlb.requestor_2.resp.miss.value == 0 and
                tlb.requestor_2.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))


def _do_test_receive_ptw_resp_nonstage_invalid_busy_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.ctrl.io_requestor_2_resp_ready.value = 0
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result, no hit anyway
    assert not (tlb.requestor_2.resp.miss.value == 0 and
                tlb.requestor_2.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
