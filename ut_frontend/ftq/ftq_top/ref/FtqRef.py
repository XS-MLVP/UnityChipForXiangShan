from .FtqPtr import *
from .status_queue import *
from .ftb_entry_mem import *
from .ftq_pc_mem import *
# from .ftq_pd_mem import *
from .ftq_meta_mem import *
from .ftq_redirect_mem import *

FTQSIZE = 64
class FTQ:
    def __init__(self, size=FTQSIZE):
        self.size = size
        # FTQ ptrs
        self.bpu_ptr = CircularQueuePtr(flag=False, value=0)
        self.ifu_ptr = CircularQueuePtr(flag=False, value=0)
        self.ifu_wb_ptr = CircularQueuePtr(flag=False, value=0)
        self.comm_ptr = CircularQueuePtr(flag=False, value=0)
        self.rob_comm_ptr = CircularQueuePtr(flag=False, value=0)
        self.pf_ptr = CircularQueuePtr(flag=False, value=0)

        # FTQ Sub Queue
        self.ftb_entry_mem = FTBEntryMem(size)
        self.ftq_pc_mem = FTQPCMem(size)
        # self.ftq_pd_mem = FTQPDMem(size)
        self.ftq_meta_mem = FTQMeta1RSram(size)
        self.ftq_redirect_mem = FTQRedirectMem(size)

        # Status Queue
        # self.fetch_status = EntryFetchStatusQueue(size)
        self.update_targets = [0] * size 
        self.cfiIndex_vec = [{"valid": 0, "bits": 0} for _ in range(size)]
        self.mispredict_vecs = [[0 for _ in range(16)] for _ in range(size)]
        self.pred_stages = [0] * size
        self.commit_states = [0] * size
        self.entry_fetch_status = [0] * size
        self.entry_hit_status = [0] * size