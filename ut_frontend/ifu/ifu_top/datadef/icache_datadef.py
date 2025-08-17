from toffee import Agent
from ..bundle import ICacheInterCtrlBundle

class ICacheResp():
	def __init__(self):
		self.itlb_pbmts = [0, 0]
		self.exceptions = [0, 0]
		self.vaddrs = [0, 0]
		self.pmp_mmios = [False, False]
		self.paddr = 0
		self.VS_non_leaf_PTE = False
		self.data = 0
		self.backend_exception = False
		self.double_line = False
		self.gpaddr = 0
		self.icache_valid = True


class ICacheStatusResp():
	def __init__(self):
		self.ready = True
		self.resp = ICacheResp()
