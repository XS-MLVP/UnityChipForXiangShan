from comm.export_dut import picker_export

TARGET_NAME = "FtqPcMem"


def build(cfg):
    return picker_export("FtqPcMemWrapper", cfg, target_name=TARGET_NAME)


## set coverage
def line_coverage_files(cfg):
    return ["FtqPcMem.v"]
