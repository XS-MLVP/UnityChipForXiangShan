import random

import toffee_test
from dut.PTW import DUTPTW

import toffee
from toffee import *

from ..bundle.bundle import PTWBundle


@toffee_test.testcase
async def test_ptw_reset(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    ptw = toffee_request.create_dut(DUTPTW, "clock")
    toffee.start_clock(ptw)

    ptw_bundle = PTWBundle()
    ptw_bundle.bind(ptw)



    #
    # reset dut
    #

    #ptw_bundle['reset'].value = 1
    ptw_bundle.reset.value = 1
    await ptw_bundle.step(10)
    ptw_bundle.reset.value = 0
    await ptw_bundle.step(1)

    assert 1 == ptw_bundle.io_req_ready.value



