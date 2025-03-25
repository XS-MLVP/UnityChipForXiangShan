---
title: IFU向FTQ写回预译码信息
linkTitle: 05_IFU向FTQ写回预译码信息
weight: 12
---

## 文档概述

IFU获取来自BPU的预测信息之后，会执行预译码，并将FTQ项写回FTQ中去。我们会比对FTQ中原BPU预测项和预译码的结果，判断是否有预测错误
### 基本流程

预译码写回ftq_pd_mem：
- FTQ从pdWb接口中获取IFU的写回信息，FTQ首先将预译码写回信息写回到ftq_pd_mem,

更新提交状态队列commitStateQueue：
- 然后根据写回信息中指令的有效情况更新提交状态队列commitStateQueue。

比对错误：
- 同时，从ftb_entry_mem读出ifu_Wb_idx所指的FTB项，将该FTB项的预测结果与预译码写回结果进行对比，看两者对分支的预测结果是否有所不同。

综合错误：
- 之后就综合根据预译码信息可能得到的错误：有前面说的比对BPU的预测结果和预译码结果得到的错误，也有直接根据预译码得到的错误预测信息。根据错误预测结果更新命中状态队列。

更新写回指针
- 最后，如果IFU成功写回，ifu_Wb_idx更新加1。

## 术语说明 

| 名称       | 定义                        |
| -------- | ------------------------- |
| 预译码      | IFU会对取指目标进预译码，之后写回FTQ     |
| ifuWbPtr | IFU写回指针，知识IFU预译码要写入FTQ的位置 |

## 模块功能说明 
### 1. 预译码写回ftq_pd_mem
写回有效：预译码信息pdWb有效时，写有效
写回地址：pdWb的ftqIdx的value
写回值：解析整个pdWb的结果

### 2. 更新提交状态队列

当预译码信息pdWb有效时，相当于写回有效，此时，根据预译码信息中每条指令的有效情况和该指令是否在有效范围内，判断指令的提交状态是否可以修改，若可以修改，则将提交状态队列，写回项中的指令状态修改
#### 详细信号表示
pdWb有效时，ifu_wb_valid拉高。
此时，对于预译码信息中每一条指令的预译码结果pd做判断：
如果预译码结果valid，且指令在有效范围内（根据insrtRange的bool数组指示），则提交状态队列commitStateQueue中，写回项中的指令状态修改为c_toCommit，表示可以提交，这是因为只有在FTQ项被预译码写回后，才能根据后端提交信息提交该FTQ项，之后会把预译码信息一并发往更新通道。
### 3. 比对预测结果与预译码结果
从ftb存储队列ftb_entry_mem中的读取ifu写回指针ifuwbptr的对应项：
- pdWb有效的时候，读有效，读取地址为预译码信息中指示的ftqIdx。
当命中状态队列指示待比对项ftb命中，且回写有效时，读取出FTB存储队列中对应的项，与预译码信息进行比对，当BPU预测的FTB项指示指令是有效分支指令，而预译码信息中则指示不是有效分支指令时，发生分支预测错误，当BPU预测的FTB项指示指令是有效jmp指令，而预译码信息中则指示不是有效jmp指令时，发生跳转预测错误
#### 详细信号表示：
ifu_wb_valid回写有效时，ftb_entry_mem回写指针对应读使能端口ren有效，读取地址为ifu_wb_idx预测译码信息中指示的ftqIdx的value值。
回写项命中且回写有效，hit_pd_valid信号有效，此时，读取ftb存储队列中的FTB项，读出brSlots与tailSlot，并进行比对：
#### 3.1 判断是否有分支预测错误br_false_hit
##### 测试点3.1.1和3.1.2对应以下两种条件导致的br_false_hit
- 判断是否有分支预测错误br_false_hit：
    1. brSlots的任意一项有效，同时在预译码信息中不满足这一项对应的pd有效且isBr字段拉高表明是分支指令，
    2. taiSlot有效且sharing字段拉高表明该slot为分支slot，同时在预译码信息中不满足这一项对应的pd有效且isBr字段拉高表明是分支指令
    满足任意条件可判断发生分支预测错误br_false_hit，该信号拉高
#### 3.2 判断是否发生jmp预测错误jal_false_hit
- 判断是否发生jmp预测错误jal_false_hit：
    - 预测结果中必须指明指令预测有效，且其中isJal拉高表面是jal指令或者指明是isjalr指令
### 4. 预译码错误
直接从预测结果中获取错误预测相关信息，如果回写项ftb命中且missoffset字段有效表明有错误预测的指令，hit_pd_mispred信号拉高，表示预译码结果中直接指明有预测错误的指令。
### 5. 综合错误
综合比对预测结果与预译码结果得到的错误信息，与预译码错误直接获得的预测错误，任意一种发生时has_false_hit拉高表示有预测错误，此时，命中状态队列entry_hit_status中写回项的状态置为h_false_hit
### 6. 更新写回指针
ifu_wb_valid拉高，表示写回有效，将ifuWbPtr更新为原值加1。

## 接口说明 

| 顶层IO    | 子接口  |
| ------- | ---- |
| fromIfu | pdWb |

## 测试点总表

| 序号      | 功能名称               | 测试点名称              | 描述                                                                                                                |
| ------- | ------------------ | ------------------ | ----------------------------------------------------------------------------------------------------------------- |
| 1       | WB_PD              | WB_PD              | 向ftq_pd_mem中写回预译码信息                                                                                               |
| 2       | UPDATE_COMMITSTATE | UPDATE_COMMITSTATE | 当预译码信息pdWb有效时，根据预译码信息中每条指令的有效情况和该指令是否在有效范围内，判断指令的提交状态是否可以修改，若可以修改，则将提交状态队列，写回项中的指令状态修改                            |
| 3\.1\.1 | BR_FALSE_HIT       | COND1              | brSlots的任意一项有效，同时在预译码信息中不满足这一项对应的pd有效且isBr字段拉高                                                                    |
| 3\.1\.2 | BR_FALSE_HIT       | COND2              | taiSlot有效且sharing字段拉高表明该slot为分支slot，同时在预译码信息中不满足这一项对应的pd有效且isBr字段拉高                                               |
| 3\.2    | JAL_FALSE_HIT      | JAL_FALSE_HIT      | 指令预测有效，且其中isJal拉高或者指明是isjalr指令                                                                                    |
| 4       | PD_MISS            | PD_MISS            | 如果回写项ftb命中且missoffset字段有效表明有错误预测的指令，hit_pd_mispred信号拉高                                                            |
| 5       | FALSE_HIT          | FALSE_HIT          | 综合比对预测结果与预译码结果得到的错误信息，与预译码错误直接获得的预测错误，任意一种发生时has_false_hit拉高表示有预测错误，此时，命中状态队列entry_hit_status中写回项的状态置为h_false_hit |
| 6       | UPDATE_IFU_WB_PTR  | UPDATE_IFU_WB_PTR  | ifu_wb_valid拉高，将ifuWbPtr更新为原值加1                                                                                   |

