import os
from comm import warning, info

def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir, get_all_rtl_files
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_ftq_redirect_mem: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    module_name = "FtqPcMem"
    file_name ="FtqPcMemWrapper.sv"
    rtl_files = get_all_rtl_files("FtqPcMemWrapper", cfg=cfg)
    internal_signals_path=""

    # build
    # export SyncDataModuleTemplate__64entry.sv
    if not os.path.exists(get_root_dir(f"dut/{module_name}")):
        info(f"Exporting {file_name}.sv")
        s,out,err = exe_cmd(f'picker export {rtl_files[0]} --tname {module_name}\
                            --lang python --tdir {get_root_dir("dut")}/ -w {module_name}.fst -c --fs ' + ' '.join(rtl_files))
        assert s, f"Failed to export {file_name}.sv: %s\n%s" % (out, err)

    return True


def get_metadata():
    return {
        "dut_name": "frontend_ftq_pc_mem",
        "dut_dir": "FtqPcMem",
        "test_targets": [
            "ut_frontend/ftq/ftq_pc_mem",
            "ut_frontend/ftq",
            "ut_frontend"
        ]
    }


## set coverage
def line_coverage_files(cfg):
    return ["FtqPcMem.v"]
