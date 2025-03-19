---
title: 果壳Cache文档案例
linkTitle: 果壳Cache文档案例
weight: 10
---

本文档将以[果壳L1Cache](https://github.com/OSCPU/NutShell/blob/fc12171d929e7e589fab9f794ab63ce12e6c594e/src/main/scala/nutcore/mem/Cache.scala)作为案例，展示一个具有相当复杂度的模块的验证文档例子。

# 果壳L1Cache验证文档


## 文档概述

本文档针对NutShell L1Cache的验证需求撰写，通过对其功能进行描述并依据功能给出参考测试点，从而帮助验证人员编制测试用例。

果壳（NutShell）是一款由5位中国科学院大学本科生设计的基于RISC-V RV64开放指令集的顺序单发射处理器([NutShell·Github](https://github.com/OSCPU/NutShell)), 隶属于国科大与计算所“一生一芯”项目。而果壳Cache（NutShell Cache）是其缓存模块，采用可定制化设计（L1 Cache和L2 Cache采用相同的模板生成，只需要调整参数），具体来说，L1 Cache（指令Cache和数据Cache）大小为32KB，L2 Cache大小为128KB, 在整体结构上，果壳Cache采用三级流水的结构。

本次验证的目标是L1 Cache，即一级缓存。

## 术语说明

优先解释模块专有缩写（如TLB， FIFO等）
对容易混淆的概念请务必明确（如虚拟地址和物理地址等）

| 缩写	| 全称 | 定义 |
| -- | ----- | ---|
| MMIO | Memory-Mapped Input/Output	| 描述1 |
| 缩写2	| FULL_NAME_2	| 描述2 |
| 缩写3	| FULL_NAME_3	| 描述3 |

## 前置知识

### Cache的层次结构 

Cache有三种主要的组织方式：直接映射（Direct-Mapped）Cache、组相连（Set-Associative）Cache和全相连（Fully-Associative）Cache。对于物理内存中的一个数据，如果在Cache中只有一个位置可以存放它，这就是直接映射Cache；如果有多个位置可以存放这个数据，这就是组相连Cache；如果Cache中的任何位置都可以存放这个数据，这就是全相连Cache。

直接映射Cache和全相连Cache实际上是组相连Cache的两种特殊情况。现代处理器中的Cache通常属于这三种方式中的一种。例如，翻译后备缓冲区（TLB）和Victim Cache多采用全相连结构，而普通的指令缓存（I-Cache）和数据缓存（D-Cache）则采用组相连结构。当处理器需要执行一个指令时，它会首先查找该指令是否在I-Cache中。如果在，则直接从I-Cache中读取指令并执行；如果不在，则需要从内存中读取指令到I-Cache中，再执行。与I-Cache类似，当处理器需要读取或写入数据时，会首先查找D-Cache。如果数据在D-Cache中，则直接读取或写入；如果不在，则需要从内存中加载数据到D-Cache中。与I-Cache不同的是，D-Cache需要考虑数据的一致性和写回策略。为了保证数据的一致性，当数据在D-Cache中被修改后，需要同步更新到内存中。

![composition](composition.png)

### Cache的写入

在执行写数据时，如果只是向D-Cache中写入数据而不改变其下级存储器中的数据，就会导致D-Cache和下级存储器对于同一地址的数据不一致（non-consistent）。为了保持一致性，一般Cache在写命中状态下采用两种写入方式：
（1）写通（Write Through）：数据写入D-Cache的同时也写入其下级存储器。然而，由于下级存储器的访问时间较长，而存储指令的频率较高，频繁地向这种较慢的存储器中写入数据会降低处理器的执行效率。
（2）写回（Write Back）：数据写入D-Cache后，只是在Cache line上做一个标记，并不立即将数据写入更下级的存储器。只有当Cache中这个被标记的line要被替换时，才将其写入下级存储器。这种方式能够减少向较慢存储器写入数据的频率，从而获得更好的性能。然而，这种方式会导致D-Cache和下级存储器中许多地址的数据不一致，给存储器的一致性管理带来一定的负担。

D-Cache处理写缺失一般有两种策略：

（1）非写分配（Non-Write Allocate）：直接将数据写入下级存储器，而不将其写入D-Cache。这意味着当发生写缺失时，数据会直接写入到下级存储器，而不会经过D-Cache。
（2）写分配（Write Allocate）：在发生写缺失时，会先将相应地址的整个数据块从下级存储器中读取到D-Cache中，然后再将要写入的数据合并到这个数据块中，最终将整个数据块写回到D-Cache中。这样做的好处是可以在D-Cache中进行更多的操作，但同时也增加了对内存的访问次数和延迟。
写通（Write Through）和非写分配（Non-Write Allocate）将数据直接写入下级存储器，而写回（Write Back）和写分配（Write Allocate）则会将数据写入到D-Cache中。通常情况下，D-Cache的写策略搭配为写通+非写分配或写回+写分配。

## 附录

**写通示意图**：

<img src="Write-through_with_no-write-allocation.png" alt="write-through" width="400" />

**写回示意图**：

<img src="Write-back_with_write-allocation.png" alt="write-back" width="400" />

## 整体框图和流水级示意

以下是L1Cache的整体框图和流水级示意：

![Cache](Cache.png)


## 子模块列表

以下是NutShell L1Cache的一些子模块：

| 子模块                 | 描述                |
| -------------------- | ------------------- |
| s1 | 缓存阶段1  |
| s2 | 缓存阶段2  |
| s3 | 缓存阶段3 |
| metaArray | 以数组形式存储元数据 |
| dataArray | 以数组形式存储缓存数据 |
| arb | 总线仲裁器 |

上下游通信总线采用SimpleBus总线，包含了req和resp两个通路，其中req通路的cmd信号表明请求的操作类型，可以通过检查该信号获得访问类型。SimpleBus总线共有七种操作类型，由于NutShell文档未涉及probe和prefetch操作，在验证中只出现五种操作：read、write、readBurst、writeBurst、writeLast，前两种为字读写，后三种为Burst读写，即一次可以操作多个字。

<mrs-functions>

## 模块功能说明 

Cache的功能是降低访存的时间开销，其功能本质上和内存是一致的。也就是说，不论是向Cache存数还是取数，其都应该和直接向内存存取的数是一样的。
因此，Cache的基础读写功能将成为我们的第一个功能点。

进一步，访问Cache的地址空间分为MMIO和内存。其中，访问MMIO的地址空间时，Cache一定会Miss，然后将请求转发到MMIO端口上。而访问内存的地址空间时，Cache则会根据该地址所在的Cache Line是否在Cache中而触发Hit或者Miss。Hit则直接返回响应，Miss则会将请求转发到内存端口。如果被替换的受害者行之前被写过，是dirty的，则要先将受害者行写回（write-back）内存，否则直接从内存加载缺失的Cache Line，重填（refill）回Cache。


### 1. 内存备份

Cache的功能本质上和内存是一致的，所以，不管向Cache存或取数据，本质上都应该和从内存存取的数一样。

据此，我们为这一功能点安排了一个测试点：即Cache应当为内存的备份。在实际测试过程中，必须同时考虑读写两方面的一致性。

### 2. MMIO

Cache会根据地址所在的区间，判断是否发生MMIO请求。

#### 2.1. MMIO读写

如果发生MMIO请求则会将请求转发到MMIO的端口上，而不会发生Cache行的读写。此外，MMIO请求不是Burst请求，每次只会写入或读出一个地址的数据，而不是一个Cache行的数据。因此，在MMIO端口上不应当观测到Burst的请求类型。

据此，我们可以设计下述两个测试点：

| 序号 |  功能名称 | 测试点名称      | 描述                  |
| ----- |-----------------|---------------------|------------------------------------|
| 2\.1 | CACHE_MMIO_RW | FORWARD | Cache接收到MMIO空间的请求时，不应发生读写，而是直接转发给MMIO端口 | 
| 2\.2 | CACHE_MMIO_RW | NO_BURST | Cache接收到MMIO空间的请求时，MMIO端口接收到的Cache请求不应为BURST类型 |

### 2.2. MMIO阻塞

NutShell手册指出，在检测出MMIO请求后会阻塞流水线。

因此，我们将设计这一测试点：当MMIO请求发出后，应当检查流水线是否阻塞。

### 3. Cache命中

NutShell的Cache采用写回策略，因此，在写命中时，需要标记脏块，后续发生缓存行替换时再将对应的缓存行写回内存。

同时，因为采用写回方式，所以，即使写命中也不需要同内存进行交互，因此收到回复的周期数更少。

#### 3.1. 写命中

由于果壳Cache采用写回策略，因此，在发生写命中时，需要标记脏位，后续还要写回内存中。据此，可以设置一个测试点。

#### 3.2. 命中时序

命中发生时，即使是写命中，也无需写回或者重填，因此，回复的时间会更短一些。

| 序号 |  功能名称 | 测试点名称      | 描述                  |
| ----- |-----------------|----------------|----------------|
| 3\.1 | CACHE_HIT | WRITE | Cache写命中时，应设置脏位 | 
| 3\.2 | CACHE_HIT | SHORTER | Cache写命中时，回复的周期应该更少 | 

### 4. Cache缺失

为了创造Cache Miss的测试环境，首先需要通过一系列的Load操作先将Cache填满。后续需要触发Cache Miss时，只需要访问上述Load覆盖范围之外的地址即可。

#### 4.1. 缺失通用行为

发生Cache Miss时，会阻塞流水线，同时，NutShell Cache重填时采用**关键字优先方案**，即缺失发生时，系统会优先获取CPU所需要的当前指令或数据所对应的字。因此，Cache向内存请求数据时，发出的首个地址应当是向Cache发出请求时的地址。例如，假设向Cache发出0x1000地址的读请求，此时发生Cache Miss，Cache会向内存发出读请求，这个请求的首地址应当是0x1000。显然Cache缺失时，回复的时间会更长。

从而，我们可以划分如下的测试点：

| 序号 |  功能名称 | 测试点名称      | 描述                  |
| ----- |-----------------|----------------|----------------|
| 4\.1\.1 | CACHE_MISS_COMMON | BLOCK | 发生缺失时，也会阻塞流水线 | 
| 4\.1\.2 | CACHE_MISS_COMMON | CRITICAL_WORD | Cache缺失时，Cache发出请求的首个地址应当是向Cache请求的地址 | 
| 4\.1\.3 | CACHE_MISS_COMMON | LONGER | Cache缺失时，回复的时间会更长 | 


#### 4.2. 脏块写回

当需要替换的Cache块是脏块时，首先会进行写回的操作。

在进行测试时，我们首先需要创建脏块的环境，由于NutShell Cache采用**随机替换**的策略，因此我们考虑将整个Cache都设置成脏块。操作也是简单的，在上述的Load的基础上，只需要在每个CacheLine的起始地址进行一次Store操作即可。

#### 4.3. 干净块不写回

当需要替换的Cache块是干净的时，不会写回这个Cache块。

</mrs-functions>

## 常量说明 \[可选项\] 需列出模块中所有可配置参数及其物理意义

| 常量名 | 常量值 | 解释 |
| ---- | ---- | ---- |
| 缓存行大小 | 64 | 以字节为单位的缓存行大小 |
| L1Cache大小 | 32 | L1Cache的总容量，单位为千字节 |

## 接口说明 \[必填项\] 详细解释各种接口的含义、来源
|信号|说明|
| --- | --- |
| clock<br>reset   | 时钟<br>复位信号|
| io\_flush<br>io\_empty <br> io\_in\_* |<br><br> 请求总线信号(req \& resp) |
| io\_out\_mem\_* & cache向内存请求的总线信号\\
    \hline
    io\_mmio\_*     & cache向MMIO请求的总线信号\\
    \hline
    io\_out\_coh\_* & 一致性相关的信号\\
    \hline
    victim\_way\_mask   & 受害者相关信号，即被替换的cache块相关信息\\
## 接口时序 \[可选项\] 对复杂接口，提供波形图的案例

### 案例1

请在这里填充时序案例1

### 案例2

请在这里填充时序案例2

## 测试点总表 (\[必填项\] 针对细分的测试点，列出表格)

实际使用下面的表格时，请用有意义的英文大写的功能名称和测试点名称替换下面表格中的名称

<mrs-testpoints>

| 序号 |  功能名称 | 测试点名称      | 描述                  |
| ----- |-----------------|---------------------|------------------------------------|
| 1\.1\.1 | FUNCTION_1_1 | TESTPOINT_A | 功能1\.1的测试点A，使用时请替换为您的测试点的输入输出和判断方法 | 
| 1\.1\.2 | FUNCTION_1_1 | TESTPOINT_B | 功能1\.1的测试点B，使用时请替换为您的测试点的输入输出和判断方法 | 
| 1\.1\.3 | FUNCTION_1_1 | TESTPOINT_C | 功能1\.1的测试点C，使用时请替换为您的测试点的输入输出和判断方法 | 
| 1\.2\.1 | FUNCTION_1_2 | TESTPOINT_X | 功能1\.2的测试点X，使用时请替换为您的测试点的输入输出和判断方法 | 
| 1\.2\.2 | FUNCTION_1_2 | TESTPOINT_Y | 功能1\.2的测试点Y，使用时请替换为您的测试点的输入输出和判断方法 | 
| 2\.1 | FUNCTION_2 | TESTPOINT_2A | 功能2的测试点2A，使用时请替换为您的测试点的输入输出和判断方法 | 
| 2\.2 | FUNCTION_2 | TESTPOINT_2B | 功能2的测试点2B，使用时请替换为您的测试点的输入输出和判断方法 | 

</mrs-testpoints>
