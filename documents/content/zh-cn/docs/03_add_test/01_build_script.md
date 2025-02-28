---
title: 添加编译脚本
linkTitle: 添加编译脚本
#menu: {main: {weight: 20}}
weight: 2
---

## 脚本目标

在`scripts`目录下使用python编写对应rtl的编译文件（例如`build_ut_frontend_ifu_rvc_expander.py`）。   
该脚本的目标是提供 RTL 到 Python DUT 的编译、目标覆盖文件，以及自定义功能等内容。

## 创建过程

### 确定文件名称

在[香山昆明湖 DUT 验证进展]()中选择需要验证的 UT，如果没有或者进一步细化，可通过编辑`configs/dutree/xiangshan-kmh.yaml`自行添加。   
比如，我们要验证的是前端部分的`ifu`模块下的`rvc_expander`模块，那么需要在`configs/dutree/xiangshan-kmh.yaml`中添加对应的部分（目前yaml中已经有该模块了，此处为举例）：

```yaml
name: "kmh_dut"
desc: "所有昆明湖DUT"
children:
  - name: "frontend"
    desc: "前端模块"
    children:
      - name: "ifu"
        desc: "指令单元 (Instruction Fetch Unit)"
        children:
          - name: "rvc_expander"
            desc: "RVC指令扩充器"
```

脚本文件的命名格式如下：

```bash
scripts/build_<顶层模块>_<下层模块名>_..._<目标模块名>.py
```

目前本项目内置了 4 个顶层模块：

1. ut_frontend 前端
1. ut_backend 后端
1. ut_mem_block 访存
1. ut_misc 其他

其中的子模块没有`ut_`前缀（顶层目录有该前缀是为了和其他目录区分开）。

例如验证目标 DUT 为`rvc_expander`模块：  
该模块是属于前端的，所以顶级模块为`ut_frontend`，它的下层模块为`ifu`，目标模块为`rvc_expander`。  
通过刚才我们打开的`yaml`文件也可以知道，`frontend`的children 为`ifu`，`ifu`的children 为`rvc_expander`。    
所以，需要创建的脚本名称为`build_ut_frontend_ifu_rvc_expander.py`。


### 编写 build(cfg) -> bool 函数

build 函数定义如下：

```python
def build(cfg) -> bool:
    """编译DUT
    Args:
        cfg: 运行时配置，可通过它访问配置项，例如 cfg.rtl.version
    Return:
        返回 True 或者 False，表明该函数是否完成预期目标
    """
```

build 在 make dut 时会被调用，其主要是将目标 RTL 转换为 Python 模块。在该过程中也可以加入其他必要过程，例如编译依赖项等。以`build_ut_frontend_ifu_rvc_expander.py`为例，主要完成了 RTL 检查、DUT 检查、RTL 编译、disasm 依赖编译等工作：

```python
import os
from comm import warning, info


def build(cfg):
    # import 相关依赖
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # 检查RTL版本（version参数为空，表示所有版本都支持）
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("ifu frontend rvc expander: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # 检查在当前RTL中，目标文件是否存在
    f = is_all_file_exist(["rtl/RVCExpander.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # 如果dut中不存在RVCExpander，则调用picker进行Python打包
    if not os.path.exists(get_root_dir("dut/RVCExpander")):
        info("Exporting RVCExpander.sv")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/RVCExpander.sv", cfg=cfg)} --lang python --tdir {get_root_dir("dut")}/ -w rvc.fst -c')
        assert s, "Failed to export RVCExpander.sv: %s\n%s" % (out, err)
    # 如果tools中不存在disasm/build，则需要编译disasm
    if not os.path.exists(get_root_dir("tools/disasm/build")):
        info("Building disasm")
        s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
        assert s, "Failed to build disasm"
    # 编译成功
    return True

def line_coverage_files(cfg):
    return ["RVCExpander.v"]
```

picker 的使用方式请参考其[文档](https://github.com/XS-MLVP/picker/blob/master/README.zh.md)和[使用](https://open-verify.cc/mlvp/docs/env_usage/picker_usage/)

在`scripts`目录中可以创建子目录保存 UT 验证需要的文件，例如 rvc_expander 模块创建了`scripts/frontend_ifu_rvc_expander`目录，其中的`rtl_file.f`用来指定输入的 RTL 文件，`line_coverage.ignore`用来保存需要忽略的代码行统计。自定义目录的命名需要合理，且能通过名字判断其所属模块和文件。

### 编写 line_coverage_files(cfg) -> list[str] 函数

line_coverage_files 函数的定义如下：

```python
def line_coverage_files(cfg)-> list[str]:
    """指定需要覆盖的文件
    Args:
        cfg: 运行时配置，可通过它访问配置项，例如 cfg.rtl.version
    Return:
        返回统计代码行覆盖率的目标RTL文件名
    """
```

在`build_ut_frontend_ifu_rvc_expander.py`文件中，`line_coverage_files`函数的定义如下：

```python
def line_coverage_files(cfg):
    return ["RVCExpander.v"]
```

标识该模块关注的是对`RVCExpander.v`文件的覆盖。如果要开启测试结果处理，还需要在`configs/_default.yaml`中的`doc-result`下`disable=False`（默认参数是`False`，也就是开启状态）;如果不开启测试结果处理则(`disable = True`)。注意，如果不开启测试结果处理，那么上述函数就不会被调用。
