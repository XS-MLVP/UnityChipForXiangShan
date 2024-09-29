# 万众一芯之香山处理器

中文|[English](/README.en.md)

本项目旨在通过开源众包的方式对[香山处理器](https://github.com/OpenXiangShan/XiangShan)的昆明湖架构进行单元（UT）验证。该项目选择Python作为主要的验证语言，参与验证你将学习到以下内容：

1. **电路的运行特性**：从软件的角度观察电路的运行特性，深入了解电路设计的原理。
2. **高性能处理器设计**：学习Chisel硬件描述语言，研读相关代码和论文，掌握最新的架构设计理念。
3. **芯片验证的基本流程**：熟悉规范文档（Spec文档），学习如何进行UT验证，并评估验证结果的合理性。
4. **Python芯片验证**：掌握异步编程、回调等高级编程模式，利用Python进行芯片验证。
5. **Linux开发环境**：学习基础的Linux操作命令，搭建验证环境。

本项目欢迎多方面的贡献，并将在一定期限内以特定方式给予奖励（如奖金、证书、实习机会等）。具体贡献类型包括：

- **贡献一**：编写验证文档，包括设计对象（Design Under Test，DUT）的规范文档、说明文档、功能描述文档等。
- **贡献二**：开发测试用例，包括针对各个功能点的测试代码与注释，以及相关的说明文档。
- **贡献三**：发现并报告香山处理器中的bug，并提供原因分析和修复建议。
- **贡献四**：其他方面的贡献，例如为本项目提供的工具增加新功能等。

万众一芯项目地址：[https://open-verify.cc](https://open-verify.cc)

期待你的参与！

### 整体状态

#### 验证进度

当前各个DUT的验证状态，包括功能点个数、代码行覆盖率、Bug数等。

<a href="https://open-verify.cc/UnityChipForXiangShan/chart/meta.html">
<img src="/docs/snapshot/chart_meta.png" alt="meta" style="max-width: 900px; width: 90%; height: auto;">
</a>

总体进展与文档请查看 [https://open-verify.cc/UnityChipForXiangShan/](https://open-verify.cc/UnityChipForXiangShan/)

- **待验证DUT列表：**[https://open-verify.cc/UnityChipForXiangShan/todolist](https://open-verify.cc/UnityChipForXiangShan/todolist)
- **DUT文档与功能：**[https://open-verify.cc/UnityChipForXiangShan/duts](https://open-verify.cc/UnityChipForXiangShan/TBD)
- **待确认bug列表：**[https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bugx](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bugc)
- **已发现bug列表：**[https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bug](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bug)
- **已修复bug列表：**[https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bugfixed](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bugfixed)
- **正在进行的任务列表：**[https://github.com/XS-MLVP/UnityChipForXiangShan/labels/task](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/task)
- **已完成的任务列表：**[https://github.com/XS-MLVP/UnityChipForXiangShan/labels/taskdone](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/taskdone)

注：本项目中的统计信息根据commit、issue等数据自动更新，参与者可以提交issue（写明任务内容，预计完成时间等）同步正在进行的任务。

### 准备环境

本项目基于`Python`编程语言进行UT验证，采用的工具和测试框架为[picker](https://github.com/XS-MLVP/picker)和[mlvp](https://github.com/XS-MLVP/mlvp)，环境需求如下：

1. Linux操作系统。建议WSL2下安装Ubuntu22.04。
1. Python。建议Python3.11。
1. picker。按照[快速开始](https://open-verify.cc/mlvp/docs/quick-start/installer/)中的提示安装最新版本。
1. mlvp。可通过`pip3 install mlvp@git+https://github.com/XS-MLVP/mlvp`安装最新版本。

环境配置完成后，clone仓库：
```bash
git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
```

下载RTL代码：

默认从仓库[https://github.com/XS-MLVP/UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中下载。用户也可以自行按照XiangShan文档编译生成RTL。

```bash
cd UnityChipForXiangShan
make rtl    # 该命下载最新的rtl代码，并解压至rtl目录，并创建软连接
# 可通过target指定版本
make rtl target=2024092701/openxiangshan-kmh-97e37a2237-24092701.tar.gz
```

所有RTL下载包请在[UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs)中查看。

### 编译DUT

该过程的目的是将RTL通过picker工具打包为Python模块。可以通过make命令指定被打包DUT，也可以一次性打包所有DUT。

```bash
# 调用scripts目录中的Makefile.build_ut_<name>，创建待验证的Python版DUT
make dut target=<name>
# 例如：
make dut target=backend_decode
# 调用scripts目录中所有的Makefile.build_ut_*文件，创建所有DUT。
make dut_all
```

以`make dut target=backend_decode`为例，命令执行完成后，会在dut目录下生成对应的Python包：

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

### 运行测试

本项目基于mlvp验证框架进行验证（mlvp基于Pytest测试框架）。运算测试时，测试框架自动搜索所有以`test_*.py`文件，并自动执行其中所有以`test_`开头的测试用例（Test Case）。

```bash
# 执行所有ut_*目录中的test case
make test_all
# 执行指定目录下的test case
make test target=<dir>
# 例如：
# 执行ut_backend/ut_decode目录中所有的test case
make test target=ut_backend/ut_decode
```

运行完成后，在out目录会生成html版本的测试报告，可通过浏览器直接打开查看（VS Code IDE建议安装`Open In Default Browser`插件）。

### 添加测试

添加一个全新的DUT测试用例，需要完成以下三部分内容：

1. **添加编译脚本**： 在`scripts`目录下编写对应的`rtl`到`python`的编译`Makefile`文件（例如Makefile.build_ut_**backend_decode**，必须以`Makefile.build_ut_`开头）以及对应的目录（目录中包含必要的输入文件，例如`rtl`的`filelist`，需要导出的内部信号等）。
1. **添加测试用例**： 在对应的`ut_*`目录中创建对应的`python`模块（例如`ut_backend/ut_decode`）,在该模块中需要包含以`test_*.py`的测试用例。测试用例的编写方法请参考[Pytest官方文档](https://docs.pytest.org/en/stable/)。
1. **添加依赖模块**： 如果有需要的话，可以在`tools、comm`等模块中添加该DUT测试需要的基础工具。如果该工具不够通用请添加到对应的`ut_`模块中，且不能以`test_`前缀进行命名（例如参考模型可以是`ut_backend/ut_xxx/reference.py`）

如果是在已有的DUT测试中增加内容，按原有目录结构添加即可。

如何通过picker和mlvp库进行Python芯片验证，请参考：[https://open-verify.cc/mlvp/docs](https://open-verify.cc/mlvp/docs)

### 添加文档

本项目的DUT文档通过`docsy`编写，文档内容位于`documents/content`目录，分`en`和`zh-cn`两种语言。具体文档编写语法，所用工具等，请参考[docsy文档](https://www.docsy.dev/docs/)和[hugo文档](https://gohugo.io/)。

可以通过以下命令查看效果（hugo安装：[documents/README.md](/documents/README.md)）：

```bash
$cd documents
$hugo server
# 找到类似输出：
Web Server is available at //localhost:1313/ (bind address 127.0.0.1)
```

通过浏览器访问`http://127.0.0.1:1313`即可查看文档。

### 目录结构

```
├── comm               # 公共函数模块，例如日志、环境配置等
├── docs               # 文档在线部署目录（web + doc），请不要修改
├── documents          # DUT docsy 文档
│   ├── content
│   │   ├── en
│   │   │   └── docs   # DUT 英文文档
│   │   └── zh-cn
│   │       └── docs   # DUT 中文文档 （提交PR时，中英文都需要）
│   └── static         # DUT 静态目录，插入的图片按content中的目录结构放该目录
├── dut                # DUT的Python模块，自动生成
├── out                # 输出
│   └── report         # 输出的测试报告
├── rtl                # RTL文件目录
├── scripts            # DUT转Python的编译脚本
├── tools              # 公共工具模块
├── ut_backend         # 后端测试集合
├── ut_cache           # cache测试集合
├── ut_frontend        # 前端测试集合
├── ut_mem             # 访存测试集合
└── ut_misc            # 其他访存测试集合
```

### 参与本项目

本项目欢迎任何人以`Fork + PR`的方式参与。

万众一芯QQ交流群：

<image src="/.github/image/600480230.jpg" alter="600480230" width=300px />
