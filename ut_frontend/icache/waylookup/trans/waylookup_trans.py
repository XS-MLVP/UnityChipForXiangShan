import random

class WayLookup_common_trans:    
    VSETIDX_W = 8
    WAYMASK_W = 4
    PTAG_W = 36
    ITLB_EXCEPTION_W = 2
    ITLB_PBMT_W = 2
    META_CODES_W = 1

    VSETIDX_MAX = (1 << VSETIDX_W) - 1
    WAYMASK_MAX = (1 << WAYMASK_W) - 1
    PTAG_MAX = (1 << PTAG_W) - 1
    ITLB_EXCEPTION_MAX = (1 << ITLB_EXCEPTION_W) - 1
    ITLB_PBMT_MAX = (1 << ITLB_PBMT_W) - 1
    META_CODES_MAX = (1 << META_CODES_W) - 1

    def __init__(self, vSetIdx=0, waymask=0, ptag=0, itlb_exception=0, itlb_pbmt=0, meta_codes=0):
        self.vSetIdx            = vSetIdx
        self.waymask            = waymask
        self.ptag               = ptag
        self.itlb_exception     = itlb_exception
        self.itlb_pbmt          = itlb_pbmt
        self.meta_codes         = meta_codes

    def _randomize_field(self, constraint_val, max_val):
        if constraint_val != -1:
            if constraint_val > max_val:
                raise ValueError(f"Constraint {constraint_val} exceeds max value {max_val}")
            return constraint_val
        else:
            return random.randint(0, max_val)


    def randomize(self, vSetIdx = -1, waymask = -1, ptag = -1, itlb_exception = -1, itlb_pbmt = -1, meta_codes = -1):
        self.vSetIdx            = self._randomize_field(vSetIdx, self.VSETIDX_MAX)
        self.waymask            = self._randomize_field(waymask, self.WAYMASK_MAX)
        self.ptag               = self._randomize_field(ptag, self.PTAG_MAX)
        self.itlb_exception     = self._randomize_field(itlb_exception, self.ITLB_EXCEPTION_MAX)
        self.itlb_pbmt          = self._randomize_field(itlb_pbmt, self.ITLB_PBMT_MAX)
        self.meta_codes         = self._randomize_field(meta_codes, self.META_CODES_MAX)

        return self

    def display(self, name='', displayer=print):
        displayer(f"{name}:\n vSetIdx:{self.vSetIdx}\n waymask:{self.waymask}\n ptag:{self.ptag}\n itlb_exception:{self.itlb_exception}\n itlb_pbmt:{self.itlb_pbmt}\n meta_codes:{self.meta_codes}\n")

    def set_from_dict(self, d):
        self.vSetIdx        = d['vSetIdx']
        self.waymask        = d['waymask']
        self.ptag           = d['ptag']
        self.itlb_exception = d['itlb_exception']
        self.itlb_pbmt      = d['itlb_pbmt']
        self.meta_codes     = d['meta_codes']

        return self

    def as_dict(self):
        trans_dict  = {}
        trans_dict['vSetIdx']           = self.vSetIdx
        trans_dict['waymask']           = self.waymask
        trans_dict['ptag']              = self.ptag
        trans_dict['itlb_exception']    = self.itlb_exception
        trans_dict['itlb_pbmt']         = self.itlb_pbmt
        trans_dict['meta_codes']        = self.meta_codes

        return trans_dict


    
class WayLookup_trans:
    
    GPF_GPADDR_W = 56
    GPF_ISFORV_W = 1
    
    GPF_GPADDR_MAX = (1 << GPF_GPADDR_W) - 1
    GPF_ISFORV_MAX = (1 << GPF_ISFORV_W) - 1
    
    def __init__(self):
        self.common0 = WayLookup_common_trans()
        self.common1 = WayLookup_common_trans()
        self.gpf_gpaddr = 0
        self.gpf_isForVSnonLeafPTE = 0    

    def _randomize_field(self, constraint_val, max_val):
        if constraint_val != -1:
            if constraint_val > max_val:
                raise ValueError(f"Constraint {constraint_val} exceeds max value {max_val}")
            return constraint_val
        else:
            return random.randint(0, max_val)

    def randomize(self, 
                vSetIdx_0           = -1, 
                waymask_0           = -1, 
                ptag_0              = -1, 
                itlb_exception_0    = -1, 
                itlb_pbmt_0         = -1, 
                meta_codes_0        = -1, 
                vSetIdx_1           = -1, 
                waymask_1           = -1, 
                ptag_1              = -1, 
                itlb_exception_1    = -1, 
                itlb_pbmt_1         = -1, 
                meta_codes_1        = -1,
                gpf_gpaddr = -1, gpf_isForVSnonLeafPTE = -1):

        self.common0.randomize(vSetIdx_0, waymask_0, ptag_0, itlb_exception_0, itlb_pbmt_0, meta_codes_0)
        self.common1.randomize(vSetIdx_1, waymask_1, ptag_1, itlb_exception_1, itlb_pbmt_1, meta_codes_1)

        self.gpf_gpaddr = self._randomize_field(gpf_gpaddr, self.GPF_GPADDR_MAX)
        self.gpf_isForVSnonLeafPTE = self._randomize_field(gpf_isForVSnonLeafPTE, self.GPF_ISFORV_MAX)

        return self


        
    def display(self, name='[WayLookUp Trans]', displayer=print):
        displayer(f"\n\n{name}:\n")        
        self.common0.display(name='entry0')
        self.common1.display(name='entry1')
        displayer(f"gpf:\n gpf_gpaddr:{self.gpf_gpaddr}\n gpf_isForVSnonLeafPTE:{self.gpf_isForVSnonLeafPTE}\n")

        
    def as_dict(self):

        trans_dict = {}

        common0_dict = self.common0.as_dict()
        for key, value in common0_dict.items():
            trans_dict[f"{key}_0"] = value

        common1_dict = self.common1.as_dict()
        for key, value in common1_dict.items():
            trans_dict[f"{key}_1"] = value
            
        trans_dict['gpf_gpaddr'] = self.gpf_gpaddr
        trans_dict['gpf_isForVSnonLeafPTE'] = self.gpf_isForVSnonLeafPTE
        
        return trans_dict


    def set_from_dict(self, d):

        common_keys = self.common0.as_dict().keys()
        
        common0_sub_dict = {}
        common1_sub_dict = {}

        for key in common_keys:
            common0_sub_dict[key] = d[f"{key}_0"]
            common1_sub_dict[key] = d[f"{key}_1"]
        
        self.common0.set_from_dict(common0_sub_dict)
        self.common1.set_from_dict(common1_sub_dict)

        self.gpf_gpaddr = d['gpf_gpaddr']
        self.gpf_isForVSnonLeafPTE = d['gpf_isForVSnonLeafPTE']

        return self




class WayLookup_update_trans:    
    BLKPADDR_W = 42
    VSETIDX_W = 8
    WAYMASK_W = 4
    CORRUPT_W = 1

    BLKPADDR_MAX = (1 << BLKPADDR_W) - 1
    VSETIDX_MAX = (1 << VSETIDX_W) - 1
    WAYMASK_MAX = (1 << WAYMASK_W) - 1
    CORRUPT_MAX = (1 << CORRUPT_W) - 1

    def __init__(self, blkPaddr=0, vSetIdx=0, waymask=0, corrupt=0):
        self.blkPaddr           = blkPaddr
        self.vSetIdx            = vSetIdx
        self.waymask            = waymask
        self.corrupt            = corrupt

    def _randomize_field(self, constraint_val, max_val):
        if constraint_val != -1:
            if constraint_val > max_val:
                raise ValueError(f"Constraint {constraint_val} exceeds max value {max_val}")
            return constraint_val
        else:
            return random.randint(0, max_val)


    def randomize(self, blkPaddr = -1, vSetIdx = -1, waymask = -1, corrupt = -1):
        self.blkPaddr           = self._randomize_field(blkPaddr, self.BLKPADDR_MAX)
        self.vSetIdx            = self._randomize_field(vSetIdx, self.VSETIDX_MAX)
        self.waymask            = self._randomize_field(waymask, self.WAYMASK_MAX)
        self.corrupt            = self._randomize_field(corrupt, self.CORRUPT_MAX)
        
        return self

    def display(self, name='[WayLookUp Update Trans]', displayer=print):
        displayer(f"\n\n{name}:\n blkPaddr:{self.blkPaddr}\n vSetIdx:{self.vSetIdx}\n waymask:{self.waymask}\n corrupt:{self.corrupt}\n")

    def set_from_dict(self, d):
        self.blkPaddr       = d['blkPaddr']
        self.vSetIdx        = d['vSetIdx']
        self.waymask        = d['waymask']
        self.corrupt        = d['corrupt']
        return self

    def as_dict(self):
        trans_dict  = {}
        trans_dict['blkPaddr']          = self.blkPaddr
        trans_dict['vSetIdx']           = self.vSetIdx
        trans_dict['waymask']           = self.waymask
        trans_dict['corrupt']           = self.corrupt
        return trans_dict
