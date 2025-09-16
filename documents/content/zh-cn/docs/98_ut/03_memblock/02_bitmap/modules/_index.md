---
title: Shield-XS Bitmap 硬件设计
description: 本部分文档将会详细介绍香山 bitmap 硬件设计
categories: [bitmap 硬件实现]
tags: [香山, bitmap, 硬件]
weight: 3
---

## Shield-XS Bitmap 硬件设计

在硬件实现层面，Bitmap 机制由两个关键组件构成，即 Bitmap Checker 和 Bitmap Cache。其中，Checker 的职责是读取内存中的权限信息，以确保内存访问的安全性；而 Cache 则旨在加速查找过程，提升整体性能。需要指出的是，当前实现仅支持单向隔离功能。
这意味着在实际应用场景中，它能够有效地防止非安全敏感型负载对安全内存区域的非法访问，但尚未支持更高阶的双向隔离功能，即安全与非安全负载之间的互相访问限制。

#### Shield-XS Bitmap 硬件示意图

![](../mod00.png)

上图展示了一次虚拟地址到物理地址转换过程中如何结合**Shield-Bitmap安全机制**进行访问权限检查。
以及bitmap cache hit 和miss的不同处理。在L1TLB hit时，无需进行bitmap检查，因为L1TLB只会存储bitmap 检查为 allow的项。
如果miss，在L2TLB的page cache中查找，如果页表项和对应的bitmap 均未命中，则先进行查表，后进行bitmap检查并返回结果。如果页表项命中但未进行过bitmap 检查，则只进行bitmap检查。 如果都命中，则直接返回。
