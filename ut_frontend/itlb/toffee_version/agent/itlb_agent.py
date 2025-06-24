from toffee.agent import *
from ..bundle import TlbBundle
from .itlb_trans import *
from toffee import Executor
from typing import List

class ItlbAgent(Agent):
    def __init__(self, bundle: TlbBundle):
        super().__init__(bundle)
        self.bundle = bundle
        self.drvReq0Flg     =   False
        self.drvReq1Flg     =   False
        self.drvReq2Flg     =   False
        
    # drive signals into dut: Sfence signals
    async def drvSfence(self, cycles, sfenceBits, trSfence:ItlbTransSfence):
        print("drv sfence")
        for i in range(cycles):
            sfenceBits._rs1.value                             =       trSfence.sfenceBitsRs1[i]
            sfenceBits._rs2.value                             =       trSfence.sfenceBitsRs2[i]
            sfenceBits._addr.value                            =       trSfence.sfenceBitsAddr[i]
            sfenceBits._id.value                              =       trSfence.sfenceBitsId[i]
            sfenceBits._flushPipe.value                       =       trSfence.sfenceBitsFlushPipe[i]
            sfenceBits._hv.value                              =       trSfence.sfenceBitsHv[i]
            sfenceBits._hg.value                              =       trSfence.sfenceBitsHg[i]
            await self.bundle.step()
    
    # drive signals into dut: flush pip        
    async def drvFlsPip(self, cycles, flushPipe, trFlsPip:ItlbTransFlsPipe):
     for i in range(cycles):
         #print("trDrvFls")
         flushPipe._0.value                                =       trFlsPip.flushPipe0[i]
         flushPipe._1.value                                =       trFlsPip.flushPipe1[i]
         flushPipe._2.value                                =       trFlsPip.flushPipe2[i]
         await self.bundle.step()
        
    # drive signals into dut: Csr signals
    def drvCsr(self, idx):
        csr         =   self.bundle.io._csr
        csr._satp._mode.value                             =       self.trCsr.csrSatpMode[idx]
        csr._satp._asid.value                             =       self.trCsr.csrSatpAsid[idx]
        csr._satp._changed.value                          =       self.trCsr.csrSatpChanged[idx]
        csr._vsatp._mode.value                            =       self.trCsr.csrVsatpMode[idx]
        csr._vsatp._asid.value                            =       self.trCsr.csrVsatpAsid[idx]
        csr._vsatp._changed.value                         =       self.trCsr.csrVsatpChanged[idx]
        csr._hgatp._mode.value                            =       self.trCsr.csrHgatpMode[idx]
        csr._hgatp._vmid.value                            =       self.trCsr.csrHgatpVmid[idx]
        csr._hgatp._changed.value                         =       self.trCsr.csrHgatpChanged[idx]
        csr._priv._virt.value                             =       self.trCsr.csrPrivVirt[idx]
        csr._priv._virt.value                             =       self.trCsr.csrPrivImode[idx]
        #await self.bundle.step()
            
    # drive signals: Requestor 0 or 1
    async def drvRequestor0(self, cycles, requestor, trReq:ItlbTransRqstReq): 
        print("drvRequestor0")
        for i in range(cycles + 1):
            if(trReq.requestorReqBitsVaddr[i] != 0):
                print(f"i = {i}")
                print(f"Vaddr = {trReq.requestorReqBitsVaddr[i]}")
                requestor._req._valid.value                      =       True
                requestor._req._bits_vaddr.value                 =       trReq.requestorReqBitsVaddr[i]
            else:
                requestor._req._valid.value                      =       False
            self.drvCsr(i)
            await self.bundle.step()
        requestor._req._valid.value                      =       False
        self.drvReq0Flg =   True
    
    # drive signals: Requestor 0 or 1
    async def drvRequestor1(self, cycles, requestor, trReq:ItlbTransRqstReq): 
        print("drvRequestor1")        
        while(not self.drvReq0Flg):
            await self.bundle.step()
        for i in range(cycles + 1):
            if(trReq.requestorReqBitsVaddr[i] != 0):
                requestor._req._valid.value                      =       True
                print(f"i = {i}")
                print(f"Vaddr = {trReq.requestorReqBitsVaddr[i]}")
                requestor._req._bits_vaddr.value                 =       trReq.requestorReqBitsVaddr[i]
            else:
                requestor._req._valid.value                      =       False
            self.drvCsr(i)
            await self.bundle.step()
        requestor._req._valid.value                      =       False
        self.drvReq1Flg =   True
    
    # drive signals: requestor 2
    async def drvRequestor2(self, cycles, requestor, trReq:ItlbTransRqstReq):
        print("drvRequestor2")
        waitCycle = 0
        while(not self.drvReq1Flg):
            await self.bundle.step()
            print("drvReq1Flg is False")
        for i in range(cycles + 1):
            requestor._req._valid.value                =        False
            while(not requestor._req._ready.value):
                requestor._req._valid.value                    =   False
                print(f"rqst2 blocked and waited {waitCycle} cycles")
                waitCycle += 1
                await self.bundle.step()
            # drive signals into dut: Requestor 2
            if(trReq.requestorReqBitsVaddr[i] != 0):
                print(f"i = {i}")
                print(f"Vaddr = {trReq.requestorReqBitsVaddr[i]}")
                requestor._req._valid.value                     =    True
                requestor._req._bits_vaddr.value                =    trReq.requestorReqBitsVaddr[i]
            else:
                requestor._req._valid.value                     =    False
            self.drvCsr(i)
            await self.bundle.step()
        requestor._req._valid.value     =   False
        self.drvReq2Flg =   False
    
    async def drvPtwResp(self, cycles, ptwResp, trPtwResp:ItlbTransPtwResp):
        for i in range(cycles):
            #print("trDrvPtwResp")
            ptwResp._valid.value                              =       True
            ptwResp._bits._s2xlate.value                      =       trPtwResp.s2xlate[i]
            ptwResp._bits._getGpa.value                       =       trPtwResp.getgpa[i]
            ptwResp._bits._s1._entry._tag.value               =       trPtwResp.s1entrytag[i]
            ptwResp._bits._s1._entry._asid.value              =       trPtwResp.s1entryasid[i]
            ptwResp._bits._s1._entry._vmid.value              =       trPtwResp.s1entryvmid[i]
            ptwResp._bits._s1._entry._n.value                 =       trPtwResp.s1entryn[i]
            ptwResp._bits._s1._entry._pbmt.value              =       trPtwResp.s1entrypbmt[i]
            ptwResp._bits._s1._entry._perm._d.value           =       trPtwResp.s1entrypermd[i]
            ptwResp._bits._s1._entry._perm._a.value           =       trPtwResp.s1entryperma[i]
            ptwResp._bits._s1._entry._perm._g.value           =       trPtwResp.s1entrypermg[i]
            ptwResp._bits._s1._entry._perm._u.value           =       trPtwResp.s1entrypermu[i]
            ptwResp._bits._s1._entry._perm._x.value           =       trPtwResp.s1entrypermx[i]
            ptwResp._bits._s1._entry._perm._w.value           =       trPtwResp.s1entrypermw[i]
            ptwResp._bits._s1._entry._perm._r.value           =       trPtwResp.s1entrypermr[i]
            ptwResp._bits._s1._entry._level.value             =       trPtwResp.s1entrylevel[i]
            ptwResp._bits._s1._entry._v.value                 =       trPtwResp.s1entryv[i]
            ptwResp._bits._s1._entry._ppn.value               =       trPtwResp.s1entryppn[i]
            ptwResp._bits._s1._addr_low.value                 =       trPtwResp.s1addrlow[i]
            ptwResp._bits._s1._ppn_low._0.value               =       trPtwResp.s1ppnlow0[i]
            ptwResp._bits._s1._ppn_low._1.value               =       trPtwResp.s1ppnlow1[i]
            ptwResp._bits._s1._ppn_low._2.value               =       trPtwResp.s1ppnlow2[i]
            ptwResp._bits._s1._ppn_low._3.value               =       trPtwResp.s1ppnlow3[i]
            ptwResp._bits._s1._ppn_low._4.value               =       trPtwResp.s1ppnlow4[i]
            ptwResp._bits._s1._ppn_low._5.value               =       trPtwResp.s1ppnlow5[i]
            ptwResp._bits._s1._ppn_low._6.value               =       trPtwResp.s1ppnlow6[i]
            ptwResp._bits._s1._ppn_low._7.value               =       trPtwResp.s1ppnlow7[i]
            ptwResp._bits._s1._valididx._0.value              =       trPtwResp.s1valididx0[i]
            ptwResp._bits._s1._valididx._1.value              =       trPtwResp.s1valididx1[i]
            ptwResp._bits._s1._valididx._2.value              =       trPtwResp.s1valididx2[i]
            ptwResp._bits._s1._valididx._3.value              =       trPtwResp.s1valididx3[i]
            ptwResp._bits._s1._valididx._4.value              =       trPtwResp.s1valididx4[i]
            ptwResp._bits._s1._valididx._5.value              =       trPtwResp.s1valididx5[i]
            ptwResp._bits._s1._valididx._6.value              =       trPtwResp.s1valididx6[i]
            ptwResp._bits._s1._valididx._7.value              =       trPtwResp.s1valididx7[i]
            ptwResp._bits._s1._pteidx._0.value                =       trPtwResp.s1pteidx0[i]
            ptwResp._bits._s1._pteidx._1.value                =       trPtwResp.s1pteidx1[i]
            ptwResp._bits._s1._pteidx._2.value                =       trPtwResp.s1pteidx2[i]
            ptwResp._bits._s1._pteidx._3.value                =       trPtwResp.s1pteidx3[i]
            ptwResp._bits._s1._pteidx._4.value                =       trPtwResp.s1pteidx4[i]
            ptwResp._bits._s1._pteidx._5.value                =       trPtwResp.s1pteidx5[i]
            ptwResp._bits._s1._pteidx._6.value                =       trPtwResp.s1pteidx6[i]
            ptwResp._bits._s1._pteidx._7.value                =       trPtwResp.s1pteidx7[i]
            ptwResp._bits._s1._pf.value                       =       trPtwResp.s1pf[i]
            ptwResp._bits._s1._af.value                       =       trPtwResp.s1af[i]
            await self.bundle.step()
            ptwResp._bits._s2._entry._tag.value               =       trPtwResp.s2entrytag[i]
            ptwResp._bits._s2._entry._vmid.value              =       trPtwResp.s2entryvmid[i]
            ptwResp._bits._s2._entry._n.value                 =       trPtwResp.s2entryn[i]
            ptwResp._bits._s2._entry._pbmt.value              =       trPtwResp.s2entrypbmt[i]
            ptwResp._bits._s2._entry._ppn.value               =       trPtwResp.s2entryppn[i]
            ptwResp._bits._s2._entry._perm._d.value           =       trPtwResp.s2entrypermd[i]
            ptwResp._bits._s2._entry._perm._a.value           =       trPtwResp.s2entryperma[i]
            ptwResp._bits._s2._entry._perm._g.value           =       trPtwResp.s2entrypermg[i]
            ptwResp._bits._s2._entry._perm._u.value           =       trPtwResp.s2entrypermu[i]
            ptwResp._bits._s2._entry._perm._x.value           =       trPtwResp.s2entrypermx[i]
            ptwResp._bits._s2._entry._perm._w.value           =       trPtwResp.s2entrypermw[i]
            ptwResp._bits._s2._entry._perm._r.value           =       trPtwResp.s2entrypermr[i]
            ptwResp._bits._s2._entry._level.value             =       trPtwResp.s2entrylevel[i]
            ptwResp._bits._s2._gpf.value                      =       trPtwResp.s2gpf[i]
            ptwResp._bits._s2._gaf.value                      =       trPtwResp.s2gaf[i]
            await self.bundle.step()
        
    # get signals: requestor 0 or 1
    async def monReqestor0(self, requestor, trResp:ItlbTransRqstResp):
        i = 0
        while(True):
            #print("trMonReq")
            if(i < trResp.validPktLen):
                trResp.requestorRespBitsPaddr[i]              =       requestor._resp_bits._paddr._0.value
                trResp.requestorRespBitsGpaddr[i]             =       requestor._resp_bits._gpaddr._0.value
                trResp.requestorRespBitsPbmt[i]               =       requestor._resp_bits._pbmt._0.value
                trResp.requestorRespBitsMiss[i]               =       requestor._resp_bits._miss.value
                trResp.requestorRespBitsIsForVSnonLeafPTE[i]  =       requestor._resp_bits._isForVSnonLeafPTE.value
                trResp.requestorRespBitsExcpGpfInstr[i]       =       requestor._resp_bits._excp._0._gpf_instr.value
                trResp.requestorRespBitsExcpPfInstr[i]        =       requestor._resp_bits._excp._0._pf_instr.value
                trResp.requestorRespBitsExcpAfInstr[i]        =       requestor._resp_bits._excp._0._af_instr.value
                i += 1
            await self.bundle.step()
    
    # get signals: requestor 0 or 1
    async def monReqestor1(self, requestor, trResp:ItlbTransRqstResp):
        i = 0
        while(True):
            #print("trMonReq")
            if(i < trResp.validPktLen):
                trResp.requestorRespBitsPaddr[i]              =       requestor._resp_bits._paddr._0.value
                trResp.requestorRespBitsGpaddr[i]             =       requestor._resp_bits._gpaddr._0.value
                trResp.requestorRespBitsPbmt[i]               =       requestor._resp_bits._pbmt._0.value
                trResp.requestorRespBitsMiss[i]               =       requestor._resp_bits._miss.value
                trResp.requestorRespBitsIsForVSnonLeafPTE[i]  =       requestor._resp_bits._isForVSnonLeafPTE.value
                trResp.requestorRespBitsExcpGpfInstr[i]       =       requestor._resp_bits._excp._0._gpf_instr.value
                trResp.requestorRespBitsExcpPfInstr[i]        =       requestor._resp_bits._excp._0._pf_instr.value
                trResp.requestorRespBitsExcpAfInstr[i]        =       requestor._resp_bits._excp._0._af_instr.value
                i += 1
            await self.bundle.step()
    
    
    async def monRequestor2(self, requestor, trResp:ItlbTransRqstResp):
        i = 0
        while(True):
            #print("trMonReq2")
            requestor._resp._ready.value              =    True
            while(not requestor._resp._valid.value):
                await self.bundle.step()
            if(i < trResp.validPktLen):
                trResp.requestorRespBitsPaddr[i]             =    requestor._resp._bits._paddr._0.value
                trResp.requestorRespBitsGpaddr[i]            =    requestor._resp._bits._gpaddr._0.value
                trResp.requestorRespBitsPbmt[i]              =    requestor._resp._bits._pbmt._0.value
                trResp.requestorRespBitsIsForVSnonLeafPTE[i] =    requestor._resp._bits._isForVSnonLeafPTE.value
                trResp.requestorRespBitsExcpGpfInstr[i]      =    requestor._resp._bits._excp._0._gpf_instr.value
                trResp.requestorRespBitsExcpPfInstr[i]       =    requestor._resp._bits._excp._0._pf_instr.value
                trResp.requestorRespBitsExcpAfInstr[i]       =    requestor._resp._bits._excp._0._af_instr.value
                i += 1
            await self.bundle.step()
    
    async def monPtwReq0(self, ptwReq, trPtwReq:ItlbTransPtwReq):
        i = 0
        while(True):
            #print("trMonPtwReq")
            while(not ptwReq._valid.value):
                await self.bundle.step()
            if(i < trPtwReq.validPktLen):
                trPtwReq.reqBitsVpn[i]                         =       ptwReq._bits._vpn.value   
                trPtwReq.reqBitsGetGpa[i]                      =       ptwReq._bits._getGpa.value
                trPtwReq.reqBitsS2Xlate[i]                     =       ptwReq._bits._s2xlate.value
                i += 1
            await self.bundle.step()
    
    async def monPtwReq1(self, ptwReq, trPtwReq:ItlbTransPtwReq):
        i = 0
        while(True):
            #print("trMonPtwReq")
            while(not ptwReq._valid.value):
                await self.bundle.step()
            if(i < trPtwReq.validPktLen):
                trPtwReq.reqBitsVpn[i]                         =       ptwReq._bits._vpn.value   
                trPtwReq.reqBitsGetGpa[i]                      =       ptwReq._bits._getGpa.value
                trPtwReq.reqBitsS2Xlate[i]                     =       ptwReq._bits._s2xlate.value
                i += 1
            await self.bundle.step()
    
    async def monPtwReq2(self, ptwReq, trPtwReq:ItlbTransPtwReq):
        i = 0
        while(True):
            #print("trMonPtwReq2")
            ptwReq._ready.value                         =       True
            while(not ptwReq._valid.value):
                await self.bundle.step()
            if(i < trPtwReq.validPktLen):
                trPtwReq.reqBitsVpn[i]                         =       ptwReq._bits._vpn.value   
                trPtwReq.reqBitsGetGpa[i]                      =       ptwReq._bits._getGpa.value
                trPtwReq.reqBitsS2Xlate[i]                     =       ptwReq._bits._s2xlate.value
            i += 1
            await self.bundle.step()
        
        
    async def delayCycle(self, cycles):
        print(f"Test clock cycles: {cycles}")
        await self.bundle.step(cycles)
     
#    # driving signals with limited cycles
#    async def drv_lim_cycle(self, cycles, sfenceBits, csr, requestor0, requestor1, requestor2, flushPipe, ptwResp,
#        trSfence: ItlbTransSfence,
#        trCsr: ItlbTransCsr,
#        trRqstReq0: ItlbTransRqstReq, trRqstReq1: ItlbTransRqstReq, trRqstReq2: ItlbTransRqstReq,
#        trFlsPip: ItlbTransFlsPipe,
#        trPtwResp: ItlbTransPtwResp
#        ):
#        async with Executor(exit="any") as exec:
#            exec(self.drv_blocked(cycles, requestor2, ptwResp, trRqstReq2, ptwResp, trPtwResp))
#            exec(self.delayCycle(4*cycles))
#    
#    # driving signals with some blocking calls
#    async def drv_blocked(self, cycles, requestor2, ptwResp,
#        trRqstReq2: ItlbTransRqstReq,
#        trPtwResp: ItlbTransPtwResp
#        ):
#        async with Executor(exit="all") as exec:
#            exec(self.drvRequestor2(cycles, requestor2, trRqstReq2))
#            exec(self.drvPtwResp(cycles, ptwResp, trPtwResp))
#    
    # agent top func
    async def agent_itlb(self, cycles,
        trSfence: ItlbTransSfence,
        trCsr: ItlbTransCsr,
        trRqstReq0: ItlbTransRqstReq, trRqstReq1: ItlbTransRqstReq, trRqstReq2: ItlbTransRqstReq,
        trRqstResp0: ItlbTransRqstResp, trRqstResp1: ItlbTransRqstResp, trRqstResp2: ItlbTransRqstResp,
        trFlsPip: ItlbTransFlsPipe,
        trPtwReq0: ItlbTransPtwReq, trPtwReq1: ItlbTransPtwReq, trPtwReq2: ItlbTransPtwReq,
        trPtwResp: ItlbTransPtwResp
        ):
        self.cycles =   cycles
        
        ## bundle abbr
        # sfence
        sfenceBits  =   self.bundle.io._sfence._bits
        # csr
        csr         =   self.bundle.io._csr
        # requestor
        requestor0  =   self.bundle.io._requestor._0
        requestor1  =   self.bundle.io._requestor._1
        requestor2  =   self.bundle.io._requestor._2
        # flushPipe
        flushPipe  =   self.bundle.io._flushPipe
        # ptw request
        ptwReq0     =   self.bundle.io._ptw._req._0
        ptwReq1     =   self.bundle.io._ptw._req._1
        ptwReq2     =   self.bundle.io._ptw._req._2
        # ptw respond
        ptwResp     =   self.bundle.io._ptw._resp
        
        self.trCsr  =   trCsr
        
        # reset
        await self.bundle.step(1)
        self.bundle.reset.value = 1
        await self.bundle.step(2)
        self.bundle.reset.value = 0
        await self.bundle.step(8)
        
        async with Executor(exit="none") as exec:
#            exec(self.drv_lim_cycle(cycles,
#            sfenceBits,csr,requestor0,requestor1,requestor2,flushPipe,ptwResp,
#            trSfence,
#            trCsr,
#            trRqstReq0,
#            trRqstReq1,
#            trRqstReq2,
#            trFlsPip,
#            trPtwResp
#            ))
            exec(self.drvSfence(cycles, sfenceBits, trSfence))
            exec(self.drvRequestor0(cycles, requestor0, trRqstReq0))
            exec(self.drvRequestor1(cycles, requestor1, trRqstReq1))
            exec(self.drvRequestor2(cycles, requestor2, trRqstReq1))
            exec(self.drvFlsPip(cycles, flushPipe, trFlsPip))
            exec(self.drvPtwResp(cycles, ptwResp, trPtwResp))
            exec(self.monReqestor0(requestor0, trRqstResp0))
            exec(self.monReqestor1(requestor1, trRqstResp1))
            exec(self.monRequestor2(requestor2, trRqstResp2))
            exec(self.monPtwReq0(ptwReq0, trPtwReq0))
            exec(self.monPtwReq1(ptwReq1, trPtwReq1))
            exec(self.monPtwReq2(ptwReq2, trPtwReq2))
        await self.bundle.step(4*cycles)
        
        return 0