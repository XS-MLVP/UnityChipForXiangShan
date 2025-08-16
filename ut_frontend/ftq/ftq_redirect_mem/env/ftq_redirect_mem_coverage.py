import toffee.funcov as fc
from toffee.funcov import CovGroup

def define_read_coverage(bundle, dut) -> CovGroup:
    g = CovGroup("")
    pass
def define_write_coverage(bundle, dut) -> CovGroup:
    
    pass

def create_coverage_groups(bundle,dut):
    read_coverage = define_read_coverage(bundle,dut)
    write_coverage = define_write_coverage(bundle,dut)
    return [read_coverage, write_coverage]