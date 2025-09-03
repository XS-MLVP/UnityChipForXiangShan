import os

from comm import info
from comm.export_dut import picker_export

TARGET_NAME = "RVCExpander"


def build(cfg):
    # import base modules
    from comm import exe_cmd, get_root_dir

    # build disasm
    if not os.path.exists(get_root_dir("tools/disasm/build")):
        info("Building disasm")
        s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
        assert s, "Failed to build disasm"
    return picker_export(TARGET_NAME, cfg)


def line_coverage_files(cfg):
    return ["RVCExpander.v"]
