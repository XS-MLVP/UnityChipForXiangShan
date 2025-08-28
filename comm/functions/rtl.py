# coding=utf8
# ***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
# **************************************************************************************/

import os
import re
import shutil
import subprocess

from pathlib import Path

__all__ = [
    "get_all_rtl_files",
    "extract_signals"
]

from collections import deque

from typing import List

from .utils import get_root_dir
from comm.functions.cfg import get_rtl_dir


def get_defined_modules(file: str) -> List[str]:
    cmd = ["sed", "-n", r"s/^ *module \+\([^ (]\+\).*/\1/p", file]
    ret = subprocess.run(cmd, cwd=get_root_dir(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert ret.returncode == 0, ret.stderr
    return ret.stdout.decode().splitlines()


def get_instant_modules(file: str) -> List[str]:
    verible_bin = shutil.which("verible-verilog-syntax")
    assert verible_bin, "verible-verilog-syntax is not installed"
    verible_cmd = [verible_bin, "--printtokens", file]
    sed_cmd = [
        "sed", "-n",
        r'/#SymbolIdentifier/ { N; /#SymbolIdentifier.*\n.*#SymbolIdentifier/ s/.*"\([^"]*\)".*\n.*/\1/p }'
    ]
    sort_cmd = ["sort", "-u"]

    # Run verible-verilog-syntax to get the tokens of verilog file
    verible_proc = subprocess.Popen(verible_cmd, cwd=get_root_dir(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Run sed to get the names of all instant modules
    sed_proc = subprocess.Popen(sed_cmd, stdin=verible_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Run sort to unique output
    sort_proc = subprocess.Popen(sort_cmd, stdin=sed_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    verible_proc.stdout.close()
    verible_out, verible_err = verible_proc.communicate()
    assert verible_proc.returncode == 0, verible_err

    sed_proc.stdout.close()
    sed_out, sed_err = sed_proc.communicate()
    assert sed_proc.returncode == 0, sed_err

    sort_out, sout_err = sort_proc.communicate()
    return sort_out.decode().splitlines()


def get_all_rtl_files(top_module: str, cfg) -> list[str]:
    """Recursively finds all Verilog source files for a given top module.

    This function traverses the Verilog module hierarchy starting from `top_module`
    to identify all dependent source files. It parses Verilog files to find
    module instantiations and recursively resolves their file paths.

    Note:
        This function assumes that each Verilog file contains only one module
        definition and that the filename matches the module name (e.g., module
        `my_fifo` is in `my_fifo.v`).

    Args:
        top_module (str): The name of the top-level module to start the search from.
        cfg: A configuration object used to determine the root directory for the
             RTL file search.

    Returns:
        list[str]: An ordered list of file paths for the top module and all its
                   submodule dependencies.
    """
    from collections import OrderedDict

    module_path: dict[str, str] = OrderedDict()
    instants = deque([top_module])
    rtl_dir = Path(get_rtl_dir(cfg=cfg))
    while instants:
        t = instants.popleft()
        for path in rtl_dir.rglob(f"**/{t}.*v"):
            if t in module_path:
                break
            p = str(path.absolute())
            module_path[t] = p
            for i in get_instant_modules(p):
                if i not in module_path:
                    instants.append(i)
    dependencies = list(module_path.values())
    return dependencies


def extract_signals(verilog_file: str, output_file: str) -> None:
    """Extracts wire/reg signals from a Verilog file into a YAML file.

    This function parses a Verilog source file to find all `wire` and `reg`
    declarations. It then formats these signal definitions and writes them
    to a specified YAML file. The `reg` type is converted to `logic`.

    Args:
        verilog_file (str): The path to the input Verilog source file.
        output_file (str): The path where the output YAML file will be saved.
    """
    # 定义匹配 wire 和 reg 的正则表达式
    signal_pattern = re.compile(r'\b(wire|reg)\b\s*(\[[^\]]+\])?\s*([\w, ]+)(;|=)')

    extracted_signals = []

    # 读取 sv 文件内容
    with open(verilog_file, 'r') as file:
        lines = file.readlines()

    # 逐行解析
    for line in lines:
        match = signal_pattern.search(line)
        if not match:
            continue
        signal_type = match.group(1)  # wire or reg
        width = match.group(2) if match.group(2) else ""  # [8:0] or empty
        names = match.group(3)  # 信号名
        if signal_type == "reg":
            signal_type = "logic"
        # 分解信号名并格式化
        if width == "":
            for name in names.split(','):
                extracted_signals.append(f"  - \"{signal_type} {name.strip()}\"")
        else:
            for name in names.split(','):
                extracted_signals.append(f"  - \"{signal_type} {width.strip()} {name.strip()}\"")

    # 写入到 yaml 文件
    basename = os.path.basename(verilog_file)
    filename = os.path.splitext(basename)[0]
    with open(output_file, 'w') as file:
        file.write(filename + ':\n')
        for signal in extracted_signals:
            file.write(signal + '\n')
