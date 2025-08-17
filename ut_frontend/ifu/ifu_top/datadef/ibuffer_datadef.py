from .ftq_datadef import FTQIdx, ResPd


# class PDInfo():
# 	def __init__(self):
# 		self.isRVCs = [False for i in range()
# 		self.brType = 0

class ToIbuffer():
	def __init__(self):
		self.valid = False
		self.pds = ResPd()
		self.ftqPtr = FTQIdx()
		self.triggereds = [0 for i in range(16)]
		self.isLastInFtqEntrys = [False for i in range(16)]
		self.exceptionTypes = [0 for i in range(16)]
		self.instrs = [0 for i in range(16)]
		self.foldpcs = [0 for i in range(16)]
		self.illegalInstrs = [False for i in range(16)] 
		self.crossPageIPFFixs = [False for i in range(16)]
		self.ftqOffset = [False for i in range(16)]
		self.backendException = False
		self.enqEnable = 0
		self.instr_valids = 0

	def __str__(self):
		return (
			"ToIbuffer(\n"
			f"  valid={self.valid},\n"
			f"  pds={self.pds},\n"
			f"  ftqPtr={self.ftqPtr},\n"
			f"  instrs={self.instrs},\n"
			f"  foldpcs={self.foldpcs},\n"
			f"  backendException={self.backendException},\n"
			f"  enqEnable={self.enqEnable},\n"
			f"  instr_valids={self.instr_valids},\n"
			f"  exceptionTypes={self.exceptionTypes}\n"
			")"
		)


	def __eq__(self, value):
		if type(value) != ToIbuffer:
			return False
		
		return self.valid == value.valid and self.pds == value.pds and self.ftqPtr == value.ftqPtr and self.instrs == value.instrs and self.foldpcs == value.foldpcs \
			and self.backendException == value.backendException and self.enqEnable == value.enqEnable and self.instr_valids == value.instr_valids and self.exceptionTypes == value.exceptionTypes

class ToBackendGpaddrMem():
	def __init__(self):
		self.waddr = 0
		self.wen = False
		self.gpaddr = 0
		self.isForVSnonLeafPTE = False

class ToIbufferAllRes():
	def __init__(self):
		self.toBackendGpaddrMem = ToBackendGpaddrMem()
		self.toIbuffer = ToIbuffer()

	def __eq__(self, value):
		if type(value) != ToIbufferAllRes:
			return False
		return self.toIbuffer == value.toIbuffer