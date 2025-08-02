import os
import random
import toffee_test
import toffee
from dut.LoadQueueUncache import DUTLoadQueueUncache
from .checkpoints_uncache_static import init_uncache_funcov
from ..util.dataclass import IORedirect, RobIO, ReqIO, Uncache
from ..env.LoadQueueUncacheEnv import LoadQueueUncacheEnv
from toffee import Executor
    
@toffee_test.testcase
async def test_smoke(loadqueue_uncache_env: LoadQueueUncacheEnv):
    random.seed(os.urandom(128))
    await loadqueue_uncache_env.agent.reset()
    for _ in range(10):
        ior_redirect = IORedirect(
            valid=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=random.randint(0, 255),
            level=random.choice([True, False])
        )
        rob_io = RobIO(
            pendingMMIOld=random.choice([True, False]),
            pendingPtr_flag=random.choice([True, False]),
            pendingPtr_value=random.randint(0, 255)
        )
        req_io = [
                ReqIO(
                valid=random.choice([True, False]),
                bits_uop_exceptionVec_3=random.choice([True, False]),
                bits_uop_exceptionVec_4=random.choice([True, False]),
                bits_uop_exceptionVec_5=random.choice([True, False]),
                bits_uop_exceptionVec_13=random.choice([True, False]),
                bits_uop_exceptionVec_21=random.choice([True, False]),
                bits_uop_trigger=random.randint(0, 15),  # 4-bit value
                bits_uop_preDecodeInfo_isRVC=random.choice([True, False]),
                bits_uop_ftqPtr_flag=random.choice([True, False]),
                bits_uop_ftqPtr_value=random.randint(0, 63),  # 6-bit value
                bits_uop_ftqOffset=random.randint(0, 15),  # 4-bit value
                bits_uop_fuOpType=random.randint(0, 511),  # 9-bit value
                bits_uop_rfWen=random.choice([True, False]),
                bits_uop_fpWen=random.choice([True, False]),
                bits_uop_vpu_vstart=random.randint(0, 255),  # 8-bit value
                bits_uop_vpu_veew=random.randint(0, 3),  # 2-bit value
                bits_uop_uopIdx=random.randint(0, 127),  # 7-bit value
                bits_uop_pdest=random.randint(0, 255),  # 8-bit value
                bits_uop_robIdx_flag=random.choice([True, False]),
                bits_uop_robIdx_value=random.randint(0, 255),  # 8-bit value
                bits_uop_storeSetHit=random.choice([True, False]),
                bits_uop_waitForRobIdx_flag=random.choice([True, False]),
                bits_uop_waitForRobIdx_value=random.randint(0, 255),  # 8-bit value
                bits_uop_loadWaitBit=random.choice([True, False]),
                bits_uop_loadWaitStrict=random.choice([True, False]),
                bits_uop_lqIdx_flag=random.choice([True, False]),
                bits_uop_lqIdx_value=random.randint(0, 127),  # 7-bit value
                bits_uop_sqIdx_flag=random.choice([True, False]),
                bits_uop_sqIdx_value=random.randint(0, 63),  # 6-bit value
                bits_vaddr=random.randint(0, 1125899906842623),  # 50-bit value
                bits_fullva=random.randint(0, 18446744073709551615),  # 64-bit value
                bits_isHyper=random.choice([True, False]),
                bits_paddr=random.randint(0, 281474976710655),  # 48-bit value
                bits_gpaddr=random.randint(0, 18446744073709551615),  # 64-bit value
                bits_isForVSnonLeafPTE=random.choice([True, False]),
                bits_mask=random.randint(0, 65535),  # 16-bit value
                bits_nc=random.choice([True, False]),
                bits_mmio=random.choice([True, False]),
                bits_memBackTypeMM=random.choice([True, False]),
                bits_isvec=random.choice([True, False]),
                bits_is128bit=random.choice([True, False]),
                bits_vecActive=random.choice([True, False]),
                bits_schedIndex=random.randint(0, 127),  # 7-bit value
                bits_rep_info_cause_0=random.choice([True, False]),
                bits_rep_info_cause_1=random.choice([True, False]),
                bits_rep_info_cause_2=random.choice([True, False]),
                bits_rep_info_cause_3=random.choice([True, False]),
                bits_rep_info_cause_4=random.choice([True, False]),
                bits_rep_info_cause_5=random.choice([True, False]),
                bits_rep_info_cause_6=random.choice([True, False]),
                bits_rep_info_cause_7=random.choice([True, False]),
                bits_rep_info_cause_8=random.choice([True, False]),
                bits_rep_info_cause_9=random.choice([True, False]),
                bits_rep_info_cause_10=random.choice([True, False])
            ) for i in range(3)
        ]
        uncache_instance = Uncache(
            resp_valid=random.choice([True, False]),
            resp_bits_data=random.randint(0, 18446744073709551615),  # 64-bit value
            resp_bits_id=random.randint(0, 127),  # 7-bit value
            resp_bits_nderr=random.choice([True, False])
        )
        async with Executor() as exec:
                exec(loadqueue_uncache_env.agent.update(req_io, rob_io, ior_redirect))
                exec(loadqueue_uncache_env.agent.uncache(uncache_instance))

@toffee_test.fixture
async def loadqueue_uncache_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTLoadQueueUncache, "clock")
    toffee.start_clock(dut)
    loadqueue_uncache_env = LoadQueueUncacheEnv(dut)
    toffee_request.add_cov_groups(init_uncache_funcov(loadqueue_uncache_env))
    
    yield loadqueue_uncache_env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break