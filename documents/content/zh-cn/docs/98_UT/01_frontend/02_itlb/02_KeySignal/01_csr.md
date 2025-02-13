---
title: 相关 CSR 寄存器
linkTitle: CSR
weight: 12
---

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

### base_connect()
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