---
title: 准备验证环境
linkTitle: 准备验证环境
#menu: {main: {weight: 20}}
weight: 13
---

#### 基础环境需求

本项目基于`Python`编程语言进行UT验证，采用的工具和测试框架为[picker](https://github.com/XS-MLVP/picker)和[toffe](https://github.com/XS-MLVP/toffe)，**环境需求**如下：

1. Linux操作系统。建议WSL2下安装Ubuntu22.04。
1. Python。建议Python3.11。
1. picker。按照[快速开始](https://open-verify.cc/mlvp/docs/quick-start/installer/)中的提示安装最新版本。
1. lcov 用于后续test阶段报告生成。使用包管理器即可下载：sudo apt install lcov

**环境配置完成**后，clone仓库：
```bash
git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
cd UnityChipForXiangShan
pip3 install -r requirements.txt # 安装python依赖（例如 toffee）
```

#### 下载RTL代码： 

默认从仓库[https://github.com/XS-MLVP/UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中下载。用户也可以自行按照XiangShan文档编译生成RTL。

```bash
make rtl    # 该命下载最新的rtl代码，并解压至rtl目录，并创建软连接
```

所有RTL下载包请在[UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中查看。

RTL压缩包的命名规范为：`名称-微架构-Git标记-日期编号.tar.gz`，例如`openxiangshan-kmh-97e37a2237-24092701.tar.gz`。在使用时，仓库代码会过滤掉git标记和后缀，例如通过 cfg.rtl.version 访问到的版本号为：`openxiangshan-kmh-24092701`。压缩包内的目录结构为：

```bash
openxiangshan-kmh-97e37a2237-24092701.tar.gz
└── rtl           # 目录
    |-- *.sv      # 所有sv文件
    `-- *.v       # 所有v文件
```

#### 编译DUT

该过程的目的是将RTL通过picker工具打包为Python模块。可以通过make命令指定被打包DUT，也可以一次性打包所有DUT。

```bash
# 调用scripts目录中的build_ut_<name>.py中的build方法，创建待验证的Python版DUT
make dut DUTS=<name>  # DUTS的值如果有多个，需要用逗号隔开，支持通配符。DUTS默认值为 "*"，编译所有DUT
# 例如：
make dut DUTS=backend_ctrl_block_decode
```

以`make dut DUTS=backend_ctrl_block_decode`为例，命令执行完成后，会在dut目录下生成对应的Python包：

```
dut/
├── __init__.py
├── DecodeStage
├── Predecode
└── RVCExpander
```

完成转换后，在测试用例代码中可以import对应的DUT，例如：
```python
from dut.PreDecode import DUTPreDecode
dut = DUTPreDecode()
```

#### 编辑配置
运行rtl、dut、test等命令时，默认使用configs/_default.yaml中的配置项。

当然，也可以使用自定义配置，方法如下：

```bash
# 指定自定义CFG文件
make CFG=path/to/your_cfg.yaml
```

类似地，可以在命令行直接指定键值对传入。目前仅有test相关阶段支持命令行配置键值对：
```bash
# 指定KV，传递命令行参数，键值对之间用空格隔开
make test KV="log.term-level=\'debug\' test.skip-tags=[\'RARELY_USED\']"
```