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
### 3.1 入队操作 (CP28)
MissUnit 内部的 priorityFIFO 负责缓存预取 MSHR 的编号，本功能点覆盖 FIFO 入队路径的各种状态。
- 功能点CP28.1 队未满，正常入队：当队列未满、`io.enq.ready=1` 且 `io.enq.valid=1` 时可以顺利入队，指针 `enq_ptr.value` 顺序递增且 `enq_ptr.flag` 保持不翻转。
- 功能点CP28.2 队未满，入队后标记位翻转：当入队指针位于队尾（索引 9）时再次入队，`enq_ptr.value` 回绕为 0 且 `enq_ptr.flag` 翻转，实现环形 FIFO。
- 功能点CP28.3 队满，入队就绪信号为低，无法入队：当 `(enq_ptr.value == deq_ptr.value) && (enq_ptr.flag ^ deq_ptr.flag)` 为真时视为队满，`io.enq.ready=0` 阻止新的请求，`enq_ptr` 保持不变。
- 测试用例：TC13 test_FIFO_moudle - 依次送入 10 条请求确认正常入队及指针累加，并通过第 11 条请求观察就绪信号拉低、指针保持不变。

### 3.2 出队操作 (CP29)
该功能点验证 priorityFIFO 的出队语义以及环形指针的正确性。
- 功能点CP29.1 队非空，正常出队：当 FIFO 有效且 `io.deq.ready=1` 时，`io.deq.fire` 触发数据吐出，`deq_ptr.value` 顺序递增。
- 功能点CP29.2 队非空，出队后标记位翻转：当 `deq_ptr.value` 为 9 时出队，指针回绕至 0 并翻转 `deq_ptr.flag`。
- 功能点CP29.3 队空，出队有效信号为低：当 `enq_ptr` 与 `deq_ptr` 完全一致时视为队空，`io.deq.valid=0`，出队握手被禁止。
- 测试用例：TC13 test_FIFO_moudle - 先填满再逐条出队查看指针递增与回绕；TC18 test_fifo_priority_ordering - 在全部元素出队后确认队空时 valid 维持低电平。

### 3.3 刷新清空操作（CP30）
flush 信号应即时清空 priorityFIFO 的读写指针和标志位，保证刷新后队列重新可用。
- 功能点CP30.1 flush 清空：当 `io.flush=1` 时，将 `enq_ptr.value`、`deq_ptr.value`、`flag` 全部复位为 0，同时 `empty=1`、`full=0`。
- 测试用例：TC05 test_set_flush - 直接驱动 flush 信号验证指针复位；TC13 test_FIFO_moudle - 在 FIFO 填满后施加 flush，确认队列恢复初始状态并可再次入队。

### 3.4 处理取指缺失请求 （CP31）
MissUnit 需要接收来自取指端的缺失请求、区分新旧 miss，并按照低索引优先策略分配 fetch MSHR。
- 功能点CP31.1 接受新的取指请求：当 `io.fetch.req.valid=1` 且 `fetchHit=0` 时，`io.fetch.req.ready=1` 并将请求送入空闲 fetch MSHR。
- 功能点CP31.2 处理已有的取指请求：当同地址 miss 再次到来时 `fetchHit=1`，`fetchDemux.io.in.valid` 保持 0，表示命中已有 MSHR 并阻止再次分配。
- 功能点CP31.3 低索引优先进入 MSHR：fetchDemux 以编号 0→3 的顺序寻找空位，优先分配低索引 fetch MSHR。
- 测试用例：TC07 test_send_fetch_request - 发送不同地址 miss 验证新请求被接收；TC14 test_mshr_hit_detection - 驱动重复地址确认命中判定；TC16 test_low_index_priority_fetch - 连续 miss 观察低索引 MSHR 依次被占用。

### 3.5 处理预取缺失请求 （CP32）
预取命中与分配策略与取指通路类似，同时增加 FIFO 排队行为。
- 功能点CP32.1 接受新的预取请求：当 `io.prefetch_req.valid=1` 且 `prefetchHit=0` 时，`io.prefetch_req.ready=1` 并写入空闲 prefetch MSHR。
- 功能点CP32.2 处理已有的预取请求：命中已有 MSHR 时 `prefetchHit=1`，请求被吸收但不再下发新的分配。
- 功能点CP32.3 低索引优先进入 MSHR：prefetchDemux 按索引 0→9 分配空闲 MSHR，优先占用低编号。
- 功能点CP32.4 先进入 MSHR 的优先进入 prefetchArb：预取 MSHR 的编号按入队顺序写入 priorityFIFO，出队顺序与入队一致，保证仲裁 FIFO 语义。
- 测试用例：TC08 test_send_prefetch_request - 检查新 miss 被接收；TC14 test_mshr_hit_detection - 复用 fetch miss 建立的 MSHR 观察命中；TC17 test_low_index_priority_prefetch - 验证低索引优先；TC18 test_fifo_priority_ordering - 验证 FIFO 先入先出。

### 3.6 MSHR 管理与查找 (CP33)
该功能点覆盖 MSHR 查找命中、资源释放及取指/预取共享命中等场景。
- 功能点CP33.1 MSHR 查找命中逻辑：新的 fetch/prefetch 请求能够遍历全部 MSHR，并在命中时拉高 `fetchHit` 或 `prefetchHit`。
- 功能点CP33.2 MSHR 状态的更新与释放：Grant 流程完成后，对应 MSHR 有效位被清零，`io.req.ready` 恢复为 1，允许接收后续 miss。
- 功能点CP33.3 Prefetch 与 fetch 地址相同时命中：当预取与取指请求地址一致且 fetch valid 时，`prefetchHit` 仍置 1，避免重复 miss。
- 功能点CP33.4 新请求未命中任何 MSHR：当查找未命中已有 miss 时，`fetchHit`/`prefetchHit` 均为 0，以便分配新槽。
- 测试用例：TC14 test_mshr_hit_detection - 覆盖命中与未命中分支；TC15 test_mshr_release_after_grant - 验证 Grant 完成后的 MSHR 释放；TC26 test_prefetch_same_address_as_fetch - 观测预取与取指同地址命中；TC07/TC08 - 验证首次 miss 时命中标志为 0。

### 3.7 acquireArb 仲裁 (CP34)
acquireArb 负责在 fetch 与 prefetch MSHR 之间进行固定优先级仲裁。
- 功能点CP34.1 acquireArb 仲裁：当 fetch 与 prefetch 同时请求时，acquireArb 优先输出源 ID < 4 的 fetch 请求。
- 功能点CP34.2 只有 prefetch 请求时被选中：当所有 fetch MSHR 空闲或无请求时，pre-fetch MSHR 的 acquire 可以被仲裁并送出。
- 测试用例：TC19 test_acquire_arbitration_priority - 先触发预取再触发取指，记录仲裁顺序并确认 fetch 优先；同用例中在 fetch 完成后验证预取请求最终被送出。

### 3.8 Grant 数据接收与 Refill (CP35)
MissUnit 必须正确收集 TileLink Grant 的多拍数据并根据 last_fire 状态完成 refill。
- 功能点CP35.1/CP35.2 正常完整 Grant 流程：在连续两个 beat 的 Grant 中，`readBeatCnt` 递增、`respDataReg` 收集数据，最后一个 beat 置 `last_fire=1`，下一拍 `last_fire_r=1`。
- 功能点CP35.3 Grant 完成后释放 MSHR：`last_fire_r=1` 时，根据 `grant.bits.source` 无效化对应 MSHR。
- 功能点CP35.4 Grant 带有 corrupt 标志：当 `grant.bits.corrupt=1` 时，模块记录 `corrupt_r`，后续响应携带污染标志。
- 测试用例：TC20 test_grant_beat_collection - 手动逐拍驱动 Grant 检查 beat 累计与 last_fire；TC10 test_api_full_fetch_flow - 完整 miss 流程中验证 last_fire_r 与 MSHR 释放；TC11 test_api_grant_with_corruption - 检查 corrupt 标志传递。

### 3.9 替换策略更新 (CP36)
当 acquire 成功发送时需要通知替换策略更新被淘汰的路，同时在响应阶段生成 waymask。
- 功能点CP36.1 正常替换更新：当 `io.mem.acquire.fire` 成功时，`io.victim.vSetIdx.valid` 拉高并输出正在替换的集合索引。
- 功能点CP36.2 生成 waymask：在 Grant 完成后，根据 L2 返回的 `mshr_resp.bits.way` 生成独热 `waymask`，用于 SRAM 写回与响应。
- 测试用例：TC21 test_victim_way_update - 在 acquire fire 时读取 victim 接口确认 valid 与 bits；TC22 test_waymask_generation - 通过设置不同 victim way 并完成 Grant，检查响应中的 waymask。

### 3.10 写回 SRAM (CP37)
当 miss refill 完整返回时，需要根据刷新/腐化状态决定是否写回 meta/data SRAM。
- 功能点CP37.1 生成写使能：在 `last_fire_r=1` 且无 flush/fencei/corrupt 条件下，`io.meta_write.valid` 与 `io.data_write.valid` 同时拉高。
- 功能点CP37.2 正常写入内容：写口携带的 virIdx、phyTag、data、waymask 等字段与 MSHR 记录一致。
- 功能点CP37.3 有 flush/fencei 时不写 SRAM：当 flush 或 fencei 有效时，即使数据返回也保持写 SRAM 使能为 0。
- 功能点CP37.4 处理 corrupt 数据：当 `corrupt_r=1` 时禁止写 SRAM，但依旧产生 fetch 响应并将 corrupt 标志向外传播。
- 测试用例：TC23 test_sram_write_conditions - 验证正常写回路径；TC24 test_no_write_with_flush_fencei - 在 flush/fencei 或 corrupt 条件下确认写使能抑制且返回带有 corrupt 标志。

### 3.11 向 mainPipe/prefetchPipe 发出 Miss 完成响应（CP38）
MissUnit 在 Grant 完成后一拍需要向取指前端返回 miss 完成信息。
- 功能点CP38.1 正常 Miss 完成响应：当 `last_fire_r=1` 时，`io.fetch_resp.valid=1`，并输出 blkPaddr、vSetIdx、waymask、data、corrupt 等字段。
- 测试用例：TC10 test_api_full_fetch_flow - 完整 miss 流程中检查 fetch_resp 的内容；TC11 test_api_grant_with_corruption - 验证响应携带 corrupt 标志并仍然有效；TC23 test_sram_write_conditions - 在正常写回场景中确认 fetch_resp 数据与写回字段一致。

### 3.12 处理 flush / fencei (CP39)
Flush/Fencei 需要同时作用于未发射与已发射的 miss，确保刷新语义正确。
- 功能点CP39.1 MSHR 未发射前 fencei：当 `io.fencei=1` 时，fetch/prefetch MSHR 的 `io.req.ready` 与 `io.acquire.valid` 均被拉低，未发射请求被取消。
- 功能点CP39.2 MSHR 未发射前 flush：`io.flush` 仅阻塞 prefetch MSHR（fetch MSHR 的 flush 恒为 0），此时预取请求 ready 拉低而取指通路仍可发射。
- 功能点CP39.3 MSHR 已发射后 flush/fencei：当请求已发射且收到刷新信号时，不再写 SRAM，但仍保持 fetch 响应有效。
- 测试用例：TC04 test_fencei_work - 在 fencei 拉高时检查所有 MSHR ready/valid 被清空；TC25 test_flush_fencei_mshr_behavior - 对 flush 与 fencei 分别验证取指/预取通路的阻断范围；TC24 test_no_write_with_flush_fencei - 在数据返回时施加刷新，确认写回抑制但响应仍产生。

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
