from .ftq_datadef import FTQQuery, FTQFlushFromBPU, FTQResp
from .icache_datadef import ICacheStatusResp
from .sub_modules_def import PreDecodeDataDef, F3PreDecodeData, PredCheckerStage1RetData, PredCheckerStage2RetData
from .ibuffer_datadef import ToIbufferAllRes
from ..commons import randbool

class NonMMIOReq():
    def __init__(self):
        self.ftq_req = FTQQuery()
        self.icache_resp = ICacheStatusResp()
        self.bpu_flush_info = FTQFlushFromBPU()
        self.fs_is_off = True
        
    def randomize(self):
        self.fs_is_off = randbool()
        self.ftq_req.randomize()
        self.icache_resp.randomize(self.ftq_req)
        self.bpu_flush_info.randomize(self.ftq_req.ftqIdx)
        
    def __repr__(self):
        return f"fs_is_off: {self.fs_is_off}\nftq_req: {self.ftq_req}\nicache_resp: {self.icache_resp}\nbpu_flush_info: {self.bpu_flush_info}"

class NonMMIOResp():
    def __init__(self):
        self.ftq_ready = False
        self.bpu_flush_res = False

        self.cut_instrs = []
        self.predecode_res : PreDecodeDataDef = PreDecodeDataDef()
        self.cut_ptrs = []

        self.exception_vecs = []
        self.pcs = []
        self.addrs = ()
        self.icache_all_valid = True

        self.ranges = 0
        self.f3_predecode_res: F3PreDecodeData = F3PreDecodeData()
        # self.expd_instrs = []
        
        self.pred_checker_stg1_res: PredCheckerStage1RetData= PredCheckerStage1RetData()
        self.pred_checker_stg2_res: PredCheckerStage2RetData = PredCheckerStage2RetData()

        self.wb_res: FTQResp = FTQResp()
        self.last_half_valid = False
        self.to_ibuffer : ToIbufferAllRes = ToIbufferAllRes()
        
    
    def __str__(self):
        return f"""ftq_ready: {self.ftq_ready}
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
pred_checker_stg1: {self.pred_checker_stg1_res}
pred_checker_stg2_res: {self.pred_checker_stg2_res}
wb_res: {self.wb_res}
last_half_valid: {self.last_half_valid}
to_ibuffer: {self.to_ibuffer}"""
        
    def __eq__(self, value):
        if not isinstance(value, NonMMIOResp):
            print(f"Type mismatch: {type(value)} != NonMMIOResp")
            return False

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
    
    # def __str__(self):
    #     return self.__repr__()

# @dataclass
# class NonMMIOResp:
#     ftq_ready: bool = False
#     bpu_flush_res: bool = False

#     cut_instrs: list = field(default_factory=list)
#     predecode_res: PreDecodeDataDef = field(default_factory=PreDecodeDataDef)
#     cut_ptrs: list = field(default_factory=list)

#     exception_vecs: list = field(default_factory=list)
#     pcs: list = field(default_factory=list)
#     addrs: list = field(default_factory=list)
#     icache_all_valid: bool = True

#     ranges: list = field(default_factory=list)
#     f3_predecode_res: F3PreDecodeData = field(default_factory=F3PreDecodeData)
#     expd_instrs: list = field(default_factory=list)
#     pred_checker_stg1_res: PredCheckerStage1RetData = field(default_factory=PredCheckerStage1RetData)
#     pred_checker_stg2_res: PredCheckerStage2RetData = field(default_factory=PredCheckerStage2RetData)

#     wb_res: FTQResp = None
#     last_half_valid: bool = False
#     to_ibuffer: ToIbufferAllRes = field(default_factory=ToIbufferAllRes)