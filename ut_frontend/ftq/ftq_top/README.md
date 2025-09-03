这是对香山RISC-V处理器中FtqTop模块的验证代码。FtqTop是指令取指目标队列模块，负责管理处理器前端的指令流。

验证内容

验证覆盖了FtqTop模块的7个主要功能：
向IFU发送取指目标
接收并处理IFU预译码信息
响应后端重定向
响应IFU重定向
向后端发送取指目标
响应重定向并更新内部状态
冲刷指针和状态队列


测试环境

操作系统：Ubuntu 22.04
Python版本：3.10.12
使用工具：Picker 0.9.0, Verilator 5.027, pytest 8.4.0


测试用例

共有7个测试文件，对应不同的功能点：
test_ftq_top3.py：测试取指目标发送功能
test_ftq_top4.py：测试预译码处理功能
test_ftq_top5.py：测试后端重定向响应
test_ftq_top6.py：测试IFU重定向响应
test_ftq_top7.py：测试向后端发送目标
test_ftq_top8.py：测试状态更新
test_ftq_top9.py：测试冲刷逻辑

运行方式：make run CASE=数字（3-9）


测试结果

所有测试用例均通过，行覆盖率达到76.2%，模块功能符合设计预期。