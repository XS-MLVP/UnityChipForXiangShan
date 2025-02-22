---
title: 关键信号说明
linkTitle: 关键信号说明
weight: 12
---

## 相关 CSR 寄存器

```scala
val csr = Input(new TlbCsrBundle)
```

`csr`：包含 `satp`、`vsatp`、`hgatp` 三个寄存器的信息以及一些权限信息。

```scala
class TlbCsrBundle(implicit p: Parameters) extends XSBundle {
	val satp = new TlbSatpBundle()
	val vsatp = new TlbSatpBundle()
	val hgatp = new TlbHgatpBundle()
	val priv = new Bundle {
		val mxr = Bool()
		val sum = Bool()
		val vmxr = Bool()
		val vsum = Bool()
		val virt = Bool()
		val spvp = UInt(1.W)
		val imode = UInt(2.W)
		val dmode = UInt(2.W)
	}
	
	override def toPrintable: Printable = {
		p"Satp mode:0x${Hexadecimal(satp.mode)} asid:0x${Hexadecimal(satp.asid)} ppn:0x${Hexadecimal(satp.ppn)} " +
		p"Priv mxr:${priv.mxr} sum:${priv.sum} imode:${priv.imode} dmode:${priv.dmode}"
	}
}
```

`TlbCsrBundle` 中包含了 `satp`、`vsatp`、`hgatp` 以及 `priv` 特权标志。其中 `satp` 与 `vsatp` 通过 `TlbSatpBundle` 实现，包括 `mode`、`asid`、`ppn`、`changed` 以及一个 `apply` 方法：

```scala
class SatpStruct(implicit p: Parameters) extends XSBundle {
	val mode = UInt(4.W)
	val asid = UInt(16.W)
	val ppn  = UInt(44.W)
}

class TlbSatpBundle(implicit p: Parameters) extends SatpStruct {
	val changed = Bool()
	
	// Todo: remove it
	def apply(satp_value: UInt): Unit = {
		require(satp_value.getWidth == XLEN)
		val sa = satp_value.asTypeOf(new SatpStruct)
		mode := sa.mode
		asid := sa.asid
		ppn := sa.ppn
		changed := DataChanged(sa.asid) // when ppn is changed, software need do the flush
	}
}
```

`hgatp` 通过 `TlbHgatpBundle` 实现，区别在于将 `asid` 替换为 `vmid`：

```scala
class HgatpStruct(implicit p: Parameters) extends XSBundle {
	val mode = UInt(4.W)
	val vmid = UInt(16.W)
	val ppn  = UInt(44.W)
}

class TlbHgatpBundle(implicit p: Parameters) extends HgatpStruct {
	val changed = Bool()
	
	// Todo: remove it
	def apply(hgatp_value: UInt): Unit = {
		require(hgatp_value.getWidth == XLEN)
		val sa = hgatp_value.asTypeOf(new HgatpStruct)
		mode := sa.mode
		vmid := sa.vmid
		ppn := sa.ppn
		changed := DataChanged(sa.vmid) // when ppn is changed, software need do the flush
	}
}
```

#### `SATP`
- `satp (Supervisor Address Translation and Protection)` 用于内核态（`Supervisor mode`）进行虚拟地址到物理地址的转换管理，通常在非虚拟化环境或作为虚拟机监控程序（`VMM`）时使用。
- `mode`：地址转换模式，控制虚拟地址的转换，位宽为 `4`。其允许的值包含 `0`、`8`、`9`，如果是其它值应当触发 `illegal instruction fault`。
  - `0`: `Bare` 模式，不进行地址转换。
  - `8`: `SV39` 模式，使用三级页表支持 `39` 位虚拟地址空间。
  - `9`: `SV48` 模式，使用四级页表支持 `48` 位虚拟地址空间。
- `asid`：地址空间标识符，用于区分不同进程，香山昆明湖架构使用的 `SV48` 中最大长度为 `16`。
- `ppn`：`Page Table Pointer`，根页表的物理页框号，其位宽为 `44` 位，由物理地址右移 `12` 位得到。

![SATP](satp.png)

#### `VSATP`
- `vsatp (Virtual Supervisor Address Translation and Protection)` 是虚拟机中客体操作系统的地址转换寄存器，提供虚拟机的虚拟地址到中间物理地址（`IPA`）的转换。
- `mode`：页表模式，控制虚拟地址的转换，模式值与 `satp` 中的类似。
- `asid`：虚拟机内地址空间标识符。
- `ppn`：虚拟机页表的物理基地址。

![VSATP](vsatp.png)

#### `HGATP`
- `hgatp (Hypervisor Guest Address Translation and Protection)` 是虚拟机监控程序（`Hypervisor`）的二级地址转换寄存器，用于将虚拟机的中间物理地址（`IPA`）转换为主机物理地址（`HPA`）。
- `mode`：页表模式，如 `SV39x4` 或 `SV48x4`，用于虚拟机的二级地址转换。
  - `0`: `Bare` 模式，不进行二级地址转换。
  - `8`: `SV39x4` 模式，即 `39` 位虚拟地址空间，允许四倍页表扩展。
  - `9`: `SV48x4` 模式，即 `48` 位虚拟地址空间，允许四倍页表扩展。
- `vmid`：虚拟机标识符，区分不同虚拟机。
- `ppn`：二级页表的物理基地址。

![HGATP](hgatp.png)

`satp` 管理主机地址空间的虚拟地址到物理地址的转换，`vsatp` 用于虚拟机中的虚拟地址到中间物理地址（`IPA`）的转换，而 `hgatp` 则负责虚拟机二级地址转换，将 `IPA` 转换为主机物理地址。

#### `PRIV`
- **mxr** : `Bool()`  
  机器可执行只读（MXR）位。控制在用户模式下是否允许执行某些在机器层面被标记为只读的页面。

- **sum** : `Bool()`  
  特权模式可访问用户（SUM）位。控制特权模式下对用户模式地址的访问权限。

- **vmxr** : `Bool()`  
  虚拟机器可执行只读（`VMXR`）位。控制虚拟机内的用户是否可以执行只读页面。

- **vsum** : `Bool()`  
  虚拟特权模式可访问用户（`VSUM`）位。控制虚拟化环境中特权模式对用户模式地址的访问权限。

- **virt** : `Bool()`  
  虚拟化状态位。指示当前系统是否处于虚拟化模式。

- **spvp** : `UInt(1.W)`  
  超级特权虚拟模式（`SPVP`）。指示当前是否处于虚拟化环境中的超级特权模式。

- **imode** : `UInt(2.W)`  
  指示当前（`ITLB`）指令的处理模式：
  - `0x3` : **ModeM**（机器模式）
  - `0x2` : **ModeH**（虚拟机监控程序模式，已删除）
  - `0x1` : **ModeS**（特权模式）
  - `0x0` : **ModeU**（用户模式）

- **dmode** : `UInt(2.W)`  
  指示当前（`DTLB`）数据的处理模式。

#### `changed`
- 用于标志对应 `CSR` 中的信息是否更改，一旦 `Mode` 或 `Asid`（`Vmid`）更改则必须同步将 `changed` 置 `1`，`TLB` 在检测到 `changed` 为 `1` 时将会执行刷新操作，刷新掉旧的 `Asid`（`Vmid`）的映射。

#### base_connect()
```scala
def base_connect(sfence: SfenceBundle, csr: TlbCsrBundle): Unit = {
	this.sfence <> sfence
	this.csr <> csr
}

// overwrite satp. write satp will cause flushpipe but csr.priv won't
// satp will be delayed several cycles from writing, but csr.priv won't
// so inside mmu, these two signals should be divided
def base_connect(sfence: SfenceBundle, csr: TlbCsrBundle, satp: TlbSatpBundle) = {
	this.sfence <> sfence
	this.csr <> csr
	this.csr.satp := satp
}
```

## sfence

```scala
val sfence = Input(new SfenceBundle)
```

`sfence`：用于传入 `SfenceBundle`，执行 `SFENCE` 指令刷新 `TLB` 缓存。

```scala
class SfenceBundle(implicit p: Parameters) extends XSBundle {
    val valid = Bool()
    val bits = new Bundle {
        val rs1 = Bool()
        val rs2 = Bool()
        val addr = UInt(VAddrBits.W)
        val id = UInt((AsidLength).W) // asid or vmid
        val flushPipe = Bool()
        val hv = Bool()
        val hg = Bool()
    }
    
    override def toPrintable: Printable = {
        p"valid:0x${Hexadecimal(valid)} rs1:${bits.rs1} rs2:${bits.rs2} addr:${Hexadecimal(bits.addr)}, flushPipe:${bits.flushPipe}"
    }
}
```

#### `valid`
- 有效标志信号，指示 `SFENCE.VMA` 操作的请求是否有效。如果该信号为高（`1`），表示当前的 `SFENCE.VMA` 操作需要执行；如果为低（`0`），则没有操作需要执行。

#### `rs1`
- 表示需要使用 `SFENCE.VMA` 指令中的 `rs1` 寄存器的值，这个值通过信号 `addr` 传入，标记了需要刷新的虚拟地址。
- 当 `rs1` 为非零时，表示 `SFENCE.VMA` 只针对该虚拟地址所对应的页表条目进行刷新操作；如果 `rs1` 为零，则表示刷新所有虚拟地址的映射。

#### `rs2`
- 表示需要使用 `SFENCE.VMA` 指令中的 `rs2` 寄存器的值，其中存储着需要刷新的 `ASID`，通过信号 `id` 传入。
- 当 `rs2` 为非零时，表示 `SFENCE.VMA` 只对指定的 `ASID` 进行刷新操作；如果 `rs2` 为零，则表示刷新所有地址空间的映射。这个信号主要用于区分不同进程的地址空间。

#### `addr`
- 表示 `SFENCE.VMA` 指令中 `rs1` 对应的虚拟地址（可能是部分地址）。该信号提供了具体的虚拟地址信息，当 `rs1` 为非零时，`TLB` 将使用该地址作为参考，刷新与该地址对应的页表条目。它用于精细控制哪些地址映射需要被刷新。
- 信号的位宽为 `VAddrBits`，即虚拟地址的位宽，可见于 \ref{subsec:consts}，大小被定义为 `50`，其中事实上使用的只有 `addr[47:12]`，也即四级页表的四级索引部分，用于找到对应虚拟地址的页表项。

#### `id`
- 表示 `SFENCE.VMA` 操作涉及的地址空间标识符（`ASID`）。用于指定某个具体的 `ASID`。它允许在多地址空间的场景下（例如多个进程共享一个处理器），只刷新某个特定进程的地址映射。
- 信号位宽为 `AsidLength`，可见于 \ref{subsec:consts}，大小为 `16`，意味着同时支持 $2^{16}$ 个虚拟地址空间。

#### `flushPipe`
- 控制是否需要 **清空流水线**。`SFENCE.VMA` 操作不仅可能涉及刷新 `TLB`，还可能需要清空流水线以确保所有未完成的指令（可能依赖旧的地址映射）不会继续使用过时的页表映射。这个信号为高时，表示需要清空流水线。

#### `hv`
- 表示当前指令是否为 `HFENCE.VVMA`。

#### `hg`
- 表示当前指令是否为 `HFENCE.GVMA`。

## 外部传入参数

#### 参数说明

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

## VAddrBits

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

## AsidLength

```scala
def AsidLength = coreParams.AsidLength  // Parameters.scala: line 619
AsidLength: Int = 16                    // Parameters.scala: line 79
```

- **ASID 位宽**：16 位
- **作用**：标识地址空间，防止进程/虚拟机虚拟地址冲突
- **支持规模**：
  - 最大 `65536` 个并发进程（16 位）
  - 虚拟机通过 `vmid` 标识（14 位，支持 `16384` 个虚拟机，符合手册要求）
