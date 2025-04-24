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

from .env import *
import inspect

### CASE EXAMPLE
# Running the following test case will show a pass:
def test_receive_ptw_resp_nonstage(tlb_fixture):
    """
    Func: TODO
        subfunc1: TODO
    """
    # connect to fixture
    tlb = tlb_fixture
    # add watch point
    # case_name = inspect.currentframe().f_back.f_code.co_name
    # g.add_watch_point(tlb.TODO, {
    #                     "TODO": fc.Eq(TODO),
    #                     "TODO": lambda TODO: TODO.value == TODO,
    # }, name = f"{case_name}: TODO")
    # set default value
    tlb.set_default_value()
    # reset
    tlb.reset()

    # add clock
    tlb.dut.xclock.StepRis(lambda _: g.sample())
    # start
    for _ in range(10000):
        # add signal and assign to dut

        # step to next cycle
        tlb.dut.Step(2)

        # assert result