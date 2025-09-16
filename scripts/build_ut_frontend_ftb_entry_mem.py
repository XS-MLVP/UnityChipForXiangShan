from comm.export_dut import picker_export

TARGET_NAME = "FtbEntryMem"


def build(cfg):
    return picker_export("SyncDataModuleTemplate__64entry_1", cfg, target_name=TARGET_NAME)


## set coverage
def line_coverage_files(cfg):
    return ["FtbEntryMem.v"]
