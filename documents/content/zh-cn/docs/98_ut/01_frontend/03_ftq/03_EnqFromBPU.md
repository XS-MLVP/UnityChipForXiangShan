---
title: FTQ接收BPU分支预测结果
linkTitle: FTQ接收BPU分支预测结果
weight: 12
---

# FTQ接收BPU分支预测结果

## 文档概述

BPU会将分支预测结果和meta数据发给FTQ。
- 从分支预测结果中，我们可以提取出分支预测块对应的取值目标，比如，一个不跨缓存行且所有指令均为RVC指令的分支预测块对应的取值目标，是从分支预测块起始地址开始的以2B为间隔的连续16条指令。
- meta信息则存储了各个预测器相关的预测信息，由于BPU预测有三个流水级，每个流水级都有相应的预测器，所以只有到s3阶段才有可能收集到所有预测器的预测信息，直到此时FTQ才接受到完整的meta，这些信息会在该分支预测块的全部指令被后端提交时交给BPU进行训练
- FTBEntry：严格来说，它其实也是meta的一部分，但是因为更新的时候ftb_entry需要在原来的基础上继续修改，为了不重新读一遍ftb，另外给它存储一个副本。

## 术语说明 
| 名称                           | 定义          |
| ---------------------------- | ----------- |
| BPU (Branch Prediction Unit) | 分支预测单元      |
| FTQ (Fetch Target Queue)     | 采集目标队列      |
| IFU (Instruction Fetch Unit) | 指令采集单元      |
| RAS (Return Address Stack)   | 返回地址堆       |
| FTQ Entry                    | FTQ队列中的单个表项 |

## 模块功能说明 。

### 1. 新的预测块进队条件
#### **1.1 成功接收数据**
##### 1.1.1 FTQ准备好接收信号
- FTQ准备好接收信号：
     当FTQ队列中元素小于FtqSize或者可以提交指令块（canCommit拉高，说明可以提交指令块，在后面的文档: FTQ向BPU发送更新信息中介绍怎么判断是否可以提交指令块）的时候，来自BPU的新的指令预测块可以进入FTQ队列，队列准备好接收新的预测块，fromBpu的resp接口ready信号拉高。
##### 1.1.2 BPU准备好要发送的信号
- BPU准备好要发送的信号：
     当BPU发往FTQ的接口vaid信号拉高，表示发送信号准备好

满足以上两个条件时,fromBpu的resp接口fire，表示接口数据被成功发送到FTQ中。
#### **1.2 允许BPU入队allowBpuIn**
- 重定向发生时，会回滚到之前的状态，新发送的BPU预测信息自然就不需要了。**允许BPU入队**时不能发生重定向
##### 1.2.1 后端重定向发生
1. 后端重定向发生：
	- 标志：接收后端写回信息的接口fromBackend的重定向接口redirect有效，则该周期不允许入队，如果没有发生真实提前重定向realAhdValid(参见FTQ接收后端重定向一文)，则下一个周期也不允许入队。
##### 1.2.2 IFU重定向发生
2. IFU重定向发生：
	- 标志：IFU重定向信息生成的两个周期，均不许入队（参见FTQ接收IFU重定向一文了解IFU重定向信息的生成）

只要避免上述两种重定向出现的情况，就可以允许BPU入队,即可以把发送到FTQ的数据，写入FTQ项
#### 1.3 以BPU预测结果重定向的方式入队
上述的BPU入队方式是一个全新的预测块进队，即BPU分支预测的s1阶段结果入队，此时未发生预测结果重定向。

当BPU发生预测结果重定向时，只要**允许BPU入队allowBpuIn**，也可以看作预测结果入队，不过这种入队是覆写队列中已有的FTQ项，没有写入新的指令块。
- BPU预测结果发生重定向的具体标志：fromBpu的resp接口的s2（s2阶段的预测信息）有效，且s2的hasRedirect拉高，表示在s2阶段发生了重定向，s3阶段重定向是一样的。

***综合两种形式的BPU入队，这里称之为广义BPU入队方便区分，记为bpu_in_fire，该信号拉高，表明发生广义BPU入队。***

### 2. 写入FTQ项

之前已经说明过了，FTQ项只是一个抽象的概念，FTQ有很多个子队列组成，它们的项共同构成一个FTQ项，所以，向FTQ中写入FTQ项，实际上就是就是把BPU的预测信息写到对应的FTQ子队列中。

FTQ主要获取以下信息作为bpu_in_resp
- bpu_in_resp：BPU交给FTQ的resp详见BPU文档，resp中含有s1,s2,s3三个阶段的指令预测信息，bpu_in_resp将获取其中某一阶段预测信息selectedResp作为其值。未发生重定向时，使用s1作为预测结果，s2或者s3发生重定向信息时，优先s3的预测信息作为selectedResp。某阶段发生重定向的标志与上文讲述的一样一样。
从selectedResp（bpu_in_resp）中，我们还可以获取以下目标信息帮助我们写入子队列：ftq_idx，帮助我们索引写入子队列的地址

#### 2.1 写入FTQ子队列：
##### 2.1.1 写入ftq_pc_mem
- ftq_pc_mem: 来自BPU的selectedResp预测信息被写入ftq_pc_mem, 该存储结构有ftqsize个表项，对应队列中的所有ftq表项，每个存储元素可以推出对应的ftq表项中每条指令的pc地址
	接收信号列表：
	- wen：接收bpu_in_fire作为写使能信号
	- waddr：接收selectedResp的ftq_idx
	- wdata：selectedResp的相应信号
##### 2.1.2 写入ftq_redirect_mem
- ftq_redirect_mem: 在BPU的s3（也就是最终阶段）接收信息，因为重定向信息只有在s3阶段才能得到。里面存储了RAS重定向相关的信息帮助BPU进行重定向。
	接收信号列表：
	- wen：从BPU（fromBpu）回应（resp）的lastStage有效信号
	- waddr：从BPU回应的lastStage的ftq_idx.value
	- wdata：从BPU回应的last_stage_spec_info
##### 2.1.3 写入ftq_meta_1r_sram
- ftq_meta_1r_sram：在 BPU的s3阶段接收信息，同样是因为对于一个指令预测块，只有在其s3阶段才能获取完整的mata信息，同样被接收的还有最后阶段ftqentry信息
	接收信号列表：
	- wen：从BPU（fromBpu）回应（resp）的lastStage有效信号
	- waddr：从BPU回应的lastStage的ftq_idx的value
	- wdata：
		- meta：从BPU回应的last_stage_meta
		- ftb_entry：从BPU回应的last_stage_ftb_entry
##### 2.1.4 写入ftb_entry_mem
- ftb_entry_mem：虽然ftq_meta_1r_sram中存储有最后阶段ftbentry，但此处出于更高效率读取专门把它存在ftb_entry_mem中。
	接收信号列表：
	- wen：从BPU（fromBpu）回应（resp）的lastStage有效信号
	- waddr：从BPU回应的lastStage的ftq_idx的value字段
	- wdata：从BPU回应的last_stage_ftb_entry
从中可以看到，FTQ虽然名字上听起来是一个队列，**实际上内部却是由数个队列组成**，他们共同构成了FTQ这个大队列
#### 2.2 写入状态队列
上述存储结构是FTQ中比较核心的存储结构，实际上，还有一些子队列用来存储一些状态信息，也同样都是存储ftqsize个（64）元素，需要被写入，写入时机是在发生bpu_in_fire的下一个周期，或者再下一个周期 。主要有以下：
##### 2.2.1 写入update_target
update_target：记录每个FTQ项的跳转目标，跳转目标有两种，一种是当该FTQ项对应的分支预测结果中指明的该分支预测块中执行跳转的分支指令将要跳转到的地址，另一种则是分支预测块中不发生跳转，跳转目标为分支预测块中指令顺序执行的下一条指令地址。
- 此外，与之配套的还有newest_entry_target，newest_entry_ptr用来指示bpu_in_resp推出的跳转目标地址，表示下一次预测时开始的目标地址，和它对应的bpu_in_resp指令预测块在FTQ中的位置。
	- 同时，有辅助信号newest_entry_target_modified和newest_entry_ptr_modified用来标识该这两个字段是否被修改。
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：bpu_in_resp.getTarget
##### 2.2.2 写入cfiIndex_vec
cfiIndex_vec：记录每个FTQ项的发生跳转的指令cfi（control flow instruction）指令在其分支预测块中的位置
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：bpu_in_resp推断出的跳转目标
##### 2.2.3 写入mispredict_vec
mispredict_vec：记录每个FTQ项的所有指令的预测结果是否有误，初始化为false
- 写入时机：相对于bpu_in_fire有效时延迟两个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：将该指令块的所有预测结果对应的值设置为false
##### 2.2.4 写入pred_stage
pred_stage：记录每个FTQ项的分支预测结果是来自于哪个阶段
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
##### 写入pred_s1_cycle（不需要测试）
pred_s1_cycle：记录每个FTQ项的分支预测结果对应的s1阶段的分支预测结果生成的时间（cycle数）
- 写入时机：相对于bpu_in_fire有效时延迟两个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
##### 2.2.5 写入commitStateQueueReg
commitStateQueueReg：记录每个FTQ项中对应的分支预测块中每条指令（一般是16条rvc指令，对应一个预测宽度）的提交状态，提交状态有c_empty ，c_toCommit ，c_committed ，c_flushed，依次用从小到大的枚举量表示，初始化为c_empty状态
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入数据：写入c_empty
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
##### 2.2.6 写入entry_fetch_status
entry_fetch_status：记录每个FTQ项的分支预测结果是否被送到ifu中，该状态由两个枚举量f_to_send ， f_sent来表示, 初始化为f_sent状态。
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入数据：写入f_to_send
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
##### 2.2.7 写入entry_hit_status
entry_hit_status：记录每个FTQ项拿到的分支预测结果是否是ftb entry hit的，即生成该分支预测结果的时候是否是从ftb中，读取到了对应的记录表项。初始化为not_hit状态。
- 写入时机：当来自BPU的全局分支预测信息中s2阶段的分支预测结果有效时，写入s2阶段分支预测结果中指名的hit状态
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：f_to_send

注：之所以延迟时钟周期写入，是为了缩短关键路径，以及帮助减少扇出

### **3 转发分支预测重定向**：
#### 3.1 转发给IFU
- s2以及s3阶段的预测重定向信息通过FTQ与Ifu的接口toIfu的flushFromBpu发送给IFU，当完整分支预测结果中的s2阶段分支预测结果发生预测结果重定向时，flushFromBpu.s2.valid拉高，flushFromBpu.s2.bits接收s2阶段分支预测结果中指明的该分支预测结果在FTQ中的位置ftq_idx。
#### 3.2 **转发给预取**
- 该重定向信号同样会通过toPrefetch.flushFromBpu接口以相同的方式传递给Prefetch
s3阶段向IFU以及Prefetch的重定向传递与s2阶段的重定向信号传递一样。该阶段的重定向信号传递会覆盖可能的s2阶段重定向信号传递结果
### 4 修正FTQ指针
此外，分支预测结果重定向也会影响ifuPtr与pfPtr两个指针信号的写入信号。
#### 4.1 正常修改
- 正常情况下，allowToIfu（条件和allowToBpu一样），同时BPU向Ifu发送FTQ项的io接口toIfu.req发生fire的时候，ifuPtr寄存器中写入ifuPtr+1。同样发生修改的还有pfPtr，当allowToIfu，同时BPU向Prefetch发送FTQ项的io接口totoPrefetch.req发生fire的时候。
#### 4.2 发生重定向时修改
- 而如果是发生重定向的时候，比如s2阶段预测结果发生重定向，此时，若ifuPtr不在s2阶段预测结果中指明的ftq_idx之前，ifuPtr写入该ftq_idx，pfPtr_write同样如此

**bpuptr**：
由FTQ交给BPU用于指示新的指令预测块应该放到FTQ队列中的位置，上述存储结构，ftq_pc_mem，ftq_redirect_mem，ftq_meta_1r_sram，ftb_entry_mem基本上也是通过与该指针相关的信号得知信息应该存储的addr（bpuptr交给BPU，BPU基于此获知每个阶段预测结果的ftq_idx）。

bpuptr寄存器的输出值直接连到FTQ发往BPU的接口toBpu的enq_ptr字段中，当然，再次之前，bpuptr的值会根据实际情况修改。

在enq from bpu的过程中，正常情况下，发生enq的时候，也就是新的预测块进队时，bpuptr+1，BPU将要向FTQ中写入的位置前进一位

但是，如果发生重定向的时候，比如，如果s2阶段预测结果发生重定向，bpuptr被更新为s2阶段分支预测结果的ftq_idx+1，表示BPU将要向FTQ中写入的位置为s2阶段预测结果在FTQ中位置的后一位，因为此时新的全局预测结果会基于s2的预测结果展开下一轮预测（即以s2分支预测块的下一块展开预测，自然会被写入），该结果会覆盖enq_fire发生时的结果，此外s3阶段的分支预测重定向时，会覆盖可能的s2阶段重定向修改的bpuptr

其他的ftq指针也是类似的，用于指示写入FTQ的地址
## 接口说明 

FTQ接收BPU分支预测结果工程中涉及到的IO接口如下，在FTQ顶层IO一文中有详细说明

| 接口          | 作用                           |
| ----------- | ---------------------------- |
| fromBackend | 根据是否有重定向确认是否允许BPU预测结果入队      |
| fromBPU     | 接收BPU预测结果                    |
| toIfu       | 发送更新的IFU指针，转发BPU预测结果重定向      |
| toPrefetch  | 发送更新的Prefetch指针，转发BPU预测结果重定向 |
| toBpu       | 发送更新的BPU指针                   |

## 测试点总表

| 序号      | 功能名称                  | 测试点名称             | 描述                                                                          |
| ------- | --------------------- | ----------------- | --------------------------------------------------------------------------- |
| 1\.1\.1 | BPU_IN_RECEIVE        | FTQ_READY         | 当FTQ队列中元素小于FtqSize或者可以提交指令块的时候，队列准备好接收新的预测块                                 |
| 1\.1\.2 | BPU_IN_RECEIVE        | BPU_VALID         | BPU准备好要发送的信号                                                                |
| 1\.2\.1 | BPU_IN_ALLOW          | BACKEND           | 接收后端写回信息的接口fromBackend的重定向接口redirect有效，则该周期不允许入队，如果没有发生真实提前重定向，则下一个周期也不允许入队 |
| 1\.2\.2 | BPU_IN_ALLOW          | IFU               | IFU重定向信息生成的两个周期，均不许入队                                                       |
| 1\.3\.1 | BPU_IN_BY_REDIRECT    | REDIRECT          | 当BPU发生预测结果重定向时，只要**允许BPU入队allowBpuIn**，也可以看作预测结果入队                          |
| 2\.1\.1 | WRITE_FTQ_SUBQUEUE    | FTQ_PC            | 根据BPU预测结果写入ftq_pc_mem                                                       |
| 2\.1\.2 | WRITE_FTQ_SUBQUEUE    | FTQ_REDIRECT      | 根据BPU预测结果写入ftq_redirect_mem                                                 |
| 2\.1\.3 | WRITE_FTQ_SUBQUEUE    | FTQ_MATA          | 根据BPU预测结果写入ftq_meta_1r_sram                                                 |
| 2\.1\.4 | WRITE_FTQ_SUBQUEUE    | FTQ_ENTRY         | 根据BPU预测结果写入ftb_entry_mem                                                    |
| 2\.2\.1 | WRITE_FTQ_STATEQUEUE  | UPDATED_TARGET    | 根据BPU预测结果写入update_target                                                    |
| 2\.2\.2 | WRITE_FTQ_STATEQUEUE  | CFIINDEX          | 根据BPU预测结果写入cfiIndex_vec                                                     |
| 2\.2\.3 | WRITE_FTQ_STATEQUEUE  | MISPREDICT        | 根据BPU预测结果写入mispredict_vec                                                   |
| 2\.2\.4 | WRITE_FTQ_STATEQUEUE  | PRED_STAGE        | 根据BPU预测结果写入pred_stage                                                       |
| 2\.2\.5 | WRITE_FTQ_STATEQUEUE  | COMMITSTATE       | 根据BPU预测结果写入commitStateQueueReg                                              |
| 2\.2\.6 | WRITE_FTQ_STATEQUEUE  | ENTRY_FETCH_STATU | 根据BPU预测结果写入entry_fetch_status                                               |
| 2\.2\.7 | WRITE_FTQ_STATEQUEUE  | ENTRY_HIT_STATU   | 根据BPU预测结果写入entry_hit_status                                                 |
| 3\.1    | TRANSFER_BPU_REDIRECT | IFU               | 转发分支预测重定向给IFU                                                               |
| 3\.2    | TRANSFER_BPU_REDIRECT | PREFETCH          | 转发分支预测重定向给PREFETCH                                                          |
| 4\.1    | UPDATE_FTQ_PTR        | NORMAL            | 正常情况下修改FTQ指针                                                                |
| 4\.2    | UPDATE_FTQ_PTR        | REDIRECT          | 发生重定向时修改FTQ指针                                                               |
