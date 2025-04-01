import toffee_test
from dut.TLB import DUTTLB
from .itlb_dut import itlb_env
from ..agent.itlb_trans import *
#from ..env.itlb_sqr import itlb_sqr
from toffee import *
import os
TEST_CYCLE = int(os.getenv("TEST_CYCLE", 100))

@toffee_test.testcase
async def test_reset(itlb_env):
    print("Test reset")
    trSfence = ItlbTransSfence()
    trCsr = ItlbTransCsr()
    trRqstReq = ItlbTransRqstReq()
    trRqstResp = ItlbTransRqstResp()
    trFlsPip = ItlbTransFlsPipe()
    trPtwReq = ItlbTransPtwReq()
    trPtwResp = ItlbTransPtwResp()
    
    
    res = await itlb_env.itlbAgent.agent_itlb(trSfence, 
                                              trCsr,
                                              trRqstReq,
                                              trRqstReq,
                                              trRqstReq,
                                              trRqstResp,
                                              trRqstResp,
                                              trRqstResp,
                                              trFlsPip,
                                              trPtwReq,
                                              trPtwReq,
                                              trPtwReq,
                                              trPtwResp
                                              )
    