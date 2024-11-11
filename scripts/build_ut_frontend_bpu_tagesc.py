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

__all__ = ["build", "line_coverage_files"]

from comm import CfgObject


def get_rtl_dependencies(top_module: str, cfg: CfgObject) -> list[str]:
    """
    Get the file path of all modules that `top_module` depends on and
    the first element of the list is the path of `top_module`.

    This function works only when there is **only on module** in the file
    and the **file name is the module name**.
    """
    import re
    from glob import iglob
    from collections import OrderedDict

    some_verilog_keywords = {
        'for', 'real', 'initial', 'input', 'endcase', 'typedef', 'primitive', 'always_comb', 'always_latch', 'negedge',
        'repeat', 'while', 'endfunction', 'int', 'output', 'wire', 'logic', 'reg', 'assign', 'function', 'case',
        'always_ff', 'if', 'posedge', 'table', 'end', 'task', 'forever', 'enum', 'endtask', 'module', 'localparam',
        'timescale', 'endprimitive', 'else', 'endtable', 'always', 'parameter', 'time', 'endmodule', 'begin',
        "and", "or", "not", "xor"
    }

    modulename_pattern = re.compile(r"\bmodule\s+(\w+)\b")
    instance_pattern = re.compile(r"\b(\w+)\s+(?!module)(\w+)\s*\(")
    module_path_map = OrderedDict()

    def parser_verilog_file(path: str) -> tuple[set, set]:
        _module_set = set()
        _inst_set = set()

        def remove_inline_comments(s: str) -> str:
            # Remove the line comment first
            s = re.sub(r"//.*$", "", s)
            # Then remove the block comment
            return re.sub(r'/\*.*?\*/', "", s)

        def parse_line(line_text: str) -> None:
            _line = remove_inline_comments(line_text)

            # Extract names of declared modules
            module_matches = modulename_pattern.finditer(_line)
            for match in module_matches:
                _name = match.group(1)
                _module_set.add(_name)

            # Extract names of instanced modules
            instance_matches = instance_pattern.finditer(_line)
            for match in instance_matches:
                _name = match.group(1)
                if _name not in some_verilog_keywords:
                    _inst_set.add(_name)

        """Code Begin Here"""
        block_comment_depth = 0
        pending_line = ''

        with open(path, "r") as file:
            while True:
                chunk = file.read(32768)
                if not chunk:
                    break

                lines = ("".join((pending_line, chunk))).split("\n")
                if lines:
                    pending_line = lines.pop()

                for line in lines:
                    # for block comment
                    start_pos = line.find("/*")
                    end_pos = line.find("*/")
                    while start_pos != -1 or end_pos != -1:
                        # if '/*' appears before '*/', increase depth
                        if start_pos != -1 and (end_pos == -1 or start_pos < end_pos):
                            block_comment_depth += 1
                            line = " ".join((line[:start_pos], line[start_pos + 2:]))
                        # if '*/' appears before '/*', decrease depth
                        elif end_pos != -1:
                            block_comment_depth -= 1
                            line = " ".join((line[:end_pos], line[end_pos + 2:]))
                        start_pos = line.find("/*")
                        end_pos = line.find("*/")

                    # skip if content of current line is in block comment
                    if block_comment_depth > 0:
                        continue
                    parse_line(line)
        if pending_line:
            parse_line(pending_line)
        return _module_set, _inst_set

    def get_rtl_dep(top_module_name: str) -> None:
        from comm import get_rtl_dir
        # Walk through the rtl dir
        rtl_dir = os.path.join(str(get_rtl_dir(cfg=cfg)), cfg.rtl.version)

        for path in iglob(f"**/{top_module_name}.*v", root_dir=rtl_dir, recursive=True):
            path = os.path.join(rtl_dir, path)
            module_set, inst_set = parser_verilog_file(path)
            for _name in module_set:
                module_path_map[_name] = path
            module_set.clear()
            for _name in inst_set:
                get_rtl_dep(_name)

    get_rtl_dep(top_module)
    return list(module_path_map.values())


def build(cfg: CfgObject):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import error, info, get_root_dir, exe_cmd
    # check version
    if not match_version(cfg.rtl.version, ["openxiangshan-kmh-97e37a2237-24092701"]):
        error(f"frontend_bpu_tagesc: Unsupported RTL version {cfg.rtl.version}")
        return False
    # find source files for Tage_SC
    rtl_files = get_rtl_dependencies("Tage_SC", cfg=cfg)
    assert rtl_files, "Cannot find RTL files of Frontend.BPU.TageSC"

    internal_signals_path = os.path.join(get_root_dir("ut_frontend/bpu/tagesc/internal.yaml"))
    assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # export Tage_SC.sv
    if not os.path.exists(get_root_dir("dut/tage_sc")):
        info("Exporting Tage_SC.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(f"picker export {rtl_files[0]} --fs {filelist.name} --lang python --tdir "
                                f"{get_root_dir('dut/tage_sc')} -w Tage_SC.fst -c --internal={internal_signals_path}")
        assert s, err
    return True


def line_coverage_files(cfg: CfgObject):
    return ["Tage_SC.v"]
