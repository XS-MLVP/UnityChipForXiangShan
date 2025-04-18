import pytest
from .instruncache_fixture import instruncache_fixture
import toffee_test
from ..env import InstrUncacheEnv


#@pytest.mark.toffee_tags(TAG_SMOKE)
@toffee_test.testcase
async def test_instruncache_smoke(instruncache_fixture):

    io_resp_valid, \
    io_resp_bits_data = await instruncache_fixture.agent._request_data(0xF0000000, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xBBBBBBBB == io_resp_bits_data



#
#  0xF0000006 case needs review
#  should define whats normal behavior
#

@toffee_test.testcase
async def test_instruncache_addr_alignment(instruncache_fixture):

    # subtest 0
    io_resp_valid, \
    io_resp_bits_data = await instruncache_fixture.agent._request_data(0xF0000002, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xAAAABBBB == io_resp_bits_data

    # subtest 1
    io_resp_valid, \
    io_resp_bits_data = await instruncache_fixture.agent._request_data(0xF0000004, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xAAAAAAAA == io_resp_bits_data

    # subtest 2
    io_resp_valid, \
    io_resp_bits_data = await instruncache_fixture.agent._request_data(0xF0000006, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0x0000AAAA == io_resp_bits_data



#
#  InstrUncache does not handle addr misalignment
#  simpley ignore the address bit 0
#
@toffee_test.testcase
async def test_instruncache_addr_misalign(instruncache_fixture):


    io_resp_valid, \
    io_resp_bits_data = await instruncache_fixture.agent._request_data(0xF0000001, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xBBBBBBBB == io_resp_bits_data

