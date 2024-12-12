from toffee import Bundle, Signals, Signal

class RVCExpanderIOBundle(Bundle):
	_in, _fsIsOff ,_out_bits,_ill = Signals(4)
