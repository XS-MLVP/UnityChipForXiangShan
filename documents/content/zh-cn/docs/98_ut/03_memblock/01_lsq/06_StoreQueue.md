---
title: StoreQueue
linkTitle: StoreQueue
weight: 12
---

**本文档参考[香山LSQ设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/tree/master/docs/memblock/LSU/LSQ)写成**

本文档撰写的内容截至[ca892e73]

请注意，本文档撰写的测试点仅供参考，如能补充更多测试点，最终获得的奖励可能更高！

# StoreQueue 简介

StoreQueue是一个队列，用来装所有的 store 指令，功能如下：

- 在跟踪 store 指令的执行状态

- 存储 store 的数据，跟踪数据的状态（是否到达）

- 为load提供查询接口，让load可以forward相同地址的store

- 负责 MMIO store和NonCacheable store的执行

- 将被 ROB 提交的 store 写到 sbuffer 中

- 维护地址和数据就绪指针，用于LoadQueueRAW的释放和LoadQueueReplay的唤醒

store进行了地址与数据分离发射的优化，即 StoreUnit 是 store 的地址发射出来走的流水线，StdExeUnit 是 store 的数据发射出来走的流水线，是两个不同的保留站，store 的数据就绪了就可以发射到 StdExeUnit，store 的地址就绪了就可以发射到 StoreUnit。

## 整体框图

<div>			
    <center>	
    <img src="../StoreQueue_structure.svg"
         alt="StoreQueue结构示意图"
         style="zoom:100%"/>
    <br>
    图1：StoreQueue结构示意图<br><br>
    </center>
</div>

StoreQueue最多可以存放64条指令，**store queue 中重要的状态位有：**

- allocated：RS在storeQueue队列有空闲时，会设置这个entry的allocated状态，开始记录这条store 的生命周期。同时发射到StoreUnit/ StdExeUnit 2条流水。当这条store指令被提交到Sbuffer时，allocated状态被清除。
- addrvalid：在StoreUnit的S1更新，表示是否已经经过了地址转换得到物理地址，用于 load forward 检查时的 cam 比较。
- datavalid：在StdExeUnit 的S1更新，表示store 的数据是否已经被发射出来，是否已经可用
- committed：在store 是否已经被 ROB commit 了
- pending：在StoreUnit的S2更新，在这条 store 是否是 MMIO 空间的 store，主要是用于控制 MMIO 的状态机
- mmio：在StoreUnit的S2更新，这条 store 是否是 MMIO 空间的 store，主要是用于控制对 sbuffer 的写

## 非对齐store指令

StoreQueue支持处理非对齐的Store指令，每一个非对齐的Store指令占用一项，并在写入dataBuffer对地址和数据对齐后写入。

## 向量store指令

如图2所示，StoreQueue会给向量store指令预分配一些项。

StoreQueue通过vecMbCommit控制向量store的提交：

1. 针对每个 store，从反馈向量 fbk 中获取相应的信息。

2. 判断该 store 是否符合提交条件（valid 且标记为 commit 或 flush），并且检查该 store 是否与 uop(i) 对应的指令匹配（通过 robIdx 和 uopIdx）。只有当满足所有条件时，才会将该 store 标记为提交。判断VecStorePipelineWidth内是否有指令满足条件，满足则判断该向量store提交，否则不提交。

3. 特殊情况处理（跨页 store 指令）:

在特殊情况下（当 store 跨页且 storeMisalignBuffer 中有相同的 uop），如果该 store 符合条件`io.maControl.toStoreQueue.withSameUop`，会强制将 vecMbCommit设置为 true，表示该 store 无论如何都已提交。

<div>			
    <center>	
    <img src="../StoreQueue_Vector.svg"
         alt="向量store指令示意图"
         style="zoom:100%"/>
    <br>
    图2：向量store指令<br><br>
    </center>
</div>


# 功能简介

<mrs-functions>

## 模块功能说明

### 功能1：store指令请求入队

1. StoreQueue 每次最多会有 2 个 entry 入队，通过入队指针 enqPtrExt 控制。在 dispatch 阶段最多可以分配2个 entry，指针每次右移 1 位或 2 位。

2. 通过比较入队指针 enqPtrExt 和出队指针 deqPtrExt 得出已经在队列中有效 entry。只有空闲的 entry 大于需要请求入队的指令时才会分配 entry 入队。

3. 入队时设置 entry 的状态位 allocated 为 true，其他状态位都为 false。

### 功能2：指令的出队

1. StoreQueue 每次最多会有2个 entry 出队释放，通过输出指针 deqPtrExt 控制，每次指针右移一位或 2 位。

2. STQ 出队的触发信号是isbuffer(i).fire延后一拍的信号，因为 sbuffer 的写动作要用 2 拍完成，在 sbuffer 写完成之前 entry 不释放可以继续 forward 数据。

### 功能3：从store的地址流水线写回结果

store 的地址从保留站发出来后会经过 StoreUnit 流水线，通过lsq/lsq_replenish总线接口在S1/S2把地址信息更新到store queue 中：

1. 在store流水线s1阶段，获得 DTLB hit/miss 的信息, 以及指令的虚拟地址vaddr和物理地址paddr

2. 在store流水线s2阶段，获得 mmio/pmp 信息，以及是否是mmio地址空间操作等信息

### 功能4：接收 store 的数据到STQ 的Datamodule

store 的数据是从与地址不同的保留站发出来的后经过`StdExeUnit`流水线，通过`storeDataIn`接口在S0/S1把数据写到对应的entry的`datamodule`里:

1. S0：给`datamodule`发写请求

2. S1：写入数据到`datamodule`同时更新 entry 的`datavalid`属性为True，接收 store 的mask到STQ 的`Datamodule`

store 的地址从保留站发出来之后会经过`StoreUnit`流水线，`s0_mask_out`在S0把地址中的mask信息更新到对应entry的`datamodule`里。

### 功能5：为 load 提供 forward 查询

1. load 需要查询 store queue 来找到在它之前相同地址的与它最近的那个 store 的数据。
    - 查询总线(`io.forwrd.sqIdx`) 和 StoreQueue 的出栈指针比较，找出所有比 load 指令老的 storeQueue 中的 entry。以 flag 相同或不同分为2种情况：

(1)same flag-> older Store范围是 (tail, sqIdx)，如图3(a)所示

(2)different flags-> older Store范围是(tail, VirtualLoadQueueSize) +(0, sqIdx)，如图3(b)所示

<div>			
    <center>	
    <img src="../StoreQueue_Forward_Mask.svg"
         alt="StoreQueue前递范围生成"
         style="zoom:100%"/>
    <br>
    图3：StoreQueue前递范围生成<br><br>
    </center>
</div>

2. 查询总线用va 和pa同时查询，如果发现物理地址匹配但是虚拟地址不匹配；或者虚拟地址匹配但是物理地址不匹配的情况就需要将那条 load 设置为 replayInst，等 load 到 ROB head 后replay。

3. 如果只发现一笔 entry 匹配且数据准备好，则直接 forward

4. 如果只发现一笔 entry 匹配且数据没有准备好，就需要让保留站负责重发

5. 如果发现多笔匹配，则选择最老的一笔 store forward，StoreQueue以1字节为单位，采用树形数据选择逻辑,如图4

<div>			
    <center>	
    <img src="../StoreQueue_Forward.svg"
         alt="StoreQueue前递数据选择"
         style="zoom:100%"/>
    <br>
    图4：StoreQueue前递数据选择<br><br>
    </center>
</div>

6. store 指令能被 load forward的条件：
    - allocated：这条 store 还在 store queue 内，还没有写到 sbuffer
    - datavalid：这条 store 的数据已经就绪
    - addrvalid：这条 store 已经完成了虚实地址转换，得到了物理地址

7. SSID (Store-Set-ID) 标记了之前 load 预测执行失败历史信息，如果当前 load 命中之前历史中的SSID，会等之前所有 older 的 store 都执行完；如果没有命中就只会等pa相同的 older Store 执行完成。

### 功能6：MMIO与NonCacheable Store指令

- **MMIO Store指令执行**:

1. MMIO 空间的 store 也只能等它到达 ROB 的 head 时才能执行，但是跟 load 稍微有些不同，store 到达 ROB 的 head 时，它不一定位于 store queue 的尾部，有可能有的 store 已经提交，但是还在 store queue 中没有写入到 sbuffer，需要等待这些 store 写到 sbuffer 之后，才能让这条 MMIO 的 store 去执行。

2. 利用一个状态机去控制MMIO的store执行

    - s_idle：空闲状态，接收到MMIO的store请求后进入到s_req状态;

    - s_req：给MMIO通道发请求，请求被MMIO通道接受后进入s_resp状态;

    - s_resp：MMIO通道返回响应，接收后记录是否产生异常，并进入到 s_wb 状态

    - s_wb：将结果转化为内部信号，写回给 ROB，成功后,如果有异常，则进入s_idle, 否则进入到 s_wait 状态

    - s_wait：等待 ROB 将这条 store 指令提交，提交后重新回到 s_idle 状态

- **NonCacheable Store指令执行**：

1. NonCacheable空间的store指令，需要等待上一个NonCacheable Store指令提交之后，才能从StoreQueue按序发送请求

2. 利用一个状态机去控制NonCacheable的store执行

    - nc_idle：空闲状态，接收到NonCacheable的store请求后进入到nc_req状态;

    - nc_req：给NonCacheable通道发请求，请求被NonCachable通道接受后, 如果启用uncacheOutstanding功能，则进入nc_idle，否则进入nc_resp状态;

    - nc_resp：接受NonCacheable通道返回响应，并进入到nc_idle状态

### 功能7：store指令提交以及写入SBuffer

StoreQueue采用提前提交的方式进行提交。

- **提前提交规则**:

1. 检查进入提交阶段的条件

    (1)指令有效。

    (2)指令的ROB对头指针不超过待提交指针。

    (3)指令不需要取消。

    (4)指令不等待Store操作完成，或者是向量指令

2. 如果是CommitGroup的第一条指令, 则

    (1)检查MMIO状态: 没有MMIO操作或者有MMIO操作并且MMIO store以及提交。

    (2)如果是向量指令，需满足vecMbCommit条件。

3. 如果不是CommitGroup的第一条指令，则：

    (1)提交状态依赖于前一条指令的提交状态。

    (2)如果是向量指令，需满足vecMbCommit条件。

提交之后可以按顺序写到 sbuffer, 先将这些 store 写到 dataBuffer 中，dataBuffer 是一个两项的缓冲区（0，1通道），用来处理从大项数 store queue 中的读出延迟。只有0通道可以编写未对齐的指令,同时为了简化设计，即使两个端口出现异常，但仍然只有一个未对齐出队。

- **写入sbuffer的过程**：

1. 写入有效信号生成

2. 0通道指令存在非对齐且跨越16字节边界时：

    (1) 0通道的指令已分配和提交

    (2) dataBuffer的0，1通道能同时接受指令，

    (3) 0通道的指令不是向量指令，并且地址和数据有效；或者是向量且vsMergeBuffer以及提交。

    (4) 没有跨越4K页表；或者跨越4K页表但是可以被出队,并且1）如果是0通道：允许有异常的数据写入; 2）如果是1通道：不允许有异常的数据写入。

    (5) 之前的指令没有NonCacheable指令，如果是第一条指令，自身不能是Noncacheable指令
3. 否则，需要满足：

    (1) 指令已分配和提交。

    (2) 不是向量且地址和数据有效，或者是向量且vsMergeBuffer以及提交。

    (3) 之前的指令没有NonCacheable和MMIO指令，如果是第一条指令，自身不能是Noncacheable和MMIO指令。

    (4) 如果未对齐store，则不能跨越16字节边界，且地址和数据有效或有异常

- **地址和数据生成**：

1. 地址拆分为高低两部分：

    (1) 低位地址：8字节对齐地址

    (2) 高位地址：低位地址加上8偏移量

2. 数据拆分为高低两部分：

    (1) 跨16字节边界数据：原始数据左移地址低4位偏移量包含的字节数

    (2) 低位数据：跨16字节边界数据的低128位；

    (3) 高位数据：跨16字节边界数据的高128位；

3. 写入选择逻辑：

    如果dataBuffer能接受非对齐指令写入,通道0的指令是非对齐并且跨越了16字节边界，则检查：

    (1) 是否跨4K页表同时跨4K页表且可以出队: 通道0使用低位地址和低位数据写入dataBuffer; 通道1使用StoreMisaligBuffer的物理地址和高位数据写入dataBuffer

    (2) 否则: 通道0使用低位地址和低位数据写入dataBuffer; 通道1使用高位地址和高位数据写入dataBuffer

    (3) 如果通道指令没有跨越16字节并且非对齐，则使用16字节对齐地址和对齐数据写入dataBuffer

    (4) 否则，将原始数据和地址写给dataBuffer

### 功能8：强制刷新sbuffer

StoreQueue采用双阈值的方法控制强制刷新Sbuffer：上阈值和下阈值。

1. 当StoreQueue的有效项数大于上阈值时， StoreQueue强制刷新Sbuffer
2. 直到StoreQueue的有效项数小于下阈值时，停止刷新Sbuffer。

</mrs-functions>

## 接口说明

| name               | description                                                  |
| ------------------ | ------------------------------------------------------------ |
| enq                | 接收来自外部模块的信息，包含入队请求、控制信号等             |
| brqRedirect        | 分支重定向信号                                               |
| vecFeedback        | 向量反馈信息                                                 |
| storeAddrIn        | store指令的地址                                              |
| storeAddrInRe      | store指令的地址，用于处理MMIO 和异常情况                     |
| storeDataIn        | store指令的数据                                              |
| storeMaskIn        | 传递store掩码，从保留站（RS）发送到 Store Queue（SQ）。store掩码通常用于指示哪些字节在store操作中是有效的。 |
| sbuffer            | 存储已提交的 Store 请求到sbuffer                             |
| uncacheOutstanding | 指示是否有未完成的uncached请求                               |
| cmoOpReg           | 发送缓存管理操作请求                                         |
| cmoOpResp          | 接收缓存管理操作的响应                                       |
| mmioStout          | 写回uncache的存储操作的结果                                  |
| forward            | 查询forwarding信息                                           |
| rob                | 接收来自 ROB 的信号或数据                                    |
| uncache            | 发送数据或信号给 uncache 模块                                |
| flushSbuffer       | 冲刷sbuffer缓冲区                                            |
| sqEmpty            | 标识store queue为空                                          |
| stAddrReadySqPtr   | 指向当前准备好地址的 store 指令                              |
| stAddrReadyVec     | 向量中对应 store 指令的地址是否已经准备好                    |
| stDataReadySqPtr   | 指向当前准备好数据的 store 指令                              |
| stDataReadyVec     | 向量中对应 store 指令的数据是否已经准备好                    |
| stIssuePtr         | 跟踪当前发出的store请求                                      |
| sqCancelCnt        | 指示在store queue中可以被取消的请求数量                      |
| sqDeq              | 当前store queue中出队的请求位置                              |
| force_write        | 是否强制写入存储操作                                         |
| maControl          | 与存储管理缓冲区（MA）进行控制信号的交互                     |