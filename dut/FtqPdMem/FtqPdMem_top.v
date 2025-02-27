module FtqPdMem_top;

  wire  clock;
  wire  reset;
  wire  io_ren_0;
  wire  io_ren_1;
  wire [5:0] io_raddr_0;
  wire [5:0] io_raddr_1;
  wire  io_rdata_0_brMask_0;
  wire  io_rdata_0_brMask_1;
  wire  io_rdata_0_brMask_2;
  wire  io_rdata_0_brMask_3;
  wire  io_rdata_0_brMask_4;
  wire  io_rdata_0_brMask_5;
  wire  io_rdata_0_brMask_6;
  wire  io_rdata_0_brMask_7;
  wire  io_rdata_0_brMask_8;
  wire  io_rdata_0_brMask_9;
  wire  io_rdata_0_brMask_10;
  wire  io_rdata_0_brMask_11;
  wire  io_rdata_0_brMask_12;
  wire  io_rdata_0_brMask_13;
  wire  io_rdata_0_brMask_14;
  wire  io_rdata_0_brMask_15;
  wire  io_rdata_0_jmpInfo_valid;
  wire  io_rdata_0_jmpInfo_bits_0;
  wire  io_rdata_0_jmpInfo_bits_1;
  wire  io_rdata_0_jmpInfo_bits_2;
  wire [3:0] io_rdata_0_jmpOffset;
  wire  io_rdata_0_rvcMask_0;
  wire  io_rdata_0_rvcMask_1;
  wire  io_rdata_0_rvcMask_2;
  wire  io_rdata_0_rvcMask_3;
  wire  io_rdata_0_rvcMask_4;
  wire  io_rdata_0_rvcMask_5;
  wire  io_rdata_0_rvcMask_6;
  wire  io_rdata_0_rvcMask_7;
  wire  io_rdata_0_rvcMask_8;
  wire  io_rdata_0_rvcMask_9;
  wire  io_rdata_0_rvcMask_10;
  wire  io_rdata_0_rvcMask_11;
  wire  io_rdata_0_rvcMask_12;
  wire  io_rdata_0_rvcMask_13;
  wire  io_rdata_0_rvcMask_14;
  wire  io_rdata_0_rvcMask_15;
  wire  io_rdata_1_brMask_0;
  wire  io_rdata_1_brMask_1;
  wire  io_rdata_1_brMask_2;
  wire  io_rdata_1_brMask_3;
  wire  io_rdata_1_brMask_4;
  wire  io_rdata_1_brMask_5;
  wire  io_rdata_1_brMask_6;
  wire  io_rdata_1_brMask_7;
  wire  io_rdata_1_brMask_8;
  wire  io_rdata_1_brMask_9;
  wire  io_rdata_1_brMask_10;
  wire  io_rdata_1_brMask_11;
  wire  io_rdata_1_brMask_12;
  wire  io_rdata_1_brMask_13;
  wire  io_rdata_1_brMask_14;
  wire  io_rdata_1_brMask_15;
  wire  io_rdata_1_jmpInfo_valid;
  wire  io_rdata_1_jmpInfo_bits_0;
  wire  io_rdata_1_jmpInfo_bits_1;
  wire  io_rdata_1_jmpInfo_bits_2;
  wire [3:0] io_rdata_1_jmpOffset;
  wire [49:0] io_rdata_1_jalTarget;
  wire  io_rdata_1_rvcMask_0;
  wire  io_rdata_1_rvcMask_1;
  wire  io_rdata_1_rvcMask_2;
  wire  io_rdata_1_rvcMask_3;
  wire  io_rdata_1_rvcMask_4;
  wire  io_rdata_1_rvcMask_5;
  wire  io_rdata_1_rvcMask_6;
  wire  io_rdata_1_rvcMask_7;
  wire  io_rdata_1_rvcMask_8;
  wire  io_rdata_1_rvcMask_9;
  wire  io_rdata_1_rvcMask_10;
  wire  io_rdata_1_rvcMask_11;
  wire  io_rdata_1_rvcMask_12;
  wire  io_rdata_1_rvcMask_13;
  wire  io_rdata_1_rvcMask_14;
  wire  io_rdata_1_rvcMask_15;
  wire  io_wen_0;
  wire [5:0] io_waddr_0;
  wire  io_wdata_0_brMask_0;
  wire  io_wdata_0_brMask_1;
  wire  io_wdata_0_brMask_2;
  wire  io_wdata_0_brMask_3;
  wire  io_wdata_0_brMask_4;
  wire  io_wdata_0_brMask_5;
  wire  io_wdata_0_brMask_6;
  wire  io_wdata_0_brMask_7;
  wire  io_wdata_0_brMask_8;
  wire  io_wdata_0_brMask_9;
  wire  io_wdata_0_brMask_10;
  wire  io_wdata_0_brMask_11;
  wire  io_wdata_0_brMask_12;
  wire  io_wdata_0_brMask_13;
  wire  io_wdata_0_brMask_14;
  wire  io_wdata_0_brMask_15;
  wire  io_wdata_0_jmpInfo_valid;
  wire  io_wdata_0_jmpInfo_bits_0;
  wire  io_wdata_0_jmpInfo_bits_1;
  wire  io_wdata_0_jmpInfo_bits_2;
  wire [3:0] io_wdata_0_jmpOffset;
  wire [49:0] io_wdata_0_jalTarget;
  wire  io_wdata_0_rvcMask_0;
  wire  io_wdata_0_rvcMask_1;
  wire  io_wdata_0_rvcMask_2;
  wire  io_wdata_0_rvcMask_3;
  wire  io_wdata_0_rvcMask_4;
  wire  io_wdata_0_rvcMask_5;
  wire  io_wdata_0_rvcMask_6;
  wire  io_wdata_0_rvcMask_7;
  wire  io_wdata_0_rvcMask_8;
  wire  io_wdata_0_rvcMask_9;
  wire  io_wdata_0_rvcMask_10;
  wire  io_wdata_0_rvcMask_11;
  wire  io_wdata_0_rvcMask_12;
  wire  io_wdata_0_rvcMask_13;
  wire  io_wdata_0_rvcMask_14;
  wire  io_wdata_0_rvcMask_15;


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


endmodule
