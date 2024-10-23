# 万众一芯之香山处理器

中文|[English](/README.en.md)

本项目旨在通过开源众包的方式对[香山处理器](https://github.com/OpenXiangShan/XiangShan)的昆明湖架构进行单元（Unit Test, UT）验证。该项目选择Python作为主要的验证语言，参与验证你将学习到以下内容：

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

万众一芯项目网址：[https://open-verify.cc](https://open-verify.cc)

期待你的参与！

#### 快速开始

参照[准备验证环境文档](https://open-verify.cc/UnityChipForXiangShan/docs/01_verfiy_env/)，配置基本环境，然后运行以下命令：

```bash
git clone git@github.com:XS-MLVP/UnityChipForXiangShan.git
cd UnityChipForXiangShan
make all
```

上述命令会自动进行以下操作：

1. 下载RTL代码；
1. 编译所有可用待验模块；
1. 搜索`ut_*`目录中所有`test_`开头的python文件，并运行其中`test_`开头的测试用例
1. 生成测试报告（测试报告位于out目录）
1. 更新统计数据（可通过[本地展示文档](#如何本地展示文档)查看统计结果）

*默认情况下，会skip过于耗时的测试，可通过设置环境变量`XS_FULL_TEST=1`运行所有用例:

```bash
make all XS_FULL_TEST=1
```

#### 如何本地展示文档

按照[文档部署说明](https://github.com/XS-MLVP/UnityChipForXiangShan/blob/main/documents/README.md)配置`hugo`环境，然后执行：

```bash
cd UnityChipForXiangShan
make doc
```

执行完上述命令后，出现类似输出：

```bash
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at //localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

此时，通过浏览器访问提示给出的地址（[http://127.0.0.1:1313](http://127.0.0.1:1313/)）即可。


**更多文档与验证进度请查看**：[https://open-verify.cc/UnityChipForXiangShan](https://open-verify.cc/UnityChipForXiangShan/docs/)

#### 万众一芯QQ交流群：

<image src="/.github/image/600480230.jpg" alter="600480230" width=300px />
