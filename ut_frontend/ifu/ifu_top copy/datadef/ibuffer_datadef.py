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
			f"	illegals={self.illegalInstrs}\n"
			")"
		)


	def __eq__(self, other):
		if not isinstance(other, ToIbuffer):
			print(f"[≠] type mismatch: self is ToIbuffer, other is {type(other)}")
			return False

		diffs = []

		# --- 基本数组长度一致性检查 ---
		def _len(name):
			return len(getattr(self, name)), len(getattr(other, name))

		for arr in ["instrs", "illegalInstrs", "exceptionTypes"]:
			ls, lo = _len(arr)
			if ls != lo:
				diffs.append(f"Mismatch in length: {arr}: {ls} != {lo}")

		# 若长度不等，先按最短长度比对，避免 IndexError
		n_instrs = min(len(self.instrs), len(other.instrs))
		n_illegal = min(len(self.illegalInstrs), len(other.illegalInstrs))

		# --- 指令逐项比对（跳过 illegal==2 的槽位）---
		for i in range(min(n_instrs, n_illegal)):
			il1 = self.illegalInstrs[i]
			il2 = other.illegalInstrs[i]
			if il1 == 2 or il2 == 2:
				continue
			if il1 != il2:
				diffs.append(f"illegalInstrs[{i}]: {il1} != {il2}")
			v1, v2 = self.instrs[i], other.instrs[i]
			if v1 != v2:
				# 以 16 进制展示更直观（按需可改）
				diffs.append(f"instrs[{i}]: {v1:#06x} != {v2:#06x}")

		# --- 逐字段比对 ---
		scalar_fields = [
			"valid", "pds", "ftqPtr", "foldpcs",
			"backendException", "enqEnable", "instr_valids", "exceptionTypes","instrValids"
		]
		for name in scalar_fields:
			a = getattr(self, name, None)
			b = getattr(other, name, None)
			if a != b:
				diffs.append(f"{name}: {a} != {b}")

		if diffs:
			print("[ToIbuffer diff]")
			for d in diffs:
				print(" -", d)
			return False

		return True

class ToBackendGpaddrMem():
	def __init__(self):
		self.waddr = 0
		self.wen = False
		self.gpaddr = 0
		self.isForVSnonLeafPTE = False
	
	def __eq__(self, value):
		if type(value) != ToBackendGpaddrMem:
			return False
		if self.wen != value.wen:
			return False
		if not self.wen:
			return True
		return self.gpaddr == value.gpaddr and self.waddr == value.waddr

class ToIbufferAllRes():
	def __init__(self):
		self.toBackendGpaddrMem = ToBackendGpaddrMem()
		self.toIbuffer = ToIbuffer()

	def __eq__(self, value):
		if type(value) != ToIbufferAllRes:
			return False
		
		# TODO: add comparation of toBackendGpaddrMem
		return self.toIbuffer == value.toIbuffer

	def __str__(self):
		return f"toIbuffer: {self.toIbuffer}"