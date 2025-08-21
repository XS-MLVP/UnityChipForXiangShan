---
title: Bitmap接口时序图
categories: [bitmap 硬件实现]
tags: [香山, bitmap, 硬件]
weight: 4
---

## Bitmap接口时序图

![](../../module03_1.png)

| 信号                | 描述                                                                   |
| ------------------- | ---------------------------------------------------------------------- |
| io_req_ready        | 8个fsm中有至少一个idle时为高，可以视为常态高                           |
| io_req_valid        | 新请求进入时高，平时为低                                               |
| io_resp_ready       | 当请求源（ptw hptw llptw）发送请求，等待返回时会拉高，平时无请求时为低 |
| io_resp_valid       | 当返回查询结果时拉高，平时为低                                         |
| io_mem_req_ready    | 有其它mem请求时（ptw llptw hptw）为低，平时为高                        |
| io_mem_req_valid    | cache miss时发起mem请求拉高，平时为低                                  |
| io_mem_resp_valid   | mem 返回结果拉高，平时为低                                             |
| io_cache_req_valid  | bimap fsm 发起 cache 请求拉高，平时为低                                |
| io_cache_req_ready  | 常态高                                                                 |
| io_cache_resp_valid | io_cache_req_valid下一clk 拉高平时低                                   |
| io_cache_resp_ready | io_cache_req_valid 下一clk 拉高平时低                                  |
