import random

import toffee_test
from dut.PTW import DUTPTW

import toffee
from toffee import *

from ..bundle.bundle import PTWBundle



@toffee_test.testcase
async def test_ptw_ptwcache_req_sv39_l2hit_nos2xlate(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    ptw = toffee_request.create_dut(DUTPTW, "clock")
    toffee.start_clock(ptw)

    ptw_bundle = PTWBundle()
    ptw_bundle.bind(ptw)



    #
    # reset dut
    #

    #ptw_bundle['reset'].value = 1
    ptw_bundle.reset.value = 1
    await ptw_bundle.step(10)
    ptw_bundle.reset.value = 0
    await ptw_bundle.step(1)

    assert 1 == ptw_bundle.io_req_ready.value


    ###
    ptw_bundle.io_llptw_ready.value = 1
    ptw_bundle.io_hptw_req_ready.value = 1
    ptw_bundle.io_mem_req_ready.value = 1
    ptw_bundle.io_resp_ready.value = 1
    ###

    ptw_bundle.io_sfence_valid.value = 0

    # satp.mode [63:60] 0:Bare, 1-7:Reserved, 8:Sv39, 9:Sv48, 10:Sv57, 11:Sv64, 12-15:Reserved
    # satp.asid [59:44]
    # satp.ppn  [43:0]  paddr >> 12
    ptw_bundle.io_csr_satp_mode.value = 8   # Sv39
    ptw_bundle.io_csr_satp_asid.value = 0
    ptw_bundle.io_csr_satp_ppn.value = 0x500
    ptw_bundle.io_csr_satp_changed.value = 0

    ptw_bundle.io_csr_vsatp_mode.value = 0
    ptw_bundle.io_csr_vsatp_asid.value = 0
    ptw_bundle.io_csr_vsatp_ppn.value = 0
    ptw_bundle.io_csr_vsatp_changed.value = 0

    ptw_bundle.io_csr_hgatp_mode.value = 0
    ptw_bundle.io_csr_hgatp_vmid.value = 0
    ptw_bundle.io_csr_hgatp_changed.value = 0
    
    # mstatus.mxr
    # The MXR (Make eXecutable Readable) bit modifies the privilege with which loads access virtual memory.
    # When MXR=0, only loads from pages marked readable (R=1 in Figure 67) will succeed.
    # When MXR=1, loads from pages marked either readable or executable (R=1 or X=1) will succeed.
    ptw_bundle.io_csr_priv_mxr.value = 0 

    # PBMT enable
    # When PBMTE=0, the implementation behaves as though Svpbmt were not implemented. 
    # If Svpbmt is not implemented, PBMTE is readonly zero. 
    # Furthermore, for implementations with the hypervisor extension, 
    # henvcfg.PBMTE is read-only zero if menvcfg.PBMTE is zero.
    ptw_bundle.io_csr_mPBMTE.value = 0
    ptw_bundle.io_csr_hPBMTE.value = 0

    ptw_bundle.io_req_valid.value = 1

    ptw_bundle.io_req_bits_req_info_vpn.value = 0x80200
    # 00 noS2xlate, 01 onlyStage1, 10 onlyStage2, 11 allStage
    ptw_bundle.io_req_bits_req_info_s2xlate.value = 0x00
    # ptw:1, miss queue:   , prefetch:2  ??
    ptw_bundle.io_req_bits_req_info_source.value = 1

    # l3(Sv48) -> l2 -> l1 -> l0, l0 is the leaf node
    ptw_bundle.io_req_bits_l3Hit.value = 0
    ptw_bundle.io_req_bits_l2Hit.value = 1
    ptw_bundle.io_req_bits_ppn.value = 0x400
    ptw_bundle.io_req_bits_stage1Hit = 0

    await ptw_bundle.step(1)
    ### valid last 1 cycle
    ptw_bundle.io_req_valid.value = 0
    await ptw_bundle.step(1)
    # pmp checks at this cycle?
    await ptw_bundle.step(1)


    # after 2 cycle, ptw should request memory to get l1 pte
    assert 1 == ptw_bundle.io_mem_req_valid.value

    #               9-b bit | 9-bit    |   9-bit
    # vpn=0x80200,        1000 0000 0010 0000 0000
    #                 vpn[2]|vpn[1]    |vpn[0]
    # vpn[2] = 10b
    #
    # ppn = 0x400, pte entry len = 8 byte
    # l1 pte paddr = 0x400 000 + 1b << 3  = 0x400008
    assert 0x400008 == ptw_bundle.io_mem_req_bits_addr.value


    # memory access takes many cycles, e.g. 10+ cycles
    # but first, set ready to 0, indicating io_mem_ interface now is busy
    ptw_bundle.io_mem_req_ready.value = 0
    await ptw_bundle.step(11)


    ptw_bundle.io_mem_resp_valid.value = 1

    #  63 62-61 60 - 54  53 - 10 9-8 7 - 0
    #  N  PBMT  Reserved   PPN   RSW DAGUXWRV
    #  0  0     0         0x300             1        no XWR, indicating it points to the next level
    #                 1100000000 0000000001
    ptw_bundle.io_mem_resp_bits.value = 0xc0001

    await ptw_bundle.step(1)
    ptw_bundle.io_mem_resp_valid.value = 0
    ptw_bundle.io_mem_req_ready.value = 1
    await ptw_bundle.step(1)

    assert 1 == ptw_bundle.io_llptw_valid.value
    # after l2, l2, ptw should not request memory again
    assert 0 == ptw_bundle.io_mem_req_valid.value




@toffee_test.testcase
async def test_ptw_ptwcache_req_sv39_l2hit_nos2xlate_2mbpage(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    ptw = toffee_request.create_dut(DUTPTW, "clock")
    toffee.start_clock(ptw)

    ptw_bundle = PTWBundle()
    ptw_bundle.bind(ptw)



    #
    # reset dut
    #

    #ptw_bundle['reset'].value = 1
    ptw_bundle.reset.value = 1
    await ptw_bundle.step(10)
    ptw_bundle.reset.value = 0
    await ptw_bundle.step(1)

    assert 1 == ptw_bundle.io_req_ready.value


    ###
    ptw_bundle.io_llptw_ready.value = 1
    ptw_bundle.io_hptw_req_ready.value = 1
    ptw_bundle.io_mem_req_ready.value = 1
    ptw_bundle.io_resp_ready.value = 1
    ###

    ptw_bundle.io_sfence_valid.value = 0

    # satp.mode [63:60] 0:Bare, 1-7:Reserved, 8:Sv39, 9:Sv48, 10:Sv57, 11:Sv64, 12-15:Reserved
    # satp.asid [59:44]
    # satp.ppn  [43:0]  paddr >> 12
    ptw_bundle.io_csr_satp_mode.value = 8   # Sv39
    ptw_bundle.io_csr_satp_asid.value = 0
    ptw_bundle.io_csr_satp_ppn.value = 0x500
    ptw_bundle.io_csr_satp_changed.value = 0

    ptw_bundle.io_csr_vsatp_mode.value = 0
    ptw_bundle.io_csr_vsatp_asid.value = 0
    ptw_bundle.io_csr_vsatp_ppn.value = 0
    ptw_bundle.io_csr_vsatp_changed.value = 0

    ptw_bundle.io_csr_hgatp_mode.value = 0
    ptw_bundle.io_csr_hgatp_vmid.value = 0
    ptw_bundle.io_csr_hgatp_changed.value = 0
    
    # mstatus.mxr
    # The MXR (Make eXecutable Readable) bit modifies the privilege with which loads access virtual memory.
    # When MXR=0, only loads from pages marked readable (R=1 in Figure 67) will succeed.
    # When MXR=1, loads from pages marked either readable or executable (R=1 or X=1) will succeed.
    ptw_bundle.io_csr_priv_mxr.value = 0 

    # PBMT enable
    # When PBMTE=0, the implementation behaves as though Svpbmt were not implemented. 
    # If Svpbmt is not implemented, PBMTE is readonly zero. 
    # Furthermore, for implementations with the hypervisor extension, 
    # henvcfg.PBMTE is read-only zero if menvcfg.PBMTE is zero.
    ptw_bundle.io_csr_mPBMTE.value = 0
    ptw_bundle.io_csr_hPBMTE.value = 0

    ptw_bundle.io_req_valid.value = 1

    ptw_bundle.io_req_bits_req_info_vpn.value = 0x80200
    # 00 noS2xlate, 01 onlyStage1, 10 onlyStage2, 11 allStage
    ptw_bundle.io_req_bits_req_info_s2xlate.value = 0x00
    # ptw:1, miss queue:   , prefetch:2  ??
    ptw_bundle.io_req_bits_req_info_source.value = 1

    # l3(Sv48) -> l2 -> l1 -> l0, l0 is the leaf node
    ptw_bundle.io_req_bits_l3Hit.value = 0
    ptw_bundle.io_req_bits_l2Hit.value = 1
    ptw_bundle.io_req_bits_ppn.value = 0x400
    ptw_bundle.io_req_bits_stage1Hit = 0

    await ptw_bundle.step(1)
    ### valid last 1 cycle
    ptw_bundle.io_req_valid.value = 0
    await ptw_bundle.step(1)
    # pmp checks at this cycle?
    await ptw_bundle.step(1)


    # after 2 cycle, ptw should request memory to get l1 pte
    assert 1 == ptw_bundle.io_mem_req_valid.value

    #               9-b bit | 9-bit    |   9-bit
    # vpn=0x80200,        1000 0000 0010 0000 0000
    #                 vpn[2]|vpn[1]    |vpn[0]
    # vpn[2] = 10b
    #
    # ppn = 0x400, pte entry len = 8 byte
    # l1 pte paddr = 0x400 000 + 1b << 3  = 0x400008
    assert 0x400008 == ptw_bundle.io_mem_req_bits_addr.value


    # memory access takes many cycles, e.g. 10+ cycles
    # but first, set ready to 0, indicating io_mem_ interface now is busy
    ptw_bundle.io_mem_req_ready.value = 0
    await ptw_bundle.step(11)


    ptw_bundle.io_mem_resp_valid.value = 1

    #  63 62-61 60 - 54  53 - 10 9-8 7 - 0
    #  N  PBMT  Reserved   PPN   RSW DAGUXWRV
    #  0  0     0         0x200           111        WR, 2MB page
    #                 1000000000 0000000111
    ptw_bundle.io_mem_resp_bits.value = 0x80007

    await ptw_bundle.step(1)
    ptw_bundle.io_mem_resp_valid.value = 0
    ptw_bundle.io_mem_req_ready.value = 1
    await ptw_bundle.step(1)

    # Since this is a 2MB page, the PTW should skip querying LLPTW for the next-level PTE
    assert 0 == ptw_bundle.io_llptw_valid.value

    # after l2, ptw should not request memory again
    assert 0 == ptw_bundle.io_mem_req_valid.value


    # should finish current request 
    assert 1 == ptw_bundle.io_resp_valid.value
 
    # TLB coalescing is inactive for large pages. Defaulting to pte idx 0
    assert 1 == ptw_bundle.io_resp_bits_resp_pteidx_0.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_1.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_2.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_3.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_4.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_5.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_6.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_7.value

    assert 0 == ptw_bundle.io_resp_bits_resp_entry_0_pf.value

    # TLB coalescing is inactive for large pages.
    # pte ppn pte[53:10] 0x200 >> 3 = 0x40
    # resp ppn io_resp_bits_resp_entry_0_ppn[40:0] + io_resp_bits_resp_entry_0_ppn_low[2:0]
    assert 0x40 == ptw_bundle.io_resp_bits_resp_entry_0_ppn.value
    assert 0x0 == ptw_bundle.io_resp_bits_resp_entry_0_ppn_low.value

    assert 0 == ptw_bundle.io_resp_bits_resp_entry_0_perm_d.value
    assert 0 == ptw_bundle.io_resp_bits_resp_entry_0_perm_a.value
    assert 0 == ptw_bundle.io_resp_bits_resp_entry_0_perm_g.value
    assert 0 == ptw_bundle.io_resp_bits_resp_entry_0_perm_u.value
    assert 0 == ptw_bundle.io_resp_bits_resp_entry_0_perm_x.value
    assert 1 == ptw_bundle.io_resp_bits_resp_entry_0_perm_w.value
    assert 1 == ptw_bundle.io_resp_bits_resp_entry_0_perm_r.value



@toffee_test.testcase
async def test_ptw_ptwcache_req_sv39_l2hit_nos2xlate_2mbpage_ppn_misaligned(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    ptw = toffee_request.create_dut(DUTPTW, "clock")
    toffee.start_clock(ptw)

    ptw_bundle = PTWBundle()
    ptw_bundle.bind(ptw)



    #
    # reset dut
    #

    #ptw_bundle['reset'].value = 1
    ptw_bundle.reset.value = 1
    await ptw_bundle.step(10)
    ptw_bundle.reset.value = 0
    await ptw_bundle.step(1)

    assert 1 == ptw_bundle.io_req_ready.value


    ###
    ptw_bundle.io_llptw_ready.value = 1
    ptw_bundle.io_hptw_req_ready.value = 1
    ptw_bundle.io_mem_req_ready.value = 1
    ptw_bundle.io_resp_ready.value = 1
    ###

    ptw_bundle.io_sfence_valid.value = 0

    # satp.mode [63:60] 0:Bare, 1-7:Reserved, 8:Sv39, 9:Sv48, 10:Sv57, 11:Sv64, 12-15:Reserved
    # satp.asid [59:44]
    # satp.ppn  [43:0]  paddr >> 12
    ptw_bundle.io_csr_satp_mode.value = 8   # Sv39
    ptw_bundle.io_csr_satp_asid.value = 0
    ptw_bundle.io_csr_satp_ppn.value = 0x500
    ptw_bundle.io_csr_satp_changed.value = 0

    ptw_bundle.io_csr_vsatp_mode.value = 0
    ptw_bundle.io_csr_vsatp_asid.value = 0
    ptw_bundle.io_csr_vsatp_ppn.value = 0
    ptw_bundle.io_csr_vsatp_changed.value = 0

    ptw_bundle.io_csr_hgatp_mode.value = 0
    ptw_bundle.io_csr_hgatp_vmid.value = 0
    ptw_bundle.io_csr_hgatp_changed.value = 0
    
    # mstatus.mxr
    # The MXR (Make eXecutable Readable) bit modifies the privilege with which loads access virtual memory.
    # When MXR=0, only loads from pages marked readable (R=1 in Figure 67) will succeed.
    # When MXR=1, loads from pages marked either readable or executable (R=1 or X=1) will succeed.
    ptw_bundle.io_csr_priv_mxr.value = 0 

    # PBMT enable
    # When PBMTE=0, the implementation behaves as though Svpbmt were not implemented. 
    # If Svpbmt is not implemented, PBMTE is readonly zero. 
    # Furthermore, for implementations with the hypervisor extension, 
    # henvcfg.PBMTE is read-only zero if menvcfg.PBMTE is zero.
    ptw_bundle.io_csr_mPBMTE.value = 0
    ptw_bundle.io_csr_hPBMTE.value = 0

    ptw_bundle.io_req_valid.value = 1

    ptw_bundle.io_req_bits_req_info_vpn.value = 0x80200
    # 00 noS2xlate, 01 onlyStage1, 10 onlyStage2, 11 allStage
    ptw_bundle.io_req_bits_req_info_s2xlate.value = 0x00
    # ptw:1, miss queue:   , prefetch:2  ??
    ptw_bundle.io_req_bits_req_info_source.value = 1

    # l3(Sv48) -> l2 -> l1 -> l0, l0 is the leaf node
    ptw_bundle.io_req_bits_l3Hit.value = 0
    ptw_bundle.io_req_bits_l2Hit.value = 1
    ptw_bundle.io_req_bits_ppn.value = 0x400
    ptw_bundle.io_req_bits_stage1Hit = 0

    await ptw_bundle.step(1)
    ### valid last 1 cycle
    ptw_bundle.io_req_valid.value = 0
    await ptw_bundle.step(1)
    # pmp checks at this cycle?
    await ptw_bundle.step(1)


    # after 2 cycle, ptw should request memory to get l1 pte
    assert 1 == ptw_bundle.io_mem_req_valid.value

    #               9-b bit | 9-bit    |   9-bit
    # vpn=0x80200,        1000 0000 0010 0000 0000
    #                 vpn[2]|vpn[1]    |vpn[0]
    # vpn[2] = 10b
    #
    # ppn = 0x400, pte entry len = 8 byte
    # l1 pte paddr = 0x400 000 + 1b << 3  = 0x400008
    assert 0x400008 == ptw_bundle.io_mem_req_bits_addr.value


    # memory access takes many cycles, e.g. 10+ cycles
    # but first, set ready to 0, indicating io_mem_ interface now is busy
    ptw_bundle.io_mem_req_ready.value = 0
    await ptw_bundle.step(11)


    ptw_bundle.io_mem_resp_valid.value = 1

    #  63 62-61 60 - 54  53 - 10 9-8 7 - 0
    #  N  PBMT  Reserved   PPN   RSW DAGUXWRV
    #  0  0     0         0x200           111        WR, 2MB page
    #                 1100000000 0000000111
    ptw_bundle.io_mem_resp_bits.value = 0xc0007

    await ptw_bundle.step(1)
    ptw_bundle.io_mem_resp_valid.value = 0
    ptw_bundle.io_mem_req_ready.value = 1
    await ptw_bundle.step(1)

    # Since this is a 2MB page, the PTW should skip querying LLPTW for the next-level PTE
    assert 0 == ptw_bundle.io_llptw_valid.value

    # after l2, ptw should not request memory again
    assert 0 == ptw_bundle.io_mem_req_valid.value


    # should finish current request 
    assert 1 == ptw_bundle.io_resp_valid.value

    # TLB coalescing is inactive for large pages. Defaulting to pte idx 0
    assert 1 == ptw_bundle.io_resp_bits_resp_pteidx_0.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_1.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_2.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_3.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_4.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_5.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_6.value
    assert 0 == ptw_bundle.io_resp_bits_resp_pteidx_7.value

    # Page fault triggered: PPN 0x300 is not 2MB aligned.
    assert 1 == ptw_bundle.io_resp_bits_resp_entry_0_pf.value

    # pte ppn pte[53:10] 0x300 >> 3 = 0x60
    # resp ppn io_resp_bits_resp_entry_0_ppn[40:0] + io_resp_bits_resp_entry_0_ppn_low[2:0]
#    assert 0x60 == ptw_bundle.io_resp_bits_resp_entry_0_ppn.value
#    assert 0x0 == ptw_bundle.io_resp_bits_resp_entry_0_ppn_low.value

