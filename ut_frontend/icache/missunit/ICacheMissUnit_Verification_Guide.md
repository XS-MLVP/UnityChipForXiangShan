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

### Bundle层次结构

```python
class ICacheMissUnitBundle(Bundle):
    def __init__(self):
        super().__init__()
        # 主要接口组
        self.io = IOBundle()           # 顶层IO接口
        self.ICacheMissUnit_ = InternalBundle()  # 内部信号
        
class IOBundle(Bundle):
    def __init__(self):
        super().__init__()
        self._fetch = FetchBundle()     # 取指接口
        self._prefetch_req = PrefetchBundle()  # 预取接口
        self._mem = MemBundle()         # 内存接口
        self._victim = VictimBundle()   # 替换策略
        self._flush = XPin()            # Flush信号
        self._fencei = XPin()           # Fencei信号
        
class FetchBundle(Bundle):
    def __init__(self):
        super().__init__()
        self._req = FetchReqBundle()    # 请求
        self._resp = FetchRespBundle()  # 响应
        
class MemBundle(Bundle):  
    def __init__(self):
        super().__init__()
        self._acquire = AcquireBundle() # Acquire通道
        self._grant = GrantBundle()     # Grant通道
```

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

### 核心API接口

#### 1. 基础控制接口

```python
async def drive_set_victim_way(self, way: int)
    """设置替换策略的victim way"""
    
async def drive_send_fetch_request(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> dict
    """发送取指请求"""
    
async def drive_send_prefetch_req(self, blkPaddr: int, vSetIdx: int, timeout_cycles: int = 10) -> dict
    """发送预取请求"""
```

#### 2. TileLink协议接口

```python
async def drive_get_acquire_request(self, timeout_cycles: int = 10) -> dict | None
    """获取acquire请求（单次）"""
    
async def drive_get_and_acknowledge_acquire(self, timeout_cycles: int = 10, ack_cycles: int = 1) -> dict | None
    """获取acquire请求并立即确认（原子操作）"""
    
async def drive_acknowledge_acquire(self, cycles: int = 1, ready_value: int = 1)
    """确认acquire请求"""
    
async def drive_respond_with_grant(self, source_id: int, data_beats: list, beat_size_code: int = 6, op_code: int = 5, corrupt: bool = False)
    """发送Grant响应（支持multi-beat）"""
```

#### 3. 响应获取接口

```python
async def drive_get_fetch_response(self, timeout_cycles: int = 10) -> dict | None
    """获取取指响应"""
```

### Agent使用示例

```python
# 完整的fetch流程
async def test_full_fetch_flow(agent):
    # 1. 发送取指请求
    result = await agent.drive_send_fetch_request(blkPaddr=0x1000, vSetIdx=0x10)
    assert result["send_success"] is True
    
    # 2. 获取并确认acquire请求
    acquire_info = await agent.drive_get_and_acknowledge_acquire()
    assert acquire_info is not None
    
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
    assert response is not None
    assert response["waymask"] == (1 << 1)  # 验证waymask
```

## 测试用例设计

### 测试分类

#### 1. 基础功能测试
- **test_smoke**: 冒烟测试，验证基本功能
- **test_send_fetch_request**: 取指请求发送测试
- **test_send_prefetch_request**: 预取请求发送测试

#### 2. MSHR管理测试
- **test_mshr_hit_detection**: MSHR查找命中逻辑测试
- **test_mshr_release_after_grant**: MSHR释放测试
- **test_low_index_priority_fetch**: Fetch MSHR低索引优先级测试
- **test_low_index_priority_prefetch**: Prefetch MSHR低索引优先级测试

#### 3. 仲裁逻辑测试
- **test_acquire_arbitration_priority**: Acquire仲裁优先级测试
- **test_fifo_priority_ordering**: FIFO优先级顺序测试

#### 4. 数据传输测试
- **test_grant_beat_collection**: Grant多beat数据收集测试
- **test_api_grant_with_corruption**: 数据损坏处理测试

#### 5. 替换策略测试
- **test_victim_way_update**: 替换策略更新测试
- **test_waymask_generation**: Waymask生成逻辑测试

#### 6. SRAM写回测试
- **test_sram_write_conditions**: SRAM写回条件测试
- **test_no_write_with_flush_fencei**: Flush/Fencei时SRAM写回抑制测试

#### 7. 特殊情况测试
- **test_flush_fencei_mshr_behavior**: Flush/Fencei对MSHR影响测试
- **test_prefetch_same_address_as_fetch**: 相同地址处理测试
- **test_demux_chosen_signal**: Demux选择信号测试

### 典型测试用例解析

#### test_acquire_arbitration_priority

```python
@toffee_test.testcase
async def test_acquire_arbitration_priority(icachemissunit_env: ICacheMissUnitEnv):
    """验证acquire仲裁逻辑：fetch请求优先于prefetch请求"""
    agent = icachemissunit_env.agent
    bundle = icachemissunit_env.bundle
    
    # 发送prefetch和fetch请求
    prefetch_result = await agent.drive_send_prefetch_req(blkPaddr=0x8000, vSetIdx=0x80)
    await bundle.step(2)
    fetch_result = await agent.drive_send_fetch_request(blkPaddr=0x9000, vSetIdx=0x90)
    await bundle.step(3)
    
    # 收集acquire请求，验证仲裁顺序
    acquire_requests = []
    for attempt in range(3):
        acquire_info = await agent.drive_get_and_acknowledge_acquire(timeout_cycles=5)
        if acquire_info is not None:
            acquire_requests.append(acquire_info)
        else:
            break
    
    # 验证fetch请求（source < 4）优先于prefetch请求（source >= 4）
    fetch_sources = [req["source"] for req in acquire_requests if req["source"] < 4]
    prefetch_sources = [req["source"] for req in acquire_requests if req["source"] >= 4]
    
    assert len(fetch_sources) > 0, "Fetch request should be processed"
    assert len(prefetch_sources) > 0, "Prefetch request should be processed"
```

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

#### 8. 特殊处理覆盖点（CP38）

```python
"CP38.1_fencei_clear_all": Fencei清除所有MSHR
"CP38.2_flush_prefetch_only": Flush只影响prefetch MSHR
```

### 覆盖点使用示例

```python
def define_missunit_coverage_groups(bundle):
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
    
    return g
```

## 验证环境配置

### 测试夹具配置

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
python -m pytest ut_frontend/icache/missunit/test/missunit_test.py

# 运行特定测试
python -m pytest ut_frontend/icache/missunit/test/missunit_test.py::test_acquire_arbitration_priority

# 运行带覆盖率的测试
python -m pytest ut_frontend/icache/missunit/test/missunit_test.py --cov
```

### 调试技巧

1. **信号监控**
```python
# 在测试中添加调试输出
print(f"MSHR 0 ready: {bundle.ICacheMissUnit_._fetchMSHRs._0._io._req_ready.value}")
print(f"Acquire valid: {bundle.io._mem._acquire._valid.value}")
```

2. **波形生成**
```python
# 在关键时间点dump波形
await bundle.step(1)  # 等待信号稳定
dut.dump_vcd("debug.vcd")  # 生成波形文件
```

3. **状态检查**
```python
# 检查内部状态
if bundle.ICacheMissUnit_.last_fire_r.value == 1:
    print("Grant processing completed")
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
- **全面的测试覆盖**：13个主要测试用例覆盖核心功能
- **量化的功能覆盖**：38个覆盖点确保验证完整性

该验证环境为ICacheMissUnit的功能验证提供了坚实的基础，支持高效的测试开发和调试工作流程。