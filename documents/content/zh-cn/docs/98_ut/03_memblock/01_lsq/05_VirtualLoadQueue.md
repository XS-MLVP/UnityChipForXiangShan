---
title: VirtualLoadQueue
linkTitle: VirtualLoadQueue
weight: 12
---

**本文档参考[香山LSQ设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/tree/master/docs/memblock/LSU/LSQ)写成**

本文档撰写的内容截至[ca892e73]

请注意，本文档撰写的测试点仅供参考，如能补充更多测试点，最终获得的奖励可能更高！

# VirtualLoadQueue 简介

Virtualloadqueue是一个队列，用于存储所有load指令的微操作(MicroOp)，并维护这些load指令之间的顺序，它的功能类似于重排序缓冲区（Reorder Buffer, ROB），但专注于load指令的管理。其主要功能是跟踪Load指令执行状态，以确保在并发执行的环境中，加载操作能够正确、有序地完成。

## 整体框图

<div>			
    <center>	
    <img src="../VirtualLoadQueue_structure.png"
         alt="VirtualLoadQueue结构示意图"
         style="zoom:100%"/>
    <br>
    图1：VirtualLoadQueue结构示意图
    </center>
</div>

Virtualloadqueue最多可以存放72条指令，dispatch阶段最多支持6条指令同时入队，最多支持8条指令出队。Virtualloadqueue对于每一个 entry 中的 load 指令都有若干状态位来标识这个 load 处于什么状态：

**allocated**：该项是否分配了load，用于确定load指令的生命周期。

**isvec**：该指令是否是向量load指令。

**committed**: 该项是否提交。

# 功能简介

<mrs-functions>

## 模块功能说明

### 功能1：load指令请求入队

在调度阶段，保留站通过入队（enq）总线向VirtualLoadQueue发起入队请求，最多支持六组并发请求。成功入队的条件包括以下几点：

1. StoreQueue 和 LoadQueue 有预留空间：确保LoadQueue有足够的容量来接收新的加载指令，以避免队列溢出。确保StoreQueu有预留空间则是基于数据一致性和避免指令阻塞的考虑，因为store指令入队阻塞可能会导致load指令无法正确读取或forward到数据。
2. 入队请求有效：入队请求必须是合法的，确保指令在调度过程中可以被正确处理。
3. 指令未被冲刷：确保指令在入队时没有被系统标记为无效或被撤销。

成功入队之后，系统会执行以下操作：

1. 将指令的lqidx作为索引，将对应的allocated寄存器置1，bits信息写入uop寄存器。
2. 计算新的lqidx值，作为enq_resp传送给保留站。

### 功能2：接收load流水线写回的数据

在 load 流水线的s3阶段，load unit会将指令执行的信息通过总线 ldin 写回到 VirtualLoadQueue。具体写回信息包括：

1. 是否发生了异常以及异常类型
2. dcache是否命中
3. tlb是否命中
4. 是否为mmio指令
5. 是否为软件预取或者硬件预取
6. 是否需要重发以及重发的原因
7. 写uop的使能信号

写回需要满足的条件如下：

1. ldin 总线的 valid 信号需要拉高，表明当前正在进行有效的数据传输。
2. 指令不应需要重发（即 `need_rep` 信号为 0），否则将影响写回的正常进行。

在满足写回条件后，系统将生成相应的写回响应，具体包括以下几个方面：

1. 如果在执行过程中发生了异常、TLB命中或软件预取操作，`addrvalid` 信号将被置为 1，表示地址信息有效。
2. 如果在执行过程中发生了异常、MMIO操作、DCACHE命中并且不需要重发，或是软件预取操作，`datavalid` 信号将被置为 1，表示数据有效。
3. 指令在流水线的 S3 阶段有效（注意：不能是硬件预取指令）。当 `ldin` 总线的写使能信号 `data_wen_dup` 拉高时，将更新队列中的uop信息，以确保指令的状态及时反映。

系统将`addrvalid`和`datavalid`分开进行处理是考虑到在一些情况下，地址可以被重用，而数据可能需要重新请求（如dcache miss/mmio/软件预取等）。分开标识可以减少流水线停顿，允许处理器在地址有效时继续执行其他指令，而不必等待数据有效性确认，从而优化整体性能。

### 功能3：load指令的出队(提交)

1. 出队时机：当被分配的entries（allocated为高）到达队头，同时allocated与committed都为1时，表示可以出队，如果是向量load，需要每个元素都committed。

</mrs-functions>

## 接口说明

|             | name                                               | I/O    | width | description                                                  |
| ----------- | -------------------------------------------------- | ------ | ----- | ------------------------------------------------------------ |
| redirect    | io.redirect.valid                                  | input  | 1     | 后端重定向有效位                                             |
|             | io.redirect.bits.robIdx.flag                       | input  | 1     | 后端重定向相关信息                                           |
|             | io.redirect.bits.robIdx.value                      | input  | 8     | 后端重定向相关信息                                           |
|             | io.redirect.bits.level                             | input  | 1     | 后端重定向相关信息                                           |
| enq         | io.enq.canAccept                                   | output | 1     | Lq能否接收派遣指令                                           |
|             | io.enq.sqcanAccept                                 | input  | 1     | sq能否接收派遣至零                                           |
|             | io.enq.needAlloc_0~5                               | input  | 1     |                                                              |
|             | io.enq.req_0~5.valid                               | input  | 1     | 入队请求的有效信号                                           |
|             | io.enq.req_0~5.bits.robIdx.flag                    | input  | 1     | 入队请求ROB指针的flag                                        |
|             | io.enq.req_0~5.bits.robIdx.value                   | input  | 8     | 入队请求ROB指针的value                                       |
|             | io.enq.req_0~5.bits.lqIdx.value                    | input  | 7     | 入队请求lqidx的value                                         |
|             | io.enq.req_0~5.bits.numLsElem                      | input  | 5     | 1. 向量寄存器的总位宽为128位，每个向量元素的大小为8位，因此每个向量寄存器可以存储16个，numLsElem表示向量寄存器中元素的个数，因此位宽为5。 2. 如果是标量值零，numLsElem的值恒为5‘b1 3. 如果是向量指令，每个端口的numLsElem的最大值为[16 2 2 2 2 2] |
| ldin        | io.ldin_0/1/2.valid                                | input  | 1     | load写回到loadqueue的信息有效                                |
|             | io.ldin_0/1/2.bits.uop.cf.exceptionVec_3/4/5/13/21 | input  | 1     | Load写回到流水线的指令发生异常                               |
|             | io.ldin_0/1/2.bits.uop.robIdx_flag                 | input  | 1     | load写回lq指令的rob指针的flag                                |
|             | io.ldin_0/1/2.bits.uop.robIdx_value                | input  | 8     | load写回lq指令的rob指针的value                               |
|             | io.ldin_0/1/2.bits.uop.lqIdx.value                 | input  | 7     | load写回lq指令的lq指针的value                                |
|             | io.ldin_0/1/2.bits.miss                            | input  | 1     | Load写回到Lq的指令发生cacheMiss                              |
|             | io.ldin_0/1.bits.tlbMiss                           | input  | 1     | Load写回到Lq的指令发生tlbMiss                                |
|             | io.ldin_0/1/2.bits.mmio                            | input  | 1     | Load写回到Lq的指令是MMIO指令                                 |
|             | io.ldin_0/1/2.bits.isPrefetch                      | input  | 1     | 指令为预取操作，预取分为软件预取和硬件预取                   |
|             | io.ldin_0/1/2.bits.isHWPrefetch                    | input  | 1     | 指令为硬件预取                                               |
|             | io.ldin_0/1/2.bits.dcacheRequireReplay             | input  | 1     | Load写回到Lq的指令需要replay                                 |
|             | io.ldin_0/1/2.bits.rep.info.cause_0~9              | input  | 1     | Load写回到Lq的指令需要replay的原因： =0：st-ld violention predirect =1：tlb miss =2：st-ld forward =3：dcache replay =4：dcache miss =5：wpu predict fail =6：dcache bank conflict =7：RAR queue nack =8：RAW queue nack =9：st-ld violention |
|             | io.ldin_0/1/2.bits.data_wen_dup_1                  | input  | 1     | uop信息的写入使能信号                                        |
| ldWbPtr     | io.ldWbPtr.flag                                    | output | 1     | writeback指针的flag                                          |
|             | io.ldWbPtr.value                                   | output | 7     | writeback指针的value                                         |
| lqEmpty     | io.lqEmpty                                         | output | 1     | Lq是否空                                                     |
| lqDeq       | io.lqDeq                                           | output | 3     | 出队表项数量                                                 |
| lqCancelCnt | io.lqCancelCnt                                     | output | 7     | 后端发生重定向时取消的load数量                               |