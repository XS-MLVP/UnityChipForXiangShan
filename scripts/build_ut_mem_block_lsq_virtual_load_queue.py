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
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir, extract_signals, get_all_rtl_files
    # check version
    if not match_version(cfg.rtl.version, []):
        warning("memblock_loadstorequeue_virtualloadqueue: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    f = is_all_file_exist(["rtl/VirtualLoadQueue.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # build
    # export VirtualLoadQueue
    if not os.path.exists(get_root_dir("dut/VirtualLoadQueue")):
        info("Exporting VirtualLoadQueue.sv")
        rtl_files = get_all_rtl_files("VirtualLoadQueue", cfg=cfg)
        internal_signals_path = os.path.join(get_root_dir("scripts/mem_block_load_queue_virtual//internal.yaml"))
        extract_signals(get_rtl_dir("rtl/VirtualLoadQueue.sv", cfg=cfg), internal_signals_path)
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/VirtualLoadQueue.sv", cfg=cfg)} --fs {filelist.name} --lang python --tdir {get_root_dir("dut")}/ -w Virtual.fst -c --internal={internal_signals_path}')
        assert s, "Failed to export VirtualLoadQueue.sv: %s\n%s" % (out, err)
    return True

def get_metadata():
    return {
        "dut_name": "mem_block_lsq_virtual_load_queue",
        "dut_dir": "VirtualLoadQueue",
        "test_targets": [
            "ut_mem_block/lsq/virtual_load_queue",
            "ut_mem_block/lsq/",
            "ut_mem_block/"
        ]
    }

def line_coverage_files(cfg):
    return ["VirtualLoadQueue.v"]