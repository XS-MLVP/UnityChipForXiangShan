---
title: 机器模式Bitmap控制状态寄存器
categories: [bitmap 技术细节]
tags: [香山, Bitmap, 技术细节]
weight: 1
---

## 机器模式 Bitmap控制状态寄存器

### 基本信息

| 寄存器名称 | MBMC（Machine BitMap Control）                                |
| ---------- | ------------------------------------------------------------- |
| 特权模式   | 机器模式                                                      |
| 寄存器编号 | 0xBC2                                                         |
| 读写权限   | 可读可写                                                      |
| 功能描述   | 用来控制Shield-bitmap 的使能、同步、Shield-XS Bitmap 基地址等 |

### 字段描述

| 地址       | 字段                     | 描述                                                                                                         |
| ---------- | ------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **[61:3]** | **BMA (Bitmap Address)** | Shield-XS Bitmap 基地址指定 Bitmap 数据结构在物理内存中的起始地址。                                          |
| 2          | CMODE (Current Mode)     | 表明当前执行模式CMODE = 1，表示安全模式CMODE = 0, 表示非安全模式。                                           |
| 1          | BCLEAR (Bitmap Clear)    | Shield-XS Bitmap 同步位BCLEAR = 1，表示刷新所有Shield-bit 副本。<br/>**注：实际使用过程，可结合HFence 指令** |
| 0          | BME (Bitmap Enable)      | Shield-XS 使能位当 BME 置为 1 时，启用 Bitmap 功能。一旦启用，无法关闭，也无法修改 Bitmap 的基地址。         |

## 数据结构

![Shield-XS Bitmap数据结构](../../feature00_1.png)

#### Shield-XS Bitmap数据结构

上图为Shield-XS Bitmap的数据结构，所有的Shield-XS Bitmap权限数据都被存放在一块连续的物理内存区域中。其中基地址是存放Shield-XS Bitmap 数据结构的内存区域的起始物理地址。这个地址可以通过MBMC寄存器中的 BMA字段进行配置。

Shield-XS Bitmap 数据结构的大小取决于系统内存的大小。每个4k物理页对应一个比特位。一个4k页对应的权限根据其物理地址存放在Shield-XS Bitmap 数据结构中，其位置可以通过基地址加上该4k页物理地址的偏移量计算得出。

**当BME =1 （开启bitmap） 且CMODE= 0 （当前模式处于 非安全模式）时，会进行bitmap检查。当bitmap 检查 当前4k页 bitmap属性 为1（ 安全页面）时，会触发访问错误（access fault）。**

**当BME =1 （开启bitmap） 且CMODE= 1 （当前模式处于 安全模式）。无论安全还是非安全页面，当前状态都允许访问，因此无需进行bitmap检查。**

**当BME =0 （关闭bitmap）无需进行bitmap检查。**
