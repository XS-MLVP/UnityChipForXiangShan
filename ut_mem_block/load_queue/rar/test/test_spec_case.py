import os
import random
import toffee_test
import toffee
from comm.functions import get_out_dir, get_root_dir
from dut.LoadQueueRAR import DUTLoadQueueRAR
from .checkpoints_update_register import get_coverage_group_of_update_register
from .checkpoints_rar_static import init_rar_funcov
from ..util.dataclass import IOQuery, IOldWbPtr, IORedirect, IORelease
from ..env.LoadQueueRAREnv import LoadQueueRAREnv
from toffee_test.reporter import set_line_coverage

def generate_random_48bit_integer():
    # 生成48位的二进制字符串
    binary_string = ''.join(random.choice(['0', '1']) for _ in range(48))
    # 将二进制字符串转换为整数
    decimal_value = int(binary_string, 2)
    return decimal_value

@toffee_test.testcase
async def test_random(loadqueue_rar_env: LoadQueueRAREnv):
    random.seed(os.urandom(128))
    await loadqueue_rar_env.agent.reset()
    num_queries = 3
    for _ in range(5000):
        query = [
            IOQuery(
                req_valid=random.choice([True, False]),
                uop_robIdx_flag=random.choice([True, False]),
                uop_robIdx_value=random.randint(0, 100),
                uop_lqIdx_flag=random.choice([True, False]),
                uop_lqIdx_value=random.randint(0, 71),
                bits_paddr=generate_random_48bit_integer(),
                data_valid=random.choice([True, False]),
                is_nc=random.choice([True, False]),
                revoke=random.choice([True, False])
            )
            for i in range(num_queries)
        ]
        redirect = IORedirect(
            valid=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=random.randint(0, 100),
            level=random.randint(0, 1)
        )
        ldWbPtr = IOldWbPtr(
            flag=random.choice([True, False]),
            value=random.randint(0, 10)  # 假设 value 的范围是 0 到 10
        )
        _ = await loadqueue_rar_env.agent.Enqueue(query, redirect, ldWbPtr)

    
@toffee_test.fixture
async def loadqueue_rar_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(
        DUTLoadQueueRAR, "clock")
    toffee.start_clock(dut)
    env = LoadQueueRAREnv(dut)
    toffee_request.add_cov_groups(init_rar_funcov(env))
    toffee_request.add_cov_groups([
        get_coverage_group_of_update_register(env)
    ])
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
            