# ICacheMissUnit模块验证报告

## 1. 基本信息

| 项目 | 内容 |
|------|------|
| 验证对象 | ICacheMissUnit模块 |
| 验证人员 | Gui-Yue |
| 验证时间 | 2025-8 |
| 报告版本 | V0.1 |
| 验证框架 | Toffee测试框架 |

## 2. 验证对象介绍

### 2.1 模块概述
ICacheMissUnit模块是香山开源处理器前端ICache中的关键组件，主要负责指令缓存缺失处理功能。该模块实现了MSHR管理机制，支持多种操作模式包括取指缺失处理、预取缺失处理、TileLink协议通信等。

### 2.2 硬件架构

ICacheMissUnit包含以下主要组件：

#### 2.2.1 MSHR管理单元
- **14个MSHR**（Miss Status Holding Register）
  - 4个fetchMSHR（ID: 0-3）：处理取指缺失
  - 10个prefetchMSHR（ID: 4-13）：处理预取缺失

#### 2.2.2 请求仲裁器
- **fetchArb**: fetch请求间的仲裁
- **prefetchArb**: prefetch请求间的仲裁  
- **acquireArb**: acquire请求间的仲裁（fetch优先于prefetch）

#### 2.2.3 TileLink协议接口
- **Acquire通道**: 向下级发送缺失请求
- **Grant通道**: 接收下级返回的数据，支持multi-beat传输

#### 2.2.4 数据处理单元
- Grant数据收集与拼装
- SRAM写回控制
- 替换策略更新

### 2.3 接口信号
模块主要接口包括：

#### 2.3.1 时钟复位信号
- **clock**：系统时钟信号
- **reset**：系统复位信号

#### 2.3.2 IO接口束（io）
- **io.fetch**：取指操作接口
  - **io.fetch.req**：取指请求接口
    - **io.fetch.req.valid**：取指请求有效信号
    - **io.fetch.req.ready**：取指请求就绪信号
    - **io.fetch.req.bits**：取指请求数据位
      - **io.fetch.req.bits.blkPaddr**：块物理地址（42位）
      - **io.fetch.req.bits.vSetIdx**：虚拟集合索引（8位）
  - **io.fetch.resp**：取指响应接口
    - **io.fetch.resp.valid**：取指响应有效信号
    - **io.fetch.resp.bits**：取指响应数据位
      - **io.fetch.resp.bits.blkPaddr**：块物理地址
      - **io.fetch.resp.bits.vSetIdx**：虚拟集合索引
      - **io.fetch.resp.bits.waymask**：路掩码（4位）
      - **io.fetch.resp.bits.data**：缓存数据（512位）
      - **io.fetch.resp.bits.corrupt**：数据损坏标志

- **io.prefetch_req**：预取请求接口
  - **io.prefetch_req.valid**：预取请求有效信号
  - **io.prefetch_req.ready**：预取请求就绪信号
  - **io.prefetch_req.bits**：预取请求数据位
    - **io.prefetch_req.bits.blkPaddr**：块物理地址（42位）
    - **io.prefetch_req.bits.vSetIdx**：虚拟集合索引（8位）

- **io.mem**：TileLink内存接口
  - **io.mem.acquire**：内存获取接口
    - **io.mem.acquire.valid**：获取请求有效信号
    - **io.mem.acquire.ready**：获取请求就绪信号
    - **io.mem.acquire.bits**：获取请求数据位
      - **io.mem.acquire.bits.source**：源标识（4位）
      - **io.mem.acquire.bits.address**：内存地址（48位）
  - **io.mem.grant**：内存授权接口
    - **io.mem.grant.valid**：授权响应有效信号
    - **io.mem.grant.ready**：授权响应就绪信号
    - **io.mem.grant.bits**：授权响应数据位
      - **io.mem.grant.bits.source**：源标识（4位）
      - **io.mem.grant.bits.opcode**：操作码（3位）
      - **io.mem.grant.bits.data**：数据（256位）
      - **io.mem.grant.bits.corrupt**：数据损坏标志

- **io.victim**：替换策略接口
  - **io.victim.vSetIdx**：替换集合索引接口
    - **io.victim.vSetIdx.valid**：替换索引有效信号
    - **io.victim.vSetIdx.bits**：替换索引值（8位）
  - **io.victim.way**：替换路选择（2位）

- **io.data_write**：数据写入接口
  - **io.data_write.valid**：数据写入有效信号
  - **io.data_write.bits**：数据写入数据位
    - **io.data_write.bits.data**：写入数据（512位）
    - **io.data_write.bits.virIdx**：虚拟索引（8位）
    - **io.data_write.bits.waymask**：路掩码（4位）

- **io.meta_write**：元数据写入接口
  - **io.meta_write.valid**：元数据写入有效信号
  - **io.meta_write.bits**：元数据写入数据位
    - **io.meta_write.bits.waymask**：路掩码（4位）
    - **io.meta_write.bits.virIdx**：虚拟索引（8位）
    - **io.meta_write.bits.phyTag**：物理标签（42位）
    - **io.meta_write.bits.bankIdx**：Bank索引（8位）

- **io.flush**：刷新信号
- **io.fencei**：指令缓存刷新信号
- **io.hartId**：硬件线程标识（8位）

#### 2.3.3 ICacheMissUnit内部接口束
- **ICacheMissUnit_.fetchMSHRs**：取指MSHR数组（4个）
  - **ICacheMissUnit_.fetchMSHRs.{i}.io.req_ready**：MSHR请求就绪信号
  - **ICacheMissUnit_.fetchMSHRs.{i}.io.acquire_valid**：MSHR获取有效信号
- **ICacheMissUnit_.prefetchMSHRs**：预取MSHR数组（10个）
  - **ICacheMissUnit_.prefetchMSHRs.{i}.io.req_ready**：MSHR请求就绪信号
  - **ICacheMissUnit_.prefetchMSHRs.{i}.io.acquire_valid**：MSHR获取有效信号
- **ICacheMissUnit_.last_fire**：最后拍触发信号
- **ICacheMissUnit_.fetchHit**：取指命中信号
- **ICacheMissUnit_.prefetchHit**：预取命中信号

---

## 3. 验证功能点

### 3.1 冒烟测试
- **CP01: 基本功能冒烟测试**
  - 验证模块的基本可用性
  - 测试关键路径的正常工作
  - 验证模块集成的兼容性
  - 确保基础功能的快速验证

### 3.2 基本控制功能
- **CP02: Bundle接口fetch请求驱动验证**
  - 验证fetch请求输入信号的驱动功能
  - 测试fetch_req_valid信号的设置
  - 验证fetch_req_bits_blkPaddr的地址驱动
  - 确保fencei信号的正确控制

- **CP03: Bundle接口ready信号读取验证**
  - 验证fetch_req_ready信号的读取正确性
  - 测试ready信号状态的实时反映
  - 验证信号取值范围的合理性
  - 确保信号读取的一致性

- **CP04: Fencei功能验证**
  - 验证fencei信号对所有MSHR的清理功能
  - 测试fencei=1时MSHR状态的重置
  - 验证fencei=0后MSHR的恢复
  - 确保fencei处理的原子性

- **CP05: Flush信号控制验证**
  - 验证flush信号的设置和清除
  - 测试flush信号的响应机制
  - 验证flush对系统状态的影响
  - 确保flush操作的正确性

- **CP06: Victim Way设置验证**
  - 验证victim way的配置功能
  - 测试所有可能的way值(0-3)
  - 验证victim way信号的正确传播
  - 确保替换策略的参数设置

### 3.3 请求发送功能
- **CP07: Fetch请求发送验证**
  - 验证fetch请求的发送能力
  - 测试4个fetch MSHR的容量限制
  - 验证第5个请求的正确拒绝
  - 确保请求发送的准确性

- **CP08: Prefetch请求发送验证**
  - 验证prefetch请求的发送能力
  - 测试10个prefetch MSHR的容量限制
  - 验证第11个请求的正确拒绝
  - 确保prefetch发送的可靠性

### 3.4 API流程功能
- **CP09: Fetch请求生成Acquire验证**
  - 验证fetch请求正确生成acquire
  - 测试source ID的正确分配
  - 验证地址映射的准确性
  - 确保请求与acquire的关联

- **CP10: 完整Fetch流程验证**
  - 验证端到端的fetch处理流程
  - 测试victim way的设置时序
  - 验证Grant响应的正确处理
  - 确保完整流程的功能正确性

- **CP11: Grant数据损坏处理验证**
  - 验证corrupt标志的正确传播
  - 测试数据损坏时的响应生成
  - 验证corrupt数据的处理机制
  - 确保错误处理的完整性

- **CP12: 完整Prefetch流程验证**
  - 验证端到端的prefetch处理流程
  - 测试prefetch source ID的分配
  - 验证prefetch响应的生成
  - 确保prefetch功能的正确性

### 3.5 FIFO功能验证
- **CP13: FIFO模块综合验证**
  - 验证Priority FIFO的完整功能
  - 测试FIFO满状态的阻塞机制
  - 验证指针回环和队列操作
  - 确保FIFO调度的正确性

### 3.6 MSHR管理功能
- **CP14: MSHR命中检测验证**
  - 验证fetch请求命中现有MSHR
  - 测试prefetch请求命中检测
  - 验证相同地址的命中逻辑
  - 确保MSHR查找的准确性

- **CP15: MSHR释放验证**
  - 验证Grant完成后MSHR的释放
  - 测试MSHR状态的正确更新
  - 验证MSHR生命周期管理
  - 确保资源释放的及时性

### 3.7 优先级策略功能
- **CP16: Fetch MSHR低索引优先级验证**
  - 验证fetchDemux的索引分配策略
  - 测试低索引MSHR的优先使用
  - 验证MSHR占用状态的更新
  - 确保优先级算法的正确性

- **CP17: Prefetch MSHR低索引优先级验证**
  - 验证prefetchDemux的索引分配
  - 测试chosen信号的正确指示
  - 验证低索引MSHR的优先使用
  - 确保prefetch优先级的实现

- **CP18: FIFO优先级顺序验证**
  - 验证prefetch请求的FIFO顺序
  - 测试source ID的递增分配
  - 验证先入先出的调度逻辑
  - 确保队列顺序的公平性

- **CP19: Acquire仲裁优先级验证**
  - 验证fetch优先于prefetch的仲裁
  - 测试混合请求的处理顺序
  - 验证仲裁逻辑的公平性
  - 确保优先级策略的实施

### 3.8 数据传输功能
- **CP20: Grant多Beat数据收集验证**
  - 验证multi-beat数据的收集
  - 测试last_fire信号的正确生成
  - 验证数据拼装的完整性
  - 确保数据传输的可靠性

- **CP21: Victim Way更新验证**
  - 验证acquire fire时victim信号生成
  - 测试victim vSetIdx的正确传播
  - 验证替换策略的更新机制
  - 确保victim信息的准确性

- **CP22: Waymask生成验证**
  - 验证根据victim way生成waymask
  - 测试独热编码的正确性
  - 验证不同way的waymask生成
  - 确保waymask逻辑的准确性

### 3.9 SRAM写回功能
- **CP23: SRAM写回条件验证**
  - 验证正常情况下的SRAM写入
  - 测试Meta和Data写信号的生成
  - 验证写回条件的判断逻辑
  - 确保写回控制的正确性

- **CP24: Flush/Fencei写回抑制验证**
  - 验证flush/fencei时不写SRAM
  - 测试写回抑制机制的正确性
  - 验证响应仍能正常生成
  - 确保异常处理的完整性

### 3.10 特殊情况处理
- **CP25: Flush/Fencei MSHR行为验证**
  - 验证flush对prefetch MSHR的影响
  - 测试fencei对所有MSHR的清理
  - 验证异常信号的处理机制
  - 确保状态管理的正确性

- **CP26: 相同地址处理验证**
  - 验证prefetch与fetch相同地址的处理
  - 测试特殊命中条件的检测
  - 验证地址冲突的解决机制
  - 确保冲突处理的合理性

- **CP27: Demux选择信号验证**
  - 验证demux chosen信号的正确性
  - 测试MSHR索引选择的准确性
  - 验证选择逻辑的一致性
  - 确保demux功能的可靠性

### 3.11 断言验证功能
- **CP28: Priority FIFO入队断言验证**
  - 验证enq信号的断言条件
  - 测试入队操作的时序约束
  - 验证违规条件的检测
  - 确保断言机制的有效性

- **CP29: Priority FIFO出队断言验证**
  - 验证deq信号的断言条件
  - 测试出队操作的时序约束
  - 验证握手协议的正确性
  - 确保断言保护的完整性

---

## 4. 验证方案

### 4.1 验证策略
采用基于Python的Toffee验证框架，通过以下方式进行验证：
- **单元测试**：针对每个功能点设计独立测试用例
- **随机测试**：使用随机数据验证模块的鲁棒性
- **边界测试**：验证极限条件下的模块行为
- **功能覆盖**：确保所有功能点都被充分测试

### 4.2 验证环境
- **测试框架**：Toffee
- **DUT封装**：DUTICacheMissUnit
- **环境类**：ICacheMissUnitEnv
- **代理类**：ICacheMissUnitAgent
- **信号束**：ICacheMissUnitBundle

### 4.3 覆盖率策略
- **行覆盖率**：通过LCOV工具统计代码行覆盖情况
- **功能覆盖率**：定义覆盖组和覆盖点，确保功能完整性
- **断言覆盖**：在关键路径添加断言检查

## 5. 测试用例

### 5.1 测试用例列表

| 序号 | 测试用例名称  | 测试目标 |
|------|-------------|----------|
| TC01 | test_smoke | 基本功能冒烟测试 |
| TC02 | test_bundle_drive_fetch_req_inputs |  验证Bundle接口fetch请求驱动 |
| TC03 | test_bundle_read_fetch_req_ready |  验证Bundle接口ready信号读取 |
| TC04 | test_fencei_work |  验证Fencei功能 |
| TC05 | test_set_flush |  验证Flush信号控制 |
| TC06 | test_set_victim_way |  验证Victim Way设置 |
| TC07 | test_send_fetch_request |  验证Fetch请求发送 |
| TC08 | test_send_prefetch_request |  验证Prefetch请求发送 |
| TC09 | test_api_fetch_request_generates_acquire |  验证Fetch请求生成Acquire |
| TC10 | test_api_full_fetch_flow |  验证完整Fetch流程 |
| TC11 | test_api_grant_with_corruption |  验证Grant数据损坏处理 |
| TC12 | test_api_full_prefetch_flow |  验证完整Prefetch流程 |
| TC13 | test_FIFO_moudle |  验证FIFO模块综合功能 |
| TC14 | test_mshr_hit_detection |  验证MSHR命中检测 |
| TC15 | test_mshr_release_after_grant |  验证MSHR释放 |
| TC16 | test_low_index_priority_fetch |  验证Fetch MSHR低索引优先级 |
| TC17 | test_low_index_priority_prefetch |  验证Prefetch MSHR低索引优先级 |
| TC18 | test_fifo_priority_ordering |  验证FIFO优先级顺序 |
| TC19 | test_acquire_arbitration_priority |  验证Acquire仲裁优先级 |
| TC20 | test_grant_beat_collection |  验证Grant多Beat数据收集 |
| TC21 | test_victim_way_update |  验证Victim Way更新 |
| TC22 | test_waymask_generation |  验证Waymask生成 |
| TC23 | test_sram_write_conditions |  验证SRAM写回条件 |
| TC24 | test_no_write_with_flush_fencei |  验证Flush/Fencei写回抑制 |
| TC25 | test_flush_fencei_mshr_behavior |  验证Flush/Fencei MSHR行为 |
| TC26 | test_prefetch_same_address_as_fetch |  验证相同地址处理 |
| TC27 | test_demux_chosen_signal |  验证Demux选择信号 |
| TC28 | test_trigger_priorityFIFO_enq_assert |  验证Priority FIFO入队断言 |
| TC29 | test_trigger_priorityFIFO_deq_assert |  验证Priority FIFO出队断言 |

### 5.2 测试数据
- **固定测试向量**：使用预定义的测试地址确保测试的可重复性
- **边界值测试**：包含满队列、空队列等边界条件测试
- **异常情况测试**：包含异常情况测试
- **递增地址模式**：使用地址递增模式生成测试数据

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
missunit/
├── test/
│   ├── missunit_test.py          # 主测试文件
│   └── missunit_fixture.py       # 测试fixture
├── env/
│   ├── missunit_env.py           # 测试环境
│   └── missunit_functionalcoverage.py  # 功能覆盖率
├── agent/
│   └── missunit_agent.py         # 测试api
└── bundle/
    └── missunit_bundle.py        # bundle定义
```

## 7. 测试结果分析

### 7.1 测试通过率
- **总测试用例数**：29
- **通过用例数**：29
- **失败用例数**：0
- **通过率**：100%

### 7.2 覆盖率分析

#### 7.2.1 行覆盖率
- **总体覆盖率**：96.5% (1479/1532行)
- **ICacheMissUnit.v**：91.2% (104/114行)
- **ICacheMissUnit_top.sv**：86.8% (264/304行)

#### 7.2.2 功能覆盖率
- **总体功能覆盖率**：100%
- **覆盖点总数**：29
- **已覆盖点数**：29
- **覆盖组数量**：11

### 7.3 覆盖率详细分析
功能覆盖率达到100%，说明所有定义的功能点都被充分测试。行覆盖率96.5%属于较高水平，未覆盖的3.5%主要集中在：
- 错误处理分支
- 极端异常情况
- 部分初始化代码路径

##### 替换策略覆盖（CP36）

| 覆盖点 | 功能描述 | 覆盖状态 |
|--------|----------|----------|
| CP36.1 | Acquire成功时更新victim | ✓ 已覆盖 |

##### SRAM写回覆盖（CP37）

| 覆盖点 | 功能描述 | 覆盖状态 |
|--------|----------|----------|
| CP37.1 | 正常SRAM写入 | ✓ 已覆盖 |
| CP37.2 | Flush/Fencei时不写SRAM | ✓ 已覆盖 |
| CP37.3 | Fetch响应总是生成 | ✓ 已覆盖 |
| CP37.4 | Corrupt数据响应 | ✓ 已覆盖 |

##### Miss完成覆盖（CP38）

| 覆盖点 | 功能描述 | 覆盖状态 |
|--------|----------|----------|
| CP38.1 | 正常Miss完成响应 | ✓ 已覆盖 |

##### 异常处理覆盖（CP39）

| 覆盖点 | 功能描述 | 覆盖状态 |
|--------|----------|----------|
| CP39.1 | MSHR未发射前fencei | ✓ 已覆盖 |
| CP39.2 | MSHR未发射前flush | ✓ 已覆盖 |
| CP39.3 | MSHR已发射后flush/fencei | ✓ 已覆盖 |

#### 8.2.3 覆盖率统计总结

- **总覆盖点数**: 31个
- **已覆盖数**: 31个
- **功能覆盖率**: 100%
- **关键功能覆盖**: 100%
- **边界条件覆盖**: 100%
- **异常处理覆盖**: 100%

---

## 8. 缺陷分析

### 8.1 发现缺陷
测试过程中未发现功能性缺陷，所有测试用例均通过。

### 8.2 潜在风险点
- ICacheMissUnit_top.sv的覆盖率相对较低(86.8%)，建议增加针对顶层模块的测试
- 部分边界条件可能需要更多测试用例

## 9. 测试结论

### 9.1 验证完成度
- √ 所有规划的功能点均已验证
- √ 功能覆盖率达到100%
- √ 行覆盖率达到96.5%，满足验证要求
- √ 所有测试用例通过

### 9.2 模块质量评估
ICacheMissUnit模块验证充分，功能实现正确，质量良好。模块在各种测试场景下表现稳定，满足设计要求。

### 9.3 改进需求
1. 需要增加对ICacheMissUnit_top.sv顶层模块的测试覆盖

### 9.4 验证结论
**ICacheMissUnit模块验证通过**，可以进入下一阶段的集成验证。