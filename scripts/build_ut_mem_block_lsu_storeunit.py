from comm.export_dut import picker_export

TARGET_NAME = "StoreUnit"


def build(cfg):

    # export ICacheMainPipe.sv
    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["StoreUnit.v"]
