import os
from comm import warning, info, get_all_rtl_files


def build(cfg):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import  get_root_dir, exe_cmd

    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning(f"frontend_icache_iprefetchpipe: Unsupported RTL version {cfg.rtl.version}")
        return False
    
    # find source files for IPrefetchPipe
    rtl_files = get_all_rtl_files("IPrefetchPipe", cfg=cfg)
    info(f"rtl_files: {rtl_files}")
    assert rtl_files, "Cannot find RTL files of Frontend.IPrefetchPipe"

    # additional internal signal files
    internal_signals_path = os.path.join(get_root_dir("scripts/icache_related/icache_iprefetchpipe_internals.yaml"))
    # assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # verilator arguments
    verilator_args = "'--x-initial;0'"

    # export IPrefetchPipe.sv
    if not os.path.exists(get_root_dir("dut/IPrefetchPipe")):
        info("Exporting IPrefetchPipe.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir "
                f"{get_root_dir('dut')}/ -w IPrefetchPipe.fst -c --internal={internal_signals_path} --vpi --rw 1"
            #    f"-V {verilator_args}"
            )
        assert s, err
    return True


def get_metadata():
    return {
        "dut_name": "frontend_icache_iprefetchpipe",
        "dut_dir": "IPrefetchPipe",
        "test_targets": [
            "ut_frontend/icache/iprefetchpipe",
            "ut_frontend/icache",
            "ut_frontend"
        ]
    }


def line_coverage_files(cfg):
    return ["IPrefetchPipe.v"]
