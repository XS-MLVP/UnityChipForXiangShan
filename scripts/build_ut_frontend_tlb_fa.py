#coding=utf8
#***************************************************************************************
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
#**************************************************************************************/


import os
from comm import warning, info


def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_itlb: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    f = is_all_file_exist(["rtl/TLBFA.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # build
    # export TLBFA.sv
    if not os.path.exists(get_root_dir("dut/TLBFA")):
        info("Exporting TLBFA.sv")
        s, _, _ = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/TLBFA.sv", cfg=cfg)} --fs {get_root_dir("scripts/frontend_itlb/tlb_fa_rtl_files.f")} --lang python --tdir {get_root_dir("dut")}/ -w tlbfa.fst -c')
        assert s, "Failed to export TLBFA.sv"
    # build disasm
    if not os.path.exists(get_root_dir("tools/disasm/build")):
        info("Building disasm")
        s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
        assert s, "Failed to build disasm"
    return True


def line_coverage_files(cfg):
    return ["TLBFA.v"]
