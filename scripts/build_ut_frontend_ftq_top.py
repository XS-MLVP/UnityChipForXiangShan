import os
from comm import warning, info

def build(cfg):
    # import base modules
    from toffee_test.markers import match_version
    from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        warning("frontend_ftq_top: %s" % f"Unsupported RTL version {cfg.rtl.version}")
        return False
    # check files 1
    module_name = "FtqTop"
    file_name ="Ftq.sv"
    dp_file_names = [
    "SyncDataModuleTemplate__64entry.sv", 
    "SyncDataModuleTemplate__64entry_1.sv", 
    "SyncDataModuleTemplate__64entry_2.sv", 
    "SyncDataModuleTemplate__64entry_3.sv", 
    "DataModule__16entry.sv", 
    "DataModule__16entry_4.sv", 
    "DataModule__16entry_8.sv", 
    "DataModule__16entry_12.sv", 
    "FTBEntryGen.sv", 
    "FtqNRSRAM.sv", 
    "FtqPcMemWrapper.sv", 
    "SRAMTemplate_65.sv", 
    "SyncDataModuleTemplate_FtqPC_64entry.sv", 
    "DataModule_FtqPC_16entry.sv", 
    "array_0_0.sv", 
    "array_0_0_ext.v",
    "ClockGate.sv",
    "MbistClockGateCell.sv",
    "sram_array_2p64x576m192s1h0l1b_ftq.sv",
    "array_8.sv",
    "array_8_ext.v",
    "MbistPipeFtq.sv"
    ]
    dp_fpaths = [f"rtl/rtl/{dp_file_name}" for dp_file_name in dp_file_names]
    dp_fpaths_after_get_root = [get_root_dir(dp_fpath) for dp_fpath in dp_fpaths]
    fpath = f"rtl/{file_name}"
    all_fpaths = dp_fpaths + [fpath]
    ## internal signals is now not determined
    internal_signals_path=""
    f = is_all_file_exist(all_fpaths, get_rtl_dir(cfg=cfg))
    #assert f is True, f"File {f} not found"
    # build
    # export ftq.sv
    if not os.path.exists(get_root_dir(f"dut/{module_name}")):
        info("Exporting Ftq.sv")
        s,out,err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir(f"{fpath}",cfg = cfg)} \
                            --lang python --tdir {get_root_dir("dut")}/ -w {module_name}.fst -c --fs ' + ' '.join(dp_fpaths_after_get_root))
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
