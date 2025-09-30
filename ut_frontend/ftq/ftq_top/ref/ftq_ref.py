from collections import namedtuple
import random

# --- 数据结构定义 ---
BpuPacket = namedtuple('BpuPacket', ['pc', 'fallThruError'])
FtqPointer = namedtuple('FtqPointer', ['value', 'flag'])
FTQ_SIZE = 64
# --- 最终版参考模型 ---

def get_random_ptr_before_bpu(bpu_ptr: FtqPointer) -> FtqPointer:
    steps_to_go_back = random.randint(1, FTQ_SIZE - 1)
    new_value = bpu_ptr.value
    new_flag = bpu_ptr.flag
    for _ in range(steps_to_go_back):
        if new_value == 0:
            new_value = FTQ_SIZE - 1
            new_flag = not new_flag
        else:
            new_value -= 1
        
    return FtqPointer(new_value, new_flag)  

class FtqAccurateRef:
    """参考模型，所有指针计算和逻辑判断直接内联执行"""


    def __init__(self, ftq_size=64):
        self.FTQ_SIZE = ftq_size
        self.bpu_ptr = FtqPointer(0, False)
        self.ifu_ptr = FtqPointer(0, False)
        self.mem = {}

    def enqueue(self, data_packet):
        if FtqPointer(
            (self.bpu_ptr.value + 1) % self.FTQ_SIZE,
            self.bpu_ptr.flag if self.bpu_ptr.value != self.FTQ_SIZE - 1 else not self.bpu_ptr.flag
        ) == self.ifu_ptr:
            return False

        self.mem[self.bpu_ptr.value] = data_packet
        self.bpu_ptr = FtqPointer(
            (self.bpu_ptr.value + 1) % self.FTQ_SIZE,
            self.bpu_ptr.flag if self.bpu_ptr.value != self.FTQ_SIZE - 1 else not self.bpu_ptr.flag
        )
        return True

    def dequeue(self):
        if self.bpu_ptr == self.ifu_ptr:
            return None

        data = self.mem[self.ifu_ptr.value]
        self.ifu_ptr = FtqPointer(
            (self.ifu_ptr.value + 1) % self.FTQ_SIZE,
            self.ifu_ptr.flag if self.ifu_ptr.value != self.FTQ_SIZE - 1 else not self.ifu_ptr.flag
        )

        
        return data

  

    def redirect(self, redirect_idx, redirect_flag, redirect_packet):
        self.mem[redirect_idx] = redirect_packet
        
        self.bpu_ptr = FtqPointer(
            (redirect_idx + 1) % self.FTQ_SIZE,
            bool(redirect_flag) if redirect_idx != self.FTQ_SIZE - 1 else not bool(redirect_flag)
        )
        
        if  (((bool(redirect_flag) == self.ifu_ptr.flag) and (redirect_idx <= self.ifu_ptr.value)) or \
                ((bool(redirect_flag) != self.ifu_ptr.flag) and (redirect_idx > self.ifu_ptr.value))):
            self.ifu_ptr = FtqPointer(redirect_idx, bool(redirect_flag))
    # 假设 FtqPointer 是一个已定义的类
    # 假设 self.mem = {}