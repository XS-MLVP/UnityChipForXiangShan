from .ftq_datadef import FTQIdx

class ToUncache():
	addr = 0
	valid = True

class FromUncache():
	data = 0
	valid = True
	

class ITLBReq():
	vaddr = 0
	valid = True

class Excp():
	gpfInstr = False
	afInstr = False
	pfInstr = False

class ITLBResp():
	valid = True
	paddr = 0
	pbmt = 0
	gpaddr = 0
	excp = Excp()
	isForVSnonLeafPTE = False


class PMPResp():
	instr = 0
	mmio = True


class RobCommit():
	valid = False
	ftqIdx = FTQIdx()
	ftqOffset = 0