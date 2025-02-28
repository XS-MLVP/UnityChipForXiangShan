import os
from comm import warning, info


def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_ifu_f3predecoder: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files
    module_name = "F3Predecoder"
    file_name = "F3Predecoder.sv"
    internal_signals_path=""
    fpath = f"rtl/{file_name}"
    f = is_all_file_exist([fpath], get_rtl_dir(cfg=cfg))
    assert f is True, f"File {f} not found"
    # build
    # export F3Predecoder.sv 
    if not os.path.exists(get_root_dir(f"dut/{module_name}")):
        info(f"Exporting {file_name}")
        s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir(f"{fpath}", cfg=cfg)} \
                              --lang python --tdir {get_root_dir("dut")}/ -w {module_name}.fst -c ')
        assert s, f"Failed to export {file_name}: %s\n%s" % (out, err)

    return True


def line_coverage_files(cfg):
    return ["F3Predecoder.v"]
