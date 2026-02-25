from toffee import Agent
from ..bundle import ICacheInterCtrlBundle
from ..commons import randbool, calc_double_line, PREDICT_WIDTH, calc_cut_ptr, calc_blk_length
from random import randint
from .ftq_datadef import FTQQuery
from ..instr_utils import construct_instrs_with_jump_idx, rebuild_cacheline_from_parts

class ICacheResp():
	def __init__(self, 
					itlb_pbmts=None,
					pmp_mmios=None,
					exceptions=None,
					vaddrs=None,
					paddr=0,
					VS_non_leaf_PTE=True,
					data=0,
					backend_exception=False,
					double_line=False,
					gpaddr=0,
					icache_valid=True,
					ftq_req: FTQQuery = None,
					init_as_valid= False
     			):

		self.itlb_pbmts = itlb_pbmts if itlb_pbmts is not None else [0, 0]
		self.pmp_mmios   = pmp_mmios if pmp_mmios is not None else [False, False]
		self.exceptions  = exceptions if exceptions is not None else [0, 0]
		self.vaddrs      = vaddrs if vaddrs is not None else [0, 0]

		self.paddr = paddr
		self.VS_non_leaf_PTE = VS_non_leaf_PTE
		self.data = data
		self.backend_exception = backend_exception
		self.double_line = double_line
		self.gpaddr = gpaddr
		self.icache_valid = icache_valid
		if init_as_valid and ftq_req is not None:
			self.init_as_valid(ftq_req)
          
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

	def init_as_valid(self, ftq_req: FTQQuery):
		self.icache_valid = True
		self.vaddrs[0] = ftq_req.startAddr
		self.vaddrs[1] = ftq_req.nextlineStart
		self.double_line = calc_double_line(ftq_req.startAddr)
	
	def randomize(self, ftq_req: FTQQuery, valid=True, last_finished=True):
		# itlb pbmt and pmp_mmio won't be changed
		self.exceptions = [0 if randbool(rate=80) else randint(1, 3) for _ in range(2)]
		self.init_as_valid(ftq_req)
		self.paddr = 0x18151192 # not useful when encountering non mmioX
		self.gpaddr = randint(0, (1 << 56) -1)
		self.backend_exception = randbool(rate=70)
		self.data = 0

		if not valid:
			cond = randint(1, 15)			
			if (cond & 1) > 0: 
				self.icache_valid = False

			if (cond & 2) > 0:
				self.vaddrs[0] = ftq_req.startAddr+32
    
			if (cond & 4) > 0:
				self.vaddrs[1] = ftq_req.nextlineStart+32

			if (cond & 8) > 0:
				self.double_line = not self.double_line
			return

		# 有效数据才需要计算
		data_construction = randint(0, 99)
		end_idx = ftq_req.ftqOffset.offsetIdx if ftq_req.ftqOffset.exists else PREDICT_WIDTH - 1
		real_jump_type =  randint(1, 3) if ftq_req.ftqOffset.exists else 0
		if data_construction < 40:
			# 无预测错误，也即ret,jalr,jal错误不存在，也不存在target, valid, non cfi问题
			instrs = construct_instrs_with_jump_idx(end_idx,cfi_res=real_jump_type, imm=ftq_req.nextStartAddr, last_finished=last_finished)
		elif data_construction < 50:
			# in this case, construct random of jal err 	
			# by constructing jump instr before the real jump idx
			instrs = construct_instrs_with_jump_idx(randint(0, max(0, end_idx-1)), cfi_res=2,last_finished=last_finished)
		elif data_construction < 60:
			# ret err
			instrs = construct_instrs_with_jump_idx(randint(0, max(0, end_idx-1)), cfi_res=4,last_finished=last_finished)
		elif data_construction < 70:
			# jalr err
			instrs = construct_instrs_with_jump_idx(randint(0, max(0, end_idx-1)), cfi_res=3,last_finished=last_finished)
		elif data_construction < 80:
			# invalid prediction
			instrs = construct_instrs_with_jump_idx(randint(min(PREDICT_WIDTH - 1, end_idx+1), PREDICT_WIDTH-1), last_finished=last_finished)
		elif data_construction < 90:
			instrs = construct_instrs_with_jump_idx(end_idx, invalid_jmp_prediction=True, last_finished=last_finished)
		else:
			#  this is a different target err producer
			instrs = construct_instrs_with_jump_idx(end_idx, imm=ftq_req.nextStartAddr + 40,last_finished=last_finished)

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
		
		
