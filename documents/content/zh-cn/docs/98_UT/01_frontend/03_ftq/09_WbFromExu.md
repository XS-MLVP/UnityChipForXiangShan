---
title: 从执行单元写回
linkTitle: 从执行单元写回
weight: 12
---

# 简介
后端的写回信息，包括重定向信息和更新信息，实际上都是执行之后，由实际执行单元根据结果发回的
# 流程
从后端写回FTQ接口fromBackend中的redirect接口中，我们可以读出valid，ftqPtr，ftqOffset（后端实际执行时确认的控制流指令的偏移），taken，mispred字段，依靠它们来判断，如何修改FTQ的状态队列和相关的变量

**执行写回时被修改的队列**：
- cfiIndex_vec：
	修改方式：执行写回修改队列中ftqPtr那一项
	- valid：fromBackend中的redirect接口中，valid有效，taken有效，且ftqOffset小于或者等于cfiIndex_vec中ftqPtr那一项指定的偏移：这说明重定向发生，实际执行结果判断ftqPtr索引的指令块确实会发生跳转，且实际执行跳转的指令在被预测为发生跳转的指令之前或等于它。所以这时指令块是会发生跳转的，控制流索引队列的ftqPtr项valid
	- bits：fromBackend中的redirect接口中，valid有效，taken有效，且ftqOffset小于cfiIndex_vec中ftqPtr那一项指定的偏移，偏移量被更新为更小值ftqOffset。
- update_target：
	- ftqPtr索引项的跳转目标修改为fromBackend的redirect接口中的cifUpdate中指定的target
- mispredict_vec：
	- 如果该重定向指令是来自后端的重定向指令， ftqPtr索引项的ftqOffset偏移指令被设置为fromBackend的redirect接口中的cifUpdate中指定的isMisPred

**其他信号**：
- newest_entry_target：
	- 被修改为重定向接口中cfiUpdate指定的target
	- 辅助信号newest_entry_target_modified被指定为true
- newest_entry_ptr：
	- 修改为重定向接口指定的ftqIdx
	- 辅助信号newest_entry_ptr_modified被指定为true

## IFU执行写回
IFU既然也能和后端一样生成重定向信息，那么他也能在产生重定向信息的时候修改这些状态队列和其他信号，区别：
- 但是，由于IFU没有真的执行，所以它的预译码结果并不能作为决定指令块是不是真的被错误预测了，所以它不能修改mispredict_vec的状态
- 其次，后端重定向优先级永远高于IFU重定向，两者同时发生时只采用后端重定向。