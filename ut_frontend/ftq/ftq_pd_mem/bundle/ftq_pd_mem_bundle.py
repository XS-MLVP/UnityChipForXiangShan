from toffee import Bundle, Signals, Signal

class RenAndRaddrBundle(Bundle):
    _0, _1 = Signals(2)

class MaskBundle(Bundle):
    _0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15 = Signals(16)

class BitsBundle(Bundle):
    _0, _1, _2 = Signals(3)

class InfoBundle(Bundle):
    _valid = Signal()
    _bits = BitsBundle.from_prefix("_bits")

class JmpBundle(Bundle):
    Info = InfoBundle.from_prefix("Info")
    Offset = Signal()

class Rdata0Bundle(Bundle): 
    _brMask = MaskBundle.from_prefix("_brMask")
    _jmp = JmpBundle.from_prefix("_jmp")
    _rvcMask = MaskBundle.from_prefix("_rvcMask")

class Rdata1AndWdato0Bundle(Bundle):
    _brMask = MaskBundle.from_prefix("_brMask")
    _jmp = JmpBundle.from_prefix("_jmp")
    _rvcMask = MaskBundle.from_prefix("_rvcMask")
    _jalTarget = Signal()

class IoBundle(Bundle):
    _ren = RenAndRaddrBundle.from_prefix("_ren")
    _raddr = RenAndRaddrBundle.from_prefix("_raddr")
    _rdata_0 = Rdata0Bundle.from_prefix("_rdata_0")
    _rdata_1 = Rdata1AndWdato0Bundle.from_prefix("_rdata_1")
    _wdata_0 = Rdata1AndWdato0Bundle.from_prefix("_wdata_0")
    _wen_0, _waddr_0 = Signals(2)

class FTQPcMemBundle(Bundle):
    clock, reset = Signals(2)
    io = IoBundle.from_prefix("io")