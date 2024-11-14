# Decode 单元验证

## 测试目标

解码单元的功能是对输入的指令进行解码，最终转换为后端可识别的微指令。输出的指令有两种类型：16位的压缩指令（RVC） 和 32位的普通指令（RVI）。本单元测试的主要目的是**检查Dcode模块是否能识别所有非法指令**。

测试基本流程为：

1. 随机生成指令
1. 把指令输给DUT，得到解码结果（结果种包含是否为异常指令）
1. 把指令输给disasm，判断能否正常解析（disasm为RISC-V官方反汇编工具，可以认为 Golden）
1. 对比DUT和disasm的结果判断是否一致


## 测试环境 Env

本测试基于disasm对 DUT 进行了封装。输入的DUT模块为 `ut.predecode`,`ut.decodestage` 和 `ut.rvcexpander` 三个模块。[TBD]

依赖：
- disasm 反汇编工具 （该工具位置为 tools.disasm）

## 功能检查点

本测试需要进行的功能点和检查点（checkpoint/coverpoint）如下（改部分建议以注释的形式写入funcov）：

|序号|功能描述|检查方法|检查点名称|
|-|-|-|-|
|1|压缩指令解码|检查所有正常指令是否都覆盖到|CK_RVC_LEGAL|
|2|           |检查所有非法指令是否都覆盖到|CK_RVC_ILLEG|
|3|常规指令解码|检查所有正常指令是否都覆盖到|CK_RVI_LEGAL|
|4|           |检查所有非法指令是否都覆盖到|CK_RVI_LEGAL|

检查点细分（Bins）：
- CK_RVC_LEGAL
    - LOAD 所有 load指令是否
    - STOR 所有 store指令是否覆盖
    - 【TBD】
- CK_RVC_ILLEG
    - 【TBD】
- CK_RVI_LEGAL
    - 【TBD】
- CK_RVI_ILLEG
    - 【TBD】

## Env提供的验证接口

为了让测试用例更通用，具有继承性，本Env提供的接口**对外屏蔽了电路引脚和时序，且接口保持稳定**：

#### 1. env.decode_wrapper.PreDecodeWrapper (class)

```python
# 对PreDecode模块进行封装的类，提供的结构如下：
def predecode() #
...
[TBD]
```

#### 2. env.decode_wrapper.DecodeWrapper (class)
```python
# 对DecodeStage模块进行封装的类，提供的结构如下：
def SetDefaultValue() #
...
[TBD]
```

#### 3. env.decode_wrapper (module)
```python
# 提供公共函数
def decoder_fixture(request): #
def comapre_result(ref_value_list, dut_value_list, num): #
...
[TBD]
```

## 用例说明

本测试创建的用例如下（以下内容建议以funciton doc的形式写入case的具体实现中，然后以link的形式做链接）:

#### 1. test_rvc_expand_full （目标覆盖点：[CK_RVC_LEGAL]()）

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|随机生成N条压缩指令（分布从A->B到）|||
|2|迭代指令，输入给RVCExpanderWrapper和disam||||
|3|获取结果进行对比|||
|4|检查两边的结果|所有非法指令判断结果一致|[.LOAD]()，[.STOR]()|

#### 2. test_rvc_inst(decoder_fixture)

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|TBD|-|-|


#### 3. test_rvi_inst(decoder_fixture)
|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|TBD|-|-|

#### 4. test_rv_custom_inst(decoder_fixture)

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|1|TBD|-|-|


## 目录结构

```bash
decode
├── README.md                 # 说明文件
├── __init__.py               # python模块文件
├── env                       # 环境模块
│   └── decode_wrapper.py     # DUT封装
└── test_rv_decode.py         # 测试用例
```
