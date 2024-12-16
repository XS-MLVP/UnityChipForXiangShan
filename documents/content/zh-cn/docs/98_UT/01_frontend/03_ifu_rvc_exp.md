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

## 功能点和测试点

### 功能点1 指令扩展

RVCExpander负责接收预译码器拼接的指令码，并进行指令扩展，如果是16位RVC指令，需要按照RISCV手册的约定完成扩展

对此，我们需要随机生成RVI指令和RVC指令，送入预译码器：

| 序号    | 名称      | 描述                   |
|-------|---------|---------------------|
| 1\.1  | RVI指令保留 | 构造RVI指令传入，检查保留情况    |
| 1\.2  | RVC指令扩展 | 构造RVC指令传入，按手册检查扩展结果 | 


#### 功能点2 非法指令判断

RVCExpander在解析指令时，如发现指令违反了手册的约定，则需要判定该指令非法

对此，我们需要随机生成非法指令送入RVI中，并检测RVCExpander对合法位的校验；同时，我们还需要校验合法指令是否会被误判为非法指令：

同时，需要判定双精度浮点指令在CSR未使能fs\.status的情况下，能否将这类指令判定为非法。

| 序号| 名称      | 描述                   |
|----|---------|----------------------|
| 2\.1| 常规非法指令测试  | 随机构造非法RVC指令传入，检查判断结果 |
| 2\.2| 合法指令测试  | 随机构造合法RVC指令传入，检查判断结果 |
| 2\.3| 双精度浮点指令测试  | CSR未使能fs\.status的情况下，双精度浮点指令应该为非法 |

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

lw的格式形如： \| imm\[11\:0\] \| rs1 \| 010 \| rd \| 0000011 \|  

#### funct \= b'011': ldsp

<image src="Cfld.png" alter="ld" width=600px />

该指令从内存加载一个64位的值到rd'寄存器。

offset的低两位是0，高位进行了0扩展。

这条指令最终扩展成为**ld rd′,offset(rs1′)**

ld的格式形如： \| imm\[11\:0\] \| rs1 \| 011 \| rd \| 0000011 \|  

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

<image src="op01funct100.png" alter="arith" width=600px />

其中SRLI64和SRAI64在昆明湖环境下可以不考虑。

##### srli

<image src="Csrli.png" alter="srli" width=600px />

当funct2为00时，为srli。

最终可翻译为**srli rd′, rd′, 64**

srli的格式形如：\|0000000\|shamt\|rs1\|101\|rd\|0010011\|

##### srai

<image src="Csrli.png" alter="srai" width=600px />

当funct2为01时，为srai。

最终可翻译为**srai rd′, rd′, 64**

SRAI的格式形如：\|0100000\|shamt\|rs1\|101\|rd\|0010011\|

##### andi

<image src="Candi.png" alter="andi" width=600px />

该指令最终扩展为**andi rd′, rd′, imm**

andi的格式形如\|imm\[11\:0]\|rs1\|111\|rd\|0010011\|

##### sub

<image src="Csub.png" alter="sub" width=600px />

这条指令最终可以扩展为：**sub rd′, rd′, rs2′**

sub指令的格式形如：\|0100000\|rs2\|rs1\|000\|rd\|0110011\|

##### xor

<image src="Csub.png" alter="xor" width=600px />

这条指令最终可以扩展为：**xor rd′, rd′, rs2′**

xor指令的格式形如：\|0000000\|rs2\|rs1\|100\|rd\|0110011\|

##### or

<image src="Csub.png" alter="or" width=600px />

这条指令最终可以扩展为：**or rd′, rd′, rs2′**

or指令的格式形如：\|0000000\|rs2\|rs1\|110\|rd\|0110011\|

##### and

<image src="Csub.png" alter="and" width=600px />

这条指令最终可以扩展为：**and rd′, rd′, rs2′**

and指令的格式形如：\|0000000\|rs2\|rs1\|111\|rd\|0110011\|

##### subw

<image src="Csub.png" alter="subw" width=600px />

这条指令最终可以扩展为：**subw rd′, rd′, rs2′**

subw指令的格式形如：\|0100000\|rs2\|rs1\|000\|rd\|0111011\|

##### addw

<image src="Csub.png" alter="addw" width=600px />

这条指令最终可以扩展为：**addw rd′, rd′, rs2′**

addw指令的格式形如：\|0000000\|rs2\|rs1\|000\|rd\|0111011\|

##### mul

从mul开始的一部分指令属于zcb扩展。

zcb扩展中，当instr(12, 10) == "111"，且instr(6, 5)为"10"时，为mul指令。

zcb扩展中，当instr(12, 10) == "111"，且instr(6, 5)为"11"时，根据instr(4,2)，
共有000的zext\.b，001的sext\.b，010的zext\.h，011的sext\.h，100的zext\.w和101的not。

<image src="mul.png" alter="mul" width=600px />

该指令可扩展为mul rd, rd, rs2

mul的格式为：\|0000001\|rs2\|rs1\|000\|rd\|0110011\|

##### zext\.b

<image src="zextb.png" alter="mul" width=600px />

这条指令可以翻译为：**andi rd'/rs1', rd'/rs1', 0xff**

andi的格式形如\|imm\[11\:0]\|rs1\|111\|rd\|0010011\|

##### sext\.b

<image src="Csextb.png" alter="Csextb" width=600px />

该指令翻译为**sext\.b rd, rd**

sext\.b指令在RVI下形如:

<image src="Isextb.png" alter="Isextb" width=600px />

##### zext\.h

<image src="Czexth.png" alter="Czexth" width=600px />

该指令翻译为**zext\.h rd, rd**

zext\.h指令在RVI下形如:

<image src="Izexth.png" alter="Izexth" width=600px />

##### sext\.h

<image src="Csexth.png" alter="Csexth" width=600px />

该指令翻译为**sext\.h rd, rd**

sext\.h指令在RVI下形如:

<image src="Isexth.png" alter="Isexth" width=600px />

##### zext\.w

<image src="zextw.png" alter="zextw" width=600px />

该指令等价为**add.uw rd'/rs1', rd'/rs1', zero**

add\.uw指令在RVI下形如:

<image src="adduw.png" alter="adduw" width=600px />

##### not

<image src="not.png" alter="not" width=600px />

该指令等价为**xori rd'/rs1', rd'/rs1', -1**

xori指令在RVI下形如： \| imm\[11\:0\] \| rs1\| 100 \| rd \| 0010011 \|

#### funct \= b'101': j

<image src="Cj.png" alter="j" width=600px />

最终这个指令将被扩展为**jal x0, offset**

jal的格式形如：\| imm\[20\|10\:1\|11\|19\:12\] \| rd \| 1101111 \|

#### funct \= b'110': beqz

<image src="Cbnez.png" alter="beqz" width=600px />

该指令可以扩展到**beq rs1‘, x0, offset**

beq指令形如： \|imm\[12\|10\:5\]\|rs2\|rs1\|000\|imm\[4\:1\|11\]\|1100011\|
imm[12|10:5]rs2rs1001imm[4:1|11]1100011BNE

#### funct \= b'111': bnez

<image src="Cbnez.png" alter="bnez" width=600px />

最终这个指令将被扩展为**bne rs1′, x0, offset**

bne指令形如：\|imm\[12\|10\:5\]\| rs2 \| rs1 \| 001 \| imm\[4\:1\|11\] \| 1100011\|

###  op \= b'10'

#### funct \= b'000': slli

<image src="Cslli.png" alter="slli" width=600px />

该指令将一个符号扩展的非0立即数加到rd存储的数字上，并将结果写入rd。

尽管手册规定立即数和rd不为0，但是立即数和rd为0的情况仍可视为合法。前者是HINT指令，而后者是NOP。

这条指令最终扩展成为**slli rd, rd, shamt\[5\:0\]**

slli的格式形如：\|000000\|shamt\|rs1\|001\|rd\|0010011\|

#### funct \= b'001': fldsp

<image src="Cfldsp.png" alter="fldsp" width=600px />

该指令最终扩展成为**fld rd, offset(x2)**

fld的格式形如： \| imm\[11\:0\] \| rs1 \| 011 \| rd \| 0000111 \| 

该指令要求CSR使能fs\.status

#### funct \= b'010': lwsp

<image src="Cfldsp.png" alter="lwsp" width=600px />

rd为0时非法。

这条指令最终扩展成为**lw rd, offset(x2)**

lw的格式形如： \| imm\[11\:0\] \| rs1 \| 010 \| rd \| 0000011 \|  

#### funct \= b'011': ldsp

<image src="Cfldsp.png" alter="ldsp" width=600px />

rd为0时非法。

这条指令最终扩展成为**ld rd, offset(x2)**

lw的格式形如： \| imm\[11\:0\] \| rs1 \| 011 \| rd \| 0000011 \|  

#### funct \= b'100': jr/mv/ebreak/jalr/add

<image src="op10funct100.png" alter="jrmvebreakjalradd" width=600px />

##### jr

<image src="Cjr.png" alter="jr" width=600px />

当rd为0时，非法。

该指令最终可以扩展为**jalr x0, 0(rs1)**

jalr指令的格式为：\|imm\[11\:0\]\|rs1\|000\|rd\|1100111\|

##### mv

<image src="Cmv.png" alter="mv" width=600px />

rd为0时，是hint指令。

该指令最终可以扩展为**add rd, x0, rs2**

add指令形如：\|0000000\|rs2\|rs1\|000\|rd\|0110011\|

##### ebreak

可以扩展为ebreak指令。

形如：\|00000000000100000000000001110011\|

##### jalr

<image src="Cjr.png" alter="jalr" width=600px />

该指令最终可以扩展为**jalr x1, 0(rs1)**

jalr指令的格式为：\|imm\[11\:0\]\|rs1\|000\|rd\|1100111\|

##### add

<image src="Cmv.png" alter="mv" width=600px />

该指令最终可以扩展为**add rd, rd, rs2**

add指令形如：\|0000000\|rs2\|rs1\|000\|rd\|0110011\|

#### funct \= b'101': fsdsp

<image src="Cfsdsp.png" alter="fsdsp" width=600px />

这条指令最终扩展成为**fsd rs2, offset(x2)**

RVI的FSD格式形如：\| imm[11:5]\| rs2 \| rs1 \| 011 \| imm[4:0] \| 0100011 \|

该指令要求CSR使能fs\.status

#### funct \= b'110': swsp

<image src="Cfsdsp.png" alter="swsp" width=600px />

这条指令最终扩展成为**sw rs2, offset(x2)**

RVI的SW格式形如：\| imm[11:5]\| rs2 \| rs1 \| 010 \| imm[4:0] \| 0100011 \|

#### funct \= b'111': sdsp

<image src="Cfsdsp.png" alter="sdsp" width=600px />

该指令最终扩展成为**sd rd, offset(x2)**

RVI的SD格式形如：\| imm[11:5]\| rs2 \| rs1 \| 011 \| imm[4:0] \| 0100111 \|