---
title: LoadQueueReplay
linkTitle: LoadQueueReplay
weight: 12
---

**本文档参考[香山LSQ设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/tree/master/docs/memblock/LSU/LSQ)写成**

本文档撰写的内容截至[ca892e73]

请注意，本文档撰写的测试点仅供参考，如能补充更多测试点，最终获得的奖励可能更高！

# LoadQueueReplay 简介

LoadQueueReplay 模块是现代处理器架构中用于处理 Load 指令重发的重要组成部分。它负责管理因各种原因而需要重发的 Load 指令，确保指令执行的正确性和高效性。

## 整体框图

<div>			
    <center>	
    <img src="../LoadQueueReplay_structure.png"
         alt="LoadQueueReplay结构示意图"
         style="zoom:100%"/>
    <br>
    图1：LoadQueueReplay结构示意图<br><br>
    </center>
</div>

LoadQueueReplay 最多存放72条指令，涉及多个状态和存储的信息。其关键组成部分如下：

- **Allocated**：
  - 表示某个 Load 重发队列项是否已经被分配，反映该项的有效性。
- **Scheduled**：
  - 指示某个 Load 重发队列项是否已被调度，意味着该项已经被选出，并将被发送至 Load Unit 进行重发。
- **Uop**：
  - 该队列项对应的 Load 指令执行信息，包括微操作（uop）。
- **Cause**：指示该 Load 指令重发的原因，主要包括以下几种情况：
  - **C_MA**：存储-加载（st-ld）违反重新执行。
  - **C_TM**：TLB（翻译后备页表）缺失。
  - **C_FF**：存储-加载转发。
  - **C_DR**：数据缓存（dcache）需要重发。
  - **C_DM**：数据缓存缺失。
  - **C_WF**：路径预测失败。
  - **C_BC**：数据缓存路径冲突。
  - **C_RAR**：读取-读取（RAR）队列无法接收。
  - **C_RAW**：读取-写入（RAW）队列无法接收。
  - **C_NK**：存储-加载违反。
- **Blocking**：指示该 Load 指令因等待条件而被阻塞，不能被调度重发。阻塞的原因和解除阻塞的条件包括：
  - **C_MA**：存储指令的地址就绪。
  - **C_TM**：TLB 回填完毕，并发送 Hint 信号。
  - **C_FF**：存储指令的数据就绪。
  - **C_DM**：数据缓存回填完毕。
  - **C_RAR**：RAR 队列未满，且 Load 指令比 Load Queue 的写回项更老。
  - **C_RAW**：RAW 队列未满，且 Load 指令比 Store Queue 中所有地址准备好的项都更老。

LoadReplayQueue 通过 FreeList 管理队列的空闲状态。FreeList 的大小等于 LoadReplayQueue 的项数，分配宽度为3（Load Unit 的数量），释放宽度为 4。同时，Free List 可以反馈 Load Replay Queue 的空余项数量以及是否已满的信息。除了FreeList，LoadQueueReplay还包含两个子模块：AgeDetector 和 LqVAddrModule，其中 AgeDetector 用于寻找一系列load replay queue项中最早入队的一项。

例如昆明湖V1的Load宽度为2，则会将load replay queue分为两半，从偶数项和奇数项中分别挑选一项最老的进行重发。LqVAddrModule 用于保存load replay queue项数个虚拟地址，读口和写口的数量均为Load的宽度（LoadUnit的数量）。

## LoadQueueReplay 存储信息
| Field                 | Description |
|-----------------------|-------------|
| allocated             | 是否已经被分配，也代表是否该项是否有效。 |
| scheduled             | 是否已经被调度，代表该项已经被选出，已经或即将被发送至LoadUnit进行重发。 |
| uop                   | load指令执行包括的uop信息。 |
| vecReplay             | 向量load指令相关信息。 |
| vaddrModule           | Load指令的虚拟地址。 |
| cause                 | 某load replay queue项对应load指令重发的原因，包括：<br>- C_MA(位0): store-load预测违例<br>- C_TM(位1): tlb miss<br>- C_FF(位2): store-to-load-forwarding store数据为准备好，导致失败<br>- C_DR(位3): 出现DCache miss，但是无法分配MSHR<br>- C_DM(位4): 出现DCache miss<br>- C_WF(位5): 路预测器预测错误<br>- C_BC(位6): Bank冲突<br>- C_RAR(位7): LoadQueueRAR没有空间接受指令<br>- C_RAR(位8): LoadQueueRAW没有空间接受指令<br>- C_NK(位9): LoadUnit监测到store-to-load-forwarding违例<br>- C_MF(位10): LoadMisalignBuffer没用空间接受指令 |
| blocking              | Load指令正在被阻塞。 |
| strict                | 访存依赖预测器判断指令是否需要等待它之前的所有store指令执行完毕进入调度阶段。 |
| blockSqIdx            | 与load指令有相关性的store指令的StoreQueue Index。 |
| missMSHRId            | load指令的dcache miss请求接受ID。 |
| tlbHintId             | load指令的tlb miss请求接受ID。 |
| replacementUpdated    | DCache的替换算法是否已经更新。 |
| replayCarry           | DCache的路预测器预测信息。 |
| missDbUpdated         | ChiselDB中Miss相关情况更新。 |
| dataInLastBeatReg     | Load指令需要的数据在两笔回填请求的最后一笔。 |

# 功能简介

<mrs-functions>

## 模块功能说明

### 功能1：需要重发的指令请求入队

根据是否满足以下条件以及freelist是否可以分配的空闲槽位决定能否直接入队：

1. `enq_X.valid` 信号有效。
2. 即将入队的项不需要重定向。
3. 该项被标记为需要重发(`enq.bits.rep_info.need_rep`)。
4. 没有异常。在入队时，必须确保没有异常发生。如果当前指令处于异常状态，入队操作应被禁止，以防止无效指令的执行。

### 功能2：指令重发解锁

LoadQueueReplay 中的指令出队分三拍：

在重发过程中，根据重发的原因和当前条件解锁相应项。在不满足解锁条件时，将会被阻塞，无法参与重发仲裁。其中C_BC（Dcache 块冲突）、C_NK（oad_unit 在 S1、S2 阶段发生 store-load 违例）、C_DR（Dcache miss 且 MSHR 满）、C_WF（路径预测失败）**无需条件即可立即重发**。

其他重发原因和对应的解锁条件如下：

1. C_MA（store_load 预测违例）：已经被分配入队并且store准备好了相应的地址，具体如下：
   1. store unit 的地址信号有效，且 `sqIdx` 与被阻塞的 `Idx` 相同，store 地址未发生 TLB miss。
   2. 被阻塞的 `SeqIdx` 在 store_queue 发送的 `stAddrReadySqPtr` 之前。
   3. 非严格阻塞，且阻塞的 `SeqIdx` 在 `stAddrReadyVec` 的向量组内。
   4. store queue 为空，无未处理项。
2. C_TM（TLB Miss）：resp信号有效，并且输入的id号等于Tlb Hint的id号，或者replay_all信号有效。
3. C_FF（store_load 数据前递失败）：因为数据前递失败导致指令重发的释放条件有下面四条：
   1. store unit 的数据信号有效，且 `sqIdx` 与被阻塞的 `Idx` 相同。
   2. 被阻塞的 `SqIdx` 在 store_queue 发送的 `stDataReadySqPtr` 之前。
   3. 阻塞的 `SeqIdx` 在 `stDataReadyVec` 的向量组内。
   4. store queue 为空，无未处理项。
4. C_DM（Dcache Miss）：Dcache 的信号有效，且 `tl_d_channel.mshrid` 与阻塞的 `missMSHRId` 相同。
5. C_RAR（RAR queue 没有回应）：RAR 未满，或 `lqIdx` 在 `ldWbPtr` 之前。
6. C_RAW（RAW 没有回应）：RAW 未满，或 `lqIdx` 在 `stAddrReadySqPtr` 之前。

### 功能3：指令重发优先级
LoadQueueReplay有3种选择调度方式：

1. 根据入队年龄

    LoadQueueReplay使用3个年龄矩阵(每一个Bank对应一个年龄矩阵)，来记录入队的时间。年龄矩阵会从已经准备好可以重发的指令中，选择一个入队时间最长的指令调度重发。

2. 根据Load指令的年龄

    LoadQueuReplay可以根据LqPtr判断靠近最老的load指令重发，判断宽度为OldestSelectStride=4。

3. DCache数据相关的load指令优先调度

    - LoadQueueReply首先调度因L2 Hint调度的重发（当dcache miss后，需要继续查询下级缓存L2 Cache。在L2 Cache回填前的2或3拍，L2 Cache会提前给LoadQueueReplay唤醒信号，称为L2 Hint）当收到L2 Hint后，LoadQueueReplay可以更早地唤醒这条因dcache miss而阻塞的Load指令进行重发。

    - 如果不存在L2 Hint情况，会将其余Load Replay的原因分为高优先级和低优先级。高优先级包括因dcache缺失或st-ld forward导致的重发，而将其他原因归纳为低优先级。如果能够从LoadQueueReplay中找出一条满足重发条件的Load指令（有效、未被调度、且不被阻塞等待唤醒），则选择该Load指令重发，否则按照入队顺序，通过AgeDetector模块寻找一系列load replay queue项中最早入队的一项进行重发。

### 功能4：指令重发逻辑

1. Load_unit s3过来的请求根据enq.bits.isLoadReplay判断是否是已经从replay_queue出队的序列，如果是已经出队的序列，根据是否needReplay和有异常做下一步的判断，如果有异常或者不需要重发则释放这个槽位，并从agedetector里面把该项出队，如果需要重发则将这个项对应的scheduled位置为false来参与后续的出队仲裁竞争。

2. 从freelist中选出发给load unit的有效项，项数为load unit的宽度（即有几条load unit的流水线），根据优先级来进行出队。

3. 第0拍将数据传递给第1拍由s0_can_go控制，当s0_can_go为1时才能将0拍得到的数据发给第一拍，s0_can_go有效的条件是s0被重定向或者s1_can_go为1。

4. 第一拍从vaddr内部取出需要的虚拟地址，发给下一拍流水线。 ColdCouter的值在0到12之间，上一拍没有被阻塞并且整个过程没有发生重定向的时候，向load unit发送请求。

5. 发送给下一拍流水线的数据受s1_can_go控制，s1_can_go为1的条件是:

  - ColdCouter的值在0到12之间 且 上一拍完成操作(未被阻塞)或者不需要发送数据两者之一。

  - 发生数据的重定向。

6. 第二拍将收到第一拍的数据发送给对应的load unit,获取仲裁权限，完成重发指令的任务。

</mrs-functions>

## 接口说明

| name                    | I/O    | description                                                  |
| ----------------------- | ------ | ------------------------------------------------------------ |
| redirect                | input  | 后端重定向相关信息                                           |
| vecFeedback             | input  | 来自两条流水线的向量反馈信息                                 |
| enq                     | input  | 表示外部模块希望将 load 指令传递给当前模块，来自 load 指令流水线的 s3 级 |
| storeAddrIn             | input  | 在一个时钟周期内接收多条 store 指令的地址信息，用于判断指令存储的地址是否已经准备好                |
| storeDataIn             | input  | 在一个时钟周期内接收多条 store 指令的数据信息，用于判断指令存储的数据是否已准备好                |
| replay                  | output | 用于处理 load 指令的重发请求，每个元素对应一个重发接口       |
| tl_d_channel            | input  | 用于接收来自数据缓存（Dcache）的信息，在处理 load 指令时会使用该端口进行数据转发 |
| stAddrReadySqPtr        | input  | 指向当前准备好地址的 store 指令                              |
| stAddrReadyVec          | input  | 向量中对应 store 指令的地址是否已经准备好                    |
| stDataReadySqPtr        | input  | 指向当前准备好数据的 store 指令                              |
| stDataReadyVec          | input  | 向量中对应 store 指令的数据是否已经准备好                    |
| sqEmpty                 | input  | 当前 store 队列是否为空                                      |
| lqFull                  | output | 当前 load 队列是否已满                                       |
| ldWbPtr                 | input  | 指向当前写回的load指令                                       |
| rarFull                 | input  | rar 队列是否已满                                             |
| rawFull                 | input  | raw 队列是否已满                                             |
| l2_hint                 | input  | 当 dcache miss 后，需要继续查询下级缓存 L2 Cache。在 L2 Cache 回填前的 2 或 3 拍，L2 Cache 会提前给 LoadQueueReplay 唤醒信号，称为 L2 Hint |
| tlb_hint                | input  | 作用类似于 l2_hint，接收当前的 TLB 提示信息                  |
| tlbReplayDelayCycleCtrl | input  | 控制 TLB 重发的延迟周期                                      |