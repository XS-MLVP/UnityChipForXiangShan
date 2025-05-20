---
title: Prepare Verification Environment
linkTitle: Prepare Verification Environment
#menu: {main: {weight: 20}}
weight: 13
---

#### Basic Environment Requirements

This project uses the `Python` programming language for UT verification, with [picker](https://github.com/XS-MLVP/picker) and [toffee](https://github.com/XS-MLVP/toffee) as the main tools and test frameworks. **Environment requirements** are as follows:

1. Linux operating system. It is recommended to install Ubuntu 22.04 under WSL2.
1. Python. Python 3.11 is recommended.
1. picker. Install the latest version as instructed in the [Quick Start](https://open-verify.cc/mlvp/docs/quick-start/installer/).
1. toffee. It will be installed automatically later. You can also manually install the latest version as instructed in the [Quick Start](https://open-verify.cc/mlvp/docs/mlvp/quick-start/).
1. lcov. Used for report generation in the test stage. Install via package manager: `sudo apt install lcov`

**After environment setup**, clone the repository:
```bash
git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
cd UnityChipForXiangShan
pip3 install -r requirements.txt # Install python dependencies (e.g., toffee)
```

#### Download RTL Code

By default, download from the repository [https://github.com/XS-MLVP/UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs). Users can also generate RTL by compiling according to the XiangShan documentation.

```bash
make rtl    # This command downloads the latest rtl code, unpacks it to the rtl directory, and creates a symlink
```

You can specify the rtl version to download with the following command:

```bash
make rtl args="rtl.version='openxiangshan-kmh-fad7803d-24120901'"
```

All RTL download packages can be found at [UnityChipXiangShanRTLs](https://github.com/XS-MLVP/UnityChipXiangShanRTLs).

The naming convention for RTL archives is: `name-microarchitecture-GitTag-date.tar.gz`, for example, `openxiangshan-kmh-97e37a2237-24092701.tar.gz`. When used, the repository code will filter out the git tag and suffix, so the version accessed via cfg.rtl.version is: `openxiangshan-kmh-24092701`. The directory structure inside the archive is:

```bash
openxiangshan-kmh-97e37a2237-24092701.tar.gz
└── rtl           # directory
    |-- *.sv      # all sv files
    `-- *.v       # all v files
```

#### Compile DUT

The purpose of this process is to package the RTL into a Python module using the picker tool. You can specify the DUT to be packaged via the make command, or package all DUTs at once.

If you want to package a specific dut yourself, you need to create a script named build_ut_<name>.py in the scripts directory. This script must implement a build method, which will be called automatically during packaging. There is also a line_coverage_files method for specifying files used for line coverage reference.

Picker's packaging supports adding internal signals; See the --internal parameter of picker and pass a custom yaml.

```bash
# Calls the build method in scripts/build_ut_<name>.py to create the Python DUT to be verified
make dut DUTS=<name>  # If there are multiple DUTS, separate them with commas. Wildcards are supported. The default value is "*", which compiles all DUTs.
# Example:
make dut DUTS=backend_ctrl_block_decode
```

For example, after running `make dut DUTS=backend_ctrl_block_decode`, the corresponding Python package will be generated in the dut directory:

```
dut/
├── __init__.py
├── DecodeStage
├── Predecode
└── RVCExpander
```

After conversion, you can import the corresponding DUT in your test case code, for example:
```python
from dut.PreDecode import DUTPreDecode
dut = DUTPreDecode()
```

#### Edit Configuration

When running rtl, dut, test, and other commands, the default configuration is used from configs/_default.yaml.

Of course, you can also use a custom configuration as follows:

```bash
# Specify a custom CFG file
make CFG=path/to/your_cfg.yaml
```

Similarly, you can specify key-value pairs directly on the command line. Currently, only the test-related stage supports command-line configuration key-value pairs:
```bash
# Specify KV, pass command-line arguments, separate key-value pairs with spaces
make test KV="log.term-level='debug' test.skip-tags=['RARELY_USED']"
```