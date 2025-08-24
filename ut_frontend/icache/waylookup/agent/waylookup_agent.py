from toffee import Agent
from ..bundle import WayLookupBundle
from ..trans import WayLookup_trans, WayLookup_update_trans
import queue
import asyncio
from typing import Callable, Any
import random
from abc import ABC, abstractmethod


class AnalysisPort:
    """
    一个【健壮的】广播端口类，模拟UVM的uvm_analysis_port。
    它强制所有回调都是同步的，以确保广播操作在零仿真时间内完成。
    """
    def __init__(self, name: str = "AnalysisPort"):
        self.name = name
        self._subscribers = []

    def connect(self, callback: Callable):
        """
        连接一个订阅者（回调函数）到这个端口。
        【重要】: 此处禁止连接异步(async def)函数，以保证零延迟语义。
        """
        if not callable(callback):
            raise TypeError(f"'{callback}' is not a callable function or method.")
        
        # 核心修改：检查回调是否是协程函数，如果是，则禁止连接
        if asyncio.iscoroutinefunction(callback):
            raise TypeError(
                f"Cannot connect an async function '{getattr(callback, '__name__', 'unknown')}' "
                f"to AnalysisPort '{self.name}'. Callbacks must be synchronous to guarantee zero-delay execution."
            )
            
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def write(self, item: Any):
        """
        【同步方法】将一个项目（例如一个transaction）广播给所有连接的订阅者。
        此操作保证在调用者的当前仿真周期内完成。
        """
        # 注意：这里不再有 async 和 await
        for callback in self._subscribers:
            try:
                callback(item) # 直接同步调用
            except Exception as e:
                print(f"Error executing callback '{getattr(callback, '__name__', 'unknown')}' for {self.name}: {e}")


class BackPressureController:

    class BackPressurePolicy(ABC):
        @abstractmethod
        def generate(self) -> bool:
            pass

    class AlwaysOnPolicy(BackPressurePolicy):
        def generate(self) -> bool:
            return True

    class AlwaysOffPolicy(BackPressurePolicy):
        def generate(self) -> bool:
            return False

    class RandomDutyCyclePolicy(BackPressurePolicy):
        def __init__(self, duty_cycle: float):
            if not 0.0 <= duty_cycle <= 1.0:
                raise ValueError("Duty cycle must be between 0.0 and 1.0")
            self._duty_cycle = duty_cycle

        def generate(self) -> bool:
            return random.random() < self._duty_cycle


    def __init__(self, initial_policy: 'BackPressureController.BackPressurePolicy' = None):
        self._policy: BackPressureController.BackPressurePolicy
        if initial_policy is None:
            self.set_policy(self.AlwaysOnPolicy())
        else:
            self.set_policy(initial_policy)
        
        self._force_value: bool = False
        self._force_duration_remaining: int = 0

    def set_policy(self, policy: 'BackPressureController.BackPressurePolicy'):
        print(f"[ReadyController] Policy updated to {policy.__class__.__name__}.")
        self._policy = policy

    def force(self, value: bool, duration: int):
        if duration < 1:
            raise ValueError("Force duration must be at least 1 cycle.")
        print(f"[ReadyController] Forcing ready to {value} for {duration} cycles.")
        self._force_value = value
        self._force_duration_remaining = duration

    def get_value(self) -> bool:
        return_value = 0
        if self._force_duration_remaining > 0:
            return_value = self._force_value
        else:
            return_value = self._policy.generate()
            
        if self._force_duration_remaining > 0:
            self._force_duration_remaining -= 1
        
        return return_value




class WayLookupAgent(Agent):

    def __init__(self, bundle: WayLookupBundle):
        super().__init__(bundle)
        bundle.set_all(0)
        self.bundle = bundle
        self.write_queue = queue.Queue()
        self.update_queue = queue.Queue()
        self.flush_status = 0

        self.read_bp = BackPressureController()
        self.flush_bp = BackPressureController()
        
        # 为每种需要监视和广播的事件创建一个AnalysisPort实例
        self.write_ap = AnalysisPort("write_ap")
        self.update_ap = AnalysisPort("update_ap")
        # 如果需要，也可以为read和flush创建
        self.read_ap = AnalysisPort("read_ap")
        self.flush_ap = AnalysisPort("flush_ap")



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
            self.bundle.io._read._ready.value = int(self.read_bp.get_value())
            await self.bundle.step()

    
    async def send_flush(self):
        while True:
            self.bundle.io._flush.value = 1-int(self.flush_bp.get_value())
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
                
                self.write_ap.write(write_trans)
            await self.bundle.step()

            
    
    async def monitor_read(self):
        while True:
            if self.bundle.io._read._valid.value == 1 and self.bundle.io._read._ready.value == 1:
                read_trans = WayLookup_trans()

                read_trans.common0.vSetIdx = self.bundle.io._read._bits._entry._vSetIdx._0.value
                read_trans.common0.waymask = self.bundle.io._read._bits._entry._waymask._0.value
                read_trans.common0.ptag = self.bundle.io._read._bits._entry._ptag._0.value
                read_trans.common0.itlb_exception = self.bundle.io._read._bits._entry._itlb._exception._0.value
                read_trans.common0.itlb_pbmt = self.bundle.io._read._bits._entry._itlb._pbmt._0.value
                read_trans.common0.meta_codes = self.bundle.io._read._bits._entry._meta_codes._0.value

                read_trans.common1.vSetIdx = self.bundle.io._read._bits._entry._vSetIdx._1.value
                read_trans.common1.waymask = self.bundle.io._read._bits._entry._waymask._1.value
                read_trans.common1.ptag = self.bundle.io._read._bits._entry._ptag._1.value
                read_trans.common1.itlb_exception = self.bundle.io._read._bits._entry._itlb._exception._1.value
                read_trans.common1.itlb_pbmt = self.bundle.io._read._bits._entry._itlb._pbmt._1.value
                read_trans.common1.meta_codes = self.bundle.io._read._bits._entry._meta_codes._1.value

                read_trans.gpf_gpaddr = self.bundle.io._read._bits._gpf._gpaddr.value
                read_trans.gpf_isForVSnonLeafPTE = self.bundle.io._read._bits._gpf._isForVSnonLeafPTE.value
                
                self.read_ap.write(read_trans)
            await self.bundle.step()


    async def monitor_update(self):
        while True:
            if self.bundle.io._update._valid.value == 1:
                update_trans = WayLookup_update_trans()

                update_trans.blkPaddr = self.bundle.io._update._bits._blkPaddr.value
                update_trans.vSetIdx = self.bundle.io._update._bits._vSetIdx.value
                update_trans.waymask = self.bundle.io._update._bits._waymask.value
                update_trans.corrupt = self.bundle.io._update._bits._corrupt.value
                
                self.update_ap.write(update_trans)
            await self.bundle.step()


    async def monitor_flush(self):
        while True:
            if self.bundle.io._flush.value == 1:
                
                self.flush_ap.write(1)
            await self.bundle.step()


##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############
##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############
##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############
##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############
##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############
##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############
##############           上方代码用于实现基本Agent功能，下方代码用于实现Sequencer功能           ##############

    def write_write_trans(self, trans: WayLookup_trans):
        """发送一个write transaction"""
        self.write_queue.put(trans)    
    
    def write_update_trans(self, trans: WayLookup_update_trans):
        """发送一个update transaction"""
        self.update_queue.put(trans)
    
    def write_flush(self, duration):
        """拉起flush"""
        self.flush_bp.force(False, duration)
    
    def write_read(self, duration):
        """拉低read"""
        self.read_bp.force(False, duration)
    
    async def delay(self, cycles: int):
        """等待指定的仿真时钟周期数"""
        if cycles > 0:
            for _ in range(cycles):
                await self.bundle.step()





    async def do_flush(self, duration: int = 1):
        """触发flush信号，并等待指定的周期数"""
        self.write_flush(duration)
        await self.delay(duration)

    async def stop_read(self, duration: int = 1):
        """在指定周期内停止读取（拉低read.ready）"""
        self.write_read(duration)


    async def send_basic_write(self, trans_count=5):
        """ 发送一系列随机的写请求。验证基本的FIFO功能。"""
        for i in range (0, trans_count):
            trans = WayLookup_trans()
            trans.randomize(
                itlb_exception_0=0,
                itlb_exception_1=0
            )
            self.write_write_trans(trans)





    async def seq_flush(self, trans_count=5):
        """ 验证flush功能：写入部分数据 -> flush -> 再写入数据。"""
        self.send_basic_write(random.randint(10,20))
        await self.delay(random.randint(5,8))
        await self.do_flush(duration=1)
        self.send_basic_write(random.randint(10,20))

    async def seq_gpf_stall(self):
        """
        核心测试点：验证GPF stall逻辑。
        1. 发送一个带GPF的transaction。
        2. 立即发送一个普通transaction。
        3. 期望普通transaction被stall，直到GPF被读取。
        """
        # flush
        await self.do_flush(duration=1)
        await self.delay(5)


        # 发送gpf，并停止读取，此时gpf应当一直在waylookup中
        self.stop_read(20)
        gpf_trans = WayLookup_trans().randomize(itlb_exception_0=2)
        self.write_write_trans(gpf_trans)
        # await self.delay(1) # 确保gpf_trans被agent的driver处理

        # 发送普通trans，该trans不应该被写入
        self.send_basic_write(1)

        # 等gpf被读出后，trans才应该被写入

    async def seq_bypass(self):
        """
        核心测试点：验证GPF stall逻辑。
        1. 发送一个带GPF的transaction。
        2. 立即发送一个普通transaction。
        3. 期望普通transaction被stall，直到GPF被读取。
        """
        # flush
        await self.do_flush(duration=1)
        await self.delay(5)

        # 发送普通trans，该trans应当立即读出
        self.send_basic_write(1)
