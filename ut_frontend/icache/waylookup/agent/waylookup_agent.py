from toffee import Agent
from ..bundle import WayLookupBundle
from ..trans import WayLookup_trans, WayLookup_update_trans
import queue

class WayLookupAgent(Agent):

    def __init__(self, bundle: WayLookupBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle
        self.write_queue = queue.Queue()
        self.update_queue = queue.Queue()
        self.read_queue = queue.Queue()


    async def send_write(self):
        while True:
            if self.write_queue.empty():
                await self.bundle.step()
            else:
                write_trans: WayLookup_trans = self.write_queue.get()
                while self.bundle.io._write._ready.value == 0:
                    await self.bundle.step()
                
                self.bundle.io._write._valid.value = 1
                self.bundle.io._write._bits._entry._vSetIdx._0.value = write_trans.common0.vSetIdx
                self.bundle.io._write._bits._entry._vSetIdx._1.value = write_trans.common1.vSetIdx
                self.bundle.io._write._bits._entry._waymask._0.value = write_trans.common0.waymask
                self.bundle.io._write._bits._entry._waymask._1.value = write_trans.common1.waymask
                self.bundle.io._write._bits._entry._ptag._0.value = write_trans.common0.ptag
                self.bundle.io._write._bits._entry._ptag._1.value = write_trans.common1.ptag
                self.bundle.io._write._bits._entry._itlb._exception._0.value = write_trans.common0.itlb_exception
                self.bundle.io._write._bits._entry._itlb._exception._1.value = write_trans.common1.itlb_exception
                self.bundle.io._write._bits._entry._itlb._pbmt._0.value = write_trans.common0.itlb_pbmt
                self.bundle.io._write._bits._entry._itlb._pbmt._1.value = write_trans.common1.itlb_pbmt
                self.bundle.io._write._bits._entry._meta_codes._0.value = write_trans.common0.meta_codes
                self.bundle.io._write._bits._entry._meta_codes._1.value = write_trans.common1.meta_codes
                self.bundle.io._write._bits._gpf._gpaddr.value = write_trans.gpf_gpaddr
                self.bundle.io._write._bits._gpf._isForVSnonLeafPTE.value = write_trans.gpf_isForVSnonLeafPTE

                await self.bundle.step()
                self.bundle.io._write._valid.value = 0




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