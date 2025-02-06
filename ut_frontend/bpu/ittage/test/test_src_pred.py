"""
    Src of prediction from:
        1. Main prediction
        2. Alt prediction
        3. FTB prediction
    Author: yzcc
"""

import toffee_test
from toffee import CovGroup
from ..util.common import UpdateReq
from ..util.meta_parser import MetaParser

from .chk_helper import get_cov_grp_of_other_pred
from ..env.ittage_wrapper import ITTageWrapper

from dut.ITTage import DUTITTage


def test_src_pred(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper

    # Start
    pins.xclock.Step(1000)

    pc = 0x0
    # Test: Use Main Pred - 2
    dut_output = pins.predict(0, pc, True)  # get meta, alloc
    meta_wrap = MetaParser(dut_output["last_stage_meta"])

    meta_wrap.allocate_bits = 4  # update
    req = UpdateReq(pc, meta_wrap.value, 0x114514, 0, 1)
    pins.update(req.asdict())
    pins.xclock.Step(10)

    dut_output = pins.predict(0, pc, True)
    assert dut_output["pred0"]["jalr_target"] == 0x114514, "Target should from main prediction"

    # Test: Use Main Pred - 1
    fake_meta = MetaParser(0)
    # except provider is unconfident
    fake_meta.provided = 1
    fake_meta.provider = 3
    fake_meta.providerCtr = 0
    fake_meta.providerTarget = 0x1919810
    # except altProvider is invalid
    fake_meta.altProvided = 0
    fake_meta.altProvidedCtr = 0x114514

    pins.update(UpdateReq(0x123, fake_meta.meta, 0xFF000, 1, 1).asdict())
    pins.in_bundle.pred3.jalr_target.value = 0xF  # T0 Target
    pins.predict(1, 0x123)
    dut_output = pins.out_bundle.as_dict()
    assert dut_output['pred0']['jalr_target'] in {0xF, 0xFF000}, "Predict Target is not from known sources"
    pins.in_bundle.pred3.jalr_target.value = 0

    # Test: Use Alt Pred
    # Alloc Second Longest
    meta_wrap.allocate_bits = 1
    req = UpdateReq(pc, meta_wrap.value, 0x1919810, 0, 1)
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

    dut_output = pins.predict(0, pc, True)
    assert dut_output["pred0"]["jalr_target"] == 0x1919810, "Target should from alt prediction"

    # Test: Use FTB Prerd
    pc = 0x114
    dut_output = pins.predict(0, pc, True)
    assert dut_output["pred0"]["jalr_target"] == 0x0, "Target should from ftb"
    
    
@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_other_pred(dut)
    ])

    yield wrapper