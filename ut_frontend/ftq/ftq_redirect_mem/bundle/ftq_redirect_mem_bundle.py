from toffee import Bundle, Signals, Signal

class _0Bundle(Bundle):
    _0, _1, _2 = Signals(3)

class FlagAndValueBundle(Bundle):
    _flag, _value = Signals(2)

class _1Bundle(Bundle):
    _histPtr = FlagAndValueBundle.from_prefix("_histPtr")
    _TOSW = FlagAndValueBundle.from_prefix("_TOSW")
    _TOSR = FlagAndValueBundle.from_prefix("_TOSR")
    _NOS = FlagAndValueBundle.from_prefix("_NOS")
    _ssp, _sctr = Signals(2)

class Rdata0Bundle(_1Bundle):
    _topAddr = Signal()

class Rdata1Bundle(_1Bundle):
    _sc_disagree_0, _sc_disagree_1 = Signals(2)

class Rdata2Bundle(Bundle):
    _histPtr_value = Signal()

class Wdata0Bundle(_1Bundle):
    _topAddr = Signal()
    _sc_disagree_0, _sc_disagree_1 = Signals(2)

class IoBundle(Bundle):
    _wen_0, _waddr_0 = Signals(2)
    _ren = _0Bundle.from_prefix("_ren")
    _raddr = _0Bundle.from_prefix("_raddr")
    _rdata_2 = Rdata2Bundle.from_prefix("_rdata_2")
    _rdata_1 = Rdata1Bundle.from_prefix("_rdata_1")
    _rdata_0 = Rdata0Bundle.from_prefix("_rdata_0")
    _wdata_0 = Wdata0Bundle.from_prefix("_wdata_0")

class FTQPcMemBundle(Bundle):
    clock, reset = Signals(2)
    io = IoBundle.from_prefix("io")
