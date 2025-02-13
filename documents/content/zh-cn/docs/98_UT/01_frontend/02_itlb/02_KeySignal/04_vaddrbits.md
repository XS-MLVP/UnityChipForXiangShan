---
title: VAddrBits
linkTitle: VAddrBits
weight: 12
---

```scala
def VAddrBits = {
    if (HasHExtension) {
        if (EnableSv48)
            coreParams.GPAddrBitsSv48x4
        else
            coreParams.GPAddrBitsSv39x4
    } else {
        if (EnableSv48)
            coreParams.VAddrBitsSv48
        else
            coreParams.VAddrBitsSv39
    }
} // Parameters.scala: line 596~608

// 相关参数定义
def HasHExtension = coreParams.HasHExtension  // Parameters.scala: line582
coreParams.HasHExtension: Boolean = true      // Parameters.scala: line66
coreParams.EnableSv48: Boolean = true         // Parameters.scala: line91

// 地址位宽定义
coreParams.VAddrBitsSv39: Int = 39
coreParams.GPAddrBitsSv39x4: Int = 41
coreParams.VAddrBitsSv48: Int = 48
coreParams.GPAddrBitsSv48x4: Int = 50        // Parameters.scala: line71~74
```

- **香山昆明湖架构下的值**：`50`
- **地址处理逻辑**：
  - 主机地址转换时仅使用后 48 位（前两位忽略）
  - 支持虚拟机时，物理地址扩展为 50 位（符合 `Sv48x4` 规范）

---