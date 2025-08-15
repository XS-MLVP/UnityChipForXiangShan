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
async def test_ctl_update(loadqueue_replay_env: LoadQueueReplayEnv):
    await loadqueue_replay_env.agent.reset()
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=213,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 1
    
    await loadqueue_replay_env.agent.reset()
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, True, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, True, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 1
    
    await loadqueue_replay_env.agent.reset()
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, True, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, True, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 2
    
    loadqueue_replay_env.agent.bundle.io._redirect._valid.value = True
    loadqueue_replay_env.agent.bundle.io._redirect._bits._robIdx._value.value = 7
    await loadqueue_replay_env.agent.bundle.step(2)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_replay_env.agent.bundle.LoadQueueReplay._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
    await loadqueue_replay_env.agent.reset()
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, True, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=False, exceptionVec=[False, False, True, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, True, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 0
    
@toffee_test.testcase
async def test_ctl_blocking(loadqueue_replay_env: LoadQueueReplayEnv):
    await loadqueue_replay_env.agent.reset()
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, True, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
            rep_info_causes=[False, False, True, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    assert inner._blocking._0.value == 1 and inner._blocking._0.value == 1
    stAddrReadySqPtr = ReadySqPtr(flag=True, value=24)
    sqEmpty = True
    stDataReadyVec = [False for i in range(56)]
    stAddrReadyVec_int = 0x00000000200000
    stAddrReadyVec_str = bin(stAddrReadyVec_int)[2:]
    padding_length = 56 - len(stAddrReadyVec_str)
    stAddrReadyVec = [0] * padding_length + [int(bit) for bit in stAddrReadyVec_str]
    stDataReadySqPtr = ReadySqPtr()
    store_addr_in_instance = [StoreAddrIn(), StoreAddrIn()]
    store_data_in_instance = [StoreDataIn(), StoreDataIn()]   
    tl_channel_instance = TLChannel() 
    rarFull = True
    rawFull = True
    ioldwbptr_instance = IOldWbPtr()
    tlb_hint_instance = TlbHint()
    inner = await loadqueue_replay_env.agent.Update_blocking(stDataReadySqPtr, stAddrReadySqPtr, sqEmpty, store_addr_in_instance,
                                                                store_data_in_instance, stAddrReadyVec, stDataReadyVec, tlb_hint_instance,
                                                                tl_channel_instance, rarFull, ioldwbptr_instance, rawFull)
    assert inner._scheduled._0.value == 1 and inner._blocking._0.value == 0 and inner._blocking._1.value == 0 and inner._blocking._2.value == 0
    
    redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, True, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
            rep_info_causes=[False, False, True, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    stAddrReadySqPtr = ReadySqPtr(flag=True, value=24)
    sqEmpty = False
    stAddrReadyVec = [False for i in range(56)]
    stDataReadyVec_int = 0x000000000000F0
    stDataReadyVec_str = bin(stDataReadyVec_int)[2:]
    padding_length = 56 - len(stDataReadyVec_str)
    stDataReadyVec = [0] * padding_length + [int(bit) for bit in stDataReadyVec_str]
    stDataReadySqPtr = ReadySqPtr(flag=True, value=23)
    store_addr_in_instance = [StoreAddrIn(), StoreAddrIn()]
    store_data_in_instance = [StoreDataIn(), StoreDataIn()]   
    tl_channel_instance = TLChannel() 
    rarFull = True
    rawFull = True
    ioldwbptr_instance = IOldWbPtr()
    tlb_hint_instance = TlbHint()
    async with Executor() as exec:
        exec(loadqueue_replay_env.agent.Update_queue(enq, redirect))
        exec(loadqueue_replay_env.agent.Update_blocking(stDataReadySqPtr, stAddrReadySqPtr, sqEmpty, store_addr_in_instance,
                                                        store_data_in_instance, stAddrReadyVec, stDataReadyVec, tlb_hint_instance,
                                                        tl_channel_instance, rarFull, ioldwbptr_instance, rawFull))
    assert inner._blocking._2.value == 1
    
@toffee_test.testcase    
async def test_diff_channel(loadqueue_replay_env: LoadQueueReplayEnv):
    await loadqueue_replay_env.agent.reset()
    for i in range(72):
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        enq = [IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i, uopIdx=i, robIdx_flag=True, robIdx_value=i,
                loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=i, sqIdx_flag=True, sqIdx_value=i, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i, rep_info_mshr_id=i,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, True, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+1, uopIdx=i+1, robIdx_flag=True, robIdx_value=i+1,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+1, sqIdx_flag=True, sqIdx_value=i+1, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=i+1, rep_info_mshr_id=i+1,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+1, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+1, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+2, uopIdx=i+2, robIdx_flag=True, robIdx_value=i+2,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+2, sqIdx_flag=True, sqIdx_value=i+2, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i+2, rep_info_mshr_id=i+2,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+2, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+2, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, True, False, False, True],
                rep_info_tlb_id=6, rep_info_tlb_full=True)
        ]
        await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_replay_env.agent.bundle.LoadQueueReplay._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72  
    
    await loadqueue_replay_env.agent.reset()
    for i in range(72):
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        enq = [IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i, uopIdx=i, robIdx_flag=True, robIdx_value=i,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i, sqIdx_flag=True, sqIdx_value=i, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=i, rep_info_mshr_id=i,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, True, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+1, uopIdx=i+1, robIdx_flag=True, robIdx_value=i+1,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+1, sqIdx_flag=True, sqIdx_value=i+1, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i+1, rep_info_mshr_id=i+1,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+1, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+1, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=False, exceptionVec=[False, False, False, True, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+2, uopIdx=i+2, robIdx_flag=True, robIdx_value=i+2,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+2, sqIdx_flag=True, sqIdx_value=i+2, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i+2, rep_info_mshr_id=i+2,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+2, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+2, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, True, False, False, True],
                rep_info_tlb_id=6, rep_info_tlb_full=True)
        ]
        await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_replay_env.agent.bundle.LoadQueueReplay._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72  
    
    await loadqueue_replay_env.agent.reset()
    for i in range(72):
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        enq = [IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i, uopIdx=i, robIdx_flag=True, robIdx_value=i,
                loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=i, sqIdx_flag=True, sqIdx_value=i, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i, rep_info_mshr_id=i,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, True, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=False, exceptionVec=[False, False, True, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+1, uopIdx=i+1, robIdx_flag=True, robIdx_value=i+1,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+1, sqIdx_flag=True, sqIdx_value=i+1, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i+1, rep_info_mshr_id=i+1,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+1, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+1, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, True, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+2, uopIdx=i+2, robIdx_flag=True, robIdx_value=i+2,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+2, sqIdx_flag=True, sqIdx_value=i+2, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=True, handledByMSHR=False, schedIndex=i+2, rep_info_mshr_id=i+2,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+2, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+2, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, True, False, False, True],
                rep_info_tlb_id=6, rep_info_tlb_full=True)
        ]
        await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_replay_env.agent.bundle.LoadQueueReplay._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72  
      
@toffee_test.testcase
async def test_queue_full(loadqueue_replay_env: LoadQueueReplayEnv):
    await loadqueue_replay_env.agent.reset()
    for i in range(24):
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i, uopIdx=i, robIdx_flag=True, robIdx_value=i,
                loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=i, sqIdx_flag=True, sqIdx_value=i, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i, rep_info_mshr_id=i,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, True, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+1, uopIdx=i+1, robIdx_flag=True, robIdx_value=i+1,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+1, sqIdx_flag=True, sqIdx_value=i+1, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i+1, rep_info_mshr_id=i+1,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+1, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+1, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=i+2, uopIdx=i+2, robIdx_flag=True, robIdx_value=i+2,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=i+2, sqIdx_flag=True, sqIdx_value=i+2, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=i+2, rep_info_mshr_id=i+2,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=i+2, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=i+2, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, True, False, False, True],
                rep_info_tlb_id=6, rep_info_tlb_full=True)
        ]
        stAddrReadySqPtr = ReadySqPtr(flag=True, value=24)
        sqEmpty = False
        stAddrReadyVec_int = 0x00000000200000
        stAddrReadyVec_str = bin(stAddrReadyVec_int)[2:]
        padding_length = 56 - len(stAddrReadyVec_str)
        stAddrReadyVec = [0] * padding_length + [int(bit) for bit in stAddrReadyVec_str]
        stDataReadyVec_int = 0x000000000000F0
        stDataReadyVec_str = bin(stDataReadyVec_int)[2:]
        padding_length = 56 - len(stDataReadyVec_str)
        stDataReadyVec = [0] * padding_length + [int(bit) for bit in stDataReadyVec_str]
        stDataReadySqPtr = ReadySqPtr(flag=True, value=23)
        store_addr_in_instance = [StoreAddrIn(), StoreAddrIn()]
        store_data_in_instance = [StoreDataIn(), StoreDataIn()]   
        tl_channel_instance = TLChannel() 
        rarFull = True
        rawFull = True
        ioldwbptr_instance = IOldWbPtr()
        tlb_hint_instance = TlbHint()
        async with Executor() as exec:
            exec(loadqueue_replay_env.agent.Update_queue(enq, redirect))
            exec(loadqueue_replay_env.agent.Update_blocking(stDataReadySqPtr, stAddrReadySqPtr, sqEmpty, store_addr_in_instance,
                                                            store_data_in_instance, stAddrReadyVec, stDataReadyVec, tlb_hint_instance,
                                                            tl_channel_instance, rarFull, ioldwbptr_instance, rawFull))
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_replay_env.agent.bundle.LoadQueueReplay._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 72
    
    await loadqueue_replay_env.agent.reset()
    for i in range(23):
        redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
        enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
                loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, True, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, False, False, False, True, False, False, True],
                rep_info_tlb_id=6, rep_info_tlb_full=True)
        ]
        stAddrReadySqPtr = ReadySqPtr(flag=True, value=24)
        sqEmpty = False
        stAddrReadyVec_int = 0x00000000200000
        stAddrReadyVec_str = bin(stAddrReadyVec_int)[2:]
        padding_length = 56 - len(stAddrReadyVec_str)
        stAddrReadyVec = [0] * padding_length + [int(bit) for bit in stAddrReadyVec_str]
        stDataReadyVec_int = 0x000000000000F0
        stDataReadyVec_str = bin(stDataReadyVec_int)[2:]
        padding_length = 56 - len(stDataReadyVec_str)
        stDataReadyVec = [0] * padding_length + [int(bit) for bit in stDataReadyVec_str]
        stDataReadySqPtr = ReadySqPtr(flag=True, value=23)
        store_addr_in_instance = [StoreAddrIn(), StoreAddrIn()]
        store_data_in_instance = [StoreDataIn(), StoreDataIn()]   
        tl_channel_instance = TLChannel() 
        rarFull = True
        rawFull = True
        ioldwbptr_instance = IOldWbPtr()
        tlb_hint_instance = TlbHint()
        async with Executor() as exec:
            exec(loadqueue_replay_env.agent.Update_queue(enq, redirect))
            exec(loadqueue_replay_env.agent.Update_blocking(stDataReadySqPtr, stAddrReadySqPtr, sqEmpty, store_addr_in_instance,
                                                            store_data_in_instance, stAddrReadyVec, stDataReadyVec, tlb_hint_instance,
                                                            tl_channel_instance, rarFull, ioldwbptr_instance, rawFull))
    allocated = []
    for i in range(72):
        allocated.append(getattr(loadqueue_replay_env.agent.bundle.LoadQueueReplay._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 69
    redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, True, True, True],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, True, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[True, True, True, True, True, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, False, True, False, False, True],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    assert allocate == 71
    redirect = IORedirect(valid=False, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, True, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=False, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, False, False, False, False, False, True, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=7,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, True, False, False, False, False, False, False, True],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    allocated = []
    for i in range(72):
        allocated.append(getattr(inner._allocated, f'_{i}').value)
    allocate = allocated.count(1)
    print("queue_full_info:",loadqueue_replay_env.agent.bundle.LoadQueueReplay_._freeList_io._empty.value)
    assert allocate == 72 and loadqueue_replay_env.agent.bundle.io._lqFull.value == 1
    
@toffee_test.testcase
async def test_ctl_replay(loadqueue_replay_env: LoadQueueReplayEnv):
    await loadqueue_replay_env.agent.reset()
    redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
    enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=79,
            loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=4,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
            rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=113,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=5,
            rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
            rep_info_causes=[False, True, False, False, False, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True),
        IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
            ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=89,
            loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
            vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
            elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
            vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=8,
            rep_info_full_fwd=False, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
            rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
            rep_info_causes=[False, False, False, False, True, False, False, False, False, False, False],
            rep_info_tlb_id=6, rep_info_tlb_full=True)
    ]
    inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
    assert inner._blocking._0.value == 1 and inner._blocking._0.value == 1
    stAddrReadySqPtr = ReadySqPtr(flag=True, value=24)
    sqEmpty = True
    stDataReadyVec = [False for i in range(56)]
    stAddrReadyVec_int = 0x00000000200000
    stAddrReadyVec_str = bin(stAddrReadyVec_int)[2:]
    padding_length = 56 - len(stAddrReadyVec_str)
    stAddrReadyVec = [0] * padding_length + [int(bit) for bit in stAddrReadyVec_str]
    stDataReadySqPtr = ReadySqPtr()
    store_addr_in_instance = [StoreAddrIn(), StoreAddrIn()]
    store_data_in_instance = [StoreDataIn(), StoreDataIn()]   
    tl_channel_instance = TLChannel(valid=True) 
    rarFull = True
    rawFull = True
    ioldwbptr_instance = IOldWbPtr()
    tlb_hint_instance = TlbHint()
    await loadqueue_replay_env.agent.Update_blocking(stDataReadySqPtr, stAddrReadySqPtr, sqEmpty, store_addr_in_instance,
                                                                store_data_in_instance, stAddrReadyVec, stDataReadyVec, tlb_hint_instance,
                                                                tl_channel_instance, rarFull, ioldwbptr_instance, rawFull)
    await loadqueue_replay_env.agent.bundle.step(2)
    assert loadqueue_replay_env.agent.bundle.io._replay._0._valid.value == 1 and loadqueue_replay_env.agent.bundle.io._replay._1._valid.value == 1
    l2_hint = L2Hint(valid=True, sourceId=7, isKeyword=False)
    await loadqueue_replay_env.agent.replay(l2_hint)
    assert loadqueue_replay_env.agent.bundle.io._replay._2._valid.value == 1
    
@toffee_test.testcase
async def test_cold_queue(loadqueue_replay_env:LoadQueueReplayEnv):
    await loadqueue_replay_env.agent.reset()
    for i in range(17):
        redirect = IORedirect(valid=True, robIdx_flag=True, robIdx_value=200, level=0)
        enq = [IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=i*3,
                loadWaitStrict=False, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
                vaddr=715691123815, mask=62347, tlbMiss=True, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=4,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=21, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=22, rep_info_last_beat=True,
                rep_info_causes=[True, False, False, False, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=i*3+1,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=5,
                rep_info_full_fwd=True, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=23, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=24, rep_info_last_beat=True,
                rep_info_causes=[False, True, False, False, False, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True),
            IOEnq(valid=True, exceptionVec=[False, False, False, False, False, False, False, False],
                ftqPtr_flag=True, ftqPtr_value=12, uopIdx=68, robIdx_flag=True, robIdx_value=i*3+2,
                loadWaitStrict=True, lqIdx_flag=True, lqIdx_value=72, sqIdx_flag=True, sqIdx_value=18, 
                vaddr=715691123815, mask=62347, tlbMiss=False, isvec=True, is128bit=True,
                elemIdx=153, alignedType=3, mbIndex=11, reg_offset=13, elemIdxInsideVd=56,
                vecActive=True, isLoadReplay=False, handledByMSHR=False, schedIndex=123, rep_info_mshr_id=8,
                rep_info_full_fwd=False, rep_info_data_inv_sq_idx_flag=True, rep_info_data_inv_sq_idx_value=28, 
                rep_info_addr_inv_sq_idx_flag=True, rep_info_addr_inv_sq_idx_value=29, rep_info_last_beat=True,
                rep_info_causes=[False, False, False, False, True, False, False, False, False, False, False],
                rep_info_tlb_id=6, rep_info_tlb_full=True)
        ]
        loadqueue_replay_env.agent.bundle.io._replay._0._ready.value = True
        loadqueue_replay_env.agent.bundle.io._replay._1._ready.value = True
        loadqueue_replay_env.agent.bundle.io._replay._2._ready.value = True
        inner = await loadqueue_replay_env.agent.Update_queue(enq, redirect)
        print(loadqueue_replay_env.agent.bundle.LoadQueueReplay._coldCounter)
    
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