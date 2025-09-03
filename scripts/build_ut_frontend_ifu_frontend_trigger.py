from comm.export_dut import picker_export

TARGET_NAME = "FrontendTrigger"


def build(cfg):
    internal_signals_path = "ut_frontend/ifu/frontend_trigger/frontend_trigger_internal.yaml"
    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["FrontendTrigger.v"]
