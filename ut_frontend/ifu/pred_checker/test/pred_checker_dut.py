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
            "JAL_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "JAL_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            f"JAL_INSTR_VALID_{j}": lambda dut, j=j: getattr(dut, f"io_in_instrValid_{j}").value == 1,
            f"JAL_INSTR_RANGE_{j+1}": lambda dut, j=j: sum(getattr(dut, f"io_in_instrRange_{i}").value for i in range(PREDICT_WIDTH)) == j+1,
            f"JAL_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
            f"JAL_PDS_INFO_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_pds_{j}_brType").value == 2
        }, name=f"JAL_PRED_COV_{j}")
    
    # For function point 2 - RET prediction error checking:
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut, {
            "RET_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "RET_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            f"RET_INSTR_VALID_{j}": lambda dut, j=j: getattr(dut, f"io_in_instrValid_{j}").value == 1,
            f"RET_INSTR_RANGE_{j+1}": lambda dut, j=j: sum(getattr(dut, f"io_in_instrRange_{i}").value for i in range(PREDICT_WIDTH)) == j+1,
            f"RET_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
            f"RET_PDS_INFO_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_pds_{j}_brType").value == 3
        }, name=f"RET_PRED_COV_{j}")
    
    # For function point 3 - JALR prediction error checking:
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut, {
            "JALR_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "JALR_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            f"JALR_INSTR_VALID_{j}": lambda dut, j=j: getattr(dut, f"io_in_instrValid_{j}").value == 1,
            f"JALR_INSTR_RANGE_{j+1}": lambda dut, j=j: sum(getattr(dut, f"io_in_instrRange_{i}").value for i in range(PREDICT_WIDTH)) == j+1,
            f"JALR_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
            f"JALR_PDS_INFO_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_pds_{j}_brType").value == 3
        }, name=f"JALR_PRED_COV_{j}")
        
    # For function point 4 - Renewing instruction range:
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut, {
            f"RANGE_LENGTH_{j+1}_COV": lambda dut, j=j: sum(1 for i in range(PREDICT_WIDTH) if getattr(dut, f"io_in_instrRange_{i}").value == 1) == j+1
        }, name=f"RANGE_FIXING_COV_{j}")
    
    # For function point 5 - Not-CFI instruction checking
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut,{
            "CFI_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "CFI_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            f"CFI_INSTR_VALID_{j}": lambda dut, j=j: getattr(dut, f"io_in_instrValid_{j}").value == 1,
            f"CFI_INSTR_RANGE_{j+1}": lambda dut, j=j: sum(getattr(dut, f"io_in_instrRange_{i}").value for i in range(PREDICT_WIDTH)) == j+1,
            f"CFI_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
            f"CFI_PDS_INFO_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_pds_{j}_brType").value  > 0
        }, name=f"CFI_PRED_COV_{j}")
    
    # For function point 6 - Invalid instruction checking
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut,{
            "INV_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "INV_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            f"INV_INSTR_OFFSET_{j}": lambda dut, j=j: getattr(dut, f"io_in_instrValid_{j}").value == 0,
            f"INV_INSTR_RANGE_{j+1}": lambda dut, j=j: sum(getattr(dut, f"io_in_instrRange_{i}").value for i in range(PREDICT_WIDTH)) == j+1,
            f"INV_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
        }, name=f"INV_PRED_COV_{j}")
    
    # For function point 7 - Target error checking
    for j in range(PREDICT_WIDTH):
        g.add_watch_point(dut,
            {
            "TGT_CFI_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "TGT_CFI_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            "TGT_CFI_INSTR_VALID": lambda dut: getattr(dut, f"io_in_instrValid_{j}").value == 1,
            f"TGT_CFI_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
            f"TGT_CFI_PDS_INFO_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_pds_{j}_brType").value  > 0,
            f"TGT_CFI_JMPOFFSET_VAL_{j}": lambda dut, j=j: getattr(dut, f"io_in_jumpOffset_{j}").value > 0,
            f"TGT_CFI_TGT_VAL": lambda dut: getattr(dut, "io_in_target").value > 0,
            f"TGT_CFI_PC_VAL_{j}": lambda dut, j=j: getattr(dut, f"io_in_pc_{j}").value > 2**50 - 2**6 - 4
            },
            name=f"TGT_ERROR_COV_{j}",
        )
    
    # For function point 8 - Random target checking
    for i in range(PREDICT_WIDTH):
        g.add_watch_point(dut,{
            "RAND_PRED_VALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 1,
            "RAND_PRED_INVALID": lambda dut: getattr(dut, "io_in_ftqOffset_valid").value == 0,
            "RAND_INSTR_VALID": lambda dut, j=j: getattr(dut, f"io_in_instrValid_{j}").value == 1,
            "RAND_INSTR_RANGE": lambda dut, j=j: sum(getattr(dut, f"io_in_instrRange_{i}").value for i in range(PREDICT_WIDTH)) == j+1,
            f"RAND_PRED_OFFSET_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_ftqOffset_bits").value == j,
            f"RAND_PDS_INFO_AT_{j}": lambda dut, j=j: getattr(dut, f"io_in_pds_{j}_brType").value  > 0,
            f"RAND_JMPOFFSET_VAL_{j}": lambda dut, j=j: getattr(dut, f"io_in_jumpOffset_{j}").value > 0,
            f"RAND_TGT_VAL": lambda dut: getattr(dut, "io_in_target").value > 0,
            f"RAND_PC_VAL_{j}": lambda dut, j=j: getattr(dut, f"io_in_pc_{j}").value > 2**50 - 2**6 - 4
        },
        name=f"TARGET_{i}_COV")
    
    # Reverse mark
    def _mark_name(name):
        return module_name_with(name, "../../test_predchecker")
    
    
    for i in range(PREDICT_WIDTH):
        g.mark_function(f"JAL_PRED_COV_{i}", _mark_name(["test_jal_chk_1_1_1", "test_jal_chk_1_1_2", "test_jal_chk_1_2_1", "test_jal_chk_1_2_2"]))
        g.mark_function(f"RET_PRED_COV_{i}", _mark_name(["test_ret_chk_2_1_1", "test_ret_chk_2_1_2", "test_ret_chk_2_2_1", "test_ret_chk_2_2_2"]))
        g.mark_function(f"JALR_PRED_COV_{i}", _mark_name(["test_jalr_chk_3_1_1", "test_jalr_chk_3_1_2", "test_jalr_chk_3_2_1", "test_jalr_chk_3_2_2"]))
        g.mark_function(f"RANGE_FIXING_COV_{i}", _mark_name(["test_renew_range_4_1", "test_renew_range_4_2", "test_renew_range_4_3"]))
        g.mark_function(f"CFI_PRED_COV_{i}", _mark_name(["test_not_cfi_chk_5_1_1", "test_not_cfi_chk_5_1_2", "test_not_cfi_chk_5_2"]))
        g.mark_function(f"INV_PRED_COV_{i}", _mark_name(["test_invalid_instr_chk_6_1_1","test_invalid_instr_chk_6_1_2", "test_invalid_instr_chk_6_1_3", "test_invalid_instr_chk_6_2" ]))
        g.mark_function(f"TGT_ERROR_COV_{i}", _mark_name(["test_tgt_chk_7_1_1", "test_tgt_chk_7_1_2", "test_tgt_chk_7_2"]))
        g.mark_function(f"TARGET_{i}_COV", _mark_name("test_rand_tgt_8")) 
    
    return g

@toffee_test.fixture
async def predchecker_env(toffee_request: toffee_test.ToffeeRequest):
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



            