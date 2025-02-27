try:
    from UT_FtqRedirectMem import *
except:
    try:
        from FtqRedirectMem import *
    except:
        from __init__ import *
import random
import pytest
import time

FtqSize = 64

last_read = []

# set write mode
def set_write_mode_imm(dut):
    dut.io_wen_0.AsImmWrite()
    dut.io_waddr_0.AsImmWrite()
    dut.io_wdata_0_histPtr_flag.AsImmWrite()
    dut.io_wdata_0_histPtr_value.AsImmWrite()
    dut.io_wdata_0_ssp.AsImmWrite()
    dut.io_wdata_0_sctr.AsImmWrite()
    dut.io_wdata_0_TOSW_flag.AsImmWrite()
    dut.io_wdata_0_TOSW_value.AsImmWrite()
    dut.io_wdata_0_TOSR_flag.AsImmWrite()
    dut.io_wdata_0_TOSR_value.AsImmWrite()
    dut.io_wdata_0_NOS_flag.AsImmWrite()
    dut.io_wdata_0_NOS_value.AsImmWrite()
    dut.io_wdata_0_topAddr.AsImmWrite()
    dut.io_ren_0.AsImmWrite()
    dut.io_ren_1.AsImmWrite()
    dut.io_ren_2.AsImmWrite()




@pytest.fixture()
def init_ref():
    #initialize the ref
    print("init ref")
    FtqRedirectMem = []
    FtqRedirectMem_entry = {
        "histPtr_flag": 0,
        "histPtr_value": 0,
        "ssp": 0,
        "sctr": 0,
        "TOSW_flag": 0,
        "TOSW_value": 0,
        "TOSR_flag": 0,
        "TOSR_value": 0,
        "NOS_flag": 0,
        "NOS_value": 0,
        "topAddr": 0
    }
    global FtqSize
    for i in range(FtqSize):
        FtqRedirectMem.append(FtqRedirectMem_entry.copy())

    # init_ref_read(FtqRedirectMem)

    return FtqRedirectMem

@pytest.fixture()
def init_dut():
    # initialize the dut
    print("init dut")
    dut = DUTFtqRedirectMem()
    
    # init clock, set wave
    dut.InitClock("clock")
    dut.SetWaveform("test_random.fst")

    # set_write mode
    set_write_mode_imm(dut)

    FtqRedirectMem_entry = {
        "histPtr_flag": 0,
        "histPtr_value": 0,
        "ssp": 0,
        "sctr": 0,
        "TOSW_flag": 0,
        "TOSW_value": 0,
        "TOSR_flag": 0,
        "TOSR_value": 0,
        "NOS_flag": 0,
        "NOS_value": 0,
        "topAddr": 0
    }
    global FtqSize
    for i in range(FtqSize):
        dut.Step(1)
        write_dut(dut=dut,wen=1,waddr=i,wdata=FtqRedirectMem_entry)
        
    return dut



def reset_dut(dut):
    dut.Step(1)
    dut.reset.value = 0
    dut.Step(1)

def init_ref_last_read():
    rdatas = []
    rdata_0 = {}
    rdata_1 = {}
    rdata_2 = {}
    rdatas.extend([rdata_0,rdata_1,rdata_2])
    rdata_0["histPtr_flag"] = 0
    rdata_0["histPtr_value"] = 0
    rdata_0["ssp"] = 0
    rdata_0["sctr"] = 0
    rdata_0["TOSW_flag"] = 0
    rdata_0["TOSW_value"] = 0
    rdata_0["TOSR_flag"] = 0
    rdata_0["TOSR_value"] = 0
    rdata_0["NOS_flag"] = 0
    rdata_0["NOS_value"] = 0
    rdata_0["topAddr"] = 0

    rdata_1["histPtr_flag"] = 0
    rdata_1["histPtr_value"] = 0
    rdata_1["ssp"] = 0
    rdata_1["sctr"] = 0
    rdata_1["TOSW_flag"] = 0
    rdata_1["TOSW_value"] = 0
    rdata_1["TOSR_flag"] = 0
    rdata_1["TOSR_value"] = 0
    rdata_1["NOS_flag"] = 0
    rdata_1["NOS_value"] = 0

    rdata_2["histPtr_value"] = 0

    global last_read
    last_read = rdatas

def write_dut(dut, wen, wdata, waddr):
        dut.io_wen_0.value = wen
        dut.io_waddr_0.value = waddr
        dut.io_wdata_0_histPtr_flag.value = wdata["histPtr_flag"]
        dut.io_wdata_0_histPtr_value.value = wdata["histPtr_value"]
        dut.io_wdata_0_ssp.value = wdata["ssp"]
        dut.io_wdata_0_sctr.value = wdata["sctr"]
        dut.io_wdata_0_TOSW_flag.value = wdata["TOSW_flag"]
        dut.io_wdata_0_TOSW_value.value = wdata["TOSW_value"]
        dut.io_wdata_0_TOSR_flag.value = wdata["TOSR_flag"]
        dut.io_wdata_0_TOSR_value.value = wdata["TOSR_value"]
        dut.io_wdata_0_NOS_flag.value = wdata["NOS_flag"]
        dut.io_wdata_0_NOS_value.value = wdata["NOS_value"]
        dut.io_wdata_0_topAddr.value = wdata["topAddr"]
        
        dut.Step(1)

def write_ref(ref, wen, wdata, waddr):
    if(wen):
        ref[waddr] = wdata
    # print("wirte data:",ref[waddr])
    # print("wirte addr:",waddr)

# must reset, it make sure that the last_read's element is given keys
def read_dut(dut, ren, raddr):
    rdatas = []
    rdata_0 = {}
    rdata_1 = {}
    rdata_2 = {}
    
    #set ren
    dut.io_ren_0.value = ren[0]
    dut.io_ren_1.value = ren[1]
    dut.io_ren_2.value = ren[2]
    #input addr
    dut.io_raddr_0.value = raddr[0]
    dut.io_raddr_1.value = raddr[1]
    dut.io_raddr_2.value = raddr[2]
    
    dut.Step(2)## some problem

    # get result

    rdata_0["histPtr_flag"] = dut.io_rdata_0_histPtr_flag.value
    rdata_0["histPtr_value"] = dut.io_rdata_0_histPtr_value.value
    rdata_0["ssp"] = dut.io_rdata_0_ssp.value
    rdata_0["sctr"] = dut.io_rdata_0_sctr.value
    rdata_0["TOSW_flag"] = dut.io_rdata_0_TOSW_flag.value
    rdata_0["TOSW_value"] = dut.io_rdata_0_TOSW_value.value
    rdata_0["TOSR_flag"] = dut.io_rdata_0_TOSR_flag.value
    rdata_0["TOSR_value"] = dut.io_rdata_0_TOSR_value.value
    rdata_0["NOS_flag"] = dut.io_rdata_0_NOS_flag.value
    rdata_0["NOS_value"] = dut.io_rdata_0_NOS_value.value
    rdata_0["topAddr"] = dut.io_rdata_0_topAddr.value

  
    rdata_1["histPtr_flag"] = dut.io_rdata_1_histPtr_flag.value
    rdata_1["histPtr_value"] = dut.io_rdata_1_histPtr_value.value
    rdata_1["ssp"] = dut.io_rdata_1_ssp.value
    rdata_1["sctr"] = dut.io_rdata_1_sctr.value
    rdata_1["TOSW_flag"] = dut.io_rdata_1_TOSW_flag.value
    rdata_1["TOSW_value"] = dut.io_rdata_1_TOSW_value.value
    rdata_1["TOSR_flag"] = dut.io_rdata_1_TOSR_flag.value
    rdata_1["TOSR_value"] = dut.io_rdata_1_TOSR_value.value
    rdata_1["NOS_flag"] = dut.io_rdata_1_NOS_flag.value
    rdata_1["NOS_value"] = dut.io_rdata_1_NOS_value.value
    # no top Addr
    #rdata_1["topAddr"] = dut.io_rdata_1_topAddr.value

    # only histptr
    rdata_2["histPtr_value"] = dut.io_rdata_2_histPtr_value.value


    rdatas.append(rdata_0)
    rdatas.append(rdata_1)    
    rdatas.append(rdata_2)
    return rdatas

def read_ref(ref,ren,raddr):
    global last_read
    rdatas = last_read
    for i in range(3):
        if(ren[i]):
            for key in rdatas[i]:
                    rdatas[i][key] = ref[raddr[i]][key]
    last_read = rdatas
    return rdatas

def test_random(init_ref, init_dut):
    # get init
    ref = init_ref
    dut = init_dut
    
    init_ref_last_read()

    for i in range(20000):
        print("round:",i)  
        # genarate random wdata
        wdata = {
            "histPtr_flag": random.randint(0,1),
            "histPtr_value": random.randint(0,2**8-1),
            "ssp": random.randint(0,2**4-1),
            "sctr": random.randint(0,2**3-1),
            "TOSW_flag": random.randint(0,1),
            "TOSW_value": random.randint(0,2**5-1),
            "TOSR_flag": random.randint(0,1),
            "TOSR_value": random.randint(0,2**5-1),
            "NOS_flag": random.randint(0,1),
            "NOS_value": random.randint(0,2**5-1),
            "topAddr": random.randint(0,2**50-1),
        }

        dut.io_wen_0.value = 0
        dut.Step(1)

        #write
        wen = random.randint(0,1)
        global FtqSize
        waddr = random.randint(0,FtqSize - 1)
        # print("waddr:",waddr)
        write_dut(dut, wen, wdata, waddr)
        write_ref(ref, wen, wdata, waddr)

        #read  
        ren = [random.randint(0, 1) for i in range(3)]
        raddr = [random.randint(0, FtqSize-1) for i in range(3)]
        read_dut_result = read_dut(dut=dut, ren=ren, raddr=raddr)
        read_ref_result = read_ref(ref=ref, ren=ren, raddr=raddr)

        # test
        # print("dut ren:", dut.io_ren_0.value,dut.io_ren_1.value,dut.io_ren_2.value)
        # print(read_dut_result)
        # print(ref[raddr[0]])
        if ren[0] == 1:
            assert read_dut_result[0] == read_ref_result[0], "read mismatch for port 0"
        if ren[1] == 1:
            assert read_dut_result[1] == read_ref_result[1], "read mismatch for port 1"
        if ren[2] == 1:
            assert read_dut_result[2] == read_ref_result[2], "read mismatch for port 2"
    # test
    print("Test Passed")
    dut.Finish()