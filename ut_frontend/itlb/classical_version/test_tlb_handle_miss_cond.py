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
from .base_components import miss_nonStage_requestor_0, miss_nonStage_requestor_1, miss_nonStage_requestor_2, \
    miss_onlyStage1_requestor_0, miss_onlyStage1_requestor_1, miss_onlyStage1_requestor_2, miss_onlyStage2_requestor_0, \
    miss_onlyStage2_requestor_1, miss_onlyStage2_requestor_2, miss_allStage_requestor_0, miss_allStage_requestor_1, \
    miss_allStage_requestor_2
from .env import *
import inspect

ROUND_NUM = 2
ROUND_SIZE = 2


def test_handle_miss_cond_miss(tlb_fixture):
    """
    no stage，miss
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    # no stage
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_nonStage_requestor_0(tlb)
        tlb.cleanup_requestor(0)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_nonStage_requestor_1(tlb)
        tlb.cleanup_requestor(1)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_nonStage_requestor_2(tlb)
            tlb.cleanup_requestor(2)  # cleanup requestor 2 after each missing

    # only stage 1
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_onlyStage1_requestor_0(tlb)
        tlb.cleanup_requestor(0)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_onlyStage1_requestor_1(tlb)
        tlb.cleanup_requestor(1)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_onlyStage1_requestor_2(tlb)
            tlb.cleanup_requestor(2)  # cleanup requestor 2 after each missing

    # only stage 2
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_onlyStage2_requestor_0(tlb)
        tlb.cleanup_requestor(0)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_onlyStage2_requestor_1(tlb)
        tlb.cleanup_requestor(1)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_onlyStage2_requestor_2(tlb)
            tlb.cleanup_requestor(2)  # cleanup requestor 2 after each missing

    # all stage
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_allStage_requestor_0(tlb)
        tlb.cleanup_requestor(0)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_allStage_requestor_1(tlb)
        tlb.cleanup_requestor(1)
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            miss_allStage_requestor_2(tlb)
            tlb.cleanup_requestor(2)  # cleanup requestor 2 after each missing


def test_handle_miss_cond_ptw_req(tlb_fixture):
    """
    no stage，miss
    """
    # connect to fixture
    tlb = tlb_fixture
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())

    # no stage
    for _ in range(ROUND_NUM):
        for _ in range(ROUND_SIZE):
            signals = miss_nonStage_requestor_0(tlb)
            assert(tlb.ctrl.io_ptw_req_0_valid.value == 1)
            assert(tlb.ptw_req_0.vpn.value == signals["vpn"])
            # simulate PTW invalid
            ppn, _ = tlb.gene_rand_addr()
            tlb.ctrl.io_ptw_resp_valid.value = 0
            tlb.ptw_resp_s1.entry_ppn.value = ppn
            tlb.ptw_resp_s1.entry_tag.value = signals["vpn"]
            tlb.dut.Step()
            # should miss when reading second time
            tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
            tlb.dut.Step(2)
            assert (tlb.requestor_0.resp.miss.value == 1)
            tlb.cleanup_requestor(0)
