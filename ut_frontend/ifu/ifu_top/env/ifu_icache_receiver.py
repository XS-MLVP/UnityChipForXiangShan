from ..commons import PREDICT_WIDTH, is_next_line, is_last_in_line

class IFUICacheReceiverRef():
    def __init__(self):
        pass
    
    def gen_exceptions(self,none_mmio_exceptions, mmio_exceptions):
        f2_exception = []
        for i in range(2):
            f2_exception.append(none_mmio_exceptions[i] if none_mmio_exceptions[i] != 0 else mmio_exceptions[i])
        return f2_exception
    
    def gen_exceptions_each_instr(self, non_mmio_exceptions, mmio_exceptions, pcs, rvcs, start_addr, double_line):
        cross_page_vec = []
        exception_each_instr = []
        f2_exception = self.gen_exceptions(non_mmio_exceptions, mmio_exceptions)
        # 生成每条指令的异常情况
        for i in range(PREDICT_WIDTH):
            if not is_next_line(pcs[i], start_addr):
                exception_each_instr.append(f2_exception[0])
            else:
                exception_each_instr.append(f2_exception[1] if double_line else 0)

            enable_next = is_last_in_line(pcs[i]) and not rvcs[i] and double_line and non_mmio_exceptions[0] == 0 
            cross_page_vec.append(non_mmio_exceptions[1] if enable_next else 0)
        return exception_each_instr, cross_page_vec
    
    