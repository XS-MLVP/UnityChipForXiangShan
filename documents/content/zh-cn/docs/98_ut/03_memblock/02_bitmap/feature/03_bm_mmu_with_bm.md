---
title: Shield-Bitmap 地址翻译2
categories: [bitmap 技术细节]
tags: [香山, Bitmap, 技术细节]
weight: 5
---

# 加入了Shield-XS安全检查后的内存地址转换流程

如前文所述， bitmap和MMU耦合。现在将介绍增加了bitmap后的MMU地址翻译流程。

![ ](../../feature03_1.jpeg)

从 **客户虚拟地址** 到 **主机物理地址** 的转换过程，同时涉及 **安全属性检查** 和 Shield-Bitmap**高速缓存访问**。以下是详细步骤：

1. **客户虚拟地址（Guest Virtual Address）**: 流程开始于计算单元（如CPU）使用客户虚拟地址发出内存访问请求。

2. **访问一级快表（L1TLB Lookup）**: 首先查询一级快表（**L1TLB**），检查是否已缓存该地址的映射。只有经历过bitmap检查才会出现在L1TLB Cache中。因此和L2TLB Cache不同，L1TLB Cache 不会存储bitmap检查位。

3. **一级快表缓存命中？**

    *  **是** → 直接从L1TLB Cache获取主机物理地址（Host Physical Address）。

    * **否** → 进入下一级查询（访问二级快表）。

4. **访问二级快表（L2TLB Lookup）**: 如果一级快表未命中，继续查询二级快表（L2TLB），检查二级快表是否有对应的映射。L2TLB Cache 存储安全允许位（cf）表示 是否经过bitmap 检查。

    * **二级快表缓存命中？**

        * **cf 和 L2TLB 页表项均命中** → 获取主机物理地址，并回填一级快表（更新L1TLB）。

        * **L2TLB 页表项命中，bitmap cf 未设**→ 发送请求至bitmap，进行权限检查。

        * **否** → 触发 **页表遍历（Page Table Walker）**，从内存中加载页表映射关系，随后进行bitmap检查。

5. **进行页表遍历**：从内存中加载页表映射关系

6. **主机虚拟地址 → 主机物理地址转换**：通过页表遍历获取主机物理地址（Host Physical Address）。

7. **安全性检查允许访问（Security Check）**： 对物理地址进行 **安全属性检查**。如果检查失败，可能触发访问错误（Access Fault）。

8. **访问（安全属性高速缓存）Shield-Bitmap Cache**：查询**Shield-Bitmap** Cache是否已缓存目标数据。

    - **Shield-Bitmap Cache 命中？**

        - **是** → 返回数据。

        - **否** → 继续访问主存**Shield-Bitmap 专属内存区域**，读取权限。

9. **访存请求合并（Shield-Bitmap Memory Request Merging）**：如果多个请求访问同一地址，可能合并访存请求以提高效率。

10. **访问错误**：如果访问不被允许，触发访问错误。

## 异常处理描述

RISC-V 特权手册规定的同步异常处理优先级

![](../../feature03_2.png)

优先级处理如下：

| 序号 | 描述                                                                   | 触发异常     |
| ---- | ---------------------------------------------------------------------- | ------------ |
| 1    | PTE.V == Invalid                                                       | Page fault   |
| 2    | PTE.V == Invalid &&<br/>Page Table Walker (PMP \|\| Bitmap) Check Fail | Access Fault |
| 3    | PTE.V valid && PTE.Permission (R/W/X) Check Fail                       | Page fault   |
| 4    | PTE.V valid && PMP Check Fail                                          | Access Fault |
