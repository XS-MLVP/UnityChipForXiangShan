from toffee import Bundle, Signals, Signal

class aBundle(Bundle):
    _0, _1 = Signals(2)

class BaseBundle(Bundle):
    _offset = Signal()
    _sharing = Signal()
    _valid = Signal()
    _lower = Signal()
    _tarStat = Signal()

class _0Bundle(Bundle):
    _isCall, _isRet, _isJalr, _valid = Signals(4)
    _brSlots_0 = BaseBundle.from_prefix("_brSlots_0")
    _tailSlot = BaseBundle.from_prefix("_tailSlot")
    pftAddr, _carry, _last_may_be_rvi_call = Signals(3)
    _strong_bias = aBundle.from_prefix("_strong_bias")

class IoBundle(Bundle):
    _raddr_0, ren_0 = Signals(2)
    _wen, _wdata_meta, _waddr = Signals(3)
    _rdata_0_ftb_entry = _0Bundle.from_prefix("_rdata_0_ftb_entry")
    _wdata_ftb_entry = _0Bundle.from_prefix("_wdata_ftb_entry")

class BoreBundle(Bundle):
    _addr = Signal()
    _addr_rd = Signal()
    _wdata = Signal()
    _wmask = Signal()
    _re = Signal()
    _we = Signal()
    _rdata = Signal()   
    _ack = Signal()
    _selectedOH = Signal()
    _array = Signal()

class BoreChildrenBundle(Bundle):
    _bore = BoreBundle.from_prefix("_bore")

class FtqMeta1rSramBundle(Bundle):
    clock, reset = Signals(2)
    io = IoBundle.from_prefix("io")
    boreChildrenBd = BoreChildrenBundle.from_prefix("boreChildrenBd")