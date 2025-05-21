# FrontendTrigger 单元验证


使用了 toffee 测试框架对 FrontendTrigger 模块进行单元验证。
并且基于 toffee 中的类 UVM 接口，编写了一系列测试函数来验证 FrontendTrigger 模块的功能。测试根目录为 `ut_frontend/ifu/frontend_trigger`。

## 文件说明


| 文件名                                 | 描述                                                                    |
| -------------------------------------- | ----------------------------------------------------------------------- |
| `doc.md`                               | 本文件，包含测试概要、测试点、测试函数和功能覆盖点等信息。              |
| `agent/frontend_trigger_agent.py`      | 定义了 FrontendTrigger 的 agent 类，包含 driver、monitor 等方法。       |
| `test/frontend_trigger_common_test.py` | 定义了一些常用通用的测试函数，用于验证 FrontendTrigger 模块的基本功能。 |
| `test/frontend_trigger_ref.py`         | 定义了参考模型，用于验证 FrontendTrigger 模块的行为是否符合预期。       |
| `test/test_bug_examples.py`            | 出现 bug 的测试用例                                                     |
| `test/test_normal_match.py`            | 单个断点并且匹配类型为等于、大于等于、小于的测试用例。                  |
| `test/test_normal_no_match.py`         | 单个断点,但一些标志位不满足的测试用例，例如 tselect=1 或 enable=0 等。  |
| `test/test_chain_match.py`             | 链式断点的测试用例，测试链式断点的触发情况。                            |
| `test/test_chain_select_no_match.py`   | 链式断点的测试用例，测试链式断点在 select 条件不满足时的触发情况。      |
| `test/test_chain_enable_no_match.py`   | 链式断点的测试用例，测试链式断点在 enable 条件不满足时的触发情况。      |



## 测试点汇总

| 序号  | 功能           | 名称                  | 描述                                                                                                              |
| ----- | -------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1.1   | 断点设置和检查 | select1判定           | 给定tdata1的select位为1，随机构造其它输入，检查断点是否没有触发                                                   |
| 1.2.1 | 断点设置和检查 | select0关系匹配判定   | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位匹配的输入，检查断点是否触发                    |
| 1.2.2 | 断点设置和检查 | select0关系不匹配判定 | 给定tdata1的select位为0，构造PC与tdata2数据的关系同tdata2的match位不匹配的输入，检查断点是否触发                  |
| 2.1   | 链式断点       | chain位测试           | 对每个trigger，在满足PC断点触发条件的情况下，设置chain位，检查断点是否一定不触发                                  |
| 2.2.1 | 链式断点       | 未命中测试            | 对两个trigger，仅设置前一个trigger的chain位，设置后一个trigger命中而前一个未命中，检查后一个trigger是否一定不触发 |
| 2.2.2 | 链式断点       | 命中测试              | 对两个trigger，仅设置前一个trigger的chain位，检查后一个trigger是否触发                                            |

## 测试函数汇总

| 测试函数                    | 测试点功能                                                                  | 包含测试点   |
| --------------------------- | --------------------------------------------------------------------------- | ------------ |
| test_tselect1_no_match      | 测试 tselect=1 时，不应该触发任何断点                                       | 1.1          |
| test_enable0_no_match       | 测试 enable=0 时，不应该触发任何断点                                        | 无           |
| test_chain_no_match         | 测试 chain 为 True 时，该断点不应该触发                                     | 2.1          |
| test_match_eq               | 测试 matchType=0 (等于) 的单个断点触发情况                                  | 1.2.1, 1.2.2 |
| test_match_ge               | 测试 matchType=2 (大于等于) 的单个断点触发情况                              | 1.2.1, 1.2.2 |
| test_match_lt               | 测试 matchType=3 (小于) 的单个断点触发情况                                  | 1.2.1, 1.2.2 |
| test_chain2_match           | 测试点：链式断点个数为 2 时，触发情况测试                                   | 2.2.2        |
| test_chain3_match           | 测试点：链式断点个数为 3 时，触发情况测试                                   | 2.2.2        |
| test_chain4_match           | 测试点：链式断点个数为 4 时，触发情况测试                                   | 2.2.2        |
| test_chain2_enable_no_match | 测试点：链式断点个数为 2 时，且随机一个 enable 条件不满足，不应该触链式断点 | 2.2.1        |
| test_chain3_enable_no_match | 测试点：链式断点个数为 3 时，且随机一个 enable 条件不满足，不应该触链式断点 | 2.2.1        |
| test_chain4_enable_no_match | 测试点：链式断点个数为 4 时，且随机一个 enable 条件不满足，不应该触链式断点 | 2.2.1        |
| test_chain2_select_no_match | 测试点：链式断点个数为 2 时，且随机一个 select 条件不满足，不应该触链式断点 | 2.2.1        |
| test_chain3_select_no_match | 测试点：链式断点个数为 3 时，且随机一个 select 条件不满足，不应该触链式断点 | 2.2.1        |
| test_chain4_select_no_match | 测试点：链式断点个数为 4 时，且随机一个 select 条件不满足，不应该触链式断点 | 2.2.1        |

## 功能覆盖点汇总

| 功能点类别            | 功能点名称                        | 功能点描述         | 可能的值                                                                                                       |
| --------------------- | --------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------- |
| **断点触发情况**      | PC0_TRIGGERED ~ PC15_TRIGGERED    | 断点0-15的触发状态 | BKPT_EXCPT: 未触发(io_triggered_i=0)<br>DEBUG_MODE: 已触发(io_triggered_i=1)                                   |
| **断点设置-匹配类型** | TRI0_MATCH_TYPE ~ TRI3_MATCH_TYPE | 断点0-3的匹配类型  | EQ: 等于(matchType=0)<br>GE: 大于等于(matchType=2)<br>LT: 小于(matchType=3)                                    |
| **断点设置-选择标志** | TRI0_SELECT ~ TRI3_SELECT         | 断点0-3的选择设置  | SELECT_0: select=0<br>SELECT_1: select=1                                                                       |
| **断点设置-动作类型** | TRI0_ACTION ~ TRI3_ACTION         | 断点0-3的动作设置  | ACTION_0: action=0<br>ACTION_1: action=1                                                                       |
| **断点设置-链式标志** | TRI0_CHAIN ~ TRI3_CHAIN           | 断点0-3的链式设置  | CHAIN_0: chain=0<br>CHAIN_1: chain=1                                                                           |
| **断点设置-地址数据** | TRI0_tdata2 ~ TRI3_tdata2         | 断点0-3的地址设置  | tdata2_0x{范围起始地址}: 地址在[range_start, range_end)范围内<br>注：地址范围按get_mask_one(50)÷1024的步长划分 |
