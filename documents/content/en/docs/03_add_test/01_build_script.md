---
title: Add Compilation Script
linkTitle: Add Compilation Script
#menu: {main: {weight: 20}}
weight: 2
---

## Script Target

Write a compilation file for the corresponding RTL in the `scripts` directory using Python (e.g., `build_ut_frontend_ifu_rvc_expander.py`).  
The goal of this script is to provide RTL-to-Python DUT compilation, target coverage files, and custom functionality.

## Creation Process

### Determine File Name

Select the UT to be verified in [XiangShan Kunming Lake DUT Verification Progress](). If it is not available or needs further refinement, you can manually add it by editing `configs/dutree/xiangshan-kmh.yaml`.  
For example, if we want to verify the `rvc_expander` module under the `ifu` module in the frontend, we need to add the corresponding part to `configs/dutree/xiangshan-kmh.yaml` (this module already exists in the YAML file; this is just an example):

```yaml
name: "kmh_dut"
desc: "All Kunming Lake DUTs"
children:
  - name: "frontend"
    desc: "Frontend Module"
    children:
      - name: "ifu"
        desc: "Instruction Fetch Unit"
        children:
          - name: "rvc_expander"
            desc: "RVC Instruction Expander"
```

The naming format for the script file is as follows:

```bash
scripts/build_<top_module>_<sub_module>_..._<target_module>.py
```

Currently, the project includes four top-level modules:

1. ut_frontend (Frontend)
1. ut_backend (Backend)
1. ut_mem_block (Memory Access)
1. ut_misc (Miscellaneous)

Submodules do not have the `ut_` prefix (the top-level directories have this prefix to distinguish them from other directories).

For example, if the target DUT to be verified is the `rvc_expander` module:  
This module belongs to the frontend, so the top-level module is `ut_frontend`. Its submodule is `ifu`, and the target module is `rvc_expander`.  
From the previously opened `yaml` file, we can also see that the `children` of `frontend` is `ifu`, and the `children` of `ifu` is `rvc_expander`.  
Thus, the script name to be created is `build_ut_frontend_ifu_rvc_expander.py`.

### Write the `build(cfg) -> bool` Function

The `build` function is defined as follows:

```python
def build(cfg) -> bool:
    """Compile DUT
    Args:
        cfg: Runtime configuration, which can be used to access configuration items, e.g., cfg.rtl.version
    Return:
        Returns True or False, indicating whether the function achieved its intended goal
    """
```

The `build` function is called during `make dut`. Its main purpose is to convert the target RTL into a Python module. Other necessary processes, such as compiling dependencies, can also be added. For example, in `build_ut_frontend_ifu_rvc_expander.py`, the function primarily performs RTL checks, DUT checks, RTL compilation, and disasm dependency compilation:

```python
import os
from comm import warning, info


def build(cfg):
    # Import related dependencies
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # Check RTL version (an empty version parameter means all versions are supported)
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("ifu frontend rvc expander: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # Check if the target file exists in the current RTL
    f = is_all_file_exist(["rtl/RVCExpander.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # If the DUT does not contain RVCExpander, use picker to package it into Python
    if not os.path.exists(get_root_dir("dut/RVCExpander")):
        info("Exporting RVCExpander.sv")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/RVCExpander.sv", cfg=cfg)} --lang python --tdir {get_root_dir("dut")}/ -w rvc.fst -c')
        assert s, "Failed to export RVCExpander.sv: %s\n%s" % (out, err)
    # If disasm/build does not exist in tools, compile disasm
    if not os.path.exists(get_root_dir("tools/disasm/build")):
        info("Building disasm")
        s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
        assert s, "Failed to build disasm"
    # Compilation successful
    return True

def line_coverage_files(cfg):
    return ["RVCExpander.v"]
```

For details on how to use `picker`, refer to its [documentation](https://github.com/XS-MLVP/picker/blob/master/README.zh.md) and [usage guide](https://open-verify.cc/mlvp/docs/env_usage/picker_usage/).

In the `scripts` directory, you can create subdirectories to store files needed for UT verification. For example, the `rvc_expander` module creates a `scripts/frontend_ifu_rvc_expander` directory, where `rtl_file.f` specifies the input RTL file, and `line_coverage.ignore` stores lines of code to be ignored in coverage statistics. Custom directory names should be reasonable and should indicate the module and file they belong to.

### Write the `line_coverage_files(cfg) -> list[str]` Function

The `line_coverage_files` function is defined as follows:

```python
def line_coverage_files(cfg) -> list[str]:
    """Specify files to be covered
    Args:
        cfg: Runtime configuration, which can be used to access configuration items, e.g., cfg.rtl.version
    Return:
        Returns the names of RTL files targeted for line coverage statistics
    """
```

In the `build_ut_frontend_ifu_rvc_expander.py` file, the `line_coverage_files` function is defined as follows:

```python
def line_coverage_files(cfg):
    return ["RVCExpander.v"]
```

This indicates that the module focuses on coverage for the `RVCExpander.v` file. If you want to enable test result processing, set `disable=False` under `doc-result` in `configs/_default.yaml` (the default parameter is `False`, meaning it is enabled). If you do not enable test result processing (`disable=True`), the above function will not be called.
