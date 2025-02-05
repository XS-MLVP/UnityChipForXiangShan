import os
import random

import pytest
import toffee
import toffee_test

from dut.Tage_SC import DUTTage_SC
from .checkpoints_sc_predict import get_coverage_group_of_sc_predict
from .checkpoints_tage_predict import get_coverage_group_of_tage_predict
from .checkpoints_tage_train import get_coverage_group_of_tage_train
from ..bundle.internal import StatusBundle
from ..env.fake_global_history import TageSCFakeGlobalHistory
from ..env.tage_sc_env import TageSCEnv


@pytest.mark.parametrize("pc_bound", list(range(8)))
@toffee_test.testcase
async def test_random(tage_sc_env: TageSCEnv, pc_bound: int):
    random.seed(os.urandom(128))
    fgh = TageSCFakeGlobalHistory()
    env = tage_sc_env
    await env.reset_dut()
    for _ in range(3500):
        taken = (random.randint(0, 1), random.randint(0, 1)) if _ > 0 else (0, 0)
        pc = 0x80000003 + random.randint(0, pc_bound)
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
    import asyncio
    dut = toffee_request.create_dut(DUTTage_SC, "clock")
    status = StatusBundle.from_prefix("").bind(dut)
    toffee_request.add_cov_groups([
        get_coverage_group_of_tage_predict(status),
        get_coverage_group_of_tage_train(status),
        get_coverage_group_of_sc_predict(status),
    ])
    toffee.start_clock(dut)
    yield TageSCEnv(dut)

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
