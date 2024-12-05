---
title: 功能覆盖率
linkTitle: 功能覆盖率
#menu: {main: {weight: 20}}
weight: 6
---

什么是功能覆盖率 [TBD]、为什么需要反标
功能覆盖率（Functional Coverage）是一种用户定义的度量标准，用于度量验证中已执行的设计规范的比例。功能覆盖率关注的是设计的功能和特性是否被测试用例覆盖到了。

反标是指从功能测试回溯到代码覆盖率，通过将功能点与代码逻辑关联起来，反向追踪测试覆盖率。
例如：
- 将功能点映射到相关代码模块或路径。
- 检查测试覆盖率工具报告，分析对应功能点的代码是否被执行。
- 确定测试用例对功能的覆盖程度，以及代码的遗漏部分。



## 本项目中相关涉及位置

在[构建测试环境](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/02_build_env/)中：
- 2. 定义功能覆盖率： 创建了功能覆盖率组,添加观察点和反标
- 3. 定义必要fixture： 把统计结果传递给toffee-report
- 4. 统计覆盖率： 添加观察点和反标

其他：
- Test case中使用



## 指定Group名称

测试报告通过Group名字和 DUT名字进行匹配，利用comm.UT_FCOV 获取 DUT前缀，例如在Python模块`ut_backend/ctrl_block/decode/env/decode_wrapper.py`中进行如下调用：

```python
from comm import UT_FCOV
# 本模块名为：ut_backend.ctrl_block.decode.env.decode_wrapper
# 通过../../去掉了上级模块env和decode_wrapper
# UT_FCOV会默认去掉前缀 ut_
name = UT_FCOV("../../INT")
```

name的值为`backend.ctrl_block.decode.INT`，在最后统计结果时，会按照最长前缀匹配到目标UT（即匹配到：backend.ctrl_block.decode 模块）

