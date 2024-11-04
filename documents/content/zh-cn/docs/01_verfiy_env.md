---
title: 准备验证环境
linkTitle: 准备验证环境
#menu: {main: {weight: 20}}
weight: 13
---

#### 基础环境需求

本项目基于`Python`编程语言进行UT验证，采用的工具和测试框架为[picker](https://github.com/XS-MLVP/picker)和[mlvp](https://github.com/XS-MLVP/mlvp)，环境需求如下：

1. Linux操作系统。建议WSL2下安装Ubuntu22.04。
1. Python。建议Python3.11。
1. picker。按照[快速开始](https://open-verify.cc/mlvp/docs/quick-start/installer/)中的提示安装最新版本。
1. mlvp。可通过`pip3 install mlvp@git+https://github.com/XS-MLVP/mlvp`安装最新版本。

环境配置完成后，clone仓库：
```bash
git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
```

#### 下载RTL代码：

默认从仓库[https://github.com/XS-MLVP/UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中下载。用户也可以自行按照XiangShan文档编译生成RTL。

```bash
cd UnityChipForXiangShan
make rtl    # 该命下载最新的rtl代码，并解压至rtl目录，并创建软连接
```

所有RTL下载包请在[UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中查看。

#### 编译DUT

该过程的目的是将RTL通过picker工具打包为Python模块。可以通过make命令指定被打包DUT，也可以一次性打包所有DUT。

```bash
# 调用scripts目录中的Makefile.build_ut_<name>，创建待验证的Python版DUT
make dut target=<name>
# 例如：
make dut target=backend_ctrlblock_decode
# 调用scripts目录中所有的Makefile.build_ut_*文件，创建所有DUT。
make dut_all
```

以`make dut target=backend_ctrlblock_decode`为例，命令执行完成后，会在dut目录下生成对应的Python包：

```
dut/
├── __init__.py
├── decodestage
├── predecode
└── rvcexpander
```

完成转换后，在测试用例代码中可以import对应的DUT，例如：
```python
from dut.predecode.UT_PreDecode import DUTPreDecode
dut = DUTPreDecode()
```
