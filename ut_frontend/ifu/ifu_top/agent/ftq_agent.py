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
    isCall, isRet, isRVC = False
    pdValid = True # if the predecode info is valid
    brType = 0 # 0 for non cfi instruction

class FTQResp():
    valid = True # indicate whether response is usable
    pds = [toIbufferPd() for i in range(16)] # indicate the predecode info for 16 concated instructions
    misOffset = ExistsIdx() # indicates if a mis branch predicate instr exists and which is it
    pcs = [0 for i in range(16)] # pcs for 16 concated instructions
    instrRanges = [True for i in range(16)] # indicate whether each instruction is in the prediction block
    ftqIdx: FTQIdx = FTQIdx() # the index of the prediction block in ftq
    jalTarget, target = 0 # jump target of the first jump instruction; next pc of the pc of last valid instruction in the prediction block
    cfiOffset_valid = False # if there exists cfi instruction in the prediction block

	
class FTQRedirect():
    ftqIdx: FTQIdx = FTQIdx()
    valid = True
    redirect_level = 0
    ftqOffset = 0

class FTQFlushFromBPUStg():
    stg_valid = True
    ftqIdx: FTQIdx = FTQIdx()

class FTQFlushFromBPU():
    stgs = {"s2": FTQFlushFromBPUStg(), "s3":FTQFlushFromBPUStg()}

class InternalFlushInfos():
    internal_flushes = [False for i in range(4)]

class FTQAgent(Agent):
    def __init__(self, bundle:FTQInterBundle, flushes: InternalFlushesBundle):
        super().__init__(bundle)
        self.bundle = bundle
        self.ftq_req_bundle = bundle._fromFtq._req
        self.ftq_wb_bundle = bundle._toFtq_pdWb
        self.ftq_redirect_bundle = bundle._fromFtq._redirect
        self.ftq_flush_stgs_bundle = bundle._fromFtq._flushFromBpu
        self.flush_res_bundle = flushes
        
    async def ftq_query(self, query: FTQQuery):
        self.ftq_req_bundle._bits._ftqIdx._flag.value = query.ftqIdx.flag
        self.ftq_req_bundle._bits._ftqIdx._value.value = query.ftqIdx.value
        self.ftq_req_bundle._bits._ftqOffset._valid.value = query.ftqOffset.exists
        self.ftq_req_bundle._bits._ftqOffset._bits.value = query.ftqOffset.offsetIdx
        self.ftq_req_bundle._bits._nextlineStart.value = query.nextlineStart
        self.ftq_req_bundle._bits._startAddr.value = query.startAddr
        self.ftq_req_bundle._bits._nextStartAddr.value = query.nextStartAddr
        await self.bundle.step(4)
        response = FTQResp()
        response.valid = self.ftq_wb_bundle._valid.value
        response.cfiOffset_valid = self.ftq_wb_bundle._bits._cfiOffset_valid.value
        response.ftqIdx.flag = self.ftq_wb_bundle._bits._ftqIdx._flag.value
        response.ftqIdx.value = self.ftq_wb_bundle._bits._ftqIdx._value.value
        response.jalTarget = self.ftq_wb_bundle._bits._jalTarget.value
        response.target = self.ftq_wb_bundle._bits._target.value
        response.misOffset.exists = self.ftq_wb_bundle._bits._misOffset._valid.value
        response.misOffset.offsetIdx = self.ftq_wb_bundle._bits._misOffset._bits.value
        for i in range(16):
            response.pcs[i] = getattr(self.ftq_wb_bundle._bits._pc, f"_{i}").value
            response.instrRanges[i] = getattr(self.ftq_wb_bundle._bits._instrRange, f"_{i}").value
            response.pds[i].brType = getattr(self.ftq_wb_bundle._bits._pd, f"_{i}")._brType.value
            response.pds[i].isCall = getattr(self.ftq_wb_bundle._bits._pd, f"_{i}")._isCall.value
            response.pds[i].isRet = getattr(self.ftq_wb_bundle._bits._pd, f"_{i}")._isRet.value
            response.pds[i].isRVC = getattr(self.ftq_wb_bundle._bits._pd, f"_{i}")._isRVC.value
            response.pds[i].pdValid = getattr(self.ftq_wb_bundle._bits._pd, f"_{i}")._valid.value
        
        return response

    async def from_ftq_flush(self, flush_bpu:FTQFlushFromBPU, redirect: FTQRedirect):  
        stg_names = ["s2", "s3"]
        for stg_name in stg_names:
            stg_bundle: StageFlushBundle = getattr(self.ftq_flush_stgs_bundle, f"_{stg_name}")
            stg_redirect: FTQFlushFromBPUStg = flush_bpu.stgs[stg_name]
            stg_bundle._bits._flag.value = stg_redirect.ftqIdx.flag
            stg_bundle._bits._value.value = stg_redirect.ftqIdx.value
            stg_bundle._valid.value = stg_redirect.stg_valid
        
        self.ftq_redirect_bundle._valid.value = redirect.valid
        self.ftq_redirect_bundle._bits._ftqOffset.value = redirect.ftqOffset
        self.ftq_redirect_bundle._bits._level.value = redirect.redirect_level
        self.ftq_redirect_bundle._bits._ftqIdx._value.value = redirect.ftqIdx.value
        self.ftq_redirect_bundle._bits._ftqIdx._flag.value = redirect.ftqIdx.flag  

        await self.bundle.step(4)

        flush_info = InternalFlushInfos()       

        flush_info[3] = self.flush_res_bundle._f3_flush.value
        flush_info[2] = self.flush_res_bundle._f2_flush.value
        flush_info[1] = self.flush_res_bundle._f1_flush.value
        flush_info[0] = self.flush_res_bundle._f1_flush.value | flush_bpu.stgs["s2"].stg_valid

        return flush_info
            