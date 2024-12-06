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

\*我们主要使用的模拟器是 Verilator,优先考虑**行覆盖率**。Verilator 支持覆盖率统计，因此我们在构建 DUT 时，如果要开启覆盖率统计，需要在编译选项中添加`-c`参数。

## 本项目中相关涉及位置

开启覆盖率需要在编译时（使用 picker 命令时）加上“-c”参数（参考 picker 的[参数解释](https://github.com/XS-MLVP/picker/blob/master/README.zh.md#%E5%8F%82%E6%95%B0%E8%A7%A3%E9%87%8A)），同时在文件中设置启用行覆盖率，这样在使用 toffee 测试时，才能够生成覆盖率统计文件。

结合上面的描述，在本项目中也就是编译，编写和启用行覆盖率函数和测试的时候会涉及到代码覆盖率：

### 添加编译脚本部分

[编写编译脚本](01_build_script.md#编写-buildcfg---bool-函数)

```python
# 省略前面
    if not os.path.exists(get_root_dir("dut/RVCExpander")):
        info("Exporting RVCExpander.sv")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/RVCExpander.sv", cfg=cfg)
                                                              } --lang python --tdir {get_root_dir("dut")}/ -w rvc.fst -c')
        assert s, "Failed to export RVCExpander.sv: %s\n%s" % (out, err)
# 省略后面
```

在`s, out, err=...`这一行，我们使用 picker 命令，并且开启代码了覆盖率(命令最后的"-c"参数)。

[设置目标覆盖文件(line_coverage_files 函数)](01_build_script.md#编写-line_coverage_filescfg---liststr-函数)

按照需求编写`line_coverage_files(cfg) -> list[str]`函数，并且开启测试结果处理(`doc_result.disable = False`)让其被调用。

### 构建测试环境部分

[定义必要 fixture](02_build_env.md#3-定义必要fixture)

```python
set_line_coverage(request, coverage_file)                          # 把生成的代码覆盖率文件告诉 toffee-report
```

通过函数`toffee-test.set_line_coverage`把覆盖率文件传递给 toffe-test，这样其才能够收集数据，以便于后面生成的报告带有行覆盖率。

## 忽略指定统计

有时候，我们可能需要手动指定某些内容不参与覆盖率统计。例如有些是不需要被统计的，有些统计不到是正常的。这时候我们就可以忽略这些内容，这对优化覆盖率报告或调试非常有帮助。
目前我们的框架可以使用两种方式来实现忽略统计的功能：

### 1.通过 verilator 指定忽略统计的内容

#### 使用 verilator_coverage_off/on 指令

Verilator 支持通过注释指令来忽略特定代码段的覆盖率统计。例如，使用如下的指令：

```verilog
// *verilator coverage_off*
// 忽略统计的代码段
...
// *verilator coverage_on*
```

举个例子

```verilog
module example;
    always @(posedge clk) begin
        // *verilator coverage_off*
        if (debug_signal) begin
            $display("This is for debugging only");
        end
        // *verilator coverage_on*
        if (enable) begin
            do_something();
        end
    end
endmodule
```

在上述示例中，debug_signal 部分的代码将不会计入覆盖率统计，而 enable 部分仍然会被统计。

更多 verilator 的忽略统计方式请参照[verilator 官方文档](https://veripool.org/guide/latest/exe_verilator.html#configuration-files)

### 2.通过 toffee 指定需要过滤掉的内存

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

```ignore
# Line covarge ignore file
# ignore Top file
*/DecodeStage_top*%
```

上述文件表示，在统计覆盖率时，会忽略掉包含"DecodeStage_top"关键字的文件（实际上是收集了对应的数据，但是最后统计的时候忽略了）。

## 查看统计结果

在经过前面所有步骤之后，包括准备测试环境中的[下载 RTL 代码](../01_verfiy_env.md#下载rtl代码)、[编译 DUT](../01_verfiy_env.md#编译DUT)、[编辑配置](../01_verfiy_env.md#编辑配置)
；添加测试中的[添加编译脚本](01_build_script.md),[构建测试环境](02_build_env.md)、[添加测试用例](03_add_test.md)。

现在[运行测试](../02_run_test.md),之后就默认在`out/report`目录会生成 html 版本的测试报告。

也可以在[进度概述](https://open-verify.cc/UnityChipForXiangShan/docs/)图形下方的“当前版本”选择对应的测试报告(按照测试时间命名)，然后点击右侧链接即可查看统计结果。
