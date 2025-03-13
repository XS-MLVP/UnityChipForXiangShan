import os
from comm import warning, info, get_all_rtl_files

def build(cfg):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import error, info, get_root_dir, exe_cmd
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        error(f"frontend_ifu_frontendTrigger: Unsupported RTL version {cfg.rtl.version}")
        return False
    # find source files for FrontendTrigger
    rtl_files = get_all_rtl_files("NewIFU", cfg=cfg)
    info(f"rtl_files: {rtl_files}")
    assert rtl_files, "Cannot find RTL files of Frontend.IFU"

    internal_signals_path = os.path.join(get_root_dir("scripts/ifu_related/ifu_top_internals.yaml"))
    # assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # export FrontendTrigger.sv
    if not os.path.exists(get_root_dir("dut/NewIFU")):
        info("Exporting IFU.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir " 
                f"{get_root_dir('dut')}/ -w FrontendTrigger.fst -c --internal={internal_signals_path}")
        assert s, err
    return True


def line_coverage_files(cfg):
    return ["NewIFU.v"]