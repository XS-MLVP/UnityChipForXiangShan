import asyncio
from toffee import Agent
from ..bundle import WayLookupBundle


class ReadBitsData:

    WayLookup_readPtr_value_before_flush: int
    WayLookup_readPtr_value_after_flush: int
    WayLookup_readPtr_flag_before_flush: bool
    WayLookup_readPtr_flag_after_flush: bool
    WayLookup_writePtr_value_before_flush: int
    WayLookup_writePtr_value_after_flush: int
    WayLookup_writePtr_flag_before_flush: bool
    WayLookup_writePtr_flag_after_flush: bool
    flush: int

    def __str__(self):
        return (
            f"\n"
            f"WayLookup_readPtr_value_before_flush: {self.WayLookup_readPtr_value_before_flush}\n"
            f"WayLookup_readPtr_value_after_flush: {self.WayLookup_readPtr_value_after_flush}\n"
            f"WayLookup_readPtr_flag_before_flush: {self.WayLookup_readPtr_flag_before_flush}\n"
            f"WayLookup_readPtr_flag_after_flush: {self.WayLookup_readPtr_flag_after_flush}\n"
            f"WayLookup_writePtr_value_before_flush: {self.WayLookup_writePtr_value_before_flush}\n"
            f"WayLookup_writePtr_value_after_flush: {self.WayLookup_writePtr_value_after_flush}\n"
            f"WayLookup_writePtr_flag_before_flush: {self.WayLookup_writePtr_flag_before_flush}\n"
            f"WayLookup_writePtr_flag_after_flush: {self.WayLookup_writePtr_flag_after_flush}\n"
            f"flush: {self.flush}\n"
        )


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
    async def flush(self) -> ReadBitsData:

        ret = ReadBitsData()

        ret.WayLookup_readPtr_value_before_flush = (
            self.bundle.WayLookup._readPtr._value.value
        )
        ret.WayLookup_readPtr_flag_before_flush = (
            self.bundle.WayLookup._readPtr._flag.value
        )
        ret.WayLookup_writePtr_value_before_flush = (
            self.bundle.WayLookup._writePtr._value.value
        )
        ret.WayLookup_writePtr_flag_before_flush = (
            self.bundle.WayLookup._writePtr._flag.value
        )

        self.bundle.io._flush.value = 1
        await self.bundle.step()

        ret.WayLookup_readPtr_value_after_flush = (
            self.bundle.WayLookup._readPtr._value.value
        )
        ret.WayLookup_readPtr_flag_after_flush = (
            self.bundle.WayLookup._readPtr._flag.value
        )
        ret.WayLookup_writePtr_value_after_flush = (
            self.bundle.WayLookup._writePtr._value.value
        )
        ret.WayLookup_writePtr_flag_after_flush = (
            self.bundle.WayLookup._writePtr._flag.value
        )

        ret.flush = self.bundle.io._flush.value
        return ret
