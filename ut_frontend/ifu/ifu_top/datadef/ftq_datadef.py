from toffee import Agent
from ..bundle import FTQInterBundle, InternalBundle, StageFlushBundle

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

class FTQQuery():
    def __init__(self):
        self.valid = True
        self.ftqIdx: FTQIdx = FTQIdx() # position of the prediction block in the ftq, 
        self.ftqOffset: ExistsIdx = ExistsIdx() # if jump instruction exists and where is it
        self.nextlineStart = 0 # addr of the next cacheline
        self.startAddr = 0 # addr of the instruction block
        self.nextStartAddr = 0 # addr of the next prediction block


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
        return f"valid: {self.valid}\npds: {self.pds}\nmisOffset: {self.misOffset}\ninstrRanges: {self.instrRanges}"

    def __eq__(self, value):
        if type(value) != FTQResp:
            return False
        return self.valid == value.valid and self.pds == value.pds and self.misOffset == value.misOffset and self.pcs == value.pcs \
            and self.instrRanges == value.instrRanges and self.ftqIdx == value.ftqIdx and self.jalTarget == value.jalTarget and self.target == value.target \
            and self.cfiOffset_valid == value.cfiOffset_valid

	
class FTQRedirect():
    def __init__(self):
        
        self.ftqIdx: FTQIdx = FTQIdx()
        self.valid = True
        self.redirect_level = False
        self.ftqOffset = 0

class FTQFlushFromBPUStg():
    def __init__(self):
        self.stg_valid = True
        self.ftqIdx: FTQIdx = FTQIdx()

class FTQFlushFromBPU():
    def __init__(self):
        self.stgs = {"s2": FTQFlushFromBPUStg(), "s3":FTQFlushFromBPUStg()}

class InternalFlushInfos():
    def __init__(self):
        self.internal_flushes = [False for i in range(4)]

class FTQFlushInfo():
    def __init__(self):
        self.flush_from_bpu = FTQFlushFromBPU()
        self.redirect = FTQRedirect()
