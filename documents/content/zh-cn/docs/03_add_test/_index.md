---
title: 添加测试
linkTitle: 添加测试
#menu: {main: {weight: 20}}
weight: 15
---


添加一个全新的DUT测试用例，需要完成以下三部分内容：

1. **添加编译脚本**： 在`scripts`目录下编写对应的`rtl`到`python`的编译`python`文件。
1. **构建测试环境**： 在目录中创建目标测试UT目录（例如`ut_backend/ctrl_block/decode`）。如果有需要的话，可以在`tools、comm`等模块中添加该DUT测试需要的基础工具。
1. **添加测试用例**： 在测试UT目录，按[PyTest规范](https://docs.pytest.org/en/stable/)添加测试用例。

如果是在已有的DUT测试中增加内容，按原有目录结构添加即可。

如何通过picker和toffee库进行Python芯片验证，请参考：[https://open-verify.cc/mlvp/docs](https://open-verify.cc/mlvp/docs)

在测试时还需要关心以下内容：

1. **UT模块说明**: 在添加的模块顶层文件夹中，添加`README.md`说明，具体格式和要求请参考[模板]()。
1. **代码覆盖率**：代码覆盖率是芯片验证的重要指标，一般需需要覆盖目标DUT的所有代码。
1. **功能覆盖率**：功能覆盖率即目标功能验证完成了多少，一般需要达到100%。

在后续的文档中，我们以decode模块为例，详细说明上述过程。

*注：目录或文件名称需要合理，能通过其命名知晓其具体含义。
