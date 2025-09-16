这是对香山RISC-V处理器中FtqMeta1rMem模块的验证代码。FtqMeta1rMem是预译码存储子队列，负责存储来自IFU的对指令块的预译码信息。


验证内容

验证覆盖了FtqMeta1rMem子对列的读写主要功能


测试环境

操作系统：Ubuntu 22.04
Python版本：3.10.12
使用工具：Picker 0.9.0, Verilator 5.027, pytest 8.4.0


测试用例

共有1个测试文件，涵盖全部的功能点

运行方式： python3 -m pytest ut_frontend/ftq/ftq_meta_1r_sram/test_ftq_meta_1r_sram.py  -v  

测试结果

所有测试用例均通过，模块功能符合设计预期。