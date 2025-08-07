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
from comm import warning, info, get_all_rtl_files


def build(cfg):
    # import base modules
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_l2tlb_ptw: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    f = is_all_file_exist(["rtl/PTW.v"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # find source files for PTW
    rtl_files = get_all_rtl_files("PTW", cfg=cfg)
    info(f"rtl_files: {rtl_files}")
    assert rtl_files, "Cannot find RTL files of PTW"

    # build
    # export PTW.v
    if not os.path.exists(get_root_dir("dut/PTW")):
        info("Exporting PTW.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir " 
                f"{get_root_dir('dut')}/ -w PTW.fst -c")
        assert s, err
    return True


def get_metadata():
    return {
        "dut_name": "frontend_l2tlb_ptw",
        "dut_dir": "PTW",
        "test_targets": [
            "ut_frontend/l2tlb/ptw",
            "ut_frontend/l2tlb",
            "ut_frontend"
        ]
    }


def line_coverage_files(cfg):
    return ["PTW.v"]
