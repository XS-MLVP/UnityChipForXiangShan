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
import ctypes
import datetime
import toffee.funcov as fc

from dut.PreDecode import *
from dut.DecodeStage import *

from comm import get_out_dir, debug, UT_FCOV, get_version_checker, module_name_with
from dut.RVCExpander import *

from toffee_test.reporter import set_func_coverage
from toffee_test.reporter import set_line_coverage

# Set the toffe log level to ERROR
toffee.setup_logging(toffee.ERROR)

# Version check
version_check = get_version_checker("openxiangshan-kmh-*")

# Create a function coverage group: INT (Int instruction)
g = fc.CovGroup(UT_FCOV("../../../CLASSIC"))


def init_rvc_expander_funcov(expander, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""
    
    # 1. Add point RVC_EXPAND_RET to check expander return value:
    #    - bin ERROR. The instruction is not illegal
    #    - bin SUCCE. The instruction is not expanded
    g.add_watch_point(expander, {
                                "ERROR": lambda x: x.stat()["ilegal"] == False,
                                "SUCCE": lambda x: x.stat()["ilegal"] != False,
                          }, name = "RVC_EXPAND_RET")

    # 2. Add point RVC_EXPAND_16B_RANGE to check expander input range
    #   - bin RANGE[start-end]. The instruction is in the range of the compressed instruction set
    # This check point is added in case 'test_rv_decode.test_rvc_expand_16bit_full' dynamically, see the test case for details

    # 3. Add point RVC_EXPAND_32B_RANGE to check expander input range
    #   - bin RANGE[start-end]. The instruction is in the range of the 32bit instruction set
    # This check point is added in case 'test_rv_decode.test_rvc_expand_32bit_full' dynamically, see the test case for details

    # 4. Add point RVC_EXPAND_32B_BITS to check expander function coverage
    #   - bin BITS[0-31]. The instruction is expanded to the corresponding 32-bit instruction
    def _check_pos(i):
        def check(expander):
            return expander.stat()["instr"] & (1<<i) != 0
        return check
    g.add_watch_point(expander, {
                                  "POS_%d"%i: _check_pos(i)
                                   for i in range(32)
                                },
                      name="RVC_EXPAND_32B_BITS")

    # 5. Reverse mark function coverage to the check point
    def _M(name):
        # get the module name
        return module_name_with(name, "../../test_rv_decode")

    #  - mark RVC_EXPAND_RET
    g.mark_function("RVC_EXPAND_RET",     _M(["test_rvc_expand_16bit_full",
                                              "test_rvc_expand_32bit_full",
                                              "test_rvc_expand_32bit_randomN"]), bin_name=["ERROR", "SUCCE"])
    #  - mark RVC_EXPAND_16B_RANGE
    g.mark_function("RVC_EXPAND_32B_BITS", _M("test_rvc_expand_32bit_randomN"), bin_name=["POS_*"], raise_error=False)

    # The End
    return None


class RVCExpander(toffee.Bundle):
    def __init__(self, cover_group, **kwargs):
        super().__init__()
        self.cover_group = cover_group
        self.dut = DUTRVCExpander(**kwargs)
        self.io = toffee.Bundle.from_prefix("io_", self.dut)
        self.bind(self.dut)

    def expand(self, instr, fsIsOff):
        self.io["in"].value = instr
        self.io["fsIsOff"].value = fsIsOff
        self.dut.RefreshComb()
        self.cover_group.sample()
        return self.io["out_bits"].value, self.io["ill"].value
    
    def stat(self):
        return {
            "instr": self.io["in"].value,
            "decode": self.io["out_bits"].value,
            "ilegal": self.io["ill"].value != 0,
        }


@pytest.fixture()
def rvc_expander(request):
    version_check()
    fname = request.node.name
    wave_file = get_out_dir("decoder/rvc_expander_%s.fst" % fname)
    coverage_file = get_out_dir("decoder/rvc_expander_%s.dat" % fname)
    coverage_dir = os.path.dirname(coverage_file)
    os.makedirs(coverage_dir, exist_ok=True)
    expander = RVCExpander(g, coverage_filename=coverage_file, waveform_filename=wave_file)
    expander.dut.io_in.AsImmWrite()
    expander.dut.io_fsIsOff.AsImmWrite()
    init_rvc_expander_funcov(expander, g)
    yield expander
    expander.dut.Finish()
    set_line_coverage(request, coverage_file)
    set_func_coverage(request, g)
    g.clear()

# Filter out certain cases where exception can be identified through instruction itself, 
# Supplement with the exception detection situation of the reference model.
def instr_filter(insn_disasm_text):
    instr_opcode = insn_disasm_text.split(' ')[0]
    is_except = 0
    if (instr_opcode == "c.lwsp" or instr_opcode == "c.ldsp" or instr_opcode == "c.addiw"):
        dst = insn_disasm_text.split()[1].split(',')[0]
        if dst == "zero":
            is_except = 1
    elif (instr_opcode == "c.addi4spn"):
        imm = insn_disasm_text.split()[3]
        if imm == "0":
            is_except = 1
    elif (instr_opcode == "c.addi16sp"):
        imm = insn_disasm_text.split()[2]
        if imm == "0":
            is_except = 1
    elif (instr_opcode == "c.lui"):
        imm = insn_disasm_text.split()[2]
        if imm == "0x0":
            is_except = 1
    elif (instr_opcode == "c.jr"):
        rs1 = insn_disasm_text.split()[1]
        if rs1 == "zero":
            is_except = 1
    elif (instr_opcode == "c.unimp"):
        is_except = 1
    return is_except
