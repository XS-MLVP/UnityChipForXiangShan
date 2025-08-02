---
title: Required Specifications
linkTitle: Required Specifications
#menu: {main: {weight: 99}}
weight: 97
---

In order to facilitate the integration of everyone's contributions, it is necessary to adopt the same "specifications" in coding, environment, and documentation.

### Environment Requirements

- **python:** When coding in Python, use the standard library as much as possible, and use general syntax compatible with most Python 3 versions (try to be compatible with Python 3.6 - Python 3.12). Do not use syntax that is too old or too new.
- **Operating System:** Ubuntu 22.04 is recommended. On Windows, it is recommended to use the WSL2 environment.
- **hugo:** Recommended version is 0.124.1 (older versions do not support symlinks)
- **Minimal dependencies:** Try to minimize the use of third-party C++/C libraries.
- **picker:** It is recommended to install the picker tool and xspcomm library via wheel.

### Test Cases

- **Code Style:** It is recommended to follow the [PEP 8 standard](https://peps.python.org/pep-0008/)
- **Build Scripts:** The naming of build scripts must follow the DUT naming structure, otherwise verification results cannot be collected correctly. For example, the build file for the `backend.ctrl_block.decode` UT in the scripts directory should be named `build_ut_backend_ctrl_block_decode.py` (with the fixed prefix `build_ut_`, and dots `.` replaced by underscores `_`). The script should implement the `build(cfg) -> bool` and `line_coverage_files(cfg) -> list[str]` methods. `build` is used to compile the DUT into a Python module, and `line_coverage_files` is used to return the files for code line coverage statistics.
- **Test Case Tags:** If a test case cannot be version-agnostic, it needs to be marked with `pytest.mark.toffee_tags` to indicate the supported versions.
- **Test Case Abstraction:** The input of the test case should not contain specific DUT pins or other strongly coupled content. Only functions encapsulated on top of the DUT can be called. For example, for an adder, the DUT's target function should be encapsulated as `dut_wrapper.add(a: int, b: int) -> int, bool`, and in the test_case, only `sum, c = add(a, b)` should be called for testing.
- **Coverage Abstraction:** When writing functional coverage, the input of the checkpoint function should also not include DUT pins.
- **Environment Abstraction:** For a verification, it is usually divided into two parts: Test Case and Env (everything except the test case is called Env, which includes DUT, drivers, monitors, etc.). The Env should provide abstract functional interfaces to the outside and should not expose too many details.
- **Test Documentation:** In the verification environment of each DUT, a `README.md` should be provided to explain the environment, such as the interfaces provided by Env to Case, directory structure, etc.

### PR Writing

- **Title:** Concise and clear, able to summarize the main content of the PR.
- **Detailed Description:** Clearly explain the purpose of the PR, the changes made, and relevant background information. If solving an existing issue, provide a link (e.g., Issue).
- **Related Issues:** Link related issues in the description, such as `Fixes #123`, so that the related issue is closed when the PR is merged.
- **Testing:** Testing is required, and the test results should be described.
- **Documentation:** Any documentation involved in the PR should be updated accordingly.
- **Decomposition:** If the PR involves many changes, consider splitting it into multiple PRs.
- **Checklist:** Check whether compilation passes, code style is reasonable, tests pass, necessary comments are present, etc.
- **Template:** Please refer to the provided PR template [reference link](08_pr_template/).

### ISSUE Writing

Same requirements as above.
