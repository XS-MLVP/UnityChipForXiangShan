import os
import random

import toffee
import toffee_test
from toffee import Executor

from dut.VirtualLoadQueue import DUTVirtualLoadQueue
from .checkpoints_virtual_static import init_virtual_funcov
from ..env.VirtualLoadQueueEnv import VirtualLoadQueueEnv
from ..util.dataclass import IORedirect, VecCommit, EnqReq, LdIn


@toffee_test.testcase
async def test_ctl_update(loadqueue_virtual_env: VirtualLoadQueueEnv):
    await loadqueue_virtual_env.agent.reset()
    enq = [
        EnqReq(valid=True, fuType=2, uopIdx=5, robIdx_flag=True, robIdx_value=4, lqIdx_flag=False,
               lqIdx_value=1, numLsElem=3),
        EnqReq(valid=True, fuType=9, uopIdx=6, robIdx_flag=True, robIdx_value=6, lqIdx_flag=False,
               lqIdx_value=2, numLsElem=5),
        EnqReq(valid=False, fuType=30, uopIdx=9, robIdx_flag=True, robIdx_value=9, lqIdx_flag=False,
               lqIdx_value=3, numLsElem=7),
        EnqReq(valid=True, fuType=78, uopIdx=10, robIdx_flag=True, robIdx_value=3, lqIdx_flag=False,
               lqIdx_value=4, numLsElem=1),
        EnqReq(valid=False, fuType=42, uopIdx=17, robIdx_flag=True, robIdx_value=1, lqIdx_flag=False,
               lqIdx_value=5, numLsElem=2),
        EnqReq(valid=True, fuType=26, uopIdx=14, robIdx_flag=True, robIdx_value=2, lqIdx_flag=False,
               lqIdx_value=6, numLsElem=7)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=5, level=0)
    inner = await loadqueue_virtual_env.agent.update(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 11

    loadqueue_virtual_env.agent.bundle.io._redirect._valid.value = True
    loadqueue_virtual_env.agent.bundle.io._redirect._bits._robIdx._value.value = 1
    await loadqueue_virtual_env.agent.bundle.step(2)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_virtual_env.agent.bundle.VirtualLoadQueue._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0


@toffee_test.testcase
async def test_ctl_commit(loadqueue_virtual_env: VirtualLoadQueueEnv):
    await loadqueue_virtual_env.agent.reset()
    enq = [
        EnqReq(valid=True, fuType=0x080000000, uopIdx=5, robIdx_flag=True, robIdx_value=4, lqIdx_flag=False,
               lqIdx_value=0, numLsElem=3),
        EnqReq(valid=True, fuType=0x200000000, uopIdx=6, robIdx_flag=True, robIdx_value=6, lqIdx_flag=False,
               lqIdx_value=3, numLsElem=5),
        EnqReq(valid=False, fuType=9, uopIdx=9, robIdx_flag=True, robIdx_value=9, lqIdx_flag=False,
               lqIdx_value=9, numLsElem=7),
        EnqReq(valid=True, fuType=13, uopIdx=10, robIdx_flag=True, robIdx_value=3, lqIdx_flag=False,
               lqIdx_value=9, numLsElem=1),
        EnqReq(valid=False, fuType=24, uopIdx=17, robIdx_flag=True, robIdx_value=1, lqIdx_flag=False,
               lqIdx_value=10, numLsElem=2),
        EnqReq(valid=True, fuType=17, uopIdx=14, robIdx_flag=True, robIdx_value=2, lqIdx_flag=False,
               lqIdx_value=10, numLsElem=7)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=19, level=0)
    inner = await loadqueue_virtual_env.agent.update(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 16

    vec_commit = [
        VecCommit(valid=True, robidx_flag=True, robidx_value=4, uopidx=5),
        VecCommit(valid=True, robidx_flag=True, robidx_value=6, uopidx=6)
    ]
    inner = await loadqueue_virtual_env.agent.commit(vec_commit)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 8


@toffee_test.testcase
async def test_ctl_writeback(loadqueue_virtual_env: VirtualLoadQueueEnv):
    await loadqueue_virtual_env.agent.reset()
    enq = [
        EnqReq(valid=True, fuType=4, uopIdx=5, robIdx_flag=True, robIdx_value=4, lqIdx_flag=False,
               lqIdx_value=0, numLsElem=1),
        EnqReq(valid=True, fuType=0x200000000, uopIdx=6, robIdx_flag=True, robIdx_value=6, lqIdx_flag=False,
               lqIdx_value=3, numLsElem=5),
        EnqReq(valid=False, fuType=9, uopIdx=9, robIdx_flag=True, robIdx_value=9, lqIdx_flag=False,
               lqIdx_value=9, numLsElem=7),
        EnqReq(valid=True, fuType=13, uopIdx=10, robIdx_flag=True, robIdx_value=3, lqIdx_flag=False,
               lqIdx_value=9, numLsElem=1),
        EnqReq(valid=False, fuType=24, uopIdx=17, robIdx_flag=True, robIdx_value=1, lqIdx_flag=False,
               lqIdx_value=10, numLsElem=2),
        EnqReq(valid=True, fuType=17, uopIdx=14, robIdx_flag=True, robIdx_value=2, lqIdx_flag=False,
               lqIdx_value=10, numLsElem=7)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=19, level=0)
    inner = await loadqueue_virtual_env.agent.update(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 14

    ld_in = [
        LdIn(valid=True, uop_lqIdx_value=0, isvec=False, updateAddrValid=True,
             rep_info_cause=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        LdIn(valid=True, uop_lqIdx_value=3, isvec=True, updateAddrValid=False,
             rep_info_cause=[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]),
        LdIn(valid=True, uop_lqIdx_value=10, isvec=False, updateAddrValid=True,
             rep_info_cause=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ]
    inner = await loadqueue_virtual_env.agent.writeback(ld_in)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 13


@toffee_test.testcase
async def test_ldin_commit_parallel(loadqueue_virtual_env: VirtualLoadQueueEnv):
    await loadqueue_virtual_env.agent.reset()
    enq = [
        EnqReq(valid=True, fuType=4, uopIdx=5, robIdx_flag=True, robIdx_value=4, lqIdx_flag=False,
               lqIdx_value=0, numLsElem=1),
        EnqReq(valid=True, fuType=0x200000000, uopIdx=6, robIdx_flag=True, robIdx_value=6, lqIdx_flag=False,
               lqIdx_value=1, numLsElem=5),
        EnqReq(valid=False, fuType=9, uopIdx=9, robIdx_flag=True, robIdx_value=9, lqIdx_flag=False,
               lqIdx_value=9, numLsElem=7),
        EnqReq(valid=True, fuType=13, uopIdx=10, robIdx_flag=True, robIdx_value=3, lqIdx_flag=False,
               lqIdx_value=9, numLsElem=1),
        EnqReq(valid=False, fuType=24, uopIdx=17, robIdx_flag=True, robIdx_value=1, lqIdx_flag=False,
               lqIdx_value=10, numLsElem=2),
        EnqReq(valid=True, fuType=17, uopIdx=14, robIdx_flag=True, robIdx_value=2, lqIdx_flag=False,
               lqIdx_value=10, numLsElem=7)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=19, level=0)
    inner = await loadqueue_virtual_env.agent.update(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 14

    ld_in = [
        LdIn(valid=True, uop_lqIdx_value=0, isvec=False, updateAddrValid=True,
             rep_info_cause=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        LdIn(valid=True, uop_lqIdx_value=3, isvec=True, updateAddrValid=False,
             rep_info_cause=[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]),
        LdIn(valid=True, uop_lqIdx_value=10, isvec=False, updateAddrValid=True,
             rep_info_cause=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ]
    vec_commit = [
        VecCommit(valid=True, robidx_flag=True, robidx_value=6, uopidx=6),
        VecCommit(valid=True, robidx_flag=True, robidx_value=7, uopidx=5)
    ]
    async with Executor() as exec:
        exec(loadqueue_virtual_env.agent.commit(vec_commit))
        exec(loadqueue_virtual_env.agent.writeback(ld_in))
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_virtual_env.agent.bundle.VirtualLoadQueue._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 8


@toffee_test.testcase
async def test_queue_full(loadqueue_virtual_env: VirtualLoadQueueEnv):
    await loadqueue_virtual_env.agent.reset()
    enq = [
        EnqReq(valid=True, fuType=4, uopIdx=5, robIdx_flag=True, robIdx_value=4, lqIdx_flag=False,
               lqIdx_value=0, numLsElem=16),
        EnqReq(valid=True, fuType=0x200000000, uopIdx=6, robIdx_flag=True, robIdx_value=6, lqIdx_flag=False,
               lqIdx_value=16, numLsElem=16),
        EnqReq(valid=True, fuType=9, uopIdx=9, robIdx_flag=True, robIdx_value=9, lqIdx_flag=False,
               lqIdx_value=16 * 2, numLsElem=16),
        EnqReq(valid=True, fuType=13, uopIdx=10, robIdx_flag=True, robIdx_value=3, lqIdx_flag=False,
               lqIdx_value=16 * 3, numLsElem=16),
        EnqReq(valid=True, fuType=24, uopIdx=17, robIdx_flag=True, robIdx_value=1, lqIdx_flag=False,
               lqIdx_value=16 * 4, numLsElem=16),
        EnqReq(valid=False, fuType=17, uopIdx=20, robIdx_flag=True, robIdx_value=2, lqIdx_flag=False,
               lqIdx_value=16 * 5, numLsElem=16)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=19, level=0)
    inner = await loadqueue_virtual_env.agent.update(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72 and loadqueue_virtual_env.agent.bundle.io._lqEmpty.value == 1


@toffee_test.testcase
async def test_random(loadqueue_virtual_env: VirtualLoadQueueEnv):
    random.seed(os.urandom(128))
    await loadqueue_virtual_env.agent.reset()
    for _ in range(5000):
        # 随机生成实例
        ior_redirect = IORedirect(
            valid=not random.getrandbits(1),
            robIdx_flag=not random.getrandbits(1),
            robIdx_value=random.randint(0, 255),  # 假设 robIdx_value 在 0-255 之间
            level=random.getrandbits(1)
        )

        vec_commit = [
            VecCommit(
                valid=not random.getrandbits(1),
                robidx_flag=not random.getrandbits(1),
                robidx_value=random.randint(0, 255),  # 假设 robidx_value 在 0-255 之间
                uopidx=random.randint(0, 127)  # 假设 uopidx 在 0-15 之间
            ) for i in range(2)
        ]

        enq_req = [
            EnqReq(
                valid=not random.getrandbits(1),
                fuType=random.randint(0, 5),  # 假设 fuType 在 0-5 之间
                uopIdx=random.randint(0, 127),  # 假设 uopIdx 在 0-15 之间
                robIdx_flag=not random.getrandbits(1),
                robIdx_value=random.randint(0, 255),  # 假设 robIdx_value 在 0-255 之间
                lqIdx_flag=not random.getrandbits(1),
                lqIdx_value=random.randint(0, 127),  # 假设 lqIdx_value 在 0-255 之间
                numLsElem=random.randint(0, 32)  # 假设 numLsElem 在 0-10 之间
            ) for i in range(6)
        ]

        ld_in = [
            LdIn(
                valid=not random.getrandbits(1),
                uop_lqIdx_value=random.randint(0, 127),  # 假设 uop_lqIdx_value 在 0-255 之间
                isvec=not random.getrandbits(1),
                updateAddrValid=not random.getrandbits(1),
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
