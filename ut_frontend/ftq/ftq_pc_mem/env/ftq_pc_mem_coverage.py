import toffee.funcov as fc
from toffee.funcov import CovGroup
from ..bundle import FtqPcMemBundle

def define_read_ifuPtr_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadIfuPtr")
    g.add_watch_point(
        bundle.io._ifuPtr._w_value,
        {
            "read_when_addr_0": fc.CovEq(0),
            # "read_when_addr_31": fc.CovEq(31)
        },
        name="FtqPcMem Read IfuPtr"
    )
    return g

def define_read_ifuPtrPlus1_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadIfuPtrPlus1")
    g.add_watch_point(
        {
            "ifuPtrPlus1": bundle.io._ifuPtr.Plus1_w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["ifuPtrPlus1"].value == 0,
            # "read_when_addr_31": lambda d: d["ifuPtrPlus1"].value == 31
        },
        name="FtqPcMem Read IfuPtrPlus1"
    )
    return g

def define_read_ifuPtrPlus2_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadIfuPtrPlus2")
    g.add_watch_point(
        {
            "ifuPtrPlus2": bundle.io._ifuPtr.Plus2_w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["ifuPtrPlus2"].value == 0,
            # "read_when_addr_31": lambda d: d["ifuPtrPlus2"].value == 31
        },
        name="FtqPcMem Read IfuPtrPlus2"
    )
    return g

def define_read_pfPtr_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPfPtr")
    g.add_watch_point(
        {
            "pfPtr": bundle.io._pfPtr._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["pfPtr"].value == 0,
            # "read_when_addr_31": lambda d: d["pfPtr"].value == 31
        },
        name="FtqPcMem Read PfPtr"
    )
    return g

def define_read_pfPtrPlus1_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadPfPtrPlus1")
    g.add_watch_point(
        {
            "pfPtrPlus1": bundle.io._pfPtr.Plus1_w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["pfPtrPlus1"].value == 0,
            # "read_when_addr_31": lambda d: d["pfPtrPlus1"].value == 31
        },
        name="FtqPcMem Read PfPtrPlus1"
    )
    return g

def define_read_commPtr_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadCommPtr")
    g.add_watch_point(
        {
            "commPtr": bundle.io._commPtr._w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["commPtr"].value == 0,
            # "read_when_addr_31": lambda d: d["commPtr"].value == 31
        },
        name="FtqPcMem Read CommPtr"
    )
    return g

def define_read_commPtrPlus1_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("ReadCommPtrPlus1")
    g.add_watch_point(
        {
            "commPtrPlus1": bundle.io._commPtr.Plus1_w_value
        },
        bins={
            "read_when_addr_0": lambda d: d["commPtrPlus1"].value == 0,
            # "read_when_addr_31": lambda d: d["commPtrPlus1"].value == 31
        },
        name="FtqPcMem Read CommPtrPlus1"
    )
    return g

def define_write_port0_coverage(bundle: FtqPcMemBundle, dut) -> CovGroup:
    g = CovGroup("WritePort0")
    g.add_watch_point(
        {
            "wen": bundle.io._wen,
            "waddr": bundle.io._waddr
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
