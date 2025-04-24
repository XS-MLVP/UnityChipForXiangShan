import os
from comm import warning, info


def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("ifu frontend rvc expander: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    f = is_all_file_exist(["rtl/RVCExpander.sv"], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # build
    # export RVCExpander.sv
    if not os.path.exists(get_root_dir("dut/RVCExpander")):
        info("Exporting RVCExpander.sv")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/RVCExpander.sv", cfg=cfg)} --lang python --tdir {get_root_dir("dut")}/ -w rvc.fst -c')
        assert s, "Failed to export RVCExpander.sv: %s\n%s" % (out, err)
    # build disasm
    if not os.path.exists(get_root_dir("tools/disasm/build")):
        info("Building disasm")
        s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
        assert s, "Failed to build disasm"
    return True


def get_metadata():
    return {
        "dut_name": "frontend_ifu_rvc_expander",
        "dut_dir": "RVCExpander",
        "test_targets": [
            "ut_frontend/ifu/rvc_expander/classical_version",
            "ut_frontend/ifu/rvc_expander/toffee_version",
            "ut_frontend/ifu/rvc_expander",
            "ut_frontend/ifu",
            "ut_frontend"
        ]
    }


def line_coverage_files(cfg):
    return ["RVCExpander.v"]