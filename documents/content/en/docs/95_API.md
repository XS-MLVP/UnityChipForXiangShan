---
title: Common APIs
linkTitle: Common APIs
#menu: {main: {weight: 99}}
weight: 95
---

## comm Module

The comm module provides some commonly used APIs, which can be called in the following ways:

```python
# import all
from comm import *
# or direct import functions you need
from comm import function_you_need
# or access from module
import comm
comm.function_you_need()
```

### cfg Submodule

#### get_config(cfg=None)
Get the current Config configuration
- Input: If cfg is not empty, return cfg. Otherwise, automatically get the global Config via toffee.
- Return: Config object

```python
import comm
cfg = comm.get_config()
print(cfg.rtl.version)
```

#### cfg_as_str(cfg: CfgObject)
Convert the config object to a string type
- Input: Config object
- Return: Encoded Config object

```python
import comm
cfg_str = comm.cfg_as_str(comm.get_config())
```

#### cfg_from_str(cfg_str)
Restore the Config object from a string
- Input: Encoded Config object
- Return: Config object

```python
import comm
cfg = comm.cfg_from_str(cfg_str)
```

#### dump_cfg(cfg: CfgObject = None, cfg_file=None)
Save the config object to a file
- Input:
  - cfg: the config to save
  - cfg_file: target file

```python
import comm
cfg = comm.get_config()
comm.dump_cfg(cfg, "config.yaml")
```

### functions Submodule

#### get_log_dir(subdir="", cfg=None)
Get the log directory
- Input:
   - subdir: subdirectory
   - cfg: config file
- Output: log directory

```python
import comm
my_log = comm.get_log_dir("my_log")
print(my_log) # /workspace/UnityChipForXiangShan/out/log/my_log
```

#### get_out_dir(subdir="", cfg=None)
Get the output directory
- Input:
   - subdir: subdirectory
   - cfg: config file
- Output: output directory

#### get_rtl_dir(subdir="", cfg=None)
Get the RTL directory
- Input:
   - subdir: subdirectory
   - cfg: config file
- Output: RTL directory

#### get_root_dir(subdir="")
Get the root directory:
- Input: subdirectory under the root directory
- Output: root directory of the current repository

#### is_all_file_exist(files_to_check, dir)
Check whether all files exist in the specified directory
- Input:
  - files_to_check: list of files to check
  - dir: target directory
- Output: whether all exist; returns False if any file does not exist

#### time_format(seconds=None, fmt="%Y%m%d-%H%M%S")
Format time
- Input:
  - seconds: time to format, None means current time
  - fmt: time format
- Return: formatted time string
```python
import comm
import time
print(time_format(time.time())) # 20241202-083726
```

#### base64_encode(input_str)
Base64 encode:
- Input: string to encode
- Output: encoded string
```python
import comm
print(comm.base64_encode("test")) # dGVzdA==
```

#### base64_decode(base64_str)
Base64 decode:
- Input: base64 encoded string
- Output: decoded original string
```python
import comm
print(comm.base64_decode("dGVzdA==")) # test
```

#### exe_cmd(cmd, no_log=False)
Execute an OS command:
- Input:
  - cmd: OS command to execute
  - no_log: whether to return command line output
- Output: success, stdout, stderr
  - success: whether the command executed successfully
  - command standard output string (forced to empty if no_log=True)
  - command standard error string (forced to empty if no_log=True)

```python
import comm
su, st, er = exe_cmd("pwd")
print(st)
```

#### get_git_commit()
Get the current repository git commit hash

#### get_git_branch()
Get the current repository git branch name

#### UT_FCOV(group, ignore_prefix="ut_")
Get function coverage group
- Input:
  - group: group name
  - ignore_prefix: prefix to remove
- Output: coverage group name with module prefix

For example, called in `ut_backend/ctrl_block/decode/env/decode_wrapper.py`:
```python
print(UT_FCOV("../../INT"))
# out
backend.ctrl_block.decode.INT
```

#### get_version_checker(target_version)
Get version check function
- Input: target version string
- Output: check function

The returned check function is usually used for version checking in fixtures.
```python
import comm
import pytest

checker = comm.get_version_checker("openxiangshan-kmh-24092701+")

@pytest.fixture
def fixture():
  checker()
  ...
```

#### module_name_with(names, prefix=None)
Add a module prefix to names
- Input:
  - names: list of strings to add prefix to
  - prefix: module prefix
- Return: list of strings with prefix added

For example, called in a/b/c/d/e.py:
```python
import comm
print(comm.module_name_with(["X", "Y"], "../../x"))
# out
["a.b.c.x.X", "a.b.c.x.Y"]
```

#### `get_all_rtl_files(top_module, cfg)`

Get a list of all RTL files (`.v` or `.sv`) that the module named `top_module` depends on, and ensure that the first element of the list is the absolute path of the file where `top_module` is located. All RTL files are located in the `UnityChipForXiangShan/rtl/rtl` directory.

- Input:
  - `top_module`: module name, type `str`
  - `cfg`: config info, type `CfgObject`

- Output:
  - Returns a list of strings, each string is the absolute path of an RTL file that the module depends on. The first element of the list is the path of the file where `top_module` is located.

Suppose `top_module` is `"ALU"`, and its dependent RTL files include `ALU.sv`, `adder.v`, and `multiplier.v`:
```python
paths = get_all_rtl_files("ALU", cfg)

"""
Possible contents of paths:
[
    "/path/to/UnityChipForXiangShan/rtl/rtl/ALU.sv",
    "/path/to/UnityChipForXiangShan/rtl/rtl/adder.v",
    "/path/to/UnityChipForXiangShan/rtl/rtl/multiplier.v"
]
"""
```
