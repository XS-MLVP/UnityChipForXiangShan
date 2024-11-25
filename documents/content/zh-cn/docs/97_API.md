---
title: 常用API
linkTitle: 常用API
#menu: {main: {weight: 99}}
weight: 97
---

## comm 模块

在comm中提供了部分可公用的API，可通过以下方式进行调用：

```python
# import all
from comm import *
# or direct import functions you need
from com import function_you_need
# or access from module
import comm
comm.function_you_need()
```

### cfg 子模块


#### get_config(cfg=None)
获取当前的Config配置
- 输入：如果cfg不为空，则返回cfg。否则则自动通过toffee获取全局Config。
- 返回：Config对象

#### cfg_as_str(cfg: CfgObject):
把config对象转换为字符类型
- 输入：Config对象
- 返回：编码后的Config对象

#### cfg_from_str(cfg_str)
把字符类型的Config对象还原
- 输入：编码后的Config对象
- 返回：Config对象

#### dump_cfg(cfg: CfgObject = None, cfg_file=None)
把config对象保持到文件
- 输入：
  - cfg 需要保存的config
  - cfg_file 目标文件

### functions 子模块

#### merge_dict(dict1, dict2)
将dict2中的内容，合并到dict1
- 输入：2个dict类型的字典
- 返回：合并之后的字典

#### get_log_dir(subdir="", cfg=None)
获取日志目录
- 输入：
   - subdir： 子目录
   - cfg：配置文件
- 输出：日志目录

#### get_out_dir(subdir="", cfg=None)
获取输出目录
- 输入：
   - subdir： 子目录
   - cfg：配置文件
- 输出：输出目录


#### get_rtl_dir(subdir="", cfg=None)
获取RTL目录
- 输入：
   - subdir： 子目录
   - cfg：配置文件
- 输出：RTL目录


#### get_root_dir(subdir="")
获取根目录：
- 输入：根目录下的子目录
- 输出：当前仓库的根目录


#### is_all_file_exist(files_to_check, dir)
判断文件是否在指定目录中都存在
- 输入：
  - files_to_check: 需要检查的文件列表
  - dir：目标目录
- 输出：是否都存在，只要有一个文件不存在都返回False


#### time_format(seconds=None, fmt="%Y%m%d-%H%M%S")
格式化时间
- 输入：
  - seconds：需要格式化的时间，为None表示当前时间
  - fmt：时间格式
- 返回：格式化之后的时间字符串


#### base64_encode(input_str)
base64编码：
- 输入：需要编码的字符串
- 输出：编码之后的字符串


#### base64_decode(base64_str)
base64解码：
- 输入：bas64编码
- 输出：解码之后的原始字符串


#### exe_cmd(cmd, no_log=False)
执行操作系统命令：
- 输入：
  - cmd：需要执行的os命令
  - 是否需要返回命令行输出
- 输出：success，stdout、sterr
  - sucess：命令是否执行成功
  - 命令标准输出字符串（no_log=True时，强制为空）
  - 命令标准错误字符串（no_log=True时，强制为空）


#### get_git_commit()
获取当前仓库git commit号


#### get_git_branch()
获取当前仓库git 分支名称


#### UT_FCOV(group, ignore_prefix="ut_")
获取功能覆盖率分组
- 输入：
  - group 分组名称
  - ignore_prefix需要去掉的前缀
- 输出：带模块前缀的覆盖率分组名

例如，在`ut_backend/ctrl_block/decode/env/decode_wrapper.py`中调用：
```python
print(UT_FCOV("../../INT"))
# out
backend.ctrl_block.decode.INT
```


#### get_version_checker(target_version)
获取版本检测函数
- 输入：目标版本字符串
- 输出：检测函数

返回的检测函数，一般在fixture中进行版本判断。


#### module_name_with(names, prefix=None)
给names统一加上模块前缀
- 输入：
  - nanmes 需要添加前缀的字符列表
  - prefix 模块前缀
- 返回：添加完成后的字符串列表

例如在a/b/c/d/e.py文件中调用该方法：
```python
import comm
print(comm.module_name_with(["X", "Y"], ,"../../x"))
# out
["a.b.c.x.X", "a.b.c.x.Y"]
```
