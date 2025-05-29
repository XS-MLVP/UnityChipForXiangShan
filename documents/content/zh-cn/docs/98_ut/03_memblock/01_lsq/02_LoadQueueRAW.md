---
title: LoadQueueRAW
linkTitle: LoadQueueRAW
weight: 12
---

**本文档参考[香山LSQ设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/tree/master/docs/memblock/LSU/LSQ)写成**

本文档撰写的内容截至[ca892e73]

请注意，本文档撰写的测试点仅供参考，如能补充更多测试点，最终获得的奖励可能更高！

# LoadQueueRAW 简介

LoadQueueRAW是用于处理store-load违例的。由于load和store在流水线中都是乱序执行，会经常出现load越过了更老的相同地址的store，即这条load本应该前递store的数据，但是由于store地址或者数据没有准备好，导致这条load没有前递到store的数据就已经提交，后续使用这条load结果的指令也都发生了错误，于是产生store to load forwarding违例。

当store address通过STA保留站发射出来进入store流水线时，会去查询LQRAW中在这条store后面的所有已经完成访存的相同地址的load，以及load流水线中正在进行的在该条store之后的相同地址的load，一旦发现有，就发生了store to load forwarding违例，可能有多个load发生了违例，需要找到离store最近的load，也就是最老的违例的load，然后给RedirectGenerator部件发送重定向请求，冲刷最老的违例的load及之后的所有指令。

当store流水线执行cbo zero指令时，也需要进行store-load违例检查。

## st-ld违例

在现代处理器中，Load 和 Store 指令通常采用乱序执行的方式进行处理。这种执行策略旨在提高处理器的并行性和整体性能。然而，由于 Load 和 Store 指令在流水线中的乱序执行，常常会出现 Load 指令越过更早的相同地址的 Store 指令的情况。这意味着，Load 指令本应通过前递（forwarding）机制从 Store 指令获取数据，但由于 Store 指令的地址或数据尚未准备好，导致 Load 指令未能成功前递到 Store 的数据，而 Store 指令已被提交。由此，后续依赖于该 Load 指令结果的指令可能会出现错误，这就是 st-ld 违例。

考虑以下伪代码示例：

```
ST R1, 0(R2)  ; 将 R1 的值存储到 R2 指向的内存地址
LD R3, 0(R2)  ; 从 R2 指向的内存地址加载值到 R3
ADD R4, R3, R5 ; 使用 R3 的值进行计算
```

假设在这个过程中，Store 指令由于某种原因（如缓存未命中）未能及时完成，而 Load 指令已经执行并读取了旧的数据（例如，从内存中读取到的值为 `0`）。此时，Load 指令并未获得 Store 指令更新后的值，导致后续计算的数据错误。

通过上述例子，可以清楚地看到 Store-to-Load 违例如何在乱序执行的环境中导致数据一致性问题。这种问题强调了在指令调度和执行过程中，确保正确的数据流动的重要性。现代处理器通过多种机制来检测和解决这种违例，以维护程序的正确性和稳定性。

## 整体框图

<div>			
    <center>	
    <img src="../LoadQueueRAW_structure.svg"
         alt="LoadQueueRAW结构示意图"
         style="zoom:100%"/>
    <br>
    图1：LoadQueueRAW结构示意图<br><br>
    </center>
</div>

LoadQueueRAW最多能够存储64条指令，通过FreeList子模块管理空闲资源。FreeList 中存储的是 entry 的编号。当一条指令满足入队条件时，FreeList 会为其分配一个 entry 编号，并将该指令存放在相应的 entry 中。指令出队时，需要释放所占用的 entry 资源，并将条目编号重新放回 FreeList 中，以供后续指令使用。Load指令在s2阶段在 LoadQueueRAR 中查询 store-to-load 违例，在s3阶段返回响应。

<mrs-functions>

## 模块功能说明

### 功能1：发生st-ld违例的指令请求入队

当query到达load流水线的s2时，判断是否满足入队条件，如果在当前load指令之前有地址未准备好的store指令，且当前指令没有被flush时，当前load可以入队。具体流程如下：

1. 判断入队条件：检查在当前 Load 指令之前是否存在未准备好的 Store 指令。如果存在这样的 Store 指令，并且当前 Load 指令尚未被冲刷（flush），则当前 Load 指令可以入队。
2. 分配 Entry 和 Index：在 Freelist 中，系统将获得一个可分配的 Entry 及其对应的 Index，以便为 Load 指令分配资源。
3. 保存物理地址：在 PaddrModule 中将入队的 Load 指令的物理地址保存到对应的 Entry。这一操作确保在后续访问中能够正确引用该地址。
4. 保存掩码信息：在 MaskModule 中，系统将入队的 Load 指令的掩码信息保存到对应的 Entry。掩码信息用于后续的地址匹配和数据访问。
5. 写入uop：将 Load 指令的uop信息写入到相应的结构中，以完成入队过程。

### 功能2：检测st-ld违例条件

在 Store 指令到达 Store 流水线的 s1 阶段时，系统会进行 Store-to-Load 违例检查。此时，Store 指令需要与 Load Queue 中已经完成访存的 Load 指令，以及在 Load 流水线 s1 和 s2 阶段正在访存的 Load 指令进行比较。这些 Load 指令可能尚未通过前递（forwarding）机制获取 Store 指令执行的结果。

具体的违例检查流程如下：

1. 物理地址匹配：在第一拍中，系统将进行物理地址匹配，并检查条件。此时，将匹配在当前 Store 指令之后的所有新的 Load 指令。如果这些 Load 指令已经成功获取了数据（`datavalid`），或者由于缓存未命中正在等待数据回填（`dcache miss`），则可以确定这些 Load 指令不会将数据前递给当前的 Store 指令。
2. 匹配 Load 指令：在第二拍中，Store 流水线中的 Store 指令根据匹配结果中的掩码（mask），在 Load Queue 的 RAW（Read After Write）结构中查找所有匹配的 Load 指令。Load Queue 中共有 32 项，这些项将被平分为4组。每组从 8 项中选出一个最老的 Load 指令，最多可得到 4 个候选最老的 Load 指令。
3. 选择最老的 Load：在第三拍中，从上述 4 个候选最老的 Load 指令中，系统将选出一个最老的 Load 指令，作为最终的目标。
4. 处理违例情况：在第四拍中，如果在两条 Store 流水线中均发生了 Store-to-Load 违例，系统将从各自的 Queue 中匹配到的最老 Load 指令中选出一个更老的 Load 指令，以产生回滚请求并发送给重定向模块（Redirect）。此时，违例的条件包括：
    - Load 和 Store 的地址相同。
    - Load 指令比 Store 指令年轻。
    - Load 指令已经成功获取了数据。

### 功能3：指令的出队

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

|                  | name                                     | I/O    | width | Description                                                  |
| ---------------- | ---------------------------------------- | ------ | ----- | ------------------------------------------------------------ |
| redirect         | io.redirect.valid                        | input  | 1     | 后端重定向的有效位                                           |
|                  | io.redirect.bits.robIdx.flag             | input  | 1     | 后端重定向的flag，用于在循环列表中判断先后                   |
|                  | io.redirect.bits.robIdx.value            | input  | 8     | 后端重定向的位置value                                        |
|                  | io.redirect.bits.level                   | input  | 1     | 后端重定向的level：1’b0：冲刷之后的指令；1‘b1：冲刷这条指令本身 |
| vecFeedback      | io.vecFeedback_0/1.valid                 | input  | 1     | 来自两条流水线的向量反馈信息有效位                           |
|                  | io.vecFeedback_0/1.bits                  | input  | 17    | 来自两条流水线的向量反馈信息                                 |
| query            | io.query_0/1/2.req.ready                 | output | 1     | 能否接收3条数据通路中load违例检查请求                        |
|                  | io.query_0/1/2.req.valid                 | input  | 1     | 3条数据通路中load违例检查有效位                              |
|                  | io.query_0/1/2.req.bits.uop.robIdx.flag  | input  | 1     | 3条数据通路中load违例检查uop在rob中的flag                    |
|                  | io.query_0/1/2.req.bits.uop.robIdx.value | input  | 8     | 3条数据通路中load违例检查uop在rob中的value                   |
|                  | io.query_0/1/2.req.bits.uop.lqIdx.flag   | input  | 1     | 3条数据通路中load违例检查uop在LoadQueue中的flag              |
|                  | io.query_0/1/2.req.bits.uop.lqIdx.value  | input  | 7     | 3条数据通路中load违例检查uop在LoadQueue中的value             |
|                  | io.query_0/1/2.req.bits.paddr            | input  | 48    | 3条数据通路中load违例检查的物理地址                          |
|                  | io.query_0/1/2.req.bits.data.valid       | input  | 1     | 3条数据通路中load违例检查data的有效                          |
|                  | io.query_0/1/2.revoke                    | input  | 1     | 3条数据通路中load违例检查的撤销                              |
| storeIn          | storeIn_0/1.bits                         | input  | 84    | 两条store流水线store指令相关信息                             |
|                  | storeIn_0/1.valid                        | input  | 1     | 两条store流水线store指令相关信息有效位                       |
| rollback         | rollback_0/1.valid                       | output | 1     | 两条store流水线回滚信息的有效性                              |
|                  | rollback_0/1.bits                        | output | 31    | 两条store流水线回滚信息                                      |
| stAddrReadySqPtr | stAddrReadySqPtr                         | input  | 7     | 指向 store 队列中已准备好的地址条目                          |
| stIssuePtr       | stIssuePtr                               | input  | 7     | 指向 store 队列中准备发射执行的指令条目                      |
| lqFull           | lqFull                                   | output | 1     | 判断队列是否满                                               |