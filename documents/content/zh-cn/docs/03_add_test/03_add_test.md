---
title: 添加测试用例
linkTitle: 添加测试用例
#menu: {main: {weight: 20}}
weight: 4
---


## 命名要求

所有测试用例文件请以`test_*.py`的方式进行命名，`*`用测试目标替换。所有测试用例也需要以`test_`前缀开头。用例名称需要具有明确意义。

命名举例如下：

```python
def test_a(): # 不合理，无法通过a判断测试目标
    pass

def test_rvc_expand_16bit_full(): # 合理，可以通过用例名称大体知道测试内容
    pass
```


## 使用Assert

在每个测试用例中，都需要通过 assert 来判断本测试是否通过。


## 编写注释

每个测试用例都需要添加必要的说明和注释，需要满足[Python注释规范]()。

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

为了方便测试用例管理，可通过toffee-test提供的`@pytest.mark.toffee_tags`标签功能，请参考[此处]()。


## 检查点反标

TBD
