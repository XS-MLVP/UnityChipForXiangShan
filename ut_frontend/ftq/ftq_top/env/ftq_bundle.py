from toffee import *  # 导入 Toffee 框架

class IfuPdSlotBundle(Bundle):
    brType = Signal()
    isCall = Signal()
    isRet  = Signal()
    valid  = Signal()

class RobCommitBundle(Bundle):
    valid             = Signal()
    bits_commitType   = Signal()
    bits_ftqIdx_flag  = Signal()
    bits_ftqIdx_value = Signal()
    bits_ftqOffset    = Signal()     

class LastStageFtbEntryBundle(Bundle):
    valid = Signal()
    isJalr = Signal()
    isCall = Signal()
    isRet = Signal()
    brSlots_0_valid = Signal()
    brSlots_0_offset = Signal()
    tailSlot_valid = Signal()
    tailSlot_offset = Signal()
    tailSlot_sharing = Signal()


class ToIfuBundle(Bundle):  # 新增：专门处理 toIfu 相关信号
    req_ready = Signal()  # 1-bit (ready)
    req_valid = Signal()  # 新增：可能需要的信号
      # 新增：从 example.py 看到需要这个信号


class ToICacheBundle(Bundle):  # 新增：专门处理 toICache 相关信号
    req_valid = Signal()
    req_bits_readValid_0 = Signal()
    req_bits_readValid_1 = Signal()
    req_bits_readValid_2 = Signal()
    req_bits_readValid_3 = Signal()
    req_bits_readValid_4 = Signal()
    req_bits_pcMemRead_0_startAddr = Signal()
    req_bits_pcMemRead_1_startAddr = Signal()
    req_bits_pcMemRead_2_startAddr = Signal()
    req_bits_pcMemRead_3_startAddr = Signal()
    req_bits_pcMemRead_4_startAddr = Signal()
    req_bits_pcMemRead_0_nextlineStart = Signal()
    req_bits_pcMemRead_1_nextlineStart = Signal()
    req_bits_pcMemRead_2_nextlineStart = Signal()
    req_bits_pcMemRead_3_nextlineStart = Signal()
    req_bits_pcMemRead_4_nextlineStart = Signal()

class ToPrefetchBundle(Bundle):  # 新增：专门处理 toPrefetch 相关信号
    req_ready = Signal()
    req_valid = Signal()

    flushFromBpu_s2_valid = Signal()
    flushFromBpu_s2_bits_flag = Signal()
    flushFromBpu_s2_bits_value = Signal()
    flushFromBpu_s3_valid = Signal()
    flushFromBpu_s3_bits_flag = Signal()
    flushFromBpu_s3_bits_value = Signal()    

 

class FromBpuBundle(Bundle):  # 新增子Bundle类，对应 fromBpu 相关信号，继承自 Bundle
    # 定义 fromBpu 响应信号（基于提供的 example.py 中的信号）
    
    resp_valid = Signal()  # 1-bit (valid)
    resp_ready = Signal()
    resp_bits_s1_pc_3 = Signal()  # 64-bit (pc)
    resp_bits_s1_full_pred_3_fallThroughErr = Signal()  # 1-bit (fallThruError)
    
    resp_bits_s2_valid_3 = Signal()  # 1-bit (valid)
    resp_bits_s2_hasRedirect_3 = Signal()  # 1-bit (hasRedirect)
    resp_bits_s2_pc_3 = Signal()  # 64-bit (pc)
    resp_bits_s2_ftq_idx_value = Signal()  # 64-bit (ftq_idx value)
    resp_bits_s2_ftq_idx_flag = Signal()  # 1-bit (ftq_idx flag)
    resp_bits_s2_full_pred_3_fallThroughErr = Signal()  # 1-bit (fallThruError)
    resp_bits_s2_full_pred_3_hit = Signal()
    
    resp_bits_s3_valid_3 = Signal()  # 1-bit (valid)
    resp_bits_s3_hasRedirect_3 = Signal()  # 1-bit (hasRedirect)
    resp_bits_s3_pc_3 = Signal()  # 64-bit (pc)
    resp_bits_s3_ftq_idx_value = Signal()  # 64-bit (ftq_idx value)
    resp_bits_s3_ftq_idx_flag = Signal()  # 1-bit (ftq_idx flag)
    resp_bits_s3_full_pred_3_fallThroughErr = Signal()  # 1-bit (fallThruError)


    last_stage_ftb_entry = LastStageFtbEntryBundle.from_prefix("resp_bits_last_stage_ftb_entry_")

class FromBackendBundle(Bundle):  # 新增：Backend 重定向信号 Bundle
    redirect_valid = Signal()  # 1-bit (valid)
    redirect_bits_ftqIdx_value = Signal()  # 64-bit (ftqIdx value)
    redirect_bits_ftqIdx_flag = Signal()
    redirect_bits_ftqOffset = Signal()  # 64-bit (ftqOffset)
    redirect_bits_cfiUpdate_target = Signal()  # 64-bit (target)
    redirect_bits_cfiUpdate_taken = Signal()  # 1-bit (taken)
    redirect_bits_cfiUpdate_isMisPred = Signal()  # 1-bit (isMisPred)

    redirect_bits_level                    = Signal()
    redirect_bits_debugIsCtrl              = Signal()
    redirect_bits_debugIsMemVio            = Signal()

    ftqIdxSelOH_bits = Signal()
    ftqIdxAhead_0_valid = Signal()
    ftqIdxAhead_0_bits_value = Signal()

    rob_commits_0 = RobCommitBundle.from_prefix("rob_commits_0_")
    rob_commits_1 = RobCommitBundle.from_prefix("rob_commits_1_")
    rob_commits_2 = RobCommitBundle.from_prefix("rob_commits_2_")
    rob_commits_3 = RobCommitBundle.from_prefix("rob_commits_3_")
    rob_commits_4 = RobCommitBundle.from_prefix("rob_commits_4_")
    rob_commits_5 = RobCommitBundle.from_prefix("rob_commits_5_")
    rob_commits_6 = RobCommitBundle.from_prefix("rob_commits_6_")
    rob_commits_7 = RobCommitBundle.from_prefix("rob_commits_7_")

class FromIfuBundle(Bundle):  # 新增：IFU 重定向信号 Bundle
    pdWb_bits_target = Signal()  # 64-bit (target)
    pdWb_bits_cfiOffset_valid = Signal()  # 1-bit (cfiOffset valid)
    pdWb_bits_misOffset_valid = Signal()  # 1-bit (misOffset valid)
    pdWb_bits_ftqIdx_value = Signal()  # 64-bit (ftqIdx value)
    pdWb_bits_ftqIdx_flag = Signal()
    pdWb_bits_misOffset_bits = Signal()  # 64-bit (misOffset bits)
    pdWb_valid = Signal()  # 1-bit (valid)

    
    

    

        # 使用原始长名，不做精简；prefix 与 DUT 完全一致
    pdWb_bits_pd_0 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_0_")
    pdWb_bits_pd_1 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_1_")
    pdWb_bits_pd_2 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_2_")
    pdWb_bits_pd_3 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_3_")
    pdWb_bits_pd_4 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_4_")
    pdWb_bits_pd_5 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_5_")
    pdWb_bits_pd_6 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_6_")
    pdWb_bits_pd_7 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_7_")
    pdWb_bits_pd_8  = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_8_")
    pdWb_bits_pd_9  = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_9_")
    pdWb_bits_pd_10 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_10_")
    pdWb_bits_pd_11 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_11_")
    pdWb_bits_pd_12 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_12_")
    pdWb_bits_pd_13 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_13_")
    pdWb_bits_pd_14 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_14_")
    pdWb_bits_pd_15 = IfuPdSlotBundle.from_prefix("pdWb_bits_pd_15_")

    pdWb_bits_pc_0  = Signal()
    pdWb_bits_pc_1  = Signal()
    pdWb_bits_pc_2  = Signal()
    pdWb_bits_pc_3  = Signal()
    pdWb_bits_pc_4  = Signal()
    pdWb_bits_pc_5  = Signal()
    pdWb_bits_pc_6  = Signal()
    pdWb_bits_pc_7  = Signal()
    pdWb_bits_pc_8  = Signal()
    pdWb_bits_pc_9  = Signal()
    pdWb_bits_pc_10 = Signal()
    pdWb_bits_pc_11 = Signal()
    pdWb_bits_pc_12 = Signal()
    pdWb_bits_pc_13 = Signal()
    pdWb_bits_pc_14 = Signal()
    pdWb_bits_pc_15 = Signal()

class FtqBundle(Bundle):

    #加from prefix只是为了给信号加前缀，并且只适用于与dut的信号绑定，与python的变量名无关。具体在agent中驱动信号名字
    #是根据bundle的子bundle实例化名字+一个“.”符号，和我们加的前缀无关
    fromBackend = FromBackendBundle.from_prefix("fromBackend_")  # 新增
    fromIfu = FromIfuBundle.from_prefix("fromIfu_")  # 新增
    fromBpu = FromBpuBundle.from_prefix("fromBpu_")
    toIfu = ToIfuBundle.from_prefix("toIfu_")
    toICache = ToICacheBundle.from_prefix("toICache_")  # 新增
    toPrefetch = ToPrefetchBundle.from_prefix("toPrefetch_")  # 新增

