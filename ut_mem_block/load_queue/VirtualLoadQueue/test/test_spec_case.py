import os
import random
import toffee_test
import toffee
from dut.VirtualLoadQueue import DUTVirtualLoadQueue
from .checkpoints_virtual_static import init_virtual_funcov
from ..util.dataclass import IORedirect, VecCommit, EnqReq, LdIn
from ..env.VirtualLoadQueueEnv import VirtualLoadQueueEnv
from toffee import Executor

@toffee_test.testcase
async def test_random(loadqueue_virtual_env: VirtualLoadQueueEnv):
    random.seed(os.urandom(128))
    await loadqueue_virtual_env.agent.reset()
    for _ in range(5000):
        # 随机生成实例
        ior_redirect = IORedirect(
            valid=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=random.randint(0, 255),  # 假设 robIdx_value 在 0-255 之间
            level=random.choice([0, 1])
        )

        vec_commit = [
            VecCommit(
                valid=random.choice([True, False]),
                robidx_flag=random.choice([True, False]),
                robidx_value=random.randint(0, 255),  # 假设 robidx_value 在 0-255 之间
                uopidx=random.randint(0, 127)  # 假设 uopidx 在 0-15 之间
            ) for i in range(2)
        ]

        enq_req = [
            EnqReq(
                valid=random.choice([True, False]),
                fuType=random.randint(0, 5),  # 假设 fuType 在 0-5 之间
                uopIdx=random.randint(0, 127),  # 假设 uopIdx 在 0-15 之间
                robIdx_flag=random.choice([True, False]),
                robIdx_value=random.randint(0, 255),  # 假设 robIdx_value 在 0-255 之间
                lqIdx_flag=random.choice([True, False]),
                lqIdx_value=random.randint(0, 127),  # 假设 lqIdx_value 在 0-255 之间
                numLsElem=random.randint(0, 32)  # 假设 numLsElem 在 0-10 之间
            ) for i in range(6)
        ]

        ld_in = [
            LdIn(
                valid=random.choice([True, False]),
                uop_lqIdx_value=random.randint(0, 127),  # 假设 uop_lqIdx_value 在 0-255 之间
                isvec=random.choice([True, False]),
                updateAddrValid=random.choice([True, False]),
                rep_info_cause=random.choices([0, 1], k=11)  # 生成一个包含 11 个元素（0或1）的数组
            ) for i in range(3)
        ]

        async with Executor() as exec:
                exec(loadqueue_virtual_env.agent.update(enq_req, ior_redirect))
                exec(loadqueue_virtual_env.agent.commit(vec_commit))
                exec(loadqueue_virtual_env.agent.writeback(ld_in))
                
@toffee_test.fixture
async def loadqueue_virtual_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTVirtualLoadQueue, "clock")
    toffee.start_clock(dut)
    env = VirtualLoadQueueEnv(dut)
    toffee_request.add_cov_groups(init_virtual_funcov(env))
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break