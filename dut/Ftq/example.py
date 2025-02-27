try:
    from UT_Ftq import *
except:
    try:
        from Ftq import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTFtq()
    # dut.init_clock("clk")

    dut.Step(1)

    dut.Finish()
