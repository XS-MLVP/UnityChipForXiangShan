---
title: Others
linkTitle: Others
#menu: {main: {weight: 99}}
weight: 96
---

## Test Case Management

If test cases are closely related to the target RTL version, changes in RTL may render previous test cases unsuitable. In addition, different scenarios have different requirements, such as not running time-consuming cases when verifying the test environment. Therefore, test cases need to be managed so that users can skip certain cases in specific scenarios. To achieve this, we use `pytest.mark.toffee_tags` to tag and version each test case. Then, in the configuration file, you can set which tags to skip or which tags to run.

```python
@pytest.mark.toffee_tags("my_tag", "version1 < version13")
def test_case_1():
    ...
```

For example, the above `test_case_1` is tagged with `my_tag` and supports versions from `version1` to `version13`. Therefore, you can specify `test.skip-tags=["my_tag"]` in the configuration file to skip this case during execution.

The parameters for `pytest.mark.toffee_tags` are as follows:

```python
@pytest.mark.toffee_tags(
    tag: Optional[list, str]     = []    # Case tag
    version: Optional[list, str] = [],   # RTL version requirement for the case
    skip: callable               = None, # Custom skip logic, skip(tag, version, item): (skip, reason)
)
```

The `tag` parameter of `toffee_tags` supports both `str` and `list[str]` types. The `version` parameter can also be `str` or `list[str]`. If it is a list, it matches exactly; if it is a string, the matching rules are as follows:

1. `name-number1 < name-number2:` means the version must be between `number1` and `number2` (inclusive, `number` can be a decimal, e.g., `1.11`)
2. `name-number1+`: means version `number1` and later
3. `name-number1-`: means version `number1` and earlier

If none of the above, and there is a `*` or `?`, it is treated as a wildcard. Other cases are exact matches.

Predefined tags can be found in `comm/constants.py`, for example:

```python
# Predefined tags for test cases
TAG_LONG_TIME_RUN = "LONG_TIME_RUN"  # Long-running
TAG_SMOKE         = "SMOKE"          # Smoke test
TAG_RARELY_USED   = "RARELY_USED"    # Rarely used
TAG_REGRESSION    = "REGRESSION"     # Regression test
TAG_PERFORMANCE   = "PERFORMANCE"    # Performance test
TAG_STABILITY     = "STABILITY"      # Stability test
TAG_SECURITY      = "SECURITY"       # Security test
TAG_COMPATIBILITY = "COMPATIBILITY"  # Compatibility test
TAG_OTHER         = "OTHER"          # Other
TAG_CI            = "CI"             # Continuous integration test
TAG_DEBUG         = "DEBUG"          # Debug test
TAG_DEMO          = "DEMO"           # Demo
```

In the default configuration (`config/_default.yaml`), tests marked with `LONG_TIME_RUN`, `REGRESSION`, `RARELY_USED`, and `CI` are filtered out.

You can use `@pytest.mark.toffee_tags` to add tags to each case, or define the following variables in a module to add tags to all test cases in the module:

```python
toffee_tags_default_tag     = []   # Corresponds to the tag parameter
toffee_tags_default_version = []   # Corresponds to the version parameter
toffee_tags_default_skip    = None # Corresponds to the skip parameter
```

*Note: The version number in this environment will automatically filter out git tags. For example, if the downloaded RTL is named `openxiangshan-kmh-97e37a2237-24092701.tar.gz`, its version number in this project is `openxiangshan-kmh-24092701`, which can be obtained via `cfg.rtl.version` or `comm.get_config().rtl.version`.

## Version Checking

In addition to using the `toffee_tags` tag for automatic version checking, you can also actively check versions via `get_version_checker`. A unit test usually consists of a test environment (Test Env) and test cases (Test Case). The Env encapsulates RTL pins and functions, then provides a stable API to the Case, so version checking is needed in the Env to determine whether to skip all test cases using this environment. For example, in Env:

```python
...
from comm import get_version_checker

version_check = get_version_checker("openxiangshan-kmh-*") # Get RTL version checker, same as the version parameter in toffee_tags

@pytest.fixture()
def my_fixture(request):
    version_check()                                        # Actively check in the fixture
    ....
    yield dut
    ...
```

In the above example, the Env actively performs version checking in the fixture named `my_fixture`. Therefore, every time the test case calls it, version checking is performed, and if the check fails, the case will be skipped.

## Repository Directory Structure

```bash
UnityChipForXiangShan
├── LICENSE            # Open source license
├── Makefile           # Main Makefile
├── README.en.md       # English readme
├── README.zh.md       # Chinese readme
├── __init__.py        # Python module file, allows importing UnityChipForXiangShan as a module
├── pytest.ini         # PyTest configuration file
├── comm               # Common components: logs, functions, configs, etc.
├── configs            # Configuration files directory
├── documents          # Documentation
├── dut                # DUT generation directory
├── out                # Output directory for logs, reports, etc.
├── requirements.txt   # Python dependencies
├── rtl                # RTL cache
├── run.py             # Main Python entry file
├── scripts            # DUT compilation scripts
├── tools              # Common tool modules
├── ut_backend         # Backend test cases
├── ut_frontend        # Frontend test cases
├── ut_mem_block       # Memory access test cases
└── ut_misc            # Other test cases
```

## Configuration File Description

Default configuration and explanation:

```yaml
# Default configuration file
# Configuration loading order: _default.yaml -> user-specified *.yaml -> command line parameters eg: log.term-level='debug'
# RTL configuration
rtl:
  # RTL download address, all *.gz.tar files from this address are treated as target RTL
  base-url: https://<your_rtl_download_address>
  # RTL version to download, e.g., openxiangshan-kmh-97e37a2237-24092701
  version: latest
  # Directory to store RTL, relative to the current config file path
  cache-dir: "../rtl"
# Test case configuration (tag and case support wildcards)
test:
  # Skip tags, all test cases with these tags will be skipped
  skip-tags: ["LONG_TIME_RUN", "RARELY_USED", "REGRESSION", "CI"]
  # Target tags, only test cases with these tags will be executed (skip-tags overrides run-tags)
  run-tags: []
  # Skipped test cases, all test cases (or module names) with these names will be skipped.
  skip-cases: []
  # Target test cases, only test cases (or module names) with these names will be executed (skip-cases overrides run-cases).
  run-cases: []
  # Skip exceptions, all test cases that throw these exceptions will be skipped
  skip-exceptions: []
# Output configuration
output:
  # Output directory, relative to the current config file path
  out-dir: "../out"
# Test report configuration
report:
  # Report generation directory, relative to output.out-dir
  report-dir: "report"
  # Report name, supports variable substitution: %{host} hostname, %{pid} process ID, %{time} current time
  report-name: "%{host}-%{pid}-%{time}/index.html"
  # Report content
  information:
    # Report title
    title: "XiangShan KMH Test Report"
    # Report user information
    user:
      name: "User"
      email: "User@example.email.com"
    # Target line coverage, e.g., 90 means 90%
    line_grate: 99
    # Other information to display, key is the title, value is the content
    meta:
      Version: "1.0"
# Log configuration
log:
  # Root output level
  root-level: "debug"
  # Terminal output level
  term-level: "info"
  # File log output directory
  file-dir: "log"
  # File log name, supports variable substitution: %{host} hostname, %{pid} process ID, %{time} current time
  file-name: "%{host}-%{pid}-%{time}.log"
  # File log output level
  file-level: "info"
# Test result configuration (this data is used to populate statistics charts in documents, original data comes from toffee-test generated reports)
#  After running the tests, you can view the results via `make doc`
doc-result:
  # Whether to enable test result post-processing
  disable: False
  # Organizational structure configuration of target DUT
  dutree: "%{root}/configs/dutree/xiangshan-kmh.yaml"
  # Result name, will be saved to the output report directory
  result-name: "ut_data_progress.json"
  # Symlink to the created test report for hugo
  report-link: "%{root}/documents/static/data/reports"
```

You can add custom parameters in the above configuration file, get global config info via `cfg = comm.get_config()`, and then access via `cfg.your_key`. The `cfg` info is read-only and cannot be modified by default.