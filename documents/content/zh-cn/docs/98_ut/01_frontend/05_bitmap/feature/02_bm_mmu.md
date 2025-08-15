---
title: Shield-Bitmap 地址翻译
categories: [bitmap 技术细节]
tags: [香山, Bitmap, 技术细节]
weight: 4
---


# 虚拟化两阶段地址翻译流程
bitmap和MMU-L2TLB耦合，会在虚拟化两阶段地址走表翻译完成后才进行隔离检查。如果bitmap检查没有通过，就向MMU-L1TLB 发送af。因此对L1TLB以及其上面的模块来说，bitmap是透明的。所以，在进一步介绍前，需要先了解MMU处理虚拟化两阶段地址的流程。
##  **基本概念**
+**两阶段翻译**：Guest Virtual Address (GVA) → Guest Physical Address (GPA) → Host Physical Address (HPA)   
+ **关键寄存器**  ：   
    - **hgatp**  ：控制G-stage（客户机阶段）页表根地址   
    - **vsatp**  ：控制VS-stage（虚拟化监督模式阶段）页表根地址   

**1. VAPT (Virtual Address Protection and Translation)**

**作用**  ：管理客户机虚拟地址（GVA）到客户机物理地址（GPA）的第一阶段翻译（VS-stage）。   

| **字段名** | **位宽** | **描述** |
| --- | --- | --- |
| **MODE** |    4   |    页表模式：      0**    -关闭翻译，   1**    -Sv32，   8**    -Sv39，   9**    -Sv48，   10**    -Sv57   |
| **ASID** |    16   |    地址空间标识符（Address Space ID），隔离不同客户机的地址空间   |
| **PPN** |    44   |    物理页号（Physical Page Number），指向VS-stage页表的根页表地址   |
| **RESERVED** |    8   |    保留位，必须写0   |
| **G** |    1   |    全局映射标志（Global bit），若为1则忽略ASID匹配   |


---

**2. SVAPT (Supervisor Virtual Address Protection and Translation)**

**作用**  ：在Hypervisor模式下管理宿主机虚拟地址（HVA）到宿主机物理地址（HPA）的翻译（HS-stage）。   

| **字段名** | **位宽** | **描述** |
| --- | --- | --- |
| **MODE** |    4   |    页表模式：      0**    -关闭翻译，   1**    -Sv32，   8**    -Sv39，   9**    -Sv48    |
| **ASID** |    16   |    宿主机地址空间标识符   |
| **PPN** |    44   |    指向HS-stage页表的根页表地址   |
| **V** |    1   |    虚拟化启用标志：      1**    -启用两阶段翻译（需配合H-extension）   |
| **RESERVED** |    7   |    保留位   |


---

**3. HGAPT (Hypervisor Guest Address Protection and Translation)**

**作用**  ：控制客户机物理地址（GPA）到宿主机物理地址（HPA）的第二阶段翻译（G-stage）。   

| **字段名** | **位宽** | **描述** |
| --- | --- | --- |
| **MODE** |    4   |    G-stage页表模式：      0**    -关闭翻译，   3**    -Sv32x4，   4**    -Sv48x4   |
| **VMID** |    14   |    虚拟机标识符（Virtual Machine ID），隔离不同虚拟机的G-stage页表   |
| **PPN** |    44   |    指向G-stage页表的根页表地址   |
| **GST** |    1   |    客户机软件TLB失效指令使能：      1**    -允许客户机执行   sfence.vma** |
| **RESERVED** |    5   |    保留位   |


---

**关键差异总结**

| **寄存器** | **控制阶段** | **核心功能** | **特权级** |
| --- | --- | --- | --- |
|    VAPT   |    VS-stage   |    GVA→GPA翻译（客户机视角）   |    VS-mode   |
|    SVAPT   |    HS-stage   |    HVA→HPA翻译（宿主机视角）   |    HS-mode   |
|    HGAPT   |    G-stage   |    GPA→HPA翻译（硬件辅助虚拟化）   |    M-mode/HS-mode   |


  
 

+ **特权级**  ：   
    - **VS-stage**  ：由Hypervisor管理，处理客户机虚拟地址   
    - **G-stage**  ：由客户机OS管理，处理客户机物理地址 

    
## **翻译过程**
**第一阶段：VS-stage (GVA → GPA)**

| **VPN部分** | **VS-stage页表** | **依赖的G-stage页表** | **说明** |
| --- | --- | --- | --- |
| VPN[3] | VS-L3 | 通过**hgatp**<br/>访问G-L3 | 最高级页表，需G-stage辅助查询 |
| VPN[2] | VS-L2 | 通过**hgatp**<br/>访问G-L2/G-L1/G-L0 | 中间级页表，需G-stage多级支持 |
| VPN[1] | VS-L1 | 通过**hgatp**<br/>访问G-L1/G-L0 | 次末级页表 |
| VPN[0] | VS-L0 | 通过**hgatp**<br/>访问G-L0 | 最后级页表，直接指向GPA |


****

**第二阶段：G-stage (GPA → HPA)**

| **页表层级** | **作用** |
| --- | --- |
| G-L3 | 顶级页表，由**hgatp**寄存器指向 |
| G-L2 | 中间级页表 |
| G-L1 | 次末级页表 |
| G-L0 | 最后级页表，与offset拼接生成HPA |


+ 任一阶段页表访问失败会触发异常：
    - VS-stage异常 → Hypervisor处理
    - G-stage异常 → 客户机Page Fault





![](../../feature02_1.svg)

#### L2TLB table walker 查表流程说明：

1. 请求首先进入PageCache查询第一阶段页表
2. 若第一阶段命中：
    - 直接由PageTableWalker处理第二阶段
3. 若第一阶段未命中：
    - 根据命中级别选择PageTableWalker或LastLevelPageTableWalker
4. 第二阶段处理：
    - 先在PageCache中查询
    - 未命中时转交HypervisorPageTableWalker
    - 翻译结果返回PageCache后完成流程

#### 关键路径：

+ 快路径：PageCache(阶段1)→PageTableWalker→PageCache(阶段2)
+ 慢路径：PageCache(阶段1)→LastLevelPTW/PTW→PageCache(阶段2)→HypervisorPTW


  
## MMU-L2TLB 地址翻译流程




![](../../feature02_2.svg)




**1. L1TLB向L2TLB发送请求** 

+ **非两阶段翻译请求**：
    - 首先访问PageCache。
    - 若命中叶子节点，直接返回结果给L1TLB。
    - 若未命中叶子节点：
        * 根据PageCache命中的页表等级，结合PageTableWalker (PTW) 和 LastLevelPageTableWalker (LLPTW) 的空闲情况：
            + 进入PTW、LLPTW 或 Miss Queue。
+ **两阶段地址翻译请求**：
    - PageCache每次只能处理一个查询请求。
    - 首先查询第一阶段的页表：
        * 若第一阶段命中，请求发送给PTW进行第二阶段的翻译。
        * 若第一阶段未命中：
            + 根据命中的页表级别，发送给PTW或LLPTW，在这两个模块中完成第二阶段的翻译。



+ **page Cache 访问流程：**

![](../../feature02_3.svg)



 

**2. PTW和LLPTW的第二阶段翻译**

+ PTW和LLPTW发送的第二阶段翻译请求会先发送到PageCache查询：
    - 若命中，PageCache直接返回结果给对应模块（PTW或LLPTW）。
    - 若未命中，发送给HypervisorPageTableWalker (HPTW) 进行翻译，结果直接返回给PTW或LLPTW

 **3. PageTableWalker (PTW) 处理**

+ PTW同时只能处理一个请求，进行HardwarePageTableWalk：
    - 访问内存中前两级页表（不访问4KB页表）。
    - 可能的结果：
        * 访问到2MB或1GB的叶子节点。
        * 发生Pagefault或Access fault。
        * 以上情况直接返回给L1TLB。
        * 否则，请求送往LLPTW访问最后一级（4KB）页表。



PTW 处理流程

![](../../feature02_4.svg)

 

**4. HypervisorPageTableWalker (HPTW) 处理**
+ HPTW每次只能处理一个请求：
    - LLPTW中第二阶段翻译的请求串行发送给HPTW。
    - HPTW访问可能触发Pagefault或Access fault，返回给PTW或LLPTW，最终返回给L1TLB。



![](../../feature02_5.svg)

 

**5. 内存访问流程**

+ PTW、LLPTW、HPTW均可向内存发送请求访问页表内容。
+ 物理地址访问内存前需通过PMP和PMA模块检查：
    - 若发生Access fault，不向内存发送请求。
+ 请求经过仲裁后，通过TileLink总线向L2Cache发送：
    - L2Cache访存宽度为512bits，每次返回8项页表。



![](../../feature02_6.svg)

 

**6. 页表压缩机制**

+ **L2TLB**：
    - 命中4KB页时，返回至多8项连续的页表项（虚拟页号高位相同且物理页号高位和属性相同）。
    - 在H拓展中，与虚拟化相关的页表仍采用压缩机制。
+ **L1TLB**：
    - 在H拓展中，与虚拟化相关的页表压缩机制无效，视为单个页表。

**7.异常处理**

+ 各级Walker（PTW、LLPTW、HPTW）访问中可能触发：
    - Pagefault或Access fault，逐级返回至L1TLB。

**8. 关键限制**

+ PTW和HPTW均单请求处理，串行化。
+ PageCache单查询请求处理，两阶段翻译需分步完成。