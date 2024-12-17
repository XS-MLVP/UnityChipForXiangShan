---
title: FrontendTrigger
linkTitle: FrontendTrigger
weight: 12
---

# FrontendTrigger子模块
该子模块的主要作用是在前端设置硬件断点和检查。

## FrontendTrigger功能介绍

### 断点设置和断点检查
在IFU的FrontendTrigger模块里共4个Trigger，编号为0,1,6,8，每个Trigger的配置信息（断点类型、匹配地址等）保存在tdata寄存器中。

当软件向CSR寄存器tselect、tdata1/2写入特定的值时，CSR会向IFU发送tUpdate请求，更新FrontendTrigger内的tdata寄存器中的配置信息。
目前前端的Trigger仅可以配置成PC断点（mcontrol(tdata1)寄存器的select位为0；当select=1时，该Trigger将永远不会命中，且不会产生异常）。

在取指时，IFU的F3流水级会向FrontendTrigger模块发起查询并在同一周期得到结果。后者会对取指块内每一条指令在每一个Trigger上做检查，
当指令的PC和tdata2寄存器内容的关系满足mcontrol的match位所指示的关系（香山支持match位为0、2、3，对应等于、大于、小于）时，
该指令会被标记为Trigger命中，随着执行在后端产生断点异常，进入M-Mode或调试模式。

### 链式断点

前端的0、6、8号Trigger支持Chain功能。
当它们对应的Chain位被置时，只有当该Trigger和编号在它后面一位的Trigger同时命中，且timing配置相同时，处理器才会产生异常。其中可以和6,8号trigger实现chain功能的7,9号trigger在后端访存部件中

## FrontEndTrigger测试点和功能点

### 功能点1 设置断点和断点检查
FrontEndTrigger目前仅支持设置PC断点，这通过设置断点的tdata1寄存器的select位为0实现。
同时，tdata2寄存器的mcontrol位负责设置指令PC和tdata2寄存器的地址需要满足的关系，
关系满足时，该指令会被标记为trigger命中。

所以，基于以上功能描述，我们需要测试：

select位为1时，断点是否永远不会处罚。

select位为0时，当PC和tdata2的数据的关系满足tdata2的match位时，是否会设置断点。

select位为0时，当PC和tdata2的数据的关系不满足tdata2的match位时，断点是否一定不会触发。

综上所述，我们在这一功能点设计的测试点如下：

| 序号      | 名称                   | 描述                                                |
|---------|----------------------|------------------------------------------------------------------|
| 1\.1    | select1判定            | 给定tdata1的select位为1，随机构造其它输入，检查断点是否没有触发                           |
| 1\.2\.1 | select0关系匹配判定   | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位匹配的输入，检查断点是否触发  | 
| 1\.2\.2 |  select0关系不匹配判定 | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位不匹配的输入，检查断点是否触发 |

### 功能点2 链式断点

当某一个trigger的chain位被置后，当其后的trigger的chain位未设置，且两个trigger均命中并且两个trigger的timing相同时，后一个trigger才会触发。

对0号trigger，不需要考虑链式的情况

由此，我们可以设置几种测试点：

| 序号   | 名称   | 描述                                                |
|------|------|---------------------------------------------------|
| 2\.1 |  chain位测试 | 对每个trigger，在满足PC断点触发条件的情况下，设置chain位，检查断点是否一定不触发。  |
| 2\.2 | timing测试 | 对两个trigger，仅设置前一个trigger的chain位，且两trigger的timing位不同，随机设置PC等，测试后一个trigger是否一定不触发。 | 
| 2\.3\.1 | 未命中测试 | 对两个trigger，仅设置前一个trigger的chain位，且两trigger的timing位相同，设置后一个trigger命中而前一个未命中，检查后一个trigger是否一定不触发。 |
| 2\.3\.2 | 命中测试 | 对两个trigger，仅设置前一个trigger的chain位，且两trigger的timing位相同且均命中，检查后一个trigger是否触发。 |

## **测试点汇总**

| 序号   | 功能          | 名称              | 描述                                                |
|------|-------------|-----------------|------------------------------------------------------------------|
| 1\.1 | 断点设置和检查     | select1判定       | 给定tdata1的select位为1，随机构造其它输入，检查断点是否没有触发                                                        |
| 1\.2\.1 | 断点设置和检查     | select0关系匹配判定  | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位匹配的输入，检查断点是否触发                               | 
| 1\.2\.2 | 断点设置和检查     | select0关系不匹配判定 | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位不匹配的输入，检查断点是否触发                              |
| 2\.1 | 链式断点        | chain位测试        | 对每个trigger，在满足PC断点触发条件的情况下，设置chain位，检查断点是否一定不触发                                               |
| 2\.2 | 链式断点        | timing测试        | 对两个trigger，仅设置前一个trigger的chain位，且两trigger的timing位不同，随机设置PC等，测试后一个trigger是否一定不触发               | 
| 2\.3\.1 | 链式断点        | 未命中测试           | 对两个trigger，仅设置前一个trigger的chain位，且两trigger的timing位相同，设置后一个trigger命中而前一个未命中，检查后一个trigger是否一定不触发 |
| 2\.3\.2 | 链式断点        | 命中测试            | 对两个trigger，仅设置前一个trigger的chain位，且两trigger的timing位相同且均命中，检查后一个trigger是否触发 |
