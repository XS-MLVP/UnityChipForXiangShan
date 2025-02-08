"""
    Test for allocate entry
    Author: yzcc
"""

import toffee_test

from dut.ITTage import DUTITTage
from ..util.common import UpdateReq
from ..util.meta_parser import MetaParser

from .chk_helper import get_cov_grp_of_other_train, get_cov_grp_of_us_train
from ..env.ittage_wrapper import ITTageWrapper


def test_alloc_train(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper

    # Start
    pins.xclock.Step(1000)

    pc = 0x114514
    dut_output = pins.predict(0, pc, True)
    meta_wrap = MetaParser(dut_output["last_stage_meta"])
    pred_target = dut_output["pred0"]["jalr_target"]

    meta_wrap.allocate_valid = 0
    meta_wrap.allocate_bits = 0

    for i in range(1000):
        req = UpdateReq(pc, meta_wrap.value, pred_target + 0x4, 0, 1)
        pins.update(req.asdict())

    # Check
    dut_output = pins.predict(0, pc, True)
    meta_wrap = MetaParser(dut_output["last_stage_meta"])
    pred_target = dut_output["pred0"]["jalr_target"]
    assert meta_wrap.provided == 0 and meta_wrap.altProvided == 0 and pred_target == 0

    fake_meta = MetaParser(0)

    # provider is unconfident and providing an incorrect target
    fake_meta.provided = 1
    fake_meta.provider = 3
    fake_meta.providerCtr = 0
    fake_meta.providerTarget = 0x114514

    # altProvider is unconfident and providing a correct target
    fake_meta.altProvided = 1
    fake_meta.altProvider = 1
    fake_meta.altProviderCtr = 0
    # altDiffers = s3_finalAltPred != s3_tageTaken_dup(3)
    #            = Mux(altProvided, altProviderInfo.ctr(ITTageCtrBits-1), True) != True
    fake_meta.altDiffers = 1
    fake_meta.altTargetCtr = 0x1919810

    pins.update(UpdateReq(0x123, fake_meta.meta, 0x1919810, 1, 0).asdict())

    assert not (pins.dut.ITTage_tables_3_io_update_valid.value
                and pins.dut.ITTage_tables_3_io_update_u.value
                and pins.dut.ITTage_tables_3_io_update_uValid.value), "provider shouldn't be set useful"
    
    
@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_other_train(dut),
        get_cov_grp_of_us_train(dut)
    ])

    yield wrapper