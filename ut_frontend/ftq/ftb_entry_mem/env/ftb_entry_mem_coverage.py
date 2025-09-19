from toffee.funcov import CovGroup
from ..bundle import FtbEntryMemBundle

def define_read0_coverage(bundle: FtbEntryMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPort0")
    g.add_watch_point(
        {
            "ren": bundle.io._ren._0,
            "raddr": bundle.io._raddr._0
        },
        bins={  
            "read_when_addr_0": lambda d: d["ren"].value == 1 and d["raddr"].value == 0,
            "read_when_addr_31": lambda d: d["ren"].value == 1 and d["raddr"].value == 31
        },
        name = "FtbEntryMem ReadPort0" 
    )
    return g

def define_read1_coverage(bundle: FtbEntryMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPort1")
    g.add_watch_point(
        {
            "ren": bundle.io._ren._1,
            "raddr": bundle.io._raddr._1
        },
        bins={  
            "read_when_addr_0": lambda d: d["ren"].value == 1 and d["raddr"].value == 0,
            "read_when_addr_31": lambda d: d["ren"].value == 1 and d["raddr"].value == 31
        },
        name = "FtbEntryMem ReadPort1" 
    )
    return g

def define_write_coverage(bundle: FtbEntryMemBundle, dut) -> CovGroup:
    g = CovGroup("WritePort")
    g.add_watch_point(
        {
            "wen": bundle.io._wen_0,
            "waddr": bundle.io._waddr_0
        },
        bins={  
            "write_when_addr_0": lambda d: d["wen"].value == 1 and d["waddr"].value == 0,
            "write_when_addr_31": lambda d: d["wen"].value == 1 and d["waddr"].value == 31
        },
        name = "FtbEntryMem WritePort" 
    )
    return g

def create_coverage_groups(bundle: FtbEntryMemBundle, dut) -> list[CovGroup]:   
    read0_coverage = define_read0_coverage(bundle, dut)
    read1_coverage = define_read1_coverage(bundle, dut)
    write_coverage = define_write_coverage(bundle, dut)
    return [read0_coverage, read1_coverage, write_coverage]
