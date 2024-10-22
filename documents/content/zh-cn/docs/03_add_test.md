---
title: 添加测试
linkTitle: 添加测试
#menu: {main: {weight: 20}}
weight: 15
---


添加一个全新的DUT测试用例，需要完成以下三部分内容：

1. **添加编译脚本**： 在`scripts`目录下编写对应的`rtl`到`python`的编译`Makefile`文件（例如Makefile.build_ut_**backend_ctrlblock_decode**，必须以`Makefile.build_ut_`开头）以及对应的目录（目录中包含必要的输入文件，例如`rtl`的`filelist`，需要导出的内部信号等）。
1. **添加测试用例**： 在对应的`ut_*`目录中创建对应的`python`模块（例如`ut_backend/ctrl_block/decode`）,在该模块中需要包含以`test_*.py`的测试用例。用例的目录结构请按照[昆明湖层级架构图](https://open-verify.cc/UnityChipForXiangShan/)进行添加，以确保收集测试结果时能与层级图对应。测试用例的编写方法请参考[Pytest官方文档](https://docs.pytest.org/en/stable/)。
1. **添加依赖模块**： 如果有需要的话，可以在`tools、comm`等模块中添加该DUT测试需要的基础工具。如果该工具不够通用请添加到对应的`ut_`模块中，且不能以`test_`前缀进行命名（例如参考模型可以是`ut_backend/ctrl_block/decode/reference.py`）

如果是在已有的DUT测试中增加内容，按原有目录结构添加即可。

*目录或文件名称需要合理，能通过其命名知晓其具体含义。

如何通过picker和mlvp库进行Python芯片验证，请参考：[https://open-verify.cc/mlvp/docs](https://open-verify.cc/mlvp/docs)

