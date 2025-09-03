from comm.export_dut import picker_export

TARGET_NAME = "Ftq"


def build(cfg):
    return picker_export(TARGET_NAME, cfg)


## set coverage
def line_coverage_files(cfg):
    return ["Ftq.v"]
