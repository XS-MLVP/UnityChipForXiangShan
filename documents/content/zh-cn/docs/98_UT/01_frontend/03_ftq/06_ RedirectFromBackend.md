---
title: 从后端重定向
linkTitle: 从后端重定向
weight: 12
---

# 简介
FTQ重定向信息有两个来源，分别是IFU 和 后端。两者的 重定向接口大致相似，但重定向的过程有一定区别。

对于重定向，后端有提前重定向机制，为了实现提前一拍读出在ftq中存储的重定向数据，减少redirect损失，后端会向ftq提前一拍（相对正式的后端redirect信号）传送ftqIdxAhead信号和ftqIdxSelOH信号。ftqIdxSelOH信号出现的原因，是早期版本要读多个ftqIdxAhead信号，以独热码的形式选其中一路作为最终确认的提前索引值，但现在只需要从一个端口获取ftqIdx信号了，ftqIdxAhead只能确认这一个端口了。

# 流程
第一个周期：
- 后端重定向写回时，首先会从后端到FTQ的IO接口（CtrltoFtqIO）中，看ftqIdx是不是有效信号，且此时后端正式重定向信号redirect无效(因为提前重定向会比正式重定向提前一拍，所以此时正式重定向无效)，这时，提前重定向信号aheadValid有效, 将使用提前获取的重定向ftqIdx，
第二个周期：
- 如果此时后端正式重定向信号有效了，且ftqIdxSelOH拉高，说明在正式重定向阶段成功对ftqIdxAhead信号进行选中，同时上一周期重定向信号aheadValid是有效的，则真实提前重定向信号realAhdValid拉高，在此时读取
第三个周期：
- 该周期会把来自后端的重定向信息的存储一份在寄存器backendRedirectReg中，具体的来说，当上一个周期后端重定向有效时，将后端重定向bits字段（存储实际内容）被写入寄存器的bits字段。
- 而实际决定信号是否有效的valid字段（决定该信号是否有效）则在上一周期真实提前重定向信号有效（表示确实使用了提前重定向的ftqIdx进行重定向）的情况下，被写入false，因为提前重定向发生时，我们直接使用当前的后端重定向信号交给FTQ就可以了。而不需要多保存一个周期。
- 真实提前重定向信号无效时，则由上一周期后端正式重定向的有效值决定，只有信号有效时，我们才需要把它存下来，之后交给FTQ。

**信号抉择**：
是提前获取后端重定向信息还是延迟一个周期从寄存器内读取？
真实重定向有效时，直接将后端重定向信息传递给FTQ，否则，取重定向寄存器内的信号作为重定向信息传递给FTQ，相当于晚一个周期发送重定向信息。最后被选择的重定向信息作为**后端重定向结果fromBackendRedirect**发送给FTQ

接下来讲讲后端重定向在这三个周期到底通过ftqIdx到底读了哪些FTQ子队列中的信息，以及怎么使用它们。

**后端重定向读取的子队列：**
- ftq_redirect_mem：FTQ会根据后端重定向提供的ftqIdx读出ftq_Redirect_SRAMEntry，借助它提供的信息重定向到之前的状态。
- ftq_entry_mem：读出重定向指令块对应的FTB项
- ftq_pd_mem：读出重定向指令块的预译码信息

**读子队列时序：**
第一个周期：
- 提前重定向信号有效时，将子队列的读端口，读有效信号拉高，输入ftqIdxAhead的value字段作为读地址，发起读取请求。

第二个周期：
- case1. 如果第一周期的提前重定向无效，而现在正式重定向有效，则在此时才拉高读有效信号，使用正式重定向接口的ftqIdx作为读取地址，发起读取请求。
- case2. 真实提前重定向有效了，此时因为前一个周期已经发起读取请求，此时可以直接从子队列的读端口读出了

第三个周期
- 真实提前重定向无效，但至少前一个周期正式重定向发起的读取请求能保证在当前周期从子队列中读出。

**处理读取信息**
*FTQ会将从子队列中读出的信息整合到fromBackendRedirect中。*
具体来说：
- 重定向redirect接口的CfiUpdateInfo接口直接接收ftq_Redirect_SRAMEntry中的同名信号。
- 利用fromBackendRedirect中指示的ftqOffset读取指令块预译码信息中实际跳转指令的预译码信息，该ftqOffset为后端执行过后确定的控制流指令在指令块内的偏移。
	- 得到的预译码信息被直接连接到CfiUpdateInfo接口的pd接口中
- 对于读出的指令块对应的FTB项，我们可以从中得知实际执行时得到的跳转指令，是否在FTB项被预测为跳转指令，或者是被预测为jmp指令，如果是，则cfiUpdateInfo的br_hit接口或者jr_hit接口被拉高，表示对应的分支预测结果正确了。
	- 具体来说：通过发送ftqOffset，ftb项以brIsSaved的方式判断是否br_hit，判断是否jr_hit的方式也是类似的（r_ftb_entry.isJalr && r_ftb_entry.tailSlot.offset === r_ftqOffset）。
	- 在CfiUpdateInfo接口设置为br_hit的时候，还会根据这条发生跳转的分支指令是哪个槽从ftq_Redirect_SRAMEntry重定向接口的sc_disagree统计SC预测错误用的性能计数器中，获取对应值，最后整合到后端重定向接口中（如果没有br_hit，对应计数器的两个值都为0）。

