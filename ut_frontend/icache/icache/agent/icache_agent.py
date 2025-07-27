from toffee import Agent, driver_method,monitor_method
from ..bundle import ICacheBundle


class ICacheAgent(Agent):
    def __init__(self, bundle: ICacheBundle):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def ICache_driver(self, core_reset,core_clock,value,
                           #l2 cache TL 
                           l2cache_address_valid_out,
                           l2cache_address_out, 
                           l2cache_address_source_out,
                           l2cache_address_ready_in,

                           l2cache_resp_valid_in,
                           l2cache_resp_opcode_in,
                           l2cache_resp_size_in,
                           l2cache_resp_source_in,
                           l2cache_resp_data_in,
                           l2cache_resp_corrupt_in,
                           #TL slave ctrlunit(cfg used)

                           #hartID
                           cpu_hartID_in,
                           #fetch
                           fetch_req_valid_in,
                           fetch_req_ready_out,
                           fetch_req_bits_backendException_in
                            ):
        #clock reset
        self.bundle.reset.value = core_reset
        self.bundle.clock.value = core_clock
        #l2 cache interface
        self.bundle.auto._client_out._a._ready.value = l2cache_address_ready_in
        self.bundle.auto._client_out._a._valid.value = l2cache_address_valid_out
        self.bundle.auto._client_out._a._bits._address.value = l2cache_address_out
        self.bundle.auto._client_out._a._bits._source.value = l2cache_address_source_out
        
        self.bundle.auto._client_out._d._valid.value = l2cache_resp_valid_in
        self.bundle.auto._client_out._d._bits._size.value = l2cache_resp_size_in
        self.bundle.auto._client_out._d._bits._data.value = l2cache_resp_data_in
        self.bundle.auto._client_out._d._bits._source.value = l2cache_resp_source_in
        self.bundle.auto._client_out._d._bits._opcode.value = l2cache_resp_opcode_in
        self.bundle.auto._client_out._d._bits._corrupt.value = l2cache_resp_corrupt_in
        #TL slave ctrlunit(cfg used)

        #cpu hartID
        self.bundle.io._hartId.value = cpu_hartID_in
        #fetch 
        self.bundle.io._fetch._req._valid.value =fetch_req_valid_in
        self.bundle.io._fetch._req._ready.value =fetch_req_ready_out
        self.bundle.io._fetch._bits._pcMemRead._0.
        self.bundle.io._fetch._bits._backendException.value = fetch_req_bits_backendException_in
        #prefetch

        print(
            f"\nBefore setting fencei: ICacheMetaArray.io_read_ready.value is:",
            self.bundle.ICache__metaArray_io_read_ready.value,
        )

        self.bundle.io._fencei.value = value
        await self.bundle.step()

        print(
            f"\nAfter setting fencei = {value}: ICacheMetaArray.io_read_ready.value is:",
            self.bundle.ICache__metaArray_io_read_ready.value,
        )


    @monitor_method()
    async def ICache_moniter(self):
          print(
            f"\nBefore setting fencei: ICacheMetaArray.io_read_ready.value is:",
          
        )

   