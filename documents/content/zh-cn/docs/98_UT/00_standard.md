---
title: 验证文档规范
linkTitle: 验证文档规范
weight: 1
---

本规范规定了“万众一芯”的文档模板（不是验证报告的模板），已发布和将来将要发布的文档都需要遵循这一规范。

以下是文档模板：

# 验证文档
## 模块功能说明
*简述功能*

*简述功能划分*

### 功能1说明
*针对功能1分解测试点*

*如果测试点较多可以先列一个小表格；针对每个测试点，给出设置cov_group的建议*

### 功能2说明

*针对功能2分解测试点*

*如果测试点较多可以先列一个小表格；针对每个测试点，给出设置cov_group的建议*

### 功能3说明
*针对功能3分解测试点*

*如果测试点较多可以先列一个小表格；针对每个测试点，给出设置cov_group的建议*

...

## 常量说明

*说明本模块中需要用到的关键常量。（可省略）*

## 接口说明
*详细解释各种接口的含义、来源*

## 测试点总表
|序号|对应功能|名称|解释| 
|-- | ---- | --- | --- |
|1.x.x| 链接相应功能 | 用英文大写？| 简单解释输入输出需要的信息 |

## 关键概念表

*列出关键概念，方便读者参考，如果没有或比较简单可以没有*

子模块的文档格式类似

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

# FIFO 验证文档

## 功能说明

本次需要验证的是FIFO，一种常见的硬件缓冲模块，在硬件电路中临时存储数据，并按照数据到达的顺序进行处理。

本次需要验证的FIFO每次可写可读8位数据，容量为8。

### 功能1：读FIFO

设置FIFO读使能之后，并且FIFO不为空时，可以从FIFO中读取数据。

#### 测试点1\.1 常规读取<a id="FIFO_READ_NORMAL"> </a>

当FIFO中已有数据时，设置读使能，从中读出一个数据。

建议对栈的状态进行观测。

#### 测试点1\.2 空读<a id="FIFO_READ_EMPTY"> </a>

当FIFO中无数据，设置读使能，不读取数据。

建议对栈的状态进行观测。

#### 测试点1\.3 无读使能不读<a id="FIFO_READ_NO_EN"> </a>

当FIFO中有数据，不设置读使能，不应该读取数据（建议判断方法：多次写之后设置读使能，读指针的数据应和第一次写入的数据一致）。

### 功能2：写FIFO

设置FIFO写使能之后，并且FIFO尚有空位时，可以向FIFO写入一个数据。

#### 测试点2\.1 常规写入<a id="FIFO_WRITE_NORMAL"> </a>

当FIFO中尚有空间时，设置写使能，可向FIFO写入一个数据。

建议对栈的状态进行观测。

#### 测试点2\.2 FIFO已满无法写入<a id="FIFO_WRITE_FULL"> </a>

当FIFO中数据已满，设置写使能，无法写入数据。

建议监测栈整体的状态。

#### 测试点2\.3 无写使能不写<a id="FIFO_WRITE_NO_EN"> </a>

当FIFO中有空间，不设置写使能，即使设置了待写入的数据，也不应该写入数据（建议判断方法：在保持写使能为假的情况下，连续读应该为空读）。

### 功能3：重置

设置rst为假后，清空队列。


#### 测试点3\.1 重置 <a id="FIFO_RESET_RESET"> </a>

设置rst为假后，下一周期时，队列应为空

## 常量说明

FIFO的容量为8。

## 接口说明

### 输入接口

rst\_n：1位信号，设置重置

wr\_en：1位信号，表示写使能

wdata：8位信号，表示写入的数据

rd\_en：1位信号，表示读使能

### 输出接口

rdata：8位信号，表示读出的数据

empty：1位信号，表示栈已经空了

full：1位信号，表示栈已经满了

## 测试点总表

建议各个测试点的覆盖组使用下表描述的功能和测试点名称进行命名。

比如FIFO\_READ的测试点覆盖点可以命名为FIFO\_READ\_NORMAL

|序号|功能名称|测试点名称|描述|
|--|---|---| --- |
|1\.1|FIFO\_READ| <a href="#FIFO_READ_NORMAL">NORMAL</a> |fifo有数据时，设置读使能，可以读出数据|
|1\.2|FIFO\_READ| <a href="#FIFO_READ_EMPTY">EMPTY</a> |fifo为空时，设置读使能，无法读出数据|
|1\.3|FIFO\_READ| <a href="#FIFO_READ_NO_EN">NO\_EN</a>  |fifo有数据时，不设置读使能，无法读出数据|
|2\.1|FIFO\_WRITE| <a href="#FIFO_WRITE_NORMAL">NORMAL</a>  |fifo未满时，设置写使能，可以写入数据|
|2\.2|FIFO\_WRITE| <a href="#FIFO_WRITE_FULL">FULL</a>   |fifo已满时，设置写使能，可以写入数据|
|2\.3|FIFO\_WRITE| <a href="#FIFO_WRITE_NO_EN">NO_EN</a>   |fifo未满时，不设置写使能，无法写入数据|
|3\.1|FIFO\_RESET| <a href="#FIFO_RESET_RESET">RESET</a>  |重置后，栈为空|

