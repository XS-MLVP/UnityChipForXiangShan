# **Translation Lookaside Buffer (TLB)**

## 一、TLB IO 信号总表

### 1. 全局控制信号

| 信号名        | 方向     | 位宽 | 描述                        |
|---------------|---------|------|-----------------------------|
| clock         | `input` | 1    | 时钟信号，驱动 TLB 的时序逻辑 |
| reset         | `input` | 1    | 复位信号，用于重置 TLB 的状态 |
| io_hartId     | `input` | 6    | 硬件线程ID                  |

### 2. SFENCE 指令接口信号

| 信号名                          | 方向     | 位宽 | 描述                                 |
|---------------------------------|---------|------|--------------------------------------|
| io_sfence_valid                 | `input` | 1    | SFENCE操作有效信号                    |
| io_sfence_bits_rs1              | `input` | 1    | 指示是否使用寄存器rs1的值（地址）      |
| io_sfence_bits_rs2              | `input` | 1    | 指示是否使用寄存器rs2的值（ASID）      |
| io_sfence_bits_addr             | `input` | 50   | SFENCE操作指定要刷新的虚拟地址，用于选择性刷新特定地址的 TLB 条目 |
| io_sfence_bits_id               | `input` | 16   | SFENCE操作指定要刷新的ASID，用于选择性刷新特定地址空间的 TLB 条目 |
| io_sfence_bits_flushPipe        | `input` | 1    | 指示当前 SFENCE 操作是否刷新流水线      |
| io_sfence_bits_hv               | `input` | 1    | 是否在Hypervisor模式下执行SFENCE       |
| io_sfence_bits_hg               | `input` | 1    | 是否在Hypervisor guest模式下执行SFENCE |

### 3. CSR 寄存器输入

| 信号名                          | 方向     | 位宽 | 描述                               |
|---------------------------------|---------|------|-----------------------------------|
| io_csr_satp_mode                | `input` | 4    | SATP寄存器模式位                   |
| io_csr_satp_asid                | `input` | 16   | SATP寄存器ASID                    |
| io_csr_satp_ppn                 | `input` | 44   | SATP寄存器PPN                     |
| io_csr_satp_changed             | `input` | 1    | SATP寄存器是否发生变化             |
| io_csr_vsatp_mode               | `input` | 4    | VSATP寄存器模式位（虚拟化）        |
| io_csr_vsatp_asid               | `input` | 16   | VSATP寄存器ASID                   |
| io_csr_vsatp_ppn                | `input` | 44   | VSATP寄存器PPN                    |
| io_csr_vsatp_changed            | `input` | 1    | VSATP寄存器是否发生变化            |
| io_csr_hgatp_mode               | `input` | 4    | HGATP寄存器模式位（虚拟化）        |
| io_csr_hgatp_vmid               | `input` | 16   | HGATP寄存器VMID                   |
| io_csr_hgatp_ppn                | `input` | 44   | HGATP寄存器PPN                    |
| io_csr_hgatp_changed            | `input` | 1    | HGATP寄存器是否发生变化            |
| io_csr_priv_virt                | `input` | 1    | 虚拟化使能信号                     |
| io_csr_priv_imode               | `input` | 2    | 当前特权模式（00：U, 01：S, 11：M） |

### 4. 请求与响应接口（Requestor 0）

| 信号名                                     | 方向      | 位宽 | 描述                            |
|--------------------------------------------|----------|------|--------------------------------|
| io_requestor_0_req_valid                   | `input`  | 1    | 请求0有效                       |
| io_requestor_0_req_bits_vaddr              | `input`  | 50   | 请求0的虚拟地址                  |
| io_requestor_0_resp_bits_paddr_0           | `output` | 48   | 响应0的物理地址                  |
| io_requestor_0_resp_bits_gpaddr_0          | `output` | 64   | 响应0的虚拟化物理地址            |
| io_requestor_0_resp_bits_pbmt_0            | `output` | 2    | 响应0的物理内存保护类型          |
| io_requestor_0_resp_bits_miss              | `output` | 1    | 响应0是否TLB缺失                |
| io_requestor_0_resp_bits_isForVSnonLeafPTE | `output` | 1    | 响应0是否为虚拟机非叶子PTE       |
| io_requestor_0_resp_bits_excp_0_gpf_instr  | `output` | 1    | 指令0的虚拟化缺页异常            |
| io_requestor_0_resp_bits_excp_0_pf_instr   | `output` | 1    | 指令0的缺页异常                 |
| io_requestor_0_resp_bits_excp_0_af_instr   | `output` | 1    | 指令0的访问权限异常              |

### 5. 请求与响应接口（Requestor 1）

| 信号名                                     | 方向      | 位宽 | 描述                            |
|--------------------------------------------|----------|------|---------------------------------|
| io_requestor_1_req_valid                   | `input`  | 1    | 请求1有效                        |
| io_requestor_1_req_bits_vaddr              | `input`  | 50   | 请求1的虚拟地址                  |
| io_requestor_1_resp_bits_paddr_0           | `output` | 48   | 响应1的物理地址                  |
| io_requestor_1_resp_bits_gpaddr_0          | `output` | 64   | 响应1的虚拟化物理地址            |
| io_requestor_1_resp_bits_pbmt_0            | `output` | 2    | 响应1的物理内存保护类型          |
| io_requestor_1_resp_bits_miss              | `output` | 1    | 响应1是否TLB缺失                |
| io_requestor_1_resp_bits_isForVSnonLeafPTE | `output` | 1    | 响应1是否为虚拟机非叶子PTE       |
| io_requestor_1_resp_bits_excp_0_gpf_instr  | `output` | 1    | 数据访问0的虚拟化缺页异常        |
| io_requestor_1_resp_bits_excp_0_pf_instr   | `output` | 1    | 数据访问0的缺页异常              |
| io_requestor_1_resp_bits_excp_0_af_instr   | `output` | 1    | 数据访问0的访问权限异常          |

### 6. 请求与响应接口（Requestor 2）

| 信号名                                      | 方向     | 位宽 | 描述                         |
|--------------------------------------------|----------|----|--------------------------------|
| io_requestor_2_req_ready                   | `output` | 1  | 请求2就绪信号                   |
| io_requestor_2_req_valid                   | `input`  | 1  | 请求2有效                      |
| io_requestor_2_req_bits_vaddr              | `input`  | 50 | 请求2的虚拟地址                 |
| io_requestor_2_resp_ready                  | `input`  | 1  | 响应2就绪信号                   |
| io_requestor_2_resp_valid                  | `output` | 1  | 响应2有效                       |
| io_requestor_2_resp_bits_paddr_0           | `output` | 48 | 响应2的物理地址                 |
| io_requestor_2_resp_bits_gpaddr_0          | `output` | 64 | 响应2的虚拟化物理地址           |
| io_requestor_2_resp_bits_pbmt_0            | `output` | 2  | 响应2的物理内存保护类型         |
| io_requestor_2_resp_bits_miss              | `output` | 1  | 响应2是否TLB缺失               |
| io_requestor_2_resp_bits_isForVSnonLeafPTE | `output` | 1  | 响应2是否为虚拟机非叶子PTE      |
| io_requestor_2_resp_bits_excp_0_gpf_instr  | `output` | 1  | PTW访问的虚拟化缺页异常         |
| io_requestor_2_resp_bits_excp_0_pf_instr   | `output` | 1  | PTW访问的缺页异常               |
| io_requestor_2_resp_bits_excp_0_af_instr   | `output` | 1  | PTW访问的访问权限异常           |

### 7. 流水线刷新信号（来自外部）

| 信号名                | 方向     | 位宽 | 描述           |
|-----------------------|---------|------|---------------|
| io_flushPipe_0        | `input` | 1    | 刷新流水线 0   |
| io_flushPipe_1        | `input` | 1    | 刷新流水线 1   |
| io_flushPipe_2        | `input` | 1    | 刷新流水线 2   |

### 8. PTW 请求接口（共3个通道）

| 信号名                      | 方向      | 位宽 | 描述                              |
|-----------------------------|----------|------|----------------------------------|
| io_ptw_req_0_valid          | `output` | 1    | PTW请求通道0有效                 |
| io_ptw_req_0_bits_vpn       | `output` | 38   | 请求的虚拟页号（VPN）             |
| io_ptw_req_0_bits_s2xlate   | `output` | 2    | 二级转换类型指示                  |
| io_ptw_req_0_bits_getGpa    | `output` | 1    | 是否请求获得GPA                  |
| io_ptw_req_1_valid          | `output` | 1    | PTW请求通道1有效                 |
| io_ptw_req_1_bits_vpn       | `output` | 38   | 请求的虚拟页号（VPN）             |
| io_ptw_req_1_bits_s2xlate   | `output` | 2    | 二级转换类型指示                  |
| io_ptw_req_1_bits_getGpa    | `output` | 1    | 是否请求获得GPA                  |
| io_ptw_req_2_ready          | `input`  | 1    | PTW请求通道2就绪                 |
| io_ptw_req_2_valid          | `output` | 1    | PTW请求通道2有效                 |
| io_ptw_req_2_bits_vpn       | `output` | 38   | 请求的虚拟页号（VPN）             |
| io_ptw_req_2_bits_s2xlate   | `output` | 2    | 二级转换类型指示                  |
| io_ptw_req_2_bits_getGpa    | `output` | 1    | 是否请求获得GPA                  |

### 9. PTW 响应接口（共1个通道）

| 信号名                             | 方向     | 位宽 | 描述                              |
|------------------------------------|---------|------|-----------------------------------|
| io_ptw_resp_valid                  | `input` | 1    | PTW响应有效                      |
| io_ptw_resp_bits_s2xlate           | `input` | 2    | 二级转换类型（回环）             |
| **s1_entry 相关信号**              |         |      | **第一级转换响应信息**               |
| io_ptw_resp_bits_s1_entry_tag      | `input` | 35   | 标签（VPN高位）                  |
| io_ptw_resp_bits_s1_entry_asid     | `input` | 16   | ASID                             |
| io_ptw_resp_bits_s1_entry_vmid     | `input` | 14   | VMID                             |
| io_ptw_resp_bits_s1_entry_n        | `input` | 1    | 非叶子节点标志                   |
| io_ptw_resp_bits_s1_entry_pbmt     | `input` | 2    | 物理内存保护类型                 |
| io_ptw_resp_bits_s1_entry_perm_d   | `input` | 1    | 脏位标志（D）                   |
| io_ptw_resp_bits_s1_entry_perm_a   | `input` | 1    | 访问位（A）                      |
| io_ptw_resp_bits_s1_entry_perm_g   | `input` | 1    | 全局映射（G）                    |
| io_ptw_resp_bits_s1_entry_perm_u   | `input` | 1    | 用户模式访问位（U）              |
| io_ptw_resp_bits_s1_entry_perm_x   | `input` | 1    | 执行位（X）                      |
| io_ptw_resp_bits_s1_entry_perm_w   | `input` | 1    | 写位（W）                        |
| io_ptw_resp_bits_s1_entry_perm_r   | `input` | 1    | 读位（R）                        |
| io_ptw_resp_bits_s1_entry_level    | `input` | 2    | 页表级（0-2）                   |
| io_ptw_resp_bits_s1_entry_v        | `input` | 1    | 页表项有效标志                   |
| io_ptw_resp_bits_s1_entry_ppn      | `input` | 41   | 物理页号（PPN）                  |
| io_ptw_resp_bits_s1_addr_low       | `input` | 3    | 虚拟地址低位（页内偏移高位）      |
| io_ptw_resp_bits_s1_ppn_low_[0-7]  | `input` | 8×3  | PPN低位（8组）                  |
| io_ptw_resp_bits_s1_valididx_[0-7] | `input` | 8×1  | 页表项索引有效性（位图）         |
| io_ptw_resp_bits_s1_pteidx_[0-7]   | `input` | 8×1  | 真实PTE索引（位图）             |
| io_ptw_resp_bits_s1_pf             | `input` | 1    | 第一级转换缺页错误标志         |
| io_ptw_resp_bits_s1_af             | `input` | 1    | 第一级转换访问错误标志         |
| **s2_entry 相关信号**              |         |      | **第二级转换响应信息**            |
| io_ptw_resp_bits_s2_entry_tag      | `input` | 38   | 标签（GPA高位）                 |
| io_ptw_resp_bits_s2_entry_vmid     | `input` | 14   | VMID                             |
| io_ptw_resp_bits_s2_entry_n        | `input` | 1    | 非叶子节点标志                   |
| io_ptw_resp_bits_s2_entry_pbmt     | `input` | 2    | 物理内存保护类型                 |
| io_ptw_resp_bits_s2_entry_ppn      | `input` | 38   | 物理页号（PPN）                  |
| io_ptw_resp_bits_s2_entry_perm_d   | `input` | 1    | 脏位标志（D）                   |
| io_ptw_resp_bits_s2_entry_perm_a   | `input` | 1    | 访问位（A）                      |
| io_ptw_resp_bits_s2_entry_perm_g   | `input` | 1    | 全局映射（G）                    |
| io_ptw_resp_bits_s2_entry_perm_u   | `input` | 1    | 用户模式访问位（U）              |
| io_ptw_resp_bits_s2_entry_perm_x   | `input` | 1    | 执行位（X）                      |
| io_ptw_resp_bits_s2_entry_perm_w   | `input` | 1    | 写位（W）                        |
| io_ptw_resp_bits_s2_entry_perm_r   | `input` | 1    | 读位（R）                        |
| io_ptw_resp_bits_s2_entry_level    | `input` | 2    | 页表级（0-2）                   |
| io_ptw_resp_bits_s2_gpf            | `input` | 1    | 第二级转换非法权限错误标志      |
| io_ptw_resp_bits_s2_gaf            | `input` | 1    | 第二级转换访问错误标志          |
| io_ptw_resp_bits_getGpa            | `input` | 1    | 响应中是否包含GPA              |

## 二、测试用 Bundle 说明

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

## 三、测试用例格式（方便复制粘贴）

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
