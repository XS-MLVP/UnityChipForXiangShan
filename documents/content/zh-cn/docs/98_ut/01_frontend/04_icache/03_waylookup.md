---
title: WayLookup
linkTitle: WayLookup
weight: 12
---

<div class="icache-ctx">

</div>

## WayLookup

<div>			
    <center>	
    <img src="../waylookup_structure_rw.png"
         alt="WayLookup 读写结构"
         style="zoom:40%"/>
    <br>		
    WayLookup 读写结构	
    </center>
</div>

<br>

<div>			
    <center>	
    <img src="../waylookup_structure_update.png"
         alt="WayLookup 更新结构"
         style="zoom:40%"/>
    <br>		
    WayLookup 更新结构	
    </center>
</div>

<br>

- 内部是 FIFO 环形队列结构。暂存 IPrefetchPipe 查询 MetaArray 和 ITLB 得到的元数据，以备 MainPipe 使用。同时监听 MSHR 写入 SRAM 的 cacheline，对命中信息进行更新。
- 通过 readPtr 和 writePtr 来管理读写位置。当有 flush 信号时，读写指针都会被重置。当写入数据时，写指针递增；读取时，读指针递增。需要处理队列的空和满的情况，empty 是读指针等于写指针，而 full 则是两者的值相同且标志位不同。
- 处理 GPF 的部分，有一个 gpf_entry 寄存器，存储 GPF 的相关信息。当写入的数据包含 GPF 异常时，需要将信息存入 gpf_entry，并记录当前的写指针位置到 gpfPtr。当读取的时候，如果当前读指针的位置与 gpfPtr 匹配，并且 gpf_entry 有效，那么就将 GPF 信息一并输出。
- IPrefetchPipe 向其写入 WayLookupInfo 信息（包括 vSetIdx，waymask，ptag，itlb_exception，itlb_pbmt，meta_codes，gpaddr，isForVSnonLeafPTE）。
  - 写入前，需要考虑队列是否已满，以及是否有 GPF 阻塞。如果有 GPF 信息待读取且未被处理，则写入需要等待，防止覆盖 GPF 信息。写入时，如果数据中包含 GPF 异常，就将信息存入 gpf_entry，并更新 gpfPtr。
- MainPipe 从其读出 WayLookupInfo 信息。
  - 在读取上，有两种情况：当队列为空但有写请求时，可以直接将写的数据旁路（bypass）给读端口；否则就从 entries 数组中读取对应读指针的数据。同时，如果当前读的位置存在 GPF 信息，就将 GPF 信息一起输出，并在读取后清除有效位。
- 允许 bypass（当队列为空但有写请求时，可以直接将写的数据旁路给读端口），为了不将更新逻辑的延迟引入到 DataArray 的访问路径上，在 MSHR 有新的写入时禁止出队，MainPipe 的 S0 流水级也需要访问 DataArray，当 MSHR 有新的写入时无法向下走，所以该措施并不会带来额外影响。
- MissUnit 向其写入命中信息。
  - 若是命中则将 waymask 更新 ICacheMissResp 信息（包括 blkPaddr，vSetIdx，waymask，data，corrupt）且 meta_codes 也更新，否则 waymask 清零。更新逻辑与 IPrefetchPipe 中相同，见 [IPrefetchPipe 子模块文档中的“命中信息的更新”](./01_iprefetchpipe.md#命中信息的更新)一节。

### GPaddr 省面积机制

由于 `gpaddr` 仅在 guest page fault 发生时有用，并且每次发生 gpf 后前端实际上工作在错误路径上，后端保证会送一个 redirect（WayLookup flush）到前端（无论是发生 gpf 前就已经预测错误/发生异常中断导致的；还是 gpf 本身导致的），因此在 WayLookup 中只需存储 reset/flush 后第一个 gpf 有效时的 gpaddr。对双行请求，只需存储第一个有 gpf 的行的 `gpaddr。`

在实现上，把 gpf 相关信号（目前只有 `gpaddr`）与其它信号（`paddr`，etc.）拆成两个 bundle，其它信号实例化 nWayLookupSize 个，gpf 相关只实例化一个寄存器。同时另用一个 `gpfPtr` 指针。总计可以节省$(\text{nWayLookupSize}\times2-1)\times \text{GPAddrBits} - \log_2{(\text{nWayLookupSize})} - 1$bit 的寄存器。
当 prefetch 向 WayLookup 写入时，若有 gpf 发生，且 WayLookup 中没有已经存在的 gpf，则将 gpf/gpaddr 写入 `gpf_entry` 寄存器，同时将 `gpfPtr` 设置为此时的 `writePtr。`
当 MainPipe 从 WayLookup 读取时，若 bypass，则仍然直接将 prefetch 入队的数据出队；否则，若 `readPtr === gpfPtr`，则读出 gpf_entry；否则读出全 0。
需要指出：

1. 考虑双行请求，`gpaddr` 只需要存一份（若第一行发生 gpf，则第二行肯定也在错误路径上，不必存储），但 gpf 信号本身仍然需要存两份，因为 ifu 需要判断是否是跨行异常。
2. `readPtr===gpfPtr` 这一条件可能导致 flush 来的比较慢时 `readPtr` 转了一圈再次与 `gpfPtr` 相等，从而错误地再次读出 gpf，但如前所述，此时工作在错误路径上，因此即使再次读出 gpf 也无所谓。
3. 需要注意一个特殊情况：一个跨页的取指块，其 32B 在前一页且无异常，后 2B 在后一页且发生 gpf，若前 32B 正好是 16 条 RVC 压缩指令，则 IFU 会将后 2B 及对应的异常信息丢弃，此时可能导致下一个取指块的 `gpaddr` 丢失。需要在 WayLookup 中已有一个未被 MainPipe 取走的 gpf 及相关信息时阻塞 WayLookup 的入队（即 IPrefetchPipe s1 流水级），见 PR#3719。

## WayLookup 的功能点和测试点

### 刷新操作

- 接收到全局刷新刷新信号 io.flush 后，读、写指针和 GPF 信息都被重置。

1. 刷新读指针

- io.flush 为高时，重置读指针。
- readPtr.value 为 0， readPtr.flag 为 false。

2. 刷新写指针

- io.flush 为高时，重置写指针。
- writePtr.value 为 0， writePtr.flag 为 false。

3. 刷新 GPF 信息

- io.flush 为高时，重置 GPF 信息。
- gpf_entry.valid 为 0， gpf_entry.bits 为 0。

### 读写指针更新

- 读写信号握手完毕之后（io.read.fire/io.write.fire 为高），对应指针加一。
- 因为是在环形队列上，所以超过队列大小后，指针会回到队列头部。

1. 读指针更新

- 当 io.read.fire 为高时，读指针加一。
- readPtr.value 加一。
- 如果 readPtr.value 超过环形队列的大小，readPtr.flag 会翻转。

2. 写指针更新

- 当 io.write.fire 为高时，写指针加一。
- writePtr.value 加一。
- 如果 writePtr.value 超过环形队列的大小，writePtr.flag 会翻转。

### 更新操作

- MissUnit 处理完 Cache miss 后，向 WayLookup 写入命中信息，也就是 update 操作。
- 情况分为两种：
  - 命中：更新 waymask 和 meta_codes。
  - 未命中：重置 waymask。

1. 命中更新

- MissUnit 返回的更新信息和 WayLookup 的信息相同时，更新 waymask 和 meta_codes。
- vset_same 和 ptag_same 为真。
- waymask 和 meta_codes 更新。
- hits 对应位为高。

2. 未命中更新

- vset_same 和 way_same 为真。
- waymask 清零。
- hit 对应位为高。

3. 不更新

- 其他情况下不更新。
- vset_same 为假或者 ptag_same 和 way_same 都为假。
- hits 对应位为低。

### 读操作

- 读操作会根据读指针从环形队列中读取信息。
- 如果达成了绕过条件，优先绕过。

1. Bypass 读

- 队列为空，并且 io.write.valid 写有效时，可以直接读取，而不经过队列。
- empty 和 io.write.valid 都为真。
- io.read.bits = io.write.bits

2. 读信号无效

- 队列为空（readPtr === writePtr）且写信号 io.write.valid 为低。
- io.read.valid 为低，读信号无效。

3. 正常读

- 未达成绕过条件（empty 和 io.write.valid 至少有一个为假）且 io.read.valid 为高。
- 从环形队列中读取信息。
- io.read.bits.entry = entries(readPtr.value)

4. gpf 命中

- io.read.valid 为高，可以读。
- 当 gpf_hits 为高时，从 GPF 队列中读取信息。
- io.read.bits.gpf = gpf_entry.bits

5. gpf 命中且被读取

- io.read.valid 为高，可以读。

  > also clear gpf_entry.valid when it's read

- 当 gpf 命中且被读取其时（io.read.fire 为高），gpf_entry.valid 会被置为 0。

6. gpf 未命中

- io.read.valid 为高，可以读。
- io.read.bits.gpf 清零。

### 写操作

- 写操作会根据写指针从环形队列中读取信息。
- 如果有 gpf 停止，就会停止写。

1. gpf 停止
   > if there is a valid gpf to be read, we should stall write

- gpf 队列数据有效，并且没有被读取或者没有命中，就会产生 gpf 停止，此时写操作会被停止。
- gpf_entry.valid && !(io.read.fire && gpf_hit) 为高时，写操作会被停止（io.write.ready 为低）。

2. 写就绪无效

- 当队列为满（(readPtr.value === writePtr.value) && (readPtr.flag ^ writePtr.flag)）或者 gpf 停止时，写操作会被停止。
- （io.write.ready 为低）

3. 正常写

- 当 io.write.valid 为高时（没满且没有 gpf 停止），写操作会被执行。
- 正常握手完毕 io.write.fire 为高。
- 写信息会被写入环形队列。
- entries(writePtr.value) = io.write.bits.entry。

有 ITLB 异常的写

- 前面与正常写相同，只不过当写信息中存在 ITLB 异常时，会更新 gpf 队列和 gpf 指针。
- 此时如果已经被绕过直接读取了，那么就不需要存储它了。
  - 4. 被绕过直接读取了
    - can_bypass 和 io.read.fire 都为高。
    - gpf_entry.valid 为 false。
    - gpf_entry.bits = io.write.bits.gpf
    - gpfPtr = writePtr
  - 5. 没有被绕过直接读取
    - can_bypass 为低。
    - gpf_entry.valid 为 true。
    - gpf_entry.bits = io.write.bits.gpf
    - gpfPtr = writePtr
