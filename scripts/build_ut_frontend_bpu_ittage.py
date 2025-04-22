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


def build(cfg):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import error, info, get_root_dir, exe_cmd, get_all_rtl_files

    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        error(f"frontend_bpu_ittage: Unsupported RTL version {cfg.rtl.version}")
        return False

    # find source files for ITTage
    rtl_files = get_all_rtl_files("ITTage", cfg=cfg)
    assert rtl_files, "Cannot find RTL files of Frontend.BPU.ITTage"

    internal_signals_path = os.path.join(get_root_dir("ut_frontend/bpu/ittage/internal.yaml"))
    assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # export ITTage.sv
    if not os.path.exists(get_root_dir("dut/ITTage")):
        info("Exporting ITTage.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir "
                f"{get_root_dir('dut')}/ -w ITTage.fst -c --internal={internal_signals_path}")
        assert s, err
    return True


def get_metadata():
    return {
        "dut_name": "frontend_bpu_ittage",
        "dut_dir": "ITTage",
        "test_targets": [
            "ut_frontend/bpu/ittage",
            "ut_frontend/bpu",
            "ut_frontend"
        ]
    }


def line_coverage_files(cfg):
    return ["ITTage.v"]
