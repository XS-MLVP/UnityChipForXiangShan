---
title: 必要规范
linkTitle: 必要规范
#menu: {main: {weight: 99}}
weight: 99
---

为了方便将所有人的贡献集合在一起，需要在编码、环境、文档编写等方面采用相同的“规范”。

### 环境要求

- **python：** 在python编码过程中，尽可能的采用标准库，采用兼容Python3大部分版本的通用语法（尽可能的在Python3.6 - Python3.12中通用），不要使用过旧或者过新的语法。
- **操作系统：** 建议Ubuntu 22.04，windows下，建议使用WSL2环境。
- **hugo** 建议版本 0.124.1（版本过旧不支持软连接）
- **少依赖** 尽可能少的使用第三方C++/C库
- **picker** 建议使用wheel安装picker工具和xspcomm库

### 测试用例

- **代码风格** 建议采用 [PEP 8 规范](https://peps.python.org/pep-0008/)
- **build脚本** 需要按DUT的命名结构进行规范命名，不然无法正确收集验证结果。例如`backend.ctrl_block.decode`UT在scripts目录中对应的build文件名称应该为`build_ut_backend_ctrl_block_decode.py`(以固定前缀`build_ut_`开始，点`.`用下划线`_`进行替换)。在脚本中实现 `build(cfg) -> bool` 和 `line_coverage_files(cfg) -> list[str]` 方法。`build`用于编译DUT为`python`模块，`line_coverage_files`方法用于返回需要统计的代码行覆盖率文件。
- **用例标签** 如果用例无法做到版本通用，需要用`pytest.mark.toffee_tags`标记支持的版本。 
- **用例抽象** 编写的测试用例输入不能出现DUT的具体引脚等强耦合内容，只能调用基于DUT之上的函数封装。例如对于加法器 adder，需要把dut的目标功能封装为 `dut_wrapper.add(a: int, b: int) -> int, bool`，在test_case中仅仅调用 `sum, c = add(a, b)`进行测试。
- **覆盖抽象** 在编写功能覆盖率时，其检查点函数的输入也不能有DUT引脚。
- **环境抽象** 对于一个验证，通常分为2部分：Test Case 和 Env （用例以外的都统一称为Env，它包含DUT、驱动、监控等），其中Env需要提供对外的功能抽象接口，不能对外呈现出太多细节。
- **测试说明** 在每个DUT的验证环境中，需要通过`README.md`对该环境进行说明，例如需要对Env提供给Case的接口进行说明，目录结构说明等。


### PR编写

- **标题** 简洁明了，能概括PR的主要内容。
- **详细描述** 详细说明PR的目的，修改的内容以及相关背景信息。入解决已有的问题需要给出链接（例如Issue）。
- **关联问题** 在描述中关联相关问题，例如 `Fixes #123`，以便在合并PR时关闭关联问题。
- **测试** 需要进行测试，并对测试结果进行描述
- **文档** PR涉及到的文档需要同步修改
- **分解** 当PR涉及到的修改很多时，需要判断是否拆分成多个PR
- **检查清单** 检查编译是否通过、代码风格是否合理、是否测试通过、是否有必要的注释等
- **模板** 以及提供的PR模块请[参考链接](08_pr_template/)。


### ISSUE编写

 要求同上
