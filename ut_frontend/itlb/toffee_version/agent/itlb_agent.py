from toffee.agent import *
from ..bundle import TlbBundle
from .itlb_trans import *
from toffee import Executor

class ItlbAgent(Agent):
    def __init__(self, bundle: TlbBundle):
        super().__init__(bundle)
        self.bundle = bundle
        
    #@driver_method
    async def drvSfence(self, sfenceBits, trSfence:ItlbTransSfence):
        # drive signals into dut: Sfence signals
        sfenceBits._rs1.value                             =       trSfence.sfenceBitsRs1
        sfenceBits._rs2.value                             =       trSfence.sfenceBitsRs2
        sfenceBits._addr.value                            =       trSfence.sfenceBitsAddr
        sfenceBits._id.value                              =       trSfence.sfenceBitsId
        sfenceBits._flushPipe.value                       =       trSfence.sfenceBitsFlushPipe
        sfenceBits._hv.value                              =       trSfence.sfenceBitsHv
        sfenceBits._hg.value                              =       trSfence.sfenceBitsHg
    
    async def drvCsr(self, csr, trCsr:ItlbTransCsr):
        # drive signals into dut: Csr signals
        csr._satp._mode.value                             =       trCsr.csrSatpMode
        csr._satp._asid.value                             =       trCsr.csrSatpAsid
        csr._satp._changed.value                          =       trCsr.csrSatpChanged
        csr._vsatp._mode.value                            =       trCsr.csrVsatpMode
        csr._vsatp._asid.value                            =       trCsr.csrVsatpAsid
        csr._vsatp._changed.value                         =       trCsr.csrVsatpChanged
        csr._hgatp._mode.value                            =       trCsr.csrHgatpMode
        csr._hgatp._vmid.value                            =       trCsr.csrHgatpVmid
        csr._hgatp._changed.value                         =       trCsr.csrHgatpChanged
        csr._priv._virt.value                             =       trCsr.csrPrivVirt
        csr._priv._virt.value                             =       trCsr.csrPrivImode
    
    async def drvReqestor(self, requestor, trReq:ItlbTransRqstReq): 
        # drive signals: Requestor 0 or 1
        requestor._req._valid.value                      =       True
        requestor._req._bits_vaddr.value                 =       trReq.requestorReqBitsVaddr
        await self.bundle.step()
        requestor._req._valid.value                      =       False
        
    async def monReqestor(self, requestor, trResp:ItlbTransRqstResp):
        # get signals: requestor 0 or 1
        trResp.requestorRespBitsPaddr              =       requestor._resp_bits._paddr.value
        trResp.requestorRespBitsGpaddr             =       requestor._resp_bits._gpaddr.value
        trResp.requestorRespBitsPbmt               =       requestor._resp_bits._pbmt.value
        trResp.requestorRespBitsMiss               =       requestor._resp_bits._miss.value
        trResp.requestorRespBitsIsForVSnonLeafPTE  =       requestor._resp_bits._isForVSnonLeafPTE.value
        trResp.requestorRespBitsExcpGpfInstr       =       requestor._resp_bits._excp._0._gpf_instr.value
        trResp.requestorRespBitsExcpPfInstr        =       requestor._resp_bits._excp._0._pf_instr.value
        trResp.requestorRespBitsExcpAfInstr        =       requestor._resp_bits._excp._0._af_instr.value
        return trResp
    
    async def drvReqestor2(self, requestor, trReq:ItlbTransRqstReq):
        # drive signals: requestor 2
        while(not requestor._req._ready.value):
            await self.bundle.step()
        # drive signals into dut: Requestor 2
        requestor._req._valid.value                     =    True
        requestor._req._bits_vaddr.value                =    trReq.requestorReqBitsVaddr
        requestor._resp._ready.value                    =    True
        await self.bundle.step()
        requestor._req._valid.value                     =    False
    
    async def monRequestor2(self, requestor, trResp:ItlbTransRqstResp):
        requestor._resp._ready.value              =    True
        while(not requestor._resp._valid.value):
            await self.bundle.step()
        trResp.requestorRespBitsPaddr             =    requestor._resp._bits._paddr
        trResp.requestorRespBitsGpaddr            =    requestor._resp._bits._gpaddr.value
        trResp.requestorRespBitsPbmt              =    requestor._resp._bits._pbmt.value
        trResp.requestorRespBitsIsForVSnonLeafPTE =    requestor._resp._bits._isForVSnonLeafPTE.value
        trResp.requestorRespBitsExcpGpfInstr      =    requestor._resp._bits._excp._0._gpf_instr.value
        trResp.requestorRespBitsExcpPfInstr       =    requestor._resp._bits._excp._0._pf_instr.value
        trResp.requestorRespBitsExcpAfInstr       =    requestor._resp._bits._excp._0._af_instr.value
        await self.bundle.step()
        requestor._resp._ready.value              =    False
        return trResp
    
    async def drvFlsPip(self, flushPipe, trFlsPip:ItlbTransFlsPipe):
        flushPipe._0.value                                =       trFlsPip.flushPipe0
        flushPipe._1.value                                =       trFlsPip.flushPipe1
        flushPipe._2.value                                =       trFlsPip.flushPipe2
        
    async def monPtwReq(self, ptwReq, trPtwReq:ItlbTransPtwReq):
        # monitor signals: ptw req 0 or 1
        while(not ptwReq._valid.value):
            await self.bundle.step()
        trPtwReq.reqBitsVpn                         =       ptwReq._bits._vpn.value   
        trPtwReq.reqBitsGetGpa                      =       ptwReq._bits._getGpa.value
        trPtwReq.reqBitsS2Xlate                     =       ptwReq._bits._s2xlate.value
        return trPtwReq
    
    async def monPtwReq2(self, ptwReq, trPtwReq:ItlbTransPtwReq):
        # monitor signals: ptw req2
        ptwReq._ready.value                         =       True
        while(not ptwReq._valid.value):
            await self.bundle.steop()
        trPtwReq.reqBitsVpn                         =       ptwReq._bits._vpn.value   
        trPtwReq.reqBitsGetGpa                      =       ptwReq._bits._getGpa.value
        trPtwReq.reqBitsS2Xlate                     =       ptwReq._bits._s2xlate.value
        ptwReq._ready.value                         =       False
        return trPtwReq
        
    
    async def drvPtwResp(self, ptwResp, trPtwResp:ItlbTransPtwResp):
        ptwResp._valid.value                              =       True
        ptwResp._bits._s2xlate.value                      =       trPtwResp.ptwrespbitss2xlate     
        ptwResp._bits._getGpa.value                       =       trPtwResp.ptwrespbitsgetgpa      
        ptwResp._bits._s1._entry._tag.value               =       trPtwResp.ptwrespbitss1entrytag  
        ptwResp._bits._s1._entry._asid.value              =       trPtwResp.ptwrespbitss1entryasid 
        ptwResp._bits._s1._entry._vmid.value              =       trPtwResp.ptwrespbitss1entryvmid 
        ptwResp._bits._s1._entry._n.value                 =       trPtwResp.ptwrespbitss1entryn    
        ptwResp._bits._s1._entry._pbmt.value              =       trPtwResp.ptwrespbitss1entrypbmt 
        ptwResp._bits._s1._entry._perm._d.value           =       trPtwResp.ptwrespbitss1entrypermd
        ptwResp._bits._s1._entry._perm._a.value           =       trPtwResp.ptwrespbitss1entryperma
        ptwResp._bits._s1._entry._perm._g.value           =       trPtwResp.ptwrespbitss1entrypermg
        ptwResp._bits._s1._entry._perm._u.value           =       trPtwResp.ptwrespbitss1entrypermu
        ptwResp._bits._s1._entry._perm._x.value           =       trPtwResp.ptwrespbitss1entrypermx
        ptwResp._bits._s1._entry._perm._w.value           =       trPtwResp.ptwrespbitss1entrypermw
        ptwResp._bits._s1._entry._perm._r.value           =       trPtwResp.ptwrespbitss1entrypermr
        ptwResp._bits._s1._entry._level.value             =       trPtwResp.ptwrespbitss1entrylevel
        ptwResp._bits._s1._entry._v.value                 =       trPtwResp.ptwrespbitss1entryv    
        ptwResp._bits._s1._entry._ppn.value               =       trPtwResp.ptwrespbitss1entryppn  
        ptwResp._bits._s1._addr_low.value                 =       trPtwResp.ptwrespbitss1addrlow   
        ptwResp._bits._s1._ppn_low._0.value               =       trPtwResp.ptwrespbitss1ppnlow0   
        ptwResp._bits._s1._ppn_low._1.value               =       trPtwResp.ptwrespbitss1ppnlow1   
        ptwResp._bits._s1._ppn_low._2.value               =       trPtwResp.ptwrespbitss1ppnlow2   
        ptwResp._bits._s1._ppn_low._3.value               =       trPtwResp.ptwrespbitss1ppnlow3   
        ptwResp._bits._s1._ppn_low._4.value               =       trPtwResp.ptwrespbitss1ppnlow4   
        ptwResp._bits._s1._ppn_low._5.value               =       trPtwResp.ptwrespbitss1ppnlow5   
        ptwResp._bits._s1._ppn_low._6.value               =       trPtwResp.ptwrespbitss1ppnlow6   
        ptwResp._bits._s1._ppn_low._7.value               =       trPtwResp.ptwrespbitss1ppnlow7   
        ptwResp._bits._s1._valididx._0.value              =       trPtwResp.ptwrespbitss1valididx0 
        ptwResp._bits._s1._valididx._1.value              =       trPtwResp.ptwrespbitss1valididx1 
        ptwResp._bits._s1._valididx._2.value              =       trPtwResp.ptwrespbitss1valididx2 
        ptwResp._bits._s1._valididx._3.value              =       trPtwResp.ptwrespbitss1valididx3 
        ptwResp._bits._s1._valididx._4.value              =       trPtwResp.ptwrespbitss1valididx4 
        ptwResp._bits._s1._valididx._5.value              =       trPtwResp.ptwrespbitss1valididx5 
        ptwResp._bits._s1._valididx._6.value              =       trPtwResp.ptwrespbitss1valididx6 
        ptwResp._bits._s1._valididx._7.value              =       trPtwResp.ptwrespbitss1valididx7 
        ptwResp._bits._s1._pteidx._0.value                =       trPtwResp.ptwrespbitss1pteidx0   
        ptwResp._bits._s1._pteidx._1.value                =       trPtwResp.ptwrespbitss1pteidx1   
        ptwResp._bits._s1._pteidx._2.value                =       trPtwResp.ptwrespbitss1pteidx2   
        ptwResp._bits._s1._pteidx._3.value                =       trPtwResp.ptwrespbitss1pteidx3   
        ptwResp._bits._s1._pteidx._4.value                =       trPtwResp.ptwrespbitss1pteidx4   
        ptwResp._bits._s1._pteidx._5.value                =       trPtwResp.ptwrespbitss1pteidx5   
        ptwResp._bits._s1._pteidx._6.value                =       trPtwResp.ptwrespbitss1pteidx6   
        ptwResp._bits._s1._pteidx._7.value                =       trPtwResp.ptwrespbitss1pteidx7   
        ptwResp._bits._s1._pf.value                       =       trPtwResp.ptwrespbitss1pf        
        ptwResp._bits._s1._af.value                       =       trPtwResp.ptwrespbitss1af        
        await self.bundle.step()
        ptwResp._bits._s2._entry._tag.value               =       trPtwResp.ptwrespbitss2entrytag  
        ptwResp._bits._s2._entry._vmid.value              =       trPtwResp.ptwrespbitss2entryvmid 
        ptwResp._bits._s2._entry._n.value                 =       trPtwResp.ptwrespbitss2entryn    
        ptwResp._bits._s2._entry._pbmt.value              =       trPtwResp.ptwrespbitss2entrypbmt 
        ptwResp._bits._s2._entry._ppn.value               =       trPtwResp.ptwrespbitss2entryppn  
        ptwResp._bits._s2._entry._perm._d.value           =       trPtwResp.ptwrespbitss2entrypermd
        ptwResp._bits._s2._entry._perm._a.value           =       trPtwResp.ptwrespbitss2entryperma
        ptwResp._bits._s2._entry._perm._g.value           =       trPtwResp.ptwrespbitss2entrypermg
        ptwResp._bits._s2._entry._perm._u.value           =       trPtwResp.ptwrespbitss2entrypermu
        ptwResp._bits._s2._entry._perm._x.value           =       trPtwResp.ptwrespbitss2entrypermx
        ptwResp._bits._s2._entry._perm._w.value           =       trPtwResp.ptwrespbitss2entrypermw
        ptwResp._bits._s2._entry._perm._r.value           =       trPtwResp.ptwrespbitss2entrypermr
        ptwResp._bits._s2._entry._level.value             =       trPtwResp.ptwrespbitss2entrylevel
        ptwResp._bits._s2._gpf.value                      =       trPtwResp.ptwrespbitss2gpf       
        ptwResp._bits._s2._gaf.value                      =       trPtwResp.ptwrespbitss2gaf       
        
        
    async def agent_itlb(self, 
        trSfence:ItlbTransSfence, \
        trCsr:ItlbTransCsr, \
        trRqstReq0:ItlbTransRqstReq, trRqstReq1:ItlbTransRqstReq, trRqstReq2:ItlbTransRqstReq, \
        trRqstResp0:ItlbTransRqstResp, trRqstResp1:ItlbTransRqstResp, trRqstResp2:ItlbTransRqstResp, \
        trFlsPip:ItlbTransFlsPipe, \
        trPtwReq0:ItlbTransPtwReq, trPtwReq1:ItlbTransPtwReq, trPtwReq2:ItlbTransPtwReq,    \
        trPtwResp:ItlbTransPtwResp
        ):
        
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
        
        # reset
        self.bundle.reset.value = 1
        await self.bundle.step(1)
        self.bundle.reset.value = 0
        
        async with Executor() as exec:
            exec(self.drvSfence(sfenceBits, trSfence))
            exec(self.drvCsr(csr, trCsr))
            exec(self.drvReqestor(requestor0, trRqstReq0))
            exec(self.drvReqestor(requestor1, trRqstReq1))
            exec(self.drvReqestor2(requestor2, trRqstReq2))
            exec(self.monReqestor(requestor0, trRqstResp0))
            exec(self.monReqestor(requestor1, trRqstResp1))
            exec(self.monRequestor2(requestor2, trRqstResp2))
            exec(self.drvFlsPip(flushPipe, trFlsPip))
            exec(self.monPtwReq(ptwReq0, trPtwReq0))
            exec(self.monPtwReq(ptwReq1, trPtwReq1))
            exec(self.monPtwReq2(ptwReq2, trPtwReq2))
            exec(self.drvPtwResp(ptwResp, trPtwResp))
        res = exec.get_results()
        await self.bundle.step(10)
        
        return res