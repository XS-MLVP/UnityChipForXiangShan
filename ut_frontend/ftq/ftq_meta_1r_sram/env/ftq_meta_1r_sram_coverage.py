from toffee.funcov import CovGroup
from ..bundle import FtqMeta1rSramBundle    

def define_read0_coverage(bundle: FtqMeta1rSramBundle, dut) -> CovGroup:
    g = CovGroup("ReadPort0")
    g.add_watch_point(
        {
            "ren": bundle.io.ren_0,
            "raddr": bundle.io._raddr_0
        },
        bins={  
            "read_when_addr_0": lambda d: d["ren"].value == 1 and d["raddr"].value == 0,
            "read_when_addr_31": lambda d: d["ren"].value == 1 and d["raddr"].value == 31
        },
        name = "FtqMeta1rSram ReadPort0" 
    )
    return g

def define_write_coverage(bundle: FtqMeta1rSramBundle, dut) -> CovGroup:
    g = CovGroup("WritePort")
    g.add_watch_point(
        {
            "wen": bundle.io._wen,
            "waddr": bundle.io._waddr
        },
        bins={  
            "write_when_addr_0": lambda d: d["wen"].value == 1 and d["waddr"].value == 0,
            "write_when_addr_31": lambda d: d["wen"].value == 1 and d["waddr"].value == 31
        },
        name = "FtqMeta1rSram WritePort" 
    )
    return g

def create_coverage_groups(bundle: FtqMeta1rSramBundle, dut) -> list[CovGroup]:
    read0_coverage = define_read0_coverage(bundle, dut)
    write_coverage = define_write_coverage(bundle, dut)
    return [read0_coverage, write_coverage]