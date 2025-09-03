from comm.export_dut import picker_export

TARGET_NAME = "NewIFU"


def build(cfg):
    internal_signals_path = "scripts/ifu_related/ifu_top_internals.yaml"

    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["NewIFU.v"]
