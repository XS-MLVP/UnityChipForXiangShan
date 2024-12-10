import random
import toffee
import toffee_test

from dut.LoadQueueRAR import *
from ..env.LoadQueueRAR import *

from comm import TAG_LONG_TIME_RUN, TAG_SMOKE, TAG_RARELY_USED, debug

@pytest.mark.toffee_tags(TAG_SMOKE)
def test_update_queue_smoke(rar_queue):
    """
     Test the RVI instruction set. randomly generate instructions for testing

     Args:
         rar_queue(fixure): the fixture of the LoadQueueRAR
     """
    # print(rar_queue.req)
    query = random.getrandbits(234)
    redirect = random.getrandbits(11)
    ldWbPtr = random.getrandbits(8)
    res=rar_queue.Enqueue(query,redirect,ldWbPtr)
    print("inner:",res,"\n")
    assert res["ready"].value == 1