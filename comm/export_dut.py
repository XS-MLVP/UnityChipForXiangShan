import os
import shutil
import subprocess
from tempfile import NamedTemporaryFile

from toffee_test.markers import match_version

from comm import get_root_dir, error, get_all_rtl_files, info, UnityChipConfig


def picker_export(
        source_name: str,
        cfg: UnityChipConfig,
        target_name: str = "",
        simulator: str = "verilator",
        access_mode: int = 0,
        internal_file: str = "",
        vflags="",
        cflags="",
        rtl_version: str | list[str] = "openxiangshan-kmh-*",
) -> bool:
    """Export RTL module to Python DUT using picker tool.

     This function exports a specified RTL module to a Python Design Under Test (DUT)
     class using the picker export tool. It handles dependency resolution, simulator
     configuration, and various export options including waveform generation and
     code coverage.

     Args:
         source_name: Name of the top-level RTL module to export. Cannot be empty.
         cfg: Configuration object.
         target_name: Name for the exported DUT class. Defaults to source_name if empty.
         simulator: Simulator to use for the export. Options include "verilator", "vcs".
             Defaults to "verilator".
         access_mode: Memory access mode. 0 for VPI mode, 1 for Mem-Direct mode.
             Mem-Direct mode only supports verilator. Defaults to 0.
         internal_file: Path to a YAML file containing internal signals to export to DUT class.
             Optional.
         vflags: Additional flags to pass to the simulator.
         cflags: Additional C++ compilation flags to pass to the compiler.
         rtl_version: Required RTL version pattern(s). Can be a string or list of strings.
             Defaults to "openxiangshan-kmh-*".

     Returns:
         bool: True if export was successful, False otherwise.

     Raises:
         AssertionError: If source_name is empty, if no RTL files are found for the module,
             or if Mem-Direct mode is used with a simulator other than verilator.

     Note:
         - Waveform format is automatically selected based on simulator: fst for verilator,
           fsdb for vcs, vcd for others
         - The exported DUT is placed in the {root}/dut directory
         - RTL version compatibility is checked before export
     """
    assert source_name, "Cannot export DUT without module name"

    # Get all dependencies
    dependencies = get_all_rtl_files(source_name, cfg)
    assert dependencies, f"Cannot found any rtl for {source_name}"

    if not match_version(cfg.rtl.version, rtl_version):
        error(f"(Export {source_name}): Unsupported RTL version {cfg.rtl.version}")
        return False

    # Mem-Direct mode only supports verilator
    if access_mode == 1:
        assert simulator == "verilator", "Mem-Direct mode only supports verilator as simulator"

    # If target name is set
    if not target_name:
        target_name = source_name

    # Picker export command
    cmd = [
        shutil.which('picker'),  # Picker export subcommand
        "export",
        dependencies[0],  # Path of the top module
        "--autobuild", "1",
        "--lang", "python",  # Export language is python
        "--cp_lib", "0",  # Disable copy xspcomm library
        "--sim", simulator,  # Set simulator
        "--rw", str(access_mode),  # Set access-mode
        "--sname", source_name,  # Top module name to export
        "--tdir", get_root_dir("dut") + "/",  # Export to %{root}/dut dir
        "--tname", target_name,
    ]

    # Waveform format
    wave_format = ""
    if simulator == "verilator":
        wave_format = "fst"
    elif simulator == "vcs":
        wave_format = "fsdb"
    else:
        wave_format = "vcd"

    # Enable waveform
    if not cfg.no_waveform:
        cmd.extend(["-w", ".".join((target_name, wave_format))])
    # Enable code coverage
    if cfg.no_code_cov is not None and cfg.no_code_cov == False:
        cmd.append("-c")
    # Export internal signals to DUT class
    if internal_file:
        internal_path = os.path.join(get_root_dir(internal_file))
        assert os.path.exists(internal_path), "Internal file not found"
        cmd.extend(["--internal", internal_path])
    # Add Flags
    if vflags:
        cmd.extend(["-V", vflags])
    if cflags:
        cmd.extend(["-C", cflags])

    with NamedTemporaryFile(mode="w+", encoding="utf-8", suffix=".txt") as filelist:
        info("Exporting %s", source_name)
        cmd.extend(["--fs", filelist.name])
        filelist.write("\n".join(dependencies))
        filelist.flush()
        # Execute picker export to generate DUT
        ret = subprocess.run(cmd, shell=False, stderr=subprocess.PIPE)
        if ret.returncode:
            error(f"Failed to export:\n {ret.stderr}")
        return ret.returncode == 0
