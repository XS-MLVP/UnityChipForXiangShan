#coding=utf8
#***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
#**************************************************************************************/

import toffee
import os
import pytest
import random
from datetime import datetime
import toffee.funcov as fc

from dut.TLB import *
from ut_frontend.itlb.classical_version.env.itlb_utils import other_than
from .itlb_consts import *
from queue import Queue
from comm import get_version_checker, get_out_dir, UT_FCOV
from toffee_test.reporter import set_func_coverage, set_line_coverage

# Set the toffee log level to ERROR
toffee.setup_logging(toffee.ERROR)

# Version check
version_check = get_version_checker("openxiangshan-kmh-*")

# Create a function coverage group
g = fc.CovGroup(UT_FCOV("../../../CLASSIC"))

def init_itlb_funcov(tlb, g: fc.CovGroup):
    """
    Add watch points to collect function coverage
    """
    # TODO: add global watchpoint here
    g.add_watch_point(tlb.ctrl.io_ptw_req_0_valid, {
                            "invalid": fc.Eq(0),
                            "valid": fc.Eq(1),
                        }, name = "PTW_REQ_0_VALID_GLOBAL")
    g.add_watch_point(tlb.ctrl.io_ptw_req_1_valid, {
                            "invalid": fc.Eq(0),
                            "valid": fc.Eq(1),
                        }, name = "PTW_REQ_1_VALID_GLOBAL")
    g.add_watch_point(tlb.ptw_req_0.vpn, {
                            "zero": fc.Eq(0),
                        }, name = "PTW_REQ_0_VPN_IS_ZERO_GLOBAL")
    g.add_watch_point(tlb.ptw_req_0.vpn, {
                            "max": fc.Eq(2 ** 38 - 1),
                        }, name = "PTW_REQ_0_VPN_IS_MAX_GLOBAL")
    g.add_watch_point(tlb.ptw_req_1.vpn, {
                            "zero": fc.Eq(0),
                        }, name = "PTW_REQ_1_VPN_IS_ZERO_GLOBAL")
    g.add_watch_point(tlb.ptw_req_1.vpn, {
                            "max": fc.Eq(2 ** 38 - 1),
                        }, name = "PTW_REQ_1_VPN_IS_MAX_GLOBAL")

@pytest.fixture()
def tlb_fixture(request):
    version_check()
    test_name = request.node.name
    wave_file = get_out_dir("TLB_%s.fst" % test_name)
    coverage_file = get_out_dir("TLB_%s.dat" % test_name)
    coverage_dir = os.path.dirname(coverage_file)
    os.makedirs(coverage_dir, exist_ok=True)
    random.seed(datetime.now().timestamp() * 10000)
    v = 1919810 + random.randint(24, 114514)
    dut = DUTTLB(
        [f"+verilator+seed+{v}", ],
        waveform_filename=wave_file,
        coverage_filename=coverage_file)
    tlb = TLBWrapper(dut)
    init_itlb_funcov(tlb, g)
    
    yield tlb
    
    tlb.dut.Finish()
    set_line_coverage(request, coverage_file)
    set_func_coverage(request, g)
    g.clear()

class ControlBundle(toffee.Bundle):
    signals = [
        "reset",
        "io_sfence_valid",
        "io_hartId",
        "io_requestor_2_resp_ready",
        "io_requestor_2_resp_valid",
        "io_ptw_req_0_valid",
        "io_ptw_req_1_valid",
        "io_ptw_req_2_ready",
        "io_ptw_req_2_valid",
        "io_ptw_resp_valid",
        "io_ptw_resp_bits_s2xlate",
        "io_ptw_resp_bits_getGpa"
    ]

class CsrBundle(toffee.Bundle):
    def __init__(self, dut):
        super().__init__()
        self.satp  = toffee.Bundle.new_class_from_xport(dut.io_csr_satp ).from_prefix("io_csr_satp_" )
        self.vsatp = toffee.Bundle.new_class_from_xport(dut.io_csr_vsatp).from_prefix("io_csr_vsatp_")
        self.hgatp = toffee.Bundle.new_class_from_xport(dut.io_csr_hgatp).from_prefix("io_csr_hgatp_")
        self.priv  = toffee.Bundle.new_class_from_xport(dut.io_csr_priv ).from_prefix("io_csr_priv_" )

class Requestor_0_Bundle(toffee.Bundle):
    def __init__(self, dut):
        super().__init__()
        self.req = toffee.Bundle.new_class_from_xport(dut.io_requestor_0_req).from_prefix("io_requestor_0_req_")
        self.resp = toffee.Bundle.new_class_from_xport(dut.io_requestor_0_resp_bits).from_prefix("io_requestor_0_resp_bits_")

class Requestor_1_Bundle(toffee.Bundle):
    def __init__(self, dut):
        super().__init__()
        self.req = toffee.Bundle.new_class_from_xport(dut.io_requestor_1_req).from_prefix("io_requestor_1_req_")
        self.resp = toffee.Bundle.new_class_from_xport(dut.io_requestor_1_resp_bits).from_prefix("io_requestor_1_resp_bits_")

class Requestor_2_Bundle(toffee.Bundle):
    def __init__(self, dut):
        super().__init__()
        self.req = toffee.Bundle.new_class_from_xport(dut.io_requestor_2_req).from_prefix("io_requestor_2_req_")
        self.resp = toffee.Bundle.new_class_from_xport(dut.io_requestor_2_resp_bits).from_prefix("io_requestor_2_resp_bits_")

class TLBWrapper(toffee.Bundle):
    """
    Support full TLB I/O.
    """
    def __init__(self, dut: DUTTLB):
        super().__init__()
        self.dut = dut
        self.dut.InitClock("clock")
        # control
        self.ctrl = ControlBundle()
        self.ctrl.set_write_mode(toffee.WriteMode.Imme)
        self.ctrl.set_write_mode(toffee.WriteMode.Fall)
        # sfence
        self.sfence = toffee.Bundle.new_class_from_xport(dut.io_sfence_bits).from_prefix("io_sfence_bits_")
        # csr
        self.csr = CsrBundle(dut)
        # requestor
        self.requestor_0 = Requestor_0_Bundle(dut)
        self.requestor_1 = Requestor_1_Bundle(dut)
        self.requestor_2 = Requestor_2_Bundle(dut)
        # flushPipe
        for i in range(consts.Width):
            setattr(self, f"flushPipe_{i}", toffee.Bundle.from_prefix(f"io_flushPipe_{i}" , dut))
        self.flushPipe = [getattr(self, f"flushPipe_{i}") for i in range(consts.Width)]
        # ptw
        self.ptw_req_0 = toffee.Bundle.new_class_from_xport(dut.io_ptw_req_0_bits).from_prefix("io_ptw_req_0_bits_")
        self.ptw_req_1 = toffee.Bundle.new_class_from_xport(dut.io_ptw_req_1_bits).from_prefix("io_ptw_req_1_bits_")
        self.ptw_req_2 = toffee.Bundle.new_class_from_xport(dut.io_ptw_req_2_bits).from_prefix("io_ptw_req_2_bits_")
        self.ptw_resp_s1 = toffee.Bundle.new_class_from_xport(dut.io_ptw_resp_bits_s1).from_prefix("io_ptw_resp_bits_s1_")
        self.ptw_resp_s2 = toffee.Bundle.new_class_from_xport(dut.io_ptw_resp_bits_s2).from_prefix("io_ptw_resp_bits_s2_")
        # data queue
        self.data_to_drive = Queue()

        self.bind(self.dut)

    def connect_check(self):
        """
        Verify if the DUT interface signals are properly bound to the Python signal pins.
        """
        print("----------------------------- CONNECT CHECK -----------------------------")
        print(">>> unconnected signals  : ", self.detect_unconnected_signals(self.dut))
        print(">>> muticonnected signals: ", self.detect_multiple_connections(self.dut))
        specific_signal_name = "io_flushPipe_2"
        print(">>> specific connectivity check:", specific_signal_name, ":", self.detect_specific_connectivity(specific_signal_name, self.flushPipe[2]))
        print("-------------------------------------------------------------------------")

    def set_default_value(self):
        """
        To eliminate interference caused by randomly initialized signal values 
        at simulation startup, you must first zeroize all signals (set to 0) 
        before asserting the reset signal. This ensures clean initialization 
        of the module's internal state.
        """
    # sfence
        self.ctrl.io_sfence_valid.value = 0
        self.sfence.rs1.value = 0
        self.sfence.rs2.value = 0
        self.sfence.addr.value = 0
        self.sfence.id.value = 0
        self.sfence.flushPipe.value = 0
        self.sfence.hv.value = 0
        self.sfence.hg.value = 0
    # csr
        self.csr.satp.mode.value = 9
        self.csr.satp.asid.value = 0
        self.csr.satp.changed.value = 0
        self.csr.vsatp.mode.value = 0
        self.csr.vsatp.asid.value = 0
        self.csr.vsatp.changed.value = 0
        self.csr.hgatp.mode.value = 0
        self.csr.hgatp.vmid.value = 0
        self.csr.hgatp.changed.value = 0
        self.csr.priv.virt.value = 0
        self.csr.priv.imode.value = 0
    # requestor
        self.requestor_0.req.valid.value = 0
        self.requestor_0.req.bits_vaddr.value = 0
        self.requestor_1.req.valid.value = 0
        self.requestor_1.req.bits_vaddr.value = 0
        self.requestor_2.req.valid.value = 0
        self.requestor_2.req.bits_vaddr.value = 0
        self.ctrl.io_requestor_2_resp_ready.value = 1
    # flushPipe
        for i in range(consts.Width):
            self.flushPipe[i].value = 0     
    # ptw
        self.ctrl.io_ptw_req_2_ready.value = 1
        self.ctrl.io_ptw_resp_valid.value = 0
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0
        self.ptw_resp_s1.entry_tag.value = 0
        self.ptw_resp_s1.entry_asid.value = 0
        self.ptw_resp_s1.entry_vmid.value = 0
        self.ptw_resp_s1.entry_perm_d.value = 0
        self.ptw_resp_s1.entry_perm_a.value = 0
        self.ptw_resp_s1.entry_perm_g.value = 0
        self.ptw_resp_s1.entry_perm_u.value = 0
        self.ptw_resp_s1.entry_perm_x.value = 0
        self.ptw_resp_s1.entry_perm_w.value = 0
        self.ptw_resp_s1.entry_perm_r.value = 0
        self.ptw_resp_s1.entry_level.value = 0
        self.ptw_resp_s1.entry_ppn.value = 0
        self.ptw_resp_s1.addr_low.value = 0
        self.ptw_resp_s1.ppn_low_0.value = 0
        self.ptw_resp_s1.ppn_low_1.value = 0
        self.ptw_resp_s1.ppn_low_2.value = 0
        self.ptw_resp_s1.ppn_low_3.value = 0
        self.ptw_resp_s1.ppn_low_4.value = 0
        self.ptw_resp_s1.ppn_low_5.value = 0
        self.ptw_resp_s1.ppn_low_6.value = 0
        self.ptw_resp_s1.ppn_low_7.value = 0
        self.ptw_resp_s1.valididx_0.value = 0
        self.ptw_resp_s1.valididx_1.value = 0
        self.ptw_resp_s1.valididx_2.value = 0
        self.ptw_resp_s1.valididx_3.value = 0
        self.ptw_resp_s1.valididx_4.value = 0
        self.ptw_resp_s1.valididx_5.value = 0
        self.ptw_resp_s1.valididx_6.value = 0
        self.ptw_resp_s1.valididx_7.value = 0
        self.ptw_resp_s1.pteidx_0.value = 0
        self.ptw_resp_s1.pteidx_1.value = 0
        self.ptw_resp_s1.pteidx_2.value = 0
        self.ptw_resp_s1.pteidx_3.value = 0
        self.ptw_resp_s1.pteidx_4.value = 0
        self.ptw_resp_s1.pteidx_5.value = 0
        self.ptw_resp_s1.pteidx_6.value = 0
        self.ptw_resp_s1.pteidx_7.value = 0
        self.ptw_resp_s1.pf.value = 0
        self.ptw_resp_s1.af.value = 0
        self.ptw_resp_s2.entry_tag.value = 0
        self.ptw_resp_s2.entry_vmid.value = 0
        self.ptw_resp_s2.entry_ppn.value = 0
        self.ptw_resp_s2.entry_perm_d.value = 0
        self.ptw_resp_s2.entry_perm_a.value = 0
        self.ptw_resp_s2.entry_perm_g.value = 0
        self.ptw_resp_s2.entry_perm_u.value = 0
        self.ptw_resp_s2.entry_perm_x.value = 0
        self.ptw_resp_s2.entry_perm_w.value = 0
        self.ptw_resp_s2.entry_perm_r.value = 0
        self.ptw_resp_s2.entry_level.value = 0
        self.ptw_resp_s2.gpf.value = 0
        self.ptw_resp_s2.gaf.value = 0
        self.ctrl.io_ptw_resp_bits_getGpa.value = 0
        self.dut.Step(2)

####################### TLB Basic Function Start From Here #######################
    def reset(self):
        """
        reset
        """
        self.dut.reset.value = 1
        self.dut.Step(10)
        self.dut.reset.value = 0
        # print(">>> RESET FINISHED !")

    def cleanup_requestor(self, requestor: int):
        self.reset()
        self.flushPipe[requestor].value = 1
        self.dut.Step()
        self.flushPipe[requestor].value = 0
        self.dut.Step(2)
        # print(f">>> CLEANUP requestor_{i} FINISHED !")

    def gene_rand_TLBreq(self):
        """
        generate random TLB request
        """
        req_valid = random.choice([0, 1])
        req_vaddr = random.randint(0, 2 ** 50 - 1)
        return req_valid, req_vaddr

    def gene_rand_TLBsignal_batch(self) -> dict:
        vpn, offset = self.gene_rand_addr()
        asid = random.randint(0, 2 ** 16 - 1)
        ppn = random.randint(0, 2 ** 36 - 1)
        ppn_low = [random.randint(0, 2 ** 3 - 1) for _ in range(8)]
        valid_idx = [random.choice([0, 1]) for _ in range(8)]
        return {
            "asid": asid,
            "vpn": vpn,
            "offset": offset,
            "ppn": ppn,
            "ppn_low": ppn_low,
            "valid_idx": valid_idx,
        }

    def gene_rand_addr(self) -> tuple[int, int]:
        addr = random.randint(0, 2 ** 50 - 1)
        pn = addr >> 12
        offset = addr & 0xfff
        return pn, offset

    def rand_req0(self):
        """
        send random TLB request from requestor0
        """
        req_0_valid, req_0_vaddr = self.gene_rand_TLBreq()
        self.requestor_0.req.valid.value = req_0_valid
        self.requestor_0.req.bits_vaddr.value = req_0_vaddr
        return req_0_valid, req_0_vaddr

    def rand_req1(self):
        """
        send random TLB request from requestor1
        """
        req_1_valid, req_1_vaddr = self.gene_rand_TLBreq()
        self.requestor_1.req.valid.value = req_1_valid
        self.requestor_1.req.bits_vaddr.value = req_1_vaddr
        return req_1_valid, req_1_vaddr

    def rand_req2(self):
        """
        send random TLB request from requestor2
        """
        req_2_valid, req_2_vaddr = self.gene_rand_TLBreq()
        self.requestor_2.req.valid.value = req_2_valid
        self.requestor_2.req.bits_vaddr.value = req_2_vaddr
        return req_2_valid, req_2_vaddr

    def rand_req(self):
        """
        send random TLB request from all requestors
        """
        req_0_valid, req_0_vaddr = self.rand_req0()
        req_1_valid, req_1_vaddr = self.rand_req1()
        req_2_valid, req_2_vaddr = self.rand_req2()
        return req_0_valid, req_0_vaddr, req_1_valid, req_1_vaddr, req_2_valid, req_2_vaddr

    def rand_ptw_resp(self, vpn, asid, s2xlate):
        """
        generate random PTW response by s2xlate
        """
        # generate random input signals
        randPPN = random.randint(0, 2 ** 36 - 1)
        randValididx = [random.choice([0,1]) for _ in range(8)]
        randPPN_low = [random.randint(0, 2 ** 3 - 1) for _ in range(8)]

        addr_low = vpn & 0b111

        # assign to DUT
        ## ctrl signals
        self.ctrl.io_ptw_resp_valid.value = 1
        self.ctrl.io_ptw_resp_bits_s2xlate.value = s2xlate
        ## nos2xlate (s2xlate == 0b00)
        if (s2xlate == 0b00):
            self.ptw_resp_s1.entry_tag.value = vpn >> 3
            self.ptw_resp_s1.entry_asid.value = asid
            self.ptw_resp_s1.entry_vmid.value = DONTCARE
            self.ptw_resp_s1.entry_n.value = UNUSED0
            self.ptw_resp_s1.entry_pbmt.value = UNUSED0
            self.ptw_resp_s1.entry_perm_d.value = UNUSED0
            self.ptw_resp_s1.entry_perm_a.value = UNUSED0
            self.ptw_resp_s1.entry_perm_g.value = UNUSED0
            self.ptw_resp_s1.entry_perm_u.value = UNUSED0
            self.ptw_resp_s1.entry_perm_x.value = UNUSED1
            self.ptw_resp_s1.entry_perm_w.value = UNUSED0
            self.ptw_resp_s1.entry_perm_r.value = UNUSED0
            self.ptw_resp_s1.entry_level.value = UNUSED0
            self.ptw_resp_s1.entry_v.value = 1
            self.ptw_resp_s1.entry_ppn.value = randPPN >> 3
            self.ptw_resp_s1.addr_low.value = addr_low
            ppn_low_dict = {
                0: self.ptw_resp_s1.ppn_low_0,
                1: self.ptw_resp_s1.ppn_low_1,
                2: self.ptw_resp_s1.ppn_low_2,
                3: self.ptw_resp_s1.ppn_low_3,
                4: self.ptw_resp_s1.ppn_low_4,
                5: self.ptw_resp_s1.ppn_low_5,
                6: self.ptw_resp_s1.ppn_low_6,
                7: self.ptw_resp_s1.ppn_low_7
            }
            valididx_dict = {
                0: self.ptw_resp_s1.valididx_0,
                1: self.ptw_resp_s1.valididx_1,
                2: self.ptw_resp_s1.valididx_2,
                3: self.ptw_resp_s1.valididx_3,
                4: self.ptw_resp_s1.valididx_4,
                5: self.ptw_resp_s1.valididx_5,
                6: self.ptw_resp_s1.valididx_6,
                7: self.ptw_resp_s1.valididx_7
            }
            pteidx_dict = {
                0: self.ptw_resp_s1.pteidx_0,
                1: self.ptw_resp_s1.pteidx_1,
                2: self.ptw_resp_s1.pteidx_2,
                3: self.ptw_resp_s1.pteidx_3,
                4: self.ptw_resp_s1.pteidx_4,
                5: self.ptw_resp_s1.pteidx_5,
                6: self.ptw_resp_s1.pteidx_6,
                7: self.ptw_resp_s1.pteidx_7
            }
            for i in range(8):
                if i == addr_low:
                    ppn_low_dict[i].value = randPPN & 0b111
                    valididx_dict[i].value = 1
                else:
                    ppn_low_dict[i].value = randPPN_low[i]
                    valididx_dict[i].value = randValididx[i]
            pteidx_dict[addr_low].value = 1
            self.ptw_resp_s1.pf.value = UNUSED0
            self.ptw_resp_s1.af.value = UNUSED0
        ## OnlyStage1 (s2xlate == 0b01)
        elif (s2xlate == 0b01):
            self.ptw_resp_s1.entry_tag.value = vpn >> 12
            self.ptw_resp_s1.entry_asid.value = asid
            # TODO
        ## OnlyStage2 (s2xlate == 0b10)
        elif (s2xlate == 0b10):
            self.ptw_resp_s1.entry_tag.value = vpn >> 12
            self.ptw_resp_s1.entry_asid.value = asid
            # TODO
        ## AllStage (s2xlate == 0b11)
        else:
            self.ptw_resp_s1.entry_tag.value = vpn >> 12
            self.ptw_resp_s1.entry_asid.value = asid
            # TODO
        return randPPN

    def init_dut_for_nostage_hit(self, vpn, asid, ppn, ppn_low):
        # prepare data
        addr_low = vpn & 0b111
        ## ctrl signals
        self.ctrl.io_ptw_resp_valid.value = 1
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0b00
        # initialize conditions
        self.ptw_resp_s1.entry_tag.value = vpn >> 3
        self.ptw_resp_s1.entry_asid.value = asid
        self.ptw_resp_s1.entry_vmid.value = DONTCARE
        self.ptw_resp_s1.entry_n.value = UNUSED0
        self.ptw_resp_s1.entry_pbmt.value = UNUSED0
        self.ptw_resp_s1.entry_perm_d.value = UNUSED0
        self.ptw_resp_s1.entry_perm_a.value = UNUSED0
        self.ptw_resp_s1.entry_perm_g.value = UNUSED0
        self.ptw_resp_s1.entry_perm_u.value = UNUSED0
        self.ptw_resp_s1.entry_perm_x.value = UNUSED1
        self.ptw_resp_s1.entry_perm_w.value = UNUSED0
        self.ptw_resp_s1.entry_perm_r.value = UNUSED0
        self.ptw_resp_s1.entry_level.value = UNUSED0
        self.ptw_resp_s1.entry_v.value = 1
        self.ptw_resp_s1.entry_ppn.value = ppn >> 3
        self.ptw_resp_s1.addr_low.value = addr_low
        ppn_low_dict = {
            0: self.ptw_resp_s1.ppn_low_0,
            1: self.ptw_resp_s1.ppn_low_1,
            2: self.ptw_resp_s1.ppn_low_2,
            3: self.ptw_resp_s1.ppn_low_3,
            4: self.ptw_resp_s1.ppn_low_4,
            5: self.ptw_resp_s1.ppn_low_5,
            6: self.ptw_resp_s1.ppn_low_6,
            7: self.ptw_resp_s1.ppn_low_7
        }
        valididx_dict = {
            0: self.ptw_resp_s1.valididx_0,
            1: self.ptw_resp_s1.valididx_1,
            2: self.ptw_resp_s1.valididx_2,
            3: self.ptw_resp_s1.valididx_3,
            4: self.ptw_resp_s1.valididx_4,
            5: self.ptw_resp_s1.valididx_5,
            6: self.ptw_resp_s1.valididx_6,
            7: self.ptw_resp_s1.valididx_7
        }
        pteidx_dict = {
            0: self.ptw_resp_s1.pteidx_0,
            1: self.ptw_resp_s1.pteidx_1,
            2: self.ptw_resp_s1.pteidx_2,
            3: self.ptw_resp_s1.pteidx_3,
            4: self.ptw_resp_s1.pteidx_4,
            5: self.ptw_resp_s1.pteidx_5,
            6: self.ptw_resp_s1.pteidx_6,
            7: self.ptw_resp_s1.pteidx_7
        }
        for i in range(8):
            if i == addr_low:
                ppn_low_dict[i].value = ppn & 0b111
                valididx_dict[i].value = 1
            else:
                ppn_low_dict[i].value = ppn_low[i]
                valididx_dict[i].value = 0
        pteidx_dict[addr_low].value = 1
        self.ptw_resp_s1.pf.value = UNUSED0
        self.ptw_resp_s1.af.value = UNUSED0


    def init_dut_for_nostage_miss(self, vpn, asid, ppn, ppn_low):
        # prepare data
        addr_low = vpn & 0b111
        ## ctrl signals
        self.ctrl.io_ptw_resp_valid.value = 1
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0b00
        # initialize conditions
        self.ptw_resp_s1.entry_tag.value = other_than(vpn >> 3)
        self.ptw_resp_s1.entry_asid.value = asid
        self.ptw_resp_s1.entry_vmid.value = DONTCARE
        self.ptw_resp_s1.entry_n.value = UNUSED0
        self.ptw_resp_s1.entry_pbmt.value = UNUSED0
        self.ptw_resp_s1.entry_perm_d.value = UNUSED0
        self.ptw_resp_s1.entry_perm_a.value = UNUSED0
        self.ptw_resp_s1.entry_perm_g.value = UNUSED0
        self.ptw_resp_s1.entry_perm_u.value = UNUSED0
        self.ptw_resp_s1.entry_perm_x.value = UNUSED1
        self.ptw_resp_s1.entry_perm_w.value = UNUSED0
        self.ptw_resp_s1.entry_perm_r.value = UNUSED0
        self.ptw_resp_s1.entry_level.value = UNUSED0
        self.ptw_resp_s1.entry_v.value = 1
        self.ptw_resp_s1.entry_ppn.value = ppn >> 3
        self.ptw_resp_s1.addr_low.value = addr_low
        ppn_low_dict = {
            0: self.ptw_resp_s1.ppn_low_0,
            1: self.ptw_resp_s1.ppn_low_1,
            2: self.ptw_resp_s1.ppn_low_2,
            3: self.ptw_resp_s1.ppn_low_3,
            4: self.ptw_resp_s1.ppn_low_4,
            5: self.ptw_resp_s1.ppn_low_5,
            6: self.ptw_resp_s1.ppn_low_6,
            7: self.ptw_resp_s1.ppn_low_7
        }
        valididx_dict = {
            0: self.ptw_resp_s1.valididx_0,
            1: self.ptw_resp_s1.valididx_1,
            2: self.ptw_resp_s1.valididx_2,
            3: self.ptw_resp_s1.valididx_3,
            4: self.ptw_resp_s1.valididx_4,
            5: self.ptw_resp_s1.valididx_5,
            6: self.ptw_resp_s1.valididx_6,
            7: self.ptw_resp_s1.valididx_7
        }
        pteidx_dict = {
            0: self.ptw_resp_s1.pteidx_0,
            1: self.ptw_resp_s1.pteidx_1,
            2: self.ptw_resp_s1.pteidx_2,
            3: self.ptw_resp_s1.pteidx_3,
            4: self.ptw_resp_s1.pteidx_4,
            5: self.ptw_resp_s1.pteidx_5,
            6: self.ptw_resp_s1.pteidx_6,
            7: self.ptw_resp_s1.pteidx_7
        }
        for i in range(8):
            if i == addr_low:
                ppn_low_dict[i].value = ppn & 0b111
                valididx_dict[i].value = 1
            else:
                ppn_low_dict[i].value = ppn_low[i]
                valididx_dict[i].value = 0
        pteidx_dict[addr_low].value = 1
        self.ptw_resp_s1.pf.value = UNUSED0
        self.ptw_resp_s1.af.value = UNUSED0

    def init_dut_for_onlyStage1_miss(self, vpn, asid, ppn, ppn_low):
        # prepare data
        addr_low = vpn & 0b111
        ## ctrl signals
        self.ctrl.io_ptw_resp_valid.value = 1
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0b01
        # initialize conditions
        self.ptw_resp_s1.entry_tag.value = other_than(vpn >> 3)
        self.ptw_resp_s1.entry_asid.value = asid
        self.ptw_resp_s1.entry_vmid.value = DONTCARE
        self.ptw_resp_s1.entry_n.value = UNUSED0
        self.ptw_resp_s1.entry_pbmt.value = UNUSED0
        self.ptw_resp_s1.entry_perm_d.value = UNUSED0
        self.ptw_resp_s1.entry_perm_a.value = UNUSED0
        self.ptw_resp_s1.entry_perm_g.value = UNUSED0
        self.ptw_resp_s1.entry_perm_u.value = UNUSED0
        self.ptw_resp_s1.entry_perm_x.value = UNUSED1
        self.ptw_resp_s1.entry_perm_w.value = UNUSED0
        self.ptw_resp_s1.entry_perm_r.value = UNUSED0
        self.ptw_resp_s1.entry_level.value = UNUSED0
        self.ptw_resp_s1.entry_v.value = 1
        self.ptw_resp_s1.entry_ppn.value = ppn >> 3
        self.ptw_resp_s1.addr_low.value = addr_low
        ppn_low_dict = {
            0: self.ptw_resp_s1.ppn_low_0,
            1: self.ptw_resp_s1.ppn_low_1,
            2: self.ptw_resp_s1.ppn_low_2,
            3: self.ptw_resp_s1.ppn_low_3,
            4: self.ptw_resp_s1.ppn_low_4,
            5: self.ptw_resp_s1.ppn_low_5,
            6: self.ptw_resp_s1.ppn_low_6,
            7: self.ptw_resp_s1.ppn_low_7
        }
        valididx_dict = {
            0: self.ptw_resp_s1.valididx_0,
            1: self.ptw_resp_s1.valididx_1,
            2: self.ptw_resp_s1.valididx_2,
            3: self.ptw_resp_s1.valididx_3,
            4: self.ptw_resp_s1.valididx_4,
            5: self.ptw_resp_s1.valididx_5,
            6: self.ptw_resp_s1.valididx_6,
            7: self.ptw_resp_s1.valididx_7
        }
        pteidx_dict = {
            0: self.ptw_resp_s1.pteidx_0,
            1: self.ptw_resp_s1.pteidx_1,
            2: self.ptw_resp_s1.pteidx_2,
            3: self.ptw_resp_s1.pteidx_3,
            4: self.ptw_resp_s1.pteidx_4,
            5: self.ptw_resp_s1.pteidx_5,
            6: self.ptw_resp_s1.pteidx_6,
            7: self.ptw_resp_s1.pteidx_7
        }
        for i in range(8):
            if i == addr_low:
                ppn_low_dict[i].value = ppn & 0b111
                valididx_dict[i].value = 1
            else:
                ppn_low_dict[i].value = ppn_low[i]
                valididx_dict[i].value = 0
        pteidx_dict[addr_low].value = 1
        self.ptw_resp_s1.pf.value = UNUSED0
        self.ptw_resp_s1.af.value = UNUSED0

    def init_dut_for_onlyStage2_miss(self, vpn, asid, ppn, ppn_low):
        # prepare data
        addr_low = vpn & 0b111
        ## ctrl signals
        self.ctrl.io_ptw_resp_valid.value = 1
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0b10
        # initialize conditions
        self.ptw_resp_s1.entry_tag.value = other_than(vpn >> 3)
        self.ptw_resp_s1.entry_asid.value = asid
        self.ptw_resp_s1.entry_vmid.value = DONTCARE
        self.ptw_resp_s1.entry_n.value = UNUSED0
        self.ptw_resp_s1.entry_pbmt.value = UNUSED0
        self.ptw_resp_s1.entry_perm_d.value = UNUSED0
        self.ptw_resp_s1.entry_perm_a.value = UNUSED0
        self.ptw_resp_s1.entry_perm_g.value = UNUSED0
        self.ptw_resp_s1.entry_perm_u.value = UNUSED0
        self.ptw_resp_s1.entry_perm_x.value = UNUSED1
        self.ptw_resp_s1.entry_perm_w.value = UNUSED0
        self.ptw_resp_s1.entry_perm_r.value = UNUSED0
        self.ptw_resp_s1.entry_level.value = UNUSED0
        self.ptw_resp_s1.entry_v.value = 1
        self.ptw_resp_s1.entry_ppn.value = ppn >> 3
        self.ptw_resp_s1.addr_low.value = addr_low
        ppn_low_dict = {
            0: self.ptw_resp_s1.ppn_low_0,
            1: self.ptw_resp_s1.ppn_low_1,
            2: self.ptw_resp_s1.ppn_low_2,
            3: self.ptw_resp_s1.ppn_low_3,
            4: self.ptw_resp_s1.ppn_low_4,
            5: self.ptw_resp_s1.ppn_low_5,
            6: self.ptw_resp_s1.ppn_low_6,
            7: self.ptw_resp_s1.ppn_low_7
        }
        valididx_dict = {
            0: self.ptw_resp_s1.valididx_0,
            1: self.ptw_resp_s1.valididx_1,
            2: self.ptw_resp_s1.valididx_2,
            3: self.ptw_resp_s1.valididx_3,
            4: self.ptw_resp_s1.valididx_4,
            5: self.ptw_resp_s1.valididx_5,
            6: self.ptw_resp_s1.valididx_6,
            7: self.ptw_resp_s1.valididx_7
        }
        pteidx_dict = {
            0: self.ptw_resp_s1.pteidx_0,
            1: self.ptw_resp_s1.pteidx_1,
            2: self.ptw_resp_s1.pteidx_2,
            3: self.ptw_resp_s1.pteidx_3,
            4: self.ptw_resp_s1.pteidx_4,
            5: self.ptw_resp_s1.pteidx_5,
            6: self.ptw_resp_s1.pteidx_6,
            7: self.ptw_resp_s1.pteidx_7
        }
        for i in range(8):
            if i == addr_low:
                ppn_low_dict[i].value = ppn & 0b111
                valididx_dict[i].value = 1
            else:
                ppn_low_dict[i].value = ppn_low[i]
                valididx_dict[i].value = 0
        pteidx_dict[addr_low].value = 1
        self.ptw_resp_s1.pf.value = UNUSED0
        self.ptw_resp_s1.af.value = UNUSED0

    def init_dut_for_allStage_miss(self, vpn, asid, ppn, ppn_low):
        # prepare data
        addr_low = vpn & 0b111
        ## ctrl signals
        self.ctrl.io_ptw_resp_valid.value = 1
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0b11
        # initialize conditions
        self.ptw_resp_s1.entry_tag.value = other_than(vpn >> 3)
        self.ptw_resp_s1.entry_asid.value = asid
        self.ptw_resp_s1.entry_vmid.value = DONTCARE
        self.ptw_resp_s1.entry_n.value = UNUSED0
        self.ptw_resp_s1.entry_pbmt.value = UNUSED0
        self.ptw_resp_s1.entry_perm_d.value = UNUSED0
        self.ptw_resp_s1.entry_perm_a.value = UNUSED0
        self.ptw_resp_s1.entry_perm_g.value = UNUSED0
        self.ptw_resp_s1.entry_perm_u.value = UNUSED0
        self.ptw_resp_s1.entry_perm_x.value = UNUSED1
        self.ptw_resp_s1.entry_perm_w.value = UNUSED0
        self.ptw_resp_s1.entry_perm_r.value = UNUSED0
        self.ptw_resp_s1.entry_level.value = UNUSED0
        self.ptw_resp_s1.entry_v.value = 1
        self.ptw_resp_s1.entry_ppn.value = ppn >> 3
        self.ptw_resp_s1.addr_low.value = addr_low
        ppn_low_dict = {
            0: self.ptw_resp_s1.ppn_low_0,
            1: self.ptw_resp_s1.ppn_low_1,
            2: self.ptw_resp_s1.ppn_low_2,
            3: self.ptw_resp_s1.ppn_low_3,
            4: self.ptw_resp_s1.ppn_low_4,
            5: self.ptw_resp_s1.ppn_low_5,
            6: self.ptw_resp_s1.ppn_low_6,
            7: self.ptw_resp_s1.ppn_low_7
        }
        valididx_dict = {
            0: self.ptw_resp_s1.valididx_0,
            1: self.ptw_resp_s1.valididx_1,
            2: self.ptw_resp_s1.valididx_2,
            3: self.ptw_resp_s1.valididx_3,
            4: self.ptw_resp_s1.valididx_4,
            5: self.ptw_resp_s1.valididx_5,
            6: self.ptw_resp_s1.valididx_6,
            7: self.ptw_resp_s1.valididx_7
        }
        pteidx_dict = {
            0: self.ptw_resp_s1.pteidx_0,
            1: self.ptw_resp_s1.pteidx_1,
            2: self.ptw_resp_s1.pteidx_2,
            3: self.ptw_resp_s1.pteidx_3,
            4: self.ptw_resp_s1.pteidx_4,
            5: self.ptw_resp_s1.pteidx_5,
            6: self.ptw_resp_s1.pteidx_6,
            7: self.ptw_resp_s1.pteidx_7
        }
        for i in range(8):
            if i == addr_low:
                ppn_low_dict[i].value = ppn & 0b111
                valididx_dict[i].value = 1
            else:
                ppn_low_dict[i].value = ppn_low[i]
                valididx_dict[i].value = 0
        pteidx_dict[addr_low].value = 1
        self.ptw_resp_s1.pf.value = UNUSED0
        self.ptw_resp_s1.af.value = UNUSED0


class TLBrwWrapper(toffee.Bundle):
    """
    Support TLB read/write only.
    """
    def __init__(self, dut: DUTTLB):
        super().__init__()
        self.dut = dut
        self.dut.InitClock("clock")
        # control
        self.ctrl = ControlBundle()
        self.ctrl.set_write_mode(toffee.WriteMode.Imme)
        self.ctrl.set_write_mode(toffee.WriteMode.Fall)
        # requestor
        self.requestor_0 = Requestor_0_Bundle(dut)
        self.requestor_1 = Requestor_1_Bundle(dut)
        self.requestor_2 = Requestor_2_Bundle(dut)
        # ptw
        self.ptw_req_0 = toffee.Bundle.new_class_from_xport(dut.io_ptw_req_0_bits).from_prefix("io_ptw_req_0_bits_")
        self.ptw_req_1 = toffee.Bundle.new_class_from_xport(dut.io_ptw_req_1_bits).from_prefix("io_ptw_req_1_bits_")
        self.ptw_req_2 = toffee.Bundle.new_class_from_xport(dut.io_ptw_req_2_bits).from_prefix("io_ptw_req_2_bits_")
        self.ptw_resp_s1 = toffee.Bundle.new_class_from_xport(dut.io_ptw_resp_bits_s1).from_prefix("io_ptw_resp_bits_s1_")
        self.ptw_resp_s2 = toffee.Bundle.new_class_from_xport(dut.io_ptw_resp_bits_s2).from_prefix("io_ptw_resp_bits_s2_")

        self.bind(self.dut)

    def set_default_value(self):
    # requestor
        self.requestor_0.req.valid.value = 0
        self.requestor_0.req.bits_vaddr.value = 0
        self.requestor_1.req.valid.value = 0
        self.requestor_1.req.bits_vaddr.value = 0
        self.requestor_2.req.valid.value = 0
        self.requestor_2.req.bits_vaddr.value = 0
        self.ctrl.io_requestor_2_resp_ready.value = 0
    # ptw
        self.ctrl.io_ptw_req_2_ready.value = 0
        self.ctrl.io_ptw_resp_valid.value = 0
        self.ctrl.io_ptw_resp_bits_s2xlate.value = 0
        self.ptw_resp_s1.entry_tag.value = 0
        self.ptw_resp_s1.entry_asid.value = 0
        self.ptw_resp_s1.entry_vmid.value = 0
        self.ptw_resp_s1.entry_perm_d.value = 0
        self.ptw_resp_s1.entry_perm_a.value = 0
        self.ptw_resp_s1.entry_perm_g.value = 0
        self.ptw_resp_s1.entry_perm_u.value = 0
        self.ptw_resp_s1.entry_perm_x.value = 0
        self.ptw_resp_s1.entry_perm_w.value = 0
        self.ptw_resp_s1.entry_perm_r.value = 0
        self.ptw_resp_s1.entry_level.value = 0
        self.ptw_resp_s1.entry_ppn.value = 0
        self.ptw_resp_s1.addr_low.value = 0
        self.ptw_resp_s1.ppn_low_0.value = 0
        self.ptw_resp_s1.ppn_low_1.value = 0
        self.ptw_resp_s1.ppn_low_2.value = 0
        self.ptw_resp_s1.ppn_low_3.value = 0
        self.ptw_resp_s1.ppn_low_4.value = 0
        self.ptw_resp_s1.ppn_low_5.value = 0
        self.ptw_resp_s1.ppn_low_6.value = 0
        self.ptw_resp_s1.ppn_low_7.value = 0
        self.ptw_resp_s1.valididx_0.value = 0
        self.ptw_resp_s1.valididx_1.value = 0
        self.ptw_resp_s1.valididx_2.value = 0
        self.ptw_resp_s1.valididx_3.value = 0
        self.ptw_resp_s1.valididx_4.value = 0
        self.ptw_resp_s1.valididx_5.value = 0
        self.ptw_resp_s1.valididx_6.value = 0
        self.ptw_resp_s1.valididx_7.value = 0
        self.ptw_resp_s1.pteidx_0.value = 0
        self.ptw_resp_s1.pteidx_1.value = 0
        self.ptw_resp_s1.pteidx_2.value = 0
        self.ptw_resp_s1.pteidx_3.value = 0
        self.ptw_resp_s1.pteidx_4.value = 0
        self.ptw_resp_s1.pteidx_5.value = 0
        self.ptw_resp_s1.pteidx_6.value = 0
        self.ptw_resp_s1.pteidx_7.value = 0
        self.ptw_resp_s1.pf.value = 0
        self.ptw_resp_s1.af.value = 0
        self.ptw_resp_s2.entry_tag.value = 0
        self.ptw_resp_s2.entry_vmid.value = 0
        self.ptw_resp_s2.entry_ppn.value = 0
        self.ptw_resp_s2.entry_perm_d.value = 0
        self.ptw_resp_s2.entry_perm_a.value = 0
        self.ptw_resp_s2.entry_perm_g.value = 0
        self.ptw_resp_s2.entry_perm_u.value = 0
        self.ptw_resp_s2.entry_perm_x.value = 0
        self.ptw_resp_s2.entry_perm_w.value = 0
        self.ptw_resp_s2.entry_perm_r.value = 0
        self.ptw_resp_s2.entry_level.value = 0
        self.ptw_resp_s2.gpf.value = 0
        self.ptw_resp_s2.gaf.value = 0
        self.ctrl.io_ptw_resp_bits_getGpa.value = 0

    def reset(self):
        self.dut.reset.value = 0
        self.dut.Step(2)
        self.dut.reset.value = 1
        self.dut.Step(10)
        self.dut.reset.value = 0
        self.dut.Step(2)
        # print(">>> RESET FINISHED !")
