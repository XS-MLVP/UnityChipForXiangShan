from toffee import Env  # 导入基类 Env

# 相对导入 FtqBundle 和 FtqAgent（从同级 bundle/ 和 agent/）
from .ftq_bundle  import FtqBundle
from .ftq_agent  import FtqAgent



class FtqEnv(Env):
    def __init__(self, ftq_bundle, dut=None):  # 接收 bundle 和 dut
        super().__init__()
        self.ftq_agent = FtqAgent(ftq_bundle)  # 设置 agent
        self.dut = dut  # 存储 dut 作为实例属性  