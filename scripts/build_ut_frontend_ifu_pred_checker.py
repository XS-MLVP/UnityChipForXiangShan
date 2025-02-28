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
        warning("frontend_ifu_pred_checker: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    module_name = "PredChecker"
    file_name = "PredChecker.sv"
    internal_signals_path="ut_frontend/ifu/pred_checker/pred_checker_internal.yaml"
    fpath = f"rtl/{file_name}"
    f = is_all_file_exist([fpath], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # build
    # export PreDecode.sv 
    if not os.path.exists(get_root_dir(f"dut/{module_name}")):
        info(f"Exporting {file_name}")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir(f"{fpath}", cfg=cfg)} \
                              --lang python --tdir {get_root_dir("dut")}/ -w {module_name}.fst -c --internal={internal_signals_path}')
        assert s, f"Failed to export {file_name}: %s\n%s" % (out, err)

    return True


def line_coverage_files(cfg):
    return ["PredChecker.v"]
