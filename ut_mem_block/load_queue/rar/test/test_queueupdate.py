import os
import random
import toffee_test
import toffee
from dut.LoadQueueRAR import DUTLoadQueueRAR
from .checkpoints_rar_static import init_rar_funcov
from ..util.dataclass import IOQuery, IOldWbPtr, IORedirect, IORelease
from ..env.LoadQueueRAREnv import LoadQueueRAREnv

# from comm import TAG_LONG_TIME_RUN, TAG_SMOKE, TAG_RARELY_USED, debug

@toffee_test.testcase
async def test_can_enqueue_smoke(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test the RVI instruction set. randomly generate instructions for testing

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    # print(rar_queue.req)
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1,
             bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=False, uop_robIdx_value=2,
                bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3,
                bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=5, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=100)
    res, inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = any(allocated)
    ready = any(res)
    assert (ready == 1 and allocate == 1)
    
@toffee_test.testcase
async def test_can_dequeue_smoke(loadqueue_rar_env: LoadQueueRAREnv):
    """
     Test the RVI instruction set. randomly generate instructions for testing

     Args:
         loadqueue_rar_env(fixure): the fixture of the LoadQueueRAR
    """
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1,
             bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=False, uop_robIdx_value=2,
                bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3,
                bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=5, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=100)
    _ , inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    # allocated = []
    count = 0
    for i in range(72):
        if getattr(inner._allocated, f'_{i}').value == 1:
            count = count + 1
    redirect_new = IORedirect(valid=True, robIdx_flag=True, robIdx_value=3, level=1)
    ldWbPtr_new = IOldWbPtr(flag=False, value=10)
    release = IORelease(valid=True, paddr=123456)
    loadqueue_rar_env.agent.bundle.io._query._0._req._valid.value = 0
    loadqueue_rar_env.agent.bundle.io._query._1._req._valid.value = 0
    loadqueue_rar_env.agent.bundle.io._query._2._req._valid.value = 0
    _, _, inner = await loadqueue_rar_env.agent.Dequeue(ldWbPtr_new, redirect_new, release)
    count_after = 0
    for i in range(72):
        if getattr(inner._allocated, f'_{i}').value == 1:
            count_after = count_after + 1
    assert (count_after < count)
    
@toffee_test.testcase
async def test_can_detect_smoke(loadqueue_rar_env: LoadQueueRAREnv):
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1,
             bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=False, uop_robIdx_value=2,
                bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3,
                bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=5, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=100)
    _ , inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1,
             bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=True, uop_robIdx_value=2,
                bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3,
                bits_paddr=789654, data_valid=True, is_nc=True, revoke=False),
    ]
    resp_flag, inner = await loadqueue_rar_env.agent.detect(query)
    resp_flag, inner = await loadqueue_rar_env.agent.detect(query)
    resp_flag, inner = await loadqueue_rar_env.agent.detect(query)
    print("LLLLL", resp_flag)
    
@toffee_test.testcase
async def test_can_releasedupdate(loadqueue_rar_env: LoadQueueRAREnv):
    await loadqueue_rar_env.agent.reset()
    query = [
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=1,
             bits_paddr=123456, data_valid=True, is_nc=False, revoke=False),
    
        IOQuery(req_valid=False, uop_robIdx_flag=False, uop_robIdx_value=2,
                bits_paddr=654321, data_valid=False, is_nc=True, revoke=True),
        
        IOQuery(req_valid=True, uop_robIdx_flag=True, uop_robIdx_value=3,
                bits_paddr=111111, data_valid=True, is_nc=True, revoke=False),
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=5, level=0)
    ldWbPtr = IOldWbPtr(flag=True, value=100)
    _ , inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    _ , inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    _ , inner = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)
    release = IORelease(valid=True, paddr=123456)
    released = await loadqueue_rar_env.agent.releasedupdate(release)
    print("TTTTTTT", released)
      
  
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