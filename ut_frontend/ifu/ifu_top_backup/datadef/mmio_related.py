from .ftq_datadef import FTQIdx

class ToUncache():
	def __init__(self):
		self.addr = 0
		self.valid = True

class FromUncache():
	def __init__(self):
		self.data = 0
		self.valid = True
	

class ITLBReq():
	def __init__(self):
		self.vaddr = 0
		self.valid = True

class Excp():
	def __init__(self):
		self.gpfInstr = False
		self.afInstr = False
		self.pfInstr = False

class ITLBResp():
	def __init__(self):
		self.valid = True
		self.paddr = 0
		self.pbmt = 0
		self.gpaddr = 0
		self.excp = Excp()
		self.isForVSnonLeafPTE = False


class PMPResp():
	def __init__(self):
		self.instr = 0
		self.mmio = True


class RobCommit():
	def __init__(self):
		self.valid = False
		self.ftqIdx = FTQIdx()
		self.ftqOffset = 0