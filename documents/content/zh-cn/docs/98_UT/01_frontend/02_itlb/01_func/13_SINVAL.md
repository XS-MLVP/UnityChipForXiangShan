---
title: 支持 SINVAL 扩展
linkTitle: 13.SINVAL
weight: 12
---

在 `RISC-V` 特权指令集中定义了 `Svinval` 扩展（`Supervisor Virtual Address Invalidation`），在香山昆明湖架构实现了该扩展。`Svinval` 扩展的意义在于将 `SFENCE.VMA` 指令更加细化为 `SFENCE.W.INVAL`、`SINVAL.VMA`、`SFENCE.INVAL.IR` 三条指令（`HFENCE.VVMA` 和 `HFENCE.GVMA` 同理）。

`SINVAL.VMA` 指令事实上与 `SFENCE.VMA` 指令的功能基本一致，只是添加了对 `SFENCE.W.INVAL` 与 `SFENCE.INVAL.IR` 两个指令的相互排序，可以理解为需要在两个指令中间进行。`SFENCE.W.INVAL` 指令用于确保当前 `RISC-V hart` 可见的任何先前存储在后续由同一个 `hart` 执行的 `SINVAL.VMA` 指令之前被重新排序。`SFENCE.INVAL.IR` 指令确保当前 `hart` 执行的任何先前 `SINVAL.VMA` 指令在后续隐式引用内存管理数据结构之前被排序。当由单个 `hart` 按顺序（不一定连续）执行 `SFENCE.W.INVAL`、`SINVAL.VMA` 和 `SFENCE.INVAL.IR` 时，可以相当于执行了 `SFENCE.VMA` 指令。

![SINVAL.VMA](SINVAL_VMA.png)

![SFENCE.W.INVAL 和 SFENCE.INVAL.IR](SFENCE_W_INVAL&INVAL_IR.png)