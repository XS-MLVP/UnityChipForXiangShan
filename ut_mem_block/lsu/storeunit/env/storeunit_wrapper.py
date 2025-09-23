import os
import toffee.funcov as fc
import pytest
import random
import toffee_test
from dut.StoreUnit import *
from toffee_test.reporter import set_func_coverage, set_line_coverage
from comm import get_out_dir
# ====== 功能覆盖率定义 ======
# 创建10个覆盖组对应10个功能
dispatch_cov = fc.CovGroup("SU_DISPATCH")
store_cov = fc.CovGroup("SU_STORE")
vector_cov = fc.CovGroup("SU_VECTOR")
replay_cov = fc.CovGroup("SU_REPLAY")
raw_cov = fc.CovGroup("SU_RAW")
sbuffer_cov = fc.CovGroup("SU_SBUFFER")
mmio_cov = fc.CovGroup("SU_MMIO")
nc_cov = fc.CovGroup("SU_NC")
misalign_cov = fc.CovGroup("SU_MISALIGN")

# 所有覆盖组列表
funcov_groups = [
    dispatch_cov, store_cov, vector_cov, replay_cov, raw_cov,
    sbuffer_cov, mmio_cov, nc_cov, misalign_cov
]
coverage_initialized = False

def init_dispatch_coverage(g, dut):
    """1. 指令派发功能覆盖率"""
    g.add_watch_point(dut,
        {
            # 标量指令派发：stin有效且就绪
            "SCALAR_DISPATCH": lambda x: x.io_stin_valid.value and x.io_stin_ready.value,
            # 向量指令派发：vecstin有效且就绪
            "VECTOR_DISPATCH": lambda x: x.io_vecstin_valid.value and x.io_vecstin_ready.value,
        },
        name="FC-Dispatch"
    )

def init_store_coverage(g, dut):
    """2. 地址流水线功能覆盖率"""
    g.add_watch_point(dut,
        {
            # S0阶段活动：任意输入有效
            "S0_ADDRESS_CALC": lambda x: x.io_s0_s1_valid.value,
            # S1阶段RAW检查：发出RAW查询
            "S1_RAW_CHECK": lambda x: x.io_stld_nuke_query_valid.value,
            # S2阶段SQ标记：LSQ更新地址有效
            "S2_SQ_MARK_READY": lambda x: x.io_lsq_valid.value and x.io_lsq_bits_updateAddrValid.value,
        },
        name="FC-StorePipeline"
    )

def init_vector_coverage(g, dut):
    """3. 向量内存指令执行功能覆盖率"""
    g.add_watch_point(dut,
        {
            # 向量拆分：元素数量>1
            "VECTOR_SPLIT": lambda x: x.io_vecstin_valid.value and x.io_vecstin_bits_uop_vpu_nf.value > 1,
            # 偏移计算：alignedType非零
            "VECTOR_OFFSET": lambda x: x.io_vecstin_valid.value and x.io_vecstin_bits_alignedType.value != 0,
        },
        name="FC-Vector"
    )

def init_replay_coverage(g, dut):
    """4. 重执行功能覆盖率"""
    g.add_watch_point(dut,
        {
            # TLB缺失重发：TLB响应有效且miss
            "REPLAY_TLB_MISS": lambda x: x.io_tlb_resp_valid.value and x.io_tlb_resp_bits_miss.value,
        },
        name="FC-Replay"
    )

def init_raw_coverage(g, dut):
    """5. RAW处理功能覆盖率"""
    g.add_watch_point(dut,
        {
            # RAW违例检测：发出查询且有匹配
            "RAW_VIOLATION": lambda x: x.io_stld_nuke_query_valid.value and x.io_stld_nuke_query_bits_matchLine.value,
            # 恢复机制：发生重定向
            "RAW_RECOVERY": lambda x: x.io_redirect_valid.value,
        },
        name="FC-RAW"
    )

def init_sbuffer_coverage(g, dut):
    """6. SBuffer优化功能覆盖率"""
    g.add_watch_point(dut,
        {
            # 写合并：DCache请求有效且是整行写
            "SBUFFER_MERGE": lambda x: x.io_dcache_req_valid.value and x.io_lsq_bits_wlineflag.value,
            # PLRU替换：LSQ NC访问（非缓存）
            "SBUFFER_REPLACE": lambda x: x.io_lsq_valid.value and x.io_lsq_bits_nc.value,
        },
        name="FC-SBuffer"
    )

def init_mmio_coverage(g, dut):
    """7. MMIO处理功能覆盖率"""
    g.add_watch_point(dut,
        {
            # 顺序执行：MMIO指令成为ROB头时执行
            "MMIO_ORDER": lambda x: x.io_lsq_valid.value and x.io_lsq_replenish_mmio.value,
            # 异常触发：原子/向量指令访问MMIO触发异常
            "MMIO_EXCEPTION": lambda x: x.io_lsq_valid.value and x.io_lsq_bits_uop_exceptionVec_7.value
        },
        name="FC-MMIO"
    )

def init_nc_coverage(g, dut):
    """8. Uncache功能覆盖率"""
    g.add_watch_point(dut,
        {
            # NC执行：LSQ NC访问
            "NC_EXEC": lambda x: x.io_lsq_valid.value and x.io_lsq_bits_nc.value,
            # 转发：NC存储完成
            "NC_FORWARD": lambda x: x.io_stout_valid.value and x.io_stout_bits_debug_isNC.value,
        },
        name="FC-NC"
    )

def init_misalign_coverage(g, dut):
    """9. 非对齐访问功能覆盖率"""
    g.add_watch_point(dut,
        {
            # 标量拆分：发送到未对齐缓冲区且非向量
            "MISALIGN_SCALAR_SPLIT": lambda x: x.io_misalign_buf_valid.value and not x.io_misalign_buf_bits_isvec.value,
            # 异常触发：未对齐异常
            "MISALIGN_EXCEPTION": lambda x: x.io_misalign_stout_valid.value and x.io_misalign_stout_bits_uop_exceptionVec_6.value,
        },
        name="FC-Misalign"
    )



def init_function_coverage(dut):
    """初始化所有功能覆盖率组"""
    global coverage_initialized
    
    # 如果已经初始化，直接返回
    if coverage_initialized:
        return
    init_dispatch_coverage(dispatch_cov, dut)
    init_store_coverage(store_cov, dut)
    init_vector_coverage(vector_cov, dut)
    init_replay_coverage(replay_cov, dut)
    init_raw_coverage(raw_cov, dut)
    init_sbuffer_coverage(sbuffer_cov, dut)
    init_mmio_coverage(mmio_cov, dut)
    init_nc_coverage(nc_cov, dut)
    init_misalign_coverage(misalign_cov, dut)

    coverage_initialized = True

def get_coverage_groups(dut=None):
    """返回StoreUnit功能覆盖率组列表"""
    return funcov_groups

# ====== 测试API实现 ======
@pytest.fixture()
def dut(request):
    """StoreUnit测试装置"""
    global coverage_initialized
    # 获取测试用例名称
    test_name = request.node.name
    
    # 创建覆盖率数据文件路径
    coverage_dir = get_out_dir("storeunit/coverage")
    # 确保目录存在
    os.makedirs(coverage_dir, exist_ok=True)
    coverage_file = os.path.join(coverage_dir, f"{test_name}.dat")
    
    # 创建波形文件路径
    wave_dir = get_out_dir("storeunit/wave")
    os.makedirs(wave_dir, exist_ok=True)
    wave_file = os.path.join(wave_dir, f"{test_name}.fst")
    
    # 创建DUT，指定覆盖率文件和波形文件
    dut = DUTStoreUnit(
        coverage_filename=coverage_file,
        waveform_filename=wave_file
    )
    
    # 初始化功能覆盖率
    if not coverage_initialized:
        init_function_coverage(dut)

    func_coverage_group = get_coverage_groups(dut)
    
    # 设置引脚写入时机为立即写入
    dut.io_stin_valid.AsImmWrite()
    dut.io_vecstin_valid.AsImmWrite()
    dut.io_tlb_resp_valid.AsImmWrite()
    
    # 初始化时钟
    dut.InitClock("clock")
    
    # 在时钟上升沿采样功能覆盖率
    dut.StepRis(lambda _: [g.sample() for g in func_coverage_group])
    
    setattr(dut, "fc_cover", {g.name: g for g in func_coverage_group})
    
    yield dut
    
    # 结束DUT
    dut.Finish()
    
    # 设置功能覆盖率和行覆盖率
    set_func_coverage(request, func_coverage_group)
    set_line_coverage(request, coverage_file)
    
    # 清空功能覆盖率
    for g in func_coverage_group:
        g.clear()

# 1. 指令派发功能
def api_dispatch_scalar(dut, vaddr, data, size, is_first_issue=False):
    """派发标量存储指令"""
    # 设置指令信息
    dut.io_stin_valid.value = 1
    dut.io_stin_bits_src_0.value = vaddr
    dut.io_stin_bits_uop_fuOpType.value = size - 1  # 根据大小设置操作类型
    dut.io_stin_bits_isFirstIssue.value = 1 if is_first_issue else 0
    
    # 推进时钟并检查是否就绪
    dut.Step(1)
    received = dut.io_stin_ready.value and dut.io_stin_valid.value
    
    # 复位信号
    dut.io_stin_valid.value = 0
    return bool(received)

def api_dispatch_vector(dut, base_vaddr, elem_count, elem_size):
    """派发向量存储指令"""
    dut.io_vecstin_valid.value = 1
    dut.io_vecstin_bits_basevaddr.value = base_vaddr
    dut.io_vecstin_bits_uop_vpu_nf.value = elem_count
    dut.io_vecstin_bits_uop_vpu_veew.value = int(elem_size).bit_length() - 1
    
    dut.Step(1)
    received = dut.io_vecstin_ready.value and dut.io_vecstin_valid.value
    
    dut.io_vecstin_valid.value = 0
    return bool(received)

# 2. 地址流水线功能
def api_address_pipeline(dut, vaddr, size):
    """测试地址计算流水线"""
    # S0阶段：指令派发
    api_dispatch_scalar(dut, vaddr, 0, size)
    
    # 模拟TLB响应
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_miss.value = 0
    dut.io_tlb_resp_bits_paddr_0.value = vaddr & 0xFFFFFFFFFFFF
    
    # S1阶段：RAW检查
    dut.Step(1)
    raw_check = dut.io_stld_nuke_query_valid.value
    
    # S2阶段：SQ更新
    dut.Step(1)
    sq_update = dut.io_lsq_valid.value and dut.io_lsq_bits_updateAddrValid.value
    
    dut.io_tlb_resp_valid.value = 0
    return (raw_check and sq_update), dut.io_tlb_resp_bits_paddr_0.value

# 3. 向量内存指令执行
def api_vector_execution(dut, base_vaddr, elem_data, elem_size, aligned_type=0):
    """执行向量存储指令"""
    # 派发指令
    api_dispatch_vector(dut, base_vaddr, len(elem_data), elem_size)
    
    # 设置对齐类型
    dut.io_vecstin_bits_alignedType.value = aligned_type
    
    # 处理每个元素
    success = 0
    for i, data in enumerate(elem_data):
        # 模拟TLB响应
        dut.io_tlb_resp_valid.value = 1
        dut.io_tlb_resp_bits_paddr_0.value = base_vaddr + i * elem_size
        
        # 检查向量处理状态
        dut.Step(1)
        if dut.io_vecstout_valid.value:
            success += 1
    
    dut.io_tlb_resp_valid.value = 0
    return success

# 4. 重执行功能
def api_replay_handling(dut, vaddr, size):
    """测试重执行机制"""
    # 派发指令
    api_dispatch_scalar(dut, vaddr, 0, size)
    
    # 第一次TLB响应：缺失
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_miss.value = 1
    dut.Step(1)
    
    # 模拟重执行
    retry_count = 0
    for _ in range(3):  # 最多重试3次
        # 重新派发
        dut.io_stin_valid.value = 1
        dut.Step(1)
        
        # 再次TLB响应
        if random.random() > 0.5:  # 50%概率命中
            dut.io_tlb_resp_valid.value = 1
            dut.io_tlb_resp_bits_miss.value = 0
            dut.io_tlb_resp_bits_paddr_0.value = vaddr & 0xFFFFFFFFFFFF
            dut.Step(1)
            retry_count += 1
            break
        else:
            dut.io_tlb_resp_valid.value = 1
            dut.io_tlb_resp_bits_miss.value = 1
            dut.Step(1)
            retry_count += 1
    
    # 清理
    dut.io_tlb_resp_valid.value = 0
    dut.io_stin_valid.value = 0
    return retry_count

# 5. RAW处理
def api_raw_hazard(dut, vaddr, size):
    """测试RAW冒险处理"""
    # 派发第一条存储指令
    api_dispatch_scalar(dut, vaddr, 0, size)
    
    # 模拟TLB响应
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_paddr_0.value = vaddr & 0xFFFFFFFFFFFF
    dut.Step(1)
    
    # 在S1阶段派发第二条重叠地址的指令
    dut.io_stin_valid.value = 1
    dut.io_stin_bits_src_0.value = vaddr + size - 1  # 部分重叠地址
    dut.io_stin_bits_uop_fuOpType.value = size - 1
    
    # 检查RAW查询
    dut.Step(1)
    raw_detected = dut.io_stld_nuke_query_valid.value
    
    # 触发重定向恢复
    if raw_detected:
        dut.io_redirect_valid.value = 1
        dut.io_redirect_bits_robIdx_value.value = dut.io_stin_bits_uop_robIdx_value.value
        dut.Step(1)
        dut.io_redirect_valid.value = 0
    
    # 清理
    dut.io_stin_valid.value = 0
    return bool(raw_detected)

# 6. SBuffer优化
def api_sbuffer_merge(dut, vaddr, data, is_full_line=True):
    """测试SBuffer写合并"""
    # 派发整行写指令
    api_dispatch_scalar(dut, vaddr, data, 16)  # 16字节整行
    
    # 设置整行写标志
    dut.io_stin_bits_wlineflag.value = 1 if is_full_line else 0
    
    # 模拟TLB响应
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_paddr_0.value = vaddr & 0xFFFFFFFFFFFF
    
    # 检查SBuffer优化
    dut.Step(2)
    merged = dut.io_dcache_req_valid.value and dut.io_lsq_bits_wlineflag.value
    
    dut.io_tlb_resp_valid.value = 0
    return bool(merged)

def api_sbuffer_replace(dut, vaddr, data, is_nc=True):
    """测试SBuffer替换策略"""
    # 派发NC指令
    api_dispatch_scalar(dut, vaddr, data, 8)
    
    # 设置NC标志
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_pbmt_0.value = 1 if is_nc else 0  # PBMT=1表示NC
    
    # 检查替换逻辑
    dut.Step(2)
    replaced = dut.io_lsq_valid.value and dut.io_lsq_bits_nc.value
    
    dut.io_tlb_resp_valid.value = 0
    return bool(replaced)

# 7. MMIO处理
def api_mmio_handling(dut, vaddr, data):
    """测试MMIO处理"""
    # 派发标量Store指令
    api_dispatch_scalar(dut, vaddr, data, 4)
    
    # 设置MMIO标志（通过PBMT字段）
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_pbmt_0.value = 2  # PBMT=2表示MMIO
    
    # 模拟成为ROB头（所有前序指令完成）
    dut.io_stin_bits_uop_robIdx_flag.value = 1  # 标记为ROB头
    
    # 检查MMIO处理
    dut.Step(2)
    
    # 正确检测MMIO访问
    is_mmio = dut.io_lsq_replenish_mmio.value
    # 正确检测异常（如果是原子/向量指令）
    exception = dut.io_lsq_bits_uop_exceptionVec_7.value
    
    # 清理
    dut.io_tlb_resp_valid.value = 0
    dut.io_stin_bits_uop_robIdx_flag.value = 0
    return bool(is_mmio), bool(exception)

# 8. Uncache功能
def api_uncache_access(dut, vaddr, data):
    """测试Uncache访问"""
    # 派发指令
    api_dispatch_scalar(dut, vaddr, data, 8)
    
    # 设置NC标志
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_pbmt_0.value = 1  # PBMT=1表示NC
    
    # 推进流水线
    dut.Step(2)
    
    # 检查完成状态
    completed = dut.io_stout_valid.value and dut.io_stout_bits_debug_isNC.value
    
    dut.io_tlb_resp_valid.value = 0
    return bool(completed)

# 9. 非对齐访问
def api_misaligned_access(dut, vaddr, size, is_vector=False):
    """测试非对齐访问处理"""
    if is_vector:
        # 向量非对齐访问
        dut.io_vecstin_valid.value = 1
        dut.io_vecstin_bits_vaddr.value = vaddr
        dut.io_vecstin_bits_mask.value = (1 << size) - 1  # 设置有效掩码
    else:
        # 标量非对齐访问
        api_dispatch_scalar(dut, vaddr, 0, size)
    
    # 设置TLB响应
    dut.io_tlb_resp_valid.value = 1
    dut.io_tlb_resp_bits_paddr_0.value = vaddr & 0xFFFFFFFFFFFF
    
    # 检查非对齐处理
    dut.Step(2)
    buffered = dut.io_misalign_buf_valid.value
    exception = dut.io_misalign_stout_valid.value and dut.io_misalign_stout_bits_uop_exceptionVec_6.value
    
    dut.io_tlb_resp_valid.value = 0
    return bool(buffered), bool(exception)
