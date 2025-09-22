from comm.export_dut import picker_export

TARGET_NAME = "PreDecode"


def build(cfg):
    internal_signals_path = "ut_frontend/ifu/predecode/predecode_internal.yaml"
    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["PreDecode.v"]
