import os
import random
import toffee_test
import toffee
from dut.LoadQueueReplay import DUTLoadQueueReplay
from .checkpoints_replay_static import init_replay_funcov
from ..util.dataclass import IORedirect, IOEnq, StoreAddrIn, StoreDataIn, TLChannel, ReadySqPtr, IOldWbPtr, L2Hint, TlbHint
from ..env.LoadQueueReplayEnv import LoadQueueReplayEnv
from toffee import Executor
    
@toffee_test.testcase
async def test_random(loadqueue_replay_env: LoadQueueReplayEnv):
    random.seed(os.urandom(128))
    await loadqueue_replay_env.agent.reset()
    for _ in range(2000):
        io_redirect_instance = IORedirect(
            valid=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=random.randint(0, 255),  # 随机生成 0 到 255 之间的值（8 bits）
            level=random.choice([True, False])
        )
        io_enq_instance = [
            IOEnq(
                valid=random.choice([True, False]),
                exceptionVec=[random.choice([True, False]) for _ in range(8)],  # 随机生成 8 个布尔值
                isRVC=random.choice([True, False]),
                ftqPtr_flag=random.choice([True, False]),
                ftqPtr_value=random.randint(0, 63),  # 6 bits
                ftqOffset=random.randint(0, 15),     # 4 bits
                fuOpType=random.randint(0, 511),      # 9 bits
                rfWen=random.choice([True, False]),
                fpWen=random.choice([True, False]),
                vpu_vstart=random.randint(0, 255),    # 8 bits
                vpu_veew=random.randint(0, 3),         # 2 bits
                uopIdx=random.randint(0, 127),         # 7 bits
                pdest=random.randint(0, 255),          # 8 bits
                robIdx_flag=random.choice([True, False]),
                robIdx_value=random.randint(0, 255),   # 8 bits
                storeSetHit=random.choice([True, False]),
                waitForRobIdx_flag=random.choice([True, False]),
                waitForRobIdx_value=random.randint(0, 255),  # 8 bits
                loadWaitBit=random.choice([True, False]),
                loadWaitStrict=random.choice([True, False]),
                lqIdx_flag=random.choice([True, False]),
                lqIdx_value=random.randint(0, 127),    # 7 bits
                sqIdx_flag=random.choice([True, False]),
                sqIdx_value=random.randint(0, 63),      # 6 bits
                vaddr=random.randint(0, 1125899906842623),  # 50 bits
                mask=random.randint(0, 65535),           # 16 bits
                tlbMiss=random.choice([True, False]),
                isvec=random.choice([True, False]),
                is128bit=random.choice([True, False]),
                elemIdx=random.randint(0, 255),           # 8 bits
                alignedType=random.randint(0, 7),         # 3 bits
                mbIndex=random.randint(0, 15),            # 4 bits
                reg_offset=random.randint(0, 15),         # 4 bits
                elemIdxInsideVd=random.randint(0, 255),   # 8 bits
                vecActive=random.choice([True, False]),
                isLoadReplay=random.choice([True, False]),
                handledByMSHR=random.choice([True, False]),
                schedIndex=random.randint(0, 127),        # 7 bits
                rep_info_mshr_id=random.randint(0, 15),   # 4 bits
                rep_info_full_fwd=random.choice([True, False]),
                rep_info_data_inv_sq_idx_flag=random.choice([True, False]),
                rep_info_data_inv_sq_idx_value=random.randint(0, 63),  # 6 bits
                rep_info_addr_inv_sq_idx_flag=random.choice([True, False]),
                rep_info_addr_inv_sq_idx_value=random.randint(0, 63),  # 6 bits
                rep_info_last_beat=random.choice([True, False]),
                rep_info_causes=[random.choice([True, False]) for _ in range(11)],
                rep_info_tlb_id=random.randint(0, 15),          # 4 bits
                rep_info_tlb_full=random.choice([True, False])
            ) for i in range(3)
        ]
        store_addr_in_instance = [
                StoreAddrIn(
                valid=random.choice([True, False]),
                sqIdx_flag=random.choice([True, False]),
                sqIdx_value=random.randint(0, 63),
                miss=random.choice([True, False])
            ) for i in range(2)
        ]
        store_data_in_instance = [
            StoreDataIn(
                valid=random.choice([True, False]),
                sqIdx_flag=random.choice([True, False]),
                sqIdx_value=random.randint(0, 63)
            ) for i in range(2)
        ]
        tl_channel_instance = TLChannel(
            valid=random.choice([True, False]),
            mshrid=random.randint(0, 15)
        )
        stDataReadySqPtr = ReadySqPtr(
            flag=random.choice([True, False]),
            value=random.randint(0, 63)
        )
        stAddrReadySqPtr = ReadySqPtr(
            flag=random.choice([True, False]),
            value=random.randint(0, 63)
        )
        ioldwbptr_instance = IOldWbPtr(
            flag=random.choice([True, False]),
            value=random.randint(0, 63) 
        )
        l2_hint_instance = L2Hint(
            valid=random.choice([True, False]),
            sourceId=random.randint(0, 15),
            isKeyword=random.choice([True, False])
        )
        tlb_hint_instance = TlbHint(
            valid=random.choice([True, False]),
            id=random.randint(0, 15), 
            replay_all=random.choice([True, False])
        )
        sqEmpty = random.choice([True, False])
        stAddrReadyVec = [random.choice([True, False]) for i in range(56)]
        stDataReadyVec = [random.choice([True, False]) for i in range(56)]
        rarFull = random.choice([True, False])
        rawFull = random.choice([True, False])
        async with Executor() as exec:
                exec(loadqueue_replay_env.agent.Update_queue(io_enq_instance, io_redirect_instance))
                exec(loadqueue_replay_env.agent.Update_blocking(stDataReadySqPtr, stAddrReadySqPtr, sqEmpty, store_addr_in_instance,
                                                                store_data_in_instance, stAddrReadyVec, stDataReadyVec, tlb_hint_instance,
                                                                tl_channel_instance, rarFull, ioldwbptr_instance, rawFull))
                exec(loadqueue_replay_env.agent.replay(l2_hint_instance))

@toffee_test.fixture
async def loadqueue_replay_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTLoadQueueReplay, "clock")
    toffee.start_clock(dut)
    env = LoadQueueReplayEnv(dut)
    toffee_request.add_cov_groups(init_replay_funcov(env))
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break