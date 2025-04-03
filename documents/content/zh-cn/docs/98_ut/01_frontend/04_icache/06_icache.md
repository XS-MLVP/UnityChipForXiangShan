---
title: ICache
linkTitle: ICache
weight: 12
---

<div class="icache-ctx">

</div>

## ICache

各种组合数据的宽度以 system verilog/verilog 中的为准。


- IPrefetchPipe 接收来自 FTQ 的预取请求，然后向 MetaArray 和 ITLB 发送请求，再从 ITLB 的响应得到 paddr，之后与 MetaArray 返回的 tag 进行比较得到命中信息，把命中信息、MetaArray ECC 校验信息和 ITLB 信息一并写入 WayLookup，同时进行 PMP 检查。未命中就将信息发送给 MissUnit 处理，MissUnit 通过 TileLink 总线向 L2Cache 发起请求，获取数据后返回给 MetaArray 和 IPrefetchPipe。之后会判断是否 Miss，如果 Miss 则把预取请求发送到 MissUnit，它会通过 TileLink 向 L2 做预取指。
- MainPipe 接收来自 FTQ 的取指请求，然后从 WayLookup 获取路命中信息和 ITLB 查询结果，再访问 DataArray。命中后向 replacer 发送 touch 请求，replacer 采用 PLRU 替换策略,接收到 MainPipe 的命中更新，向 MissUnit 提供写入的 waymask。同时进行 PMP 检查，接收 DataArry 返回的数据。对 DataArray 做 ECC 校验，根据 DataArry 和 MetaArry 的校验结果（MetaArray 的校验结果来自 Waylookup）判断是否将错误报告给总线（beu）。之后，如果 DataArry 没有命中，将信息发往 MissUnit 处理。MissUnit 通过 TileLink 总线向 L2Cache 发起请求，获取数据后返回给 DataArray 和 MainPipe。之后就可以将数据返回给 IFU。
- MetaArray 存储缓存行的标签（Tag）和 ECC 校验码
  - 使用双 Bank SRAM 结构，支持双线访问（Double-Line），每个 Bank 存储部分元数据。
  - 标签包含物理地址的高位，用于地址匹配。
  - 支持标签 ECC 校验，检测和纠正存储错误。
  - valid_array 记录每个 Way 的有效状态，Flush 操作会清零
- DataArray 存储实际的指令数据块。
  - 数据按 Bank 划分为八个，每个 Bank 宽度为 64 位，支持多 Bank 并行访问。
  - 数据 ECC 校验，分段生成校验码，增强错误检测能力。
  - 支持双线访问，根据地址偏移选择 Bank，单周期可读取 32 字节数据。
- 冲刷信号有三种：ftqPrefetch.flushFromBpu，itlbFlushPipe，模块外部的 fencei 和 flush 信号。
  - ftqPrefetch.flushFromBpu：通过 FTQ 来自的 BPU 刷新信号，用于控制预取请求的冲刷。
  - itlbFlushPipe：ITLB 的冲刷信号，itlb 在收到该信号时会冲刷 gpf 缓存。
  - fencei:刷新 MetaArray，清除所有路的 valid_array 清零；missUnit 中所有 MSHR 置无效。
  - flush:mainPipe 和 prefetchPipe 所有流水级直接置无效，wayLookup 读写指针复位，gpf_entry 直接置无效,missUnit 中所有 MSHR 置无效。

### Replacer

采用 PLRU 更新算法，考虑到每次取指可能访问连续的 doubleline，对于奇地址和偶地址设置两个 replacer，在进行 touch 和 victim 时根据地址的奇偶分别更新 replacer。

<div>			
    <center>	
    <img src="../plru.png"
         alt="PLRU 算法示意"
         style="zoom:100%"/>
    <br>		
    PLRU 算法示意	
    </center>
</div>

<br>

#### touch

Replacer 具有两个 touch 端口，用以支持双行，根据 touch 的地址奇偶分配到对应的 replacer 进行更新。

#### victim

Replacer 只有一个 victim 端口，因为同时只有一个 MSHR 会写入 SRAM，同样根据地址的奇偶从对应的 replacer 获取 waymask。并且在下一拍再进行 touch 操作更新 replacer。

## ICache 的功能点和测试点

### FTQ 预取请求处理

接收来自 FTQ 的预取请求，经 IPrefetchPipe 请求过滤（查询 ITLB 地址，是否命中 MetaArry，PMP 检查），（有异常则由 MissUnit 处理）后进入 WayLookup。

1. 预取地址命中，无异常

- io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 匹配，pmp 检查通过。
- 如果没有监听到 MSHR 同样的位置发生了其它 cacheline 的写入，那么验证 wayLookup.io.write 的内容应该命中的取指数据。
- 如果监听到 MSHR 同样的位置发生了其它 cacheline 的写入，那么验证 wayLookup.io.write 的内容应该是未命中的取指数据。

2. 预取地址未命中，无异常

- io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 不匹配，pmp 检查通过。
- 如果监听到 MSHR 将该请求对应的 cacheline 写入了 SRAM，那么验证 wayLookup.io.write 的内容应该命中的取指数据。
- 如果监听到 MSHR 没有将该请求对应的 cacheline 写入了 SRAM，那么验证 wayLookup.io.write 的内容应该未命中的取指数据。

3. 预取地址 TLB 异常，无其他异常

- io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 异常。
- 验证 wayLookup.io.write 的 itlb_exception 内容中，其有对应的异常类型编号（pf:01;gpf:10;af:11）。

4. 预取地址 PMP 异常，无其他异常

- io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 匹配，pmp 检查未通过。
- 验证 wayLookup.io.write 的 tlb_pbmt 内容中，其有对应的异常类型编号（nc:01;io:10）。

### FTQ 取指请求处理

io.fetch.resp <> mainPipe.io.fetch.resp 发送回 IFU 的数据是在 io.fetch.resp。

接收来自 FTQ 的取指请求，从 WayLookup 获取路命中信息和 ITLB 查询结果，再访问 DataArray，监控 MSHR 的响应。更新 replacer，做 pmp 检查。后做 DataArray 和 MetaArray 的 ECC 校验。最后将数据发送给 IFU。

1. 取指请求命中，无异常

- io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查正常，DataArray 和 MetaArray 的 ECC 校验正常。
- 验证 replacer.io.touch 的 vSetIdx 和 way 和 ftq 的 fetch 一致，missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。
- 验证 io.fetch.resp 的数据应该是取指的数据。

2. 取指请求未命中，MSHR 返回的响应命中，无异常

- io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，未命中，pmp 检查正常，DataArray 和 MetaArray 的 ECC 校验正常。
- 请求在 MSHR 返回的响应命中。
- 验证 missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。
- 验证 io.fetch.resp 的数据应该是取指的数据。

3. 取指请求命中,ECC 校验错误，无其他异常

- io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查正常，DataArray 或 MetaArray 的 ECC 校验错误。
- 验证 io.error.valid 为高，且 io.error.bits 内容为对应的错误源和错误类型。
- 先刷 MetaArray 的 ValidArray,给 MissUnit 发请求，由其在 L2 重填，阻塞至数据返回。
- 验证 replacer.io.touch 的 vSetIdx 和 way 和 ftq 的 fetch 一致，missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。
- 验证 io.fetch.resp 的数据应该是取指的数据。

4. 取指请求未命中，但是 exception 非 0（af、gpf、pf），无其他异常

- io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查未通过，DataArray 和 MetaArray 的 ECC 校验正常。
- 验证 io.fetch.resp 为对应的错误源和错误类型。
- 验证 io.fetch.resp 的数据无效，里面有异常类型。

5. 取指请求未命中，通过 WayLookup 中读取到的预取过来的 itlb 中返回 pbmt。

- 有 itlb_pbmt 和 pmp_mmio 时，他们合成 s1_mmio，传递到 s2_mmio,生成 s2_miss,有特殊情况就不会取指。
- io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查通过，DataArray 和 MetaArray 的 ECC 校验正常。
- 验证 io.fetch.resp 为对应的错误源和错误类型。
- 验证 io.fetch.resp 的数据无效，里面有特殊情况类型类型。

6. 取指请求未命中，pmp 返回 mmio ，处理同 5。

### MetaArray 功能

在 IPrefetchPipe 的 S0，接收来自 IPrefetchPipe 的读请求 read，返回对应路和组的响应 readResp。
在 miss 的时候，MissUnit 会将会应的数据写入 write 到 MetaArray。
MetaArray 主要存储了每个 Cache 行的标签和 ECC 校验码。

1. 元数据写入操作（对应的 Set 已满）: ICacheMetaArray 应当能够正确地将元数据（标签和有效位）写入到指定的 Set 和 Way 。

- 从 MissUnit 返回的请求都是未命中的请求（已命中不会向 MissUnit 请求，那么 MissUnit 自然也不会向 MetaArray 写入）。
- 发送一个写请求 write 到 ICacheMetaArray，ICacheReplacer 根据 PLRU 替换策略指定 way，替换路被写入 waymask，最后指定 virIdx、phyTag、waymask、bankIdx、poison。
- 写入操作后，发起一个对相同虚拟索引的读请求。验证 readResp 的 metas 和 codes 分别包含写入的 ptag 和 ecc code，并且对于写入的路，readResp.entryValid 信号被置为有效。

2. 元数据读取操作 (命中): 当一个读请求在 ICacheMetaArray 中命中时（存在有效的条目），它应该返回正确的元数据（标签和有效位）。

- 首先，向特定的虚拟索引（组和路）写入元数据（参照上面的写入操作）。然后，向相同的虚拟索引发送一个读请求。
- 验证 readResp.metas 包含之前写入的物理标签，并且对于相应的路，readResp.entryValid 信号被置为有效。

3. 元数据读取操作 (未命中): 当读取一个尚未被写入的地址时，ICacheMetaArray 应当指示未命中（条目无效）。

- 向 ICacheMetaArray 发送一个读请求，请求的虚拟索引在复位后从未被写入过。
- 验证对于任何路，readResp.entryValid 信号都没有被置为有效。 对应的 readResp.metas 和 codes 的内容是 DontCare 也就是 0。

4. 独立的缓存组刷新：在第 i 个端口是有效的刷新请求，并且该请求的 waymask 指定了当前正在处理的第 w 路时，应该使第 i 个端口的条目无效。

- 先向 ICacheMetaArray 写入指定一个或多个端口的元数据，然后再给对应的端口的路发送刷新请求 io.flush，其包含虚拟索引 virIdx 和路掩码 waymask。
- 验证 valid_array 对应的路中的 virIdx 被置为无效，io.readResp.entryValid 对应路的对应端口为无效。

5. 全部刷新操作: ICacheMetaArray 应当能够在接收到全部刷新请求时，使所有条目无效。

- 先向多个不同的虚拟索引写入元数据。然后置位 io.flushAll 信号。
- 验证步骤: 在 io.flushAll 信号置位后，发起对所有之前写入过的虚拟索引的读请求。验证在所有的读取响应中，对于任何路，readResp.entryValid 信号都没有被置为有效。

### DataArray 功能

与 MetaArray 类似，在 MainPipe 的 S0，接收来自 MainPipe 的读请求 read，返回对应路和组的响应 readResp。
在 miss 的时候，MissUnit 会将会应的数据写入 write 到 DataArray。
DataArray 主要存储了每个 Cache 行的标签和 ECC 校验码。

1. 数据写入操作（对应的 Set 已满）: ICacheDataArray 应当能够正确地将数据写入到指定的 Set (组)、Way (路) 和数据 Bank (存储体)。

- 发送一个写请求 write 到 ICacheDataArray，ICacheReplacer 根据 PLRU 替换策略指定 way，替换路被写入 waymask，最终指定虚拟索引、数据、路掩码、存储体索引 bankIdx 和毒化位。写入的数据模式应跨越多个数据存储体。
- 写入操作后，发起一个对相同虚拟索引和块偏移量的读请求。验证 readResp.datas 与写入的数据相匹配。

2. 数据读取操作 (命中): 当一个读请求命中时（相应的元数据有效），它应该从相应的组、路和数据存储体返回正确的数据。

- 首先，向特定的虚拟索引和块偏移量写入数据。然后，向相同的虚拟索引和块偏移量发送一个读请求。使用不同的块偏移量进行测试，以覆盖存储体的选择逻辑。
- 验证 readResp.datas 包含之前写入的数据。

3. 数据读取操作 (未命中): 当读取一个尚未被写入的地址时，ICacheDataArray 的输出应该是默认值或无关值。

- 向 ICacheDataArray 发送一个读请求，请求的虚拟索引在复位后从未被写入过。
- 验证 readResp.datas 为 0。
