from comm.export_dut import picker_export

TARGET_NAME = "FtqTop"


def build(cfg):
    return picker_export(
        source_name="Ftq",        
        target_name=TARGET_NAME,
        access_mode=1,
        cfg=cfg,
    )


## set coverage
def line_coverage_files(cfg):
    return ["Ftq.v"]
