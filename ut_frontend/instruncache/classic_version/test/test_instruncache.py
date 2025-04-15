import random

import toffee_test
#from picker_out_instruncache import DUTInstrUncache
from dut.InstrUncache import DUTInstrUncache

import toffee
from toffee import *


class InstrUncacheBundle(Bundle):
        
    clock, \
    reset, \
    auto_client_out_a_ready, \
    auto_client_out_a_valid, \
    auto_client_out_a_bits_address, \
    auto_client_out_d_ready, \
    auto_client_out_d_valid, \
    auto_client_out_d_bits_source, \
    auto_client_out_d_bits_data, \
    io_req_ready, \
    io_req_valid, \
    io_req_bits_addr, \
    io_resp_valid, \
    io_resp_bits_data = Signals(14)



@toffee_test.testcase
async def test_instruncache_smoke(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)


    # Simulate L2 already ready
    instruncache_bundle.auto_client_out_a_ready.value = 1


    #
    # reset dut
    #

    #instruncache_bundle['reset'].value = 1
    instruncache_bundle.reset.value = 1
    await instruncache_bundle.step(10)
    instruncache_bundle.reset.value = 0
    await instruncache_bundle.step(1)

    assert 1 == instruncache_bundle.io_req_ready.value


    #
    # Simulate IFU sends a request
    #

    instruncache_bundle.io_req_bits_addr.value= 0xF0000000;
    instruncache_bundle.io_req_valid.value = 1;

    await instruncache_bundle.step(1)

    # pull io_req_valid low after seeing io_req_ready high for one cycle
    instruncache_bundle.io_req_valid.value = 0;

    await instruncache_bundle.step(1)


    # InstrUncache should be busy now
    assert 0 == instruncache_bundle.io_req_ready.value

    # InstrUncache should send out request to L2
    assert 0xF0000000 == instruncache_bundle.auto_client_out_a_bits_address.value
    assert 1 == instruncache_bundle.auto_client_out_a_valid.value

    # after seeing auto_client_out_a_valid high for once cycle, L2 should turn to busy
    instruncache_bundle.auto_client_out_a_ready.value = 0

    await instruncache_bundle.step(1)


    #
    # Simulate L2 takes the request and sends back data
    #


    # L2 may take variable cycles to get back the data
    await instruncache_bundle.step(5)

    assert 1 == instruncache_bundle.auto_client_out_d_ready.value

    instruncache_bundle.auto_client_out_d_valid.value = 1
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0xAAAAAAAABBBBBBBB
   
    # _data with _valid last for one cycle
    await instruncache_bundle.step(1)
    instruncache_bundle.auto_client_out_d_valid.value = 0
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0

    # L2 ready to take another request
    instruncache_bundle.auto_client_out_a_ready.value = 1



    #
    # Test InstrUncache return data to IFU the requester
    #

    # Needs one cycle for the data to go through InstrUncache, registering
    await instruncache_bundle.step(1)

    assert 1 == instruncache_bundle.io_resp_valid.value
    assert 0xBBBBBBBB == instruncache_bundle.io_resp_bits_data.value



async def _request_data(instruncache_bundle, req_addr, \
                        l2_resp_source, \
                        l2_resp_data):

    # Simulate L2 already ready
    instruncache_bundle.auto_client_out_a_ready.value = 1


    #
    # reset dut
    #

    #instruncache_bundle['reset'].value = 1
    instruncache_bundle.reset.value = 1
    await instruncache_bundle.step(10)
    instruncache_bundle.reset.value = 0
    await instruncache_bundle.step(1)

    assert 1 == instruncache_bundle.io_req_ready.value


    #
    # Simulate IFU sends a request
    #

    instruncache_bundle.io_req_bits_addr.value= req_addr;
    instruncache_bundle.io_req_valid.value = 1;

    await instruncache_bundle.step(1)

    # pull io_req_valid low after seeing io_req_ready high for one cycle
    instruncache_bundle.io_req_valid.value = 0;

    await instruncache_bundle.step(1)


    # InstrUncache should be busy now
    assert 0 == instruncache_bundle.io_req_ready.value

    # InstrUncache should send out request to L2
    assert 0xF0000000 == instruncache_bundle.auto_client_out_a_bits_address.value
    assert 1 == instruncache_bundle.auto_client_out_a_valid.value

    # after seeing auto_client_out_a_valid high for once cycle, L2 should turn to busy
    instruncache_bundle.auto_client_out_a_ready.value = 0

    await instruncache_bundle.step(1)


    #
    # Simulate L2 takes the request and sends back data
    #


    # L2 may take variable cycles to get back the data
    await instruncache_bundle.step(5)

    assert 1 == instruncache_bundle.auto_client_out_d_ready.value

    instruncache_bundle.auto_client_out_d_valid.value = 1
    instruncache_bundle.auto_client_out_d_bits_source.value = l2_resp_source
    instruncache_bundle.auto_client_out_d_bits_data.value = l2_resp_data
   
    # _data with _valid last for one cycle
    await instruncache_bundle.step(1)
    instruncache_bundle.auto_client_out_d_valid.value = 0
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0

    # L2 ready to take another request
    instruncache_bundle.auto_client_out_a_ready.value = 1



    #
    # Test InstrUncache return data to IFU the requester
    #

    # Needs one cycle for the data to go through InstrUncache, registering
    await instruncache_bundle.step(1)

    return instruncache_bundle.io_resp_valid.value, instruncache_bundle.io_resp_bits_data.value



#
#  0xF0000006 case is questionable
#  should define whats normal behavior
#

@toffee_test.testcase
async def test_instruncache_addr_alignment(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)

    # subtest 0
    io_resp_valid, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000002, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xAAAABBBB == io_resp_bits_data

    # subtest 1
    io_resp_valid, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000004, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xAAAAAAAA == io_resp_bits_data

    # subtest 2
    io_resp_valid, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000006, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0x0000AAAA == io_resp_bits_data


#
#  InstrUncache does not handle addr misalignment
#  simpley ignore the address bit 0
#
@toffee_test.testcase
async def test_instruncache_addr_misalign(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)


    io_resp_valid, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000001, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0xBBBBBBBB == io_resp_bits_data


