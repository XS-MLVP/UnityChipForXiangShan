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
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir, extract_signals, get_rtl_dependencies
    # check version
    if not match_version(cfg.rtl.version, []):
        warning("memblock_loadstorequeue_rar: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    f = is_all_file_exist(["rtl/LoadQueueRAR.sv", "rtl/LqPAddrModule.sv", "rtl/FreeList_3.sv", "rtl/DelayNWithValid_3.sv", "rtl/DelayN_220.sv", "rtl/DelayNWithValid_6.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # build
    # export LoadQueueRAR
    if not os.path.exists(get_root_dir("dut/LoadQueueRAR")):
        info("Exporting LoadQueueRAR.sv")
        internal_signals_path = os.path.join(get_root_dir("scripts/mem_block/load_queue_rar/internal.yaml"))
        extract_signals(get_rtl_dir("rtl/LoadQueueRAR.sv", cfg=cfg), internal_signals_path)
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/LoadQueueRAR.sv", cfg=cfg)} --fs {get_root_dir("scripts/mem_block_load_queue_rar/rtl_files.f")} --lang python --tdir {get_root_dir("dut")}/ -w RAR.fst --internal={internal_signals_path} -c')
        assert s, "Failed to export LoadQueueRAR.sv: %s\n%s" % (out, err)
    return True

def line_coverage_files(cfg):
    return ["LoadQueueRAR.v"]