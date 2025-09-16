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
async def test_ctl_update(storequeue_env: StoreQueueEnv):
    await storequeue_env.agent.reset()
    enq_req = [
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=3, lastUop=True,
            robIdx_flag=True, robIdx_value=2, sqIdx_flag=True, sqIdx_value=0, numLsElem=4),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=7, lastUop=True,
            robIdx_flag=True, robIdx_value=7, sqIdx_flag=True, sqIdx_value=4, numLsElem=1),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=9, lastUop=True,
            robIdx_flag=True, robIdx_value=9, sqIdx_flag=True, sqIdx_value=5, numLsElem=2),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=17, lastUop=True,
            robIdx_flag=True, robIdx_value=13, sqIdx_flag=True, sqIdx_value=7, numLsElem=5),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=16, lastUop=True,
            robIdx_flag=True, robIdx_value=16, sqIdx_flag=True, sqIdx_value=12, numLsElem=3),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=25, lastUop=True,
            robIdx_flag=True, robIdx_value=23, sqIdx_flag=True, sqIdx_value=15, numLsElem=2)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=137, level=True)
    inner = await storequeue_env.agent.update(enq_req, redirect)
    allocated = []
    for i in range(56):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 15
    
@toffee_test.testcase
async def test_queue_full(storequeue_env:StoreQueueEnv):
    await storequeue_env.agent.reset()
    for i in range(4):
        enq_req = [
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=3, lastUop=True,
                robIdx_flag=True, robIdx_value=2, sqIdx_flag=True, sqIdx_value=0+i*14, numLsElem=4),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=7, lastUop=True,
                robIdx_flag=True, robIdx_value=7, sqIdx_flag=True, sqIdx_value=4+i*14, numLsElem=1),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=9, lastUop=True,
                robIdx_flag=True, robIdx_value=9, sqIdx_flag=True, sqIdx_value=5+i*14, numLsElem=2),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=17, lastUop=True,
                robIdx_flag=True, robIdx_value=13, sqIdx_flag=True, sqIdx_value=7+i*14, numLsElem=5),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=16, lastUop=True,
                robIdx_flag=True, robIdx_value=16, sqIdx_flag=True, sqIdx_value=12+i*14, numLsElem=2),
            EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=25, lastUop=True,
                robIdx_flag=True, robIdx_value=23, sqIdx_flag=True, sqIdx_value=15+i*14, numLsElem=2)
        ]
        redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=137, level=True)
        await storequeue_env.agent.update(enq_req, redirect)
    allocated = []
    for i in range(56):
        allocated.append(getattr(storequeue_env.agent.bundle.StoreQueue._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 56 and storequeue_env.agent.bundle.io._sqEmpty.value == 0
    
    storequeue_env.agent.bundle.io._brqRedirect._valid.value = True
    storequeue_env.agent.bundle.io._brqRedirect._bits._robIdx._value.value = 3
    await storequeue_env.agent.bundle.step(2)
    allocated = []
    for i in range(56):
        allocated.append(getattr(storequeue_env.agent.bundle.StoreQueue._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 16    
    
@toffee_test.testcase
async def test_enqueue_boundary(storequeue_env:StoreQueueEnv):
    await storequeue_env.agent.reset()
    for i in range(5):
        enq_req = [
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=3, lastUop=True,
                robIdx_flag=True, robIdx_value=2, sqIdx_flag=True, sqIdx_value=0+i*11, numLsElem=4),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=7, lastUop=True,
                robIdx_flag=True, robIdx_value=7, sqIdx_flag=True, sqIdx_value=4+i*11, numLsElem=1),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=9, lastUop=True,
                robIdx_flag=True, robIdx_value=9, sqIdx_flag=True, sqIdx_value=5+i*11, numLsElem=2),
            EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=17, lastUop=True,
                robIdx_flag=True, robIdx_value=13, sqIdx_flag=True, sqIdx_value=7+i*11, numLsElem=4),
            EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=16, lastUop=True,
                robIdx_flag=True, robIdx_value=16, sqIdx_flag=True, sqIdx_value=12+i*11, numLsElem=2),
            EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=25, lastUop=True,
                robIdx_flag=True, robIdx_value=23, sqIdx_flag=True, sqIdx_value=15+i*11, numLsElem=2)
        ]
        redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=137, level=True)
        await storequeue_env.agent.update(enq_req, redirect)
    enq_req = [
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=3, lastUop=True,
            robIdx_flag=True, robIdx_value=2, sqIdx_flag=True, sqIdx_value=55, numLsElem=4),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=7, lastUop=True,
            robIdx_flag=True, robIdx_value=7, sqIdx_flag=True, sqIdx_value=4+i*11, numLsElem=1),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=9, lastUop=True,
            robIdx_flag=True, robIdx_value=9, sqIdx_flag=True, sqIdx_value=5+i*11, numLsElem=2),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=17, lastUop=True,
            robIdx_flag=True, robIdx_value=13, sqIdx_flag=True, sqIdx_value=7+i*11, numLsElem=4),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=16, lastUop=True,
            robIdx_flag=True, robIdx_value=16, sqIdx_flag=True, sqIdx_value=12+i*11, numLsElem=2),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=25, lastUop=True,
            robIdx_flag=True, robIdx_value=23, sqIdx_flag=True, sqIdx_value=15+i*11, numLsElem=2)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=137, level=True)
    await storequeue_env.agent.update(enq_req, redirect)
    allocated = []
    for i in range(56):
        allocated.append(getattr(storequeue_env.agent.bundle.StoreQueue._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 56 and storequeue_env.agent.bundle.io._sqEmpty.value == 0
    
@toffee_test.testcase
async def test_ctl_forward(storequeue_env:StoreQueueEnv):
    await storequeue_env.agent.reset()
    enq_req = [
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=3, lastUop=True,
            robIdx_flag=True, robIdx_value=2, sqIdx_flag=True, sqIdx_value=0, numLsElem=4),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=7, lastUop=True,
            robIdx_flag=True, robIdx_value=7, sqIdx_flag=True, sqIdx_value=4, numLsElem=1),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=9, lastUop=True,
            robIdx_flag=True, robIdx_value=9, sqIdx_flag=True, sqIdx_value=5, numLsElem=2),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=17, lastUop=True,
            robIdx_flag=True, robIdx_value=13, sqIdx_flag=True, sqIdx_value=7, numLsElem=5),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=16, lastUop=True,
            robIdx_flag=True, robIdx_value=16, sqIdx_flag=True, sqIdx_value=12, numLsElem=3),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=25, lastUop=True,
            robIdx_flag=True, robIdx_value=23, sqIdx_flag=True, sqIdx_value=15, numLsElem=2)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=137, level=True)
    inner = await storequeue_env.agent.update(enq_req, redirect)
    
    store_addr_in = [
        StoreAddrIn(valid=True, uop_exceptionVec_3=False, uop_exceptionVec_6=False,
            uop_exceptionVec_7=False, uop_exceptionVec_15=False, uop_exceptionVec_23=False, uop_fuOpType=2, uop_uopIdx=37, 
            uop_robIdx_flag=True, uop_robIdx_value=27, uop_sqIdx_value=0, vaddr=5842633485, fullva=17652359845,
            vaNeedExt=True, isHyper=True, paddr=15263498, gpaddr=715638945, isForVSnonLeafPTE=True, mask=23345, 
            wlineflag=True, miss=True, nc=True, isFrmMisAlignBuf=True, isvec=True, isMisalign= True,
            misalignWith16Byte=True, updateAddrValid=True),
        StoreAddrIn(valid=True, uop_exceptionVec_3=False, uop_exceptionVec_6=False,
            uop_exceptionVec_7=False, uop_exceptionVec_15=True, uop_exceptionVec_23=False, uop_fuOpType=2, uop_uopIdx=37, 
            uop_robIdx_flag=True, uop_robIdx_value=27, uop_sqIdx_value=0, vaddr=5842633485, fullva=17652359845,
            vaNeedExt=True, isHyper=True, paddr=15263498, gpaddr=715638945, isForVSnonLeafPTE=True, mask=23345, 
            wlineflag=True, miss=False, nc=True, isFrmMisAlignBuf=True, isvec=True, isMisalign= True,
            misalignWith16Byte=True, updateAddrValid=True)
    ]
    store_data_in = [
        StoreDataIn(valid=True, bits_uop_fuType=0x080000000, bits_uop_fuOpType=2, bits_uop_sqIdx_value=0, bits_data=14578693243),
        StoreDataIn(valid=True, bits_uop_fuType=0x200000000, bits_uop_fuOpType=2, bits_uop_sqIdx_value=0, bits_data=14578693243)
    ]
    store_addr_in_re = [
        StoreAddrInRe(uop_exceptionVec_3=False, uop_exceptionVec_6=False, uop_exceptionVec_15=False,
            uop_exceptionVec_23=False, uop_uopIdx=24, uop_robIdx_flag=True, uop_robIdx_value=233, fullva=14758,
            vaNeedExt=True, isHyper=True, gpaddr=71563284596, isForVSnonLeafPTE=True, af=True, mmio=False,
            memBackTypeMM=True, hasException=True, isvec=True, updateAddrValid=True),
        StoreAddrInRe(uop_exceptionVec_3=False, uop_exceptionVec_6=False, uop_exceptionVec_15=False,
            uop_exceptionVec_23=False, uop_uopIdx=24, uop_robIdx_flag=True, uop_robIdx_value=233, fullva=14758,
            vaNeedExt=True, isHyper=True, gpaddr=71563284596, isForVSnonLeafPTE=True, af=True, mmio=False,
            memBackTypeMM=True, hasException=True, isvec=True, updateAddrValid=True)
    ]
    store_mask_in = [
        StoreMaskIn(valid=True, sqIdx_value=60, mask=211),
        StoreMaskIn(valid=True, sqIdx_value=60, mask=211)
    ]
    forward = [
        Forward(vaddr=5248925627, paddr=1586048842, mask=25463, uop_waitForRobIdx_flag=True,
            uop_waitForRobIdx_value=12, uop_loadWaitBit=True, uop_loadWaitStrict=True, uop_sqIdx_flag=True,
            uop_sqIdx_value=21, valid=True, forwardMask=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            forwardData=[1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0], sqIdx_flag=True, dataInvalid=True,
            matchInvalid=True, addrInvalid=True, sqIdxMask=0x0000000000000001, dataInvalidSqIdx_flag=True,
            dataInvalidSqIdx_value=27, addrInvalidSqIdx_flag=True, addrInvalidSqIdx_value=23),
        Forward(vaddr=5248925627, paddr=1586048842, mask=25463, uop_waitForRobIdx_flag=True,
            uop_waitForRobIdx_value=12, uop_loadWaitBit=True, uop_loadWaitStrict=True, uop_sqIdx_flag=True,
            uop_sqIdx_value=21, valid=True, forwardMask=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            forwardData=[127,136,0,0,0,0,0,0,127,136,0,0,0,0,0,0], sqIdx_flag=True, dataInvalid=True,
            matchInvalid=True, addrInvalid=True, sqIdxMask=1452638954, dataInvalidSqIdx_flag=True,
            dataInvalidSqIdx_value=27, addrInvalidSqIdx_flag=True, addrInvalidSqIdx_value=23)
    ]
    async with Executor() as exec:
            exec(storequeue_env.agent.forwardquery(forward))
            exec(storequeue_env.agent.writeback(store_addr_in, store_addr_in_re, store_data_in, store_mask_in))
    assert storequeue_env.agent.bundle.StoreQueue._forwardMask2.value == 0x0000000000000001
    
@toffee_test.testcase
async def test_mmio(storequeue_env:StoreQueueEnv):
    await storequeue_env.agent.reset()
    enq_req = [
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=24, lastUop=True,
            robIdx_flag=True, robIdx_value=1, sqIdx_flag=True, sqIdx_value=0, numLsElem=4),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=7, lastUop=True,
            robIdx_flag=True, robIdx_value=7, sqIdx_flag=True, sqIdx_value=4, numLsElem=1),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=9, lastUop=True,
            robIdx_flag=True, robIdx_value=9, sqIdx_flag=True, sqIdx_value=5, numLsElem=2),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=17, lastUop=True,
            robIdx_flag=True, robIdx_value=13, sqIdx_flag=True, sqIdx_value=7, numLsElem=5),
        EnqReq(valid=True, fuType=2, fuOpType=1, uopIdx=16, lastUop=True,
            robIdx_flag=True, robIdx_value=16, sqIdx_flag=True, sqIdx_value=12, numLsElem=3),
        EnqReq(valid=False, fuType=2, fuOpType=1, uopIdx=25, lastUop=True,
            robIdx_flag=True, robIdx_value=23, sqIdx_flag=True, sqIdx_value=15, numLsElem=2)
    ]
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=137, level=True)
    store_addr_in = [
        StoreAddrIn(valid=True, uop_exceptionVec_3=False, uop_exceptionVec_6=False,
            uop_exceptionVec_7=False, uop_exceptionVec_15=False, uop_exceptionVec_23=False, uop_fuOpType=2, uop_uopIdx=24, 
            uop_robIdx_flag=True, uop_robIdx_value=1, uop_sqIdx_value=0, vaddr=5842633485, fullva=17652359845,
            vaNeedExt=True, isHyper=True, paddr=15263498, gpaddr=715638945, isForVSnonLeafPTE=True, mask=23345, 
            wlineflag=True, miss=False, nc=False, isFrmMisAlignBuf=True, isvec=True, isMisalign= True,
            misalignWith16Byte=True, updateAddrValid=True),
        StoreAddrIn(valid=True, uop_exceptionVec_3=False, uop_exceptionVec_6=False,
            uop_exceptionVec_7=False, uop_exceptionVec_15=True, uop_exceptionVec_23=False, uop_fuOpType=2, uop_uopIdx=24, 
            uop_robIdx_flag=True, uop_robIdx_value=1, uop_sqIdx_value=0, vaddr=5842633485, fullva=17652359845,
            vaNeedExt=True, isHyper=True, paddr=15263498, gpaddr=715638945, isForVSnonLeafPTE=True, mask=23345, 
            wlineflag=True, miss=False, nc=False, isFrmMisAlignBuf=True, isvec=True, isMisalign= True,
            misalignWith16Byte=True, updateAddrValid=True)
    ]
    store_addr_in_re = [
        StoreAddrInRe(uop_exceptionVec_3=False, uop_exceptionVec_6=False, uop_exceptionVec_15=False,
            uop_exceptionVec_23=False, uop_uopIdx=24, uop_robIdx_flag=True, uop_robIdx_value=1, fullva=14758,
            vaNeedExt=True, isHyper=True, gpaddr=71563284596, isForVSnonLeafPTE=True, af=True, mmio=True,
            memBackTypeMM=True, hasException=False, isvec=True, updateAddrValid=True),
        StoreAddrInRe(uop_exceptionVec_3=False, uop_exceptionVec_6=False, uop_exceptionVec_15=False,
            uop_exceptionVec_23=False, uop_uopIdx=24, uop_robIdx_flag=True, uop_robIdx_value=13, fullva=14758,
            vaNeedExt=True, isHyper=True, gpaddr=71563284596, isForVSnonLeafPTE=True, af=True, mmio=True,
            memBackTypeMM=True, hasException=False, isvec=True, updateAddrValid=True)
    ]
    store_data_in = [
        StoreDataIn(valid=True, bits_uop_fuType=0x080000001, bits_uop_fuOpType=2, bits_uop_sqIdx_value=0, bits_data=14578693243),
        StoreDataIn(valid=True, bits_uop_fuType=0x200000001, bits_uop_fuOpType=2, bits_uop_sqIdx_value=0, bits_data=14578693243)
    ]
    uncache = Uncache(req_ready=True, resp_valid=True, resp_bits_nc=False, resp_bits_nderr=False)
    rob = IORob(rob_scommit=7, pendingst=True, pendingPtr_flag=True, pendingPtr_value=1)
    store_mask_in = [
        StoreMaskIn(valid=True, sqIdx_value=60, mask=211),
        StoreMaskIn(valid=True, sqIdx_value=60, mask=211)
    ]
    async with Executor() as exec:
            exec(storequeue_env.agent.update(enq_req, redirect))
            exec(storequeue_env.agent.mmio(uncache, rob))
            exec(storequeue_env.agent.writeback(store_addr_in, store_addr_in_re, store_data_in, store_mask_in))
    assert storequeue_env.agent.bundle.StoreQueue._commitVec._0.value == 1
    await storequeue_env.agent.bundle.step(2)
    state = storequeue_env.agent.bundle.StoreQueue._mmioState.value
    assert state==1
    
@toffee_test.testcase
async def test_random(storequeue_env: StoreQueueEnv):
    random.seed(os.urandom(128))
    await storequeue_env.agent.reset()
    for _ in range(2000):
        enq_req_instance = [EnqReq(
            valid=not random.getrandbits(1),
            fuType=random.randint(0, 3),
            fuOpType=random.randint(0, 3),
            uopIdx=random.randint(0, 15),
            lastUop=not random.getrandbits(1),
            robIdx_flag=not random.getrandbits(1),
            robIdx_value=random.randint(0, 63),
            sqIdx_flag=not random.getrandbits(1),
            sqIdx_value=random.randint(0, 63),
            numLsElem=random.randint(0, 7)
        ) for i in range(6)]
        io_redirect_instance = IORedirect(
            valid=not random.getrandbits(1),
            robIdx_flag=not random.getrandbits(1),
            robIdx_value=random.randint(0, 255),
            level=not random.getrandbits(1)
        )
        vec_feedback_instance = [VecFeedback(
            valid=not random.getrandbits(1),
            robidx_flag=not random.getrandbits(1),
            robidx_value=random.randint(0, 255),
            uopidx=random.randint(0, 127),
            vaddr=random.randint(0, 2**64 - 1),
            vaNeedExt=not random.getrandbits(1),
            gpaddr=random.randint(0, 2**50 - 1),
            isForVSnonLeafPTE=not random.getrandbits(1),
            feedback_0=not random.getrandbits(1),
            feedback_1=not random.getrandbits(1),
            exceptionVec_3=not random.getrandbits(1),
            exceptionVec_6=not random.getrandbits(1),
            exceptionVec_7=not random.getrandbits(1),
            exceptionVec_15=not random.getrandbits(1),
            exceptionVec_23=not random.getrandbits(1)
        ) for i in range(2)]
        store_addr_in_instance = [StoreAddrIn(
            valid=not random.getrandbits(1),
            uop_exceptionVec_3=not random.getrandbits(1),
            uop_exceptionVec_6=not random.getrandbits(1),
            uop_exceptionVec_7=not random.getrandbits(1),
            uop_exceptionVec_15=not random.getrandbits(1),
            uop_exceptionVec_23=not random.getrandbits(1),
            uop_fuOpType=random.randint(0, 511),
            uop_uopIdx=random.randint(0, 127),
            uop_robIdx_flag=not random.getrandbits(1),
            uop_robIdx_value=random.randint(0, 255),
            uop_sqIdx_value=random.randint(0, 63),
            vaddr=random.randint(0, 2**50 - 1),
            fullva=random.randint(0, 2**64 - 1),
            vaNeedExt=not random.getrandbits(1),
            isHyper=not random.getrandbits(1),
            paddr=random.randint(0, 2**48 - 1),
            gpaddr=random.randint(0, 2**64 - 1),
            isForVSnonLeafPTE=not random.getrandbits(1),
            mask=random.randint(0, 65535),
            wlineflag=not random.getrandbits(1),
            miss=not random.getrandbits(1),
            nc=not random.getrandbits(1),
            isFrmMisAlignBuf=not random.getrandbits(1),
            isvec=not random.getrandbits(1),
            isMisalign=not random.getrandbits(1),
            misalignWith16Byte=not random.getrandbits(1),
            updateAddrValid=not random.getrandbits(1)
        ) for i in range(2)]
        store_addr_in_re_instance = [StoreAddrInRe(
            uop_exceptionVec_3=not random.getrandbits(1),
            uop_exceptionVec_6=not random.getrandbits(1),
            uop_exceptionVec_15=not random.getrandbits(1),
            uop_exceptionVec_23=not random.getrandbits(1),
            uop_uopIdx=random.randint(0, 127),
            uop_robIdx_flag=not random.getrandbits(1),
            uop_robIdx_value=random.randint(0, 255),
            fullva=random.randint(0, 2**64 - 1),
            vaNeedExt=not random.getrandbits(1),
            isHyper=not random.getrandbits(1),
            gpaddr=random.randint(0, 2**64 - 1),
            isForVSnonLeafPTE=not random.getrandbits(1),
            af=not random.getrandbits(1),
            mmio=not random.getrandbits(1),
            memBackTypeMM=not random.getrandbits(1),
            hasException=not random.getrandbits(1),
            isvec=not random.getrandbits(1),
            updateAddrValid=not random.getrandbits(1)
        )  for i in range(2)]
        store_data_in_instance = [StoreDataIn(
            valid=not random.getrandbits(1),
            bits_uop_fuType=random.randint(0, 2**35 - 1),
            bits_uop_fuOpType=random.randint(0, 511),
            bits_uop_sqIdx_value=random.randint(0, 63),
            bits_data=random.randint(0, 2**128 - 1)
        ) for i in range(2)]
        forward_instance = [Forward(
            vaddr=random.randint(0, 2**50 - 1),
            paddr=random.randint(0, 2**48 - 1),
            mask=random.randint(0, 65535),
            uop_waitForRobIdx_flag=not random.getrandbits(1),
            uop_waitForRobIdx_value=random.randint(0, 255),
            uop_loadWaitBit=not random.getrandbits(1),
            uop_loadWaitStrict=not random.getrandbits(1),
            uop_sqIdx_flag=not random.getrandbits(1),
            uop_sqIdx_value=random.randint(0, 63),
            valid=not random.getrandbits(1),
            forwardMask=[random.randint(0, 1) for _ in range(16)],
            forwardData=[random.randint(0, 255) for _ in range(16)],
            sqIdx_flag=not random.getrandbits(1),
            dataInvalid=not random.getrandbits(1),
            matchInvalid=not random.getrandbits(1),
            addrInvalid=not random.getrandbits(1),
            sqIdxMask=random.randint(0, 2**56 - 1),
            dataInvalidSqIdx_flag=not random.getrandbits(1),
            dataInvalidSqIdx_value=random.randint(0, 63),
            addrInvalidSqIdx_flag=not random.getrandbits(1),
            addrInvalidSqIdx_value=random.randint(0, 63)
        ) for i in range(2)]
        iorob_instance = IORob(
            rob_scommit=random.randint(0, 15),
            pendingst=not random.getrandbits(1),
            pendingPtr_flag=not random.getrandbits(1),
            pendingPtr_value=random.randint(0, 255)
        )
        uncache_instance = Uncache(
            req_ready=not random.getrandbits(1),
            req_valid=not random.getrandbits(1),
            req_bits_addr=random.randint(0, 2**48 - 1),
            req_bits_vaddr=random.randint(0, 2**50 - 1),
            req_bits_data=random.randint(0, 2**64 - 1),
            req_bits_mask=random.randint(0, 255),
            req_bits_id=random.randint(0, 127),
            req_bits_nc=not random.getrandbits(1),
            req_bits_memBackTypeMM=not random.getrandbits(1),
            resp_valid=not random.getrandbits(1),
            resp_bits_id=random.randint(0, 127),
            resp_bits_nc=not random.getrandbits(1),
            resp_bits_nderr=not random.getrandbits(1)
        )
        ma_control_input_instance = MaControlInput(
            crossPageWithHit=not random.getrandbits(1),
            crossPageCanDeq=not random.getrandbits(1),
            paddr=random.randint(0, 2**48 - 1),
            withSameUop=not random.getrandbits(1)
        )
        store_mask_in_instance = [StoreMaskIn(
            valid=not random.getrandbits(1),
            sqIdx_value=random.randint(0, 63),
            mask=random.randint(0, 255)
        ) for i in range(2)]
        async with Executor() as exec:
                exec(storequeue_env.agent.update(enq_req_instance, io_redirect_instance))
                exec(storequeue_env.agent.writeback(store_addr_in_instance, store_addr_in_re_instance, store_data_in_instance, store_mask_in_instance))
                exec(storequeue_env.agent.forwardquery(forward_instance))
                exec(storequeue_env.agent.mmio(uncache_instance, iorob_instance))
                exec(storequeue_env.agent.ncstore(not random.getrandbits(1), uncache_instance, not random.getrandbits(1)))
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