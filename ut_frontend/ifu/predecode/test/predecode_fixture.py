import toffee_test
from dut.PreDecode import DUTPreDecode
from ..env import PreDecodeEnv
from toffee import start_clock
import toffee.funcov as fc
from comm import UT_FCOV, module_name_with

grp = fc.CovGroup(UT_FCOV("../../CLASSIC"))


def check_isRVC(index: int, expected_value: int):
    def checker(x):
        attr_name = f"io_out_pd_{index}_isRVC"
        return getattr(x, attr_name).value == expected_value

    return checker


def check_hasHalfValid(index: int, expected_value: int):
    def checker(x):
        attr_name = f"io_out_hasHalfValid_{index}"
        return getattr(x, attr_name).value == expected_value

    return checker


def check_pdValid(index: int, expected_value: int):
    def checker(x):
        attr_name = f"io_out_pd_{index}_valid"
        return getattr(x, attr_name).value == expected_value

    return checker


def init_cov(dut:DUTPreDecode, grp: fc.CovGroup):
    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is rvc:": check_isRVC(i, 1),
                "instr is rvi:": check_isRVC(i, 0),
            },
            name=f"check_rvc_rvi_{i}",
        )

    for i in range(2,16):
        grp.add_cover_point(
            dut,
            {
                "instr is half_valid_start:": check_hasHalfValid(i, 1),
                "instr is not half_valid_start:": check_hasHalfValid(i, 0),
            },
            name=f"check_half_valid_start_{i}",
        )

    for i in range(1,16):
        grp.add_cover_point(
            dut,
            {
                "instr is valid_starts:": check_pdValid(i, 1),
                "instr is not valid_starts:": check_pdValid(i, 0),
            },
            name=f"check_valid_start_{i}",
        )

    def _mark(name):
        return module_name_with(name, "../predecode_test")

    for i in range(16):
        grp.mark_function(f'check_rvc_rvi_{i}',_mark(["test_rvc_rvi_checker_2_1_2","test_rvc_rvi_checker_2_1_1"]))
    for i in range(2,16):
        grp.mark_function(f'check_half_valid_start_{i}',_mark(["test_precoding_checker_2_3_2"]))
    for i in range(1,16):
        grp.mark_function(f'check_valid_start_{i}',_mark(["test_precoding_checker_2_3_1"]))

    return grp


@toffee_test.fixture
async def predecode_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTPreDecode)
    toffee_request.add_cov_groups(init_cov(dut, grp))
    start_clock(dut)
    predecode_env = PreDecodeEnv(dut)
    yield predecode_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
