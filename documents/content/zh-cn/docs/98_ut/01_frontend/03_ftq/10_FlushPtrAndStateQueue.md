---
title: 冲刷指针和状态队列
linkTitle: 10_冲刷指针和状态队列
weight: 12
---

## 文档概述
之前讲了，后端和IFU重定向写回会修改一些状态队列。此外，FtqPtr也是一种比较重要的维护信息。由后端或者IFU引起的重定向，需要恢复各种类型用来索引FTQ项的FtqPtr。而当重定向是由后端发起的时候，还要修改提交状态队列，说明指令已经被执行。
## 术语说明 

| 名称    | 定义                                   |
| ----- | ------------------------------------ |
| FTQ指针 | 用来索引FTQ项，有不同类型的FTQ指针，比如bpuPtr，ifuPtr |
| flush | 冲刷，发生时需要重置FTQ指针，以及重置其他状态             |
| 融合指令  | 一条指令可以和其他指令融合，形成融合指令                 |

## 模块功能说明
### 1. 冲刷FTQ指针及提交状态队列
#### 流程
后端和IFU的重定向信号都会冲刷指针，更具体的来说：
#### 1.1 冲刷条件
- 后端写回接口fromBackend有效，或者IFU重定向有效：（当预译码写回pdWb有效，且pdWb的missOffset字段有效表明存在预测错误的指令，同时后端冲刷信号backendFlush无效）。（参考：从IFU重定向的第一个周期，重定向valid值有效条件）
#### 1.2 冲刷指针
第一个周期：
- 冲刷指针：确认后端和IFU的重定向信号可能冲刷指针时，从两个重定向来源的redirect接口读出重定向信息，包括ftqIdx，ftqOffset，重定向等级RedirectLevel。有两个来源时，优先后端的重定向信息。
	冲刷指针列表：
	- bpuPtr：ftqIdx+1
	- ifuPtr：ftqIdx+1
	- ifuWbPtr：ftqIdx+1
	- pfPtr：ftqIdx+1
	*注：只是在当前周期向指针寄存器写入更新信息，实际生效是在下一个周期。*
	这样一来，所有类型指针当前指向的都是发生重定向的指令块的下一项了，我们从这一项开始重新进行分支预测，预译码，等等。	
#### 1.3 冲刷提交状态队列
第二个周期：
 如果上一个周期的重定向来源是后端，FTQ会进一步更改提交状态队列
 - 提交状态队列中，对于重定向的指令块（通过ftqIdx索引），位于ftqOffset后面的指令的状态被设置为c_empty
 - 对于正好处于ftqOffset的指令，判断RedirectLevel，低表示在本位置后flush，高表示在本位置flush，所以level为高时，对于的指令提交状态被设置为flush。

### 2 转发到顶层IO
实际上，在发生重定向的时候，还涉及一些将重定向信息通过FTQ顶层IO接口转发给其他模块的操作，比如ICache需要flush信号取进行冲刷，IFU也需要后端的重定向信号对它进行重定向，具体来说：
在**流程**的第一个周期：
#### 2.1 flush转发到icacheFlush
- flush信号顶层IO转发（icacheFlush）：
	- 确认后端和IFU的重定向信号可能冲刷指针时，拉高FTQ顶层IO接口中的icacheFlush信号，把重定向产生的flush信号转发给ICache
#### 2.2 重定向信号转发到IFU
- 重定向信号顶层IO转发（toIFU）：
	- redirect：
		- bits：接收来自后端的重定向信号
		- valid：后端的重定向信号有效时有效，保持有效，直到下个周期依然有效
### 3 重排序缓冲区提交
其实，除了后端重定向会更新提交状态队列，最直接的更新提交状态队列的方式是通过FTQ顶层IO中frombackend里提供的提交信息，rob_commits告知我们哪些指令需要被提交。

rob_commits的valid字段有效，可以根据其中信息对指令进行提交，修改状态队列。对于被执行的指令，是如何提交的，如何对应地修改提交状态队列，有两种情况：
#### 3.1 提交普通指令
- 对于普通指令，根据rob_commits的ftqIdx和ftqOffset索引提交状态队列中的某条指令，将对应的提交状态设置为c_commited	
### 3.2 提交融合指令
- 对于融合指令，根据提交类型commitType对被索引的指令和另一与之融合的指令进行提交，将对应的提交状态设置为c_commited
	1. commitType = 4：同时把被索引指令的下一条指令设为c_commited
	2. commitType = 5：同时把被索引指令的之后的第二条指令设为c_commited
	3. commitType = 6：同时把被指令块的下一个指令块的第0条指令设为c_commited
	4. commitType = 7：同时把被指令块的下一个指令块的第1条指令设为c_commited
## 接口说明 

| 顶层IO        | 作用                |
| ----------- | ----------------- |
| fromBackend | 接收后端重定向和指令提交      |
| fromIfu     | 接收IFU重定向          |
| icacheFlush | 将flush信号转发到icache |
| toIFU       | 将后端重定向转发到IFU      |

## 测试点总表

| 序号   | 功能名称                         | 测试点名称              | 描述                                                                        |
| ---- | ---------------------------- | ------------------ | ------------------------------------------------------------------------- |
| 1.1  | FLUSH_FTQPTR_AND_COMMITSTATE | FLUSH_COND         | 后端写回接口fromBackend有效，或者IFU重定向有效时，进行冲刷                                      |
| 1\.2 | FLUSH_FTQPTR_AND_COMMITSTATE | FLUSH_FTQ_PTR      | 优先采用后端重定向信息冲刷FTQ指针                                                        |
| 1\.3 | FLUSH_FTQPTR_AND_COMMITSTATE | FLUSH_COMMIT_STATE | 发生后端重定向时，进一步修改提交状态队列                                                      |
| 2\.1 | TRANSFER_TO_TOP              | FLUSH              | 后端和IFU的重定向信号可能冲刷指针，拉高FTQ顶层IO接口中的icacheFlush信号                             |
| 2\.2 | TRANSFER_TO_TOP              | IFU                | 将重定向信号转发到IFU                                                              |
| 3\.1 | COMMIT_BY_ROB                | NORMAL             | 对于普通指令，根据rob_commits的ftqIdx和ftqOffset索引提交状态队列中的某条指令，将对应的提交状态设置为c_commited |
| 3\.2 | COMMIT_BY_ROB                | FUSION             | 对于融合指令，根据提交类型commitType对被索引的指令和另一与之融合的指令进行提交，将对应的提交状态设置为c_commited        |

