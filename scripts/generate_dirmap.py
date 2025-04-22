import os
import re
import importlib.util
import sys


def generate_dirmap(scripts_dir=".", output_file="../.dirmap.autogen"):
    script_root = os.path.abspath(os.path.dirname(__file__))
    scripts_dir = os.path.join(script_root, scripts_dir)
    output_path = os.path.abspath(os.path.join(script_root, output_file))

    script_files = [
        f for f in os.listdir(scripts_dir)
        if f.startswith("build_ut_") and f.endswith(".py")
    ]

    with open(output_path, "w") as f_out:
        for script_file in script_files:
            dut_name = re.search(r"build_ut_(.*)\.py", script_file).group(1)
            script_path = os.path.join(scripts_dir, script_file)
            module_name = f"build_ut_{dut_name}"
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            if not hasattr(module, "get_metadata"):
                print(f"WARNING: {script_file} has no get_metadata() function, skipping")
                continue
            try:
                metadata = module.get_metadata()
                dut_dir = metadata.get("dut_dir")
                test_targets = metadata.get("test_targets", [])
            except Exception as e:
                print(f"ERROR: Failed to get metadata from {script_file}: {str(e)}")
                continue
            if not dut_dir or not test_targets:
                print(f"WARNING: {script_file} has invalid metadata (missing dut_dir or test_targets)")
                continue
            for target in test_targets:
                f_out.write(f"{dut_name} --> {dut_dir} --> {target}\n")


if __name__ == "__main__":
    generate_dirmap()