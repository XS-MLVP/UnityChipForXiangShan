from toffee import Bundle, Signals, Signal


class _00Bundle(Bundle):
    _0 = Signal()


class _0Bundle(Bundle):
    _flag, _value = Signals(2)


class _1Bundle(Bundle):
    _readPtr = _0Bundle.from_prefix("_readPtr")
    _writePtr = _0Bundle.from_prefix("_writePtr")
    _io_write_ready = _00Bundle.from_prefix("_io_write_ready")
    _entries_30_waymask_0 = Signal()


class _2Bundle(Bundle):
    _0, _1 = Signals(2)


class _3Bundle(Bundle):
    _exception = _2Bundle.from_prefix("_exception")
    _pbmt = _2Bundle.from_prefix("_pbmt")


class _4Bundle(Bundle):
    _waymask = _2Bundle.from_prefix("_waymask")
    _vSetIdx = _2Bundle.from_prefix("_vSetIdx")
    _ptag = _2Bundle.from_prefix("_ptag")
    _meta_codes = _2Bundle.from_prefix("_meta_codes")
    _itlb = _3Bundle.from_prefix("_itlb")


class _5Bundle(Bundle):
    _isForVSnonLeafPTE, _gpaddr = Signals(2)


class _6Bundle(Bundle):
    _gpf = _5Bundle.from_prefix("_gpf")
    _entry = _4Bundle.from_prefix("_entry")


class _7Bundle(Bundle):
    _bits = _6Bundle.from_prefix("_bits")
    _valid, _ready = Signals(2)


class _8Bundle(Bundle):
    _corrupt, _vSetIdx, _blkPaddr, _waymask = Signals(4)


class _9Bundle(Bundle):
    _bits = _8Bundle.from_prefix("_bits")
    _valid = Signal()


class _10Bundle(Bundle):
    _update = _9Bundle.from_prefix("_update")
    _write = _7Bundle.from_prefix("_write")
    _read = _7Bundle.from_prefix("_read")
    _flush = Signal()


class WayLookupBundle(Bundle):
    io = _10Bundle.from_prefix("io")
    WayLookup = _1Bundle.from_prefix("WayLookup")
    reset, clock = Signals(2)
