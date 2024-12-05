---
title: 添加测试
linkTitle: 添加测试
#menu: {main: {weight: 20}}
weight: 15
---

添加一个全新的 DUT 测试用例，需要完成以下三部分内容：

1. **添加编译脚本**： 在`scripts`目录下使用`python`编写对应`rtl`的编译文件（例如`build_ut_backend_ctrl_block_decode.py`）。
1. **构建测试环境**： 在目录中创建目标测试 UT 目录（例如`ut_backend/ctrl_block/decode`）。如果有需要的话，可以在`tools、comm`等模块中添加该 DUT 测试需要的基础工具。
1. **添加测试用例**： 在测试 UT 目录，按[PyTest 规范](https://docs.pytest.org/en/stable/)添加测试用例。

如果是在已有的 DUT 测试中增加内容，按原有目录结构添加即可。

如何通过 picker 和 toffee 库进行 Python 芯片验证，请参考：[https://open-verify.cc/mlvp/docs](https://open-verify.cc/mlvp/docs)

在测试时还需要关心以下内容：

1. **UT 模块说明**: 在添加的模块顶层文件夹中，添加`README.md`说明，具体格式和要求请参考[模板](https://open-verify.cc/UnityChipForXiangShan/docs/10_template_ut_readme/)。
1. **代码覆盖率**：代码覆盖率是芯片验证的重要指标，一般需需要覆盖目标 DUT 的所有代码。
1. **功能覆盖率**：功能覆盖率即目标功能验证完成了多少，一般需要达到 100%。

在后续的文档中，我们以 decode 模块为例，详细说明上述过程。

\*注：目录或文件名称需要合理，能通过其命名知晓其具体含义。
