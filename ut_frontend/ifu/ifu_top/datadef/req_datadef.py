from .ftq_datadef import FTQQuery, FTQFlushFromBPU, FTQResp
from .icache_datadef import ICacheStatusResp, ICacheResp
from .sub_modules_def import PreDecodeDataDef, F3PreDecodeData, PredCheckerStage1RetData, PredCheckerStage2RetData
from .ibuffer_datadef import ToIbufferAllRes
from ..commons import randbool, check_icache_resp_all_valid, calc_double_line
import random

def log_based_random(initial_roof=0.5, decay_rate=0.5, max_val=6):
    """
    用一个随机数计算val值的通用函数
    
    参数:
    - initial_roof: 初始屋顶值，默认0.5
    - decay_rate: 衰减率，默认0.5
    - max_val: val的最大值，默认10
    
    返回值:
    - val: 计算得到的整数值
    
    逻辑分析:
    1. 第k次成功（val增加到k）的概率是：initial_roof * decay_rate^(k-1)
    2. 连续成功k次的概率是：(initial_roof)^k * decay_rate^(k*(k-1)/2)
    3. 可以通过将[0,1)区间按概率分布划分为不同范围来直接确定val
    
    如果为了性能考虑，后续可以对特别大的max_val添加对数函数支持
    """
    if initial_roof <= 0 or decay_rate <= 0 or decay_rate >= 1:
        raise ValueError("initial_roof应大于0，decay_rate应在(0,1)之间")
    
    r = random.random()  # 生成[0,1)的随机数
    
    # 计算累积概率分布
    new_roof = initial_roof
    cnt = 0
    for _ in range(max_val):
        if r >= new_roof:
            break
        cnt += 1
        new_roof *= decay_rate
    
    # 如果循环结束仍未返回，说明所有可能都成功了，返回最大值
    return cnt
        

class ICacheValidRelated():
    def __init__(self):
        icache_resp_valid = True
        vaddrs = [0, 0]
        icache_doubleline = False
        start = 0
        next_start = 0
        # icache_resp_valid, vaddrs, icache_doubleline, req_doubleline, start, next_start
        pass

    # def

class NonMMIOSingleReq():
    def __init__(self):    
        # f0 stage inputs
        self.icache_ready = True
        self.ftq_req = FTQQuery()
        self.bpu_flush_info = FTQFlushFromBPU()
        
        # stage 2 inputs
        self.invalid_icache_resps: list[ICacheResp]=[]
        self.final_icache_resp = ICacheResp()

        # stage 3 inputs
        self.fs_is_off = True

        # other info for controlling, which may be add for future features
    
    def get_icache_block_terms(self):
        return len(self.invalid_icache_resps)
        
    def randomize(self, randomly_choosing_finished=False, finished=True, ftq_idx=None):
        """gen random data

        Args:
            randomly_choosing_finished (bool, optional): choose the param finished randomly. Defaults to False.
            finished (bool, optional): whether the last instr is finished or cross prediction block. Defaults to True.
            ftq_idx (_type_, optional): ftq idx of FTQQuery. Defaults to None.
        """
        icache_block_terms = log_based_random()
        self.fs_is_off = randbool()
        self.ftq_req.randomize(ftq_idx=ftq_idx)
        
        self.bpu_flush_info.randomize(self.ftq_req.ftqIdx)
        
        # here we init the invalid icache resps
        self.invalid_icache_resps = []
        for _ in range(icache_block_terms):
            res = ICacheResp()
            res.randomize(self.ftq_req, False)
        self.final_icache_resp.randomize(self.ftq_req, True, last_finished=finished if not randomly_choosing_finished else random.randint(0, 99) < 70)
            
        
    def __repr__(self):
        return f"NonMMIOSingleReq(\nfs_is_off: {self.fs_is_off}\nftq_req: {self.ftq_req}\n\
            final_icache_resp: {self.final_icache_resp}\nbpu_flush_info: {self.bpu_flush_info}\n\
                icache_ready: {self.icache_ready})\nicache_blocks: {self.get_icache_block_terms()}\nicache_block_resps:{self.invalid_icache_resps}"
    
class ClusteredNonMMIOReqs():
    def __init__(self):
        self.reqs: list[NonMMIOSingleReq] = []
        self.resps: list[NonMMIOResp] = []
    
    def randomize(self):
        num_reqs = log_based_random(initial_roof=0.4, max_val=7)
        self.reqs = []
        for _ in range(num_reqs - 1):
            req = NonMMIOSingleReq()
            req.randomize(finished=False)
            self.reqs.append(req)
        req = NonMMIOSingleReq()
        req.randomize(finished=True)
        self.reqs.append(req)
        
    def __repr__(self):
        return f"ClusteredNonMMIOReqs(\nreqs: {self.reqs}\nref_resps: {self.resps}\n)\n"

class NonMMIOResp():
    def __init__(self):
        # ret of stage 0
        self.ftq_ready = False
        self.bpu_flush_res = False

        # ret of stage 2
        self.cut_instrs = []
        self.predecode_res : PreDecodeDataDef = PreDecodeDataDef()
        self.cut_ptrs = []
        self.icache_all_valid = True
        

        # ret of stage 3
        self.exceptions = []
        self.ranges = 0
        self.pcs = []
        self.addrs = ()
        self.f3_predecode_res: F3PreDecodeData = F3PreDecodeData()
        self.exception_vecs = []
        
        # self.expd_instrs = []
        
        self.pred_checker_stg1_res: PredCheckerStage1RetData= PredCheckerStage1RetData()
        self.to_ibuffer : ToIbufferAllRes = ToIbufferAllRes()

        # ret of wb
        self.wb_res : FTQResp = FTQResp()
        self.last_half_valid = False
        self.pred_checker_stg2_res: PredCheckerStage2RetData = PredCheckerStage2RetData()
        
        # assistant info, no usage 
        self.pin_flush = False
        self.f3_flush = False

    def __repr__(self):
        return f"""NonMMIOResp(
    ftq_ready: {self.ftq_ready}
    bpu_flush_res: {self.bpu_flush_res}
    cut_instrs: {self.cut_instrs}
    predecode_res: {self.predecode_res}
    cut_ptrs: {self.cut_ptrs}
    exception_vecs: {self.exception_vecs}
    pcs: {self.pcs}
    addrs: {self.addrs}
    icache_all_valid: {self.icache_all_valid}
    ranges: {self.ranges}
    f3_predecode_res: {self.f3_predecode_res}
    pred_checker_stg1_res: {self.pred_checker_stg1_res}
    pred_checker_stg2_res: {self.pred_checker_stg2_res}
    wb_res: {self.wb_res}
    last_half_valid: {self.last_half_valid}
    to_ibuffer: {self.to_ibuffer}
)"""
        
    def __eq__(self, value):
        if not isinstance(value, NonMMIOResp):
            print(f"Type mismatch: {type(value)} != NonMMIOResp")
            return False

        if not self.ftq_ready or self.bpu_flush_res:
            return self.ftq_ready == value.ftq_ready and self.bpu_flush_res == value.bpu_flush_res
        
        checks = [
            ("ftq_ready", self.ftq_ready, value.ftq_ready),
            ("bpu_flush_res", self.bpu_flush_res, value.bpu_flush_res),
            ("cut_instrs", self.cut_instrs, value.cut_instrs),
            ("predecode_res", self.predecode_res, value.predecode_res),
            ("cut_ptrs", self.cut_ptrs, value.cut_ptrs),
            ("exception_vecs", self.exception_vecs, value.exception_vecs),
            ("pcs", self.pcs, value.pcs),
            ("addrs", self.addrs, value.addrs),
            ("icache_all_valid", self.icache_all_valid, value.icache_all_valid),
            ("ranges", self.ranges, value.ranges),
            ("f3_predecode_res", self.f3_predecode_res, value.f3_predecode_res),
            ("pred_checker_stg1_res", self.pred_checker_stg1_res, value.pred_checker_stg1_res),
            ("pred_checker_stg2_res", self.pred_checker_stg2_res, value.pred_checker_stg2_res),
            ("wb_res", self.wb_res, value.wb_res),
            ("last_half_valid", self.last_half_valid, value.last_half_valid),
            ("to_ibuffer", self.to_ibuffer, value.to_ibuffer),
        ]

        for name, a, b in checks:
            if a != b:
                print(f"Mismatch in {name}: {str(a)} != {str(b)}")
                return False

        return True
    
class NonMMIOReqLogger():
    
    def __init__(self):
        self.before = None
        self.cur = None
    
    def save(self, mmio_req: NonMMIOSingleReq):
        self.before = self.cur
        self.cur = mmio_req
    
    def __repr__(self):
        return f'''{self.__class__.__name__}:
before: {self.before}
cur: {self.cur}'''

non_mmio_logger_instance = NonMMIOReqLogger()