from ..bundle import InstrUncacheIOBundle
from toffee import Agent, driver_method

class InstrUncacheAgent(Agent):
    def __init__(self, bundle:InstrUncacheIOBundle):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def _request_data(self, \
                            req_addr, \
                            l2_resp_source, \
                            l2_resp_data):
    

        # Simulate L2 already ready
        self.bundle.auto_client_out_a_ready.value = 1
    
    
        #
        # reset dut
        #
    
        #self.bundle['reset'].value = 1
        self.bundle.reset.value = 1
        await self.bundle.step(10)
        self.bundle.reset.value = 0
        await self.bundle.step(1)
    
        assert 1 == self.bundle.io_req_ready.value
    
    
        #
        # Simulate IFU sends a request
        #
    
        self.bundle.io_req_bits_addr.value= req_addr;
        self.bundle.io_req_valid.value = 1;
    
        await self.bundle.step(1)
    
        # pull io_req_valid low after seeing io_req_ready high for one cycle
        self.bundle.io_req_valid.value = 0;
    
        await self.bundle.step(1)
    
    
        # InstrUncache should be busy now
        assert 0 == self.bundle.io_req_ready.value
    
        # InstrUncache should send out request to L2
        assert 0xF0000000 == self.bundle.auto_client_out_a_bits_address.value
        assert 1 == self.bundle.auto_client_out_a_valid.value
    
        # after seeing auto_client_out_a_valid high for once cycle, L2 should turn to busy
        self.bundle.auto_client_out_a_ready.value = 0
    
        await self.bundle.step(1)
    
    
        #
        # Simulate L2 takes the request and sends back data
        #
    
    
        # L2 may take variable cycles to get back the data
        await self.bundle.step(5)
    
#        assert 1 == self.bundle.auto_client_out_d_ready.value
    
        self.bundle.auto_client_out_d_valid.value = 1
        self.bundle.auto_client_out_d_bits_source.value = l2_resp_source
        self.bundle.auto_client_out_d_bits_data.value = l2_resp_data
    
        # _data with _valid last for one cycle
        await self.bundle.step(1)
        self.bundle.auto_client_out_d_valid.value = 0
        self.bundle.auto_client_out_d_bits_source.value = 0
        self.bundle.auto_client_out_d_bits_data.value = 0
    
        # L2 ready to take another request
        self.bundle.auto_client_out_a_ready.value = 1
    
    
    
        #
        # Test InstrUncache return data to IFU the requester
        #
    
        # Needs one cycle for the data to go through InstrUncache, registering
        await self.bundle.step(1)
    
        return self.bundle.io_resp_valid.value, self.bundle.io_resp_bits_data.value


