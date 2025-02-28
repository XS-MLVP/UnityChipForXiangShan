from toffee import Env
from ..bundle import PreDecodeBundle
from dut.PreDecode import DUTPreDecode
from ..agent import PreDecodeAgent

class PreDecodeEnv(Env):

    def __init__(self, dut: DUTPreDecode):
        super().__init__()
        bundle = PreDecodeBundle.from_prefix("").bind(dut)
        bundle.io._in_bits_data.set_write_mode_as_imme()
        self.agent = PreDecodeAgent(bundle)

