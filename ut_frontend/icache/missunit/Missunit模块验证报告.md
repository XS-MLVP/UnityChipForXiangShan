# MissUnit模块验证报告

## 1. 基本信息

| 项目 | 内容 |
|------|------|
| 验证对象 | ICache MissUnit 模块 |
| 验证人员 | Gui-Yue |
| 验证时间 | 2025-11 |
| 报告版本 | V0.2 |
| 验证框架 | Toffee 测试框架 |

## 2. 验证对象介绍

### 2.1 模块概述
MissUnit 位于香山前端 ICache 的 miss 处理管线，其职责是接收取指和预取 miss，请求下行 TileLink 层获得 cache line，并将回填结果写入 data/meta 阵列。模块内部同时维护 4 个取指 MSHR、10 个预取 MSHR 以及一个带优先级的 FIFO，以保证 fetch/prefetch miss 可以并行处理、避免重复 miss，并与 victim 选择及 cache 写回流程配合。

### 2.2 主要功能
- **Fetch miss 管理**：对 `io.fetch.req` 进行命中判定、队列分发与 MSHR 分配，命中时直接回送 ready，未命中则生成 Acquire。
- **Prefetch miss 管理**：维护预取专用 MSHR，并通过 priority FIFO 与 Acquire 仲裁器交互，保证预取请求顺序。
- **MSHR 查找与合并**：14 路 MSHR 均支持根据 `blkPaddr/vSetIdx` 做 hit 检查，避免重复请求并提供 victim way 信息。
- **Acquire/Grant 协作**：5 路仲裁器将 fetch 与 prefetch 的 Acquire 合并发送，同时在 Grant 返回后将数据拼成 512-bit 响应，回写 meta/data，并驱动 difftest。
- **替换/写回接口**：对外输出 `io.victim`, `io.meta_write`, `io.data_write`，并与 flush/fencei 控制联动，保证异常处理时能清空状态。

### 2.3 接口信号

#### 2.3.1 时钟复位
- `clock`, `reset`

#### 2.3.2 `io` 顶层接口

| 子接口 | 握手/方向 | 字段说明 |
|--------|-----------|----------|
| `io.fencei` | in | FenceI 控制，高电平时阻断新 miss 并禁止写阵列。 |
| `io.flush` | in | Flush 控制，仅作用于预取路径。 |
| `io.hartId` | in | Hart ID，随 difftest 输出。 |
| `io.fetch.req` | ready/valid（输入） | `blkPaddr[41:0]`, `vSetIdx[7:0]` |
| `io.fetch.resp` | ready/valid（输出） | `blkPaddr`, `vSetIdx`, `waymask[3:0]`, `data[511:0]`, `corrupt` |
| `io.prefetch_req` | ready/valid（输入） | 字段同 fetch req |
| `io.victim.vSetIdx` | valid/bits（输出） | MissUnit 对外报告的 victim 虚拟集合 |
| `io.victim.way` | out | Victim way 选择 |
| `io.mem.acquire` | ready/valid（输出） | `source[3:0]`, `address[47:0]` |
| `io.mem.grant` | valid（输入） | `opcode[3:0]`, `size[2:0]`, `source[3:0]`, `data[255:0]`, `corrupt`（两拍合成 512-bit） |
| `io.meta_write` | valid（输出） | `virIdx[7:0]`, `phyTag[35:0]`, `waymask[3:0]`, `bankIdx` |
| `io.data_write` | valid（输出） | `virIdx[7:0]`, `data[511:0]`, `waymask[3:0]` |

#### 2.3.3 `ICacheMissUnit_` 调试层级

`bundle.ICacheMissUnit_` 公开了内部结构，便于白盒验证：

- `_prefetchMSHRs._0 ... _9._io`：每个预取 MSHR 的端口，包括 `_req_ready`、`_acquire_valid`、`_invalid`、`_lookUps_0._hit`、`_lookUps_1._hit`、`_resp_bits.{_blkPaddr,_vSetIdx,_way}` 等信号。
- `_fetchMSHRs._0 ... _3._io`：与预取 MSHR 相同的观测点。
- Prefetch priority FIFO：在同层级下，可读取 `enq_ptr_value/flag`、`deq_ptr_value/flag`、`full`、`io_enq_ready`、`io_deq_ready` 以及 `_prefetchDemux_io_chosen`，用于 FIFO 行为检查。

## 3. 验证功能点

### 3.1 基础控制与 API（非 CP）

1. **Bundle / Agent API 连通性**
   - 场景：直接操作 `ICacheMissUnitBundle` 的 fetch 请求、`fencei` 信号，确认写入后一个周期即可从 bundle 读回。
   - 检查：`io.fetch.req.valid`, `io.fetch.req.bits.blkPaddr`, `io.fencei` 等寄存器能在 step 后保持设置值。
   - 用例：TC02 `test_bundle_drive_fetch_req_inputs`。

2. **Flush / FenceI 快速冒烟测试**
   - 场景：通过 Agent 拉高 `fencei`，等待 10 个周期，再次拉低。
   - 检查：冒烟测试期间不存在断言或仿真崩溃；用于快速确认仿真初始化正确。
   - 用例：TC01 `test_smoke`。

3. **Victim/Flush API 设置**
   - 场景：使用 Agent API 轮流设置 `io.flush`、四种 `victim_way`，并在 bundle 中回读。
   - 检查：Flush 拉高时 `bundle.io._flush` = 1，victim_way 依次为 0~3。
   - 用例：TC04 `test_set_flush`、TC05 `test_set_victim_way`。

4. **Fetch / Prefetch API 测试流**
   - 场景：`drive_send_fetch_request` / `drive_send_prefetch_req` 在队列空/满、重复 miss 等场合多次调用。
   - 检查：`send_success`、`bundle.io._fetch._req._ready` 的状态切换；prefetch 第 11 次请求被阻塞再放行。
   - 用例：TC06 `test_send_fetch_request`、TC10 `test_send_prefetch_request`。

5. **Acquire / Grant 全流程**
   - 场景：发送 miss -> 捕获 `io.mem.acquire` -> 拉高 ready 完成握手 -> 模拟 Grant -> 等待 fetch_resp。
   - 检查：Acquire 地址 `blkPaddr << 6`、source ID、Victim 路设置与对应的独热编码 `waymask`；Grant 分两拍写入，`corrupt` 标志在响应链路中保持一致。
   - 用例：TC07 `test_api_fetch_request_generates_acquire`, TC08 `test_api_full_fetch_flow`, TC09 `test_api_grant_with_corruption`, TC11 `test_api_full_prefetch_flow`.

### 3.2 Priority FIFO 功能（CP28～CP30）

**CP28 入队行为**  
测试用例：TC12 `test_FIFO_moudle_CP28_CP29_enq_and_deq_operation`  
- CP28.1 队未满正常入队：一次性注入 9 个预取 miss，`enq_ptr_value` 逐项累加、`enq_ready=1`，说明 FIFO 在有空位时可以连续握手。  
- CP28.2 入队后指针翻转：当写指针指向 9 时再次入队，观测 `enq_ptr_value` 回到 0、`enq_ptr_flag` 翻转、`full` 置 1。  
- CP28.3 队满无法入队：继续发送请求，`io.prefetch_req.ready` 与 `priorityFIFO.io_enq_ready` 均为 0，API 返回 `send_success=False`。

**CP29 出队行为**  
测试用例：TC12 `test_FIFO_moudle_CP28_CP29_enq_and_deq_operation`  
- CP29.1 正常出队：拉高 `io.mem.acquire.ready` 触发 acquireArb，`deq_ptr_value` 依次递增。  
- CP29.2 出队后指针翻转：当 `deq_ptr_value` 为 9 时再出队，指针回到 0 且 `deq_ptr_flag` 翻转。  
- CP29.3 队空阻塞：FIFO 被完全取走后，`deq_valid=0`、`priorityFIFO.io_deq_ready=0`，额外出队不会改变指针。

**CP30 Flush 行为**  
测试用例：TC13 `test_FIFO_moudle_CP30_flush_operation`  
- 拉高 `io.flush` 时，`enq_ptr`、`deq_ptr` 以及 flag 均复位，`full=0`、`enq_ready=1`。Flush 后重新发起预取请求，队列能再次入队，证明状态确实被清空。

### 3.3 Miss pipeline 功能（CP31～CP39）

**CP31 处理取指缺失**  
测试用例：TC14 `test_MISSUNIT_CP31_fetch_miss_process`  
- CP31.1 新 miss 进入：当 `fetchHit=0`、`io.fetch.req.valid=1` 时，`io.fetch.req.ready=1` 并通过 `fetchDemux` 分发到最低索引的空闲 MSHR。  
- CP31.2 命中已有 miss：再次发送相同地址，`fetchHit=1`，`fetchDemux.io.in.valid=0` 但 `ready` 仍为 1，实现“表面接收、实际不入队”。  
- CP31.3 低索引优先：同一周期多个 miss 时，`fetchDemux.io.chosen` 总是选择编号最小的空闲 MSHR。

**CP32 处理预取缺失**  
测试用例：TC15 `test_MISSUNIT_CP32_prefetch_miss_process`  
- CP32.1 新预取 miss 入队：`prefetchHit=0` 时 `prefetchDemux` 将请求写入第一个空闲的 prefetch MSHR，同时将索引放入 priority FIFO。  
- CP32.2 命中已有预取：再次发送同址请求，`prefetchHit=1`，`prefetchDemux` 不再 握手，但 `io.prefetch.req.ready=1`。  
- CP32.3 低索引优先：多条预取 miss 同到时，`prefetchDemux.io.chosen` 总是最小空闲索引。  
- CP32.4 FIFO 顺序：结合 TC12/TC13 观察 `prefetchArb` 的 出队 顺序与 priority FIFO 入队顺序一致。

**CP33 MSHR 管理与查找**  
测试用例：TC16 `test_MISSUNIT_CP33_MSHR_manage`、TC23 `test_MISSUNIT_addational_all_mshr_lookup_coverage`  
- CP33.1 Fetch 查找命中：通过内部信号确认 fetch lookUp 判定 `fetchHit`。  
- CP33.2 Prefetch 查找命中：同理验证 prefetch lookUp。  
- CP33.3 Prefetch 与 Fetch 同址：`test_MISSUNIT_addational_all_mshr_lookup_coverage` 构造 fetch/prefetch 同地址，`prefetchHit` 仍会被置高。  
- CP33.4 MSHR 释放：Grant 返回后，对应 MSHR 的 `valid` 拉低，腾出入口。

**CP34 Acquire 仲裁**  
测试用例：TC18 `test_MISSUNIT_CP34_acquireArb_arbitration`  
- 构造 fetch 与 prefetch 同时有 acquire，`acquireArb.io.out` 优先选择 fetch (source 0~3)，仅在 fetch 空闲时才向 prefetch 的 source(4~13) 放行。

**CP35 Grant / Refill**  
测试用例：TC19 `test_MISSUNIT_CP35_grant_accept_and_refill`、TC09 `test_api_grant_with_corruption`  
- CP35.1 第 1 beat：`io.mem_grant.valid=1` 时，数据写入 `respDataReg_0`，`readBeatCnt` 从 0 -> 1。  
- CP35.2 第 2 beat：继续 握手，数据写入 `respDataReg_1`，`readBeatCnt` 回到 0，`last_fire` 置 1。  
- CP35.3 MSHR 失效：`last_fire_r=1` 后，根据 source ID 拉高对应 MSHR 的 `io.invalid`。  
- CP35.4 带 `corrupt` 的 Grant：在第二个 beat 设置 `corrupt=1`，`corrupt_r` 拉高并反映到 fetch_resp；若下一次 Grant 正常，该标志被清零。

**CP36 替换策略更新**  
测试用例：TC20 `test_MISSUNIT_CP36_Replacer`、TC08 `test_api_full_fetch_flow`  
- CP36.1 Acquire 时更新 vSetIdx：当 `io.mem.acquire.ready` 与仲裁输出握手时，`io.victim.vSetIdx.valid=1` 且值等于该 miss 的虚拟集合号。  
- CP36.2 Waymask 生成：Grant 完成后，`response["waymask"]` 等于 `1 << victim_way`，同时内部 `mshr_resp_way` 与期望一致。

**CP37 SRAM 写回**  
测试用例：TC21 `test_MISSUNIT_CP37_SRAM_writeback`  
- CP37.1 正常写回：没有 flush/fencei 且 `corrupt_r=0` 时，`io.meta_write.valid`、`io.data_write.valid` 均为 1，字段内容与 MSHR 记录匹配。  
- CP37.2 有 flush/fencei 或 corrupt：在 flush/fencei 拉高或 Grant 标记 `corrupt` 的场景中，写回有效信号保持 0。

**CP38 Miss Completion**  
测试用例：TC22 `test_MISSUNIT_CP38_mainpipe_iprefetchpipe_response`  
- Grant 全部返回后，无论 flush/fencei 是否发生，`io.fetch_resp.valid=1`，并将 `blkPaddr/vSetIdx/waymask/data/corrupt` 正确送回 mainpipe/预取管线。

**CP39 Flush/FenceI 处理**  
测试用例：TC03 `test_fencei_work`、TC04 `test_set_flush`、TC23 `test_MISSUNIT_CP39_flush_fencei_operation`  
- CP39.1 fencei 在发射前：拉高 fencei 时，所有 MSHR 的 `io.req.ready` 与 `io.acquire.valid` 变低，新的 miss 不再发射。  
- CP39.2 flush 在发射前：flush 只影响 prefetch MSHR，拉高时仅允许 fetch 请求继续发射。  
- CP39.3 已发射后的 flush/fencei：当请求已经发出，再出现 flush/fencei 时，Grant 数据仍需接收但不写 SRAM；`io.fetch_resp.valid` 仍会如期拉高。

综上，所有 CP 功能点均在测试集中得到覆盖，且每个场景明确对应的 Toffee 用例可复现。

## 4. 验证方案

### 4.1 验证目标
- 覆盖 fetch/prefetch miss 的全链路控制与数据路径。
- 证明 priority FIFO、MSHR 查找、Arbiter、Replacer 在所有 CP（31~39）下行为正确。
- 验证 API 层能够驱动/观测关键信号，便于系统集成。
- 收集足够的行覆盖率与功能覆盖率，确保各类边界场景（flush/fencei、corrupt、FIFO 指针回绕）被触发。

### 4.2 验证环境
- **DUT**：`DUTICacheMissUnit`
- **环境类**：`ICacheMissUnitEnv`
- **Agent**：`ICacheMissUnitAgent`（提供 fetch/prefetch/acquire/grant API）
- **Bundle**：`ICacheMissUnitBundle`
- **仿真器**：Verilator + Toffee runtime

### 4.3 覆盖率策略
- **代码覆盖**：基于 Verilator LCOV，目标文件包括 `ICacheMissUnit.v`、`ICacheMissUnit_top.sv` 以及 10+ MSHR/Mux 组件，统计 line/toggle/branch/expression。
- **功能覆盖**：在 `missunit_coverage.py` 中定义 4 组覆盖（Basic/FIFO/Main/Timing），共 19 个覆盖点、40 个 bin，覆盖 API 控制、FIFO 事件、MSHR/Arbiter/Grant/Flush 时序。
- **断言覆盖**：继承 RTL 中 `assert` 语句，对 FIFO handshake、refill `last_fire` 等关键条件进行运行时校验。

## 5. 测试用例

### 5.1 用例列表

| 序号 | 用例名称 | 目标 |
|------|---------|------|
| TC01 | test_smoke | 基础 fencei 触发冒烟测试 |
| TC02 | test_bundle_drive_fetch_req_inputs | 验证 bundle 可写 fetch_req/fencei |
| TC03 | test_fencei_work | 确认 fencei 清空所有 MSHR |
| TC04 | test_set_flush | flush API 高低电平切换 |
| TC05 | test_set_victim_way | victim way 编程覆盖四路 |
| TC06 | test_send_fetch_request | fetch_req 发起与 ready 行为 |
| TC07 | test_api_fetch_request_generates_acquire | fetch miss 触发 Acquire |
| TC08 | test_api_full_fetch_flow | Fetch miss 全流程（victim、Grant、response） |
| TC09 | test_api_grant_with_corruption | Grant 携带 `corrupt` 标志的传递 |
| TC10 | test_send_prefetch_request | 预取 miss 配额与重复请求 |
| TC11 | test_api_full_prefetch_flow | Prefetch miss 全流程 |
| TC12 | test_FIFO_moudle_CP28_CP29_enq_and_deq_operation | FIFO 入/出队及指针翻转 |
| TC13 | test_FIFO_moudle_CP30_flush_operation | FIFO flush 行为 |
| TC14 | test_MISSUNIT_CP31_fetch_miss_process | Fetch miss 分类与命中 |
| TC15 | test_MISSUNIT_CP32_prefetch_miss_process | Prefetch miss 分类与命中 |
| TC16 | test_MISSUNIT_CP33_MSHR_manage | 14 路 MSHR 查找逻辑 |
| TC17 | test_MISSUNIT_addational_all_mshr_lookup_coverage | 极端查找组合补充 |
| TC18 | test_MISSUNIT_CP34_acquireArb_arbitration | Acquire 仲裁及 source ID |
| TC19 | test_MISSUNIT_CP35_grant_accept_and_refill | Grant 数据节拍收集与 last_fire 判定 |
| TC20 | test_MISSUNIT_CP36_Replacer | Victim 路/waymask 更新 |
| TC21 | test_MISSUNIT_CP37_SRAM_writeback | SRAM 写/flush/corrupt 路径 |
| TC22 | test_MISSUNIT_CP38_mainpipe_iprefetchpipe_response | miss completion 响应 |
| TC23 | test_MISSUNIT_CP39_flush_fencei_operation | Flush/FenceI 在不同阶段动作 |

### 5.2 测试数据
- **固定向量与序列**：地址、集合索引用固定步长生成，便于复现。
- **并发交互**：Acquire/Grant/Prefetch 等接口使用 Toffee 的多协程等待，确保握手次序可控。
- **特殊场景**：Grant corrupt、flush/fencei 插入、MSHR hit/miss 全组合。

## 6. 测试环境

### 6.1 硬件/软件
- 仿真：Verilator 5.038
- 主机：x86_64 Linux
- Python 3.10 + Toffee + pytest-asyncio

### 6.2 目录结构
```
missunit/
├── agent/                # ICacheMissUnitAgent，封装 API
├── bundle/               # ICacheMissUnitBundle 结构
├── env/                  # Env、功能覆盖定义
├── test/                 # missunit_test.py 及 fixture
└── Missunit模块验证报告.md
```

## 7. 测试结果分析

### 7.1 通过率
- **总用例数**：23
- **通过**：23
- **失败**：0
- **通过率**：100%

### 7.2 覆盖率

#### 7.2.1 代码覆盖
- **行覆盖**：83.86%（1335/1592）
- **Toggle 覆盖**：84.80%（8006/9441）
- **分支覆盖**：89.31%（259/290）
- **表达式覆盖**：97.01%（324/334）
- **关键文件**：
  - `ICacheMissUnit.v`：80.34%（94/117），未覆盖的部分集中在assert以及reset状态
  - `ICacheMSHR_*`, `MuxBundle`, `FIFOReg` 等辅助模块都完成覆盖，未覆盖的部分集中在reset状态。

#### 7.2.2 功能覆盖
- **覆盖组**：4 组（Basic / FIFO / Main / Timing）
- **覆盖点**：19
- **Bins**：40
- **覆盖率**：100%（所有 once/hinted bin 均触发）
- **亮点**：CP33 的 4 类 MSHR hit/merge、CP37 SRAM 写回、CP39 flush/fencei 前后时序 均有对应例程触发。

### 7.3 结果解读
- 行覆盖低于 90% 的部分集中在顶层 wrapper 与某些异常分支（如 `refill_done` 断言失败路径）。这些路径需要特制用例（例如强制 TL 错误）才能覆盖。
- 功能覆盖完整说明规划的 MissUnit CP 已全部执行，特别是 priority FIFO 与 flush/fencei 时序，覆盖点统计已确认 40 个 bin 全命中。

## 8. 缺陷与风险
- 本轮测试未发现功能性缺陷。
- 风险点：
  1. `ICacheMissUnit_top.sv` 覆盖率较低，建议在系统级压测中插入额外的 DPI/monitor 流程以覆盖剩余路径。
  2. 未针对 TL 错误、Grant 超时等极端情形编写测试，可能遗漏异常恢复路径。

## 9. 结论
- √ 规划的功能点全部验证，功能覆盖率 100%。
- √ 23 个用例全部通过，API/FIFO/MSHR/时序场景均被覆盖。

综合结论：**MissUnit 模块当前验证结果通过**，满足集成验证准入条件，可进入下一阶段测试。
