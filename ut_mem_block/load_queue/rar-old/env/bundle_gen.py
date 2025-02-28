from bundle_code_gen import *
import sys
import os

# 添加新模块路径到 sys.path
sys.path.append(os.path.abspath("../../../../"))
from dut.LoadQueueRAR import *

dut = DUTLoadQueueRAR()
code = gen_bundle_code_from_prefix('InnerBundle', dut, 'LoadQueueRAR_')
with open("InnerBundle.py", 'w') as file:
        file.write(code + '\n')  # 写入代码并换行
# gen_bundle_code_from_regex('AdderBundle', dut, r'io_(.*)')

