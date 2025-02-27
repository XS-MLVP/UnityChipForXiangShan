module FtqPdMem_top;

  logic  clock;
  logic  reset;
  logic  io_ren_0;
  logic  io_ren_1;
  logic [5:0] io_raddr_0;
  logic [5:0] io_raddr_1;
  logic  io_rdata_0_brMask_0;
  logic  io_rdata_0_brMask_1;
  logic  io_rdata_0_brMask_2;
  logic  io_rdata_0_brMask_3;
  logic  io_rdata_0_brMask_4;
  logic  io_rdata_0_brMask_5;
  logic  io_rdata_0_brMask_6;
  logic  io_rdata_0_brMask_7;
  logic  io_rdata_0_brMask_8;
  logic  io_rdata_0_brMask_9;
  logic  io_rdata_0_brMask_10;
  logic  io_rdata_0_brMask_11;
  logic  io_rdata_0_brMask_12;
  logic  io_rdata_0_brMask_13;
  logic  io_rdata_0_brMask_14;
  logic  io_rdata_0_brMask_15;
  logic  io_rdata_0_jmpInfo_valid;
  logic  io_rdata_0_jmpInfo_bits_0;
  logic  io_rdata_0_jmpInfo_bits_1;
  logic  io_rdata_0_jmpInfo_bits_2;
  logic [3:0] io_rdata_0_jmpOffset;
  logic  io_rdata_0_rvcMask_0;
  logic  io_rdata_0_rvcMask_1;
  logic  io_rdata_0_rvcMask_2;
  logic  io_rdata_0_rvcMask_3;
  logic  io_rdata_0_rvcMask_4;
  logic  io_rdata_0_rvcMask_5;
  logic  io_rdata_0_rvcMask_6;
  logic  io_rdata_0_rvcMask_7;
  logic  io_rdata_0_rvcMask_8;
  logic  io_rdata_0_rvcMask_9;
  logic  io_rdata_0_rvcMask_10;
  logic  io_rdata_0_rvcMask_11;
  logic  io_rdata_0_rvcMask_12;
  logic  io_rdata_0_rvcMask_13;
  logic  io_rdata_0_rvcMask_14;
  logic  io_rdata_0_rvcMask_15;
  logic  io_rdata_1_brMask_0;
  logic  io_rdata_1_brMask_1;
  logic  io_rdata_1_brMask_2;
  logic  io_rdata_1_brMask_3;
  logic  io_rdata_1_brMask_4;
  logic  io_rdata_1_brMask_5;
  logic  io_rdata_1_brMask_6;
  logic  io_rdata_1_brMask_7;
  logic  io_rdata_1_brMask_8;
  logic  io_rdata_1_brMask_9;
  logic  io_rdata_1_brMask_10;
  logic  io_rdata_1_brMask_11;
  logic  io_rdata_1_brMask_12;
  logic  io_rdata_1_brMask_13;
  logic  io_rdata_1_brMask_14;
  logic  io_rdata_1_brMask_15;
  logic  io_rdata_1_jmpInfo_valid;
  logic  io_rdata_1_jmpInfo_bits_0;
  logic  io_rdata_1_jmpInfo_bits_1;
  logic  io_rdata_1_jmpInfo_bits_2;
  logic [3:0] io_rdata_1_jmpOffset;
  logic [49:0] io_rdata_1_jalTarget;
  logic  io_rdata_1_rvcMask_0;
  logic  io_rdata_1_rvcMask_1;
  logic  io_rdata_1_rvcMask_2;
  logic  io_rdata_1_rvcMask_3;
  logic  io_rdata_1_rvcMask_4;
  logic  io_rdata_1_rvcMask_5;
  logic  io_rdata_1_rvcMask_6;
  logic  io_rdata_1_rvcMask_7;
  logic  io_rdata_1_rvcMask_8;
  logic  io_rdata_1_rvcMask_9;
  logic  io_rdata_1_rvcMask_10;
  logic  io_rdata_1_rvcMask_11;
  logic  io_rdata_1_rvcMask_12;
  logic  io_rdata_1_rvcMask_13;
  logic  io_rdata_1_rvcMask_14;
  logic  io_rdata_1_rvcMask_15;
  logic  io_wen_0;
  logic [5:0] io_waddr_0;
  logic  io_wdata_0_brMask_0;
  logic  io_wdata_0_brMask_1;
  logic  io_wdata_0_brMask_2;
  logic  io_wdata_0_brMask_3;
  logic  io_wdata_0_brMask_4;
  logic  io_wdata_0_brMask_5;
  logic  io_wdata_0_brMask_6;
  logic  io_wdata_0_brMask_7;
  logic  io_wdata_0_brMask_8;
  logic  io_wdata_0_brMask_9;
  logic  io_wdata_0_brMask_10;
  logic  io_wdata_0_brMask_11;
  logic  io_wdata_0_brMask_12;
  logic  io_wdata_0_brMask_13;
  logic  io_wdata_0_brMask_14;
  logic  io_wdata_0_brMask_15;
  logic  io_wdata_0_jmpInfo_valid;
  logic  io_wdata_0_jmpInfo_bits_0;
  logic  io_wdata_0_jmpInfo_bits_1;
  logic  io_wdata_0_jmpInfo_bits_2;
  logic [3:0] io_wdata_0_jmpOffset;
  logic [49:0] io_wdata_0_jalTarget;
  logic  io_wdata_0_rvcMask_0;
  logic  io_wdata_0_rvcMask_1;
  logic  io_wdata_0_rvcMask_2;
  logic  io_wdata_0_rvcMask_3;
  logic  io_wdata_0_rvcMask_4;
  logic  io_wdata_0_rvcMask_5;
  logic  io_wdata_0_rvcMask_6;
  logic  io_wdata_0_rvcMask_7;
  logic  io_wdata_0_rvcMask_8;
  logic  io_wdata_0_rvcMask_9;
  logic  io_wdata_0_rvcMask_10;
  logic  io_wdata_0_rvcMask_11;
  logic  io_wdata_0_rvcMask_12;
  logic  io_wdata_0_rvcMask_13;
  logic  io_wdata_0_rvcMask_14;
  logic  io_wdata_0_rvcMask_15;


 SyncDataModuleTemplate__64entry_2 SyncDataModuleTemplate__64entry_2(
    .clock(clock),
    .reset(reset),
    .io_ren_0(io_ren_0),
    .io_ren_1(io_ren_1),
    .io_raddr_0(io_raddr_0),
    .io_raddr_1(io_raddr_1),
    .io_rdata_0_brMask_0(io_rdata_0_brMask_0),
    .io_rdata_0_brMask_1(io_rdata_0_brMask_1),
    .io_rdata_0_brMask_2(io_rdata_0_brMask_2),
    .io_rdata_0_brMask_3(io_rdata_0_brMask_3),
    .io_rdata_0_brMask_4(io_rdata_0_brMask_4),
    .io_rdata_0_brMask_5(io_rdata_0_brMask_5),
    .io_rdata_0_brMask_6(io_rdata_0_brMask_6),
    .io_rdata_0_brMask_7(io_rdata_0_brMask_7),
    .io_rdata_0_brMask_8(io_rdata_0_brMask_8),
    .io_rdata_0_brMask_9(io_rdata_0_brMask_9),
    .io_rdata_0_brMask_10(io_rdata_0_brMask_10),
    .io_rdata_0_brMask_11(io_rdata_0_brMask_11),
    .io_rdata_0_brMask_12(io_rdata_0_brMask_12),
    .io_rdata_0_brMask_13(io_rdata_0_brMask_13),
    .io_rdata_0_brMask_14(io_rdata_0_brMask_14),
    .io_rdata_0_brMask_15(io_rdata_0_brMask_15),
    .io_rdata_0_jmpInfo_valid(io_rdata_0_jmpInfo_valid),
    .io_rdata_0_jmpInfo_bits_0(io_rdata_0_jmpInfo_bits_0),
    .io_rdata_0_jmpInfo_bits_1(io_rdata_0_jmpInfo_bits_1),
    .io_rdata_0_jmpInfo_bits_2(io_rdata_0_jmpInfo_bits_2),
    .io_rdata_0_jmpOffset(io_rdata_0_jmpOffset),
    .io_rdata_0_rvcMask_0(io_rdata_0_rvcMask_0),
    .io_rdata_0_rvcMask_1(io_rdata_0_rvcMask_1),
    .io_rdata_0_rvcMask_2(io_rdata_0_rvcMask_2),
    .io_rdata_0_rvcMask_3(io_rdata_0_rvcMask_3),
    .io_rdata_0_rvcMask_4(io_rdata_0_rvcMask_4),
    .io_rdata_0_rvcMask_5(io_rdata_0_rvcMask_5),
    .io_rdata_0_rvcMask_6(io_rdata_0_rvcMask_6),
    .io_rdata_0_rvcMask_7(io_rdata_0_rvcMask_7),
    .io_rdata_0_rvcMask_8(io_rdata_0_rvcMask_8),
    .io_rdata_0_rvcMask_9(io_rdata_0_rvcMask_9),
    .io_rdata_0_rvcMask_10(io_rdata_0_rvcMask_10),
    .io_rdata_0_rvcMask_11(io_rdata_0_rvcMask_11),
    .io_rdata_0_rvcMask_12(io_rdata_0_rvcMask_12),
    .io_rdata_0_rvcMask_13(io_rdata_0_rvcMask_13),
    .io_rdata_0_rvcMask_14(io_rdata_0_rvcMask_14),
    .io_rdata_0_rvcMask_15(io_rdata_0_rvcMask_15),
    .io_rdata_1_brMask_0(io_rdata_1_brMask_0),
    .io_rdata_1_brMask_1(io_rdata_1_brMask_1),
    .io_rdata_1_brMask_2(io_rdata_1_brMask_2),
    .io_rdata_1_brMask_3(io_rdata_1_brMask_3),
    .io_rdata_1_brMask_4(io_rdata_1_brMask_4),
    .io_rdata_1_brMask_5(io_rdata_1_brMask_5),
    .io_rdata_1_brMask_6(io_rdata_1_brMask_6),
    .io_rdata_1_brMask_7(io_rdata_1_brMask_7),
    .io_rdata_1_brMask_8(io_rdata_1_brMask_8),
    .io_rdata_1_brMask_9(io_rdata_1_brMask_9),
    .io_rdata_1_brMask_10(io_rdata_1_brMask_10),
    .io_rdata_1_brMask_11(io_rdata_1_brMask_11),
    .io_rdata_1_brMask_12(io_rdata_1_brMask_12),
    .io_rdata_1_brMask_13(io_rdata_1_brMask_13),
    .io_rdata_1_brMask_14(io_rdata_1_brMask_14),
    .io_rdata_1_brMask_15(io_rdata_1_brMask_15),
    .io_rdata_1_jmpInfo_valid(io_rdata_1_jmpInfo_valid),
    .io_rdata_1_jmpInfo_bits_0(io_rdata_1_jmpInfo_bits_0),
    .io_rdata_1_jmpInfo_bits_1(io_rdata_1_jmpInfo_bits_1),
    .io_rdata_1_jmpInfo_bits_2(io_rdata_1_jmpInfo_bits_2),
    .io_rdata_1_jmpOffset(io_rdata_1_jmpOffset),
    .io_rdata_1_jalTarget(io_rdata_1_jalTarget),
    .io_rdata_1_rvcMask_0(io_rdata_1_rvcMask_0),
    .io_rdata_1_rvcMask_1(io_rdata_1_rvcMask_1),
    .io_rdata_1_rvcMask_2(io_rdata_1_rvcMask_2),
    .io_rdata_1_rvcMask_3(io_rdata_1_rvcMask_3),
    .io_rdata_1_rvcMask_4(io_rdata_1_rvcMask_4),
    .io_rdata_1_rvcMask_5(io_rdata_1_rvcMask_5),
    .io_rdata_1_rvcMask_6(io_rdata_1_rvcMask_6),
    .io_rdata_1_rvcMask_7(io_rdata_1_rvcMask_7),
    .io_rdata_1_rvcMask_8(io_rdata_1_rvcMask_8),
    .io_rdata_1_rvcMask_9(io_rdata_1_rvcMask_9),
    .io_rdata_1_rvcMask_10(io_rdata_1_rvcMask_10),
    .io_rdata_1_rvcMask_11(io_rdata_1_rvcMask_11),
    .io_rdata_1_rvcMask_12(io_rdata_1_rvcMask_12),
    .io_rdata_1_rvcMask_13(io_rdata_1_rvcMask_13),
    .io_rdata_1_rvcMask_14(io_rdata_1_rvcMask_14),
    .io_rdata_1_rvcMask_15(io_rdata_1_rvcMask_15),
    .io_wen_0(io_wen_0),
    .io_waddr_0(io_waddr_0),
    .io_wdata_0_brMask_0(io_wdata_0_brMask_0),
    .io_wdata_0_brMask_1(io_wdata_0_brMask_1),
    .io_wdata_0_brMask_2(io_wdata_0_brMask_2),
    .io_wdata_0_brMask_3(io_wdata_0_brMask_3),
    .io_wdata_0_brMask_4(io_wdata_0_brMask_4),
    .io_wdata_0_brMask_5(io_wdata_0_brMask_5),
    .io_wdata_0_brMask_6(io_wdata_0_brMask_6),
    .io_wdata_0_brMask_7(io_wdata_0_brMask_7),
    .io_wdata_0_brMask_8(io_wdata_0_brMask_8),
    .io_wdata_0_brMask_9(io_wdata_0_brMask_9),
    .io_wdata_0_brMask_10(io_wdata_0_brMask_10),
    .io_wdata_0_brMask_11(io_wdata_0_brMask_11),
    .io_wdata_0_brMask_12(io_wdata_0_brMask_12),
    .io_wdata_0_brMask_13(io_wdata_0_brMask_13),
    .io_wdata_0_brMask_14(io_wdata_0_brMask_14),
    .io_wdata_0_brMask_15(io_wdata_0_brMask_15),
    .io_wdata_0_jmpInfo_valid(io_wdata_0_jmpInfo_valid),
    .io_wdata_0_jmpInfo_bits_0(io_wdata_0_jmpInfo_bits_0),
    .io_wdata_0_jmpInfo_bits_1(io_wdata_0_jmpInfo_bits_1),
    .io_wdata_0_jmpInfo_bits_2(io_wdata_0_jmpInfo_bits_2),
    .io_wdata_0_jmpOffset(io_wdata_0_jmpOffset),
    .io_wdata_0_jalTarget(io_wdata_0_jalTarget),
    .io_wdata_0_rvcMask_0(io_wdata_0_rvcMask_0),
    .io_wdata_0_rvcMask_1(io_wdata_0_rvcMask_1),
    .io_wdata_0_rvcMask_2(io_wdata_0_rvcMask_2),
    .io_wdata_0_rvcMask_3(io_wdata_0_rvcMask_3),
    .io_wdata_0_rvcMask_4(io_wdata_0_rvcMask_4),
    .io_wdata_0_rvcMask_5(io_wdata_0_rvcMask_5),
    .io_wdata_0_rvcMask_6(io_wdata_0_rvcMask_6),
    .io_wdata_0_rvcMask_7(io_wdata_0_rvcMask_7),
    .io_wdata_0_rvcMask_8(io_wdata_0_rvcMask_8),
    .io_wdata_0_rvcMask_9(io_wdata_0_rvcMask_9),
    .io_wdata_0_rvcMask_10(io_wdata_0_rvcMask_10),
    .io_wdata_0_rvcMask_11(io_wdata_0_rvcMask_11),
    .io_wdata_0_rvcMask_12(io_wdata_0_rvcMask_12),
    .io_wdata_0_rvcMask_13(io_wdata_0_rvcMask_13),
    .io_wdata_0_rvcMask_14(io_wdata_0_rvcMask_14),
    .io_wdata_0_rvcMask_15(io_wdata_0_rvcMask_15)
 );


  export "DPI-C" function get_clockxxPfBDHPD4E6m;
  export "DPI-C" function set_clockxxPfBDHPD4E6m;
  export "DPI-C" function get_resetxxPfBDHPD4E6m;
  export "DPI-C" function set_resetxxPfBDHPD4E6m;
  export "DPI-C" function get_io_ren_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_ren_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_ren_1xxPfBDHPD4E6m;
  export "DPI-C" function set_io_ren_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_raddr_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_raddr_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_raddr_1xxPfBDHPD4E6m;
  export "DPI-C" function set_io_raddr_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_3xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_4xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_5xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_6xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_7xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_8xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_9xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_10xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_11xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_12xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_13xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_14xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_brMask_15xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_jmpInfo_validxxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_jmpInfo_bits_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_jmpInfo_bits_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_jmpInfo_bits_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_jmpOffsetxxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_3xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_4xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_5xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_6xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_7xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_8xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_9xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_10xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_11xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_12xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_13xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_14xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_0_rvcMask_15xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_3xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_4xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_5xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_6xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_7xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_8xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_9xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_10xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_11xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_12xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_13xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_14xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_brMask_15xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_jmpInfo_validxxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_jmpInfo_bits_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_jmpInfo_bits_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_jmpInfo_bits_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_jmpOffsetxxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_jalTargetxxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_3xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_4xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_5xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_6xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_7xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_8xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_9xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_10xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_11xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_12xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_13xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_14xxPfBDHPD4E6m;
  export "DPI-C" function get_io_rdata_1_rvcMask_15xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wen_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wen_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_waddr_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_waddr_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_1xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_2xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_3xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_3xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_4xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_4xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_5xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_5xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_6xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_6xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_7xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_7xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_8xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_8xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_9xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_9xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_10xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_10xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_11xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_11xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_12xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_12xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_13xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_13xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_14xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_14xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_brMask_15xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_brMask_15xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_jmpInfo_validxxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_jmpInfo_validxxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_jmpInfo_bits_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_jmpInfo_bits_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_jmpInfo_bits_1xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_jmpInfo_bits_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_jmpInfo_bits_2xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_jmpInfo_bits_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_jmpOffsetxxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_jmpOffsetxxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_jalTargetxxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_jalTargetxxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_0xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_0xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_1xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_1xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_2xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_2xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_3xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_3xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_4xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_4xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_5xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_5xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_6xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_6xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_7xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_7xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_8xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_8xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_9xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_9xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_10xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_10xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_11xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_11xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_12xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_12xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_13xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_13xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_14xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_14xxPfBDHPD4E6m;
  export "DPI-C" function get_io_wdata_0_rvcMask_15xxPfBDHPD4E6m;
  export "DPI-C" function set_io_wdata_0_rvcMask_15xxPfBDHPD4E6m;


  function void get_clockxxPfBDHPD4E6m;
    output logic  value;
    value=clock;
  endfunction

  function void set_clockxxPfBDHPD4E6m;
    input logic  value;
    clock=value;
  endfunction

  function void get_resetxxPfBDHPD4E6m;
    output logic  value;
    value=reset;
  endfunction

  function void set_resetxxPfBDHPD4E6m;
    input logic  value;
    reset=value;
  endfunction

  function void get_io_ren_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_ren_0;
  endfunction

  function void set_io_ren_0xxPfBDHPD4E6m;
    input logic  value;
    io_ren_0=value;
  endfunction

  function void get_io_ren_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_ren_1;
  endfunction

  function void set_io_ren_1xxPfBDHPD4E6m;
    input logic  value;
    io_ren_1=value;
  endfunction

  function void get_io_raddr_0xxPfBDHPD4E6m;
    output logic [5:0] value;
    value=io_raddr_0;
  endfunction

  function void set_io_raddr_0xxPfBDHPD4E6m;
    input logic [5:0] value;
    io_raddr_0=value;
  endfunction

  function void get_io_raddr_1xxPfBDHPD4E6m;
    output logic [5:0] value;
    value=io_raddr_1;
  endfunction

  function void set_io_raddr_1xxPfBDHPD4E6m;
    input logic [5:0] value;
    io_raddr_1=value;
  endfunction

  function void get_io_rdata_0_brMask_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_0;
  endfunction

  function void get_io_rdata_0_brMask_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_1;
  endfunction

  function void get_io_rdata_0_brMask_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_2;
  endfunction

  function void get_io_rdata_0_brMask_3xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_3;
  endfunction

  function void get_io_rdata_0_brMask_4xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_4;
  endfunction

  function void get_io_rdata_0_brMask_5xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_5;
  endfunction

  function void get_io_rdata_0_brMask_6xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_6;
  endfunction

  function void get_io_rdata_0_brMask_7xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_7;
  endfunction

  function void get_io_rdata_0_brMask_8xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_8;
  endfunction

  function void get_io_rdata_0_brMask_9xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_9;
  endfunction

  function void get_io_rdata_0_brMask_10xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_10;
  endfunction

  function void get_io_rdata_0_brMask_11xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_11;
  endfunction

  function void get_io_rdata_0_brMask_12xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_12;
  endfunction

  function void get_io_rdata_0_brMask_13xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_13;
  endfunction

  function void get_io_rdata_0_brMask_14xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_14;
  endfunction

  function void get_io_rdata_0_brMask_15xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_brMask_15;
  endfunction

  function void get_io_rdata_0_jmpInfo_validxxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_jmpInfo_valid;
  endfunction

  function void get_io_rdata_0_jmpInfo_bits_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_jmpInfo_bits_0;
  endfunction

  function void get_io_rdata_0_jmpInfo_bits_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_jmpInfo_bits_1;
  endfunction

  function void get_io_rdata_0_jmpInfo_bits_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_jmpInfo_bits_2;
  endfunction

  function void get_io_rdata_0_jmpOffsetxxPfBDHPD4E6m;
    output logic [3:0] value;
    value=io_rdata_0_jmpOffset;
  endfunction

  function void get_io_rdata_0_rvcMask_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_0;
  endfunction

  function void get_io_rdata_0_rvcMask_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_1;
  endfunction

  function void get_io_rdata_0_rvcMask_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_2;
  endfunction

  function void get_io_rdata_0_rvcMask_3xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_3;
  endfunction

  function void get_io_rdata_0_rvcMask_4xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_4;
  endfunction

  function void get_io_rdata_0_rvcMask_5xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_5;
  endfunction

  function void get_io_rdata_0_rvcMask_6xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_6;
  endfunction

  function void get_io_rdata_0_rvcMask_7xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_7;
  endfunction

  function void get_io_rdata_0_rvcMask_8xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_8;
  endfunction

  function void get_io_rdata_0_rvcMask_9xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_9;
  endfunction

  function void get_io_rdata_0_rvcMask_10xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_10;
  endfunction

  function void get_io_rdata_0_rvcMask_11xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_11;
  endfunction

  function void get_io_rdata_0_rvcMask_12xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_12;
  endfunction

  function void get_io_rdata_0_rvcMask_13xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_13;
  endfunction

  function void get_io_rdata_0_rvcMask_14xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_14;
  endfunction

  function void get_io_rdata_0_rvcMask_15xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_0_rvcMask_15;
  endfunction

  function void get_io_rdata_1_brMask_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_0;
  endfunction

  function void get_io_rdata_1_brMask_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_1;
  endfunction

  function void get_io_rdata_1_brMask_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_2;
  endfunction

  function void get_io_rdata_1_brMask_3xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_3;
  endfunction

  function void get_io_rdata_1_brMask_4xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_4;
  endfunction

  function void get_io_rdata_1_brMask_5xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_5;
  endfunction

  function void get_io_rdata_1_brMask_6xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_6;
  endfunction

  function void get_io_rdata_1_brMask_7xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_7;
  endfunction

  function void get_io_rdata_1_brMask_8xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_8;
  endfunction

  function void get_io_rdata_1_brMask_9xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_9;
  endfunction

  function void get_io_rdata_1_brMask_10xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_10;
  endfunction

  function void get_io_rdata_1_brMask_11xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_11;
  endfunction

  function void get_io_rdata_1_brMask_12xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_12;
  endfunction

  function void get_io_rdata_1_brMask_13xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_13;
  endfunction

  function void get_io_rdata_1_brMask_14xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_14;
  endfunction

  function void get_io_rdata_1_brMask_15xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_brMask_15;
  endfunction

  function void get_io_rdata_1_jmpInfo_validxxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_jmpInfo_valid;
  endfunction

  function void get_io_rdata_1_jmpInfo_bits_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_jmpInfo_bits_0;
  endfunction

  function void get_io_rdata_1_jmpInfo_bits_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_jmpInfo_bits_1;
  endfunction

  function void get_io_rdata_1_jmpInfo_bits_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_jmpInfo_bits_2;
  endfunction

  function void get_io_rdata_1_jmpOffsetxxPfBDHPD4E6m;
    output logic [3:0] value;
    value=io_rdata_1_jmpOffset;
  endfunction

  function void get_io_rdata_1_jalTargetxxPfBDHPD4E6m;
    output logic [49:0] value;
    value=io_rdata_1_jalTarget;
  endfunction

  function void get_io_rdata_1_rvcMask_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_0;
  endfunction

  function void get_io_rdata_1_rvcMask_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_1;
  endfunction

  function void get_io_rdata_1_rvcMask_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_2;
  endfunction

  function void get_io_rdata_1_rvcMask_3xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_3;
  endfunction

  function void get_io_rdata_1_rvcMask_4xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_4;
  endfunction

  function void get_io_rdata_1_rvcMask_5xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_5;
  endfunction

  function void get_io_rdata_1_rvcMask_6xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_6;
  endfunction

  function void get_io_rdata_1_rvcMask_7xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_7;
  endfunction

  function void get_io_rdata_1_rvcMask_8xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_8;
  endfunction

  function void get_io_rdata_1_rvcMask_9xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_9;
  endfunction

  function void get_io_rdata_1_rvcMask_10xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_10;
  endfunction

  function void get_io_rdata_1_rvcMask_11xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_11;
  endfunction

  function void get_io_rdata_1_rvcMask_12xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_12;
  endfunction

  function void get_io_rdata_1_rvcMask_13xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_13;
  endfunction

  function void get_io_rdata_1_rvcMask_14xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_14;
  endfunction

  function void get_io_rdata_1_rvcMask_15xxPfBDHPD4E6m;
    output logic  value;
    value=io_rdata_1_rvcMask_15;
  endfunction

  function void get_io_wen_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_wen_0;
  endfunction

  function void set_io_wen_0xxPfBDHPD4E6m;
    input logic  value;
    io_wen_0=value;
  endfunction

  function void get_io_waddr_0xxPfBDHPD4E6m;
    output logic [5:0] value;
    value=io_waddr_0;
  endfunction

  function void set_io_waddr_0xxPfBDHPD4E6m;
    input logic [5:0] value;
    io_waddr_0=value;
  endfunction

  function void get_io_wdata_0_brMask_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_0;
  endfunction

  function void set_io_wdata_0_brMask_0xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_0=value;
  endfunction

  function void get_io_wdata_0_brMask_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_1;
  endfunction

  function void set_io_wdata_0_brMask_1xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_1=value;
  endfunction

  function void get_io_wdata_0_brMask_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_2;
  endfunction

  function void set_io_wdata_0_brMask_2xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_2=value;
  endfunction

  function void get_io_wdata_0_brMask_3xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_3;
  endfunction

  function void set_io_wdata_0_brMask_3xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_3=value;
  endfunction

  function void get_io_wdata_0_brMask_4xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_4;
  endfunction

  function void set_io_wdata_0_brMask_4xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_4=value;
  endfunction

  function void get_io_wdata_0_brMask_5xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_5;
  endfunction

  function void set_io_wdata_0_brMask_5xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_5=value;
  endfunction

  function void get_io_wdata_0_brMask_6xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_6;
  endfunction

  function void set_io_wdata_0_brMask_6xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_6=value;
  endfunction

  function void get_io_wdata_0_brMask_7xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_7;
  endfunction

  function void set_io_wdata_0_brMask_7xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_7=value;
  endfunction

  function void get_io_wdata_0_brMask_8xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_8;
  endfunction

  function void set_io_wdata_0_brMask_8xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_8=value;
  endfunction

  function void get_io_wdata_0_brMask_9xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_9;
  endfunction

  function void set_io_wdata_0_brMask_9xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_9=value;
  endfunction

  function void get_io_wdata_0_brMask_10xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_10;
  endfunction

  function void set_io_wdata_0_brMask_10xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_10=value;
  endfunction

  function void get_io_wdata_0_brMask_11xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_11;
  endfunction

  function void set_io_wdata_0_brMask_11xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_11=value;
  endfunction

  function void get_io_wdata_0_brMask_12xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_12;
  endfunction

  function void set_io_wdata_0_brMask_12xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_12=value;
  endfunction

  function void get_io_wdata_0_brMask_13xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_13;
  endfunction

  function void set_io_wdata_0_brMask_13xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_13=value;
  endfunction

  function void get_io_wdata_0_brMask_14xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_14;
  endfunction

  function void set_io_wdata_0_brMask_14xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_14=value;
  endfunction

  function void get_io_wdata_0_brMask_15xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_brMask_15;
  endfunction

  function void set_io_wdata_0_brMask_15xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_brMask_15=value;
  endfunction

  function void get_io_wdata_0_jmpInfo_validxxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_jmpInfo_valid;
  endfunction

  function void set_io_wdata_0_jmpInfo_validxxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_jmpInfo_valid=value;
  endfunction

  function void get_io_wdata_0_jmpInfo_bits_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_jmpInfo_bits_0;
  endfunction

  function void set_io_wdata_0_jmpInfo_bits_0xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_jmpInfo_bits_0=value;
  endfunction

  function void get_io_wdata_0_jmpInfo_bits_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_jmpInfo_bits_1;
  endfunction

  function void set_io_wdata_0_jmpInfo_bits_1xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_jmpInfo_bits_1=value;
  endfunction

  function void get_io_wdata_0_jmpInfo_bits_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_jmpInfo_bits_2;
  endfunction

  function void set_io_wdata_0_jmpInfo_bits_2xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_jmpInfo_bits_2=value;
  endfunction

  function void get_io_wdata_0_jmpOffsetxxPfBDHPD4E6m;
    output logic [3:0] value;
    value=io_wdata_0_jmpOffset;
  endfunction

  function void set_io_wdata_0_jmpOffsetxxPfBDHPD4E6m;
    input logic [3:0] value;
    io_wdata_0_jmpOffset=value;
  endfunction

  function void get_io_wdata_0_jalTargetxxPfBDHPD4E6m;
    output logic [49:0] value;
    value=io_wdata_0_jalTarget;
  endfunction

  function void set_io_wdata_0_jalTargetxxPfBDHPD4E6m;
    input logic [49:0] value;
    io_wdata_0_jalTarget=value;
  endfunction

  function void get_io_wdata_0_rvcMask_0xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_0;
  endfunction

  function void set_io_wdata_0_rvcMask_0xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_0=value;
  endfunction

  function void get_io_wdata_0_rvcMask_1xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_1;
  endfunction

  function void set_io_wdata_0_rvcMask_1xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_1=value;
  endfunction

  function void get_io_wdata_0_rvcMask_2xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_2;
  endfunction

  function void set_io_wdata_0_rvcMask_2xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_2=value;
  endfunction

  function void get_io_wdata_0_rvcMask_3xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_3;
  endfunction

  function void set_io_wdata_0_rvcMask_3xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_3=value;
  endfunction

  function void get_io_wdata_0_rvcMask_4xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_4;
  endfunction

  function void set_io_wdata_0_rvcMask_4xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_4=value;
  endfunction

  function void get_io_wdata_0_rvcMask_5xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_5;
  endfunction

  function void set_io_wdata_0_rvcMask_5xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_5=value;
  endfunction

  function void get_io_wdata_0_rvcMask_6xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_6;
  endfunction

  function void set_io_wdata_0_rvcMask_6xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_6=value;
  endfunction

  function void get_io_wdata_0_rvcMask_7xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_7;
  endfunction

  function void set_io_wdata_0_rvcMask_7xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_7=value;
  endfunction

  function void get_io_wdata_0_rvcMask_8xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_8;
  endfunction

  function void set_io_wdata_0_rvcMask_8xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_8=value;
  endfunction

  function void get_io_wdata_0_rvcMask_9xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_9;
  endfunction

  function void set_io_wdata_0_rvcMask_9xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_9=value;
  endfunction

  function void get_io_wdata_0_rvcMask_10xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_10;
  endfunction

  function void set_io_wdata_0_rvcMask_10xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_10=value;
  endfunction

  function void get_io_wdata_0_rvcMask_11xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_11;
  endfunction

  function void set_io_wdata_0_rvcMask_11xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_11=value;
  endfunction

  function void get_io_wdata_0_rvcMask_12xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_12;
  endfunction

  function void set_io_wdata_0_rvcMask_12xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_12=value;
  endfunction

  function void get_io_wdata_0_rvcMask_13xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_13;
  endfunction

  function void set_io_wdata_0_rvcMask_13xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_13=value;
  endfunction

  function void get_io_wdata_0_rvcMask_14xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_14;
  endfunction

  function void set_io_wdata_0_rvcMask_14xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_14=value;
  endfunction

  function void get_io_wdata_0_rvcMask_15xxPfBDHPD4E6m;
    output logic  value;
    value=io_wdata_0_rvcMask_15;
  endfunction

  function void set_io_wdata_0_rvcMask_15xxPfBDHPD4E6m;
    input logic  value;
    io_wdata_0_rvcMask_15=value;
  endfunction



  initial begin
    $dumpfile("FtqPdMem.fst");
    $dumpvars(0, FtqPdMem_top);
  end

  export "DPI-C" function finish_PfBDHPD4E6m;
  function void finish_PfBDHPD4E6m;
    $finish;
  endfunction


endmodule
