from toffee.funcov import CovGroup
from ..bundle import FtqPcMemBundle

def define_read_ifuPtr_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_IfuPtr")
    g.add_watch_point(
        {
            "ifuPtr": bundle.io._ifuPtr._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["ifuPtr"].value == 0,
            "read_when_addr_31": lambda d: d["ifuPtr"].value == 31
        },
        name="FtqPcMem Read IfuPtr"
    )
    return g

def define_read_ifuPtrPlus1_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_IfuPtrPlus1")
    g.add_watch_point(
        {
            "ifuPtrPlus1": bundle.io._ifuPtrPlus1._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["ifuPtrPlus1"].value == 0,
            "read_when_addr_31": lambda d: d["ifuPtrPlus1"].value == 31
        },
        name="FtqPcMem Read IfuPtrPlus1"
    )
    return g

def define_read_ifuPtrPlus2_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_IfuPtrPlus2")
    g.add_watch_point(
        {
            "ifuPtrPlus2": bundle.io._ifuPtrPlus2._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["ifuPtrPlus2"].value == 0,
            "read_when_addr_31": lambda d: d["ifuPtrPlus2"].value == 31
        },
        name="FtqPcMem Read IfuPtrPlus2"
    )
    return g

def define_read_pfPtr_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_PfPtr")
    g.add_watch_point(
        {
            "pfPtr": bundle.io._pfPtr._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["pfPtr"].value == 0,
            "read_when_addr_31": lambda d: d["pfPtr"].value == 31
        },
        name="FtqPcMem Read PfPtr"
    )
    return g

def define_read_pfPtrPlus1_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_PfPtrPlus1")
    g.add_watch_point(
        {
            "pfPtrPlus1": bundle.io._pfPtrPlus1._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["pfPtrPlus1"].value == 0,
            "read_when_addr_31": lambda d: d["pfPtrPlus1"].value == 31
        },
        name="FtqPcMem Read PfPtrPlus1"
    )
    return g

def define_read_commPtr_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_CommPtr")
    g.add_watch_point(
        {
            "commPtr": bundle.io._commPtr._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["commPtr"].value == 0,
            "read_when_addr_31": lambda d: d["commPtr"].value == 31
        },
        name="FtqPcMem Read CommPtr"
    )
    return g

def define_read_commPtrPlus1_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Read_CommPtrPlus1")
    g.add_watch_point(
        {
            "commPtrPlus1": bundle.io._commPtrPlus1._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["commPtrPlus1"].value == 0,
            "read_when_addr_31": lambda d: d["commPtrPlus1"].value == 31
        },
        name="FtqPcMem Read CommPtrPlus1"
    )
    return g

def define_write_port0_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("Write_Port0")
    g.add_watch_point(
        {
            "wen": bundle.io._wen._0,
            "waddr": bundle.io._waddr._0
        },
        bins={
            "write_when_addr_0": lambda d: d["wen"].value == 1 and d["waddr"].value == 0,
            "write_when_addr_31": lambda d: d["wen"].value == 1 and d["waddr"].value == 31
        },
        name="FtqPcMem Write Port0"
    )
    return g

def create_coverage_groups(bundle: FtqPcMemBundle, dut) -> list[CovGroup]:
    return [
        define_read_ifuPtr_coverage(bundle, dut),
        define_read_ifuPtrPlus1_coverage(bundle, dut),
        define_read_ifuPtrPlus2_coverage(bundle, dut),
        define_read_pfPtr_coverage(bundle, dut),
        define_read_pfPtrPlus1_coverage(bundle, dut),
        define_read_commPtr_coverage(bundle, dut),
        define_read_commPtrPlus1_coverage(bundle, dut),
        define_write_port0_coverage(bundle, dut),
    ]
