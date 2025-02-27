import toffee_test
import toffee
from operator import *
from ..env import PredCheckerEnv
from dut.PredChecker import DUTPredChecker
import toffee.funcov as fc
from toffee.funcov import CovGroup
from comm.functions import UT_FCOV, module_name_with
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL

# moudle path is ut_frontend.ifu.pred_checker.test.pred_checker_dut
gr = fc.CovGroup(UT_FCOV("../../../pred_checker"))

def init_pred_checker_funcov(dut:DUTPredChecker, g:fc.CovGroup, env:PredCheckerEnv):
    mdl = env.mdl
    # For function point 1 - JAL prediction error checking:
    # NO_JAL_FALSE_REPORT - 误检检查: False detection test
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut, {
            "NO_JAL_FALSE_REPORT": lambda dut: all(getattr(dut, f"io_out_stage2Out_fixedMissPred_{i}").value == False for i in range(PREDICT_WIDTH)),
            f"JAL_FAL_PRED_AT_{j}": lambda dut: getattr(dut, f"io_out_stage2Out_fixedMissPred_{j}").value == 1
        }, name=f"JAL_PRED_COV_{j}")
    
    # For function point 2 - RET prediction error checking:
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut, {
            "NO_RET_FALSE_REPORT": lambda dut: all(getattr(dut, f"io_out_stage2Out_fixedMissPred_{i}").value == False for i in range(PREDICT_WIDTH)),
            f"RET_FAL_PRED_AT_{j}": lambda dut: getattr(dut, f"io_out_stage2Out_fixedMissPred_{j}").value == 1
        }, name=f"RET_PRED_COV_{j}")
    
    # For function point 3 - Renewing instruction range:
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut, {
            f"RANGE_LENGTH_{j}_COV": lambda dut: sum(1 for i in range(PREDICT_WIDTH) if getattr(dut, f"io_out_stage1Out_fixedRange_{i}").value == 1) == j
        }, name=f"RANGE_FIXING_COV_{j}")
    
    # For function point 4 - Not-CFI instruction checking
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut,{
            "NO_CFI_FALSE_REPORT": lambda dut: all(getattr(dut, f"io_out_stage2Out_fixedMissPred_{i}").value == False for i in range(PREDICT_WIDTH)),
            f"CFI_FAL_PRED_AT_{j}": lambda dut: getattr(dut, f"io_out_stage2Out_fixedMissPred_{j}").value == 1
        }, name=f"CFI_PRED_COV_{j}")
    
    # For function point 5 - Invalid instruction checking
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut,{
            "NO_INV_REPORT": lambda dut: all(getattr(dut, f"io_out_stage2Out_fixedMissPred_{i}").value == False for i in range(PREDICT_WIDTH)),
            f"INV_FAL_PRED_AT_{j}": lambda dut: getattr(dut, f"io_out_stage2Out_fixedMissPred_{j}").value == 1
        }, name=f"INV_PRED_COV_{j}")
    
    # For function point 6 - Target error checking
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut,
            {
            "NO_TGT_ERR_REPORT": lambda dut: all(getattr(dut, f"io_out_stage2Out_fixedMissPred_{i}").value == False for i in range(PREDICT_WIDTH)),
            f"TGT_FAL_PRED_AT_{j}": lambda dut: getattr(dut, f"io_out_stage2Out_fixedMissPred_{j}").value == 1
            },
            name=f"TGT_ERROR_COV_{j}",
        )
    
    # For function point 7 - Random target checking
    for i in range(PREDICT_WIDTH):
        g.add_watch_point(dut,{
            f"FIXED_TARGET_{i}_CORRECT": lambda dut: getattr(dut, f"io_out_stage2Out_fixedTarget_{i}").value == mdl.pc[i] + mdl.jumpOffset[i]
                                                    or getattr(dut, f"io_out_stage2Out_fixedTarget_{i}").value == mdl.pc[i] + mdl.jumpOffset[i] - 2**50
                                                    or getattr(dut, f"io_out_stage2Out_fixedTarget_{i}").value == mdl.pc[i] + 2
                                                    or getattr(dut, f"io_out_stage2Out_fixedTarget_{i}").value == mdl.pc[i] + 4,
            f"JAL_TARGET_{i}_CORRECT": lambda dut: getattr(dut, f"io_out_stage2Out_jalTarget_{i}").value == mdl.pc[i] + mdl.jumpOffset[i]
                                                    or getattr(dut, f"io_out_stage2Out_jalTarget_{i}").value == mdl.pc[i] + mdl.jumpOffset[i] - 2**50,
            f"FIXED_TARGET_{i}_BOUNDARY": lambda dut: getattr(dut, f"io_out_stage2Out_fixedTarget_{i}").value > 0x3_FFFF_FFFF_FFC0,
            f"JAL_TARGET_{i}_BOUNDARY": lambda dut: getattr(dut, f"io_out_stage2Out_jalTarget_{i}").value > 0x3_FFFF_FFFF_FFC0
        },
        name=f"TARGET_{i}_COV")
    
    # Reverse mark
    def _mark_name(name):
        return module_name_with(name, "../../test_predchecker")
    
    
    for i in range(PREDICT_WIDTH):
        g.mark_function(f"JAL_PRED_COV_{i}", _mark_name(["test_jal_chk_1_1_1", "test_jal_chk_1_1_2", "test_jal_chk_1_2_1", "test_jal_chk_1_2_2"]))
        g.mark_function(f"RET_PRED_COV_{i}", _mark_name(["test_ret_chk_2_1_1", "test_ret_chk_2_1_2", "test_ret_chk_2_2_1", "test_ret_chk_2_2_2"]))
        g.mark_function(f"RANGE_FIXING_COV_{i}", _mark_name(["test_renew_range_3_1", "test_renew_range_3_2", "test_renew_range_3_3"]))
        g.mark_function(f"CFI_PRED_COV_{i}", _mark_name(["test_not_cfi_chk_4_1_1", "test_not_cfi_chk_4_1_2", "test_not_cfi_chk_4_2"]))
        g.mark_function(f"INV_PRED_COV_{i}", _mark_name(["test_invalid_instr_chk_5_1_1","test_invalid_instr_chk_5_1_2", "test_invalid_instr_chk_5_1_3", "test_invalid_instr_chk_5_2" ]))
        g.mark_function(f"TGT_ERROR_COV_{i}", _mark_name(["test_tgt_chk_6_1_1", "test_tgt_chk_6_1_2", "test_tgt_chk_6_2"]))
        g.mark_function(f"TARGET_{i}_COV", _mark_name("test_rand_tgt_7")) 
    
    return g

@toffee_test.fixture
async def predchecker_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(DUTPredChecker)
    dut.InitClock("clock")
    toffee.start_clock(dut)
    env = PredCheckerEnv(dut)
    toffee_request.add_cov_groups(init_pred_checker_funcov(dut, gr, env))
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



            