from .ftq_datadef import FTQIdx
from enum import IntEnum
from dataclasses import dataclass
from random import randint
from ..commons import calc_double_line, randbool

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

	def __eq__(self, value):
		if type(value) != ITLBReq:
			return False
		if self.valid != value.valid:
			return False
		if not self.valid:
			return True
		return self.vaddr == value.vaddr

	def __repr__(self):
		return f"vaddr: {self.vaddr}\nvalid: {self.valid}\n"
 
class Excp():
	def __init__(self):
		self.pfInstr = False
		self.gpfInstr = False
		self.afInstr = False
	
	def set_excp_one_hot(self, num):
		self.pfInstr = False
		self.gpfInstr = False
		self.afInstr = False
		if num == 1:
			self.pfInstr = True
		elif num == 2:
			self.gpfInstr = True
		elif num == 3:
			self.afInstr = True
			

class ExceptionType():
	NONE = 0
	PF = 1
	GPF = 2
	AF = 3

class ITLBResp():

	def __init__(self):
		self.valid = True
		self.paddr = 0
		self.pbmt = 0
		self.gpaddr = 0
		self.excp = Excp()
		self.isForVSnonLeafPTE = False

	def get_excp_code(self):
		return ExceptionType.PF if self.excp.pfInstr else ExceptionType.GPF if self.excp.gpfInstr else ExceptionType.AF if self.excp.afInstr else ExceptionType.NONE


class PMPResp():
	def __init__(self):
		self.instr = False
		self.mmio = True


class RobCommit():
	def __init__(self):
		self.valid = False
		self.ftqIdx = FTQIdx()
		self.ftqOffset = 0

class MMIOCycleInfo():
	def __init__(self):
		self.exceptions = [False, False]
		self.ftq_start_addr = 0
		self.ftq_idx: FTQIdx = FTQIdx()
		self.csr_fs_is_off = False
		self.icache_paddr = 0
		self.icache_pmp_mmios = [False, False]
		self.icache_itlb_pbmts = [False, False]
	
	def workable_randomize(self):
		self.ftq_start_addr = randint(0, (1 << 50) -1)
		self.csr_fs_is_off = randbool()
		self.ftq_idx.flag = randbool()
		self.ftq_idx.value = randint(0, 15)
		into_mmio_space_type = randint(0, 2)
		if into_mmio_space_type == 0:
			self.icache_pmp_mmios[0] = True
		elif into_mmio_space_type == 1:
			self.icache_itlb_pbmts[0] = PbmtAssist.NC
		else:
			self.icache_itlb_pbmts[0] = PbmtAssist.IO
		if calc_double_line(self.ftq_start_addr):
			self.icache_pmp_mmios[1] = self.icache_pmp_mmios[0]
			self.icache_itlb_pbmts[1] = self.icache_itlb_pbmts[0]
		addr_type = randint(0, 7)
		self.icache_paddr = randint(0, (1 << 48) - 1)
		if addr_type < 3:
			self.icache_paddr |= 6


class MMIOReq():

	def __init__(self):
		self.last_commited = False
		self.to_uncache_ready = False
		self.from_uncache: FromUncache = FromUncache()
		self.itlb_req_ready = False
		self.itlb_resp: ITLBResp = ITLBResp()
		self.pmp_resp: PMPResp = PMPResp()
		self.rob_commits: list[RobCommit] = [RobCommit() for i in range(8)]
		self.to_ibuffer_ready = True
	
	def randomize_with_cycles(self, cycle_info: MMIOCycleInfo):
		self.last_commited = randbool(rate=70)
		self.to_uncache_ready = randbool(rate=70)
		self.from_uncache.valid = randbool(rate=70)
		self.from_uncache.data = randint(0, (1 << 32) - 1)
		self.itlb_req_ready = randbool(rate=70)
		self.itlb_resp.valid = randbool(rate=70)
		self.itlb_resp.pbmt = cycle_info.icache_itlb_pbmts[0] if randbool(rate=80) else cycle_info.icache_itlb_pbmts[0] + 1
		self.itlb_resp.paddr = randint(0, (1 << 48) - 1)
		self.itlb_resp.gpaddr = randint(0, (1 << 56) -1)
		self.itlb_resp.excp.set_excp_one_hot(randint(0, 3))
		self.pmp_resp.instr = randbool(rate=30)
		self.pmp_resp.mmio = cycle_info.icache_pmp_mmios[0] if randbool(rate=70) else not cycle_info.icache_pmp_mmios[0]
		construct_commit = randbool(rate=80)
		if construct_commit:
			pos = randint(0, 7)
			self.rob_commits[pos].valid = True
			self.rob_commits[pos].ftqIdx = cycle_info.ftq_idx
			self.rob_commits[pos].ftqOffset = 0 if randbool(rate=80) else randint(1, 15)
		else:
			self.rob_commits = [RobCommit() for i in range(8)]
		self.to_ibuffer_ready = randbool(rate=70)





class MMIOToIbufferFTQ():
	def __init__(self):
		self.br_type = 0
		self.is_rvc = False
		self.is_call = False
		self.is_ret = False
		self.expd_instr = 0
		self.ill = 0
  
	def __repr__(self):
		return f"""br_type: {self.br_type}
rvc: {self.is_rvc}
call: {self.is_call}
ret: {self.is_ret}
expd_instr: {self.expd_instr}
ill: {self.ill}"""

	def cmp_ill_instr(self, ill, instr):
		if ill == 2 or self.ill == 2:
			return True
		return self.ill == ill and self.expd_instr == instr
 
	def __eq__(self, value):
		if type(value) != MMIOToIbufferFTQ:
			return False
		# if self.ill == 2 or 
		return self.br_type == value.br_type and self.is_rvc == value.is_rvc and self.is_call == value.is_call \
			and self.is_ret == value.is_ret and self.cmp_ill_instr(value.ill, value.expd_instr)
  
class MMIOState(IntEnum):
    STATE_IDLE = 0
    STATE_WAIT_LAST_CMT = 1
    STATE_SEND_REQ = 2
    STATE_WAIT_RESP = 3
    STATE_SEND_TLB = 4
    STATE_TLB_RESP = 5
    STATE_SEND_PMP = 6
    STATE_RESEND_REQ = 7
    STATE_WAIT_RESEND_RESP = 8
    STATE_WAIT_COMMIT = 9
    STATE_COMMITED = 10

class PbmtAssist():
    NC = 1
    IO = 2

    def is_uncache(self, num):
        return num == self.NC or num == self.IO
	

		