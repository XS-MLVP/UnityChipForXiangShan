# Decode 单元验证

## 测试目标

解码单元的功能是对输入的指令进行解码，最终转换为后端可识别的微指令。输出的指令有两种类型：16位的压缩指令（RVC） 和 32位的普通指令（RVI）。本单元测试的主要目的是**检查Dcode模块是否能识别所有非法指令**。

测试基本流程为：

1. 随机生成指令
1. 把指令输给DUT，得到解码结果（结果种包含是否为异常指令）
1. 把指令输给disasm，判断能否正常解析（disasm为RISC-V官方反汇编工具，可以认为 Golden）
1. 对比DUT和disasm的结果判断是否一致


## 测试环境 Env

本测试基于disasm对 DUT 进行了封装。输入的DUT模块为 `ut.predecode`,`ut.decodestage` 和 `ut.rvcexpander` 三个模块。

- **ut.rvcexpander**
在 env 环境中，通过RVCExpander对DUT进行了封装，提供指令展开接口。

- **ut.predecode**
[TBD]

- **ut.decodestage**
[TBD]


依赖：
- disasm 反汇编工具 （该工具位置为 tools.disasm）

## 功能检查点

本测试需要进行的功能点和检查点（checkpoint/coverpoint）如下（该部分建议以注释的形式写入funcov）：

|序号|涉及模块|功能描述|检查方法|检查点名称|
|-|-|-|-|-|
|1|rvcexpander|压缩指令展开|检查是否有非法判断|RVC_EXPAND_RET|
|1|rvcexpander|压缩指令展开|检查所有正常指令是否都覆盖到|RVC_EXPAND_16B_RANGE|
|2||           |检查所有非法指令是否都覆盖到|同上|
|3|rvcexpander|常规指令展开|检查随机输入得指令，<br>每一位是否都被覆盖过<br>eg: ins[7] == 1|RVC_EXPAND_32B_BITS|
|5|TBD|           |-|-|

检查点细分（Bins，一个检查点由多个bin组成，只有所有bin都触发，该检查点才算被覆盖）：
- RVC_EXPAND_RET
    - ERROR expander 得非法检查返回 0
    - SUCCE expander 得非法检查返回 1
- RVC_EXPAND_16B_RANGE
    - RANGE[start-end] 16为指令公有 2^16种可能，需要start-end覆盖整个16bit的取值范围
- RVC_EXPAND_32B_BITS
    - POS_(0-31)

## Env提供的验证接口(API)

为了让测试用例更通用，具有继承性，本Env提供的接口**对外屏蔽了电路引脚和时序，且接口保持稳定**：

#### 1. rvcexpander

```python

# 封装主类
class RVCExpander
    # 对指令指令 instr 进行展开
    # 参数：
    #    instr 输入指令
    # 返回：
    #    value 扩展结果
    #    ilegel 是否非法指令
    def expand(self, instr) -> (value, ilegal):
    # 获取 expander的状态
    # 返回：
    #    {
    #     instr：当前的输入指令
    #     decode: 展开结果
    #     ilegal：输入是否为非法指令
    #     }
    def stat(self) -> dict(instr => int, decode=>int, ilegal => bool):

# 用于自动创建RVCExpander的fixture
@pytest.fixture()
def rvc_expander(request) -> RVCExpander:
```

#### 2. TBD

## 用例说明

本测试创建的用例如下（以下内容建议以funciton doc的形式写入case的具体实现中，然后以link的形式做链接）:

#### 1. test_rv_decode.test_rvc_expand_16bit_smoke 压缩指令展开冒烟测试 

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|选择一条特定压缩指令||[RVC_EXPAND_RET]()|
|2|通过RVCExpander.expand接口获取解码结果||||
||通过disasm获取反汇编结果|||
|3|检查两边的结果是否一致|所有指令是否非法指令判断结果一致|[.SUCCE]()，[.ERROR]()|


#### 2. test_rv_decode.test_rvc_expand_32bit_smoke 普通指令展开冒烟测试 
|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|选择一条特定32位指令||[RVC_EXPAND_RET]()|
|2|通过RVCExpander.expand接口获取解码结果||||
||通过disasm获取反汇编结果|||
|3|检查两边的结果是否一致|所有指令是否非法指令判断结果一致|[.SUCCE]()，[.ERROR]()|


#### 3.test_rv_decode.test_rvc_expand_16bit_full 对所有压缩指令进行展开检查
|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|将16位指令的取值范围拆分为N个分段|-|[1->RVC_EXPAND_RET](), [2->RVC_EXPAND_16B_RANGE]()|
|2|遍历每个分段中的所有值，作为压缩指令|-|[2.RANGE]()|
|3|通过RVCExpander.expand接口获取解码结果|-|-|
||通过disasm获取反汇编结果|||
|4|检查两边的结果是否一致|所有指令是否非法指令判断结果一致|[1.SUCCE]()，[1.ERROR]()|


#### 3.test_rv_decode.test_rvc_expand_32bit_randomN 随机对32位指令进行展开检查
|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|随机运行K次，每次随机生成N个32位指令|-|[1->RVC_EXPAND_RET](), [2->RVC_EXPAND_32B_BITS]()|
|2|遍历N个指令|-|[2.POS_i(0-32)]()|
|3|通过RVCExpander.expand接口获取解码结果|-|-|
||通过disasm获取反汇编结果|||
|4|检查两边的结果是否一致|所有指令是否非法指令判断结果一致|[1.SUCCE]()，[1.ERROR](), |


## 目录结构

```bash
decode
├── README.md                 # 说明文件
├── __init__.py               # python模块文件
├── env                       # 环境模块
│   └── __init__.py
│   └── decode_wrapper.py
└── test_rv_decode.py         # 测试用例
```

## 检查列表

- [ ] 模块 README 包含[模板]()中提到的所有内容
- [ ] Env提供的API不包含任何DUT引脚和时序信息（已对必要情况进行了说明）
- [ ] 功能点（共有[ ]个）与[设计文档]()一致
- [ ] 检查点（共有[ ]个）覆盖所有功能点
- [ ] 检查点的输入不依赖任何DUT引脚，仅依赖Env的标准API
- [ ] Env的API保持稳定（共有[ ]个）
- [ ] 所有测试用例（共有[ ]个）都对功能检查点进行了反标
- [ ] 对行覆盖率过滤需求进行了检查
- [ ] Env中对所支持的RTL版本（支持版本[ ]）进行了检查
