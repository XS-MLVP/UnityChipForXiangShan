---
title: LoadQueueUncache
linkTitle: LoadQueueUncache
weight: 12
---

**本文档参考[香山LSQ设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/tree/master/docs/memblock/LSU/LSQ)写成**

本文档撰写的内容截至[66e9b546]

请注意，本文档撰写的测试点仅供参考，如能补充更多测试点，最终获得的奖励可能更高！

# LoadQueueUncache 简介

LoadQueueUncache 和 Uncache 模块，对于 uncache load 访问请求来说，起到一个从 LoadUnit 流水线到总线访问的中间站作用。其中 Uncache 模块，作为靠近总线的一方，主要用于处理 uncache 访问到总线的请求和响应。LoadQueueUncache 作为靠近流水线的一方，需要承担以下责任：

1. 接收 LoadUnit 流水线传过来的 uncache load 请求。

2. 选择已准备好 uncache 访问的 uncache load 请求 发送到 Uncache Buffer。

3. 接收来自 Uncache Buffer 的处理完的 uncache load 请求。

4. 将处理完的 uncache load 请求 返回给 LoadUnit。

LoadQueueUncache 结构上，目前有 4 项（项数可配）UncacheEntry，每一项独立负责一个请求并利用一组状态寄存器控制其具体处理流程；有一个 FreeList，管理各项分配和回收的情况。而 LoadQueueUncache 主要是协同 4 项的新项分配、请求选择、响应分派、出队等统筹逻辑。

## 整体框图

<div>			
    <center>	
    <img src="../LoadQueueUncache_structure.svg"
         alt="LoadQueueUncache结构示意图"
         style="zoom:100%"/>
    <br>
    图1：LoadQueueUncache结构示意图
    </center>
</div>

UnCacheBuffer 最多存放4条指令，除了 FreeList 之外，另一个重要的子模块是 UncacheEntry，管理每个Uncahce请求，负责发起Uncache，写回Uncache数据。每个Entry内维护一个用于发起Uncache请求的状态机，状态机的状态转换图如下：

<div>			
    <center>	
    <img src="../UncacheEntry.png"
         alt="UncacheEntry结构示意图"
         style="zoom:100%"/>
    <br>
    图2：UncacheEntry状态转换图
    </center>
</div>

- s_idl:该项还未发起一个MMIO请求。

- s_req:向uncache模块发起MMIO请求，等待请求被接收。

- s_resp:等待uncache模块的MMIO响应。

- s_wait:等待将MMIO结果写回流水线。

# 功能简介

<mrs-functions>

## 模块功能说明

### 功能1：Uncache指令请求入队

LoadQueueUncache 负责接收来自 LoadUnit 0、1、2 三个模块的请求，这些请求可以是 MMIO 请求，也可以是 NC 请求。

1. 首先，系统会根据请求的 robIdx 按照时间顺序（从最老到最新）对请求进行排序，以确保最早的请求能优先分配到空闲项，避免特殊情况下因老项回滚（rollback）而导致死锁。

2. 进入入队处理的条件是：请求没有重发、没有异常，并且系统会根据 FreeList 中可分配的空闲项依次为请求分配项。

3. 当 LoadQueueUncache 达到容量上限，且仍有请求未分配到项时，系统会从这些未分配的请求中选择最早的请求进行 rollback。

UncacheBuffer 的入队分为 s1 和 s2 两个阶段：

s1：

- **请求收集**：通过 `io.req.map(_.bits)` 收集所有请求的内容，形成 `s1_req` 向量。

- **有效性标记**：通过 `io.req.map(_.valid)` 收集所有请求的有效性，形成 `s1_valid` 向量。

s2：

执行入队操作，主要分为以下几步：

- 使用 `RegEnable` 将 **s1** 阶段的请求 `s1_req` 注册到 `s2_req`，确保在请求有效时保持其状态。

- 通过以下条件生成`s2_valid`向量，判断每个请求是否有效：
    
    1. `RegNext(s1_valid(i))`：确保请求在 **s1** 阶段有效。
    
    2. `!s2_req(i).uop.robIdx.needFlush(RegNext(io.redirect))`：确保请求的 ROB 索引不需要因重定向而被刷新。
    
    3. `!s2_req(i).uop.robIdx.needFlush(io.redirect)`：确保请求的 ROB 索引不需要因当前重定向而被刷新。

- 检查每个请求是否需要重发，结果存储在 `s2_need_replay` 向量中。

- 在 **s2** 阶段，使用 `s2_enqueue` 向量来决定哪些请求成功入队。入队条件包括：

    - `s2_valid(w)`：请求在 **s2** 阶段有效。

    - `!s2_has_exception(w)`：请求没有异常。

    - `!s2_need_replay(w)`：请求不需要重发。

    - `s2_req(w).mmio`：请求是一个内存映射 IO（MMIO）请求。

- 通过 `enqValidVec` 和 `enqIndexVec` 的有效管理，确保每个加载请求在满足有效性和可分配条件时能够正确地申请和分配FreeList槽位。

### 功能2：Uncache指令的出队

1. 当一个项完成 Uncache 访问操作并返回给 LoadUnit ，或被 redirect 刷新时，则该项出队并释放 FreeList 中该项的标志。

    具体流程如下：

    - 计算`freeMaskVec`掩码，用于标记每个槽位的释放状态，指示相应槽位是否可用。

    - 如果当前条目被选择 (`e.io.select`) 且其输出信号有效 (`e.io.ldout.fire`)，则对应槽位的释放状态被标记为 `true`，表示该槽位可用。

    - 如果接收到刷新信号 (`e.io.flush`)，同样将对应槽位的释放状态设置为 `true`。

2. 同一拍可能有多个项出队。返回给 LoadUnit 的请求，会在第一拍中选出，第二拍返回。

3. 其中，可供处理 uncache 返回请求的 LoadUnit 端口是预先设定的。当前，MMIO 只返回到 LoadUnit 2；NC 可返回到 LoadUnit 1\2。在多个端口返回的情况下，利用 uncache entry id 与端口数的余数，来指定每个项可以返回到的 LoadUnit 端口，并从该端口的候选项中选择一个项进行返回。

### 功能3：Uncache交互逻辑

1. 发送 req

第一拍先从当前已准备好 uncache 访问中选择一个，第二拍将其发送给 Uncache Buffer。发送的请求中，会标记选中项的 id，称为 mid 。其中是否被成功接收，可根据 req.ready 判断。

2. 接收 idResp

如果发送的请求被 Uncache Buffer 接收，那么会在接收的下一拍收到 Uncache 的 idResp。该响应中，包含 mid 和 Uncache Buffer 为该请求分配 entry id（称为 sid）。LoadQueueUncache 利用 mid 找到内部对应的项，并将 sid 存储在该项中。

3. 接收 resp

待 Uncache Buffer 完成该请求的总线访问后，会将访问结果返回给 LoadQueueUncache。该响应中，包含 sid。考虑到 Uncache Buffer 的合并特性（详细入队合并逻辑见 Uncache），一个 sid 可能对应 LoadQueueUncache 的多个项。LoadQueueUncache 利用 sid 找到内部所有相关项，并将访问结果传递给这些项。

### 功能4：Uncache回滚检测

freelist 没有空闲表现导致 MMIO Load 进入 UncacheBuffer 失败时需要进行 rollback，此
时需要根据 robidx 选择不能入队的 MMIO 中最老的指令进行 rollback。整个流程分为以下几个周期：

- Cycle 0：进行 uncache 请求入队。

- Cycle 1：选择最旧的 uncache 加载请求。

- Cycle 2：发出重定向请求。

    - 从 load 流水线中选择最旧的 load 请求。

    - 根据检测到的拒绝情况准备重定向请求。

    - 如果重定向请求有效，则发出请求。

使用 `selectOldestRedirect` 函数来选择最旧的重定向请求，具体步骤如下：

- 比较向量生成：

    - 创建一个比较向量 `compareVec`，用于判断请求的顺序，比较每个请求的 ROB 索引。

- 生成独热编码结果：

    - `resultOnehot` 向量根据有效性和比较结果生成，标记出最旧的可重定向请求。

</mrs-functions>

## 接口说明

| name        | I/O    | description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| redirect    | input  | 后端重定向相关信息                                           |
| req         | input  | 接收写入请求                                                 |
| ldout       | output | 写回 MMIO 数据接口，输出 MemExuOutput 类型的数据，处理与 MMIO 的写回操作 |
| ld_raw_data | output | 读取原始数据输出接口                                         |
| rob         | input  | 接收来自 ROB 的信号或数据                                    |
| uncache     | output | 发送数据或信号给 uncache 模块                                |
| rollback    | output | 当 uncache 缓存满时，从前端进行回滚                          |