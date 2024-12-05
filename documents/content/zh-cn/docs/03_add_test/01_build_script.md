---
title: 添加编译脚本
linkTitle: 添加编译脚本
#menu: {main: {weight: 20}}
weight: 2
---

## 脚本目标

该脚本的目标是提供RTL到Python DUT的编译、目标覆盖文件，以及自定义功能等内容。

## 创建过程

### 确定文件名称

在[香山昆明湖DUT验证进展]()中选择需要验证的UT，如果没有或者进一步细化，可通过编辑`configs/dutree/xiangshan-kmh.yaml`自行添加。

脚本文件的命名格式如下：

```bash
scripts/build_<顶层模块>_<下层模块名>_..._<目标模块名>.py
```

目前本项目内置了4个顶层模块：
1. ut_frontend 前端
1. ut_backend 后端
1. ut_mem_block 访存
1. ut_misc 其他

其中的子模块没有`ut_`前缀（顶层目录有该前缀是为了和其他目录区分开）。

例如验证目标DUT为：`backend.ctrl_block.decode`，需要创建的脚本名称为 `build_ut_backend_ctrl_block_decode.py`。

### 编写 build(cfg) -> bool 函数

build函数定义如下：
```python
def build(cfg) -> bool:
    """编译DUT
    Args:
        cfg: 运行时配置，可通过它访问配置项，例如 cfg.rtl.version
    Return:
        返回 True 或者 False，表明该函数是否完成预期目标
    """
```

build在make dut 时会被调用，其主要是将目标 RTL 转换为 Python 模块。在该过程中也可以加入其他必要过程，例如编译依赖项等。以`build_ut_backend_ctrl_block_decode.py`为例，主要完成了RTL检查、DUT检查、RTL编译、disasm依赖编译等工作：

```python
def build(cfg) -> bool:
    # import 相关依赖
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # 检查RTL版本（version参数为空，表示所有版本都支持）
    if not match_version(cfg.rtl.version, []):
        warning("backend_ctrlblock_decode: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # 检查在当前RTL中，目标文件是否存在
    f = is_all_file_exist(["rtl/RVCExpander.sv", "rtl/PreDecode.sv", "rtl/DecodeStage.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # 如果dut中不存在RVCExpander/PreDecode/DecodeStage，则调用picker进行Python打包
    if not os.path.exists(get_root_dir("dut/RVCExpander")):
        info("Exporting RVCExpander.sv")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/RVCExpander.sv", cfg=cfg)
                                                              } --lang python --tdir {get_root_dir("dut")}/ -w rvc.fst -c')
        assert s, "Failed to export RVCExpander.sv: %s\n%s" % (out, err)
    if not os.path.exists(get_root_dir("dut/PreDecode")):
        info("Exporting PreDecode.sv")
        s, _, _ = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/PreDecode.sv", cfg=cfg)
                                                          } --lang python --tdir {get_root_dir("dut")}/ -w predecode.fst -c')
        assert s, "Failed to export PreDecode.sv"
    if not os.path.exists(get_root_dir("dut/DecodeStage")):
        info("Exporting DecodeStage.sv")
        s, _, _ = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/DecodeStage.sv", cfg=cfg)
                                                          } --fs {
                                                            get_root_dir("scripts/backend_ctrlblock_decode/rtl_files.f")
                                                            } --lang python --tdir {get_root_dir("dut")}/ -w decode.fst -c')
        assert s, "Failed to export DecodeStage.sv"
    # 如果tools中不存在disasm/build，则需要编译disasm
    if not os.path.exists(get_root_dir("tools/disasm/build")):
        info("Building disasm")
        s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
        assert s, "Failed to build disasm"
    # 编译成功
    return True
```

picker的使用方式请参考其[使用文档]()

在`scripts`目录中可以创建子目录保存UT验证需要的文件，例如decode模块创建了`scripts/backend_ctrlblock_decode`目录，其中的`rtl_file.f`用来指定输入的RTL文件，`line_coverage.ignore`用来保存需要忽略的代码行统计。自定义目录的命名需要合理，且能通过名字判断其所属模块和文件。


### 编写 line_coverage_files(cfg) -> list[str] 函数


line_coverage_files函数的定义如下：
```python
def line_coverage_files(cfg)-> list[str]:
    """指定需要覆盖的文件
    Args:
        cfg: 运行时配置，可通过它访问配置项，例如 cfg.rtl.version
    Return:
        返回统计代码行覆盖率的目标RTL文件名
    """
```

在`build_ut_backend_ctrl_block_decode.py`文件中，`line_coverage_files`函数的定义如下：

```python
def line_coverage_files(cfg):
    return ["PreDecode.v", "DecodeStage.v"]
```

标识该模块关注的是对`PreDecode.v`, `DecodeStage.v`文件的覆盖。如果不开启测试结果后处理(`cfg.doc_result.disable = False`)，上述函数则不会被调用。
