# 万众一芯之香山处理器

中文|[English](README.md)

本项目旨在通过开源众包的方式对[香山处理器](https://github.com/OpenXiangShan/XiangShan)的昆明湖架构进行单元（UT）验证，并选择Python作为主要的验证语言。参与本项目，你将学习到以下内容：

1. **电路的运行特性**：从软件的角度观察电路的运行特性，深入了解电路设计的原理。
2. **香山处理器的高性能设计**：学习Chisel硬件描述语言，研读相关代码和论文，掌握最新的架构设计理念。
3. **芯片验证的基本流程**：熟悉规范文档（Spec文档），学习如何执行UT验证，并评估验证结果的合理性。
4. **Python在芯片验证中的应用**：掌握异步编程、回调等高级编程模式，利用Python进行芯片验证。
5. **Linux环境下的软件开发流程**：学习基础的操作命令，搭建基本的开发环境。

本项目欢迎多方面的贡献，并将在一定期限内以特定方式给予奖励（如奖金、证书、实习机会等）。具体贡献类型包括：

- **贡献一**：编写验证文档，包括设计对象（Design Under Test，DUT）的规范文档、说明文档、功能描述文档等。
- **贡献二**：开发测试用例，包括针对各个功能点的测试代码和注释，以及相关的说明文档。
- **贡献三**：发现并报告香山处理器中的bug，并提供原因分析和修复建议。
- **贡献四**：其他方面的贡献，例如为本项目提供的工具增加新功能等。

期待你的参与！


### 整体状态

#### 验证进度

当前各个DUT的验证状态，包括功能点个数、代码行覆盖率、Bug数等。

<a href="https://open-verify.cc/UnityChipForXiangShan/chart/meta.html">
<img src="docs/snapshot/chart_meta.png" alt="meta" style="max-width: 900px; width: 90%; height: auto;">
</a>

总体目标进展与当前文档请查看 [https://open-verify.cc/UnityChipForXiangShan/](https://open-verify.cc/UnityChipForXiangShan/)

- **已发现的bug列表**：TBD
- **已同步的验证文档**：TBD
- **已验证的DUT列表**：TBD
- **DUT与功能列表**：TBD
- **带验证的DUT列表**：TBD

注：本项目中的的统计信息每周根据commit、issue等数据自动更新

### 准备环境

本项目基于`Python`编程语言进行UT验证，采用的工具和测试框架为[picker](https://github.com/XS-MLVP/picker)和[mlvp](https://github.com/XS-MLVP/mlvp)，基本环境需求如下：

1. 操作系统Linux。建议Ubuntu22.04。
1. Python。建议Python3.11。
1. picker。按照[快速开始](https://open-verify.cc/mlvp/docs/quick-start/installer/)中的提示安装最新版本。
1. mlvp。可通过`pip3 install mlvp@git+https://github.com/XS-MLVP/mlvp`安装最新版本。

环境配置完成后，clone本仓库：
```bash
git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
```

下载RTL代码：

默认从仓库[https://github.com/XS-MLVP/UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中下载。用户也可以自行按照XiangShan文档编译生成RTL。

```bash
cd UnityChipForXiangShan
make rtl    # 该命下载最新的rtl代码，并解压至rtl目录，并创建软连接
make rtl target=2024092701/openxiangshan-kmh-97e37a2237-24092701.tar.gz    # 可通过target指定版本
```

所有RTL下载包请在[UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中查看。

### 编译DUT

该过程的目的是将RTL通过picker工具打包为Python模块，可以通过make命令指定被打包DUT，也可以一次性打包所有支持的DUT。

```bash
make dut target=<name>    # 调用scripts目录中的Makefile.build_ut_<name>对应的Makefile创建待验证的Python版DUT
# 例如：
make dut target=backend_decode
make dut_all              # 调用scripts目录中所有的Makefile.build_ut_*文件，创建所有DUT。
```

以`make dut target=backend_decode`为例，命令执行完成后，会在dut目录下生成对应的Python包：

```
dut/
├── __init__.py
├── decodestage
├── predecode
└── rvcexpander
```

在测试代码中就可以import对应的DUT，例如：
```python
from dut.predecode.UT_PreDecode import DUTPreDecode
dut = DUTPreDecode()
```

### 运行测试

本项目基于mlvp验证框架进行验证（mlvp基于Pytest测试框架）。运算测试时，测试框架自动搜索所有以`test_*.py`文件，并自动执行其中所有以`test_`开头的测试用例（Test Case）。运行完成后，建在out目录生成html版本的测试报告，可通过浏览器直接打开查看。

```bash
make test_all           # 执行所有ut_*目录中的test case
make test target=<dir>  # 执行指定目录下的test case
# 例如
make test target=ut_backend/ut_decode  # 执行ut_backend/ut_decode目录中所有的test case
```

### 添加测试

TBD

### 可视化文档

TBD

### 添加文档

TBD

### 目录结构介绍

TBD

### 参与本项目

TBD

### PR提交建议

TBD
