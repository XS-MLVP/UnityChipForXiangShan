---
title: Build Test Environment
linkTitle: Build Test Environment
#menu: {main: {weight: 20}}
weight: 3
---

## Determine Directory Structure

The directory structure of the Unit Test (UT) should match its naming convention. For example, `frontend.ifu.rvc_expander` should be located in the `ut_frontend/ifu/rvc_expander` directory, and each directory level must include an `__init__.py` file to enable Python imports.

**The file for this chapter is `your_module_wrapper.py`** (if your module is `rvc_expander`, the file would be `rvc_expander_wrapper.py`).

A wrapper is essentially a layer of abstraction that encapsulates the methods needed for testing into APIs decoupled from the DUT. These APIs are then used in test cases.

\*Note: Decoupling ensures that test cases are independent of the DUT, allowing them to be written and debugged without needing to know the DUT's implementation details. For more information, refer to [Decoupling Verification Code from the DUT](https://open-verify.cc/mlvp/docs/mlvp/canonical_env/#%E5%B0%86%E9%AA%8C%E8%AF%81%E4%BB%A3%E7%A0%81%E4%B8%8Edut%E8%BF%9B%E8%A1%8C%E8%A7%A3%E8%80%A6).

This file should be placed in the `ut_frontend_or_backend/top_module/your_module/env` directory. For example, if `rvc_expander` belongs to the frontend, its top-level directory should be `ut_frontend`. The next-level directory would be `ifu`, followed by `rvc_expander`. Since we are **building the test environment**, an additional `env` directory is created. The full path would be: `ut_frontend_or_backend/top_module/your_module/env`.

```shell
ut_frontend/ifu/rvc_expander
├── classical_version
│   ├── env
│   │   ├── __init__.py
│   │   └── rvc_expander_wrapper.py
│   ├── __init__.py
│   └── test_rvc_expander.py
├── __init__.py
├── README.md
└── toffee_version
    ├── agent
    │   └── __init__.py
    ├── bundle
    │   └── __init__.py
    ├── env
    │   ├── __init__.py
    │   └── ref_rvc_expand.py
    ├── __init__.py
    └── test
        ├── __init__.py
        ├── rvc_expander_fixture.py
        └── test_rvc.py
```

In the `rvc_expander` directory, there are two versions: `classical_version` (traditional) and `toffee_version` (using Toffee).  
The traditional version uses the `pytest` framework for testing, while the Toffee version leverages more features of the Toffee framework.  
In general, **the traditional version is sufficient for most cases**, and the Toffee version is only needed when the traditional version cannot meet the requirements.  
When building the test environment, **choose one version**.  
The directory structure within a module (e.g., `rvc_expander`) is determined by the contributor. You do **not** need to create additional `classical_version` or `toffee_version` directories, but the structure must comply with Python standards and be logically and consistently named.

## Env Requirements

- Perform RTL version checks.
- The APIs provided by Env must be independent of pins and timing.
- The APIs provided by Env must be stable and should not undergo arbitrary changes in interfaces or return values.
- Define necessary fixtures.
- Initialize functional checkpoints (functional checkpoints can be independent modules).
- Perform coverage statistics.
- Include documentation.

## Building the Test Environment: Traditional Version

In the test environment for the UT verification module, the goal is to accomplish the following:

1. Encapsulate DUT functionality to provide stable APIs for testing.
2. Define functional coverage.
3. Define necessary fixtures for test cases.
4. Collect coverage statistics at appropriate times.

Taking the RVCExpander in the IFU environment as an example (`ut_frontend/ifu/rvc_expander/classical_version/env/rvc_expander_wrapper.py`):

### 1. DUT Encapsulation

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/env/rvc_expander_wrapper.py`.

```python
class RVCExpander(toffee.Bundle):
    def __init__(self, cover_group, **kwargs):
        super().__init__()
        self.cover_group = cover_group
        self.dut = DUTRVCExpander(**kwargs)                     # Create DUT
        self.io = toffee.Bundle.from_prefix("io_", self.dut)    # Bind pins using Bundle and prefix
        self.bind(self.dut)                                     # Bind Bundle to DUT

    def expand(self, instr, fsIsOff):
        self.io["in"].value = instr                                 # Assign value to DUT pin
        self.io["fsIsOff"].value = fsIsOff                          # Assign value to DUT pin
        self.dut.RefreshComb()                                      # Trigger combinational logic
        self.cover_group.sample()                                   # Collect functional coverage statistics
        return self.io["out_bits"].value, self.io["ill"].value      # Return result and illegal instruction flag

    def stat(self):  # Get current state
        return {
            "instr": self.io["in"].value,           # Input instruction
            "decode": self.io["out_bits"].value,    # Decoded result
            "illegal": self.io["ill"].value != 0,   # Whether the input is illegal
        }
```

In the example above, `class RVCExpander` encapsulates `DUTRVCExpander` and provides two APIs:

- `expand(instr: int, fsIsOff: bool) -> (int, int)`: Accepts an input instruction `instr` for decoding and returns `(result, illegal instruction flag)`. If the illegal instruction flag is non-zero, the input instruction is illegal.
- `stat() -> dict(instr, decode, illegal)`: Returns the current state, including the input instruction, decoded result, and illegal instruction flag.

These APIs **abstract away the DUT's pins**, exposing only general functionality to external programs.

### 2. Define Functional Coverage

Define functional coverage in the environment whenever possible. If necessary, coverage can also be defined in test cases. For details on defining functional coverage with Toffee, refer to [What is Functional Coverage](http://localhost:1313/docs/03_add_test/05_cover_func/). To establish a clear relationship between functional checkpoints and test cases, functional coverage definitions should be linked to test cases (reverse marking).

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/env/rvc_expander_wrapper.py`.

```python
import toffee.funcov as fc
# Create a functional coverage group
g = fc.CovGroup(UT_FCOV("../../../CLASSIC"))

def init_rvc_expander_funcov(expander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect functional coverage information"""

    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR: The instruction is not illegal
    #    - bin SUCCE: The instruction is not expanded
    g.add_watch_point(expander, {
                                "ERROR": lambda x: x.stat()["illegal"] == False,
                                "SUCCE": lambda x: x.stat()["illegal"] != False,
                          }, name="RVC_EXPAND_RET")
    ...
    # 5. Reverse mark functional coverage to the checkpoint
    def _M(name):
        # Get the module name
        return module_name_with(name, "../../test_rv_decode")

    #  - Mark RVC_EXPAND_RET
    g.mark_function("RVC_EXPAND_RET", _M(["test_rvc_expand_16bit_full",
                                          "test_rvc_expand_32bit_full",
                                          "test_rvc_expand_32bit_randomN"]), bin_name=["ERROR", "SUCCE"])
    ...
```

In the code above, a functional checkpoint named `RVC_EXPAND_RET` is added to check whether the `RVCExpander` module can return illegal instructions. The checkpoint requires both `ERROR` and `SUCCE` conditions to be met, meaning the `illegal` field in `stat()` must have both `True` and `False` values. After defining the checkpoint, the `mark_function` method is used to link it to the relevant test cases.

### 3. Define Necessary Fixtures

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/env/rvc_expander_wrapper.py`.

```python
version_check = get_version_checker("openxiangshan-kmh-*")                  # Specify the required RTL version
@pytest.fixture()
def rvc_expander(request):
    version_check()                                                         # Perform version check
    fname = request.node.name                                               # Get the name of the test case using this fixture
    wave_file = get_out_dir("decoder/rvc_expander_%s.fst" % fname)          # Set waveform file path
    coverage_file = get_out_dir("decoder/rvc_expander_%s.dat" % fname)      # Set code coverage file path
    coverage_dir = os.path.dirname(coverage_file)
    os.makedirs(coverage_dir, exist_ok=True)                                # Create directory if it doesn't exist
    expander = RVCExpander(g, coverage_filename=coverage_file, waveform_filename=wave_file)
                                                                            # Create RVCExpander
    expander.dut.io_in.AsImmWrite()                                         # Set immediate write timing for io_in pin
    expander.dut.io_fsIsOff.AsImmWrite()                                    # Set immediate write timing for io_fsIsOff pin
    init_rvc_expander_funcov(expander, g)                                   # Initialize functional checkpoints
    yield expander                                                          # Return the created RVCExpander to the test case
    expander.dut.Finish()                                                   # End DUT after the test case is executed
    set_line_coverage(request, coverage_file)                               # Report code coverage file to toffee-report
    set_func_coverage(request, g)                                           # Report functional coverage data to toffee-report
    g.clear()                                                               # Clear functional coverage statistics
```

This fixture accomplishes the following:

1. Performs RTL version checks. If the version does not meet the `"openxiangshan-kmh-*"` requirement, the test case using this fixture is skipped.
2. Creates the DUT and specifies the paths for waveform and code coverage files (the paths include the name of the test case using the fixture: `fname`).
3. Calls `init_rvc_expander_funcov` to add functional coverage points.
4. Ends the DUT and processes code and functional coverage (sending them to `toffee-report` for processing).
5. Clears functional coverage statistics.

\*Note: In PyTest, before executing a test case like `test_A(rvc_expander, ...)`, (**rvc_expander is the method name we defined when we used the fixure decorator**), the part of `rvc_expander(request)` before the `yield` keyword will be automatically called and executed (which is equivalent to initialization). and then `rvc_expander` will be returned to call the `test_A` case via `yield` (**the object returned by yield is the method name we defined in our fixture of the test case**). After the execution of the case is completed, then continue to execute the part of the `fixture` after the `field` keyword. For example: refer to the following code of statistical coverage, the penultimate line of `rvc_expand(rvc_expander, generate_rvc_instructions(start, end))`, where `rvc_expander` is the name of the method that we defined in the `fixture`, that is, the `yield` return object.

### 4. Collect Coverage Statistics

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/test_rvc_expander.py`.

```python
N = 10
T = 1 << 16
@pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
@pytest.mark.parametrize("start,end",
                         [(r * (T // N), (r + 1) * (T // N) if r < N - 1 else T) for r in range(N)])
def test_rvc_expand_16bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full compressed instruction set

    Description:
        Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
    """
    # Add checkpoint: RVC_EXPAND_RANGE to check expander input range.
    #   When run to here, the range[start, end] is covered
    covered = -1
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]" % (start, end): lambda _: covered == end
                          }, name="RVC_EXPAND_ALL_16B", dynamic_bin=True)
    # Reverse mark function to the checkpoint
    g.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]" % (start, end))
    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end))
    # When go to here, the range[start, end] is covered
    covered = end
    g.sample()  # Sample coverage
```

After defining coverage, it must be collected in the test cases. In the code above, a functional checkpoint `rvc_expander` is added in the test case using `add_watch_point`. The checkpoint is then marked and sampled. Coverage sampling triggers a callback function to evaluate the `bins` defined in `add_watch_point`. If any `bins`'s condition evaluates to `True`, it is counted as a `pass`.

## Building the Test Environment: Toffee Version

Testing with Python can be enhanced by using our open-source testing framework [Toffee](https://github.com/XS-MLVP/toffee).

The official Toffee tutorial can be found [here](https://open-verify.cc/mlvp/docs/mlvp/).

### Bundle: Quick DUT Encapsulation

Toffee uses Bundles to bind to DUTs. It provides multiple methods for establishing Bundle-to-DUT bindings. Relevant code can be found in `ut_frontend/ifu/rvc_expander/toffee_version/bundle`.

#### Manual Binding

In the Toffee framework, the lowest-level class supporting pin binding is `Signal`, which binds to DUT pins using name matching. For example, consider the simplest RVCExpander with the following I/O pins:

```verilog
module RVCExpander(
  input  [31:0] io_in,
  input         io_fsIsOff,
  output [31:0] io_out_bits,
  output        io_ill
);
```

There are four signals: `io_in`, `io_fsIsOff`, `io_out_bits`, and `io_ill`. A common prefix, such as `io_`, can be extracted (note that `in` cannot be used directly as a variable name in Python). The remaining parts can be defined as pin names in the corresponding Bundle class:

```python
class RVCExpanderIOBundle(Bundle):
    _in, _fsIsOff, _out_bits, _ill = Signals(4)
```

In a higher-level Env or Bundle, the `from_prefix` method can be used to complete the prefix binding:

```python
self.agent = RVCExpanderAgent(RVCExpanderIOBundle.from_prefix("io").bind(dut))
```

#### Automatic Bundle Definition

The Bundle class definition can also be omitted by using prefix binding:

```python
self.io = toffee.Bundle.from_prefix("io_", self.dut)  # Bind pins using Bundle and prefix
self.bind(self.dut)
```

If the `from_prefix` method is passed a DUT, it automatically generates pin definitions based on the prefix and DUT pin names. Accessing the pins can then be done using a dictionary-like approach:

```python
self.io["in"].value = instr
self.io["fsIsOff"].value = False
```

#### Bundle Code Generation

The Toffee framework's [scripts](https://github.com/XS-MLVP/toffee/tree/master/scripts) provide two scripts.

The `bundle_code_gen.py` script offers three methods:

```python
def gen_bundle_code_from_dict(bundle_name: str, dut, dict: dict, max_width: int = 120)
def gen_bundle_code_from_prefix(bundle_name: str, dut, prefix: str = "", max_width: int = 120)
def gen_bundle_code_from_regex(bundle_name: str, dut, regex: str, max_width: int = 120)
```

These methods generate Bundle code by passing in a DUT and generation rules (dict, prefix, or regex).

The `bundle_code_intel_gen.py` script parses the `signals.json` file generated by Picker to automatically generate hierarchical Bundle code. It can be invoked from the command line:

```bash
python bundle_code_intel_gen.py [signal] [target]
```

If you encounter bugs in the auto-generation scripts, feel free to submit an issue for us to fix.

### Agent: Driving Methods

If Bundles abstract the data responsibilities of a DUT, Agents encapsulate its behavioral responsibilities into interfaces. Simply put, an Agent provides multiple methods that abstract groups of I/O operations into specific behaviors:

```python
class RVCExpanderAgent(Agent):
    def __init__(self, bundle: RVCExpanderIOBundle):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def expand(self, instr, fsIsOff):             # Accepts RVC instruction and fs.status enable flag
        self.bundle._in.value = instr                   # Assign value to pin
        self.bundle._fsIsOff.value = fsIsOff            # Assign value to pin

        await self.bundle.step()                        # Trigger clock
        return self.bundle._out_bits.value,             # Return expanded instruction
               self.bundle._ill.value                   # Return legality check
```

For example, the RVCExpander's instruction expansion function accepts an input instruction (which could be an RVI or RVC instruction) and the CSR's enable flag for `fs.status`. This functionality is abstracted into the `expand` method, which takes two parameters in addition to `self`. The method returns the corresponding RVI instruction and a legality check for the input instruction.

### Env: Test Environment

```python
class RVCExpanderEnv(Env):
    def __init__(self, dut: DUTRVCExpander):
        super().__init__()
        dut.io_in.xdata.AsImmWrite()
        dut.io_fsIsOff.xdata.AsImmWrite()  # Set pin write timing
        self.agent = RVCExpanderAgent(RVCExpanderIOBundle.from_prefix("io").bind(dut))  # Complete prefix and bind DUT
```

### Coverage Definition

The method for defining coverage groups is similar to the one described earlier and will not be repeated here.

### Test Suite Definition

The definition of test suites differs slightly:

```python
@toffee_test.fixture
async def rvc_expander(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    version_check()
    dut = toffee_request.create_dut(DUTRVCExpander)
    start_clock(dut)
    init_rvc_expander_funcov(dut, gr)

    toffee_request.add_cov_groups([gr])
    expander = RVCExpanderEnv(dut)
    yield expander

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
```

Due to Toffee's more powerful coverage management features, manual line coverage settings are not needed. Additionally, because of Toffee's clock mechanism, it is recommended to check if all tasks have ended at the end of the suite code.
