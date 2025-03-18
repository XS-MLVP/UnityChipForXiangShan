---
title: 从BPU进入FTQ
linkTitle: 从BPU进入FTQ
weight: 12
---

# 来自BPU

## 新的预测块进队条件：
新的BPU预测块进入FTQ队列中要满足两个条件，一个是来自BPU的接收接口fromBpu的成功接收数据，一个是要根据是否有重定向信号判断是否允许BPU入队
### **成功接收数据**
- FTQ准备好接收信号：
     当FTQ队列中元素小于FtqSize或者可以commit的时候可以提交指令块（canCommit，在后面的文档中介绍怎么判断是否可以提交指令块）的时候，来自BPU的新的指令预测块可以进入FTQ队列，队列准备好接收新的预测块，fromBpu的resp接口ready信号拉高。

- BPU准备好要发送的信号：

     当BPU发往FTQ的接口vaid信号拉高，表示发送信号准备好

满足以上两个条件时,fromBpu的resp接口，表示接口数据被成功发送到FTQ中。
### **允许BPU入队allowBpuIn**
- 重定向发生时，会回滚到之前的状态，新发送的BPU预测信息自然就不需要了。**允许BPU入队**时不能发生重定向
	1. 后端重定向发生：
		- 标志：接收后端写回信息的接口fromBackend的重定向接口redirect有效，则该周期不允许入队，如果没有发生真实提前重定向，则下一个周期也不允许入队。
	2. IFU重定向发生：
		- 标志：IFU重定向信息生成的两个周期，均不许入队

	只要避免上述两种重定向出现的情况，就可以允许BPU入队
### 以BPU预测结果重定向的方式入队
上述的BPU入队方式是一个全新的预测块进队，即BPU分支预测的s1阶段结果入队，此时未发生预测结果重定向。

当BPU发生预测结果重定向时，只要**允许BPU入队allowBpuIn**，也可以看作预测结果入队，不过这种入队是覆写队列中已有的FTQ项，没有写入新的指令块。
- BPU预测结果发生重定向的具体标志：fromBpu的resp接口的s2（s2阶段的预测信息）有效，且s2的hasRedirect拉高，表示在s2阶段发生了重定向，s3阶段重定向是一样的。

***综合两种形式的BPU入队，这里称之为广义BPU入队方便区分，记为bpu_in_fire。***

## 写入FTQ项
之前已经说明过了，FTQ项只是一个抽象的概念，FTQ有很多个子队列组成，它们的项共同构成一个FTQ项，所以，向FTQ中写入FTQ项，实际上就是就是把BPU的预测信息写到对应的FTQ子队列中。

FTQ主要获取以下信息作为bpu_in_resp
- bpu_in_resp：BPU交给FTQ的resp详见BPU文档，resp中含有s1,s2,s3三个阶段的指令预测信息，bpu_in_resp将获取其中某一阶段预测信息selectedResp作为其值。未发生重定向时，使用s1作为预测结果，s2或者s3发生重定向信息时，优先s3的预测信息作为selectedResp。某阶段发生重定向的标志与上文讲述的一样一样。
从selectedResp（bpu_in_resp）中，我们还可以获取以下目标信息帮助我们写入子队列：ftq_idx，帮助我们索引写入子队列的地址

### 存储接收信息写入FTQ子队列：

- ftq_pc_mem: 来自BPU的selectedResp预测信息被写入ftq_pc_mem, 该存储结构有ftqsize个表项，对应队列中的所有ftq表项，每个存储元素可以推出对应的ftq表项中每条指令的pc地址
	接收信号列表：
	- wen：接收bpu_in_fire作为写使能信号
	- waddr：接收selectedResp的ftq_idx
	- wdata：selectedResp的相应信号

- ftq_redirect_mem: 在BPU的s3（也就是最终阶段）接收信息，因为重定向信息只有在s3阶段才能得到。里面存储了RAS重定向相关的信息帮助BPU进行重定向。
	接收信号列表：
	- wen：从BPU（fromBpu）回应（resp）的lastStage有效信号
	- waddr：从BPU回应的lastStage的ftq_idx.value
	- wdata：从BPU回应的last_stage_spec_info

- ftq_meta_1r_sram：在 BPU的s3阶段接收信息，同样是因为对于一个指令预测块，只有在其s3阶段才能获取完整的mata信息，同样被接收的还有最后阶段ftqentry信息
	接收信号列表：
	- wen：从BPU（fromBpu）回应（resp）的lastStage有效信号
	- waddr：从BPU回应的lastStage的ftq_idx的value
	- wdata：
		- meta：从BPU回应的last_stage_meta
		- ftb_entry：从BPU回应的last_stage_ftb_entry

- ftb_entry_mem：虽然ftq_meta_1r_sram中存储有最后阶段ftbentry，但此处出于更高效率读取专门把它存在ftb_entry_mem中。
	接收信号列表：
	- wen：从BPU（fromBpu）回应（resp）的lastStage有效信号
	- waddr：从BPU回应的lastStage的ftq_idx的value字段
	- wdata：从BPU回应的last_stage_ftb_entry
从中可以看到，FTQ虽然名字上听起来是一个队列，**实际上内部却是由数个队列组成**，他们共同构成了FTQ这个大队列
### 写入状态队列
上述存储结构是FTQ中比较核心的存储结构，实际上，还有一些子队列用来存储一些状态信息，也同样都是存储ftqsize个（64）元素，需要被写入，写入时机是在发生bpu_in_fire的下一个周期，或者再下一个周期 v。主要有以下：

update_target：记录每个FTQ项的跳转目标，跳转目标有两种，一种是当该FTQ项对应的分支预测结果中指明的该分支预测块中执行跳转的分支指令将要跳转到的地址，另一种则是分支预测块中不发生跳转，跳转目标为分支预测块中指令顺序执行的下一条指令地址。
- 此外，与之配套的还有newest_entry_target，newest_entry_ptr用来指示bpu_in_resp推出的跳转目标地址，表示下一次预测时开始的目标地址，和它对应的bpu_in_resp指令预测块在FTQ中的位置。
	- 同时，有辅助信号newest_entry_target_modified和newest_entry_ptr_modified用来标识该这两个字段是否被修改。
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：bpu_in_resp.getTarget

cfiIndex_vec：记录每个FTQ项的发生跳转的指令cfi（control flow instruction）指令在其分支预测块中的位置
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：bpu_in_resp推断出的跳转目标

mispredict_vec：记录每个FTQ项的所有指令的预测结果是否有误，初始化为false
- 写入时机：相对于bpu_in_fire有效时延迟两个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：将该指令块的所有预测结果对应的值设置为false

pred_stage：记录每个FTQ项的分支预测结果是来自于哪个阶段
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址

pred_s1_cycle：记录每个FTQ项的分支预测结果对应的s1阶段的分支预测结果生成的时间（cycle数）
- 写入时机：相对于bpu_in_fire有效时延迟两个周期写入。
- 写入地址：bpu_in_resp记录的要写入FTQ的地址

commitStateQueueReg：记录每个FTQ项中对应的分支预测块中每条指令（一般是16条rvc指令，对应一个预测宽度）的提交状态，提交状态有c_empty ，c_toCommit ，c_committed ，c_flushed，依次用从小到大的枚举量表示，初始化为c_empty状态
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入数据：写入c_empty
- 写入地址：bpu_in_resp记录的要写入FTQ的地址

entry_fetch_status：记录每个FTQ项的分支预测结果是否被送到ifu中，该状态由两个枚举量f_to_send ， f_sent来表示, 初始化为f_sent状态。
- 写入时机：相对于bpu_in_fire有效时延迟一个周期写入。
- 写入数据：写入f_to_send
- 写入地址：bpu_in_resp记录的要写入FTQ的地址

entry_hit_status：记录每个FTQ项拿到的分支预测结果是否是ftb entry hit的，即生成该分支预测结果的时候是否是从ftb中，读取到了对应的记录表项。初始化为not_hit状态。
- 写入时机：当来自BPU的全局分支预测信息中s2阶段的分支预测结果有效时，写入s2阶段分支预测结果中指名的hit状态
- 写入地址：bpu_in_resp记录的要写入FTQ的地址
- 写入数据：f_to_send

注：之所以延迟时钟周期写入，是为了缩短关键路径，以及帮助减少扇出
### **转发分支预测重定向**：
**转发给IFU**:
- s2以及s3阶段的预测重定向信息通过FTQ与Ifu的接口toIfu的flushFromBpu发送给IFU，当完整分支预测结果中的s2阶段分支预测结果发生预测结果重定向时，flushFromBpu.s2.valid拉高，flushFromBpu.s2.bits接收s2阶段分支预测结果中指明的该分支预测结果在FTQ中的位置ftq_idx。

**转发给预取**
- 该重定向信号同样会通过toPrefetch.flushFromBpu接口以相同的方式传递给Prefetch
s3阶段向IFU以及Prefetch的重定向传递与s2阶段的重定向信号传递一样。该阶段的重定向信号传递会覆盖可能的s2阶段重定向信号传递结果

**修正FTQ指针**
此外，分支预测结果重定向也会影响ifuPtr与pfPtr两个指针信号的写入信号。
- 正常情况下，allowToIfu（条件和allowToBpu一样），同时BPU向Ifu发送FTQ项的io接口toIfu.req发生fire的时候，ifuPtr寄存器中写入ifuPtr+1。同样发生修改的还有pfPtr，当allowToIfu，同时BPU向Prefetch发送FTQ项的io接口totoPrefetch.req发生fire的时候。
- 而如果是发生重定向的时候，比如s2阶段预测结果发生重定向，此时，若ifuPtr不在s2阶段预测结果中指明的ftq_idx之前，ifuPtr写入该ftq_idx，pfPtr_write同样如此

**bpuptr**：
由FTQ交给BPU用于指示新的指令预测块应该放到FTQ队列中的位置，上述存储结构，ftq_pc_mem，ftq_redirect_mem，ftq_meta_1r_sram，ftb_entry_mem基本上也是通过与该指针相关的信号得知信息应该存储的addr（bpuptr交给BPU，BPU基于此获知每个阶段预测结果的ftq_idx）。

bpuptr寄存器的输出值直接连到FTQ发往BPU的接口toBpu的enq_ptr字段中，当然，再次之前，bpuptr的值会根据实际情况修改。

在enq from bpu的过程中，正常情况下，发生enq的时候，也就是新的预测块进队时，bpuptr+1，BPU将要向FTQ中写入的位置前进一位

但是，如果发生重定向的时候，比如，如果s2阶段预测结果发生重定向，bpuptr被更新为s2阶段分支预测结果的ftq_idx+1，表示BPU将要向FTQ中写入的位置为s2阶段预测结果在FTQ中位置的后一位，因为此时新的全局预测结果会基于s2的预测结果展开下一轮预测（即以s2分支预测块的下一块展开预测，自然会被写入），该结果会覆盖enq_fire发生时的结果，此外s3阶段的分支预测重定向时，会覆盖可能的s2阶段重定向修改的bpuptr

其他的ftq指针也是类似的，用于指示写入FTQ的地址