# WayLookup模块验证报告

## 1. 基本信息

| 项目 | 内容 |
|------|------|
| 验证对象 | WayLookup模块 |
| 验证人员 | Gui-Yue |
| 验证时间 | 2025-8 |
| 报告版本 | V0.1 |
| 验证框架 | Toffee测试框架 |

## 2. 验证对象介绍

### 2.1 模块概述
WayLookup模块是香山开源处理器前端ICache中的关键组件，主要负责缓存路查找功能。该模块实现了队列式的查找机制，支持多种操作模式包括读写操作、bypass、刷新操作等。

### 2.2 主要功能
- **队列管理**：实现FIFO队列的基本操作，包括入队、出队
- **指针管理**：维护队列的读写指针，支持指针环绕操作
- **旁路功能**：支持数据旁路传输，提高访问效率
- **刷新操作**：支持队列的flush操作，用于异常处理和状态重置
- **更新操作**：支持对队列条目的动态更新
- **GPF异常处理**：处理Guest Page Fault异常情况

### 2.3 接口信号
模块主要接口包括：

#### 2.3.1 时钟复位信号
- **clock**：系统时钟信号
- **reset**：系统复位信号

#### 2.3.2 IO接口束（io）
- **io.flush**：刷新信号
- **io.read**：读操作接口
  - **io.read.ready**：读操作就绪信号
  - **io.read.valid**：读操作有效信号
  - **io.read.bits**：读操作数据位
    - **io.read.bits.entry**：读条目数据
      - **io.read.bits.entry.waymask**：路掩码
      - **io.read.bits.entry.vSetIdx**：虚拟集合索引
      - **io.read.bits.entry.ptag**：物理标签
      - **io.read.bits.entry.meta_codes**：元数据编码
      - **io.read.bits.entry.itlb**：ITLB相关信息
        - **io.read.bits.entry.itlb.exception**：异常信息
        - **io.read.bits.entry.itlb.pbmt**：页面属性
    - **io.read.bits.gpf**：Guest Page Fault信息
      - **io.read.bits.gpf.isForVSnonLeafPTE**：VS非叶页表项标志
      - **io.read.bits.gpf.gpaddr**：Guest物理地址
- **io.write**：写操作接口
  - **io.write.ready**：写操作就绪信号
  - **io.write.valid**：写操作有效信号
  - **io.write.bits**：写操作数据位（结构同io.read.bits）
- **io.update**：更新操作接口
  - **io.update.valid**：更新操作有效信号
  - **io.update.bits**：更新操作数据位
    - **io.update.bits.corrupt**：损坏标志
    - **io.update.bits.vSetIdx**：虚拟集合索引
    - **io.update.bits.blkPaddr**：块物理地址
    - **io.update.bits.waymask**：路掩码

#### 2.3.3 WayLookup内部接口束
- **WayLookup._readPtr**：读指针
  - **WayLookup._readPtr._flag**：读指针标志
  - **WayLookup._readPtr._value**：读指针值
- **WayLookup._writePtr**：写指针
  - **WayLookup._writePtr._flag**：写指针标志
  - **WayLookup._writePtr._value**：写指针值
- **WayLookup._io_write_ready**：IO写就绪信号
- **WayLookup._entries_i_waymask_j**：条目i路掩码位j

## 3. 验证功能点

WayLookup 有刷新、读写指针更新，更新操作，读操作，写操作五大类（CP23～CP27）。下文逐项说明每个功能点在验证中的场景构造、检查内容与覆盖的测试用例。

### 3.1 刷新操作（CP23）
当 WayLookup 接收到全局刷新信号 `io.flush` 时，需要同时清空 FIFO 内的读写指针和 GPF 缓存。验证时我们先写入一条普通条目和一条带 GPF 的条目，记录当前指针与 GPF 寄存器状态，再拉高 `io.flush`，观察各字段是否回到初始值。

- 测试点 CP23.1：flush 后 `readPtr.value` 重置为 0，`readPtr.flag` 归零。  
- 测试点 CP23.2：flush 后 `writePtr.value` 重置为 0，`writePtr.flag` 归零。  
- 测试点 CP23.3：`gpf_entry.valid` 清零，`gpf_entry.bits` 清零，gpfPtr 与指针同步。  
- 测试用例：TC13 `test_cp23_flush_operations`。

### 3.2 读写指针更新（CP24）
读写握手完成（`io.read.fire` / `io.write.fire` 为高）后，WayLookup 的指针需要按环形结构递增，并在越界时翻转 flag。我们先连续写入多条请求确认写指针自增，再配合读取验证读指针变化，最后通过超过 32 次的写读操作观察 flag 翻转。

- 测试点 CP24.1：`io.read.fire` 为高时，`readPtr.value` 加一，越界后 `readPtr.flag` 翻转。  
- 测试点 CP24.2：`io.write.fire` 为高时，`writePtr.value` 加一，越界后 `writePtr.flag` 翻转。  
- 测试用例：TC14 `test_cp24_pointer_updates`、TC18 `test_pointer_wraparound`。

### 3.3 更新操作（CP25）
MissUnit 在 miss 处理完成后会调用 `io.update` 接口。文档区分命中更新、未命中清零和无需更新三种分支。我们先写入一条候选条目，然后构造不同组合的 `blkPaddr/vSetIdx/waymask/corrupt` 参数，逐一比对更新结果。

- 测试点 CP25.1：命中（`vset_same` 与 `ptag_same` 为真）时，`waymask` 与 `meta_codes` 被更新。  
- 测试点 CP25.2：未命中但 `waymask` 对齐（`vset_same` 和 `way_same` 为真）时，`waymask` 被清零。  
- 测试点 CP25.3：其他情况不更新，原条目保持不变。  
- 测试用例：TC15 `test_cp25_update_operations`。

### 3.4 读操作（CP26）
WayLookup 的读口支持多分支逻辑：当队列为空且写口有效时直接旁路；队列为空且写无效时读信号拉低；普通读取需从 entries 中取数据；若当前读位置匹配 gpfPtr，则带出 GPF 信息并在读取后清空。验证时按文档顺序搭建场景：先测试空队列下的无效读，再触发 bypass，随后写入普通条目与 GPF 条目并依次读出，检查 GPF 字段变化。

- 测试点 CP26.1：`empty` 与 `io.write.valid` 同时为真时，读口直接旁路写数据。  
- 测试点 CP26.2：`empty` 为真且写无效时，`io.read.valid` 维持 0。  
- 测试点 CP26.3：达不到旁路条件时，`io.read.bits.entry` 取自 FIFO 中对应行。  
- 测试点 CP26.4：gpf 命中时，`io.read.bits.gpf` 输出 `gpf_entry` 数据。  
- 测试点 CP26.5：gpf 命中且被读取后，`gpf_entry.valid` 被清零。  
- 测试点 CP26.6：gpf 未命中时，`io.read.bits.gpf` 清零。  
- 测试用例：TC16 `test_cp26_read_operations`。

### 3.5 写操作（CP27）
写路径需要处理队列满、GPF 阻塞、正常写入以及携带 ITLB 异常的特殊逻辑。我们依次执行：填满队列观察 `io.write.ready` 拉低，保留一个待消费的 GPF 条目验证写阻塞，再进行普通写→读闭环验证，最后写入包含 ITLB 异常的条目并区分是否被旁路读取，确认 gpf_entry 更新符合要求。

- 测试点 CP27.1：存在未消费的 gpf_entry 时，`io.write.ready` 变低，写操作被阻塞。  
- 测试点 CP27.2：队列满（读写指针值相同且 flag 不同）时，`io.write.ready` 变低。  
- 测试点 CP27.3：`io.write.valid` 为高且无阻塞时，写入成功并写回 `entries(writePtr)`。  
- 测试点 CP27.4.1：带 ITLB 异常的条目在被旁路立即读取时，`gpf_entry.valid` 仍为 false。  
- 测试点 CP27.4.2：带 ITLB 异常但未被旁路时，`gpf_entry`、`gpfPtr` 被更新等待后续读取。  
- 测试用例：TC17 `test_cp27_write_operations`（旁路相关子场景复用 `test_bypass_functionality` 的日志辅助判定）。

以上测试点覆盖了 WayLookup 官方文档列出的全部功能，确保刷新、指针、更新、读写及异常路径均经过逐项验证。

## 4. 验证方案

### 4.1 验证策略
采用基于Python的Toffee验证框架，通过以下方式进行验证：
- **功能测试**：针对每个功能点设计独立测试用例，验证模块的基本功能
- **接口测试**：验证所有bundle接口信号的可访问性和设置范围
- **场景测试**：测试特定场景如bypass、GPF处理、队列满等
- **数据一致性测试**：验证写入和读取数据的一致性

### 4.2 验证环境
- **测试框架**：Toffee
- **DUT封装**：DUTWayLookup
- **环境类**：WayLookupEnv
- **api**：WayLookupAgent
- **bundle**：WayLookupBundle

### 4.3 覆盖率策略
- **行覆盖率**：通过LCOV工具统计代码行覆盖情况
- **功能覆盖率**：定义覆盖组和覆盖点，确保功能完整性
- **断言覆盖**：在关键路径添加断言检查

## 5. 测试用例

### 5.1 测试用例列表

| 序号 | 测试用例名称  | 测试目标 |
|------|-------------|----------|
| TC01 | test_smoke  | 基本功能冒烟测试 |
| TC02 | test_basic_control_apis  | 验证基本控制API功能 |
| TC03 | test_queue_status_apis  | 验证队列状态查询API |
| TC04 | test_write_entry_api  | 验证写条目API |
| TC05 | test_read_entry_api  | 验证读条目API |
| TC06 | test_helper_apis  | 验证辅助函数API |
| TC07 | test_bypass_functionality  | 验证旁路功能 |
| TC08 | test_comprehensive_queue_operations  | 验证综合队列操作 |
| TC09 | test_bundle_interface_comprehensive  | 验证接口束综合功能 |
| TC10 | test_bundle_signal_ranges_and_limits  | 验证信号范围限制 |
| TC11 | test_bundle_readback_consistency  | 验证接口束一致性 |
| TC12 | test_bundle_signal_coverage_complete  | 验证信号覆盖完整性 |
| TC13 | test_cp23_flush_operations  | 验证刷新操作 |
| TC14 | test_cp24_pointer_updates  | 验证指针更新 |
| TC15 | test_cp25_update_operations  | 验证更新操作 |
| TC16 | test_cp26_read_operations  | 验证读操作 |
| TC17 | test_cp27_write_operations  | 验证写操作 |
| TC18 | test_pointer_wraparound  | 验证指针环绕处理 |

### 5.2 测试数据
- **固定测试向量**：使用预定义的测试数据确保测试的可重复性
- **信号范围测试**：测试信号的0值、最大值以及有效范围
- **异常情况测试**：包含ITLB异常、GPF异常等异常情况测试
- **模式化数据**：fill_queue使用递增模式生成测试数据

## 6. 测试环境

### 6.1 硬件环境
- 仿真器：Verilator
- 操作系统：Linux

### 6.2 软件环境
- Python测试框架：Toffee
- 覆盖率工具：LCOV
- 波形查看：FST格式文件

### 6.3 文件结构
```
waylookup/
├── test/
│   ├── waylookup_test.py          # 主测试文件
│   └── waylookup_fixture.py       # 测试fixture
├── env/
│   ├── waylookup_env.py           # 测试环境
│   └── waylookup_functionalcoverage.py  # 功能覆盖率
├── agent/
│   └── waylookup_agent.py         # 测试api
└── bundle/
    └── waylookup_bundle.py        # bundle定义
```

## 7. 测试结果分析

### 7.1 测试通过率
- **总测试用例数**：18
- **通过用例数**：18
- **失败用例数**：0
- **通过率**：100%

### 7.2 覆盖率分析

#### 7.2.1 行覆盖率
- **总体覆盖率**：97.3% (2396/2462行)
- **WayLookup.v**：99.2% (2259/2277行)
- **WayLookup_top.sv**：74.1% (137/185行)

#### 7.2.2 功能覆盖率
- **总体功能覆盖率**：100%
- **覆盖点总数**：31
- **已覆盖点数**：31
- **覆盖组数量**：7

### 7.3 覆盖率详细分析
功能覆盖率达到100%，说明所有定义的功能点都被充分测试。行覆盖率97.3%属于较高水平，未覆盖的2.7%主要集中在：
- 错误处理分支
- 极端异常情况
- 部分初始化代码路径

## 8. 缺陷分析

### 8.1 发现缺陷
测试过程中未发现功能性缺陷，所有测试用例均通过。

### 8.2 潜在风险点
- WayLookup_top.sv的覆盖率相对较低(74.1%)，建议增加针对顶层模块的测试
- 部分边界条件可能需要更多测试用例

## 9. 测试结论

### 9.1 验证完成度
- √ 所有规划的功能点均已验证
- √ 功能覆盖率达到100%
- √ 行覆盖率达到97.3%，满足验证要求
- √ 所有测试用例通过

### 9.2 模块质量评估
WayLookup模块验证充分，功能实现正确，质量良好。模块在各种测试场景下表现稳定，满足设计要求。

### 9.3 验证结论
**WayLookup模块验证通过**，可以进入下一阶段的集成验证。
