from comm.export_dut import picker_export

TARGET_NAME = "StoreUnit"


def build(cfg):

    # export StoreUnit.sv
    return picker_export(TARGET_NAME, cfg)


def line_coverage_files(cfg):
    return ["StoreUnit.v"]
