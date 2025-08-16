---
title: 香山bitmap 应用场景
description: 香山bitmap 应用场景
categories: [香山 Bitmap 基础设计]
tags: [香山, Bitmap, 基础]
weight: 4
---

## 应用场景

### 1. 机密虚拟机

![应用场景-机密虚拟机](../../basic03_1.png)

Shield-XS用于普通虚拟机和机密虚拟机的隔离。在机密虚拟机（Confidential VM， CVM）环境中，bitmap 用于标记和隔离安全内存区域。

普通虚拟机在访问内存时，硬件通过 bitmap 检查机制确保其只能访问被授权的内存区域，从而实现虚拟机之间的内存隔离。

注：机密虚拟机之间的隔离通过MMU 完成，不需要经过Bitmap 的检查机制。

CVM Bitmap 的资源的标记和分配由C-SDSM (Confidential Supervisor Domain Security Manager) 完成，Hypervisor 和 CVM 通过TEECall 和 TEEResume 进行安全世界的交互。

![安全世界接口](../../basic03_2.png)

**TEECall**

- 从普通世界（Normal World）切换到安全世界（TEE），进入敏感工作负载执行流程。

**TEEResume**

- 从 TEE 返回普通世界，恢复 Normal Workloads 的执行。

### 2. 安全增强容器

![应用场景-容器](../../basic03_3.png)

上图显示了bitmap在容器中的应用场景。安全容器和普通容器都位于可信计算基的保护范围内。在安全容器中运行的应用程序可能包含敏感数据或关键业务逻辑。为了防止这些数据被普通容器或恶意软件访问，采用通过 **bitmap 机制**进行隔离。

Bitmap 数据结构用于标记哪些物理页属于安全容器的存储空间，通过将对应该容器内存区域的位图数据写为1，确保普通容器无法访问这些存储空间。只有安全容器内的应用程可以访问这些被标记为安全的内存页。

普通容器中的应用程序可能来自不可信的来源。通过 bitmap 机制，普通容器的内存访问被限制在非安全内存区域。任何试图访问安全内存的请求都会被硬件拦截，并触发Access Fault。

在上述场景的具体的实施细节中，**<font style="color:#ee0000;">软件模块负责Bitmap管理和配置 ， 硬件机制负责Bitmap检查和同步。<font>**
