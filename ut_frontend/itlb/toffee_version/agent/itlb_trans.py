class baseTr():
    def __init__(self):
        self.startIdx       =   0
        self.validPktLen    =   0

# Trans packet for tlb
class ItlbTransSfence(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.sfenceBitsRs1 = [0] * pktLen
        self.sfenceBitsRs2 = [0] * pktLen
        self.sfenceBitsAddr = [0] * pktLen
        self.sfenceBitsId = [0] * pktLen 
        self.sfenceBitsFlushPipe = [0] * pktLen
        self.sfenceBitsHv = [0] * pktLen
        self.sfenceBitsHg = [0] * pktLen

class ItlbTransCsr(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.csrSatpMode = [0] * pktLen
        self.csrSatpAsid = [0] * pktLen
        self.csrSatpChanged = [0] * pktLen
        self.csrVsatpMode = [0] * pktLen
        self.csrVsatpAsid = [0] * pktLen
        self.csrVsatpChanged = [0] * pktLen
        self.csrHgatpMode = [0] * pktLen
        self.csrHgatpVmid = [0] * pktLen
        self.csrHgatpChanged = [0] * pktLen
        self.csrPrivVirt = [0] * pktLen
        self.csrPrivImode = [0] * pktLen

class ItlbTransRqstReq(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.requestorReqBitsVaddr = [0] * pktLen

class ItlbTransRqstResp(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.requestorRespBitsPaddr             =   [0] * pktLen
        self.requestorRespBitsGpaddr            =   [0] * pktLen
        self.requestorRespBitsPbmt              =   [0] * pktLen
        self.requestorRespBitsMiss              =   [0] * pktLen
        self.requestorRespBitsIsForVSnonLeafPTE =   [0] * pktLen
        self.requestorRespBitsExcpGpfInstr      =   [0] * pktLen
        self.requestorRespBitsExcpPfInstr       =   [0] * pktLen
        self.requestorRespBitsExcpAfInstr       =   [0] * pktLen

class ItlbTransFlsPipe(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.flushPipe0 = [0] * pktLen
        self.flushPipe1 = [0] * pktLen
        self.flushPipe2 = [0] * pktLen
        
class ItlbTransPtwReq(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.reqBitsVpn             =   [0] * pktLen
        self.reqBitsS2Xlate         =   [0] * pktLen
        self.reqBitsGetGpa          =   [0] * pktLen
        
class ItlbTransPtwResp(baseTr):
    def __init__(self, pktLen):
        super().__init__()
        self.validPktLen    =   pktLen
        self.s2xlate         =   [0] * pktLen
        self.s1entrytag      =   [0] * pktLen
        self.s1entryasid     =   [0] * pktLen
        self.s1entryvmid     =   [0] * pktLen
        self.s1entryn        =   [0] * pktLen
        self.s1entrypbmt     =   [0] * pktLen
        self.s1entrypermd    =   [0] * pktLen
        self.s1entryperma    =   [0] * pktLen
        self.s1entrypermg    =   [0] * pktLen
        self.s1entrypermu    =   [0] * pktLen
        self.s1entrypermx    =   [0] * pktLen
        self.s1entrypermw    =   [0] * pktLen
        self.s1entrypermr    =   [0] * pktLen
        self.s1entrylevel    =   [0] * pktLen
        self.s1entryv        =   [0] * pktLen
        self.s1entryppn      =   [0] * pktLen
        self.s1addrlow       =   [0] * pktLen
        self.s1ppnlow0       =   [0] * pktLen
        self.s1ppnlow1       =   [0] * pktLen
        self.s1ppnlow2       =   [0] * pktLen
        self.s1ppnlow3       =   [0] * pktLen
        self.s1ppnlow4       =   [0] * pktLen
        self.s1ppnlow5       =   [0] * pktLen
        self.s1ppnlow6       =   [0] * pktLen
        self.s1ppnlow7       =   [0] * pktLen
        self.s1valididx0     =   [0] * pktLen
        self.s1valididx1     =   [0] * pktLen
        self.s1valididx2     =   [0] * pktLen
        self.s1valididx3     =   [0] * pktLen
        self.s1valididx4     =   [0] * pktLen
        self.s1valididx5     =   [0] * pktLen
        self.s1valididx6     =   [0] * pktLen
        self.s1valididx7     =   [0] * pktLen
        self.s1pteidx0       =   [0] * pktLen
        self.s1pteidx1       =   [0] * pktLen
        self.s1pteidx2       =   [0] * pktLen
        self.s1pteidx3       =   [0] * pktLen
        self.s1pteidx4       =   [0] * pktLen
        self.s1pteidx5       =   [0] * pktLen
        self.s1pteidx6       =   [0] * pktLen
        self.s1pteidx7       =   [0] * pktLen
        self.s1pf            =   [0] * pktLen
        self.s1af            =   [0] * pktLen
        self.s2entrytag      =   [0] * pktLen
        self.s2entryvmid     =   [0] * pktLen
        self.s2entryn        =   [0] * pktLen
        self.s2entrypbmt     =   [0] * pktLen
        self.s2entryppn      =   [0] * pktLen
        self.s2entrypermd    =   [0] * pktLen
        self.s2entryperma    =   [0] * pktLen
        self.s2entrypermg    =   [0] * pktLen
        self.s2entrypermu    =   [0] * pktLen
        self.s2entrypermx    =   [0] * pktLen
        self.s2entrypermw    =   [0] * pktLen
        self.s2entrypermr    =   [0] * pktLen
        self.s2entrylevel    =   [0] * pktLen
        self.s2gpf           =   [0] * pktLen
        self.s2gaf           =   [0] * pktLen
        self.getgpa          =   [0] * pktLen

