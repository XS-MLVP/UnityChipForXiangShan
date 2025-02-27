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

Ftqsize = 64


# init the ref, and set each element in every entry to 0
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