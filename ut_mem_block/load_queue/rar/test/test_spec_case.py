import os
import random
import toffee_test
import toffee
from comm.functions import get_out_dir, get_root_dir
from dut.LoadQueueRAR import DUTLoadQueueRAR
from .checkpoints_rar_static import init_rar_funcov
from ..util.dataclass import IOQuery, IOldWbPtr, IORedirect, IORelease
from ..env.LoadQueueRAREnv import LoadQueueRAREnv
from toffee_test.reporter import set_line_coverage

# from comm import TAG_LONG_TIME_RUN, TAG_SMOKE, TAG_RARELY_USED, debug

@toffee_test.testcase
async def test_ctl_enqueue(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test enqueue when the enqueue control signal is satisfied.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1, uop_lqIdx_flag=True, 
                uop_lqIdx_value=2, bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=False, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect()
    #redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=1, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=4)
    inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 1
    
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=4, bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=654321, data_valid=True, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=4, level=1)
    ldWbPtr = IOldWbPtr(flag=True, value=1)
    inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 2
    
    
    
@toffee_test.testcase
async def test_ctl_dequeue(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test dequeue when the dequeue control signal is satisfied.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=123456, data_valid=True, is_nc=False, revoke=True),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=654321, data_valid=True, is_nc=False, revoke=False),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=9, uop_lqIdx_flag=True, 
                uop_lqIdx_value=7, bits_paddr=111111, data_valid=True, is_nc=False, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=10, level=1)
    ldWbPtr = IOldWbPtr(flag=True, value=1)
    inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    # allocate = allocated.count(1)
    
    redirect_new = IORedirect(valid=True, robIdx_flag=True, robIdx_value=7, level=0)
    ldWbPtr_new = IOldWbPtr(flag=True, value=4)
    inner_after = await loadqueue_rar_env.agent.Dequeue(ldWbPtr_new, redirect_new)
    
    allocated_after = []
    for i in range(72):
        allocated_after.append(getattr(inner_after._allocated, f'_{i}').value)
    allocated_after = allocated_after.count(1)
    assert allocated_after == 0
    
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=123456, data_valid=True, is_nc=False, revoke=True),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=654321, data_valid=True, is_nc=False, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=9, uop_lqIdx_flag=True, 
                uop_lqIdx_value=7, bits_paddr=111111, data_valid=True, is_nc=False, revoke=True),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=10, level=1)
    ldWbPtr = IOldWbPtr(flag=True, value=1)
    inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    await loadqueue_rar_env.agent.bundle.step(2)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
@toffee_test.testcase
async def test_revoke_redirect(loadqueue_rar_env:LoadQueueRAREnv):
    """
     Test revoke when the revoke control signal is satisfied in the last cycle.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=123456, data_valid=True, is_nc=False, revoke=True),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=654321, data_valid=True, is_nc=False, revoke=False),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=9, uop_lqIdx_flag=True, 
                uop_lqIdx_value=7, bits_paddr=111111, data_valid=True, is_nc=False, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=10, level=1)
    ldWbPtr = IOldWbPtr(flag=True, value=1)
    inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    assert inner._allocated._0.value == 1
    loadqueue_rar_env.agent.bundle.io._redirect._bits._robIdx._value.value = 4
    await loadqueue_rar_env.agent.bundle.step(1)
    assert inner._allocated._0.value == 0
    
@toffee_test.testcase
async def test_ctl_releasedupdate(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test the update of the released register and the query for RAR violation.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=4, bits_paddr=747113358170, data_valid=False, is_nc=True, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=5, uop_lqIdx_flag=True, 
                uop_lqIdx_value=6, bits_paddr=183041682239, data_valid=True, is_nc=False, revoke=False),
        
        IOQuery(req_valid=False, uop_robIdx_flag=True, uop_robIdx_value=3, uop_lqIdx_flag=True, 
                uop_lqIdx_value=8, bits_paddr=773314057378, data_valid=True, is_nc=False, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=10, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=1)
    loadqueue_rar_env.agent.bundle.io._release._valid.value = True
    loadqueue_rar_env.agent.bundle.io._release._bits_paddr.value = 183041682239
    _ = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    released = []
    for i in range(72):
        released.append(getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._released, f'_{i}').value)
    release = released.count(1)
    assert release == 2
    loadqueue_rar_env.agent.bundle.io._query._2._req._valid.value = True
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._uop._robIdx._flag.value = True
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._uop._robIdx._value.value = 3
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._uop._lqIdx._flag.value = True
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._uop._lqIdx._value.value = 8
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._paddr.value = 773314057378
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._data_valid.value = True
    loadqueue_rar_env.agent.bundle.io._query._2._req._bits._is_nc.value = False
    loadqueue_rar_env.agent.bundle.io._query._2._revoke.value = False
    loadqueue_rar_env.agent.bundle.io._ldWbPtr._flag.value = True
    loadqueue_rar_env.agent.bundle.io._ldWbPtr._value.value = 1
    loadqueue_rar_env.agent.bundle.io._redirect._valid.value = False
    await loadqueue_rar_env.agent.bundle.step(1)
    loadqueue_rar_env.agent.bundle.io._release._valid.value = True
    loadqueue_rar_env.agent.bundle.io._release._bits_paddr.value = 773314057378
    await loadqueue_rar_env.agent.bundle.step(1)
    loadqueue_rar_env.agent.bundle.io._release._valid.value = False
    await loadqueue_rar_env.agent.bundle.step(1)
    released_after_1 = []
    for i in range(72):
        released_after_1.append(getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._released, f'_{i}').value)
    release_after_1 = released_after_1.count(1)
    assert release_after_1 == 3
    query_after_2 = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=6, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=109635647804, data_valid=False, is_nc=False, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=8, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=281474976710655, data_valid=True, is_nc=False, revoke=False),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=7, bits_paddr=183041682239, data_valid=True, is_nc=False, revoke=False),
    ]
    _ = await loadqueue_rar_env.agent.Enqueue(query_after_2, redirect, ldWbPtr)
    loadqueue_rar_env.agent.bundle.io._release._valid.value = True
    loadqueue_rar_env.agent.bundle.io._release._bits_paddr.value = 281474976710655
    await loadqueue_rar_env.agent.bundle.step(1)
    loadqueue_rar_env.agent.bundle.io._release._valid.value = False
    await loadqueue_rar_env.agent.bundle.step(1)
    assert loadqueue_rar_env.agent.bundle.io._query._2._resp._bits_rep_frm_fetch.value == 1
    query_after_3 = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1, uop_lqIdx_flag=True, 
                uop_lqIdx_value=1, bits_paddr=747113358170, data_valid=False, is_nc=False, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=6, bits_paddr=773314057378, data_valid=True, is_nc=False, revoke=False),
        
        IOQuery(req_valid=False, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=7, bits_paddr=281474976710655, data_valid=True, is_nc=False, revoke=False),
    ]
    _ = await loadqueue_rar_env.agent.Enqueue(query_after_3, redirect, ldWbPtr)
    await loadqueue_rar_env.agent.bundle.step(2)
    assert loadqueue_rar_env.agent.bundle.io._query._0._resp._bits_rep_frm_fetch.value == 1 \
        and loadqueue_rar_env.agent.bundle.io._query._1._resp._bits_rep_frm_fetch.value == 1
    
@toffee_test.testcase
async def test_enqueue_dequeue_parallel(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test the scenario when enqueue and dequeue occur simultaneously.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=7, uop_lqIdx_flag=True, 
                uop_lqIdx_value=2, bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=4, uop_lqIdx_flag=True, 
                uop_lqIdx_value=3, bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=9, uop_lqIdx_flag=True, 
                uop_lqIdx_value=5, bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=10, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=1)
    inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 3
    
    query_new = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=7, bits_paddr=78658392, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3, uop_lqIdx_flag=True, 
                uop_lqIdx_value=4, bits_paddr=32467548, data_valid=False, is_nc=True, revoke=False),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1, uop_lqIdx_flag=True, 
                uop_lqIdx_value=6, bits_paddr=23476345, data_valid=False, is_nc=True, revoke=False),
    ]
    redirect_new = IORedirect(valid=True, robIdx_flag=True, robIdx_value=8, level=0)
    ldWbPtr_new = IOldWbPtr(flag=True, value=2)
    inner_new = await loadqueue_rar_env.agent.Enqueue(query_new, redirect_new, ldWbPtr_new)
    allocated_new = []
    for i in range(72):
        allocated_new.append(getattr(inner_new._allocated, f'_{i}').value)
    allocate_new = allocated_new.count(1)
    assert allocate_new == 3
    
def generate_random_48bit_integer():
    # 生成48位的二进制字符串
    binary_string = ''.join(random.choice(['0', '1']) for _ in range(48))
    # 将二进制字符串转换为整数
    decimal_value = int(binary_string, 2)
    return decimal_value

@toffee_test.testcase
async def test_freelist_boundary(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test the boundary scenarios of the free list.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    for i in range(23):
        query = [
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+1, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+1, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
            
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+2, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+2, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=0, level=0)
        ldWbPtr = IOldWbPtr(flag=True, value=0)
        _ = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    query_new = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=69, bits_paddr=78658392, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=True, uop_robIdx_value=3, uop_lqIdx_flag=True, 
                uop_lqIdx_value=71, bits_paddr=32467548, data_valid=False, is_nc=True, revoke=False),
        
        IOQuery(req_valid=False, uop_robIdx_flag=True, uop_robIdx_value=1, uop_lqIdx_flag=True, 
                uop_lqIdx_value=70, bits_paddr=23476345, data_valid=False, is_nc=True, revoke=False),
    ]
    redirect_new = IORedirect(valid=False, robIdx_flag=True, robIdx_value=100, level=0)
    ldWbPtr_new = IOldWbPtr(flag=True, value=0)
    _ = await loadqueue_rar_env.agent.Enqueue(query_new, redirect_new, ldWbPtr_new)
    query_full = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=2, uop_lqIdx_flag=True, 
                uop_lqIdx_value=70, bits_paddr=78658392, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3, uop_lqIdx_flag=True, 
                uop_lqIdx_value=71, bits_paddr=32467548, data_valid=True, is_nc=False, revoke=False),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1, uop_lqIdx_flag=True, 
                uop_lqIdx_value=57, bits_paddr=23476345, data_valid=True, is_nc=False, revoke=False),
    ]
    redirect_full = IORedirect(valid=False, robIdx_flag=True, robIdx_value=100, level=0)
    ldWbPtr_full = IOldWbPtr(flag=True, value=0)
    inner = await loadqueue_rar_env.agent.Enqueue(query_full, redirect_full, ldWbPtr_full)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72 and loadqueue_rar_env.agent.bundle.io._lqFull
    
    redirect_full = IORedirect(valid=True, robIdx_flag=True, robIdx_value=100, level=0)
    ldWbPtr_full = IOldWbPtr(flag=True, value=4)
    inner = await loadqueue_rar_env.agent.Dequeue(ldWbPtr_full, redirect_full)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 68
    
@toffee_test.testcase
async def test_freelist_full(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test the full scenarios of the free list.

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    for i in range(24):
        query = [
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+1, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+1, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+2, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+2, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
            
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+3, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=0, level=0)
        ldWbPtr = IOldWbPtr(flag=True, value=0)
        _ = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72
  
    await loadqueue_rar_env.agent.reset()
    for i in range(24):
        query = [
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+1, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+1, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+2, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+2, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
            
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+3, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=0, level=0)
        ldWbPtr = IOldWbPtr(flag=True, value=1)
        _ = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 71
    
    await loadqueue_rar_env.agent.reset()
    for i in range(24):
        query = [
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+1, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+1, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3+2, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+2, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
            
            IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=i*3, uop_lqIdx_flag=True, 
                    uop_lqIdx_value=i*3+3, bits_paddr=generate_random_48bit_integer(), data_valid=True, is_nc=False, revoke=False),
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=0, level=0)
        ldWbPtr = IOldWbPtr(flag=True, value=2)
        _ = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 70
    
@toffee_test.fixture
async def loadqueue_rar_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTLoadQueueRAR, "clock")
    toffee.start_clock(dut)
    env = LoadQueueRAREnv(dut)
    toffee_request.add_cov_groups(init_rar_funcov(env))
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break