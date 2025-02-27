try:
    from UT_FtqPdMem import *
except:
    try:
        from FtqPdMem import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTFtqPdMem()
    # dut.init_clock("clk")

    dut.Step(1)

    dut.Finish()
