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

    def __init__(self, bundle: WayLookupBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle

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
