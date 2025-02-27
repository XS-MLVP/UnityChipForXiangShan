module FtqRedirectMem_top;

  logic  clock;
  logic  reset;
  logic  io_ren_0;
  logic  io_ren_1;
  logic  io_ren_2;
  logic [5:0] io_raddr_0;
  logic [5:0] io_raddr_1;
  logic [5:0] io_raddr_2;
  logic  io_rdata_0_histPtr_flag;
  logic [7:0] io_rdata_0_histPtr_value;
  logic [3:0] io_rdata_0_ssp;
  logic [2:0] io_rdata_0_sctr;
  logic  io_rdata_0_TOSW_flag;
  logic [4:0] io_rdata_0_TOSW_value;
  logic  io_rdata_0_TOSR_flag;
  logic [4:0] io_rdata_0_TOSR_value;
  logic  io_rdata_0_NOS_flag;
  logic [4:0] io_rdata_0_NOS_value;
  logic [49:0] io_rdata_0_topAddr;
  logic  io_rdata_1_histPtr_flag;
  logic [7:0] io_rdata_1_histPtr_value;
  logic [3:0] io_rdata_1_ssp;
  logic [2:0] io_rdata_1_sctr;
  logic  io_rdata_1_TOSW_flag;
  logic [4:0] io_rdata_1_TOSW_value;
  logic  io_rdata_1_TOSR_flag;
  logic [4:0] io_rdata_1_TOSR_value;
  logic  io_rdata_1_NOS_flag;
  logic [4:0] io_rdata_1_NOS_value;
  logic [7:0] io_rdata_2_histPtr_value;
  logic  io_wen_0;
  logic [5:0] io_waddr_0;
  logic  io_wdata_0_histPtr_flag;
  logic [7:0] io_wdata_0_histPtr_value;
  logic [3:0] io_wdata_0_ssp;
  logic [2:0] io_wdata_0_sctr;
  logic  io_wdata_0_TOSW_flag;
  logic [4:0] io_wdata_0_TOSW_value;
  logic  io_wdata_0_TOSR_flag;
  logic [4:0] io_wdata_0_TOSR_value;
  logic  io_wdata_0_NOS_flag;
  logic [4:0] io_wdata_0_NOS_value;
  logic [49:0] io_wdata_0_topAddr;


 SyncDataModuleTemplate__64entry SyncDataModuleTemplate__64entry(
    .clock(clock),
    .reset(reset),
    .io_ren_0(io_ren_0),
    .io_ren_1(io_ren_1),
    .io_ren_2(io_ren_2),
    .io_raddr_0(io_raddr_0),
    .io_raddr_1(io_raddr_1),
    .io_raddr_2(io_raddr_2),
    .io_rdata_0_histPtr_flag(io_rdata_0_histPtr_flag),
    .io_rdata_0_histPtr_value(io_rdata_0_histPtr_value),
    .io_rdata_0_ssp(io_rdata_0_ssp),
    .io_rdata_0_sctr(io_rdata_0_sctr),
    .io_rdata_0_TOSW_flag(io_rdata_0_TOSW_flag),
    .io_rdata_0_TOSW_value(io_rdata_0_TOSW_value),
    .io_rdata_0_TOSR_flag(io_rdata_0_TOSR_flag),
    .io_rdata_0_TOSR_value(io_rdata_0_TOSR_value),
    .io_rdata_0_NOS_flag(io_rdata_0_NOS_flag),
    .io_rdata_0_NOS_value(io_rdata_0_NOS_value),
    .io_rdata_0_topAddr(io_rdata_0_topAddr),
    .io_rdata_1_histPtr_flag(io_rdata_1_histPtr_flag),
    .io_rdata_1_histPtr_value(io_rdata_1_histPtr_value),
    .io_rdata_1_ssp(io_rdata_1_ssp),
    .io_rdata_1_sctr(io_rdata_1_sctr),
    .io_rdata_1_TOSW_flag(io_rdata_1_TOSW_flag),
    .io_rdata_1_TOSW_value(io_rdata_1_TOSW_value),
    .io_rdata_1_TOSR_flag(io_rdata_1_TOSR_flag),
    .io_rdata_1_TOSR_value(io_rdata_1_TOSR_value),
    .io_rdata_1_NOS_flag(io_rdata_1_NOS_flag),
    .io_rdata_1_NOS_value(io_rdata_1_NOS_value),
    .io_rdata_2_histPtr_value(io_rdata_2_histPtr_value),
    .io_wen_0(io_wen_0),
    .io_waddr_0(io_waddr_0),
    .io_wdata_0_histPtr_flag(io_wdata_0_histPtr_flag),
    .io_wdata_0_histPtr_value(io_wdata_0_histPtr_value),
    .io_wdata_0_ssp(io_wdata_0_ssp),
    .io_wdata_0_sctr(io_wdata_0_sctr),
    .io_wdata_0_TOSW_flag(io_wdata_0_TOSW_flag),
    .io_wdata_0_TOSW_value(io_wdata_0_TOSW_value),
    .io_wdata_0_TOSR_flag(io_wdata_0_TOSR_flag),
    .io_wdata_0_TOSR_value(io_wdata_0_TOSR_value),
    .io_wdata_0_NOS_flag(io_wdata_0_NOS_flag),
    .io_wdata_0_NOS_value(io_wdata_0_NOS_value),
    .io_wdata_0_topAddr(io_wdata_0_topAddr)
 );


  export "DPI-C" function get_clockxxPfBDHOX2wiz;
  export "DPI-C" function set_clockxxPfBDHOX2wiz;
  export "DPI-C" function get_resetxxPfBDHOX2wiz;
  export "DPI-C" function set_resetxxPfBDHOX2wiz;
  export "DPI-C" function get_io_ren_0xxPfBDHOX2wiz;
  export "DPI-C" function set_io_ren_0xxPfBDHOX2wiz;
  export "DPI-C" function get_io_ren_1xxPfBDHOX2wiz;
  export "DPI-C" function set_io_ren_1xxPfBDHOX2wiz;
  export "DPI-C" function get_io_ren_2xxPfBDHOX2wiz;
  export "DPI-C" function set_io_ren_2xxPfBDHOX2wiz;
  export "DPI-C" function get_io_raddr_0xxPfBDHOX2wiz;
  export "DPI-C" function set_io_raddr_0xxPfBDHOX2wiz;
  export "DPI-C" function get_io_raddr_1xxPfBDHOX2wiz;
  export "DPI-C" function set_io_raddr_1xxPfBDHOX2wiz;
  export "DPI-C" function get_io_raddr_2xxPfBDHOX2wiz;
  export "DPI-C" function set_io_raddr_2xxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_histPtr_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_histPtr_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_sspxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_sctrxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_TOSW_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_TOSW_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_TOSR_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_TOSR_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_NOS_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_NOS_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_0_topAddrxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_histPtr_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_histPtr_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_sspxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_sctrxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_TOSW_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_TOSW_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_TOSR_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_TOSR_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_NOS_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_1_NOS_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_rdata_2_histPtr_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_wen_0xxPfBDHOX2wiz;
  export "DPI-C" function set_io_wen_0xxPfBDHOX2wiz;
  export "DPI-C" function get_io_waddr_0xxPfBDHOX2wiz;
  export "DPI-C" function set_io_waddr_0xxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_histPtr_flagxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_histPtr_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_histPtr_valuexxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_histPtr_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_sspxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_sspxxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_sctrxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_sctrxxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_TOSW_flagxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_TOSW_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_TOSW_valuexxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_TOSW_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_TOSR_flagxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_TOSR_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_TOSR_valuexxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_TOSR_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_NOS_flagxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_NOS_flagxxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_NOS_valuexxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_NOS_valuexxPfBDHOX2wiz;
  export "DPI-C" function get_io_wdata_0_topAddrxxPfBDHOX2wiz;
  export "DPI-C" function set_io_wdata_0_topAddrxxPfBDHOX2wiz;


  function void get_clockxxPfBDHOX2wiz;
    output logic  value;
    value=clock;
  endfunction

  function void set_clockxxPfBDHOX2wiz;
    input logic  value;
    clock=value;
  endfunction

  function void get_resetxxPfBDHOX2wiz;
    output logic  value;
    value=reset;
  endfunction

  function void set_resetxxPfBDHOX2wiz;
    input logic  value;
    reset=value;
  endfunction

  function void get_io_ren_0xxPfBDHOX2wiz;
    output logic  value;
    value=io_ren_0;
  endfunction

  function void set_io_ren_0xxPfBDHOX2wiz;
    input logic  value;
    io_ren_0=value;
  endfunction

  function void get_io_ren_1xxPfBDHOX2wiz;
    output logic  value;
    value=io_ren_1;
  endfunction

  function void set_io_ren_1xxPfBDHOX2wiz;
    input logic  value;
    io_ren_1=value;
  endfunction

  function void get_io_ren_2xxPfBDHOX2wiz;
    output logic  value;
    value=io_ren_2;
  endfunction

  function void set_io_ren_2xxPfBDHOX2wiz;
    input logic  value;
    io_ren_2=value;
  endfunction

  function void get_io_raddr_0xxPfBDHOX2wiz;
    output logic [5:0] value;
    value=io_raddr_0;
  endfunction

  function void set_io_raddr_0xxPfBDHOX2wiz;
    input logic [5:0] value;
    io_raddr_0=value;
  endfunction

  function void get_io_raddr_1xxPfBDHOX2wiz;
    output logic [5:0] value;
    value=io_raddr_1;
  endfunction

  function void set_io_raddr_1xxPfBDHOX2wiz;
    input logic [5:0] value;
    io_raddr_1=value;
  endfunction

  function void get_io_raddr_2xxPfBDHOX2wiz;
    output logic [5:0] value;
    value=io_raddr_2;
  endfunction

  function void set_io_raddr_2xxPfBDHOX2wiz;
    input logic [5:0] value;
    io_raddr_2=value;
  endfunction

  function void get_io_rdata_0_histPtr_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_0_histPtr_flag;
  endfunction

  function void get_io_rdata_0_histPtr_valuexxPfBDHOX2wiz;
    output logic [7:0] value;
    value=io_rdata_0_histPtr_value;
  endfunction

  function void get_io_rdata_0_sspxxPfBDHOX2wiz;
    output logic [3:0] value;
    value=io_rdata_0_ssp;
  endfunction

  function void get_io_rdata_0_sctrxxPfBDHOX2wiz;
    output logic [2:0] value;
    value=io_rdata_0_sctr;
  endfunction

  function void get_io_rdata_0_TOSW_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_0_TOSW_flag;
  endfunction

  function void get_io_rdata_0_TOSW_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_rdata_0_TOSW_value;
  endfunction

  function void get_io_rdata_0_TOSR_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_0_TOSR_flag;
  endfunction

  function void get_io_rdata_0_TOSR_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_rdata_0_TOSR_value;
  endfunction

  function void get_io_rdata_0_NOS_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_0_NOS_flag;
  endfunction

  function void get_io_rdata_0_NOS_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_rdata_0_NOS_value;
  endfunction

  function void get_io_rdata_0_topAddrxxPfBDHOX2wiz;
    output logic [49:0] value;
    value=io_rdata_0_topAddr;
  endfunction

  function void get_io_rdata_1_histPtr_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_1_histPtr_flag;
  endfunction

  function void get_io_rdata_1_histPtr_valuexxPfBDHOX2wiz;
    output logic [7:0] value;
    value=io_rdata_1_histPtr_value;
  endfunction

  function void get_io_rdata_1_sspxxPfBDHOX2wiz;
    output logic [3:0] value;
    value=io_rdata_1_ssp;
  endfunction

  function void get_io_rdata_1_sctrxxPfBDHOX2wiz;
    output logic [2:0] value;
    value=io_rdata_1_sctr;
  endfunction

  function void get_io_rdata_1_TOSW_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_1_TOSW_flag;
  endfunction

  function void get_io_rdata_1_TOSW_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_rdata_1_TOSW_value;
  endfunction

  function void get_io_rdata_1_TOSR_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_1_TOSR_flag;
  endfunction

  function void get_io_rdata_1_TOSR_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_rdata_1_TOSR_value;
  endfunction

  function void get_io_rdata_1_NOS_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_rdata_1_NOS_flag;
  endfunction

  function void get_io_rdata_1_NOS_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_rdata_1_NOS_value;
  endfunction

  function void get_io_rdata_2_histPtr_valuexxPfBDHOX2wiz;
    output logic [7:0] value;
    value=io_rdata_2_histPtr_value;
  endfunction

  function void get_io_wen_0xxPfBDHOX2wiz;
    output logic  value;
    value=io_wen_0;
  endfunction

  function void set_io_wen_0xxPfBDHOX2wiz;
    input logic  value;
    io_wen_0=value;
  endfunction

  function void get_io_waddr_0xxPfBDHOX2wiz;
    output logic [5:0] value;
    value=io_waddr_0;
  endfunction

  function void set_io_waddr_0xxPfBDHOX2wiz;
    input logic [5:0] value;
    io_waddr_0=value;
  endfunction

  function void get_io_wdata_0_histPtr_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_wdata_0_histPtr_flag;
  endfunction

  function void set_io_wdata_0_histPtr_flagxxPfBDHOX2wiz;
    input logic  value;
    io_wdata_0_histPtr_flag=value;
  endfunction

  function void get_io_wdata_0_histPtr_valuexxPfBDHOX2wiz;
    output logic [7:0] value;
    value=io_wdata_0_histPtr_value;
  endfunction

  function void set_io_wdata_0_histPtr_valuexxPfBDHOX2wiz;
    input logic [7:0] value;
    io_wdata_0_histPtr_value=value;
  endfunction

  function void get_io_wdata_0_sspxxPfBDHOX2wiz;
    output logic [3:0] value;
    value=io_wdata_0_ssp;
  endfunction

  function void set_io_wdata_0_sspxxPfBDHOX2wiz;
    input logic [3:0] value;
    io_wdata_0_ssp=value;
  endfunction

  function void get_io_wdata_0_sctrxxPfBDHOX2wiz;
    output logic [2:0] value;
    value=io_wdata_0_sctr;
  endfunction

  function void set_io_wdata_0_sctrxxPfBDHOX2wiz;
    input logic [2:0] value;
    io_wdata_0_sctr=value;
  endfunction

  function void get_io_wdata_0_TOSW_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_wdata_0_TOSW_flag;
  endfunction

  function void set_io_wdata_0_TOSW_flagxxPfBDHOX2wiz;
    input logic  value;
    io_wdata_0_TOSW_flag=value;
  endfunction

  function void get_io_wdata_0_TOSW_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_wdata_0_TOSW_value;
  endfunction

  function void set_io_wdata_0_TOSW_valuexxPfBDHOX2wiz;
    input logic [4:0] value;
    io_wdata_0_TOSW_value=value;
  endfunction

  function void get_io_wdata_0_TOSR_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_wdata_0_TOSR_flag;
  endfunction

  function void set_io_wdata_0_TOSR_flagxxPfBDHOX2wiz;
    input logic  value;
    io_wdata_0_TOSR_flag=value;
  endfunction

  function void get_io_wdata_0_TOSR_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_wdata_0_TOSR_value;
  endfunction

  function void set_io_wdata_0_TOSR_valuexxPfBDHOX2wiz;
    input logic [4:0] value;
    io_wdata_0_TOSR_value=value;
  endfunction

  function void get_io_wdata_0_NOS_flagxxPfBDHOX2wiz;
    output logic  value;
    value=io_wdata_0_NOS_flag;
  endfunction

  function void set_io_wdata_0_NOS_flagxxPfBDHOX2wiz;
    input logic  value;
    io_wdata_0_NOS_flag=value;
  endfunction

  function void get_io_wdata_0_NOS_valuexxPfBDHOX2wiz;
    output logic [4:0] value;
    value=io_wdata_0_NOS_value;
  endfunction

  function void set_io_wdata_0_NOS_valuexxPfBDHOX2wiz;
    input logic [4:0] value;
    io_wdata_0_NOS_value=value;
  endfunction

  function void get_io_wdata_0_topAddrxxPfBDHOX2wiz;
    output logic [49:0] value;
    value=io_wdata_0_topAddr;
  endfunction

  function void set_io_wdata_0_topAddrxxPfBDHOX2wiz;
    input logic [49:0] value;
    io_wdata_0_topAddr=value;
  endfunction



  initial begin
    $dumpfile("FtqRedirectMem.fst");
    $dumpvars(0, FtqRedirectMem_top);
  end

  export "DPI-C" function finish_PfBDHOX2wiz;
  function void finish_PfBDHOX2wiz;
    $finish;
  endfunction


endmodule
