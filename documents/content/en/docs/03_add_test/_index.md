---
title: Add Test
linkTitle: Add Test
#menu: {main: {weight: 20}}
weight: 15
---

To add a brand-new DUT test case, the following three steps need to be completed (this section uses the `rvc_expander` under the frontend `ifu` as an example):

1. **Add a compilation script**: Write a compilation file for the corresponding `rtl` in the `scripts` directory using `python` (e.g., `build_ut_frontend_ifu_rvc_expander.py`).
1. **Build the test environment**: Create the target test UT directory in the appropriate location (e.g., `ut_frontend/ifu/rvc_expander`). If necessary, add the basic tools required for the DUT test in modules such as `tools` or `comm`.
1. **Add test cases**: Add test cases in the UT directory following the [PyTest specification](https://docs.pytest.org/en/stable/).

If you are adding content to an existing DUT test, simply follow the original directory structure.

For information on how to perform Python chip verification using the picker and toffee libraries, refer to: [https://open-verify.cc/mlvp/docs](https://open-verify.cc/mlvp/docs)

When testing, you also need to pay attention to the following:

1. **UT Module Description**: Add a `README.md` file in the top-level folder of the added module to provide an explanation. For specific formats and requirements, refer to the [template](https://open-verify.cc/UnityChipForXiangShan/docs/10_template_ut_readme/).
1. **Code Coverage**: Code coverage is an important metric for chip verification. Generally, all code of the target DUT needs to be covered.
1. **Functional Coverage**: Functional coverage indicates how much of the target functionality has been verified. It usually needs to reach 100%.

In subsequent documentation, we will continue to use the `rvc_expander` module as an example to explain the above process in detail.

\*Note: Directory or file names should be reasonable so that their specific meaning can be inferred from the naming.
