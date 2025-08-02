---
title: Functional Coverage
linkTitle: Functional Coverage
#menu: {main: {weight: 20}}
weight: 6
---

Functional Coverage is a **user-defined** metric used to measure the proportion of design specifications executed during verification. Functional coverage focuses on whether the features and functionalities of the design have been covered by the test cases.

Mapping refers to associating functional points with test cases. This allows you to see which test cases correspond to each functional point during statistics, making it easier to identify which functional points have more test cases and which have fewer. This helps optimize test cases in the later stages.

## Relevant Locations in This Project

Functional coverage must be defined before it can be collected, primarily during the process of building the test environment.

In [Building the Test Environment](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/02_build_env/):

- [Define Functional Coverage](02_build_env.md#2-define-functional-coverage): Create functional coverage groups, add watch points, and map them.
- [Define Necessary Fixtures](02_build_env.md#3-define-necessary-fixtures): Pass the collected results to `toffee-report`.
- [Collect Coverage](02_build_env.md#4-collect-coverage): Add watch points and mappings.

Other:

- Functional points can also be written in each test case for use in test cases.

## Functional Coverage Workflow

### Specify Group Name

The test report matches the Group name with the DUT name. Use `comm.UT_FCOV` to obtain the DUT prefix. For example, in the Python module `ut_frontend/ifu/rvc_expander/classical_version/env/rvc_expander_wrapper.py`, the following call is made:

```python
from comm import UT_FCOV
# Module name: ut_frontend.ifu.rvc_expander.classical_version.env.rvc_expander_wrapper
# Remove classical_version and the parent module env, rvc_expander_wrapper using ../../../
# UT_FCOV will automatically remove the prefix ut_
g = fc.CovGroup(UT_FCOV("../../../CLASSIC"))
# name = UT_FCOV("../../../CLASSIC")
```

The value of `name` is `frontend.ifu.rvc_expander.CLASSIC`. When collecting the final results, the longest prefix will be matched to the target UT (i.e., matched to the `frontend.ifu.rvc_expander` module).

### Create Coverage Group

Use `toffee`'s `funcov` to create a coverage group.

```python
import toffee.funcov as fc
# Use the GROUP name specified above
g = fc.CovGroup(name)
```

These two steps can also be combined into one: `g = fc.CovGroup(UT_FCOV("../../../CLASSIC"))`.  
The created `g` object represents a functional coverage group, which can be used to provide watch points and mappings.

### Add Watch Points and Mappings

Inside each test case, you can use `add_watch_point` (or its alias `add_cover_point`, which is identical) to add watch points and `mark_function` to add mappings.  
A watch point is triggered when the signal meets the conditions defined in the watch point, and its name (i.e., the functional point) will be recorded in the functional coverage.  
A mapping associates functional points with test cases, allowing you to see which test cases correspond to each functional point during statistics.

The location of the watch point depends on the actual situation. Generally, adding watch points outside the test case is acceptable. However, sometimes more flexibility is required.

1. Outside the test case (in `decode_wrapper.py`):

```python
def init_rvc_expander_funcov(expander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect functional coverage information"""
    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR: The instruction is not illegal
    #    - bin SUCCE: The instruction is not expanded
    g.add_watch_point(expander, {
                                "ERROR": lambda x: x.stat()["ilegal"] == False,
                                "SUCCE": lambda x: x.stat()["ilegal"] != False,
                          }, name="RVC_EXPAND_RET")
    # 5. Reverse mark function coverage to the check point
    def _M(name):
        # Get the module name
        return module_name_with(name, "../../test_rv_decode")

    #  - mark RVC_EXPAND_RET
    g.mark_function("RVC_EXPAND_RET", _M(["test_rvc_expand_16bit_full",
                                          "test_rvc_expand_32bit_full",
                                          "test_rvc_expand_32bit_randomN"]), bin_name=["ERROR", "SUCCE"])

    # The End
    return None
```

In this example, the first `g.add_watch_point` is placed outside the test case because it is not directly related to the existing test cases. Placing it outside the test case is more convenient. Once the conditions in the `bins` of the `add_watch_point` method are triggered, the `toffee-test` framework will collect the corresponding functional points.

2. Inside the test case (in `test_rvc_expander.py`):

```python
N = 10
T = 1 << 32
@pytest.mark.toffee_tags([TAG_LONG_TIME_RUN, TAG_RARELY_USED])
@pytest.mark.parametrize("start,end",
                         [(r * (T // N), (r + 1) * (T // N) if r < N - 1 else T) for r in range(N)])
def test_rvc_expand_32bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full 32-bit instruction set

    Description:
        Randomly generate N 32-bit instructions for each check, and repeat the process K times.
    """
    # Add check point: RVC_EXPAND_ALL_32B to check instr bits.
    covered = -1
    g.add_watch_point(rvc_expander, {"RANGE[%d-%d]" % (start, end): lambda _: covered == end},
                      name="RVC_EXPAND_ALL_32B", dynamic_bin=True)
    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_32B", test_rvc_expand_32bit_full)
    # Drive the expander and check the result
    rvc_expand(rvc_expander, list([_ for _ in range(start, end)]))
    # When reaching here, the range [start, end] is covered
    covered = end
    g.sample()
```

In this example, the watch point is inside the test case because `start` and `end` are determined by `pytest.mark.parametrize`. Since the values are not fixed, the watch point needs to be added inside the test case.

### Sampling

At the end of the previous example, we called `g.sample()`. This function notifies `toffee-test` that the `bins` in `add_watch_point` have been executed. If the conditions are met, the watch point is recorded as a pass.

There is also an automatic sampling option. During the test environment setup, you can add `StepRis(lambda x: g.sample())` in the fixture definition. This will automatically sample at the rising edge of each clock cycle.

The following content is from `ut_backend/ctrl_block/decode/env/decode_wrapper.py`:

```python
@pytest.fixture()
def decoder(request):
    # Before test
    init_rv_decoder_funcov(g)
    func_name = request.node.name
    # If the output directory does not exist, create it
    output_dir_path = get_out_dir("decoder/log")
    os.makedirs(output_dir_path, exist_ok=True)
    decoder = Decode(DUTDecodeStage(
        waveform_filename=get_out_dir("decoder/decode_%s.fst" % func_name),
        coverage_filename=get_out_dir("decoder/decode_%s.dat" % func_name),
    ))
    decoder.dut.InitClock("clock")
    decoder.dut.StepRis(lambda x: g.sample())
    yield decoder
    # After test
    decoder.dut.Finish()
    coverage_file = get_out_dir("decoder/decode_%s.dat" % func_name)
    if not os.path.exists(coverage_file):
        raise FileNotFoundError(f"File not found: {coverage_file}")
    set_line_coverage(request, coverage_file, get_root_dir("scripts/backend_ctrlblock_decode"))
    set_func_coverage(request, g)
    g.clear()
```

As shown above, we call `g.sample()` before `yield`, enabling automatic sampling at the rising edge of each clock cycle.

The `StepRis` function executes the passed function at the rising edge of each clock cycle. For more details, refer to the [Picker Usage Guide](https://open-verify.cc/mlvp/docs/env_usage/picker_usage/).
