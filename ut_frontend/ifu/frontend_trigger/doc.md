# 万众一芯-ifu-trigger 模块验证报告

## **FrontendTrigger 简介**

### **接口说明**

```java
module FrontendTrigger(
  input         clock,
  input         reset,
  // tdata 寄存器更新信号，每一个断点都有一个 tdata 寄存器
  input         io_frontendTrigger_tUpdate_valid,
  input  [1:0]  io_frontendTrigger_tUpdate_bits_addr,
  input  [1:0]  io_frontendTrigger_tUpdate_bits_tdata_matchType,
  input         io_frontendTrigger_tUpdate_bits_tdata_select,
  input  [3:0]  io_frontendTrigger_tUpdate_bits_tdata_action,
  input         io_frontendTrigger_tUpdate_bits_tdata_chain,
  input  [63:0] io_frontendTrigger_tUpdate_bits_tdata_tdata2,
  // 前端的四个断点使能信号
  input         io_frontendTrigger_tEnableVec_0,
  input         io_frontendTrigger_tEnableVec_1,
  input         io_frontendTrigger_tEnableVec_2,
  input         io_frontendTrigger_tEnableVec_3,
  // 是否处于 debug mode
  input         io_frontendTrigger_debugMode,
  input         io_frontendTrigger_triggerCanRaiseBpExp,
  // 触发信号
  output [3:0]  io_triggered_0,
  output [3:0]  io_triggered_1,
  output [3:0]  io_triggered_2,
  output [3:0]  io_triggered_3,
  output [3:0]  io_triggered_4,
  output [3:0]  io_triggered_5,
  output [3:0]  io_triggered_6,
  output [3:0]  io_triggered_7,
  output [3:0]  io_triggered_8,
  output [3:0]  io_triggered_9,
  output [3:0]  io_triggered_10,
  output [3:0]  io_triggered_11,
  output [3:0]  io_triggered_12,
  output [3:0]  io_triggered_13,
  output [3:0]  io_triggered_14,
  output [3:0]  io_triggered_15,
  //  16个连续的 PC 值
  input  [49:0] io_pc_0,
  input  [49:0] io_pc_1,
  input  [49:0] io_pc_2,
  input  [49:0] io_pc_3,
  input  [49:0] io_pc_4,
  input  [49:0] io_pc_5,
  input  [49:0] io_pc_6,
  input  [49:0] io_pc_7,
  input  [49:0] io_pc_8,
  input  [49:0] io_pc_9,
  input  [49:0] io_pc_10,
  input  [49:0] io_pc_11,
  input  [49:0] io_pc_12,
  input  [49:0] io_pc_13,
  input  [49:0] io_pc_14,
  input  [49:0] io_pc_15
);
```

**FrontendTrigger 模块的输入输出接口主要可以分为以下几类：**

<table>
<tr>
<td>信号描述<br/></td><td>信号类型<br/></td><td>信号改变时影响输出的延迟<br/></td></tr>
<tr>
<td>**tdata 寄存器更新信号**：用于更新断点的配置信息，包括地址、匹配类型、选择标志、动作类型和链式标志等<br/></td><td>输入<br/></td><td>2 个周期<br/></td></tr>
<tr>
<td>**标志位信息**：包括四个断点的使能信号、调试模式标志和触发异常标志<br/></td><td>输入<br/></td><td>两个周期<br/></td></tr>
<tr>
<td>**连续 PC 值输入**：用于提供当前指令块的 16 个连续 PC 值<br/></td><td>输入<br/><br/></td><td>当前周期立即影响<br/></td></tr>
<tr>
<td>**触发信号输出**：16 个 pc 在断点上的触发状态<br/></td><td>输出<br/></td><td>N/A（这是输出结果）<br/></td></tr>
</table>

### **FrontendTrigger 工作过程**

FrontendTrigger 模块作为硬件断点控制单元，主要通过以下过程实现断点触发检测：

1. 后端写 tdata 寄存器更新断点配置信息时，会向 FrontendTrigger 模块更新对应的断点信息，以及标志位信息
2. 前端取指令时，会将当前指令块的 16 个连续 PC 值输入到 FrontendTrigger 模块
3. FrontendTrigger 模块根据当前的 PC 值和断点配置信息，判断是否触发断点（当前周期输出）
4. 触发结果会通过 io_triggered_x 输出，表示每个 PC 的触发状态 -->

#### **配置阶段**

1. **断点寄存器配置**：后端通过写入 tdata 系列寄存器配置断点信息

- 设置断点地址（tdata2）
- 配置匹配类型（matchType：等于/大于等于/小于）
- 设置选择标志（select）、动作类型（action）和链式标志（chain）
- 此类配置变更在 2 个时钟周期后生效

2. **运行时标志控制**：

   - 设置断点使能向量（tEnableVec[<u>0:3</u>]）控制各断点激活状态

- 配置调试模式标志（debugMode）和异常触发标志（triggerCanRaiseBpExp）
- 标志位变更同样在 2 个时钟周期后影响触发结果

#### **检测阶段**

1. **指令获取**：前端取指单元将当前指令块的 16 个连续 PC 值（每个相差 2 字节）输入到模块

- PC 值变更会在当前周期立即触发断点检查

2. **断点匹配计算**：

- 对每个 PC 值应用所有有效断点的匹配规则
- 根据 matchType 进行相应的比较运算（等于/大于等于/小于）
- 考虑 select、enable 标志对断点条件的影响

3. **链式处理**：

- 处理链式断点关系，确保链式断点的正确连续触发
- 当前一个断点的 chain=1 且触发时，才允许检查下一个断点

#### **输出阶段**

- **触发结果输出**：通过 io_triggered_n[<u>3:0</u>] 信号（4 位宽）输出每个 PC 位置的触发状态

整个过程中，PC 值变更会立即影响输出，而断点配置和标志位变更则需要 2 个时钟周期后才会影响输出结果。

## **验证方案**

使用了 toffee 测试框架对 FrontendTrigger 模块进行单元验证。

并且基于 toffee 中的类 UVM 接口，编写了一系列测试函数来验证 FrontendTrigger 模块的功能。测试根目录为 `ut_frontend/ifu/frontend_trigger` 。

**具体文件结构如下：**

<table>
<tr>
<td>文件名<br/></td><td>描述<br/></td></tr>
<tr>
<td>`doc.md`<br/></td><td>本文件，包含测试概要、测试点、测试函数和功能覆盖点等信息。<br/></td></tr>
<tr>
<td>`agent/frontend_trigger_agent.py`<br/></td><td>定义了 FrontendTrigger 的 agent 类，包含 driver、monitor 等方法。<br/></td></tr>
<tr>
<td>`test/frontend_trigger_common_test.py`<br/></td><td>定义了一些常用通用的测试函数，用于验证 FrontendTrigger 模块的基本功能。<br/></td></tr>
<tr>
<td>`test/frontend_trigger_ref.py`<br/></td><td>定义了参考模型，用于验证 FrontendTrigger 模块的行为是否符合预期。<br/></td></tr>
<tr>
<td>`test/test_bug_examples.py`<br/></td><td>出现 bug 的测试用例<br/></td></tr>
<tr>
<td>`test/test_normal_match.py`<br/></td><td>单个断点并且匹配类型为等于、大于等于、小于的测试用例。<br/></td></tr>
<tr>
<td>`test/test_normal_no_match.py`<br/></td><td>单个断点, 但一些标志位不满足的测试用例，例如 tselect=1 或 enable=0 等。<br/></td></tr>
<tr>
<td>`test/test_chain_match.py`<br/></td><td>链式断点的测试用例，测试链式断点的触发情况。<br/></td></tr>
<tr>
<td>`test/test_chain_select_no_match.py`<br/></td><td>链式断点的测试用例，测试链式断点在 select 条件不满足时的触发情况。<br/></td></tr>
<tr>
<td>`test/test_chain_enable_no_match.py`<br/></td><td>链式断点的测试用例，测试链式断点在 enable 条件不满足时的触发情况。<br/></td></tr>
</table>

### **Agent 介绍**

在本次验证中，使用了 toffee 框架中的 agent 概念来组织 FrontendTrigger 模块的验证，共创建一个 agent（`agent/frontend_trigger_agent.py`），包含多个 Driver 和 Monitor 方法。

#### **Driver 方法**

<table>
<tr>
<td>函数名称<br/></td><td>作用<br/></td></tr>
<tr>
<td>reset<br/></td><td>重置 FrontendTrigger 模块<br/></td></tr>
<tr>
<td>set_breakpoint_update<br/></td><td>设置断点更新信息，包括断点地址、匹配类型、select 标志、链式标志等参数<br/></td></tr>
<tr>
<td>set_breakpoint_flags<br/></td><td>设置断点标志位，如使能向量(tEnableVec)、调试模式(debugMode)和触发断点异常(triggerCanRaiseBpExp)等<br/></td></tr>
<tr>
<td>set_pcs<br/></td><td>设置 16 个连续的 PC 值（每个值必须比前一个大 2，表示连续指令）<br/></td></tr>
<tr>
<td>send_cycle<br/></td><td>统计周期信息，用于在每个周期触发 Ref 模型<br/></td></tr>
</table>

#### **Monitor 方法**

<table>
<tr>
<td>函数名称<br/></td><td>作用<br/></td></tr>
<tr>
<td>monitor_breakpoint_update<br/></td><td>监控断点更新，当断点更新有效时收集触发信息<br/></td></tr>
<tr>
<td>monitor_breakpoint_flags<br/></td><td>监控断点标志变化，当标志位变化时记录日志并收集触发信息<br/></td></tr>
<tr>
<td>monitor_pcs_changed<br/></td><td>监控 PC 值变化，当 PC 值发生变化时收集触发信息<br/></td></tr>
</table>

### **FrontendTrigger 参考模型工作流程**

参考模型是一个行为级模型，用于验证设计实现的正确性。该模型通过模拟 FrontendTrigger 模块的工作过程，在每次输入改变时计算预期输出并与 DUT 进行比对。

整个参考模型采用事件驱动方式工作，等待并响应各类输入事件，确保在每次输入变化时都能计算出与硬件设计一致的预期输出。

**在所有事件中，当前仿真周期的处理是核心，所有输入事件都基于当前周期进行处理，不会阻塞等待任意一个事件的完成**。

**参考模型的工作流程如下：**

1. **初始化**

   - 初始化 ifu-trigger 参考实现 (BpRefImpl)
   - 建立与 Agent 通信的驱动(DriverPort)和监控端口(MonitorPort)
2. **主循环处理**

   - 获取当前仿真周期
     - 按优先级处理**各类输入事件**：断点更新、断点标志更新、PC 值更新（**非阻塞处理，如果当前周期没有该事件就不处理**）
   - 检测退出条件

**各类输入事件工作流程:**

1. **断点更新处理**

   - 接收断点地址和断点配置信息
   - 更新内部断点寄存器状态
   - 调用断点检查逻辑计算新的触发结果
   - 将计算出的触发结果发送到监视端口进行比对
2. **断点标志更新处理**

   - 接收新的标志位配置（enable 向量、调试模式、触发异常标志等）
   - 更新参考模型内部标志位状态
   - 调用断点检查逻辑计算新的触发结果
   - 将结果发送到监视端口进行比对
3. **PC 值更新处理**

   - 接收新的 16 个 PC 值
   - 记录旧 PC 和新 PC 值变化
   - 更新参考模型内部 PC 状态
   - 计算触发结果并发送到监控端口进行比对
4. **参考模型断点触发检查逻辑**

   - 构建 PC-断点触发矩阵，记录每个 PC 在每个断点上的触发情况
   - 处理链式断点逻辑，确保链式断点正确触发
   - 按优先级选择触发动作

## **功能点与测试函数**

<table>
<tr>
<td>序号<br/></td><td>功能<br/></td><td>名称<br/></td><td>描述<br/></td></tr>
<tr>
<td>1.1<br/></td><td>断点设置和检查<br/></td><td>select1 判定<br/></td><td>给定 tdata1 的 select 位为 1，随机构造其它输入，检查断点是否没有触发<br/></td></tr>
<tr>
<td>1.2.1<br/></td><td>断点设置和检查<br/></td><td>select0 关系匹配判定<br/></td><td>给定 tdata1 的 select 位为 0，构造 PC 与 tdata2 数据的关系同 tdata2 的 match 位匹配的输入，检查断点是否触发<br/></td></tr>
<tr>
<td>1.2.2<br/></td><td>断点设置和检查<br/></td><td>select0 关系不匹配判定<br/></td><td>给定 tdata1 的 select 位为 0，构造 PC 与 tdata2 数据的关系同 tdata2 的 match 位不匹配的输入，检查断点是否触发<br/></td></tr>
<tr>
<td>2.1<br/></td><td>链式断点<br/></td><td>chain 位测试<br/></td><td>对每个 trigger，在满足 PC 断点触发条件的情况下，设置 chain 位，检查断点是否一定不触发<br/></td></tr>
<tr>
<td>2.2.1<br/></td><td>链式断点<br/></td><td>未命中测试<br/></td><td>对两个 trigger，仅设置前一个 trigger 的 chain 位，设置后一个 trigger 命中而前一个未命中，检查后一个 trigger 是否一定不触发<br/></td></tr>
<tr>
<td>2.2.2<br/></td><td>链式断点<br/></td><td>命中测试<br/></td><td>对两个 trigger，仅设置前一个 trigger 的 chain 位，检查后一个 trigger 是否触发<br/></td></tr>
</table>

<table>
<tr>
<td>测试函数<br/></td><td>测试函数功能<br/></td><td>包含测试点<br/></td></tr>
<tr>
<td>test_tselect1_no_match<br/></td><td>测试 tselect=1 时，不应该触发任何断点<br/></td><td>1.1<br/></td></tr>
<tr>
<td>test_enable0_no_match<br/></td><td>测试 enable=0 时，不应该触发任何断点<br/></td><td>无<br/></td></tr>
<tr>
<td>test_chain_no_match<br/></td><td>测试 chain 为 True 时，该断点不应该触发<br/></td><td>2.1<br/></td></tr>
<tr>
<td>test_match_eq<br/></td><td>测试 matchType=0 (等于) 的单个断点触发情况<br/></td><td>1.2.1, 1.2.2<br/></td></tr>
<tr>
<td>test_match_ge<br/></td><td>测试 matchType=2 (大于等于) 的单个断点触发情况<br/></td><td>1.2.1, 1.2.2<br/></td></tr>
<tr>
<td>test_match_lt<br/></td><td>测试 matchType=3 (小于) 的单个断点触发情况<br/></td><td>1.2.1, 1.2.2<br/></td></tr>
<tr>
<td>test_chain2_match<br/></td><td>测试点：链式断点个数为 2 时，触发情况测试<br/></td><td>2.2.1，2.2.2<br/></td></tr>
<tr>
<td>test_chain3_match<br/></td><td>测试点：链式断点个数为 3 时，触发情况测试<br/></td><td>2.2.1，2.2.2<br/></td></tr>
<tr>
<td>test_chain4_match<br/></td><td>测试点：链式断点个数为 4 时，触发情况测试<br/></td><td>2.2.1，2.2.2<br/></td></tr>
<tr>
<td>test_chain2_enable_no_match<br/></td><td>测试点：链式断点个数为 2 时，且随机一个 enable 条件不满足，不应该触链式断点<br/></td><td>2.2.1<br/></td></tr>
<tr>
<td>test_chain3_enable_no_match<br/></td><td>测试点：链式断点个数为 3 时，且随机一个 enable 条件不满足，不应该触链式断点<br/></td><td>2.2.1<br/></td></tr>
<tr>
<td>test_chain4_enable_no_match<br/></td><td>测试点：链式断点个数为 4 时，且随机一个 enable 条件不满足，不应该触链式断点<br/></td><td>2.2.1<br/></td></tr>
<tr>
<td>test_chain2_select_no_match<br/></td><td>测试点：链式断点个数为 2 时，且随机一个 select 条件不满足，不应该触链式断点<br/></td><td>2.2.1<br/></td></tr>
<tr>
<td>test_chain3_select_no_match<br/></td><td>测试点：链式断点个数为 3 时，且随机一个 select 条件不满足，不应该触链式断点<br/></td><td>2.2.1<br/></td></tr>
<tr>
<td>test_chain4_select_no_match<br/></td><td>测试点：链式断点个数为 4 时，且随机一个 select 条件不满足，不应该触链式断点<br/></td><td>2.2.1<br/></td></tr>
</table>

### **测试函数详细介绍**

#### **test_tselect1_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>将 tselect 设置为 true，其余全随机<br/></td><td>开启所有断点（enable=1），其余标志位均为正常情况<br/></td><td>16 个连续 pc 值，必定会包含一个已经设置断点的触发情况<br/></td><td>没有断点被触发<br/></td></tr>
</table>

#### **test_enable0_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>全随机<br/></td><td>关闭所有断点（enable=0），其余标志位均为正常情况<br/></td><td>16 个连续 pc 值，必定会包含一个已经设置断点的触发情况<br/></td><td>没有断点被触发<br/></td></tr>
</table>

#### **test_chain_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>将 chain 设置为 true，其余全随机<br/></td><td>开启所有断点（enable=1），其余标志位均为正常情况<br/></td><td>16 个连续 pc 值，必定会包含一个已经设置断点的触发情况<br/></td><td>没有断点被触发<br/></td></tr>
</table>

#### **test_match_eq**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>matchType == 0，select == false，chain == false，其余随机<br/></td><td>开启所有断点（enable=1），其余标志位均为正常情况<br/></td><td>16 个连续 pc 值，必定会包含一个已经设置断点的触发情况<br/></td><td>断点触发情况正确<br/></td></tr>
</table>

#### **test_match_ge**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>matchType == 2，select == false，chain == false，其余随机<br/></td><td>开启所有断点（enable=1），其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个已经设置断点的触发情况<br/></td><td>断点触发情况正确<br/></td></tr>
</table>

#### **test_match_lt**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>matchType == 3，select == false，chain == false，其余随机<br/></td><td>开启所有断点（enable=1），其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个已经设置断点的触发情况<br/></td><td>断点触发情况正确<br/></td></tr>
</table>

#### **test_chain2_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次2两个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select == 0<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>只开启待测试的链式断点所在的断点位置（enable==1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正确<br/></td></tr>
</table>

#### **test_chain3_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新3个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select == 0<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>只开启待测试的链式断点所在的断点位置（enable==1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正确<br/></td></tr>
</table>

#### **test_chain4_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新4个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select == 0<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>只开启待测试的链式断点所在的断点位置（enable==1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正确<br/></td></tr>
</table>

#### **test_chain2_enable_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新2个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select == 0<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>随机决定链式断点所在的断点的开启情况（enable == 0 or 1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正常<br/><br/></td></tr>
</table>

#### **test_chain3_enable_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新3个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select == 0<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>随机决定链式断点所在的断点的开启情况（enable == 0 or 1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正常<br/><br/></td></tr>
</table>

#### **test_chain4_enable_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新4个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select == 0<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>随机决定链式断点所在的断点的开启情况（enable == 0 or 1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正常<br/><br/></td></tr>
</table>

#### **test_chain2_select_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新2个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select 随机选择（select == 0 or 1）<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>只开启待测试的链式断点所在的断点位置（enable==1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正确<br/></td></tr>
</table>

#### **test_chain3_select_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新3个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select 随机选择（select == 0 or 1）<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>只开启待测试的链式断点所在的断点位置（enable==1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正确<br/></td></tr>
</table>

#### **test_chain4_select_no_match**

<table>
<tr>
<td>Tdata 寄存器更新信号逻辑<br/></td><td>标志位信息更新逻辑<br/></td><td>连续pc输入逻辑<br/></td><td>预期结果<br/></td></tr>
<tr>
<td>一次更新4个断点信息，满足链式断点要求，要求如下：<br/>1. 所有断点 select 随机选择（select == 0 or 1）<br/>2. 前置断点 chain == true，最后一个断点 chain == false<br/>3. 链式断点 pc 触发条件不互斥<br/><br/>当生成符合要求的**链式断点**时，会将该链式断点尝试放入所有可能的位置，并进行测试。<br/>例如：有 0、1、2、3 四个断点槽位。有一个符合条件的链式断点（**包含两个断点**），则会将该链式断点依次放入（0、1）（1、2）（1、2）（2、3）槽位进行测试。当链式断点包含更多断点时，规则依旧。<br/><br/></td><td>只开启待测试的链式断点所在的断点位置（enable==1）<br/>其余标志位均为正常情况<br/><br/></td><td>16 个连续 pc 值，必定会包含一个符合该链式断点条件的 pc<br/><br/></td><td>链式断点触发情况正确<br/><br/></td></tr>
</table>

### **功能覆盖点汇总**

<table>
<tr>
<td>功能点类别<br/></td><td>功能点名称<br/></td><td>功能点描述<br/></td><td>可能的值<br/></td></tr>
<tr>
<td>**断点触发情况**<br/><br/></td><td>PC0_TRIGGERED ~ PC15_TRIGGERED<br/><br/></td><td>断点 0-15 的触发状态<br/><br/></td><td>- BKPT_EXCPT: 未触发(io_triggered_i=0)<br/>- DEBUG_MODE: 已触发(io_triggered_i=1)<br/></td></tr>
<tr>
<td>**断点设置-匹配类型**<br/></td><td>TRI0_MATCH_TYPE ~ TRI3_MATCH_TYPE<br/></td><td>断点 0-3 的匹配类型<br/></td><td>- EQ: 等于(matchType=0) <br/>- GE: 大于等于(matchType=2)<br/>- LT: 小于(matchType=3)<br/></td></tr>
<tr>
<td>**断点设置-选择标志**<br/></td><td>TRI0_SELECT ~ TRI3_SELECT<br/></td><td>断点 0-3 的选择设置<br/></td><td>- SELECT_0: select=0 <br/>- SELECT_1: select=1<br/></td></tr>
<tr>
<td>**断点设置-动作类型**<br/></td><td>TRI0_ACTION ~ TRI3_ACTION<br/></td><td>断点 0-3 的动作设置<br/></td><td>- ACTION_0: action=0 <br/>- ACTION_1: action=1<br/></td></tr>
<tr>
<td>**断点设置-链式标志**<br/></td><td>TRI0_CHAIN ~ TRI3_CHAIN<br/></td><td>断点 0-3 的链式设置<br/></td><td>- CHAIN_0: chain=0 <br/>- CHAIN_1: chain=1<br/></td></tr>
<tr>
<td>**断点设置-地址数据**<br/><br/></td><td>TRI0_tdata2 ~ TRI3_tdata2<br/><br/></td><td>断点 0-3 的地址设置<br/><br/></td><td>- tdata2_0x{范围起始地址}: 地址在[range_start, range_end)范围内 （注：地址范围按 get_mask_one(50)÷1024 的步长划分）<br/><br/></td></tr>
</table>

## 测试结果

### 测试环境

**硬件环境**

<table>
<tr>
<td>**硬件/系统属性**<br/></td><td>**详细信息**<br/></td></tr>
<tr>
<td>**操作系统 (OS)**<br/></td><td>Arch Linux x86_64<br/></td></tr>
<tr>
<td>**主机型号 (Host)**<br/></td><td>MINI PRO-AHP (Version 1.0)<br/></td></tr>
<tr>
<td>**内核版本 (Kernel)**<br/></td><td>Linux 6.14.6-zen1-1.1-zen<br/></td></tr>
<tr>
<td>**处理器 (CPU)**<br/></td><td>AMD Ryzen 7 8745H (16 核心) @ 4.97 GHz<br/></td></tr>
</table>

**软件环境**

<table>
<tr>
<td>软件名称<br/></td><td>版本号<br/></td></tr>
<tr>
<td>python<br/></td><td>3.12.7<br/></td></tr>
<tr>
<td>pytest<br/></td><td>8.3.5<br/></td></tr>
<tr>
<td>pytest-asyncio<br/></td><td>0.26.0<br/></td></tr>
<tr>
<td>pytoffee<br/></td><td>0.3.2.dev1+gbe1eae1<br/></td></tr>
<tr>
<td>toffee-test<br/></td><td>0.3.0<br/></td></tr>
<tr>
<td>picker<br/></td><td>0.9.0-master-a6699e6-dirty<br/></td></tr>
</table>

### 代码覆盖率

<table>
<tr>
<td>Coverage Rate<br/></td><td>Hint Lines<br/></td><td>Total Lines<br/></td></tr>
<tr>
<td>97.87%<br/></td><td>1559<br/></td><td>1593<br/></td></tr>
</table>

注：未命中部分均为 DPIC 函数

### 功能覆盖率

<table>
<tr>
<td>Coverage Rate<br/></td><td>Hint Points<br/></td><td>Total Points<br/></td></tr>
<tr>
<td>88.89%<br/></td><td>32<br/></td><td>36<br/></td></tr>
</table>

注：未完全覆盖的功能均属于**断点设置-地址数据**类型，50 位的 PC 地址范围太大，由于性能原因，完全覆盖内存和时间消耗过长

### 失败测试用例汇总

<table>
<tr>
<td>用例名称<br/></td><td>说明<br/></td><td>备注<br/></td></tr>
<tr>
<td>test_match_lt<br/></td><td>Pc 值与断点值的小于比较出错<br/></td><td>在最新的香山代码中已经修复，但本次测试的rtl代码存在问题<br/></td></tr>
</table>

注：在链式断点中，因为**小于比较实现错误**的原因，所有链式断点中的断点类型，**都只包括大于等于、等于两种类型**断点！！！！！！！！！！！

### 测试中的一些性能问题

- 功能覆盖率消耗内存过大，当添加数万个功能点时（例如：以 4k 为单位，对 pc 地址进行切分，生成多个功能覆盖点），内存消耗过大，导致测试无法进行。
- 测试用例内存消耗过大，但有数万个测试用例时（例如：使用 pytest 的参数化功能，对输入的 pc 以 4k 为单位进行切分，生成单独的测试用例），消耗内存过大，导致测试无法进行。
