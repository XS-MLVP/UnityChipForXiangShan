---
title: FTQ向后端发送取指目标
linkTitle: 08_FTQ向后端发送取指目标
weight: 12
---

## 文档概述

pc取值目标会发给后端pc mem让他自己进行存储，之后从自己的pc mem取指，此外，最新的FTQ项和对应的跳转目标也会发给后端。

怎样算是一个最新的FTQ项，BPU最新发送的预测块可以是最新的FTQ项，其次，重定向发生时，需要回滚到发生错误预测之前的状态，从指定的FTQ项开始重新开始预测，预译码等等，这也可以是被更新的最新的FTQ项。

## 术语说明 

| 名称  | 定义  |
| --- | --- |
| 暂无  | 暂无  |

## 模块功能说明 
#### 流程
#### 1.发送取值目标到pc mem
- 发送时机：bpu_in_fire，即BPU向前端发送有效预测信息，或者重定向信息的时候。以此为基础之后的第二个周期，进行发送，通过将toBackend接口的pc_mem_wen设置为true的方式指明开始发送
- 接口信号列表：
	- pc_mem_wen：设置为true
	- pc_mem_waddr：接收bpu_in_fire那个周期BPU发送的ftqIdx	
	- pc_mem_wdata：接收bpu_in_fire那个周期，FTQ读取的ftq_pc_mem中的取指目标
#### 2.更新最新的FTQ项
- 发送时机：
	- 最新的FTQ项可能是由BPU写入最新预测信息造成的，**发送取值目标到pc mem**也是因为BPU写入最新预测信息才写入的，如果是这种情况造成的，更新FTQ项和写入pc mem的时机是一致的。
	- 此外发生重定向时，也会进行状态回滚更新FTQ项，标志是后端接口fromBackend的重定向redirect信号有效，或者写入BPU的接口toBPU的redirctFromIFU拉高说明当前有来自IFU的重定向
		- *（注释（可忽略）IFU重定向信号生成有两个周期，可以认为第一个周期预译码信息中missoffset有效说明IFU重定向发生，也可以认为第二个周期redirctFromIFU拉高说明重定向发生，此处取后者）。*
	- 同样是向toBackend中写入
- 接口信号列表：
	- newest_entry_en：前面说的发送时机到来时，再延迟一个周期达到真正的写入时机，这时才拉高信号
	- newest_entry_ptr：发送时机到来时的newest_entry_ptr，在真正的写入时机写入
	- newest_entry_target：发送时机到来时的newest_entry_target
	newest_entry_ptr，newest_entry_target这几个都是同名的内部信号，如之前所说，BPU新的写入，重定向等等都会对最新FTQ项进行新的安排，在相应的文档中，对其生成方式做具体的描述。
## 接口说明

| 顶层IO      | 作用              |
| --------- | --------------- |
| toBackend | 发送取指令目标，让后端进行储存 |

## 测试点总表 


| 序号  | 功能名称               | 测试点名称         | 描述            |
| --- | ------------------ | ------------- | ------------- |
| 1   | SEND_PC_TO_BACKEND | SEND_PC       | 发送取值目标到pc mem |
| 2   | SEND_PC_TO_BACKEND | UPDATE_NEWEST | 更新最新的FTQ项     |

</mrs-testpoints>

