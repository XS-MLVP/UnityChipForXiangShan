---
title: Bitmap Cache
categories: [bitmap 硬件实现]
tags: [香山, bitmap, 硬件]
weight: 2
---

### Bitmap Cache硬件模块

#### Bitmap cache简介

Bitmap cache用于缓存 bitmap 数据块以减少 memory 访问延迟，存储最近访问的 bitmap 数据，**共16个entry。每个 entry 存储一个 64-bit 数据段**。使用plru替换策略。

#### Bitmap模块结构

Cache 一回合出结果，不需要pipeline。此外，refill也只需要一回合。Refill使用plru进行充填。

#### Bitmap cache接口

| io_req               | 位宽 | Bm 发起请求                                 |
| -------------------- | ---- | ------------------------------------------- |
| io_req_bits_tag      | 36   | Tag for cache lookup ([35:6] = tag)         |
| io_req_bits_order    | 8    | 发起请求的Fsm编号                           |
| Io resp              |      | 返回bm请求                                  |
| io_resp_bits_hit     | 1    | 是否hit cache                               |
| io_resp_bits_order   | 8    | 发起请求的Fsm编号                           |
| io_resp_bits_cfs     | 8    | 相邻8个的权限                               |
| Io refill            |      | Refill接口，来自bm，bm resp valid时发起重填 |
| io_refill_bits_tag   | 36   | Tag for cache refill ([35:6] = tag)         |
| io_refill_bits_data  | 64   | Data to refill into cache                   |
| io_resp_bits_hit     | 1    | 是否hit cache                               |
| CSR                  |      |                                             |
| io_sfence_valid      | 1    | 同步刷新请求有效（触发缓存刷新）            |
| io_csr_satp_changed  | 1    | SATP CSR 变更标志（触发缓存刷新）           |
| io_csr_vsatp_changed | 1    | VSATP CSR 变更标志（触发缓存刷新）          |
| io_csr_hgatp_changed | 1    | HGATP CSR 变更标志（触发缓存刷新）          |
| io_csr_mbmc_BCLEAR   | 1    | 缓存清除信号（触发缓存刷新）                |
