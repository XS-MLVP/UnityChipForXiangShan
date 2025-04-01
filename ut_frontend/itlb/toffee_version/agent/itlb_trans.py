# Trans packet for tlb
class ItlbTransSfence():
    def __init__(self):
        self.sfenceBitsRs1 = 0
        self.sfenceBitsRs2 = 0
        self.sfenceBitsAddr = 0
        self.sfenceBitsId = 0
        self.sfenceBitsFlushPipe = 0
        self.sfenceBitsHv = 0
        self.sfenceBitsHg = 0

class ItlbTransCsr():
    def __init__(self):
        self.csrSatpMode = 0
        self.csrSatpAsid = 0
        self.csrSatpChanged = 0
        self.csrVsatpMode = 0
        self.csrVsatpAsid = 0
        self.csrVsatpChanged = 0
        self.csrHgatpMode = 0
        self.csrHgatpVmid = 0
        self.csrHgatpChanged = 0
        self.csrPrivVirt = 0
        self.csrPrivImode = 0

class ItlbTransRqstReq():
    def __init__(self):
        self.requestorReqBitsVaddr = 0

class ItlbTransRqstResp():
    def __init__(self):
        self.requestorRespBitsPaddr             =   0
        self.requestorRespBitsGpaddr            =   0
        self.requestorRespBitsPbmt              =   0
        self.requestorRespBitsMiss              =   0
        self.requestorRespBitsIsForVSnonLeafPTE =   0
        self.requestorRespBitsExcpGpfInstr      =   0
        self.requestorRespBitsExcpPfInstr       =   0
        self.requestorRespBitsExcpAfInstr       =   0

class ItlbTransFlsPipe():
    def __init__(self):
        self.flushPipe0 = 0
        self.flushPipe1 = 0
        self.flushPipe2 = 0
        
class ItlbTransPtwReq():
    def __init__(self):
        self.reqBitsVpn             =   0
        self.reqBitsS2Xlate         =   0
        self.reqBitsGetGpa          =   0
        
class ItlbTransPtwResp():
    def __init__(self):
        self.ptwrespbitss2xlate         =   0
        self.ptwrespbitss1entrytag      =   0
        self.ptwrespbitss1entryasid     =   0
        self.ptwrespbitss1entryvmid     =   0
        self.ptwrespbitss1entryn        =   0
        self.ptwrespbitss1entrypbmt     =   0
        self.ptwrespbitss1entrypermd    =   0
        self.ptwrespbitss1entryperma    =   0
        self.ptwrespbitss1entrypermg    =   0
        self.ptwrespbitss1entrypermu    =   0
        self.ptwrespbitss1entrypermx    =   0
        self.ptwrespbitss1entrypermw    =   0
        self.ptwrespbitss1entrypermr    =   0
        self.ptwrespbitss1entrylevel    =   0
        self.ptwrespbitss1entryv        =   0
        self.ptwrespbitss1entryppn      =   0
        self.ptwrespbitss1addrlow       =   0
        self.ptwrespbitss1ppnlow0       =   0
        self.ptwrespbitss1ppnlow1       =   0
        self.ptwrespbitss1ppnlow2       =   0
        self.ptwrespbitss1ppnlow3       =   0
        self.ptwrespbitss1ppnlow4       =   0
        self.ptwrespbitss1ppnlow5       =   0
        self.ptwrespbitss1ppnlow6       =   0
        self.ptwrespbitss1ppnlow7       =   0
        self.ptwrespbitss1valididx0     =   0
        self.ptwrespbitss1valididx1     =   0
        self.ptwrespbitss1valididx2     =   0
        self.ptwrespbitss1valididx3     =   0
        self.ptwrespbitss1valididx4     =   0
        self.ptwrespbitss1valididx5     =   0
        self.ptwrespbitss1valididx6     =   0
        self.ptwrespbitss1valididx7     =   0
        self.ptwrespbitss1pteidx0       =   0
        self.ptwrespbitss1pteidx1       =   0
        self.ptwrespbitss1pteidx2       =   0
        self.ptwrespbitss1pteidx3       =   0
        self.ptwrespbitss1pteidx4       =   0
        self.ptwrespbitss1pteidx5       =   0
        self.ptwrespbitss1pteidx6       =   0
        self.ptwrespbitss1pteidx7       =   0
        self.ptwrespbitss1pf            =   0
        self.ptwrespbitss1af            =   0
        self.ptwrespbitss2entrytag      =   0
        self.ptwrespbitss2entryvmid     =   0
        self.ptwrespbitss2entryn        =   0
        self.ptwrespbitss2entrypbmt     =   0
        self.ptwrespbitss2entryppn      =   0
        self.ptwrespbitss2entrypermd    =   0
        self.ptwrespbitss2entryperma    =   0
        self.ptwrespbitss2entrypermg    =   0
        self.ptwrespbitss2entrypermu    =   0
        self.ptwrespbitss2entrypermx    =   0
        self.ptwrespbitss2entrypermw    =   0
        self.ptwrespbitss2entrypermr    =   0
        self.ptwrespbitss2entrylevel    =   0
        self.ptwrespbitss2gpf           =   0
        self.ptwrespbitss2gaf           =   0
        self.ptwrespbitsgetgpa          =   0

        