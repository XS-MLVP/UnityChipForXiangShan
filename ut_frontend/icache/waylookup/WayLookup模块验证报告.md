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

### 3.1 冒烟测试
- **CP01: 基本功能冒烟测试**
  - 验证模块的基本可用性

### 3.2 基本控制功能
- **CP02: 基本控制API验证**
  - 验证api的基本控制接口功能
  - 测试reset和flush api的正常运作
  
- **CP03: 队列状态API验证**
  - 测试队列查询api的可用性

### 3.3 条目操作功能
- **CP04: 写条目API验证**
  - 验证单个条目写入的正确性
  - 测试写入操作的握手协议
  - 验证写入数据的存储和保持
  - 确保写操作正确更新队列状态
- **CP05: 读条目API验证**
  - 验证单个条目读取的正确性
  - 测试读取操作的握手协议
  - 验证读取数据的完整性和准确性
  - 验证写入的数据和读取的数据相匹配
- **CP06: 辅助函数API验证**
  - 验证fill_queue批量写入功能的正确性
  - 测试drain_queue批量读取功能的正确性
  - 验证wait_for_condition条件等待功能
  - 测试队列状态查询的准确性

### 3.4 高级功能
- **CP07: bypass功能验证**
  - 验证bypass功能的正确性
  - 测试bypass读写的一致性
- **CP08: 综合队列操作验证**
  - 验证入队和出队操作的正确性
  - 测试并发读写操作的数据一致性
  - 验证队列在各种负载下的稳定性
  - 确保FIFO队列语义的正确实现

### 3.5 接口验证
- **CP09: bundle综合验证**
  - 验证所有接口信号的综合功能
  - 测试接口间的相互作用
  - 验证接口协议的完整性
- **CP10:bundle 信号范围和限制验证**
  - 验证信号的有效取值范围
  - 测试超出范围时的错误处理
  - 验证信号的边界值行为
  - 确保信号约束的正确实现
- **CP11:bundle一致性验证**
  - 验证接口信号的逻辑一致性
  - 测试信号时序的匹配关系
  - 验证接口状态的同步更新
  - 确保接口行为的可预测性
- **CP12: bundle信号覆盖完整性验证**
  - 验证所有定义信号的功能覆盖
  - 测试信号的各种取值组合
  - 验证异常信号的处理机制
  - 确保信号定义的完备性

### 3.6 专项功能验证
- **CP13: 刷新操作验证**
  - 验证flush信号对队列的清空功能
  - 测试刷新操作后读写指针被重置为0
  - 验证刷新操作后队列状态变为空
  - 确保刷新操作的正确性

- **CP14: 指针更新验证**
  - 验证写操作成功时写指针正确递增
  - 验证读操作成功时读指针正确递增
  - 测试指针在fire信号触发时的更新行为
  - 确保指针在32条目队列中的正确环绕

- **CP15: 更新操作验证**
  - 验证命中更新时waymask字段的正确更新
  - 测试vSetIdx不匹配时更新操作不生效
  - 验证corrupt标志设置时更新操作不生效
  - 测试miss更新时waymask字段被清零的条件

- **CP16: 读操作验证**
  - 验证队列空且写信号无效时读信号无效
  - 测试bypass读操作的数据一致性
  - 验证GPF命中时读取正确的GPF信息
  - 测试GPF miss时读取正常条目数据

- **CP17: 写操作验证**
  - 验证正常写操作的成功执行
  - 测试带ITLB异常的写操作
  - 验证队列满时写操作失败
  - 测试写操作的握手协议和数据完整性

- **CP18: 指针环绕处理验证**
  - 验证读写指针在队列边界的环绕行为
  - 测试连续写入超过队列大小时的指针管理
  - 验证连续读取时指针的正确递增和环绕
  - 确保环形缓冲区语义的正确实现

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
