from ..agent.itlb_trans import *
import random

class ItlbSqr:
    def __init__(self, pktLen):
        self.pktLen = pktLen
        self.trSfence    =   ItlbTransSfence(2*self.pktLen)
        self.trCsr       =   ItlbTransCsr(2*self.pktLen)
        self.trRqstReq0  =   ItlbTransRqstReq(2*self.pktLen) 
        self.trRqstReq1  =   ItlbTransRqstReq(2*self.pktLen) 
        self.trRqstReq2  =   ItlbTransRqstReq(2*self.pktLen) 
        self.trRqstResp0 =   ItlbTransRqstResp(2*self.pktLen)
        self.trRqstResp1 =   ItlbTransRqstResp(2*self.pktLen)  
        self.trRqstResp2 =   ItlbTransRqstResp(2*self.pktLen)  
        self.trFlsPip    =   ItlbTransFlsPipe(2*self.pktLen)
        self.trPtwReq0   =   ItlbTransPtwReq(2*self.pktLen)
        self.trPtwReq1   =   ItlbTransPtwReq(2*self.pktLen)
        self.trPtwReq2   =   ItlbTransPtwReq(2*self.pktLen)
        self.trPtwResp   =   ItlbTransPtwResp(2*self.pktLen)
    
    def gen_vec(self, caseTag):
        if(caseTag == 0):
            pass
        elif caseTag == "caseAcptRqst":
            for i in range(1, self.pktLen + 1):
                self.trRqstReq0.requestorReqBitsVaddr[i] = random.randint(0, 2**50 - 1)
                self.trRqstReq1.requestorReqBitsVaddr[i] = random.randint(0, 2**50 - 1)
                self.trRqstReq2.requestorReqBitsVaddr[i] = random.randint(0, 2**50 - 1)
            for i in range(self.pktLen):
                self.trCsr.csrSatpMode[i] = 9
                self.trCsr.csrSatpAsid[i] = 1
        else:
            print("Case Tag does not exist!")
        
        return self.trSfence, self.trCsr, self.trRqstReq0, self.trRqstReq1, self.trRqstReq2, self.trRqstResp0, self.trRqstResp1, self.trRqstResp2, self.trFlsPip, self.trPtwReq0, self.trPtwReq1, self.trPtwReq2, self.trPtwResp
    
    def __set_resp(self):
        for i in range(self.pktLen):
            self.trPtwResp.s1entryasid[i] = self.trcsr.csrSatpAsid[i]
            self.trPtwResp.s1entryvmid[i] = 0
            self.trPtwResp.s1entrypermd[i] = 0
            self.trPtwResp.s1entryperma[i] = random.choice(True, False)
            self.trPtwResp.s1entrypermg[i] = random.choice(True, False)
            self.trPtwResp.s1entrypermu[i] = random.choice(True, False)
            self.trPtwResp.s1entrypermx[i] = random.choice(True, False)
            self.trPtwResp.s1entrypermw[i] = random.choice(True, False)
            self.trPtwResp.s1entrypermr[i] = random.choice(True, False)
            self.trPtwResp.s1entrylevel[i] = 0
            self.trPtwResp.s1entryppn[i] = random.randint(2*33 - 1)
            self.trPtwResp.s1addrlow[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow0[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow1[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow2[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow3[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow4[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow5[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow6[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1ppnlow7[i] = random.randint(2*3 - 1)
            self.trPtwResp.s1valididx0[i] = 0
            self.trPtwResp.s1valididx1[i] = 0
            self.trPtwResp.s1valididx2[i] = 0
            self.trPtwResp.s1valididx3[i] = 0
            self.trPtwResp.s1valididx4[i] = 0
            self.trPtwResp.s1valididx5[i] = 0
            self.trPtwResp.s1valididx6[i] = 0
            self.trPtwResp.s1valididx7[i] = 0
            self.trPtwResp.s1pteidx0[i] = 0
            self.trPtwResp.s1pteidx1[i] = 0
            self.trPtwResp.s1pteidx2[i] = 0
            self.trPtwResp.s1pteidx3[i] = 0
            self.trPtwResp.s1pteidx4[i] = 0
            self.trPtwResp.s1pteidx5[i] = 0
            self.trPtwResp.s1pteidx6[i] = 0
            self.trPtwResp.s1pteidx7[i] = 0
            self.trPtwResp.s1pf[i] = 0
            self.trPtwResp.s1af[i] = 0
            self.trPtwResp.s2entrytag[i] = 0
            self.trPtwResp.s2entryvmid[i] = 0
            self.trPtwResp.s2entryn[i] = 0
            self.trPtwResp.s2entrypbmt[i] = 0
            self.trPtwResp.s2entryppn[i] = 0
            self.trPtwResp.s2entrypermd[i] = 0
            self.trPtwResp.s2entryperma[i] = 0
            self.trPtwResp.s2entrypermg[i] = 0
            self.trPtwResp.s2entrypermu[i] = 0
            self.trPtwResp.s2entrypermx[i] = 0
            self.trPtwResp.s2entrypermw[i] = 0
            self.trPtwResp.s2entrypermr[i] = 0
            self.trPtwResp.s2entrylevel[i] = 0
            self.trPtwResp.s2gpf[i] = 0
            self.trPtwResp.s2gaf[i] = 0
            self.trPtwResp.getgpa[i] = 0
            
            
            
            
        
    def __del__(self):
        pass
        #for i in range(self.pktLen):
        #    del self.trSfence[i]   
        #    del self.trCsr[i]      
        #    del self.trRqstReq0[i] 
        #    del self.trRqstReq1[i] 
        #    del self.trRqstReq2[i] 
        #    del self.trRqstResp0[i]
        #    del self.trRqstResp1[i]
        #    del self.trRqstResp2[i]
        #    del self.trFlsPip[i]   
        #    del self.trPtwReq0[i]  
        #    del self.trPtwReq1[i]  
        #    del self.trPtwReq2[i]  
        #    del self.trPtwResp[i]  
    