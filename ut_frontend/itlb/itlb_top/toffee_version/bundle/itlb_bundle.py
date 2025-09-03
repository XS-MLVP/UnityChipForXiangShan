#coding=utf8
#***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
#**************************************************************************************/

from toffee.bundle import *

# Sfence Bundle
class SfenceSignalBundle(Bundle):
    '''
    Signals:

    rs1, rs2, addr, id, flushpipe, hv, hg
    '''
    rs1, rs2, addr, id, flushpipe, hv, hg = Signals(7)

class SfenceBundle(Bundle):
    '''
    Signals:

    valid, bits.{rs1, rs2, addr, id, flushpipe, hv, hg}
    '''
    valid = Signal()
    bits = SfenceSignalBundle.from_prefix('bits_')

# CSR Bundle
class CSRSatpBundle(Bundle):
    '''
    Signals:

    mode, asid, ppn, changed
    '''
    mode, asid, ppn, changed = Signals(4)
class CSRVsatpBundle(Bundle):
    '''
    Signals:

    mode, asid, ppn, changed
    '''
    mode, asid, ppn, changed = Signals(4)
class CSRHgatpBundle(Bundle):
    '''
    Signals:

    mode, vmid, ppn, changed
    '''
    mode, vmid, ppn, changed = Signals(4)
class CSRPrivBundle(Bundle):
    '''
    Signals:

    virt, imode
    '''
    virt, imode = Signals(2)

class CSRBundle(Bundle):
    '''
    Signals:

    satp.{mode, asid, ppn, changed},
    vsatp.{mode, asid, ppn, changed},
    hgatp.{mode, vmid, ppn, changed},
    priv.{virt, imode}
    '''
    satp = CSRSatpBundle.from_prefix('satp_')
    vsatp = CSRVsatpBundle.from_prefix('vsatp_')
    hgatp = CSRHgatpBundle.from_prefix('hgatp_')
    priv = CSRPrivBundle.from_prefix('priv_')

# Requestors Bundle
class RequestorReqBundle(Bundle):
    '''
    Signals:

    valid, ready, vaddr
    '''
    valid, ready, vaddr = Signals(3)

class RequestorRespBundle(Bundle):
    '''
    Signals:

    valid, ready, paddr, gpaddr, pbmt, miss, isForVSnonLeafPTE, gpf, pf, af
    '''
    valid, ready, paddr, gpaddr, pbmt, miss, isForVSnonLeafPTE, gpf, pf, af = Signals(10)

class RequestorSubBundle(Bundle):
    '''
    Signals:

    req.{valid, ready, vaddr},
    resp.{valid, ready, paddr, gpaddr, pbmt, miss, isForVSnonLeafPTE, gpf, pf, af}
    '''
    req = RequestorReqBundle.from_dict({
        'valid': 'valid',
        'ready': 'ready',
        'vaddr': 'bits_vaddr'
    })
    resp = RequestorRespBundle.from_dict({
        'valid': 'valid',
        'ready': 'ready',
        'paddr': 'paddr_0',
        'gpaddr': 'gpaddr_0',
        'pbmt': 'pbmt_0',
        'miss': 'miss',
        'isForVSnonLeafPTE': 'isForVSnonLeafPTE',
        'gpf': 'excp_0_gpf_instr',
        'pf': 'excp_0_pf_instr',
        'af': 'excp_0_af_instr'
    })

# PTW Bundle
class PTWReqSubBundle(Bundle):
    '''
    Signals:

    valid, vpn, s2xlate, getgpa
    '''
    valid, vpn, s2xlate, getgpa = Signals(4)

class PTWRespEntryPermBundle(Bundle):
    '''
    Signals:

    d, a, g, u, x, w, r
    '''
    d, a, g, u, x, w, r = Signals(7)

class PTWRespS1EntryBundle(Bundle):
    '''
    Signals:

    tag, asid, vmid, n, pbmt, level, v, ppn,
    perm.{d, a, g, u, x, w, r}
    '''
    tag, asid, vmid, n, pbmt, level, v, ppn = Signals(8)
    perm = PTWRespEntryPermBundle.from_prefix('perm_')

class PTWRespS1Bundle(Bundle):
    '''
    Signals:

    addr_low, pf, af,
    entry.{
        tag, asid, vmid, n, pbmt, level, v, ppn,
        perm.{d, a, g, u, x, w, r}
    },
    ppn_low[0, 1, 2, 3, 4, 5, 6, 7],
    valididx[0, 1, 2, 3, 4, 5, 6, 7],
    pteidx[0, 1, 2, 3, 4, 5, 6, 7]
    '''
    addr_low, pf, af = Signals(3)
    entry = PTWRespS1EntryBundle.from_prefix('entry_')
    ppn_low = SignalList("ppn_low_#", 8)
    valididx = SignalList("valididx_#", 8)
    pteidx = SignalList("pteidx_#", 8)

class PTWRespS2EntryBundle(Bundle):
    '''
    Signals:

    tag, vmid, n, pbmt, ppn, level,
    perm.{d, a, g, u, x, w, r}
    '''
    tag, vmid, n, pbmt, ppn, level = Signals(6)
    perm = PTWRespEntryPermBundle.from_prefix('perm_')

class PTWRespS2Bundle(Bundle):
    '''
    Signals:

    gpf, gaf,
    entry.{
        tag, vmid, n, pbmt, ppn, level,
        perm.{d, a, g, u, x, w, r}
    }
    '''
    gpf, gaf = Signals(2)
    entry = PTWRespS2EntryBundle.from_prefix('entry_')

class PTWRespBundle(Bundle):
    '''
    Signals:

    valid, s2xlate, getgpa,
    s1.{
        addr_low, pf, af,
        entry.{
            tag, asid, vmid, n, pbmt, level, v, ppn,
            perm.{d, a, g, u, x, w, r}
        },
        ppn_low[0, 1, 2, 3, 4, 5, 6, 7],
        valididx[0, 1, 2, 3, 4, 5, 6, 7],
        pteidx[0, 1, 2, 3, 4, 5, 6, 7]
    },
    s2.{
        gpf, gaf,
        entry.{
            tag, vmid, n, pbmt, ppn, level,
            perm.{d, a, g, u, x, w, r}
        }
    }
    '''
    valid, s2xlate, getgpa = Signals(3)
    s1 = PTWRespS1Bundle.from_prefix('bits_s1_')
    s2 = PTWRespS2Bundle.from_prefix('bits_s2_')

class PTWBundle(Bundle):
    '''
    Signals:

    req.{
        valid, vpn, s2xlate, getgpa
    }
    resp.{
        valid, s2xlate, getgpa,
        s1.{
            addr_low, pf, af,
            entry.{
                tag, asid, vmid, n, pbmt, level, v, ppn,
                perm.{d, a, g, u, x, w, r}
            },
            ppn_low[0, 1, 2, 3, 4, 5, 6, 7],
            valididx[0, 1, 2, 3, 4, 5, 6, 7],
            pteidx[0, 1, 2, 3, 4, 5, 6, 7]
        },
        s2.{
            gpf, gaf,
            entry.{
                tag, vmid, n, pbmt, ppn, level,
                perm.{d, a, g, u, x, w, r}
            }
        }
    }
    '''
    req = BundleList(PTWReqSubBundle, "req_#_", 3)
    resp = PTWRespBundle.from_prefix('resp_')

class TLBBundle(Bundle):
    '''
    Signals:

    hartid,
    sfence.{
        valid, bits.{rs1, rs2, addr, id, flushpipe, hv, hg}
    },
    csr.{
        satp.{mode, asid, ppn, changed},
        vsatp.{mode, asid, ppn, changed},
        hgatp.{mode, vmid, ppn, changed},
        priv.{virt, imode}
    },
    requestor[0, 1, 2].{
        req.{valid, ready*, vaddr},
        resp.{valid*, ready*, paddr, gpaddr, pbmt, miss, isForVSnonLeafPTE, gpf, pf, af}
    }(*: Only requestor[2]),
    flushpipe[0, 1, 2],
    ptw.{
        req.{
            valid, vpn, s2xlate, getgpa
        }
        resp.{
            valid, s2xlate, getgpa,
            s1.{
                addr_low, pf, af,
                entry.{
                    tag, asid, vmid, n, pbmt, level, v, ppn,
                    perm.{d, a, g, u, x, w, r}
                },
                ppn_low[0, 1, 2, 3, 4, 5, 6, 7],
                valididx[0, 1, 2, 3, 4, 5, 6, 7],
                pteidx[0, 1, 2, 3, 4, 5, 6, 7]
            },
            s2.{
                gpf, gaf,
                entry.{
                    tag, vmid, n, pbmt, ppn, level,
                    perm.{d, a, g, u, x, w, r}
                }
            }
        }
    }
    '''
    hartid = Signal()
    sfence = SfenceBundle.from_prefix('sfence_')
    csr = CSRBundle.from_prefix('csr_')
    requestor = BundleList(RequestorSubBundle, "requestor_#_", 3)
    flushpipe = SignalList("flushPipe_#", 3)
    ptw = PTWBundle.from_prefix('ptw_')