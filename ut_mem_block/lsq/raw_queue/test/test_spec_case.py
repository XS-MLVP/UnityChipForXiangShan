import os
import random
import toffee_test
import toffee
from dut.LoadQueueRAW import DUTLoadQueueRAW
from .checkpoints_raw_static import init_raw_funcov
from ..util.dataclass import IOQuery, IORedirect, Ptr, StoreIn
from ..env.LoadQueueRAWEnv import LoadQueueRAWEnv
from toffee import Executor

def generate_random_bit_integer(num: int):
    # 生成48位的二进制字符串
    binary_string = ''.join(random.choice(['0', '1']) for _ in range(num))
    # 将二进制字符串转换为整数
    decimal_value = int(binary_string, 2)
    return decimal_value

@toffee_test.testcase
async def test_smoke(loadqueue_raw_env: LoadQueueRAWEnv):
    random.seed(os.urandom(128))
    await loadqueue_raw_env.agent.reset()
    num_queries = 3
    for _ in range(10):
        query = [
            IOQuery(
            valid=random.choice([True, False]),
            uop_preDecodeInfo_isRVC=random.choice([True, False]),
            uop_ftqPtr_flag=random.choice([True, False]),
            uop_ftqPtr_value=generate_random_bit_integer(6),
            uop_ftqOffset=generate_random_bit_integer(4),
            uop_robIdx_flag=random.choice([True, False]),
            uop_robIdx_value=generate_random_bit_integer(8),
            uop_sqIdx_flag=random.choice([True, False]),
            uop_sqIdx_value = generate_random_bit_integer(6),
            mask=generate_random_bit_integer(16), 
            bits_paddr=generate_random_bit_integer(48),
            datavalid=random.choice([True, False]),
            revoke=random.choice([True, False]),
        )
            for i in range(num_queries)
        ]
        redirect = IORedirect(
            valid=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=generate_random_bit_integer(8),
            level=random.randint(0, 1)
        )
        stIssuePtr = Ptr(flag=random.choice([True, False]), value=generate_random_bit_integer(6))
        stAddrReadySqPtr = Ptr(flag=random.choice([True, False]), value=generate_random_bit_integer(6))
        stores = [
            StoreIn(valid=random.choice([True, False]), robIdx_flag=random.choice([True, False]), robIdx_value=generate_random_bit_integer(8), paddr=generate_random_bit_integer(48), mask=generate_random_bit_integer(16), miss=random.choice([True, False])),
            StoreIn(valid=random.choice([True, False]), robIdx_flag=random.choice([True, False]), robIdx_value=generate_random_bit_integer(8), paddr=generate_random_bit_integer(48), mask=generate_random_bit_integer(16), miss=random.choice([True, False]))
        ]
        async with Executor() as exec:
            exec(loadqueue_raw_env.agent.update(query, redirect, stIssuePtr, stAddrReadySqPtr))
            exec(loadqueue_raw_env.agent.detect(stores))

@toffee_test.fixture
async def loadqueue_raw_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTLoadQueueRAW, "clock")
    toffee.start_clock(dut)
    loadqueue_raw_env = LoadQueueRAWEnv(dut)
    toffee_request.add_cov_groups(init_raw_funcov(loadqueue_raw_env))
    
    yield loadqueue_raw_env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
