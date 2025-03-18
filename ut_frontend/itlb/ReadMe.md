# **Translation Lookaside Buffer (TLB)**

## 一、TLB.sv 接口说明

### 基本控制信号

1. **`clock`**: 时钟信号，驱动 TLB 的时序逻辑。
2. **`reset`**: 复位信号，用于重置 TLB 的状态。

### 刷新（SFENCE）接口信号

这些信号与 TLB 的刷新操作相关，当页表被修改时，这些信号用于通知 TLB 刷新其内容。

3. **`io_sfence_valid`**: 表示 SFENCE 操作的有效性。
4. **`io_sfence_bits_rs1`**: 表示 SFENCE 操作是否使用寄存器 rs1 的值。
5. **`io_sfence_bits_rs2`**: 表示 SFENCE 操作是否使用寄存器 rs2 的值。
6. **`io_sfence_bits_addr`**: SFENCE 操作指定的地址，用于选择性刷新特定地址的 TLB 条目。
7. **`io_sfence_bits_id`**: 标识符，用于区分不同的刷新操作。
8. **`io_sfence_bits_flushPipe`**: 请求刷新整个管道（Pipeline）。
9. **`io_sfence_bits_hv`**: 代表是否是 Hypervisor 模式下的 SFENCE 操作。
10. **`io_sfence_bits_hg`**: 代表是否是 Guest 模式下的 SFENCE 操作。

### 控制与状态寄存器（CSR）接口信号

这些信号与 TLB 的控制与状态寄存器（CSR）配置相关。

11. **`io_csr_satp_mode`**: SATP 寄存器的模式字段（如裸模式、Sv32、Sv39 等）。
12. **`io_csr_satp_asid`**: 当前 SATP 寄存器的 ASID（地址空间标识符）。
13. **`io_csr_satp_changed`**: 指示 SATP 寄存器的值是否已更改。
14. **`io_csr_vsatp_mode`**: VSATP 寄存器的模式字段。
15. **`io_csr_vsatp_asid`**: VSATP 寄存器的 ASID。
16. **`io_csr_vsatp_changed`**: 指示 VSATP 寄存器的值是否已更改。
17. **`io_csr_hgatp_mode`**: HGATP 寄存器的模式字段。
18. **`io_csr_hgatp_vmid`**: HGATP 寄存器的 VMID（虚拟机标识符）。
19. **`io_csr_hgatp_changed`**: 指示 HGATP 寄存器的值是否已更改。
20. **`io_csr_priv_virt`**: 是否在虚拟模式下运行。
21. **`io_csr_priv_imode`**: 指令模式的特权级（如用户态、内核态等）。

### 请求者（Requestor）接口信号

这些信号用于与处理器或其他模块之间的请求与响应操作。

#### Requestor 0 信号

22. **`io_requestor_0_req_valid`**: 请求者 0 的请求有效信号。
23. **`io_requestor_0_req_bits_vaddr`**: 请求者 0 的请求虚拟地址（vaddr）。
24. **`io_requestor_0_resp_bits_paddr_0`**: 请求者 0 的物理地址（paddr）响应信号。
25. **`io_requestor_0_resp_bits_gpaddr_0`**: 请求者 0 的物理地址转换为 GPA（Guest Physical Address）的响应信号。
26. **`io_requestor_0_resp_bits_miss`**: 请求者 0 请求的地址未命中的信号。
27. **`io_requestor_0_resp_bits_excp_0_gpf_instr`**: 请求者 0 出现 General Protection Fault (GPF) 异常的信号。
28. **`io_requestor_0_resp_bits_excp_0_pf_instr`**: 请求者 0 出现 Page Fault (PF) 异常的信号。
29. **`io_requestor_0_resp_bits_excp_0_af_instr`**: 请求者 0 出现 Access Fault (AF) 异常的信号。

#### Requestor 1 信号

30. **`io_requestor_1_req_valid`**: 请求者 1 的请求有效信号。
31. **`io_requestor_1_req_bits_vaddr`**: 请求者 1 的请求虚拟地址。
32. **`io_requestor_1_resp_bits_paddr_0`**: 请求者 1 的物理地址响应信号。
33. **`io_requestor_1_resp_bits_gpaddr_0`**: 请求者 1 的 GPA 响应信号。
34. **`io_requestor_1_resp_bits_miss`**: 请求者 1 的未命中信号。
35. **`io_requestor_1_resp_bits_excp_0_gpf_instr`**: 请求者 1 出现 GPF 异常的信号。
36. **`io_requestor_1_resp_bits_excp_0_pf_instr`**: 请求者 1 出现 PF 异常的信号。
37. **`io_requestor_1_resp_bits_excp_0_af_instr`**: 请求者 1 出现 AF 异常的信号。

#### Requestor 2 信号

38. **`io_requestor_2_req_ready`**: 请求者 2 的请求就绪信号。
39. **`io_requestor_2_req_valid`**: 请求者 2 的请求有效信号。
40. **`io_requestor_2_req_bits_vaddr`**: 请求者 2 的请求虚拟地址。
41. **`io_requestor_2_resp_ready`**: 请求者 2 的响应就绪信号。
42. **`io_requestor_2_resp_valid`**: 请求者 2 的响应有效信号。
43. **`io_requestor_2_resp_bits_paddr_0`**: 请求者 2 的物理地址响应信号。
44. **`io_requestor_2_resp_bits_gpaddr_0`**: 请求者 2 的 GPA 响应信号。
45. **`io_requestor_2_resp_bits_excp_0_gpf_instr`**: 请求者 2 出现 GPF 异常的信号。
46. **`io_requestor_2_resp_bits_excp_0_pf_instr`**: 请求者 2 出现 PF 异常的信号。
47. **`io_requestor_2_resp_bits_excp_0_af_instr`**: 请求者 2 出现 AF 异常的信号。

### 刷新管道（Flush Pipe）信号

这些信号用于通知 TLB 刷新请求。

48. **`io_flushPipe_0`**: 刷新管道 0 的信号。
49. **`io_flushPipe_1`**: 刷新管道 1 的信号。
50. **`io_flushPipe_2`**: 刷新管道 2 的信号。

### 页表遍历（Page Table Walker, PTW）接口信号

这些信号用于与页表遍历单元（PTW）的交互，处理 TLB 未命中的情况。

#### PTW 请求信号

51. **`io_ptw_req_0_valid`**: PTW 请求 0 有效信号。
52. **`io_ptw_req_0_bits_vpn`**: PTW 请求 0 的虚拟页号（VPN）。
53. **`io_ptw_req_0_bits_s2xlate`**: PTW 请求 0 的 S2 转换位。
54. **`io_ptw_req_0_bits_getGpa`**: PTW 请求 0 的获取 GPA 信号。
55. **`io_ptw_req_1_valid`**: PTW 请求 1 有效信号。
56. **`io_ptw_req_1_bits_vpn`**: PTW 请求 1 的虚拟页号。
57. **`io_ptw_req_1_bits_s2xlate`**: PTW 请求 1 的 S2 转换位。
58. **`io_ptw_req_1_bits_getGpa`**: PTW 请求 1 的获取 GPA 信号。
59. **`io_ptw_req_2_ready`**: PTW 请求 2 就绪信号。
60. **`io_ptw_req_2_valid`**: PTW 请求 2 有效信号。
61. **`io_ptw_req_2_bits_vpn`**: PTW 请求 2 的虚拟页号。
62. **`io_ptw_req_2_bits_s2xlate`**: PTW 请求 2 的 S2 转换位。
63. **`io_ptw_req_2_bits_getGpa`**: PTW 请求 2 的获取 GPA 信号。

#### PTW 响应信号

64. **`io_ptw_resp_valid`**: PTW 响应有效信号。
65. **`io_ptw_resp_bits_s2xlate`**: PTW 响应的 S2 转换位。
66. **`io_ptw_resp_bits_s1_entry_tag`**: PTW 响应的第一级页表条目标签。
67. **`io_ptw_resp_bits_s1_entry_asid`**: PTW 响应的第一级页表条目 ASID。
68. **`io_ptw_resp_bits_s1_entry_vmid`**: PTW 响应的第一级页表条目 VMID。
69. **`io_ptw_resp_bits_s1_entry_perm_d`**: PTW 响应的第一级页表条目可写位。
70. **`io_ptw_resp_bits_s1_entry_perm_a`**: PTW 响应的第一级页表条目已访问位。
71. **`io_ptw_resp_bits_s1_entry_perm_g`**: PTW 响应的第一级页表条目全局位。
72. **`io_ptw_resp_bits_s1_entry_perm_u`**: PTW 响应的第一级页表条目用户模式位。
73. **`io_ptw_resp_bits_s1_entry_perm_x`**: PTW 响应的第一级页表条目可执行位。
74. **`io_ptw_resp_bits_s1_entry_perm_w`**: PTW 响应的第一级页表条目可写位。
75. **`io_ptw_resp_bits_s1_entry_perm_r`**: PTW 响应的第一级页表条目可读位。
76. **`io_ptw_resp_bits_s1_entry_level`**: PTW 响应的第一级页表条目级别。
77. **`io_ptw_resp_bits_s1_entry_ppn`**: PTW 响应的第一级页表条目物理页号（PPN）。
78. **`io_ptw_resp_bits_s1_addr_low`**: PTW 响应的第一级页表条目地址低位。
79. **`io_ptw_resp_bits_s1_ppn_low_*`**: PTW 响应的第一级页表条目 PPN 低位。
80. **`io_ptw_resp_bits_s1_valididx_*`**: PTW 响应的第一级页表条目有效索引。
81. **`io_ptw_resp_bits_s1_pteidx_*`**: PTW 响应的第一级页表条目 PTE 索引。
82. **`io_ptw_resp_bits_s1_pf`**: PTW 响应的第一级页表条目页错误信号。
83. **`io_ptw_resp_bits_s1_af`**: PTW 响应的第一级页表条目访问错误信号。
84. **`io_ptw_resp_bits_s2_entry_tag`**: PTW 响应的第二级页表条目标签。
85. **`io_ptw_resp_bits_s2_entry_vmid`**: PTW 响应的第二级页表条目 VMID。
86. **`io_ptw_resp_bits_s2_entry_ppn`**: PTW 响应的第二级页表条目 PPN。
87. **`io_ptw_resp_bits_s2_entry_perm_*`**: PTW 响应的第二级页表条目的权限位。
88. **`io_ptw_resp_bits_s2_entry_level`**: PTW 响应的第二级页表条目级别。
89. **`io_ptw_resp_bits_s2_gpf`**: PTW 响应的第二级页表条目 GPF 信号。
90. **`io_ptw_resp_bits_s2_gaf`**: PTW 响应的第二级页表条目 GAF 信号。
91. **`io_ptw_resp_bits_getGpa`**: PTW 响应的获取 GPA 信号。

## 二、测试用 Bundle 说明

- **`TLBWrapper`**
    - `clock`
    - `ctrl`
        - `reset`
        - `io_sfence_valid`
        - `io_requestor_2_resp_ready`
        - `io_requestor_2_resp_valid`
        - `io_ptw_req_0_valid`
        - `io_ptw_req_1_valid`
        - `io_ptw_req_2_ready`
        - `io_ptw_req_2_valid`
        - `io_ptw_resp_valid`
        - `io_ptw_resp_bits_s2xlate`
        - `io_ptw_resp_bits_getGpa`
    - `sfence`
        - `rs1`
        - `rs2`
        - `addr`
        - `id`
        - `flushPipe`
        - `hv`
        - `hg`
    - `csr`
        - `satp`
            - `mode`
            - `asid`
            - `changed`
        - `vsatp`
            - `mode`
            - `asid`
            - `changed`
        - `hgatp`
            - `mode`
            - `vmid`
            - `changed`
        - `priv`
            - `virt`
            - `imode`
    - `requestor_0`
        - `req`
            - `valid`
            - `bits_vaddr`
        - `resp`
            - `paddr_0`
            - `gpaddr_0`
            - `miss`
            - `excp_0_gpf_instr`
            - `excp_0_pf_instr`
            - `excp_0_af_instr`
    - `requestor_1`
        - `req`
            - `valid`
            - `bits_vaddr`
        - `resp`
            - `paddr_0`
            - `gpaddr_0`
            - `miss`
            - `excp_0_gpf_instr`
            - `excp_0_pf_instr`
            - `excp_0_af_instr`
    - `requestor_2`
        - `req`
            - `valid`
            - `ready`
            - `bits_vaddr`
        - `resp`
            - `paddr_0`
            - `gpaddr_0`
            - `excp_0_gpf_instr`
            - `excp_0_pf_instr`
            - `excp_0_af_instr`
    - `flushPipe[3]`
    - `ptw_req_0`
        - `vpn`
        - `s2xlate`
        - `getGpa`
    - `ptw_req_1`
        - `vpn`
        - `s2xlate`
        - `getGpa`
    - `ptw_req_2`
        - `vpn`
        - `s2xlate`
        - `getGpa`
    - `ptw_resp_s1`
        - `entry_tag`
        - `entry_asid`
        - `entry_vmid`
        - `entry_perm_*`
        - `entry_level`
        - `entry_ppn`
        - `addr_low`
        - `ppn_low_*`
        - `valididx_*`
        - `pteidx_*`
        - `pf`
        - `af`
    - `ptw_resp_s2`
        - `entry_tag`
        - `entry_vmid`
        - `entry_perm_*`
        - `entry_level`
        - `gpf`
        - `gaf`

## 三、测试用例格式（方便复制粘贴）

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
