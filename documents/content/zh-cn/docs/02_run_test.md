---
title: 运行测试
linkTitle: 运行测试
#menu: {main: {weight: 20}}
weight: 14
---

本项目基于toffee验证框架进行验证（toffee基于Pytest测试框架）。运算测试时，测试框架自动搜索所有以`test_*.py`文件，并自动执行其中所有以`test_`开头的测试用例（Test Case）。

```bash
# 执行所有ut_*目录中的test case
make test_all
# 执行指定目录下的test case
make test target=<dir>
# 例如执行ut_backend/ctrl_block/decode目录中所有的test case
make test target=ut_backend/ctrl_block/decode
```

运行完成后，在out目录会生成html版本的测试报告，可通过浏览器直接打开查看（VS Code IDE建议安装`Open In Default Browser`插件）。
