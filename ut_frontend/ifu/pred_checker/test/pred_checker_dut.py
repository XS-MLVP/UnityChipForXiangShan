import toffee_test
import toffee
from ..env import PredCheckerEnv
from ..bundle import PredCheckerBundle, _13Bundle
from dut.PredChecker import DUTPredChecker
import toffee.funcov as fc
from toffee.funcov import CovGroup

def pred_checker_cover_point(pred_checker):
    g = CovGroup("predChecker addition function")
    # g.add_cover_point(pred_checker.io_out_stage1Out_fixedRange_0, {"io_stage1Out_fixedRange is 0": fc.Eq(0)}, name="stage1Out0 is 0")
    return g
 

@toffee_test.fixture
async def predchecker_env(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(DUTPredChecker)
    toffee_request.add_cov_groups(pred_checker_cover_point(dut))
    dut.InitClock("clock")
    toffee.start_clock(dut)
    env = PredCheckerEnv(dut)
    return env