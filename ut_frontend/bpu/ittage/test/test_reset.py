import toffee_test

from toffee import CovGroup

from dut.ITTage import DUTITTage
from .chk_helper import get_cov_grp_of_main_pred
from ..env.ittage_wrapper import ITTageWrapper


def test_reset(ittage_wrapper: ITTageWrapper):
    pins = ittage_wrapper

    dut_output = pins.predict(0, 0x123, True)

    for i in range(4):
        assert dut_output[f"pred{i}"]["jalr_target"] == 0


@toffee_test.fixture
async def ittage_wrapper(toffee_request: toffee_test.ToffeeRequest):
    dut: DUTITTage = toffee_request.create_dut(DUTITTage, "clock")
    wrapper = ITTageWrapper(dut)
    toffee_request.add_cov_groups([
        get_cov_grp_of_main_pred(dut),
    ])

    yield wrapper
