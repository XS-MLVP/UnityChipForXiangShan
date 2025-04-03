---
title: IPrefetchPipe
linkTitle: IPrefetchPipe
weight: 12
---

<div class="icache-ctx">

</div>

## IPrefetchPipe

IPrefetchPipe 为预取的流水线，三级流水设计，负责预取请求的过滤。

<div>			
    <center>	
    <img src="../iprefetchpipe_structure.png"
         alt="IPrefetchPipe模块结构示意图"
         style="zoom:100%"/>
    <br>		
    IPrefetchPipe结构示意图	
    </center>
</div>

<br>

1. 接收预取请求（s0 阶段）：

- 从 FTQ 或后端接收预取请求。
- 发送读请求到 ITLB 和 MetaArray 缓存元数据模块。

2. 地址转换和缓存检查（s1 阶段）：

- 接收 ITLB 的地址转换结果，处理可能的缺失和重发。
- 从缓存元数据中读取标签和有效位，检查是否命中。
- 进行 PMP 权限检查，合并异常信息。
- 根据情况决定是否发送请求到 WayLookup 模块。

3. 未命中请求处理（s2 阶段）：

- 检查与 missUnit 的交互，更新命中状态。
- 对于无异常的未命中请求，向 missUnit 发送请求以获取数据。
- 控制流水线的推进和刷新，处理可能的阻塞和异常。

### S0 流水级

在 S0 流水级，接收来自 FTQ 的预取请求，向 MetaArray 和 ITLB 发送请求。

- 接收预取请求：从 FTQ 或后端接收预取请求，提取预取请求的虚拟地址、FTQ 索引、是否为软件预取、是否跨缓存行信、虚拟组索引（s0_req_vSetIdx）和后端的异常信息。
- 发送请求到 ITLB：将虚拟地址发送到 ITLB 进行地址转换。
- 发送请求到缓存元数据（Meta SRAM）：将请求发送到缓存的元数据存储器，以便在后续阶段读取缓存标签和有效位。

### S1 流水级

软件预取 enqway 持续一拍...

- 接收 ITLB 的响应：从 ITLB 接收地址转换的结果，包括物理地址 paddr、异常类型(`af`/`pf`)和特殊情况(`pbmt.nc`/`pbmt.io`)。
- 接收缓存元数据的响应并检查缓存命中：从缓存元数据存储器 MetaArray 读取缓存标签 `tag` 和有效位，检查预取地址是否在缓存中已存在，命中结果存入 `waymask` 中。
- 权限检查：使用 PMP 对物理地址进行权限检查，确保预取操作的合法性。
- 异常处理和合并：合并来自后端、ITLB、PMP 的异常信息，准备在后续阶段处理。
- 发送请求到 WayLookup 模块：当条件满足时，将元数据（命中信息 `waymask`、ITLB 信息 `paddr`/`af`/`pf`）发送到 WayLookup 模块，以便进行后续的缓存访问。
- 状态机转换：根据当前状态和条件，更新下一个状态。
  - 状态机初始状态为 `idle`，当 S1 流水级进入新的请求时，首先判断 ITLB 是否缺失，如果缺失，就进入 `itlbResend`；如果 ITLB 命中但命中信息未入队 WayLookup，就进入 `enqWay`；如果 ITLB 命中且 WayLookup 入队但 S2 请求未处理完，就进入 `enterS2`。
  - 在 `itlbResend` 状态，重发 ITLB 请求，此时占用 ITLB 端口，直至请求回填完成，在回填完成的当拍向 MetaArray 再次发送读请求，回填期间可能发生新的写入，如果 MetaArray 繁忙（正在被写入），就进入`metaResend`，否则进入 `enqWay`。
  - 在 `metaResend` 状态，重发 MetaArray 读请求，发送成功后进入 `enqWay`。
  - 在 `enqWay` 状态，尝试将元数据入队 WayLookup，如果 WayLookup 队列已满，就阻塞至 WayLookup 入队成功，另外在 MSHR 发生新的写入时禁止入队，主要是为了防止写入的信息与命中信息所冲突，需要对命中信息进行更新。当成功入队 WayLookup 或者是软件预取时，如果 S2 空闲，就直接进入 `idle`，否则进入 `enterS2`。
  - 在 `enterS2` 状态，尝试将请求流入下一流水级，流入后进入 `idle`。

<div>			<!--块级封装-->
    <center>	<!--将图片和文字居中-->
    <img src="../iprefetchpipe_fsm.png"
         alt="IPrefetchPipe状态机"
         style="zoom:100%"/>
    <br>		<!--换行-->
    IPrefetchPipe S1状态机	<!--标题-->
    </center>
</div>

<br>

### S2 流水级

- 监控 missUnit 的请求：更新 MSHR 的匹配状态。综合该请求的命中结果、ITLB 异常、PMP 异常、meta 损坏，判断是否需要预取，只有不存在异常时才进行预取。
- 发送请求到 missUnit：因为同一个预测块可能对应两个 cacheline，所以通过 Arbiter 依次将请求发送至 MissUnit。

### 命中信息的更新

在 S1 流水级中得到命中信息后，距离命中信息真正在 MainPipe 中被使用要经过两个阶段，分别是在 IPrefetchPipe 中等待入队 WayLookup 阶段和在 WayLookup 中等待出队阶段，在等待期间可能会发生 MSHR 对 Meta/DataArray 的更新，因此需要对 MSHR 的响应进行监听，分为两种情况：

1. 请求在 MetaArray 中未命中，监听到 MSHR 将该请求对应的 cacheline 写入了 SRAM，需要将命中信息更新为命中状态。
2. 请求在 MetaArray 中已经命中，监听到同样的位置发生了其它 cacheline 的写入，原有数据被覆盖，需要将命中信息更新为缺失状态。

为了防止更新逻辑的延迟引入到 DataArray 的访问路径上，在 MSHR 发生新的写入时禁止入队 WayLookup，在下一拍入队。

### 刷新机制

在 IPrefetch 中如果收到后端重定向、IFU 预译码、fencei 带来的刷新，就冲刷整个流水线

IPrefetchPipe 模块中的刷新信号主要来自以下两个方面：

1. 全局刷新信号：由系统的其他模块发出的全局刷新信号，如怀疑流水线中存在错误数据或需要清除流水线时触发。

- io.flush：模块输入的全局刷新信号。当系统需要清除所有流水线阶段的数据时，该信号被置为高。

2. 来自分支预测单元（BPU）的刷新信号：当分支预测错误或需要更新预测信息时，BPU 会发出刷新信号。

- io.flushFromBpu：包含来自 BPU 的刷新信息，指示哪些指令需要被刷新。

## IPrefetchPipe 的功能点和测试点

### 接收预取请求

从 FTQ 接收预取请求，请求可能有效（ io.req.valid 为高），可能无效； IPrefetchPipe 可能处于空闲（ io.req.ready 为高），可能处于非空闲状态。
只有在请求有效且 IPrefetchPipe 处于空闲状态时，预取请求才会被接收（这里暂不考虑 s0 的刷新信号 s0_flush ，默认其为低）。
预取请求分为不同类型，包括硬件预取请求 (isSoftPrefetch = false)和软件预取请求 (isSoftPrefetch = true)。
cacheline 也分为单 cacheline 和双 cacheline。

1. 硬件预取请求：
   预取请求为硬件 (isSoftPrefetch = false)

   1. 预取请求可以继续：
      - 当预取请求有效且 IPrefetchPipe 处于空闲状态时，预取请求应该被接收。
      - s0_fire 信号在没有 s0 的刷新信号（ s0_flush 为低）时，应该被置为高。
   2. 预取请求被拒绝--预取请求无效时：
      - 当预取请求无效时，预取请求应该被拒绝。
      - s0_fire 信号应该被置为低。
   3. 预取请求被拒绝--IPrefetchPipe 非空闲时：
      - 当 IPrefetchPipe 非空闲时，预取请求应该被拒绝。
      - s0_fire 信号应该被置为低。
   4. 预取请求被拒绝--预取请求无效且 IPrefetchPipe 非空闲时：
      - 当预取请求无效且 IPrefetchPipe 非空闲时，预取请求应该被拒绝。
      - s0_fire 信号应该被置为低。
   5. 预取请求有效且为单 cacheline 时：
      - 当预取请求有效且为单 cacheline 时，预取请求应该被接收。
      - s0_fire 为高，s0_doubleline 应该被置低（false）。
   6. 预取请求有效且为双 cacheline 时：
      - 当预取请求有效且为双 cacheline 时，预取请求应该被接收。
      - s0_fire 为高，s0_doubleline 应该被置高（true）。

2. 软件预取请求：
   预取请求为软件 (isSoftPrefetch = true)

   1. 软件预取请求可以继续：
      - 当预取请求有效且 IPrefetchPipe 处于空闲状态时，软件预取请求应该被接收。
      - s0_fire 信号在没有 s0 的刷新信号（ s0_flush 为低）时，应该被置为高。
   2. 软件预取请求被拒绝--预取请求无效时：
      - 当预取请求无效时，软件预取请求应该被拒绝。
      - s0_fire 信号应该被置为低。
   3. 软件预取请求被拒绝--IPrefetchPipe 非空闲时：
      - 当 IPrefetchPipe 非空闲时，软件预取请求应该被拒绝。
      - s0_fire 信号应该被置为低。
   4. 软件预取请求被拒绝--预取请求无效且 IPrefetchPipe 非空闲时：
      - 当预取请求无效且 IPrefetchPipe 非空闲时，软件预取请求应该被拒绝。
      - s0_fire 信号应该被置为低。
   5. 软件预取请求有效且为单 cacheline 时：
      - 当软件预取请求有效且为单 cacheline 时，软件预取请求应该被接收。
      - s0_fire 为高，s0_doubleline 应该被置低（false）。
   6. 软件预取请求有效且为双 cacheline 时：
      - 当软件预取请求有效且为双 cacheline 时，软件预取请求应该被接收。
      - s0_fire 为高，s0_doubleline 应该被置高（true）。

### 接收来自 ITLB 的响应并处理结果

接收 ITLB 的响应，完成虚拟地址到物理地址的转换。
当 ITLB 发生缺失（miss）时，保存请求信息，等待 ITLB 完成后再继续处理。

1. 地址转换完成：

   - 根据 ITLB 的响应，接收物理地址（paddr），并完成地址转换。
   - 处理 ITLB 响应可能在不同周期到达的情况，管理有效信号和数据保持机制，确保正确使用物理地址。

   1. 当 ITLB 正常返回物理地址时：

      - ITLB 在一个周期内成功返回物理地址 paddr，s1_valid 为高。
      - 确认 s1 阶段正确接收到 paddr。

   2. 当 ITLB 发生 TLB 缺失，需要重试时：
      - fromITLB(PortNumber).bits.miss 为高，表示对应通道的 ITLB 发生了 TLB 缺失，需要重发。
      - 重发完成后，后续步骤继续进行，fromITLB(PortNumber).bits.miss 为低。

2. 处理 ITLB 异常：

   - 根据 ITLB 的异常信息，处理可能的异常。pf 缺页、pgf 虚拟机缺页、af 访问错误。

   1. 当 ITLB 发生页错误异常时：
      - s1_itlb_exception 返回的页错误。
      - iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示页错误 pf。
   2. 当 ITLB 发生虚拟机页错误异常时：
      - s1_itlb_exception 返回的虚拟机页错误。
      - iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示虚拟机页错误 pgf。
   3. 当 ITLB 发生访问错误异常时：
      - s1_itlb_exception 返回的访问错误。
      - iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示访问错误 af。

3. 处理虚拟机物理地址（用于虚拟化）：

   - 在虚拟化环境下，处理虚拟机物理地址（gpaddr），确定访问是否针对二级虚拟机的非叶子页表项（isForVSnonLeafPTE）。

   1. 发生虚拟机页错误异常返回虚拟机物理地址（gpaddr）：
      - 发生 pgf 后，需要返回对应的 gpaddr。
      - 只有一个通道发生 pgf 时，返回对应通道的 gpaddr 即可；多个通道发生 pgf 时，返回第一个通道的 gpaddr。
   2. 当访问二级虚拟机的非叶子页表项时：
      - 发生 gpf 后，如果是访问二级虚拟机的非叶子页表项时，需要返回对应的 gpaddr。
      - 只有一个通道发生 pgf 时，返回对应通道的 gpaddr 即可；多个通道发生 pgf 时，返回第一个通道的 gpaddr。

4. 返回基于页面的内存类型 pbmt 信息：
   - TLB 有效时，返回 pbmt 信息。

### 接收来自 IMeta（缓存元数据）的响应并检查缓存命中

从 Meta SRAM 中读取缓存标签和有效位。
将物理地址的标签部分与缓存元数据中的标签比较，确定是否命中。

1. 缓存标签比较和有效位检查：

   - 从物理地址中提取物理标签（ptag），将其与缓存元数据中的标签进行比较，检查所有缓存路（Way）。检查有效位，确保只考虑有效的缓存行。

   1. 缓存未命中（标签不匹配或有效位为假）：
      - 当标签不匹配或者标签匹配，但是有效位为假时，表示缓存未命中。
      - s1_meta_ptags(PortNumber)(nWays) 不等于 ptags(PortNumber) 或者它们相等，但是对应的 s1_meta_valids 为低时，总之返回的 waymasks 为全 0。
   2. 单路缓存命中（标签匹配且有效位为真）：
      - 当标签匹配，且有效位为真时，表示缓存命中。
      - waymasks 对应的位为 1。

### PMP（物理内存保护）权限检查

对物理地址进行 PMP 权限检查，确保预取操作的合法性。
处理 PMP 返回的异常和 MMIO 信息

1.  访问被允许的内存区域
    - itlb 返回的物理地址在 PMP 允许的范围内。
    - s1_pmp_exception(i) 为 none。
2.  访问被禁止的内存区域
    - s1_req_paddr(i) 对应的地址在 PMP 禁止的范围内。
    - s1_pmp_exception(i) 为 af。
3.  访问 MMIO 区域
    - itlb 返回的物理地址在 MMIO 区域。
    - s1_pmp_mmio 为高。

### 异常处理和合并

backend 优先级最高，merge 方法里的异常越靠前优先级越高

合并来自后端、ITLB、PMP 的异常信息，按照优先级确定最终的异常类型。

1.  仅 ITLB 产生异常
    - s1_itlb_exception(i) 为非零，s1_pmp_exception(i) 为零。
    - s1_exception_out(i) 正确包含 ITLB 异常。
2.  仅 PMP 产生异常
    - s1_itlb_exception(i) 为零，s1_pmp_exception(i) 为非零。
    - s1_exception_out(i) 正确包含 PMP 异常。
3.  仅 后端 产生异常
    - s1_itlb_exception(i) 为零，s1_pmp_exception(i) 为零。
    - s1_exception_out(i) 正确包含 后端 异常。
4.  ITLB 和 PMP 都产生异常
    - s1_itlb_exception(i) 和 s1_pmp_exception(i) 都为非零。
    - s1_exception_out(i) 包含 ITLB 异常（优先级更高）。
5.  ITLB 和 后端 都产生异常
    - s1_itlb_exception(i) 和 s1_backendException(i) 都为非零。
    - s1_exception_out(i) 包含 后端 异常（优先级更高）。
6.  PMP 和 后端 都产生异常
    - s1_pmp_exception(i) 和 s1_backendException(i) 都为非零。
    - s1_exception_out(i) 包含 后端 异常（优先级更高）。
7.  ITLB、PMP 和 后端 都产生异常
    - s1_itlb_exception(i)、s1_pmp_exception(i) 和 s1_backendException(i) 都为非零。
    - s1_exception_out(i) 包含 后端 异常（优先级更高）。
8.  无任何异常
    - s1_itlb_exception(i)、s1_pmp_exception(i)、s1_backendException(i) 都为零。
    - s1_exception_out(i) 指示无异常。

### 发送请求到 WayLookup 模块

当条件满足时，将请求发送到 WayLookup 模块，以进行后续的缓存访问。

1.  正常发送请求到 WayLookup
    - toWayLookup.valid 为高，toWayLookup.ready 为高，s1_isSoftPrefetch 为假。
    - 请求成功发送，包含正确的地址、标签、waymask 和异常信息。
2.  WayLookup 无法接收请求
    - toWayLookup.valid 为高，toWayLookup.ready 为假。
    - 状态机等待 WayLookup 准备好，不会错误地推进。
3.  软件预取请求不发送到 WayLookup
    - s1_isSoftPrefetch 为真。
    - toWayLookup.valid 为假，不会发送预取请求到 WayLookup。

### 状态机控制和请求处理流程

使用状态机管理 s1 阶段的请求处理流程。
包括处理 ITLB 重发、Meta 重发、进入 WayLookup、等待 s2 准备等状态

1. 初始为 m_idle 状态：

   1. 正常流程推进，保持 m_idle 状态

   - s1_valid 为高，itlb_finish 为真，toWayLookup.fire 为真，s2_ready 为真。
   - 状态机保持在 m_idle 状态，s1 阶段顺利推进。

   2. ITLB 未完成，需要重发

   - s1_valid 为高，itlb_finish 为假。
   - 状态机进入 m_itlbResend 状态，等待 ITLB 完成。

   3. ITLB 完成，WayLookup 未命中

   - s1_valid 为高，itlb_finish 为真，toWayLookup.fire 为假。
   - 状态机进入 m_enqWay 状态，等待 WayLookup 入队。

2. 初始为 m_itlbResend 状态：
   1. ITLB 命中, MetaArray 空闲，需要 WayLookup 入队
      - itlb_finish 为假，toMeta.ready 为真。
      - 状态机进入 m_enqWay 状态，等待 WayLookup 入队。
   2. ITLB 命中, MetaArray 繁忙，等待 MetaArray 读请求
      - itlb_finish 为假，toMeta.ready 为假。
      - 状态机进入 m_metaResend 状态，MetaArray 读请求
3. 初始为 m_metaResend 状态：

   1. MetaArray 空闲 ，需要 WayLookup 入队
      - toMeta.ready 为真。
      - 状态机进入 m_enqWay 状态，等待 WayLookup 入队。

4. 初始为 m_enqWay 状态：

   1. WayLookup 入队完成或者为软件预取, S2 空闲, 重新进入空闲状态
      - toWayLookup.fire 或 s1_isSoftPrefetch 为真，s2_ready 为假。
      - 状态机进入空闲状态 m_idle。
   2. WayLookup 入队完成或者为软件预取, S2 繁忙，需要 enterS2 状态
      - toWayLookup.fire 或 s1_isSoftPrefetch 为真，s2_ready 为真。
      - 状态机进入 m_enterS2 状态，等待 s2 阶段准备好。

5. 初始为 m_enterS2 状态：
   1. s2 阶段准备好，请求进入下流水级，流入后进入 m_idle 状态
   - s2_ready 为真。
   - 状态机进入空闲状态 m_idle。

### 监控 missUnit 的请求

检查 missUnit 的响应，更新缓存的命中状态和 MSHR 的匹配状态。

1. 请求与 MSHR 匹配且有效：

   - s2_req_vSetIdx 和 s2_req_ptags 与 fromMSHR 中的数据匹配，且 fromMSHR.valid 为高，fromMSHR.bits.corrupt 为假。
   - s2_MSHR_match(PortNumber) 为真, s2_MSHR_hits(PortNumber) 应保持为真

2. 请求在 SRAM 中命中：

   - s2_waymasks(PortNumber) 中有一位为高，表示在缓存中命中。
   - s2_SRAM_hits(PortNumber) 为真,s2_hits(PortNumber) 应为真。

3. 请求未命中 MSHR 和 SRAM：
   - 请求未匹配 MSHR，且 s2_waymasks(PortNumber) 为空。
   - s2_MSHR_hits(PortNumber)、s2_SRAM_hits(PortNumber) 均为假, s2_hits(PortNumber) 为假。

### 发送请求到 missUnit

对于未命中的预取请求，向 missUnit 发送请求，以获取缺失的数据。

1. 确定需要发送给 missUnit 的请求

- 根据命中状态、异常信息、MMIO 信息等，确定哪些请求需要发送到 missUnit（即 s2_miss）。

  1.  请求未命中且无异常，需要发送到 missUnit：

      - s2_hits(PortNumber) 为假(未命中缓存)，s2_exception 无异常，s2_mmio 为假(不是 MMIO 或不可缓存的内存)。
      - s2_miss(PortNumber) 为真，表示需要发送请求到 missUnit。

  2.  请求命中或有异常，不需要发送到 missUnit：

      - s2_hits(i) 为真（已命中）或者 s2_exception 有异常 或者 s2_mmio 为真（MMIO 访问）。
      - s2_miss(i) 为假，不会发送请求到 missUnit。

  3.  双行预取时，处理第二个请求的条件：
      - s2_doubleline 为真，处理第二个请求。
      - 如果第一个请求有异常或 MMIO，s2_miss(1) 应为假，后续请求被取消或处理。

2. 避免发送重复请求，发送请求到 missUnit

- 使用寄存器 has_send 记录每个端口是否已发送请求，避免重复发送。
- 将需要发送的请求通过仲裁器 toMSHRArbiter 发送到 missUnit。

  1.  在 s1_real_fire 时，复位 has_send：

      - s1_real_fire 为高。
      - has_send(PortNumber) 应被复位为假，表示新的请求周期开始。

  2.  当请求成功发送时，更新 has_send：

      - toMSHRArbiter.io.in(PortNumber).fire 为高（请求已发送）。
      - has_send(PortNumber) 被设置为真，表示该端口已发送请求。

  3.  避免重复发送请求：

      - 同一请求周期内，has_send(PortNumber) 为真，s2_miss(PortNumber) 为真。
      - toMSHRArbiter.io.in(PortNumber).valid 为假，不会再次发送请求。

  4.  正确发送需要的请求到 missUnit：

      - s2_valid 为高，s2_miss(i) 为真，has_send(i) 为假。
      - toMSHRArbiter.io.in(i).valid 为高，请求被成功发送。

  5.  仲裁器正确仲裁多个请求：
      - 多个端口同时需要发送请求。
      - 仲裁器按照优先级或设计要求选择请求发送到 missUnit,未被选中的请求在下个周期继续尝试发送。

### 刷新机制

- io.flush: 全局刷新信号，当该信号为高时，所有请求都需要刷新。
- from_bpu_s0_flush：当请求不是软件预取（!s0_isSoftPrefetch, 软件预取请求是由特定的指令触发的，与指令流中的分支预测无关。因此，在处理刷新信号时，对于软件预取请求，通常不受来自 BPU 的刷新信号影响。），且 BPU 指示需要在 Stage 2 或 Stage 3 刷新的请求，由于该请求尚未进入 s1 阶段，因此在 s0 阶段也需要刷新。
- s0_flush：综合考虑全局刷新信号、来自 BPU 的刷新信号，以及 s1 阶段的刷新信号
- from_bpu_s1_flush：当 s1 阶段的请求有效且不是软件预取，且 BPU 指示在 Stage 3 需要刷新，则在 s1 阶段需要刷新。
- io.itlbFlushPipe：当 s1 阶段需要刷新时，该信号用于通知 ITLB 刷新其流水线，以保持一致性。
- s1_flush：综合考虑全局刷新信号和来自 BPU 的刷新信号。
- s2_flush：用于控制 s2 阶段是否需要刷新。

1. 发生全局刷新
   - io.flush 为高。
   - s0_flush、s1_flush、s2_flush 分别为高，所有阶段的请求被正确清除。
2. 来自 BPU 的刷新
   - io.flushFromBpu.shouldFlushByStageX 为真（X 为 2 或 3），且请求不是软件预取。
   - 对应阶段的 from_bpu_sX_flush 为高，sX_flush 为高，阶段请求被刷新。
3. 刷新时状态机复位
   - s1_flush 为高。
   - 状态机 state 被重置为 m_idle 状态。
4. ITLB 管道同步刷新
   - s1_flush 为高。
   - io.itlbFlushPipe 为高，ITLB 被同步刷新。
