import os
from comm import warning, info

def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_ftq_pd_mem: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    module_name = "FtqPdMem"
    file_name ="SyncDataModuleTemplate__64entry_2.sv"
    dp_file_names = [
    "DataModule__16entry_8.sv", 
    ]
    dp_fpaths = [f"rtl/rtl/{dp_file_name}" for dp_file_name in dp_file_names]
    dp_fpaths_after_get_root = [get_root_dir(dp_fpath) for dp_fpath in dp_fpaths]
    fpath = f"rtl/{file_name}"
    all_fpaths = dp_fpaths + [fpath]
    ## internal signals is now not determined
    internal_signals_path=""
    f = is_all_file_exist(all_fpaths, get_rtl_dir(cfg=cfg))
    #assert f is True, f"File {f} not found"    ##some problem here
    # build
    # export SyncDataModuleTemplate__64_1entry.sv
    if not os.path.exists(get_root_dir(f"dut/{module_name}")):
        info(f"Exporting {file_name}.sv")
        s,out,err = exe_cmd(f'picker export {get_rtl_dir(f"{fpath}",cfg = cfg)} --tname {module_name}\
                            --lang python --tdir {get_root_dir("dut")}/ -w {module_name}.fst -c --fs ' + ' '.join(dp_fpaths_after_get_root))
        assert s, f"Failed to export {file_name}.sv: %s\n%s" % (out, err)

    return True

## set coverage
def line_coverage_files(cfg):
    return ["FtqPdMem.v"]
