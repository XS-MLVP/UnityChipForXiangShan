import toffee_test
from comm import get_version_checker

from dut.InstrUncache import DUTInstrUncache
from toffee import *
from ..env import InstrUncacheEnv
from ..bundle import InstrUncacheIOBundle


version_check = get_version_checker("openxiangshan-kmh-*")


@toffee_test.fixture
async def instruncache_fixture(toffee_request: toffee_test.ToffeeRequest):
    version_check()
    dut = toffee_request.create_dut(DUTInstrUncache, "clock")
    start_clock(dut)


    instruncache_bundle = InstrUncacheIOBundle()
    instruncache_bundle.bind(dut)

    return InstrUncacheEnv(instruncache_bundle)

