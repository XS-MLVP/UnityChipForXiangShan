---
title: 单元验证
description:  验证需求
categories: [香山bitmap验证]
tags: [香山, bitmap, 验证]
weight: 1
---

## 单元验证
###   TLB 相关功能验证
| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| TLB_001 | ITLB hit/miss 场景验证 | 设计测试用例覆盖 ITLB 命中和未命中 | 4K/2M/1G/512G 页大小 |
| TLB_002 | DTLB hit/miss 场景验证 | 设计测试用例覆盖 DTLB 命中和未命中 | 4K/2M/1G/512G 页大小 |
| TLB_003 | L2TLB hit/miss 场景验证 | 设计测试用例覆盖 L2TLB 命中和替换 | 4K/2M/1G/512G 页大小 |
| TLB_004 | L2TLB 压缩功能验证<br/>注：仅支持一阶段地址转换压缩，最多压缩8项 | 测试TLB 压缩场景下，Bitmap 查询结果是否正确 | TLB 压缩启用 + 4K 页大小<br/> |




### Bitmap Cache 相关功能验证 


| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| BITMAP_001 | Bitmap Cache hit/miss 场景验证 | 设计测试用例覆盖命中和未命中 | Bitmap Y/N + 跨bitmap cache line |
| BITMAP_002 | Bitmap check 功能验证 | 验证 bitmap check 的正确性 | Bitmap check 启用 + 4K 页大小 |
| BITMAP_003 | 跨bitmap cache line 场景验证 | 测试跨 cache line 的访问行为 | 跨bitmap cache line + 2M 页大小 |
| BITMAP_004 | NAPOT 拓展开启，验证Bitmap 的行为 | 开启NAPOT，设置PTE.n 位，验证Bitmap  检测流程 | 跨bitmap cache line + 64K 页大小切换PTE.n 位 |




### Bitmap Cache 和 TLB 组合相关功能验证 
| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| **TLB_BITMAP_001** | Bitmap与TLB混合命中场景验证 | 组合Bitmap命中与各级TLB命中，验证多级缓存协同 | Bitmap hit + ITLB/DTLB/L2TLB全命中<br/><br/> |
| **TLB_BITMAP_002** | 全未命中极端场景验证 | 设计冷启动或冲刷缓存后首次访问的全未命中用例 | Bitmap miss + ITLB/DTLB/L2TLB全miss + 触发页表遍历 |
| **TLB_BITMAP_003** | Bitmap跨行与TLB替换场景验证 | 强制Bitmap跨cache line访问并触发TLB替换（如duplicate access或页表更新） | Bitmap跨行 + DTLB miss + L2TLB替换 |
| **TLB_BITMAP_004** | 重复访问与Cache/TLB交互验证 | 通过相同地址重复访问验证Bitmap/TLB的重复访问优化 | Bitmap重复命中 + ITLB重复命中 + 无替换<br/>Bitmap重复Miss + ITLB重复Miss + 替换 |




---

### 页表遍历（PTW）相关功能验证
| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| PTW_001 | PTW/HPTW/LLPTW 优先级验证 | 测试多级页表遍历的优先级 | PTW + HPTW 并发 |
| PTW_002 | PTW 返回异常（access fault）验证 | 模拟 PTW 返回异常的场景 | PTW return af + 跨Page |
| PTW_003 | PTE 合法性验证 | 测试非法 PTE 的处理 | 非法 PTE + PMP check |


---

###  异常与重放（Replay）功能验证
| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| REPLAY_001 | 标量 replay 场景验证 | 测试标量指令重放行为 | 标量 replay + access fault |
| REPLAY_002 | 向量访存 replay 场景验证 | 测试向量指令重放行为 | 向量 replay + 跨MMO |
| EXCEPT_001 | 异常优先级验证（access/page fault/guest page fault） | 验证异常触发的优先级 | page fault/guest page fault<br/>page table walker 过程中的PMP/bitmap 检测失败<br/>转换之后的物理地址PMP 检测失败 |


---

###   特权级与扩展功能验证
| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| PRIV_001 | U/S/M 特权级切换验证 | 测试不同特权级下的访问权限 | U/S/M + 4K/2M 页大小 |
| EXT_001 | H-extension 功能验证 | 测试 H-extension 启用和禁用场景 | H-extension + 跨tlb entry |
| PMP_001 | PMP check 功能验证 | 测试bitmap 内PMP 权限检查 | PMP Y/N + 跨Page |


---

###   Fense验证
| 验证功能编号 | 验证描述 | 覆盖方法 | 排列组合示例 |
| --- | --- | --- | --- |
| MISC_001 | Fence 操作验证 | 测试 fence 指令的同步效果 | Fence + 切换Cmode |




###   验证方法说明
**覆盖方法**：通过随机测试、定向测试和边界值测试覆盖功能点。

 **排列组合**：优先覆盖高频场景，再逐步覆盖低频组合（如 512G 页）。

###   备注
·        需根据实际硬件行为调整测试用例的输入和预期输出。

·        动态检查（如 PMP check）需结合具体权限配置。
