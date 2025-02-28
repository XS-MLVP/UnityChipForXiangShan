---
title: 其他
linkTitle: 其他
#menu: {main: {weight: 99}}
weight: 96
---

## 测试用例管理

如果测试用例和目标RTL版本紧密相关，RTL发生变化，之前的测试用例不一定适用。此外，不同场景下有不同需求，例如验证测试环境时，不运行耗时太长的用例等。因此需要对用例进行管理，让用户能在在特定场景下跳过某些用例。为了实现该目标，我们需要通过`pytest.mark.toffee_tags`对于每个用例进行tag和version标记。然后在配置文件中设置需要跳过哪些tag或者只运行哪些tag的测试。

```python
@pytest.mark.toffee_tags("my_tag", "version1 < version13")
def test_case_1():
    ...
```

例如上述`test_case_1`被标记上了标签`my_tag`，支持版本设置为`version1`到`version13`。因此可以在配置文件中指定`test.skip-tags=["my_tag"]`，来表示运行过程中跳过该用例。

`pytest.mark.toffee_tags`的参数说明如下：

```python
@pytest.mark.toffee_tags(
    tag: Optional[list, str]     = []    # 用例标签
    version: Optional[list, str] = [],   # 用例rtl版本需求
    skip: callable               = None, # 自定义是否调过该用例，skip(tag, version, item): (skip, reason)
)
```

`toffee_tags`函数的参数`tag`支持`str`和`list[str]`类型。`version`参数也可以是`str`和`list[str]`类型，当为`list`类型时，进行精确匹配，如果为`str`则匹配规则如下：

1. `name-number1 < namer-number2:` 表示版本需要在`number1`和`number2`之间（包含边界，`number`表示数字，也可以为小数，eg `1.11`）
1. `name-number1+`：表示`number1`版本以及以后的版本
1. `name-number1-`：表示`number1`版本以及以前的版本

如果不存在上述情况，且有`*`或者`?`表示通配符类型。其他情况为精确匹配。

预定义标签，可以在comm/constants.py中查看，例如：

```python
# Predefined tags for test cases
TAG_LONG_TIME_RUN = "LONG_TIME_RUN"  # 运行时间长
TAG_SMOKE         = "SMOKE"          # 冒烟测试
TAG_RARELY_USED   = "RARELY_USED"    # 非常少用
TAG_REGRESSION    = "REGRESSION"     # 回归测试
TAG_PERFORMANCE   = "PERFORMANCE"    # 性能测试
TAG_STABILITY     = "STABILITY"      # 稳定测试
TAG_SECURITY      = "SECURITY"       # 安全测试
TAG_COMPATIBILITY = "COMPATIBILITY"  # 兼容测试
TAG_OTHER         = "OTHER"          # 其他
TAG_CI            = "CI"             # 集成测试
TAG_DEBUG         = "DEBUG"          # 测试
TAG_DEMO          = "DEMO"           # demo
```

在默认配置中(`config/_default.yaml`)，会过滤掉：`LONG_TIME_RUN`、`REGRESSION`、`RARELY_USED`、`CI` 标记的测试。


可以通过`@pytest.mark.toffee_tags`可以为每个用例添加标签，也可以在模块中定义如下变量，实现对整个模块的所有测试用例添加标签。



```python
toffee_tags_default_tag     = []   # 对应 tag 参数
toffee_tags_default_version = []   # 对应 version 参数
toffee_tags_default_skip    = None # 对应 skip 参数
```

*注：本环境中的版本号会自动过滤掉git标记，例如下载的RTL名称为`openxiangshan-kmh-97e37a2237-24092701.tar.gz`，则其版本号在本项目中为：`openxiangshan-kmh-24092701`, 可通过`cfg.rtl.version`或者`comm.get_config().rtl.version`获得。

## 版本检查

除了可以用标签`toffee_tags`自动检查版本外，还可以通过`get_version_checker`主动进行检查。一个单元测试通常由测试环境（Test Env）和测试用例组成（Test Case），Env对RTL引脚和功能进行封装，然后向Case提供稳定API，因此在Env中需要进行RTL版本判断，判断是否需要跳过使用本环境的所有测试用例。例如在Env中：

```python
...
from comm import get_version_checker

version_check = get_version_checker("openxiangshan-kmh-*") # 获取RTL版本检查器，同toffee_tags中的veriosn参数

@pytest.fixture()
def my_fixture(request):
    version_check()                                        # 在 fixture 中主动检查
    ....
    yield dut
    ...
```

在上述例子中，Env在名称为`my_fixture`的[fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html)中主动进行了版本检查。因此，在测试用例每次调用它时都会进行版本检查，如果检查不满足要求，则会跳过该用例的执行。


## 仓库目录说明


```bash
UnityChipForXiangShan
├── LICENSE            # 开源协议
├── Makefile           # Makefile主文件
├── README.en.md       # 英文readme
├── README.zh.md       # 中文readme
├── __init__.py        # Python模块文件，可以把整个UnityChipForXiangShan当成一个模块进行import
├── pytest.ini         # PyTest 配置文件
├── comm               # 公用组件：日志，函数，配置等
├── configs            # 配置文件目录
├── documents          # 文档
├── dut                # dut生成目录
├── out                # log，report等生成目录
├── requirements.txt   # python依赖
├── rtl                # rtl缓存
├── run.py             # 主python入口文件
├── scripts            # dut编译脚本
├── tools              # 公共工具模块
├── ut_backend         # 后端测试用例
├── ut_frontend        # 前端测试用例
├── ut_mem_block       # 访存测试用例
└── ut_misc            # 其他测试用例
```


## 配置文件说明


默认配置与说明如下：

```yaml
# 默认配置文件
# 配置加载顺序: _default.yaml -> 用户指定的 *.yaml -> 命令行参数 eg: log.term-level='debug'
# RTL 配置
rtl:
  # RLT下载地址，从该地址获取所有*.gz.tar文件当成目标RTL
  base-url: https://<your_rtl_download_address>
  # 需要下载的RTL版本 eg: openxiangshan-kmh-97e37a2237-24092701
  version: latest
  # 需要存储RTL的目录，相对于当前配置文件的路径
  cache-dir: "../rtl"
# 测试用例配置（tag和case支持通配符）
test:
  # 跳过标签，所有带有该标签的测试用例都会被跳过
  skip-tags: ["LONG_TIME_RUN", "RARELY_USED", "REGRESSION", "CI"]
  # 目标标签，只有带有该标签的测试用例才会被执行（skip-tags会覆盖run-tags）
  run-tags: []
  # 跳过的测试用例，所有带有该名字（或者模块名）的测试用例都会被跳过。
  skip-cases: []
  # 目标测试用例，只有带有该名字（或者模块名）的测试用例才会被执行（skip-cases会覆盖run-cases）。
  run-cases: []
  # 跳过异常，所有抛出该异常的测试用例都会被跳过
  skip-exceptions: []
# 输出配置
output:
  # 输出目录，相对于当前配置文件的路径
  out-dir: "../out"
# 测试报告配置
report:
  # 报告生成目录，相对于output.out-dir
  report-dir: "report"
  # 报告名称，支持变量替换：%{host} 主机名，%{pid} 进程ID，%{time} 当前时间
  report-name: "%{host}-%{pid}-%{time}/index.html"
  # 报告内容
  information:
    # 报告标题
    title: "XiangShan KMH Test Report"
    # 报告用户信息
    user:
      name: "User"
      email: "User@example.email.com"
    # 目标行覆盖率 eg: 90 表示 90%
    line_grate: 99
    # 其他需要展示的信息，key为标题，value为内容
    meta:
      Version: "1.0"
# 日志配置
log:
  # 根输出级别
  root-level: "debug"
  # 终端输出级别
  term-level: "info"
  # 文件日志输出级别
  file-dir: "log"
  # 文件日志名称，支持变量替换：%{host} 主机名，%{pid} 进程ID，%{time} 当前时间
  file-name: "%{host}-%{pid}-%{time}.log"
  # 文件日志输出级别
  file-level: "info"
# 测试结果配置（该数据用于填充documents中的统计图等，原始数据来源于toffee-test生成的report）
#  运行完测试后，可通过 `make doc` 查看结果
doc-result:
  # 是否开测试结果后处理
  disable: False
  # 目标DUT的组织结构配置
  dutree: "%{root}/configs/dutree/xiangshan-kmh.yaml"
  # 结果名称，将会保存到输出的report目录
  result-name: "ut_data_progress.json"
  # 创建的测试报告的软连接到 hugo
  report-link: "%{root}/documents/static/data/reports"
```

可在上述配置文件中添加自定义参数，通过`cfg = comm.get_config()`获取全局配置信息，然后通过`cfg.your_key`进行访问。`cfg`信息为只读信息，默认情况下不能进行修改。