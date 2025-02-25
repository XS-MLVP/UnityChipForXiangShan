import random
import toffee
import toffee_test

from dut.LoadQueueRAR import *
from ..env.LoadQueueRAR import *
import toffee.funcov as fc

# g = fc.CovGroup(UT_FCOV("../../Group-A"))

from comm import TAG_LONG_TIME_RUN, TAG_SMOKE, TAG_RARELY_USED, debug

@pytest.mark.toffee_tags(TAG_SMOKE)
def test_can_enqueue_smoke(rar_queue):
    """
     Test the RVI instruction set. randomly generate instructions for testing

     Args:
         rar_queue(fixure): the fixture of the LoadQueueRAR
    """
    # print(rar_queue.req)
    query = random.getrandbits(234)
    bits_to_set = [1, 79, 157]
    # 创建一个掩码
    mask = 0
    for bit in bits_to_set:
        mask |= (1 << bit)  # 使用 | 运算符设置位
    query |= mask
    redirect = random.getrandbits(11)
    ldWbPtr = random.getrandbits(8)
    res, inner = rar_queue.Enqueue(query, redirect, ldWbPtr)
    allocated = []
    for i in range(72):
        signal_name = f"allocated_{i}"  # 构造信号名称
        allocated.append(inner[signal_name].value)
    allocate = any(allocated)
    print(allocate)
    assert (res["ready"].value == 1 and allocate == 1)
    
@pytest.mark.toffee_tags(TAG_SMOKE)
def test_can_dequeue_smoke(rar_queue):
    """
     Test the RVI instruction set. randomly generate instructions for testing

     Args:
         rar_queue(fixure): the fixture of the LoadQueueRAR
    """
    # 确保已经有一些项入队
    query = random.getrandbits(234)
    bits_to_set = [1, 79, 157]
    mask = 0
    for bit in bits_to_set:
        mask |= (1 << bit)  # 使用 | 运算符设置位
    query |= mask
    redirect_1 = random.getrandbits(11)
    ldWbPtr_1 = random.getrandbits(8)
    _, inner = rar_queue.Enqueue(query, redirect_1, ldWbPtr_1)
    # allocated = []
    count = 0
    for i in range(72):
        signal_name = f"allocated_{i}"  # 构造信号名称
        # allocated.append(inner[signal_name].value)
        if inner[signal_name].value == 1:
            count = count + 1
    ldWbPtr = random.getrandbits(8)
    redirect = random.getrandbits(11)
    vecFeedback = random.getrandbits(36)
    release = random.getrandbits(48)
    while ldWbPtr and redirect and vecFeedback and release == 0:
        temp = random.getrandbits(8)
        ldWbPtr = ldWbPtr + temp
        temp = random.getrandbits(11)
        redirect = redirect + temp
        temp = random.getrandbits(36)
        vecFeedback = vecFeedback + temp
        temp = random.getrandbits(48)
        release = release + temp
    inner = rar_queue.Dequeue(ldWbPtr, redirect, vecFeedback, release)
    count_after = 0
    for i in range(72):
        signal_name = f"allocated_{i}"  # 构造信号名称
        # allocated.append(inner[signal_name].value)
        if inner[signal_name].value == 1:
            count_after = count_after + 1
    # rar_queue.cover_group.add_watch_point(rar_queue., 
    #                   {
    #                     "can dequeue successfully": lambda x: x.value > 0,
    #                   }, name = "RAR_DEQUEUE", dynamic_bin=True)
    # rar_queue.cover_group.mark_function("RAR_DEQUEUE", test_can_dequeue_smoke, bin_name=["can dequeue successfully"])
    assert (count_after < count)

