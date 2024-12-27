---
title: F3PreDecoder
linkTitle: F3PreDecoder
weight: 12
---

<div class="ifu-ctx">

# 子模块：F3PreDecoder模块简介

这个模块是从PreDecoder中时序优化出来的，负责判定CFI指令的类型

## F3PreDecoder功能介绍

### CFI指令类型判定

要想确定CFI指令类型，只需要分别尝试匹配JAL、JALR、BR和他们的RVC版本即可，注意，RVC的EBREAK
不应该被视为CFI指令。在匹配的过程中，自然CFI指令的类型就被甄别出来了。在这一步中，我们将所有指令分到如下四类brType中：

| CFI指令类型 | brType类型编码 |
| --- | --- |
| 非CFI | 00 | 
| branch指令 | 01 |
| jal指令 | 10 |
| jalr指令 | 11 |

### ret、call判定

然后，我们需要判断是否为call或者ret，这可以通过rd和rs的取值来考察，具体来说，RISCV的RVI指令中，提供了对rd和rs取值的约定，
当二者取到link寄存器的序号（x1为标准的返回地址寄存器，x5为备用的link寄存器），分别对应着压栈和弹栈。详细的对应情况如下：

![links](linkjal.png)

## F3PreDecoder子模块测试点和功能点

### 功能点1 CFI指令类型判定

要想确定CFI指令类型，只需要分别尝试匹配JAL、JALR、BR和他们的RVC版本即可，注意，RVC的EBREAK
不应该被视为CFI指令。

| 序号 | 名称     | 描述                                 |
|-----|--------|------------------------------------|
| 1\.1| 非CFI判定 | 对传入的非CFI指令（包括RVC\.EBREAK），应该判定为类型0 |
| 1\.2| BR判定   | 对传入的BR指令，应该判定为类型1   |
| 1\.3| JAL判定  | 对传入的JAL指令，应该判定为类型2  |
| 1\.4| JALR判定 | 对传入的JALR指令，应该判定为类型3 |

### 功能点2 ret、call判定

然后，需要判断是否为call或者ret，这可以通过rd和rs的取值来考察。当然，首先必须得满足无条件跳转指令。

对于类型2，只有为RVC指令且目的寄存器rd为link寄存器（x1或x5）时，才为Call。

对于类型3，当rd为link寄存器时，必为Call。当rs为link寄存器且rd不为时，必为Ret。

| 序号   | 名称               | 描述                                     |
|------|------------------|----------------------------------------|
| 2\.1 | 非CFI和BR不判定       | 对传入的非CFI和BR指令，都不应判定为call或者ret                  |
| 2\.2\.1\.1 | RVC\.JAL判定call | 对传入的RVC\.JAL指令，当rd设置为1或5，应当判定该指令为call          |
| 2\.2\.1\.2 | RVC\.JAL例外    | 对传入的RVC\.JAL指令，当rd设置为1和5之外的值，不应当判定该指令为call或ret |
| 2\.2\.2 | RVI\.JAL不判定   | 对传入的RVI\.JAL指令，无论什么情况都不能判定为call或ret    |
| 2\.3 | JALR和rd为link     | 传入JALR指令，并且rd为1或5，无论其他取值，都应判定为call     |
| 2\.3 | JALR且仅rs为link    | 传入JALR指令，rd不为1和5，rs为1或5，应判定为ret        |
| 2\.3 | JALR无link        | 对传入的JALR指令，若rd和rs均不为link，则不应判定为ret和cal |

## 测试点汇总

| 序号     | 功能            | 名称             | 描述                                 |
|--------|---------------|----------------|------------------------------------|
| 1\.1   | CFI指令类型判定     | 非CFI判定         | 对传入的非CFI指令（包括RVC\.EBREAK），应该判定为类型0 |
| 1\.2   | CFI指令类型判定     | BR判定           | 对传入的BR指令，应该判定为类型1                  |
| 1\.3   | CFI指令类型判定     | JAL判定          | 对传入的JAL指令，应该判定为类型2                             |
| 1\.4   | CFI指令类型判定     | JALR判定         | 对传入的JALR指令，应该判定为类型3                            |
| 2\.1   | ret、call判定    | 非CFI和BR不判定     | 对传入的非CFI和BR指令，都不应判定为call或者ret                  |
| 2\.2\.1\.1 | ret、call判定    | RVC\.JAL判定call | 对传入的RVC\.JAL指令，当rd设置为1或5，应当判定该指令为call          |
| 2\.2\.1\.2 | ret、call判定    | RVC\.JAL例外     | 对传入的RVC\.JAL指令，当rd设置为1和5之外的值，不应当判定该指令为call或ret |
| 2\.2\.2 | ret、call判定    | RVI\.JAL不判定    | 对传入的RVI\.JAL指令，无论什么情况都不能判定为call或ret    |
| 2\.3   | ret、call判定    | JALR和rd为link   | 传入JALR指令，并且rd为1或5，无论其他取值，都应判定为call     |
| 2\.3   | ret、call判定    | JALR且仅rs为link  | 传入JALR指令，rd不为1和5，rs为1或5，应判定为ret        |
| 2\.3   | ret、call判定    | JALR无link      | 对传入的JALR指令，若rd和rs均不为link，则不应判定为ret和call |

</div>