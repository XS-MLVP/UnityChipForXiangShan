"""
    Random Test
    Author: yzcc
"""

import random

import toffee_test
from toffee import CovGroup

from dut.ITTage import DUTITTage
from ..util.common import UpdateReq

from .chk_helper import get_cov_grp_of_main_pred, get_cov_grp_of_us_train, get_cov_grp_of_other_train
from ..env.ittage_wrapper import ITTageWrapper


def test_random(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper

    # Start Test
    pins.reset()

    random.seed(19260817)
    pc = 0x114514
    for ite in range(10000):
        pc += random.randint(0, 0x3) * 2

        # predict
        dut_output = pins.predict(0, pc, True)
        meta = dut_output["last_stage_meta"]
        pred_target = dut_output["pred0"]["jalr_target"]

        # update
        if random.randint(0, 1):
            req = UpdateReq(pc, meta, pred_target, 0, 0)
        else:
            req = UpdateReq(pc, meta, pred_target + 0x1, 0, 1)
        pins.update(req.asdict())


@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_main_pred(dut),
        get_cov_grp_of_us_train(dut),
        get_cov_grp_of_other_train(dut)
    ])

    yield wrapper