################################################################################
# hit
################################################################################

def hit_nonStage_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_0.resp.miss.value == 0)


def hit_nonStage_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_1.resp.miss.value == 0)


def hit_nonStage_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_hit(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.paddr_0.value == ((signals["ppn"] << 12) | signals["offset"]))
    assert (tlb.requestor_2.resp.miss.value == 0)


################################################################################
# miss
################################################################################

# no stage
def miss_nonStage_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.miss.value == 1)


def miss_nonStage_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.miss.value == 1)


def miss_nonStage_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_nostage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.miss.value == 1)


# only stage 1
def miss_onlyStage1_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_onlyStage1_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.miss.value == 1)


def miss_onlyStage1_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_onlyStage1_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.miss.value == 1)


def miss_onlyStage1_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_onlyStage1_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.miss.value == 1)


# only stage 2
def miss_onlyStage2_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_onlyStage2_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.miss.value == 1)


def miss_onlyStage2_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_onlyStage2_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.miss.value == 1)


def miss_onlyStage2_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_onlyStage2_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.miss.value == 1)


# all stage
def miss_allStage_requestor_0(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_allStage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 1
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_0.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_0.resp.miss.value == 1)


def miss_allStage_requestor_1(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_allStage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 1
    tlb.requestor_2.req.valid.value = 0
    tlb.requestor_1.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_1.resp.miss.value == 1)


def miss_allStage_requestor_2(tlb):
    # generate signals
    signals = tlb.gene_rand_TLBsignal_batch()
    # initialize dut with signals
    tlb.init_dut_for_allStage_miss(signals["vpn"], signals["asid"], signals["ppn"], signals["ppn_low"])
    tlb.csr.satp.asid.value = signals["asid"]
    # step to next cycle
    tlb.dut.Step()
    # switch requestor
    tlb.requestor_0.req.valid.value = 0
    tlb.requestor_1.req.valid.value = 0
    tlb.requestor_2.req.valid.value = 1
    tlb.ctrl.io_requestor_2_resp_ready.value = 1
    tlb.requestor_2.req.bits_vaddr.value = (signals["vpn"] << 12) | signals["offset"]
    # step to next cycle
    tlb.dut.Step(2)
    # assert result
    assert (tlb.requestor_2.resp.miss.value == 1)
