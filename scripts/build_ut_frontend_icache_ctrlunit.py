from comm.export_dut import picker_export

TARGET_NAME = "ICacheCtrlUnit"


def build(cfg):
    # additional internal signal files
    internal_signals_path = "scripts/icache_related/icache_ctrlunit_internals.yaml"
    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["ICacheCtrlUnit.v"]
