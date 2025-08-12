from toffee import Bundle, Signals, Signal

class RenAndRaddrBundle(Bundle):
    _0, _1 = Signals(2)

class BrSlotsBundle(Bundle):
    _offset, _valid = Signals(2)

class TailSlotBundle(Bundle):
    _offset, _sharing, _valid = Signals(3)

class _0Bundle(Bundle):
    _isCall, _isRet, _isJalr = Signals(3)
    _brSlots_0 = BrSlotsBundle.from_prefix("_brSlots_0")
    _tailSlot = TailSlotBundle.from_prefix("_tailSlot")

class _1Bundle(Bundle):
    _isJalr = Signal()
    _brSlots_0 = BrSlotsBundle.from_prefix("_brSlots_0")
    _tailSlot = TailSlotBundle.from_prefix("_tailSlot")

class IoBundle(Bundle):
    _wen_0, _waddr_0 = Signals(2)
    _ren = RenAndRaddrBundle.from_prefix("_ren")
    _raddr = RenAndRaddrBundle.from_prefix("_raddr")
    _rdata_0 = _0Bundle.from_prefix("_rdata_0")
    _wdata_0 = _0Bundle.from_prefix("_wdata_0")
    _rdata_1 = _1Bundle.from_prefix("_rdata_1")

class FTQPcMemBundle(Bundle):
    clock, reset = Signals(2)
    io = IoBundle.from_prefix("io")