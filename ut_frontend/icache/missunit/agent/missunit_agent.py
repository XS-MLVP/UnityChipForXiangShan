import asyncio
from toffee import Agent
from ..bundle import ICacheMissUnitBundle


class ICacheMissUnitAgent(Agent):
    def __init__(self, bundle: ICacheMissUnitBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def fencei_func(self, value):
    #   self.bundle.reset.value = 1
    #   await self.bundle.step(10)
    #   self.bundle.reset.value = 0
    #   await self.bundle.step(10)

        print(f"\nBefore setting fencei :")

        for i in range(10):
            print(
                f"prefetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"prefetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )
            
        for i in range(4):
            print(
                f"fetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"fetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )

        self.bundle.io._fencei.value = value
        await self.bundle.step(10)
        # self.bundle.io._fencei.value = 0  # Reset fencei after setting
        # await self.bundle.step(10)  # Ensure the change is processed
        print("waited 10 cycles after setting fencei")
        print(f"\nAfter setting fencei = {value}")

        for i in range(10):
            print(
                f"prefetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"prefetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._prefetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )

        for i in range(4):
            print(
                f"fetchMSHRs.{i}.io.req.ready.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._req_ready.value,
            )
            print(
                f"fetchMSHRs.{i}.io.acquire.valid.value:",
                getattr(
                    self.bundle.ICacheMissUnit_._fetchMSHRs, f"_{i}"
                )._io._acquire_valid.value,
            )
        

    async def drive_set_flush(self, value: bool):
    # Sets or clears the io_flush signal.
        current_value = int(value)
        print(f"Setting io_flush to {current_value}")
        self.bundle.io._flush.value = current_value
        await self.bundle.step()
        print(f"io_flush is now {self.bundle.io._flush.value}")
    
    async def drive_set_victim_way(self, way: int):
        print(f"Setting io_victim_way to {way}")
        # io_victim_way is under io._victim
        self.bundle.io._victim._way.value = way
        await self.bundle.step()
        print(f"io_victim_way is now {self.bundle.io._victim._way.value}")

    async def drive_send_fetch_request(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> bool:
        print(f"Attempting to send fetch request: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
        self.bundle.io._fetch._req._bits._blkPaddr.value = blkPaddr
        self.bundle.io._fetch._req._bits._vSetIdx.value = vSetIdx
        self.bundle.io._fetch._req._valid.value = 1

        for i in range(timeout_cycles):
            if self.bundle.io._fetch._req._ready.value == 1:
                print(f"Fetch request accepted (cycle {i+1}). fetch_req_ready=1")
                await self.bundle.step()
                self.bundle.io._fetch._req._valid.value = 0
                return True
            await self.bundle.step()

        print(f"Timeout: Fetch request not accepted after {timeout_cycles} cycles.")
        self.bundle.io._fetch._req._valid.value = 0
        return False

    def drive_prefetch_req(self, blkPaddr: int, vSetIdx: int, valid: bool):
        """Drives the prefetch request bus. This is a non-blocking, single-cycle action."""
        self.bundle.io._prefetch_req._valid.value = int(valid)
        if valid:
            self.bundle.io._prefetch_req._bits._blkPaddr.value = blkPaddr
            self.bundle.io._prefetch_req._bits._vSetIdx.value = vSetIdx

    async def drive_send_prefetch_req(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10):
        """High-level API: Drives a prefetch request and waits for acceptance."""
        print(f"Attempting to send prefetch request: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
    
        # drive valid to high
        self.drive_prefetch_req(blkPaddr, vSetIdx, valid=True)
    
        # wait for ready
        for i in range(timeout_cycles):
            # before every cycle, check whether ready
            if self.bundle.io._prefetch_req._ready.value == 1:
                print(f"Prefetch request accepted on cycle {i+1}.")
                await self.bundle.step()
                self.drive_prefetch_req(0, 0, valid=False)
                return True
        
            # if not ready，push to next cycle
            await self.bundle.step()
        
        # timeout
        print("Timeout: Prefetch request not accepted.")
        self.drive_prefetch_req(0, 0, valid=False) # cancel valid
        return False

    async def drive_acknowledge_acquire(self, cycles: int = 1, ready_value: int = 1):
        print(f"Setting io_mem_acquire_ready to {ready_value} for {cycles} cycle(s).")
        self.bundle.io._mem._acquire._ready.value = ready_value
        for _ in range(cycles):
            if self.bundle.io._mem._acquire._valid.value == 1 and self.bundle.io._mem._acquire._ready.value == 1:
                print(f"Acquire handshake occurred.")
            await self.bundle.step()
        if cycles > 0 :
            self.bundle.io._mem._acquire._ready.value = 0
            print(f"Setting io_mem_acquire_ready back to 0.")

    async def drive_get_acquire_request(self, timeout_cycles: int = 10) -> dict | None:
        print(f"Waiting for memory acquire request...")
        for i in range(timeout_cycles):
            if self.bundle.io._mem._acquire._valid.value == 1:
                acquire_info = {
                    "source": self.bundle.io._mem._acquire._bits._source.value,
                    "address": self.bundle.io._mem._acquire._bits._address.value
                }
                print(f"Captured acquire request (cycle {i+1}): {acquire_info}")
                return acquire_info
            await self.bundle.step()
        
        print(f"Timeout: Did not capture acquire request after {timeout_cycles} cycles.")
        return None

    async def drive_respond_with_grant(self,
                               source_id: int,
                               data_beats: list,
                               beat_size_code: int = 6,
                               op_code: int = 5,
                               is_corrupt_list: list = None
                              ):
        num_beats = len(data_beats)
        if is_corrupt_list is None:
            is_corrupt_list = [False] * num_beats
        elif len(is_corrupt_list) != num_beats:
            raise ValueError("is_corrupt_list length must match data_beats length")

        print(f"Starting to send Grant for source_id={source_id}, {num_beats} beats.")

        for i in range(num_beats):
            current_beat_data = data_beats[i]
            current_corrupt = is_corrupt_list[i]

            self.bundle.io._mem._grant._bits._opcode.value = op_code
            self.bundle.io._mem._grant._bits._size.value = beat_size_code
            self.bundle.io._mem._grant._bits._source.value = source_id
            self.bundle.io._mem._grant._bits._data.value = current_beat_data
            self.bundle.io._mem._grant._bits._corrupt.value = int(current_corrupt)
            self.bundle.io._mem._grant._valid.value = 1
        
            print(f"Sending Grant beat {i+1}/{num_beats}: data={hex(current_beat_data)}, corrupt={current_corrupt}")
            await self.bundle.step()

        self.bundle.io._mem._grant._valid.value = 0
        print(f"Grant transmission finished for source_id={source_id}.")
    
    async def drive_get_fetch_response(self, timeout_cycles: int = 20) -> dict | None:
        print(f"Waiting for fetch response...")
        for i in range(timeout_cycles):
            # io_fetch_resp_valid -> io._fetch._resp._valid
            if self.bundle.io._fetch._resp._valid.value == 1:
                response_info = {
                    "blkPaddr": self.bundle.io._fetch._resp._bits._blkPaddr.value,
                    "vSetIdx": self.bundle.io._fetch._resp._bits._vSetIdx.value,
                    "waymask": self.bundle.io._fetch._resp._bits._waymask.value,
                    "data": self.bundle.io._fetch._resp._bits._data.value,
                    "corrupt": bool(self.bundle.io._fetch._resp._bits._corrupt.value)
                }
                print(f"Captured fetch response (cycle {i+1}): {response_info}")
                return response_info
            await self.bundle.step()
        
        print(f"Timeout: Did not capture fetch response after {timeout_cycles} cycles.")
        return None