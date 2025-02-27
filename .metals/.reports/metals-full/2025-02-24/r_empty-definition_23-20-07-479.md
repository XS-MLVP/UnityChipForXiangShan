error id: `<none>`.
file://<WORKSPACE>/rtl/openxiangshan-kmh-ca892e73-25010301/rtl/AXI.scala
empty definition using pc, found symbol in pc: `<none>`.
empty definition using semanticdb
|empty definition using fallback
non-local guesses:
	 -chisel3/Int#
	 -chisel3/util/Int#
	 -Int#
	 -scala/Predef.Int#

Document text:

```scala
package axi

import chisel3._
import chisel3.util._

class AXIInterface(val addrWidth: Int, val dataWidth: Int) extends Bundle {
  // Read Address Channel
  val arid = Output(UInt(4.W))
  val araddr = Output(UInt(addrWidth.W))
  val arlen = Output(UInt(8.W)) 
  val arsize = Output(UInt(3.W))
  val arburst = Output(UInt(2.W))
  val arlock = Output(Bool())
  val arcache = Output(UInt(4.W))
  val arprot = Output(UInt(3.W))
  val arvalid = Output(Bool())
  val arready = Input(Bool())

  // Read Data Channel
  val rid = Input(UInt(4.W))
  val rdata = Input(UInt(dataWidth.W))
  val rresp = Input(UInt(2.W))
  val rlast = Input(Bool())
  val rvalid = Input(Bool())
  val rready = Output(Bool())

  // Write Address Channel  
  val awid = Output(UInt(4.W))
  val awaddr = Output(UInt(addrWidth.W))
  val awlen = Output(UInt(8.W))
  val awsize = Output(UInt(3.W))
  val awburst = Output(UInt(2.W))
  val awlock = Output(Bool())
  val awcache = Output(UInt(4.W))
  val awprot = Output(UInt(3.W))
  val awvalid = Output(Bool())
  val awready = Input(Bool())

  // Write Data Channel
  val wid = Output(UInt(4.W))
  val wdata = Output(UInt(dataWidth.W))
  val wstrb = Output(UInt((dataWidth/8).W))
  val wlast = Output(Bool())
  val wvalid = Output(Bool())
  val wready = Input(Bool())

  // Write Response Channel
  val bid = Input(UInt(4.W))
  val bresp = Input(UInt(2.W))
  val bvalid = Input(Bool())
  val bready = Output(Bool())
}

class AXI(val addrWidth: Int = 32, val dataWidth: Int = 32) extends Module {
  val io = IO(new AXIInterface(addrWidth, dataWidth))

  // Instantiate channel modules
  val readAddr = Module(new ReadAddrChannel(addrWidth))
  val readData = Module(new ReadDataChannel(dataWidth))
  val writeAddr = Module(new WriteAddrChannel(addrWidth))
  val writeData = Module(new WriteDataChannel(dataWidth))
  val writeResp = Module(new WriteRespChannel())

  // Connect channel modules
  io << readAddr.io
  io << readData.io
  io << writeAddr.io
  io << writeData.io
  io << writeResp.io
}

// Channel modules to be implemented
class ReadAddrChannel(val addrWidth: Int) extends Module {
  val io = IO(new Bundle {
    val axi = new ReadAddrInterface(addrWidth)
  })
  // Implementation to be added
}

class ReadDataChannel(val dataWidth: Int) extends Module {
  val io = IO(new Bundle {
    val axi = new ReadDataInterface(dataWidth)
  })
  // Implementation to be added
}

class WriteAddrChannel(val addrWidth: Int) extends Module {
  val io = IO(new Bundle {
    val axi = new WriteAddrInterface(addrWidth)
  })
  // Implementation to be added
}

class WriteDataChannel(val dataWidth: Int) extends Module {
  val io = IO(new Bundle {
    val axi = new WriteDataInterface(dataWidth)
  })
  // Implementation to be added
}

class WriteRespChannel() extends Module {
  val io = IO(new Bundle {
    val axi = new WriteRespInterface()
  })
  // Implementation to be added
}

```

#### Short summary: 

empty definition using pc, found symbol in pc: `<none>`.