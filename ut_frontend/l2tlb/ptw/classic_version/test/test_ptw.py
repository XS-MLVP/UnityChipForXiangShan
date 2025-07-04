import random

import toffee_test
from dut.PTW import DUTPTW

import toffee
from toffee import *


class PTWBundle(Bundle):
        
    clock, \
    reset, \
    io_sfence_valid, \
    io_csr_satp_mode, \
    io_csr_satp_asid, \
    io_csr_satp_ppn, \
    io_csr_satp_changed, \
    io_csr_vsatp_mode, \
    io_csr_vsatp_asid, \
    io_csr_vsatp_ppn, \
    io_csr_vsatp_changed, \
    io_csr_hgatp_mode, \
    io_csr_hgatp_vmid, \
    io_csr_hgatp_changed, \
    io_csr_priv_mxr, \
    io_csr_mPBMTE, \
    io_csr_hPBMTE, \
    io_req_ready, \
    io_req_valid, \
    io_req_bits_req_info_vpn, \
    io_req_bits_req_info_s2xlate, \
    io_req_bits_req_info_source, \
    io_req_bits_l3Hit, \
    io_req_bits_l2Hit, \
    io_req_bits_ppn, \
    io_req_bits_stage1Hit, \
    io_req_bits_stage1_entry_0_tag, \
    io_req_bits_stage1_entry_0_asid, \
    io_req_bits_stage1_entry_0_vmid, \
    io_req_bits_stage1_entry_0_n, \
    io_req_bits_stage1_entry_0_pbmt, \
    io_req_bits_stage1_entry_0_perm_d, \
    io_req_bits_stage1_entry_0_perm_a, \
    io_req_bits_stage1_entry_0_perm_g, \
    io_req_bits_stage1_entry_0_perm_u, \
    io_req_bits_stage1_entry_0_perm_x, \
    io_req_bits_stage1_entry_0_perm_w, \
    io_req_bits_stage1_entry_0_perm_r, \
    io_req_bits_stage1_entry_0_level, \
    io_req_bits_stage1_entry_0_v, \
    io_req_bits_stage1_entry_0_ppn, \
    io_req_bits_stage1_entry_0_ppn_low, \
    io_req_bits_stage1_entry_0_pf, \
    io_req_bits_stage1_entry_1_tag, \
    io_req_bits_stage1_entry_1_asid, \
    io_req_bits_stage1_entry_1_vmid, \
    io_req_bits_stage1_entry_1_n, \
    io_req_bits_stage1_entry_1_pbmt, \
    io_req_bits_stage1_entry_1_perm_d, \
    io_req_bits_stage1_entry_1_perm_a, \
    io_req_bits_stage1_entry_1_perm_g, \
    io_req_bits_stage1_entry_1_perm_u, \
    io_req_bits_stage1_entry_1_perm_x, \
    io_req_bits_stage1_entry_1_perm_w, \
    io_req_bits_stage1_entry_1_perm_r, \
    io_req_bits_stage1_entry_1_level, \
    io_req_bits_stage1_entry_1_v, \
    io_req_bits_stage1_entry_1_ppn, \
    io_req_bits_stage1_entry_1_ppn_low, \
    io_req_bits_stage1_entry_1_pf, \
    io_req_bits_stage1_entry_2_tag, \
    io_req_bits_stage1_entry_2_asid, \
    io_req_bits_stage1_entry_2_vmid, \
    io_req_bits_stage1_entry_2_n, \
    io_req_bits_stage1_entry_2_pbmt, \
    io_req_bits_stage1_entry_2_perm_d, \
    io_req_bits_stage1_entry_2_perm_a, \
    io_req_bits_stage1_entry_2_perm_g, \
    io_req_bits_stage1_entry_2_perm_u, \
    io_req_bits_stage1_entry_2_perm_x, \
    io_req_bits_stage1_entry_2_perm_w, \
    io_req_bits_stage1_entry_2_perm_r, \
    io_req_bits_stage1_entry_2_level, \
    io_req_bits_stage1_entry_2_v, \
    io_req_bits_stage1_entry_2_ppn, \
    io_req_bits_stage1_entry_2_ppn_low, \
    io_req_bits_stage1_entry_2_pf, \
    io_req_bits_stage1_entry_3_tag, \
    io_req_bits_stage1_entry_3_asid, \
    io_req_bits_stage1_entry_3_vmid, \
    io_req_bits_stage1_entry_3_n, \
    io_req_bits_stage1_entry_3_pbmt, \
    io_req_bits_stage1_entry_3_perm_d, \
    io_req_bits_stage1_entry_3_perm_a, \
    io_req_bits_stage1_entry_3_perm_g, \
    io_req_bits_stage1_entry_3_perm_u, \
    io_req_bits_stage1_entry_3_perm_x, \
    io_req_bits_stage1_entry_3_perm_w, \
    io_req_bits_stage1_entry_3_perm_r, \
    io_req_bits_stage1_entry_3_level, \
    io_req_bits_stage1_entry_3_v, \
    io_req_bits_stage1_entry_3_ppn, \
    io_req_bits_stage1_entry_3_ppn_low, \
    io_req_bits_stage1_entry_3_pf, \
    io_req_bits_stage1_entry_4_tag, \
    io_req_bits_stage1_entry_4_asid, \
    io_req_bits_stage1_entry_4_vmid, \
    io_req_bits_stage1_entry_4_n, \
    io_req_bits_stage1_entry_4_pbmt, \
    io_req_bits_stage1_entry_4_perm_d, \
    io_req_bits_stage1_entry_4_perm_a, \
    io_req_bits_stage1_entry_4_perm_g, \
    io_req_bits_stage1_entry_4_perm_u, \
    io_req_bits_stage1_entry_4_perm_x, \
    io_req_bits_stage1_entry_4_perm_w, \
    io_req_bits_stage1_entry_4_perm_r, \
    io_req_bits_stage1_entry_4_level, \
    io_req_bits_stage1_entry_4_v, \
    io_req_bits_stage1_entry_4_ppn, \
    io_req_bits_stage1_entry_4_ppn_low, \
    io_req_bits_stage1_entry_4_pf, \
    io_req_bits_stage1_entry_5_tag, \
    io_req_bits_stage1_entry_5_asid, \
    io_req_bits_stage1_entry_5_vmid, \
    io_req_bits_stage1_entry_5_n, \
    io_req_bits_stage1_entry_5_pbmt, \
    io_req_bits_stage1_entry_5_perm_d, \
    io_req_bits_stage1_entry_5_perm_a, \
    io_req_bits_stage1_entry_5_perm_g, \
    io_req_bits_stage1_entry_5_perm_u, \
    io_req_bits_stage1_entry_5_perm_x, \
    io_req_bits_stage1_entry_5_perm_w, \
    io_req_bits_stage1_entry_5_perm_r, \
    io_req_bits_stage1_entry_5_level, \
    io_req_bits_stage1_entry_5_v, \
    io_req_bits_stage1_entry_5_ppn, \
    io_req_bits_stage1_entry_5_ppn_low, \
    io_req_bits_stage1_entry_5_pf, \
    io_req_bits_stage1_entry_6_tag, \
    io_req_bits_stage1_entry_6_asid, \
    io_req_bits_stage1_entry_6_vmid, \
    io_req_bits_stage1_entry_6_n, \
    io_req_bits_stage1_entry_6_pbmt, \
    io_req_bits_stage1_entry_6_perm_d, \
    io_req_bits_stage1_entry_6_perm_a, \
    io_req_bits_stage1_entry_6_perm_g, \
    io_req_bits_stage1_entry_6_perm_u, \
    io_req_bits_stage1_entry_6_perm_x, \
    io_req_bits_stage1_entry_6_perm_w, \
    io_req_bits_stage1_entry_6_perm_r, \
    io_req_bits_stage1_entry_6_level, \
    io_req_bits_stage1_entry_6_v, \
    io_req_bits_stage1_entry_6_ppn, \
    io_req_bits_stage1_entry_6_ppn_low, \
    io_req_bits_stage1_entry_6_pf, \
    io_req_bits_stage1_entry_7_tag, \
    io_req_bits_stage1_entry_7_asid, \
    io_req_bits_stage1_entry_7_vmid, \
    io_req_bits_stage1_entry_7_n, \
    io_req_bits_stage1_entry_7_pbmt, \
    io_req_bits_stage1_entry_7_perm_d, \
    io_req_bits_stage1_entry_7_perm_a, \
    io_req_bits_stage1_entry_7_perm_g, \
    io_req_bits_stage1_entry_7_perm_u, \
    io_req_bits_stage1_entry_7_perm_x, \
    io_req_bits_stage1_entry_7_perm_w, \
    io_req_bits_stage1_entry_7_perm_r, \
    io_req_bits_stage1_entry_7_level, \
    io_req_bits_stage1_entry_7_v, \
    io_req_bits_stage1_entry_7_ppn, \
    io_req_bits_stage1_entry_7_ppn_low, \
    io_req_bits_stage1_entry_7_pf, \
    io_req_bits_stage1_pteidx_0, \
    io_req_bits_stage1_pteidx_1, \
    io_req_bits_stage1_pteidx_2, \
    io_req_bits_stage1_pteidx_3, \
    io_req_bits_stage1_pteidx_4, \
    io_req_bits_stage1_pteidx_5, \
    io_req_bits_stage1_pteidx_6, \
    io_req_bits_stage1_pteidx_7, \
    io_req_bits_stage1_not_super, \
    io_resp_ready, \
    io_resp_valid, \
    io_resp_bits_source, \
    io_resp_bits_s2xlate, \
    io_resp_bits_resp_entry_0_tag, \
    io_resp_bits_resp_entry_0_asid, \
    io_resp_bits_resp_entry_0_vmid, \
    io_resp_bits_resp_entry_0_n, \
    io_resp_bits_resp_entry_0_pbmt, \
    io_resp_bits_resp_entry_0_perm_d, \
    io_resp_bits_resp_entry_0_perm_a, \
    io_resp_bits_resp_entry_0_perm_g, \
    io_resp_bits_resp_entry_0_perm_u, \
    io_resp_bits_resp_entry_0_perm_x, \
    io_resp_bits_resp_entry_0_perm_w, \
    io_resp_bits_resp_entry_0_perm_r, \
    io_resp_bits_resp_entry_0_level, \
    io_resp_bits_resp_entry_0_v, \
    io_resp_bits_resp_entry_0_ppn, \
    io_resp_bits_resp_entry_0_ppn_low, \
    io_resp_bits_resp_entry_0_af, \
    io_resp_bits_resp_entry_0_pf, \
    io_resp_bits_resp_entry_1_tag, \
    io_resp_bits_resp_entry_1_asid, \
    io_resp_bits_resp_entry_1_vmid, \
    io_resp_bits_resp_entry_1_n, \
    io_resp_bits_resp_entry_1_pbmt, \
    io_resp_bits_resp_entry_1_perm_d, \
    io_resp_bits_resp_entry_1_perm_a, \
    io_resp_bits_resp_entry_1_perm_g, \
    io_resp_bits_resp_entry_1_perm_u, \
    io_resp_bits_resp_entry_1_perm_x, \
    io_resp_bits_resp_entry_1_perm_w, \
    io_resp_bits_resp_entry_1_perm_r, \
    io_resp_bits_resp_entry_1_level, \
    io_resp_bits_resp_entry_1_v, \
    io_resp_bits_resp_entry_1_ppn, \
    io_resp_bits_resp_entry_1_ppn_low, \
    io_resp_bits_resp_entry_1_af, \
    io_resp_bits_resp_entry_1_pf, \
    io_resp_bits_resp_entry_2_tag, \
    io_resp_bits_resp_entry_2_asid, \
    io_resp_bits_resp_entry_2_vmid, \
    io_resp_bits_resp_entry_2_n, \
    io_resp_bits_resp_entry_2_pbmt, \
    io_resp_bits_resp_entry_2_perm_d, \
    io_resp_bits_resp_entry_2_perm_a, \
    io_resp_bits_resp_entry_2_perm_g, \
    io_resp_bits_resp_entry_2_perm_u, \
    io_resp_bits_resp_entry_2_perm_x, \
    io_resp_bits_resp_entry_2_perm_w, \
    io_resp_bits_resp_entry_2_perm_r, \
    io_resp_bits_resp_entry_2_level, \
    io_resp_bits_resp_entry_2_v, \
    io_resp_bits_resp_entry_2_ppn, \
    io_resp_bits_resp_entry_2_ppn_low, \
    io_resp_bits_resp_entry_2_af, \
    io_resp_bits_resp_entry_2_pf, \
    io_resp_bits_resp_entry_3_tag, \
    io_resp_bits_resp_entry_3_asid, \
    io_resp_bits_resp_entry_3_vmid, \
    io_resp_bits_resp_entry_3_n, \
    io_resp_bits_resp_entry_3_pbmt, \
    io_resp_bits_resp_entry_3_perm_d, \
    io_resp_bits_resp_entry_3_perm_a, \
    io_resp_bits_resp_entry_3_perm_g, \
    io_resp_bits_resp_entry_3_perm_u, \
    io_resp_bits_resp_entry_3_perm_x, \
    io_resp_bits_resp_entry_3_perm_w, \
    io_resp_bits_resp_entry_3_perm_r, \
    io_resp_bits_resp_entry_3_level, \
    io_resp_bits_resp_entry_3_v, \
    io_resp_bits_resp_entry_3_ppn, \
    io_resp_bits_resp_entry_3_ppn_low, \
    io_resp_bits_resp_entry_3_af, \
    io_resp_bits_resp_entry_3_pf, \
    io_resp_bits_resp_entry_4_tag, \
    io_resp_bits_resp_entry_4_asid, \
    io_resp_bits_resp_entry_4_vmid, \
    io_resp_bits_resp_entry_4_n, \
    io_resp_bits_resp_entry_4_pbmt, \
    io_resp_bits_resp_entry_4_perm_d, \
    io_resp_bits_resp_entry_4_perm_a, \
    io_resp_bits_resp_entry_4_perm_g, \
    io_resp_bits_resp_entry_4_perm_u, \
    io_resp_bits_resp_entry_4_perm_x, \
    io_resp_bits_resp_entry_4_perm_w, \
    io_resp_bits_resp_entry_4_perm_r, \
    io_resp_bits_resp_entry_4_level, \
    io_resp_bits_resp_entry_4_v, \
    io_resp_bits_resp_entry_4_ppn, \
    io_resp_bits_resp_entry_4_ppn_low, \
    io_resp_bits_resp_entry_4_af, \
    io_resp_bits_resp_entry_4_pf, \
    io_resp_bits_resp_entry_5_tag, \
    io_resp_bits_resp_entry_5_asid, \
    io_resp_bits_resp_entry_5_vmid, \
    io_resp_bits_resp_entry_5_n, \
    io_resp_bits_resp_entry_5_pbmt, \
    io_resp_bits_resp_entry_5_perm_d, \
    io_resp_bits_resp_entry_5_perm_a, \
    io_resp_bits_resp_entry_5_perm_g, \
    io_resp_bits_resp_entry_5_perm_u, \
    io_resp_bits_resp_entry_5_perm_x, \
    io_resp_bits_resp_entry_5_perm_w, \
    io_resp_bits_resp_entry_5_perm_r, \
    io_resp_bits_resp_entry_5_level, \
    io_resp_bits_resp_entry_5_v, \
    io_resp_bits_resp_entry_5_ppn, \
    io_resp_bits_resp_entry_5_ppn_low, \
    io_resp_bits_resp_entry_5_af, \
    io_resp_bits_resp_entry_5_pf, \
    io_resp_bits_resp_entry_6_tag, \
    io_resp_bits_resp_entry_6_asid, \
    io_resp_bits_resp_entry_6_vmid, \
    io_resp_bits_resp_entry_6_n, \
    io_resp_bits_resp_entry_6_pbmt, \
    io_resp_bits_resp_entry_6_perm_d, \
    io_resp_bits_resp_entry_6_perm_a, \
    io_resp_bits_resp_entry_6_perm_g, \
    io_resp_bits_resp_entry_6_perm_u, \
    io_resp_bits_resp_entry_6_perm_x, \
    io_resp_bits_resp_entry_6_perm_w, \
    io_resp_bits_resp_entry_6_perm_r, \
    io_resp_bits_resp_entry_6_level, \
    io_resp_bits_resp_entry_6_v, \
    io_resp_bits_resp_entry_6_ppn, \
    io_resp_bits_resp_entry_6_ppn_low, \
    io_resp_bits_resp_entry_6_af, \
    io_resp_bits_resp_entry_6_pf, \
    io_resp_bits_resp_entry_7_tag, \
    io_resp_bits_resp_entry_7_asid, \
    io_resp_bits_resp_entry_7_vmid, \
    io_resp_bits_resp_entry_7_n, \
    io_resp_bits_resp_entry_7_pbmt, \
    io_resp_bits_resp_entry_7_perm_d, \
    io_resp_bits_resp_entry_7_perm_a, \
    io_resp_bits_resp_entry_7_perm_g, \
    io_resp_bits_resp_entry_7_perm_u, \
    io_resp_bits_resp_entry_7_perm_x, \
    io_resp_bits_resp_entry_7_perm_w, \
    io_resp_bits_resp_entry_7_perm_r, \
    io_resp_bits_resp_entry_7_level, \
    io_resp_bits_resp_entry_7_v, \
    io_resp_bits_resp_entry_7_ppn, \
    io_resp_bits_resp_entry_7_ppn_low, \
    io_resp_bits_resp_entry_7_af, \
    io_resp_bits_resp_entry_7_pf, \
    io_resp_bits_resp_pteidx_0, \
    io_resp_bits_resp_pteidx_1, \
    io_resp_bits_resp_pteidx_2, \
    io_resp_bits_resp_pteidx_3, \
    io_resp_bits_resp_pteidx_4, \
    io_resp_bits_resp_pteidx_5, \
    io_resp_bits_resp_pteidx_6, \
    io_resp_bits_resp_pteidx_7, \
    io_resp_bits_resp_not_super, \
    io_resp_bits_h_resp_entry_tag, \
    io_resp_bits_h_resp_entry_vmid, \
    io_resp_bits_h_resp_entry_n, \
    io_resp_bits_h_resp_entry_pbmt, \
    io_resp_bits_h_resp_entry_ppn, \
    io_resp_bits_h_resp_entry_perm_d, \
    io_resp_bits_h_resp_entry_perm_a, \
    io_resp_bits_h_resp_entry_perm_g, \
    io_resp_bits_h_resp_entry_perm_u, \
    io_resp_bits_h_resp_entry_perm_x, \
    io_resp_bits_h_resp_entry_perm_w, \
    io_resp_bits_h_resp_entry_perm_r, \
    io_resp_bits_h_resp_entry_level, \
    io_resp_bits_h_resp_gpf, \
    io_resp_bits_h_resp_gaf, \
    io_llptw_ready, \
    io_llptw_valid, \
    io_llptw_bits_req_info_vpn, \
    io_llptw_bits_req_info_s2xlate, \
    io_llptw_bits_req_info_source, \
    io_hptw_req_ready, \
    io_hptw_req_valid, \
    io_hptw_req_bits_source, \
    io_hptw_req_bits_gvpn, \
    io_hptw_resp_valid, \
    io_hptw_resp_bits_h_resp_entry_tag, \
    io_hptw_resp_bits_h_resp_entry_vmid, \
    io_hptw_resp_bits_h_resp_entry_n, \
    io_hptw_resp_bits_h_resp_entry_pbmt, \
    io_hptw_resp_bits_h_resp_entry_ppn, \
    io_hptw_resp_bits_h_resp_entry_perm_d, \
    io_hptw_resp_bits_h_resp_entry_perm_a, \
    io_hptw_resp_bits_h_resp_entry_perm_g, \
    io_hptw_resp_bits_h_resp_entry_perm_u, \
    io_hptw_resp_bits_h_resp_entry_perm_x, \
    io_hptw_resp_bits_h_resp_entry_perm_w, \
    io_hptw_resp_bits_h_resp_entry_perm_r, \
    io_hptw_resp_bits_h_resp_entry_level, \
    io_hptw_resp_bits_h_resp_gpf, \
    io_hptw_resp_bits_h_resp_gaf, \
    io_mem_req_ready, \
    io_mem_req_valid, \
    io_mem_req_bits_addr, \
    io_mem_resp_valid, \
    io_mem_resp_bits, \
    io_mem_mask, \
    io_pmp_req_bits_addr, \
    io_pmp_resp_ld, \
    io_pmp_resp_mmio, \
    io_refill_req_info_vpn, \
    io_refill_req_info_s2xlate, \
    io_refill_req_info_source, \
    io_refill_level, \
    io_perf_0_value, \
    io_perf_1_value, \
    io_perf_2_value, \
    io_perf_3_value, \
    io_perf_4_value, \
    io_perf_5_value, \
    io_perf_6_value = Signals(388)
  



@toffee_test.testcase
async def test_ptw_reset(toffee_request: toffee_test.ToffeeRequest):

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



@toffee_test.testcase
async def test_ptw_ptwcache_req_sv39_l2l1miss_nos2xlate_smoke(toffee_request: toffee_test.ToffeeRequest):

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
    ptw_bundle.io_req_bits_l2Hit.value = 0
    ptw_bundle.io_req_bits_ppn.value = 0
    ptw_bundle.io_req_bits_stage1Hit = 0

    await ptw_bundle.step(1)
    ### valid last 1 cycle
    ptw_bundle.io_req_valid.value = 0
    await ptw_bundle.step(1)
    # pmp checks at this cycle?
    await ptw_bundle.step(1)


    # after 2 cycle, ptw should request memory to get l2 pte
    assert 1 == ptw_bundle.io_mem_req_valid.value

    #               9-b bit | 9-bit    |   9-bit
    # vpn=0x80200,        1000 0000 0010 0000 0000
    #                 vpn[2]|vpn[1]    |vpn[0]
    # vpn[2] = 10b
    #
    # satp.ppn = 0x500, pte entry len = 8 byte
    # l2 pte paddr = 0x500 000 + 10b << 3  = 0x500010
    assert 0x500010 == ptw_bundle.io_mem_req_bits_addr.value


    # memory access takes many cycles, e.g. 10+ cycles
    # but first, set ready to 0, indicating io_mem_ interface now is busy
    ptw_bundle.io_mem_req_ready.value = 0
    await ptw_bundle.step(11)


    ptw_bundle.io_mem_resp_valid.value = 1

    #  63 62-61 60 - 54  53 - 10 9-8 7 - 0
    #  N  PBMT  Reserved   PPN   RSW DAGUXWRV
    #  0  0     0         0x400             1        no XWR, indicating it points to the next level
    #                10000000000 0000000001
    ptw_bundle.io_mem_resp_bits.value = 0x100001

    await ptw_bundle.step(1)
    ptw_bundle.io_mem_resp_valid.value = 0
    ptw_bundle.io_mem_req_ready.value = 1
    await ptw_bundle.step(1)
    # pmp
    await ptw_bundle.step(1)
    
    # ptw now do l1 pte
    assert 1 == ptw_bundle.io_mem_req_valid.value

    #               9-b bit | 9-bit    |   9-bit
    # vpn=0x80200,        1000 0000 0010 0000 0000
    #                 vpn[2]|vpn[1]    |vpn[0]
    # vpn[1] = 1b
    #
    # pte.ppn = 0x400, pte entry len = 8 byte
    # l1 pte paddr = 0x400 000 + 1b << 3  = 0x400008
    assert 0x400008 == ptw_bundle.io_mem_req_bits_addr.value

    # memory access takes many cycles, e.g. 10+ cycles
    # but first, set ready to 0, indicating io_mem_ interface now is busy
    ptw_bundle.io_mem_req_ready.value = 0
    await ptw_bundle.step(11)

    ptw_bundle.io_mem_resp_valid.value = 1

    #  63 62-61 60 - 54  53 - 10 9-8 7 - 0
    #  N  PBMT  Reserved   PPN   RSW DAGUXWRV
    #  0  0     0         0x300             1       no XWR, indicating it points to the next level
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




