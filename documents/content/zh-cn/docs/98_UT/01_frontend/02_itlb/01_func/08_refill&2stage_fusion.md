---
title: 支持回填条目与两阶段条目融合
linkTitle: 08.refill&2stage_fusion
weight: 12
---

参照支持缓存映射条目与支持读取 `PTW` 返回条目，对于主机地址转换（`nos2xlate`）的情况对应填入 `entry` 中的对应表项即可，此时访客有关信号无效。注意大页时，即 `level` 不为 `0` 时，`ppn_low` 无效。

| TLB entry                   | 填入的来自 PTW 的信号      |
|-----------------------------|-----------------------------|
| s2xlate[1:0]                | 0b00 (nos2xlate)           |
| tag[34:0]                   | s1.tag[34:0]               |
| asid[15:0]                  | s1.asid[15:0]              |
| vmid[13:0]                  | 无效                        |
| level[1:0]                  | s1.level[1:0]              |
| ppn[32:0]                   | s1.ppn[32:0]               |
| ppn_low[2:0]×8              | s1.ppn_low_*                |
| valididx×8                  | s1.valididx_*               |
| pteidx×8                    | s1.pteidx_*                 |
| perm_pf                     | s1.pf                       |
| perm_af                     | s1.af                       |
| perm_a                      | s1.perm.a                   |
| perm_g                      | s1.perm.g                   |
| perm_u                      | s1.perm.u                   |
| perm_x                      | s1.perm.x                   |
| gperm_gpf                   | 无效                        |
| gperm_gaf                   | 无效                        |
| gperm_a                     | 无效                        |
| gperm_x                     | 无效                        |
| *s2xlate=0b00 时填入 TLB entry 示意表*

在 `OnlyStage1` 的情况下，主机的异常信号以及部分不可复用的权限位无效，其余均与主机地址转换一致。

| TLB entry                   | 填入的来自 PTW 的信号      |
|-----------------------------|-----------------------------|
| s2xlate[1:0]                | 0b01 (OnlyStage1)          |
| tag[34:0]                   | s1.tag[34:0]               |
| asid[15:0]                  | s1.asid[15:0]              |
| vmid[13:0]                  | s1.vmid[13:0]              |
| level[1:0]                  | s1.level[1:0]              |
| ppn[32:0]                   | s1.ppn[32:0]               |
| ppn_low[2:0]×8              | s1.ppn_low_*                |
| valididx×8                  | s1.valididx_*               |
| pteidx×8                    | s1.pteidx_*                 |
| perm_pf                     | s1.pf                       |
| perm_af                     | s1.af                       |
| perm_a                      | s1.perm.a                   |
| perm_g                      | s1.perm.g                   |
| perm_u                      | s1.perm.u                   |
| perm_x                      | s1.perm.x                   |
| gperm_gpf                   | 无效                        |
| gperm_gaf                   | 无效                        |
| gperm_a                     | 无效                        |
| gperm_x                     | 无效                        |
| *s2xlate=0b01 时填入 TLB entry 示意表*

对于 `OnlyStage2` 的情况，`asid` 无效，`vmid` 使用 `s1.vmid`（由于 `PTW` 模块无论什么情况都会填写这个字段，所以可以直接使用这个字段写入），`pteidx` 根据 `s2` 的 `tag` 的低 `3` 位来确定。如果 `s2` 是大页，那么 `TLB` 项的 `valididx` 均为有效，否则 `TLB` 项的 `pteidx` 对应 `valididx` 有效。`ppn` 的填写复用了 `allStage` 的逻辑，将在 `allStage` 的情况下介绍。

| TLB entry                   | 填入的来自 PTW 的信号      |
|-----------------------------|-----------------------------|
| s2xlate[1:0]                | 0b10 (OnlyStage2)          |
| tag[34:0]                   | s2.tag[37:3]               |
| asid[15:0]                  | 无效                        |
| vmid[13:0]                  | s1.vmid[13:0]              |
| level[1:0]                  | s2.level[1:0]              |
| ppn[32:0]                   | s2.ppn[35:3]               |
| ppn_low[2:0]×8              | { s2.ppn[2:0], 无效×7 }    |
| valididx×8                  | { 1， 0×7 }                 |
| pteidx×8                    | s2.tag[2:0]                |
| perm_pf                     | 无效                        |
| perm_af                     | 无效                        |
| perm_a                      | 无效                        |
| perm_g                      | 无效                        |
| perm_u                      | 无效                        |
| perm_x                      | 无效                        |
| gperm_gpf                   | s2.gpf                      |
| gperm_gaf                   | s2.gaf                      |
| gperm_a                     | s2.perm.a                   |
| gperm_x                     | s2.perm.x                   |
| *s2xlate=0b10 时填入 TLB entry 示意表*

如果两阶段地址转换均启用，`TLB` 将两阶段的结果合并存储，并丢弃中间物理地址（`s1` 阶段的 `ppn`），仅存储最终物理地址。`level` 需要取 `s1.level` 与 `s2.level` 中的较大值，此时需要注意，当 `s1` 阶段为大页，而 `s2` 阶段为小页的情况下，例如中间物理地址指向一个 `2MB` 页，而 `s2` 阶段转换的结果却是一个 `4KB` 页，在这种情况下，需要特殊处理，将 `s1.tag` 的高位（在此例子中为高 `11+9+9=29` 位）和 `s2.tag` 的低位（在此例子中为低 `9` 位）共 `38` 位合并存储到 `tag` 与 `pteidx` 中，如果不足 `38` 位则在后面补 `0`（例如中间物理地址指向 `1GB` 页而 `s2` 阶段指向 `2MB` 页，此时 `tag[34:0] = {s1.tag[34:15], s2.tag[17:9], 6'b0}`）。在这种情况（`s1` 大页 `s2` 小页）下 `ppn` 也需要处理后存储，根据 `s2.level` 将 `s2.ppn` 与 `s2.tag` 进行拼接后存储。

| TLB entry                   | 填入的来自 PTW 的信号      |
|-----------------------------|-----------------------------|
| s2xlate[1:0]                | 0b11 (allStage)            |
| tag[34:0]                   | 根据策略选择 s1.tag/s2.tag 的部分位 |
| asid[15:0]                  | s1.asid                     |
| vmid[13:0]                  | s1.vmid                     |
| level[1:0]                  | s1.level 与 s2.level 的较大者 |
| ppn[32:0]                   | s2.ppn 与 s2.tag 根据 s2.level 的拼接的高位 |
| ppn_low[2:0]×8              | s2.ppn 与 s2.tag 根据 s2.level 的拼接的低位 |
| valididx×8                  | 根据 level 确定            |
| pteidx×8                    | tag 的低位                  |
| perm_pf                     | s1.pf                       |
| perm_af                     | s1.af                       |
| perm_a                      | s1.perm.a                   |
| perm_g                      | s1.perm.g                   |
| perm_u                      | s1.perm.u                   |
| perm_x                      | s1.perm.x                   |
| gperm_gpf                   | s2.gpf                      |
| gperm_gaf                   | s2.gaf                      |
| gperm_a                     | s2.perm.a                   |
| gperm_x                     | s2.perm.x                   |
| *s2xlate=0b11 时填入 TLB entry 示意表*