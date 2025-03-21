---
title: FrontendTrigger
linkTitle: FrontendTrigger
weight: 12
---

<div class="ifu-ctx">

# FrontendTrigger子模块

该子模块的主要作用是在前端设置硬件断点和检查。

该模块的输入pc有一个隐含条件，那就是这个pc是通过ftq传递的startAddr计算出来的。

## FrontendTrigger功能介绍

### 断点设置和断点检查
在IFU的FrontendTrigger模块里共4个Trigger，编号为0,1,2,3，每个Trigger的配置信息（断点类型、匹配地址等）保存在tdata寄存器中。

当软件向CSR寄存器`tselect`、`tdata1/2`写入特定的值时，CSR会向IFU发送tUpdate请求，更新FrontendTrigger内的`tdata`寄存器中的配置信息。
目前前端的Trigger仅可以配置成PC断点`mcontrol.tdata1`寄存器的select位为0；当select=1时，该Trigger将永远不会命中，且不会产生异常）。

在取指时，IFU的F3流水级会向FrontendTrigger模块发起查询并在同一周期得到结果。后者会对取指块内每一条指令在每一个Trigger上做检查，
当指令的PC和`tdata2`寄存器内容的关系满足`mcontrol.match`位所指示的关系（香山支持match位为0、2、3，对应等于、大于等于、小于）时，
该指令会被标记为Trigger命中，随着执行在后端产生断点异常，进入M-Mode或调试模式。

### 链式断点

根据RISCV的debug spec，香山实现的是mcontrol6。

当它们对应的Chain位被置时，只有当该Trigger和编号在它后面一位的Trigger同时命中，~~且timing配置相同时~~（在最新的手册中，这一要求已被删除），处理器才会产生异常。

在过去（riscv-debug-spec-draft，对应 XiangShan 2024.10.05 合入的 [PR#3693](https://github.com/OpenXiangShan/XiangShan/pull/3693) 前）的版本中，Chain 还需要满足两个 Trigger 的 `mcontrol.timing` 是相同的。而在新版（riscv-debug-spec-v1.0.0）中，`mcontrol.timing` 被移除。目前 XiangShan 的 scala 实现仍保留了这一位，但其值永远为 0 且不可写入，编译生成的 verilog 代码中没有这一位。


## FrontendTrigger 接口说明

设计上并没有提供一个或一组对外的接口来查询某个断点的状态，因此，要在测试中检查断点状态，要么需要检查内部信号的情况（仓库中提供的构建脚本已经暴露了所有内部信号），要么通过具体执行过程中，断点的触发情况来判定。

### 输入接口

主要分为控制接口和执行信息（目前执行信息只有pc）

#### 控制接口 io_frontendTrigger

本接口存储了frontendTrigger的控制信息，包含以下信号/信号组：

##### debugMode

当前是否处于debug模式下

##### tEnableVec

对FrontendTrigger的每个断点，指示其是否有效。

##### tUpdate

更新断点的控制信息，包含以下信号/信号组：

valid：此次更新是否有效/是否更新。

bits\_addr：此次更新的是哪个断点（0~3）

bits\_tdata\_action：断点触发条件达成后的行为

bits\_tdata\_chain：断点是否链式传导

bits\_tdata\_matchType：断点匹配类型（等于、大于、小于三种）

bits\_tdata\_select：目前为止，select为0时为pc断点

bits\_tdata\_tdata2：用于和PC比较的基准值

##### triggerCanRaiseBpExp

trigger是否可以引起异常

#### pc

pc有一个隐含条件，就是16条指令的pc必定是连续的

### 输出接口

triggered：16条指令的断点触发情况。

## FrontEndTrigger 测试点和功能点

### 功能点1 设置断点和断点检查
FrontEndTrigger目前仅支持设置PC断点，这通过设置断点的tdata1寄存器的select位为0实现。
同时，tdata2寄存器的mcontrol位负责设置指令PC和tdata2寄存器的地址需要满足的关系，
关系满足时，该指令会被标记为trigger命中。

所以，基于以上功能描述，我们需要测试：

select位为1时，断点是否永远不会触发。

select位为0时，当PC和tdata2的数据的关系满足tdata2的match位时，是否会设置断点。

select位为0时，当PC和tdata2的数据的关系不满足tdata2的match位时，断点是否一定不会触发。

综上所述，我们在这一功能点设计的测试点如下：

| 序号      | 名称                   | 描述                                                |
|---------|----------------------|------------------------------------------------------------------|
| 1\.1    | select1判定            | 给定tdata1的select位为1，随机构造其它输入，检查断点是否没有触发                           |
| 1\.2\.1 | select0关系匹配判定   | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位匹配的输入，检查断点是否触发  | 
| 1\.2\.2 |  select0关系不匹配判定 | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位不匹配的输入，检查断点是否触发 |

### 功能点2 链式断点

当某一个trigger的chain位被置后，当其后的trigger的chain位未设置，且两个trigger均命中~~并且两个trigger的timing相同~~时，后一个trigger才会触发。

对0号trigger，不需要考虑链式的情况

由此，我们可以设置几种测试点：

| 序号   | 名称   | 描述                                                |
|------|------|---------------------------------------------------|
| 2\.1 |  chain位测试 | 对每个trigger，在满足PC断点触发条件的情况下，设置chain位，检查断点是否一定不触发。  |
| 2\.2\.1 | 未命中测试 | 对两个trigger，仅设置前一个trigger的chain位~~且两trigger的timing位相同~~，设置后一个trigger命中而前一个未命中，检查后一个trigger是否一定不触发。 |
| 2\.2\.2 | 命中测试 | 对两个trigger，仅设置前一个trigger的chain位~~且两trigger的timing位相同~~且均命中，检查后一个trigger是否触发。 |

## **测试点汇总**

| 序号   | 功能          | 名称              | 描述                                                |
|------|-------------|-----------------|------------------------------------------------------------------|
| 1\.1 | 断点设置和检查     | select1判定       | 给定tdata1的select位为1，随机构造其它输入，检查断点是否没有触发                                                        |
| 1\.2\.1 | 断点设置和检查     | select0关系匹配判定  | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位匹配的输入，检查断点是否触发                               | 
| 1\.2\.2 | 断点设置和检查     | select0关系不匹配判定 | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位不匹配的输入，检查断点是否触发                              |
| 2\.1 | 链式断点        | chain位测试        | 对每个trigger，在满足PC断点触发条件的情况下，设置chain位，检查断点是否一定不触发                                               |
| 2\.2\.1 | 链式断点        | 未命中测试           | 对两个trigger，仅设置前一个trigger的chain位，设置后一个trigger命中而前一个未命中，检查后一个trigger是否一定不触发 |
| 2\.2\.2 | 链式断点        | 命中测试            | 对两个trigger，仅设置前一个trigger的chain位，检查后一个trigger是否触发 |

</div>