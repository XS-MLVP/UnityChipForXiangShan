from toffee import Agent
from ..bundle import WayLookupBundle
from ..trans import WayLookup_trans, WayLookup_update_trans
import queue
import asyncio
from typing import Callable, Any

class AnalysisPort:
    """
    一个简单的广播端口类，模拟UVM的uvm_analysis_port。
    它可以连接多个订阅者（回调函数），并在调用write()时将数据广播给所有订阅者。
    """
    def __init__(self, name: str = "AnalysisPort"):
        """
        初始化AnalysisPort。
        :param name: 端口的名称，用于调试和日志记录。
        """
        self.name = name
        self._subscribers = []

    def connect(self, callback: Callable):
        """
        连接一个订阅者（回调函数）到这个端口。
        :param callback: 一个可调用对象 (callable)，它接受一个参数（要广播的数据）。
                         这个回调可以是普通函数或异步函数。
        """
        if not callable(callback):
            raise TypeError(f"'{callback}' is not a callable function or method.")
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    async def write(self, item: Any):
        """
        将一个项目（例如一个transaction）广播给所有连接的订阅者。
        :param item: 要广播的数据。
        """
        if not self._subscribers:
            return  # 如果没有订阅者，直接返回

        # 遍历并调用所有回调函数
        for callback in self._subscribers:
            try:
                # 检查回调是否是协程函数 (async def)
                if asyncio.iscoroutinefunction(callback):
                    await callback(item)
                else:
                    callback(item)
            except Exception as e:
                print(f"Error executing callback '{getattr(callback, '__name__', 'unknown')}' for {self.name}: {e}")



class WayLookupAgent(Agent):

    def __init__(self, bundle: WayLookupBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle
        self.write_queue = queue.Queue()
        self.update_queue = queue.Queue()
        self.read_status = 1
        self.flush_status = 0


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
    
    
    async def send_update(self):
        while True:
            if self.update_queue.empty():
                await self.bundle.step()
            else:
                update_trans: WayLookup_update_trans = self.update_queue.get()
                
                self.bundle.io._update._valid.value = 1
                self.bundle.io._update._bits._blkPaddr.value = update_trans.blkPaddr
                self.bundle.io._update._bits._vSetIdx.value = update_trans.vSetIdx
                self.bundle.io._update._bits._waymask.value = update_trans.waymask
                self.bundle.io._update._bits._corrupt.value = update_trans.corrupt

                await self.bundle.step()
                if self.update_queue.empty():
                    self.bundle.io._update._valid.value = 0    
    
    async def send_read(self):
        while True:
            self.bundle.io._read._ready.value = self.read_status
            await self.bundle.step()

    
    async def send_flush(self):
        while True:
            self.bundle.io._flush.value = self.flush_status
            await self.bundle.step()



    
    async def monitor_write(self):
        while True:
            if self.bundle.io._write._valid.value == 1 and self.bundle.io._write._ready.value == 1:
                write_trans = WayLookup_trans()

                write_trans.common0.vSetIdx = self.bundle.io._write._bits._entry._vSetIdx._0.value
                write_trans.common0.waymask = self.bundle.io._write._bits._entry._waymask._0.value
                write_trans.common0.ptag = self.bundle.io._write._bits._entry._ptag._0.value
                write_trans.common0.itlb_exception = self.bundle.io._write._bits._entry._itlb._exception._0.value
                write_trans.common0.itlb_pbmt = self.bundle.io._write._bits._entry._itlb._pbmt._0.value
                write_trans.common0.meta_codes = self.bundle.io._write._bits._entry._meta_codes._0.value

                write_trans.common1.vSetIdx = self.bundle.io._write._bits._entry._vSetIdx._1.value
                write_trans.common1.waymask = self.bundle.io._write._bits._entry._waymask._1.value
                write_trans.common1.ptag = self.bundle.io._write._bits._entry._ptag._1.value
                write_trans.common1.itlb_exception = self.bundle.io._write._bits._entry._itlb._exception._1.value
                write_trans.common1.itlb_pbmt = self.bundle.io._write._bits._entry._itlb._pbmt._1.value
                write_trans.common1.meta_codes = self.bundle.io._write._bits._entry._meta_codes._1.value

                write_trans.gpf_gpaddr = self.bundle.io._write._bits._gpf._gpaddr.value
                write_trans.gpf_isForVSnonLeafPTE = self.bundle.io._write._bits._gpf._isForVSnonLeafPTE.value
                


            await self.bundle.step()




















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