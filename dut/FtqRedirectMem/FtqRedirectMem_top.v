module FtqRedirectMem_top;

  wire  clock;
  wire  reset;
  wire  io_ren_0;
  wire  io_ren_1;
  wire  io_ren_2;
  wire [5:0] io_raddr_0;
  wire [5:0] io_raddr_1;
  wire [5:0] io_raddr_2;
  wire  io_rdata_0_histPtr_flag;
  wire [7:0] io_rdata_0_histPtr_value;
  wire [3:0] io_rdata_0_ssp;
  wire [2:0] io_rdata_0_sctr;
  wire  io_rdata_0_TOSW_flag;
  wire [4:0] io_rdata_0_TOSW_value;
  wire  io_rdata_0_TOSR_flag;
  wire [4:0] io_rdata_0_TOSR_value;
  wire  io_rdata_0_NOS_flag;
  wire [4:0] io_rdata_0_NOS_value;
  wire [49:0] io_rdata_0_topAddr;
  wire  io_rdata_1_histPtr_flag;
  wire [7:0] io_rdata_1_histPtr_value;
  wire [3:0] io_rdata_1_ssp;
  wire [2:0] io_rdata_1_sctr;
  wire  io_rdata_1_TOSW_flag;
  wire [4:0] io_rdata_1_TOSW_value;
  wire  io_rdata_1_TOSR_flag;
  wire [4:0] io_rdata_1_TOSR_value;
  wire  io_rdata_1_NOS_flag;
  wire [4:0] io_rdata_1_NOS_value;
  wire [7:0] io_rdata_2_histPtr_value;
  wire  io_wen_0;
  wire [5:0] io_waddr_0;
  wire  io_wdata_0_histPtr_flag;
  wire [7:0] io_wdata_0_histPtr_value;
  wire [3:0] io_wdata_0_ssp;
  wire [2:0] io_wdata_0_sctr;
  wire  io_wdata_0_TOSW_flag;
  wire [4:0] io_wdata_0_TOSW_value;
  wire  io_wdata_0_TOSR_flag;
  wire [4:0] io_wdata_0_TOSR_value;
  wire  io_wdata_0_NOS_flag;
  wire [4:0] io_wdata_0_NOS_value;
  wire [49:0] io_wdata_0_topAddr;


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


endmodule
