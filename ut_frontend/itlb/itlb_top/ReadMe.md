# **Translation Lookaside Buffer (TLB)**

## �ź��ܱ�

| ԭʼ�˿��ź� | �źŷ��� | λ�� | �ṹ��Bundle·�� | ˵�� |
| :--- | :--- | :--- | :--- | :--- |
| **ʱ���븴λ** |  |  |  |  |
| `clock` | `input` | 1 | (δ������Bundle��) | ȫ��ʱ���ź� |
| `reset` | `input` | 1 | (δ������Bundle��) | ȫ�ָ�λ�ź� |
| **Sfence��դ�ϣ��ӿ�** |  |  | **`sfence`** |  |
| `io_sfence_valid` | `input` | 1 | `sfence.valid` | Sfence������Ч |
| `io_sfence_bits_rs1` | `input` | 1 | `sfence.bits.rs1` |  |
| `io_sfence_bits_rs2` | `input` | 1 | `sfence.bits.rs2` |  |
| `io_sfence_bits_addr` | `input` | 50 | `sfence.bits.addr` | Ŀ�������ַ |
| `io_sfence_bits_id` | `input` | 16 | `sfence.bits.id` |  |
| `io_sfence_bits_flushPipe` | `input` | 1 | `sfence.bits.flushpipe` | �Ƿ�ˢ����ˮ�� |
| `io_sfence_bits_hv` | `input` | 1 | `sfence.bits.hv` |  |
| `io_sfence_bits_hg` | `input` | 1 | `sfence.bits.hg` |  |
| **CSR��������״̬�Ĵ������ӿ�** |  |  | **`csr`** |  |
| `io_csr_satp_mode` | `input` | 4 | `csr.satp.mode` | SATP�Ĵ���ģʽλ |
| `io_csr_satp_asid` | `input` | 16 | `csr.satp.asid` | SATP�Ĵ���ASID |
| `io_csr_satp_ppn` | `input` | 44 | `csr.satp.ppn` | SATP�Ĵ���PPN |
| `io_csr_satp_changed` | `input` | 1 | `csr.satp.changed` | SATP�Ĵ��������ı� |
| `io_csr_vsatp_mode` | `input` | 4 | `csr.vsatp.mode` | VSATP�Ĵ���ģʽλ |
| `io_csr_vsatp_asid` | `input` | 16 | `csr.vsatp.asid` | VSATP�Ĵ���ASID |
| `io_csr_vsatp_ppn` | `input` | 44 | `csr.vsatp.ppn` | VSATP�Ĵ���PPN |
| `io_csr_vsatp_changed` | `input` | 1 | `csr.vsatp.changed` | VSATP�Ĵ��������ı� |
| `io_csr_hgatp_mode` | `input` | 4 | `csr.hgatp.mode` | HGATP�Ĵ���ģʽλ |
| `io_csr_hgatp_vmid` | `input` | 16 | `csr.hgatp.asid` | **��һ�£��˿�Ϊvmid��Bundleӳ��Ϊasid** |
| `io_csr_hgatp_ppn` | `input` | 44 | `csr.hgatp.ppn` | HGATP�Ĵ���PPN |
| `io_csr_hgatp_changed` | `input` | 1 | `csr.hgatp.changed` | HGATP�Ĵ��������ı� |
| `io_csr_priv_virt` | `input` | 1 | `csr.priv.virt` | ���⻯ģʽ |
| `io_csr_priv_imode` | `input` | 2 | `csr.priv.imode` | �ж�ģʽ |
| `io_hartId` | `input` | 6 | (δ������Bundle��) | Ӳ���߳�ID |
| **������ 0 (Requestor 0) �ӿ�** |  |  | **`requestor[0]`** | **Requestor 0 Ϊ����ӿ�** |
| `io_requestor_0_req_valid` | `input` | 1 | `requestor[0].req.valid` | ������Ч |
| `io_requestor_0_req_bits_vaddr` | `input` | 50 | `requestor[0].req.vaddr` | �����ַ |
| `io_requestor_0_resp_bits_paddr_0` | `output` | 48 | `requestor[0].resp.paddr` | �����ַ |
| `io_requestor_0_resp_bits_gpaddr_0` | `output` | 64 | `requestor[0].resp.gpaddr` | �ͻ������ַ |
| `io_requestor_0_resp_bits_pbmt_0` | `output` | 2 | `requestor[0].resp.pbmt` | Page-Based Memory Type |
| `io_requestor_0_resp_bits_miss` | `output` | 1 | `requestor[0].resp.miss` | TLBȱʧ |
| `io_requestor_0_resp_bits_isForVSnonLeafPTE` | `output` | 1 | `requestor[0].resp.isForVSnonLeafPTE` | �Ƿ�ΪVS��ҶPTE |
| `io_requestor_0_resp_bits_excp_0_gpf_instr` | `output` | 1 | `requestor[0].resp.gpf` | �ͻ�Ȩ�޴��� |
| `io_requestor_0_resp_bits_excp_0_pf_instr` | `output` | 1 | `requestor[0].resp.pf` | ҳ���� |
| `io_requestor_0_resp_bits_excp_0_af_instr` | `output` | 1 | `requestor[0].resp.af` | ����Ȩ�޴��� |
| **������ 1 (Requestor 1) �ӿ�** |  |  | **`requestor[1]`** | **Requestor 1 Ϊ����ӿ�** |
| `io_requestor_1_req_valid` | `input` | 1 | `requestor[1].req.valid` | ������Ч |
| `io_requestor_1_req_bits_vaddr` | `input` | 50 | `requestor[1].req.vaddr` | �����ַ |
| `io_requestor_1_resp_bits_paddr_0` | `output` | 48 | `requestor[1].resp.paddr` | �����ַ |
| `io_requestor_1_resp_bits_gpaddr_0` | `output` | 64 | `requestor[1].resp.gpaddr` | �ͻ������ַ |
| `io_requestor_1_resp_bits_pbmt_0` | `output` | 2 | `requestor[1].resp.pbmt` | Page-Based Memory Type |
| `io_requestor_1_resp_bits_miss` | `output` | 1 | `requestor[1].resp.miss` | TLBȱʧ |
| `io_requestor_1_resp_bits_isForVSnonLeafPTE` | `output` | 1 | `requestor[1].resp.isForVSnonLeafPTE` | �Ƿ�ΪVS��ҶPTE |
| `io_requestor_1_resp_bits_excp_0_gpf_instr` | `output` | 1 | `requestor[1].resp.gpf` | �ͻ�Ȩ�޴��� |
| `io_requestor_1_resp_bits_excp_0_pf_instr` | `output` | 1 | `requestor[1].resp.pf` | ҳ���� |
| `io_requestor_1_resp_bits_excp_0_af_instr` | `output` | 1 | `requestor[1].resp.af` | ����Ȩ�޴��� |
| **������ 2 (Requestor 2) �ӿ�** |  |  | **`requestor[2]`** | **Requestor 2 Ϊ˫�����ֽӿ�** |
| `io_requestor_2_req_ready` | `output` | 1 | `requestor[2].req.ready` | ������� |
| `io_requestor_2_req_valid` | `input` | 1 | `requestor[2].req.valid` | ������Ч |
| `io_requestor_2_req_bits_vaddr` | `input` | 50 | `requestor[2].req.vaddr` | �����ַ |
| `io_requestor_2_resp_ready` | `input` | 1 | `requestor[2].resp.ready` | ��Ӧ���� |
| `io_requestor_2_resp_valid` | `output` | 1 | `requestor[2].resp.valid` | ��Ӧ��Ч |
| `io_requestor_2_resp_bits_paddr_0` | `output` | 48 | `requestor[2].resp.paddr` | �����ַ |
| `io_requestor_2_resp_bits_gpaddr_0` | `output` | 64 | `requestor[2].resp.gpaddr` | �ͻ������ַ |
| `io_requestor_2_resp_bits_pbmt_0` | `output` | 2 | `requestor[2].resp.pbmt` | Page-Based Memory Type |
| `io_requestor_2_resp_bits_miss` | `output` | 1 | `requestor[2].resp.miss` | TLBȱʧ |
| `io_requestor_2_resp_bits_isForVSnonLeafPTE` | `output` | 1 | `requestor[2].resp.isForVSnonLeafPTE` | �Ƿ�ΪVS��ҶPTE |
| `io_requestor_2_resp_bits_excp_0_gpf_instr` | `output` | 1 | `requestor[2].resp.gpf` | �ͻ�Ȩ�޴��� |
| `io_requestor_2_resp_bits_excp_0_pf_instr` | `output` | 1 | `requestor[2].resp.pf` | ҳ���� |
| `io_requestor_2_resp_bits_excp_0_af_instr` | `output` | 1 | `requestor[2].resp.af` | ����Ȩ�޴��� |
| **��ˮ��ˢ�½ӿ�** |  |  | **`flushpipe`** |  |
| `io_flushPipe_0` | `input` | 1 | `flushpipe[0]` | ������0��ˢ���ź� |
| `io_flushPipe_1` | `input` | 1 | `flushpipe[1]` | ������1��ˢ���ź� |
| `io_flushPipe_2` | `input` | 1 | `flushpipe[2]` | ������2��ˢ���ź� |
| **PTW��ҳ�������������ӿ�** |  |  | **`ptw.req`** |  |
| `io_ptw_req_0_valid` | `output` | 1 | `ptw.req[0].valid` | PTW����0��Ч������ |
| `io_ptw_req_0_bits_vpn` | `output` | 38 | `ptw.req[0].vpn` | ����ҳ�� |
| `io_ptw_req_0_bits_s2xlate` | `output` | 2 | `ptw.req[0].s2xlate` | ����׶� |
| `io_ptw_req_0_bits_getGpa` | `output` | 1 | `ptw.req[0].getgpa` | �Ƿ��ȡGPA |
| `io_ptw_req_1_valid` | `output` | 1 | `ptw.req[1].valid` | PTW����1��Ч������ |
| `io_ptw_req_1_bits_vpn` | `output` | 38 | `ptw.req[1].vpn` | ����ҳ�� |
| `io_ptw_req_1_bits_s2xlate` | `output` | 2 | `ptw.req[1].s2xlate` | ����׶� |
| `io_ptw_req_1_bits_getGpa` | `output` | 1 | `ptw.req[1].getgpa` | �Ƿ��ȡGPA |
| `io_ptw_req_2_ready` | `input` | 1 | `ptw.req[2].ready` | PTW����2���� |
| `io_ptw_req_2_valid` | `output` | 1 | `ptw.req[2].valid` | PTW����2��Ч��˫�����֣� |
| `io_ptw_req_2_bits_vpn` | `output` | 38 | `ptw.req[2].vpn` | ����ҳ�� |
| `io_ptw_req_2_bits_s2xlate` | `output` | 2 | `ptw.req[2].s2xlate` | ����׶� |
| `io_ptw_req_2_bits_getGpa` | `output` | 1 | `ptw.req[2].getgpa` | �Ƿ��ȡGPA |
| **PTW��ҳ�����������Ӧ�ӿ�** |  |  | **`ptw.resp`** |  |
| `io_ptw_resp_valid` | `input` | 1 | `ptw.resp.valid` | PTW��Ӧ��Ч |
| `io_ptw_resp_bits_s2xlate` | `input` | 2 | `ptw.resp.s2xlate` | ��Ӧ��Ӧ�ķ���׶� |
| `io_ptw_resp_bits_getGpa` | `input` | 1 | `ptw.resp.getgpa` | ��Ӧ�Ƿ�ΪGPA |
| **PTW��Ӧ - S1����ź�** |  |  | **`ptw.resp.s1`** | ��һ�׶η����� |
| `io_ptw_resp_bits_s1_entry_tag` | `input` | 35 | `ptw.resp.s1.entry.tag` | TLB Tag |
| `io_ptw_resp_bits_s1_entry_asid` | `input` | 16 | `ptw.resp.s1.entry.asid` | ASID |
| `io_ptw_resp_bits_s1_entry_vmid` | `input` | 14 | `ptw.resp.s1.entry.vmid` | VMID |
| `io_ptw_resp_bits_s1_entry_n` | `input` | 1 | `ptw.resp.s1.entry.n` |  |
| `io_ptw_resp_bits_s1_entry_pbmt` | `input` | 2 | `ptw.resp.s1.entry.pbmt` | PBMT |
| `io_ptw_resp_bits_s1_entry_perm_d` | `input` | 1 | `ptw.resp.s1.entry.perm.d` | Ȩ�ޣ�Dirty |
| `io_ptw_resp_bits_s1_entry_perm_a` | `input` | 1 | `ptw.resp.s1.entry.perm.a` | Ȩ�ޣ�Accessed |
| `io_ptw_resp_bits_s1_entry_perm_g` | `input` | 1 | `ptw.resp.s1.entry.perm.g` | Ȩ�ޣ�Global |
| `io_ptw_resp_bits_s1_entry_perm_u` | `input` | 1 | `ptw.resp.s1.entry.perm.u` | Ȩ�ޣ�User |
| `io_ptw_resp_bits_s1_entry_perm_x` | `input` | 1 | `ptw.resp.s1.entry.perm.x` | Ȩ�ޣ�eXecute |
| `io_ptw_resp_bits_s1_entry_perm_w` | `input` | 1 | `ptw.resp.s1.entry.perm.w` | Ȩ�ޣ�Write |
| `io_ptw_resp_bits_s1_entry_perm_r` | `input` | 1 | `ptw.resp.s1.entry.perm.r` | Ȩ�ޣ�Read |
| `io_ptw_resp_bits_s1_entry_level` | `input` | 2 | `ptw.resp.s1.entry.level` | ҳ��㼶 |
| `io_ptw_resp_bits_s1_entry_v` | `input` | 1 | `ptw.resp.s1.entry.v` | ��Ŀ��Чλ |
| `io_ptw_resp_bits_s1_entry_ppn` | `input` | 41 | `ptw.resp.s1.entry.ppn` | ����ҳ�� |
| `io_ptw_resp_bits_s1_addr_low` | `input` | 3 | `ptw.resp.s1.addr_low` | ��ַ��λ |
| `io_ptw_resp_bits_s1_ppn_low_0` | `input` | 3 | `ptw.resp.s1.ppn_low[0]` | PPN��λ (Way 0) |
| `io_ptw_resp_bits_s1_ppn_low_1` | `input` | 3 | `ptw.resp.s1.ppn_low[1]` | PPN��λ (Way 1) |
| `io_ptw_resp_bits_s1_ppn_low_2` | `input` | 3 | `ptw.resp.s1.ppn_low[2]` | PPN��λ (Way 2) |
| `io_ptw_resp_bits_s1_ppn_low_3` | `input` | 3 | `ptw.resp.s1.ppn_low[3]` | PPN��λ (Way 3) |
| `io_ptw_resp_bits_s1_ppn_low_4` | `input` | 3 | `ptw.resp.s1.ppn_low[4]` | PPN��λ (Way 4) |
| `io_ptw_resp_bits_s1_ppn_low_5` | `input` | 3 | `ptw.resp.s1.ppn_low[5]` | PPN��λ (Way 5) |
| `io_ptw_resp_bits_s1_ppn_low_6` | `input` | 3 | `ptw.resp.s1.ppn_low[6]` | PPN��λ (Way 6) |
| `io_ptw_resp_bits_s1_ppn_low_7` | `input` | 3 | `ptw.resp.s1.ppn_low[7]` | PPN��λ (Way 7) |
| `io_ptw_resp_bits_s1_valididx_0` | `input` | 1 | `ptw.resp.s1.valididx[0]` | ��Ч���� (Way 0) |
| `io_ptw_resp_bits_s1_valididx_1` | `input` | 1 | `ptw.resp.s1.valididx[1]` | ��Ч���� (Way 1) |
| `io_ptw_resp_bits_s1_valididx_2` | `input` | 1 | `ptw.resp.s1.valididx[2]` | ��Ч���� (Way 2) |
| `io_ptw_resp_bits_s1_valididx_3` | `input` | 1 | `ptw.resp.s1.valididx[3]` | ��Ч���� (Way 3) |
| `io_ptw_resp_bits_s1_valididx_4` | `input` | 1 | `ptw.resp.s1.valididx[4]` | ��Ч���� (Way 4) |
| `io_ptw_resp_bits_s1_valididx_5` | `input` | 1 | `ptw.resp.s1.valididx[5]` | ��Ч���� (Way 5) |
| `io_ptw_resp_bits_s1_valididx_6` | `input` | 1 | `ptw.resp.s1.valididx[6]` | ��Ч���� (Way 6) |
| `io_ptw_resp_bits_s1_valididx_7` | `input` | 1 | `ptw.resp.s1.valididx[7]` | ��Ч���� (Way 7) |
| `io_ptw_resp_bits_s1_pteidx_0` | `input` | 1 | `ptw.resp.s1.pteidx[0]` | PTE���� (Way 0) |
| `io_ptw_resp_bits_s1_pteidx_1` | `input` | 1 | `ptw.resp.s1.pteidx[1]` | PTE���� (Way 1) |
| `io_ptw_resp_bits_s1_pteidx_2` | `input` | 1 | `ptw.resp.s1.pteidx[2]` | PTE���� (Way 2) |
| `io_ptw_resp_bits_s1_pteidx_3` | `input` | 1 | `ptw.resp.s1.pteidx[3]` | PTE���� (Way 3) |
| `io_ptw_resp_bits_s1_pteidx_4` | `input` | 1 | `ptw.resp.s1.pteidx[4]` | PTE���� (Way 4) |
| `io_ptw_resp_bits_s1_pteidx_5` | `input` | 1 | `ptw.resp.s1.pteidx[5]` | PTE���� (Way 5) |
| `io_ptw_resp_bits_s1_pteidx_6` | `input` | 1 | `ptw.resp.s1.pteidx[6]` | PTE���� (Way 6) |
| `io_ptw_resp_bits_s1_pteidx_7` | `input` | 1 | `ptw.resp.s1.pteidx[7]` | PTE���� (Way 7) |
| `io_ptw_resp_bits_s1_pf` | `input` | 1 | `ptw.resp.s1.pf` | S1ҳ���� |
| `io_ptw_resp_bits_s1_af` | `input` | 1 | `ptw.resp.s1.af` | S1����Ȩ�޴��� |
| **PTW��Ӧ - S2����ź�** |  |  | **`ptw.resp.s2`** | �ڶ��׶η����� |
| `io_ptw_resp_bits_s2_entry_tag` | `input` | 38 | `ptw.resp.s2.entry.tag` | TLB Tag |
| `io_ptw_resp_bits_s2_entry_vmid` | `input` | 14 | `ptw.resp.s2.entry.vmid` | VMID |
| `io_ptw_resp_bits_s2_entry_n` | `input` | 1 | `ptw.resp.s2.entry.n` |  |
| `io_ptw_resp_bits_s2_entry_pbmt` | `input` | 2 | `ptw.resp.s2.entry.pbmt` | PBMT |
| `io_ptw_resp_bits_s2_entry_ppn` | `input` | 38 | `ptw.resp.s2.entry.ppn` | ����ҳ�� |
| `io_ptw_resp_bits_s2_entry_perm_d` | `input` | 1 | `ptw.resp.s2.entry.perm.d` | Ȩ�ޣ�Dirty |
| `io_ptw_resp_bits_s2_entry_perm_a` | `input` | 1 | `ptw.resp.s2.entry.perm.a` | Ȩ�ޣ�Accessed |
| `io_ptw_resp_bits_s2_entry_perm_g` | `input` | 1 | `ptw.resp.s2.entry.perm.g` | Ȩ�ޣ�Global |
| `io_ptw_resp_bits_s2_entry_perm_u` | `input` | 1 | `ptw.resp.s2.entry.perm.u` | Ȩ�ޣ�User |
| `io_ptw_resp_bits_s2_entry_perm_x` | `input` | 1 | `ptw.resp.s2.entry.perm.x` | Ȩ�ޣ�eXecute |
| `io_ptw_resp_bits_s2_entry_perm_w` | `input` | 1 | `ptw.resp.s2.entry.perm.w` | Ȩ�ޣ�Write |
| `io_ptw_resp_bits_s2_entry_perm_r` | `input` | 1 | `ptw.resp.s2.entry.perm.r` | Ȩ�ޣ�Read |
| `io_ptw_resp_bits_s2_entry_level` | `input` | 2 | `ptw.resp.s2.entry.level` | ҳ��㼶 |
| `io_ptw_resp_bits_s2_gpf` | `input` | 1 | `ptw.resp.s2.gpf` | S2�ͻ�Ȩ�޴��� |
| `io_ptw_resp_bits_s2_gaf` | `input` | 1 | `ptw.resp.s2.gaf` | S2�ͻ�����Ȩ�޴��� |