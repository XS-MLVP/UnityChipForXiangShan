"""
    Test the main prediction func
    Author: yzcc
"""

import asyncio
import toffee_test
from random import randint

from dut.ITTage import DUTITTage
from ..util.common import UpdateReq
from ..util.meta_parser import MetaParser

from .chk_helper import get_cov_grp_of_main_pred
from ..env.ittage_wrapper import ITTageWrapper

@toffee_test.testcase
async def test_main_pred(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper

    # Start
    pins.reset()

    for tab in range(5):
        pc = tab
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        pred_target = dut_output["pred0"]["jalr_target"]

        meta_wrap.allocate_bits = tab

        req = UpdateReq(pc, meta_wrap.value, pred_target + randint(1, 0x114514), 0, 1)
        pins.update(req.asdict())

        # Check
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        assert meta_wrap.provided == 1 and meta_wrap.provider == tab, f"T{tab} should be hit"

@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_main_pred(dut)
    ])

    yield wrapper
