from comm.export_dut import picker_export

TARGET_NAME = "IPrefetchPipe"


def _extract_signals_with_ports(verilog_file: str, output_file: str) -> None:
    """Export both internal declarations and IO ports for mem-direct access."""
    import os
    import re

    decl = re.compile(
        r"^\s*(?:(input|output|inout)\s+)?(?:(wire|reg|logic)\s+)?(\[[^\]]+\]\s+)?"
        r"([A-Za-z_][\w$]*(?:\s*,\s*[A-Za-z_][\w$]*)*)\s*(?:[,;]|=)"
    )

    seen = set()
    extracted = []

    with open(verilog_file, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("//"):
                continue
            m = decl.match(raw)
            if not m:
                continue
            direction, sig_type, width, names = m.groups()
            # Skip non-declaration statements accidentally matched.
            if direction is None and sig_type is None:
                continue
            signal_type = sig_type or "wire"
            if signal_type == "reg":
                signal_type = "logic"
            width = (width or "").strip()
            for name in [x.strip() for x in names.split(",")]:
                if name.startswith("_GEN") or name in seen:
                    continue
                seen.add(name)
                if width:
                    extracted.append(f'  - "{signal_type} {width} {name}"')
                else:
                    extracted.append(f'  - "{signal_type} {name}"')

    module_name = os.path.splitext(os.path.basename(verilog_file))[0]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{module_name}:\n")
        f.write("\n".join(extracted))
        f.write("\n")


def build(cfg):
    # Use mem-direct mode and export a complete internal list so
    # GetInternalSignal(use_vpi=False) can be used safely in tests.
    import os
    from tempfile import NamedTemporaryFile
    from comm import get_rtl_dir

    # verilator arguments
    verilator_args = "--x-initial;0"

    with NamedTemporaryFile("w+", prefix=TARGET_NAME, suffix=".yaml") as internal:
        internal_signals_path = internal.name
        rtl_file = get_rtl_dir(f"{TARGET_NAME}.sv", cfg=cfg)
        if not os.path.exists(rtl_file):
            rtl_file = get_rtl_dir(f"{TARGET_NAME}.v", cfg=cfg)
        _extract_signals_with_ports(rtl_file, internal_signals_path)
        return picker_export(
            TARGET_NAME,
            cfg,
            access_mode=1,
            internal_file=internal_signals_path,
            vflags=verilator_args,
        )


def line_coverage_files(cfg):
    return ["IPrefetchPipe.v"]
