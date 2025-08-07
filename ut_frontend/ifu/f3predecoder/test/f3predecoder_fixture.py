import toffee_test
from dut.F3Predecoder import DUTF3Predecoder
from toffee import start_clock
from ..env import F3PreDecoderEnv
import toffee.funcov as fc
from comm import UT_FCOV, module_name_with

grp = fc.CovGroup(UT_FCOV("../../CLASSIC"))
def init_cov(dut:DUTF3Predecoder, grp: fc.CovGroup):
    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is not cfi": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_brType"
                ).value
                == 0,
                "instr is branch": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_brType"
                ).value
                == 1,
                "instr is jal": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_brType"
                ).value
                == 2,
                "instr is jalr": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_brType"
                ).value
                == 3,
            },
            name=f"check_cfi_{i}",
        )

    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is RVI.JAL and is call": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isCall"
                ).value
                == 1
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b1101111,
                "instr is RVI.JAL and is not call or ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isCall"
                ).value
                == 0
                and getattr(x, f"io_out_pd_{current_i}_isRet").value == 0
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b1101111,
                "instr is RVC.JAL and is not call or ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isCall"
                ).value
                == 0
                and getattr(x, f"io_out_pd_{current_i}_isRet").value == 0
                and getattr(x, f"io_in_instr_{current_i}").value & 0b11 == 0b01
                and (getattr(x, f"io_in_instr_{current_i}").value >> 13) == 0b101,
            },
            name=f"check_jal_{i}",
        )

    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is RVI.JALR and is call": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isCall"
                ).value
                == 1
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b1100111,
                "instr is RVI.JALR and is ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isRet"
                ).value
                == 1
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b1100111,
                "instr is RVI.JALR and is not call or ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isRet"
                ).value
                == 0
                and getattr(x, f"io_out_pd_{current_i}_isCall").value == 0
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b1100111,
                "instr is RVC.JALR and is not call or ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isRet"
                ).value
                == 0
                and getattr(x, f"io_out_pd_{current_i}_isCall").value == 0
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b0000010
                and (getattr(x, f"io_in_instr_{current_i}").value >> 12) == 0b1001,
            },
            name=f"check_jalr_{i}",
        )

    for i in range(16):
        grp.add_cover_point(
            dut,
            {
                "instr is RVC.JR and is ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{i}_isRet"
                ).value
                == 1
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b0000010
                and (getattr(x, f"io_in_instr_{current_i}").value >> 12) == 0b1000,
                "instr is RVC.JR and is not call or ret": lambda x, current_i=i: getattr(
                    x, f"io_out_pd_{current_i}_isRet"
                ).value
                == 0
                and getattr(x, f"io_out_pd_{current_i}_isCall").value == 0
                and getattr(x, f"io_in_instr_{current_i}").value & 0b1111111
                == 0b0000010
                and (getattr(x, f"io_in_instr_{current_i}").value >> 12) == 0b1000,
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
