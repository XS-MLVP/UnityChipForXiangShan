from toffee import Agent
from ..bundle import FTQInterBundle, InternalBundle, StageFlushBundle
from ..commons import randbool
from random import randint

class FTQIdx(object):
    def __init__(self):
        self.flag = False
        self.value = 0 # different flags with greater value will also be flushed

    def __eq__(self, value):
        if type(value) != FTQIdx:
            return False
        return self.flag == value.flag and self.value == value.value

    def __lt__(self, value):
        
        return self.flag ^ value.flag ^ (self.value < value.value)
    
    def __gt__(self, value):
        return self.flag ^ value.flag ^ (self.value > value.value)
    
    def __str__(self):
        return f"[flag: {self.flag}; value: {self.value}]\n"
    
    def randomize(self):
        self.flag = randbool()
        self.value = randint(0, 63)

class ExistsIdx(object):
    def __init__(self):
        self.offsetIdx = 0
        self.exists = False

    def __str__(self):
        return f"exist: {self.exists}\noffIdx: {self.offsetIdx}\n"

    def __eq__(self, value):
        if type(value) != ExistsIdx:
            return False
        
        if self.exists != value.exists:
            return False
        
        if not self.exists:
            return True
        
        return self.offsetIdx == value.offsetIdx
    
    def randomize(self):
        self.exists = randbool(rate=40)
        self.offsetIdx = randint(0, 15)

class FTQQuery():
    def __init__(self):
        self.valid = True # 同拍子
        self.ftqIdx: FTQIdx = FTQIdx() # position of the prediction block in the ftq, 
        self.ftqOffset: ExistsIdx = ExistsIdx() # if jump instruction exists and where is it
        self.nextlineStart = 0 # addr of the next cacheline
        self.startAddr = 0 # addr of the instruction block
        self.nextStartAddr = 0 # addr of the next prediction block
    
    def __str__(self):
        return (
            f"{FTQQuery.__name__}(\n"
            f"  valid={self.valid},\n"
            f"  ftqIdx={self.ftqIdx},\n"
            f"  ftqOffset={self.ftqOffset},\n"
            f"  nextlineStart={self.nextlineStart},\n"
            f"  startAddr={self.startAddr},\n"
            f"  nextStartAddr={self.nextStartAddr}\n"
            f")"
        )
    
    def set_start_addr(self, start_addr):
        self.startAddr = start_addr
        self.nextlineStart = (self.startAddr + 64) & ((1 << 50)-1)
    
    def randomize(self):
        self.ftqIdx.randomize()
        self.ftqOffset.randomize()
        self.set_start_addr((randint(0, (1 << 49) - 1 ) << 1) & ((1 << 50)-1))
    
        self.nextStartAddr =  (randint(0, (1 << 49) - 1 ) << 1) & ((1 << 50)-1) if self.ftqOffset.exists \
            else (self.startAddr + randint(1, 16) * 2) & ((1 << 50)-1)
        

class ResPd():
    def __init__(self):
        
        self.isCalls = [False for i in range(16)] 
        self.isRets = [False for i in range(16)] 
        self.isRVCs = [False for i in range(16)] 
        self.pdValids = [True for i in range(16)] # if the instr is valid in the block
        self.brTypes = [0 for i in range(16)] # 0 for non cfi 
        
    def __str__(self):
        return f"calls: {self.isCalls}\nrets: {self.isRets}\nrvcs: {self.isRVCs}\nvalids: {self.pdValids}\nbrTypes: {self.brTypes}"

    def __eq__(self, value):
        if type(value) != ResPd:
            return False
        return self.isCalls == value.isCalls and self.isRets == value.isRets and self.isRVCs == value.isRVCs and self.pdValids == value.pdValids and self.brTypes == value.brTypes

class FTQResp():
    def __init__(self):
        
        self.valid = True # indicate whether response is usable
        self.pds = ResPd() # indicate the predecode info for 16 concated instructions
        self.misOffset = ExistsIdx() # indicates if a mis branch predicate instr exists and which is it
        self.pcs = [0 for i in range(16)] # pcs for 16 concated instructions
        self.instrRanges = [True for i in range(16)] # indicate whether each instruction is in the prediction block
        self.ftqIdx: FTQIdx = FTQIdx() # the index of the prediction block in ftq
        self.jalTarget = 0
        self.target = 0 # jump target of the first jump instruction; next pc of the pc of last valid instruction in the prediction block
        self.cfiOffset_valid = False # if there exists cfi instruction in the prediction block
    
    def __str__(self):
        return f"valid: {self.valid}\npds: {self.pds}\nmisOffset:\n{self.misOffset}\npcs: {self.pcs}\ninstrRanges: {self.instrRanges}\nftqIdx:{self.ftqIdx}\njalTarget: {self.jalTarget}\ntarget: {self.target}\ncfioffset_valid: {self.cfiOffset_valid}"

    def __eq__(self, value):
        if not isinstance(value, FTQResp):
            print(f"Type mismatch: {type(value)} != FTQResp")
            return False

        checks = [
            ("valid", self.valid, value.valid),
            ("pds", self.pds, value.pds),
            ("misOffset", self.misOffset, value.misOffset),
            ("pcs", self.pcs, value.pcs),
            ("instrRanges", self.instrRanges, value.instrRanges),
            ("ftqIdx", self.ftqIdx, value.ftqIdx),
            ("jalTarget", self.jalTarget, value.jalTarget),
            ("target", self.target, value.target),
            ("cfiOffset_valid", self.cfiOffset_valid, value.cfiOffset_valid),
        ]

        for name, a, b in checks:
            if a != b:
                print(f"Mismatch in {name}: {a!r} != {b!r}")
                return False

        return True

	
class FTQRedirect():
    def __init__(self):
        
        self.ftqIdx: FTQIdx = FTQIdx()
        self.valid = False
        self.redirect_level = False
        self.ftqOffset = 0

class FTQFlushFromBPUStg():
    def __init__(self):
        self.stg_valid = False
        self.ftqIdx: FTQIdx = FTQIdx()
    
    def randomize(self, idx: FTQIdx):
        if_flush = randbool(rate=25)
        if if_flush:
            self.stg_valid = True
            reverse_flag = False if idx.value == 63 else True if idx.value == 0 \
                else randbool()
            self.ftqIdx.flag = not idx.flag if reverse_flag else idx.flag
            self.ftqIdx.value = randint(idx.value + 1, 63) if reverse_flag else randint(0, idx.value)
    
    def __str__(self):
        return (
            f"{self.__class__.__name__}(\n"
            f"  stg_valid={self.stg_valid},\n"
            f"  ftqIdx={self.ftqIdx}\n"
            f")"
        )

class FTQFlushFromBPU():
    def __init__(self):
        self.stgs : dict[str, FTQFlushFromBPUStg]= {"s2": FTQFlushFromBPUStg(), "s3":FTQFlushFromBPUStg()}

    def randomize(self, idx: FTQIdx):
        self.stgs["s2"].randomize(idx)
        self.stgs["s3"].randomize(idx)
        self.stgs["s3"].stg_valid = False
        
    def __str__(self):
        stgs_str = ",\n".join([f"  {k}={v}" for k, v in self.stgs.items()])
        return (
            f"{self.__class__.__name__}(\n"
            f"{stgs_str}\n"
            f")"
        )
            
        

class InternalFlushInfos():
    def __init__(self):
        self.internal_flushes = [False for i in range(4)]

class FTQFlushInfo():
    def __init__(self):
        self.flush_from_bpu = FTQFlushFromBPU()
        self.redirect = FTQRedirect()
