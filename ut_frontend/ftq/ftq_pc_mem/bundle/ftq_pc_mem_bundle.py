from toffee import Bundle, Signals, Signal

class Rdata1Bundle(Bundle):
	_startAddr, _nextLineAddr, _fallThruError = Signals(3)

class Rdata2Bundle(Bundle):
	_startAddr, _nextLineAddr = Signals(2)
	
class Rdata3Bundle(Bundle):
	_startAddr = Signal()
		
class IfuPtrBundle(Bundle):
	_w_value, Plus1_w_value, Plus2_w_value = Signals(3)
	_rdata = Rdata1Bundle.from_prefix("_rdata")
	Plus1_rdata = Rdata1Bundle.from_prefix("Plus1_rdata")
	Plus2_rdata = Rdata3Bundle.from_prefix("Plus2_rdata")

class PfPtrBundle(Bundle):
	_w_value, Plus1_w_value = Signals(2)
	_rdata = Rdata2Bundle.from_prefix("_rdata")
	Plus1_rdata = Rdata2Bundle.from_prefix("Plus1_rdata")

class CommPtrBundle(Bundle):
	_w_value, Plus1_w_value = Signals(2)
	_rdata = Rdata3Bundle.from_prefix("_rdata")
	Plus1_rdata = Rdata3Bundle.from_prefix("Plus1_rdata")

class WdataBundle(Bundle):
	_startAddr, _nextLineAddr, _fallThruError = Signals(3)

class IoBundle(Bundle):
	_wen, _waddr = Signals(2)
	_ifuPtr  = IfuPtrBundle.from_prefix("_ifuPtr")
	_pfPtr   = PfPtrBundle.from_prefix("_pfPtr")
	_commPtr = CommPtrBundle.from_prefix("_commPtr")
	_wdata   = WdataBundle.from_prefix("_wdata")

class FtqPcMemBundle(Bundle):
	io = IoBundle.from_prefix("io")
	clock, reset = Signals(2)