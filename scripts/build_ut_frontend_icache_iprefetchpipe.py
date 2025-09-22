from comm.export_dut import picker_export

TARGET_NAME = "IPrefetchPipe"


def build(cfg):
    # additional internal signal files
    internal_signals_path = "scripts/icache_related/icache_iprefetchpipe_internals.yaml"

    # verilator arguments
    verilator_args = "--x-initial;0"

    return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path, vflags=verilator_args)


def line_coverage_files(cfg):
    return ["IPrefetchPipe.v"]
