from .env import *


def test_scalar_dispatch(dut):

    """验证标量Store指令派发时分配一个StoreQueue条目
    
    测试点：
        SU_DISPATCH.SCALAR_DISPATCH
    """

def test_vector_dispatch(dut):

    """验证向量Store指令的一个uop分配多个LSQ条目（根据元素数量）
    
    测试点：
        SU_DISPATCH.VECTOR_DISPATCH
    """

def test_s0_address_calc(dut):

    """验证s0阶段地址计算和仲裁
    
    测试点：
        SU_STORE.S0_ADDRESS_CALC 
    """

def test_s1_raw_check(dut):

    """验证s1阶段RAW冒险检测

    测试点：
        SU_STORE.S1_RAW_CHECK
    """

def test_s2_sq_mark_ready(dut):

    """验证s2阶段StoreQueue地址就绪标记 
    
    测试点：
        SU_STORE.S2_SQ_MARK_READY
    """

def test_split(dut):

    """验证uop拆分成多个元素
    
    测试点：
        SU_VECTOR.SPLIT
    """

def test_offset(dut):

    """验证向量元素的偏移地址计算，以及元素地址是否正确生成

    测试点：
        SU_VECTOR.OFFSET
    """

def test_tlb_miss(dut):

    """ 验证TLB响应信号和指令重发逻辑

    测试点：
        SU_REPLAY.TLB_MISS
    """

def test_violation(dut):

    """ 验证RAW违例检测机制

    测试点：
        SU_RAW.VIOLATION
    """

def test_recovery_mech(dut):

    """ 验证RAW违例后的恢复机制，包括流水线清空和重定向

    测试点：
        SU_RAW.RECOVERY_MECH
    """

def test_write_merge(dut):

    """ 验证SBuffer中的写合并功能

    测试点：
        SU_SBUFFER.WRITE_MERGE
    """

def test_plru_replace(dut):

    """ 验证SBuffer满时点PLRU替换策略

    测试点：
        SU_SBUFFER.PLRU_REPLACE
    """

def test_order(dut):

        """ 验证MMIO指令的强顺序执行，确保MMIO指令成为ROB头

    测试点：
        SU_MMIO.ORDER
    """

def test_exception(dut):

    """ 验证原子指令/向量指令访问MMIO地址空间时触发异常

    测试点：
        SU_MMIO.EXCEPTION
    """

def test_exec(dut):

    """ 验证Uncache访问的乱序执行，确保NC指令允许乱序

    测试点：
        SU_NC.EXEC
    """

def test_forward(dut):

    """ 验证Uncache模块store到load转发功能

    测试点：
        SU_NC.FORWARD
    """

def test_scalar_split(dut):

    """ 验证标量指令非对齐访问跨越16B边界时，拆分为两个对齐访问

    测试点：
        SU_MISALIGN.SCALAR_SPLIT
    """

def test_seg_handle(dut):

    """ 验证向量Segment指令的非对齐处理

    测试点：
        SU_MISALIGN.SEG_HANDLE
    """

def test_exception(dut):

    """ 验证原子指令、MMIO、NC空间非对齐访问触发异常

    测试点：
        SU_MISALIGN.EXCEPTION
    """

def test_preload(dut):

    """ 验证原子指令、MMIO、NC空间非对齐访问触发异常
    
    测试点：
        SU_ATOMIC.PRELOAD
    """

def test_preload(dut):

    """ 验证原子指令操作正确执行，包括数据读写和状态更新

    测试点：
        SU_ATOMIC.OPS
    """
