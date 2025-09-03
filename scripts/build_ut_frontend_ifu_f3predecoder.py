from comm.export_dut import picker_export

TARGET_NAME = "F3Predecoder"


def build(cfg):
    return picker_export(TARGET_NAME, cfg)


def line_coverage_files(cfg):
    return ["F3Predecoder.v"]
