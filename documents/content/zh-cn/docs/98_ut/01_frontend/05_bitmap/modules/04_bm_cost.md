---
title: 开销评估
categories: [bitmap 硬件实现]
tags: [香山,bitmap, 硬件]
weight: 5
---



##  开销评估
**1.      基本配置**

| **类别** | **配置项** | **参数****/****设置** |
| :--- | :--- | :--- |
| **Shield-Bit 配置** | 有效 Shield-XS 隔离模型 | - |
| | 设置 Shield-Bitmap  | _ |
| | Shield-Bitmap缓存大小 | 128 × 8 Bytes |
| **KunminghuV2 配置** | TileLink Prototype | - |
| **缓存层级配置** | L1 指令/数据缓存大小 | 64KB |
| | L1 指令/数据 TLB | 48-全关联（Full Association） |
| | L2 缓存大小 | 1MB |
| | L3 缓存大小 | 16MB |



**2.      SPEC2006 性能数据**

SPECInt2006 Simpoint est.@**3GHz**  **GEOMEAN 44.62 **->** 44.29 (0.72% )**



![](../../module04_1.png)

图 9.1 SPEC2006 性能开销

性能开销与DTLB Miss-rate 呈正比。有效的减少 DTLB 和 Shield-bitmap Cache 的miss-rate,  可以进一步提升性能。例如将缓存从 16 项扩展到 128 项，可使 GemsFDTD 的性能开销从 6.51% 降低至 2.36%。

**3.      硬件开销**

采用7纳米工艺制程，硬件面积开销仅为0.2%。

<!-- | **模块** | **Cell ****面积****（平方微米）** |
| --- | --- |
| Shield-Bitmap Cache | 5,075 |
| Shield-Bitmap Checker | 1,088 |
| MMU Area | 50,843 |
| KMH V2 Core Area | 2,000,000 |
| Area Percentage | **<font style="color:#c00000;"><font style="color:#c00000;">0.3%** | -->

|工艺 |子模块前 (单位: μm2) |子模块后 (单位: μm2) |百分比|
|---|---|---|---|
|T7 |Memblock.withoutBitmap:462415.887238 |Memblock.withBitmap:471410.993566 |+1.94524%|
T7 |L2TLB.withoutBitmap: 41538.554989|L2TLB.withBitmap : 50843.978450 |+22.4%|
## 时序违例
|模块路径	|clock period	|clock uncertainty	|data arrival time	|setup time	|slack|
|---|---|---|---|---|---|
 |bitmap FSM -> bitmap Cache Data Reg	|0.333 ns	|0.1 ns	|0.2724 ns	|0.0107 ns	|-0.0501 ns|