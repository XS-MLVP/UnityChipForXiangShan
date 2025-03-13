from .ftq_datadef import FTQIdx


class PDInfo():
	isRVC = False
	brType = 0

class ToIbuffer():
	valid = False
	pds = [PDInfo() for i in range(16)]
	ftqPtr = FTQIdx()
	triggereds = [0 for i in range(16)]
	isLastInFtqEntrys = [False for i in range(16)]
	exceptionTypes = [0 for i in range(16)]
	instrs = [0 for i in range(16)]
	foldpcs = [0 for i in range(16)]
	illegalInstrs = [False for i in range(16)] 
	crossPageIPFFixs = [False for i in range(16)]
	ftqOffset = [False for i in range(16)]
	backendException = False
	enqEnable = 0
	instr_valids = 0

class ToBackendGpaddrMem():
	waddr = 0
	wen = False
	gpaddr = 0
	isForVSnonLeafPTE = False

class ToIbufferAllRes():
	toBackendGpaddrMem = ToBackendGpaddrMem()
	toIbuffer = ToIbuffer()