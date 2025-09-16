from comm.export_dut import picker_export

TARGET_NAME = "FtqMetairSram"


def build(cfg):
    return picker_export("FtqNRSRAM", cfg, target_name=TARGET_NAME)


## set coverage
def line_coverage_files(cfg):
    return ["FtqMetairSram.v"]
