import toffee_test
import toffee
from comm.functions import module_name_with
from dut.FrontendTrigger import DUTFrontendTrigger
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_ref import (
    BpRefModel,
)
from comm.functions import UT_FCOV, module_name_with
import toffee.funcov as fc


from ..env import FrontendTriggerEnv


gr = fc.CovGroup(UT_FCOV("../../TOFFEE"), disable_sample_when_point_hinted=False)


def init_frontend_trigger_funcov(dut: DUTFrontendTrigger, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""

    for i in range(16):
        g.add_watch_point(
            dut,
            {
                "BKPT_EXCPT": lambda d: getattr(dut, f"io_triggered_{i}").value == 0,
                "DEBUG_MODE": lambda d: getattr(dut, f"io_triggered_{i}").value == 1,
            },
            name=f"PC{i}_TRIGGERED",
        )

    # Reverse mark function coverage to the check point
    # BUG: 加不加 mark_function 对最后的 funcov 都没有影响
    for i in range(16):
        g.mark_function(
            f"PC{i}_TRIGGERED",
            func=[
                module_name_with("test_match_eq", "./test_normal_match"),
                module_name_with("test_match_ge", "./test_normal_match"),
                module_name_with("test_match_lt", "./test_normal_match"),
            ],
            bin_name=["BKPT_EXCPT", "DEBUG_MODE"],
        )


@toffee_test.fixture
async def frontend_trigger_env(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.INFO, log_file="toffee.log")
    dut = toffee_request.create_dut(DUTFrontendTrigger)
    # toffee_request.add_cov_groups(pred_checker_cover_point(dut))
    dut.InitClock("clock")
    toffee.start_clock(dut)

    init_frontend_trigger_funcov(dut, gr)
    toffee_request.add_cov_groups([gr])

    env = FrontendTriggerEnv(dut)
    env.attach(BpRefModel())

    # await env.agent.reset()
    yield env
    import asyncio

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
