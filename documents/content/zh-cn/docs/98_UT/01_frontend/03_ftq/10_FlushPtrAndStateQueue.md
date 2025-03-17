# 简介
之前讲了，后端和IFU重定向写回会修改一些状态队列。此外，FtqPtr也是一种比较重要的维护信息。由后端或者IFU引起的重定向，需要恢复各种类型用来索引FTQ项的FtqPtr。而当重定向是由后端发起的时候，还要修改提交状态队列，说明指令已经被执行。

# 流程
后端和IFU的重定向信号都会冲刷指针，更具体的来说：
- 后端写回接口fromBackend有效，或者IFU重定向有效：当预译码写回pdWb有效，且pdWb的missOffset字段有效表明存在预测错误的指令，同时后端冲刷信号backendFlush无效时。（参考：从IFU重定向的第一个周期，重定向valid值有效条件）

第一个周期：
- 冲刷指针：确认后端和IFU的重定向信号可能冲刷指针时，从两个重定向来源的redirect接口读出重定向信息，包括ftqIdx，ftqOffset，重定向等级RedirectLevel。有两个来源时，优先后端的重定向信息。
	冲刷指针列表：
	- bpuPtr：ftqIdx+1
	- ifuPtr：ftqIdx+1
	- ifuWbPtr：ftqIdx+1
	- pfPtr：ftqIdx+1
	*注：只是在当前周期向指针寄存器写入更新信息，实际生效是在下一个周期。*
	这样一来，所有类型指针当前指向的都是发生重定向的指令块的下一项了，我们从这一项开始重新进行分支预测，预译码，等等。	

第二个周期：
 如果上一个周期的重定向来源是后端，FTQ会进一步更改提交状态队列
 - 提交状态队列中，对于重定向的指令块（通过ftqIdx索引），位于ftqOffset后面的指令的状态被设置为c_empty
 - 对于正好处于ftqOffset的指令，判断RedirectLevel，低表示在本位置后flush，高表示在本位置flush，所以level为高时，对于的指令提交状态被设置为flush。

## IO转发
实际上，在发生重定向的时候，还涉及一些将重定向信息通过FTQ顶层IO接口转发给其他模块的操作，比如ICache需要flush信号取进行冲刷，IFU也需要后端的重定向信号对它进行重定向，具体来说：
在**流程**的第一个周期：
- flush信号顶层IO转发（icacheFlush）：
	- 确认后端和IFU的重定向信号可能冲刷指针时，拉高FTQ顶层IO接口中的icacheFlush信号，把重定向产生的flush信号转发给ICache
- 重定向信号顶层IO转发（toIFU）：
	- redirect：
		- bits：接收来自后端的重定向信号
		- valid：后端的重定向信号有效时有效，维持到下个周期依然有效

## 重排序缓冲区提交
其实，除了后端重定向会更新提交状态队列，最直接的更新提交状态队列的方式是通过FTQ顶层IO中frombackend里提供的提交信息，rob_commits告知我们哪些指令需要被提交。

rob_commits的valid字段有效，可以根据其中信息对指令进行提交，修改状态队列。对于被执行的指令，是如何提交的，如何对应地修改提交状态队列，有两种情况：
1. 对于普通指令，根据rob_commits的ftqIdx和ftqOffset索引提交状态队列中的某条指令，将对应的提交状态设置为c_commited
	1. 对于融合指令，根据提交类型commitType对被索引的指令和另一与之融合的指令进行提交，将对应的提交状态设置为c_commited
		1. commitType = 4：同时把被索引指令的下一条指令设为c_commited
		2. commitType = 5：同时把被索引指令的之后的第二条指令设为c_commited
		3. commitType = 6：同时把被指令块的下一个指令块的第0条指令设为c_commited
		4. commitType = 7：同时把被指令块的下一个指令块的第1条指令设为c_commited