"""
    Test for alternative prediction
    Author: yzcc
"""

import toffee_test
from random import randint
from toffee import CovGroup

from dut.ITTage import DUTITTage
from ..util.common import UpdateReq
from ..util.meta_parser import MetaParser

from .chk_helper import get_cov_grp_of_alt_pred
from ..env.ittage_wrapper import ITTageWrapper


def test_alt_pred(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper
    # Start
    pins.xclock.Step(1000)

    # Test: use T1~T4 as alt_pred
    for tab in range(4):
        pc = tab * 4

        # Alloc Longest
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        pred_target = dut_output["pred0"]["jalr_target"]

        meta_wrap.allocate_bits = 4
        req = UpdateReq(pc, meta_wrap.value, pred_target + randint(1, 0x114514), 0, 1)
        pins.update(req.asdict())
        pins.xclock.Step(10)

        # Alloc Second Longest
        meta_wrap.allocate_bits = tab
        req = UpdateReq(pc, meta_wrap.value, pred_target + randint(1, 0x114514), 0, 1)
        pins.update(req.asdict())
        pins.xclock.Step(10)

        # Set longest to unconfident
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        pred_target = dut_output["pred0"]["jalr_target"]

        meta_wrap.provided = 1
        meta_wrap.provider = 4
        meta_wrap.providerCtr = 0b01
        req = UpdateReq(pc, meta_wrap.value, pred_target + 0x1, 0, 1)
        pins.update(req.asdict())
        pins.xclock.Step(10)

        pins.update(req.asdict())
        pins.xclock.Step(10)

        # Pred and Check
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        assert meta_wrap.altProvided == 1 and meta_wrap.providerCtr == 0, "should use alternative pred"

        pins.xclock.Step(100)


@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_alt_pred(dut)
    ])

    yield wrapper