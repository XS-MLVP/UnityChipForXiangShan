---
title: FIFO文档案例
linkTitle: FIFO文档案例
weight: 5
draft: false
---

以下以FIFO为例，展示了一个简单的文档案例

```verilog
`timescale 1ns / 1ps
module FIFO ( //data_width = 8  data depth =8
  input clk,
  input rst_n,
  input wr_en,          //写使能
  input rd_en,          //读使能
  input [7:0]wdata,     //写入数据输入
  output [7:0]rdata,    //读取数据输出
  output empty,         //读空标志信号
  output full           //写满标志信号
);
  reg [7:0] rdata_reg = 8'd0;
  assign rdata = rdata_reg;

  reg  [7:0] data [7:0];     //数据存储单元(8bit数据8个)
  reg  [3:0] wr_ptr = 4'd0;  //写指针
  reg  [3:0] rd_ptr = 4'd0;  //读指针
  wire [2:0] wr_addr;        //写地址(写指针的低3位)
  wire [2:0] rd_addr;        //读地址(读指针的低3位)

assign wr_addr = wr_ptr[2:0];
assign rd_addr = rd_ptr[2:0];

always@(posedge clk or negedge rst_n)begin //写数据
  if(!rst_n) 
    wr_ptr <= 4'd0;
  else if(wr_en && !full)begin
    data[wr_addr]  <= wdata;
    wr_ptr <= wr_ptr + 4'd1;
  end
end

always@(posedge clk or negedge rst_n)begin //读数据
  if(!rst_n)
    rd_ptr <= 'd0;
  else if(rd_en && !empty)begin
    rdata_reg  <= data[rd_addr];
    rd_ptr <= rd_ptr + 4'd1;
  end
end

assign empty = (wr_ptr == rd_ptr); //读空
assign full  = (wr_ptr == {~rd_ptr[3],rd_ptr[2:0]}); //写满

endmodule

```

# FIFO 模块验证文档

## 文档概述

本文档描述FIFO的功能，并根据功能给出测试点参考，方便测试的参与者理解测试需求，编写相关测试用例。

## 术语说明

| 缩写	| 全称 | 定义 |
| -- | ----- | ---|
| FIFO | First In First Out | 先进先出的数据缓冲队列 |

## 功能说明

本次需要验证的是FIFO，一种常见的硬件缓冲模块，在硬件电路中临时存储数据，并按照数据到达的顺序进行处理。

本次需要验证的FIFO每次可写可读8位数据，容量为8。

### 1. 读FIFO操作

#### 1.1. 常规读取

**功能描述**：当rd_en=1且empty=0时，在时钟上升沿输出rdata

**建议观测点**：
- 读指针递增逻辑
- rdata与预期数据匹配

#### 1.2. 读空栈

**功能描述**：当empty=1且rd_en=1时，rdata保持无效值

**建议观测点**：
- empty信号持续为高
- 读指针无变化

#### 1.3. 无读使能不读

**功能描述**：当rd_en=0时，无论FIFO状态如何均不更新rdata

**建议观测点**：
- 连续写入后关闭读使能，验证读指针冻结

### 2. 写FIFO操作

#### 2.1. 常规写入

**功能描述**：当wr_en=1且full=0时，在时钟上升沿存储wdata

**观测点**：
- 写指针递增逻辑
- 存储阵列数据更新

#### 2.2. FIFO已满无法写入

**功能描述**：当full=1且wr_en=1时，wdata被丢弃

**观测点**：
- full信号持续为高
- 存储阵列内容不变

#### 2.3. 无写使能不写

**功能描述**：当wr_en=0时，无论FIFO状态如何均不写入数据

**观测点**：
- 写指针冻结
- 存储阵列内容保持不变

### 3. 复位操作

#### 3.1. 复位控制

**功能描述**：当rst_n=0时，清空FIFO并重置指针

**观测点**：
- 复位后empty=1且full=0
- 读写指针归零

## 常量说明
| 常量名 | 常量值 | 解释 |
| ---- | ----| -------|
| FIFO_DEPTH | 8 | FIFO存储单元数量|
| DATA_WIDTH | 8 |数据总线位宽 |

## 接口说明

### 输入接口
| 信号名 | 方向 | 位宽 | 描述 | 
| ---| --- |--- |--- |--- |
| clk | Input | 1 | 主时钟 | 
| rst_n | Input	| 1	| 异步复位 | 
| wr_en	| Input	| 1 | 写使能 | 
| wdata	| Input	| 8	| 写入数据 | 
| rd_en | Input | 1	| 读使能 | 
### 输出接口

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- |--- | --- | 
| rdata | Output | 8 | 读出数据 |
| empty | Output | 1 | FIFO空标志（高有效）|
| full | Output |	1 |	FIFO满标志（高有效）|

## 测试点总表

建议各个测试点的覆盖组使用下表描述的功能和测试点名称进行命名。

比如FIFO\_READ的测试点NORMAL，其覆盖点建议命名为FIFO\_READ\_NORMAL

<mrs-testpoints>

|序号|功能名称|测试点名称|描述|
|--|---|---| --- |
|1\.1|[FIFO\_READ](#1-读fifo操作)| NORMAL |fifo有数据时，设置读使能，可以读出数据|
|1\.2|FIFO\_READ| EMPTY |fifo为空时，设置读使能，无法读出数据|
|1\.3|FIFO\_READ| NO\_EN  |fifo有数据时，不设置读使能，无法读出数据|
|2\.1|[FIFO\_WRITE](#2-写fifo操作)| NORMAL  |fifo未满时，设置写使能，可以写入数据|
|2\.2|FIFO\_WRITE| FULL   |fifo已满时，设置写使能，可以写入数据|
|2\.3|FIFO\_WRITE| NO_EN   |fifo未满时，不设置写使能，无法写入数据|
|3\.1|[FIFO\_RESET](#3-复位操作)| RESET  |重置后，栈为空|

</mrs-testpoints>

