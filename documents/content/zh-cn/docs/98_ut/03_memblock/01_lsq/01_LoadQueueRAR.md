---
title: LoadQueueRAR
linkTitle: LoadQueueRAR
weight: 12
---

**本文档参考[香山LSQ设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/tree/master/docs/memblock/LSU/LSQ)写成**

本文档撰写的内容截至[ca892e73]

请注意，本文档撰写的测试点仅供参考，如能补充更多测试点，最终获得的奖励可能更高！

# LoadQueueRAR 简介

LoadQueueRAR用于保存已经完成的load指令的用于load to load违例检测的信息。

多核环境下会出现load to load违例。单核环境下相同地址的load乱序执行本来是不关心的，但是如果两个load之间有另外一个核做了相同地址的store，并且本身这个核的两个load做了乱序调度，就有可能导致新的load没有看到store更新的结果，但是旧的load看到了，出现了顺序错误。

多核环境下的load-load违例有一个特征，当前DCache一定会收到L2 cache发来的Probe请求，使得DCache主动释放掉这个数据副本，这时DCache会通知load queue，将相同地址的load queue中已经完成访存的项做一个release标记。后续发往流水线的load指令会查询load queue中在它之后相同地址的load指令，如果存在release标记，就发生了load-load违例。

## 术语说明

| 名称                             | 描述                                       |
| ------------------------------- | ------------------------------------------ |
| L2Cache | 二级高速缓存 |
| DCache  | 数据缓存 |
| ROB     | 重排序缓冲区 |
| CAM     | 内容可寻址存储器  |
| FTQ     | 取指目标队列   |

## ld-ld违例

多核环境下，可能会出现load to load违例：在单核环境中，相同地址的load乱序执行通常不被关注，因为它们在同一核内执行，不会影响其他核的状态，也不会被其他核的操作影响。但是，当两个load操作之间有另一个核对相同地址进行了store操作，情况就变得复杂。

考虑以下指令序列：
```
load1（core1）
store（core2） 
load2（core1）
```
指令的实际执行顺序为：
```
load2（core1）
store（core2） 
load1（core1）
```
由于指令的乱序执行，可能导致以下情况：旧的 load1 指令在执行时读取到了 store 修改后的新数据，而新的 load2 指令却读取到了未被修改的旧数据。这种执行顺序的变化会导致数据的不一致性，进而引发访存错误。

因此，在多核环境中，正确处理指令的执行顺序和内存一致性是至关重要的，以确保所有核都能看到一致的内存状态。

## 整体框图

<div>			
    <center>	
    <img src="../LoadQueueRAR_structure.svg"
         alt="LoadQueueRAR结构示意图"
         style="zoom:100%"/>
    <br>
    图1：LoadQueueRAR结构示意图<br><br>
    </center>
</div>

LoadQueueRAR最多能够存储72条指令（为了同VirtualLoadQueue的大小保持一致），每条指令占用一个条目。每个条目包含指令的物理地址（paddr）、与指令相关的信息（uop）、以及标记为已释放（released）和已分配（allocated）的状态寄存器。

该模块通过 FreeList 子模块管理 entry 资源，FreeList 中存储的是 entry 的编号。当一条指令满足入队条件时，FreeList 会为其分配一个 entry 编号，并将该指令存放在相应的 entry 中。指令出队时，需要释放所占用的 entry 资源，并将条目编号重新放回 FreeList 中，以供后续指令使用。

PaddrModule 的实现基于内容可寻址存储器（CAM），其深度为 72，数据宽度为 48。CAM 为每条流水线提供一个写端口，其中物理地址（paddr）作为写数据（wdata），条目编号作为写地址（waddr）。此外，CAM 还为每条流水线提供了一个地址查询端口（releaseViolationMdata），并为数据缓存（DCache）提供另一个地址查询端口（releaseMdata）。

<mrs-functions>

## 模块功能说明

### 功能1：发生ld-ld违例的指令请求入队

当query到达load流水线的s2时，判断是否满足入队条件，如果在当前load指令之前有未完成的load指令,且当前指令没有被flush时，当前load可以入队。

具体入队条件如下：

1. 指令的入队请求必须有效，具体通过检查 `query.req.valid` 是否等于 1。如果该条件满足，系统将继续处理指令的入队。

2. 指令必须确认尚未写回到重排序缓冲区（ROB）。这一条件通过比较指令在 VirtualLoadQueue 中的写回指针与该指令分配的 `lqIdx` 来验证。指令只有在到达 VirtualLoadQueue 的队头，并且其地址和数据均已准备好后，才能被写回到 ROB。这一机制确保了指令执行的顺序性和数据的有效性。

3. 指令不能处于冲刷状态。为此，系统需要比较重定向指针所指向的指令与该指令的 `robIdx`、`ftqidx`及 FTQ 内的偏移（`ftqoffset`）。如果两者不相同，则说明该指令可以安全入队，从而避免潜在的冲突和数据不一致性。

在 LoadQueueRAR 指令成功入队后，系统会执行一系列响应操作，以确保指令被正确管理和处理。具体的入队响应操作如下：

1. 拉高 allocated 寄存器。系统将指令的 `allocated` 寄存器设置为高电平。这一操作的目的是明确标识该指令已成功分配到 LoadQueueRAR 中。通过将 `allocated` 寄存器拉高，后续的处理逻辑能够迅速识别出该指令的状态，从而避免对未分配指令的误操作。

2. 写入指令相关信息到 uop。指令的相关信息将被写入到微操作（`uop`）中。这些信息包括指令的类型、目标寄存器、操作数等关键信息。将这些信息存储在 `uop` 中，确保后续的执行阶段能够准确获取和使用这些数据，从而执行相应的操作。这一过程对于指令的正确执行至关重要。

3. 物理地址写入 PaddrModule。指令的物理地址将被写入到 PaddrModule 中。这一操作的主要目的是为后续的地址查询和管理提供支持。

4. 检测 Release 的 Valid 信号。系统将检测 `release` 的有效信号是否被拉高。如果该信号有效，将进一步比较物理地址是否相同。如果物理地址一致，则对应条目的 `released` 信号将被设置为高电平，可以用于后续操作。

### 功能2：检测ld-ld违例条件

在 Load 指令的处理过程中，为了确保数据的一致性和正确性，系统需要检测潜在的 Load-Load 违例。当 load 到达流水线的 s2 时，会检查RAR队列中是否存在与当前load指令物理地址相同且比当前指令年轻的load指令，如果这些 load 已经拿到了数据，并且被标记了release，说明发生 load - load 违例，被标记release的指令需要从取指重发。 该检测过程主要涉及将查询指令的物理地址和相关信息与队列中存储的指令进行对比。具体流程如下：

1. 对比 ROB 索引。通过对比两条指令的robidx识别队列中是否存在比查询指令更年轻的指令。
2. 物理地址匹配。检查这两条指令的物理地址是否相同。这一对比通过 `releaseViolationMmask(w)(i)` 来进行，以确定两条指令是否访问了相同的内存位置。
3. 检查 Released 标记。如果该条指令的 `released` 寄存器被拉高，表明该指令已被标记为释放，说明它可以被重新使用。

一旦检测到 Load-Load 违例，系统将在下一个时钟周期内将 `resp.rep_rm_fetch` 信号拉高，以通知其他组件发生了违例。触发 Load-Load 违例的 Load 指令将被标记为需要重新从取指阶段执行。重定向请求将在这些指令到达 ROB 队列的尾部时发出，确保指令能够在合适的时机得到正确的处理。

该过程分为两个时钟周期进行：

- 第一拍进行条件匹配，对比物理地址和指令状态，得到mask。
- 第二拍生成是否发生违例的响应信号（`resp.rep_rm_fetch` ）。

由于 Load-Load 违例出现的频率相对较低，因此系统会选择在指令到达 ROB 的头部时才进行处理。这种处理方式类似于异常处理，确保系统能够在合适的时机对潜在的违例情况进行响应。

### 功能3：released寄存器更新

released寄存器需要更新的三种情况：

1. missQueue模块的replace_req在mainpipe流水线的s3栈发起release释放dcache块，release信号在下一拍进入loadqueue。
2. probeQueue模块的probe_req在mainpipe流水线的s3栈发起release释放dcache块，release信号在下一拍进入loadqueue。
3. atomicsUnit模块的请求在mainpipe流水线的s3栈发生miss时需要释放dcache块，release信号在下一拍进入loadQueue。

release信号的到达时机可以分为以下两种情况：

1. 指令入队时到达。如果查询指令传来的paddr的高42位信号与paddr的高位信号相同，并且该指令能够成功入队将对应entry的released寄存器信号拉高
2. 指令入队后到达。如果paddrmodule中存放的paddr的高42位信号与paddr的高位信号相同,将对应的released寄存器信号拉高

值得注意的是，dcache release 信号在更新 load queue 中 `released` 状态位时, 会与正常 load 流水线中的 load-load 违例检查争用 load paddr cam 端口. release 信号更新 load queue 有更高的优先级. 如果争用不到资源, 流水线中的 load 指令将立刻被从保留站重发.

### 功能4：指令的出队

Load指令的出队需要满足以下条件其中之一：

1. 当比队列entry中存放的指令更老的指令已经全部写回到ROB时，该指令可以出队。
2. 当这条指令需要被冲刷时，通常是出现数据依赖性问题、预测错误、异常或错误的情况下，迫使系统强制性地移除该指令，以保证处理器能够恢复到一个稳定的状态。

出队执行的操作：

1. 将指令对应的 `allocated` 寄存器设置为低电平。这一操作的目的是标识该指令不再占用 LoadQueueRAR 的资源，从而为后续指令的入队和处理腾出空间。
2. 将entry对应的`free`掩码拉高，表示该条目已被释放并可供后续使用。

在load流水线的s3阶段可以向队列发送revoke信号撤销上一拍的请求。如果指令当前周期的revoke信号拉高（revoke ==1），并且在上一个周期已经入队，需要执行撤销操作：

1. 该entry对应的allocated寄存器清零
2. 该entry对应的free掩码拉高

</mrs-functions>

## 接口说明

|                        | name                                     | I/O                 | width              | Description                                      |
| ---------------------- | ---------------------------------------- | ------------------- | ------------------ | ------------------------------------------------ |
| redirect               |                                          |                     |                    |                                                  |
| io.redirect.valid      | input                                    | 1                   | 后端重定向的有效位 |                                                  |
|                        | io.redirect.bits.robIdx.flag             | input               | 1                  | 后端重定向的flag，用于在循环列表中判断先后       |
|                        | io.redirect.bits.robIdx.value            | input               | 8                  | 后端重定向的位置value                            |
|                        | io.redirect.bits.level                   |                     |                    |                                                  |
| input                  | 1                                        | 后端重定向的level： |                    |                                                  |
| 1’b0：冲刷之后的指令； |                                          |                     |                    |                                                  |
| 1‘b1：冲刷这条指令本身 |                                          |                     |                    |                                                  |
| vecFeedback            | io.vecFeedback_0/1.valid                 | input               | 1                  | 来自两条流水线的向量反馈信息有效位               |
|                        | io.vecFeedback_0/1.bits                  | input               | 17                 | 来自两条流水线的向量反馈信息                     |
| query                  | io.query_0/1/2.req.ready                 | output              | 1                  | 能否接收3条数据通路中load违例检查请求            |
|                        | io.query_0/1/2.req.valid                 | input               | 1                  | 3条数据通路中load违例检查有效位                  |
|                        | io.query_0/1/2.req.bits.uop.robIdx.flag  | input               | 1                  | 3条数据通路中load违例检查uop在rob中的flag        |
|                        | io.query_0/1/2.req.bits.uop.robIdx.value | input               | 8                  | 3条数据通路中load违例检查uop在rob中的value       |
|                        | io.query_0/1/2.req.bits.uop.lqIdx.flag   | input               | 1                  | 3条数据通路中load违例检查uop在LoadQueue中的flag  |
|                        | io.query_0/1/2.req.bits.uop.lqIdx.value  | input               | 7                  | 3条数据通路中load违例检查uop在LoadQueue中的value |
|                        | io.query_0/1/2.req.bits.paddr            | input               | 48                 | 3条数据通路中load违例检查的物理地址              |
|                        | io.query_0/1/2.req.bits.data.valid       | input               | 1                  | 3条数据通路中load违例检查data的有效              |
|                        | io.query_0/1/2.resp.valid                | output              | 1                  | 3条数据通路中load违例检查响应的有效位            |
|                        | io.query_0/1/2.resp.bits.rep.frm.fetch   | output              | 1                  | 3条数据通路中load违例检查的响应                  |
|                        | io.query_0/1/2.revoke                    | input               | 1                  | 3条数据通路中load违例检查的撤销                  |
| release                | io.release.valid                         | input               | 1                  | Dcache释放块有效位                               |
|                        | io.release.bits.paddr                    | input               | 48                 | Dcache释放块的物理地址                           |
| ldwbptr                | io.ldWbPtr.flag                          | input               | 1                  | VirtualLoadQueue中writeback的flag                |
|                        | io.ldWbPtr.value                         | input               | 7                  | VirtualLoadQueue中writeback的位置value           |
| Lqfull                 | io.lqFull                                | output              | 1                  | 表示loadqueue RAR满了                            |
| performance            | io.perf_0/1_value                        | output              | 6                  | 性能计数器                                       |
