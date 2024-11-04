---
title: 添加测试
linkTitle: 添加测试
#menu: {main: {weight: 20}}
weight: 15
---


添加一个全新的DUT测试用例，需要完成以下三部分内容：

1. **添加编译脚本**： 在`scripts`目录下编写对应的`rtl`到`python`的编译`Makefile`文件（例如Makefile.build_ut_**backend_ctrlblock_decode**，必须以`Makefile.build_ut_`开头）以及对应的目录（目录中包含必要的输入文件，例如`rtl`的`filelist`，需要导出的内部信号等）。
1. **添加测试用例**： 在对应的`ut_*`目录中创建对应的`python`模块（例如`ut_backend/ctrl_block/decode`）,在该模块中需要包含以`test_*.py`的测试用例。用例的目录结构请按照[昆明湖层级架构图](https://open-verify.cc/UnityChipForXiangShan/)进行添加，以确保收集测试结果时能与层级图对应。测试用例的编写方法请参考[Pytest官方文档](https://docs.pytest.org/en/stable/)。
1. **添加依赖模块**： 如果有需要的话，可以在`tools、comm`等模块中添加该DUT测试需要的基础工具。如果该工具不够通用请添加到对应的`ut_`模块中，且不能以`test_`前缀进行命名（例如参考模型可以是`ut_backend/ctrl_block/decode/reference.py`）

如果是在已有的DUT测试中增加内容，按原有目录结构添加即可。

*目录或文件名称需要合理，能通过其命名知晓其具体含义。

如何通过picker和toffee库进行Python芯片验证，请参考：[https://open-verify.cc/mlvp/docs](https://open-verify.cc/mlvp/docs)

### 测试用例管理

测试用例和目标RTL版本紧密相关，如果RTL发生变化，之前的测试用例不一定适用。此外，不同场景下有不通需求，例如开始测试时，不运行耗时太长的用例等。因此需要对用例进行管理，让用户能在在特定场景下跳过某些用例。为了实现该目标，我们需要通过`pytest.mark.toffee_tags`对于每个用例进行tag和version标记。然后在配置文件中设置需要跳过哪些tag或者只运行哪些tag的测试。

```python
@pytest.mark.toffee_tags("my_tag", "version1 < version13")
def test_case_1():
    ...
```

例如上述`test_case_1`被标记上了标签`my_tag`，支持版本设置为`version1`到`version13`。因此可以在配置文件中指定`test.skip-tags=["my_tag"]`，来表示运行过程中跳过该用例。预定义标签，请在comm/constants.py中查看。具体配置说明请参考[配置文件说明](#配置文件说明)。

`pytest.mark.toffee_tags`的参数说明如下：

```python
@pytest.mark.toffee_tags(
    tag: Optional[list, str]     = []    # 用例标签
    version: Optional[list, str] = [],   # 用例rtl版本需求
    skip: callable               = None, # 自定义是否调过该用例，skip(tag, version, item): (skip, resion)
)
```

`toffee_tags`函数的参数`tag`支持`str`和`list[str]`类型。`version`参数也可以是`str`和`list[str]`类型，当为`list`类型时，进行精确匹配，如果为`str`则匹配规则如下：

1. `name-number1 < namer-number2:` 表示版本需要在`number1`和`number2`之间（包含边界，`number`表示数字，也可以为小数，eg `1.11`）
1. `name-number1+`：表示`number1`版本以及以后的版本
1. `name-number1-`：表示`number1`版本以及以前的版本

如果不存在上述情况，且有`*`或者`?`表示通配符类型。其他情况为精确匹配。


可以通过`@pytest.mark.toffee_tags`可以为每个用例添加标签，也可以在模块中定义如下变量，实现对整个模块的所有测试用例添加标签。


```python
toffee_tags_default_tag     = []   # 对应 tag 参数
toffee_tags_default_version = []   # 对应 version 参数
toffee_tags_default_skip    = None # 对应 skip 参数
```


### 仓库目录说明


```bash
UnityChipForXiangShan
├── LICENSE            # 开源协议
├── Makefile           # Makefile主文件
├── README.en.md       # 英文readme
├── README.zh.md       # 中文readme
├── __init__.py        # Python模块文件，可以把整个UnityChipForXiangShan当成一个模块进行import
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


### 配置文件说明


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
  skip-tags: ["LONG_TIME_RUN"]
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
```
