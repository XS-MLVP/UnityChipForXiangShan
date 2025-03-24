import os
from comm import warning, info, get_all_rtl_files


def build(cfg):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import error, info, get_root_dir, exe_cmd

    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        error(f"frontend_icache_missunit: Unsupported RTL version {cfg.rtl.version}")
        return False
    
    # find source files for ICacheMissUnit
    rtl_files = get_all_rtl_files("ICacheMissUnit", cfg=cfg)
    info(f"rtl_files: {rtl_files}")
    assert rtl_files, "Cannot find RTL files of Frontend.ICacheMissUnit"

    # additional internal signal files
    # internal_signals_path = os.path.join(get_root_dir("scripts/icache_related/MissUnit_internals.yaml"))
    # assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # export ICacheMissUnit.sv
    if not os.path.exists(get_root_dir("dut/ICacheMissUnit")):
        info("Exporting ICacheMissUnit.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir "
                #           f"{get_root_dir('dut')}/ -w ICacheMissUnit.fst -c --internal={internal_signals_path}")
                f"{get_root_dir('dut')}/ -w ICacheMissUnit.fst -c "
            )
        assert s, err
    return True


def line_coverage_files(cfg):
    return ["ICacheMissUnit.v"]
