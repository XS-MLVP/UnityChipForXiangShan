
from .pyxspcomm import *
import sys
import traceback

# handle exception when callback
def cb_exception_handler(func):
    print(f"\033[31mCallback Error in \033[0m{func.__qualname__}: ", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("", file=sys.stderr)

# PinBind
PinBind__old__setattr__ = PinBind.__setattr__
def PinBind__setattr__(self: PinBind, name, value):
    if name != "value":
        return PinBind__old__setattr__(self, name, value)
    return self.Set(value)

PinBind.__setattr__ = PinBind__setattr__


# XData
XData_old__init__ = XData.__init__
def XData__init__(self: XData, width: int, direction = XData.In, raw_args = None):
    if raw_args is not None:
        return XData_old__init__(self, *(width, direction, *raw_args))
    return XData_old__init__(self, width, direction)

def XData__str__(self: XData):
    return f"XData(width={self.mWidth}, value=0x{self.String()})"

XData_old__setattr__ = XData.__setattr__
def XData__setattr__(self: XData, name, value):
    if name != "value":
        return XData_old__setattr__(self, name, value)
    if type(value) is bool:
        return self.Set(1 if value else 0)
    bit_length = self.W()
    if type(value) is int:
        if bit_length <= 64:
            return self.Set(value)
        # add extra byte for python `to_bytes` method to contain sign bit
        # the extra bits will be truncated in `SetBytes` method
        self.SetBytes(value.to_bytes((self.W() + 15) // 8, byteorder='little', signed=True))
    else:
        return self.Set(value)

XData_old__getattribute__ = XData.__getattribute__
XData_old_U = XData.U
def XData__getattribute__(self: XData, name):
    if name != "value":
        return XData_old__getattribute__(self, name)
    bit_length = self.W()
    if bit_length <= 64:
        data = XData_old_U(self)
    else:
        data = int.from_bytes(self.GetBytes(), byteorder='little', signed=False)
    return data

XData_old_S = XData.S
def XData_S(self: XData):
    bit_length = self.W()
    if bit_length <= 64:
        data = XData_old_S(self)
    else:
        bytes_list = bytearray(self.GetVU8())
        bit_length = len(bytes_list)
        sign_pos = (bit_length - 1) // 8
        sign_off = (bit_length - 1) %  8
        sing_val = 1 << sign_off
        if (bytes_list[sign_pos] & sing_val != 0):
            # Negative
            bytes_list[sign_pos] |= (~(sing_val | (sing_val - 1))) & 0xff
            sign_pos += 1
            while sign_pos < bit_length:
                bytes_list[sign_pos] = 0xff
                sign_pos +=1
        data = int.from_bytes(bytes(bytes_list), byteorder='little', signed=True)
    return data

def XData_U(self: XData):
    return self.value

XData_old_Set = XData.Set
def XData_Set(self:XData, value):
    if isinstance(value, bytes):
        self.SetBytes(value)
        return self
    return XData_old_Set(self, value)

def XData__getitem__(self: XData, key):
    return self.At(key).AsInt32()

def XData__setitem__(self: XData, key, value):
    self.At(key).Set(value)

def XDataBindDPIName(self: XData, dut, name):
    self.mName = name
    return self.BindDPIPtr(dut.GetDPIHandle(name, 0), dut.GetDPIHandle(name, 1))

XData_old__eq__ = XData.__eq__
def XData__eq__(self: XData, other):
    assert isinstance(other, XData), "XData Only support compare with XData. Do you missed `.value`?"
    return XData_old__eq__(self, other)

XData.__init__ = XData__init__
XData.__str__ = XData__str__
XData.__setattr__ = XData__setattr__
XData.__getattribute__ = XData__getattribute__
XData.__getitem__ = XData__getitem__
XData.__setitem__ = XData__setitem__
XData.S = XData_S
XData.U = XData_U
XData.Set = XData_Set
XData.BindDPIName = XDataBindDPIName
XData.__eq__ = XData__eq__

# XPort
XPort_old__init__ = XPort.__init__
def XPort__init__(self: XPort, prefix = ""):
    return XPort_old__init__(self, prefix)

def XPort__str__(self: XPort):
    return f"XPort(prefix={self.prefix}, size={self.PortCount()})"

def XPort__getitem__(self: XPort, key):
    return self.Get(key)

def XPort__setitem__(self: XPort, key, value):
    self.Get(key).value = value

XPort.__init__ = XPort__init__
XPort.__str__ = XPort__str__
XPort.__getitem__ = XPort__getitem__
XPort.__setitem__ = XPort__setitem__

# XClock
class xclock_cb_step(cb_int_bool):
    """XClock step call back"""
    def __init__(self, func):
        cb_int_bool.__init__(self)
        self.func = func
    def call(self, dump: bool):
        try:
            return self.func(dump)
        except Exception as e:
            cb_exception_handler(self.func)
            assert(0)
            
class xclock_cb_step_rf(cb_void_u64_voidp):
    """XClock step Ris/Fal call back"""
    def __init__(self, dut, func, args, kwargs):
        cb_void_u64_voidp.__init__(self)
        self.func = func
        self.dut = dut
        self.args = args
        self.kwargs = kwargs
    def call(self, cycle: int, args=None):
        try:
            return self.func(cycle, *self.args, **self.kwargs)
        except Exception as e:
            XClock_Add_Exception(self.dut, e)

# Async
import asyncio

timestamp = 0
def tick_timestamp():
    global timestamp
    timestamp = (timestamp + 1) % 2**32

def has_unwait_task():
    for task in asyncio.all_tasks():
        if "XClock_RunStep" not in task.__repr__() and "wait_for" not in task.__repr__():
            return True
    return False

async def tick_clock_ready():
    global timestamp
    timestamp_old = timestamp
    await asyncio.sleep(0)
    while has_unwait_task() or timestamp_old != timestamp:
        await asyncio.sleep(0)
        timestamp_old = timestamp



XClock_old_init__ = XClock.__init__
def XClock__init__(self, step_func, dut=None):
    self._step_event = asyncio.Event()
    self._step_event.clear()
    if callable(step_func):
        fc = xclock_cb_step(step_func)
        fc.set_force_callable()
        return XClock_old_init__(self, fc.__disown__())
    assert isinstance(step_func, int), "step_func must be callable or int"
    assert isinstance(dut, int), "dut must be int"
    return XClock_old_init__(self, step_func, dut)

XClock.__init__ = XClock__init__

def XClock__getEvent(self):
    return self._step_event

XClock.getEvent = XClock__getEvent

XClock_old_StepRis = XClock.StepRis
XClock_old_StepFal = XClock.StepFal
def XClock_StepRis(self, call_back, args=(), kwargs={}):
    if callable(call_back):
        fc = xclock_cb_step_rf(self, call_back, args, kwargs)
        fc.set_force_callable()
        return XClock_old_StepRis(self, fc.__disown__(), None, call_back.__name__)
    assert isinstance(call_back, int), "call_back must be callable or int"
    if args:
        assert isinstance(args, int), "args must be int"
    else:
        args = 0
    return XClock_old_StepRis(self, call_back, args, "C_RIS_%x_%x" % (call_back, args))

def XClock_StepFal(self, call_back, args=(), kwargs={}):
    if callable(call_back):
        fc = xclock_cb_step_rf(self, call_back, args, kwargs)
        fc.set_force_callable()
        return XClock_old_StepFal(self, fc.__disown__(), None, call_back.__name__)
    assert isinstance(call_back, int), "call_back must be callable or int"
    if args:
        assert isinstance(args, int), "args must be int"
    else:
        args = 0
    return XClock_old_StepFal(self, call_back, args, "C_FAL_%x_%x" % (call_back, args))

def XClock_Add_Exception(self, exception):
    if getattr(self, "exceptions", None) is None:
        self.exceptions = [exception]
    else:
        self.exceptions.append(exception)

def XClock_Check_Exceptions(self):
    if getattr(self, "exceptions", None) is None:
        return
    print("[Error] Find %d exceptions in cycle[%d], raise the first one" % (len(self.exceptions), self.clk), file=sys.stderr)
    raise self.exceptions[0]

XClock.StepRis = XClock_StepRis
XClock.StepFal = XClock_StepFal

XClock__old_Step = XClock.Step
def XClock_Step(self, cycle: int):
    for i in range(cycle):
        XClock__old_Step(self, 1)
        XClock_Check_Exceptions(self)
        self._step_event.set()
        self._step_event.clear()

async def XClock_AStep(self, cycle: int):
    for i in range(cycle):
        await self._step_event.wait()

async def XClock_ACondition(self, condition):
    assert callable(condition), "condition must be callable"
    while not condition():
        await self._step_event.wait()

async def XClock_ANext(self):
    return await self._step_event.wait()

async def XClock_RunStep(self, cycle: int):
    for i in range(cycle):
        await tick_clock_ready()
        XClock_Step(self, 1)
        await asyncio.sleep(0)

XClock.Step = XClock_Step
XClock.AStep = XClock_AStep
XClock.ACondition = XClock_ACondition
XClock.ANext =XClock_ANext
XClock.RunStep = XClock_RunStep


class Event:
    def __init__(self):
        self.event = asyncio.Event()

    async def wait(self):
        await self.event.wait()
        tick_timestamp()

    def set(self):
        self.event.set()

    def clear(self):
        self.event.clear()


class Queue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def put(self, value):
        await self.queue.put(value)
        tick_timestamp()

    async def get(self):
        ret = await self.queue.get()
        tick_timestamp()
        return ret

    def put_nowait(self, value):
        self.queue.put_nowait(value)

    def get_nowait(self):
        return self.queue.get_nowait()

async def sleep(delay: float):
    await asyncio.sleep(delay)
    tick_timestamp()


# XPin

class XPin:
    def __init__(self, xdata, event):
        self.xdata = xdata
        self.event = event

    def __str__(self):
        return f"XPin({self.xdata})"

    def __getattribute__(self, name):
        if name == "xdata" or name == "event":
            return object.__getattribute__(self, name)
        return self.xdata.__getattribute__(name)

    def __setattr__(self, name, value):
        if name == "xdata" or name == "event":
            return object.__setattr__(self, name, value)
        return self.xdata.__setattr__(name, value)

    def __getitem__(self, key):
        return self.xdata[key]

    def __setitem__(self, key, value):
        self.xdata[key] = value

    def __eq__(self, other):
        assert isinstance(other, XPin), "XPin Only support compare with XPin. Do you missed `.value`?"
        return self.xdata == other.xdata

__version__ = version()
