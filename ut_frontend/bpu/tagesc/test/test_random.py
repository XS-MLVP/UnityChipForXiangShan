import random

import toffee
import toffee_test

from dut.tage_sc.UT_Tage_SC import DUTTage_SC
from .checkpoints_sc_predict import get_coverage_group_of_sc_predict
from .checkpoints_tage_predict import get_coverage_group_of_tage_predict
from .checkpoints_tage_train import get_coverage_group_of_tage_train
from ..env.fake_global_history import TageSCFakeGlobalHistory
from ..env.tage_sc_env import TageSCEnv


@toffee_test.testcase
async def test_random(tage_sc_env: TageSCEnv):
    random.seed(0x1145141)
    fgh = TageSCFakeGlobalHistory()
    env = tage_sc_env
    await env.reset_dut()
    for _ in range(20000):
        taken = (random.randint(0, 1), random.randint(0, 1)) if _ > 0 else (0, 0)
        pc = 0x80000003 + random.randint(0, 3)
        async with toffee.Executor() as _exec:
            _exec(env.ctrl_agent.exec_activate())
            _exec(env.predict_agent.exec_predict(pc, fgh.value))

        io_out = env.predict_agent.io_out
        miss = io_out.s3.br_taken_mask_0.value != taken[0], io_out.s3.br_taken_mask_1.value != taken[1]
        await env.train_agent.exec_update(pc, 1, 1, 1, io_out.last_stage_meta.value, fgh.value, *taken, *miss, 0, 0)
        for t in taken:
            fgh.update(t > 0)


@toffee_test.fixture
async def tage_sc_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTTage_SC, "clock")
    toffee_request.add_cov_groups([
        get_coverage_group_of_tage_predict(dut),
        get_coverage_group_of_tage_train(dut),
        get_coverage_group_of_sc_predict(dut),
    ])
    toffee.start_clock(dut)
    return TageSCEnv(dut)
