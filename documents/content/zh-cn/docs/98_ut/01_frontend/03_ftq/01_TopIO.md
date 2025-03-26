---
title: FTQ顶层
linkTitle: 01_FTQ顶层
weight: 12
---

# 简述
在FTQ概述中，我们已经知道了，FTQ的作用就是多个模块交互的中转站，大致了解了它接受其他模块的哪些信息，它如何接受并存储这些信息在FTQ中，并如何把这些存储信息传递给需要的模块。
下面我们来具体了解一下FTQ与其他模块的交互接口，我们会对这种交互有一个更具体的认识。
# IO一览
## 模块间IO
- **fromBpu：接受BPU预测结果的接口（BpuToFtqIO）**
- **fromIfu：接受IFU预译码写回的接口（IfuToFtqIO）**
- **fromBackend：接受后端执行结果和commit信号的接口（CtrlToFtqIO）**
- **toBpu：向BPU发送训练信息和重定向信息的接口（FtqToBpuIO）**
- **toIfu：向IFU发送取值目标和重定向信息的接口（FtqToIfuIO）**
- toICache：向ICache发送取值目标的接口（FtqToICacheIO）
- **toBackend：向后端发送取值目标的接口（FtqToCtrlIO）**
- toPrefetch：向Prefetch发送取值目标的接口（FtqToPrefetchIO）
- mmio
## 其他
上述是主要的IO接口，此外，还有一些用于性能统计的IO接口，比如对BPU预测正确和错误结果次数进行统计，并进行转发的IO, 还有转发BPU各预测器预测信息的IO。

# [BpuToFtqIO](https://open-verify.cc/xs-bpu/docs/ports/02_global_ports/)

# IfuToFtqIO
我们知道从IFU，我们会得到预译码信息和重定向信息，而后者其实也是从预译码信息中生成。所以从IFU到FTQ的接口主要就是用来传递预译码信息的
- pdWb：IFU向FTQ写回某个FTQ项的预译码信息
	- 接口类型：**PredecodeWritebackBundle**
	- 信号列表：
		- pc：一个分支预测块覆盖的预测范围内的所有pc
			- 接口类型：Vec(PredictWidth, UInt(VAddrBits.W))
		- pd：预测范围内所有指令的预译码信息
			- 接口类型：Vec(PredictWidth, new PreDecodeInfo)
			-  PreDecodeInfo：每条指令的预译码信息
				- 接口类型：PreDecodeInfo
				- 信号列表：
					- valid：预译码有效信号
						- 接口类型：Bool
					- isRVC：是RVC指令
						- 接口类型：Bool
					- brType：跳转指令类型
						- 接口类型：UInt(2.W)
						- 说明：根据brType的值判断跳转指令类型
							- b01：对应分支指令
							- b10：对应jal
							- b11：对应jalr
							- b00：对应非控制流指令
					- isCall：是Call指令
						- 接口类型：Bool
					- isRet：是Ret指令
						- 接口类型：Bool
		- ftqIdx：FTQ项的索引，标记写回到哪个FTQ项
			- 接口类型：FtqPtr
		- ftqOffset：由BPU预测结果得到的，在该指令块中指令控制流指令的位置（指令控制流指令就是实际发生跳转的指令）
			- 接口类型：UInt(log2Ceil(PredictWidth).W)
		- misOffset：预译码发现发生预测错误的指令在指令块中的位置
			- 接口类型：ValidUndirectioned(UInt(log2Ceil(PredictWidth).W))
			- 说明：它的valid信号拉高表示该信号有效，也就说明存在预测错误，会引发重定向
		- cfiOffset：由预译码结果得到的，在该指令块中指令控制流指令的位置（指令控制流指令就是实际发生跳转的指令）
			- 接口类型：ValidUndirectioned(UInt(log2Ceil(PredictWidth).W))
		- target：该指令块的目标地址
			- 接口类型：UInt(VAddrBits.W)
			- 说明：所谓目标地址，即在指令块中有控制流指令时，控制流指令的地址，在没有控制流指令时，指令块顺序执行，该指令块最后一条指令的下一条指令
		- jalTarget：jal指令的跳转地址
			- 接口类型：UInt(VAddrBits.W)
		- instrRange：有效指令范围
			- 接口类型：Vec(PredictWidth, Bool())
			- 说明：表示该条指令是不是在这个预测块的有效指令范围内（第一条有效跳转指令之前的指令） 
# CtrlToFtqIO

后端控制块向FTQ发送指令提交信息，后端执行结果的接口。
- rob_commits：一个提交宽度内的RobCommitInfo信息。
	- 接口类型：Vec(CommitWidth, Valid(new RobCommitInfo))
	- 详情链接：RobCommitInfo
- redirect：后端提供重定向信息的接口。
	- 接口类型：Valid(new Redirect)
	- 详情链接：Redirect
- ftqIdxAhead：提前重定向的FTQ指针，将要重定向的FTQ项的指针提前发送
	- 接口类型： Vec(BackendRedirectNum, Valid(new FtqPtr)) 
	- 说明：虽然有三个接口，但实际上只用到了第一个接口，后面两个弃用了
- ftqIdxSelOH：独热码，本来是依靠该信号从提前重定向ftqIdxAhead中选择一个，但现在只有一个接口了，独热码也只有一位了。
	- 接口类型：Valid(UInt((BackendRedirectNum).W))
	- 说明：为了实现提前一拍读出在ftq中存储的重定向数据，减少redirect损失，后端会向ftq提前一拍（相对正式的后端redirect信号）传送ftqIdxAhead信号和ftqIdxSelOH信号。
# [FtqToBpuIO](https://open-verify.cc/xs-bpu/docs/ports/02_global_ports/)
# FtqToICacheIO
FTQ向IFU发送取值目标，ICache是指令缓存，如果取值目标在ICache中命中，由ICache将指令发给IFU
- req：FTQ向ICache发送取值目标的请求
	- 接口类型：Decoupled(new FtqToICacheRequestBundle)
	- 信号列表：
		- pcMemRead：FTQ针对ICache发送的取值目标，ICache通过5个端口同时读取取指目标
			- 接口类型：Vec(5, new FtqICacheInfo)
			- FtqICacheInfo: FTQ针对ICache发送的取值目标
				- 信号列表：
					- ftqIdx：指令块在FTQ中的位置索引
						- 接口类型：FtqPtr
					- startAddr：预测块起始地址
						- 接口类型：UInt(VAddrBits.W)
					- nextlineStart：起始地址所在cacheline的下一个cacheline的开始地址
						- 接口类型：UInt(VAddrBits.W)
					- 说明：通过startAddr(blockOffBits - 1)这一位（也就是块内偏移地址的最高位）可以判断该预读取pc地址是位于cacheline的前半块还是后半块，若是前半块，由于取值块大小为cacheline大小的一半，不会发生跨cacheline行
		- readValid: 对应5个pcMemRead是否有效
		- backendException：是否有后端异常
# FtqToCtrlIO
FTQ向后端控制模块转发PC，后端将这些pc存储在本地，之后直接在本地读取这些pc
**写入后端pc mem**
- pc_mem_wen：FTQ向后端pc存储单元pc_mem写使能信号
	- 接口类型：Output(Bool())
- pc_mem_waddr：写入地址
	- 接口类型：Output(UInt(log2Ceil(FtqSize).W))
- pc_mem_wdata：写入数据，是一个指令块的取值目标
	- 接口类型：Output(new Ftq_RF_Components)，详见FTQ子队列相关介绍
**写入最新目标**
- newest_entry_en：是否启用
	- 接口类型：Output(Bool())
- newest_entry_target：最新指令块的跳转目标
	- 接口类型：Output(UInt(VAddrBits.W))
- newest_entry_ptr：最新指令块的索引值
	- 接口类型： Output(new FtqPtr)
# FtqToPrefetchIO
- req：FTQ向Prefetch发送取值目标的请求
	- 接口类型：FtqICacheInfo
- flushFromBPU: 来自BPU的冲刷信息
	- 接口类型：BpuFlushInfo
	- 信号列表：
		- s2 ：BPU预测结果重定向（注意这种重定向是BPU自己产生的，与其他类型要做区分）发生在s2阶段时，此阶段的分支预测块的索引
			- 接口类型：Valid(new FtqPtr)
			- 说明：valid信号有效时，说明此时s2流水级分支预测结果与其s1阶段预测结果不一致，产生s2阶段重定向
		- s3：BPU预测结果重定向（注意这种重定向是BPU自己产生的，与其他类型要做区分）发生在s3阶段时，此阶段的分支预测块的索引
			- 接口类型：Valid(new FtqPtr)
			- 说明：与s2类似
		- 说明：发生预测结果重定向的时候，预取单元和IFU都可能会被冲刷，比如，如果发生s2阶段重定向，FTQ会比较发给IFU req接口中的ftqIdx和s2阶段预测结果的ftqIdx，如果s2阶段的ftqIdx不在req的ftqIdx之后，这意味着，s2阶段产生的预测结果重定向之前的错误预测结果s1阶段预测结果被发给IFU进行取指了，为了消除这种错误，需要向IFU发送s2阶段flush信号。
- backendException：后端执行发生的异常
	- 接口类型：UInt(ExceptionType.width.W)
	- 说明：表示后端执行时发生异常的类型，有这样几种类型的异常：
		
```scala
def none:  UInt = "b00".U(width.W)
def pf:    UInt = "b01".U(width.W) // instruction page fault
def gpf:   UInt = "b10".U(width.W) // instruction guest page fault
def af:    UInt = "b11".U(width.W) // instruction access fault
```