"""
   Test the saturation of the training
   Author: yzcc 
"""

import toffee_test

from dut.ITTage import DUTITTage
from ..util.common import UpdateReq
from ..util.meta_parser import MetaParser

from .chk_helper import get_cov_grp_of_train_saturation, get_cov_grp_of_other_train
from ..env.ittage_wrapper import ITTageWrapper


def test_saturation_train(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper
    
    # Start
    pins.xclock.Step(1000)

    pc = None
    for tab in range(5):
        # Up Saturating
        pc = tab

        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        pred_target = dut_output["pred0"]["jalr_target"]

        meta_wrap.provided = 1
        meta_wrap.provider = tab
        meta_wrap.providerCtr = 0b11  # up bound
        req = UpdateReq(pc, meta_wrap.value, pred_target, 0, 0)
        pins.update(req.asdict())

        pins.xclock.Step(10)

        # Check
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        assert meta_wrap.provided == 1 and meta_wrap.provider == tab and meta_wrap.providerCtr == 0b11, f"T{tab} up saturation fails"

        # Down Saturating
        pc = tab + 47

        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        pred_target = dut_output["pred0"]["jalr_target"]

        meta_wrap.allocate_valid = 0
        meta_wrap.provided = 1
        meta_wrap.provider = tab
        meta_wrap.providerCtr = 0b00
        req = UpdateReq(pc, meta_wrap.value, pred_target + 1, 0, 1)
        pins.update(req.asdict())

        pins.xclock.Step(10)

        # Check
        dut_output = pins.predict(0, pc, True)
        meta_wrap = MetaParser(dut_output["last_stage_meta"])
        assert meta_wrap.provided == 1 and meta_wrap.provider == tab and meta_wrap.providerCtr == 0b00, f"T{tab} down saturation fails"
      
        
@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_train_saturation(dut),
        get_cov_grp_of_other_train(dut),
    ])

    yield wrapper