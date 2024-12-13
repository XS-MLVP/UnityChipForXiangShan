---
title: 构建测试环境
linkTitle: 构建测试环境
#menu: {main: {weight: 20}}
weight: 3
---

## 确定目录结构

UT(Unit Test, 单元测试)所在的目录位置的层级结构应该与名称一致，例如`backend.ctrl_block.decode`应当位于`ut_backend/ctrl_block/decode`目录，且每层目录都需要有`__init__.py`，便于通过 python 进行`import`。

**本章节的文件为`your_module_wrapper.py`**（如果你的模块是decode，那么文件就是`decode_wrapper.py`）。

wrapper 是包装的意思，也就是我们测试中需要用到的方法封装成和dut解耦合的API提供给测试用例使用。

\*注：解耦合是为了测试用例和 DUT 解耦，使得测试用例可以独立于 DUT 进行编写和调试，也就是在测试用例中，不需要知道 DUT 的具体实现细节，只需要知道如何使用 API 即可。可以参照[将验证代码与DUT进行解耦](https://open-verify.cc/mlvp/docs/mlvp/canonical_env/#%E5%B0%86%E9%AA%8C%E8%AF%81%E4%BB%A3%E7%A0%81%E4%B8%8Edut%E8%BF%9B%E8%A1%8C%E8%A7%A3%E8%80%A6)

该文件应该放于`ut_frontend_or_backend/top_module/your_module/env`（这里依然以`decode`举例：`decode`属于后端，其顶层目录则应该是`ut_backend`；`decode`的顶层模块是`ctrlblock`，那么次级目录就是`ctrl_block`;之后的就是`decode`自己了；最后，由于我们是在**构建测试环境**，再建一级`env`目录。将它们连起来就是：`ut_frontend_or_backend/top_module/your_module/env`）目录下。

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

## 编写测试环境：一般思路

在 UT 验证模块的测试环境中，目标是完成以下工作：

1. 对 DUT 进行功能封装，为测试提供稳定 API
2. 定义功能覆盖率
3. 定义必要 fixture 提供给测试用例
4. 在合理时刻统计覆盖率

以 IFU 环境中的 RVCExpander 为例（`ut_frontend/ifu/rvc_expander/classical_version/env/rvc_expander_wrapper.py`）：

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

    def expand(self, instr, fsIsOff):
        self.io["in"].value = instr         # 给DUT引脚赋值
        self.io["fsIsOff"].value = fsIsOff  # 给DUT引脚赋值
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

- expand(instr: int, fsIsOff: bool) -> (int, int) ：该函数用于接受输入指令 instr 进行解码，返回（结果，非法指令标记）。如果非法指令标记不为 0，者说明输入指令非法。
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

### 3. 定义必要fixture

```python
version_check = get_version_checker("openxiangshan-kmh-*")             # 指定满足要的RTL版本
@pytest.fixture()
def rvc_expander(request):
    version_check()                                                    # 进行版本检查
    fname = request.node.name                                          # 获取调用该fixture的测试用例
    wave_file = get_out_dir("decoder/rvc_expander_%s.fst" % fname)     # 设置波形文件路径
    coverage_file = get_out_dir("decoder/rvc_expander_%s.dat" % fname) # 设置代码覆盖率文件路径
    coverage_dir = os.path.dirname(coverage_file)
    os.makedirs(coverage_dir, exist_ok=True)                           # 目标目录不存在则创建目录
    expander = RVCExpander(g, coverage_filename=coverage_file, waveform_filename=wave_file)
                                                                       # 创建RVCExpander
    expander.dut.io_in.AsImmWrite()                                    # 设置io_in引脚的写入时机为立即写入             
    expander.dut.io_fsIsOff.AsImmWrite()                               # 设置io_fsIsOff引脚的写入时机为立即写入  
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

\*注：在 PyTest 中，执行测试用例`test_A(rvc_expander, ....)`前（**rvc_expander是我们在使用fixure装饰器时定义的方法名**），会自动调用并执行`rvc_expander(request)`中`yield`关键字前的部分（相当于初始化），然后通过`yield`返回`rvc_expander`调用`test_A`用例（**yield返回的对象，在测试用例里就是我们fixture下定义的方法名**），用例执行完成后，再继续执行`fixture`中`yield`关键字之后的部分。比如：参照下面统计覆盖率的代码，倒数第四行的
`rvc_expand(rvc_expander, generate_rvc_instructions(start, end))`，其中的`rvc_expander`就是我们在`fixture`中定义的方法名，也就是`yield`返回的对象。


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

在定义了覆盖率之后，还需要在测试用例中进行覆盖率统计。上述代码中，在测试用例中使用`add_watch_point`添加了一个功能检查点`rvc_expander`，并在后面进行了标记和采样,而且在最后一样对覆盖率进行了采样。
覆盖率采样，实际上是通过回调函数触发了一次`add_watch_point`中bins的判断，当其中bins的判断结果为`True`时，就会统计一次Pass。

### Env 编写要求

- 需要进行 RTL 版本检查
- Env 提供的 API 需要和引脚、时序无关
- Env 提供的 API 需要稳定，不能随意进行接口/返回值修改
- 需要定义必要的 fixture
- 需要初始化功能检查点（功能检查点可以独立成一个模块）
- 需要进行覆盖率统计
- 需要有说明文档

## toffee框架支持的测试环境

使用python语言进行的测试可以通过引入我们的开源测试框架[toffee](https://github.com/XS-MLVP/toffee)来得到更好的支持。

toffee的官方教程可以参考[这里](https://open-verify.cc/mlvp/docs/mlvp/)。

### bundle：快捷DUT封装

toffee通过Bundle实现了对DUT的绑定。toffee提供了多种建立Bundle与DUT绑定的方法。相关代码

#### 手动绑定

toffee框架下，用于支持绑定引脚的最底层类是Signal，其通过命名匹配的方式和DUT中的各个引脚进行绑定。相关代码参照`ut_frontend/ifu/rvc_expander/toffee_version`。

以最简单的RVCExpander为例，其io引脚形如：

``` verilog
module RVCExpander(
  input  [31:0] io_in,
  input         io_fsIsOff,
  output [31:0] io_out_bits,
  output        io_ill
);

```

一共四个信号，io\_in, io\_fsIsOff, io\_out\_bits, io\_ill。我们可以抽取共同的前缀，比如\"io_\"（不过由于in在python中有其他含义，其不能直接作为变量名，虽然可以使用setattr 和getattr方法来规避这个问题，但是出于代码简洁的考虑，我们只选取\"io\"作为前缀），将后续部分作为引脚名定义在对应的Bundle类中：


```python

class RVCExpanderIOBundle(Bundle):
	_in, _fsIsOff ,_out_bits,_ill = Signals(4)

```

然后在更高一级的Env或者Bundle中，采取from\_prefix的方式完成前缀的绑定：

```python
self.agent = RVCExpanderAgent(RVCExpanderIOBundle.from_prefix("io").bind(dut))
```

#### 自动定义Bundle

实际上，Bundle类的定义也不一定需要写明，可以仅仅通过前缀绑定：

```python

self.io = toffee.Bundle.from_prefix("io_", self.dut) # 通过 Bundle 使用前缀关联引脚
self.bind(self.dut)   

```

如果Bundle的from_prefix方法传入dut，其将根据前缀和DUT的引脚名自动生成引脚的定义，而在访问的时候，使用dict访问的思路即可：

```python

self.io["in"].value = instr
self.io["fsIsOff"].value = False

```

#### Bundle代码生成

toffee框架的[scripts](https://github.com/XS-MLVP/toffee/tree/master/scripts)提供了两个脚本。

bundle\_code\_gen\.py脚本主要提供了三个方法：

```python
def gen_bundle_code_from_dict(bundle_name: str, dut, dict: dict, max_width: int = 120)
def gen_bundle_code_from_prefix(bundle_name: str, dut, prefix: str = "", max_width: int = 120):
def gen_bundle_code_from_regex(bundle_name: str, dut, regex: str, max_width: int = 120):
```
通过传入dut和生成规则（包括dict、prefix、regex三种），自动生成对应的bundle代码。

而bundle\_code\_intel\_gen\.py则解析picker生成的signals\.json文件，自动生成层次化的bundle代码。可以直接在命令行调用：

```bash
python bundle_code_intel_gen.py [signal] [target]
```

如发现自动生成脚本存在bug，欢迎提issue以便我们修正。

### Agent：驱动方法

如果说Bundle是将DUT的数据职责进行抽象的话，那么Agent则是将DUT的行为职责封装为一个个接口。简单地说，Agent通过封装多个对外开放的方法，将多组IO操作抽象为一个具体的行为：

```python

class RVCExpanderAgent(Agent):
    def __init__(self, bundle:RVCExpanderIOBundle):
        super().__init__(bundle)
        self.bundle = bundle
    
    @driver_method()
    async def expand(self, instr, fsIsOff):             # 传入参数：RVC指令和fs.status使能情况
        self.bundle._in.value = instr                   # 引脚赋值
        self.bundle._fsIsOff.value = fsIsOff            # 引脚赋值
        
        await self.bundle.step()                        # 推动时钟
        return self.bundle._out_bits.value,             # 返回值：扩展后指令
                self.bundle._ill.value                  # 返回值：指令合法校验
```

譬如，RVCExpander的指令扩展功能接收输入的指令（可能为RVI指令，也可能为RVC指令）和CSR对fs\.status的使能情况。我们将这个功能抽象为expand方法，提供除self以外的两个参数。同时，指令扩展最终将会返回传入指令对应的RVI指令和该指令是否合法的判断，对应地，该方法也返回这两个值。

### Env：测试环境

```python
class RVCExpanderEnv(Env):
    def __init__(self, dut:DUTRVCExpander):
        super().__init__()
        dut.io_in.xdata.AsImmWrite()        
        dut.io_fsIsOff.xdata.AsImmWrite()   # 设置引脚写入时机
        self.agent = RVCExpanderAgent(RVCExpanderIOBundle.from_prefix("io").bind(dut)) # 补全前缀，绑定DUT
```

### 覆盖率定义

定义覆盖率组的方式和前述方式类似，这里就不再赘述了。

### 测试套件定义

测试套件的定义略有不同：

```python
@toffee_test.fixture
async def rvc_expander(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    version_check()
    dut = toffee_request.create_dut(DUTRVCExpander)
    start_clock(dut)
    init_rvc_expander_funcov(dut, gr)
    
    toffee_request.add_cov_groups([gr])
    expander = RVCExpanderEnv(dut)
    yield expander

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
```

由于toffee提供了更强大的测试覆盖率管理功能，因此不需要手动设置行覆盖率。同时，由于toffee的时钟机制，建议在套件代码最后额外检查任务是否全部结束。