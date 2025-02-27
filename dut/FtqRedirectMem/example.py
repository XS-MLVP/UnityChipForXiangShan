try:
    from UT_FtqRedirectMem import *
except:
    try:
        from FtqRedirectMem import *
    except:
        from __init__ import *
import random
 
#read 
def read(dut,ren_0):
    #read enable
    dut.io_ren_0.value = ren_0
 

    #input raddr
    dut.io_raddr_0 = random.randint(0,2**6-1)

    #
    dut.Step(1)
    return 
  

#reset
def reset(dut):
    dut.reset.value = 0
    dut.Step(1)
    dut.reset.value = 0
    dut.Step(7)




if __name__ == "__main__":
    
    #create dut
    dut = DUTFtqRedirectMem()

    #initialize 
    dut.InitClock("clock")
    dut.SetWaveform("test_redirect_mem.fst")
    
    
    # test clock
    dut.Step(3)
    dut.Finish()


    
    
    # #reset
    # reset(dut)

    # #test

    # ## write
    # dut.io_wen_0.value = 1
    # dut.io_waddr_0.value = 0
    # dut.io_wdata_0_histPtr_value.value = 16
    
    # ## read
    # # dut.io_ren_0.value = 1
    # # dut.io_raddr_0.value = 0
    # # dut.Step(1)
    # # print(dut.io_rdata_0_histPtr_value.value)

    # ## read
    # dut.io_ren_0.value = 1
    # dut.io_raddr_0.value = 0
    # dut.io_ren_1.value = 1
    # dut.io_raddr_1.value = 0
    
    # print(dut.io_rdata_0_histPtr_value.value)
    # dut.Step(1)
    # # dut.io_ren_0.value = 1
    # # dut.io_raddr_0.value = 0
    # dut.Step(1)
    # print(dut.io_rdata_0_histPtr_value.value)

    # ## write_new
    # dut.io_wen_0.value = 1
    # dut.io_waddr_0.value = 0
    # dut.io_wdata_0_histPtr_value.value = 32
    
    # dut.io_ren_0.value = 1
    # dut.io_raddr_0.value = 0
    # # dut.Step(1)
    # print(dut.io_rdata_0_histPtr_value.value)


    # dut.Step(1)
    # dut.io_ren_0.value = 1
    # dut.io_raddr_0.value = 0
    # # dut.Step(1)
    # print(dut.io_rdata_0_histPtr_value.value)


