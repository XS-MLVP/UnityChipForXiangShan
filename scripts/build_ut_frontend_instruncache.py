from comm.export_dut import picker_export

TARGET_NAME = "InstrUncache"


def build(cfg):
    # additional internal signal files
    internal_signals_path = "scripts/instruncache_related/instruncache_internals.yaml"

    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["InstrUncache.v"]
