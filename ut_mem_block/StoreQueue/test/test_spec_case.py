import os
import random
import toffee_test
import toffee
from dut.StoreQueue import DUTStoreQueue
from .checkpoints_store_static import init_store_funcov
from ..util.dataclass import EnqReq, IORedirect, VecFeedback, StoreAddrIn, StoreAddrInRe, StoreDataIn, Forward, IORob, Uncache, MaControlInput, StoreMaskIn
from ..env.StoreQueueEnv import StoreQueueEnv
from toffee import Executor
    
@toffee_test.testcase
async def test_random(storequeue_env: StoreQueueEnv):
    random.seed(os.urandom(128))
    await storequeue_env.agent.reset()
    for _ in range(2000):
        enq_req_instance = [EnqReq(
            valid=random.choice([True, False]),
            fuType=random.randint(0, 3),
            fuOpType=random.randint(0, 3),
            uopIdx=random.randint(0, 15),
            lastUop=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=random.randint(0, 63),
            sqIdx_flag=random.choice([True, False]),
            sqIdx_value=random.randint(0, 63),
            numLsElem=random.randint(0, 7)
        ) for i in range(6)]
        io_redirect_instance = IORedirect(
            valid=random.choice([True, False]),
            robIdx_flag=random.choice([True, False]),
            robIdx_value=random.randint(0, 255),
            level=random.choice([True, False])
        )
        vec_feedback_instance = [VecFeedback(
            valid=random.choice([True, False]),
            robidx_flag=random.choice([True, False]),
            robidx_value=random.randint(0, 255),
            uopidx=random.randint(0, 127),
            vaddr=random.randint(0, 2**64 - 1),
            vaNeedExt=random.choice([True, False]),
            gpaddr=random.randint(0, 2**50 - 1),
            isForVSnonLeafPTE=random.choice([True, False]),
            feedback_0=random.choice([True, False]),
            feedback_1=random.choice([True, False]),
            exceptionVec_3=random.choice([True, False]),
            exceptionVec_6=random.choice([True, False]),
            exceptionVec_7=random.choice([True, False]),
            exceptionVec_15=random.choice([True, False]),
            exceptionVec_23=random.choice([True, False])
        ) for i in range(2)]
        store_addr_in_instance = [StoreAddrIn(
            valid=random.choice([True, False]),
            uop_exceptionVec_3=random.choice([True, False]),
            uop_exceptionVec_6=random.choice([True, False]),
            uop_exceptionVec_7=random.choice([True, False]),
            uop_exceptionVec_15=random.choice([True, False]),
            uop_exceptionVec_23=random.choice([True, False]),
            uop_fuOpType=random.randint(0, 511),
            uop_uopIdx=random.randint(0, 127),
            uop_robIdx_flag=random.choice([True, False]),
            uop_robIdx_value=random.randint(0, 255),
            uop_sqIdx_value=random.randint(0, 63),
            vaddr=random.randint(0, 2**50 - 1),
            fullva=random.randint(0, 2**64 - 1),
            vaNeedExt=random.choice([True, False]),
            isHyper=random.choice([True, False]),
            paddr=random.randint(0, 2**48 - 1),
            gpaddr=random.randint(0, 2**64 - 1),
            isForVSnonLeafPTE=random.choice([True, False]),
            mask=random.randint(0, 65535),
            wlineflag=random.choice([True, False]),
            miss=random.choice([True, False]),
            nc=random.choice([True, False]),
            isFrmMisAlignBuf=random.choice([True, False]),
            isvec=random.choice([True, False]),
            isMisalign=random.choice([True, False]),
            misalignWith16Byte=random.choice([True, False]),
            updateAddrValid=random.choice([True, False])
        ) for i in range(2)]
        store_addr_in_re_instance = [StoreAddrInRe(
            uop_exceptionVec_3=random.choice([True, False]),
            uop_exceptionVec_6=random.choice([True, False]),
            uop_exceptionVec_15=random.choice([True, False]),
            uop_exceptionVec_23=random.choice([True, False]),
            uop_uopIdx=random.randint(0, 127),
            uop_robIdx_flag=random.choice([True, False]),
            uop_robIdx_value=random.randint(0, 255),
            fullva=random.randint(0, 2**64 - 1),
            vaNeedExt=random.choice([True, False]),
            isHyper=random.choice([True, False]),
            gpaddr=random.randint(0, 2**64 - 1),
            isForVSnonLeafPTE=random.choice([True, False]),
            af=random.choice([True, False]),
            mmio=random.choice([True, False]),
            memBackTypeMM=random.choice([True, False]),
            hasException=random.choice([True, False]),
            isvec=random.choice([True, False]),
            updateAddrValid=random.choice([True, False])
        )  for i in range(2)]
        store_data_in_instance = [StoreDataIn(
            valid=random.choice([True, False]),
            bits_uop_fuType=random.randint(0, 2**35 - 1),
            bits_uop_fuOpType=random.randint(0, 511),
            bits_uop_sqIdx_value=random.randint(0, 63),
            bits_data=random.randint(0, 2**128 - 1)
        ) for i in range(2)]
        forward_instance = [Forward(
            vaddr=random.randint(0, 2**50 - 1),
            paddr=random.randint(0, 2**48 - 1),
            mask=random.randint(0, 65535),
            uop_waitForRobIdx_flag=random.choice([True, False]),
            uop_waitForRobIdx_value=random.randint(0, 255),
            uop_loadWaitBit=random.choice([True, False]),
            uop_loadWaitStrict=random.choice([True, False]),
            uop_sqIdx_flag=random.choice([True, False]),
            uop_sqIdx_value=random.randint(0, 63),
            valid=random.choice([True, False]),
            forwardMask=[random.randint(0, 1) for _ in range(16)],
            forwardData=[random.randint(0, 255) for _ in range(16)],
            sqIdx_flag=random.choice([True, False]),
            dataInvalid=random.choice([True, False]),
            matchInvalid=random.choice([True, False]),
            addrInvalid=random.choice([True, False]),
            sqIdxMask=random.randint(0, 2**56 - 1),
            dataInvalidSqIdx_flag=random.choice([True, False]),
            dataInvalidSqIdx_value=random.randint(0, 63),
            addrInvalidSqIdx_flag=random.choice([True, False]),
            addrInvalidSqIdx_value=random.randint(0, 63)
        ) for i in range(2)]
        iorob_instance = IORob(
            rob_scommit=random.randint(0, 15),
            pendingst=random.choice([True, False]),
            pendingPtr_flag=random.choice([True, False]),
            pendingPtr_value=random.randint(0, 255)
        )
        uncache_instance = Uncache(
            req_ready=random.choice([True, False]),
            req_valid=random.choice([True, False]),
            req_bits_addr=random.randint(0, 2**48 - 1),
            req_bits_vaddr=random.randint(0, 2**50 - 1),
            req_bits_data=random.randint(0, 2**64 - 1),
            req_bits_mask=random.randint(0, 255),
            req_bits_id=random.randint(0, 127),
            req_bits_nc=random.choice([True, False]),
            req_bits_memBackTypeMM=random.choice([True, False]),
            resp_valid=random.choice([True, False]),
            resp_bits_id=random.randint(0, 127),
            resp_bits_nc=random.choice([True, False]),
            resp_bits_nderr=random.choice([True, False])
        )
        ma_control_input_instance = MaControlInput(
            crossPageWithHit=random.choice([True, False]),
            crossPageCanDeq=random.choice([True, False]),
            paddr=random.randint(0, 2**48 - 1),
            withSameUop=random.choice([True, False])
        )
        store_mask_in_instance = [StoreMaskIn(
            valid=random.choice([True, False]),
            sqIdx_value=random.randint(0, 63),
            mask=random.randint(0, 255)
        ) for i in range(2)]
        async with Executor() as exec:
                exec(storequeue_env.agent.update(enq_req_instance, io_redirect_instance))
                exec(storequeue_env.agent.writeback(store_addr_in_instance, store_addr_in_re_instance, store_data_in_instance, store_mask_in_instance))
                exec(storequeue_env.agent.forwardquery(forward_instance))
                exec(storequeue_env.agent.mmio(uncache_instance, iorob_instance))
                exec(storequeue_env.agent.ncstore(random.choice([True, False]), uncache_instance, random.choice([True, False])))
                exec(storequeue_env.agent.commit(iorob_instance, ma_control_input_instance, vec_feedback_instance))
                
@toffee_test.fixture
async def storequeue_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTStoreQueue, "clock")
    toffee.start_clock(dut)
    env = StoreQueueEnv(dut)
    toffee_request.add_cov_groups(init_store_funcov(env))
    
    yield env
    
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break