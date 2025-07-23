import toffee_test
from dut.TLB import DUTTLB
from .itlb_dut import itlb_env
from ..agent.itlb_trans import *
from ..env.itlb_sqr import *
from toffee import *
import os
TEST_CYCLE = int(os.getenv("TEST_CYCLE", 100))

#@toffee_test.testcase
#async def test_reset(itlb_env):
#    print("Test reset")
#    sqr = ItlbSqr()
#    res = await itlb_env.itlbAgent.agent_itlb(*sqr.gen_vec(0))
#    del sqr
    
    
@toffee_test.testcase
async def test_tlb_acpt_rqst(itlb_env):
    print("Test TLB accepted request")
    res = []
    sqr = ItlbSqr(TEST_CYCLE)
    res= await itlb_env.itlbAgent.agent_itlb(TEST_CYCLE, *(sqr.gen_vec("caseAcptRqst")))
    del sqr