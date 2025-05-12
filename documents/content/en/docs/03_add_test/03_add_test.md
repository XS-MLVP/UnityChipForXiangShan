---
title: Add Test Cases
linkTitle: Add Test Cases
#menu: {main: {weight: 20}}
weight: 4
---

## Naming Requirements

All test case files should be named in the format `test_*.py`, where `*` is replaced with the test target (e.g., `test_rvc_expander.py`). All test cases should also start with the `test_` prefix. The test case names must have clear and meaningful descriptions.

Examples of naming:

```python
def test_a():  # Not acceptable, as "a" does not indicate the test target
    pass

def test_rvc_expand_16bit_full():  # Acceptable, as the name indicates the test content
    pass
```

## Using Assert

Each test case must use `assert` to determine whether the test passes.  
`pytest` relies on the results of `assert` statements, so these statements must ensure correctness.

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/test_rvc_expander.py`:

```python
def rvc_expand(rvc_expander, ref_insts, is_32bit=False, fsIsOff=False):
    """Compare the RVC expand result with the reference

    Args:
        rvc_expander (wrapper): the fixture of the RVC expander
        ref_insts (list[int]): the reference instruction list
    """
    find_error = 0
    for insn in ref_insts:
        insn_disasm = disasmbly(insn)
        value, instr_ex = rvc_expander.expand(insn, fsIsOff)
        if is_32bit:
            assert value == insn, "RVC expand error, 32-bit instruction must remain unchanged"
        if (insn_disasm == "unknown") and (instr_ex == 0):
            debug(f"Found bad instruction: {insn}, ref: 1, dut: 0")
            find_error += 1
        elif (insn_disasm != "unknown") and (instr_ex == 1):
            if (instr_filter(insn_disasm) != 1):
                debug(f"Found bad instruction: {insn}, disasm: {insn_disasm}, ref: 0, dut: 1")
                find_error += 1
    assert find_error == 0, f"RVC expand error ({find_error} errors)"
```

## Writing Comments

Each test case must include necessary explanations and comments, adhering to the [Python Docstring Conventions](https://peps.python.org/pep-0257/).

Example format for test case documentation:

```python
def test_<name>(a: type_a, b: type_b):
    """Test abstract

    Args:
        a (type_a): Description of argument a.
        b (type_b): Description of argument b.

    Detailed test description here (if needed).
    """
    ...
```

## Test Case Management

To facilitate test case management, use the `@pytest.mark.toffee_tags` tag feature provided by `toffee-test`. Refer to the [Other](https://open-verify.cc/UnityChipForXiangShan/docs/98_others/) section of this site and the [toffee-test documentation](https://github.com/XS-MLVP/toffee-test/blob/master/README_zh.md#%E7%AE%A1%E7%90%86%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B%E8%B5%84%E6%BA%90).

## Reference Test Cases

If many test cases share the same operations, the common parts can be extracted into a utility function. For example, in RVCExpander verification, the comparison of compressed instruction expansion with the reference model (`disasm`) can be encapsulated into the following function:

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/test_rvc_expander.py`:

```python
def rvc_expand(rvc_expander, ref_insts, is_32bit=False, fsIsOff=False):
    """Compare the RVC expand result with the reference

    Args:
        rvc_expander (wrapper): the fixture of the RVC expander
        ref_insts (list[int]): the reference instruction list
    """
    find_error = 0
    for insn in ref_insts:
        insn_disasm = disasmbly(insn)
        value, instr_ex = rvc_expander.expand(insn, fsIsOff)
        if is_32bit:
            assert value == insn, "RVC expand error, 32-bit instruction must remain unchanged"
        if (insn_disasm == "unknown") and (instr_ex == 0):
            debug(f"Found bad instruction: {insn}, ref: 1, dut: 0")
            find_error += 1
        elif (insn_disasm != "unknown") and (instr_ex == 1):
            if (instr_filter(insn_disasm) != 1):
                debug(f"Found bad instruction: {insn}, disasm: {insn_disasm}, ref: 0, dut: 1")
                find_error += 1
    assert find_error == 0, f"RVC expand error ({find_error} errors)"
```

The above utility function includes `assert` statements, so the test cases calling this function can also rely on these assertions to determine the results.

During test case development, debugging is often required. To quickly set up the verification environment, "smoke tests" can be written for debugging. For example, a smoke test for expanding 16-bit compressed instructions in RVCExpander is as follows:

```python
@pytest.mark.toffee_tags(TAG_SMOKE)
def test_rvc_expand_16bit_smoke(rvc_expander):
    """Test the RVC expand function with 1 compressed instruction"""
    rvc_expand(rvc_expander, generate_rvc_instructions(start=100, end=101))
```

For easier management, the above test case is tagged with the `SMOKE` label using `toffee_tags`. Its input parameter is `rvc_expander`, which will automatically invoke the corresponding `fixture` with the same name during runtime.

The goal of testing 16-bit compressed instructions in RVCExpander is to traverse all 2^16 compressed instructions and verify that all cases match the reference model (`disasm`). If a single test is used for traversal, it would take a significant amount of time. To address this, we can use `pytest`'s `parametrize` feature to configure test parameters and execute them in parallel using the `pytest-xdist` plugin:

The following content is located in `ut_frontend/ifu/rvc_expander/classical_version/test_rvc_expander.py`:

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
    # When run to here, the range [start, end] is covered
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]" % (start, end): lambda _: True
                          }, name="RVC_EXPAND_ALL_16B").sample()

    # Reverse mark function to the checkpoint
    g.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]" % (start, end))

    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end))
```

In the above test case, the parameters `start` and `end` are defined to specify the range of compressed instructions. These parameters are grouped and assigned using the `@pytest.mark.parametrize` decorator. The variable `N` specifies the number of groups for the target data, with a default of 10 groups. During runtime, the test case `test_rvc_expand_16bit_full` will expand into 10 test cases, such as `test_rvc_expand_16bit_full[0-6553]` to `test_rvc_expand_16bit_full[58977-65536]`.
