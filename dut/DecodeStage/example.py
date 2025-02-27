try:
    from UT_DecodeStage import *
except:
    try:
        from DecodeStage import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTDecodeStage()
    # dut.init_clock("clk")

    dut.Step(1)

    dut.Finish()
