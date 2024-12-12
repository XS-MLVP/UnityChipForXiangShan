---
title: 添加测试用例
linkTitle: 添加测试用例
#menu: {main: {weight: 20}}
weight: 4
---

## 命名要求

所有测试用例文件请以`test_*.py`的方式进行命名，`*`用测试目标替换（例如`test_rv_decode.py`）。所有测试用例也需要以`test_`前缀开头。用例名称需要具有明确意义。

命名举例如下：

```python
def test_a(): # 不合理，无法通过a判断测试目标
    pass

def test_rvc_expand_16bit_full(): # 合理，可以通过用例名称大体知道测试内容
    pass
```

## 使用 Assert

在每个测试用例中，都需要通过`assert`来判断本测试是否通过。
`pytest`统计的是`assert`语句的结果，因此`assert`语句需要保证能够通过。

```python
 def test_rvi_inst(decoder, rvc_expander):
     """
     Test the RVI instruction set. randomly generate instructions for testing

     Args:
         decoder (fixure): the fixture of the decoder
     """
     need_log_file   = True
     insn_list_temp  = generate_random_32bits(100)
     ref_lists       = convert_reference_format(rvc_expander, insn_list_temp, True, libdisasm.disasm, libdisasm.disasm_free_mem)
     assert decode_run(decoder, ref_lists, need_log_file,"test_rvi_inst") == True, "RVI decode error"
     g.add_cover_point(decoder, {"illegal_inst_triggers_an_exception": lambda _: decoder.Get_decode_checkpoint_illeagl_inst() != 0}, name="RVI_illegal_inst").sample()
     g.add_cover_point(decoder, {"fast_check_random_32bit_int": lambda _: True}, name="RVI").sample()
```

## 编写注释

每个测试用例都需要添加必要的说明和注释，需要满足[Python 注释规范](https://peps.python.org/pep-0257/)。

测试用例说明参考格式：

```python
def test_<name>(a: type_a, b: type_b):
    """Test abstract

    Args:
        a (type_a): description of arg a.
        b (type_b): description of arg b.

    Detailed test description here (if need).
    """
    ...
```

## 用例管理

为了方便测试用例管理，可通过 toffee-test 提供的`@pytest.mark.toffee_tags`标签功能，请参考
本网站的[其他](https://open-verify.cc/UnityChipForXiangShan/docs/98_others/)部分和[toffee-test](https://github.com/XS-MLVP/toffee-test/blob/master/README_zh.md#%E7%AE%A1%E7%90%86%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B%E8%B5%84%E6%BA%90)。

## 参考用例

如果很多测试用例（Test）具有相同的操作，该公共操作部分可以提炼成一个通用函数。以 RVCExpander 验证为例，可以把压缩指令的展开与参考模型（disasm）的对比封装成以下函数：

```python
def rvc_expand(rvc_expander, ref_insts):
    """compare the RVC expand result with the reference

    Args:
        rvc_expander (warpper): the fixture of the RVC expander
        ref_insts (list[int]]): the reference instruction list
    """
    find_error = 0
    for insn in ref_insts:
        insn_disasm = disasmbly(insn)
        _, instr_ex = rvc_expander.expand(insn)
        if (insn_disasm == "unknown") and  (instr_ex == 0):
            debug(f"find bad inst:{insn}, ref: 1, dut: 0")
            find_error +=1
        elif (insn_disasm != "unknown") and  (instr_ex == 1):
            debug(f"find bad inst:{insn}, ref: 0, dut: 1")
            find_error +=1
    assert 0 == find_error, "RVC expand error (%d errros)" % find_error
```

在上述公共部分中有 assert，因此调用该函数的 Test 也能提过该 assert 判断运行结果是否提过。

在测试用例的开发过程中，通常存在大量的调试工作，为了让验证环境快速就位，需要编写一些“冒烟测试”进行调试。RVCExpander 展开 16 位压缩指令的冒烟测试如下：

```python
@pytest.mark.toffee_tags(TAG_SMOKE)
def test_rvc_expand_16bit_smoke(rvc_expander):
    """Test the RVC expand function with 1 compressed instruction"""
    rvc_expand(rvc_expander, generate_rvc_instructions(start=100, end=101))
```

为了方便进行管理，上述测试用例通过`toffee_tags`标记上了 SMOKE 标签。它的输入参数为`rvc_expander`，则在在运行时，会自动调用对应同名的`fixture`进行该参数的填充。

RVCExpander 展开 16 位压缩指令的测试目标是对 2^16 所有压缩指令进行遍历，检测所有情况是否都与参考模型 disasm 一致。在实现上，如果仅仅用一个 Test 进行遍历，则需要耗费大量时间，为此我们可以利用 PyTest 提供的`parametrize`对 test 进行参数化配置，然后通过`pytest-xdist`插件并行执行：

```python
N = 10
T = 1<<16
@pytest.mark.toffee_tags(TAG_LONG_TIME_RUN)
@pytest.mark.parametrize("start,end",
                         [(r*(T//N), (r+1)*(T//N) if r < N-1 else T) for r in range(N)])
def test_rvc_expand_16bit_full(rvc_expander, start, end):
    """Test the RVC expand function with a full compressed instruction set

    Description:
        Perform an expand check on 16-bit compressed instructions within the range from 'start' to 'end'.
    """
    # Add check point: RVC_EXPAND_RANGE to check expander input range.
    #   When run to here, the range[start, end] is covered
    g.add_watch_point(rvc_expander, {
                                "RANGE[%d-%d]"%(start, end): lambda _: True
                          }, name = "RVC_EXPAND_ALL_16B").sample()

    # Reverse mark function to the check point
    g.mark_function("RVC_EXPAND_ALL_16B", test_rvc_expand_16bit_full, bin_name="RANGE[%d-%d]"%(start, end))

    # Drive the expander and check the result
    rvc_expand(rvc_expander, generate_rvc_instructions(start, end))
```

在上述用例中定义了参数化参数`start`, `end`，用来指定压缩指令的开始值和结束值，然后通过装饰器`@pytest.mark.parametrize`对他们进行分组赋值。变量 N 可以指定将目标数据进行分组的组数，默认设置为 10 组。在运行时用例`test_rvc_expand_16bit_full`会展开为`test_rvc_expand_16bit_full[0-6553]`至`test_rvc_expand_16bit_full[58977-65536]`10 个测试用例运行。
