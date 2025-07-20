# PTW

## 测试目标

PTW (Page Table Walker) 模块用于L2TLB miss时遍历页表找到与指定virtual address对应的physical address。

对于sv39 (39位物理地址)模式，页表共有三级，分别是l2，l1，l0。其中l0是leaf pte，由LLPTW (Last Level Page Table Walker) 模块负责翻译。

`````verilog
module PTW(
  input         clock,
  input         reset,
  input         io_sfence_valid,
  input  [3:0]  io_csr_satp_mode,
  input  [15:0] io_csr_satp_asid,
  input  [43:0] io_csr_satp_ppn,
  input         io_csr_satp_changed,
  input  [3:0]  io_csr_vsatp_mode,
  input  [15:0] io_csr_vsatp_asid,
  input  [43:0] io_csr_vsatp_ppn,
  input         io_csr_vsatp_changed,
  input  [3:0]  io_csr_hgatp_mode,
  input  [15:0] io_csr_hgatp_vmid,
  input         io_csr_hgatp_changed,
  input         io_csr_priv_mxr,
  input         io_csr_mPBMTE,
  input         io_csr_hPBMTE,
  output        io_req_ready,
  input         io_req_valid,
  input  [37:0] io_req_bits_req_info_vpn,
  input  [1:0]  io_req_bits_req_info_s2xlate,
  input  [1:0]  io_req_bits_req_info_source,
  input         io_req_bits_l3Hit,
  input         io_req_bits_l2Hit,
  input  [43:0] io_req_bits_ppn,
  input         io_req_bits_stage1Hit,
  input  [34:0] io_req_bits_stage1_entry_0_tag,
  input  [15:0] io_req_bits_stage1_entry_0_asid,
  input  [13:0] io_req_bits_stage1_entry_0_vmid,
  input         io_req_bits_stage1_entry_0_n,
  input  [1:0]  io_req_bits_stage1_entry_0_pbmt,
  input         io_req_bits_stage1_entry_0_perm_d,
  input         io_req_bits_stage1_entry_0_perm_a,
  input         io_req_bits_stage1_entry_0_perm_g,
  input         io_req_bits_stage1_entry_0_perm_u,
  input         io_req_bits_stage1_entry_0_perm_x,
  input         io_req_bits_stage1_entry_0_perm_w,
  input         io_req_bits_stage1_entry_0_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_0_level,
  input         io_req_bits_stage1_entry_0_v,
  input  [40:0] io_req_bits_stage1_entry_0_ppn,
  input  [2:0]  io_req_bits_stage1_entry_0_ppn_low,
  input         io_req_bits_stage1_entry_0_pf,
  input  [34:0] io_req_bits_stage1_entry_1_tag,
  input  [15:0] io_req_bits_stage1_entry_1_asid,
  input  [13:0] io_req_bits_stage1_entry_1_vmid,
  input         io_req_bits_stage1_entry_1_n,
  input  [1:0]  io_req_bits_stage1_entry_1_pbmt,
  input         io_req_bits_stage1_entry_1_perm_d,
  input         io_req_bits_stage1_entry_1_perm_a,
  input         io_req_bits_stage1_entry_1_perm_g,
  input         io_req_bits_stage1_entry_1_perm_u,
  input         io_req_bits_stage1_entry_1_perm_x,
  input         io_req_bits_stage1_entry_1_perm_w,
  input         io_req_bits_stage1_entry_1_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_1_level,
  input         io_req_bits_stage1_entry_1_v,
  input  [40:0] io_req_bits_stage1_entry_1_ppn,
  input  [2:0]  io_req_bits_stage1_entry_1_ppn_low,
  input         io_req_bits_stage1_entry_1_pf,
  input  [34:0] io_req_bits_stage1_entry_2_tag,
  input  [15:0] io_req_bits_stage1_entry_2_asid,
  input  [13:0] io_req_bits_stage1_entry_2_vmid,
  input         io_req_bits_stage1_entry_2_n,
  input  [1:0]  io_req_bits_stage1_entry_2_pbmt,
  input         io_req_bits_stage1_entry_2_perm_d,
  input         io_req_bits_stage1_entry_2_perm_a,
  input         io_req_bits_stage1_entry_2_perm_g,
  input         io_req_bits_stage1_entry_2_perm_u,
  input         io_req_bits_stage1_entry_2_perm_x,
  input         io_req_bits_stage1_entry_2_perm_w,
  input         io_req_bits_stage1_entry_2_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_2_level,
  input         io_req_bits_stage1_entry_2_v,
  input  [40:0] io_req_bits_stage1_entry_2_ppn,
  input  [2:0]  io_req_bits_stage1_entry_2_ppn_low,
  input         io_req_bits_stage1_entry_2_pf,
  input  [34:0] io_req_bits_stage1_entry_3_tag,
  input  [15:0] io_req_bits_stage1_entry_3_asid,
  input  [13:0] io_req_bits_stage1_entry_3_vmid,
  input         io_req_bits_stage1_entry_3_n,
  input  [1:0]  io_req_bits_stage1_entry_3_pbmt,
  input         io_req_bits_stage1_entry_3_perm_d,
  input         io_req_bits_stage1_entry_3_perm_a,
  input         io_req_bits_stage1_entry_3_perm_g,
  input         io_req_bits_stage1_entry_3_perm_u,
  input         io_req_bits_stage1_entry_3_perm_x,
  input         io_req_bits_stage1_entry_3_perm_w,
  input         io_req_bits_stage1_entry_3_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_3_level,
  input         io_req_bits_stage1_entry_3_v,
  input  [40:0] io_req_bits_stage1_entry_3_ppn,
  input  [2:0]  io_req_bits_stage1_entry_3_ppn_low,
  input         io_req_bits_stage1_entry_3_pf,
  input  [34:0] io_req_bits_stage1_entry_4_tag,
  input  [15:0] io_req_bits_stage1_entry_4_asid,
  input  [13:0] io_req_bits_stage1_entry_4_vmid,
  input         io_req_bits_stage1_entry_4_n,
  input  [1:0]  io_req_bits_stage1_entry_4_pbmt,
  input         io_req_bits_stage1_entry_4_perm_d,
  input         io_req_bits_stage1_entry_4_perm_a,
  input         io_req_bits_stage1_entry_4_perm_g,
  input         io_req_bits_stage1_entry_4_perm_u,
  input         io_req_bits_stage1_entry_4_perm_x,
  input         io_req_bits_stage1_entry_4_perm_w,
  input         io_req_bits_stage1_entry_4_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_4_level,
  input         io_req_bits_stage1_entry_4_v,
  input  [40:0] io_req_bits_stage1_entry_4_ppn,
  input  [2:0]  io_req_bits_stage1_entry_4_ppn_low,
  input         io_req_bits_stage1_entry_4_pf,
  input  [34:0] io_req_bits_stage1_entry_5_tag,
  input  [15:0] io_req_bits_stage1_entry_5_asid,
  input  [13:0] io_req_bits_stage1_entry_5_vmid,
  input         io_req_bits_stage1_entry_5_n,
  input  [1:0]  io_req_bits_stage1_entry_5_pbmt,
  input         io_req_bits_stage1_entry_5_perm_d,
  input         io_req_bits_stage1_entry_5_perm_a,
  input         io_req_bits_stage1_entry_5_perm_g,
  input         io_req_bits_stage1_entry_5_perm_u,
  input         io_req_bits_stage1_entry_5_perm_x,
  input         io_req_bits_stage1_entry_5_perm_w,
  input         io_req_bits_stage1_entry_5_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_5_level,
  input         io_req_bits_stage1_entry_5_v,
  input  [40:0] io_req_bits_stage1_entry_5_ppn,
  input  [2:0]  io_req_bits_stage1_entry_5_ppn_low,
  input         io_req_bits_stage1_entry_5_pf,
  input  [34:0] io_req_bits_stage1_entry_6_tag,
  input  [15:0] io_req_bits_stage1_entry_6_asid,
  input  [13:0] io_req_bits_stage1_entry_6_vmid,
  input         io_req_bits_stage1_entry_6_n,
  input  [1:0]  io_req_bits_stage1_entry_6_pbmt,
  input         io_req_bits_stage1_entry_6_perm_d,
  input         io_req_bits_stage1_entry_6_perm_a,
  input         io_req_bits_stage1_entry_6_perm_g,
  input         io_req_bits_stage1_entry_6_perm_u,
  input         io_req_bits_stage1_entry_6_perm_x,
  input         io_req_bits_stage1_entry_6_perm_w,
  input         io_req_bits_stage1_entry_6_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_6_level,
  input         io_req_bits_stage1_entry_6_v,
  input  [40:0] io_req_bits_stage1_entry_6_ppn,
  input  [2:0]  io_req_bits_stage1_entry_6_ppn_low,
  input         io_req_bits_stage1_entry_6_pf,
  input  [34:0] io_req_bits_stage1_entry_7_tag,
  input  [15:0] io_req_bits_stage1_entry_7_asid,
  input  [13:0] io_req_bits_stage1_entry_7_vmid,
  input         io_req_bits_stage1_entry_7_n,
  input  [1:0]  io_req_bits_stage1_entry_7_pbmt,
  input         io_req_bits_stage1_entry_7_perm_d,
  input         io_req_bits_stage1_entry_7_perm_a,
  input         io_req_bits_stage1_entry_7_perm_g,
  input         io_req_bits_stage1_entry_7_perm_u,
  input         io_req_bits_stage1_entry_7_perm_x,
  input         io_req_bits_stage1_entry_7_perm_w,
  input         io_req_bits_stage1_entry_7_perm_r,
  input  [1:0]  io_req_bits_stage1_entry_7_level,
  input         io_req_bits_stage1_entry_7_v,
  input  [40:0] io_req_bits_stage1_entry_7_ppn,
  input  [2:0]  io_req_bits_stage1_entry_7_ppn_low,
  input         io_req_bits_stage1_entry_7_pf,
  input         io_req_bits_stage1_pteidx_0,
  input         io_req_bits_stage1_pteidx_1,
  input         io_req_bits_stage1_pteidx_2,
  input         io_req_bits_stage1_pteidx_3,
  input         io_req_bits_stage1_pteidx_4,
  input         io_req_bits_stage1_pteidx_5,
  input         io_req_bits_stage1_pteidx_6,
  input         io_req_bits_stage1_pteidx_7,
  input         io_req_bits_stage1_not_super,
  input         io_resp_ready,
  output        io_resp_valid,
  output [1:0]  io_resp_bits_source,
  output [1:0]  io_resp_bits_s2xlate,
  output [34:0] io_resp_bits_resp_entry_0_tag,
  output [15:0] io_resp_bits_resp_entry_0_asid,
  output [13:0] io_resp_bits_resp_entry_0_vmid,
  output        io_resp_bits_resp_entry_0_n,
  output [1:0]  io_resp_bits_resp_entry_0_pbmt,
  output        io_resp_bits_resp_entry_0_perm_d,
  output        io_resp_bits_resp_entry_0_perm_a,
  output        io_resp_bits_resp_entry_0_perm_g,
  output        io_resp_bits_resp_entry_0_perm_u,
  output        io_resp_bits_resp_entry_0_perm_x,
  output        io_resp_bits_resp_entry_0_perm_w,
  output        io_resp_bits_resp_entry_0_perm_r,
  output [1:0]  io_resp_bits_resp_entry_0_level,
  output        io_resp_bits_resp_entry_0_v,
  output [40:0] io_resp_bits_resp_entry_0_ppn,
  output [2:0]  io_resp_bits_resp_entry_0_ppn_low,
  output        io_resp_bits_resp_entry_0_af,
  output        io_resp_bits_resp_entry_0_pf,
  output [34:0] io_resp_bits_resp_entry_1_tag,
  output [15:0] io_resp_bits_resp_entry_1_asid,
  output [13:0] io_resp_bits_resp_entry_1_vmid,
  output        io_resp_bits_resp_entry_1_n,
  output [1:0]  io_resp_bits_resp_entry_1_pbmt,
  output        io_resp_bits_resp_entry_1_perm_d,
  output        io_resp_bits_resp_entry_1_perm_a,
  output        io_resp_bits_resp_entry_1_perm_g,
  output        io_resp_bits_resp_entry_1_perm_u,
  output        io_resp_bits_resp_entry_1_perm_x,
  output        io_resp_bits_resp_entry_1_perm_w,
  output        io_resp_bits_resp_entry_1_perm_r,
  output [1:0]  io_resp_bits_resp_entry_1_level,
  output        io_resp_bits_resp_entry_1_v,
  output [40:0] io_resp_bits_resp_entry_1_ppn,
  output [2:0]  io_resp_bits_resp_entry_1_ppn_low,
  output        io_resp_bits_resp_entry_1_af,
  output        io_resp_bits_resp_entry_1_pf,
  output [34:0] io_resp_bits_resp_entry_2_tag,
  output [15:0] io_resp_bits_resp_entry_2_asid,
  output [13:0] io_resp_bits_resp_entry_2_vmid,
  output        io_resp_bits_resp_entry_2_n,
  output [1:0]  io_resp_bits_resp_entry_2_pbmt,
  output        io_resp_bits_resp_entry_2_perm_d,
  output        io_resp_bits_resp_entry_2_perm_a,
  output        io_resp_bits_resp_entry_2_perm_g,
  output        io_resp_bits_resp_entry_2_perm_u,
  output        io_resp_bits_resp_entry_2_perm_x,
  output        io_resp_bits_resp_entry_2_perm_w,
  output        io_resp_bits_resp_entry_2_perm_r,
  output [1:0]  io_resp_bits_resp_entry_2_level,
  output        io_resp_bits_resp_entry_2_v,
  output [40:0] io_resp_bits_resp_entry_2_ppn,
  output [2:0]  io_resp_bits_resp_entry_2_ppn_low,
  output        io_resp_bits_resp_entry_2_af,
  output        io_resp_bits_resp_entry_2_pf,
  output [34:0] io_resp_bits_resp_entry_3_tag,
  output [15:0] io_resp_bits_resp_entry_3_asid,
  output [13:0] io_resp_bits_resp_entry_3_vmid,
  output        io_resp_bits_resp_entry_3_n,
  output [1:0]  io_resp_bits_resp_entry_3_pbmt,
  output        io_resp_bits_resp_entry_3_perm_d,
  output        io_resp_bits_resp_entry_3_perm_a,
  output        io_resp_bits_resp_entry_3_perm_g,
  output        io_resp_bits_resp_entry_3_perm_u,
  output        io_resp_bits_resp_entry_3_perm_x,
  output        io_resp_bits_resp_entry_3_perm_w,
  output        io_resp_bits_resp_entry_3_perm_r,
  output [1:0]  io_resp_bits_resp_entry_3_level,
  output        io_resp_bits_resp_entry_3_v,
  output [40:0] io_resp_bits_resp_entry_3_ppn,
  output [2:0]  io_resp_bits_resp_entry_3_ppn_low,
  output        io_resp_bits_resp_entry_3_af,
  output        io_resp_bits_resp_entry_3_pf,
  output [34:0] io_resp_bits_resp_entry_4_tag,
  output [15:0] io_resp_bits_resp_entry_4_asid,
  output [13:0] io_resp_bits_resp_entry_4_vmid,
  output        io_resp_bits_resp_entry_4_n,
  output [1:0]  io_resp_bits_resp_entry_4_pbmt,
  output        io_resp_bits_resp_entry_4_perm_d,
  output        io_resp_bits_resp_entry_4_perm_a,
  output        io_resp_bits_resp_entry_4_perm_g,
  output        io_resp_bits_resp_entry_4_perm_u,
  output        io_resp_bits_resp_entry_4_perm_x,
  output        io_resp_bits_resp_entry_4_perm_w,
  output        io_resp_bits_resp_entry_4_perm_r,
  output [1:0]  io_resp_bits_resp_entry_4_level,
  output        io_resp_bits_resp_entry_4_v,
  output [40:0] io_resp_bits_resp_entry_4_ppn,
  output [2:0]  io_resp_bits_resp_entry_4_ppn_low,
  output        io_resp_bits_resp_entry_4_af,
  output        io_resp_bits_resp_entry_4_pf,
  output [34:0] io_resp_bits_resp_entry_5_tag,
  output [15:0] io_resp_bits_resp_entry_5_asid,
  output [13:0] io_resp_bits_resp_entry_5_vmid,
  output        io_resp_bits_resp_entry_5_n,
  output [1:0]  io_resp_bits_resp_entry_5_pbmt,
  output        io_resp_bits_resp_entry_5_perm_d,
  output        io_resp_bits_resp_entry_5_perm_a,
  output        io_resp_bits_resp_entry_5_perm_g,
  output        io_resp_bits_resp_entry_5_perm_u,
  output        io_resp_bits_resp_entry_5_perm_x,
  output        io_resp_bits_resp_entry_5_perm_w,
  output        io_resp_bits_resp_entry_5_perm_r,
  output [1:0]  io_resp_bits_resp_entry_5_level,
  output        io_resp_bits_resp_entry_5_v,
  output [40:0] io_resp_bits_resp_entry_5_ppn,
  output [2:0]  io_resp_bits_resp_entry_5_ppn_low,
  output        io_resp_bits_resp_entry_5_af,
  output        io_resp_bits_resp_entry_5_pf,
  output [34:0] io_resp_bits_resp_entry_6_tag,
  output [15:0] io_resp_bits_resp_entry_6_asid,
  output [13:0] io_resp_bits_resp_entry_6_vmid,
  output        io_resp_bits_resp_entry_6_n,
  output [1:0]  io_resp_bits_resp_entry_6_pbmt,
  output        io_resp_bits_resp_entry_6_perm_d,
  output        io_resp_bits_resp_entry_6_perm_a,
  output        io_resp_bits_resp_entry_6_perm_g,
  output        io_resp_bits_resp_entry_6_perm_u,
  output        io_resp_bits_resp_entry_6_perm_x,
  output        io_resp_bits_resp_entry_6_perm_w,
  output        io_resp_bits_resp_entry_6_perm_r,
  output [1:0]  io_resp_bits_resp_entry_6_level,
  output        io_resp_bits_resp_entry_6_v,
  output [40:0] io_resp_bits_resp_entry_6_ppn,
  output [2:0]  io_resp_bits_resp_entry_6_ppn_low,
  output        io_resp_bits_resp_entry_6_af,
  output        io_resp_bits_resp_entry_6_pf,
  output [34:0] io_resp_bits_resp_entry_7_tag,
  output [15:0] io_resp_bits_resp_entry_7_asid,
  output [13:0] io_resp_bits_resp_entry_7_vmid,
  output        io_resp_bits_resp_entry_7_n,
  output [1:0]  io_resp_bits_resp_entry_7_pbmt,
  output        io_resp_bits_resp_entry_7_perm_d,
  output        io_resp_bits_resp_entry_7_perm_a,
  output        io_resp_bits_resp_entry_7_perm_g,
  output        io_resp_bits_resp_entry_7_perm_u,
  output        io_resp_bits_resp_entry_7_perm_x,
  output        io_resp_bits_resp_entry_7_perm_w,
  output        io_resp_bits_resp_entry_7_perm_r,
  output [1:0]  io_resp_bits_resp_entry_7_level,
  output        io_resp_bits_resp_entry_7_v,
  output [40:0] io_resp_bits_resp_entry_7_ppn,
  output [2:0]  io_resp_bits_resp_entry_7_ppn_low,
  output        io_resp_bits_resp_entry_7_af,
  output        io_resp_bits_resp_entry_7_pf,
  output        io_resp_bits_resp_pteidx_0,
  output        io_resp_bits_resp_pteidx_1,
  output        io_resp_bits_resp_pteidx_2,
  output        io_resp_bits_resp_pteidx_3,
  output        io_resp_bits_resp_pteidx_4,
  output        io_resp_bits_resp_pteidx_5,
  output        io_resp_bits_resp_pteidx_6,
  output        io_resp_bits_resp_pteidx_7,
  output        io_resp_bits_resp_not_super,
  output [37:0] io_resp_bits_h_resp_entry_tag,
  output [13:0] io_resp_bits_h_resp_entry_vmid,
  output        io_resp_bits_h_resp_entry_n,
  output [1:0]  io_resp_bits_h_resp_entry_pbmt,
  output [37:0] io_resp_bits_h_resp_entry_ppn,
  output        io_resp_bits_h_resp_entry_perm_d,
  output        io_resp_bits_h_resp_entry_perm_a,
  output        io_resp_bits_h_resp_entry_perm_g,
  output        io_resp_bits_h_resp_entry_perm_u,
  output        io_resp_bits_h_resp_entry_perm_x,
  output        io_resp_bits_h_resp_entry_perm_w,
  output        io_resp_bits_h_resp_entry_perm_r,
  output [1:0]  io_resp_bits_h_resp_entry_level,
  output        io_resp_bits_h_resp_gpf,
  output        io_resp_bits_h_resp_gaf,
  input         io_llptw_ready,
  output        io_llptw_valid,
  output [37:0] io_llptw_bits_req_info_vpn,
  output [1:0]  io_llptw_bits_req_info_s2xlate,
  output [1:0]  io_llptw_bits_req_info_source,
  input         io_hptw_req_ready,
  output        io_hptw_req_valid,
  output [1:0]  io_hptw_req_bits_source,
  output [43:0] io_hptw_req_bits_gvpn,
  input         io_hptw_resp_valid,
  input  [37:0] io_hptw_resp_bits_h_resp_entry_tag,
  input  [13:0] io_hptw_resp_bits_h_resp_entry_vmid,
  input         io_hptw_resp_bits_h_resp_entry_n,
  input  [1:0]  io_hptw_resp_bits_h_resp_entry_pbmt,
  input  [37:0] io_hptw_resp_bits_h_resp_entry_ppn,
  input         io_hptw_resp_bits_h_resp_entry_perm_d,
  input         io_hptw_resp_bits_h_resp_entry_perm_a,
  input         io_hptw_resp_bits_h_resp_entry_perm_g,
  input         io_hptw_resp_bits_h_resp_entry_perm_u,
  input         io_hptw_resp_bits_h_resp_entry_perm_x,
  input         io_hptw_resp_bits_h_resp_entry_perm_w,
  input         io_hptw_resp_bits_h_resp_entry_perm_r,
  input  [1:0]  io_hptw_resp_bits_h_resp_entry_level,
  input         io_hptw_resp_bits_h_resp_gpf,
  input         io_hptw_resp_bits_h_resp_gaf,
  input         io_mem_req_ready,
  output        io_mem_req_valid,
  output [47:0] io_mem_req_bits_addr,
  input         io_mem_resp_valid,
  input  [63:0] io_mem_resp_bits,
  input         io_mem_mask,
  output [47:0] io_pmp_req_bits_addr,
  input         io_pmp_resp_ld,
  input         io_pmp_resp_mmio,
  output [37:0] io_refill_req_info_vpn,
  output [1:0]  io_refill_req_info_s2xlate,
  output [1:0]  io_refill_req_info_source,
  output [1:0]  io_refill_level,
  output [5:0]  io_perf_0_value,
  output [5:0]  io_perf_1_value,
  output [5:0]  io_perf_2_value,
  output [5:0]  io_perf_3_value,
  output [5:0]  io_perf_4_value,
  output [5:0]  io_perf_5_value,
  output [5:0]  io_perf_6_value
);

`````

测试方法：模拟PTWCache向PTW发起页表查询请求。PTW收到请求后向内存接口发读数据请求。模拟内存返回数据，检测PTW是否继续下一级页表查询或向LLPTW发起最后一层页表请求。

## 测试环境

Ubuntu 24.04, 测试环境依赖g++, python3，verilator，xspcomm，picker，pytest，toffee，toffee-test。

## 功能检测

1. `test_ptw_reset`

   测试PTW设备重置

2. `test_ptw_ptwcache_req_sv39_l2l1miss_nos2xlate_smoke`

   sv39模式下l2 l1 miss, nos2xlate，测试PTW查询l2，l1两级页表后向LLPTW发出l0页表查询请求。

3. `test_ptw_ptwcache_req_sv39_l2miss_nos2xlate_1gbpage`

   sv39模式下l2, nos2xlate，测试PTW查询l2页表后，得到1GB页表项，向PTWCache返回结果。

4. `test_ptw_ptwcache_req_sv39_l2l1miss_nos2xlate_2mbpage`

   sv39模式下l2, nos2xlate，测试PTW查询l2，l1页表后，得到2MB页表项，向PTWCache返回结果。

5. `test_ptw_ptwcache_req_sv39_l2hit_nos2xlate`

   sv39模式下nos2xlate，l2 hit, 测试PTW查询l1页表后向LLPTW发出l0页表查询请求。

6. `test_ptw_ptwcache_req_sv39_l2hit_nos2xlate_2mbpage`

   sv39模式下nos2xlate，l2 hit, 测试PTW查询l1页表后，得到2MB页表项，向PTWCache返回结果。


## 用例说明

#### 测试用例1：test\_ptw\_reset

测试步骤

###### 1. reset

拉高reset信号10个时钟周期，再恢复reset到0。

检测

`````python
    assert 1 == ptw_bundle.io_req_ready.value
`````

值为1表示设备重置，可以接受请求。


#### 测试用例2： test\_ptw\_ptwcache\_req\_sv39\_l2l1miss\_nos2xlate\_smoke

测试步骤

###### 1. reset

拉高reset信号10个时钟周期，再恢复reset到0。

检测

`````python
    assert 1 == ptw_bundle.io_req_ready.value
`````

值为1表示设备重置，可以接受请求。


###### 2. 设置PTW工作模式

模拟csr.satp中，sv39，根页表物理页号为0x500。

csr.vsatp csr.hsatp均为0。


`````verilog

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
`````

###### 3. 模拟PTWCache发出页表查询请求

虚拟地址页号0x80200。

`````verilog
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
`````

检测PTW向内存接口发出读内存请求，内存地址是page table base所在页的一个page table entry。


`````verilog

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
`````

模拟内存接口11个cycle后返回内存数据，其中下一级页表的物理地址的页号是0x400。


`````verilog

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
`````

PTW接下来处理l1 page table，再次向内存接口发出读内存请求。

检测内存地址是0x400页中的一个page table entry。


`````verilog
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
`````

再次模拟内存接口返回内存数据。

`````verilog
    ptw_bundle.io_mem_resp_valid.value = 1

    #  63 62-61 60 - 54  53 - 10 9-8 7 - 0
    #  N  PBMT  Reserved   PPN   RSW DAGUXWRV
    #  0  0     0         0x300             1       no XWR, indicating it points to the next level
    #                 1100000000 0000000001
    ptw_bundle.io_mem_resp_bits.value = 0xc0001
`````

PTW取得l1 page table entry后，向LLPTW查询l0 page table entry。


`````verilog
    assert 1 == ptw_bundle.io_llptw_valid.value
    # after l2, l2, ptw should not request memory again
    assert 0 == ptw_bundle.io_mem_req_valid.value
`````



# How Has This Been Tested

`````shell
UnityChipForXiangShan$ make test target=ut_frontend/l2tlb/ptw/
`````

