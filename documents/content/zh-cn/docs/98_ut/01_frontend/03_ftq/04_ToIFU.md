---
title: FTQ向IFU发送取指目标
linkTitle: 04_FTQ向IFU发送取指目标
weight: 12
---

## 文档概述
IFU需要取FTQ中的项进行取指令操作，同时也会简单地对指令进行解析，并写回错误的指令
FTQ发送给IFU的信号同时也需发送给ICache一份，ICache是指令缓存，帮助快速读取指令。

## 术语说明 

- ifuPtr：该寄存器信号指示了当前FTQ中需要读取的项的指针。直接发送给io.toIfu.req接口的ftqIdx。
- entry_is_to_send：entry_fetch_status存储每个FTQ项的发送状态，初始化并默认为当前ifuptr指向的项对应的发送状态，后续可能因为旁路逻辑等改变
- entry_ftq_offset: 从cfiIndex_vec中初始化并默认为当前ifuptr指向项的跳转指令在预测块中的偏移，后续可能因为旁路逻辑等改变
- entry_next：本次取指结束后下一次取值的开始地址
- pc_mem_ifu_ptr_rdata：获取ifuptr指向FTQ项的取指信息（从ftq_pc_mem的读取接口ifuPtr_rdata中获取）
- pc_mem_ifu_plus1_rdata：获取ifuptr+1指向FTQ项的pc相关信息（从ftq_pc_mem的读取接口ifuPtrPlus1_rdata中）
- copied_ifu_plus1_to_send：多个相同的复制信号，entry_fetch_status中指向ifuPtrPlus1的项是f_to_send状态或者上一周期bpu_in_fire,同时旁路bpu指针bpu_in_bypass_ptr等于ifuptr+1时，信号copied_ifu_plus1_to_send在一周期后拉高
- copied_ifu_ptr_to_send：同理，只是把ifuptr+1改成了ifuptr

## 模块功能说明 
### 1. 获取取指目标信息
获取取指目标有两个来源，一个是BPU写入信息时，直接将取指目标旁路出来，一种则是从存储取指目标的队列ftq_pc_mem中读取。使用前一种方式的前提，是刚好ifuPtr指向的读取项刚好就是旁路指针信号bpu_in_resp_ptr（BPU入队时写入项的ftqIdx）
- 旁路逻辑：pc信号在被写入存储子队列时就被旁路一份，写入信号ftq_pc_mem.io.wdata在bpu_in_fire信号拉高时被旁路到旁路信号寄存器bpu_in_bypass_buf中。同时被旁路的还有指针信号bpu_in_resp_ptr，在同样的条件下被旁路到寄存器bpu_in_bypass_ptr中
- 读取ftq_pc_mem: 存储pc相关的取指目标，该存储队列有多个读接口，对所有ftqptr的写入信号（比如ifuPtr_write, ifuPtrPlus1_write等）被直接连接到存储队列的读取接口，这样，在ftqPtr寄存器正式被更新时，就可以同时直接从对应的读取接口中返回对应指针的读取结果，比如ftq_pc_mem.io.ifuPtr_rdata
#### 1.1 准备发往ICache的取指目标
有以下三种情况，分别对应**测试点1.1.1，1.1.2，1.1.3**
1. 旁路生效，即旁路bpu指针等于ifuptr，且上一周期bpu输入有效结果（last_cycle_bpu_in表示上一周期bpu_in_fire）有效（也就相当于该旁路指针是有效的），此时，直接向toICache接口输入旁路pc信息bpu_in_bypass_buf
2. 不满足情况1，但是上一周期发生ifu_fire（即FTQ发往IFU的接口发生fire），成功传输信号，此toICache中被写入pc存储子队列ftq_pc_mem中ifuptr+1对应项的结果，这是因为此时发生了ifu_fire，新的ifuptr还未来得及更新（即加1），所以直接从后一项中获取新的发送数据
3. 前两种情况都不满足，此时toICache接口中被写入pc存储队列中ifuptr对应项的结果
#### 1.2 提前一周期准备发往Prefetch的取指目标
有以下三种情况，分别对应**测试点1.2.1，1.2.2，1.2.3**
同样有三种情况：
1. bpu有信号写入（bpu_in_fire），同时bpu_in_resp_ptr等于pfptr的写入信号pfptr_write, （此时pfptr_write还没有正式被写入pfptr中），读取bpu向pc存储队列的写入信号wdata，下一周期写入ToPrefetch
     *xxxptr_write：是相应FTQptr寄存器的write信号，连接到寄存器的写端口，寄存器在时钟上升沿成功写入write信号*
2. 不满足情况1，且由bpu到prefetch的接口发生fire，即bpu向预取单元成功发送信号，pc存储单元的pfPtrPlus1_rdata下一周期写入ToPrefetch接口，选择指针加1对应项的原因与toICache类似。
3. 不满足以上两种情况：pc存储单元的pfPtr_rdata在下一周期被写入ToPrefetch接口
#### 1.3 设置下一个发送的指令块的起始地址
有以下三种情况，分别对应**测试点1.3.1，1.3.2，1.3.3**

**target（entry_next_addr）旁路逻辑：**
有三种情况：
1. 上一周期bpu写入信号，且旁路指针等于ifuptr：
	- toIfu：写入旁路pc信息bpu_in_bypass_buf
	- entry_is_to_send ：拉高
	- entry_next_addr ：bpu预测结果中跳转地址last_cycle_bpu_target
	- entry_ftq_offset ：bpu预测结果中跳转指令在预测块中的偏移last_cycle_cfiIndex
2. 不满足情况1，bpu到ifu的接口发生fire，信号成功写入 
	- toIfu：写入pc存储队列的读出信号ifuPtrPlus1_rdata，这同样是因为ifuptr还没来得及更改，所以直接使用ifuptr+1对应项的rdata
	- entry_is_to_send ：发送状态队列中ifuPtrPlus1对应项为f_to_send或者在上一周期bpu有写入时旁路bpu指针等于ifuptr加1，entry_is_to_send拉高。
	- entry_next_addr ：
		-  如果上一周期bpu有写入且bpu旁路指针等于ifuptr+1，写入bpu旁路pc信号的startAddr字段，而这个项的pc信息还没有写入，正在pc旁路信号中，这是因为ifuptr+1对应下一个指令预测块，它的起始地址实际上就是ifuptr对应指令的预测块的跳转目标。
		- 如果不满足该条件，
			1. ifuptr等于newest_entry_ptr: 使用newest_entry_target作为entry_next_addr，newest_entry_ptr，newest_entry_target这几个内部信号，表明我们当前队列中最新的有效的FTQ项。如之前所说，BPU新的写入，重定向等等都会对最新FTQ项进行新的安排，在相应的文档中，对其生成方式做具体的描述。
			2. 不满足条件1：使用pc存储队列的ifuPtrPlus2_rdata.startAddr
3. 不满足情况1，2：
- toIfu：写入pc存储队列的读出信号ifuPtr_rdata
- entry_is_to_send ：发送状态队列中ifuPtr对应项为f_to_send或者在上一周期bpu有写入时旁路bpu指针等于ifuptr
- entry_next_addr ：
- 如果上一周期bpu有写入且bpu旁路指针等于ifuptr+1，写入bpu旁路pc信号的startAddr字段。
-  如果不满足该条件，
	         1. ifuptr等于newest_entry_ptr: 使用newest_entry_target作为entry_next_addr。
	         2. 不满足上面的条件1：使用pc存储队列的ifuPtrPlus1_rdata.startAddr，为什么条件2和条件3，一个使用ifuPtrPlus2_rdata.startAddr作为entry_next_addr ，一个使用ifuPtrPlus1_rdata.startAddr作为，这也是出于时序的考虑：
因为要获得实际上的ifuptr+1对应项的start值作为结果，而因为第一处那里因为ifuptr还没来得及更新（加1）同步到当前实际的ifuptr，所以要加2来达到实际上的ifuptr+1对应的值，而第二处的ifuptr已经更新了，所以只用加1就行了。
### 2. 发送取指信息
#### 2.1 发送取指目标
##### 2.1.1 发送给IFU
**toIfu接口的req接口：**
FTQ通过该接口向IFU发送取指信号：
- valid：要发送的FTQ项处于将发送状态entry_is_to_send且ifuptr不等于bpuptr
- nextStartAddr：递交最终的entry_next_addr
- ftqOffset：递交最终的entry_ftq_offset
- toIfu：递交pc信息
##### 2.1.2 发送给ICache
**toICache的req接口：**
FTQ通过该接口向ICache发送取指信号：
- valid：FTQ项处于将发送状态entry_is_to_send且ifuptr不等于bpuptr
- readValid：ICache的有多个read接口，readVlid是一个向量，表示这几个read接口是否有效，readVlid中的每个元素的写入值与valid一样
- pcMemRead：同样是一个向量，对应readVlid向量的ICache的多个pc信号read接口，从toIfu接口中将pc信息结果写入向量中各接口，接口的ftqIdx字段被写入ifuPtr
- backendException：后端出现异常，同时后端pc错误指针等于ifuPtr
#### 2.1.3 发送给Prefetch
**toPrefetch的req接口：**
- valid：传给预取模块的项的状体toPrefetchEntryToSend为1，（toPrefetchEntryToSend会玩一个周期存储nextCycleToPrefetchEntryToSend的值），且pfptr不等于bpuptr，
- toPrefetch：递交pc
- ftqIdx字段被设置为pfptr寄存器的值
- backendException：在后端pc错误指针等于pfptr的时候，传入后端异常信号，否则传入无异常信号
#### 2.2 错误命中
**错误命中falsehit：**
当发往Ifu的pc接口toIfu中发生fallThruError（预测块的fall through地址小于预测的起始地址时），且hit状态队列entry_hit_status中ifuPtr对应项显示命中的话，进行如下判断：

当发往ifu的接口toIfu的req接口发生fire，且bpu的预测结果不发生满足以下条件的重定向: s2或者s3的重定向的预测块对应的FTQ项索引号ftq_idx等于ifuptr, 此时，hit状态队列中ifuptr对应项被设置为false_hit。
#### 2.3 BPU冲刷
**bpu向ifu的req请求的flush：**
发往ifu的flushfrombpu(来自bpu的冲刷)接口中，记录有s2，s3阶段的指针，如果其中一条指针不大于发往ifu的req接口的ftqIdx的时候，表示应该被冲刷掉req信号，即冲刷掉新的发送给FTQ的预测信息。
#### 2.4 更新发送状态
**成功发送：**
发往ifu的req接口发生fire，且req不被来自bpu的flush给冲刷掉时：
entry_fetch_status状态队列中ifuptr对应项的发送状态置为f_sent。表示该ftq项被成功发送 了
## 接口说明 

| 顶层IO       | 子接口          | 作用             |
| ---------- | ------------ | -------------- |
| toIFU      | req          | 发送取指目标         |
| toIFU      | flushfrombpu | 冲刷掉发送给IFU的取指目标 |
| toICache   | req          | 发送取指目标         |
| toPrefetch | req          | 发送取指目标         |

## 测试点总表 

| 序号      | 功能名称                | 测试点名称             | 描述                                                                                          |
| ------- | ------------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| 1\.1\.1 | GET_PC_FOR_ICACHE   | COND1             | 旁路生效，即旁路bpu指针等于ifuptr，且上一周期bpu输入有效结果有效，直接向toICache接口输入旁路pc信息bpu_in_bypass_buf               |
| 1\.1\.2 | GET_PC_FOR_ICACHE   | COND2             | 不满足情况1，但是上一周期发生ifu_fire，成功传输信号，此时toICache中被写入pc存储子队列ftq_pc_mem中ifuptr+1对应项的结果               |
| 1\.1\.3 | GET_PC_FOR_ICACHE   | COND3             | 前两种情况都不满足，此时toICache中被写入pc存储队列中ifuptr对应项的结果                                                 |
| 1\.2\.1 | GET_PC_FOR_PREFETCH | COND1             | bpu有信号写入，同时bpu_in_resp_ptr等于pfptr的写入信号pfptr_write, 读取bpu向pc存储队列的写入信号wdata，下一周期写入ToPrefetch  |
| 1\.2\.2 | GET_PC_FOR_PREFETCH | COND2             | 不满足情况1，且由bpu到prefetch的接口发生fire，即bpu向预取单元成功发送信号，pc存储单元的pfPtrPlus1_rdata下一周期写入ToPrefetch接口    |
| 1\.2\.3 | GET_PC_FOR_PREFETCH | COND3             | 不满足以上两种情况：pc存储单元的pfPtr_rdata在下一周期被写入ToPrefetch接口                                            |
| 1\.3\.1 | SET_NEXT_ADDR       | COND1             | 上一周期bpu写入信号，且旁路指针等于ifuptr时设置下一个发送的指令块的起始地址                                                  |
| 1\.3\.2 | SET_NEXT_ADDR       | COND2             | 不满足情况1，bpu到ifu的接口发生fire时设置下一个发送的指令块的起始地址                                                    |
| 1\.3\.3 | SET_NEXT_ADDR       | COND3             | 不满足情况1，2时设置下一个发送的指令块的起始地址                                                                   |
| 2\.1\.1 | SEND_PC             | IFU               | 向IFU发送取指目标                                                                                  |
| 2\.1\.2 | SEND_PC             | ICACHE            | 向ICache发送取指目标                                                                               |
| 2\.1\.3 | SEND_PC             | PREFETCH          | 向Prefetch发送取指目标                                                                             |
| 2\.2    | FALSE_HIT           | FALSE_HIT         | 当发往Ifu的pc接口toIfu中发生fallThruError，且FTB项命中时判断是否是错误命中                                          |
| 2\.3    | FLUSH_FROM_BPU      | FLUSH_FROM_BPU    | 发往ifu的flushfrombpu(来自bpu的冲刷)接口中的s2，s3阶段的指针其中一条指针不大于发往ifu的req接口的ftqIdx的时候，应该冲刷掉新的发送给FTQ的预测信息 |
| 2\.4    | UPDATE_SEND_STATU   | UPDATE_SEND_STATU | 发往ifu的req接口发生fire，且req不被来自bpu的flush给冲刷掉时：<br>entry_fetch_status状态队列中ifuptr对应项的发送状态置为f_sent  |
