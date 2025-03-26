from toffee import Agent
from ..bundle import FTQInterBundle, InternalFlushesBundle, StageFlushBundle

class FTQIdx(object):
    flag = False
    value = 0 # different flags with greater value will also be flushed

    def __eq__(self, value):
        if type(value) != FTQIdx:
            return False
        return self.flag == value.flag and self.value == value.value

    def __lt__(self, value):

        return self.flag ^ value.flag ^ self.value < value.value
    
    def __gt__(self, value):
        return self.flag ^ value.flag ^ self.value < value.value

class ExistsIdx(object):
    offsetIdx = 0
    exists = False

class FTQQuery():
    ftqIdx: FTQIdx = FTQIdx() # position of the prediction block in the ftq, 
    ftqOffset: ExistsIdx = ExistsIdx() # if jump instruction exists and where is it
    nextlineStart = 0 # addr of the next cacheline
    startAddr = 0 # addr of the instruction block
    nextStartAddr = 0 # addr of the next prediction block

class toIbufferPd():
    isCall = False
    isRet = False 
    isRVC = False
    pdValid = True # if the predecode info is valid
    brType = 0 # 0 for non cfi instruction

class FTQResp():
    valid = True # indicate whether response is usable
    pds = [toIbufferPd() for i in range(16)] # indicate the predecode info for 16 concated instructions
    misOffset = ExistsIdx() # indicates if a mis branch predicate instr exists and which is it
    pcs = [0 for i in range(16)] # pcs for 16 concated instructions
    instrRanges = [True for i in range(16)] # indicate whether each instruction is in the prediction block
    ftqIdx: FTQIdx = FTQIdx() # the index of the prediction block in ftq
    jalTarget = 0
    target = 0 # jump target of the first jump instruction; next pc of the pc of last valid instruction in the prediction block
    cfiOffset_valid = False # if there exists cfi instruction in the prediction block

	
class FTQRedirect():
    ftqIdx: FTQIdx = FTQIdx()
    valid = True
    redirect_level = False
    ftqOffset = 0

class FTQFlushFromBPUStg():
    stg_valid = True
    ftqIdx: FTQIdx = FTQIdx()

class FTQFlushFromBPU():
    stgs = {"s2": FTQFlushFromBPUStg(), "s3":FTQFlushFromBPUStg()}

class InternalFlushInfos():
    internal_flushes = [False for i in range(4)]

class FTQFlushInfo():
    flush_from_bpu = FTQFlushFromBPU()
    redirect = FTQRedirect()
