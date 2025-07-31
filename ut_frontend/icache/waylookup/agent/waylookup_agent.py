import asyncio
from toffee import Agent
from ..bundle import WayLookupBundle

class WayLookupAgent(Agent):
    def __init__(self, bundle: WayLookupBundle, dut: None):
        super().__init__(bundle)
        self.bundle = bundle
        self.dut = dut
        bundle.set_all(0)

    # ==================== 基础控制API ====================
    
    async def reset_dut(self):
        """Reset the DUT"""
        self.bundle.reset.value = 1
        await self.bundle.step(5)
        self.bundle.reset.value = 0
        await self.bundle.step(5)
        print("DUT reset completed")

    async def drive_set_flush(self, value: bool):
        """Sets or clears the io_flush signal"""
        current_value = int(value)
        self.bundle.io._flush.value = current_value
        await self.bundle.step()
        print(f"Flush signal set to {current_value}")

    async def flush_write_ptr(self):
        # set io_write_fire，io.write.ready is already 1
        self.bundle.io._write._valid.value = 1
        await self.bundle.step()
        
        # set write_ptr by writting entry
        self.bundle.io._write._bits._entry._vSetIdx._0.value = 0
        self.bundle.io._write._bits._entry._vSetIdx._1.value = 1
        self.bundle.io._write._bits._entry._waymask._0.value = 0
        self.bundle.io._write._bits._entry._waymask._1.value = 1
        self.bundle.io._write._bits._entry._ptag._0.value = 0
        self.bundle.io._write._bits._entry._ptag._1.value = 1
        self.bundle.io._write._bits._entry._itlb._exception._0.value = 0
        self.bundle.io._write._bits._entry._itlb._exception._1.value = 1
        self.bundle.io._write._bits._entry._meta_codes._0.value = 0
        self.bundle.io._write._bits._entry._meta_codes._1.value = 1
        await self.bundle.step()
        print("Before flush, write_ptr is: ", self.bundle.WayLookup._writePtr._value.value)
        
        # flush
        self.bundle.io._flush.value = 1
        await self.bundle.step()
        
        # print
        print("After flush, write_ptr is: ", self.bundle.WayLookup._writePtr._value.value)
        await self.bundle.step()
    # ==================== 写操作API ====================
    
    async def drive_write_entry(self, 
                               vSetIdx_0: int = 0,
                               vSetIdx_1: int = 0,
                               waymask_0: int = 0,
                               waymask_1: int = 0,
                               ptag_0: int = 0,
                               ptag_1: int = 0,
                               itlb_exception_0: int = 0,
                               itlb_exception_1: int = 0,
                               itlb_pbmt_0: int = 0,
                               itlb_pbmt_1: int = 0,
                               meta_codes_0: int = 0,
                               meta_codes_1: int = 0,
                               gpf_gpaddr: int = 0,
                               gpf_isForVSnonLeafPTE: int = 0,
                               timeout_cycles: int = 10) -> dict:
        """
        Drive a write entry request and wait for acceptance
        Returns dict with send_success status and actual values written
        """
        write_info = {}
        write_info["send_success"] = False
        
        print(f"Attempting to write entry, timeout: {timeout_cycles} cycles")
        
        for i in range(timeout_cycles):
            # Check if write is ready and we haven't already asserted valid
            if (self.bundle.io._write._ready.value == 1 and 
                self.bundle.io._write._valid.value == 0):
                
                # Set up write data
                self.bundle.io._write._bits._entry._vSetIdx._0.value = vSetIdx_0
                self.bundle.io._write._bits._entry._vSetIdx._1.value = vSetIdx_1
                self.bundle.io._write._bits._entry._waymask._0.value = waymask_0
                self.bundle.io._write._bits._entry._waymask._1.value = waymask_1
                self.bundle.io._write._bits._entry._ptag._0.value = ptag_0
                self.bundle.io._write._bits._entry._ptag._1.value = ptag_1
                self.bundle.io._write._bits._entry._itlb._exception._0.value = itlb_exception_0
                self.bundle.io._write._bits._entry._itlb._exception._1.value = itlb_exception_1
                self.bundle.io._write._bits._entry._itlb._pbmt._0.value = itlb_pbmt_0
                self.bundle.io._write._bits._entry._itlb._pbmt._1.value = itlb_pbmt_1
                self.bundle.io._write._bits._entry._meta_codes._0.value = meta_codes_0
                self.bundle.io._write._bits._entry._meta_codes._1.value = meta_codes_1
                self.bundle.io._write._bits._gpf._gpaddr.value = gpf_gpaddr
                self.bundle.io._write._bits._gpf._isForVSnonLeafPTE.value = gpf_isForVSnonLeafPTE
                
                # Assert valid
                self.bundle.io._write._valid.value = 1
                print(f"Write request accepted (cycle {i+1})")
                
                await self.bundle.step()
                
                # Deassert valid
                self.bundle.io._write._valid.value = 0
                
                # Check if handshake completed
                if self.bundle.io._write._ready.value == 1:
                    write_info["send_success"] = True
                    write_info.update({
                        "vSetIdx_0": self.bundle.io._write._bits._entry._vSetIdx._0.value,
                        "vSetIdx_1": self.bundle.io._write._bits._entry._vSetIdx._1.value,
                        "waymask_0": self.bundle.io._write._bits._entry._waymask._0.value,
                        "waymask_1": self.bundle.io._write._bits._entry._waymask._1.value,
                        "ptag_0": self.bundle.io._write._bits._entry._ptag._0.value,
                        "ptag_1": self.bundle.io._write._bits._entry._ptag._1.value,
                        "itlb_exception_0": self.bundle.io._write._bits._entry._itlb._exception._0.value,
                        "itlb_exception_1": self.bundle.io._write._bits._entry._itlb._exception._1.value,
                        "itlb_pbmt_0": self.bundle.io._write._bits._entry._itlb._pbmt._0.value,
                        "itlb_pbmt_1": self.bundle.io._write._bits._entry._itlb._pbmt._1.value,
                        "meta_codes_0": self.bundle.io._write._bits._entry._meta_codes._0.value,
                        "meta_codes_1": self.bundle.io._write._bits._entry._meta_codes._1.value,
                        "gpf_gpaddr": self.bundle.io._write._bits._gpf._gpaddr.value,
                        "gpf_isForVSnonLeafPTE": self.bundle.io._write._bits._gpf._isForVSnonLeafPTE.value
                    })
                
                return write_info
            else:
                print(f"Write request not accepted (cycle {i+1}). write_ready={self.bundle.io._write._ready.value}")
            
            await self.bundle.step()
        
        print(f"Timeout: Write request not accepted after {timeout_cycles} cycles")
        self.bundle.io._write._valid.value = 0
        await self.bundle.step()
        return write_info

    async def drive_write_entry_with_gpf(self,
                                       vSetIdx_0: int,
                                       vSetIdx_1: int,
                                       waymask_0: int = 1,
                                       waymask_1: int = 1,
                                       ptag_0: int = 0x1000,
                                       ptag_1: int = 0x1001,
                                       gpf_gpaddr: int = 0xDEADBEEF,
                                       gpf_isForVSnonLeafPTE: int = 1,
                                       timeout_cycles: int = 10) -> dict:
        """
        Write entry with GPF exception (itlb_exception = 2)
        """
        return await self.drive_write_entry(
            vSetIdx_0=vSetIdx_0,
            vSetIdx_1=vSetIdx_1,
            waymask_0=waymask_0,
            waymask_1=waymask_1,
            ptag_0=ptag_0,
            ptag_1=ptag_1,
            itlb_exception_0=2,  # GPF exception
            itlb_exception_1=2,  # GPF exception
            itlb_pbmt_0=0,
            itlb_pbmt_1=0,
            meta_codes_0=0,
            meta_codes_1=0,
            gpf_gpaddr=gpf_gpaddr,
            gpf_isForVSnonLeafPTE=gpf_isForVSnonLeafPTE,
            timeout_cycles=timeout_cycles
        )

    # ==================== 读操作API ====================
    
    async def drive_read_entry(self, timeout_cycles: int = 10) -> dict:
        """ 
        Drive a read request and get response
        Returns dict with read data or None if timeout
        """
        print(f"Attempting to read entry, timeout: {timeout_cycles} cycles")
        
        # Set read_ready to enable reading
        self.bundle.io._read._ready.value = 1
        
        try:
            for i in range(timeout_cycles):
                if self.bundle.io._read._valid.value == 1:
                    read_info = {
                        "read_success": True,
                        "vSetIdx_0": self.bundle.io._read._bits._entry._vSetIdx._0.value,
                        "vSetIdx_1": self.bundle.io._read._bits._entry._vSetIdx._1.value,
                        "waymask_0": self.bundle.io._read._bits._entry._waymask._0.value,
                        "waymask_1": self.bundle.io._read._bits._entry._waymask._1.value,
                        "ptag_0": self.bundle.io._read._bits._entry._ptag._0.value,
                        "ptag_1": self.bundle.io._read._bits._entry._ptag._1.value,
                        "itlb_exception_0": self.bundle.io._read._bits._entry._itlb._exception._0.value,
                        "itlb_exception_1": self.bundle.io._read._bits._entry._itlb._exception._1.value,
                        "itlb_pbmt_0": self.bundle.io._read._bits._entry._itlb._pbmt._0.value,
                        "itlb_pbmt_1": self.bundle.io._read._bits._entry._itlb._pbmt._1.value,
                        "meta_codes_0": self.bundle.io._read._bits._entry._meta_codes._0.value,
                        "meta_codes_1": self.bundle.io._read._bits._entry._meta_codes._1.value,
                        "gpf_gpaddr": self.bundle.io._read._bits._gpf._gpaddr.value,
                        "gpf_isForVSnonLeafPTE": self.bundle.io._read._bits._gpf._isForVSnonLeafPTE.value
                    }
                    print(f"Read data captured (cycle {i+1}): vSetIdx_0={hex(read_info['vSetIdx_0'])}")
                    
                    await self.bundle.step()  # Complete handshake
                    return read_info
                
                await self.bundle.step()
            
            print(f"Timeout: No read data available after {timeout_cycles} cycles")
            return {"read_success": False}
        finally:
            # Ensure read_ready is deasserted after the operation
            self.bundle.io._read._ready.value = 0
            await self.bundle.step()

    # ==================== 更新操作API ====================
    
    async def drive_update_entry(self,
                               blkPaddr: int,
                               vSetIdx: int,
                               waymask: int,
                               corrupt: bool = False):
        """
        Drive an update operation (from MissUnit)
        """
        print(f"Driving update: blkPaddr={hex(blkPaddr)}, vSetIdx={hex(vSetIdx)}, waymask={waymask}")
        
        self.bundle.io._update._valid.value = 1
        self.bundle.io._update._bits._blkPaddr.value = blkPaddr
        self.bundle.io._update._bits._vSetIdx.value = vSetIdx
        self.bundle.io._update._bits._waymask.value = waymask
        self.bundle.io._update._bits._corrupt.value = int(corrupt)
        
        await self.bundle.step()
        
        # Clear update signals
        self.bundle.io._update._valid.value = 0
        print("Update operation completed")

    # ==================== 状态查询API ====================
    
    async def get_queue_status(self) -> dict:
        """Get current queue status"""
        # because the readPtr value of bundle is not right, use internal signal as replace
        read_ptr_value = self.dut.GetInternalSignal("WayLookup_top.WayLookup.readPtr_value", use_vpi=False).value
        read_ptr_flag = self.bundle.WayLookup._readPtr._flag.value
        # because the writePtr value of bundle is not right, use internal signal as replace
        write_ptr_value = self.dut.GetInternalSignal("WayLookup_top.WayLookup.writePtr_value", use_vpi=False).value
        write_ptr_flag = self.bundle.WayLookup._writePtr._flag.value
        
        # Calculate queue status

        empty = bool(self.dut.GetInternalSignal("WayLookup_top.WayLookup.empty", use_vpi=False).value)
        full = (read_ptr_value == write_ptr_value) and (read_ptr_flag != write_ptr_flag)
        
        # Calculate count
        if empty:
            count = 0
        elif full:
            count = 32
        elif read_ptr_flag == write_ptr_flag:
            count = write_ptr_value - read_ptr_value
        else:
            count = 32 - read_ptr_value + write_ptr_value
        
        return {
            "empty": empty,
            "full": full,
            "count": count,
            "read_ptr_value": read_ptr_value,
            "read_ptr_flag": read_ptr_flag,
            "write_ptr_value": write_ptr_value,
            "write_ptr_flag": write_ptr_flag,
            "write_ready": bool(self.bundle.io._write._ready.value),
            "read_valid": bool(self.bundle.io._read._valid.value)
        }

    async def get_pointers(self) -> dict:
        """Get read and write pointer states"""
        return {
            "read_ptr_value": self.dut.GetInternalSignal("WayLookup_top.WayLookup.readPtr_value", use_vpi=False).value,
            "read_ptr_flag": self.bundle.WayLookup._readPtr._flag.value,
            "write_ptr_value": self.dut.GetInternalSignal("WayLookup_top.WayLookup.writePtr_value", use_vpi=False).value,
            "write_ptr_flag": self.bundle.WayLookup._writePtr._flag.value
        }

    async def get_gpf_status(self) -> dict:
        """Get GPF-related status (accessing internal signals if available)"""
        # Note: These internal signals may need to be exposed via DPI or accessed differently
        return {
            "write_ready": bool(self.bundle.io._write._ready.value),
            "read_valid": bool(self.bundle.io._read._valid.value),
            "gpf_entry_valid": bool(self.dut.GetInternalSignal("WayLookup_top.WayLookup.gpf_entry_valid", use_vpi=False).value),
            "gpfPtr_flag": bool(self.dut.GetInternalSignal("WayLookup_top.WayLookup.gpfPtr_flag", use_vpi=False).value),
            "gpfPtr_value": self.dut.GetInternalSignal("WayLookup_top.WayLookup.gpfPtr_value", use_vpi=False).value
        }

    # ==================== 辅助验证API ====================
    
    async def fill_queue(self, count: int) -> list:
        """Fill queue with specified number of entries"""
        written_entries = []
        
        for i in range(count):
            entry_data = {
                "vSetIdx_0": 0x10 + i,
                "vSetIdx_1": 0x20 + i,
                "waymask_0": i % 4,  # 2-bit field: 0-3
                "waymask_1": (i + 1) % 4,  # 2-bit field: 0-3
                "ptag_0": 0x1000 + i,
                "ptag_1": 0x2000 + i
            }
            
            result = await self.drive_write_entry(**entry_data)
            await self.bundle.step(2)
            if result["send_success"]:
                written_entries.append(entry_data)
                print(f"Filled entry {i+1}/{count}")
            else:
                print(f"Failed to fill entry {i+1}/{count}, queue may be full")
                break
        
        return written_entries

    async def drain_queue(self) -> list:
        """Drain all entries from queue"""
        drained_entries = []
        
        while True:
            status = await self.get_queue_status()
            print(f"Now there are {status['count']} entries")
            if status["empty"]:
                break
                
            result = await self.drive_read_entry(timeout_cycles=5)
            if result["read_success"]:
                drained_entries.append(result)
                print(f"Drained entry {len(drained_entries)}")
            else:
                break
        
        print(f"Drained {len(drained_entries)} entries from queue")
        return drained_entries

    async def wait_for_condition(self, condition_func, timeout_cycles: int = 100) -> bool:
        """Wait for a custom condition to be true"""
        for i in range(timeout_cycles):
            if await condition_func():
                return True
            await self.bundle.step()
        return False

    # ==================== 高级组合API ====================
    
    async def test_bypass_condition(self) -> dict:
        """Test bypass functionality"""
        # Ensure queue is empty
        await self.drive_set_flush(True)
        await self.drive_set_flush(False)
        
        # Prepare write data
        write_data = {
            "vSetIdx_0": 0xAA,
            "vSetIdx_1": 0xBB,
            "waymask_0": 0x1,  # 2-bit field: 0-3
            "waymask_1": 0x2,  # 2-bit field: 0-3
            "ptag_0": 0xDEAD,
            "ptag_1": 0xBEEF
        }
        
        # Set up concurrent write and read
        self.bundle.io._read._ready.value = 1
        
        # Drive write
        self.bundle.io._write._bits._entry._vSetIdx._0.value = write_data["vSetIdx_0"]
        self.bundle.io._write._bits._entry._vSetIdx._1.value = write_data["vSetIdx_1"]
        self.bundle.io._write._bits._entry._waymask._0.value = write_data["waymask_0"]
        self.bundle.io._write._bits._entry._waymask._1.value = write_data["waymask_1"]
        self.bundle.io._write._bits._entry._ptag._0.value = write_data["ptag_0"]
        self.bundle.io._write._bits._entry._ptag._1.value = write_data["ptag_1"]
        self.bundle.io._write._valid.value = 1
        
        await self.bundle.step()
        
        # Check if bypass occurred
        read_data = {}
        if self.bundle.io._read._valid.value == 1:
            read_data = {
                "vSetIdx_0": self.bundle.io._read._bits._entry._vSetIdx._0.value,
                "vSetIdx_1": self.bundle.io._read._bits._entry._vSetIdx._1.value,
                "waymask_0": self.bundle.io._read._bits._entry._waymask._0.value,
                "waymask_1": self.bundle.io._read._bits._entry._waymask._1.value,
                "ptag_0": self.bundle.io._read._bits._entry._ptag._0.value,
                "ptag_1": self.bundle.io._read._bits._entry._ptag._1.value
            }
        
        # Clear signals
        self.bundle.io._write._valid.value = 0
        self.bundle.io._read._ready.value = 0
        
        return {
            "bypass_occurred": self.bundle.io._read._valid.value == 1,
            "write_data": write_data,
            "read_data": read_data,
            "data_match": write_data == read_data
        }
