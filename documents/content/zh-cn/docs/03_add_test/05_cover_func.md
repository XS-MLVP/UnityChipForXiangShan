---
title: 功能覆盖率
linkTitle: 功能覆盖率
#menu: {main: {weight: 20}}
weight: 6
---

什么是功能覆盖率 [TBD]、为什么需要反标


## 本项目中相关涉及位置

1、Env 中创建 cover group
2、Env 或者 Test case中使用
3、fixture传递结果给toffee-report


## 指定Group名称

测试报告通过Group名字和 DUT名字进行匹配，利用comm.UT_FCOV 获取 DUT前缀，例如在Python模块`ut_backend/ctrl_block/decode/env/decode_wrapper.py`中进行如下调用：

```python
from comm import UT_FCOV
# 本模块名为：ut_backend.ctrl_block.decode.env.decode_wrapper
# 通过../../去掉了上级模块env和decode_wrapper
# UT_FCOV会默认去掉前缀 ut_
name = UT_FCOV("../../INT")
```

name的值为`backend.ctrl_block.decode.INT`，在最后统计结果时，会安装最长前缀匹配到目标UT（即匹配到：backend.ctrl_block.decode 模块）

