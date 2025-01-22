import os
from comm import warning, info
from .build_ut_frontend_bpu_tagesc import get_rtl_dependencies

def build(cfg):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import error, info, get_root_dir, exe_cmd
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        error(f"frontend_bpu_tagesc: Unsupported RTL version {cfg.rtl.version}")
        return False
    # find source files for Tage_SC
    rtl_files = get_rtl_dependencies("NewIFU", cfg=cfg)
    info(f"rtl_files: {rtl_files}")
    assert rtl_files, "Cannot find RTL files of Frontend.IFU"

    internal_signals_path = os.path.join(get_root_dir("scripts/ifu_related/ifu_top_internals.yaml"))
    # assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # export Tage_SC.sv
    if not os.path.exists(get_root_dir("dut/IFU")):
        info("Exporting IFU.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir " 
                f"{get_root_dir('dut')}/ -w Tage_SC.fst -c --internal={internal_signals_path}")
        assert s, err
    return True


def line_coverage_files(cfg):
    return ["NewIFU.v"]