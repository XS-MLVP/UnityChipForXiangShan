---
title: Shield-XS Bitmap总体设计
description: 本节将更近一步介绍Shield-XS Bitmap的技术细节
categories: [bitmap 技术细节]
tags: [香山, Bitmap, 技术细节]
weight: 2
---
本节介绍bitmap的总体设计，不包括具体的硬件实现，只解释概念，包含：
  + **机器模式 Bitmap控制状态寄存器**
 + **Shield-Bitmap Cache 加速查表**
 + **虚拟化两阶段内存地址翻译转换原理**
 + **加入了Shield-XS安全检查后的内存地址转换流程**
 