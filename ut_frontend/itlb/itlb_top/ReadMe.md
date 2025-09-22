# **Translation Lookaside Buffer (TLB)**

## 信号总表

| 原始端口信号 | 信号方向 | 位宽 | 结构化Bundle路径 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| **时钟与复位** |  |  |  |  |
| `clock` | `input` | 1 | (未包含在Bundle中) | 全局时钟信号 |
| `reset` | `input` | 1 | (未包含在Bundle中) | 全局复位信号 |
| **Sfence（栅障）接口** |  |  | **`sfence`** |  |
| `io_sfence_valid` | `input` | 1 | `sfence.valid` | Sfence操作有效 |
| `io_sfence_bits_rs1` | `input` | 1 | `sfence.bits.rs1` |  |
| `io_sfence_bits_rs2` | `input` | 1 | `sfence.bits.rs2` |  |
| `io_sfence_bits_addr` | `input` | 50 | `sfence.bits.addr` | 目标虚拟地址 |
| `io_sfence_bits_id` | `input` | 16 | `sfence.bits.id` |  |
| `io_sfence_bits_flushPipe` | `input` | 1 | `sfence.bits.flushpipe` | 是否刷新流水线 |
| `io_sfence_bits_hv` | `input` | 1 | `sfence.bits.hv` |  |
| `io_sfence_bits_hg` | `input` | 1 | `sfence.bits.hg` |  |
| **CSR（控制与状态寄存器）接口** |  |  | **`csr`** |  |
| `io_csr_satp_mode` | `input` | 4 | `csr.satp.mode` | SATP寄存器模式位 |
| `io_csr_satp_asid` | `input` | 16 | `csr.satp.asid` | SATP寄存器ASID |
| `io_csr_satp_ppn` | `input` | 44 | `csr.satp.ppn` | SATP寄存器PPN |
| `io_csr_satp_changed` | `input` | 1 | `csr.satp.changed` | SATP寄存器发生改变 |
| `io_csr_vsatp_mode` | `input` | 4 | `csr.vsatp.mode` | VSATP寄存器模式位 |
| `io_csr_vsatp_asid` | `input` | 16 | `csr.vsatp.asid` | VSATP寄存器ASID |
| `io_csr_vsatp_ppn` | `input` | 44 | `csr.vsatp.ppn` | VSATP寄存器PPN |
| `io_csr_vsatp_changed` | `input` | 1 | `csr.vsatp.changed` | VSATP寄存器发生改变 |
| `io_csr_hgatp_mode` | `input` | 4 | `csr.hgatp.mode` | HGATP寄存器模式位 |
| `io_csr_hgatp_vmid` | `input` | 16 | `csr.hgatp.asid` | **不一致：端口为vmid，Bundle映射为asid** |
| `io_csr_hgatp_ppn` | `input` | 44 | `csr.hgatp.ppn` | HGATP寄存器PPN |
| `io_csr_hgatp_changed` | `input` | 1 | `csr.hgatp.changed` | HGATP寄存器发生改变 |
| `io_csr_priv_virt` | `input` | 1 | `csr.priv.virt` | 虚拟化模式 |
| `io_csr_priv_imode` | `input` | 2 | `csr.priv.imode` | 中断模式 |
| `io_hartId` | `input` | 6 | (未包含在Bundle中) | 硬件线程ID |
| **请求者 0 (Requestor 0) 接口** |  |  | **`requestor[0]`** | **Requestor 0 为单向接口** |
| `io_requestor_0_req_valid` | `input` | 1 | `requestor[0].req.valid` | 请求有效 |
| `io_requestor_0_req_bits_vaddr` | `input` | 50 | `requestor[0].req.vaddr` | 虚拟地址 |
| `io_requestor_0_resp_bits_paddr_0` | `output` | 48 | `requestor[0].resp.paddr` | 物理地址 |
| `io_requestor_0_resp_bits_gpaddr_0` | `output` | 64 | `requestor[0].resp.gpaddr` | 客户物理地址 |
| `io_requestor_0_resp_bits_pbmt_0` | `output` | 2 | `requestor[0].resp.pbmt` | Page-Based Memory Type |
| `io_requestor_0_resp_bits_miss` | `output` | 1 | `requestor[0].resp.miss` | TLB缺失 |
| `io_requestor_0_resp_bits_isForVSnonLeafPTE` | `output` | 1 | `requestor[0].resp.isForVSnonLeafPTE` | 是否为VS非叶PTE |
| `io_requestor_0_resp_bits_excp_0_gpf_instr` | `output` | 1 | `requestor[0].resp.gpf` | 客户权限错误 |
| `io_requestor_0_resp_bits_excp_0_pf_instr` | `output` | 1 | `requestor[0].resp.pf` | 页错误 |
| `io_requestor_0_resp_bits_excp_0_af_instr` | `output` | 1 | `requestor[0].resp.af` | 访问权限错误 |
| **请求者 1 (Requestor 1) 接口** |  |  | **`requestor[1]`** | **Requestor 1 为单向接口** |
| `io_requestor_1_req_valid` | `input` | 1 | `requestor[1].req.valid` | 请求有效 |
| `io_requestor_1_req_bits_vaddr` | `input` | 50 | `requestor[1].req.vaddr` | 虚拟地址 |
| `io_requestor_1_resp_bits_paddr_0` | `output` | 48 | `requestor[1].resp.paddr` | 物理地址 |
| `io_requestor_1_resp_bits_gpaddr_0` | `output` | 64 | `requestor[1].resp.gpaddr` | 客户物理地址 |
| `io_requestor_1_resp_bits_pbmt_0` | `output` | 2 | `requestor[1].resp.pbmt` | Page-Based Memory Type |
| `io_requestor_1_resp_bits_miss` | `output` | 1 | `requestor[1].resp.miss` | TLB缺失 |
| `io_requestor_1_resp_bits_isForVSnonLeafPTE` | `output` | 1 | `requestor[1].resp.isForVSnonLeafPTE` | 是否为VS非叶PTE |
| `io_requestor_1_resp_bits_excp_0_gpf_instr` | `output` | 1 | `requestor[1].resp.gpf` | 客户权限错误 |
| `io_requestor_1_resp_bits_excp_0_pf_instr` | `output` | 1 | `requestor[1].resp.pf` | 页错误 |
| `io_requestor_1_resp_bits_excp_0_af_instr` | `output` | 1 | `requestor[1].resp.af` | 访问权限错误 |
| **请求者 2 (Requestor 2) 接口** |  |  | **`requestor[2]`** | **Requestor 2 为双向握手接口** |
| `io_requestor_2_req_ready` | `output` | 1 | `requestor[2].req.ready` | 请求就绪 |
| `io_requestor_2_req_valid` | `input` | 1 | `requestor[2].req.valid` | 请求有效 |
| `io_requestor_2_req_bits_vaddr` | `input` | 50 | `requestor[2].req.vaddr` | 虚拟地址 |
| `io_requestor_2_resp_ready` | `input` | 1 | `requestor[2].resp.ready` | 响应就绪 |
| `io_requestor_2_resp_valid` | `output` | 1 | `requestor[2].resp.valid` | 响应有效 |
| `io_requestor_2_resp_bits_paddr_0` | `output` | 48 | `requestor[2].resp.paddr` | 物理地址 |
| `io_requestor_2_resp_bits_gpaddr_0` | `output` | 64 | `requestor[2].resp.gpaddr` | 客户物理地址 |
| `io_requestor_2_resp_bits_pbmt_0` | `output` | 2 | `requestor[2].resp.pbmt` | Page-Based Memory Type |
| `io_requestor_2_resp_bits_miss` | `output` | 1 | `requestor[2].resp.miss` | TLB缺失 |
| `io_requestor_2_resp_bits_isForVSnonLeafPTE` | `output` | 1 | `requestor[2].resp.isForVSnonLeafPTE` | 是否为VS非叶PTE |
| `io_requestor_2_resp_bits_excp_0_gpf_instr` | `output` | 1 | `requestor[2].resp.gpf` | 客户权限错误 |
| `io_requestor_2_resp_bits_excp_0_pf_instr` | `output` | 1 | `requestor[2].resp.pf` | 页错误 |
| `io_requestor_2_resp_bits_excp_0_af_instr` | `output` | 1 | `requestor[2].resp.af` | 访问权限错误 |
| **流水线刷新接口** |  |  | **`flushpipe`** |  |
| `io_flushPipe_0` | `input` | 1 | `flushpipe[0]` | 请求者0的刷新信号 |
| `io_flushPipe_1` | `input` | 1 | `flushpipe[1]` | 请求者1的刷新信号 |
| `io_flushPipe_2` | `input` | 1 | `flushpipe[2]` | 请求者2的刷新信号 |
| **PTW（页表遍历器）请求接口** |  |  | **`ptw.req`** |  |
| `io_ptw_req_0_valid` | `output` | 1 | `ptw.req[0].valid` | PTW请求0有效（单向） |
| `io_ptw_req_0_bits_vpn` | `output` | 38 | `ptw.req[0].vpn` | 虚拟页号 |
| `io_ptw_req_0_bits_s2xlate` | `output` | 2 | `ptw.req[0].s2xlate` | 翻译阶段 |
| `io_ptw_req_0_bits_getGpa` | `output` | 1 | `ptw.req[0].getgpa` | 是否获取GPA |
| `io_ptw_req_1_valid` | `output` | 1 | `ptw.req[1].valid` | PTW请求1有效（单向） |
| `io_ptw_req_1_bits_vpn` | `output` | 38 | `ptw.req[1].vpn` | 虚拟页号 |
| `io_ptw_req_1_bits_s2xlate` | `output` | 2 | `ptw.req[1].s2xlate` | 翻译阶段 |
| `io_ptw_req_1_bits_getGpa` | `output` | 1 | `ptw.req[1].getgpa` | 是否获取GPA |
| `io_ptw_req_2_ready` | `input` | 1 | `ptw.req[2].ready` | PTW请求2就绪 |
| `io_ptw_req_2_valid` | `output` | 1 | `ptw.req[2].valid` | PTW请求2有效（双向握手） |
| `io_ptw_req_2_bits_vpn` | `output` | 38 | `ptw.req[2].vpn` | 虚拟页号 |
| `io_ptw_req_2_bits_s2xlate` | `output` | 2 | `ptw.req[2].s2xlate` | 翻译阶段 |
| `io_ptw_req_2_bits_getGpa` | `output` | 1 | `ptw.req[2].getgpa` | 是否获取GPA |
| **PTW（页表遍历器）响应接口** |  |  | **`ptw.resp`** |  |
| `io_ptw_resp_valid` | `input` | 1 | `ptw.resp.valid` | PTW响应有效 |
| `io_ptw_resp_bits_s2xlate` | `input` | 2 | `ptw.resp.s2xlate` | 响应对应的翻译阶段 |
| `io_ptw_resp_bits_getGpa` | `input` | 1 | `ptw.resp.getgpa` | 响应是否为GPA |
| **PTW响应 - S1相关信号** |  |  | **`ptw.resp.s1`** | 第一阶段翻译结果 |
| `io_ptw_resp_bits_s1_entry_tag` | `input` | 35 | `ptw.resp.s1.entry.tag` | TLB Tag |
| `io_ptw_resp_bits_s1_entry_asid` | `input` | 16 | `ptw.resp.s1.entry.asid` | ASID |
| `io_ptw_resp_bits_s1_entry_vmid` | `input` | 14 | `ptw.resp.s1.entry.vmid` | VMID |
| `io_ptw_resp_bits_s1_entry_n` | `input` | 1 | `ptw.resp.s1.entry.n` |  |
| `io_ptw_resp_bits_s1_entry_pbmt` | `input` | 2 | `ptw.resp.s1.entry.pbmt` | PBMT |
| `io_ptw_resp_bits_s1_entry_perm_d` | `input` | 1 | `ptw.resp.s1.entry.perm.d` | 权限：Dirty |
| `io_ptw_resp_bits_s1_entry_perm_a` | `input` | 1 | `ptw.resp.s1.entry.perm.a` | 权限：Accessed |
| `io_ptw_resp_bits_s1_entry_perm_g` | `input` | 1 | `ptw.resp.s1.entry.perm.g` | 权限：Global |
| `io_ptw_resp_bits_s1_entry_perm_u` | `input` | 1 | `ptw.resp.s1.entry.perm.u` | 权限：User |
| `io_ptw_resp_bits_s1_entry_perm_x` | `input` | 1 | `ptw.resp.s1.entry.perm.x` | 权限：eXecute |
| `io_ptw_resp_bits_s1_entry_perm_w` | `input` | 1 | `ptw.resp.s1.entry.perm.w` | 权限：Write |
| `io_ptw_resp_bits_s1_entry_perm_r` | `input` | 1 | `ptw.resp.s1.entry.perm.r` | 权限：Read |
| `io_ptw_resp_bits_s1_entry_level` | `input` | 2 | `ptw.resp.s1.entry.level` | 页表层级 |
| `io_ptw_resp_bits_s1_entry_v` | `input` | 1 | `ptw.resp.s1.entry.v` | 条目有效位 |
| `io_ptw_resp_bits_s1_entry_ppn` | `input` | 41 | `ptw.resp.s1.entry.ppn` | 物理页号 |
| `io_ptw_resp_bits_s1_addr_low` | `input` | 3 | `ptw.resp.s1.addr_low` | 地址低位 |
| `io_ptw_resp_bits_s1_ppn_low_0` | `input` | 3 | `ptw.resp.s1.ppn_low[0]` | PPN低位 (Way 0) |
| `io_ptw_resp_bits_s1_ppn_low_1` | `input` | 3 | `ptw.resp.s1.ppn_low[1]` | PPN低位 (Way 1) |
| `io_ptw_resp_bits_s1_ppn_low_2` | `input` | 3 | `ptw.resp.s1.ppn_low[2]` | PPN低位 (Way 2) |
| `io_ptw_resp_bits_s1_ppn_low_3` | `input` | 3 | `ptw.resp.s1.ppn_low[3]` | PPN低位 (Way 3) |
| `io_ptw_resp_bits_s1_ppn_low_4` | `input` | 3 | `ptw.resp.s1.ppn_low[4]` | PPN低位 (Way 4) |
| `io_ptw_resp_bits_s1_ppn_low_5` | `input` | 3 | `ptw.resp.s1.ppn_low[5]` | PPN低位 (Way 5) |
| `io_ptw_resp_bits_s1_ppn_low_6` | `input` | 3 | `ptw.resp.s1.ppn_low[6]` | PPN低位 (Way 6) |
| `io_ptw_resp_bits_s1_ppn_low_7` | `input` | 3 | `ptw.resp.s1.ppn_low[7]` | PPN低位 (Way 7) |
| `io_ptw_resp_bits_s1_valididx_0` | `input` | 1 | `ptw.resp.s1.valididx[0]` | 有效索引 (Way 0) |
| `io_ptw_resp_bits_s1_valididx_1` | `input` | 1 | `ptw.resp.s1.valididx[1]` | 有效索引 (Way 1) |
| `io_ptw_resp_bits_s1_valididx_2` | `input` | 1 | `ptw.resp.s1.valididx[2]` | 有效索引 (Way 2) |
| `io_ptw_resp_bits_s1_valididx_3` | `input` | 1 | `ptw.resp.s1.valididx[3]` | 有效索引 (Way 3) |
| `io_ptw_resp_bits_s1_valididx_4` | `input` | 1 | `ptw.resp.s1.valididx[4]` | 有效索引 (Way 4) |
| `io_ptw_resp_bits_s1_valididx_5` | `input` | 1 | `ptw.resp.s1.valididx[5]` | 有效索引 (Way 5) |
| `io_ptw_resp_bits_s1_valididx_6` | `input` | 1 | `ptw.resp.s1.valididx[6]` | 有效索引 (Way 6) |
| `io_ptw_resp_bits_s1_valididx_7` | `input` | 1 | `ptw.resp.s1.valididx[7]` | 有效索引 (Way 7) |
| `io_ptw_resp_bits_s1_pteidx_0` | `input` | 1 | `ptw.resp.s1.pteidx[0]` | PTE索引 (Way 0) |
| `io_ptw_resp_bits_s1_pteidx_1` | `input` | 1 | `ptw.resp.s1.pteidx[1]` | PTE索引 (Way 1) |
| `io_ptw_resp_bits_s1_pteidx_2` | `input` | 1 | `ptw.resp.s1.pteidx[2]` | PTE索引 (Way 2) |
| `io_ptw_resp_bits_s1_pteidx_3` | `input` | 1 | `ptw.resp.s1.pteidx[3]` | PTE索引 (Way 3) |
| `io_ptw_resp_bits_s1_pteidx_4` | `input` | 1 | `ptw.resp.s1.pteidx[4]` | PTE索引 (Way 4) |
| `io_ptw_resp_bits_s1_pteidx_5` | `input` | 1 | `ptw.resp.s1.pteidx[5]` | PTE索引 (Way 5) |
| `io_ptw_resp_bits_s1_pteidx_6` | `input` | 1 | `ptw.resp.s1.pteidx[6]` | PTE索引 (Way 6) |
| `io_ptw_resp_bits_s1_pteidx_7` | `input` | 1 | `ptw.resp.s1.pteidx[7]` | PTE索引 (Way 7) |
| `io_ptw_resp_bits_s1_pf` | `input` | 1 | `ptw.resp.s1.pf` | S1页错误 |
| `io_ptw_resp_bits_s1_af` | `input` | 1 | `ptw.resp.s1.af` | S1访问权限错误 |
| **PTW响应 - S2相关信号** |  |  | **`ptw.resp.s2`** | 第二阶段翻译结果 |
| `io_ptw_resp_bits_s2_entry_tag` | `input` | 38 | `ptw.resp.s2.entry.tag` | TLB Tag |
| `io_ptw_resp_bits_s2_entry_vmid` | `input` | 14 | `ptw.resp.s2.entry.vmid` | VMID |
| `io_ptw_resp_bits_s2_entry_n` | `input` | 1 | `ptw.resp.s2.entry.n` |  |
| `io_ptw_resp_bits_s2_entry_pbmt` | `input` | 2 | `ptw.resp.s2.entry.pbmt` | PBMT |
| `io_ptw_resp_bits_s2_entry_ppn` | `input` | 38 | `ptw.resp.s2.entry.ppn` | 物理页号 |
| `io_ptw_resp_bits_s2_entry_perm_d` | `input` | 1 | `ptw.resp.s2.entry.perm.d` | 权限：Dirty |
| `io_ptw_resp_bits_s2_entry_perm_a` | `input` | 1 | `ptw.resp.s2.entry.perm.a` | 权限：Accessed |
| `io_ptw_resp_bits_s2_entry_perm_g` | `input` | 1 | `ptw.resp.s2.entry.perm.g` | 权限：Global |
| `io_ptw_resp_bits_s2_entry_perm_u` | `input` | 1 | `ptw.resp.s2.entry.perm.u` | 权限：User |
| `io_ptw_resp_bits_s2_entry_perm_x` | `input` | 1 | `ptw.resp.s2.entry.perm.x` | 权限：eXecute |
| `io_ptw_resp_bits_s2_entry_perm_w` | `input` | 1 | `ptw.resp.s2.entry.perm.w` | 权限：Write |
| `io_ptw_resp_bits_s2_entry_perm_r` | `input` | 1 | `ptw.resp.s2.entry.perm.r` | 权限：Read |
| `io_ptw_resp_bits_s2_entry_level` | `input` | 2 | `ptw.resp.s2.entry.level` | 页表层级 |
| `io_ptw_resp_bits_s2_gpf` | `input` | 1 | `ptw.resp.s2.gpf` | S2客户权限错误 |
| `io_ptw_resp_bits_s2_gaf` | `input` | 1 | `ptw.resp.s2.gaf` | S2客户访问权限错误 |