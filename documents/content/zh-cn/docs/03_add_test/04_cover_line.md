---
title: 代码覆盖率
linkTitle: 代码覆盖率
#menu: {main: {weight: 20}}
weight: 5
---

代码覆盖率是一项评价指标，它衡量了被测代码中哪些部分被执行了，哪些部分没有被执行。通过统计代码覆盖率，可以评估测试的有效性和覆盖程度。

代码覆盖率包括：

- 行覆盖率(line coverage): 被测代码中被执行的行数，最简单的指标，一般期望达到 100%。
- 条件覆盖率(branch coverage): 每一个控制结构的每个分支是否均被执行。例如，给定一个 if 语句，其 true 和 false 分支是否均被执行？
- 有限状态机覆盖率(fsm coverage): 状态机所有状态是否都达到过。
- 翻转覆盖率(toggle coverage): 统计被测代码中被执行的翻转语句，检查电路的每个节点是否都有 0 -> 1 和 1 -> 0 的跳变。
- 路径覆盖率(path coverage): 检查路径的覆盖情况。在 always 语句块和 initial 语句块中，有时会使用 if ... else 和 case 语句，在电路结构上便会产生一系列的数据路径。。

## 本项目中相关涉及位置

#### [添加编译脚本](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/01_build_script/)

picker 命令行开启代码覆盖率("-c"参数)、设置目标覆盖文件(line_coverage_files 函数)

#### [构建测试环境-3.定义必要 fixture](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/02_build_env/)

通过函数`toffee-test.set_line_coverage`把覆盖率文件传递给 toffe-test。

## 忽略指定统计

1、[通过 verilator 指定忽略统计的内容](https://veripool.org/guide/latest/exe_verilator.html#configuration-files)

2、提过 toffee 指定需要过滤掉的内存

```python
def set_line_coverage(request, datfile, ignore=[]):
    """Pass

    Args:
        request (pytest.Request): Pytest的默认fixture，
        datfile (string): DUT生成的
        ignore (list[str]): 覆盖率过滤文件/或者文件夹
    """
```

ignore 参数可以指定在覆盖率文件中需要过滤掉的内容，例如：

```python
...
set_line_coverage(request, coverage_file,
                  get_root_dir("scripts/backend_ctrlblock_decode"))
```

在统计覆盖率时，会在"scripts/backend_ctrlblock_decode"目录中搜索到`line_coverage.ignore`文件，然后按其中每行的通配符进行过滤。

## 查看统计结果

在[进度概述](https://open-verify.cc/UnityChipForXiangShan/docs/)图形下方的“当前版本”选择对应的测试报告，然后点击右侧链接即可查看统计结果。
