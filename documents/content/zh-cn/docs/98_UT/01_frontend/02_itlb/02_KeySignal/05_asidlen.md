---
title: AsidLength
linkTitle: AsidLength
weight: 12
---

```scala
def AsidLength = coreParams.AsidLength  // Parameters.scala: line 619
AsidLength: Int = 16                    // Parameters.scala: line 79
```

- **ASID 位宽**：16 位
- **作用**：标识地址空间，防止进程/虚拟机虚拟地址冲突
- **支持规模**：
  - 最大 `65536` 个并发进程（16 位）
  - 虚拟机通过 `vmid` 标识（14 位，支持 `16384` 个虚拟机，符合手册要求）
