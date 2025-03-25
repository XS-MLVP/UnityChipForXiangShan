# **Translation Lookaside Buffer (TLB)**

## һ��TLB.sv �ӿ�˵��

### ���������ź�

1. **`clock`**: ʱ���źţ����� TLB ��ʱ���߼���
2. **`reset`**: ��λ�źţ��������� TLB ��״̬��

### ˢ�£�SFENCE���ӿ��ź�

��Щ�ź��� TLB ��ˢ�²�����أ���ҳ���޸�ʱ����Щ�ź�����֪ͨ TLB ˢ�������ݡ�

3. **`io_sfence_valid`**: ��ʾ SFENCE ��������Ч�ԡ�
4. **`io_sfence_bits_rs1`**: ��ʾ SFENCE �����Ƿ�ʹ�üĴ��� rs1 ��ֵ��
5. **`io_sfence_bits_rs2`**: ��ʾ SFENCE �����Ƿ�ʹ�üĴ��� rs2 ��ֵ��
6. **`io_sfence_bits_addr`**: SFENCE ����ָ���ĵ�ַ������ѡ����ˢ���ض���ַ�� TLB ��Ŀ��
7. **`io_sfence_bits_id`**: ��ʶ�����������ֲ�ͬ��ˢ�²�����
8. **`io_sfence_bits_flushPipe`**: ����ˢ�������ܵ���Pipeline����
9. **`io_sfence_bits_hv`**: �����Ƿ��� Hypervisor ģʽ�µ� SFENCE ������
10. **`io_sfence_bits_hg`**: �����Ƿ��� Guest ģʽ�µ� SFENCE ������

### ������״̬�Ĵ�����CSR���ӿ��ź�

��Щ�ź��� TLB �Ŀ�����״̬�Ĵ�����CSR��������ء�

11. **`io_csr_satp_mode`**: SATP �Ĵ�����ģʽ�ֶΣ�����ģʽ��Sv32��Sv39 �ȣ���
12. **`io_csr_satp_asid`**: ��ǰ SATP �Ĵ����� ASID����ַ�ռ��ʶ������
13. **`io_csr_satp_changed`**: ָʾ SATP �Ĵ�����ֵ�Ƿ��Ѹ��ġ�
14. **`io_csr_vsatp_mode`**: VSATP �Ĵ�����ģʽ�ֶΡ�
15. **`io_csr_vsatp_asid`**: VSATP �Ĵ����� ASID��
16. **`io_csr_vsatp_changed`**: ָʾ VSATP �Ĵ�����ֵ�Ƿ��Ѹ��ġ�
17. **`io_csr_hgatp_mode`**: HGATP �Ĵ�����ģʽ�ֶΡ�
18. **`io_csr_hgatp_vmid`**: HGATP �Ĵ����� VMID���������ʶ������
19. **`io_csr_hgatp_changed`**: ָʾ HGATP �Ĵ�����ֵ�Ƿ��Ѹ��ġ�
20. **`io_csr_priv_virt`**: �Ƿ�������ģʽ�����С�
21. **`io_csr_priv_imode`**: ָ��ģʽ����Ȩ�������û�̬���ں�̬�ȣ���

### �����ߣ�Requestor���ӿ��ź�

��Щ�ź������봦����������ģ��֮�����������Ӧ������

#### Requestor 0 �ź�

22. **`io_requestor_0_req_valid`**: ������ 0 ��������Ч�źš�
23. **`io_requestor_0_req_bits_vaddr`**: ������ 0 �����������ַ��vaddr����
24. **`io_requestor_0_resp_bits_paddr_0`**: ������ 0 �������ַ��paddr����Ӧ�źš�
25. **`io_requestor_0_resp_bits_gpaddr_0`**: ������ 0 �������ַת��Ϊ GPA��Guest Physical Address������Ӧ�źš�
26. **`io_requestor_0_resp_bits_miss`**: ������ 0 ����ĵ�ַδ���е��źš�
27. **`io_requestor_0_resp_bits_excp_0_gpf_instr`**: ������ 0 ���� General Protection Fault (GPF) �쳣���źš�
28. **`io_requestor_0_resp_bits_excp_0_pf_instr`**: ������ 0 ���� Page Fault (PF) �쳣���źš�
29. **`io_requestor_0_resp_bits_excp_0_af_instr`**: ������ 0 ���� Access Fault (AF) �쳣���źš�

#### Requestor 1 �ź�

30. **`io_requestor_1_req_valid`**: ������ 1 ��������Ч�źš�
31. **`io_requestor_1_req_bits_vaddr`**: ������ 1 �����������ַ��
32. **`io_requestor_1_resp_bits_paddr_0`**: ������ 1 �������ַ��Ӧ�źš�
33. **`io_requestor_1_resp_bits_gpaddr_0`**: ������ 1 �� GPA ��Ӧ�źš�
34. **`io_requestor_1_resp_bits_miss`**: ������ 1 ��δ�����źš�
35. **`io_requestor_1_resp_bits_excp_0_gpf_instr`**: ������ 1 ���� GPF �쳣���źš�
36. **`io_requestor_1_resp_bits_excp_0_pf_instr`**: ������ 1 ���� PF �쳣���źš�
37. **`io_requestor_1_resp_bits_excp_0_af_instr`**: ������ 1 ���� AF �쳣���źš�

#### Requestor 2 �ź�

38. **`io_requestor_2_req_ready`**: ������ 2 ����������źš�
39. **`io_requestor_2_req_valid`**: ������ 2 ��������Ч�źš�
40. **`io_requestor_2_req_bits_vaddr`**: ������ 2 �����������ַ��
41. **`io_requestor_2_resp_ready`**: ������ 2 ����Ӧ�����źš�
42. **`io_requestor_2_resp_valid`**: ������ 2 ����Ӧ��Ч�źš�
43. **`io_requestor_2_resp_bits_paddr_0`**: ������ 2 �������ַ��Ӧ�źš�
44. **`io_requestor_2_resp_bits_gpaddr_0`**: ������ 2 �� GPA ��Ӧ�źš�
45. **`io_requestor_2_resp_bits_excp_0_gpf_instr`**: ������ 2 ���� GPF �쳣���źš�
46. **`io_requestor_2_resp_bits_excp_0_pf_instr`**: ������ 2 ���� PF �쳣���źš�
47. **`io_requestor_2_resp_bits_excp_0_af_instr`**: ������ 2 ���� AF �쳣���źš�

### ˢ�¹ܵ���Flush Pipe���ź�

��Щ�ź�����֪ͨ TLB ˢ������

48. **`io_flushPipe_0`**: ˢ�¹ܵ� 0 ���źš�
49. **`io_flushPipe_1`**: ˢ�¹ܵ� 1 ���źš�
50. **`io_flushPipe_2`**: ˢ�¹ܵ� 2 ���źš�

### ҳ�������Page Table Walker, PTW���ӿ��ź�

��Щ�ź�������ҳ�������Ԫ��PTW���Ľ��������� TLB δ���е������

#### PTW �����ź�

51. **`io_ptw_req_0_valid`**: PTW ���� 0 ��Ч�źš�
52. **`io_ptw_req_0_bits_vpn`**: PTW ���� 0 ������ҳ�ţ�VPN����
53. **`io_ptw_req_0_bits_s2xlate`**: PTW ���� 0 �� S2 ת��λ��
54. **`io_ptw_req_0_bits_getGpa`**: PTW ���� 0 �Ļ�ȡ GPA �źš�
55. **`io_ptw_req_1_valid`**: PTW ���� 1 ��Ч�źš�
56. **`io_ptw_req_1_bits_vpn`**: PTW ���� 1 ������ҳ�š�
57. **`io_ptw_req_1_bits_s2xlate`**: PTW ���� 1 �� S2 ת��λ��
58. **`io_ptw_req_1_bits_getGpa`**: PTW ���� 1 �Ļ�ȡ GPA �źš�
59. **`io_ptw_req_2_ready`**: PTW ���� 2 �����źš�
60. **`io_ptw_req_2_valid`**: PTW ���� 2 ��Ч�źš�
61. **`io_ptw_req_2_bits_vpn`**: PTW ���� 2 ������ҳ�š�
62. **`io_ptw_req_2_bits_s2xlate`**: PTW ���� 2 �� S2 ת��λ��
63. **`io_ptw_req_2_bits_getGpa`**: PTW ���� 2 �Ļ�ȡ GPA �źš�

#### PTW ��Ӧ�ź�

64. **`io_ptw_resp_valid`**: PTW ��Ӧ��Ч�źš�
65. **`io_ptw_resp_bits_s2xlate`**: PTW ��Ӧ�� S2 ת��λ��
66. **`io_ptw_resp_bits_s1_entry_tag`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ��ǩ��
67. **`io_ptw_resp_bits_s1_entry_asid`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ ASID��
68. **`io_ptw_resp_bits_s1_entry_vmid`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ VMID��
69. **`io_ptw_resp_bits_s1_entry_perm_d`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ��дλ��
70. **`io_ptw_resp_bits_s1_entry_perm_a`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ�ѷ���λ��
71. **`io_ptw_resp_bits_s1_entry_perm_g`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀȫ��λ��
72. **`io_ptw_resp_bits_s1_entry_perm_u`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ�û�ģʽλ��
73. **`io_ptw_resp_bits_s1_entry_perm_x`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ��ִ��λ��
74. **`io_ptw_resp_bits_s1_entry_perm_w`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ��дλ��
75. **`io_ptw_resp_bits_s1_entry_perm_r`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ�ɶ�λ��
76. **`io_ptw_resp_bits_s1_entry_level`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ����
77. **`io_ptw_resp_bits_s1_entry_ppn`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ����ҳ�ţ�PPN����
78. **`io_ptw_resp_bits_s1_addr_low`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ��ַ��λ��
79. **`io_ptw_resp_bits_s1_ppn_low_*`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ PPN ��λ��
80. **`io_ptw_resp_bits_s1_valididx_*`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ��Ч������
81. **`io_ptw_resp_bits_s1_pteidx_*`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ PTE ������
82. **`io_ptw_resp_bits_s1_pf`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀҳ�����źš�
83. **`io_ptw_resp_bits_s1_af`**: PTW ��Ӧ�ĵ�һ��ҳ����Ŀ���ʴ����źš�
84. **`io_ptw_resp_bits_s2_entry_tag`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ��ǩ��
85. **`io_ptw_resp_bits_s2_entry_vmid`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ VMID��
86. **`io_ptw_resp_bits_s2_entry_ppn`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ PPN��
87. **`io_ptw_resp_bits_s2_entry_perm_*`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ��Ȩ��λ��
88. **`io_ptw_resp_bits_s2_entry_level`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ����
89. **`io_ptw_resp_bits_s2_gpf`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ GPF �źš�
90. **`io_ptw_resp_bits_s2_gaf`**: PTW ��Ӧ�ĵڶ���ҳ����Ŀ GAF �źš�
91. **`io_ptw_resp_bits_getGpa`**: PTW ��Ӧ�Ļ�ȡ GPA �źš�

## ���������� Bundle ˵��

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

## ��������������ʽ�����㸴��ճ����

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
