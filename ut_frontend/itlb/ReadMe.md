# **Translation Lookaside Buffer (TLB)**

## һ��TLB IO �ź��ܱ�

### 1. ȫ�ֿ����ź�

| �ź���        | ����     | λ�� | ����                        |
|---------------|---------|------|-----------------------------|
| clock         | `input` | 1    | ʱ���źţ����� TLB ��ʱ���߼� |
| reset         | `input` | 1    | ��λ�źţ��������� TLB ��״̬ |
| io_hartId     | `input` | 6    | Ӳ���߳�ID                  |

### 2. SFENCE ָ��ӿ��ź�

| �ź���                          | ����     | λ�� | ����                                 |
|---------------------------------|---------|------|--------------------------------------|
| io_sfence_valid                 | `input` | 1    | SFENCE������Ч�ź�                    |
| io_sfence_bits_rs1              | `input` | 1    | ָʾ�Ƿ�ʹ�üĴ���rs1��ֵ����ַ��      |
| io_sfence_bits_rs2              | `input` | 1    | ָʾ�Ƿ�ʹ�üĴ���rs2��ֵ��ASID��      |
| io_sfence_bits_addr             | `input` | 50   | SFENCE����ָ��Ҫˢ�µ������ַ������ѡ����ˢ���ض���ַ�� TLB ��Ŀ |
| io_sfence_bits_id               | `input` | 16   | SFENCE����ָ��Ҫˢ�µ�ASID������ѡ����ˢ���ض���ַ�ռ�� TLB ��Ŀ |
| io_sfence_bits_flushPipe        | `input` | 1    | ָʾ��ǰ SFENCE �����Ƿ�ˢ����ˮ��      |
| io_sfence_bits_hv               | `input` | 1    | �Ƿ���Hypervisorģʽ��ִ��SFENCE       |
| io_sfence_bits_hg               | `input` | 1    | �Ƿ���Hypervisor guestģʽ��ִ��SFENCE |

### 3. CSR �Ĵ�������

| �ź���                          | ����     | λ�� | ����                               |
|---------------------------------|---------|------|-----------------------------------|
| io_csr_satp_mode                | `input` | 4    | SATP�Ĵ���ģʽλ                   |
| io_csr_satp_asid                | `input` | 16   | SATP�Ĵ���ASID                    |
| io_csr_satp_ppn                 | `input` | 44   | SATP�Ĵ���PPN                     |
| io_csr_satp_changed             | `input` | 1    | SATP�Ĵ����Ƿ����仯             |
| io_csr_vsatp_mode               | `input` | 4    | VSATP�Ĵ���ģʽλ�����⻯��        |
| io_csr_vsatp_asid               | `input` | 16   | VSATP�Ĵ���ASID                   |
| io_csr_vsatp_ppn                | `input` | 44   | VSATP�Ĵ���PPN                    |
| io_csr_vsatp_changed            | `input` | 1    | VSATP�Ĵ����Ƿ����仯            |
| io_csr_hgatp_mode               | `input` | 4    | HGATP�Ĵ���ģʽλ�����⻯��        |
| io_csr_hgatp_vmid               | `input` | 16   | HGATP�Ĵ���VMID                   |
| io_csr_hgatp_ppn                | `input` | 44   | HGATP�Ĵ���PPN                    |
| io_csr_hgatp_changed            | `input` | 1    | HGATP�Ĵ����Ƿ����仯            |
| io_csr_priv_virt                | `input` | 1    | ���⻯ʹ���ź�                     |
| io_csr_priv_imode               | `input` | 2    | ��ǰ��Ȩģʽ��00��U, 01��S, 11��M�� |

### 4. ��������Ӧ�ӿڣ�Requestor 0��

| �ź���                                     | ����      | λ�� | ����                            |
|--------------------------------------------|----------|------|--------------------------------|
| io_requestor_0_req_valid                   | `input`  | 1    | ����0��Ч                       |
| io_requestor_0_req_bits_vaddr              | `input`  | 50   | ����0�������ַ                  |
| io_requestor_0_resp_bits_paddr_0           | `output` | 48   | ��Ӧ0�������ַ                  |
| io_requestor_0_resp_bits_gpaddr_0          | `output` | 64   | ��Ӧ0�����⻯�����ַ            |
| io_requestor_0_resp_bits_pbmt_0            | `output` | 2    | ��Ӧ0�������ڴ汣������          |
| io_requestor_0_resp_bits_miss              | `output` | 1    | ��Ӧ0�Ƿ�TLBȱʧ                |
| io_requestor_0_resp_bits_isForVSnonLeafPTE | `output` | 1    | ��Ӧ0�Ƿ�Ϊ�������Ҷ��PTE       |
| io_requestor_0_resp_bits_excp_0_gpf_instr  | `output` | 1    | ָ��0�����⻯ȱҳ�쳣            |
| io_requestor_0_resp_bits_excp_0_pf_instr   | `output` | 1    | ָ��0��ȱҳ�쳣                 |
| io_requestor_0_resp_bits_excp_0_af_instr   | `output` | 1    | ָ��0�ķ���Ȩ���쳣              |

### 5. ��������Ӧ�ӿڣ�Requestor 1��

| �ź���                                     | ����      | λ�� | ����                            |
|--------------------------------------------|----------|------|---------------------------------|
| io_requestor_1_req_valid                   | `input`  | 1    | ����1��Ч                        |
| io_requestor_1_req_bits_vaddr              | `input`  | 50   | ����1�������ַ                  |
| io_requestor_1_resp_bits_paddr_0           | `output` | 48   | ��Ӧ1�������ַ                  |
| io_requestor_1_resp_bits_gpaddr_0          | `output` | 64   | ��Ӧ1�����⻯�����ַ            |
| io_requestor_1_resp_bits_pbmt_0            | `output` | 2    | ��Ӧ1�������ڴ汣������          |
| io_requestor_1_resp_bits_miss              | `output` | 1    | ��Ӧ1�Ƿ�TLBȱʧ                |
| io_requestor_1_resp_bits_isForVSnonLeafPTE | `output` | 1    | ��Ӧ1�Ƿ�Ϊ�������Ҷ��PTE       |
| io_requestor_1_resp_bits_excp_0_gpf_instr  | `output` | 1    | ���ݷ���0�����⻯ȱҳ�쳣        |
| io_requestor_1_resp_bits_excp_0_pf_instr   | `output` | 1    | ���ݷ���0��ȱҳ�쳣              |
| io_requestor_1_resp_bits_excp_0_af_instr   | `output` | 1    | ���ݷ���0�ķ���Ȩ���쳣          |

### 6. ��������Ӧ�ӿڣ�Requestor 2��

| �ź���                                      | ����     | λ�� | ����                         |
|--------------------------------------------|----------|----|--------------------------------|
| io_requestor_2_req_ready                   | `output` | 1  | ����2�����ź�                   |
| io_requestor_2_req_valid                   | `input`  | 1  | ����2��Ч                      |
| io_requestor_2_req_bits_vaddr              | `input`  | 50 | ����2�������ַ                 |
| io_requestor_2_resp_ready                  | `input`  | 1  | ��Ӧ2�����ź�                   |
| io_requestor_2_resp_valid                  | `output` | 1  | ��Ӧ2��Ч                       |
| io_requestor_2_resp_bits_paddr_0           | `output` | 48 | ��Ӧ2�������ַ                 |
| io_requestor_2_resp_bits_gpaddr_0          | `output` | 64 | ��Ӧ2�����⻯�����ַ           |
| io_requestor_2_resp_bits_pbmt_0            | `output` | 2  | ��Ӧ2�������ڴ汣������         |
| io_requestor_2_resp_bits_miss              | `output` | 1  | ��Ӧ2�Ƿ�TLBȱʧ               |
| io_requestor_2_resp_bits_isForVSnonLeafPTE | `output` | 1  | ��Ӧ2�Ƿ�Ϊ�������Ҷ��PTE      |
| io_requestor_2_resp_bits_excp_0_gpf_instr  | `output` | 1  | PTW���ʵ����⻯ȱҳ�쳣         |
| io_requestor_2_resp_bits_excp_0_pf_instr   | `output` | 1  | PTW���ʵ�ȱҳ�쳣               |
| io_requestor_2_resp_bits_excp_0_af_instr   | `output` | 1  | PTW���ʵķ���Ȩ���쳣           |

### 7. ��ˮ��ˢ���źţ������ⲿ��

| �ź���                | ����     | λ�� | ����           |
|-----------------------|---------|------|---------------|
| io_flushPipe_0        | `input` | 1    | ˢ����ˮ�� 0   |
| io_flushPipe_1        | `input` | 1    | ˢ����ˮ�� 1   |
| io_flushPipe_2        | `input` | 1    | ˢ����ˮ�� 2   |

### 8. PTW ����ӿڣ���3��ͨ����

| �ź���                      | ����      | λ�� | ����                              |
|-----------------------------|----------|------|----------------------------------|
| io_ptw_req_0_valid          | `output` | 1    | PTW����ͨ��0��Ч                 |
| io_ptw_req_0_bits_vpn       | `output` | 38   | ���������ҳ�ţ�VPN��             |
| io_ptw_req_0_bits_s2xlate   | `output` | 2    | ����ת������ָʾ                  |
| io_ptw_req_0_bits_getGpa    | `output` | 1    | �Ƿ�������GPA                  |
| io_ptw_req_1_valid          | `output` | 1    | PTW����ͨ��1��Ч                 |
| io_ptw_req_1_bits_vpn       | `output` | 38   | ���������ҳ�ţ�VPN��             |
| io_ptw_req_1_bits_s2xlate   | `output` | 2    | ����ת������ָʾ                  |
| io_ptw_req_1_bits_getGpa    | `output` | 1    | �Ƿ�������GPA                  |
| io_ptw_req_2_ready          | `input`  | 1    | PTW����ͨ��2����                 |
| io_ptw_req_2_valid          | `output` | 1    | PTW����ͨ��2��Ч                 |
| io_ptw_req_2_bits_vpn       | `output` | 38   | ���������ҳ�ţ�VPN��             |
| io_ptw_req_2_bits_s2xlate   | `output` | 2    | ����ת������ָʾ                  |
| io_ptw_req_2_bits_getGpa    | `output` | 1    | �Ƿ�������GPA                  |

### 9. PTW ��Ӧ�ӿڣ���1��ͨ����

| �ź���                             | ����     | λ�� | ����                              |
|------------------------------------|---------|------|-----------------------------------|
| io_ptw_resp_valid                  | `input` | 1    | PTW��Ӧ��Ч                      |
| io_ptw_resp_bits_s2xlate           | `input` | 2    | ����ת�����ͣ��ػ���             |
| **s1_entry ����ź�**              |         |      | **��һ��ת����Ӧ��Ϣ**               |
| io_ptw_resp_bits_s1_entry_tag      | `input` | 35   | ��ǩ��VPN��λ��                  |
| io_ptw_resp_bits_s1_entry_asid     | `input` | 16   | ASID                             |
| io_ptw_resp_bits_s1_entry_vmid     | `input` | 14   | VMID                             |
| io_ptw_resp_bits_s1_entry_n        | `input` | 1    | ��Ҷ�ӽڵ��־                   |
| io_ptw_resp_bits_s1_entry_pbmt     | `input` | 2    | �����ڴ汣������                 |
| io_ptw_resp_bits_s1_entry_perm_d   | `input` | 1    | ��λ��־��D��                   |
| io_ptw_resp_bits_s1_entry_perm_a   | `input` | 1    | ����λ��A��                      |
| io_ptw_resp_bits_s1_entry_perm_g   | `input` | 1    | ȫ��ӳ�䣨G��                    |
| io_ptw_resp_bits_s1_entry_perm_u   | `input` | 1    | �û�ģʽ����λ��U��              |
| io_ptw_resp_bits_s1_entry_perm_x   | `input` | 1    | ִ��λ��X��                      |
| io_ptw_resp_bits_s1_entry_perm_w   | `input` | 1    | дλ��W��                        |
| io_ptw_resp_bits_s1_entry_perm_r   | `input` | 1    | ��λ��R��                        |
| io_ptw_resp_bits_s1_entry_level    | `input` | 2    | ҳ����0-2��                   |
| io_ptw_resp_bits_s1_entry_v        | `input` | 1    | ҳ������Ч��־                   |
| io_ptw_resp_bits_s1_entry_ppn      | `input` | 41   | ����ҳ�ţ�PPN��                  |
| io_ptw_resp_bits_s1_addr_low       | `input` | 3    | �����ַ��λ��ҳ��ƫ�Ƹ�λ��      |
| io_ptw_resp_bits_s1_ppn_low_[0-7]  | `input` | 8��3  | PPN��λ��8�飩                  |
| io_ptw_resp_bits_s1_valididx_[0-7] | `input` | 8��1  | ҳ����������Ч�ԣ�λͼ��         |
| io_ptw_resp_bits_s1_pteidx_[0-7]   | `input` | 8��1  | ��ʵPTE������λͼ��             |
| io_ptw_resp_bits_s1_pf             | `input` | 1    | ��һ��ת��ȱҳ�����־         |
| io_ptw_resp_bits_s1_af             | `input` | 1    | ��һ��ת�����ʴ����־         |
| **s2_entry ����ź�**              |         |      | **�ڶ���ת����Ӧ��Ϣ**            |
| io_ptw_resp_bits_s2_entry_tag      | `input` | 38   | ��ǩ��GPA��λ��                 |
| io_ptw_resp_bits_s2_entry_vmid     | `input` | 14   | VMID                             |
| io_ptw_resp_bits_s2_entry_n        | `input` | 1    | ��Ҷ�ӽڵ��־                   |
| io_ptw_resp_bits_s2_entry_pbmt     | `input` | 2    | �����ڴ汣������                 |
| io_ptw_resp_bits_s2_entry_ppn      | `input` | 38   | ����ҳ�ţ�PPN��                  |
| io_ptw_resp_bits_s2_entry_perm_d   | `input` | 1    | ��λ��־��D��                   |
| io_ptw_resp_bits_s2_entry_perm_a   | `input` | 1    | ����λ��A��                      |
| io_ptw_resp_bits_s2_entry_perm_g   | `input` | 1    | ȫ��ӳ�䣨G��                    |
| io_ptw_resp_bits_s2_entry_perm_u   | `input` | 1    | �û�ģʽ����λ��U��              |
| io_ptw_resp_bits_s2_entry_perm_x   | `input` | 1    | ִ��λ��X��                      |
| io_ptw_resp_bits_s2_entry_perm_w   | `input` | 1    | дλ��W��                        |
| io_ptw_resp_bits_s2_entry_perm_r   | `input` | 1    | ��λ��R��                        |
| io_ptw_resp_bits_s2_entry_level    | `input` | 2    | ҳ����0-2��                   |
| io_ptw_resp_bits_s2_gpf            | `input` | 1    | �ڶ���ת���Ƿ�Ȩ�޴����־      |
| io_ptw_resp_bits_s2_gaf            | `input` | 1    | �ڶ���ת�����ʴ����־          |
| io_ptw_resp_bits_getGpa            | `input` | 1    | ��Ӧ���Ƿ����GPA              |

## ���������� Bundle ˵��

| **TLBWrapper** |                              |                     |
|----------------|------------------------------|---------------------|
|`clock`         |                              |                     |
|`ctrl`          | `reset`                      |                     |
|                | `io_sfence_valid`            |                     |
|                | `io_hartId`                  |                     |
|                | `io_requestor_2_resp_ready`  |                     |
|                | `io_requestor_2_resp_valid`  |                     |
|                | `io_ptw_req_0_valid`         |                     |
|                | `io_ptw_req_1_valid`         |                     |
|                | `io_ptw_req_2_ready`         |                     |
|                | `io_ptw_req_2_valid`         |                     |
|                | `io_ptw_resp_valid`          |                     |
|                | `io_ptw_resp_bits_s2xlate`   |                     |
|                | `io_ptw_resp_bits_getGpa`    |                     |
| `sfence`       | `rs1`                        |                     |
|                | `rs2`                        |                     |
|                | `addr`                       |                     |
|                | `id`                         |                     |
|                | `flushPipe`                  |                     |
|                | `hv`                         |                     |
|                | `hg`                         |                     |
| `csr`          | `satp`                       | `mode`              |
|                |                              | `asid`              |
|                |                              | `changed`           |
|                | `vsatp`                      | `mode`              |
|                |                              | `asid`              |
|                |                              | `changed`           |
|                | `hgatp`                      | `mode`              |
|                |                              | `vmid`              |
|                |                              | `changed`           |
|                | `priv`                       | `virt`              |
|                |                              | `imode`             |
| `requestor_0`  | `req`                        | `valid`             |
|                |                              | `bits_vaddr`        |
|                | `resp`                       | `paddr_0`           |
|                |                              | `gpaddr_0`          |
|                |                              | `pbmt_0`            |
|                |                              | `miss`              |
|                |                              | `idForVSnonLeafPTE` |
|                |                              | `excp_0_gpf_instr`  |
|                |                              | `excp_0_pf_instr`   |
|                |                              | `excp_0_af_instr`   |
| `requestor_1`  | `req`                        | `valid`             |
|                |                              | `bits_vaddr`        |
|                | `resp`                       | `paddr_0`           |
|                |                              | `gpaddr_0`          |
|                |                              | `pbmt_0`            |
|                |                              | `miss`              |
|                |                              | `idForVSnonLeafPTE` |
|                |                              | `excp_0_gpf_instr`  |
|                |                              | `excp_0_pf_instr`   |
|                |                              | `excp_0_af_instr`   |
| `requestor_0`  | `req`                        | `valid`             |
|                |                              | `ready`             |
|                |                              | `bits_vaddr`        |
|                | `resp`                       | `paddr_0`           |
|                |                              | `gpaddr_0`          |
|                |                              | `pbmt_0`            |
|                |                              | `miss`              |
|                |                              | `idForVSnonLeafPTE` |
|                |                              | `excp_0_gpf_instr`  |
|                |                              | `excp_0_pf_instr`   |
|                |                              | `excp_0_af_instr`   |
| `flushPipe[3]` |                              |                     |
| `ptw_req_0`    | `vpn`                        |                     |
|                | `s2xlate`                    |                     |
|                | `getGpa`                     |                     |
| `ptw_req_1`    | `vpn`                        |                     |
|                | `s2xlate`                    |                     |
|                | `getGpa`                     |                     |
| `ptw_req_2`    | `vpn`                        |                     |
|                | `s2xlate`                    |                     |
|                | `getGpa`                     |                     |
| `ptw_resp_s1`  | `entry_tag`                  |                     |
|                | `entry_asid`                 |                     |
|                | `entry_vmid`                 |                     |
|                | `entry_n`                    |                     |
|                | `entry_pbmt`                 |                     |
|                | `entry_perm_d`               |                     |
|                | `entry_perm_a`               |                     |
|                | `entry_perm_g`               |                     |
|                | `entry_perm_u`               |                     |
|                | `entry_perm_x`               |                     |
|                | `entry_perm_w`               |                     |
|                | `entry_perm_r`               |                     |
|                | `entry_level`                |                     |
|                | `entry_v`                    |                     |
|                | `entry_ppn`                  |                     |
|                | `addr_low`                   |                     |
|                | `ppn_low_0`                  |                     |
|                | `ppn_low_1`                  |                     |
|                | `ppn_low_2`                  |                     |
|                | `ppn_low_3`                  |                     |
|                | `ppn_low_4`                  |                     |
|                | `ppn_low_5`                  |                     |
|                | `ppn_low_6`                  |                     |
|                | `ppn_low_7`                  |                     |
|                | `valididx_0`                 |                     |
|                | `valididx_1`                 |                     |
|                | `valididx_2`                 |                     |
|                | `valididx_3`                 |                     |
|                | `valididx_4`                 |                     |
|                | `valididx_5`                 |                     |
|                | `valididx_6`                 |                     |
|                | `valididx_7`                 |                     |
|                | `pteidx_0`                   |                     |
|                | `pteidx_1`                   |                     |
|                | `pteidx_2`                   |                     |
|                | `pteidx_3`                   |                     |
|                | `pteidx_4`                   |                     |
|                | `pteidx_5`                   |                     |
|                | `pteidx_6`                   |                     |
|                | `pteidx_7`                   |                     |
|                | `pf`                         |                     |
|                | `af`                         |                     |
| `ptw_resp_s2`  | `entry_tag`                  |                     |
|                | `entry_vmid`                 |                     |
|                | `entry_n`                    |                     |
|                | `entry_pbmt`                 |                     |
|                | `entry_ppn`                  |                     |
|                | `entry_perm_d`               |                     |
|                | `entry_perm_a`               |                     |
|                | `entry_perm_g`               |                     |
|                | `entry_perm_u`               |                     |
|                | `entry_perm_x`               |                     |
|                | `entry_perm_w`               |                     |
|                | `entry_perm_r`               |                     |
|                | `entry_level`                |                     |
|                | `gpf`                        |                     |
|                | `gaf`                        |                     |

## ��������������ʽ�����㸴��ճ����

```python
def test_TODO(tlb_fixture):
    """
    Func: TODO
        subfunc1: TODO
    """
    # connect to fixture
    tlb = tlb_fixture
    # add watch point
    case_name = inspect.currentframe().f_back.f_code.co_name
    g.add_watch_point(tlb.TODO, {
                        "TODO": fc.Eq(TODO),
                        "TODO": lambda TODO: TODO.value == TODO,
    }, name = f"{case_name}: TODO")
    # set default value
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(TODO):
        # add signal and assign to dut

        # step to next cycle
        tlb.dut.Step(2)

        # assert result
```
