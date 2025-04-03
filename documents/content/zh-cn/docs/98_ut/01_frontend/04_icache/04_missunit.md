---
title: MissUnit
linkTitle: MissUnit
weight: 12
---

<div class="icache-ctx">

</div>

## 子模块：FIFO

- 一个先入先出的循环队列，目前仅在 MissUnit 中有使用，作为优先队列 priorityFIFO。
- 按照在 MissUnit 中的实例化，pipe 是默认值 false，hasflush 是 true。
- 队列的指针都是环形的，分为入队指针（写指针，ent_ptr）和出队指针（读指针，deq_ptr），记录读和写的位置。
- 两个指针都有对应的 flag 位，当指针超过队列大小时，flag 位会翻转，用以判断是否已经循环。
- 在入队、出队对应的 fire（valid && ready） 信号有效时，移动对应的指针。

## FIFO 的功能点和测试点

### 入队操作

1. 队未满，正常入队

- 当队列未满，且空位不小于一时，可以正常入队，如果从零号位开始入队到最大容量，入队指针的 flag 不会翻转。
- io.enq.fire 为高有效，regFiles(enq_ptr.value) = io.enq.bits，enq_ptr.value+1 入队指针移动，入队指针标记位不翻转。
- 重复以上操作至队满。

2. 队未满，入队后标记位翻转

- 当队未满，但是空位却是靠近队尾时，入队一位后就到达了队头，入队指针的 flag 会翻转。
- 队列的容量为 10，入队指针指向 9，队未满。此时如果 io.enq.fire 为高，则 regFiles(9) = io.enq.bits，enq_ptr.value+1（循环队列，加完后 enq_ptr.value=0）入队指针移动，入队指针标记位翻转。

3. 队满，入队就绪信号为低，无法入队

- 当队满时，(enq_ptr.value === deq_ptr.value) && (enq_ptr.flag ^ deq_ptr.flag) 为高，io.enq.ready 为低，io.enq.fire 为低无效。
- 此时入队，入队指针的 value 和 flag 不变。

### 出队操作

1. 队非空，正常出队

- 当队列非空时，可以正常出队，如果出队指针不经过最大容量位置，出队指针的 flag 不会翻转。
- io.deq.fire 为高有效，io.deq.bits = regFiles(deq_ptr.value)，deq_ptr.value+1 出队指针移动，出队指针标记位不翻转。

2. 队非空，出队后标记位翻转

- 当队非空，但是出队指针是靠近队尾时，出队一位后就到达了队头，出队指针的 flag 会翻转。
- 队列的容量为 10，出队指针指向 9，队非空。此时如果 io.deq.fire 为高，则 io.deq.bits = regFiles(9)，deq_ptr.value+1（循环队列，加完后 deq_ptr.value=0）出队指针移动，出队指针标记位翻转。

3. 队空，出队有效信号为低，无法出队

- 当队空时，enq_ptr === deq_ptr 为高，io.deq.valid 为低，io.deq.fire 为低无效。
- 此时出队，出队指针的 value 和 flag 不变。

### 刷新清空操作

1. flush 清空

- 当刷新信号有效时，重置出队和入队的指针和标记位，清空队列。
- 当 flush 为高时，deq_ptr.value=0，enq_ptr.value=0，deq_ptr.flag=false，enq_ptr.flag=false，empty=true,full=false。

## MissUnit

<div>			
    <center>	
    <img src="../missunit_structure.png"
         alt="MissUnit 结构"
         style="zoom:100%"/>
    <br>		
    MissUnit 结构	
    </center>
</div>

<br>

- 接收并管理多个 Miss 请求
  - 处理来自 Fetch 和 Prefetch 的 Miss 请求。
  - 将这些请求分派给适当数量的 MSHR 进行排队和状态管理。
- 管理 MSHR
  - ICacheMissUnit 使用多个 MSHR 来跟踪和管理未完成的缓存未命中请求。为了防止 flush 时取指 MSHR 不能完全释放，设置取指 MSHR 的数量为 4，预取 MSHR 的数量为 10。采用数据和地址分离的设计方法，所有的 MSHR 共用一组数据寄存器，在 MSHR 只存储请求的地址信息、状态等信息。
  - 接收来自 MainPipe 的取指请求和来自 IPrfetchPipe 的预取请求，取指请求只能被分配到 fetchMSHR，预取请求只能分配到 prefetchMSHR，入队时采用低 index 优先的分配方式。
  - 在入队的同时对 MSHR 进行查询，如果请求已经在 MSHR 中存在，就丢弃该请求，对外接口仍表现 fire，只是不入队到 MSHR 中。==在入队时向 Replacer 请求写入 waymask==。当请求完成后，MSHR 会被释放，以便处理新的请求。
- 通过 TileLink 协议与 L2 缓存进行通信，发送获取缓存块的请求（mem_acquire），并接收 L2 缓存的响应（mem_grant）。
  - 当到 L2 的总线空闲时，选择 MSHR 表现进行处理，整体 fetchMSHR 的优先级高于 prefetchMSHR，只有没有需要处理的 fetchMSHR，才会处理 prefetchMSHR。
  - 对于 fetchMSHR，采用低 index 优先的优先级策略，因为同时最多只有两个请求需要处理，并且只有当两个请求都处理完成时才能向下走，所有 fetchMSHR 之间的优先级并不重要。
  - 对于 prefetchMSHR，考虑到预取请求之间具有时间顺序，采用先到先得的优先级策略，在入队时通过一个 FIFO 记录入队顺序，处理时按照入队顺序进行处理。
  - 通过状态机与 Tilelink 的 D 通道进行交互，到 L2 的带宽为 32byte，需要分 2 次传输，并且不同的请求不会发生交织，所以只需要一组寄存器来存储数据。
  - 当一次传输完成时，根据传输的 id 选出对应的 MSHR，从 MSHR 中读取地址、掩码等信息，将相关信息写入 SRAM，同时将 MSHR 释放。
- 向 MetaArray 和 DataArray 发送写请求，向 MainPipe 发送响应
  - 当数据传回后，MissUnit 根据相应的替换策略信息（victim way），将新数据写回 ICache 的 SRAM(Meta/Data) 。
  - 同时向取指端（或预取端）返回“Miss 已完成”的响应，包括：写入了哪一路（way）、实际数据以及可能的校验信息（如 corrupt 标记等）。
- 处理特殊情况（如 flush、fencei、数据损坏等）
  - 遇到 Flush 或 fence.i 等指令时，MissUnit 可以终止或跳过某些 Miss 请求的写回，从而保证不在无效或过期的情况下写入缓存。
  - 数据若出现 corrupt（部分拍损坏），也会在写回或发给前端时进行特殊处理或标记。

过程：

1. fetch_req 和 prefetch_req 分别先经过 DeMultiplexer (Demux)，把请求分发给对应数量的 MSHR。fetch 的 MSHR 和 prefetch 的 MSHR 分成两组，分别处理取指和预取请求。
2. 每个 MSHR 内部会记录当前 Miss 请求的地址、索引、是否已经发出 acquire 等状态。当有其它相同的 miss 请求进来时，可以直接 “ hit MSHR ” 而不用重复创建新的请求。
3. 对于 fetchMSHR，采用低 index 优先的优先级策略；对于 prefetchMSHR，采用先到先得的优先级策略，在入队 prefetchMSHR 前通过一个 priorityFIFO.记录入队顺序，处理时按照入队顺序进行处理。
4. fetchMSHR 发出的请求与 prefetchArb 选出的 prefetchMSHR 通过 acquireArb 合并后，通过 mem_acquire 发送给下一级或外部存储。
5. mem_grant 表示对这一条 Miss 请求的返回数据。需要分多个 beat 收集，直到收满一个 Cacheline。
6. 收集完 Cacheline 数据后，会根据对应 MSHR 的信息向 metaArray 和 dataArray 发起写操作 (meta_write, data_write)，同时向取指端 (fetch_resp) 发送补全后的数据和标记 (waymask 等)。
7. 如果发生 flush 或 fencei，在未发出请求前，请求会被无效化；请求被发出后，会持续阻止新请求进入，已经发出的访问最终会将返回过程走完，但收到的响应并不会回复给 MainPipe 和 IPrefetchPipe，也不会写给 MetaArray 和 DataArray。

Demultiplexer 类
grant:选择第一个 ready（能写）的 mshr，写进去（第 0 到 n 个端口，前面有 ready 的。比如 grant=seq(false,true),grant(1)为 true，表示 1 端口前面有一个 ready 的端口（0 端口））
io.out(i).valid:前 i-1 个 mshr 没有 ready 的,输入的写有效。
io.in.ready := grant.last || io.out.last.ready，给 MissUnit 的 ready 信号有一个有效，那么 MissUnit 给 MSHR 的 ready 信号就有效。

## MissUnit 的功能点和测试点

### 处理取指缺失请求

处理来自 MainPipe 的取指单元的缓存缺失请求，将缺失请求分发到多个 Fetch MSHR 中的一个，避免重复请求。
低索引的请求优先处理。

1. 接受新的取指请求

   - 当新的 fetch miss 与 MSHR 中的已有请求不重复时（通过 io.fetch_req.bits.blkPaddr / vSetIdx 给出具体地址），MissUnit 会将请求分配到一个空闲的 Fetch MSHR 中。
   - 当有新的取指缺失请求到达时（io.fetch_req.valid 为高），且没有命中已有的 MSHR（fetchHit 为低），io.fetch_req.ready 应为高，表示可以接受请求。
   - io.fetch_req.fire 成功握手后，该 MSHR 处于 valid = true 状态，并记录地址。

2. 处理已有的取指请求

   - 当已有取指缺失请求到达时（io.fetch_req.valid 为高），且命中已有的 MSHR（fetchHit 为高），io.fetch_req.ready 应为高，虽然不接受请求，但是表现出来为已经接收请求。
   - fetchDemux.io.in.valid 应为低，fetchDemux.io.in.fire 为低，表示没有新的请求被分发到 MSHR。

3. 低索引的请求优先进入 MSHR
   - Fetch 的请求会通过 fetchDemux 分配到多个 Fetch MSHR，fetchDemux 的实现中，低索引的 MSHR 会优先被分配请求。
   - 当取指请求有多个 io.out(i).read 时，选择其中的第一个，也就是低索引的写入 MSHR，io.chose 为对应的索引。

### 处理预取缺失请求

与 Fetch Miss 类似，但走另一些 MSHR（Prefetch MSHR）。

1. 接受新的预取请求

   - 当新的 prefetch miss 与 MSHR 中的已有请求不重复时（通过 io.prefetch_req.bits.blkPaddr / vSetIdx 给出具体地址），MissUnit 会将请求分配到一个空闲的 Prefetch MSHR 中。
   - 当有新的预取缺失请求到达时（io.prefetch_req.valid 为高），且没有命中已有的 MSHR（prefetchHit 为低），io.prefetch_req.ready 应为高，表示可以接受请求。
   - io.prefetch_req.fire 成功握手后，该 MSHR 处于 valid = true 状态，并记录地址。

2. 处理已有的预取请求

   - 当已有预取缺失请求到达时（io.prefetch_req.valid 为高），且命中已有的 MSHR（prefetchHit 为高），io.prefetch_req.ready 应为高，虽然不接受请求，但是表现出来为已经接收请求。
   - prefetchDemux.io.in.valid 应为低，prefetchDemux.io.in.fire 为低，表示请求被接受但未分发到新的 MSHR。

3. 低索引的请求优先进入 MSHR

   - Prefetch 的请求会通过 prefetchDemux 分配到多个 Prefetch MSHR，prefetchDemux 的实现中，低索引的 MSHR 会优先被分配请求。
   - 当取指请求有多个 io.out(i).read 时，选择其中的第一个，也就是低索引的写入 MSHR，io.chose 为对应的索引。

4. 先进入 MSHR 的优先进入 prefetchArb
   - 从 prefetchDemux 离开后，请求的编号会进入 priorityFIFO，priorityFIFO 会根据进入队列的顺序排序，先进入队列的请求会先进入 prefetchArb。
   - prefetchDemux.io.in.fire 为高，并且 prefetchDemux.io.chosen 有数据时，将其编号写入 priorityFIFO。
   - 在 priorityFIFO 中有多个编号时，出队的顺序和入队顺序一致。
   - 检查 priorityFIFO.io.deq.bit 中的数据即可。

### MSHR 管理与查找

1. MSHR 查找命中逻辑

   - 当新的请求到来时，能够正确查找所有 MSHR，判断请求是否命中已有 MSHR。
   - 当新的请求（取指或预取）到来时，系统遍历所有 MSHR，根据所有 MSHR 的查找信号 allMSHRs(i).io.lookUps(j).hit，检查请求是否已经存在于某个 MSHR 中。
   - 如果命中，则对应的 fetchHit 或 prefetchHit 为高。
   - 对于 prefetchHit 为高，还有一种情况：预取的物理块地址和组索引与取指的相等（(io.prefetch_req.bits.blkPaddr === io.fetch_req.bits.blkPaddr) && (io.prefetch_req.bits.vSetIdx === io.fetch_req.bits.vSetIdx)）并且有取指请求 io.fetch_req.valid 有效时，也算命中

2. MSHR 状态的更新与释放

   - 当请求完成后，也就是来自内存总线的响应完成（D 通道接收完所有节拍），MSHR 能够正确地释放（清除其有效位），以便接收新的请求。
   - TileLink D 通道返回的 source ID ，即 io.mem_grant.bits.source。
   - 无效化信号 allMSHRs(i).io.invalid 为高，对应的 MSHR 的有效位 allMSHRs(i).valid 变为低

### acquireArb 仲裁

预取和取指的 acquire 都会发送给 acquireArb，acquireArb 会选择一个 acquire 发送给 mem_acquire。
acquireArb 使用 chisel 自带的 Arbiter 实现,Arbiter 使用固定优先级仲裁，优先级从编号 0 开始，编号越小优先级越高。

1. acquireArb 仲裁
   - acquireArb 会选择一个 acquire 发送给 mem_acquire。
   - 当有多个 MSHR 同时发出请求时，acquireArb 会根据优先级进行仲裁，选择优先级最高的 MSHR 发送请求。
   - 取指请求总是在 0-3 号，预取请求直接在最后一号，所以取指请求优先级高于预取请求。
   - 当取指 acquire 和预取 acquire 同时发出时，fetchMSHRs(i).io.acquire 和 prefetchMSHRs(i).io.acquire 都有效，仲裁结果 acquireArb.io.out 应该和 fetchMSHRs(i).io.acquire 一致。

### Grant 数据接收与 Refill

在收到 TileLink D 通道数据时收集整行

- 累计 beat 数（readBeatCnt），直到完成一整行 (last_fire)
- 记录 corrupt 标志
- 将完成的请求映射回对应的 MSHR (id_r = mem_grant.bits.source)

1. 正常完整 Grant 流程，readBeatCnt 为 0 时
   - readBeatCnt 初始为 0，refillCycles - 1 也为 0。
   - io.mem_grant.valid 为高（因为 io.mem_grant.ready 默认为高，所以 io.mem_grant.fire 为高只需要 io.mem_grant.valid 为高）且 io.mem_grant.bits.opcpde(0)为高。
   - 此时 respDataReg(0)= io.mem_grant.bits.data
   - readBeatCnt 加一为 1。
2. 正常完整 Grant 流程，readBeatCnt 为 1 时
   - io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高。
   - 此时 respDataReg(1)= io.mem_grant.bits.data
   - readBeatCnt 重置回 0。
   - last_fire 为高。
   - 下一拍 last_fire_r 为高，id_r=io.mem_grant.bits.source。
3. 正常完整 Grant 流程，last_fire_r 为高
   - last_fire_r 为高，并且 id_r 为 0-13 中的一个。
   - 对应的 fetchMSHRs 或者 prefetchMSHRs 会被无效，也就是 fetchMSHRs_i 或 prefetchMSHRs_i-4 的 io_invalid 会被置高。
4. Grant 带有 corrupt 标志
   - io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高，io.mem_grant.bits.corrupt 为高，则 corrupt_r 应为高。
   - 如果 io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高，io.mem_grant.bits.corrupt 为高中有一个不满足，且此时 last_fire_r 为高，则 corrupt_r 重置为低。

### 替换策略更新 (Replacer)

MissUnit 在发出 Acquire 请求时，还会将本次选中的 victim way 对应的索引告诉 io.victim，让替换策略更新其记录（替换策略采用 PLRU）
只有当 Acquire 真正“fire”时，才说明成功替换，replacer 需要更新状态

1. 正常替换更新
   - 当 io.mem.acquire.ready & acquireArb.io.out.valid 同时为高，也就是 acquireArb.io.out.fir 为高时，io.victim.vSetIdx.valid 也为高。
   - io.victim.vSetIdx.bits = 当前 MSHR 请求的 acquireArb.io.out.bits.vSetIdx。
2. 生成 waymask
   - 根据从 L2 返回的 mshr_resp 中 mshr_resp.bits.way 生成 waymask 信息。
   - 返回的 mshr_resp.bits.way 有 16 位，通过独热码生成一位掩码信息，waymask 表示其中哪一路被替换。
   - 生成的 waymask 应该和 mshr_resp.bits.way 一致。

### 写回 SRAM (Meta / Data)

在一条 Miss Request refill 完成时，将新得到的 Cache line 写到 ICache。
生成 io.meta_write 和 io.data_write 的请求，带上 waymask, tag, idx, data 。
生成 io.meta_write.valid 和 io.data_write.valid 信号。

1. 生成 io.meta_write.valid 和 io.data_write.valid 信号
   - 当 grant 传输完成后，经过一拍后，即 last_fire_r 为高，且从 TileLink 返回的 mshr_resp 中的 mshr_resp.valid 为高。
   - 并且此时没有硬件刷新信号和软件刷新信号，也就是 io.flush 和 io.fencei 为低。 在等待 l2 响应的过程中，没有刷新信号
   - 也没有数据 corrupt，即 corrupt_r 为低。
   - 那么 io.meta_write.valid 和 io.data_write.valid 均为高。
2. 正常写 SRAM
   - io.meta_write.bits 的 virIdx、phyTag、waymask、bankIdx、poison 应该正常更新
   - io.data_write.bits 的 virIdx、data、waymask、bankIdx、poison 应该正常更新

### 向 mainPipe/prefetchPipe 发出 Miss 完成响应（fetch_resp）

在完成 refill 后，无论是否要真正写阵列，都会向取指端发送“Miss 请求完成”
更新 io.fetch_resp.valid 和 fetch_resp.bits。

1. 正常 Miss 完成响应
   - 当 grant 传输完成后，经过一拍后，即 last_fire_r 为高，且从 TileLink 返回的 mshr_resp 中的 mshr_resp.valid 为高。
   - 无论此时是否有硬件刷新信号和软件刷新信号， io.fetch_resp.valid 都为高，说明可向取指端发送响应。
   - io.fetch_resp.bits 中的数据更新：
     - io.fetch_resp.bits.blkPaddr = mshr_resp.bits.blkPaddr
     - io.fetch_resp.bits.vSetIdx = mshr_resp.bits.vSetIdx
     - io.fetch_resp.bits.waymask = waymask
     - io.fetch_resp.bits.data = respDataReg.asUInt
     - io.fetch_resp.bits.corrupt = corrupt_r

### 处理 flush / fencei

一旦收到 io.flush 或 io.fencei 时，对未发射的请求可立即取消，对已经发射的请求在拿到数据后也不写 SRAM。

1. MSHR 未发射前 fencei
   - 如果 MSHR 还没有通过 io.acquire.fire 发出请求，就应立即取消该 MSHR（mshr_resp.valid= false），既不发出请求，也不要写 SRAM。
   - 当 io.fencei 为高时，fetchMSHRs 和 prefetchMSHRs 的 io.req.ready 和 io.acquire.valid 均为低，表示请求不发射。
2. MSHR 未发射前 flush
   - 由于 fetchMSHRs 的 io.flush 被直接设置为 false，所以 io.flush 对 fetchMSHRs 无效，但是对 prefetchMSHRs 有效。
   - 当 io.flush 为高时，只能发射 fetchMSHRs 的请求。
3. MSHR 已发射后 flush/fencei
   - 已经发射了请求，之后再有刷新信号，那么等数据回来了但不写 SRAM。
   - 在发射后，io.flush/io.fencei 为高时，等待数据回来，但是写 SRAM 的信号，write_sram_valid、io.meta_write.valid 和 io.data_write.valid 均为低，表示不写 SRAM。
   - 对于 response fetch 无影响。