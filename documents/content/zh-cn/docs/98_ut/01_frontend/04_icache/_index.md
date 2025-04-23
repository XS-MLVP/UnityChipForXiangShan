---
title: ICache
linkTitle: ICache
weight: 12
---

**本文档参考[香山 IFU 设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/blob/master/docs/frontend/ICache/index.md)写成**

本次验证对象是昆明湖前端指令缓存（ICache）的模块。验证的代码版本为[XiangShan_20250307_4b2c87ba](https://github.com/OpenXiangShan/XiangShan/tree/4b2c87ba1d7965f6f2b0a396be707a6e2f6fb345)

请注意，本文档撰写的测试点仅供参考，部分测试点需要修改，如能补充或修改测试点，最终获得的奖励可能更高！

# **ICache 说明文档**

<div class="icache-ctx">

## 文档概述

本文档描述 ICache 的模块列表、设计规格、参数列表、功能概述和详述。
<br>
功能概述部分提供 ICache 整体数据流向图和过程。

## 术语说明

| 缩写       | 全称                                           | 中文名称                         | 说明                                                                                                                 |
| ---------- | ---------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| ICache     | Instruction Cache                              | L1 指令缓存                      | 用于存储最近访问过的指令，以减少对主内存的访问次数，从而提高处理速度。                                               |
| DCache     | Data Cache                                     | L1 数据缓存                      | 用于存储最近访问过的数据，以减少对主内存的访问次数，从而提高处理速度。                                               |
| L2 Cache   | Level Two Cache                                | L2 缓存                          | 从主内存中预取指令和数据,作为 iCache 和主内存之间的缓冲区。                                                          |
| ITLB       | Instruction TLB                                | 指令地址转换缓冲                 | 用于将虚拟地址转换为物理地址的缓冲。                                                                                 |
| BPU        | Branch Prediction Unit                         | 分支预测单元                     | 预测程序中的条件分支，以便提前获取和解码后续指令，这样可以减少等待分支结果的时间。                                   |
| FTQ        | Fetch Target Queue                             | 取指目标队列                     | 暂存 BPU 预测的取指目标，并根据这些取指目标给 IFU 发送取指请求。                                                     |
| IFU        | Instruction Fetch Unit                         | 取指单元                         | 进行取指，预译码，分支预测检查，指令扩展和非法检查。                                                                 |
| BEU        | Bus Error Unit                                 | 总线错误单元                     | 总线错误可以使用总线错误单元 (BEU) 对 hart 产生中断。                                                                |
| PF         | Page Fault                                     | 缺页异常                         | 当 CPU 访问的内存地址不在物理内存中时，会触发缺页异常。                                                              |
| GPF        | Guest Page Fault                               | 虚拟机缺页异常                   | 是在虚拟化环境中，客户机（guest）操作系统尝试访问的虚拟地址未能成功映射到物理地址时产生的异常。                      |
| AF         | Access Fault                                   | 访问错误                         | 当 CPU 试图访问一个不允许的物理地址时，会触发访问错误。                                                              |
| PMP        | Physical Memory Protection                     | 物理内存保护模块                 | RISC-V 架构中提供的一种硬件机制，用于控制不同内存区域的读、写和执行权限，主要目的是提供对物理内存的保护和隔离。      |
| PMA        | Physical Memory Attribute                      | 物理内存属性模块（PMP 的一部分） | RISC-V 系统中，机器物理地址空间的每个区域的这些属性和能力称为物理内存属性。                                          |
| PBMT       | Page-Base Memory Type                          | 基于页面的内存类型               | 一种内存管理机制，它使用分页（paging）技术来管理虚拟内存。见特权手册 Svpbmt 扩展。                                   |
| MMIO       | Memory-Mapped Input/Output                     | 内存映射输入/输出                | 在 MMIO 中，外设的寄存器和内存被映射到同一个地址空间。                                                               |
| cacheline  | cacheline                                      | 缓存行                           | 缓存中的最小存储单位。                                                                                               |
| MetaArray  | MetaArray                                      | 元数据数组                       | 用于存储指令的元数据信息，包括指令的地址、访问权限、是否有效等。                                                     |
| DataArray  | DataArray                                      | 数据数组                         | 用于存储指令数据的数组。                                                                                             |
| SRAM       | Static Random Access Memory                    | 静态随机存取存储器               | 一种用于存储数据的存储器，具有随机访问特性。                                                                         |
| MSHR       | Miss Status Holding Register                   | 缺失状态保持寄存器               | 用来处理非阻塞缓存（non-blocking cache）中的缓存未命中（cache miss）情况 。                                          |
| SATP       | Supervisor Address Translation and Protection  | 监管者地址转换和保护单元         | 管理地址转换和保护机制，它决定了虚拟地址到物理地址的转换方式以及访问权限的控制。                                     |
| VS         | Virtual Supervisor                             | 虚拟监管者                       | 是 H 扩展引入的一种特权模式，用于运行虚拟机中的操作系统。包括两级地址翻译，虚拟 CSR 和异常和中断虚拟化等机制。       |
| hartID     | hardware thread ID                             | 硬件线程标识                     | RISC-V 硬件线程 ID。在 RISC-V 架构中，每个处理器核心都有一个唯一的 hart ID，用于区分同一处理器中运行的多个硬件线程。 |
| SFENCE.VMA | Supervisor Memory-Management Fence Instruction | 监管者内存管理屏障指令           | 同步对内存中内存管理数据结构的更新与当前执行的指令。                                                                 |
| fence.i    | fence.i                                        | 屏障指令                         | 用于同步指令流与数据流，确保在指令之前的存储操作对后续取指可见。                                                     |
|FDIP|Fetch-directed instruction prefetching |取指导向指令预取|通过在分支预测单元和取指单元之间引入一个取指目标队列（Fetch Target Queue，FTQ），将两者解耦。分支预测单元会预测未来的控制流，并将预测的分支目标地址存入FTQ。取指单元则根据FTQ中的地址信息，提前从更高级别的缓存或内存中获取指令块，并将其放入一个全相联的缓冲区中，以便与L1指令缓存并行访问。|

## ICache 和 DCache 区别

### 功能用途

ICache 专门用于存储指令。当 CPU 从内存中读取指令时，这些指令会先被存储在 ICache 中。这样，当 CPU 需要再次执行相同的指令时，可以直接从 ICache 中读取，而无需再次访问速度较慢的内存，从而提高指令的读取速度，加快程序的执行效率。

DCache 用于存储数据。程序运行过程中，CPU 需要频繁地读取和写入数据。DCache 的作用就是缓存这些数据，使得 CPU 对数据的访问速度更快。当 CPU 访问内存中的数据时，如果数据已经在 DCache 中，就可以直接从 DCache 中读取或写入，减少了访问内存的次数，提高了数据访问的效率。

### 数据一致性问题

ICache 通常不需要考虑数据一致性问题。因为**指令是只读的**，一旦程序开始运行，指令的内容一般不会改变。所以，ICache 中的指令可以一直使用，直到程序结束或者新的指令被加载进来。即使内存中的指令被修改了，也不会影响 ICache 中已经缓存的指令的执行。

DCache 数据一致性是一个重要的问题。因为数据可能会被多个处理器或者设备访问和修改。如果一个处理器修改了 DCache 中的数据，而其他处理器或者设备仍然使用旧的数据，就会导致数据不一致的问题。为了保证数据一致性，需要采用一些机制，如缓存一致性协议（如 MESI 协议等），来确保所有处理器和设备看到的数据是一致的。

为什么我们需要区分数据和指令呢？原因之一是出于性能的考量。CPU 在执行程序时，可以同时获取指令和数据，做到硬件上的并行，提升性能。另外，指令和数据有很大的不同。例如，指令一般不会被修改，所以 iCache 在硬件设计上是可以是只读的，这在一定程度上降低硬件设计的成本。所以硬件设计上，系统中一般存在 L1 dCache 和 L1 iCache，L2 Cache 和 L3 Cache。

### 区分原因

指令访问模式是：通常按照程序的顺序依次执行，具有较高的局部性。并且在程序运行过程中通常是只读的，不会被修改。
数据访问模式是：数据的访问通常较为随机，可能涉及频繁的读写操作。数据需要支持读写操作，这意味着 DCache 需要处理数据的写入和一致性问题。

将数据和指令分开存储到 DCache 和 ICache，有利于提高命中率和减少冲突，提升性能（CPU 在执行程序时，可以同时获取指令和数据，做到硬件上的并行），简化设计（ICache 可以专注读指令，而 DCache 需要数据的读写操作，还需要考虑数据一致性问题）。

## 为什么需要预取

预取是 CPU 用来提高执行性能的一种技术，它在实际需要之前将指令或数据从原来存储在较慢内存中的位置取到较快的本地内存中（因此称为 "预取"）。

<div>			
    <center>	
    <img src="difference between cpu and memory.png"
         alt="CPU 和内存的性能差异"
         style="zoom:100%"/>
    <br>		<!--换行-->
    CPU 和内存的性能差异	<!--标题-->
    </center>
</div>

<br>

由处理器和内存之前的性能差异越来大，所以我们需要预取。<br>
从上图可以看出，1980年至2015年间，CPU的性能提升了将近一万倍，可是内存相关的性能只提升了十倍。如果等CPU需要执行相关指令或者需要修改数据的时候再从内存中去读取，那么大部分时间都会花费在等待数据上，这是不可容忍的。这时预取的重要性就体现了，把将要访问的内容提前从内存搬移到Cache中，CPU就可以即时拿到所需的内容，避免了等待。当然，如果预取做得不好，是有可能导致性能下降的，由于Cache的大小是很宝贵的，如果预取判断出错，预取的是无用的数据，然后反而把Cache中后续有可能还会用到的数据给Evict了，那么会增加系统的功耗，减低性能。

## 模块列表

| 子模块                            | 描述                                          |
| --------------------------------- | --------------------------------------------- |
| [MainPipe](02_mainpipe)           | 主流水线                                      |
| [IPrefetchPipe](01_iprefetchpipe) | 预取流水线                                    |
| [WayLookup](03_waylookup)         | 元数据缓冲队列                                |
| [MetaArray](06_icache)            | 元数据 SRAM                                   |
| [DataArray](06_icache)            | 数据 SRAM                                     |
| [MissUnit](04_missunit)           | 缺失处理单元                                  |
| [Replacer](06_icache)             | 替换策略单元                                  |
| [CtrlUnit](05_ctrlunit)           | 控制单元，目前仅用于控制错误校验/错误注入功能 |
| [ICache](06_icache)               | ICache 顶层模块                               |
| [FIFO](04_missunit)               | 先入先出循环队列，在 MissUnit 中有使用        |

## 设计规格

- 缓存指令数据
- 缺失时通过 tilelink 总线向 L2 请求数据
- 软件维护 L1 I/D Cache 一致性（`fence.i`）
- 支持跨 cacheline （预）取指请求
- 支持冲刷（bpu redirect、backend redirect、`fence.i`）
- 支持预取指请求
  - 硬件预取为 FDIP 预取算法
  - 软件预取为 Zicbop 扩展`prefetch.i`指令
- 支持可配置的替换算法
- 支持可配置的缺失状态寄存器数量
- 支持检查地址翻译错误、物理内存保护错误
- 支持错误检查 & 错误恢复 & 错误注入[^ecc]
  - 默认采用 parity code
  - 通过从 L2 重取实现错误恢复
  - 软件可通过 MMIO 空间访问的错误注入控制寄存器
- DataArray 支持分 bank 存储，细存储粒度实现低功耗

[^ecc]: 本文档也将错误检查 & 错误恢复 & 错误注入相关功能称为 ECC，见 [ECC](#ecc) 一节开始的说明。

## 参数列表

若和 chisel 代码不一致，以 chisel 代码为准。

| 参数                | 默认值 | 描述                                                  | 要求                                 |
| ------------------- | ------ | ----------------------------------------------------- | ------------------------------------ |
| nSets               | 256    | SRAM set 数量                                         | 2 的幂次                             |
| nWays               | 4      | SRAM way 数量                                         |                                      |
| nFetchMshr          | 4      | 取指 MSHR 的数量                                      |                                      |
| nPrefetchMshr       | 10     | 预取 MSHR 的数量                                      |                                      |
| nWayLookupSize      | 32     | WayLookup 深度，同时可以反压限制预取最大距离          |                                      |
| DataCodeUnit        | 64     | 校验单元大小，单位为 bit，每 64bit 对应 1bit 的校验位 |                                      |
| ICacheDataBanks     | 8      | cacheline 划分 bank 数量                              |                                      |
| ICacheDataSRAMWidth | 66     | DataArray 基本 SRAM 的宽度                            | 大于每 bank 的 data 和 code 宽度之和 |

## 功能概述

<div>			<!--块级封装-->
    <center>	<!--将图片和文字居中-->
    <img src="ftq_pointer.png"
         alt="FTQ 指针示意"
         style="zoom:100%"/>
    <br>		<!--换行-->
    FTQ 指针示意	<!--标题-->
    </center>
</div>

<br>

FTQ 中存储着 BPU 生成的预测块，fetchPtr 指向取指预测块，prefetchPtr 指向预取预测块，当复位时 prefetchPtr 与 fetchPtr 相同，每成功发送一次取指请求时 fetchPtr++，每成功发送一次预取请求时 prefetchPtr++。详细说明见[FTQ 设计文档](https://github.com/OpenXiangShan/XiangShan-Design-Doc/blob/master/docs/frontend/FTQ/index.md)。

<div>			
    <center>	
    <img src="icache_structure.png"
         alt="ICache整体数据流向图"
         style="zoom:100%"/>
    <br>		
    ICache整体数据流向图	
    </center>
</div>

<br>

ICache 结构如上图所示，有 MainPipe 和 IPrefetchPipe 两个流水线，MainPipe 接收来自 FTQ 的取指请求，IPrefetchPipe 接收来自 FTQ/MemBlock 的硬/软件预取请求。

- 对于预取请求，IPrefetch 对 MetaArray 进行查询，将元数据（在哪一路命中、ECC 校验码、是否发生异常等）存储到 WayLookup 中，如果该请求缺失，就发送至 MissUnit 进行预取。
- 对于取指请求，MainPipe 首先从 WayLookup 中读取命中信息，如果 WayLookup 中没有可用信息，MainPipe 就会阻塞，直至 IPrefetchPipe 将信息写入 WayLookup 中，该方案将 MetaArray 和 DataArray 的访问分离，一次只访问 DataArray 单路，代价是产生了一个周期的重定向延迟。

- MissUnit 处理来自 MainPipe 的取指请求和来自 IPrefetchPipe 的预取请求，通过 MSHR 进行管理，所有 MSHR 公用一组数据寄存器以减少面积。

- CtrlUnit 主要负责 ECC 校验使能/错误注入等功能。从 MetaArray 读取元数据，之后向 MetaArray 写入毒化的标签，向 DataArray 写入毒化的数据。Tilelink 用于外部配置和状态监控，通过 eccctrl 和 ecciaddr 寄存器实现读写交互。

- Replacer 为替换器，采用 PLRU 替换策略，接收来自 MainPipe 的命中更新，向 MissUnit 提供写入的 waymask。

- MetaArray 分为奇偶两个 bank，用于支持跨 cacheline 的双行访问。

- DataArray 中的 cacheline 分为 8 个 bank 存储，每个 bank 中存储的有效数据为 64bit，另外对于每 64bit 还需要 1bit 的校验位，由于 65bit 宽度的 SRAM 表现不好，所以选用深度 256\*宽度 66bit 的 SRAM 作为基本单元，一共有 32 个这样的基本单元。一次访问需要 34Byte 的指令数据，每次需要访问 5 个 bank($8\times 5 > 34$)，根据起始地址进行选择。

## 功能详述

### 取指/预取指请求

<div>			
    <center>	
    <img src="icache_stages.png"
         alt="ICache 两条流水线的关系"
         style="zoom:100%"/>
    <br>		
    ICache 两条流水线的关系	
    </center>
</div>

<br>

FTQ 分别把取指/预取指请求发送到对应的取指/预取指流水线进行处理。如前所述，由 IPrefetch 对 MetaArray 和 ITLB 进行查询，将元数据（在哪一路命中、ECC 校验码、是否发生异常等）在 IPrefetchPipe s1 流水级存储到 WayLookup 中，以供 MainPipe s0 流水级读取。

在上电解复位/重定向时，由于 WayLookup 为空，而 FTQ 的 prefetchPtr、fetchPtr 复位到同一位置，MainPipe s0 流水级不得不阻塞等待 IPrefetchPipe s1 流水级的写入，这引入了一拍的额外重定向延迟。但随着 BPU 向 FTQ 填充预测块的进行和 MainPipe/IFU 因各种原因阻塞（e.g. miss、IBuffer 满），IPrefetchPipe 将工作在 MainPipe 前（`prefetchPtr > fetchPtr`），而 WayLookup 中也会有足够的元数据，此时 MainPipe s0 级和 IPrefetchPipe s0 级的工作将是并行的。

详细的取指过程见[MainPipe](02_mainpipe)、[IPrefetchPipe](01_iprefetchpipe)和[WayLookup](03_waylookup)。

#### 硬件预取与软件预取

V2R2 后，ICache 可能接受两个来源的预取请求：

1. 来自 Ftq 的硬件预取请求，基于 FDIP 算法。
2. 来自 Memblock 中 LoadUint 的软件预取请求，其本质是 Zicbop 扩展中的 prefetch.i 指令，请参考 RISC-V CMO 手册。

然而，PrefetchPipe 每周期仅可以处理一个预取请求，故需要进行仲裁。ICache 顶层负责缓存软件预取请求，并与来自 Ftq 的硬件预取请求二选一送往 PrefetchPipe，软件预取请求的优先级高于硬件预取请求。

逻辑上来说，每个 LoadUnit 都有可能发出软件预取请求，因此每周期至多会有 LoadUnit 数量（目前默认参数为 LduCnt=3）个软件预取请求。但出于实现成本和性能收益考量，ICache 每周期至多仅接收并处理一个，多余的会被丢弃，端口下标最小的优先。此外，若 PrefetchPipe 阻塞，而 ICache 内已经缓存了一个软件预取请求，那么原先的软件预取请求将被覆盖。

<div>			
    <center>	
    <img src="prefetch_mux.png"
         alt="ICache 预取请求接收与仲裁"
         style="zoom:100%"/>
    <br>		
    ICache 预取请求接收与仲裁	
    </center>
</div>

<br>
发送到 PrefetchPipe 后，软件预取请求的处理和硬件预取请求的处理几乎是一致的，除了：

- 软件预取请求不会影响控制流，即**不会**发送到 MainPipe（和后续的 Ifu、IBuffer 等环节），仅做：1) 判断是否 miss 或异常；2) 若 miss 且无异常，发送到 MissUnit 做预取指并重填 SRAM。

关于 PrefetchPipe 的细节请查看子模块文档。

### 异常传递/特殊情况处理

ICache 负责对取指请求的地址进行权限检查（通过 ITLB 和 PMP），可能的异常和特殊情况有：

| 来源     | 异常       | 描述                         | 处理                                                                                                                           |
| -------- | ---------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| ITLB     | af         | 虚拟地址翻译过程出现访问错误 | 禁止取指，标记取指块为 af，经 IFU、IBuffer 发送到后端处理                                                                      |
| ITLB     | gpf        | 客户机页错误                 | 禁止取指，标记取指块为 gpf，经 IFU、IBuffer 发送到后端处理，将有效的 `gpaddr` 和 `isForNonLeafPTE`发送到后端的 GPAMem 以备使用 |
| ITLB     | pf         | 页错误                       | 禁止取指，标记取指块为 pf，经 IFU、IBuffer 发送到后端处理                                                                      |
| backend  | af/pf/gpf  | 同 ITLB 的 af/pf/gpf         | 同 ITLB 的 af/pf/gpf                                                                                                           |
| PMP      | af         | 物理地址无权限访问           | 同 ITLB af                                                                                                                     |
| MissUnit | L2 corrupt | L2 cache 响应 corrupt        | 标记取指块为 af，经 IFU、IBuffer 发送到后端处理                                                                                |

需要指出，对于一般的取指流程来说，并不存在 backend 异常这一项。但 XiangShan 出于节省硬件资源的考虑，在前端传递的 pc 只有 41 / 50 bit（Sv39*4 / Sv48*4），而对于 `jr`、`jalr` 等指令，跳转目标来源于 64 bit 寄存器。根据 RISC-V 规范，高位非全 0 或全 1 时的地址不合法，需要引发异常，这一检查只能由后端完成，并随同后端重定向信号一起发送到 Ftq，进而随同取指请求一起发送到 ICache。其本质是一种 ITLB 异常，因此解释描述和处理方式与 ITLB 相同。

另外，L2 cache 通过 tilelink 总线响应 corrupt 可能是 L2 ECC 错误（`d.corrupt`），亦可能是无权限访问总线地址空间导致拒绝访问（`d.denied`）。tilelink 手册规定，当拉高 `d.denied` 时必须同时拉高 `d.corrupt`。而这两种情况都需要将取指块标记为 access fault，因此目前在 ICache 中无需区分这两种情况（即无需关注 `d.denied`，其可能被 chisel 自动优化掉而导致 verilog 中看不到）。

这些异常间存在优先级：backend 异常 > ITLB 异常 > PMP 异常 > MissUnit 异常。这是自然的：

1. 当出现 backend 异常时，发送到前端的 vaddr 不完整且不合法，故 ITLB 地址翻译过程无意义，检查出的异常无效；
2. 当出现 ITLB 异常时，翻译得到的 paddr 无效，故 PMP 检查过程无意义，检查出的异常无效；
3. 当出现 PMP 异常时，paddr 无权限访问，不会发送（预）取指请求，故不会从 MissUnit 得到响应。

而对于 backend 的三种异常、ITLB 的三种异常，由 backend 和 ITLB 内部进行有优先级的选择，保证同时至多只有一种拉高。

此外，一些机制还会引发一些特殊情况，在旧版文档/代码中也称为异常，但其实际上并不引发 RISC-V 手册定义的 `exception`，为了避免混淆，此后将称为特殊情况：

| 来源     | 特殊情况  | 描述                                        | 处理                                                     |
| -------- | --------- | ------------------------------------------- | -------------------------------------------------------- |
| PMP      | mmio      | 物理地址为 mmio 空间                        | 禁止取指，标记取指块为 mmio，由 IFU 进行**非推测性**取指 |
| ITLB     | pbmt.NC   | 页属性为不可缓存、幂等                      | 禁止取指，由 IFU 进行**推测性**取指                      |
| ITLB     | pbmt.IO   | 页属性为不可缓存、非幂等                    | 同 pmp mmio                                              |
| MainPipe | ECC error | 主流水检查发现 MetaArray/DataArray ECC 错误 | 见[ECC 一节](#ecc)，旧版同 ITLB af，新版做自动重取       |

### DataArray 分 bank 的低功耗设计

目前，ICache 中每个 cacheline 分为 8 个 bank，bank0-7。一个取指块需要 34B 指令数据，故一次访问连续的 5 个 bank。存在两种情况：

1. 这 5 个 bank 位于单个 cacheline 中（起始地址位于 bank0-3）。假设起始地址位于 bank2，则所需数据位于 bank2-6。如下图 a。
2. 跨 cacheline（起始地址位于 bank4-7）。假设起始地址位于 bank6，则数据位于 cacheline0 的 bank6-7、cacheline1 的 bank0-2。有些类似于环形缓冲区。如下图 b。

<div>			
    <center>	
    <img src="dataarray_bank.png"
         alt="DataArray 分 bank 示意图"
         style="zoom:100%"/>
    <br>		
    DataArray 分 bank 示意图	
    </center>
</div>

<br>

当从 SRAM 或 MSHR 中获取 cacheline 时，根据地址将数据放入对应的 bank。

由于每次访问只需要 5 个 bank 的数据，因此 ICache 到 IFU 的端口实际上只需要一个 64B 的端口，将两个 cacheline 各自的 bank 选择出来并拼接在一起返回给 IFU（在 DataArray 模块内完成）；IFU 将这一个 64B 的数据复制一份拼接在一起，即可直接根据取指块起始地址选择出取指块的数据。不跨行/跨行两种情况的示意图如下：

<div>			
    <center>	
    <img src="dataarray_bank_read_singleline.png"
         alt="DataArray 单行数据返回示意图"
         style="zoom:100%"/>
    <br>		
    DataArray 单行数据返回示意图	
    </center>
</div>

<br>

<div>			
    <center>	
    <img src="dataarray_bank_read_multiline.png"
         alt="DataArray 双行数据返回示意图"
         style="zoom:100%"/>
    <br>		
    DataArray 双行数据返回示意图	
    </center>
</div>

<br>

亦可参考 [IFU.scala 中的注释](https://github.com/OpenXiangShan/XiangShan/blob/fad7803d97ed4a987a743036cec42d1c07b48e2e/src/main/scala/xiangshan/frontend/IFU.scala#L474-L502)。

```markdown
NOTE: the following `Cat(_data, _data)` _is_ intentional.
Explanation:
In the old design, IFU is responsible for selecting requested data from two adjacent cachelines,
so IFU has to receive 2*64B (2cacheline * 64B) data from ICache, and do `Cat(_data(1), _data(0))` here.
However, a fetch block is 34B at max, sending 2*64B is quiet a waste of power.
In current design (2024.06~), ICacheDataArray is responsible for selecting data from two adjacent cachelines,
so IFU only need to receive 40B (5bank * 8B) valid data, and use only one port is enough.
For example, when pc falls on the 6th bank in cacheline0(so this is a doubleline request):
MSB LSB
cacheline 1 || 1-7 | 1-6 | 1-5 | 1-4 | 1-3 | 1-2 | 1-1 | 1-0 ||
cacheline 0 || 0-7 | 0-6 | 0-5 | 0-4 | 0-3 | 0-2 | 0-1 | 0-0 ||
and ICacheDataArray will respond:
fromICache.bits.data || 0-7 | 0-6 | xxx | xxx | xxx | 1-2 | 1-1 | 1-0 ||
therefore simply make a copy of the response and `Cat` together, and obtain the requested data from centre:
f2_data_2_cacheline || 0-7 | 0-6 | xxx | xxx | xxx | 1-2 | 1-1 | 1-0 | 0-7 | 0-6 | xxx | xxx | xxx | 1-2 | 1-1 | 1-0 ||
requested data: ^-----------------------------^
For another example, pc falls on the 1st bank in cacheline 0, we have:
fromICache.bits.data || xxx | xxx | 0-5 | 0-4 | 0-3 | 0-2 | 0-1 | xxx ||
f2_data_2_cacheline || xxx | xxx | 0-5 | 0-4 | 0-3 | 0-2 | 0-1 | xxx | xxx | xxx | 0-5 | 0-4 | 0-3 | 0-2 | 0-1 | xxx ||
requested data: ^-----------------------------^
Each "| x-y |" block is a 8B bank from cacheline(x).bank(y)
Please also refer to:

- DataArray selects data:
  https://github.com/OpenXiangShan/XiangShan/blob/d4078d6edbfb4611ba58c8b0d1d8236c9115dbfc/src/main/scala/xiangshan/frontend/icache/ICache.scala#L355-L381
  https://github.com/OpenXiangShan/XiangShan/blob/d4078d6edbfb4611ba58c8b0d1d8236c9115dbfc/src/main/scala/xiangshan/frontend/icache/ICache.scala#L149-L161
- ICache respond to IFU:
  https://github.com/OpenXiangShan/XiangShan/blob/d4078d6edbfb4611ba58c8b0d1d8236c9115dbfc/src/main/scala/xiangshan/frontend/icache/ICacheMainPipe.scala#L473
```

### 冲刷

在后端/IFU 重定向、BPU 重定向、`fence.i` 指令执行时，需要视情况对 ICache 内的存储结构和流水级进行冲刷。可能的冲刷目标/动作有：

1. MainPipe、IPrefetchPipe 所有流水级
   - 冲刷时直接将 `s0/1/2_valid` 置为 `false.B` 即可
2. MetaArray 中的 valid
   - 冲刷时直接将 `valid` 置为 `false.B` 即可
   - `tag`、`code`不需要冲刷，因为它们的有效性由 `valid` 控制
   - DataArray 中的数据不需要冲刷，因为它们的有效性由 MetaArray 中的 `valid` 控制
3. WayLookup
   - 读写指针复位
   - `gpf_entry.valid` 置为 `false.B`
4. MissUnit 中所有 MSHR
   - 若 MSHR 尚未向总线发出请求，请求和预取请求直接置无效（`valid === false.B`）
   - 若 MSHR 已经向总线发出请求，记录待冲刷（`flush === true.B` 或 `fencei === true.B`），等到 d 通道收到 grant 响应时再置无效，同时不把 grant 的数据回复给 MainPipe/PrefetchPipe，也不写入 SRAM
         - 需要留意，当 d 通道收到 grant 响应的同时收到冲刷（`io.flush === true.B` 或 `io.fencei === true.B`）时，MissUnit 同样不写入 SRAM，但**会**将数据回复给 MainPipe/PrefetchPipe，避免将端口的延时引入响应逻辑中，此时 MainPipe/PrefetchPipe 也同步收到了冲刷请求，因此会将数据丢弃

每种冲刷原因需要执行的冲刷目标：

| 冲刷原因        | 1                       | 2   | 3                       | 4   |
| --------------- | ----------------------- | --- | ----------------------- | --- |
| 后端/IFU 重定向 | Y                       |     | Y                       | Y   |
| BPU 重定向      | Y[^redirect_tab_bpu]    |     |                         |     |
| `fence.i`       | Y[^redirect_tab_fencei] | Y   | Y[^redirect_tab_fencei] | Y   |

[^redirect_tab_bpu]:
    BPU 精确预测器（BPU s2/s3 给出结果）可能覆盖简单预测器（BPU s0 给出结果）的预测，显然其重定向请求最晚在预取请求的 1- 2 拍之后就到达 ICache，因此仅需要：

    BPU s2 redirect：冲刷 IPrefetchPipe s0

    BPU s3 redirect：冲刷 IPrefetchPipe s0/1

    当 IPrefetchPipe 的对应流水级中的请求来自于软件预取时 `isSoftPrefetch === true.B`，不需要进行冲刷

    当 IprefetchPipe 的对应流水级中的请求来自于硬件预取，但 `ftqIdx` 与冲刷请求不匹配时，不需要进行冲刷

[^redirect_tab_fencei]: `fence.i` 在逻辑上需要冲刷 MainPipe 和 IPrefetchPipe（因为此时流水级中的数据可能无效），但实际上`io.fencei`拉高必然伴随一个后端重定向，因此目前的实现中没有冲刷 MainPipe 和 IPrefetchPipe 的必要。

ICache 进行冲刷时不接收取指/预取请求（`io.req.ready === false.B`）

#### 对 ITLB 的冲刷

ITLB 的冲刷比较特殊，其缓存的页表项仅需要在执行 `sfence.vma` 指令时冲刷，而这条冲刷通路由后端负责，因此前端或 ICache 一般不需要管理 ITLB 的冲刷。只有一个特例：目前 ITLB 为了节省资源，不会存储 `gpaddr`，而是在 `gpf` 发生时去 L2TLB 重取，重取状态由一个 `gpf` 缓存控制，这要求 ICache 在收到 `ITLB.resp.excp.gpf_instr` 时保证下面两个条件之一：

1. 重发相同的 `ITLB.req.vaddr`，直到 `ITLB.resp.miss` 拉低（此时`gpf`、`gpaddr`均有效，正常发往后端处理即可），ITLB 此时会冲刷 `gpf` 缓存。
2. 给 `ITLB.flushPipe`，ITLB 在收到该信号时会冲刷 `gpf` 缓存。

若 ITLB 的 `gpf` 缓存未被冲刷，就收到了不同 `ITLB.req.vaddr` 的请求，且再次发生 `gpf`，将导致核卡死。

因此，每当冲刷 IPrefetchPipe 的 s1 流水级时，无论冲刷原因为何，都需要同步冲刷 ITLB 的 `gpf` 缓存（即拉高 `ITLB.flushPipe`）。

### ECC

首先需要指出，ICache 在默认参数下使用 parity code，其仅具备 1 bit 错误检测能力，不具备错误恢复能力，严格意义上不能算是 ECC（Error Correction Code）。但一方面，其可以配置为使用 secded code；另一方面，我们在代码中大量使用 ECC 来命名错误检测与错误恢复相关的功能（`ecc_error`、`ecc_inject`等）。因此本文档仍将使用 ECC 一词来指代错误检测、错误恢复、错误注入相关功能以保证与代码的一致性。

ICache 支持错误检测、错误恢复、错误注入功能，是 RAS[^ras] 能力的一部分，可以参考 RISC-V RERI[^reri] 手册，由 CtrlUnit 进行控制。

[^ras]: 此 RAS（Reliability, Availability, and Serviceability）非彼 RAS（Return Address Stack）。
[^reri]: RERI（RAS Error-record Register Interface），参考 [RISC-V RERI 手册](https://github.com/riscv-non-isa/riscv-ras-eri)。

#### 错误检测

在 MissUnit 向 MetaArray 和 DataArray 重填数据时，会计算 meta 和 data 的校验码，前者和 meta 一起存储在 Meta SRAM 中，后者存储在单独的 Data Code SRAM 中。

当取指请求读取 SRAM 时，会同步读取出校验码，在 MainPipe 的 s1/s2 流水级中分别对 meta/data 进行校验。软件可以通过向 mmio-mapped CSR 中相应位置写入特定的值来使能/关闭这一功能，详见 [CtrlUnit 文档](05_ctrlunit)。

在校验码设计方面，ICache 使用的校验码可由参数控制，默认使用的是 parity code，即校验码为对数据做规约异或 $code = \oplus data$。检查时只需将校验码和数据一起做规约异或 $error = (\oplus data) \oplus code$，结果为 1 则发生错误，反之**认为没有**错误（可能出现偶数个错误，但此处检查不出来）。

ICache 支持错误注入，这要求 ICache 支持向 MetaArray/DataArray 写入错误的校验码。因此实现了一个`poison`位，当其拉高时，翻转写入的 code，即 $code = (\oplus data) \oplus poison$。

为了减少检查不出的情况，目前将 data 划分成 DataCodeUnit（默认为 64bit）的单元分别进行奇偶校验，因此对每个 64B 的缓存行，总计会计算 $8(data) + 1(meta) = 9$ 个校验码。

当 MainPipe 的 s1/s2 流水级检查到错误时，会进行以下处理：

在 6 月至 11 月的版本中：

1. 错误处理：引起 access fault 异常，由软件处理。
2. 错误报告：向 BEU 报告错误，后者会引起中断向软件报告错误。
3. 取消请求：当 MetaArray 被检查出错误时，其读出的 ptag 不可靠，进而对 hit 与否的判断不可靠，因此无论是否 hit 都不向 L2 Cache 发送请求，而是直接将异常传递到 IFU、进而传递到后端处理。

在后续版本（[#3899](https://github.com/OpenXiangShan/XiangShan/pull/3899) 后）实现了错误自动恢复机制，故只需进行以下处理：

1. 错误处理：从 L2 Cache 重新取指，见[错误自动恢复](#错误自动恢复)。
2. 错误报告：拉高 erros.valid 向顶层报告错误。

#### 错误自动恢复

注意到，ICache 与 DCache 不同，是只读的，因此其数据必然不是 dirty 的，这意味着我们总是可以从下级存储结构（L2/3 Cache、memory）中重新获取正确的数据。因此，ICache 可以通过向 L2 Cache 重新发起 miss 请求来实现错误自动恢复。

实现重取功能本身只需要复用现有的 miss 取指路径，走 MainPipe -> MissUnit -> MSHR --tilelink-> L2 Cache 的请求路径。MissUnit 向 SRAM 重填数据时会自然地计算新的校验码并存储，因此在重取后会回到无错误的状态而不需要额外的处理。

6-11 月和后续代码行为差异的伪代码示意如下：

```diff
- exception = itlb_exception || pmp_exception || ecc_error
+ exception = itlb_exception || pmp_exception

- should_fetch = !hit && !exception
+ should_fetch = (!hit || ecc_error) && !exception
```

需要留意的是：为了避免重取后出现 multi-hit（即，同一个 set 内存在多个 way 的 ptag 相同），需要在重取前将 metaArray 对应位置的 valid 清空：

- 若 MetaArray 错误：meta 保存的 ptag 本身可能出错，命中结果（one-hot 的 waymask）不可靠，“对应位置”指该 set 的所有 way
- 若 DataArray 错误：命中结果可靠，“对应位置”指该 set 中 waymask 拉高的那一 way

#### 错误注入

根据 RERI 手册[^reri]的说明，为了使软件能够测试 ECC 功能，进而更好地判断硬件功能是否正常，需要提供错误注入功能，即主动地触发 ECC 错误。

ICache 的错误注入功能由 CtrlUnit 控制，通过向 mmio-mapped CSR 中相应位置写入特定的值来触发。详见 [CtrlUnit 文档](05_ctrlunit)。

目前 ICache 支持：

- 向特定 paddr 注入，当请求注入的 paddr 未命中时，注入失败
- 向 MetaArray 或 DataArray 注入
- 当 ECC 校验功能本身未使能时，注入失败

软件注入流程示意如下：

```asm
inject_target:
  # maybe do something
  ret

test:
  la t0, $BASE_ADDR     # 载入 mmio-mapped CSR 基地址
  la t1, inject_target  # 载入注入目标地址
  jalr ra, 0(t1)        # 跳转到注入目标以保证其加载到 ICache
  sd t1, 8(t0)          # 向 CSR 写入注入目标地址
  la t2, ($TARGET << 2 | 1 << 1 | 1 << 0)  # 设置注入目标、注入使能、校验使能
  sd t1, 0(t0)          # 向 CSR 写入注入请求
loop:
  ld t1, 0(t0)          # 读取 CSR
  andi t1, t1, (0b11 << (4+1)) # 读取注入状态
  beqz t1, loop         # 如果注入未完成，继续等待

  addi t1, t1, -1
  bnez t1, error        # 如果注入失败，跳转到错误处理

  jalr ra, 0(t1)        # 注入成功，跳转到注入目标地址以触发错误
  j    finish           # 结束

error:
  # handle error
finish:
  # finish
```

我们编写了一个测试用例，见[此仓库](https://github.com/OpenXiangShan/nexus-am/pull/48)，其测试了如下情况：

1. 正常注入 MetaArray
2. 正常注入 DataArray
3. 注入无效的目标
4. 注入但 ECC 校验未使能
5. 注入未命中的地址
6. 尝试写入只读的 CSR 域

## 参考文献

1. Glenn Reinman, Brad Calder, and Todd Austin. "[Fetch directed instruction prefetching.](https://doi.org/10.1109/MICRO.1999.809439)" 32nd Annual ACM/IEEE International Symposium on Microarchitecture (MICRO). 1999.

<mrs-functions>

## ICache 模块功能说明

---

以下是**IPrefetchPipe**模块的功能

### 1. 接收预取请求

从 FTQ 接收预取请求，请求可能有效（ io.req.valid 为高），可能无效； IPrefetchPipe 可能处于空闲（ io.req.ready 为高），可能处于非空闲状态。
只有在请求有效且 IPrefetchPipe 处于空闲状态时，预取请求才会被接收（这里暂不考虑 s0 的刷新信号 s0_flush ，默认其为低）。
预取请求分为不同类型，包括硬件预取请求 (isSoftPrefetch = false)和软件预取请求 (isSoftPrefetch = true)。
cacheline 也分为单 cacheline 和双 cacheline。

#### 1.1 硬件预取请求：

预取请求为硬件 (isSoftPrefetch = false)

| 序号  | 名称                                                | 描述                                                                                                                                         |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.1.1 | 预取请求可以继续                                    | 当预取请求有效且 IPrefetchPipe 处于空闲状态时，预取请求应该被接收。<br> s0_fire 信号在没有 s0 的刷新信号（ s0_flush 为低）时，应该被置为高。 |
| 1.1.2 | 预取请求被拒绝--预取请求无效                        | 当预取请求无效时，预取请求应该被拒绝。<br> s0_fire 信号应该被置为低。                                                                        |
| 1.1.3 | 预取请求被拒绝--IPrefetchPipe 非空闲                | 当 IPrefetchPipe 非空闲时，预取请求应该被拒绝。<br> s0_fire 信号应该被置为低。                                                               |
| 1.1.4 | 预取请求被拒绝--预取请求无效且 IPrefetchPipe 非空闲 | 当预取请求无效且 IPrefetchPipe 非空闲时，预取请求应该被拒绝。<br>s0_fire 信号应该被置为低。                                                  |
| 1.1.5 | 预取请求有效且为单 cacheline                        | 当预取请求有效且为单 cacheline 时，预取请求应该被接收。<br>s0_fire 为高，s0_doubleline 应该被置低（false）。                                 |
| 1.1.6 | 预取请求有效且为双 cacheline                        | 当预取请求有效且为双 cacheline 时，预取请求应该被接收。<br> s0_fire 为高，s0_doubleline 应该被置高（true）。                                 |

#### 1.2 软件预取请求：

预取请求为软件 (isSoftPrefetch = true)

| 序号  | 名称                                                    | 描述                                                                                                                                               |
| ----- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2.1 | 软件预取请求可以继续                                    | 当预取请求有效且 IPrefetchPipe 处于空闲状态时，软件预取请求应该被接收。<br>当预取请求有效且 IPrefetchPipe 处于空闲状态时，软件预取请求应该被接收。 |
| 1.2.2 | 软件预取请求被拒绝--预取请求无效                        | 当预取请求无效时，软件预取请求应该被拒绝。<br>s0_fire 信号应该被置为低。                                                                           |
| 1.2.3 | 软件预取请求被拒绝--IPrefetchPipe 非空闲                | 当 IPrefetchPipe 非空闲时，软件预取请求应该被拒绝。<br>s0_fire 信号应该被置为低。                                                                  |
| 1.2.4 | 软件预取请求被拒绝--预取请求无效且 IPrefetchPipe 非空闲 | 当预取请求无效且 IPrefetchPipe 非空闲时，软件预取请求应该被拒绝。<br> s0_fire 信号应该被置为低。                                                   |
| 1.2.5 | 软件预取请求有效且为单 cacheline                        | 当软件预取请求有效且为单 cacheline 时，软件预取请求应该被接收。<br>s0_fire 为高，s0_doubleline 应该被置低（false）。                               |
| 1.2.6 | 软件预取请求有效且为双 cacheline                        | 当软件预取请求有效且为双 cacheline 时，软件预取请求应该被接收。<br> s0_fire 为高，s0_doubleline 应该被置高（true）。                               |

### 2. 接收来自 ITLB 的响应并处理结果

接收 ITLB 的响应，完成虚拟地址到物理地址的转换。
当 ITLB 发生缺失（miss）时，保存请求信息，等待 ITLB 完成后再继续处理。

#### 2.1 地址转换完成

- 根据 ITLB 的响应，接收物理地址（paddr），并完成地址转换。
- 处理 ITLB 响应可能在不同周期到达的情况，管理有效信号和数据保持机制，确保正确使用物理地址。

| 序号  | 名称                         | 描述                                                                                                                                                         |
| ----- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2.1.1 | ITLB 正常返回物理地址        | ITLB 在一个周期内成功返回物理地址 paddr，s1_valid 为高。<br> 确认 s1 阶段正确接收到 paddr。                                                                  |
| 2.1.2 | ITLB 发生 TLB 缺失，需要重试 | fromITLB(PortNumber).bits.miss 为高，表示对应通道的 ITLB 发生了 TLB 缺失，需要重发。<br> 重发完成后，后续步骤继续进行，fromITLB(PortNumber).bits.miss 为低。 |

#### 2.2 处理 ITLB 异常

- 根据 ITLB 的异常信息，处理可能的异常。pf 缺页、pgf 虚拟机缺页、af 访问错误。

| 序号  | 名称                      | 描述                                                                                                                                                |
| ----- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.2.1 | ITLB 发生页错误异常       | s1_itlb_exception 返回的页错误。<br> iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示页错误 pf。              |
| 2.2.2 | ITLB 发生虚拟机页错误异常 | s1_itlb_exception 返回的虚拟机页错误。<br> iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示虚拟机页错误 pgf。 |
| 2.2.3 | ITLB 发生访问错误异常     | s1_itlb_exception 返回的访问错误。<br> iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示访问错误 af。          |

#### 2.3 处理虚拟机物理地址（用于虚拟化）

- 在虚拟化环境下，处理虚拟机物理地址（gpaddr），确定访问是否针对二级虚拟机的非叶子页表项（isForVSnonLeafPTE）。

| 序号  | 名称                                             | 描述                                                                                                                                                                               |
| ----- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.3.1 | 发生虚拟机页错误异常返回虚拟机物理地址（gpaddr） | 发生 pgf 后，需要返回对应的 gpaddr。<br> 只有一个通道发生 pgf 时，返回对应通道的 gpaddr 即可；多个通道发生 pgf 时，返回第一个通道的 gpaddr。                                       |
| 2.3.2 | ITLB 发生虚拟机页错误异常                        | 发生 gpf 后，如果是访问二级虚拟机的非叶子页表项时，需要返回对应的 gpaddr。<br> 只有一个通道发生 pgf 时，返回对应通道的 gpaddr 即可；多个通道发生 pgf 时，返回第一个通道的 gpaddr。 |

#### 2.4 返回基于页面的内存类型 pbmt 信息

- TLB 有效时，返回 pbmt 信息。

### 3. 接收来自 IMeta（缓存元数据）的响应并检查缓存命中

从 Meta SRAM 中读取缓存标签和有效位。
将物理地址的标签部分与缓存元数据中的标签比较，确定是否命中。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|3.1|缓存标签比较和有效位检查： |从物理地址中提取物理标签（ptag），将其与缓存元数据中的标签进行比较，检查所有缓存路（Way）。检查有效位，确保只考虑有效的缓存行。 |
|3.1|缓存未命中（标签不匹配或有效位为假）： |当标签不匹配或者标签匹配，但是有效位为假时，表示缓存未命中。 <br>s1_meta_ptags(PortNumber)(nWays) 不等于 ptags(PortNumber) 或者它们相等，但是对应的 s1_meta_valids 为低时，总之返回的 waymasks 为全 0。 |
|3.2|单路缓存命中（标签匹配且有效位为真）： |当标签匹配，且有效位为真时，表示缓存命中。 <br>waymasks 对应的位为 1。 |

### 4. PMP（物理内存保护）权限检查

对物理地址进行 PMP 权限检查，确保预取操作的合法性。
处理 PMP 返回的异常和 MMIO 信息
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|4.1|访问被允许的内存区域 |itlb 返回的物理地址在 PMP 允许的范围内。 <br>s1_pmp_exception(i) 为 none。 |
|4.2|访问被禁止的内存区域 |s1_req_paddr(i) 对应的地址在 PMP 禁止的范围内。 <br>s1_pmp_exception(i) 为 af。 |
|4.3|访问 MMIO 区域 |itlb 返回的物理地址在 MMIO 区域。 <br>s1_pmp_mmio 为高。 |

### 5. 异常处理和合并

backend 优先级最高，merge 方法里的异常越靠前优先级越高
合并来自后端、ITLB、PMP 的异常信息，按照优先级确定最终的异常类型。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|5.1|仅 ITLB 产生异常 |s1_itlb_exception(i) 为非零，s1_pmp_exception(i) 为零。 <br>s1_exception_out(i) 正确包含 ITLB 异常。 |
|5.2|仅 PMP 产生异常 |s1_itlb_exception(i) 为零，s1_pmp_exception(i) 为非零。 <br>s1_exception_out(i) 正确包含 PMP 异常。 |
|5.3|仅 后端 产生异常 |s1_itlb_exception(i) 为零，s1_pmp_exception(i) 为零。 <br>s1_exception_out(i) 正确包含 后端 异常。 |
|5.4|ITLB 和 PMP 都产生异常 |s1_itlb_exception(i) 和 s1_pmp_exception(i) 都为非零。 <br>s1_exception_out(i) 包含 ITLB 异常（优先级更高）。 |
|5.5|ITLB 和 后端 都产生异常 |s1_itlb_exception(i) 和 s1_backendException(i) 都为非零。 <br>s1_exception_out(i) 包含 后端 异常（优先级更高）。 |
|5.6|PMP 和 后端 都产生异常 |s1_pmp_exception(i) 和 s1_backendException(i) 都为非零。 <br>s1_exception_out(i) 包含 后端 异常（优先级更高）。 |
|5.7|ITLB、PMP 和 后端 都产生异常 |s1_itlb_exception(i)、s1_pmp_exception(i) 和 s1_backendException(i) 都为非零。 <br>s1_exception_out(i) 包含 后端 异常（优先级更高）。 |
|5.8|无任何异常 |s1_itlb_exception(i)、s1_pmp_exception(i)、s1_backendException(i) 都为零。 <br>s1_exception_out(i) 指示无异常。 |

### 6. 发送请求到 WayLookup 模块

当条件满足时，将请求发送到 WayLookup 模块，以进行后续的缓存访问。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|6.1|正常发送请求到 WayLookup |toWayLookup.valid 为高，toWayLookup.ready 为高，s1_isSoftPrefetch 为假。 <br>请求成功发送，包含正确的地址、标签、waymask 和异常信息。 |
|6.2|WayLookup 无法接收请求 |toWayLookup.valid 为高，toWayLookup.ready 为假。 <br>状态机等待 WayLookup 准备好，不会错误地推进。 |
|6.3|软件预取请求不发送到 WayLookup |s1_isSoftPrefetch 为真。 <br>toWayLookup.valid 为假，不会发送预取请求到 WayLookup。 |

### 7. 状态机控制和请求处理流程

使用状态机管理 s1 阶段的请求处理流程。
包括处理 ITLB 重发、Meta 重发、进入 WayLookup、等待 s2 准备等状态

#### 7.1 初始为 m_idle 状态

| 序号  | 名称                           | 描述                                                                                                                    |
| ----- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| 7.1.1 | 正常流程推进，保持 m_idle 状态 | s1_valid 为高，itlb_finish 为真，toWayLookup.fire 为真，s2_ready 为真。 <br>状态机保持在 m_idle 状态，s1 阶段顺利推进。 |
| 7.1.2 | ITLB 未完成，需要重发          | s1_valid 为高，itlb_finish 为假。 <br>状态机进入 m_itlbResend 状态，等待 ITLB 完成。                                    |
| 7.1.3 | ITLB 完成，WayLookup 未命中    | s1_valid 为高，itlb_finish 为真，toWayLookup.fire 为假。 <br>状态机进入 m_enqWay 状态，等待 WayLookup 入队。            |

#### 7.2 初始为 m_itlbResend 状态

| 序号  | 名称                                             | 描述                                                                                      |
| ----- | ------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| 7.2.1 | ITLB 命中, MetaArray 空闲，需要 WayLookup 入队   | itlb_finish 为假，toMeta.ready 为真。 <br>状态机进入 m_enqWay 状态，等待 WayLookup 入队。 |
| 7.2.2 | ITLB 命中, MetaArray 繁忙，等待 MetaArray 读请求 | itlb_finish 为假，toMeta.ready 为假。 <br>状态机进入 m_metaResend 状态，MetaArray 读请求  |

#### 7.3 初始为 m_metaResend 状态

| 序号 | 名称                                 | 描述                                                                    |
| ---- | ------------------------------------ | ----------------------------------------------------------------------- |
| 7.3  | MetaArray 空闲 ，需要 WayLookup 入队 | toMeta.ready 为真。 <br>状态机进入 m_enqWay 状态，等待 WayLookup 入队。 |

#### 7.4 初始为 m_enqWay 状态

| 序号  | 名称                                                         | 描述                                                                                                            |
| ----- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 7.4.1 | WayLookup 入队完成或者为软件预取, S2 空闲, 重新进入空闲状态  | toWayLookup.fire 或 s1_isSoftPrefetch 为真，s2_ready 为假。 <br>状态机进入空闲状态 m_idle。                     |
| 7.4.2 | WayLookup 入队完成或者为软件预取, S2 繁忙，需要 enterS2 状态 | toWayLookup.fire 或 s1_isSoftPrefetch 为真，s2_ready 为真。 <br>状态机进入 m_enterS2 状态，等待 s2 阶段准备好。 |

#### 7.5 初始为 m_enterS2 状态

| 序号 | 名称                                                    | 描述                                            |
| ---- | ------------------------------------------------------- | ----------------------------------------------- |
| 7.5  | s2 阶段准备好，请求进入下流水级，流入后进入 m_idle 状态 | s2_ready 为真。 <br>状态机进入空闲状态 m_idle。 |

### 8. 监控 missUnit 的请求

检查 missUnit 的响应，更新缓存的命中状态和 MSHR 的匹配状态。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|8.1|请求与 MSHR 匹配且有效： |s2_req_vSetIdx 和 s2_req_ptags 与 fromMSHR 中的数据匹配，且 fromMSHR.valid 为高，fromMSHR.bits.corrupt 为假。 <br>s2_MSHR_match(PortNumber) 为真, s2_MSHR_hits(PortNumber) 应保持为真 |
|8.2|请求在 SRAM 中命中： |s2_waymasks(PortNumber) 中有一位为高，表示在缓存中命中。 <br>s2_SRAM_hits(PortNumber) 为真,s2_hits(PortNumber) 应为真。 |
|8.3|请求未命中 MSHR 和 SRAM： |请求未匹配 MSHR，且 s2_waymasks(PortNumber) 为空。 <br>s2_MSHR_hits(PortNumber)、s2_SRAM_hits(PortNumber) 均为假, s2_hits(PortNumber) 为假。 |

### 9. 发送请求到 missUnit

对于未命中的预取请求，向 missUnit 发送请求，以获取缺失的数据。

#### 9.1 确定需要发送给 missUnit 的请求

根据命中状态、异常信息、MMIO 信息等，确定哪些请求需要发送到 missUnit（即 s2_miss）。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|9.1.1|请求未命中且无异常，需要发送到 missUnit： |s2_hits(PortNumber) 为假(未命中缓存)，s2_exception 无异常，s2_mmio 为假(不是 MMIO 或不可缓存的内存)。 <br>s2_miss(PortNumber) 为真，表示需要发送请求到 missUnit。 |
|9.1.2|请求命中或有异常，不需要发送到 missUnit： |s2_hits(i) 为真（已命中）或者 s2_exception 有异常 或者 s2_mmio 为真（MMIO 访问）。 <br>s2_miss(i) 为假，不会发送请求到 missUnit。 |
|9.1.3|双行预取时，处理第二个请求的条件： |s2_doubleline 为真，处理第二个请求。 <br>如果第一个请求有异常或 MMIO，s2_miss(1) 应为假，后续请求被取消或处理。 |

#### 9.2 避免发送重复请求，发送请求到 missUnit

- 使用寄存器 has_send 记录每个端口是否已发送请求，避免重复发送。
- 将需要发送的请求通过仲裁器 toMSHRArbiter 发送到 missUnit。

| 序号  | 名称                                | 描述                                                                                                                                     |
| ----- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 9.2.1 | 在 s1_real_fire 时，复位 has_send： | s1_real_fire 为高。 <br>has_send(PortNumber) 应被复位为假，表示新的请求周期开始。                                                        |
| 9.2.2 | 当请求成功发送时，更新 has_send：   | toMSHRArbiter.io.in(PortNumber).fire 为高（请求已发送）。 <br>has_send(PortNumber) 被设置为真，表示该端口已发送请求。                    |
| 9.2.3 | 避免重复发送请求：                  | 同一请求周期内，has_send(PortNumber) 为真，s2_miss(PortNumber) 为真。 <br>toMSHRArbiter.io.in(PortNumber).valid 为假，不会再次发送请求。 |
| 9.2.4 | 正确发送需要的请求到 missUnit：     | s2_valid 为高，s2_miss(i) 为真，has_send(i) 为假。 <br>toMSHRArbiter.io.in(i).valid 为高，请求被成功发送。                               |
| 9.2.5 | 仲裁器正确仲裁多个请求：            | 多个端口同时需要发送请求。 <br>仲裁器按照优先级或设计要求选择请求发送到 missUnit,未被选中的请求在下个周期继续尝试发送。                  |

### 10. 刷新机制

- io.flush: 全局刷新信号，当该信号为高时，所有请求都需要刷新。
- from_bpu_s0_flush：当请求不是软件预取（!s0_isSoftPrefetch, 软件预取请求是由特定的指令触发的，与指令流中的分支预测无关。因此，在处理刷新信号时，对于软件预取请求，通常不受来自 BPU 的刷新信号影响。），且 BPU 指示需要在 Stage 2 或 Stage 3 刷新的请求，由于该请求尚未进入 s1 阶段，因此在 s0 阶段也需要刷新。
- s0_flush：综合考虑全局刷新信号、来自 BPU 的刷新信号，以及 s1 阶段的刷新信号
- from_bpu_s1_flush：当 s1 阶段的请求有效且不是软件预取，且 BPU 指示在 Stage 3 需要刷新，则在 s1 阶段需要刷新。
- io.itlbFlushPipe：当 s1 阶段需要刷新时，该信号用于通知 ITLB 刷新其流水线，以保持一致性。
- s1_flush：综合考虑全局刷新信号和来自 BPU 的刷新信号。
- s2_flush：用于控制 s2 阶段是否需要刷新。

| 序号 | 名称              | 描述                                                                                                                                                 |
| ---- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10.1 | 发生全局刷新      | io.flush 为高。 <br>s0_flush、s1_flush、s2_flush 分别为高，所有阶段的请求被正确清除。                                                                |
| 10.2 | 来自 BPU 的刷新   | io.flushFromBpu.shouldFlushByStageX 为真（X 为 2 或 3），且请求不是软件预取。 <br>对应阶段的 from_bpu_sX_flush 为高，sX_flush 为高，阶段请求被刷新。 |
| 10.3 | 刷新时状态机复位  | s1_flush 为高。 <br>状态机 state 被重置为 m_idle 状态。                                                                                              |
| 10.4 | ITLB 管道同步刷新 | s1_flush 为高。 <br>io.itlbFlushPipe 为高，ITLB 被同步刷新。                                                                                         |

---

以下是**MainPipe**模块的功能

### 11. 访问 DataArray 的单路

根据从 WayLookup 获取信息，包括路命中信息和 ITLB 查询结果还有 DataArray 当前的情况，决定是否需要从 DataArray 中读取数据。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|11.1|访问 DataArray 的单路 |当 WayLookup 中的信息表明路命中时，ITLB 查询成功，并且 DataArray 当前没有写时，MainPipe 会向 DataArray 发送读取请求，以获取数据。 <br>s0_hits 为高（一路命中），s0_itlb_exception 信号为零（ITLB 查询成功），toData.last.ready 为高（DataArray 没有正在进行的写操作）。 <br>toData.valid 信号为高，表示 MainPipe 向 DataArray 发出了读取请求。 |
|11.2|不访问 DataArray（Way 未命中） ==会访问，但是返回数据无效== |当 WayLookup 中的信息表明路未命中时，MainPipe 不会向 DataArray 发送读取请求。 <br>s0_hits 为低表示缓存未命中 <br>toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。 |
|11.3|不访问 DataArray（ITLB 查询失败）==会访问，但是返回数据无效== |当 ITLB 查询失败时，MainPipe 不会向 DataArray 发送读取请求。 <br>s0_itlb_exception 信号不为零（ITLB 查询失败）。 <br>toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。 |
|11.4|不访问 DataArray（DataArray 正在进行写操作） |当 DataArray 正在进行写操作时，MainPipe 不会向 DataArray 发送读取请求。 <br>toData.last.ready 信号为低，表示 DataArray 正在进行写操作。 <br>toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。 |

### 12. Meta ECC 校验

将物理地址的标签部分与对应的 Meta 进行 ECC 校验，以确保 Meta 的完整性。
|  序号  |  名称  |  描述  |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|12.1|无 ECC 错误 |当 waymask 全为 0（没有命中），则 hit_num 为 0 或 waymask 有一位为 1（一路命中），hit_num 为 1 且 ECC 对比通过（encodeMetaECC(meta) == code） <br>s1_meta_corrupt 为假。 |
|12.2|单路命中的 ECC 错误 |当 waymask 有一位为 1（一路命中），ECC 对比失败（encodeMetaECC(meta) != code） <br>s1_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。 |
|12.3|多路命中 |> hit multi-way, must be an ECC failure <br>当 waymask 有两位及以上为 1（多路命中），视为 ECC 错误。 <br>s1_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。 |
|12.4|ECC 功能关闭 |当奇偶校验关闭时（ecc_enable 为低），强制清除 s1_meta_corrupt 信号置位。 <br>不管是否发生 ECC 错误，s1_meta_corrupt 都为假。 |

### 13. PMP 检查

- 将 S1 的物理地址 s1_req_paddr(i) 和指令 TlbCmd.exec 发往 PMP，判断取指是否合法。
- 防止非法地址，区分普通内存和 MMIO 内存。

| 序号 | 名称                                 | 描述                                                                                    |
| ---- | ------------------------------------ | --------------------------------------------------------------------------------------- |
| 13.1 | 没有异常                             | s1_pmp_exception 为全零，表示没有 PMP 异常。                                            |
| 13.2 | 通道 0 有 PMP 异常                   | s1_pmp_exception(0) 为真，表示通道 0 有 PMP 异常。                                      |
| 13.3 | 通道 1 有 PMP 异常                   | s1_pmp_exception(1) 为真，表示通道 1 有 PMP 异常。                                      |
| 13.4 | 通道 0 和通道 1 都有 PMP 异常        | s1_pmp_exception(0) 和 s1_pmp_exception(1) 都为真，表示通道 0 和通道 1 都有 PMP 异常。  |
| 13.5 | 没有映射到 MMIO 区域                 | s1_pmp_mmio（0） 和 s1_pmp_mergemmio（1） 都为假，表示没有映射到 MMIO 区域。            |
| 13.6 | 通道 0 映射到了 MMIO 区域            | s1_pmp_mmio（0） 为真，表示映射到了 MMIO 区域。                                         |
| 13.7 | 通道 1 映射到了 MMIO 区域            | s1_pmp_mmio（1） 为真，表示映射到了 MMIO 区域。                                         |
| 13.8 | 通道 0 和通道 1 都映射到了 MMIO 区域 | s1_pmp_mmio（0） 和 s1_pmp_mmio（1） 都为真，表示通道 0 和通道 1 都映射到了 MMIO 区域。 |

### 14. 异常合并

- 将 s1_itlbmergeption 与 s1_pmp_exception 合并生成 s1_exception_out。
- ITLB 异常通常优先于 PMP 异常。merge

| 序号 | 名称                     | 描述                                                                                     |
| ---- | ------------------------ | ---------------------------------------------------------------------------------------- |
| 14.1 | 没有异常                 | s1_exception_out 为全零，表示没有异常。                                                  |
| 14.2 | 只有 ITLB 异常           | s1_exception_out 和 s1_itlb_exception 一致                                               |
| 14.3 | 只有 PMP 异常            | s1_exception_out 和 s1_pmp_exception 一致                                                |
| 14.4 | ITLB 与 PMP 异常同时出现 | > itlb has the highest priority, pmp next <br>s1_exception_out 和 s1_itlb_exception 一致 |

### 15. MSHR 匹配和数据选择

- 检查当前的请求是否与 MSHR 中正在处理的缺失请求匹配。
- 判断 缓存组索引相同(s1_req_vSetIdx(i) == fromMSHR.bits.vSetIdx) ，物理标签相同 (s1_req_ptags(i) == fromMSHR.bits.blkPaddr)；若匹配 MSHR 有效且没有错误（fromMSHR.valid && !fromMSHR.bits.corrupt），则优先使用 MSHR 中的数据
- 避免重复访问 Data SRAM，提升性能；当 MSHR 中已有重填结果时，可立即命中。

| 序号 | 名称              | 描述                                                                                                                                                         |
| ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 15.1 | 命中 MSHR         | MSHR 中已有正确数据时，S1 阶段能直接拿到 <br>s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 s1_bankMSHRHit(i)，s1_data_is_from_MSHR(i) 为 true                   |
| 15.2 | 未命中 MSHR       | MSHR 中存放的地址与当前请求不同，那么应该读取 SRAM 的数据 <br>s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false |
| 15.3 | MSHR 数据 corrupt | fromMSHR.bits.corrupt = true，那么 MSHR 将不匹配，应该读取 SRAM 的数据 <br>s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false                |

### 16. Data ECC 校验

在 S2 阶段，对从 S1 或 MSHR 获得的数据（如 s2_datas）进行 ECC 校验：

- 若 ECC 校验失败，则标记 s2_data_corrupt(i) = true。
- 若数据来自 MSHR，则不重复进行 ECC 校验（或忽略 corrupt）

| 序号 | 名称             | 描述                                                                                                                                                                                                                                         |
| ---- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 16.1 | 无 ECC 错误      | s2_bank 全部没有损坏，bank 也选对了对应的端口和 bank，数据不来自 MSHR <br>s2_data_corrupt(i) 为 false，没有 ECC 错误。                                                                                                                       |
| 16.2 | 单 Bank ECC 错误 | s2_bank_corrupt(bank) 有一个为 true ,即对应的 bank 有损坏；同时 bank 也选对了对应的端口和 bank，数据不来自 MSHR <br>s2_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。      |
| 16.3 | 多 Bank ECC 错误 | s2_bank_corrupt(bank) 有两个或以上为 true,即对应的 bank 有损坏；同时 bank 也选对了对应的端口和 bank，数据不来自 MSHR <br>s2_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。 |
| 16.4 | ECC 功能关闭     | 当奇偶校验关闭时（ecc_enable 为低），强制清除 s2_data_corrupt 信号置位。 <br>不管是否发生 ECC 错误，s2_data_corrupt 都为假。                                                                                                                 |

### 17. 冲刷 MetaArray

Meta 或者 Data ECC 校验错误时，会冲刷 MetaArray，为重取做准备。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|17.1|只有 Meta ECC 校验错误 |> if is meta corrupt, clear all way (since waymask may be unreliable) <br>当 s1_meta_corrupt 为真时，MetaArray 的所有路都会被冲刷。 <br>toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的所有路置位。 |
|17.2|只有 Data ECC 校验错误 |> if is data corrupt, only clear the way that has error <br>当 s2_data_corrupt 为真时，只有对应路会被冲刷。 <br>toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的对应路置位。 |
|17.3|同时有 Meta ECC 校验错误和 Data ECC 校验错误 |处理 Meta ECC 的优先级更高， 将 MetaArray 的所有路冲刷。 <br>toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的所有路置位。 |

### 18. 监控 MSHR 匹配与数据更新

- 判断是否命中 MSHR
- 根据 MSHR 是否命中和 s1 阶段是否发射来更新 s2 的数据，s2 的命中状态和 l2 是否损坏

| 序号 | 名称                          | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 18.1 | MSHR 命中（匹配且本阶段有效） | MSHR 的 vSetIdx / blkPaddr 与 S2 请求一致， fromMSHR.valid 有效，s2_valid 也有效 <br>s2_MSHR_match，s2_MSHR_hits 为高，s2_bankMSHRHit 对应 bank 为高 <br>s1_fire 无效时，s2_datas 更新为 MSHR 的数据，将 s2_data_is_from_MSHR 对应位置位，s2_hits 置位，清除 s2_data_corrupt，l2 的 corrupt 更新为 fromMSHR.bits.corrupt <br>s1_fire 有效时，s2_datas 为 s1_datas 的数据，将 s2_data_is_from_MSHR 对应位置为 s1 的 s1_data_is_from_MSHR，s2_hits 置为 s1_hits，清除 s2_data_corrupt，l2 的 corrupt 为 false |
| 18.2 | MSHR 未命中                   | MSHR 的 vSetIdx / blkPaddr 与 S2 请求一致， fromMSHR.valid 有效，s2_valid 也有效，至少有一个未达成 <br>s2_MSHR_hits(i) = false，S2 不会更新 s2_datas，继续保持原先 SRAM 数据或进入 Miss 流程。                                                                                                                                                                                                                                                                                                              |

### 19. Miss 请求发送逻辑和合并异常

- 通过计算 s2_should_fetch(i) 判断是否需要向 MSHR 发送 Miss 请求：
  - 当出现未命中 (!s2_hits(i)) 或 ECC 错误(s2_meta_corrupt(i) || s2_data_corrupt(i)) 时，需要请求重新获取。
  - 若端口存在异常或处于 MMIO 区域，则不发送 Miss 请求。
- 使用 Arbiter 将多个端口的请求合并后发送至 MSHR。
- 通过 s2_has_send(i) 避免重复请求。
- 将 S2 阶段已有的 ITLB/PMP 异常（s2_exception）与 L2 Cache 报告的 s2_l2_corrupt(i)（封装后为 s2_l2_exception(i)）进行合并。

| 序号 | 名称               | 描述                                                                                                                                                                                                                                                                           |
| ---- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 19.1 | 未发生 Miss        | 当 s2_hits(i) 为高（s2 已经命中），s2 的 meta 和 data 都没有错误，s2 异常，处于 mmio 区域 <br>以上条件至少满足一个时，s2_should_fetch(i) 为低，表示不发送 Miss 请求。    |
| 19.2 | 单口 Miss          | 当出现未命中 (!s2_hits(i)) 或 ECC 错误(s2_meta_corrupt(i) <br>s2_data_corrupt(i))，端口不存在异常且未处于 MMIO 区域时，会向 MSHR 发送 Miss 请求。 <br>toMSHRArbiter.io.in(i).valid = true ，Arbiter 只发送一条 Miss 请求。 |
| 19.3 | 双口都需要 Miss    | 同上，但是两个端口都满足 s2_should_fetch 为高的条件。 <br>toMSHRArbiter.io.in(0).valid、toMSHRArbiter.io.in(1).valid 均为 true，Arbiter 根据仲裁顺序依次发出请求。   |
| 19.4 | 重复请求屏蔽       | 当 s1_fire 为高，表示可以进入 s2 阶段,那么 s2 还没有发送 s2_has_send(i) := false.B <br>如果已经有请求发送了，那么对应的 toMSHRArbiter.io.in(i).fire 为高，表示对应的请求可以发送，s2_has_send(i) := true。 <br>此时再次发送，toMSHRArbiter.io.in(i).valid 为低，表示发送失败。 |
| 19.5 | 仅 ITLB/PMP 异常   | S1 阶段已记录了 ITLB 或 PMP 异常，L2 corrupt = false。 <br>2_exception_out 仅保留 ITLB/PMP 异常标记，无新增 AF 异常。                                                                                                                                                          |
| 19.6 | 仅 L2 异常         | S2 阶段 s2_l2_corrupt(i) = true，且无 ITLB/PMP 异常。 <br>s2_exception_out(i) 表示 L2 访问错误(AF)。                                                                                                                                                                           |
| 19.7 | ITLB + L2 同时出现 | 同时触发 ITLB 异常和 L2 corrupt。 <br>s2_exception_out 优先保留 ITLB 异常类型，不被 L2 覆盖。                                                                                                                                                                                  |
| 19.8 | s2 阶段取指完成    | s2_should_fetch 的所有端口都为低，表示需要取指，那么取指完成 <br>s2_fetch_finish 为高                                                                                                                                                                                          |

### 20. 响应 IFU

- 若当前周期 S2 成功发射（s2_fire = true）且数据获取完毕（s2_fetch_finish），则把数据、异常信息、物理地址等打包到 toIFU.bits 输出。
- 若为双行请求（s2_doubleline = true），也会向 IFU 发送第二路的信息（地址、异常）。

| 序号 | 名称           | 描述                                                                                                                                                                                                                    |
| ---- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 20.1 | 正常命中并返回 | 不存在任何异常或 Miss，s2 命中，s2 阶段取指完成，外部的 respStall 停止信号也为低 。 <br>toIFU.valid = true，toIFU.bits.data 为正确的 Cacheline 数据，toIFU.bits.exception、pmp_mmio、itlb_pbmt = none。                 |
| 20.2 | 异常返回       | 设置 ITLB、PMP、或 L2 corrupt 异常。 <br>toIFU.bits.exception(i) = 对应异常类型，pmp_mmio、itlb_pbmt 根据是否有对应的异常设置为 true。                                                                                  |
| 20.3 | 跨行取指       | s2_doubleline = true，同时检查第一路、第二路返回情况。 <br>toIFU.bits.doubleline = true。 <br>若第二路正常，toIFU.bits.exception(1) = none；若第二路异常，则 exception(1) 标记相应类型。 <br>pmp_mmio、itlb_pbmt 类似。 |
| 20.4 | RespStall      | 外部 io.respStall = true，导致 S2 阶段无法发射到 IFU。 <br>s2_fire = false，toIFU.valid 也不拉高，S2 保持原状态等待下一拍（或直到 respStall 解除）。                                                                    |

### 21. L2 Corrupt 报告

- 当检测到 L2 Cache 返回的 corrupt 标记时（s2_l2_corrupt(i) = true），在 S2 完成发射后额外向外部错误接口 io.errors(i) 报告。
- 与 Data ECC 或 Meta ECC 不同，L2 corrupt 由 L2 自己报告给 BEU，这里不需要再次报告给 beu。

| 序号 | 名称             | 描述                                                                                                                                                                               |
| ---- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 21.1 | L2 Corrupt 单路  | s2 阶段准备完成可以发射（s2_fire 为高），s2_MSHR_hits(0)和 fromMSHR.bits.corrupt 为高 <br>s2_l2_corrupt(0) = true，io.errors(0).valid = true，io.errors(0).bits.source.l2 = true。 |
| 21.2 | 双路同时 corrupt | 端口 0 和端口 1 都从 L2 corrupt 数据中获取。 <br>s2_l2_corrupt 均为 true，发射后分别报告到 io.errors(0) 和 io.errors(1)。                                                          |

### 22. 刷新机制

- io.flush：外部的全局刷新信号，它用于指示整个流水线需要被冲刷（清空）。
- s0_flush： S0 阶段内部的刷新信号，它由 io.flush 传递而来，用于控制 S0 阶段的刷新操作。
- s1_flush： S1 阶段内部的刷新信号，它由 io.flush 传递而来，用于控制 S1 阶段的刷新操作。
- s2_flush： S2 阶段内部的刷新信号，它由 io.flush 传递而来，用于控制 S2 阶段的刷新操作。

| 序号 | 名称        | 描述                                                                                                                                            |
| ---- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 22.1 | 全局刷新    | io.flush 被激活时，流水线的各个阶段（S0, S1 和 S2）都能正确响应并执行刷新操作。 <br>io.flush = true。 <br>s0_flush, s1_flush, s2_flush = true。 |
| 22.2 | S0 阶段刷新 | s0_flush = true。 <br>s0_fire = false。                                                                                                         |
| 22.3 | S1 阶段刷新 | s1_flush = true。 <br>s1_valid， s1_fire = false。                                                                                              |
| 22.4 | S2 阶段刷新 | s2_flush = true。 <br>s2_valid， toMSHRArbiter.io.in(i).valid ， s2_fire = false                                                                |

---

以下是**WayLookup**模块的功能

### 23. 刷新操作

- 接收到全局刷新刷新信号 io.flush 后，读、写指针和 GPF 信息都被重置。

| 序号 | 名称          | 描述                                                                              |
| ---- | ------------- | --------------------------------------------------------------------------------- |
| 23.1 | 刷新读指针    | io.flush 为高时，重置读指针。 <br>readPtr.value 为 0， readPtr.flag 为 false。    |
| 23.2 | 刷新写指针    | io.flush 为高时，重置写指针。 <br>writePtr.value 为 0， writePtr.flag 为 false。  |
| 23.3 | 刷新 GPF 信息 | io.flush 为高时，重置 GPF 信息。 <br>gpf_entry.valid 为 0， gpf_entry.bits 为 0。 |

### 24. 读写指针更新

- 读写信号握手完毕之后（io.read.fire/io.write.fire 为高），对应指针加一。
- 因为是在环形队列上，所以超过队列大小后，指针会回到队列头部。

| 序号 | 名称       | 描述                                                                                                                               |
| ---- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 24.1 | 读指针更新 | 当 io.read.fire 为高时，读指针加一。 <br>readPtr.value 加一。 <br>如果 readPtr.value 超过环形队列的大小，readPtr.flag 会翻转。     |
| 24.2 | 写指针更新 | 当 io.write.fire 为高时，写指针加一。 <br>writePtr.value 加一。 <br>如果 writePtr.value 超过环形队列的大小，writePtr.flag 会翻转。 |

### 25. 更新操作

- MissUnit 处理完 Cache miss 后，向 WayLookup 写入命中信息，也就是 update 操作。
- 情况分为两种：
  - 命中：更新 waymask 和 meta_codes。
  - 未命中：重置 waymask。

| 序号 | 名称       | 描述                                                                                                                                                                    |
| ---- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 25.1 | 命中更新   | MissUnit 返回的更新信息和 WayLookup 的信息相同时，更新 waymask 和 meta_codes。 <br>vset_same 和 ptag_same 为真。 <br>waymask 和 meta_codes 更新。 <br>hits 对应位为高。 |
| 25.2 | 未命中更新 | vset_same 和 way_same 为真。 <br>waymask 清零。 <br>hit 对应位为高。                                                                                                    |
| 25.3 | 不更新     | 其他情况下不更新。 <br>vset_same 为假或者 ptag_same 和 way_same 都为假。 <br>hits 对应位为低。                                                                          |

### 26. 读操作

- 读操作会根据读指针从环形队列中读取信息。
- 如果达成了绕过条件，优先绕过。

| 序号 | 名称             | 描述                                                                                                                                                        |
| ---- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 26.1 | Bypass 读        | 队列为空，并且 io.write.valid 写有效时，可以直接读取，而不经过队列。 <br>empty 和 io.write.valid 都为真。 <br>io.read.bits = io.write.bits                  |
| 26.2 | 读信号无效       | 队列为空（readPtr === writePtr）且写信号 io.write.valid 为低。 <br>io.read.valid 为低，读信号无效。                                                         |
| 26.3 | 正常读           | 未达成绕过条件（empty 和 io.write.valid 至少有一个为假）且 io.read.valid 为高。 <br>从环形队列中读取信息。 <br>io.read.bits.entry = entries(readPtr.value)  |
| 26.4 | gpf 命中         | io.read.valid 为高，可以读。 <br>当 gpf_hits 为高时，从 GPF 队列中读取信息。 <br>io.read.bits.gpf = gpf_entry.bits                                          |
| 26.5 | gpf 命中且被读取 | io.read.valid 为高，可以读。 <br>> also clear gpf_entry.valid when it's read <br>当 gpf 命中且被读取其时（io.read.fire 为高），gpf_entry.valid 会被置为 0。 |
| 26.6 | gpf 未命中       | io.read.valid 为高，可以读。 <br>io.read.bits.gpf 清零。                                                                                                    |

### 27. 写操作

- 写操作会根据写指针从环形队列中读取信息。
- 如果有 gpf 停止，就会停止写。

| 序号 | 名称       | 描述                                                                                                                                                                                                                                                    |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 27.1 | gpf 停止   | > if there is a valid gpf to be read, we should stall write <br>gpf 队列数据有效，并且没有被读取或者没有命中，就会产生 gpf 停止，此时写操作会被停止。 <br>gpf_entry.valid && !(io.read.fire && gpf_hit) 为高时，写操作会被停止（io.write.ready 为低）。 |
| 27.2 | 写就绪无效 | 当队列为满（(readPtr.value === writePtr.value) && (readPtr.flag ^ writePtr.flag)）或者 gpf 停止时，写操作会被停止。 <br>（io.write.ready 为低）                                                                                                         |
| 27.3 | 正常写     | 当 io.write.valid 为高时（没满且没有 gpf 停止），写操作会被执行。 <br>正常握手完毕 io.write.fire 为高。 <br>写信息会被写入环形队列。 <br>entries(writePtr.value) = io.write.bits.entry。                                                                |

#### 27.4 有 ITLB 异常的写

- 前面与正常写相同，只不过当写信息中存在 ITLB 异常时，会更新 gpf 队列和 gpf 指针。
- 此时如果已经被绕过直接读取了，那么就不需要存储它了。

| 序号   | 名称               | 描述                                                                                                                                 |
| ------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| 27.4.1 | 被绕过直接读取了   | can_bypass 和 io.read.fire 都为高。 <br>gpf_entry.valid 为 false。 <br>gpf_entry.bits = io.write.bits.gpf <br>gpfPtr = writePtr <br> |
| 27.4.2 | 没有被绕过直接读取 | can_bypass 为低。 <br>gpf_entry.valid 为 true。 <br>gpf_entry.bits = io.write.bits.gpf <br>gpfPtr = writePtr                         |

---

以下是**FIFO**模块的功能

### 28. 入队操作

| 序号 | 名称                             | 描述                                                                                                                                                                                                                                                                           |
| ---- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 28.1 | 队未满，正常入队                 | 当队列未满，且空位不小于一时，可以正常入队，如果从零号位开始入队到最大容量，入队指针的 flag 不会翻转。 <br>io.enq.fire 为高有效，regFiles(enq_ptr.value) = io.enq.bits，enq_ptr.value+1 入队指针移动，入队指针标记位不翻转。 <br>重复以上操作至队满。                          |
| 28.2 | 队未满，入队后标记位翻转         | 当队未满，但是空位却是靠近队尾时，入队一位后就到达了队头，入队指针的 flag 会翻转。 <br>队列的容量为 10，入队指针指向 9，队未满。此时如果 io.enq.fire 为高，则 regFiles(9) = io.enq.bits，enq_ptr.value+1（循环队列，加完后 enq_ptr.value=0）入队指针移动，入队指针标记位翻转。 |
| 28.3 | 队满，入队就绪信号为低，无法入队 | 当队满时，(enq_ptr.value === deq_ptr.value) && (enq_ptr.flag ^ deq_ptr.flag) 为高，io.enq.ready 为低，io.enq.fire 为低无效。 <br>此时入队，入队指针的 value 和 flag 不变。                                                                                                     |

### 29. 出队操作

| 序号 | 名称                             | 描述                                                                                                                                                                                                                                                                             |
| ---- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 29.1 | 队非空，正常出队                 | 当队列非空时，可以正常出队，如果出队指针不经过最大容量位置，出队指针的 flag 不会翻转。 <br>io.deq.fire 为高有效，io.deq.bits = regFiles(deq_ptr.value)，deq_ptr.value+1 出队指针移动，出队指针标记位不翻转。                                                                     |
| 29.2 | 队非空，出队后标记位翻转         | 当队非空，但是出队指针是靠近队尾时，出队一位后就到达了队头，出队指针的 flag 会翻转。 <br>队列的容量为 10，出队指针指向 9，队非空。此时如果 io.deq.fire 为高，则 io.deq.bits = regFiles(9)，deq_ptr.value+1（循环队列，加完后 deq_ptr.value=0）出队指针移动，出队指针标记位翻转。 |
| 29.3 | 队空，出队有效信号为低，无法出队 | 当队空时，enq_ptr === deq_ptr 为高，io.deq.valid 为低，io.deq.fire 为低无效。 <br>此时出队，出队指针的 value 和 flag 不变。                                                                                                                                                      |

### 30. 刷新清空操作

| 序号 | 名称       | 描述                                                                                                                                                                              |
| ---- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 30.1 | flush 清空 | 当刷新信号有效时，重置出队和入队的指针和标记位，清空队列。 <br>当 flush 为高时，deq_ptr.value=0，enq_ptr.value=0，deq_ptr.flag=false，enq_ptr.flag=false，empty=true,full=false。 |

---

以下是**MissUnit**模块的功能

### 31. 处理取指缺失请求

处理来自 MainPipe 的取指单元的缓存缺失请求，将缺失请求分发到多个 Fetch MSHR 中的一个，避免重复请求。
低索引的请求优先处理。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|31.1|接受新的取指请求 |当新的 fetch miss 与 MSHR 中的已有请求不重复时（通过 io.fetch_req.bits.blkPaddr / vSetIdx 给出具体地址），MissUnit 会将请求分配到一个空闲的 Fetch MSHR 中。 <br>当有新的取指缺失请求到达时（io.fetch_req.valid 为高），且没有命中已有的 MSHR（fetchHit 为低），io.fetch_req.ready 应为高，表示可以接受请求。 <br>io.fetch_req.fire 成功握手后，该 MSHR 处于 valid = true 状态，并记录地址。 |
|31.2|处理已有的取指请求 |当已有取指缺失请求到达时（io.fetch_req.valid 为高），且命中已有的 MSHR（fetchHit 为高），io.fetch_req.ready 应为高，虽然不接受请求，但是表现出来为已经接收请求。 <br>fetchDemux.io.in.valid 应为低，fetchDemux.io.in.fire 为低，表示没有新的请求被分发到 MSHR。 |
|31.3|低索引的请求优先进入 MSHR |Fetch 的请求会通过 fetchDemux 分配到多个 Fetch MSHR，fetchDemux 的实现中，低索引的 MSHR 会优先被分配请求。 <br>当取指请求有多个 io.out(i).read 时，选择其中的第一个，也就是低索引的写入 MSHR，io.chose 为对应的索引。 |

### 32. 处理预取缺失请求

与 Fetch Miss 类似，但走另一些 MSHR（Prefetch MSHR）。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|32.1|接受新的预取请求 |当新的 prefetch miss 与 MSHR 中的已有请求不重复时（通过 io.prefetch_req.bits.blkPaddr / vSetIdx 给出具体地址），MissUnit 会将请求分配到一个空闲的 Prefetch MSHR 中。 <br>当有新的预取缺失请求到达时（io.prefetch_req.valid 为高），且没有命中已有的 MSHR（prefetchHit 为低），io.prefetch_req.ready 应为高，表示可以接受请求。 <br>io.prefetch_req.fire 成功握手后，该 MSHR 处于 valid = true 状态，并记录地址。 |
|32.2|处理已有的预取请求 |当已有预取缺失请求到达时（io.prefetch_req.valid 为高），且命中已有的 MSHR（prefetchHit 为高），io.prefetch_req.ready 应为高，虽然不接受请求，但是表现出来为已经接收请求。 <br>prefetchDemux.io.in.valid 应为低，prefetchDemux.io.in.fire 为低，表示请求被接受但未分发到新的 MSHR。 |
|32.3|低索引的请求优先进入 MSHR |Prefetch 的请求会通过 prefetchDemux 分配到多个 Prefetch MSHR，prefetchDemux 的实现中，低索引的 MSHR 会优先被分配请求。 <br>当取指请求有多个 io.out(i).read 时，选择其中的第一个，也就是低索引的写入 MSHR，io.chose 为对应的索引。 |
|32.4|先进入 MSHR 的优先进入 prefetchArb |从 prefetchDemux 离开后，请求的编号会进入 priorityFIFO，priorityFIFO 会根据进入队列的顺序排序，先进入队列的请求会先进入 prefetchArb。 <br>prefetchDemux.io.in.fire 为高，并且 prefetchDemux.io.chosen 有数据时，将其编号写入 priorityFIFO。 <br>在 priorityFIFO 中有多个编号时，出队的顺序和入队顺序一致。 <br>检查 priorityFIFO.io.deq.bit 中的数据即可。 |

### 33. MSHR 管理与查找

| 序号 | 名称                  | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 33.1 | MSHR 查找命中逻辑     | 当新的请求到来时，能够正确查找所有 MSHR，判断请求是否命中已有 MSHR。 <br>当新的请求（取指或预取）到来时，系统遍历所有 MSHR，根据所有 MSHR 的查找信号 allMSHRs(i).io.lookUps(j).hit，检查请求是否已经存在于某个 MSHR 中。 <br>如果命中，则对应的 fetchHit 或 prefetchHit 为高。 <br>对于 prefetchHit 为高，还有一种情况：预取的物理块地址和组索引与取指的相等（(io.prefetch_req.bits.blkPaddr === io.fetch_req.bits.blkPaddr) && (io.prefetch_req.bits.vSetIdx === io.fetch_req.bits.vSetIdx)）并且有取指请求 io.fetch_req.valid 有效时，也算命中 |
| 33.2 | MSHR 状态的更新与释放 | 当请求完成后，也就是来自内存总线的响应完成（D 通道接收完所有节拍），MSHR 能够正确地释放（清除其有效位），以便接收新的请求。 <br>TileLink D 通道返回的 source ID ，即 io.mem_grant.bits.source。 <br>无效化信号 allMSHRs(i).io.invalid 为高，对应的 MSHR 的有效位 allMSHRs(i).valid 变为低                                                                                                                                                                                                                                                        |

### 34. acquireArb 仲裁

预取和取指的 acquire 都会发送给 acquireArb，acquireArb 会选择一个 acquire 发送给 mem_acquire。
acquireArb 使用 chisel 自带的 Arbiter 实现,Arbiter 使用固定优先级仲裁，优先级从编号 0 开始，编号越小优先级越高。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|34.1|acquireArb 仲裁 |acquireArb 会选择一个 acquire 发送给 mem_acquire。 <br>当有多个 MSHR 同时发出请求时，acquireArb 会根据优先级进行仲裁，选择优先级最高的 MSHR 发送请求。 <br>取指请求总是在 0-3 号，预取请求直接在最后一号，所以取指请求优先级高于预取请求。 <br>当取指 acquire 和预取 acquire 同时发出时，fetchMSHRs(i).io.acquire 和 prefetchMSHRs(i).io.acquire 都有效，仲裁结果 acquireArb.io.out 应该和 fetchMSHRs(i).io.acquire 一致。 |

### 35. Grant 数据接收与 Refill

在收到 TileLink D 通道数据时收集整行

- 累计 beat 数（readBeatCnt），直到完成一整行 (last_fire)
- 记录 corrupt 标志
- 将完成的请求映射回对应的 MSHR (id_r = mem_grant.bits.source)

| 序号 | 名称                                     | 描述                                                                                                                                                                                                                                                                                      |
| ---- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 35.1 | 正常完整 Grant 流程，readBeatCnt 为 0 时 | readBeatCnt 初始为 0，refillCycles - 1 也为 0。 <br>io.mem_grant.valid 为高（因为 io.mem_grant.ready 默认为高，所以 io.mem_grant.fire 为高只需要 io.mem_grant.valid 为高）且 io.mem_grant.bits.opcpde(0)为高。 <br>此时 respDataReg(0)= io.mem_grant.bits.data <br>readBeatCnt 加一为 1。 |
| 35.2 | 正常完整 Grant 流程，readBeatCnt 为 1 时 | io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高。 <br>此时 respDataReg(1)= io.mem_grant.bits.data <br>readBeatCnt 重置回 0。 <br>last_fire 为高。 <br>下一拍 last_fire_r 为高，id_r=io.mem_grant.bits.source。                                                                  |
| 35.3 | 正常完整 Grant 流程，last_fire_r 为高    | last_fire_r 为高，并且 id_r 为 0-13 中的一个。 <br>对应的 fetchMSHRs 或者 prefetchMSHRs 会被无效，也就是 fetchMSHRs_i 或 prefetchMSHRs_i-4 的 io_invalid 会被置高。                                                                                                                       |
| 35.4 | Grant 带有 corrupt 标志                  | io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高，io.mem_grant.bits.corrupt 为高，则 corrupt_r 应为高。 <br>如果 io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高，io.mem_grant.bits.corrupt 为高中有一个不满足，且此时 last_fire_r 为高，则 corrupt_r 重置为低。       |

### 36. 替换策略更新 (Replacer)

MissUnit 在发出 Acquire 请求时，还会将本次选中的 victim way 对应的索引告诉 io.victim，让替换策略更新其记录（替换策略采用 PLRU）
只有当 Acquire 真正“fire”时，才说明成功替换，replacer 需要更新状态
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|36.1|正常替换更新 |当 io.mem.acquire.ready & acquireArb.io.out.valid 同时为高，也就是 acquireArb.io.out.fir 为高时，io.victim.vSetIdx.valid 也为高。 <br>io.victim.vSetIdx.bits = 当前 MSHR 请求的 acquireArb.io.out.bits.vSetIdx。 |
|36.2|生成 waymask |根据从 L2 返回的 mshr_resp 中 mshr_resp.bits.way 生成 waymask 信息。 <br>返回的 mshr_resp.bits.way 有 16 位，通过独热码生成一位掩码信息，waymask 表示其中哪一路被替换。 <br>生成的 waymask 应该和 mshr_resp.bits.way 一致。 |

### 37. 写回 SRAM (Meta / Data)

在一条 Miss Request refill 完成时，将新得到的 Cache line 写到 ICache。
生成 io.meta_write 和 io.data_write 的请求，带上 waymask, tag, idx, data 。
生成 io.meta_write.valid 和 io.data_write.valid 信号。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|37.1|生成 io.meta_write.valid 和 io.data_write.valid 信号 |当 grant 传输完成后，经过一拍后，即 last_fire_r 为高，且从 TileLink 返回的 mshr_resp 中的 mshr_resp.valid 为高。 <br>并且此时没有硬件刷新信号和软件刷新信号，也就是 io.flush 和 io.fencei 为低。 在等待 l2 响应的过程中，没有刷新信号 <br>也没有数据 corrupt，即 corrupt_r 为低。 <br>那么 io.meta_write.valid 和 io.data_write.valid 均为高。 |
|37.2|正常写 SRAM |io.meta_write.bits 的 virIdx、phyTag、waymask、bankIdx、poison 应该正常更新 <br>io.data_write.bits 的 virIdx、data、waymask、bankIdx、poison 应该正常更新 |

### 38. 向 mainPipe/prefetchPipe 发出 Miss 完成响应（fetch_resp）

在完成 refill 后，无论是否要真正写阵列，都会向取指端发送“Miss 请求完成”
更新 io.fetch_resp.valid 和 fetch_resp.bits。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|38.1|正常 Miss 完成响应 |当 grant 传输完成后，经过一拍后，即 last_fire_r 为高，且从 TileLink 返回的 mshr_resp 中的 mshr_resp.valid 为高。 <br>无论此时是否有硬件刷新信号和软件刷新信号， io.fetch_resp.valid 都为高，说明可向取指端发送响应。 <br>io.fetch_resp.bits 中的数据更新： <br>io.fetch_resp.bits.blkPaddr = mshr_resp.bits.blkPaddr <br>io.fetch_resp.bits.vSetIdx = mshr_resp.bits.vSetIdx <br>io.fetch_resp.bits.waymask = waymask <br>io.fetch_resp.bits.data = respDataReg.asUInt <br>io.fetch_resp.bits.corrupt = corrupt_r |

### 39. 处理 flush / fencei

一旦收到 io.flush 或 io.fencei 时，对未发射的请求可立即取消，对已经发射的请求在拿到数据后也不写 SRAM。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|39.1|MSHR 未发射前 fencei |如果 MSHR 还没有通过 io.acquire.fire 发出请求，就应立即取消该 MSHR（mshr_resp.valid= false），既不发出请求，也不要写 SRAM。 <br>当 io.fencei 为高时，fetchMSHRs 和 prefetchMSHRs 的 io.req.ready 和 io.acquire.valid 均为低，表示请求不发射。 |
|39.2|MSHR 未发射前 flush |由于 fetchMSHRs 的 io.flush 被直接设置为 false，所以 io.flush 对 fetchMSHRs 无效，但是对 prefetchMSHRs 有效。 <br>当 io.flush 为高时，只能发射 fetchMSHRs 的请求。 |
|39.3|MSHR 已发射后 flush/fencei |已经发射了请求，之后再有刷新信号，那么等数据回来了但不写 SRAM。 <br>在发射后，io.flush/io.fencei 为高时，等待数据回来，但是写 SRAM 的信号，write_sram_valid、io.meta_write.valid 和 io.data_write.valid 均为低，表示不写 SRAM。 <br>对于 response fetch 无影响。 |

---

以下是**CtrlUnit**模块的功能

### 40. ECC 启用/禁用

控制 eccctrl.enable 字段来启用或禁用 ECC 功能。外部系统可以通过写寄存器 eccctrl 来控制 ECC 是否启用。

- 通过寄存器写入控制信号 enable，当 enable 为 true 时，ECC 功能启用；为 false 时，ECC 功能禁用。

| 序号 | 名称     | 描述                                                                                                                                                                                                                                                                                                                                                                     |
| ---- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 40.1 | 启用 ECC | 向 eccctrl.enable 寄存器写入 true，验证模块内部 eccctrl.enable 设置为 true，并确保后续的错误注入操作能够成功进行。此测试确保 eccctrl.enable 写操作被执行。 <br>确保 eccctrl.enable 被正确设置为 true，并触发 eccctrlRegWriteFn 中的写操作逻辑。                                                                                                                          |
| 40.2 | 禁用 ECC | 向 eccctrl.enable 寄存器写入 false，验证模块内部 eccctrl.enable 设置为 false，并确保在后续的错误注入过程中，ECC 功能被禁用，不允许进行错误注入。此测试确保 eccctrl.enable 写操作被正确设置为 false。 <br>验证禁用 ECC 时 eccctrl.enable 为 false，并触发 eccctrlRegWriteFn 中的错误处理分支。x.istatus = eccctrlInjStatus.error 和 x.ierror = eccctrlInjError.notEnabled |

### 41. 状态机转换

根据状态机的状态，验证错误注入的流程是否正确。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|41.1|is_idle 状态 |初始为 is_idle 状态。 <br>当 eccctrl.istatus 为 working 时，验证此时的状态为 is_readMetaReq。 |
|41.2|is_readMetaReq 状态 |当握手成功后（io.metaRead.ready 和 io.metaRead.valid 都为高），验证此时的状态为 is_readMetaResp。 |

#### 41.3 is_readMetaResp 状态

| 序号   | 名称   | 描述                                                                                                                                                                                                                                |
| ------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 41.3.1 | 未命中 | 当 waymask 全零的时候，表示没有命中，会进入 is_idle 状态，并且设置错误错误注入状态和错误原因。 <br>验证此时的状态为 is_idle， eccctrl.istatus = error 和 eccctrl.ierror = notFound。                                                |
| 41.3.2 | 命中   | 当 waymask 不全零的时候，表示命中，会根据错误注入目标来判断是向元数据还是数据阵列写入错误。 <br>当 eccctrl.itarget=metaArray 时，验证此时的状态为 is_writeMeta ；当 eccctrl.itarget！=metaArray 时，验证此时的状态为 is_writeData。 |

#### 41.4 is_writeMeta 状态

| 序号   | 名称       | 描述                                                                                                                                                                                                                                                                                                                                                                         |
| ------ | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 41.4.1 | RegWriteFn | 此状态进入后，io.dataWrite.valid 会为高 <br>x.itarget = req.itarget <br>当 req.inject 为高并且 x.istatus = idle 时： <br>1. 如果 ecc 的 req.enable = false，则验证 x.istatus = error 且 x.ierror = notEnabled <br>2. 否则，如果 req.itarget ！= metaArray 和 dataArray，则验证 x.istatus = error 且 x.ierror = targetInvalid <br>3. 如果都不满足，则验证 x.istatus = working |
| 41.4.2 | 状态转换   | 当 io.metaWrite.fire 为高， 验证下一个状态为 is_idle，并且 eccctrl.istatus = injected。                                                                                                                                                                                                                                                                                      |

#### 41.5 is_writeData 状态

| 序号   | 名称       | 描述                                                                                                                                                                              |
| ------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 41.5.1 | RegWriteFn | 此状态进入后，io.dataWrite.valid 会为高 <br>res.inject = false <br>当 ready 为高，且 x.istatus = injected 或 x.istatus = error 时，验证 x.istatus = idle 和 x.ierror = notEnabled |
| 41.5.2 | 状态转换   | 当 io.dataWrite.fire 为高， 验证下一个状态为 is_idle，并且 eccctrl.istatus = injected。                                                                                           |

### 42. 寄存器映射和外部访问

通过 TileLink 总线将寄存器映射到特定地址，使外部模块可以读写 ECC 控制寄存器和注入地址寄存器。

- 使用 TLRegisterNode 实现寄存器的映射，使得外部系统可以通过地址访问寄存器。寄存器的读写操作通过 TileLink 协议进行。

| 序号 | 名称                          | 描述                                                                                                                            |
| ---- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 42.1 | 外部读取和写入 ECC 控制寄存器 | 验证外部模块可以通过 TileLink 协议正确读取和写入 eccctrl 和 ecciaddr 寄存器，并对模块内部的状态产生影响，确保读写操作完全覆盖。 |
| 42.2 | 外部模块触发错误注入          | 通过外部模块经 TileLink 总线向 eccctrl.inject 寄存器写入 true，触发错误注入，验证内部状态是否按 RegWriteFn 内部过程执行。       |

---

以下是**ICache 顶层**模块的功能

### 43. FTQ 预取请求处理

接收来自 FTQ 的预取请求，经 IPrefetchPipe 请求过滤（查询 ITLB 地址，是否命中 MetaArry，PMP 检查），（有异常则由 MissUnit 处理）后进入 WayLookup。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|43.1|预取地址命中，无异常 |io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 匹配，pmp 检查通过。 <br>如果没有监听到 MSHR 同样的位置发生了其它 cacheline 的写入，那么验证 wayLookup.io.write 的内容应该命中的取指数据。 <br>如果监听到 MSHR 同样的位置发生了其它 cacheline 的写入，那么验证 wayLookup.io.write 的内容应该是未命中的取指数据。 |
|43.2|预取地址未命中，无异常 |io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 不匹配，pmp 检查通过。 <br>如果监听到 MSHR 将该请求对应的 cacheline 写入了 SRAM，那么验证 wayLookup.io.write 的内容应该命中的取指数据。 <br>如果监听到 MSHR 没有将该请求对应的 cacheline 写入了 SRAM，那么验证 wayLookup.io.write 的内容应该未命中的取指数据。 |
|43.3|预取地址 TLB 异常，无其他异常 |io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 异常。 <br>验证 wayLookup.io.write 的 itlb_exception 内容中，其有对应的异常类型编号（pf:01;gpf:10;af:11）。 |
|43.4|预取地址 PMP 异常，无其他异常 |io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 匹配，pmp 检查未通过。 <br>验证 wayLookup.io.write 的 tlb_pbmt 内容中，其有对应的异常类型编号（nc:01;io:10）。 |

### 44. FTQ 取指请求处理

io.fetch.resp <> mainPipe.io.fetch.resp 发送回 IFU 的数据是在 io.fetch.resp。
接收来自 FTQ 的取指请求，从 WayLookup 获取路命中信息和 ITLB 查询结果，再访问 DataArray，监控 MSHR 的响应。更新 replacer，做 pmp 检查。后做 DataArray 和 MetaArray 的 ECC 校验。最后将数据发送给 IFU。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|44.1|取指请求命中，无异常 |io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查正常，DataArray 和 MetaArray 的 ECC 校验正常。 <br>验证 replacer.io.touch 的 vSetIdx 和 way 和 ftq 的 fetch 一致，missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。 <br>验证 io.fetch.resp 的数据应该是取指的数据。 |
|44.2|取指请求未命中，MSHR 返回的响应命中，无异常 |io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，未命中，pmp 检查正常，DataArray 和 MetaArray 的 ECC 校验正常。 <br>请求在 MSHR 返回的响应命中。 <br>验证 missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。 <br>验证 io.fetch.resp 的数据应该是取指的数据。 |
|44.3|取指请求命中,ECC 校验错误，无其他异常 |io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查正常，DataArray 或 MetaArray 的 ECC 校验错误。 <br>验证 io.error.valid 为高，且 io.error.bits 内容为对应的错误源和错误类型。 <br>先刷 MetaArray 的 ValidArray,给 MissUnit 发请求，由其在 L2 重填，阻塞至数据返回。 <br>验证 replacer.io.touch 的 vSetIdx 和 way 和 ftq 的 fetch 一致，missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。 <br>验证 io.fetch.resp 的数据应该是取指的数据。 |
|44.4|取指请求未命中，但是 exception 非 0（af、gpf、pf），无其他异常 |io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查未通过，DataArray 和 MetaArray 的 ECC 校验正常。 <br>验证 io.fetch.resp 为对应的错误源和错误类型。 <br>验证 io.fetch.resp 的数据无效，里面有异常类型。 |
|44.5|取指请求未命中，通过 WayLookup 中读取到的预取过来的 itlb 中返回 pbmt。 |有 itlb_pbmt 和 pmp_mmio 时，他们合成 s1_mmio，传递到 s2_mmio,生成 s2_miss,有特殊情况就不会取指。 <br>io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查通过，DataArray 和 MetaArray 的 ECC 校验正常。 <br>验证 io.fetch.resp 为对应的错误源和错误类型。 <br>验证 io.fetch.resp 的数据无效，里面有特殊情况类型类型。 |
|44.6|取指请求未命中，pmp 返回 mmio 。 | 处理同 5。 |

### 45. MetaArray 功能

在 IPrefetchPipe 的 S0，接收来自 IPrefetchPipe 的读请求 read，返回对应路和组的响应 readResp。
在 miss 的时候，MissUnit 会将会应的数据写入 write 到 MetaArray。
MetaArray 主要存储了每个 Cache 行的标签和 ECC 校验码。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|45.1|元数据写入操作（对应的 Set 已满）: ICacheMetaArray 应当能够正确地将元数据（标签和有效位）写入到指定的 Set 和 Way 。 |从 MissUnit 返回的请求都是未命中的请求（已命中不会向 MissUnit 请求，那么 MissUnit 自然也不会向 MetaArray 写入）。 <br>发送一个写请求 write 到 ICacheMetaArray，ICacheReplacer 根据 PLRU 替换策略指定 way，替换路被写入 waymask，最后指定 virIdx、phyTag、waymask、bankIdx、poison。 <br>写入操作后，发起一个对相同虚拟索引的读请求。验证 readResp 的 metas 和 codes 分别包含写入的 ptag 和 ecc code，并且对于写入的路，readResp.entryValid 信号被置为有效。 |
|45.2|元数据读取操作 (命中): 当一个读请求在 ICacheMetaArray 中命中时（存在有效的条目），它应该返回正确的元数据（标签和有效位）。 |首先，向特定的虚拟索引（组和路）写入元数据（参照上面的写入操作）。然后，向相同的虚拟索引发送一个读请求。 <br>验证 readResp.metas 包含之前写入的物理标签，并且对于相应的路，readResp.entryValid 信号被置为有效。 |
|45.3|元数据读取操作 (未命中): 当读取一个尚未被写入的地址时，ICacheMetaArray 应当指示未命中（条目无效）。 |向 ICacheMetaArray 发送一个读请求，请求的虚拟索引在复位后从未被写入过。 <br>验证对于任何路，readResp.entryValid 信号都没有被置为有效。 对应的 readResp.metas 和 codes 的内容是 DontCare 也就是 0。 |
|45.4|独立的缓存组刷新：在第 i 个端口是有效的刷新请求，并且该请求的 waymask 指定了当前正在处理的第 w 路时，应该使第 i 个端口的条目无效。 |先向 ICacheMetaArray 写入指定一个或多个端口的元数据，然后再给对应的端口的路发送刷新请求 io.flush，其包含虚拟索引 virIdx 和路掩码 waymask。 <br>验证 valid_array 对应的路中的 virIdx 被置为无效，io.readResp.entryValid 对应路的对应端口为无效。 |
|45.5|全部刷新操作: ICacheMetaArray 应当能够在接收到全部刷新请求时，使所有条目无效。 |先向多个不同的虚拟索引写入元数据。然后置位 io.flushAll 信号。 <br>验证步骤: 在 io.flushAll 信号置位后，发起对所有之前写入过的虚拟索引的读请求。验证在所有的读取响应中，对于任何路，readResp.entryValid 信号都没有被置为有效。 |

### 46. DataArray 功能

与 MetaArray 类似，在 MainPipe 的 S0，接收来自 MainPipe 的读请求 read，返回对应路和组的响应 readResp。
在 miss 的时候，MissUnit 会将会应的数据写入 write 到 DataArray。
DataArray 主要存储了每个 Cache 行的标签和 ECC 校验码。
| 序号 | 名称 | 描述 |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
|46.1|数据写入操作（对应的 Set 已满）: ICacheDataArray 应当能够正确地将数据写入到指定的 Set (组)、Way (路) 和数据 Bank (存储体)。 |发送一个写请求 write 到 ICacheDataArray，ICacheReplacer 根据 PLRU 替换策略指定 way，替换路被写入 waymask，最终指定虚拟索引、数据、路掩码、存储体索引 bankIdx 和毒化位。写入的数据模式应跨越多个数据存储体。 <br>写入操作后，发起一个对相同虚拟索引和块偏移量的读请求。验证 readResp.datas 与写入的数据相匹配。 |
|46.2|数据读取操作 (命中): 当一个读请求命中时（相应的元数据有效），它应该从相应的组、路和数据存储体返回正确的数据。 |首先，向特定的虚拟索引和块偏移量写入数据。然后，向相同的虚拟索引和块偏移量发送一个读请求。使用不同的块偏移量进行测试，以覆盖存储体的选择逻辑。 <br>验证 readResp.datas 包含之前写入的数据。 |
|46.3|数据读取操作 (未命中): 当读取一个尚未被写入的地址时，ICacheDataArray 的输出应该是默认值或无关值。 |向 ICacheDataArray 发送一个读请求，请求的虚拟索引在复位后从未被写入过。 <br>验证 readResp.datas 为 0。 |

---

</mrs-functions>

## ICache 接口说明

为方便测试开展，需要对 ICache 的接口进行进一步的说明，以明确各个接口的含义。

\*注意：源文件编译成 verilog/system verilog 后，部分接口会被优化，实际接口以编译后的为准。

### IPrefetch 模块接口

#### 控制接口

| 接口名        | 解释                                |
| ------------- | ----------------------------------- |
| csr_pf_enable | 控制 s1_real_fire，软件控制预取开关 |
| ecc_enable    | 编译后被优化 ，控制 ecc 开启        |
| flush         | 刷新信号                            |

#### req:FTQ 预取请求

由于 BPU 基本无阻塞，它经常能走到 IFU 的前面，于是 BPU 提供的这些还没发到 IFU 的取指请求就可以用作指令预取，FTQ 中实现了这部分逻辑，直接给 ICache 发送预取请求。
预取请求来自 FTQ，在 S0 流水级传入。
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|ready||指示 s0 能否继续|
|valid|指示软件预取或者硬件预取是否有效。|
|startAddr | 预测块起始地址。 |
|nextlineStart | 预测块下一个缓存行的起始地址。 |
|ftqIdx| 指示当前预测块在 FTQ 中的位置，包含 flag 和 value 两个量。|
|isSoftPrefetch|是否为软件预取(来自 Memblock 中 LoadUint 的软件预取请求)。|
|backendException| ICache 向 IFU 报告后端存在的异常类型。|

#### flushFromBpu:来自 BPU 的刷新信息

由 FTQ 传递而来的 BPU 刷新信息，在 S0 流水级传入。
这是预测错误引起的，包括 s2 和 s3 两个同构成员，指示是否在 BPU 的 s2 和 s3 流水级发现了问题。
s2 的详细结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|valid|指示 s2 是否有效。|
|ftqIdx|指示 s2 流水级请求冲刷的预测块在 FTQ 中的位置，包含 flag 和 value 两个量。|

#### itlb:请求和响应 itlb 的信息

在 s0 流水级，发送 itlb_req；在 s1 流水级，如果 itlb 命中则直接接收 itlb_resp，否则重发 itlb_req。

req 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|valid|指示 req 请求是否有效。|
|Tlbreq|有多个子结构，这里我们只用上了 vaddr,即 req 请求的虚拟地址|

resp 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|paddr|指令物理地址。|
|gpaddr|客户页地址。|
|pbmt|基于页面的内存类型。|
|miss|指示 itlb 是否未命中。|
|isForVSnonLeafPTE|指示是否为非叶 PTE。|
|excp|ITLB 可能产生的异常，包括：访问异常指令 af_instr、客户页错误指令 gpf_instr、页错误指令 pf_instr。见[异常传递/特殊情况处理](#异常传递特殊情况处理)|

#### itlbFlushPipe:itlb 刷新信号

在 itlb 中，如果出现 gpf 的取指请求处于推测路径上，且发现出现错误的推测，则会通过 flushPipe 信号进行刷新（包括后端 redirect、或前端多级分支预测器出现后级预测器的预测结果更新前级预测器的预测结果等）。
当 iprefetchpipe 的 s1 被刷新时，itlb 也应该被刷新，该信号会在 s1 流水被置位。

#### pmp: 物理内存保护相关的信息

在 s1 流水级做 pmp 检查。
pmp 包含 req 和 resp 两个子结构。

req 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|addr|pmp 检查的地址。|

resp 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|instr|指示物理地址是否有权限访问，没有则会引起 pmp 的 af 异常。|
|mmio|地址在 mmio 空间。|

#### metaRead： 和 MetaArray 交互的读请求和读响应

在 s1 流水级读 meta。

metaRead 包含 toIMeta 和 fromIMeta 两个子结构，即读请求和读响应。

toIMeta 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|vSetIdx|虚拟地址的缓存组索引（Virtual Set Index）。|
|isDoubleLine|预测块是否跨缓存行。|

fromIMeta 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|metas|MetaArray 的本身，包含 tag 量。tag，即 cache 的标签。|
|codes|ptag 的 ecc 校验码。|
|entryValid|指示 meta 是否有效。|

#### MSHRReq： MSHR 请求

预取逻辑检测到未命中时，在 s2 流水级，向 MissUnit 发送请求。

| 接口名   | 解释                                   |
| -------- | -------------------------------------- |
| blkPaddr | 要从 tilelink 获取的缓存行的物理地址。 |
| vSetIdx  | 虚拟地址的缓存组索引。                 |

#### MSHRResp: MSHR 响应

用于在 s1 流水级更新 waymasks 和 meta_codes 以及 s2 流水级判断返回的响应是否命中。

| 接口名   | 解释                                                                              |
| -------- | --------------------------------------------------------------------------------- |
| blkPaddr | 已从 tilelink 获取的缓存行的物理地址。                                            |
| vSetIdx  | 虚拟地址的缓存组索引。                                                            |
| waymask  | 标识由 MSHR 处理的缺失（miss）请求完成后，返回的数据块应该写入到哪个路（way）中。 |
| corrupt  | 返回的数据块是否损坏。                                                            |

#### wayLookupWrite： 向 waylookup 写数据

在 s1 流水级，向 waylookup 写数据。
包含 entry（WayLookupEntry）和 gpf（WayLookupGPFEntry）两个子结构。

entry 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|vSetIdx|虚拟地址的缓存组索引。|
|waymask|来自 MSHR 的 waymask。|
|ptag|物理地址标签。|
|itlb_exception|指示 itlb 是否产生了异常 pf/gpf/af|
|itlb_pbmt|指示 itlb 是否产生 pbmt。|
|meta_codes|meta 的 ecc 校验码。|

gpf 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|gpaddr|客户页地址。|
|isForVSnonLeafPTE|指示是否为非叶 PTE。|

### MainPipe 模块接口

#### 不需要关注的接口

`hartId`硬件线程 ID，difftest 使用，不需要关注。

`perfInfo`性能信息，不需要关注。

#### dataArray：和 DataArray 交互的读请求和读响应

在 s0 流水级读请求。

dataArray 包含 toData 和 fromData 两个子结构，即读请求和读响应。

toData 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|vSetIdx|虚拟地址的缓存组索引。|
|waymask|标识由 MSHR 处理的缺失（miss）请求完成后，返回的数据块应该写入到哪个路（way）中。通过 MissUnit 写给 prefetch，prefetch 写入 waylookup，mainpipe 从 waylookup 中读出。|
|blkOffset|指令在块中的偏移。|
|isDoubleLine|预测块是否跨缓存行。|

fromData 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|datas|DataArray 本身的数据。|
|codes|data 的 ecc 校验码。|

#### metaArrayFlush： 刷新 metaArray

在 s2 流水级，向 metaArray 发送刷新请求, 为重新取指做准备。

| 接口名  | 解释                     |
| ------- | ------------------------ |
| virIdx  | 需要刷新的虚拟地址索引。 |
| waymask | 需要刷新的路。           |

#### touch: 更新 replacer

在 s1 流水级，更新 replacer，向 replacer 发送 touch 请求。
把一次访问告诉 replacer，让它更新 plru 状态。
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|vSetIdx|被访问的缓存行的虚拟组索引。|
|way|被访问的缓存行在集合中的路。|

#### wayLookupRead： 读取预取流水写入 waylookup 的信息

在 s0 流水级，从 waylookup 获取元信息。
包含 entry（WayLookupEntry）和 gpf（WayLookupGPFEntry）两个子结构。

entry 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|waymask|来自 MSHR 的 waymask。|
|ptag|物理地址标签。|
|itlb_exception|指示 itlb 是否产生了异常 pf/gpf/af|
|itlb_pbmt|指示 itlb 是否产生 pbmt。|
|meta_codes|meta 的 ecc 校验码。|

gpf 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|gpaddr|客户页地址。|
|isForVSnonLeafPTE|指示是否为非叶 PTE。|

#### mshr: 对 MissUnit 中的 mshr 的请求和响应

在 s1 流水级，监听 MSHR 的响应。
在 s2 流水级，缺失时将请求发送至 MissUnit，同时对 MSHR 的响应进行监听，命中时寄存 MSHR 响应的数据。

包含 req 和 resp 两个子结构。

req 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|blkPaddr|要从 tilelink 获取的缓存行的物理地址。|
|vSetIdx|虚拟地址的缓存组索引。|
resp 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|blkPaddr|已从 tilelink 获取的缓存行的物理地址。|
|vSetIdx|虚拟地址的缓存组索引。|
|waymask|标识由 MSHR 处理的缺失（miss）请求完成后，返回的数据块应该写入到哪个路（way）中。|
|data|返回的数据块。|
|corrupt|返回的数据块是否损坏。|

#### fetch: 与 FTQ 交互和 IFU 交互接口

包含 req 和 resp 两个子结构。

##### req： FTQ 取指请求

在 s0 流水级，接收 FTQ 的取指请求。
包含 pcMemRead,readValid 和 backendException 三个子结构。

其中 pcMemRead 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|startAddr|预测块起始地址。|
|nextlineStart|预测块下一个缓存行的起始地址。|

readValid:读取请求的有效性。

backendException：是否有来自后端的 Exception。

##### resp: IFU 取指响应

在 s2 流水级，向 IFU 发送取指响应。

| 接口名 | 解释 |
| ------ | ---- |

|doubleLine| 指示预测块是否跨缓存行。|
|vaddr |指令块起始虚拟地址、下一个缓存行的虚拟地址。|
|data |要传送的缓存行。|
|paddr |指令块的起始物理地址|
|exception| 向 IFU 报告每个缓存行上的异常情况，方便 ICache 生成每个指令的异常向量。|
|pmp_mmio| 指示当前指令块是否在 MMIO 空间。|
|itlb_pbmt |ITLB 基于客户页的内存类型，对 MMIO 状态有用。|
|backendException| 后端是否存在异常。|
|gpaddr| 客户页地址。|
|isForVSnonLeafPTE| 是否为非叶的 PTE，来自 itlb。|

#### flush：全局刷新信号

来自 FTQ。

#### pmp: 物理内存保护相关的信息

在 s1 流水级做 pmp 检查。
pmp 包含 req 和 resp 两个子结构。

req 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|addr|需要检查的地址|

resp 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|instr|指示物理地址是否有权限访问，没有则会引起 pmp 的 af 异常。|
|mmio|地址在 mmio 空间。|

#### respStall

IFU 的 f3_ready 为低时会被置位,表示 IFU 没有准备好接收数据，此时需要 stall。

#### errors: 向 BEU 报告指令缓存中检测到的错误

在 s2 流水级，综合 data 的 ECC 校验加上从 s1 传来的 meta 的 ECC 校验结果，决定是否向 BEU 报告错误。

编译后：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|valid|指示 errors 是否有效。|
|bits|有两个量。paddr 表示错误的物理地址，report_to_beu 表示是否向 beu 报告错误|

#### perfInfo： 性能相关信息，不关注

### WayLookup 模块接口

#### flush：全局刷新信号

来自 FTQ。

#### read：Mainpipe 的读接口

包含 entry（WayLookupEntry）和 gpf（WayLookupGPFEntry）两个子结构。

entry 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|waymask|来自 MSHR 的 waymask。|
|ptag|物理地址标签。|
|itlb_exception|指示 itlb 是否产生了异常 pf/gpf/af|
|itlb_pbmt|指示 itlb 是否产生 pbmt。|
|meta_codes|meta 的 ecc 校验码。|

gpf 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|gpaddr|客户页地址。|
|isForVSnonLeafPTE|指示是否为非叶 PTE。|

#### write：IprefetchPipe 的写接口

包含 entry（WayLookupEntry）和 gpf（WayLookupGPFEntry）两个子结构。

entry 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|vSetIdx|虚拟地址的缓存组索引。|
|waymask|来自 MSHR 的 waymask。|
|ptag|物理地址标签。|
|itlb_exception|指示 itlb 是否产生了异常 pf/gpf/af|
|itlb_pbmt|指示 itlb 是否产生 pbmt。|
|meta_codes|meta 的 ecc 校验码。|

gpf 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|gpaddr|客户页地址。|
|isForVSnonLeafPTE|指示是否为非叶 PTE。|

#### update：MissUnit 的更新接口

在 IPrefetchPipe 中等待入队 WayLookup 阶段和在 WayLookup 中等待出队阶段，可能会发生 MSHR 对 Meta/DataArray 的更新。也就是命中状态可能在出入队 WayLookup 时不同。

| 接口名   | 解释                                                                              |
| -------- | --------------------------------------------------------------------------------- |
| blkPaddr | 已从 tilelink 获取的缓存行的物理地址。                                            |
| vSetIdx  | 虚拟地址的缓存组索引。                                                            |
| waymask  | 标识由 MSHR 处理的缺失（miss）请求完成后，返回的数据块应该写入到哪个路（way）中。 |
| corrupt  | 返回的数据块是否损坏。                                                            |

### MissUnit 模块接口

#### fencei： 软件刷新信号

#### flush：全局刷新信号

来自 FTQ。

#### fetch_req：MainPipe 的取指请求缺失时的请求

| 接口名   | 解释                                   |
| -------- | -------------------------------------- |
| blkPaddr | 要从 tilelink 获取的缓存行的物理地址。 |
| vSetIdx  | 虚拟地址的缓存组索引。                 |

#### fetch_respf: MainPipe 的取指响应缺失时的响应

| 接口名   | 解释                                                                              |
| -------- | --------------------------------------------------------------------------------- |
| blkPaddr | 已从 tilelink 获取的缓存行的物理地址。                                            |
| vSetIdx  | 虚拟地址的缓存组索引。                                                            |
| waymask  | 标识由 MSHR 处理的缺失（miss）请求完成后，返回的数据块应该写入到哪个路（way）中。 |
| data     | 返回的数据块。                                                                    |
| corrupt  | 返回的数据块是否损坏。                                                            |

#### prefetch_req: IPrefetchPipe 的预取请求缺失时的请求

| 接口名   | 解释                                   |
| -------- | -------------------------------------- |
| blkPaddr | 要从 tilelink 获取的缓存行的物理地址。 |
| vSetIdx  | 虚拟地址的缓存组索引。                 |

#### meta_write: MetaArray 的写请求接口

| 接口名  | 解释                       |
| ------- | -------------------------- |
| virIdx  | 需要写入的虚拟地址索引。   |
| phyTag  | 需要写入的物理地址标签。   |
| waymask | 指示写入哪一路。           |
| bankIdx | 指示写入哪一个存储体索引。 |

#### data_write: DataArray 的写请求接口

| 接口名  | 解释                     |
| ------- | ------------------------ |
| virIdx  | 需要写入的虚拟地址索引。 |
| data    | 需要写入的数据块。       |
| waymask | 需要写入的路。           |

#### victim：与缓存的替换器（replacer）交互，获取需要被替换的缓存路（way）的信息

| 接口名  | 解释                   |
| ------- | ---------------------- |
| vSetIdx | 虚拟地址的缓存组索引。 |
| way     | 被替换的路。           |

#### mem_acquire：Tilelink a 通道发送请求

L2 的总线空闲时，发送请求。

| 接口名  | 解释                         |
| ------- | ---------------------------- |
| source  | 标识发起此请求的源。         |
| address | 要访问的内存的起始物理地址。 |

#### mem_grant：Tilelink d 通道返回数据

| 接口名  | 解释                                                                                               |
| ------- | -------------------------------------------------------------------------------------------------- |
| opcode  | 标识响应消息类型的关键字段，它指示了响应的性质和意图。针对 acquire 请求的响应是 GrantData (5,授予) |
| source  | 请求的源标识。                                                                                     |
| data    | 返回的数据块。                                                                                     |
| corrupt | 返回的数据块是否损坏。                                                                             |

### FIFO 模块接口

#### enq: 入队信号

| 接口名 | 解释                |
| ------ | ------------------- |
| valid  | 指示 enq 是否有效。 |
| bits   | 要入队的数据。      |

#### deq: 出队信号

| 接口名 | 解释                |
| ------ | ------------------- |
| ready  | 指示 deq 是否就绪。 |
| bits   | 要出队的数据。      |

### Replacer 模块接口

#### touch： 更新 replacer

| 接口名  | 解释                         |
| ------- | ---------------------------- |
| vSetIdx | 被访问的缓存行的虚拟组索引。 |
| way     | 被访问的缓存行在集合中的路。 |

#### victim： 与缓存的替换器（replacer）交互，获取需要被替换的缓存路（way）的信息

| 接口名  | 解释                   |
| ------- | ---------------------- |
| vSetIdx | 虚拟地址的缓存组索引。 |
| way     | 被替换的路。           |

### MetaArray 模块接口

#### write: MetaArray 的写请求接口

写请求来自 MissUnit 或者 CtrlUnit。

| 接口名  | 解释                       |
| ------- | -------------------------- |
| virIdx  | 需要写入的虚拟地址索引。   |
| phyTag  | 需要写入的物理地址标签。   |
| waymask | 指示写入哪一路。           |
| bankIdx | 指示写入哪一个存储体索引。 |
| poison  | 指示是否为毒化位。         |

#### read: MetaArray 的读请求接口

| 接口名       | 解释                                        |
| ------------ | ------------------------------------------- |
| vSetIdx      | 虚拟地址的缓存组索引（Virtual Set Index）。 |
| isDoubleLine | 预测块是否跨缓存行。                        |

#### readResp： MetaArray 的读响应接口

fromIMeta 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|metas|MetaArray 的本身，包含 tag 量。tag，即 cache 的标签。|
|codes|ptag 的 ecc 校验码。|
|entryValid|指示 meta 是否有效。|

#### flush：双端刷新信号

来自 MainPipe 的刷新信号。可以只刷新指定的某一个端口，也可以都刷新。

| 接口名  | 解释                     |
| ------- | ------------------------ |
| virIdx  | 需要刷新的虚拟地址索引。 |
| waymask | 需要刷新的路。           |

#### flushAll：刷新所有 MetaArray

来自软件刷新信号 fencei。

### DataArray 模块接口

#### write：DataArray 的写请求接口

来自 MissUnit 或者 CtrlUnit 的写请求。

| 接口名  | 解释                     |
| ------- | ------------------------ |
| virIdx  | 需要写入的虚拟地址索引。 |
| data    | 需要写入的数据块。       |
| waymask | 需要写入的路。           |
| poison  | 指示是否为毒化位。       |

#### read：DataArray 的读请求接口

来自 MainPipe 的读请求。

| 接口名    | 解释                                                                                                                                                                  |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| vSetIdx   | 虚拟地址的缓存组索引。                                                                                                                                                |
| waymask   | 标识由 MSHR 处理的缺失（miss）请求完成后，返回的数据块应该写入到哪个路（way）中。通过 MissUnit 写给 prefetch，prefetch 写入 waylookup，mainpipe 从 waylookup 中读出。 |
| blkOffset | 指令在块中的偏移。                                                                                                                                                    |

#### readResp：DataArray 的读响应接口

| 接口名 | 解释                   |
| ------ | ---------------------- |
| datas  | DataArray 本身的数据。 |
| codes  | data 的 ecc 校验码。   |

### CtrlUnit 模块接口

#### auto_in: Tilelink 相关接口

CtrlUnit 和 Tilelink 交互，分为 a 通道和 d 通道。

a 通道：
| 接口名 | 解释 |
| ------- | ---------------------------- |
|opcode|标识携带消息类型。|
|size|传输的数据大小对数，表示操作的字节数为$2^n$。|
|source| 标识发起此请求的源，主设备源标识符。 |
|address|传输的目标字节地址。|
|mask|要读的字节通道。|
|data|忽略。|

d 通道：
| 接口名 | 解释 |
| ------- | ---------------------------- |
|opcode|标识携带消息类型。|
|size|传输的数据大小对数，表示操作的字节数为$2^n$。|
|source| 标识发起此请求的源，主设备源标识符。 |
|data|数据载荷。|

#### ecc_enable： ecc 控制信号

指示 ecc 是否开启。

#### injecting： ecc 注入信号

指示 eccctrl 的 istatus 域是否处于 working 状态，即收到注入请求，注入中

#### metaRead： 对 MetaArray 的读请求

在对应读状态机 is_readMetaReq 中，对 MetaArray 发起读请求。
| 接口名 | 解释 |
| ------------ | ------------------------------------------- |
| vSetIdx | 要读取的拟地址的缓存组索引。 |

#### metaReadResp： 对 MetaArray 的读响应

在状态机 is_readMetaResp 中，接收 MetaArray 的读响应。

| 接口名     | 解释                                                  |
| ---------- | ----------------------------------------------------- |
| metas      | MetaArray 的本身，包含 tag 量。tag，即 cache 的标签。 |
| entryValid | 指示 meta 是否有效。                                  |

#### metaWrite： 对 MetaArray 的写

在状态机 is_writeMeta 中，对 MetaArray 发起写。

| 接口名  | 解释                       |
| ------- | -------------------------- |
| virIdx  | 需要写入的虚拟地址索引。   |
| phyTag  | 需要写入的物理地址标签。   |
| waymask | 指示写入哪一路。           |
| bankIdx | 指示写入哪一个存储体索引。 |

#### dataWrite： 对 DataArray 的写请求

在状态机 is_writeData 中，对 DataArray 发起写请求。

| 接口名  | 解释                     |
| ------- | ------------------------ |
| virIdx  | 需要写入的虚拟地址索引。 |
| waymask | 需要写入的路。           |

### ICache 顶层模块接口

在 scala 代码中，顶层模块除了包含对外的接口，实际上还包括了 MetaArray、DataArray 和 Replacer。在编译成 verilog 后，这三个模块会被编译成三个独立的模块，然后再通过顶层模块的接口连接起来。

#### 不需要关注的接口

`hartId`硬件线程 ID，difftest 使用，不需要关注。
`perfInfo`性能信息，不需要关注。

#### auto_ctrlUnitOpt_in：CtrlUnit 和 Tilelink 交互的接口

CtrlUnit 和 Tilelink 交互，分为 a 通道和 d 通道。

a 通道：
| 接口名 | 解释 |
| ------- | ---------------------------- |
|opcode|标识携带消息类型。|
|size|传输的数据大小对数，表示操作的字节数为$2^n$。|
|source| 标识发起此请求的源，主设备源标识符。 |
|address|传输的目标字节地址。|
|mask|要读的字节通道。|
|data|忽略。|

d 通道：
| 接口名 | 解释 |
| ------- | ---------------------------- |
|opcode|标识携带消息类型。|
|size|传输的数据大小对数，表示操作的字节数为$2^n$。|
|source| 标识发起此请求的源，主设备源标识符。 |
|data|数据载荷。|

#### auto_client_out： MissUnit 和 Tilelink 交互的接口

MissUnit 和 Tilelink 交互，分为 a 通道和 d 通道。
a 通道：
| 接口名 | 解释 |
| ------- | ---------------------------- |
| source | 标识发起此请求的源。 |
| address | 要访问的内存的起始物理地址。 |

d 通道：

| 接口名  | 解释                                                                                               |
| ------- | -------------------------------------------------------------------------------------------------- |
| opcode  | 标识响应消息类型的关键字段，它指示了响应的性质和意图。针对 acquire 请求的响应是 GrantData (5,授予) |
| source  | 请求的源标识。                                                                                     |
| data    | 返回的数据块。                                                                                     |
| corrupt | 返回的数据块是否损坏。                                                                             |

#### fetch: 与 FTQ 交互和 IFU 交互接口

包含 req 和 resp 两个子结构。

##### req： FTQ 取指请求

在 s0 流水级，接收 FTQ 的取指请求。
包含 pcMemRead,readValid 和 backendException 三个子结构。

其中 pcMemRead 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|startAddr|预测块起始地址。|
|nextlineStart|预测块下一个缓存行的起始地址。|

readValid:读取请求的有效性。

backendException：是否有来自后端的 Exception。

##### resp: IFU 取指响应

在 s2 流水级，向 IFU 发送取指响应。

| 接口名            | 解释                                                                    |
| ----------------- | ----------------------------------------------------------------------- |
| doubleLine        | 指示预测块是否跨缓存行。                                                |
| vaddr             | 指令块起始虚拟地址、下一个缓存行的虚拟地址。                            |
| data              | 要传送的缓存行。                                                        |
| paddr             | 指令块的起始物理地址                                                    |
| exception         | 向 IFU 报告每个缓存行上的异常情况，方便 ICache 生成每个指令的异常向量。 |
| pmp_mmio          | 指示当前指令块是否在 MMIO 空间。                                        |
| itlb_pbmt         | ITLB 基于客户页的内存类型，对 MMIO 状态有用。                           |
| backendException  | 后端是否存在异常。                                                      |
| gpaddr            | 客户页地址。                                                            |
| isForVSnonLeafPTE | 是否为非叶的 PTE，来自 itlb。                                           |

#### ftqPrefetch:FTQ 预取相关信息

包含三个子结构：
req： 来自 FTQ 的预取请求
flushFromBpu:来自 BPU 的刷新信息
bakckendException:来自后端的异常信息

##### req： 来自 FTQ 的预取请求

由于 BPU 基本无阻塞，它经常能走到 IFU 的前面，于是 BPU 提供的这些还没发到 IFU 的取指请求就可以用作指令预取，FTQ 中实现了这部分逻辑，直接给 ICache 发送预取请求。
预取请求来自 FTQ，在 MainPipe 的 S0 流水级传入。
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|ready||指示 s0 能否继续|
|valid|指示软件预取或者硬件预取是否有效。|
|startAddr | 预测块起始地址。 |
|nextlineStart | 预测块下一个缓存行的起始地址。 |
|ftqIdx| 指示当前预测块在 FTQ 中的位置，包含 flag 和 value 两个量。|

##### flushFromBpu:来自 BPU 的刷新信息

由 FTQ 传递而来的 BPU 刷新信息，在 MainPipe 的 S0 流水级传入。
这是预测错误引起的，包括 s2 和 s3 两个同构成员，指示是否在 BPU 的 s2 和 s3 流水级发现了问题。
s2 的详细结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|valid|指示 s2 是否有效。|
|ftqIdx|指示 s2 流水级请求冲刷的预测块在 FTQ 中的位置，包含 flag 和 value 两个量。|

##### backendException： 后端异常信息

ICache 向 IFU 报告后端存在的异常类型

#### softPrefetch： 来自 Memblock 的软件预取信息

| 接口名 | 解释                 |
| ------ | -------------------- |
| vaddr  | 软件预取的虚拟地址。 |

#### stop： IFU 发送到 ICache 的停止信号

IFU 在 F3 流水级之前出现了问题，通知 ICache 停下。

#### ToIFU： 发送给 I FU 的就绪信号

由 MainPipe 的 s0 流水级 s0_can_go 生成。该信号用于提醒 IFU，Icache 的流水可用，可以发送换存行了。

#### pmp： MainPipe 和 PrefetchPipe 的 pmp 信息

0,1 通道为 MainPipe 的 pmp 信息，2,3 通道为 PrefetchPipe 的 pmp 信息。
pmp 包含 req 和 resp 两个子结构。

req 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|addr|需要检查的地址|

resp 的结构如下（编译后）：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|instr|指示物理地址是否有权限访问，没有则会引起 pmp 的 af 异常。|
|mmio|地址在 mmio 空间。|

#### itlb：PrefetchPipe 的 itlb 信息

在 PrefetchPipe 的 s0 流水级，发送 itlb_req；在 PrefetchPipe 的 s1 流水级，如果 itlb 命中则直接接收 itlb_resp，否则重发 itlb_req。

itlb 包含 req 和 resp 两个子结构。

req 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|valid|指示 req 请求是否有效。|
|Tlbreq|有多个子结构，这里我们只用上了 vaddr,即 req 请求的虚拟地址|

resp 的结构如下：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|paddr|指令物理地址。|
|gpaddr|客户页地址。|
|pbmt|基于页面的内存类型。|
|miss|指示 itlb 是否未命中。|
|isForVSnonLeafPTE|指示是否为非叶 PTE。|
|excp|ITLB 可能产生的异常，包括：访问异常指令 af_instr、客户页错误指令 gpf_instr、页错误指令 pf_instr。见[异常传递/特殊情况处理](#异常传递特殊情况处理)|

#### itlbFlushPipe： itlb 刷新信号

在 itlb 中，如果出现 gpf 的取指请求处于推测路径上，且发现出现错误的推测，则会通过 flushPipe 信号进行刷新（包括后端 redirect、或前端多级分支预测器出现后级预测器的预测结果更新前级预测器的预测结果等）。
当 iprefetchpipe 的 s1 被刷新时，itlb 也应该被刷新，该信号会在 iprefetchpipe 的 s1 流水被置位。

#### error：向 BEU 报告指令缓存中检测到的错误

将 MainPipe 中收集到的 errors 多个错误信息，使用优先级选择器选择索引最小且有效的错误信息，然后通过 error 信号发送给 BEU。接口结构和 MainPipe 中相同，区别在于 MainPipe 中有两个端口，所以有两个 errors,而这里要发送的只有一个。

编译后：
| 接口名 | 解释 |
| ---------- | ------------------------------------------------------ |
|valid|指示 errors 是否有效。|
|bits|有两个量。paddr 表示错误的物理地址，report_to_beu 表示是否向 beu 报告错误|

#### csr_pf_enable

控制 s1_real_fire，软件控制预取开关

#### fencei： 软件刷新信号

#### flush： 全局刷新信号

在 FTQ 中，有后端重新定向或者 IFU 重定向时，会将其 icacheFlush 信号拉高，触发 icache 的刷新。

## **<a id="icache_functions">测试点汇总 </a>**

再次声明，本测试点仅供参考，如果有其他测试点需要补充可以告知我们。

建议覆盖点采用`功能名称`\_`测试点名称`命名。

<mrs-testpoints>

| 序号   | 功能名称                                                                           | 测试点名称                                           | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | ---------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | 
| 1.1.1  | [ICACHE_PREFETCH_HARDPREFETCH](#11-硬件预取请求)                                   | RECEIVE                                              | 当预取请求有效且 IPrefetchPipe 处于空闲状态时，预取请求应该被接收。<br> s0_fire 信号在没有 s0 的刷新信号（ s0_flush 为低）时，应该被置为高。                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.1.2  | ICACHE_PREFETCH_HARDPREFETCH                                                       | INVALID_PREFETCH                                     | 当预取请求无效时，预取请求应该被拒绝。<br> s0_fire 信号应该被置为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.1.3  | ICACHE_PREFETCH_HARDPREFETCH                                                       | PREFETCHPIPE_BUSY                                    | 当 IPrefetchPipe 非空闲时，预取请求应该被拒绝。<br> s0_fire 信号应该被置为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 1.1.4  | ICACHE_PREFETCH_HARDPREFETCH                                                       | INVALID_PREFETCH_AND_PREFETCHPIPE_BUSY               | 当预取请求无效且 IPrefetchPipe 非空闲时，预取请求应该被拒绝。<br>s0_fire 信号应该被置为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 1.1.5  | ICACHE_PREFETCH_HARDPREFETCH                                                       | SINGLE_CACHELINE                                     | 当预取请求有效且为单 cacheline 时，预取请求应该被接收。<br>s0_fire 为高，s0_doubleline 应该被置低（false）。                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.1.6  | ICACHE_PREFETCH_HARDPREFETCH                                                       | DOUBLE_CACHELINE                                     | 当预取请求有效且为双 cacheline 时，预取请求应该被接收。<br> s0_fire 为高，s0_doubleline 应该被置高（true）。                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| 1.2.1  | [ICACHE_PREFETCH_SOFTPREFETCH](#12-软件预取请求)                                   | RECEIVE                                              | 当预取请求有效且 IPrefetchPipe 处于空闲状态时，软件预取请求应该被接收。<br>当预取请求有效且 IPrefetchPipe 处于空闲状态时，软件预取请求应该被接收。                                                                                                                                                                                                                                                                                                                                                                                               |
| 1.2.2  | ICACHE_PREFETCH_SOFTPREFETCH                                                       | INVALID_PREFETCH                                     | 当预取请求无效时，软件预取请求应该被拒绝。<br>s0_fire 信号应该被置为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 1.2.3  | ICACHE_PREFETCH_SOFTPREFETCH                                                       | PREFETCHPIPE_BUSY                                    | 当 IPrefetchPipe 非空闲时，软件预取请求应该被拒绝。<br>s0_fire 信号应该被置为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 1.2.4  | ICACHE_PREFETCH_SOFTPREFETCH                                                       | INVALID_PREFETCH_AND_PREFETCHPIPE_BUSY               | 当预取请求无效且 IPrefetchPipe 非空闲时，软件预取请求应该被拒绝。<br> s0_fire 信号应该被置为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 1.2.5  | ICACHE_PREFETCH_SOFTPREFETCH                                                       | SINGLE_CACHELINE                                     | 当软件预取请求有效且为单 cacheline 时，软件预取请求应该被接收。<br>s0_fire 为高，s0_doubleline 应该被置低（false）。                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 1.2.6  | ICACHE_PREFETCH_SOFTPREFETCH                                                       | DOUBLE_CACHELINE                                     | 当软件预取请求有效且为双 cacheline 时，软件预取请求应该被接收。<br> s0_fire 为高，s0_doubleline 应该被置高（true）。                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 2.1.1  | [ICACHE_PREFETCH_ITLB_ADDR](#21-地址转换完成)                                      | RETURN_PADDR                                         | ITLB 在一个周期内成功返回物理地址 paddr，s1_valid 为高。<br> 确认 s1 阶段正确接收到 paddr。                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 2.1.2  | ICACHE_PREFETCH_ITLB_ADDR                                                          | TLB_MISS                                             | fromITLB(PortNumber).bits.miss 为高，表示对应通道的 ITLB 发生了 TLB 缺失，需要重发。<br> 重发完成后，后续步骤继续进行，fromITLB(PortNumber).bits.miss 为低。                                                                                                                                                                                                                                                                                                                                                                                     |
| 2.2.1  | [ICACHE_PREFETCH_ITLB_EXCEPTION](#22-处理-itlb-异常)                               | PF                                                   | s1_itlb_exception 返回的页错误。<br> iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示页错误 pf。                                                                                                                                                                                                                                                                                                                                                                                                           |
| 2.2.2  | ICACHE_PREFETCH_ITLB_EXCEPTION                                                     | PGF                                                  | s1_itlb_exception 返回的虚拟机页错误。<br> iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示虚拟机页错误 pgf。                                                                                                                                                                                                                                                                                                                                                                                              |
| 2.2.3  | ICACHE_PREFETCH_ITLB_EXCEPTION                                                     | AF                                                   | s1_itlb_exception 返回的访问错误。<br> iTLB 返回的物理地址有效（fromITLB(PortNumber).bits.miss 为低），s1_itlb_exception 指示访问错误 af。                                                                                                                                                                                                                                                                                                                                                                                                       |
| 2.3.1  | [ICACHE_PREFETCH_ITLB_GPADDR](#23-处理虚拟机物理地址用于虚拟化)                    | PGF                                                  | 发生 pgf 后，需要返回对应的 gpaddr。<br> 只有一个通道发生 pgf 时，返回对应通道的 gpaddr 即可；多个通道发生 pgf 时，返回第一个通道的 gpaddr。                                                                                                                                                                                                                                                                                                                                                                                                     |
| 2.3.2  | ICACHE_PREFETCH_ITLB_GPADDR                                                        | VS_NONLEAF_PTE                                       | 发生 gpf 后，如果是访问二级虚拟机的非叶子页表项时，需要返回对应的 gpaddr。<br> 只有一个通道发生 pgf 时，返回对应通道的 gpaddr 即可；多个通道发生 pgf 时，返回第一个通道的 gpaddr。                                                                                                                                                                                                                                                                                                                                                               |
| 2.4    | [ICACHE_PREFETCH_ITLB_PBMT](#24-返回基于页面的内存类型-pbmt-信息)                  | PBMT                                                 | TLB 有效时，返回 pbmt 信息。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 3.1    | [ICACHE_PREFETCH_IMETA](#3-接收来自-imeta缓存元数据的响应并检查缓存命中)           | PTAG_AND_VALID                                       | 从物理地址中提取物理标签（ptag），将其与缓存元数据中的标签进行比较，检查所有缓存路（Way）。检查有效位，确保只考虑有效的缓存行。                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 3.1    | ICACHE_PREFETCH_IMETA                                                              | MISS                                                 | 当标签不匹配或者标签匹配，但是有效位为假时，表示缓存未命中。 <br>s1_meta_ptags(PortNumber)(nWays) 不等于 ptags(PortNumber) 或者它们相等，但是对应的 s1_meta_valids 为低时，总之返回的 waymasks 为全 0。                                                                                                                                                                                                                                                                                                                                          |
| 3.2    | ICACHE_PREFETCH_IMETA                                                              | SINGLE_HIT                                           | 当标签匹配，且有效位为真时，表示缓存命中。 <br>waymasks 对应的位为 1。                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 4.1    | [ICACHE_PREFETCH_PMP](#4-pmp物理内存保护权限检查)                                  | NONE_EXCEPTION                                       | itlb 返回的物理地址在 PMP 允许的范围内。 <br>s1_pmp_exception(i) 为 none。                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 4.2    | ICACHE_PREFETCH_PMP                                                                | AF_EXCEPTION                                         | s1_req_paddr(i) 对应的地址在 PMP 禁止的范围内。 <br>s1_pmp_exception(i) 为 af。                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 4.3    | ICACHE_PREFETCH_PMP                                                                | MMIO                                                 | itlb 返回的物理地址在 MMIO 区域。 <br>s1_pmp_mmio 为高。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 5.1    | [ICACHE_PREFETCH_EXCEPTION_MERGE](#5-异常处理和合并)                               | ONLY_ITLB_EXCEPTION                                  | s1_itlb_exception(i) 为非零，s1_pmp_exception(i) 为零。 <br>s1_exception_out(i) 正确包含 ITLB 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 5.2    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | ONLY_PMP_EXCEPTION                                   | s1_itlb_exception(i) 为零，s1_pmp_exception(i) 为非零。 <br>s1_exception_out(i) 正确包含 PMP 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 5.3    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | ONLY_BACKEND_EXCEPTION                               | s1_itlb_exception(i) 为零，s1_pmp_exception(i) 为零。 <br>s1_exception_out(i) 正确包含 后端 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 5.4    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | ITLB_AND_PMP_EXCEPTION                               | s1_itlb_exception(i) 和 s1_pmp_exception(i) 都为非零。 <br>s1_exception_out(i) 包含 ITLB 异常（优先级更高）。                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 5.5    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | ITLB_AND_BACKEND_EXCEPTION                           | s1_itlb_exception(i) 和 s1_backendException(i) 都为非零。 <br>s1_exception_out(i) 包含 后端 异常（优先级更高）。                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 5.6    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | PMP_AND_BACKEND_EXCEPTION                            | s1_pmp_exception(i) 和 s1_backendException(i) 都为非零。 <br>s1_exception_out(i) 包含 后端 异常（优先级更高）。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 5.7    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | ALL_EXCEPTION                                        | s1_itlb_exception(i)、s1_pmp_exception(i) 和 s1_backendException(i) 都为非零。 <br>s1_exception_out(i) 包含 后端 异常（优先级更高）。                                                                                                                                                                                                                                                                                                                                                                                                            |
| 5.8    | ICACHE_PREFETCH_EXCEPTION_MERGE                                                    | NONE_EXCEPTION                                       | s1_itlb_exception(i)、s1_pmp_exception(i)、s1_backendException(i) 都为零。 <br>s1_exception_out(i) 指示无异常。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 6.1    | [ICACHE_PREFETCH_WAYLOOKUP](#6-发送请求到-waylookup-模块)                          | NORMAL                                               | toWayLookup.valid 为高，toWayLookup.ready 为高，s1_isSoftPrefetch 为假。 <br>请求成功发送，包含正确的地址、标签、waymask 和异常信息。                                                                                                                                                                                                                                                                                                                                                                                                            |
| 6.2    | ICACHE_PREFETCH_WAYLOOKUP                                                          | WAYLOOKUP_REJECT                                     | toWayLookup.valid 为高，toWayLookup.ready 为假。 <br>状态机等待 WayLookup 准备好，不会错误地推进。                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 6.3    | ICACHE_PREFETCH_WAYLOOKUP                                                          | SOFTPREFETCH_NOT_GO_WAYLOOKUP                        | s1_isSoftPrefetch 为真。 <br>toWayLookup.valid 为假，不会发送预取请求到 WayLookup。                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 7.1.1  | [ICACHE_PREFETCH_FSM_IDLE](#71-初始为-m_idle-状态)                                 | NORMAL_IMPEL_KEEP_IDLE                               | s1_valid 为高，itlb_finish 为真，toWayLookup.fire 为真，s2_ready 为真。 <br>状态机保持在 m_idle 状态，s1 阶段顺利推进。                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 7.1.2  | ICACHE_PREFETCH_FSM_IDLE                                                           | ITLB_UNFINISH_RESEND                                 | s1_valid 为高，itlb_finish 为假。 <br>状态机进入 m_itlbResend 状态，等待 ITLB 完成。                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 7.1.3  | ICACHE_PREFETCH_FSM_IDLE                                                           | ITLB_FINISH_WAYLOOKUP_MISS                           | s1_valid 为高，itlb_finish 为真，toWayLookup.fire 为假。 <br>状态机进入 m_enqWay 状态，等待 WayLookup 入队。                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 7.2.1  | ICACHE_PREFETCH_FSM_ITLBRESEND                                                     | WAIT_WAYLOOKUP_ENQ                                   | itlb_finish 为假，toMeta.ready 为真。 <br>状态机进入 m_enqWay 状态，等待 WayLookup 入队。                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 7.2.2  | ICACHE_PREFETCH_FSM_ITLBRESEND                                                     | WAIT_META_READ_REQ                                   | itlb_finish 为假，toMeta.ready 为假。 <br>状态机进入 m_metaResend 状态，MetaArray 读请求                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 7.3    | ICACHE_PREFETCH_FSM_METARESEND                                                     | WAIT_WAYLOOKUP_ENQ                                   | toMeta.ready 为真。 <br>状态机进入 m_enqWay 状态，等待 WayLookup 入队。                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 7.4.1  | ICACHE_PREFETCH_FSM_ENQWAY                                                         | ENTER_IDLE                                           | toWayLookup.fire 或 s1_isSoftPrefetch 为真，s2_ready 为假。 <br>状态机进入空闲状态 m_idle。                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 7.4.2  | ICACHE_PREFETCH_FSM_ENQWAY                                                         | WAIT_ENTERS2                                         | toWayLookup.fire 或 s1_isSoftPrefetch 为真，s2_ready 为真。 <br>状态机进入 m_enterS2 状态，等待 s2 阶段准备好。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 7.5    | ICACHE_PREFETCH_FSM_ENTERS2                                                        | ENTER_IDLE                                           | s2_ready 为真。 <br>状态机进入空闲状态 m_idle。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 8.1    | [ICACHE_PREFETCH_MISSUNIT_MONITER](#8-监控-missunit-的请求)                        | MATCH_AND_VALID                                      | s2_req_vSetIdx 和 s2_req_ptags 与 fromMSHR 中的数据匹配，且 fromMSHR.valid 为高，fromMSHR.bits.corrupt 为假。 <br>s2_MSHR_match(PortNumber) 为真, s2_MSHR_hits(PortNumber) 应保持为真                                                                                                                                                                                                                                                                                                                                                            |
| 8.2    | ICACHE_PREFETCH_MISSUNIT_MONITER                                                   | SRAM_HIT                                             | s2_waymasks(PortNumber) 中有一位为高，表示在缓存中命中。 <br>s2_SRAM_hits(PortNumber) 为真,s2_hits(PortNumber) 应为真。                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 8.3    | ICACHE_PREFETCH_MISSUNIT_MONITER                                                   | MISS                                                 | 请求未匹配 MSHR，且 s2_waymasks(PortNumber) 为空。 <br>s2_MSHR_hits(PortNumber)、s2_SRAM_hits(PortNumber) 均为假, s2_hits(PortNumber) 为假。                                                                                                                                                                                                                                                                                                                                                                                                     |
| 9.1.1  | [ICACHE_PREFETCH_MISSUNIT_REQ](#91-确定需要发送给-missunit-的请求)                 | SEND_TO_MISSUNIT                                     | s2_hits(PortNumber) 为假(未命中缓存)，s2_exception 无异常，s2_mmio 为假(不是 MMIO 或不可缓存的内存)。 <br>s2_miss(PortNumber) 为真，表示需要发送请求到 missUnit。                                                                                                                                                                                                                                                                                                                                                                                |
| 9.1.2  | ICACHE_PREFETCH_MISSUNIT_REQ                                                       | NO_SEND_TO_MISSUNIT                                  | s2_hits(i) 为真（已命中）或者 s2_exception 有异常 或者 s2_mmio 为真（MMIO 访问）。 <br>s2_miss(i) 为假，不会发送请求到 missUnit。                                                                                                                                                                                                                                                                                                                                                                                                                |
| 9.1.3  | ICACHE_PREFETCH_MISSUNIT_REQ                                                       | DOUBLE_PREFETCH                                      | s2_doubleline 为真，处理第二个请求。 <br>如果第一个请求有异常或 MMIO，s2_miss(1) 应为假，后续请求被取消或处理。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 9.2.1  | [ICACHE_PREFETCH_MISSUNIT_UNIQUE](#92-避免发送重复请求发送请求到-missunit)         | RESET_HAS_SEND                                       | s1_real_fire 为高。 <br>has_send(PortNumber) 应被复位为假，表示新的请求周期开始。                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 9.2.2  | ICACHE_PREFETCH_MISSUNIT_UNIQUE                                                    | UPDATE_HAS_SEND                                      | toMSHRArbiter.io.in(PortNumber).fire 为高（请求已发送）。 <br>has_send(PortNumber) 被设置为真，表示该端口已发送请求。                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 9.2.3  | ICACHE_PREFETCH_MISSUNIT_UNIQUE                                                    | UNIQUE_REQ                                           | 同一请求周期内，has_send(PortNumber) 为真，s2_miss(PortNumber) 为真。 <br>toMSHRArbiter.io.in(PortNumber).valid 为假，不会再次发送请求。                                                                                                                                                                                                                                                                                                                                                                                                         |
| 9.2.4  | ICACHE_PREFETCH_MISSUNIT_UNIQUE                                                    | RIGHTLY_SEND                                         | s2_valid 为高，s2_miss(i) 为真，has_send(i) 为假。 <br>toMSHRArbiter.io.in(i).valid 为高，请求被成功发送。                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 9.2.5  | ICACHE_PREFETCH_MISSUNIT_UNIQUE                                                    | ARBITRATE_REQ                                        | 多个端口同时需要发送请求。 <br>仲裁器按照优先级或设计要求选择请求发送到 missUnit,未被选中的请求在下个周期继续尝试发送。                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 10.1   | [ICACHE_PREFETCH_FLUSH](#10-刷新机制)                                              | GLOBAL_FLUSH                                         | io.flush 为高。 <br>s0_flush、s1_flush、s2_flush 分别为高，所有阶段的请求被正确清除。                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 10.2   | ICACHE_PREFETCH_FLUSH                                                              | FLUSH_FROM_BPU                                       | io.flushFromBpu.shouldFlushByStageX 为真（X 为 2 或 3），且请求不是软件预取。 <br>对应阶段的 from_bpu_sX_flush 为高，sX_flush 为高，阶段请求被刷新。                                                                                                                                                                                                                                                                                                                                                                                             |
| 10.3   | ICACHE_PREFETCH_FLUSH                                                              | RESET_FSM                                            | s1_flush 为高。 <br>状态机 state 被重置为 m_idle 状态。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 10.4   | ICACHE_PREFETCH_FLUSH                                                              | ITLB_FLUSH_PIPE                                      | s1_flush 为高。 <br>io.itlbFlushPipe 为高，ITLB 被同步刷新。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 11.1   | [ICACHE_MAINPIPE_DATA_ARRAY](#11-访问-dataarray-的单路)                            | WAY_HIT_AND_ITLB_SUCCESS                             | 当 WayLookup 中的信息表明路命中时，ITLB 查询成功，并且 DataArray 当前没有写时，MainPipe 会向 DataArray 发送读取请求，以获取数据。 <br>s0_hits 为高（一路命中），s0_itlb_exception 信号为零（ITLB 查询成功），toData.last.ready 为高（DataArray 没有正在进行的写操作）。 <br>toData.valid 信号为高，表示 MainPipe 向 DataArray 发出了读取请求。                                                                                                                                                                                                   |
| 11.2   | ICACHE_MAINPIPE_DATA_ARRAY                                                         | WAY_MISS                                             | 当 WayLookup 中的信息表明路未命中时，MainPipe 不会向 DataArray 发送读取请求。 <br>s0_hits 为低表示缓存未命中 <br>toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。                                                                                                                                                                                                                                                                                                                                                              |
| 11.3   | ICACHE_MAINPIPE_DATA_ARRAY                                                         | ITLB_FAIL                                            | 当 ITLB 查询失败时，MainPipe 不会向 DataArray 发送读取请求。 <br>s0_itlb_exception 信号不为零（ITLB 查询失败）。 <br>toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。                                                                                                                                                                                                                                                                                                                                                          |
| 11.4   | ICACHE_MAINPIPE_DATA_ARRAY                                                         | DATA_ARRAY_WRITING                                   | 当 DataArray 正在进行写操作时，MainPipe 不会向 DataArray 发送读取请求。 <br>toData.last.ready 信号为低，表示 DataArray 正在进行写操作。 <br>toData.valid 信号为低，表示 MainPipe 未向 DataArray 发出读取请求。                                                                                                                                                                                                                                                                                                                                   |
| 12.1   | [ICACHE_MAINPIPE_META_ECC](#12-meta-ecc-校验)                                      | NO_ECC_ERROR                                         | 当 waymask 全为 0（没有命中），则 hit_num 为 0 或 waymask 有一位为 1（一路命中），hit_num 为 1 且 ECC 对比通过（encodeMetaECC(meta) == code） <br>s1_meta_corrupt 为假。                                                                                                                                                                                                                                                                                                                                                                         |
| 12.2   | ICACHE_MAINPIPE_META_ECC                                                           | SINGLE_ECC_ERROR                                     | 当 waymask 有一位为 1（一路命中），ECC 对比失败（encodeMetaECC(meta) != code） <br>s1_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。                                                                                                                                                                                                                                                                                                                                           |
| 12.3   | ICACHE_MAINPIPE_META_ECC                                                           | MULTI_WAY_HIT                                        | > hit multi-way, must be an ECC failure <br>当 waymask 有两位及以上为 1（多路命中），视为 ECC 错误。 <br>s1_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。                                                                                                                                                                                                                                                                                                                     |
| 12.4   | ICACHE_MAINPIPE_META_ECC                                                           | ECC_CLOSE                                            | 当奇偶校验关闭时（ecc_enable 为低），强制清除 s1_meta_corrupt 信号置位。 <br>不管是否发生 ECC 错误，s1_meta_corrupt 都为假。                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 13.1   | [ICACHE_MAINPIPE_PMP](#13-pmp-检查)                                                | NONE_EXCEPTION                                       | s1_pmp_exception 为全零，表示没有 PMP 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 13.2   | ICACHE_MAINPIPE_PMP                                                                | CHANNEL_0_EXCEPTION                                  | s1_pmp_exception(0) 为真，表示通道 0 有 PMP 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 13.3   | ICACHE_MAINPIPE_PMP                                                                | CHANNEL_1_EXCEPTION                                  | s1_pmp_exception(1) 为真，表示通道 1 有 PMP 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 13.4   | ICACHE_MAINPIPE_PMP                                                                | CHANNEL_0_AND_1_EXCEPTION                            | s1_pmp_exception(0) 和 s1_pmp_exception(1) 都为真，表示通道 0 和通道 1 都有 PMP 异常。                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 13.5   | ICACHE_MAINPIPE_PMP                                                                | NONE_MMIO                                            | s1_pmp_mmio（0） 和 s1_pmp_mergemmio（1） 都为假，表示没有映射到 MMIO 区域。                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 13.6   | ICACHE_MAINPIPE_PMP                                                                | CHANNEL_0_MMIO                                       | s1_pmp_mmio（0） 为真，表示映射到了 MMIO 区域。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 13.7   | ICACHE_MAINPIPE_PMP                                                                | CHANNEL_1_MMIO                                       | s1_pmp_mmio（1） 为真，表示映射到了 MMIO 区域。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 13.8   | ICACHE_MAINPIPE_PMP                                                                | CHANNEL_0_AND_1_MMIO                                 | s1_pmp_mmio（0） 和 s1_pmp_mmio（1） 都为真，表示通道 0 和通道 1 都映射到了 MMIO 区域。                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 14.1   | [ICACHE_MAINPIPE_EXCEPTION_MERGE](#14-异常合并)                                    | NONE_EXCEPTION                                       | s1_exception_out 为全零，表示没有异常。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 14.2   | ICACHE_MAINPIPE_EXCEPTION_MERGE                                                    | ITLB_EXCEPTION                                       | s1_exception_out 和 s1_itlb_exception 一致                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 14.3   | ICACHE_MAINPIPE_EXCEPTION_MERGE                                                    | PMP_EXCEPTION                                        | s1_exception_out 和 s1_pmp_exception 一致                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 14.4   | ICACHE_MAINPIPE_EXCEPTION_MERGE                                                    | ITLB_AND_PMP_EXCEPTION                               | > itlb has the highest priority, pmp next <br>s1_exception_out 和 s1_itlb_exception 一致                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 15.1   | [ICACHE_MAINPIPE_MSHR_MATCH](#15-mshr-匹配和数据选择)                              | MSHR_HIT                                             | MSHR 中已有正确数据时，S1 阶段能直接拿到 <br>s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 s1_bankMSHRHit(i)，s1_data_is_from_MSHR(i) 为 true                                                                                                                                                                                                                                                                                                                                                                                                       |
| 15.2   | ICACHE_MAINPIPE_MSHR_MATCH                                                         | MSHR_MISS                                            | MSHR 中存放的地址与当前请求不同，那么应该读取 SRAM 的数据 <br>s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false                                                                                                                                                                                                                                                                                                                                                                                     |
| 15.3   | ICACHE_MAINPIPE_MSHR_MATCH                                                         | MSHR_DATA_CORRUPT                                    | fromMSHR.bits.corrupt = true，那么 MSHR 将不匹配，应该读取 SRAM 的数据 <br>s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false                                                                                                                                                                                                                                                                                                                                                                                                    |
| 16.1   | [ICACHE_MAINPIPE_DATA_ECC](#16-data-ecc-校验)                                      | NO_ECC_ERROR                                         | s2_bank 全部没有损坏，bank 也选对了对应的端口和 bank，数据不来自 MSHR <br>s2_data_corrupt(i) 为 false，没有 ECC 错误。                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 16.2   | ICACHE_MAINPIPE_DATA_ECC                                                           | SINGLE_Bank_ECC_ERROR                                | s2_bank_corrupt(bank) 有一个为 true ,即对应的 bank 有损坏；同时 bank 也选对了对应的端口和 bank，数据不来自 MSHR <br>s2_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。                                                                                                                                                                                                                                                                                                          |
| 16.3   | ICACHE_MAINPIPE_DATA_ECC                                                           | MULTIPLE_Bank_ECC_ERROR                              | s2_bank_corrupt(bank) 有两个或以上为 true,即对应的 bank 有损坏；同时 bank 也选对了对应的端口和 bank，数据不来自 MSHR <br>s2_data_corrupt(i)， io.errors(i).valid， io.errors(i).bits.report_to_beu， io.errors(i).bits.source.data 为 true。                                                                                                                                                                                                                                                                                                     |
| 16.4   | ICACHE_MAINPIPE_DATA_ECC                                                           | ECC_CLOSE                                            | 当奇偶校验关闭时（ecc_enable 为低），强制清除 s2_data_corrupt 信号置位。 <br>不管是否发生 ECC 错误，s2_data_corrupt 都为假。                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 17.1   | [ICACHE_MAINPIPE_META_FLUSH](#17-冲刷-metaarray)                                   | FLUSH_META_ARRAY                                     | > if is meta corrupt, clear all way (since waymask may be unreliable) <br>当 s1_meta_corrupt 为真时，MetaArray 的所有路都会被冲刷。 <br>toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的所有路置位。                                                                                                                                                                                                                                                                                                                            |
| 17.2   | ICACHE_MAINPIPE_META_FLUSH                                                         | FLUSH_DATA_ARRAY                                     | > if is data corrupt, only clear the way that has error <br>当 s2_data_corrupt 为真时，只有对应路会被冲刷。 <br>toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的对应路置位。                                                                                                                                                                                                                                                                                                                                                    |
| 17.3   | ICACHE_MAINPIPE_META_FLUSH                                                         | FLUSH_META_ARRAY_AND_DATA_ARRAY                      | 处理 Meta ECC 的优先级更高， 将 MetaArray 的所有路冲刷。 <br>toMetaFlush(i).valid 为真，toMetaFlush(i).bits.waymask 对应端口的所有路置位。                                                                                                                                                                                                                                                                                                                                                                                                       |
| 18.1   | [ICACHE_MAINPIPE_MSHR_MONITER](#18-监控-mshr-匹配与数据更新)                       | MSHR_HIT                                             | MSHR 的 vSetIdx / blkPaddr 与 S2 请求一致， fromMSHR.valid 有效，s2_valid 也有效 <br>s2_MSHR_match，s2_MSHR_hits 为高，s2_bankMSHRHit 对应 bank 为高 <br>s1_fire 无效时，s2_datas 更新为 MSHR 的数据，将 s2_data_is_from_MSHR 对应位置位，s2_hits 置位，清除 s2_data_corrupt，l2 的 corrupt 更新为 fromMSHR.bits.corrupt <br>s1_fire 有效时，s2_datas 为 s1_datas 的数据，将 s2_data_is_from_MSHR 对应位置为 s1 的 s1_data_is_from_MSHR，s2_hits 置为 s1_hits，清除 s2_data_corrupt，l2 的 corrupt 为 false                                      |
| 18.2   | ICACHE_MAINPIPE_MSHR_MONITER                                                       | MSHR_MISS                                            | MSHR 的 vSetIdx / blkPaddr 与 S2 请求一致， fromMSHR.valid 有效，s2_valid 也有效，至少有一个未达成 <br>s2_MSHR_hits(i) = false，S2 不会更新 s2_datas，继续保持原先 SRAM 数据或进入 Miss 流程。                                                                                                                                                                                                                                                                                                                                                   |
| 19.1   | [ICACHE_MAINPIPE_MISS_REQ](#19-miss-请求发送逻辑和合并异常)                        | NONE_MISS                                            | 当 s2_hits(i) 为高（s2 已经命中），s2 的 meta 和 data 都没有错误，s2 异常，处于 mmio 区域 <br>以上条件至少满足一个时，s2_should_fetch(i) 为低，表示不发送 Miss 请求。                                                                                                                                                                                                                                                                                                                                                                            |
| 19.2   | ICACHE_MAINPIPE_MISS_REQ                                                           | SINGLE_MISS                                          | 当出现未命中 (!s2_hits(i)) 或 ECC 错误(s2_meta_corrupt(i)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     | s2_data_corrupt(i))，端口不存在异常且未处于 MMIO 区域时，会向 MSHR 发送 Miss 请求。 <br>toMSHRArbiter.io.in(i).valid = true ，Arbiter 只发送一条 Miss 请求。 |
| 19.3   | ICACHE_MAINPIPE_MISS_REQ                                                           | DOUBLE_MISS                                          | 同上，但是两个端口都满足 s2_should_fetch 为高的条件。 <br>toMSHRArbiter.io.in(0).valid、toMSHRArbiter.io.in(1).valid 均为 true，Arbiter 根据仲裁顺序依次发出请求。                                                                                                                                                                                                                                                                                                                                                                               |
| 19.4   | ICACHE_MAINPIPE_MISS_REQ                                                           | BLOCK_REPETITION                                     | 当 s1_fire 为高，表示可以进入 s2 阶段,那么 s2 还没有发送 s2_has_send(i) := false.B <br>如果已经有请求发送了，那么对应的 toMSHRArbiter.io.in(i).fire 为高，表示对应的请求可以发送，s2_has_send(i) := true。 <br>此时再次发送，toMSHRArbiter.io.in(i).valid 为低，表示发送失败。                                                                                                                                                                                                                                                                   |
| 19.5   | ICACHE_MAINPIPE_MISS_REQ                                                           | ONLY_ITLB_OR_PMP_EXCEPTION                           | S1 阶段已记录了 ITLB 或 PMP 异常，L2 corrupt = false。 <br>2_exception_out 仅保留 ITLB/PMP 异常标记，无新增 AF 异常。                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 19.6   | ICACHE_MAINPIPE_MISS_REQ                                                           | ONLY_L2_EXCEPTION                                    | S2 阶段 s2_l2_corrupt(i) = true，且无 ITLB/PMP 异常。 <br>s2_exception_out(i) 表示 L2 访问错误(AF)。                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 19.7   | ICACHE_MAINPIPE_MISS_REQ                                                           | ITLB_AND_L2_EXCEPTION                                | 同时触发 ITLB 异常和 L2 corrupt。 <br>s2_exception_out 优先保留 ITLB 异常类型，不被 L2 覆盖。                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 19.8   | ICACHE_MAINPIPE_MISS_REQ                                                           | S2_FETCH_FINISH                                      | s2_should_fetch 的所有端口都为低，表示需要取指，那么取指完成 <br>s2_fetch_finish 为高                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 20.1   | [ICACHE_MAINPIPE_IFU](#20-响应-ifu)                                                | HIT_AND_RETURN                                       | 不存在任何异常或 Miss，s2 命中，s2 阶段取指完成，外部的 respStall 停止信号也为低 。 <br>toIFU.valid = true，toIFU.bits.data 为正确的 Cacheline 数据，toIFU.bits.exception、pmp_mmio、itlb_pbmt = none。                                                                                                                                                                                                                                                                                                                                          |
| 20.2   | ICACHE_MAINPIPE_IFU                                                                | ABNORMAL_RETURN                                      | 设置 ITLB、PMP、或 L2 corrupt 异常。 <br>toIFU.bits.exception(i) = 对应异常类型，pmp_mmio、itlb_pbmt 根据是否有对应的异常设置为 true。                                                                                                                                                                                                                                                                                                                                                                                                           |
| 20.3   | ICACHE_MAINPIPE_IFU                                                                | CROSSLINE_FETCH                                      | s2_doubleline = true，同时检查第一路、第二路返回情况。 <br>toIFU.bits.doubleline = true。 <br>若第二路正常，toIFU.bits.exception(1) = none；若第二路异常，则 exception(1) 标记相应类型。 <br>pmp_mmio、itlb_pbmt 类似。                                                                                                                                                                                                                                                                                                                          |
| 20.4   | ICACHE_MAINPIPE_IFU                                                                | RESPSTALL                                            | 外部 io.respStall = true，导致 S2 阶段无法发射到 IFU。 <br>s2_fire = false，toIFU.valid 也不拉高，S2 保持原状态等待下一拍（或直到 respStall 解除）。                                                                                                                                                                                                                                                                                                                                                                                             |
| 21.1   | [ICACHE_MAINPIPE_L2_CORRUPT](#21-l2-corrupt-报告)                                  | SINGLE_L2_CORRUPT                                    | s2 阶段准备完成可以发射（s2_fire 为高），s2_MSHR_hits(0)和 fromMSHR.bits.corrupt 为高 <br>s2_l2_corrupt(0) = true，io.errors(0).valid = true，io.errors(0).bits.source.l2 = true。                                                                                                                                                                                                                                                                                                                                                               |
| 21.2   | ICACHE_MAINPIPE_L2_CORRUPT                                                         | DOUBLE_L2_CORRUPT                                    | 端口 0 和端口 1 都从 L2 corrupt 数据中获取。 <br>s2_l2_corrupt 均为 true，发射后分别报告到 io.errors(0) 和 io.errors(1)。                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 22.1   | [ICACHE_MAINPIPE_FLUSH](#22-刷新机制)                                              | GLOBAL_FLUSH                                         | io.flush 被激活时，流水线的各个阶段（S0, S1 和 S2）都能正确响应并执行刷新操作。 <br>io.flush = true。 <br>s0_flush, s1_flush, s2_flush = true。                                                                                                                                                                                                                                                                                                                                                                                                  |
| 22.2   | ICACHE_MAINPIPE_FLUSH                                                              | S0_FLUSH                                             | s0_flush = true。 <br>s0_fire = false。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 22.3   | ICACHE_MAINPIPE_FLUSH                                                              | S1_FLUSH                                             | s1_flush = true。 <br>s1_valid， s1_fire = false。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 22.4   | ICACHE_MAINPIPE_FLUSH                                                              | S2_FLUSH                                             | s2_flush = true。 <br>s2_valid， toMSHRArbiter.io.in(i).valid ， s2_fire = false                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 23.1   | [ICACHE_WAYLOOKUP_FLUSH](#22-刷新机制)                                             | READ_POINTER                                         | io.flush 为高时，重置读指针。 <br>readPtr.value 为 0， readPtr.flag 为 false。                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 23.2   | ICACHE_WAYLOOKUP_FLUSH                                                             | WRITE_POINTER                                        | io.flush 为高时，重置写指针。 <br>writePtr.value 为 0， writePtr.flag 为 false。                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 23.3   | ICACHE_WAYLOOKUP_FLUSH                                                             | GPF                                                  | io.flush 为高时，重置 GPF 信息。 <br>gpf_entry.valid 为 0， gpf_entry.bits 为 0。                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 24.1   | [ICACHE_WAYLOOKUP_UPDATE_POINTER](#24-读写指针更新)                                | READ_POINTER                                         | 当 io.read.fire 为高时，读指针加一。 <br>readPtr.value 加一。 <br>如果 readPtr.value 超过环形队列的大小，readPtr.flag 会翻转。                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 24.2   | ICACHE_WAYLOOKUP_UPDATE_POINTER                                                    | WRITE_POINTER                                        | 当 io.write.fire 为高时，写指针加一。 <br>writePtr.value 加一。 <br>如果 writePtr.value 超过环形队列的大小，writePtr.flag 会翻转。                                                                                                                                                                                                                                                                                                                                                                                                               |
| 25.1   | [ICACHE_WAYLOOKUP_UPDATE](#25-更新操作)                                            | HIT                                                  | MissUnit 返回的更新信息和 WayLookup 的信息相同时，更新 waymask 和 meta_codes。 <br>vset_same 和 ptag_same 为真。 <br>waymask 和 meta_codes 更新。 <br>hits 对应位为高。                                                                                                                                                                                                                                                                                                                                                                          |
| 25.2   | ICACHE_WAYLOOKUP_UPDATE                                                            | MISS                                                 | vset_same 和 way_same 为真。 <br>waymask 清零。 <br>hit 对应位为高。                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 25.3   | ICACHE_WAYLOOKUP_UPDATE                                                            | NONE_UPDATE                                          | 其他情况下不更新。 <br>vset_same 为假或者 ptag_same 和 way_same 都为假。 <br>hits 对应位为低。                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 26.1   | [ICACHE_WAYLOOKUP_READ](#26-读操作)                                                | BYPASS_READ                                          | 队列为空，并且 io.write.valid 写有效时，可以直接读取，而不经过队列。 <br>empty 和 io.write.valid 都为真。 <br>io.read.bits = io.write.bits                                                                                                                                                                                                                                                                                                                                                                                                       |
| 26.2   | ICACHE_WAYLOOKUP_READ                                                              | READ_INVALID                                         | 队列为空（readPtr === writePtr）且写信号 io.write.valid 为低。 <br>io.read.valid 为低，读信号无效。                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 26.3   | ICACHE_WAYLOOKUP_READ                                                              | NORMAL_READ                                          | 未达成绕过条件（empty 和 io.write.valid 至少有一个为假）且 io.read.valid 为高。 <br>从环形队列中读取信息。 <br>io.read.bits.entry = entries(readPtr.value)                                                                                                                                                                                                                                                                                                                                                                                       |
| 26.4   | ICACHE_WAYLOOKUP_READ                                                              | GPF_HIT                                              | io.read.valid 为高，可以读。 <br>当 gpf_hits 为高时，从 GPF 队列中读取信息。 <br>io.read.bits.gpf = gpf_entry.bits                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 26.5   | ICACHE_WAYLOOKUP_READ                                                              | GPF_HIT_AND_READ                                     | io.read.valid 为高，可以读。 <br>> also clear gpf_entry.valid when it's read <br>当 gpf 命中且被读取其时（io.read.fire 为高），gpf_entry.valid 会被置为 0。                                                                                                                                                                                                                                                                                                                                                                                      |
| 26.6   | ICACHE_WAYLOOKUP_READ                                                              | GPF_MISS                                             | io.read.valid 为高，可以读。 <br>io.read.bits.gpf 清零。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 27.1   | [ICACHE_WAYLOOKUP_WRITE](#27-写操作)                                               | GPF_STOP                                             | > if there is a valid gpf to be read, we should stall write <br>gpf 队列数据有效，并且没有被读取或者没有命中，就会产生 gpf 停止，此时写操作会被停止。 <br>gpf_entry.valid && !(io.read.fire && gpf_hit) 为高时，写操作会被停止（io.write.ready 为低）。                                                                                                                                                                                                                                                                                          |
| 27.2   | ICACHE_WAYLOOKUP_WRITE                                                             | WRITE_READY_INVALID                                  | 当队列为满（(readPtr.value === writePtr.value) && (readPtr.flag ^ writePtr.flag)）或者 gpf 停止时，写操作会被停止。 <br>（io.write.ready 为低）                                                                                                                                                                                                                                                                                                                                                                                                  |
| 27.3   | ICACHE_WAYLOOKUP_WRITE                                                             | NORMAL_WRITE                                         | 当 io.write.valid 为高时（没满且没有 gpf 停止），写操作会被执行。 <br>正常握手完毕 io.write.fire 为高。 <br>写信息会被写入环形队列。 <br>entries(writePtr.value) = io.write.bits.entry。                                                                                                                                                                                                                                                                                                                                                         |
| 27.4.1 | [ICACHE_WAYLOOKUP_WRITE_WITH_ITLB_EXCEPTION](#274-有-itlb-异常的写)                | BYPASS                                               | can_bypass 和 io.read.fire 都为高。 <br>gpf_entry.valid 为 false。 <br>gpf_entry.bits = io.write.bits.gpf <br>gpfPtr = writePtr <br>                                                                                                                                                                                                                                                                                                                                                                                                             |
| 27.4.2 | ICACHE_WAYLOOKUP_WRITE_WITH_ITLB_EXCEPTION                                         | NO_BYPASS                                            | can_bypass 为低。 <br>gpf_entry.valid 为 true。 <br>gpf_entry.bits = io.write.bits.gpf <br>gpfPtr = writePtr                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 28.1   | [ICACHE_WAYLOOKUP_ENQ](#28-入队操作)                                               | NORMAL_ENQ                                           | 当队列未满，且空位不小于一时，可以正常入队，如果从零号位开始入队到最大容量，入队指针的 flag 不会翻转。 <br>io.enq.fire 为高有效，regFiles(enq_ptr.value) = io.enq.bits，enq_ptr.value+1 入队指针移动，入队指针标记位不翻转。 <br>重复以上操作至队满。                                                                                                                                                                                                                                                                                            |
| 28.2   | ICACHE_WAYLOOKUP_ENQ                                                               | REVERSE_FLAG                                         | 当队未满，但是空位却是靠近队尾时，入队一位后就到达了队头，入队指针的 flag 会翻转。 <br>队列的容量为 10，入队指针指向 9，队未满。此时如果 io.enq.fire 为高，则 regFiles(9) = io.enq.bits，enq_ptr.value+1（循环队列，加完后 enq_ptr.value=0）入队指针移动，入队指针标记位翻转。                                                                                                                                                                                                                                                                   |
| 28.3   | ICACHE_WAYLOOKUP_ENQ                                                               | FULL                                                 | 当队满时，(enq_ptr.value === deq_ptr.value) && (enq_ptr.flag ^ deq_ptr.flag) 为高，io.enq.ready 为低，io.enq.fire 为低无效。 <br>此时入队，入队指针的 value 和 flag 不变。                                                                                                                                                                                                                                                                                                                                                                       |
| 29.1   | [ICACHE_WAYLOOKUP_DEQ](#29-出队操作)                                               | NORMAL_DEQ                                           | 当队列非空时，可以正常出队，如果出队指针不经过最大容量位置，出队指针的 flag 不会翻转。 <br>io.deq.fire 为高有效，io.deq.bits = regFiles(deq_ptr.value)，deq_ptr.value+1 出队指针移动，出队指针标记位不翻转。                                                                                                                                                                                                                                                                                                                                     |
| 29.2   | ICACHE_WAYLOOKUP_DEQ                                                               | REVERSE_FLAG                                         | 当队非空，但是出队指针是靠近队尾时，出队一位后就到达了队头，出队指针的 flag 会翻转。 <br>队列的容量为 10，出队指针指向 9，队非空。此时如果 io.deq.fire 为高，则 io.deq.bits = regFiles(9)，deq_ptr.value+1（循环队列，加完后 deq_ptr.value=0）出队指针移动，出队指针标记位翻转。                                                                                                                                                                                                                                                                 |
| 29.3   | ICACHE_WAYLOOKUP_DEQ                                                               | EMPTY                                                | 当队空时，enq_ptr === deq_ptr 为高，io.deq.valid 为低，io.deq.fire 为低无效。 <br>此时出队，出队指针的 value 和 flag 不变。                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 30.1   | [ICACHE_WAYLOOKUP_FLUSH](#30-刷新清空操作)                                         | FLUSH                                                | 当刷新信号有效时，重置出队和入队的指针和标记位，清空队列。 <br>当 flush 为高时，deq_ptr.value=0，enq_ptr.value=0，deq_ptr.flag=false，enq_ptr.flag=false，empty=true,full=false。                                                                                                                                                                                                                                                                                                                                                                |
| 31.1   | [ICACHE_MISSUNIT_HANDLE_FETCH](#31-处理取指缺失请求)                               | RECEIVE_NEW_REQ                                      | 当新的 fetch miss 与 MSHR 中的已有请求不重复时（通过 io.fetch_req.bits.blkPaddr / vSetIdx 给出具体地址），MissUnit 会将请求分配到一个空闲的 Fetch MSHR 中。 <br>当有新的取指缺失请求到达时（io.fetch_req.valid 为高），且没有命中已有的 MSHR（fetchHit 为低），io.fetch_req.ready 应为高，表示可以接受请求。 <br>io.fetch_req.fire 成功握手后，该 MSHR 处于 valid = true 状态，并记录地址。                                                                                                                                                      |
| 31.2   | ICACHE_MISSUNIT_HANDLE_FETCH                                                       | ALREADY_REQ                                          | 当已有取指缺失请求到达时（io.fetch_req.valid 为高），且命中已有的 MSHR（fetchHit 为高），io.fetch_req.ready 应为高，虽然不接受请求，但是表现出来为已经接收请求。 <br>fetchDemux.io.in.valid 应为低，fetchDemux.io.in.fire 为低，表示没有新的请求被分发到 MSHR。                                                                                                                                                                                                                                                                                  |
| 31.3   | ICACHE_MISSUNIT_HANDLE_FETCH                                                       | MSHR_PRIORITY                                        | Fetch 的请求会通过 fetchDemux 分配到多个 Fetch MSHR，fetchDemux 的实现中，低索引的 MSHR 会优先被分配请求。 <br>当取指请求有多个 io.out(i).read 时，选择其中的第一个，也就是低索引的写入 MSHR，io.chose 为对应的索引。                                                                                                                                                                                                                                                                                                                            |
| 32.1   | [ICACHE_MISSUNIT_HANDLE_PREFETCH](#32-处理预取缺失请求)                            | RECEIVE_NEW_REQ                                      | 当新的 prefetch miss 与 MSHR 中的已有请求不重复时（通过 io.prefetch_req.bits.blkPaddr / vSetIdx 给出具体地址），MissUnit 会将请求分配到一个空闲的 Prefetch MSHR 中。 <br>当有新的预取缺失请求到达时（io.prefetch_req.valid 为高），且没有命中已有的 MSHR（prefetchHit 为低），io.prefetch_req.ready 应为高，表示可以接受请求。 <br>io.prefetch_req.fire 成功握手后，该 MSHR 处于 valid = true 状态，并记录地址。                                                                                                                                 |
| 32.2   | ICACHE_MISSUNIT_HANDLE_PREFETCH                                                    | ALREADY_REQ                                          | 当已有预取缺失请求到达时（io.prefetch_req.valid 为高），且命中已有的 MSHR（prefetchHit 为高），io.prefetch_req.ready 应为高，虽然不接受请求，但是表现出来为已经接收请求。 <br>prefetchDemux.io.in.valid 应为低，prefetchDemux.io.in.fire 为低，表示请求被接受但未分发到新的 MSHR。                                                                                                                                                                                                                                                               |
| 32.3   | ICACHE_MISSUNIT_HANDLE_PREFETCH                                                    | MSHR_PRIORITY                                        | Prefetch 的请求会通过 prefetchDemux 分配到多个 Prefetch MSHR，prefetchDemux 的实现中，低索引的 MSHR 会优先被分配请求。 <br>当取指请求有多个 io.out(i).read 时，选择其中的第一个，也就是低索引的写入 MSHR，io.chose 为对应的索引。                                                                                                                                                                                                                                                                                                                |
| 32.4   | ICACHE_MISSUNIT_HANDLE_PREFETCH                                                    | FIFO_PRIORITY                                        | 从 prefetchDemux 离开后，请求的编号会进入 priorityFIFO，priorityFIFO 会根据进入队列的顺序排序，先进入队列的请求会先进入 prefetchArb。 <br>prefetchDemux.io.in.fire 为高，并且 prefetchDemux.io.chosen 有数据时，将其编号写入 priorityFIFO。 <br>在 priorityFIFO 中有多个编号时，出队的顺序和入队顺序一致。 <br>检查 priorityFIFO.io.deq.bit 中的数据即可。                                                                                                                                                                                       |
| 33.1   | [ICACHE_MISSUNIT_MSHR](#33-mshr-管理与查找)                                        | HIT                                                  | 当新的请求到来时，能够正确查找所有 MSHR，判断请求是否命中已有 MSHR。 <br>当新的请求（取指或预取）到来时，系统遍历所有 MSHR，根据所有 MSHR 的查找信号 allMSHRs(i).io.lookUps(j).hit，检查请求是否已经存在于某个 MSHR 中。 <br>如果命中，则对应的 fetchHit 或 prefetchHit 为高。 <br>对于 prefetchHit 为高，还有一种情况：预取的物理块地址和组索引与取指的相等（(io.prefetch_req.bits.blkPaddr === io.fetch_req.bits.blkPaddr) && (io.prefetch_req.bits.vSetIdx === io.fetch_req.bits.vSetIdx)）并且有取指请求 io.fetch_req.valid 有效时，也算命中 |
| 33.2   | ICACHE_MISSUNIT_MSHR                                                               | UPDATE_AND RELEASE                                   | 当请求完成后，也就是来自内存总线的响应完成（D 通道接收完所有节拍），MSHR 能够正确地释放（清除其有效位），以便接收新的请求。 <br>TileLink D 通道返回的 source ID ，即 io.mem_grant.bits.source。 <br>无效化信号 allMSHRs(i).io.invalid 为高，对应的 MSHR 的有效位 allMSHRs(i).valid 变为低                                                                                                                                                                                                                                                        |
| 34.1   | [ICACHE_MISSUNIT_ACQUIREARB](#34-acquirearb-仲裁)                                  | ARBITRATE                                            | acquireArb 会选择一个 acquire 发送给 mem_acquire。 <br>当有多个 MSHR 同时发出请求时，acquireArb 会根据优先级进行仲裁，选择优先级最高的 MSHR 发送请求。 <br>取指请求总是在 0-3 号，预取请求直接在最后一号，所以取指请求优先级高于预取请求。 <br>当取指 acquire 和预取 acquire 同时发出时，fetchMSHRs(i).io.acquire 和 prefetchMSHRs(i).io.acquire 都有效，仲裁结果 acquireArb.io.out 应该和 fetchMSHRs(i).io.acquire 一致。                                                                                                                       |
| 35.1   | [ICACHE_MISSUNIT_GRANT](#35-grant-数据接收与-refill)                               | READBEATCNT_EQUAL_0                                  | readBeatCnt 初始为 0，refillCycles - 1 也为 0。 <br>io.mem_grant.valid 为高（因为 io.mem_grant.ready 默认为高，所以 io.mem_grant.fire 为高只需要 io.mem_grant.valid 为高）且 io.mem_grant.bits.opcpde(0)为高。 <br>此时 respDataReg(0)= io.mem_grant.bits.data <br>readBeatCnt 加一为 1。                                                                                                                                                                                                                                                        |
| 35.2   | ICACHE_MISSUNIT_GRANT                                                              | READBEATCNT_EQUAL_1                                  | io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高。 <br>此时 respDataReg(1)= io.mem_grant.bits.data <br>readBeatCnt 重置回 0。 <br>last_fire 为高。 <br>下一拍 last_fire_r 为高，id_r=io.mem_grant.bits.source。                                                                                                                                                                                                                                                                                                                         |
| 35.3   | ICACHE_MISSUNIT_GRANT                                                              | LAST_FIRE_R_EQUAL_HIGH                               | last_fire_r 为高，并且 id_r 为 0-13 中的一个。 <br>对应的 fetchMSHRs 或者 prefetchMSHRs 会被无效，也就是 fetchMSHRs_i 或 prefetchMSHRs_i-4 的 io_invalid 会被置高。                                                                                                                                                                                                                                                                                                                                                                              |
| 35.4   | ICACHE_MISSUNIT_GRANT                                                              | GRANT_WITH_CORRUPT                                   | io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高，io.mem_grant.bits.corrupt 为高，则 corrupt_r 应为高。 <br>如果 io.mem_grant.valid 为高且 io.mem_grant.bits.opcpde(0)为高，io.mem_grant.bits.corrupt 为高中有一个不满足，且此时 last_fire_r 为高，则 corrupt_r 重置为低。                                                                                                                                                                                                                                                              |
| 36.1   | [ICACHE_MISSUNIT_REPLACER](#36-替换策略更新-replacer)                              | UPDATE                                               | 当 io.mem.acquire.ready & acquireArb.io.out.valid 同时为高，也就是 acquireArb.io.out.fir 为高时，io.victim.vSetIdx.valid 也为高。 <br>io.victim.vSetIdx.bits = 当前 MSHR 请求的 acquireArb.io.out.bits.vSetIdx。                                                                                                                                                                                                                                                                                                                                 |
| 36.2   | ICACHE_MISSUNIT_REPLACER                                                           | GENERATE_WAYMASK                                     | 根据从 L2 返回的 mshr_resp 中 mshr_resp.bits.way 生成 waymask 信息。 <br>返回的 mshr_resp.bits.way 有 16 位，通过独热码生成一位掩码信息，waymask 表示其中哪一路被替换。 <br>生成的 waymask 应该和 mshr_resp.bits.way 一致。                                                                                                                                                                                                                                                                                                                      |
| 37.1   | [ICACHE_MISSUNIT_WRITE_SRAM](#37-写回-sram-meta--data)                             | GENERATE_META_AND_DATA_WRITE_VALID                   | 当 grant 传输完成后，经过一拍后，即 last_fire_r 为高，且从 TileLink 返回的 mshr_resp 中的 mshr_resp.valid 为高。 <br>并且此时没有硬件刷新信号和软件刷新信号，也就是 io.flush 和 io.fencei 为低。 在等待 l2 响应的过程中，没有刷新信号 <br>也没有数据 corrupt，即 corrupt_r 为低。 <br>那么 io.meta_write.valid 和 io.data_write.valid 均为高。                                                                                                                                                                                                   |
| 37.2   | ICACHE_MISSUNIT_WRITE_SRAM                                                         | WRITE_SRAM                                           | io.meta_write.bits 的 virIdx、phyTag、waymask、bankIdx、poison 应该正常更新 <br>io.data_write.bits 的 virIdx、data、waymask、bankIdx、poison 应该正常更新                                                                                                                                                                                                                                                                                                                                                                                        |
| 38.1   | [ICACHE_MISSUNIT_FINISH](#38-向-mainpipeprefetchpipe-发出-miss-完成响应fetch_resp) | MISS_REQ_FINISH                                      | 当 grant 传输完成后，经过一拍后，即 last_fire_r 为高，且从 TileLink 返回的 mshr_resp 中的 mshr_resp.valid 为高。 <br>无论此时是否有硬件刷新信号和软件刷新信号， io.fetch_resp.valid 都为高，说明可向取指端发送响应。 <br>io.fetch_resp.bits 中的数据更新： <br>io.fetch_resp.bits.blkPaddr = mshr_resp.bits.blkPaddr <br>io.fetch_resp.bits.vSetIdx = mshr_resp.bits.vSetIdx <br>io.fetch_resp.bits.waymask = waymask <br>io.fetch_resp.bits.data = respDataReg.asUInt <br>io.fetch_resp.bits.corrupt = corrupt_r                                |
| 39.1   | [ICACHE_MISSUNIT_FLUSH_OR_FENCEI](#39-处理-flush--fencei)                          | FENCEI_BEFORE_MSHR_ISSUE                             | 如果 MSHR 还没有通过 io.acquire.fire 发出请求，就应立即取消该 MSHR（mshr_resp.valid= false），既不发出请求，也不要写 SRAM。 <br>当 io.fencei 为高时，fetchMSHRs 和 prefetchMSHRs 的 io.req.ready 和 io.acquire.valid 均为低，表示请求不发射。                                                                                                                                                                                                                                                                                                    |
| 39.2   | ICACHE_MISSUNIT_FLUSH_OR_FENCEI                                                    | FLUSH_BEFORE_MSHR_ISSUE                              | 由于 fetchMSHRs 的 io.flush 被直接设置为 false，所以 io.flush 对 fetchMSHRs 无效，但是对 prefetchMSHRs 有效。 <br>当 io.flush 为高时，只能发射 fetchMSHRs 的请求。                                                                                                                                                                                                                                                                                                                                                                               |
| 39.3   | ICACHE_MISSUNIT_FLUSH_OR_FENCEI                                                    | FLUSH_OR_FENCEI_AFTER_MSHR_ISSUE                     | 已经发射了请求，之后再有刷新信号，那么等数据回来了但不写 SRAM。 <br>在发射后，io.flush/io.fencei 为高时，等待数据回来，但是写 SRAM 的信号，write_sram_valid、io.meta_write.valid 和 io.data_write.valid 均为低，表示不写 SRAM。 <br>对于 response fetch 无影响。                                                                                                                                                                                                                                                                                 |
| 40.1   | [ICACHE_CTRLUNIT_ECCCTRL](#40-ecc-启用禁用)                                        | ENABLE_ECC                                           | 向 eccctrl.enable 寄存器写入 true，验证模块内部 eccctrl.enable 设置为 true，并确保后续的错误注入操作能够成功进行。此测试确保 eccctrl.enable 写操作被执行。 <br>确保 eccctrl.enable 被正确设置为 true，并触发 eccctrlRegWriteFn 中的写操作逻辑。                                                                                                                                                                                                                                                                                                  |
| 40.2   | ICACHE_CTRLUNIT_ECCCTRL                                                            | DISANLE_ECC                                          | 向 eccctrl.enable 寄存器写入 false，验证模块内部 eccctrl.enable 设置为 false，并确保在后续的错误注入过程中，ECC 功能被禁用，不允许进行错误注入。此测试确保 eccctrl.enable 写操作被正确设置为 false。 <br>验证禁用 ECC 时 eccctrl.enable 为 false，并触发 eccctrlRegWriteFn 中的错误处理分支。x.istatus = eccctrlInjStatus.error 和 x.ierror = eccctrlInjError.notEnabled                                                                                                                                                                         |
| 41.1   | [ICACHE_CTRLUNIT_FSM](#41-状态机转换)                                              | IDLE                                                 | 初始为 is_idle 状态。 <br>当 eccctrl.istatus 为 working 时，验证此时的状态为 is_readMetaReq。                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 41.2   | ICACHE_CTRLUNIT_FSM                                                                | READMETAREQ                                          | 当握手成功后（io.metaRead.ready 和 io.metaRead.valid 都为高），验证此时的状态为 is_readMetaResp。                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 41.3.1 | [ICACHE_CTRLUNIT_FSM_READMETARESP](#413-is_readmetaresp-状态)                      | MISS                                                 | 当 waymask 全零的时候，表示没有命中，会进入 is_idle 状态，并且设置错误错误注入状态和错误原因。 <br>验证此时的状态为 is_idle， eccctrl.istatus = error 和 eccctrl.ierror = notFound。                                                                                                                                                                                                                                                                                                                                                             |
| 41.3.2 | ICACHE_CTRLUNIT_FSM_READMETARESP                                                   | HIT                                                  | 当 waymask 不全零的时候，表示命中，会根据错误注入目标来判断是向元数据还是数据阵列写入错误。 <br>当 eccctrl.itarget=metaArray 时，验证此时的状态为 is_writeMeta ；当 eccctrl.itarget！=metaArray 时，验证此时的状态为 is_writeData。                                                                                                                                                                                                                                                                                                              |
| 41.4.1 | [ICACHE_CTRLUNIT_FSM_WRITEMETA](#414-is_writemeta-状态)                            | REGWRITEFN                                           | 此状态进入后，io.dataWrite.valid 会为高 <br>x.itarget = req.itarget <br>当 req.inject 为高并且 x.istatus = idle 时： <br>1. 如果 ecc 的 req.enable = false，则验证 x.istatus = error 且 x.ierror = notEnabled <br>2. 否则，如果 req.itarget ！= metaArray 和 dataArray，则验证 x.istatus = error 且 x.ierror = targetInvalid <br>3. 如果都不满足，则验证 x.istatus = working                                                                                                                                                                     |
| 41.4.2 | ICACHE_CTRLUNIT_FSM_WRITEMETA                                                      | STATE_TRANSFER                                       | 当 io.metaWrite.fire 为高， 验证下一个状态为 is_idle，并且 eccctrl.istatus = injected。                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 41.5.1 | [ICACHE_CTRLUNIT_FSM_WRITEDATA](#415-is_writedata-状态)                            | REGWRITEFN                                           | 此状态进入后，io.dataWrite.valid 会为高 <br>res.inject = false <br>当 ready 为高，且 x.istatus = injected 或 x.istatus = error 时，验证 x.istatus = idle 和 x.ierror = notEnabled                                                                                                                                                                                                                                                                                                                                                                |
| 41.5.2 | ICACHE_CTRLUNIT_FSM_WRITEDATA                                                      | STATE_TRANSFER                                       | 当 io.dataWrite.fire 为高， 验证下一个状态为 is_idle，并且 eccctrl.istatus = injected。                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 42.1   | [ICACHE_CTRLUNIT_EXTERNAL](#42-寄存器映射和外部访问)                               | READ_OR_WRITE_ECC_REGISTER                           | 验证外部模块可以通过 TileLink 协议正确读取和写入 eccctrl 和 ecciaddr 寄存器，并对模块内部的状态产生影响，确保读写操作完全覆盖。                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 42.2   | ICACHE_CTRLUNIT_EXTERNAL                                                           | EXTERNAL_MODULE_TRIGGER_ERROR_INJECT                 | 通过外部模块经 TileLink 总线向 eccctrl.inject 寄存器写入 true，触发错误注入，验证内部状态是否按 RegWriteFn 内部过程执行。                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 43.1   | [ICACHE_ICACHE_PREFETCH](#43-ftq-预取请求处理)                                     | PREFETCH_HIT_WITHOUT_EXCEPTION                       | io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 匹配，pmp 检查通过。 <br>如果没有监听到 MSHR 同样的位置发生了其它 cacheline 的写入，那么验证 wayLookup.io.write 的内容应该命中的取指数据。 <br>如果监听到 MSHR 同样的位置发生了其它 cacheline 的写入，那么验证 wayLookup.io.write 的内容应该是未命中的取指数据。                                                                                                                                                   |
| 43.2   | ICACHE_ICACHE_PREFETCH                                                             | PREFETCH_MISS_WITHOUT_EXCEPTION                      | io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 不匹配，pmp 检查通过。 <br>如果监听到 MSHR 将该请求对应的 cacheline 写入了 SRAM，那么验证 wayLookup.io.write 的内容应该命中的取指数据。 <br>如果监听到 MSHR 没有将该请求对应的 cacheline 写入了 SRAM，那么验证 wayLookup.io.write 的内容应该未命中的取指数据。                                                                                                                                                     |
| 43.3   | ICACHE_ICACHE_PREFETCH                                                             | ONLY_TLB_EXCEPTION                                   | io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 异常。 <br>验证 wayLookup.io.write 的 itlb_exception 内容中，其有对应的异常类型编号（pf:01;gpf:10;af:11）。                                                                                                                                                                                                                                                                                                                                                         |
| 43.4   | ICACHE_ICACHE_PREFETCH                                                             | ONLY_TPMP_EXCEPTION                                  | io.ftqPrefetch.req.bits 的 startAddr 和 nextlineStart 在正常地址范围内，itlb 命中无异常，itlb 查询到的地址与 MetaArry 的 ptag 匹配，pmp 检查未通过。 <br>验证 wayLookup.io.write 的 tlb_pbmt 内容中，其有对应的异常类型编号（nc:01;io:10）。                                                                                                                                                                                                                                                                                                     |
| 44.1   | [ICACHE_ICACHE_FETCH](#44-ftq-取指请求处理)                                        | FETCH_HIT_WITHOUT_EXCEPTION                          | io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查正常，DataArray 和 MetaArray 的 ECC 校验正常。 <br>验证 replacer.io.touch 的 vSetIdx 和 way 和 ftq 的 fetch 一致，missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。 <br>验证 io.fetch.resp 的数据应该是取指的数据。                                                                                                                                                                                          |
| 44.2   | ICACHE_ICACHE_FETCH                                                                | FETCH_MISS_MSHR_HIT_WITHOUT_EXCEPTION                | io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，未命中，pmp 检查正常，DataArray 和 MetaArray 的 ECC 校验正常。 <br>请求在 MSHR 返回的响应命中。 <br>验证 missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。 <br>验证 io.fetch.resp 的数据应该是取指的数据。                                                                                                                                                                                                                 |
| 44.3   | ICACHE_ICACHE_FETCH                                                                | FETCH_MISS_AND_ECC_ERROR_WITHOUT_ELSE_EXCEPTION      | io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查正常，DataArray 或 MetaArray 的 ECC 校验错误。 <br>验证 io.error.valid 为高，且 io.error.bits 内容为对应的错误源和错误类型。 <br>先刷 MetaArray 的 ValidArray,给 MissUnit 发请求，由其在 L2 重填，阻塞至数据返回。 <br>验证 replacer.io.touch 的 vSetIdx 和 way 和 ftq 的 fetch 一致，missUnit.io.victim 的 vSetIdx 和 way 是按照制定的算法生成的。 <br>验证 io.fetch.resp 的数据应该是取指的数据。                      |
| 44.4   | ICACHE_ICACHE_FETCH                                                                | FETCH_MISS_AND_SOME_EXCEPTION_WITHOUT_ELSE_EXCEPTION | io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查未通过，DataArray 和 MetaArray 的 ECC 校验正常。 <br>验证 io.fetch.resp 为对应的错误源和错误类型。 <br>验证 io.fetch.resp 的数据无效，里面有异常类型。                                                                                                                                                                                                                                                                   |
| 44.5   | ICACHE_ICACHE_FETCH                                                                | FETCH_MISS_AND_ITLB_PBMT                             | 有 itlb_pbmt 和 pmp_mmio 时，他们合成 s1_mmio，传递到 s2_mmio,生成 s2_miss,有特殊情况就不会取指。 <br>io.fetch.req.bits.pcMemRead 的 0-4 的 startAddr 和 nextlineStart 在正常地址范围内，从 WayLookup 获取信息，命中，pmp 检查通过，DataArray 和 MetaArray 的 ECC 校验正常。 <br>验证 io.fetch.resp 为对应的错误源和错误类型。 <br>验证 io.fetch.resp 的数据无效，里面有特殊情况类型类型。                                                                                                                                                       |
| 44.6   | ICACHE_ICACHE_FETCH                                                                | FETCH_MISS_AND_PMP_MMIO                              | 处理同 5。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 45.1   | [ICACHE_ICACHE_METAARRAY](#45-metaarray-功能)                                      | WRITE_META                                           | 从 MissUnit 返回的请求都是未命中的请求（已命中不会向 MissUnit 请求，那么 MissUnit 自然也不会向 MetaArray 写入）。 <br>发送一个写请求 write 到 ICacheMetaArray，ICacheReplacer 根据 PLRU 替换策略指定 way，替换路被写入 waymask，最后指定 virIdx、phyTag、waymask、bankIdx、poison。 <br>写入操作后，发起一个对相同虚拟索引的读请求。验证 readResp 的 metas 和 codes 分别包含写入的 ptag 和 ecc code，并且对于写入的路，readResp.entryValid 信号被置为有效。                                                                                      |
| 45.2   | ICACHE_ICACHE_METAARRAY                                                            | READ_META_HIT                                        | 首先，向特定的虚拟索引（组和路）写入元数据（参照上面的写入操作）。然后，向相同的虚拟索引发送一个读请求。 <br>验证 readResp.metas 包含之前写入的物理标签，并且对于相应的路，readResp.entryValid 信号被置为有效。                                                                                                                                                                                                                                                                                                                                  |
| 45.3   | ICACHE_ICACHE_METAARRAY                                                            | READ_META_MISS                                       | 向 ICacheMetaArray 发送一个读请求，请求的虚拟索引在复位后从未被写入过。 <br>验证对于任何路，readResp.entryValid 信号都没有被置为有效。 对应的 readResp.metas 和 codes 的内容是 DontCare 也就是 0。                                                                                                                                                                                                                                                                                                                                               |
| 45.4   | ICACHE_ICACHE_METAARRAY                                                            | SINGLE_CACHELINE_FLUSH                               | 先向 ICacheMetaArray 写入指定一个或多个端口的元数据，然后再给对应的端口的路发送刷新请求 io.flush，其包含虚拟索引 virIdx 和路掩码 waymask。 <br>验证 valid_array 对应的路中的 virIdx 被置为无效，io.readResp.entryValid 对应路的对应端口为无效。                                                                                                                                                                                                                                                                                                  |
| 45.5   | ICACHE_ICACHE_METAARRAY                                                            | FLUSH_ALL                                            | 先向多个不同的虚拟索引写入元数据。然后置位 io.flushAll 信号。 <br>验证步骤: 在 io.flushAll 信号置位后，发起对所有之前写入过的虚拟索引的读请求。验证在所有的读取响应中，对于任何路，readResp.entryValid 信号都没有被置为有效。                                                                                                                                                                                                                                                                                                                    |
| 46.1   | [ICACHE_ICACHE_DATAARRAY](#46-dataarray-功能)                                      | WRITE_DATA                                           | 发送一个写请求 write 到 ICacheDataArray，ICacheReplacer 根据 PLRU 替换策略指定 way，替换路被写入 waymask，最终指定虚拟索引、数据、路掩码、存储体索引 bankIdx 和毒化位。写入的数据模式应跨越多个数据存储体。 <br>写入操作后，发起一个对相同虚拟索引和块偏移量的读请求。验证 readResp.datas 与写入的数据相匹配。                                                                                                                                                                                                                                   |
| 46.2   | ICACHE_ICACHE_DATAARRAY                                                            | READ_DATA_HIT                                        | 首先，向特定的虚拟索引和块偏移量写入数据。然后，向相同的虚拟索引和块偏移量发送一个读请求。使用不同的块偏移量进行测试，以覆盖存储体的选择逻辑。 <br>验证 readResp.datas 包含之前写入的数据。                                                                                                                                                                                                                                                                                                                                                      |
| 46.3   | ICACHE_ICACHE_DATAARRAY                                                            | READ_DATA_MISS                                       | 向 ICacheDataArray 发送一个读请求，请求的虚拟索引在复位后从未被写入过。 <br>验证 readResp.datas 为 0。                                                                                                                                                                                                                                                                                                                                                                                                                                           |

</mrs-testpoints>

</div>
