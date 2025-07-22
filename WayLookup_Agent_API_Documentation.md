# WayLookup Agent API 文档

## 概述

WayLookupAgent是用于测试WayLookup模块的测试代理，提供了完整的读写操作、状态查询和验证功能的API接口。

## API分类

### 1. 基础控制API

#### `reset_dut()`
- **功能**: 重置DUT（被测设计）
- **参数**: 无
- **返回**: 无
- **说明**: 拉高reset信号5个周期，然后拉低5个周期完成复位

#### `drive_set_flush(value: bool)`
- **功能**: 设置或清除flush信号
- **参数**: `value` - flush信号值
- **返回**: 无
- **说明**: 用于控制WayLookup的刷新操作

#### `flush() -> ReadBitsData`
- **功能**: 执行flush操作并返回前后状态
- **参数**: 无
- **返回**: `ReadBitsData` - 包含flush前后的指针状态
- **说明**: 兼容性方法，记录flush前后的读写指针状态

### 2. 写操作API

#### `drive_write_entry(...) -> dict`
- **功能**: 向WayLookup写入条目
- **参数**: 
  - `vSetIdx_0/1`: 虚拟集合索引
  - `waymask_0/1`: 路掩码
  - `ptag_0/1`: 物理标签  
  - `itlb_exception_0/1`: ITLB异常
  - `itlb_pbmt_0/1`: ITLB页面基本内存类型
  - `meta_codes_0/1`: 元数据代码
  - `gpf_gpaddr`: GPF地址
  - `gpf_isForVSnonLeafPTE`: GPF标志
  - `timeout_cycles`: 超时周期数（默认10）
- **返回**: 包含写入成功状态和实际写入值的字典
- **说明**: 支持超时机制，等待write_ready信号

#### `drive_write_entry_with_gpf(...) -> dict`
- **功能**: 写入包含GPF异常的条目
- **参数**: 基本参数 + GPF相关参数
- **返回**: 同`drive_write_entry`
- **说明**: 自动设置`itlb_exception=2`表示GPF异常

### 3. 读操作API

#### `drive_read_entry(timeout_cycles: int = 10) -> dict`
- **功能**: 从WayLookup读取条目
- **参数**: `timeout_cycles` - 超时周期数
- **返回**: 包含读取数据的字典，失败时返回`{"read_success": False}`
- **说明**: 设置read_ready等待read_valid信号

#### `check_read_valid() -> bool`
- **功能**: 检查当前读数据是否有效
- **参数**: 无
- **返回**: 读数据有效性状态
- **说明**: 立即返回read_valid信号状态

### 4. 更新操作API

#### `drive_update_entry(blkPaddr, vSetIdx, waymask, corrupt=False)`
- **功能**: 执行更新操作（模拟MissUnit更新）
- **参数**:
  - `blkPaddr`: 块物理地址
  - `vSetIdx`: 虚拟集合索引
  - `waymask`: 路掩码
  - `corrupt`: 损坏标志
- **返回**: 无
- **说明**: 用于测试命中信息更新功能

### 5. 状态查询API

#### `get_queue_status() -> dict`
- **功能**: 获取队列当前状态
- **参数**: 无
- **返回**: 包含队列状态的字典
  - `empty/full`: 队列空/满状态
  - `count`: 当前队列条目数
  - `read_ptr_value/flag`: 读指针状态
  - `write_ptr_value/flag`: 写指针状态
  - `write_ready/read_valid`: IO信号状态

#### `get_pointers() -> dict`
- **功能**: 获取读写指针状态
- **参数**: 无
- **返回**: 读写指针的值和标志位

#### `get_gpf_status() -> dict`
- **功能**: 获取GPF相关状态
- **参数**: 无  
- **返回**: GPF状态信息
- **说明**: 部分内部信号可能需要额外暴露

### 6. 辅助验证API

#### `fill_queue(count: int) -> list`
- **功能**: 向队列填充指定数量的条目
- **参数**: `count` - 要填充的条目数
- **返回**: 成功写入的条目列表
- **说明**: 用于测试队列容量和写入功能

#### `drain_queue() -> list`
- **功能**: 排空队列中的所有条目
- **参数**: 无
- **返回**: 读取到的所有条目列表
- **说明**: 用于清空队列并验证数据完整性

#### `wait_for_condition(condition_func, timeout_cycles=100) -> bool`
- **功能**: 等待自定义条件成立
- **参数**: 
  - `condition_func`: 条件函数
  - `timeout_cycles`: 超时周期数
- **返回**: 条件是否在超时前成立
- **说明**: 通用的条件等待工具

### 7. 高级组合API

#### `test_bypass_condition() -> dict`
- **功能**: 测试bypass功能
- **参数**: 无
- **返回**: bypass测试结果
- **说明**: 验证当队列为空且有写请求时的直通功能

## 使用示例

```python
# 初始化agent
agent = WayLookupAgent(bundle)

# 重置DUT
await agent.reset_dut()

# 写入条目
result = await agent.drive_write_entry(
    vSetIdx_0=0x10, waymask_0=1, ptag_0=0x1000
)

# 读取条目  
data = await agent.drive_read_entry()

# 检查队列状态
status = await agent.get_queue_status()

# 测试bypass功能
bypass_result = await agent.test_bypass_condition()
```

## 设计特点

1. **异步接口**: 所有API都是异步的，支持时序控制
2. **超时机制**: 重要操作支持超时参数防止死锁
3. **状态监控**: 提供丰富的状态查询接口
4. **组合功能**: 提供高级API简化复杂测试场景
5. **错误处理**: 返回详细的成功/失败状态信息

## API详细说明

### ReadBitsData类
用于存储flush操作前后的状态信息：
- `WayLookup_readPtr_value_before/after_flush`: flush前后读指针值
- `WayLookup_readPtr_flag_before/after_flush`: flush前后读指针标志
- `WayLookup_writePtr_value_before/after_flush`: flush前后写指针值  
- `WayLookup_writePtr_flag_before/after_flush`: flush前后写指针标志
- `flush`: flush信号值

### 错误处理
- 所有写操作支持超时机制，防止在队列满时无限等待
- 读操作在没有数据时返回明确的失败状态
- 状态查询API提供实时的队列和信号状态信息

### 测试场景支持
- **基础功能测试**: 单次读写操作
- **队列管理测试**: 填充、排空、状态监控
- **异常处理测试**: GPF异常写入和读取
- **边界条件测试**: 队列满、空状态处理
- **旁路功能测试**: bypass条件验证
- **更新功能测试**: MissUnit命中信息更新

## 注意事项

1. 所有API都需要在异步环境中调用
2. 写操作前建议检查队列状态，避免不必要的超时等待
3. GPF相关功能需要确保内部信号正确暴露
4. 使用组合API时注意信号状态的前置条件
5. 测试完成后建议执行flush清理队列状态