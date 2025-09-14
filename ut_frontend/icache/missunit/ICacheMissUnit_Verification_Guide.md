# ICacheMissUnit 验证环境开发文档

## 概述

本文档介绍基于Toffee验证框架搭建的ICacheMissUnit（指令缓存缺失处理单元）验证环境，包括RTL设计分析、Bundle接口、Agent接口、测试用例和功能覆盖点的详细说明。

## 目录结构

```
ut_frontend/icache/missunit/
├── agent/
│   ├── __init__.py
│   └── missunit_agent.py          # Agent接口实现
├── bundle/
│   ├── __init__.py
│   └── missunit_bundle.py         # Bundle接口定义
├── env/
│   ├── __init__.py
│   ├── missunit_coverage.py       # 功能覆盖点定义
│   └── missunit_env.py            # 验证环境
└── test/
    ├── __init__.py
    ├── missunit_fixture.py        # 测试夹具
    └── missunit_test.py           # 测试用例
```

## RTL设计分析

### 硬件架构概述

ICacheMissUnit是XiangShan处理器中负责处理指令缓存缺失的关键模块，主要功能包括：

1. **MSHR管理**：管理14个MSHR（Miss Status Holding Register）
   - 4个fetchMSHR（ID: 0-3）：处理取指缺失
   - 10个prefetchMSHR（ID: 4-13）：处理预取缺失

2. **请求仲裁**：
   - fetchArb：fetch请求间的仲裁
   - prefetchArb：prefetch请求间的仲裁  
   - acquireArb：acquire请求间的仲裁（fetch优先于prefetch）

3. **TileLink协议**：
   - Acquire：向下级发送缺失请求
   - Grant：接收下级返回的数据

4. **数据处理**：
   - Grant数据收集（支持multi-beat传输）
   - SRAM写回控制
   - 替换策略更新

### 关键信号接口

```verilog
module ICacheMissUnit (
    // 取指请求接口
    input         io_fetch_req_valid,
    output        io_fetch_req_ready,
    input  [41:0] io_fetch_req_bits_blkPaddr,
    input  [7:0]  io_fetch_req_bits_vSetIdx,
    
    // 预取请求接口  
    input         io_prefetch_req_valid,
    output        io_prefetch_req_ready,
    input  [41:0] io_prefetch_req_bits_blkPaddr,
    input  [7:0]  io_prefetch_req_bits_vSetIdx,
    
    // TileLink内存接口
    output        io_mem_acquire_valid,
    input         io_mem_acquire_ready,
    output [3:0]  io_mem_acquire_bits_source,
    output [47:0] io_mem_acquire_bits_address,
    
    input         io_mem_grant_valid,
    output        io_mem_grant_ready,
    input  [3:0]  io_mem_grant_bits_source,
    input  [2:0]  io_mem_grant_bits_opcode,
    input  [255:0] io_mem_grant_bits_data,
    input         io_mem_grant_bits_corrupt,
    
    // 取指响应接口
    output        io_fetch_resp_valid,
    output [41:0] io_fetch_resp_bits_blkPaddr,
    output [7:0]  io_fetch_resp_bits_vSetIdx,
    output [3:0]  io_fetch_resp_bits_waymask,
    output [511:0] io_fetch_resp_bits_data,
    output        io_fetch_resp_bits_corrupt,
    
    // 控制信号
    input  [1:0]  io_victim_way,
    input         io_flush,
    input         io_fencei,
    
    // SRAM写接口
    output        io_meta_write_valid,
    output [3:0]  io_meta_write_bits_waymask,
    output        io_data_write_valid,
    output [3:0]  io_data_write_bits_waymask
);
```

## Bundle接口设计

Bundle是Toffee框架中用于信号层次化管理的核心组件，将RTL信号组织成结构化的接口。
### 信号访问示例

```python
# 访问取指请求信号
bundle.io._fetch._req._valid.value = 1
bundle.io._fetch._req._bits._blkPaddr.value = 0x1000

# 访问内存接口信号  
acquire_valid = bundle.io._mem._acquire._valid.value
grant_data = bundle.io._mem._grant._bits._data.value

# 访问内部信号
last_fire = bundle.ICacheMissUnit_.last_fire.value
mshr_ready = bundle.ICacheMissUnit_._fetchMSHRs._0._io._req_ready.value
```

## Agent接口设计

Agent提供高级API来驱动DUT和验证行为，封装了复杂的时序控制和协议细节。

### API参考文档

#### 基础控制接口

##### `async def fencei_func(self, value: int)`
**功能**: 设置fencei信号并等待处理完成  
**参数**:
- `value` (int): fencei信号值 (0/1)

**返回值**: None  
**异常**: None  
**用法示例**:
```python
await agent.fencei_func(1)  # 激活fencei
await agent.fencei_func(0)  # 清除fencei
```

##### `async def drive_set_flush(self, value: bool)`
**功能**: 设置或清除flush信号  
**参数**:
- `value` (bool): flush信号状态

**返回值**: None  
**异常**: None  
**用法示例**:
```python
await agent.drive_set_flush(True)   # 激活flush
await agent.drive_set_flush(False)  # 清除flush
```

##### `async def drive_set_victim_way(self, way: int)`
**功能**: 设置替换策略的victim way  
**参数**:
- `way` (int): way编号 (0-3)

**返回值**: None  
**异常**: None  
**用法示例**:
```python
await agent.drive_set_victim_way(1)  # 设置victim way为1
```

#### 请求发送接口

##### `async def drive_send_fetch_request(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> dict`
**功能**: 发送取指请求并等待接受  
**参数**:
- `blkPaddr` (int): 块物理地址
- `vSetIdx` (int): 虚拟set索引
- `timeout_cycles` (int, 可选): 超时周期数，默认10

**返回值**: 
```python
{
    "send_success": bool,    # 请求是否成功发送
    "blkPaddr": int,        # 实际发送的块地址
    "vSetIdx": int          # 实际发送的set索引
}
```

**异常**: None  
**用法示例**:
```python
result = await agent.drive_send_fetch_request(blkPaddr=0x1000, vSetIdx=0x10)
if result["send_success"]:
    print("Fetch request sent successfully")
```

##### `async def drive_send_prefetch_req(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> dict`
**功能**: 发送预取请求并等待接受  
**参数**:
- `blkPaddr` (int): 块物理地址
- `vSetIdx` (int): 虚拟set索引
- `timeout_cycles` (int, 可选): 超时周期数，默认10

**返回值**: 
```python
{
    "send_success": bool,    # 请求是否成功发送
    "blkPaddr": int,        # 实际发送的块地址
    "vSetIdx": int          # 实际发送的set索引
}
```

**异常**: None  
**用法示例**:
```python
result = await agent.drive_send_prefetch_req(blkPaddr=0x2000, vSetIdx=0x20)
assert result["send_success"], "Prefetch request should succeed"
```

#### TileLink协议接口

##### `async def drive_get_acquire_request(self, timeout_cycles: int = 10) -> dict | None`
**功能**: 获取acquire请求（单次获取，不执行handshake）  
**参数**:
- `timeout_cycles` (int, 可选): 超时周期数，默认10

**返回值**: 
```python
{
    "source": int,    # 源ID (0-3: fetch, 4-13: prefetch)
    "address": int    # 请求地址
}
# 或 None (超时)
```

**异常**: None  
**注意**: 此API只获取请求信息，不执行handshake，需要手动调用`drive_acknowledge_acquire`  
**用法示例**:
```python
acquire_info = await agent.drive_get_acquire_request()
if acquire_info:
    print(f"Got acquire: source={acquire_info['source']}")
    await agent.drive_acknowledge_acquire()
```

##### `async def drive_get_and_acknowledge_acquire(self, timeout_cycles: int = 10, ack_cycles: int = 1) -> dict | None`
**功能**: 获取acquire请求并立即执行handshake（原子操作）  
**参数**:
- `timeout_cycles` (int, 可选): 超时周期数，默认10
- `ack_cycles` (int, 可选): 确认持续周期数，默认1

**返回值**: 与`drive_get_acquire_request`相同  
**异常**: None  
**注意**: 这是推荐的API，避免重复获取同一个acquire请求  
**用法示例**:
```python
acquire_info = await agent.drive_get_and_acknowledge_acquire()
if acquire_info:
    print(f"Processed acquire: source={acquire_info['source']}")
```

##### `async def drive_acknowledge_acquire(self, cycles: int = 1, ready_value: int = 1)`
**功能**: 确认acquire请求  
**参数**:
- `cycles` (int, 可选): 确认持续周期数，默认1
- `ready_value` (int, 可选): ready信号值，默认1

**返回值**: None  
**异常**: None  
**用法示例**:
```python
await agent.drive_acknowledge_acquire(cycles=2)  # 持续2个周期
```

##### `async def drive_respond_with_grant(self, source_id: int, data_beats: list, beat_size_code: int = 6, op_code: int = 5, is_corrupt_list: list = None)`
**功能**: 发送Grant响应（支持multi-beat传输）  
**参数**:
- `source_id` (int): 目标源ID
- `data_beats` (list): 数据beats列表，每个元素为int类型
- `beat_size_code` (int, 可选): beat大小编码，默认6
- `op_code` (int, 可选): 操作码，默认5 (GrantData)
- `is_corrupt_list` (list, 可选): 每个beat的corruption状态，默认全False

**返回值**: None  
**异常**: ValueError (当is_corrupt_list长度与data_beats不匹配时)  
**用法示例**:
```python
# 发送正常的2-beat Grant
grant_data = [0x1234567890ABCDEF, 0xFEDCBA0987654321]
await agent.drive_respond_with_grant(source_id=0, data_beats=grant_data)

# 发送带corruption的Grant
grant_data = [0x1111111111111111, 0x2222222222222222]
corrupt_flags = [False, True]  # 第二个beat有corruption
await agent.drive_respond_with_grant(
    source_id=0, 
    data_beats=grant_data, 
    is_corrupt_list=corrupt_flags
)
```

#### 响应获取接口

##### `async def drive_get_fetch_response(self, timeout_cycles: int = 20) -> dict | None`
**功能**: 获取fetch响应  
**参数**:
- `timeout_cycles` (int, 可选): 超时周期数，默认20

**返回值**: 
```python
{
    "blkPaddr": int,    # 块物理地址
    "vSetIdx": int,     # 虚拟set索引
    "waymask": int,     # way掩码 (独热编码)
    "data": int,        # 响应数据
    "corrupt": bool     # 数据是否损坏
}
# 或 None (超时)
```

**异常**: None  
**用法示例**:
```python
response = await agent.drive_get_fetch_response()
if response:
    print(f"Got response: waymask={response['waymask']}")
    assert not response['corrupt'], "Data should not be corrupt"
```

### 完整流程示例

```python
async def complete_fetch_flow_example(agent):
    """完整的fetch流程示例"""
    
    # 1. 发送fetch请求
    result = await agent.drive_send_fetch_request(blkPaddr=0x1000, vSetIdx=0x10)
    assert result["send_success"], "Fetch request should succeed"
    
    # 2. 获取并确认acquire请求
    acquire_info = await agent.drive_get_and_acknowledge_acquire()
    assert acquire_info is not None, "Should get acquire request"
    
    # 3. 设置victim way
    await agent.drive_set_victim_way(way=1)
    
    # 4. 发送Grant响应
    grant_data = [0x1234567890ABCDEF, 0xFEDCBA0987654321]
    await agent.drive_respond_with_grant(
        source_id=acquire_info['source'], 
        data_beats=grant_data
    )
    
    # 5. 获取fetch响应
    response = await agent.drive_get_fetch_response()
    assert response is not None, "Should get fetch response"
    assert response["waymask"] == (1 << 1), "Waymask should match victim way"
    
    return response

async def flush_scenario_example(agent):
    """flush场景示例"""
    
    # 发送请求
    await agent.drive_send_fetch_request(blkPaddr=0x1000, vSetIdx=0x10)
    acquire_info = await agent.drive_get_and_acknowledge_acquire()
    
    # 在Grant前激活flush
    await agent.drive_set_flush(True)
    
    # 发送Grant
    grant_data = [0x1111111111111111, 0x2222222222222222]
    await agent.drive_respond_with_grant(
        source_id=acquire_info['source'], 
        data_beats=grant_data
    )
    
    # 仍然应该得到响应，但SRAM不会被写入
    response = await agent.drive_get_fetch_response()
    assert response is not None, "Should get response even with flush"
    
    # 清除flush
    await agent.drive_set_flush(False)
```

## 测试用例设计

### 完整测试用例列表 (共27个)

#### 1. 基础功能测试
1. **test_smoke** - 冒烟测试，验证基本功能
2. **test_bundle_drive_fetch_req_inputs** - Bundle接口fetch请求输入测试
3. **test_bundle_read_fetch_req_ready** - Bundle接口fetch ready信号读取测试
4. **test_fencei_work** - Fencei功能测试
5. **test_set_flush** - Flush信号设置测试
6. **test_set_victim_way** - Victim way设置测试

#### 2. 请求发送测试
7. **test_send_fetch_request** - 取指请求发送测试
8. **test_send_prefetch_request** - 预取请求发送测试

#### 3. API完整流程测试
9. **test_api_fetch_request_generates_acquire** - API取指请求生成acquire测试
10. **test_api_full_fetch_flow** - API完整取指流程测试
11. **test_api_grant_with_corruption** - API Grant数据损坏处理测试
12. **test_api_full_prefetch_flow** - API完整预取流程测试

#### 4. FIFO和优先级测试
13. **test_FIFO_moudle** - FIFO模块功能测试

#### 5. MSHR管理测试
14. **test_mshr_hit_detection** - MSHR查找命中逻辑测试
15. **test_mshr_release_after_grant** - MSHR在Grant完成后的释放测试

#### 6. 优先级策略测试
16. **test_low_index_priority_fetch** - Fetch MSHR低索引优先级测试
17. **test_low_index_priority_prefetch** - Prefetch MSHR低索引优先级测试
18. **test_fifo_priority_ordering** - FIFO优先级顺序测试
19. **test_acquire_arbitration_priority** - Acquire仲裁优先级测试

#### 7. 数据传输与处理测试
20. **test_grant_beat_collection** - Grant多beat数据收集测试
21. **test_victim_way_update** - 替换策略更新测试
22. **test_waymask_generation** - Waymask生成逻辑测试

#### 8. SRAM写回测试
23. **test_sram_write_conditions** - SRAM写回条件测试
24. **test_no_write_with_flush_fencei** - Flush/Fencei时SRAM写回抑制测试

#### 9. 特殊情况测试
25. **test_flush_fencei_mshr_behavior** - Flush/Fencei对MSHR影响测试
26. **test_prefetch_same_address_as_fetch** - 相同地址处理测试
27. **test_demux_chosen_signal** - Demux选择信号测试

### 测试分类总结

| 分类 | 测试用例数量 | 主要验证内容 |
|------|-------------|-------------|
| 基础功能 | 6个 | Bundle接口、基本信号控制 |
| 请求发送 | 2个 | Fetch/Prefetch请求发送 |
| API流程 | 4个 | 完整的API使用流程 |
| FIFO功能 | 1个 | Priority FIFO操作 |
| MSHR管理 | 2个 | MSHR分配、释放、命中检测 |
| 优先级策略 | 4个 | 各级优先级仲裁逻辑 |
| 数据传输 | 3个 | Grant处理、waymask生成 |
| SRAM写回 | 2个 | 写回控制和条件判断 |
| 特殊情况 | 3个 | Flush/Fencei、边界条件 |
| **总计** | **27个** | **全面覆盖ICacheMissUnit功能** |

## 功能覆盖点设计

功能覆盖点用于量化验证完整性，确保所有关键功能场景都被测试覆盖。

### 覆盖点分类

#### 1. FIFO操作覆盖点（CP28-30）

```python
# CP28: 入队操作覆盖
"enq_when_not_full": 正常入队
"enq_when_will_full": 入队导致满状态  
"enq_blocked_when_full": 队满时阻塞

# CP29: 出队操作覆盖
"deq_when_not_null": 正常出队
"deq_when_will_wrap": 出队指针回环
"deq_blocked_when_null": 队空时阻塞

# CP30: Flush操作覆盖
"after_flush": Flush后状态重置
```

#### 2. 请求处理覆盖点（CP31-32）

```python
# CP31: Fetch请求处理
"CP31.1": 接受新的取指请求
"CP31.2": 处理已有的取指请求
"CP31.3": 低索引优先级仲裁

# CP32: Prefetch请求处理  
"CP32.1": 接受新的预取请求
"CP32.2": 处理已有的预取请求
```

#### 3. MSHR管理覆盖点（CP33）

```python
"CP33.1_fetch_hit_existing": Fetch请求命中现有MSHR
"CP33.2_prefetch_hit_existing": Prefetch请求命中现有MSHR
"CP33.3_prefetch_hit_fetch_same": 相同地址命中
"CP33.4_no_hit": 请求未命中任何MSHR
```

#### 4. 仲裁逻辑覆盖点（CP34）

```python
"CP34.1_fetch_priority": Fetch请求优先于prefetch
"CP34.2_prefetch_selected": 仅prefetch请求时被选中
```

#### 5. Grant数据处理覆盖点（CP35）

```python
"CP35.1_first_beat": 第一个beat数据接收
"CP35.2_last_beat": 最后一个beat数据接收  
"CP35.3_grant_corrupt": Grant数据带corrupt标志
"CP35.4_grant_completion": Grant完成后状态
```

#### 6. 替换策略覆盖点（CP36）

```python
"CP36.1_victim_update": Acquire成功时更新victim
```

#### 7. SRAM写回覆盖点（CP37）

```python
"CP37.1_normal_sram_write": 正常写SRAM
"CP37.2_no_write_with_flush": Flush/Fencei时不写SRAM但仍响应  
"CP37.3_fetch_resp_always": Fetch响应总是生成
"CP37.4_corrupt_response": Corrupt数据响应
```

#### 8. Miss 完成响应覆盖点（CP38）

```python
# CP38.1: 正常 Miss 完成响应
"CP38.1_normal_miss_completion": 正常Miss完成响应
```

#### 9. 特殊处理覆盖点（CP39）

```python
# CP39.1: MSHR 未发射前 fencei
"CP39.1_fencei_before_fire": Fencei阻止MSHR发射

# CP39.2: MSHR 未发射前 flush
"CP39.2_flush_before_fire": Flush只阻止prefetch MSHR发射

# CP39.3: MSHR 已发射后 flush/fencei
"CP39.3_flush_fencei_after_fire": 发射后flush/fencei抑制写回但不影响响应
```

### 覆盖点使用示例

```python
def define_missunit_coverage_groups(bundle, dut):
    g = CovGroup("MissUnit_Main_Coverage")
    
    # CP33: MSHR查找命中逻辑覆盖点
    g.add_watch_point(
        {
            "fetch_req_valid": bundle.io._fetch._req._valid,
            "fetch_hit": bundle.ICacheMissUnit_.fetchHit,
            "prefetch_req_valid": bundle.io._prefetch_req._valid,
            "prefetch_hit": bundle.ICacheMissUnit_.prefetchHit,
        },
        bins={
            "CP33.1_fetch_hit_existing": lambda d: d["fetch_req_valid"].value == 1 and d["fetch_hit"].value == 1,
            "CP33.2_prefetch_hit_existing": lambda d: d["prefetch_req_valid"].value == 1 and d["prefetch_hit"].value == 1,
        },
        name="MSHR_lookup_hit_logic"
    )
    
    # CP38.1: Miss 完成响应覆盖点
    g.add_watch_point(
        {
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
            "last_fire_r": bundle.ICacheMissUnit_.last_fire_r,
            # 使用DUT内部信号访问mshr_resp（从RTL信号路径获取）
            "mshr_resp_blkPaddr": dut.GetInternalSignal("ICacheMissUnit_top.ICacheMissUnit.mshr_resp_blkPaddr", use_vpi=False),
            "mshr_resp_vSetIdx": dut.GetInternalSignal("ICacheMissUnit_top.ICacheMissUnit.mshr_resp_vSetIdx", use_vpi=False),
        },
        bins={
            # 38.1: 正常 Miss 完成响应
            # 当 last_fire_r 为高时，且内部mshr_resp有效数据时，无论是否有刷新信号，
            # io.fetch_resp.valid 都为高
            "CP38.1_normal_miss_completion": lambda d: d["last_fire_r"].value == 1 and \
                                                       d["fetch_resp_valid"].value == 1 and \
                                                       (d["mshr_resp_blkPaddr"].value != 0 or d["mshr_resp_vSetIdx"].value != 0),
        },
        name="miss_completion_response"
    )
    
    # CP39: 处理 flush/fencei 覆盖点
    g.add_watch_point(
        {
            "flush": bundle.io._flush,
            "fencei": bundle.io._fencei,
            "last_fire_r": bundle.ICacheMissUnit_.last_fire_r,
            "meta_write_valid": bundle.io._meta_write._valid,
            "data_write_valid": bundle.io._data_write._valid,
            "fetch_resp_valid": bundle.io._fetch._resp._valid,
        },
        bins={
            # 39.3: MSHR 已发射后 flush/fencei
            # 已经发射了请求，之后再有刷新信号，等数据回来但不写 SRAM
            "CP39.3_flush_fencei_after_fire": lambda d: (d["flush"].value == 1 or d["fencei"].value == 1) and \
                                                        d["last_fire_r"].value == 1 and \
                                                        d["meta_write_valid"].value == 0 and \
                                                        d["data_write_valid"].value == 0 and \
                                                        d["fetch_resp_valid"].value == 1,
        },
        name="flush_fencei_after_fire"
    )
    
    return g
```

## 验证环境配置

### fixture 配置

```python
@toffee_test.fixture
async def icachemissunit_env(toffee_request: toffee_test.ToffeeRequest):
    # 初始化DUT
    dut = toffee_request.create_dut(DUTICacheMissUnit)
    start_clock(dut)
    
    # 创建验证环境
    icachemissunit_env = ICacheMissUnitEnv(dut)
    
    # 复位序列
    icachemissunit_env.dut.reset.value = 1
    icachemissunit_env.dut.Step(10)
    icachemissunit_env.dut.reset.value = 0
    icachemissunit_env.dut.Step(10)
    
    # 初始化时钟
    dut.InitClock("clock")
    
    # 添加功能覆盖点
    coverage_groups = create_all_coverage_groups(icachemissunit_env.bundle, dut)
    for coverage_group in coverage_groups:
        toffee_request.add_cov_groups(coverage_group)
    
    yield icachemissunit_env
```

## 运行和调试

### 测试执行

```bash
# 运行所有测试
cd UnityChipForXiangShan
make test target=ut_frontend/icache/missunit
```

## 最佳实践

### 1. 测试设计原则
- **单一职责**：每个测试专注验证一个功能点
- **时序控制**：正确使用`await bundle.step()`控制时序
- **错误处理**：提供有意义的错误信息和调试输出
- **可重复性**：测试结果应该稳定可重复

### 2. 覆盖点设计原则
- **完整性**：覆盖所有关键功能场景
- **正交性**：覆盖点之间相互独立
- **可观测性**：选择容易观测的信号作为覆盖条件

### 3. Agent接口设计原则
- **高级抽象**：隐藏协议细节，提供易用接口
- **原子操作**：提供组合操作避免时序问题
- **错误处理**：超时和异常情况的合理处理

## 扩展指南

### 添加新的测试用例

1. 在`missunit_test.py`中添加测试函数
2. 使用`@toffee_test.testcase`装饰器
3. 通过`icachemissunit_env`参数获取验证环境
4. 使用agent API编写测试逻辑

### 添加新的覆盖点

1. 在`missunit_coverage.py`中定义覆盖点
2. 选择合适的观测信号
3. 定义覆盖条件（lambda函数）
4. 在`create_all_coverage_groups`中注册

### 扩展Agent接口

1. 在`missunit_agent.py`中添加新的API
2. 遵循异步编程模式
3. 提供适当的超时处理
4. 添加调试输出

## 结论

基于Toffee框架的ICacheMissUnit验证环境提供了完整的验证解决方案，包括：

- **结构化的Bundle接口**：清晰的信号层次组织
- **高级的Agent API**：易用的协议驱动接口
- **全面的测试覆盖**：27个测试用例覆盖核心功能
- **量化的功能覆盖**：（CP28-CP39）覆盖点确保验证完整性

该验证环境为ICacheMissUnit的功能验证提供了坚实的基础，支持高效的测试开发和调试工作流程。