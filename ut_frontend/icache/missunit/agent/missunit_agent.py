import asyncio
from toffee import Agent
from ..bundle import ICacheMissUnitBundle
import toffee


class ICacheMissUnitAgent(Agent):
    def __init__(self, bundle: ICacheMissUnitBundle):
        super().__init__(bundle)
        self.bundle = bundle

    async def fencei_func(self, value):
    # Sets the io_fencei signal.
        self.bundle.io._fencei.value = value
        await self.bundle.step(10)


    async def drive_set_flush(self, value: bool):
    # Sets or clears the io_flush signal.
        current_value = int(value)
        self.bundle.io._flush.value = current_value
        await self.bundle.step()
    
    async def drive_set_victim_way(self, way: int):
    # Sets the victim way.
        self.bundle.io._victim._way.value = way
        await self.bundle.step()

    async def drive_send_fetch_request(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> dict:
        fetch_info = {}
        fetch_info["send_success"] = False
        for i in range(timeout_cycles):
            if self.bundle.io._fetch._req._ready.value == 1 and self.bundle.io._fetch._req._valid.value == 0:
                self.bundle.io._fetch._req._bits._blkPaddr.value = blkPaddr
                self.bundle.io._fetch._req._bits._vSetIdx.value = vSetIdx
                self.bundle.io._fetch._req._valid.value = 1
                toffee.info(f"Fetch request accepted (cycle {i+1}). fetch_req_ready=1")
                await self.bundle.step()
                self.bundle.io._fetch._req._valid.value = 0
                fetch_info["blkPaddr"] = self.bundle.io._fetch._req._bits._blkPaddr.value
                fetch_info["vSetIdx"] = self.bundle.io._fetch._req._bits._vSetIdx.value
                if self.bundle.io._fetch._req._ready.value == 1:
                    fetch_info["send_success"] = True
                return fetch_info
            else:
                toffee.info(f"Fetch request not accepted (cycle {i+1}). fetch_req_ready=0")
            await self.bundle.step()

        toffee.info(f"Timeout: Fetch request not accepted after {timeout_cycles} cycles.")
        self.bundle.io._fetch._req._valid.value = 0
        await self.bundle.step()
        return fetch_info

    async def drive_send_prefetch_req(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> dict:
        """High-level API: Drives a prefetch request and waits for acceptance."""
        prefetch_info = {}
        prefetch_info["send_success"] = False
        # wait for ready
        for i in range(timeout_cycles):
            # before every cycle, check whether ready
            if self.bundle.io._prefetch_req._ready.value == 1 and self.bundle.io._prefetch_req._valid.value == 0:
                toffee.info(f"Attempting to send prefetch request ,and at most wait for {timeout_cycles} cycles: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}")
                # drive valid to high
                self.bundle.io._prefetch_req._valid.value = 1
                self.bundle.io._prefetch_req._bits._blkPaddr.value = blkPaddr
                self.bundle.io._prefetch_req._bits._vSetIdx.value = vSetIdx
                await self.bundle.step()  # wait for the next cycle
                toffee.info(f"Prefetch request accepted on cycle {i+1}.")
                self.bundle.io._prefetch_req._valid.value = 0  # reset valid to low
                prefetch_info["blkPaddr"] = self.bundle.io._prefetch_req._bits._blkPaddr.value
                prefetch_info["vSetIdx"] = self.bundle.io._prefetch_req._bits._vSetIdx.value
                if self.bundle.io._prefetch_req._ready.value == 1:
                    prefetch_info["send_success"] = True
                return prefetch_info
            else:
                toffee.info(f"Preetch request not accepted (cycle {i+1}). fetch_req_ready=0")
            # if not ready，push to next cycle
            await self.bundle.step()
        
        # timeout
        toffee.info("Timeout: Prefetch request not accepted.")
        self.bundle.io._prefetch_req._valid.value = 0 # cancel valid
        await self.bundle.step()
        return prefetch_info

    async def drive_acknowledge_acquire(self, cycles: int = 1, ready_value: int = 1):
        toffee.info(f"Setting io_mem_acquire_ready to {ready_value} for {cycles} cycle(s).")
        self.bundle.io._mem._acquire._ready.value = ready_value
        for _ in range(cycles):
            if self.bundle.io._mem._acquire._valid.value == 1 and self.bundle.io._mem._acquire._ready.value == 1:
                toffee.info(f"Acquire handshake occurred.")
            await self.bundle.step()
        if cycles > 0 :
            self.bundle.io._mem._acquire._ready.value = 0
            toffee.info(f"Setting io_mem_acquire_ready back to 0.")

    async def drive_get_acquire_request(self, timeout_cycles: int = 10) -> dict | None:
        toffee.info(f"Waiting for memory acquire request...")

        for i in range(timeout_cycles):
            if self.bundle.io._mem._acquire._valid.value == 1:
                acquire_info = {
                    "source": self.bundle.io._mem._acquire._bits._source.value,
                    "address": self.bundle.io._mem._acquire._bits._address.value
                }
                toffee.info(f"Captured acquire request (cycle {i+1}): {acquire_info}")
                return acquire_info
            await self.bundle.step()
        
        toffee.info(f"Timeout: Did not capture acquire request after {timeout_cycles} cycles.")
        return None

    async def drive_get_and_acknowledge_acquire(self, timeout_cycles: int = 10, ack_cycles: int = 1) -> dict | None:
        """
        获取acquire请求并立即进行handshake确认
        这是一个组合操作，确保每个acquire请求只被处理一次
        """
        toffee.info(f"Waiting for memory acquire request...")
        
        for i in range(timeout_cycles):
            if self.bundle.io._mem._acquire._valid.value == 1:
                acquire_info = {
                    "source": self.bundle.io._mem._acquire._bits._source.value,
                    "address": self.bundle.io._mem._acquire._bits._address.value
                }
                toffee.info(f"Captured acquire request (cycle {i+1}): {acquire_info}")
                
                # 立即进行handshake确认
                toffee.info(f"Immediately acknowledging acquire request...")
                self.bundle.io._mem._acquire._ready.value = 1
                await self.bundle.step()
                
                # 确认handshake完成
                if self.bundle.io._mem._acquire._valid.value == 1 and self.bundle.io._mem._acquire._ready.value == 1:
                    toffee.info(f"Acquire handshake occurred.")
                
                # 等待额外的确认周期
                for _ in range(ack_cycles - 1):
                    await self.bundle.step()
                
                # 关闭ready信号
                self.bundle.io._mem._acquire._ready.value = 0
                toffee.info(f"Setting io_mem_acquire_ready back to 0.")
                
                # 等待acquire_valid变为0，确保这个请求已被完全处理
                for wait_cycle in range(5):
                    await self.bundle.step()
                    if self.bundle.io._mem._acquire._valid.value == 0:
                        toffee.info(f"Acquire valid dropped after {wait_cycle + 1} cycles.")
                        break
                
                return acquire_info
            await self.bundle.step()
        
        toffee.info(f"Timeout: Did not capture acquire request after {timeout_cycles} cycles.")
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

        toffee.info(f"Starting to send Grant for source_id={source_id}, {num_beats} beats.")

        for i in range(num_beats):
            current_beat_data = data_beats[i]
            current_corrupt = is_corrupt_list[i]

            self.bundle.io._mem._grant._bits._opcode.value = op_code
            self.bundle.io._mem._grant._bits._size.value = beat_size_code
            self.bundle.io._mem._grant._bits._source.value = source_id
            self.bundle.io._mem._grant._bits._data.value = current_beat_data
            self.bundle.io._mem._grant._bits._corrupt.value = int(current_corrupt)
            self.bundle.io._mem._grant._valid.value = 1
        
            toffee.info(f"Sending Grant beat {i+1}/{num_beats}: data={hex(current_beat_data)}, corrupt={current_corrupt}")
            await self.bundle.step()

        self.bundle.io._mem._grant._valid.value = 0
        toffee.info(f"Grant transmission finished for source_id={source_id}.")
    
    async def drive_get_fetch_response(self, timeout_cycles: int = 20) -> dict | None:
        toffee.info(f"Waiting for fetch response...")
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
                toffee.info(f"Captured fetch response (cycle {i+1}): {response_info}")
                return response_info
            await self.bundle.step()
        
        toffee.info(f"Timeout: Did not capture fetch response after {timeout_cycles} cycles.")
        return None