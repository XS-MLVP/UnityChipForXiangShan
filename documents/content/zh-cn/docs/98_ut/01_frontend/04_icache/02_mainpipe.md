---
title: MainPipe
linkTitle: MainPipe
weight: 12
---

<div class="icache-ctx">

</div>

## MainPipe

MainPipe 为 ICache 的主流水，为三级流水设计，负责从 DataArray 中读取数据，pmp 检查，缺失处理，并且将结果返回给 IFU。

<div>			
    <center>	
    <img src="../mainpipe_structure.png"
         alt="MainPipe结构示意图"
         style="zoom:100%"/>
    <br>		
    MainPipe结构示意图	
    </center>
</div>

<br>

1. 从 WayLookup 获取信息，访问 DataArray 单路（S0 阶段）
   在 S0 流水级，从 WayLookup 获取元数据，包括路命中信息和 ITLB 查询结果，访问 DataArray 的单路，如果 DataArray 正在被写或 WayLookup 中没有有效表项，流水线就会阻塞。每次重定向后，FTQ 中同一个请求被同时发送到 MainPipe 和 IPrefetchPipe 中，MainPipe 始终需要等待 IPrefetchPipe 将请求的查询信息写入 WayLookup 后才能向下走，导致了 1 拍重定向延迟，当预取超过取指时，该延迟就会被覆盖。

- 接收并解析来自 FTQ 的取指请求，提取必要的请求信息，如虚拟地址、缓存组索引、块内偏移、是否为双行读、后端的异常信息。
- 从 WayLookup 模块获取缓存命中信息和 TLB 信息，包括 waymask、物理标签、虚拟机物理地址、是否为叶节点、 ITLB 异常、ITLB 的 PBMT 信息、缓存元数据的校验码。
- 访问 DataArray 的单路，如果 DataArray 正在被写或 WayLookup 中没有有效表项，流水线就会阻塞。
- 每次重定向后，FTQ 中同一个请求被同时发送到 MainPipe 和 IPrefetchPipe 中，MainPipe 始终需要等待 IPrefetchPipe 将请求的查询信息写入 WayLookup 后才能向下走，导致了 1 拍重定向延迟，当预取超过取指时，该延迟就会被覆盖。

2. 接收上一个阶段的信息并进行数据暂存、PMP 检查、从 DataArray 获取读响应异常合并、替换策略更新以及监控 MissUnit（S1 阶段）

- 寄存并延迟 S0 阶段信息
  - 从 S0 获取的地址、tag、命中方式（waymask）、TLB 异常标志、下一拍要用的数据等，都会在 S1 寄存一拍，保证在流水线停顿时也能维持正确值。
- Meta ECC 检查
  - 对 S0 读出的 meta 和其校验码（ECC/Parity）进行比对，判断是否发生错误。如果关闭 parity 功能，则跳过该检查。
- 更新 replacer
  - 对确定命中的访问请求，进行“touch”更新，标记最近使用过的 way，以便后续替换算法正确运行。
- PMP 检查
  - 根据 S0 得到的物理地址（paddr），在 S1 对其进行 PMP 检查，判断是否拥有执行权限、是否为 MMIO 等。在当拍收到响应，将结果寄存到下一流水级进行处理。
  - 需要指出，IPrefetchPipe s1 流水级也会进行 PMP 检查，和此处的检查实际上是完全一样的，分别检查只是为了优化时序（避免 `ITLB(reg) -> ITLB.resp -> PMP.req -> PMP.resp -> WayLookup.write -> bypass -> WayLookup.read -> MainPipe s1(reg)` 的超长组合逻辑路径）。
- 异常合并
  - 将 ITLB 与 PMP 异常进行优先级合并，产生最终的异常标记。
- 选择数据来源：MSHR 或 SRAM
  - 接收 DataArray 返回的 data 和 code 并寄存，同时监听 MSHR 的响应，当 DataArray 和 MSHR 的响应同时有效时，后者的优先级更高。当 MSHR 已在填充一些数据，如果当前请求与 MSHR 命中，可以在 S1 阶段直接选用 MSHR 的数据，而不必依赖 SRAM 读出的结果。

3. 监控 MissUnit，在 ECC 校验、异常处理和缺失处理之后，将最终的数据、异常信息传递给 IFU，完成取指流程（S2 阶段）

- ECC 校验
  - DataArray ECC 校验，对 S1 流水级寄存的 code 进行校验，生成 data 是否损坏信号 s2_data_corrupt。如果校验出错，就将错误报告给 BEU。
  - MetaArray ECC 校验，IPrefetchPipe 读出 MetaArray 的数据后会直接进行校验，并将校验结果随命中信息一起入队 WayLookup 并随 MainPipe 流水到达 S2 级（meta_corrupt 信号），在此处随 DataArray 的 ECC 校验结果一起报告给 BEU。
- 监控 MissUnit 响应端口
  - 检查当前 S2 阶段的请求是否与 MSHR 中的条目匹配，命中时寄存 MSHR 响应的数据，为了时序在下一拍才将数据发送到 IFU。
  - 更新 Data 和其是否来自 MSHR 的信息。
  - 更新 s2_hits 和处理异常。
  - 处理 L2 Cache 的 Corrupt 标志。
- 缺失处理，发送 Miss 请求到 MSHR
  - 计算是否需要重新获取（Refetch）。
  - 通过是否命中、ECC 错误、正确跨行、是否异常和是否属于 MMIO 区域来发送 Miss 请求。
  - 设置 Arbiter 合并多个端口的 Miss 请求，确保一次只处理一个请求，同时有避免重复请求的设置。
  - 判断 Fetch 是否完成。
  - 生成 L2 Cache 的异常标记，再将当前 S2 阶段的异常（包括 ITLB、PMP）与 L2 Cache 的异常进行合并。
- 响应 IFU
  - 将最终的数据、异常信息传递给 IFU，完成取指流程。
  - 根据请求是否为跨行，决定如何处理双行数据。
- 报告 TileLink 的 Corrupt 错误
  - 对于每个端口，如果在当前周期 s2_fire 时检测到来自 L2 Cache 的数据 corrupt 错误，就将错误报告给 BEU。

## MainPipe 的功能点和测试点

### 访问 DataArray 的单路

根据从 WayLookup 获取信息，包括路命中信息和 ITLB 查询结果还有 DataArray 当前的情况，决定是否需要从 DataArray 中读取数据。

1. 访问 DataArray 的单路
   - 当 WayLookup 中的信息表明路命中时，ITLB 查询成功，并且 DataArray 当前没有写时，MainPipe 会向 DataArray 发送读取请求，以获取数据。
   - s0_hits 为高（一路命中），s0_itlb_exception 信号为零（ITLB 查询成功），toData.last.ready 为高（DataArray 没有正在进行的写操作）。
   - toData.valid 信号为高，表示 MainPipe 向 DataArray 发出了读取请求。
2. 不访问 DataArray（Way 未命中） ==会访问，但是返回数据无效==
   - 当 WayLookup 中的信息表明路未命中时，MainPipe 不会向 DataArray 发送读取请求。
   - s0_hits 为低表示缓存未命中
   - toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。
3. 不访问 DataArray（ITLB 查询失败）==会访问，但是返回数据无效==
   - 当 ITLB 查询失败时，MainPipe 不会向 DataArray 发送读取请求。
   - s0_itlb_exception 信号不为零（ITLB 查询失败）。
   - toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。
4. 不访问 DataArray（DataArray 正在进行写操作）
   - 当 DataArray 正在进行写操作时，MainPipe 不会向 DataArray 发送读取请求。
   - toData.last.ready 信号为低，表示 DataArray 正在进行写操作。
   - toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。

### Meta ECC 校验

将物理地址的标签部分与对应的 Meta 进行 ECC 校验，以确保 Meta 的完整性。

1. 无 ECC 错误

- 当 waymask 全为 0（没有命中），则 hit_num 为 0 或 waymask 有一位为 1（一路命中），hit_num 为 1 且 ECC 对比通过（encodeMetaECC(meta) == code）
- s1_meta_corrupt 为假。

2. 单路命中的 ECC 错误

- 当 waymask 有一位为 1（一路命中），ECC 对比失败（encodeMetaECC(meta) != code）
- s1_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。

3. 多路命中
   > hit multi-way, must be an ECC failure

- 当 waymask 有两位及以上为 1（多路命中），视为 ECC 错误。
- s1_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。

4. ECC 功能关闭

- 当奇偶校验关闭时（ecc_enable 为低），强制清除 s1_meta_corrupt 信号置位。
- 不管是否发生 ECC 错误，s1_meta_corrupt 都为假。

### PMP 检查

- 将 S1 的物理地址 s1_req_paddr(i) 和指令 TlbCmd.exec 发往 PMP，判断取指是否合法。
- 防止非法地址，区分普通内存和 MMIO 内存。

1. 没有异常
   - s1_pmp_exception 为全零，表示没有 PMP 异常。
2. 通道 0 有 PMP 异常
   - s1_pmp_exception(0) 为真，表示通道 0 有 PMP 异常。
3. 通道 1 有 PMP 异常
   - s1_pmp_exception(1) 为真，表示通道 1 有 PMP 异常。
4. 通道 0 和通道 1 都有 PMP 异常
   - s1_pmp_exception(0) 和 s1_pmp_exception(1) 都为真，表示通道 0 和通道 1 都有 PMP 异常。
5. 没有映射到 MMIO 区域
   - s1_pmp_mmio（0） 和 s1_pmp_mergemmio（1） 都为假，表示没有映射到 MMIO 区域。
6. 通道 0 映射到了 MMIO 区域
   - s1_pmp_mmio（0） 为真，表示映射到了 MMIO 区域。
7. 通道 1 映射到了 MMIO 区域
   - s1_pmp_mmio（1） 为真，表示映射到了 MMIO 区域。
8. 通道 0 和通道 1 都映射到了 MMIO 区域
   - s1_pmp_mmio（0） 和 s1_pmp_mmio（1） 都为真，表示通道 0 和通道 1 都映射到了 MMIO 区域。

### 异常合并

- 将 s1_itlbmergeption 与 s1_pmp_exception 合并生成 s1_exception_out。
- ITLB 异常通常优先于 PMP 异常。merge

1. 没有异常
   - s1_exception_out 为全零，表示没有异常。
2. 只有 ITLB 异常
   - s1_exception_out 和 s1_itlb_exception 一致
3. 只有 PMP 异常
   - s1_exception_out 和 s1_pmp_exception 一致
4. ITLB 与 PMP 异常同时出现
   > itlb has the highest priority, pmp next
   - s1_exception_out 和 s1_itlb_exception 一致

### MSHR 匹配和数据选择

- 检查当前的请求是否与 MSHR 中正在处理的缺失请求匹配。
- 判断 缓存组索引相同(s1_req_vSetIdx(i) == fromMSHR.bits.vSetIdx) ，物理标签相同 (s1_req_ptags(i) == fromMSHR.bits.blkPaddr)；若匹配 MSHR 有效且没有错误（fromMSHR.valid && !fromMSHR.bits.corrupt），则优先使用 MSHR 中的数据
- 避免重复访问 Data SRAM，提升性能；当 MSHR 中已有重填结果时，可立即命中。

1. 命中 MSHR

- MSHR 中已有正确数据时，S1 阶段能直接拿到
- s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 s1_bankMSHRHit(i)，s1_data_is_from_MSHR(i) 为 true

2. 未命中 MSHR

- MSHR 中存放的地址与当前请求不同，那么应该读取 SRAM 的数据
- s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false

3. MSHR 数据 corrupt

- fromMSHR.bits.corrupt = true，那么 MSHR 将不匹配，应该读取 SRAM 的数据
- s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false

### Data ECC 校验

在 S2 阶段，对从 S1 或 MSHR 获得的数据（如 s2_datas）进行 ECC 校验：

- 若 ECC 校验失败，则标记 s2_data_corrupt(i) = true。
- 若数据来自 MSHR，则不重复进行 ECC 校验（或忽略 corrupt）

1. 无 ECC 错误

- s2_bank 全部没有损坏，bank 也选对了对应的端口和 bank，数据不来自 MSHR
- s2_data_corrupt(i) 为 false，没有 ECC 错误。

2. 单 Bank ECC 错误

- s2_bank_corrupt(bank) 有一个为 true ,即对应的 bank 有损坏；同时 bank 也选对了对应的端口和 bank，数据不来自 MSHR
- s2_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。

3. 多 Bank ECC 错误

- s2_bank_corrupt(bank) 有两个或以上为 true,即对应的 bank 有损坏；同时 bank 也选对了对应的端口和 bank，数据不来自 MSHR
- s2_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。

4. ECC 功能关闭

- 当奇偶校验关闭时（ecc_enable 为低），强制清除 s2_data_corrupt 信号置位。
- 不管是否发生 ECC 错误，s2_data_corrupt 都为假。

### 冲刷 MetaArray

Meta 或者 Data ECC 校验错误时，会冲刷 MetaArray，为重取做准备。

1. 只有 Meta ECC 校验错误
   > if is meta corrupt, clear all way (since waymask may be unreliable)

- 当 s1_meta_corrupt 为真时，MetaArray 的所有路都会被冲刷。
- toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的所有路置位。

2. 只有 Data ECC 校验错误
   > if is data corrupt, only clear the way that has error

- 当 s2_data_corrupt 为真时，只有对应路会被冲刷。
- toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的对应路置位。

3. 同时有 Meta ECC 校验错误和 Data ECC 校验错误

- 处理 Meta ECC 的优先级更高， 将 MetaArray 的所有路冲刷。
- toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的所有路置位。

### 监控 MSHR 匹配与数据更新

- 判断是否命中 MSHR
- 根据 MSHR 是否命中和 s1 阶段是否发射来更新 s2 的数据，s2 的命中状态和 l2 是否损坏

1. MSHR 命中（匹配且本阶段有效）

- MSHR 的 vSetIdx / blkPaddr 与 S2 请求一致， fromMSHR.valid 有效，s2_valid 也有效
- s2_MSHR_match，s2_MSHR_hits 为高，s2_bankMSHRHit 对应 bank 为高
- s1_fire 无效时，s2_datas 更新为 MSHR 的数据，将 s2_data_is_from_MSHR 对应位置位，s2_hits 置位，清除 s2_data_corrupt，l2 的 corrupt 更新为 fromMSHR.bits.corrupt
- s1_fire 有效时，s2_datas 为 s1_datas 的数据，将 s2_data_is_from_MSHR 对应位置为 s1 的 s1_data_is_from_MSHR，s2_hits 置为 s1_hits，清除 s2_data_corrupt，l2 的 corrupt 为 false

2. MSHR 未命中

- MSHR 的 vSetIdx / blkPaddr 与 S2 请求一致， fromMSHR.valid 有效，s2_valid 也有效，至少有一个未达成
- s2_MSHR_hits(i) = false，S2 不会更新 s2_datas，继续保持原先 SRAM 数据或进入 Miss 流程。

### Miss 请求发送逻辑和合并异常

- 通过计算 s2_should_fetch(i) 判断是否需要向 MSHR 发送 Miss 请求：
  - 当出现未命中 (!s2_hits(i)) 或 ECC 错误(s2_meta_corrupt(i) || s2_data_corrupt(i)) 时，需要请求重新获取。
  - 若端口存在异常或处于 MMIO 区域，则不发送 Miss 请求。
- 使用 Arbiter 将多个端口的请求合并后发送至 MSHR。
- 通过 s2_has_send(i) 避免重复请求。
- 将 S2 阶段已有的 ITLB/PMP 异常（s2_exception）与 L2 Cache 报告的 s2_l2_corrupt(i)（封装后为 s2_l2_exception(i)）进行合并。

1. 未发生 Miss

- 当 s2_hits(i) 为高（s2 已经命中），s2 的 meta 和 data 都没有错误，s2 异常，处于 mmio 区域
- 以上条件至少满足一个时，s2_should_fetch(i) 为低，表示不发送 Miss 请求。

2. 单口 Miss

- 当出现未命中 (!s2_hits(i)) 或 ECC 错误(s2_meta_corrupt(i) || s2_data_corrupt(i))，端口不存在异常且未处于 MMIO 区域时，会向 MSHR 发送 Miss 请求。
- toMSHRArbiter.io.in(i).valid = true ，Arbiter 只发送一条 Miss 请求。

3. 双口都需要 Miss

- 同上，但是两个端口都满足 s2_should_fetch 为高的条件。
- toMSHRArbiter.io.in(0).valid、toMSHRArbiter.io.in(1).valid 均为 true，Arbiter 根据仲裁顺序依次发出请求。

4. 重复请求屏蔽

- 当 s1_fire 为高，表示可以进入 s2 阶段,那么 s2 还没有发送 s2_has_send(i) := false.B
- 如果已经有请求发送了，那么对应的 toMSHRArbiter.io.in(i).fire 为高，表示对应的请求可以发送，s2_has_send(i) := true。
- 此时再次发送，toMSHRArbiter.io.in(i).valid 为低，表示发送失败。

5. 仅 ITLB/PMP 异常

- S1 阶段已记录了 ITLB 或 PMP 异常，L2 corrupt = false。
- 2_exception_out 仅保留 ITLB/PMP 异常标记，无新增 AF 异常。

6. 仅 L2 异常

- S2 阶段 s2_l2_corrupt(i) = true，且无 ITLB/PMP 异常。
- s2_exception_out(i) 表示 L2 访问错误(AF)。

7. ITLB + L2 同时出现

- 同时触发 ITLB 异常和 L2 corrupt。
- s2_exception_out 优先保留 ITLB 异常类型，不被 L2 覆盖。

8. s2 阶段取指完成

- s2_should_fetch 的所有端口都为低，表示需要取指，那么取指完成
- s2_fetch_finish 为高

### 响应 IFU

- 若当前周期 S2 成功发射（s2_fire = true）且数据获取完毕（s2_fetch_finish），则把数据、异常信息、物理地址等打包到 toIFU.bits 输出。
- 若为双行请求（s2_doubleline = true），也会向 IFU 发送第二路的信息（地址、异常）。

1. 正常命中并返回

- 不存在任何异常或 Miss，s2 命中，s2 阶段取指完成，外部的 respStall 停止信号也为低 。
- toIFU.valid = true，toIFU.bits.data 为正确的 Cacheline 数据，toIFU.bits.exception、pmp_mmio、itlb_pbmt = none。

2. 异常返回

- 设置 ITLB、PMP、或 L2 corrupt 异常。
- toIFU.bits.exception(i) = 对应异常类型，pmp_mmio、itlb_pbmt 根据是否有对应的异常设置为 true。

3. 跨行取指

- s2_doubleline = true，同时检查第一路、第二路返回情况。
- toIFU.bits.doubleline = true。
- 若第二路正常，toIFU.bits.exception(1) = none；若第二路异常，则 exception(1) 标记相应类型。
- pmp_mmio、itlb_pbmt 类似。

4. RespStall

- 外部 io.respStall = true，导致 S2 阶段无法发射到 IFU。
- s2_fire = false，toIFU.valid 也不拉高，S2 保持原状态等待下一拍（或直到 respStall 解除）。

### L2 Corrupt 报告

- 当检测到 L2 Cache 返回的 corrupt 标记时（s2_l2_corrupt(i) = true），在 S2 完成发射后额外向外部错误接口 io.errors(i) 报告。
- 与 Data ECC 或 Meta ECC 不同，L2 corrupt 由 L2 自己报告给 BEU，这里不需要再次报告给 beu。

1. L2 Corrupt 单路

- s2 阶段准备完成可以发射（s2_fire 为高），s2_MSHR_hits(0)和 fromMSHR.bits.corrupt 为高
- s2_l2_corrupt(0) = true，io.errors(0).valid = true，io.errors(0).bits.source.l2 = true。

2. 双路同时 corrupt

- 端口 0 和端口 1 都从 L2 corrupt 数据中获取。
- s2_l2_corrupt 均为 true，发射后分别报告到 io.errors(0) 和 io.errors(1)。

### 刷新机制

- io.flush：外部的全局刷新信号，它用于指示整个流水线需要被冲刷（清空）。
- s0_flush： S0 阶段内部的刷新信号，它由 io.flush 传递而来，用于控制 S0 阶段的刷新操作。
- s1_flush： S1 阶段内部的刷新信号，它由 io.flush 传递而来，用于控制 S1 阶段的刷新操作。
- s2_flush： S2 阶段内部的刷新信号，它由 io.flush 传递而来，用于控制 S2 阶段的刷新操作。

1. 全局刷新

- io.flush 被激活时，流水线的各个阶段（S0, S1 和 S2）都能正确响应并执行刷新操作。
- io.flush = true。
- s0_flush, s1_flush, s2_flush = true。

2. S0 阶段刷新

- s0_flush = true。
- s0_fire = false。

3. S1 阶段刷新

- s1_flush = true。
- s1_valid， s1_fire = false。

4. S2 阶段刷新

- s2_flush = true。
- s2_valid， toMSHRArbiter.io.in(i).valid ， s2_fire = false