import random
import toffee_test
from ..env import FtqBundle
from ..env import FtqEnv 
import toffee

from dut.FtqTop import DUTFtqTop
import toffee.funcov as fc
from toffee.funcov import CovGroup

class NewDUTFtqTop(DUTFtqTop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 目标相关信号
        #储存的时候不能加上.value  因为储存时是静态的 必须放到test中调用.value
        self.newest_entry_target = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_target")
        self.newest_entry_ptr_value = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_ptr_value")
        self.newest_entry_target_modified = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_target_modified")
        

        self.has_false_hit = self.GetInternalSignal("FtqTop_top.Ftq.has_false_hit")
        

        self.ifu_redirect_valid = self.GetInternalSignal("FtqTop_top.Ftq.fromIfuRedirect_valid_probe")
        self.ifu_redirect_pc = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_pc")
        self.ifu_redirect_pd_valid = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_pd_valid")
        self.ifu_redirect_pd_isRet = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_pd_isRet")
        self.ifu_redirect_target = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_target")
        self.ifu_redirect_taken = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_taken")
        self.ifu_flush = self.GetInternalSignal("FtqTop_top.Ftq.ifuFlush")
        self.ifu_redirect_ftq_idx = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_ftqIdx_value")
        self.ifu_redirect_ftq_offset = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_ftqOffset")
        
        self.tobackend_newest_entry_en = self.GetInternalSignal("FtqTop_top.io_toBackend_newest_entry_en")
        self.tobackend_newest_entry_ptr = self.GetInternalSignal("FtqTop_top.io_toBackend_newest_entry_ptr_value")
        self.tobackend_newest_target = self.GetInternalSignal("FtqTop_top.io_toBackend_newest_entry_target")
        self.tobackend_pc_mem_wen = self.GetInternalSignal("FtqTop_top.io_toBackend_pc_mem_wen")
        self.tobackend_pc_mem_waddr = self.GetInternalSignal("FtqTop_top.io_toBackend_pc_mem_waddr")
        self.tobackend_pc_mem_wdata_start = self.GetInternalSignal("FtqTop_top.io_toBackend_pc_mem_wdata_startAddr")
        
        self.icache_flush = self.GetInternalSignal("FtqTop_top.io_icacheFlush")

        self.toBpu_redirect_bits_cfiUpdate_br_hit = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_br_hit")
        self.toBpu_redirect_bits_cfiUpdate_jr_hit = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_jr_hit")
        self.toBpu_redirect_bits_cfiUpdate_shift = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_shift")
        self.toBpu_redirect_bits_cfiUpdate_addIntoHist = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_addIntoHist")

        
        # 新增：各种指针信号
        self.bpu_ptr = self.GetInternalSignal("FtqTop_top.Ftq.bpuPtr_value")
        self.ifu_ptr_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtr_write_value")
        self.ifu_wb_ptr_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuWbPtr_value")
        self.ifu_ptr_plus1_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtrPlus1_value")
        self.ifu_ptr_plus2_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtrPlus2_value")
        self.pf_ptr_write = self.GetInternalSignal("FtqTop_top.Ftq.pfPtr_value")
        self.pf_ptr_plus1_write = self.GetInternalSignal("FtqTop_top.Ftq.pfPtrPlus1_value")

        self.topdown_redirect_valid = self.GetInternalSignal("FtqTop_top.io_toIfu_topdown_redirect_valid")
        self.topdown_redirect_debugIsCtrl = self.GetInternalSignal("FtqTop_top.io_toIfu_topdown_redirect_bits_debugIsCtrl")
        self.topdown_redirect_debugIsMemVio = self.GetInternalSignal("FtqTop_top.io_toIfu_topdown_redirect_bits_debugIsMemVio")
        
        self.toifu_redirect_valid = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_valid")
        self.toifu_redirect_ftqIdx_value = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_bits_ftqIdx_value")
        self.toifu_redirect_ftqOffset = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_bits_ftqOffset")
        self.toifu_redirect_level = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_bits_level")

        # 动态索引信号的访问方法
        def get_update_target(idx):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.update_target_{idx}")
            
        def get_cfi_index_bits(idx):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.cfiIndex_vec_{idx}_bits")
            
        def get_cfi_index_valid(idx):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.cfiIndex_vec_{idx}_valid")
            
        def get_mispredict_vec(idx, offset):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.mispredict_vec_{idx}_{offset}")

        def get_commit_state_queue_reg(ftq_idx, offset):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.commitStateQueueReg_{ftq_idx}_{offset}")    
        
        #  不能直接调用函数 必须用封闭包绑定self33333
        self.get_update_target = get_update_target
        self.get_cfi_index_bits = get_cfi_index_bits
        self.get_cfi_index_valid = get_cfi_index_valid
        self.get_mispredict_vec = get_mispredict_vec
        self.get_commit_state_queue_reg = get_commit_state_queue_reg




def ftq_cover_point(dut):
    """
    为 FTQ 创建功能覆盖点
    """
    g = CovGroup("FTQ redirect and management function")

    # Backend 重定向信号覆盖点
    g.add_cover_point(dut.io_fromBackend_redirect_valid, {"backend_redirect_valid is 0": fc.Eq(0)}, name="Backend redirect valid is 0")
    g.add_cover_point(dut.io_fromBackend_redirect_valid, {"backend_redirect_valid is 1": fc.Eq(1)}, name="Backend redirect valid is 1")
    
    g.add_cover_point(dut.io_fromBackend_redirect_bits_cfiUpdate_taken, {"backend_taken is 0": fc.Eq(0)}, name="Backend taken is 0")
    g.add_cover_point(dut.io_fromBackend_redirect_bits_cfiUpdate_taken, {"backend_taken is 1": fc.Eq(1)}, name="Backend taken is 1")
    
    g.add_cover_point(dut.io_fromBackend_redirect_bits_cfiUpdate_isMisPred, {"backend_isMisPred is 0": fc.Eq(0)}, name="Backend isMisPred is 0")
    g.add_cover_point(dut.io_fromBackend_redirect_bits_cfiUpdate_isMisPred, {"backend_isMisPred is 1": fc.Eq(1)}, name="Backend isMisPred is 1")

    # IFU 重定向信号覆盖点
    g.add_cover_point(dut.io_fromIfu_pdWb_valid, {"ifu_redirect_valid is 0": fc.Eq(0)}, name="IFU redirect valid is 0")
    g.add_cover_point(dut.io_fromIfu_pdWb_valid, {"ifu_redirect_valid is 1": fc.Eq(1)}, name="IFU redirect valid is 1")
    
    g.add_cover_point(dut.io_fromIfu_pdWb_bits_cfiOffset_valid, {"ifu_cfiOffset_valid is 0": fc.Eq(0)}, name="IFU cfiOffset valid is 0")
    g.add_cover_point(dut.io_fromIfu_pdWb_bits_cfiOffset_valid, {"ifu_cfiOffset_valid is 1": fc.Eq(1)}, name="IFU cfiOffset valid is 1")
    
    g.add_cover_point(dut.io_fromIfu_pdWb_bits_misOffset_valid, {"ifu_misOffset_valid is 0": fc.Eq(0)}, name="IFU misOffset valid is 0")
    g.add_cover_point(dut.io_fromIfu_pdWb_bits_misOffset_valid, {"ifu_misOffset_valid is 1": fc.Eq(1)}, name="IFU misOffset valid is 1")


  
    return g

def get_ftq_simple_timing_coverage(dut):  #qqqq

    group = CovGroup("FTQ Simple Timing Coverage")

    
    # 添加覆盖点
    group.add_watch_point(dut.io_fromBpu_resp_bits_s2_valid_3, {"ICache Request When s2 Redirect": fc.Eq(1)}, 
                         name="ICache Request When s2 Redirect")
    
    return group

@toffee_test.fixture
async def ftq_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(NewDUTFtqTop,"clock")  # 假设 DUT 类名为 DUTFtqTop，根据实际调整
    #toffee_request.add_cov_groups(ftq_cover_point(dut))  # 可选：添加覆盖
    #toffee_request.add_cov_groups(get_ftq_simple_timing_coverage(dut))  

    simple_timing_coverage = get_ftq_simple_timing_coverage(dut)#qqqqq
    simple_timing_coverage2 = ftq_cover_point(dut)




    toffee.start_clock(dut)


    ftq_bundle = FtqBundle.from_prefix('io_')
    
    ftq_bundle.bind(dut)  # 绑定到 DUT



    async def monitor_icache_req_when_ifu_redirect():  #qqqqq
        print("dcccccd")
        #await Value(dut.io_fromBpu_resp_bits_s2_valid_3, 1)
        while True:
            #print("ddddd")
            #print(dut.io_fromBpu_resp_bits_s2_valid_3.value)
            assert dut.io_fromBpu_resp_bits_s2_valid_3.value == 0
            #await Value(dut.io_fromBpu_resp_bits_s2_valid_3, 1)
            #print("wwwwww")
            simple_timing_coverage.sample()
            #print("ttttt")

        print("aaaaaa")    



    #toffee.create_task(monitor_icache_req_when_ifu_redirect())    #qqqqq


    yield FtqEnv(ftq_bundle, dut=dut)  

    
    
    print("99999999")
    #return FtqEnv(ftq_bundle, dut=dut)  
    toffee_request.cov_groups.append(simple_timing_coverage)#qqqq