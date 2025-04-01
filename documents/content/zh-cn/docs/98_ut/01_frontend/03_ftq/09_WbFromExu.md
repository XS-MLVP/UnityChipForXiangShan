---
title: 执行单元修改FTQ状态队列
linkTitle: 09_执行单元修改FTQ状态队列
weight: 12
---

## 文档概述
后端的写回信息，包括重定向信息和更新信息，实际上都是执行之后，由实际执行单元根据结果发回的
## 术语说明 

| 名称            | 定义                                            |
| ------------- | --------------------------------------------- |
| cfiIndex_vec  | 控制流指令索引队列，记录每个指令块中控制流指令的索引                    |
| update_target | 更新目标队列，记录每个指令块的跳转目标                           |
| FTQ最新项        | BPU新的写入，重定向等等都会对最新FTQ项进行新的安排，表明我们当前关注的最新FTQ项。 |

## 模块功能说明 

### 1. 由后端的写回信号修改FTQ状态
#### 1.1 修改FTQ状态队列
从后端写回FTQ接口fromBackend中的redirect接口中，我们可以读出valid，ftqPtr，ftqOffset（后端实际执行时确认的控制流指令的偏移），taken，mispred字段，依靠它们来判断，如何修改FTQ的状态队列和相关的变量

**后端执行单元写回时被修改的队列**：
#### 1.1.1 修改cfiIndex_vec
- cfiIndex_vec：
	修改方式：执行写回修改队列中ftqPtr那一项
	- valid：fromBackend中的redirect接口中，valid有效，taken有效，且ftqOffset小于或者等于cfiIndex_vec中ftqPtr那一项指定的偏移：这说明重定向发生，实际执行结果判断ftqPtr索引的指令块确实会发生跳转，且实际执行跳转的指令在被预测为发生跳转的指令之前或等于它。所以这时指令块是会发生跳转的，控制流索引队列的ftqPtr项valid
	- bits：fromBackend中的redirect接口中，valid有效，taken有效，且ftqOffset小于cfiIndex_vec中ftqPtr那一项指定的偏移，偏移量被更新为更小值ftqOffset。
#### 1.1.2 修改update_target
- update_target：
	- ftqPtr索引项的跳转目标修改为fromBackend的redirect接口中的cifUpdate中指定的target
#### 1.1.3 修改mispredict_vec
- mispredict_vec：
	- 如果该重定向指令是来自后端的重定向指令， ftqPtr索引项的ftqOffset偏移指令被设置为fromBackend的redirect接口中的cifUpdate中指定的isMisPred
#### 1.2 修改FTQ最新项
- newest_entry_target：
	- 被修改为重定向接口中cfiUpdate指定的target
	- 辅助信号newest_entry_target_modified被指定为true
- newest_entry_ptr：
	- 修改为重定向接口指定的ftqIdx
	- 辅助信号newest_entry_ptr_modified被指定为true
### 2. 由IFU的写回信号修改FTQ状态
IFU既然也能和后端一样生成重定向信息，那么他也能在产生重定向信息的时候修改这些状态队列和FTQ最新项，区别：
- 但是，由于IFU没有真的执行，所以它的预译码结果并不能作为决定指令块是不是真的被错误预测了，所以它不能修改mispredict_vec的状态
- 其次，后端重定向优先级永远高于IFU重定向，两者同时发生时只采用后端重定向。

所以这个部分也有以下测试点：
#### 2.1.1 修改cfiIndex_vec
#### 2.1.2 修改update_target
#### 2.2 修改FTQ最新项

## 常量说明

| 常量名 | 常量值 | 解释    |
| --- | --- | ----- |
| 常量1 | 64  | 常量1解释 |
| 常量2 | 8   | 常量2解释 |
| 常量3 | 16  | 常量3解释 |

## 接口说明 

| 顶层IO        | 子接口      |     |
| ----------- | -------- | --- |
| fromBackend | redirect |     |

## 测试点总表

实际使用下面的表格时，请用有意义的英文大写的功能名称和测试点名称替换下面表格中的名称

| 序号      | 功能名称                           | 测试点名称                          | 描述                        |
| ------- | ------------------------------ | ------------------------------ | ------------------------- |
| 1\.1\.1 | BACKEDN_REDIRECT_UPDATE_STATE  | UPDATE_CFIINDEXVEC             | 后端重定向修改cfiinedex状态队列      |
| 1\.1\.2 | BACKEDN_REDIRECT_UPDATE_STATE  | UPDATE_UPDATE_TARGET           | 后端重定向修改update_target状态队列  |
| 1\.1\.3 | BACKEDN_REDIRECT_UPDATE_STATE  | UPDATE_MISPREDICTVEC           | 后端重定向修改mispredict状态队列     |
| 1\.2    | BACKEDN_REDIRECT_UPDATE_NEWEST | BACKEDN_REDIRECT_UPDATE_NEWEST | 后端重定向修改FTQ最新项             |
| 2\.1\.1 | IFU_REDIRECT_UPDATE_STATE      | UPDATE_CFIINDEXVEC             | IFU重定向修改cfiinedex状态队列     |
| 2\.1\.2 | IFU_REDIRECT_UPDATE_STATE      | UPDATE_UPDATE_TARGET           | IFU重定向修改update_target状态队列 |
| 2\.2    | IFU_REDIRECT_UPDATE_NEWEST     | IFU_REDIRECT_UPDATE_NEWEST     | IFU重定向修改FTQ最新项            |

