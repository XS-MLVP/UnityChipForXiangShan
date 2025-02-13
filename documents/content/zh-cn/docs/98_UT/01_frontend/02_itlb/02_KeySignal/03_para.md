---
title: 外部传入参数
linkTitle: 参数
weight: 12
---

### 参数说明

```scala
class TLB(Width: Int, nRespDups: Int = 1, Block: Seq[Boolean], q: TLBParameters)(implicit p: Parameters) extends TlbModule
  with HasCSRConst
  with HasPerfEvents
```

| 参数                  | 说明                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `Width: Int`          | 指示 `requestor` 的数量                                              |
| `nRespDups: Int = 1`  | 需要复制 `response` 的数目，默认为 `1`（不复制）                     |
| `Block: Seq[Boolean]` | 指示每个 `requestor` 是否被阻塞                                      |
| `q: TLBParameters`    | TLB 使用的参数                                                       |
| `p: Parameter`        | 全局参数（香山架构参数）                                             |

实例化 `TLB` 时以香山架构的 `itlb` 为例：

```scala
val itlb = Module(new TLB(coreParams.itlbPortNum, nRespDups = 1, Seq.fill(PortNumber)(false) ++ Seq(true), itlbParams))
```

- `Width` 值为 `coreParams.itlbParams`（实际计算逻辑）：
  ```scala
  itlbPortNum: Int = ICacheParameters().PortNumber + 1  // Parameters.scala: line 276
  ICacheParameters.PortNumber: Int = 2                 // ICache.scala: line 43
  ```
  最终 `Width = 3`

- `Block` 参数说明：
  ```scala
  Seq.fill(PortNumber)(false) ++ Seq(true)  // 前 2 端口不阻塞，第 3 端口阻塞
  ```
  对应 `itlb` 的三个 `requestor`：`requestor0/1` 不阻塞，`requestor2` 阻塞。

---