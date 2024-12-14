---
title: IFU-RVC-Expander
linkTitle: IFU-RVC-Expander
weight: 12
---

# 子模块：RVCExpander简介

RVCExpander是IFU的子模块，负责对传入的指令进行指令扩展，并解码计算非法信息。

该模块接收的输入量是两个：一条RVC指令或者RVI指令；CSR对fs\.status的使能情况。

输出量也是两个：输入指令对应的RVI指令；RVC指令是否非法。

## 指令扩展

如果是RVI指令，则无需扩展。

否则对RVC指令，按照手册的约定进行扩展。

## 非法指令判断

RVI指令永远判断为合法。

对于RVC指令的判定，详细内容参阅20240411的RISCV手册的26\.8节表格列出的指令条件。

## RVC扩展辅助阅读材料

为方便参考模型的书写，在这里根据20240411版本的手册内容整理了部分指令扩展的思路。

对于RVC指令来说，op \= instr\(1, 0\)；funct \= instr\(15, 13\)

| op\\funct | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| ----- | --- | --- | --- | --- | --- | --- | ---| --- |
| 00 | addi4spn | fld | lw | ld | lbu<br>lhu;lh<br>sb;sh | fsd | sw | sd |
| 01 | addi | addiw | li | lui<br>addi16sp<br>zcmop | ARITHs<br>zcb | j | beqz | bnez |
| 10 | slli | fldsp | lwsp | ldsp | jr;mv<br>ebreak<br>jalr;add | fsdsp | fwsp | sdsp |

在开始阅读各指令的扩展规则时，需要了解一些RVC扩展的前置知识，比如：

rd', rs1'和rs2'寄存器：受限于16位指令的位宽限制，这几个寄存器只有3位来表示，他们对应到x8~x15寄存器。

###  op \= b'00'

#### funct \= b'000': ADDI4SPN

<image src="Caddi4spn.png" alter="addi4spn" width=600px />

该指令将一个0扩展的非0立即数加到栈指针寄存器x2上，并将结果写入rd'

其中，nzuimm\[5\:4\|9\:6\|2\|3\]的含义是：

这条指令的第12至11位是立即数的5至4位，第10至7位是立即数的9至6位，第6位是立即数的第2位，第7位是立即数的第3位。

这条指令最终扩展成为**addi rd', x2, nzuimm\[9\:2\]**

addi的格式形如：\| imm\[11\:0\] \| rs1 \| 000 \| rd \| 0010011 \|

注意，该指令的立即数为0的时候，不合法。

#### funct \= b'001': fld

<image src="Cfld.png" alter="fld" width=600px />

该指令从内存加载一个双精度浮点数到rd'寄存器。

offset的低三位是0，高位进行了0扩展。

这条指令最终扩展成为**fld rd′,offset(rs1′)**

fld的格式形如： \| imm\[11\:0\] \| rs1 \| 011 \| rd \| 0000111 \| 

注意：在昆明湖环境下，该指令要求CSR使能fs\.status，也即入参fsIsOff为假。

#### funct \= b'010': lw

<image src="Cfld.png" alter="lw" width=600px />

该指令从内存加载一个32位的值到rd'寄存器。

offset的低两位是0，高位进行了0扩展。

这条指令最终扩展成为**lw rd′,offset(rs1′)**

RVI的fw的格式形如： \| imm\[11\:0\] \| rs1 \| 010 \| rd \| 0000011 \|  

#### funct \= b'011': ldsp

<image src="Cfld.png" alter="ld" width=600px />

该指令从内存加载一个64位的值到rd'寄存器。

offset的低两位是0，高位进行了0扩展。

这条指令最终扩展成为**ld rd′,offset(rs1′)**

RVI的fw的格式形如： \| imm\[11\:0\] \| rs1 \| 011 \| rd \| 0000011 \|  

#### funct \= b'100': zcb extensions 1

在RVC指令中，这部分对应的是zcb扩展中的5条指令：lbu,lhu,lh,sb,sh

在zcb扩展中，进一步地取instr\[12\:10\]作为zcb扩展的指令码，我们记作funct_zcb

##### funct_zcb \= b'000': lbu

\| 100 \| 000 \| rs1' \| uimm\[0\|1\] \| rd' \| 00 \|

这个指令从rs1'+uimm的地址读取一字节，用0扩展并并加载到rd'中。

最终翻译为 lb rd', uimm(rs1')

lb指令的格式形如：\| imm\[11\:0\] \| rs1 \| 000 \| rd \| 0000011 \| 

##### funct_zcb \= b'001', instr[6] \=0 : lhu

\| 100 \| 001 \| rs1' \| 0 \| uimm\[1\] \| rd' \| 00 \|

这个指令从地址rs1' + uimm读取半word，用0扩展加载到rd'中。

最终翻译为 lhu rd', uimm(rs1')

lhu指令的格式形如：\| imm\[11\:0\] \| rs1 \| 101 \| rd \| 0000011 \| 

##### funct_zcb \= b'001', instr[6] \=1 : lh

\| 100 \| 001 \| rs1' \| 1 \| uimm\[1\] \| rd' \| 00 \|

这个指令从地址rs1' + uimm读取半word，符号扩展并加载到rd'中。

最终翻译为 lh rd', uimm(rs1')

lh指令的格式形如：\| imm\[11\:0\] \| rs1 \| 001 \| rd \| 0000011 \| 

##### funct_zcb \= b'010'： sb

\| 100 \| 010 \| rs1' \| uimm\[0 \| 1\] \| rd' \| 00 \|

这个指令把rs2'的低字节存储到地址rs1' + uimm指示的内存地址中。

最终翻译为 sb rs2, uimm(rs1')

RVI中sb指令的格式形如：\|imm\[11\:5\] \| rs2 \| rs1 \| 000 \| imm\[4\:0\] \| 0100011 \|

##### funct_zcb \= b'011': sh

\| 100 \| 011 \| rs1' \| 0 \| uimm\[1\] \| rd' \| 00 \|

这个指令把rs2'的低半字存储到地址rs1' + uimmz指示的内存地址中。

最终翻译为 sh rd', uimm(rs1')

sh指令的格式形如：\|imm\[11\:5\] \| rs2 \| rs1 \| 001 \| imm\[4\:0\] \| 0100011 \|

#### funct \= b'101': fsd

<image src="Cfsd.png" alter="fsd" width=600px />

fsd将rs2'中的双精度浮点数存储到rs1' + imm指示的内存区域

该指令的立即数低3位为0，同时进行了0符号扩展。

最终这个指令将被扩展为**fsd rs2′, offset(rs1′)**

RVI的FSD格式形如：\| imm[11:5]\| rs2 \| rs1 \| 011 \| imm[4:0] \| 0100011 \|

注意：在昆明湖环境下，该指令要求CSR使能fs\.status，也即入参fsIsOff为假。

#### funct \= b'110': sw

<image src="Cfsd.png" alter="sw" width=600px />

sw将rs2'中的一个字存储到rs1' + imm指示的内存区域

该指令的立即数低2位为0，同时进行了0符号扩展。

最终这个指令将被扩展为**sw rs2′, offset(rs1′)**

RVI的SW格式形如：\| imm[11:5]\| rs2 \| rs1 \| 010 \| imm[4:0] \| 0100011 \|

#### funct \= b'111': sd

<image src="Cfsd.png" alter="sd" width=600px />

fsd将rs2'中的双字存储到rs1' + imm指示的内存区域

该指令的立即数低3位为0，同时进行了0符号扩展。

最终这个指令将被扩展为**sd rs2′, offset(rs1′)**

RVI的SD格式形如：\| imm[11:5]\| rs2 \| rs1 \| 011 \| imm[4:0] \| 0100111 \|

###  op \= b'01'

#### funct \= b'000': addi

<image src="Caddi.png" alter="addi" width=600px />

该指令将一个符号扩展的非0立即数加到rd存储的数字上，并将结果写入rd。

尽管手册规定立即数和rd不为0，但是立即数和rd为0的情况仍可视为合法。前者是HINT指令，而后者是NOP。

这条指令最终扩展成为**addi rd, rd, imm**

addi的格式形如：\| imm\[11\:0\] \| rs1 \| 000 \| rd \| 0010011 \|

#### funct \= b'001': addiw

<image src="Caddi.png" alter="addiw" width=600px />

该指令的功能和addi类似，但是先计算得到32位数，然后再符号扩展至64位。

该指令的rd为0时非法。

当立即数不为0时，该指令最终扩展成为**addiw, rd, rd, imm**

addiw的指令格式为\| imm\[11\:0\] \| rs1 \| 000 \| rd \| 0011011 \|

如果立即数为0,该指令将会扩展成为sext.w rd，不过和addiw的格式是一样的，因此可以将他们归为一类。

#### funct \= b'010': li

<image src="Cli.png" alter="li" width=600px />

该指令将符号扩展的立即数加载到rd中。

当立即数为0时，该指令为hint，可以看作合法。

这条指令最终扩展成为**addi rd, x0, imm**

addi的格式形如：\| imm\[11\:0\] \| rs1 \| 000 \| rd \| 0010011 \|

#### funct \= b'011': lui/addi16sp/zcm

<image src="Cli.png" alter="lui" width=600px />

当rd不为0且不为2时，为lui指令，可以扩展为**lui rd, imm**

lui指令的格式形如： \| imm[31:12] \| rd \| 0110111 \|

当rd为0时，为hint，也可当作cli进行译码。

当rd为2时，为addi16sp指令：

<image src="Caddi.png" alter="addi16sp" width=600px />

扩展为**addi x2, x2, nzimm[9:4]**

addi的格式形如：\| imm\[11\:0\] \| rs1 \| 000 \| rd \| 0010011 \|

对addi16sp，立即数为0时非法。

此外，当第12至11位皆为0，第7位是1且第6至2位为0时，为zcmop，可以直接翻译为一个不起效的指令，比如与立即数0。

#### funct \= b'100': arith & zcb extension2 

在RVC指令中，这部分对应的是数学运算指令和zcb扩展中的另一部分指令，数学计算指令的对应如下：


#### funct \= b'101': j

<image src="Cj.png" alter="j" width=600px />

最终这个指令将被扩展为**jal x0, offset**

jal的格式形如：\| imm\[20\|10\:1\|11\|19\:12\] \| rd \| 1101111 \|

#### funct \= b'110': beqz

<image src="Cbnez.png" alter="beqz" width=600px />

sw将rs2'中的一个字存储到rs1' + imm指示的内存区域

该指令的立即数低2位为0，同时进行了0符号扩展。

最终这个指令将被扩展为**sw rs2′, offset(rs1′)**

RVI的SW格式形如：\| imm[11:5]\| rs2 \| rs1 \| 010 \| imm[4:0] \| 0100011 \|

#### funct \= b'111': bnez

<image src="Cbnez.png" alter="bnez" width=600px />

fsd将rs2'中的双字存储到rs1' + imm指示的内存区域

该指令的立即数低3位为0，同时进行了0符号扩展。

最终这个指令将被扩展为**sd rs2′, offset(rs1′)**

RVI的SD格式形如：\| imm[11:5]\| rs2 \| rs1 \| 011 \| imm[4:0] \| 0100111 \|

本处给出文字描述。

### opcode\[1, 0\] = 0：

C\.ADDI4SPN（opcode\[15,13\]=b\'000\'）：立即数为0时非法。

C\.FLD（opcode\[15,13\]=b\'001\'）：要求架构支持双精度浮点数，昆明湖环境下该指令要求csr使能了xstatus\.fs。

C\.LW（opcode\[15,13\]=b\'010\'）：永远合法。

C\.FLW/C\.LD（opcode\[15,13\]=b\'011\'）：要求架构支持浮点数以及通用寄存器位宽为64，昆明湖环境下该指令合法。

ZCB扩展指令（opcode\[15,13\]=b\'100\'）：第12位不得为1；opcode\[12,10\]为b\'011\'时，opcode\[6\]为1是不合法的

C\.FSD（opcode\[15,13\]=b\'101\'）：支持双精度浮点数，昆明湖环境下该指令要求csr使能了xstatus\.fs。

C\.SW（opcode\[15,13\]=b\'110\'）：永远合法。

C\.FSW/C\.SD（opcode\[15,13\]=b\'111\'）：要求架构支持浮点数以及通用寄存器位宽为64，昆明湖环境下该指令合法。

### opcode\[1, 0\] = 1：

C\.ADDI（opcode\[15,13\]=b\'000\'）：合法

C\.ADDIW（opcode\[15,13\]=b\'001\'）：昆明湖环境下，rd为0时非法。

C\.LI（opcode\[15,13\]=b\'010\'）：合法

C\.LUI/C\.ADDI16SP/ZCMOP（opcode\[15,13\]=b\'011\'）：
如果是LUI和ADDI16SP指令（rd为2），则立即数不能为0；
如果是ZCMOP扩展指令，则opcode\[11, 7\]应该为16以下的奇数

算术指令（opcode\[15,13\]=b\'100\'）：合法

C\.J（opcode\[15,13\]=b\'101\'）：合法

C\.BEQZ（opcode\[15,13\]=b\'110\'）：合法

C\.BNEZ（opcode\[15,13\]=b\'111\'）：合法

### opcode\[1, 0\] = 2：

C\.SLLI（opcode\[15,13\]=b\'000\'）：合法

C\.FLDSP（opcode\[15,13\]=b\'001\'）：应当支持双精度浮点数，昆明湖环境下要求csr使能了xstatus\.fs。

C\.LWSP（opcode\[15,13\]=b\'010\'）：rd为0时非法。

C\.LDSP（opcode\[15,13\]=b\'011\'）：昆明湖环境下，rd为0非法

C\.JALR（opcode\[15,13\]=b\'100\'）：opcode\[12\] = 0 的情况下，如果JR指令或MV指令的寄存器均为0，则非法

C\.FSDSP（opcode\[15,13\]=b\'101\'）：应当支持双精度浮点数，昆明湖环境下要求csr使能了xstatus\.fs。

C\.SWSP（opcode\[15,13\]=b\'110\'）：合法

C\.SDSP（opcode\[15,13\]=b\'111\'）：昆明湖架构下恒合法