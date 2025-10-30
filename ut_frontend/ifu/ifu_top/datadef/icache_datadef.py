from toffee import Agent
from ..bundle import ICacheInterCtrlBundle
from ..commons import randbool, calc_double_line, PREDICT_WIDTH, calc_cut_ptr, calc_blk_length
from random import randint
from .ftq_datadef import FTQQuery
from ..instr_utils import construct_instrs_with_jump_idx, rebuild_cacheline_from_parts

class ICacheResp():
	def __init__(self):
		self.itlb_pbmts = [0, 0]
		self.pmp_mmios = [False, False]
		self.exceptions = [0, 0]
		self.vaddrs = [0, 0]
		self.paddr = 0
		self.VS_non_leaf_PTE = True
		self.data = 0
		self.backend_exception = False
		self.double_line = False
		self.gpaddr = 0
		self.icache_valid = True
  
	def __str__(self):
		return (
			f"{self.__class__.__name__}(\n"
			f"  itlb_pbmts={self.itlb_pbmts},\n"
			f"  pmp_mmios={self.pmp_mmios},\n"
			f"  exceptions={self.exceptions},\n"
			f"  vaddrs={self.vaddrs},\n"
			f"  paddr={self.paddr},\n"
			f"  VS_non_leaf_PTE={self.VS_non_leaf_PTE},\n"
			f"  data={self.data},\n"
			f"  backend_exception={self.backend_exception},\n"
			f"  double_line={self.double_line},\n"
			f"  gpaddr={self.gpaddr},\n"
			f"  icache_valid={self.icache_valid}\n"
			f")"
		)
  
	def randomize(self, ftq_req: FTQQuery):
		# itlb pbmt and pmp_mmio won't be changed
		self.exceptions = [0 if randbool(rate=80) else randint(1, 3) for _ in range(2)]
		self.vaddrs[0] = ftq_req.startAddr 
		self.vaddrs[1] = ftq_req.nextlineStart 
		self.paddr = 0x18151192 # not useful when encountering non mmioX
		self.double_line = calc_double_line(ftq_req.startAddr)
		self.gpaddr = randint(0, (1 << 56) -1)
		self.icache_valid = True
		self.backend_exception = randbool(rate=70)
		
		data_construction = randint(0, 99)
		jmp_idx = ftq_req.ftqOffset.offsetIdx if ftq_req.ftqOffset.exists else PREDICT_WIDTH
		seq_end_idx = min(PREDICT_WIDTH, jmp_idx)
		safe_jmp_idx = max(0, seq_end_idx)
		if data_construction < 40:
			# 无预测错误，也即ret,jalr,jal错误不存在，也不存在target, valid, non cfi问题
			instrs = construct_instrs_with_jump_idx(safe_jmp_idx)
		elif data_construction < 50:
			# in this case, construct random of jal err 	
			instrs = construct_instrs_with_jump_idx(randint(0, max(0, safe_jmp_idx-1)), 2)
		elif data_construction < 60:
			instrs = construct_instrs_with_jump_idx(randint(0, max(0, safe_jmp_idx-1)), 4)
		elif data_construction < 70:
			instrs = construct_instrs_with_jump_idx(randint(0, max(0, safe_jmp_idx-1)), 3)
		elif data_construction < 90:
			instrs = construct_instrs_with_jump_idx(randint(0, min(PREDICT_WIDTH, safe_jmp_idx+1)))
		else:
			#  this is a different target err producer
			instrs = construct_instrs_with_jump_idx(safe_jmp_idx, cfi_res=-1, imm=ftq_req.nextStartAddr + 40)
   
		self.data = rebuild_cacheline_from_parts(ftq_req.startAddr, instrs)


class ICacheStatusResp():
	def __init__(self):
		self.ready = True
		self.resp = ICacheResp()
  
	def randomize(self, ftq_req: FTQQuery):
		self.ready = randbool(rate=80)
		self.resp.randomize(ftq_req)
  
	def __str__(self):
		return (
			f"{self.__class__.__name__}(\n"
			f"  ready={self.ready},\n"
			f"  resp={self.resp}\n"
			f")"
		)
		
		
