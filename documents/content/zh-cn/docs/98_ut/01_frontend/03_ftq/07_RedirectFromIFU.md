---
title: FTQ接收IFU重定向
linkTitle: 07_FTQ接收IFU重定向
weight: 12
---

## 文档概述
除了后端，IFU也会发送重定向相关消息，和后端不同，IFU的重定向信息来自于预译码写回信息。相同的是，它们都是通过BranchPredictionRedirect的接口传递重定向信息。
## 术语说明 

| 名称               | 定义                                                                         |
| ---------------- | -------------------------------------------------------------------------- |
| RedirectLevel    | 重定向等级，重定向请求是否包括本位置，低表示在本位置后重定向，高表示在本位置重定向。它在之后决定了由重定向导致的冲刷信号是否会影响到发生重定向的指令 |

## 模块功能说明 
### 1. IFU重定向信号生成
#### 流程
IFU重定向是通过这个BranchPredictionRedirect接口传递的，下面来讲述IFU重定向怎么生成IFU的BranchPredictionRedirect内相应信号的，这个过程需要两个周期
信号列表：
**第一个周期**
#### 1.1 IFU 重定向触发条件
- valid：当预译码写回pdWb有效，且pdWb的missOffset字段有效表明存在预测错误的指令，同时后端冲刷信号backendFlush无效时，valid信号有效。
#### 1.2 IFU生成重定向信号
- ftqIdx：接收pdWb指定的ftqIdx
- ftqOffset：接收pdWb的missOffset的bits字段
- level：RedirectLevel.flushAfter，将重定向等级设置为flushAfter
- BTBMissBubble：true
- debugIsMemVio：false
- debugIsCtrl：false
- cfiUpdate：
	信号列表:
	- pc：pdWb中记录的指令块中所有指令pc中，missOffset对应的pc
	- pd：pdWb中记录的指令块中所有指令的pd中，missOffset对应的pd
	- predTaken：从cfiIndex_vec子队列中读取pdWb中ftqIdx索引的项是否valid，有效说明指令块内被预测为有控制流指令。
	- target：pdWb中的target
	- taken：pdWb中cfiOffset的valid字段，有效时表明预译码认为指令块中存在指令控制流指令
	- isMisPred：pdWb中missOffset的valid字段，有效时表明预译码认为指令块中存在预测错误的指令

**第二个周期：**
该周期进行的信号生成是在第一周期valid字段有效的情况下才继续的
 - cifUpdate：
	 信号列表：
	 - 重定向RAS相关信号：通过ftqIdx索引从 ftq_redirect_mem读出ftq_Redirect_SRAMEntry，把其中的所有信号直接传递给cfiUpdate的同名信号中。
	 - target：已在第一周期写入cfiUpdate的pd有效，且isRet字段拉高，指明发生预测错误的指令本是一条Ret指令，此时，将target设置为cfiUpdate的topAddr，帮助回到发生错误之前的状态。

### 2. 重定向结果生效

两个周期生成完整的重定向信息后，IFU重定向信息才有效，有可能被FTQ采取，完整的**IFU重定向结果记为ifuRedirectToBpu**

### 3. IFU 冲刷信号 (`ifuFlush`)

**指令流控制信号**：
ifuFlush：来自IFU的冲刷信号，主要是由IFU重定向造成的，生成IFU重定向信息的两个周期内，该信号都拉高
- 标志：IFU重定向信息产生接口BranchPredictionRedirect中valid有效，表示开始生成重定向信息，该周期以及下一个周期，ifuFlush拉高
## 接口说明

| 顶层IO    | 作用            |
| ------- | ------------- |
| fromIFU | 接收来自IFU的预译码信息 |

## 接口时序 

## 测试点总表 

| 序号   | 功能名称                | 测试点名称                  | 描述                                                                             |
| ---- | ------------------- | ---------------------- | ------------------------------------------------------------------------------ |
| 1\.1 | IFU_REDIRECT        | IFU_REDIRECT_GRN_VALID | 当预译码写回pdWb有效，且pdWb的missOffset字段有效表明存在预测错误的指令，同时后端冲刷信号backendFlush无效时，valid信号有效 |
| 1\.2 | IFU_REDIRECT        | IFU_REDIRECT_GEN       | 允许生成IFU重定向时，在两周期内生成具体信号                                                        |
| 2    | IFU_REDIRECT_TO_BPU | IFU_REDIRECT_TO_BPU    | IFU重定向生成后，IFU重定向结果生效                                                           |
| 3    | IFU_FLUSH           | IFU_FLUSH              | 生成IFU重定向信息的两个周期内，ifuFlush信号都拉高                                                 |

</mrs-testpoints>
