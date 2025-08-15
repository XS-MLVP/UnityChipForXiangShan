---
title: Shield-XS Bitmap 基础知识
description: 本文档介绍了bitmap 安全隔离的基础设计思想，通过阅读本文档，你可以知道为什么需要bitmap， 以及其应用场景
categories: [香山 Bitmap 基础设计]
tags: [香山, Bitmap, 基础]
weight: 1
---
 本节将介绍bitmap的一些基础知识，有助于理解为什么我们需要bitmap，本节包含：
 + **背景描述**
 + **威胁模型**
 + **防御原理**
 + **工作流程**
 + **应用场景**
#### 术语描述
| 缩写 | 全名 |含义|
| --- | --- | --- |
| TCB  | Trusted Computing Base | 可信计算基，负责底层硬件的安全可信操作 |
| TEE  | Trusted Execution Environment | 可信执行环境 |
| MMU  | Memory Management  Unit | 内存管理单元 |
| RDSM | Root Domain Security Mananger | 根域权限管理器 |
| C-SDSM | Confidencial Supervisor Domain Security Manager   | 可信监督域 权限管理器 |
| APLIC | advanced platform level interrupt controller | 平台级中断控制器 |
| LLC | Last Lavel Cache | 末级缓存 |
| DMA | Direct Memory Access | 直接内存访问 |
| CVM | Confidencial Virtual Machine | 可信虚拟机 |
| TLB | Translation Lookaside Buffer | 页表缓存 |
| MBMC | machine level bitmap check | bitmap CSR 特殊状态寄存器 |
| BMA | Bitmap Adress | Shield Bitmap 专属内存区域基地址 |
| CMODE | Confidencial Mode | 开启bitmap后当前模式是否是可信 |
| BME | Bitmap Enable | 是否开启 Bitmap |
| PTW | Page Table Walker | <font style="color:rgb(0, 29, 53);">页表遍历器  |
| HPTW | <font style="color:rgba(0, 0, 0, 0.87);">Hypervisor PTW | 监督域页表遍历器 |
| LLPTW | Last Level PTW | 末级页表遍历器 |



