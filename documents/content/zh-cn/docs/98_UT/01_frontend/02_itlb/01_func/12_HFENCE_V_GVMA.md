---
title: 支持 HFENCE.VVMA 与 HFENCE.GVMA 指令
linkTitle: 12.HFENCE_V/GVMA
weight: 12
---

事实上，对 `hv`（`SFENCE Bundle` 中的信号，用于刷新第一阶段地址转换的条目）和 `hg`（`SFENCE Bundle` 中的信号，用于刷新第二阶段地址转换的条目）信号不为 `0` 的情况执行的指令并不是 `SFENCE.VMA`，而是 `HFENCE.VVMA` 和 `HFENCE.GVMA`：

![HFENCE.VVMA 与 HFENCE.GVMA](HFENCE.png)

这两个指令与 `SFENCE.VMA` 功能很相似，区别在于 `HFENCE.VVMA` 适用于由 `vsatp` 控制的 `VS` 级别内存管理数据结构；`HFENCE.GVMA` 适用于由 `hgatp` 控制的虚拟机监管程序 `G` 阶段内存管理数据结构。

`HFENCE.VVMA` 仅在 `M` 模式或 `HS` 模式生效，类似于暂时进入 `VS` 模式并执行 `SFENCE.VMA` 指令，可以保证当前 `hart` 之前的所有存储操作在后续的隐式读取 `VS` 级别内存管理数据结构之前都已经排序；注意这里所说的隐式读取指的仅有在 `HFENCE.VVMA` 之后执行的，并且 `hgatp.VMID` 与执行 `HFENCE.VVMA` 相同的时候，简单来说就是仅对当前这一个虚拟机生效。`rs1` 与 `rs2` 的功能与 `SFENCE.VMA` 相同。

对 `HFENCE.GVMA` 来说，`rs1` 指定的是客机的物理地址。由于主机采用 `SV48` 而虚拟机采用 `SV48x4`，客机物理地址比主机物理地址多两位，因此此时需要将 `rs1` 对应的客机物理地址右移两位。如果某一个虚拟机的地址翻译模式更改了，也即 `hgatp.MODE` 对某个 `VMID` 更改了，则必须使用 `HFENCE.GVMA` 指令，将 `rs1` 设为 `0`，`rs2` 设为 `0` 或 `VMID` 进行刷新。

在香山中，由于 `TLB` 本身不存储中间物理地址，也即 `TLB` 并不存储 `VS` 阶段转换出来的虚拟机物理地址，也无法单独提供 `G` 阶段地址转换请求。在 `TLB` 中存储的是两阶段地址翻译的最终结果，因此 `HFENCE.VVMA` 与 `HFENCE.GVMA` 在 `TLB` 中作用相同，均为刷新掉两阶段地址翻译的结果。无论 `hv` 与 `hg` 哪一个信号为 `1` 都将刷新两阶段的条目。