---
title: CtrlUnit
linkTitle: CtrlUnit
weight: 12
---

<div class="icache-ctx">

</div>

## CtrlUnit

目前 CtrlUnit 主要负责 ECC 校验使能/错误注入等功能。
RegField 案例类和伴生对象的作用，RegReadFn 和 RegWriteFn 案例类和伴生对象的作用。

通过两个控制寄存器 CSR：eccctrl 和 ecciaddr，来实现错误注入。
在 eccctrlBundle 中，定义 eccctrl 的 ierror、istatus、itarget、inject、enable 域的初始值。
在 ecciaddrBundle 中，定义 ecciaddr 的 paddr 域的初始值。

### mmio-mapped CSR

CtrlUnit 内实现了一组 mmio-mapped CSR，连接在 tilelink 总线上，地址可由参数 `cacheCtrlAddressOpt` 配置，默认地址为`0x38022080`。总大小为 128B。

当参数 `cacheCtrlAddressOpt` 为 `None` 时，CtrlUnit **不会实例化**。此时 ECC 校验使能**默认开启**，软件不可控制关闭；软件不可控制错误注入。

目前实现的 CSR 如下：

```plain
              64     10        7         4         2        1        0
0x00 eccctrl   | WARL | ierror | istatus | itarget | inject | enable |

              64 PAddrBits-1               0
0x08 ecciaddr  | WARL |       paddr        |
```

| CSR           | field   | desp                                                                                                                                                                                                                                               |
| ------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| eccctrl       | enable  | ECC 错误校验使能，原 sfetchctl(0) 。 <br>注：即使不使能，在 icache 重填时仍会计算 parity，可能会有额外功耗；但如果不计算，则在未使能转换成使能时需要冲刷 icache（否则读出的 parity 有 50%概率是错的）。                                            |
| eccctrl       | inject  | ECC 错误注入使能，写 1 即使能，读恒 0                                                                                                                                                                                                              |
| eccctrl       | itarget | ECC 错误注入目标 <br>0: metaArray<br>1: rsvd<br>2: dataArray<br>3: rsvd                                                                                                                                                                            |
| eccctrl       | istatus | ECC 错误注入状态（read-only）<br>0: idle：注入控制器闲置<br>1: working：收到注入请求，注入中<br>2: injected：注入完成，等待触发<br>3: rsvd<br>4: rsvd<br>5: rsvd<br>6: rsvd<br>7: error：注入出错                                                  |
| eccctrl       | ierror  | ECC 错误原因（read-only）<br>0: ECC 未使能 (i.e. !eccctrl.enable) <br>1: inject 目标 SRAM 无效 (i.e. eccctrl.itarget==rsvd) <br>2: inject 目标地址 (i.e. ecciaddr.paddr) 不在 ICache 中<br>3: rsvd <br>4: rsvd <br>5: rsvd <br>6: rsvd <br>7: rsvd |
| ecciaddr      | paddr   | ECC 错误注入物理地址                                                                                                                                                                                                                               |
| RERI standard |         | RERI 手册还要求了错误计数等寄存器，用于软件获取 RAS controller 状态，参考手册，可能需要与 dcache、L2cache 统一在后端实现，icache 像现在给 BEU 送 error 一样送给后端。<br>即：暂时不需要在 icache 实现，但要把错误计数等机制所需的接口准备出来      |

### 错误校验使能

CtrlUnit 的 `eccctrl.enable` 位直接连接到 MainPipe，控制 ECC 校验使能。当该位为 0 时，ICache 不会进行 ECC 校验。但仍会在重填时计算校验码并存储，这可能会有少量的额外功耗；如果不计算，则在未使能转换成使能时需要冲刷 ICache（否则读出的 parity code 可能是错的）。

### 错误注入使能

CtrlUnit 内部使用一个状态机控制错误注入过程，其 status （注意：与 `eccctrl.istatus` 不同）有：

- idle：注入控制器闲置
- readMetaReq：发送读取 metaArray 请求
- readMetaResp：接收读取 metaArray 响应
- writeMeta：写入 metaArray
- writeData：写入 dataArray

当软件向 `eccctrl.inject` 写入 1 时，进行以下简单检查，检查通过时状态机进入 `readMetaReq` 状态：

- 若 `eccctrl.enable` 为 0，报错 `eccctrl.ierror=0`
- 若 `eccctrl.itarget` 为 rsvd(1/3)，报错 `eccctrl.ierror=1`

在 `readMetaReq` 状态下，CtrlUnit 向 MetaArray 发送 `ecciaddr.paddr` 地址对应的 set 读取的请求，等待握手。握手后转移到 `readMetaResp` 状态。

在 `readMetaResp` 状态下，CtrlUnit 接收到 MetaArray 的响应，检查 `ecciaddr.paddr` 地址对应的 ptag 是否命中，若未命中则报错 `eccctrl.ierror=2`。否则，根据 `eccctrl.itarget` 进入 `writeMeta` 或 `writeData` 状态。

在 `writeMeta` 或 `writeData` 状态下，CtrlUnit 向 MetaArray/DataArray 写入任意数据，同时拉高 `poison` 位，写入完成后状态机进入 `idle` 状态。

ICache 顶层中实现了一个 Mux，当 CtrlUnit 的状态机不为 `idle` 时，将 MetaArray/DataArray 的读写口连接到 CtrlUnit，而非 MainPipe/IPrefetchPipe/MissUnit。当状态机 `idle` 时反之。

状态机和错误注入流程

- `is_idle`：模块处于空闲状态，等待错误注入的触发。只有当 `eccctrl.istatus` 为 `working` 时，状态机才会转移到 `is_readMetaReq` 状态，准备读取元数据。
- `is_readMetaReq`：发送读取元数据请求。通过接口 `metaRead` 向缓存发送读取请求。当握手成功后状态会转移到 `is_readMetaResp`。
- `is_readMetaResp`：接收元数据响应并验证。如果未命中，则会设置错误状态。没命中会转移状态到`is_idle`,并设置错误错误注入状态和错误原因；如果找到有效的缓存行并且标签匹配，根据错误注入目标来判断是向元数据还是数据阵列写入错误。
- `is_writeMeta`：写入带 poison 标记的数据完成注入。当握手成功后，错误注入状态设置为 injected（注入完成，等待触发）,状态转移到`is_idle`。
- `is_writeData`：写入带 poison 标记的数据完成注入。当握手成功后，向数据阵列写入错误数据，错误注入状态设置为 injected（注入完成，等待触发）,状态转移到`is_idle`。

寄存器和接口映射

- eccctrl：控制 ECC 启用、错误注入状态等。寄存器通过 eccctrlRegField 进行映射。
- ecciaddr：指定错误注入的物理地址。通过 ecciaddrRegField 映射。
- 通过寄存器描述符（RegFieldDesc）和寄存器字段（RegField），定义了寄存器的这些是寄存器的描述信息和读写逻辑。
- 通过 node.regmap，这两个寄存器被映射到指定的地址偏移。eccctrl 寄存器被映射到 params.eccctrlOffset 地址，ecciaddr 寄存器被映射到 params.ecciaddrOffset 地址。
- `node.regmap` 使得这两个寄存器可以通过外部的 TileLink 接口进行访问，外部模块可以读写这些寄存器以控制 ECC 和错误注入功能。

## CtrlUnit 的功能点和测试点

### ECC 启用/禁用

控制 eccctrl.enable 字段来启用或禁用 ECC 功能。外部系统可以通过写寄存器 eccctrl 来控制 ECC 是否启用。

- 通过寄存器写入控制信号 enable，当 enable 为 true 时，ECC 功能启用；为 false 时，ECC 功能禁用。

1. 启用 ECC

- 向 eccctrl.enable 寄存器写入 true，验证模块内部 eccctrl.enable 设置为 true，并确保后续的错误注入操作能够成功进行。此测试确保 eccctrl.enable 写操作被执行。
- 确保 eccctrl.enable 被正确设置为 true，并触发 eccctrlRegWriteFn 中的写操作逻辑。

2. 禁用 ECC

- 向 eccctrl.enable 寄存器写入 false，验证模块内部 eccctrl.enable 设置为 false，并确保在后续的错误注入过程中，ECC 功能被禁用，不允许进行错误注入。此测试确保 eccctrl.enable 写操作被正确设置为 false。
- 验证禁用 ECC 时 eccctrl.enable 为 false，并触发 eccctrlRegWriteFn 中的错误处理分支。x.istatus = eccctrlInjStatus.error 和 x.ierror = eccctrlInjError.notEnabled

### 状态机转换

根据状态机的状态，验证错误注入的流程是否正确。

1. is_idle 状态

- 初始为 is_idle 状态。
- 当 eccctrl.istatus 为 working 时，验证此时的状态为 is_readMetaReq。

2. is_readMetaReq 状态

- 当握手成功后（io.metaRead.ready 和 io.metaRead.valid 都为高），验证此时的状态为 is_readMetaResp。

3. is_readMetaResp 状态

- 未命中
  - 当 waymask 全零的时候，表示没有命中，会进入 is_idle 状态，并且设置错误错误注入状态和错误原因。
  - 验证此时的状态为 is_idle， eccctrl.istatus = error 和 eccctrl.ierror = notFound。
- 命中
  - 当 waymask 不全零的时候，表示命中，会根据错误注入目标来判断是向元数据还是数据阵列写入错误。
  - 当 eccctrl.itarget=metaArray 时，验证此时的状态为 is_writeMeta ；当 eccctrl.itarget！=metaArray 时，验证此时的状态为 is_writeData。

4. is_writeMeta 状态

- RegWriteFn
  - 此状态进入后，io.dataWrite.valid 会为高
  - x.itarget = req.itarget
  - 当 req.inject 为高并且 x.istatus = idle 时：
    - 如果 ecc 的 req.enable = false，则验证 x.istatus = error 且 x.ierror = notEnabled
    - 否则，如果 req.itarget ！= metaArray 和 dataArray，则验证 x.istatus = error 且 x.ierror = targetInvalid
    - 如果都不满足，则验证 x.istatus = working
- 状态转换
  - 当 io.metaWrite.fire 为高， 验证下一个状态为 is_idle，并且 eccctrl.istatus = injected。

5. is_writeData 状态

- RegWriteFn
  - 此状态进入后，io.dataWrite.valid 会为高
  - res.inject = false
  - 当 ready 为高，且 x.istatus = injected 或 x.istatus = error 时，验证 x.istatus = idle 和 x.ierror = notEnabled
- 状态转换
  - 当 io.dataWrite.fire 为高， 验证下一个状态为 is_idle，并且 eccctrl.istatus = injected。

### 寄存器映射和外部访问

通过 TileLink 总线将寄存器映射到特定地址，使外部模块可以读写 ECC 控制寄存器和注入地址寄存器。

- 使用 TLRegisterNode 实现寄存器的映射，使得外部系统可以通过地址访问寄存器。寄存器的读写操作通过 TileLink 协议进行。

1. 外部读取和写入 ECC 控制寄存器

- 验证外部模块可以通过 TileLink 协议正确读取和写入 eccctrl 和 ecciaddr 寄存器，并对模块内部的状态产生影响，确保读写操作完全覆盖。

2. 外部模块触发错误注入

- 通过外部模块经 TileLink 总线向 eccctrl.inject 寄存器写入 true，触发错误注入，验证内部状态是否按 RegWriteFn 内部过程执行。