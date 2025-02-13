---
title: sfence
linkTitle: sfence
weight: 12
---

```scala
val sfence = Input(new SfenceBundle)
```

`sfence`：用于传入 `SfenceBundle`，执行 `SFENCE` 指令刷新 `TLB` 缓存。

```scala
class SfenceBundle(implicit p: Parameters) extends XSBundle {
    val valid = Bool()
    val bits = new Bundle {
        val rs1 = Bool()
        val rs2 = Bool()
        val addr = UInt(VAddrBits.W)
        val id = UInt((AsidLength).W) // asid or vmid
        val flushPipe = Bool()
        val hv = Bool()
        val hg = Bool()
    }
    
    override def toPrintable: Printable = {
        p"valid:0x${Hexadecimal(valid)} rs1:${bits.rs1} rs2:${bits.rs2} addr:${Hexadecimal(bits.addr)}, flushPipe:${bits.flushPipe}"
    }
}
```

#### `valid`
- 有效标志信号，指示 `SFENCE.VMA` 操作的请求是否有效。如果该信号为高（`1`），表示当前的 `SFENCE.VMA` 操作需要执行；如果为低（`0`），则没有操作需要执行。

#### `rs1`
- 表示需要使用 `SFENCE.VMA` 指令中的 `rs1` 寄存器的值，这个值通过信号 `addr` 传入，标记了需要刷新的虚拟地址。
- 当 `rs1` 为非零时，表示 `SFENCE.VMA` 只针对该虚拟地址所对应的页表条目进行刷新操作；如果 `rs1` 为零，则表示刷新所有虚拟地址的映射。

#### `rs2`
- 表示需要使用 `SFENCE.VMA` 指令中的 `rs2` 寄存器的值，其中存储着需要刷新的 `ASID`，通过信号 `id` 传入。
- 当 `rs2` 为非零时，表示 `SFENCE.VMA` 只对指定的 `ASID` 进行刷新操作；如果 `rs2` 为零，则表示刷新所有地址空间的映射。这个信号主要用于区分不同进程的地址空间。

#### `addr`
- 表示 `SFENCE.VMA` 指令中 `rs1` 对应的虚拟地址（可能是部分地址）。该信号提供了具体的虚拟地址信息，当 `rs1` 为非零时，`TLB` 将使用该地址作为参考，刷新与该地址对应的页表条目。它用于精细控制哪些地址映射需要被刷新。
- 信号的位宽为 `VAddrBits`，即虚拟地址的位宽，可见于 \ref{subsec:consts}，大小被定义为 `50`，其中事实上使用的只有 `addr[47:12]`，也即四级页表的四级索引部分，用于找到对应虚拟地址的页表项。

#### `id`
- 表示 `SFENCE.VMA` 操作涉及的地址空间标识符（`ASID`）。用于指定某个具体的 `ASID`。它允许在多地址空间的场景下（例如多个进程共享一个处理器），只刷新某个特定进程的地址映射。
- 信号位宽为 `AsidLength`，可见于 \ref{subsec:consts}，大小为 `16`，意味着同时支持 $2^{16}$ 个虚拟地址空间。

#### `flushPipe`
- 控制是否需要 **清空流水线**。`SFENCE.VMA` 操作不仅可能涉及刷新 `TLB`，还可能需要清空流水线以确保所有未完成的指令（可能依赖旧的地址映射）不会继续使用过时的页表映射。这个信号为高时，表示需要清空流水线。

#### `hv`
- 表示当前指令是否为 `HFENCE.VVMA`。

#### `hg`
- 表示当前指令是否为 `HFENCE.GVMA`。