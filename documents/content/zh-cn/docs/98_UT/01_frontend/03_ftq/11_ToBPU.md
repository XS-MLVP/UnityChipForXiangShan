# 简介
FTQ将已提交指令的更新信息发往BPU进行训练，同时转发重定向信息。
# 涉及的顶层IO接口
toBpu
- 向BPU发送重定向信息与更新信息。

fromBackend
- 获取指令交割信息，判断指令块是否被提交

mmioCommitRead
- 发送mmio指令的提交信息
# 转发重定向
向toBPU接口进行转发：
- redirctFromIFU：IFU重定向结果有效（注意：IFU重定向有效的时机有两种说法，因为IFU重定向结果生成需要两个周期，此处取后者，即，IFU重定向生成过程的第二个周期有效，也是IFU生成完整重定向结果的周期）
- redirect：如果后端重定向结果fromBackendRedirect有效，选用fromBackendRedirect，否则选用IFU重定向结果ifuRedirectToBpu
# BPU更新暂停
BPU的更新需要两个周期，故需要三种状态去表明我们当前的更新状态：更新的第一个周期，第二个周期，更新完成（也可以认为是未更新）。
当发生更新的时候，会暂停FTQ对指令块的提交以及发送更新信息。

# 提交指令块
FTQ需要对当前comPtr指向的当前提交指令块，进行判断是否能够提交。
这个过程比较复杂。
由于 香山V2版本 的后端会在 ROB 中重新压缩 FTQ entry，因此并不能保证提交一个 entry 中的每条指令，甚至不能保证每一个 entry 都有指令提交。

**判断一个 entry 是否被提交有如下几种可能**：
- robCommPtr 在 commPtr 之后（ptr更大）。也就是说，后端已经开始提交之后 entry 的指令，在 robCommPtr 指向的 entry 之前的 entry 一定都已经提交完成
- commitStateQueue 中指令块内最后一条有效范围内指令被提交。FTQ项中该指令被提交意味着这FTQ项内的指令已经全部被提交

在此以外，还必须要考虑到，后端存在 flush itself 的 redirect 请求，这意味着这条指令自身也需要重新执行，这包括异常、load replay 等情况。在这种情况下，这一FTQ项不应当被提交以更新 BPU，否则会导致 BPU 准确率显著下降。
## canCommit
具体来看，判断commPtr指向的指令块能否提交，如果可以提交记为canCommit。
- canCommit：
	1. 当commPtr不等于ifuWbPtr，且没有因为BPU更新而暂停，同时robCommPtr在commPtr之后。之所以要求commPtr不等于ifuWbPtr是因为，前面说过了必须先预译码写回FTQ项才能提交
	2. commitStateQueue 中commPtr对应指令块有指令处于c_toCommit 或c_committed状态。且指令块中最后一条处于c_toCommit 或c_committed状态的指令是c_committed的。

这两种情况下，canCommit拉高，说明可以提交该指令块
## canMoveCommPtr
在commPtr指向的指令块如果能提交，那么我们自然可以移动CommPtr只想下一个FTQ项了。但除此之外，commitStateQueue 中commPtr对应指令块的第一条指令被后端重定向冲刷掉了，这表明该指令需要重新执行，这一FTQ项不应被提交，但是却可以更新CommPtr指针，因为该指令块内已经没有可以提交的指令了。
- CanMoveCommPtr时，commPtr指针更新加1（一周期后成功写入）。
## robCommPtr更新
有几种情况
1. 当来自后端接口fromBackend的rob_commits信息中，有信息有效时，取最后一条有效交割信息的ftqIdx
2. 不满足情况1，选取commPtr, robCommPtr中较大的那个
## mmio提交
发往mmioCommitRead接口
- mmioLastCommit：
 1. 当commPtr比来自mmioCommitRead接口的mmioFtqPtr大时， 
 2. 或者两者正好相等，且commPtr指向的指令块中有c_toCommit 或c_committed状态的指令，最后一条处于c_toCommit 或c_committed状态的指令是c_committed的

在这两种情况下，mmioLastCommit信号在下一个周期被拉高
# 发送BPU更新信息
FTQ需要从FTQ子队列中，读取提交项的预测信息，重定向信息，meta信息，用这些信息来对BPU发送更新信息。

当canCommit时，可以提交commPtr指向的指令块时，从ftq_pd_mem，ftq_redirect_mem,ftq_meta_1r_sram_mem这些子队列，以及一些小的状态队列中读出对应指令块的相应信息，这些信息需要专门花一个周期才能读取到。具体来说：

- 从预译码信息子队列ftq_pd_mem中读取提交提交指令块（commptr所指）的预译码信息
- 从取指目标子队列ftq_pc_mem中读取取指信息
- 从分支预测重定向信息子队列ftq_redirect_mem中读取提交指令块的重定向信息。
- 从预测阶段状态队列中读取提交块来自BPU的哪个预测阶段
- 从meta信息子队列ftq_meta_1r_sram中读取提交指令块的meta，和相应的ftb_entry。
- 从提交状态队列commitStateQueueReg中读取提交状态，并确认指令快中哪些指令为c_committed,用bool数组表示
- 从控制流索引状态队列cfiIndex_vec中读取指令控制流指令在块中索引
- 结合错误预测状态队列mispredict_vec，和提交状态队列信息确认指令块中的提交错误指令。(即提交状态指示为c_commited 同时错误预测指示为预测错误)
- 从表项命中状态队列entry_hit_status中读取提交指令块是否命中
- 如果命中状态队列指示命中或者cfi状态队列指示存在cfi指令（该提交块在cfi中有效），该指令块的提交会产生更新信息，并在之后向BPU发送。
- 获取提交块的目标，如果commPtr等于newest_entry_ptr，则取newest_entry_target_modified拉高时的newest_entry_target，否则取ftq_pc_mem.io.commPtrPlus1_rdata.startAddr

整合完上述信息后，FTQ会向toBpu的update接口发送更新请求，具体如下：
- valid：canCommit 且 指令块满足命中或者存在cfi指令，valid接口有效，表明可以发送更新请求
- bits：
	- false_hit：提交块命中状态指示为h_false_hit，该信号拉高
	- pc：提交块的取指信息中的startAddr
	- meta：提交块的meta
	- cfi_idx：提交块中cfi指令的index
	- full_target：提交块的目标
	- from_stage：提交块属于哪个预测阶段
	- spec_info：提交块的meta
	- pred_hit：提交块的命中状态为hit或者false_hit

另外，被更新的FTB表项也会**同时**被转发到更新接口，但是新的FTB表项生成方式相对复杂，下一节专门展开叙述
## 修正FTB项
更新结果会基于旧的FTB项进行更新，然后直接转发给更新接口。你可能需要先阅读[FTB项相关文档](https://open-verify.cc/xs-bpu/docs/ports/00_ftb/)了解FTB项的结构和相关信号生成方式

commit表项的相关信息会被发送给一个名为FTBEntryGen的接口，经过一系列组合电路处理，输出更新后的FTB表项信息。

为了更新FTB项，提交项如下信息会被读取：
- 取值目标中的起始地址 startAddr
- meta中旧FTB项 old_entry 
- 包含FTQ项内32Byte内所有分支指令的预译码信息 pd 
- 此FTQ项内有效指令的真实跳转结果 cfiIndex，包括是否跳转，以及跳转指令相对startAddr的偏移 
- 此FTQ项内分支指令（如跳转）的跳转地址（执行结果） 
- 预测时FTB是否真正命中（旧FTB项是否有效）
- 对应FTQ项内所有可能指令的误预测 mask

接下来介绍如何通过这些信息更新FTB。
 FTB项生成逻辑： 
### **情况1：FTB未命中，则创建一个新的FTB项**
 *我们会根据预译码信息进行判断，预译码会告诉我们，指令块中cfi指令是否是br指令，jmp指令信息（以及是哪种类型的jmp指令）*
 1) 无条件跳转指令处理： 
	 - 不论是否被执行，都一定会被写入新FTB项的tailSlot 
	 - 如果最终FTQ项内跳转的指令是条件分支指令，写入新FTB项的第一个brSlot（目前也只有这一个），对应的strongbias被设置为1作为初始化
2) pftAddr设置： 
	- 存在无条件跳转指令时：以无条件跳转指令的结束地址设置
	- 无无条件跳转指令时：以startAddr+取指宽度（32B）设置
	- 特殊情况：当4Byte宽度的无条件跳转指令起始地址位于startAddr+30时，虽然结束地址超出取指宽度范围，仍按startAddr+32设置
3) carry位根据pftAddr的条件同时设置 
4) 设置分支类型标志： 
	- isJalr、isCall、isRet按照无条件跳转指令的类型设置 
	- 特殊标志：当且仅当4Byte宽度的无条件跳转指令起始地址位于startAddr+30时，置last_may_be_rvi_call位

*详细信号说明*：
- cfiIndex有效（说明指令块存在跳转指令），且pd的brmask指明该指令是br指令。则判断控制流指令是br指令
- pd的jmpinfo有效，且cifIndx有效。则进一步根据jmpinfo判断是那种类型的jmp指令
	1. 最低位为0：jal
	2. 最低为为1：jalr
	3. 第一位为1：call
	4. 第二位为1：ret
- 判断最后一条指令是否是rvi（4byte）的jmp指令：jmpinfo有效，pd中jmpOffset等于15，且pd的rvcMask指明最后一条指令不是rvc指令
- 判断cfi指令是否是jal指令：cfiindx = jmpOffset，且根据之前的判断确认jmp指令是jal指令
- 判断cfi指令是jalr指令也是同理的。

- FTB生成：valid被初始化为true
	- brslot：在判断控制流指令是br指令时，进行填充
		- valid：初始化为true
		- offset：cfiindx
		- lower和stat：根据startaddr和提交块指定的target计算
		- 对应的strongbias：被初始化为true
	- tailslot：pd的jmpinfo有效时，进行填充
		- valid：根据之前的判断确认jmp指令是jal指令或者是jalr指令时，valid有效
		- offset：pd的jmpoffset
		- lower和stat：根据startaddr和target计算，如果cfi指令是jalr指令，使用提交块指定的target，否则用pd预测的jalTarget
		- 对应的strongbias：根据之前的判断确认jmp指令是jalr指令时，拉高。strongbias是针对于BPU的ittage预测器的，该预测器基于一些统计信息工作，strongbias用来指向指令跳转偏好的强弱，其中jal指令不需要记录strongbias。
	- pftAddr：上方介绍已经够详细了
	- carry：上方介绍已经足够
	- isJalr/isCall/isRet
	- last_may_be_rvi_call

### 情况2：FTB命中，修改旧的FTB项
#### 插入brslot的FTB项
*在原来的基础上改动即可，比如插入新的slot，注意，只针对新的brslot*
1. **修改条件**：首先根据oldftbentry判断在旧entry中，cfi指令是否被记录为br指令，如果不是，**则说明这是一个新的br指令**。
2. 接着从旧FTB中判断哪些slot可以被插入slot：
	- brslot：如果旧FTB的brslot无效，表示该slot空闲，此时可以在此位置插入新的brslot，此外，如果新slot在旧slot之前（新的br指令在旧slotbr指令之前执行，或者说在指令块之前的位置），即使不空也能插入
	- tailslot：当不能在brslot插入时，才考虑tailslot，同样，在该slot空闲或者新slot在旧slot之前，可以插入此位置
3. 插入slot：
	1. brslot：能插入时则在这里插入，不能的时候，把对应的strongbias拉低，因为这说明新slot一定在旧slot之后（如果不想要详细了解ittage的原理可以不用理解原因）。
	2. tailslot：能插入时则在这里插入，不能的时候，如果新slot在旧slot之后，把对应的strongbias拉低，如果不在之后，当原brslot有效（即不空闲），则用插入前的brslot代替该tailslot。对应的strongbias维持不变。

*注：tailslot不能插入且新slot在其之前，其实就已经说明brslot一定是可以插入的，所以才有后面的替代*

***pftaddr***
出现新的br指令，同时旧的FTB项内没有空闲的slot，这说明确实发生了在FTB项内确实发生了FTB项的替换，pftaddr也需要做相应的调整。
- 如果没有能插入的位置，使用新的br指令的偏移作为pftaddr对应的偏移，因为此时，新br指令一定在两个slot之后。否则，使用旧FTB项的最后一个slot的offset。将ptfoffset结合startAddr得到最后的pftAddr，carry也进行相应的设置。
- last_may_be_rvi_call，isCall，isRet ，isJalr全部置false。
#### 修改jmp target的FTB项
**修改条件**：**当cfi指令是一个jalr指令**，且旧的tailslot对应的是一个jump的指令，但tailslot指示的target与提交项指示的target不同时，说明需要对跳转目标进行修改。
- 根据正确的跳转目标对lower和stat进行修改
- 两位strongbias设置成0
#### 修改bias的FTB项
**当cfi指令就是原FTB项的条件跳转指令**，只需要根据跳转情况设置跳转的强弱
- brslot：旧的brslot有发生跳转时，bias在原bias拉高，发生跳转的cfiindex等于该slot的offset，brslot有效时，保持拉高，其余情况拉低。
- tailslot：旧的brslot没有跳转，而tailslot有分支指令且发生跳转，把brslot的bias置为false，tailslot保持bias的方式与上面的brslot一致。

**修改条件**：当旧的bias拉高且对应的旧的FTB项中的slot中有分支指令，同时修改后的bias拉低。任何一个slot出现这种情况都需要进行修改。

最后，需要抉择出一个修改的FTB项
- 如果cfi是一个新的分支指令，我们采用插入新的slot的FTB项。
- 如果是cfi是一个jalr指令，且跳转目标发生修改，我们采用修改jmp跳转目标的FTB项
- 如cfi指令就是原FTB项的条件跳转指令，采用修改bias的FTB项

### 得到更新的FTB项
此时，根据是否hit，我们已经得到更新后的FTB项了，在这个基础上我们继续更新一些相关信号以发送到FTQ更新接口。
- new_br_insert_pos：使用之前我们判断的FTB项中可插入位置的bool数组
- taken_mask：根据cfi指令在更新后FTB项的位置判断，只有分支指令才做此计算，若是jmp指令置为0。
- jump_taken: cfi指令在更新后FTB项的taislot，且jmpValid。
- mispred_mask的最后一项：更新后的FTB项jumpValid，且预译码推断的jmp指令在提交项的错误预测信息中指示错误。
	- **mispred_mask** 预测块内预测错误的掩码。第一、二位分别代表两个条件分支指令是否预测错误，第三位指示无条件跳转指令是否预测错误。
	    - 接口类型：`Vec(numBr+1, Bool())`
- old_entry：如果hit，且FTB项不做任何修改，即不满足上述三种修改FTB项的条件，拉高该信号，说明更新后的FTB项是旧的FTB项。
### 发送处理后的更新信息
此时，我们就可以向BPU发送处理好的更新信息了，下面是update的接口接收的信号
- ftb_entry：更新后的FTB项
- new_br_insert_pos：上一小节已述
- mispred_mask：上一小节已述
- old_entry：上一小节已述
- br_taken_mask: 上一小节已述
- br_committed：根据提交项的提交状态信息判断新FTB项中的有效分支指令是否已经提交
- jmp_taken：上一小节已述
