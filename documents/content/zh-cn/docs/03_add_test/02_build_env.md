---
title: 构建测试环境
linkTitle: 构建测试环境
#menu: {main: {weight: 20}}
weight: 3
---

## 确定目录结构

UT(单元测试)所在的目录位置的层级结构应该与名称一致，例如`backend.ctrl_block.decode`应当位于`ut_backend/ctrl_block/decode`目录，且每层目录都需要有`__init__.py`，便于通过 python 进行`import`。

```shell
ut_backend/ctrl_block/decode
├── env
│   ├── decode_wrapper.py
│   ├── __init__.py
├── __init__.py
├── README.md
└── test_rv_decode.py
```

模块（例如`decode`）中的代码目录结构由贡献者自行决定，但需要满足 python 规范，且逻辑和命名合理。

## 编写测试环境

在 UT 验证模块的测试环境中，目标是完成以下工作：

1. 对 DUT 进行功能封装，为测试提供稳定 API
2. 定义功能覆盖率
3. 定义必要 fixture 提供给测试用例
4. 在合理时刻统计覆盖率

以 decode 环境中的 RVCExpander 为例（`ut_backend/ctrl_block/decode/env/decode_wrapper.py`）：

### 1. DUT 封装

```python
class RVCExpander(toffee.Bundle):
    def __init__(self, cover_group, **kwargs):
        super().__init__()
        self.cover_group = cover_group
        self.dut = DUTRVCExpander(**kwargs) # 创建DUT
        self.dut.io_in.AsImmWrite()         # DUTRVCExpander为组合电路，将输入引脚设置为ImmWrite写入模式
        self.io = toffee.Bundle.from_prefix("io_", self.dut) # 通过 Bundle 使用前缀关联引脚
        self.bind(self.dut)                 # 把 Bundle 与 DUT 进行绑定

    def expand(self, instr):
        self.io["in"].value = instr         # 给DUT引脚赋值
        self.dut.RefreshComb()              # 推动组合电路
        self.cover_group.sample()           # 调用sample对功能覆盖率进行统计
        return self.io["out_bits"].value, self.io["ill"].value  # 返回结果 和 是否是非法指令

    def stat(self):                         # 获取当前状态
        return {
            "instr": self.io["in"].value,         # 输入指令
            "decode": self.io["out_bits"].value,  # 返回展开结果
            "ilegal": self.io["ill"].value != 0,  # 输入是否非法
        }
```

在上述例子中，`class RVCExpander`对`DUTRVCExpander`进行了封装，对外提供了两个 API：

- expand(instr: int) -> (int, int) ：该函数用于接受输入指令 instr 进行解码，返回（结果，非法指令标记）。如果非法指令标记不为 0，者说明输入指令非法。
- stat() -> dict(instr, decode, ilegal)：该函数用于返回当前的状态，其中包含当前的输入指令，解码结果以及非法指令标记。

上述 API **屏蔽了 DUT 的引脚**，对外程序通用功能。

### 2. 定义功能覆盖率

尽可能的在 Env 中定义好功能覆盖率，如果有必要也可以在测试用例中定义覆盖率。toffee 功能覆盖率的定义请参考[什么是功能覆盖率](http://localhost:1313/docs/03_add_test/05_cover_func/)。为了完善功能检查点和测试用例之间的对应关系，功能覆盖率定义完成后，需要在适合的位置进行检查点和测试用例的对应（测试点反标）。

```python
import toffee.funcov as fc
# 创建功能覆盖率组
g = fc.CovGroup(UT_FCOV("../../INT"))

def init_rvc_expander_funcov(expander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""

    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR. The instruction is not illegal
    #    - bin SUCCE. The instruction is not expanded
    g.add_watch_point(expander, {
                                "ERROR": lambda x: x.stat()["ilegal"] == False,
                                "SUCCE": lambda x: x.stat()["ilegal"] != False,
                          }, name = "RVC_EXPAND_RET")
    ...
    # 5. Reverse mark function coverage to the check point
    def _M(name):
        # get the module name
        return module_name_with(name, "../../test_rv_decode")

    #  - mark RVC_EXPAND_RET
    g.mark_function("RVC_EXPAND_RET",     _M(["test_rvc_expand_16bit_full",
                                              "test_rvc_expand_32bit_full",
                                              "test_rvc_expand_32bit_randomN"]), bin_name=["ERROR", "SUCCE"])
    ...
```

在上述代码中添加了名为`RVC_EXPAND_RET`的功能检查点来检查`RVCExpander`模块是否具有返回非法指令的能力。需要满足`ERROR`和`SUCCE`两个条件，即`stat()`中的`ileage`需要有`True`也需要有`False`值。在定义完检查点后，通过`mark_function`方法，对会覆盖到该检查的测试用例进行了标记。

### 3. 定义必要 fixture

```python
version_check = get_version_checker("openxiangshan-kmh-*")             # 指定满足要的RTL版本
@pytest.fixture()
def rvc_expander(request):
    version_check()                                                    # 进行版本检查
    fname = request.node.name                                          # 获取调用该fixture的测试用例
    wave_file = get_out_dir("decoder/rvc_expander_%s.fst" % fname)     # 设置波形文件路径
    coverage_file = get_out_dir("decoder/rvc_expander_%s.dat" % fname) # 设置代码覆盖率文件路径
    coverage_dir = os.path.dirname(coverage_file)
    os.makedirs(coverage_dir, exist_ok=True)                           # 目标目录不正在则创建目录
    expander = RVCExpander(g, coverage_filename=coverage_file, waveform_filename=wave_file)
                                                                       # 创建RVCExpander
    init_rvc_expander_funcov(expander, g)                              # 初始化功能检查点
    yield expander                                                     # 返回创建好的 RVCExpander 给 Test Case
    expander.dut.Finish()                                              # Tests Case运行完成后，结束DUT
    set_line_coverage(request, coverage_file)                          # 把生成的代码覆盖率文件告诉 toffee-report
    set_func_coverage(request, g)                                      # 把生成的功能覆盖率数据告诉 toffee-report
    g.clear()                                                          # 清空功能覆盖统计
```

上述 fixture 完成了以下功能：

1. 进行 RTL 版本检查，如果不满足`"openxiangshan-kmh-*"`要求，则跳过调用改 fixture 的测试用例
2. 创建 DUT，并指定了波形，代码行覆盖率文件路径（路径中含有调用该 fixure 的用例名称：fname）
3. 调用`init_rvc_expander_funcov`添加功能覆盖点
4. 结束 DUT，处理代码行覆盖率和功能覆盖率（发往 toffee-report 进行处理）
5. 清空功能覆盖率

\*注：在 PyTest 中，执行测试用例`test_A(rvc_expander, ....)`前，会自动调用并执行`rvc_expander(request)`中`yield`关键字前的部分，然后通过`yield`返回`rvc_expander`调用`test_A`用例，用例执行完成后，再继续执行`fixture`中`yield`关键字之后的部分。

### 4. 统计覆盖率

```python
N = 10
T = 1<<16
@pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_16bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full compressed instruction set

    Description:
        Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
    """
    # Add check point: RVC_EXPAND_RANGE to check expander input range.
    #   When run to here, the range[start, end] is covered
    covered = -1
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]"%(start, end): lambda _: covered == end
                          }, name = "RVC_EXPAND_ALL_16B", dynamic_bin=True)
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]"%(start, end))
    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end))
    # When go to here, the range[start, end] is covered
    covered = end
    g.sample()                                                              # 覆盖率采样
```

在定义了覆盖率之后，还需要在测试用例中进行覆盖率统计。上述代码中，在测试用例中使用`add_watch_point`添加了一个功能检查点`rvc_expander`，并在后面进行了标记和采样。

### Env 编写要求

- 需要进行 RTL 版本检查
- Env 提供的 API 需要和引脚、时序无关
- Env 提供的 API 需要稳定，不能随意进行接口/返回值修改
- 需要定义必要的 fixture
- 需要初始化功能检查点（功能检查点可以独立成一个模块）
- 需要进行覆盖率统计
- 需要有说明文档
