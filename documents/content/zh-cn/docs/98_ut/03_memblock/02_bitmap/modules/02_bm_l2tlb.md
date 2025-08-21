---
title: Bitmap 与L2TLB交互
categories: [bitmap 硬件实现]
tags: [香山, bitmap, 硬件]
weight: 3
---

### Bitmap 与L2TLB内的交互

![](../../module02_1.png)

#### Page Cache 与 Bitmap 检测机制的交互

##### 新增信号

发向 PTW 的 bitmap check 信号：用于触发 PTW 进行 bitmap 检测。

发向 HPTW 的 bitmap check 信号：用于触发 HPTW 进行 bitmap 检测。

接收来自 bitmap 的重填信号（bitmap wakeup）：用于接收 bitmap 检测结果并更新缓存。

##### Bitmap Wakeup接口: refill bitmap

功能描述：当接收到 wake up valid 信号时，将 check_success 结果写入对应的 sp 或 l0 的 cache bitmap reg 中。

工作原理：cache bitmap reg 用于标识缓存项是否通过 bitmap 检测。值为 1 表示已通过检测；值为 0 表示检测未通过或尚未检测。如果发现 PtwCache 命中的表项未通过检测，则触发 Bitmap 检测流程，并通过 bitmap wakeup 更新缓存项。此外，在走表过程中所有bitmap返回的项都会回填page cache。

<center><img src=../../module02_2.jpeg width=30% /></center>


##### Ptw/llptw接口:refill data 后第一次伪hit发起bitmap请求

功能描述：当缓存命中且 bitmap valid = 0 时，首次命中不直接返回 L1TLB，而是返回响应请求源并发起 bitmap 请求。

工作原理：使用 is_hptw 判断请求源。请求源在获取 bitmap 权限后，将结果重新填充到 Page Cache 中。

#### Page Table walker 交互

##### 状态机更新

新增状态：PTW、LLPTW 和 HPTW 的状态机中新增了 state_bitmap_check。

工作流程：在 PTW、LLPTW 和 HPTW 的状态机中，于 state_mem_resp 阶段进行 bitmap 检测，并将 bitmap 检测的使能信号传递给这些部件。如果满足 bitmap 检测条件，则进入 state_bitmap_check 并获取检测结果。如果检测失败，则触发访问故障（Access Fault）并将结果返回。

##### 触发条件

PTW：仅在未开启虚拟化且检测到巨页（hugepage）时进行 bitmap 检测。

LLPTW：仅在请求未开启虚拟化（即进行 VA 到 PA 的地址转换时）进行 bitmap 检测。如果请求通过 HPTW，则 HPTW 已在工作过程中进行了 bitmap 检测。

HPTW：在遍历到最后一级页表时，于 mem_resp 阶段进行 bitmap 检测。

##### 新接口

Req_bitmapcheck 接口：用于在 Page Cache 首次命中时发起 bitmap 检测。仅在 PTW 和 LLPTW 上实现。如果有效，则直接接收一个 PTE 并检查权限。状态机直接跳转到 state_bitmap_check，获取权限后直接返回 pagecache。

Bitmap 接口：用于在 state_bitmap_check 阶段发送 bitmap 请求，并检查权限是否通过。如果检测失败，则触发访问故障。HPTW 和 LLPTW 均具备此接口。

##### 刷新

bitmap 依赖软件辅助刷新，硬件刷新不完整。在刷新前，需依次sfence 和 hfence L1 和L2TLB内所有项目，然后才可以拉高 CSR_MBMC_BCLEAR 进行bitmap cache刷新。
