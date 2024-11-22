---
title: 代码覆盖率
linkTitle: 代码覆盖率
#menu: {main: {weight: 20}}
weight: 5
---

TBD [简单描述 + 参考]

## 本项目中相关涉及位置

#### 1. build script
picker命令行开启代码覆盖率(picker -c参数)、设置目标覆盖文件(line_coverage_files函数)

#### 1. Env中的fixture


通过函数`toffee-test.set_line_coverage`把覆盖率文件传递给toffe-test。


## 忽略指定统计

1、[通过 verilator 指定忽略统计的内容](https://veripool.org/guide/latest/exe_verilator.html#configuration-files)


2、提过toffee指定需要过滤掉的内存

```python
def set_line_coverage(request, datfile, ignore=[]):
    """Pass
    
    Args:
        request (pytest.Request): Pytest的默认fixture，
        datfile (string): DUT生成的
        ignore (list[str]): 覆盖率过滤文件/或者文件夹
    """
```

ignore参数可以指定在覆盖率文件中需要过滤掉的内容，例如：

```python
...
set_line_coverage(request, coverage_file, 
                  get_root_dir("scripts/backend_ctrlblock_decode"))
```

在统计覆盖率时，会在"scripts/backend_ctrlblock_decode"目录中搜索到`line_coverage.ignore`文件，然后按其中没行的通配符进行过滤。


## 查看统计结果

在 测试报告 和 进度章节 有展示
