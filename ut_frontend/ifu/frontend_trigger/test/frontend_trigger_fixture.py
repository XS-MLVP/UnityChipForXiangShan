import toffee
import toffee.funcov as fc
import toffee_test

from comm.functions import UT_FCOV
from dut.FrontendTrigger import DUTFrontendTrigger
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_ref import BpRefModel
from ut_frontend.ifu.frontend_trigger.test.frontend_trigger_tools import get_mask_one
from ..env import FrontendTriggerEnv

gr = fc.CovGroup(UT_FCOV("../../TOFFEE"), disable_sample_when_point_hinted=False)


def init_frontend_trigger_funcov(dut: DUTFrontendTrigger, g: fc.CovGroup):
    """Add watch points to the RVCExpander module to collect function coverage information"""

    # Helper function factories to replace lambdas
    def create_trigger_checker(index, expected_value):
        def checker(d):
            return getattr(d, f"io_triggered_{index}").value == expected_value

        return checker

    def create_matchtype_checker(index, expected_value):
        def checker(d):
            return getattr(d, f"FrontendTrigger_tdataVec_{index}_matchType").value == expected_value

        return checker

    def create_select_checker(index, expected_value):
        def checker(d):
            return getattr(d, f"FrontendTrigger_tdataVec_{index}_select").value == expected_value

        return checker

    def create_action_checker(index, expected_value):
        def checker(d):
            return getattr(d, f"FrontendTrigger_tdataVec_{index}_action").value == expected_value

        return checker

    def create_chain_checker(index, expected_value):
        def checker(d):
            return getattr(d, f"FrontendTrigger_tdataVec_{index}_chain").value == expected_value

        return checker

    def create_tdata2_range_checker(index, min_val, max_val):
        def checker(d):
            val = getattr(d, f"FrontendTrigger_tdataVec_{index}_tdata2").value
            return val >= min_val and val < max_val

        return checker

    # 断点触发情况
    for i in range(16):
        g.add_watch_point(
            dut,
            {
                "BKPT_EXCPT": create_trigger_checker(i, 0),
                "DEBUG_MODE": create_trigger_checker(i, 1),
            },
            name=f"PC{i}_TRIGGERED",
        )

    # 断点设置情况 matchType
    for i in range(4):
        g.add_watch_point(
            dut,
            {
                "EQ": create_matchtype_checker(i, 0),
                "GE": create_matchtype_checker(i, 2),
                "LT": create_matchtype_checker(i, 3),
            },
            name=f"TRI{i}_MATCH_TYPE",
        )
    # 断点设置情况 select
    for i in range(4):
        g.add_watch_point(
            dut,
            {
                "SELECT_0": create_select_checker(i, 0),
                "SELECT_1": create_select_checker(i, 1),
            },
            name=f"TRI{i}_SELECT",
        )
    # 断点设置情况 action
    for i in range(4):
        g.add_watch_point(
            dut,
            {
                "ACTION_0": create_action_checker(i, 0),
                "ACTION_1": create_action_checker(i, 1),
            },
            name=f"TRI{i}_ACTION",
        )
    # 断点设置情况 chain
    for i in range(4):
        g.add_watch_point(
            dut,
            {
                "CHAIN_0": create_chain_checker(i, 0),
                "CHAIN_1": create_chain_checker(i, 1),
            },
            name=f"TRI{i}_CHAIN",
        )
    # 断点设置情况 tdata2

    tdata2_range_list = []
    step = get_mask_one(50) // 1024  # 区间过大速度就慢
    for pc_range in range(0, get_mask_one(50), step):
        tdata2_range_list.append(
            (
                "tdata2_0x{:x}".format(pc_range),
                pc_range,
                pc_range + step,
            )
        )

    for i in range(4):
        cur_lambda_dict = {}
        for tdata2_range in tdata2_range_list:
            cur_lambda_dict[tdata2_range[0]] = create_tdata2_range_checker(
                i, tdata2_range[1], tdata2_range[2]
            )
        g.add_watch_point(
            dut,
            cur_lambda_dict,
            name=f"TRI{i}_tdata2",
        )

    # # Reverse mark function coverage to the check point
    # for i in range(16):
    #     g.mark_function(
    #         f"PC{i}_TRIGGERED",
    #         func=[
    #             module_name_with("test_match_eq", "./test_normal_match"),
    #             module_name_with("test_match_ge", "./test_normal_match"),
    #             module_name_with("test_match_lt", "./test_normal_match"),
    #         ],
    #         bin_name=["BKPT_EXCPT", "DEBUG_MODE"],
    #     )


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
