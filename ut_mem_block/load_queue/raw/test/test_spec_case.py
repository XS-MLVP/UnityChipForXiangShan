import os
import random
import toffee_test
import toffee
from dut.LoadQueueRAW import DUTLoadQueueRAW
from .checkpoints_raw_static import init_raw_funcov
from ..util.dataclass import IOQuery, IORedirect, Ptr, StoreIn
from ..env.LoadQueueRAWEnv import LoadQueueRAWEnv

@toffee_test.testcase
async def test_ctl_upadte(loadqueue_raw_env: LoadQueueRAWEnv):
    await loadqueue_raw_env.agent.reset()
    query = [
        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=5, uop_sqIdx_flag=True, uop_sqIdx_value=5, 
                mask=32767, bits_paddr=56789012345678, datavalid=True, revoke=False),

        IOQuery(valid=False, uop_preDecodeInfo_isRVC=True, uop_ftqPtr_flag=False, uop_ftqPtr_value=20, 
                uop_ftqOffset=2, uop_robIdx_flag=True, uop_robIdx_value=10, uop_sqIdx_flag=True, uop_sqIdx_value=6, 
                mask=32767, bits_paddr=67819012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=30, 
                uop_ftqOffset=3, uop_robIdx_flag=True, uop_robIdx_value=6, uop_sqIdx_flag=True, uop_sqIdx_value=7, 
                mask=32767, bits_paddr=78920123456718, datavalid=True, revoke=False)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=100, level=0)
    stIssuePtr = Ptr(flag=True, value=6)
    stAddrReadySqPtr = Ptr(flag=True, value=5)
    inner = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 1
    
    # test change stIssuePtr and stAddrReadySqPtr
    await loadqueue_raw_env.agent.reset()
    query = [
        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=5, uop_sqIdx_flag=True, uop_sqIdx_value=5, 
                mask=32767, bits_paddr=56789012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=True, uop_ftqPtr_flag=False, uop_ftqPtr_value=20, 
                uop_ftqOffset=2, uop_robIdx_flag=True, uop_robIdx_value=10, uop_sqIdx_flag=True, uop_sqIdx_value=6, 
                mask=32767, bits_paddr=67819012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=30, 
                uop_ftqOffset=3, uop_robIdx_flag=True, uop_robIdx_value=6, uop_sqIdx_flag=True, uop_sqIdx_value=7, 
                mask=32767, bits_paddr=78920123456718, datavalid=True, revoke=False)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=9, level=0)
    stIssuePtr = Ptr(flag=True, value=4)
    stAddrReadySqPtr = Ptr(flag=True, value=1)
    inner = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 2
    # loadqueue_raw_env.agent.bundle.io._stIssuePtr._value.value = 6
    loadqueue_raw_env.agent.bundle.io._stAddrReadySqPtr._value.value = 6
    await loadqueue_raw_env.agent.bundle.step(2)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 1
    
    loadqueue_raw_env.agent.bundle.io._stIssuePtr._value.value = 6
    loadqueue_raw_env.agent.bundle.io._stAddrReadySqPtr._value.value = 6
    await loadqueue_raw_env.agent.bundle.step(2)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
    query = [
        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=5, uop_sqIdx_flag=True, uop_sqIdx_value=5, 
                mask=32767, bits_paddr=56789012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=True, uop_ftqPtr_flag=False, uop_ftqPtr_value=20, 
                uop_ftqOffset=2, uop_robIdx_flag=True, uop_robIdx_value=10, uop_sqIdx_flag=True, uop_sqIdx_value=6, 
                mask=32767, bits_paddr=67819012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=30, 
                uop_ftqOffset=3, uop_robIdx_flag=True, uop_robIdx_value=6, uop_sqIdx_flag=True, uop_sqIdx_value=7, 
                mask=32767, bits_paddr=78920123456718, datavalid=True, revoke=False)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=9, level=0)
    stIssuePtr = Ptr(flag=True, value=4)
    stAddrReadySqPtr = Ptr(flag=True, value=1)
    inner = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    loadqueue_raw_env.agent.bundle.io._redirect._valid.value = True
    loadqueue_raw_env.agent.bundle.io._redirect._bits._robIdx._value.value = 4
    await loadqueue_raw_env.agent.bundle.step(2)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
    # test stIssuePtr === stAddrReadySqPtr
    await loadqueue_raw_env.agent.reset()
    query = [
        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=5, uop_sqIdx_flag=True, uop_sqIdx_value=5, 
                mask=32767, bits_paddr=56789012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=True, uop_ftqPtr_flag=False, uop_ftqPtr_value=20, 
                uop_ftqOffset=2, uop_robIdx_flag=True, uop_robIdx_value=10, uop_sqIdx_flag=True, uop_sqIdx_value=6, 
                mask=32767, bits_paddr=67819012345678, datavalid=True, revoke=False),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=30, 
                uop_ftqOffset=3, uop_robIdx_flag=True, uop_robIdx_value=6, uop_sqIdx_flag=True, uop_sqIdx_value=7, 
                mask=32767, bits_paddr=78920123456718, datavalid=True, revoke=False)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=9, level=0)
    stIssuePtr = Ptr(flag=True, value=3)
    stAddrReadySqPtr = Ptr(flag=True, value=3)
    inner = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
def generate_random_bit_integer(num: int):
    # 生成48位的二进制字符串
    binary_string = ''.join(random.choice(['0', '1']) for _ in range(num))
    # 将二进制字符串转换为整数
    decimal_value = int(binary_string, 2)
    return decimal_value

@toffee_test.testcase
async def test_freelist_full(loadqueue_raw_env: LoadQueueRAWEnv):
    await loadqueue_raw_env.agent.reset()
    for i in range(10):
        query = [
            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+1, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+2, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False)
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        stIssuePtr = Ptr(flag=True, value=4)
        stAddrReadySqPtr = Ptr(flag=True, value=1)
        _ = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(loadqueue_raw_env.agent.bundle.LoadQueueRAW._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 28
    
    # redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=56, level=0)
    # ldWbPtr = IOldWbPtr(flag=True, value=58)
    # inner = await loadqueue_rar_env.agent.Dequeue(ldWbPtr, redirect)
    # allocated = []
    # for i in range(72):
    #     allocated.append(getattr(inner._allocated, f'_{i}').value)
    # allocate = allocated.count(1)
    # assert allocate == 0
  
    await loadqueue_raw_env.agent.reset()
    for i in range(10):
        query = [
            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+1, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+2, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False)
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        stIssuePtr = Ptr(flag=True, value=4)
        stAddrReadySqPtr = Ptr(flag=True, value=2)
        _ = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(loadqueue_raw_env.agent.bundle.LoadQueueRAW._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 27
    
    await loadqueue_raw_env.agent.reset()
    for i in range(10):
        query = [
            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+1, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+2, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False)
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        stIssuePtr = Ptr(flag=True, value=4)
        stAddrReadySqPtr = Ptr(flag=True, value=3)
        _ = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(loadqueue_raw_env.agent.bundle.LoadQueueRAW._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 26
    
    for i in range(11):
        query = [
            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+1, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+2, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False),

            IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                    uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=generate_random_bit_integer(7), uop_sqIdx_flag=True, uop_sqIdx_value=i*3+3, 
                    mask=generate_random_bit_integer(16), bits_paddr=generate_random_bit_integer(48), datavalid=True, revoke=False)
        ]
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        stIssuePtr = Ptr(flag=True, value=4)
        stAddrReadySqPtr = Ptr(flag=True, value=0)
        _ = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(loadqueue_raw_env.agent.bundle.LoadQueueRAW._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 32
    # stores = [
    #     StoreIn(valid=True, robIdx_flag=True, robIdx_value=255, paddr=12345678901234, mask=65535, miss=False),
    #     StoreIn(valid=True, robIdx_flag=False, robIdx_value=128, paddr=98765432109876, mask=32768, miss=True),
    #     StoreIn(valid=False, robIdx_flag=True, robIdx_value=0, paddr=11223344556677, mask=0, miss=False)
    # ]
    
@toffee_test.testcase
async def test_ctl_revoke(loadqueue_raw_env: LoadQueueRAWEnv):
    await loadqueue_raw_env.agent.reset()
    query = [
        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=10, 
                uop_ftqOffset=1, uop_robIdx_flag=True, uop_robIdx_value=5, uop_sqIdx_flag=True, uop_sqIdx_value=5, 
                mask=32767, bits_paddr=56789012345678, datavalid=True, revoke=True),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=True, uop_ftqPtr_flag=False, uop_ftqPtr_value=20, 
                uop_ftqOffset=2, uop_robIdx_flag=True, uop_robIdx_value=10, uop_sqIdx_flag=True, uop_sqIdx_value=6, 
                mask=32767, bits_paddr=67819012345678, datavalid=True, revoke=True),

        IOQuery(valid=True, uop_preDecodeInfo_isRVC=False, uop_ftqPtr_flag=True, uop_ftqPtr_value=30, 
                uop_ftqOffset=3, uop_robIdx_flag=True, uop_robIdx_value=6, uop_sqIdx_flag=True, uop_sqIdx_value=7, 
                mask=32767, bits_paddr=78920123456718, datavalid=True, revoke=True)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=20, level=0)
    stIssuePtr = Ptr(flag=True, value=4)
    stAddrReadySqPtr = Ptr(flag=True, value=1)
    inner = await loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 3
    await loadqueue_raw_env.agent.bundle.step(1)
    allocated = []
    for i in range(32):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
# @toffee_test.testcase
# async def test_ctl_raw_violation(loadqueue_raw_env: LoadQueueRAWEnv):

@toffee_test.fixture
async def loadqueue_raw_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTLoadQueueRAW, "clock")
    toffee.start_clock(dut)
    env = LoadQueueRAWEnv(dut)
    toffee_request.add_cov_groups(init_raw_funcov(env))
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
