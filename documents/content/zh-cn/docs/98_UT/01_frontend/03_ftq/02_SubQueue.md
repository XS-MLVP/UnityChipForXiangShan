---
title: FTQ子队列
linkTitle: FTQ子队列
weight: 12
---


# FTQ子队列简介
在之前的介绍中，我们采用FTQ项这个术语描述描述FTQ队列中的每一个元素，实际上，这只是一种便于抽象的说法。

实际上的FTQ队列，是由好多个子队列共同构成的，一些子队列维护一类信息，另一些子队列维护另一类信息，相同ftqIdx索引的子队列信息共同构成一个完整的FTQ项。

为什么要把它们分开成多个子队列呢？因为某些模块只需要FTQ项中的某一些信息，比如IFU想要取值目标，它只需要专门存储取值目标的子队列提供的信息就行了。另外，在我们更改FTQ项的内容时，也只需要写入需要更新的子队列，比如IFU预译码写回时，只需要写回专门存储预译码信息的队列了。

下面来介绍一些FTQ的主要子队列，以及它们内部存储的数据结构。此外，FTQ还有一些存储中间状态的更小的队列
# ftq_redirect_mem

ftq_redirect_mem是香山ftq的一个子队列。它记录了重定向需要的一些信息，帮助重定向回正确状态，这些信息来自于BPU分支预测中的RAS预测器，以及顶层的分支历史指针，如果想要了解，可以参考BPU的RAS子文档了解如何通过这些信息回溯到之前的状态。
## 读写
它是一个寄存器堆，由64（FtqSize）个表项（Ftq_Redirect_SRAMEntry）构成。支持同步读写操作。有3个读端口和1个写端口，每个读端口负责与不同的模块交互。
- 读操作：
    - 输入：
        - 需要使能ren，这是一个向量，可指定任意读端口可读
            - 对应接口：ren
        - 从任意读端口中输入要读取的元素在ftq_redirect_mem中的地址，这是一个从0到ftqsize-1的索引
            - 对应接口：raddr
    - 输出：
        - 从发起输入的读端口对应的读出端口中读出Ftq_Redirect_SRAMEntry。
            - 对应接口：rdata
- 写操作
    - 输入：
        -  需要使能wen，可指定写端口可写
            - 对应接口：wen
        - 向写端口中输入要写入的元素在ftq_redirect_mem中的地址，这是一个从0到ftqsize-1的索引
            - 对应接口：waddr
        - 向wdata中写入Ftq_Redirect_SRAMEntry
            - 对应接口：wdata
- 多端口读：可以从多个读端口读取结果

*每个子队列的读写基本都是类似的，后面不再赘述*
## Ftq_Redirect_SRAMEntry
继承自SpeculativeInfo，存储RAS预测器相关重定向信息，根据这些信息回溯到之前的状态
- sc_disagree：统计分支指令在sc预测器中预测是否发生错误
	- 接口类型：Some(Vec(numBr, Bool()))
	- 说明：Option 类型，表明这个值可能不存在，在非FPGA平台才有，否则为none
	- 信号列表：
		- SpeculativeInfo：推测信息，帮助BPU在发生重定向的时候回归正常的状态
			- 接口列表:
				- histPtr：重定向请求需要恢复的全局历史指针，可参见BPU顶层文档了解详情
					- 接口类型：CGHPtr
			- 说明：以下都属于RAS重定向信息,可参见BPU文档了解如何利用这些信息进行重定向
				- ssp：重定向请求指令对应的 RAS 推测栈栈顶在提交栈位置的指针
					- 接口类型：UInt(log2Up(RasSize).W)
				- sctr：重定向请求指令对应的 RAS 推测栈栈顶递归计数 Counter
					- 接口类型：RasCtrSize.W
				- TOSW：重定向请求指令对应的 RAS 推测栈（队列）写指针
					- 接口类型：RASPtr
				- TOSR：重定向请求指令对应的 RAS 推测栈（队列）读指针
					- 接口类型：RASPtr
				- NOS：重定向请求指令对应的 RAS 推测栈（队列）读指针
					- 接口类型：RASPtr
				- topAddr：
					- 接口类型：UInt(VAddrBits.W)
				
# ftq_pd_mem
由64（FtqSize）个表项（Ftq_pd_Entry）构成。支持同步读写操作。有2个读端口和1个写端口。具有读写使能信号。
## ftq_pd_mem简介

存储来自IFU预译码的写回信息，它是一个寄存器堆，由64（FtqSize）个表项（Ftq_pd_Entry）构成。有2个读端口和1个写端口。

ftq_pd_mem直接接收来自IfuToFtqIO的信号，从中获取Ftq_pd_Entry，表示一个指令块对应的预译码信息表项。读取时获取预测块内某条指令的预测信息
## Ftq_pd_Entry

- brMask：一个指令预测宽度内（16条rvc指令）的指令块中，哪些指令是分支指令
	- 接口类型：Vec(PredictWidth, Bool())
- jmpInfo：jump信息，其值对应不同的jmp指令类型，表示指令块内jmp指令类型
	- 接口类型：ValidUndirectioned(Vec(3, Bool()))
	- 说明：  jumpinfo有效的时候，第0位是0，表示jal指令，第0位是1，表示jalr指令，第1位是1，表示call指令，第二位是1，表示ret指令。
- jmpOffset：jmp指令在指令预测块中的偏移地址
	- 接口类型： UInt(log2Ceil(PredictWidth).W)
- rvcMask：一个预测块内的指令（16条rvc指令）哪些是rvc指令
	- 接口类型：Vec(PredictWidth, Bool())

## 读取与写入

### 写入
#### **PredecodeWritebackBundle（IfuToFtqIO）如何写入ftq_pd_mem的一条Ftq_pd_Entry**

Ftq_pd_Entry项的写入是通过PredecodeWritebackBundle这个接口进行写入的（其实也就是IfuToFtqIO）
*fromPdWb*：
   - brmask：PredecodeWritebackBundle有一个预测块内的所有指令的预译码信息，当一条指令的预译码信息有效(valid)且是分支指令（is_br）时, bool序列对应位置的指令被判定为分支指令
   - jumpInfo：
	  - valid：预测块内存在一条指令，其预译码信息有效（valid），且是jmp指令（isJal或者isJalr）时，jumpInfo有效
	  - bits：预测块内的第一条有效跳转指令的info，它是一个三位序列，从低到高（拉高）对应该指令被预译码为是isJalr，isCall，isRet
   - jmpOffset：预测块内第一条有效jmp跳转指令的偏移
   - rvcMask：原封不动接受同名信号
   - jalTarget：原封不动接收同名信号
### 读取
#### **ftq_pd_mem的一条Ftq_pd_Entry如何以PreDecodeInfo（to pd）的形式输出**

PreDecodeInfo是一个Ftq_pd_Entry中的一条指令的预译码，需要输入offset，指定该预译码指令在预测块内的偏移

- valid：直接set为1

- isRVC：rvcMask bool序列中对应偏移的值

- isBr：brMask bool序列中对应偏移的值

- isJalr：该偏移量等于jumpOffset，且jumpInfo有效并指明该指令type是isJalr（jmpInfo.valid && jmpInfo.bits(0)）

# ftb_entry_mem
有两个读端口，一个写端口，FtqSize个表项，存储的数据项为FTBEntry_FtqMem，FTBEntry_FtqMem与FTBEntry基本上是一致的。
## FTBEntry_FtqMem
- brSlots：分支指令槽
	- 接口类型：Vec(numBrSlot, new FtbSlot_FtqMem)
	- FtbSlot_FtqMem：
		- 信号列表：
			- offset：给分支指令在相对于指令块起始地址的偏移
				- 接口类型：UInt(log2Ceil(PredictWidth).W)
			- sharing：对于tailSlot来说，启用sharing表示把这个slot让给分支指令来被预测
				- 接口类型：Bool
			- valid：预测槽有效
				- 接口类型：Bool
				- 说明：当slot有效时，我们才能说这条指令是br指令还是jmp指令
- tailSlot：跳转指令槽
	- 接口类型：FtbSlot_FtqMem
- FTBEntry_part：FTBEntry_FtqMem的父类，存储部分FTB信息，记录跳转指令的类型
	- 信号列表：
		- isCall：接口类型：Bool
		- isRet：接口类型：Bool
		- isJalr：接口类型：Bool
## 读取
可以从FTBEntry_FtqMem获取以下有效信息：
- jmpValid：预测块中jmp指令有效
	- 说明：当tailslot有效且不分享给分支指令时，jmp有效
- getBrRecordedVec：三维向量，对于三个slot
	- 说明：接收一个offset偏移，如果命中有效分支slot（或者sharing拉高的tailslot），对应slot的向量元素拉高。
- brIsSaved：给定offset的指令是否是分支指令
	- 说明：采用slot预测结果来说明是不是分支指令，前提需要信号有效
- getBrMaskByOffset：
	- 说明：在给定offset范围内的三个slot中的指令是否是有效分支指令，用一个三位maks表示
- newBrCanNotInsert：能否插入新的brSlot
	- 说明：给定offset超过有效tailSlot对应的offset时，不能插入新的brSlot
## 读取时机 

# ftq_pc_mem
pc存储子队列。存储项为Ftq_RF_Components，用来读取取指信息，取值信息交给IFU进行取指。
## Ftq_RF_Components

**信号含义**
- startAddr: 预测块的起始地址
- nexLineAddr: 预测块下一个缓存行的起始地址
    - startAddr加上64个字节，一个缓存行的大小是64字节
- isNextMask: 一个预测宽度内的16条指令各自是否属于下一个预测块
    - 通过计算某条指令相对于预测块起始地址的偏移量（每条指令两个字节）得到偏移地址，该偏移地址的第4位（从0开始）为1，表示该指令属于下一个预测块。
    - 进一步说，其实也就可以根据它判断该指令是否在预测块跨缓存行的时候判断该指令是否属于下一个cacheline了
- fallThruError ：预测出的下一个顺序取指地址是否存在错误
## 读取和写入
**信息获取：上述信息都可以从一个单流水级分支预测结果 (BranchPredictionBundle)中获取**。
获取方式：startAddr直接获取BranchPredictonBundle中的pc，fallThruError直接获取BranchPredictionBundle中的fallThruError。

**PC生成：预测块内每条指令的PC都可以通以下方式获取：**
每次从ICache取指都会取一个或两个CacheLineSize（64 Bytes）长度的缓存行指令数据，是否取两个由预测块是否跨缓存行决定。
而每个预测块的长度为PredictWidth（16）个压缩指令的长度（32 Bytes）。每个缓存行的长度为每个预测块长度的两倍，所以每个预测块的startAddr要么在当前缓存行的前半部分（startAddr[5] = 0），要么在当前缓存行的后半部分（startAddr[5] = 1）。
- 如果startAddr[5] = 0，那么当前预测块必然不会跨缓存行，那么此时预测指令pc = {startAddr[38, 6], startAddr[5, 1] + offset, 1’b0}。
- 如果startAddr[5] = 1，那么当前预测块可能会出现跨缓存行的情况。此时：
    - 如果isNextMask(offset) = 0，表示当前预测指令pc未跨缓存行，那么此时预测指令pc = {startAddr[38, 6], startAddr[5, 1] + offset, 1’b0}
    - 如果isNextMask(offset) = 1，表示当前预测指令pc跨越了缓存行，那么此时预测指令pc = {nextLineAddr[38,6], startAddr[5, 1] + offset, 1’b0}
## 读写时机
**写入时机**：BPU流水级的S1阶段，创建新的预测entry时写入
**读出时机**： 读数据每个时钟周期都会存进Reg。如果IFU不需要从bypass中读取数据，Reg数据直连给Icache和IFU，如果IFU不需要从bypass中读取数据，Reg数据直连给Icache和IFU
# ftq_meta_1r_sram
存储的数据为Ftq_1R_SRAMEntry，同样有FtqSize项
Ftq_1R_SRAMEntry接口列表
- meta：分支预测的meta数据
- ftb_entry：分支预测的FTB项
**写入时机**：在 BPU的s3阶段接收信息，因为对于一个指令预测块，只有在其s3阶段才能获取完整的mata信息，同样被接收的还有最后阶段ftqentry信息

# 其余状态子队列
上述存储结构是FTQ中比较核心的存储结构，实际上，还有一些子队列用来存储一些状态信息，也同样都是存储ftqsize个（64）元素。主要有以下：

update_target：记录每个FTQ项的跳转目标，跳转目标有两种，一种是当该FTQ项对应的分支预测结果中指明的该分支预测块中执行跳转的分支指令将要跳转到的地址，另一种则是分支预测块中不发生跳转，跳转目标为分支预测块中指令顺序执行的下一条指令地址。

- 此外，与之配套的还有newest_entry_target，newest_entry_ptr用来指示新写入的跳转目标地址，和它对应的指令预测块或者说FTQ项的在FTQ中的位置，同时，有辅助信号newest_entry_target_modified和newest_entry_ptr_modified用来标识该地址的FTQ项跳转地址是否被修改。

写入时机：上一个周期的bpu_in_fire有效的时候，或者说相对于bpu_in_fire有效时延迟一个周期写入。

cfiIndex_vec：记录每个FTQ项的发生跳转的指令cfi（control flow instruction）指令在其分支预测块中的位置
写入时机：相对于bpu_in_fire有效时延迟一个周期写入。

mispredict_vec：记录每个FTQ项的分支预测结果是否有误，初始化为false

pred_stage：记录每个FTQ项的分支预测结果是来自于哪个阶段
写入时机：相对于bpu_in_fire有效时延迟一个周期写入。

pred_s1_cycle：记录每个FTQ项的分支预测结果对应的s1阶段的分支预测结果生成的时间（cycle数）
写入时机：相对于bpu_in_fire有效时延迟两个周期写入。

commitStateQueueReg：记录每个FTQ项中对应的分支预测块中每条指令（一般是16条rvc指令，对应一个预测宽度）的提交状态，提交状态有c_empty ，c_toCommit ，c_committed ，c_flushed，依次用从小到大的枚举量表示，初始化为c_empty状态
写入时机：相对于bpu_in_fire有效时延迟一个周期写入。

entry_fetch_status：记录每个FTQ项的分支预测结果是否被送到ifu中，该状态由两个枚举量f_to_send ， f_sent来表示, 初始化为f_sent状态。
写入时机：上一个周期的bpu_in_fire有效的时候，相对于bpu_in_fire有效时延迟一个周期写入。
写入数据：写入f_to_send

entry_hit_status：记录每个FTQ项拿到的分支预测结果是否是ftb entry hit的（链接），即生成该分支预测结果的时候是否是从FTB ( [预测结果生成：hit](https://open-verify.cc/xs-bpu/docs/modules/03_ftb/))(其实不需要点开链接了解也没关系)中，读取到了对应的记录表项。初始化为not_hit状态。
写入时机：当来自BPU的全局分支预测信息中s2阶段的分支预测结果有效时，写入s2阶段分支预测结果中指名的hit状态，因为FTB预测器是分支预测s2阶段开始生效的，在此时判断预测项是否在FTB缓存中命中

newest_entry_ptr，newest_entry_target这几个内部信号，它们不是队列，但是它们很重要，表明我们当前应该关注的最新的FTQ项及对应的跳转目标。BPU新的写入，重定向等等都会对最新FTQ项进行新的安排，在相应的文档中，对其生成方式做具体的描述。