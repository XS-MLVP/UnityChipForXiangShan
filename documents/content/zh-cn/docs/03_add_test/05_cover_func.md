---
title: 功能覆盖率
linkTitle: 功能覆盖率
#menu: {main: {weight: 20}}
weight: 6
---

功能覆盖率（Functional Coverage）是一种**用户定义**的度量标准，用于度量验证中已执行的设计规范的比例。功能覆盖率关注的是设计的功能和特性是否被测试用例覆盖到了。

反标是指将功能点与测试用例对应起来。这样，在统计时，就能看到每个功能点对应了哪些测试用例，从而方便查看哪些功能点用的测试用例多，哪些功能点用的测试用例少，有利于后期的测试用例优化。

## 本项目中相关涉及位置

功能覆盖率需要我们先定义了才能统计，主要是在构建测试环境的时候涉及。

在[构建测试环境](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/02_build_env/)中：

- [定义功能覆盖率](02_build_env.md#2-定义功能覆盖率)： 创建了功能覆盖率组,添加观察点和反标
- [定义必要 fixture](02_build_env.md#3-定义必要fixture)： 把统计结果传递给 toffee-report
- [统计覆盖率](02_build_env.md#4-统计覆盖率)： 添加观察点和反标

其他：

- 在 Test case 中使用，可以在每个测试用例里也编写一个功能点。

## 功能覆盖率使用流程

### 指定 Group 名称

测试报告通过 Group 名字和 DUT 名字进行匹配，利用 comm.UT_FCOV 获取 DUT 前缀，例如在 Python 模块`ut_backend/ctrl_block/decode/env/decode_wrapper.py`中进行如下调用：

```python
from comm import UT_FCOV
# 本模块名为：ut_backend.ctrl_block.decode.env.decode_wrapper
# 通过../../去掉了上级模块env和decode_wrapper
# UT_FCOV会默认去掉前缀 ut_
name = UT_FCOV("../../INT")
```

name 的值为`backend.ctrl_block.decode.INT`，在最后统计结果时，会按照最长前缀匹配到目标 UT（即匹配到：backend.ctrl_block.decode 模块）

### 创建覆盖率组

使用`toffee`的`funcov`可以创建覆盖率组。

```python
import toffee.funcov as fc
# 使用上面指定的GROUP名字
g = fc.CovGroup(name)
```

创建的g对象就表示了一个功能覆盖率组，可以使用其来提供观察点和反标。

### 添加观察点和反标

在每个测试用例内部，可以使用`add_watch_point`（`add_cover_point`是其别名，二者完全一致）来添加观察点和`mark_function`来添加反标。
观察点是，当对应的信号触发了我们在观察点内部定义的要求后，这个观察点的名字（也就是功能点）就会被统计到功能覆盖率中。
反标是，将功能点和测试用例进行关联，这样在统计时，就能看到每个功能点对应了哪些测试用例。

对于观察点的位置，需要根据实际情况来定，一般来说，在测试用例外直接添加观察点是没有问题的。
不过有时候我们可以更加的灵活。

1. 在测试用例之外（`decode_wrapper.py`中）
```python
def init_rvc_expander_funcov(expander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""
    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR. The instruction is not illegal
    #    - bin SUCCE. The instruction is not expanded
    g.add_watch_point(expander, {
                                "ERROR": lambda x: x.stat()["ilegal"] == False,
                                "SUCCE": lambda x: x.stat()["ilegal"] != False,
                          }, name = "RVC_EXPAND_RET")
    # 5. Reverse mark function coverage to the check point
    def _M(name):
        # get the module name
        return module_name_with(name, "../../test_rv_decode")

    #  - mark RVC_EXPAND_RET
    g.mark_function("RVC_EXPAND_RET",_M(["test_rvc_expand_16bit_full",
                                              "test_rvc_expand_32bit_full",
                                              "test_rvc_expand_32bit_randomN"]), bin_name=["ERROR", "SUCCE"])

    # The End                                                                              
    return None 


```
这个例子的第一个`g.add_watch_point`是放在测试用例之外的，因为它和现有的测试用例没有直接关系，放在测试用例之外反而更加方便。添加观察点之后，只要`add_watch_point`方法中的`bins`条件触发了，我们的`toffee-test`框架就能够收集到对应的功能点。

2. 在测试用例之中（`test_rv_decode.py`中）

```python
N=10
T=1<<32
@pytest.mark.toffee_tags([TAG_LONG_TIME_RUN, TAG_RARELY_USED])
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_32bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full 32 bit instruction set

    Description:
        Randomly generate N 32-bit instructions for each check, and repeat the process K times.
    """
    # Add check point: RVC_EXPAND_ALL_32B to check instr bits.
    covered = -1
    g.add_watch_point(rvc_expander, {"RANGE[%d-%d]"%(start, end): lambda _: covered == end},
                      name = "RVC_EXPAND_ALL_32B", dynamic_bin=True)
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_32B", test_rvc_expand_32bit_full)
    # Drive the expander and check the result
    rvc_expand(rvc_expander, list([_ for _ in range(start, end)]))
    # When go to here, the range[start, end] is covered
    covered = end
    g.sample()
```

这个例子的观察点在测试用例里面，因为这里的`start`和`end`是由`pytest.mark.parametrize`来决定的，数值不是固定的，所以我们需要在测试用例里面添加观察点。

### 采样

在上一个例子的最后，我们调用了`g.sample()`，这个函数的作用是告诉`toffee-test`，`add_watch_point`里的`bins`已经执行过了，判断一下是不是True，是的话就为这个观察点记录一次Pass。

有手动就有自动。我们可以在构建测试环境时，在定义fixture中加入`StepRis(lambda x: g.sample())`,这样就会在每个时钟周期的上升沿自动采样。

```python
@pytest.fixture()
def decoder(request):
    # before test
    init_rv_decoder_funcov(g)
    func_name = request.node.name
    # If the output directory does not exist, create it
    output_dir_path = get_out_dir("decoder/log")
    os.makedirs(output_dir_path, exist_ok=True)
    decoder = Decode(DUTDecodeStage(
        waveform_filename=get_out_dir("decoder/decode_%s.fst"%func_name),
        coverage_filename=get_out_dir("decoder/decode_%s.dat"%func_name),
    ))
    decoder.dut.InitClock("clock")
    decoder.dut.StepRis(lambda x: g.sample())
    yield decoder
    # after test
    decoder.dut.Finish()
    coverage_file = get_out_dir("decoder/decode_%s.dat"%func_name)
    if not os.path.exists(coverage_file):
        raise FileNotFoundError(f"File not found: {coverage_file}")
    set_line_coverage(request, coverage_file, get_root_dir("scripts/backend_ctrlblock_decode"))
    set_func_coverage(request, g)
    g.clear()
```

如上面所示，我们在`yield`之前调用了`g.sample()`，这样就会在每个时钟周期的上升沿自动采样。

`StepRis`函数的作用是在每个时钟周期的上升沿执行传入的函数，详情可参照[picker使用介绍](https://open-verify.cc/mlvp/docs/env_usage/picker_usage/)