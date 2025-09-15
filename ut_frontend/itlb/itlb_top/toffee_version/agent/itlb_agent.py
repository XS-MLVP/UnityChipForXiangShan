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

from toffee.agent import *

class Requestor0_Agent(Agent):
    @driver_method()
    async def input(self, req_valid, req_vaddr, n_cycle=1):
        self.dut.requestor[0].req.valid.value = req_valid
        self.dut.requestor[0].req.vaddr.value = req_vaddr
        await self.dut.step(n_cycle)
        resp_paddr = self.dut.requestor[0].resp.paddr.value
        resp_gpaddr = self.dut.requestor[0].resp.gpaddr.value
        resp_pbmt = self.dut.requestor[0].resp.pbmt.value
        resp_miss = self.dut.requestor[0].resp.miss.value
        resp_isForVSnonLeafPTE = self.dut.requestor[0].resp.isForVSnonLeafPTE.value
        resp_gpf = self.dut.requestor[0].resp.gpf.value
        resp_pf = self.dut.requestor[0].resp.pf.value
        resp_af = self.dut.requestor[0].resp.af.value
        return (resp_paddr, resp_gpaddr, resp_pbmt, resp_miss, resp_isForVSnonLeafPTE, resp_gpf, resp_pf, resp_af)