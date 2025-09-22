import toffee_test
from dut.F3Predecoder import DUTF3Predecoder
from toffee import start_clock
from ..env import F3PreDecoderEnv
import toffee.funcov as fc
from comm import UT_FCOV, module_name_with


grp = fc.CovGroup(UT_FCOV("../../CLASSIC"))


def check_function(
    attr_name: str, expected_value: int, mask: int = 0xFFFFFFFF, shift: int = 0
):
    def checker(x):
        return ((getattr(x, attr_name).value & mask) >> shift) == expected_value

    return checker


def init_cov(dut:DUTF3Predecoder, grp: fc.CovGroup):
    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is not cfi": check_function(f"io_out_pd_{i}_brType", 0),
                "instr is branch": check_function(f"io_out_pd_{i}_brType", 1),
                "instr is jal": check_function(f"io_out_pd_{i}_brType", 2),
                "instr is jalr": check_function(f"io_out_pd_{i}_brType", 3),
            },
            name=f"check_cfi_{i}",
        )
    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is RVI.JAL and is call": check_function(
                    f"io_out_pd_{i}_isCall", 1
                )
                and check_function(f"io_in_instr_{i}", 0b1101111, mask=0b1111111),
                "instr is RVI.JAL and is not call or ret": check_function(
                    f"io_out_pd_{i}_isCall", 0
                )
                and check_function(f"io_out_pd_{i}_isRet", 0)
                and check_function(f"io_in_instr_{i}", 0b1101111, mask=0b1111111),
                "instr is RVC.JAL and is not call or ret": check_function(
                    f"io_out_pd_{i}_isCall", 0
                )
                and check_function(f"io_out_pd_{i}_isRet", 0)
                and check_function(f"io_in_instr_{i}", 0b01, mask=0b11)
                and check_function(f"io_in_instr_{i}", 0b101, shift=13),
            },
            name=f"check_jal_{i}",
        )

    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is RVI.JALR and is call": check_function(
                    f"io_out_pd_{i}_isCall", 1
                )
                and check_function(f"io_in_instr_{i}",0b1100111,mask = 0b1111111),
                "instr is RVI.JALR and is ret": check_function(
                    f"io_out_pd_{i}_isRet", 1
                )
                and check_function(f"io_in_instr_{i}", 0b1100111, mask=0b1111111),
                "instr is RVI.JALR and is not call or ret": check_function(
                    f"io_out_pd_{i}_isRet", 0
                )
                and check_function(f"io_out_pd_{i}_isCall", 0)
                and check_function(f"io_in_instr_{i}", 0b1100111, mask=0b1111111),
                "instr is RVC.JALR and is not call or ret": check_function(
                    f"io_out_pd_{i}_isRet", 0
                )
                and check_function(f"io_out_pd_{i}_isCall", 0)
                and check_function(f"io_in_instr_{i}", 0b0000010, mask=0b1111111)
                and check_function(f"io_in_instr_{i}", 0b1001, shift=12),
            },
            name=f"check_jalr_{i}",
        )

    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is RVC.JR and is ret": check_function(f"io_out_pd_{i}_isRet", 1)
                and check_function(f"io_in_instr_{i}",0b0000010,mask = 0b1111111)
                and check_function(f"io_in_instr_{i}",0b1000,shift= 12),
                "instr is RVC.JR and is not call or ret": check_function(
                    f"io_out_pd_{i}_isRet", 0
                )
                and check_function(f"io_out_pd_{i}_isCall", 0)
                and check_function(f"io_in_instr_{i}",0b0000010,mask = 0b1111111)
                and check_function(f"io_in_instr_{i}",0b1000,shift=12),
            },
            name=f"check_jr_{i}",
        )

    def _mark(name):
        return module_name_with(name, "../f3predecoder_test")

    for i in range(16):
        grp.mark_function(f'check_cfi_{i}',_mark(["test_cfi_checker_1_1","test_cfi_checker_1_2","test_cfi_checker_1_3"]))
        grp.mark_function(f'check_jal_{i}',_mark(["test_cfi_checker_2_2_1_1","test_cfi_checker_2_2_1_2","test_cfi_checker_2_2_2"]))
        grp.mark_function(f'check_jalr_{i}',_mark(["test_cfi_checker_2_3_2_1","test_cfi_checker_2_3_1_2","test_cfi_checker_2_3_1_3","test_cfi_checker_2_3_2_1"]))
        grp.mark_function(f'check_jr_{i}',_mark(["test_cfi_checker_2_3_2_2_1","test_cfi_checker_2_3_2_2_2"]))
    return grp


@toffee_test.fixture
async def f3predecoder_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTF3Predecoder)
    toffee_request.add_cov_groups(init_cov(dut, grp))
    start_clock(dut)
    predecode_env = F3PreDecoderEnv(dut)
    yield predecode_env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
