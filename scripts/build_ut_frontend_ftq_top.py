import os
from comm import warning, info

def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir, get_all_rtl_files
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_ftq_top: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files 1
    module_name = "FtqTop"
    file_name ="Ftq.sv"
    rtl_files = get_all_rtl_files("Ftq", cfg=cfg)
    internal_signals_path=""

    # build
    # export ftq.sv
    if not os.path.exists(get_root_dir(f"dut/{module_name}")):
        info("Exporting Ftq.sv")
        s,out,err = exe_cmd(f'picker export --cp_lib false {rtl_files[0]} --tname {module_name}\
                            --lang python --tdir {get_root_dir("dut")}/ -w {module_name}.fst -c --fs ' + ' '.join(rtl_files))
        assert s, f"Failed to export Ftq.sv: %s\n%s" % (out, err)

    return True


def get_metadata():
    return {
        "dut_name": "frontend_ftq_top",
        "dut_dir": "FtqTop",
        "test_targets": [
            "ut_frontend/ftq/ftq_top",
            "ut_frontend/ftq",
            "ut_frontend"
        ]
    }


## set coverage
def line_coverage_files(cfg):
    return ["Ftq.v"]
