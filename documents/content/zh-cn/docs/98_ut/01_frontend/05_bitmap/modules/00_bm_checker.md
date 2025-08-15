---
title: Bitmap Checker
categories: [bitmap 硬件实现]
tags: [香山,bitmap, 硬件]
weight: 1
---

#  Bitmap Checker硬件模块
##  Bitmap checker简介
Bitmap checker 的作用是将来自外部（ptw/lptw/hptw）的请求发送至cache，并根据是否命中进行内存访问查权限。最后将cache返回的或者内存访问得到的权限发送回请求源。

此外，bitmap（walker）支持non blocking 特性，每一个请求来源都有FSM负责录入请求进行处理。但是一次只能有一个fsm进行cache访问。



##   状态机描述
 为了保持non blocking，有8个独立的状态机（entries）并行运行。每个 entry 维护独立的状态和数据处理。当有请求进入时，从下到上依次将fsm填满，由于总共就8个请求来源，因此不会出现无空闲fsm可用的情况。

 当entry的PA重复时，仅有一个fsm会进行一次查cache 或者访问memory，其余重复fsm项的状态会被部分跳过。重复表示PA的tag位[47:18] 一致。

| PA | | | |
| --- | --- | --- | --- |
| 段| tag | Bitmap offset | Page offset |
| 位| [47:18] | [17:12] | [11:0] |



#### Bitmap checker 模块状态机


![](../../modul00_1.png)



#### 状态机状态

| state_idle | 标明该fsm状态为空，可以录入新请求<br/>当io.req.fire时，切换到新状态<br/>转换条件：<br/>io.req.fire → state_addr_check (无重复请求)<br/>io.req.fire && to_wait → state_mem_waiting (检测到重复请求在等待) 同时写入重复项的id到fsm<br/>io.req.fire && to_mem_out → state_mem_out (重复请求已完成) 同时写入重复项的id到fsm<br/> |
| --- | --- |
| state_addr_check | 进行pmp检查<br/>转换条件：<br/>accessFault=true → state_mem_out (检查失败)<br/>accessFault=false → state_cache_req (检查通过) |
| state_cache_req | 将cachereq拉高，fire后→ state_cache_resp |
| state_cache_resp | Cache resp fire后更新<br/>hit=true → state_mem_out (缓存命中)<br/>hit=false && cm_to_mem_out → state_mem_out (重复请求已完成) 同时写入重复项的id到fsm<br/>hit=false && cm_to_wait → state_mem_waiting (检测到重复请求) 同时写入重复项的id到fsm<br/>hit=false → state_mem_req (无重复请求) <br/> |
| state_mem_req | 拉高valid 并等待，mem req fire时，将所有重复项目的id跟新为本fsm id，并将所有重复和本机 state 设置为mem wait |
| state_mem_waiting | Fire时，→state_mem_out，并将所有的符合id项目内值全部跟新为mem返回值。 |
| state_mem_out | 拉高 resp valid ，fire时→ state_idle |




##  接口信号
| 信号| 位宽| 描述|
| --- | --- | --- |
| Io.mem |  | 内存访问相关信号|
| io.mem.resp.bits.id | 4 | memory 响应返回的 ID(需为bitmap编号) |
| io.mem.resp.bits.value | 512 | memory 返回的 bitmap 数据块 |
| io.mem.req_mask | 20 | Memory 请求屏蔽位 |
| io.mem.req.bits.addr | 56 | memory 请求的 bitmap 数据地址 |
| io.mem.req.bits.id | 4 | memory 请求的编号(恒定为bitmap编号) |
| io.mem.req.bits.hptw_bypassed| 1| （和</font>bitmap </font>模块内部无关）|
| Io.Req|  | 请求信号|
| io.req.bits.bmppn | 27 | 被检查的物理页号 PPN |
| io.req.bits.id| 4| 请求编号，用于标识请求来源（和</font>bitmap </font>模块内部无关）|
| io.req.bits.vpn| 27| 对应虚拟页号VPN</font>，用于唤醒</font>pagecache</font>（和</font>bitmap </font>模块内部无关）|
| io.req.bits.level| 2| 所查询页表的级别信息（</font>0/1/2</font>），用于唤醒</font>pagecache</font>（和</font>bitmap </font>模块内部无关）|
| io.req.bits.way_info| 8| TLB way </font>编号用于唤醒</font>pagecache</font>（和</font>bitmap </font>模块内部无关）|
| io.req.bits.hptw_bypassed| 1| 用于唤醒</font>pagecache</font>（和</font>bitmap </font>模块内部无关）|
| Io.resp|  | 返回结果|
| io.resp.bits.cf | 1 | 检查权限是否允许访问 |
| io.resp.bits.cfs | 8 | 相邻8个（3bit地址空间）的权限 |
| io.resp.bits.id| 4| 响应对应的请求id</font>（和</font>bitmap </font>模块内部无关）|
| Io.pmp|  | Pmp</font>查|
| io.pmp.req.bits.addr | 56 | 进行PMP检查的物理地址 |
| io.pmp.req.bits.cmd | 2 | 读/写权限请求类型（恒定为读） |
| io.pmp.req.bits.size | 3 | 请求访问大小（恒定） |
| io.pmp.resp.ld | 1 | PMP Load 权限检查结果 |
| io.pmp.resp.mmio | 1 | PMP MMIO 检查结果 |
| Io.wakeup|  | Resp</font>时且非</font>hptw bypassed </font>进行重填pagecache|
| io.wakeup.bits.setIndex| 4| 唤醒用的setIndex</font>（和</font>bitmap </font>模块内部无关）|
| io.wakeup.bits.tag| 4| 唤醒tag</font>（</font>VPN</font>高位）（和</font>bitmap </font>模块内部无关）|
| io.wakeup.bits.isSp| 1| 是否为</font>superpage</font>（和</font>bitmap </font>模块内部无关）|
| io.wakeup.bits.way_info| 8| TLB</font>对应的way </font>信息（和</font>bitmap </font>模块内部无关）|
| io.wakeup.bits.pte_index| 6| PTE </font>在段页表中的索引位置（和</font>bitmap </font>模块内部无关）|
| io.wakeup.bits.check_success | 1 | 是否 bitmap 检查通过 |
| Refill|  |  |
| io.refill.bits.data| 64| 要写入cache </font>的bitmap </font>数据|
| CSR|  |  |
| io_sfence_valid| 1| SFENCE </font>操作有效信号（为高刷新</font>fsm</font>）|
| io_csr_satp_changed| 1| SATP </font>寄存器变更标志（为高刷新</font>fsm</font>）|
| io_csr_vsatp_changed| 1| VSATP </font>寄存器变更标志（为高刷新</font>fsm</font>）|
| io_csr_hgatp_changed| 1| HGATP </font>寄存器变更标志（为高刷新</font>fsm</font>）|
| io_csr_mbmc_BMA| 58| Bitmap </font>基址寄存器值|
